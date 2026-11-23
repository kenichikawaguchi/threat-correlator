# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-23 15:00 UTC
- **対象期間**: `2026-11-22T15:00:38.000Z` 〜 `2026-11-23T15:00:20.000Z`
- **重要CVE数**: 70 件（Critical 9.0+: 10 件 / High 7.0〜: 60 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **リモートコード実行 (RCE)・認証回避・デシリアライズ** が共通した攻撃パターンとして目立ちます。  
- IoT ルータや NAS、Web アプリの管理インターフェイスが **認証なしで OS コマンドを実行** できるケースが増加。  
- PHP/WordPress 系プラグインや Python/Node.js のライブラリに **オブジェクトインジェクション／デシリアライズ** の脆弱性が集中。  
- いずれも「外部から直接アクセス可能」なサービスが対象で、攻撃者は **ネットワーク境界だけで侵入** できる点が危険です。  

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲・被害シナリオ | 注目理由 |
|-----|------|----------------|------------------------|----------|
| **CVE‑2026‑134882** | 10.0 | OS コマンドインジェクション (CGI) | TOTOLINK A7100RU 7.4cu ルータの `/cgi-bin/cstecgi.cgi` の `exportOvpn` パラメータで `Username` を操作すると任意コマンド実行。認証不要・リモートから直接攻撃可能。 | **最高スコア 10.0**。IoT ルータは社内外のネットワークに常時接続されているため、侵入後の横展開が容易。 |
| **CVE‑2026‑120382** | 9.8 | コマンドインジェクション／任意ファイル操作 | Synology DiskStation Manager (DSM) の OAuth API で引数区切り文字が正規化されず、リモートから任意ファイルの読み書きやサービス停止が可能。DSM 7.1.1‑42962‑10 以前が対象。 | Synology は企業・個人のデータ保管基盤として広く利用。認証不要でファイル改ざん・情報漏洩が起こり得る。 |
| **CVE‑2026‑131782** | 9.8 | PHP オブジェクトインジェクション (WordPress) | `wordpress-simple-paypal-shopping-cart` (Simple Shopping Cart) のシリアライズデータを改ざんし、任意 PHP オブジェクトを注入。バージョン 5.3.3 までが対象。 | WordPress プラグインは多数のサイトで共通利用。管理者権限取得やマルウェア設置が即座に可能。 |
| **CVE‑2026‑131754** | 9.8 | PHP オブジェクトインジェクション (APCu Manager) | `apcu-manager` のシリアライズデータを操作し、任意コード実行。4.6.1 までが影響。 | APCu は高トラフィックサイトでキャッシュとして必須。攻撃者がサーバ上で永続的にコードを実行できる。 |
| **CVE‑2026‑121613** | 9.3 | 認証・認可欠如 (ファームウェアアップロード) | 特定の管理インターフェイスが認証なしでコマンド送信・ファームウェアアップロードを許可。デバイスの再起動やマルウェア化が可能。 | IoT デバイスの「アップデート機構」が直接攻撃対象になる珍しいケース。 |

> **※** それ以外にも `simple‑git` (9.2) や `binary‑parser` (9.2) など、開発ツールチェーンに潜む RCE が多数報告されています。開発・CI 環境への波及リスクも無視できません。

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ

| 製品 / ライブラリ | 現行脆弱バージョン | 推奨バージョン | 備考 |
|-------------------|-------------------|----------------|------|
| **TOTOLINK A7100RU ルータ** | 7.4cu.2313_B20191024 以前 | 7.4cu.2313_B20231115 以降（メーカー提供の最新ファームウェア） | ファームウェア更新時は **設定バックアップ** と **リセット** を実施。 |
| **Synology DSM** | 7.1.1‑42962‑10、7.2.1‑69057‑14、7.2.2‑72806‑11、7.3.2‑86009‑6、7.4.1‑90080‑2 以前 | 7.4.1‑90080‑2 以降（または最新の 7.5 系） | DSM の **自動更新** を有効化し、**OAuth API の外部公開** をファイアウォールで遮断。 |
| **WordPress Simple Shopping Cart** (`wordpress-simple-paypal-shopping-cart`) | ≤ 5.3.3 | 5.3.4 以上 | プラグイン更新後は **キャッシュクリア** と **不正ファイルのスキャン** を実施。 |
| **APCu Manager** | ≤ 4.6.1 | 4.6.2 以上 | APCu 本体は 5.1.22 以降が推奨。 |
| **simple‑git (Node.js)** | < 4.1.0 | ≥ 4.1.0 | `npm install simple-git@latest` で更新。 |
| **binary‑parser (Node.js)** | < 2.3.1 | ≥ 2.3.1 | 同上。 |
| **Gunicorn** | < 27.0.0 | ≥ 27.0.0 | `pip install --upgrade gunicorn` |
| **Faye / websocket‑driver / websocket‑extensions** | < 0.8.0 / <0.2.0 | 各ライブラリの最新安定版 | 依存関係が多いため、`npm audit fix` で一括更新を推奨。 |
| **msgpackr** | < 2.1.4 | ≥ 2.1.4 | `npm install msgpackr@latest` |
| **Portainer** | 2.39.0‑2.39.8、2.40.0‑2.45.3、3.0.0‑3.0.9 | 2.39.9 以上、2.45.4 以上、3.1.0 以上 | 標準ユーザーの権限設定を見直し、**最小権限の原則** を徹底。 |
| **Kirby** | < 5.6.4 | ≥ 5.6.4 | アップロード機能の **SVG サニ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-134882

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-23T09:17:05.653 |

A weakness has been identified in TOTOLINK A7100RU 7.4cu.2313_B20191024. This issue affects the function exportOvpn of the file /cgi-bin/cstecgi.cgi of the component CGI Handler. This manipulation of the argument Username causes os command injection. The attack is possible to be carried out remotely.

### CVE-2026-120382

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-23T08:17:14.183 |

An improper neutralization of argument delimiters in a command vulnerability in the OAuth API in Synology DiskStation Manager (DSM) before 7.1.1-42962-10, 7.2.1-69057-14, 7.2.2-72806-11, 7.3.2-86009-6, and 7.4.1-90080-2 allows remote attackers to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-131782

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-22T15:17:12.543 |

Deserialization of Untrusted Data vulnerability in mra13 / Team Tips and Tricks HQ Simple Shopping Cart wordpress-simple-paypal-shopping-cart allows Object Injection.This issue affects Simple Shopping Cart: from n/a through 5.3.3.

### CVE-2026-131754

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-22T15:17:12.247 |

Deserialization of Untrusted Data vulnerability in Pierre Lannoy APCu Manager apcu-manager allows Object Injection.This issue affects APCu Manager: from n/a through 4.6.1.

### CVE-2026-121613

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-23T10:17:15.397 |

Missing authentication and authorization on an exposed interface allows an unauthenticated remote attacker to send arbitrary commands to the affected component, which can force a device reboot or let the attacker upload malicious firmware.

### CVE-2026-115899

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-23T09:17:05.010 |

An attacker must control pagination data returned by an upstream API or service queried by an existing REST Collector. The Collector must use affected response-based pagination and process the crafted data during a job run. Successful exploitation executes code with the Worker service account's permissions.

### CVE-2026-134624

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-22T19:16:32.163 |

N-able MailAssure (SpamExperts) before 20261121.1943 does not restrict the destination of the LDAP synchronisation connection check performed when a relay is configured. An authenticated API user can cause the server to connect to arbitrary internal hosts and ports, determine which are reachable, and send crafted data to internal services.

### CVE-2026-134815

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-22T22:17:35.807 |

simple-git before 4.1.0 contains an argument injection vulnerability that allows attackers to bypass the allowUnsafePack guard by supplying the --exec option to non-push git operations. Attackers who influence arguments passed to listRemote() or raw() can inject --exec for ls-remote, archive, fetch-pack or send-pack to execute commands on the host.

### CVE-2026-134814

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-22T22:17:35.660 |

binary-parser before 2.3.1 contains a code injection vulnerability that allows attackers controlling parser definitions to inject JavaScript through string-typed options passed unvalidated by Context.generateOption(). Attackers can supply crafted length, lengthInBytes, key, tag, offset, or namely() alias values to execute arbitrary JavaScript in the Node.js process when the parser is compiled.

### CVE-2026-134838

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-11-22T22:17:39.607 |

Weblate before 2026.11 contains an account takeover vulnerability in the reset_password view that allows unauthenticated attackers to reset victim passwords by abusing case-insensitive Unicode e-mail matching. Attackers controlling a lookalike mailbox using a dotless i or other case-folding variant receive the victim's reset link, since it is sent to the typed address, and set a new password.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-93585

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-23T14:17:27.077 |

An improper authorization vulnerability in the EV Reach Client Agent allows authenticated users with low privileges to execute arbitrary commands on a remote Windows endpoint with LocalSystem privileges. The affected agent service does not sufficiently enforce authorization restrictions for certain privileged remote management operations. Under specific conditions, the agent fails to apply the intended user impersonation mechanism and executes user-supplied commands within the security context of the agent service, which runs as NT AUTHORITY\SYSTEM.

As a result, an authenticated attacker may bypass the intended privilege restrictions and execute arbitrary commands with the highest user-mode privileges on an affected Windows system. Successful exploitation may lead to complete compromise of the affected endpoint, including unauthorized access to sensitive information, modification of system configurations, installation of malicious software, or disruption of system availability. 

The vulnerability does not require administrative credentials or user interaction after successful authentication.

### CVE-2026-86312

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441;CWE-749` |
| Published | 2026-11-23T13:17:06.350 |

Under some configurations a request to the ping endpoint could carry out more than a simple health check. In deployments that rely on Solr's rule-based authorization, a client granted only the low-privilege health permission could thereby trigger behavior that should require higher privileges; where the shipped security.json template leaves the health permission unauthenticated, no credentials are required at all. 


This issue affects Apache Solr from 9.0.0 through the releases preceding the fixed versions. Users are recommended to upgrade to version 9.11.0 or 10.1.0, which resolve the issue.




You are affected if you run an affected version and allow the /admin/ping endpoint to be reached with only the health permission. This includes the default sample security configuration installed by the bin/solr CLI, where that endpoint is unauthenticated.

Users who cannot upgrade immediately should restrict access to the /admin/ping endpoint in their authorization configuration — for example by requiring a trusted role for that path — and ensure Solr is not reachable from untrusted clients or networks, as recommended for all Solr deployments.

### CVE-2026-123886

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-23T11:16:58.460 |

Spring Data Elasticsearch replaces positional placeholders in string-based @Query methods with the method arguments before it evaluates SpEL expressions in the resulting query string.



As a result, an argument that contains a SpEL expression is evaluated as part of the query, even if the declared query does not use SpEL.



 An application is affected if it passes untrusted input as an argument to a repository query method that declares a @Query with positional placeholders.



In that case, a remote attacker can execute arbitrary code in the application, and repeated requests can exhaust memory through the unbounded expression cache.

### CVE-2026-133646

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-23T11:16:59.203 |

Synchronet BBS, in versions 3.20b to 3.21e, contains an out-of-bounds write vulnerability in the answer() function when processing the terminal attribute of the SSH service. The call to cryptGetAttributeString() does not limit the copy to the size of the destination buffer, of which 41 bytes are used. An unauthenticated remote client can send a TERM value of up to 64 bytes and overwrite adjacent fields of the session object. If the SSH service is enabled, this tampering can cause connection threads to be blocked for an extended period, even after the client has disconnected. By exhausting the available sockets, the attacker can prevent new connections and cause a denial of service requiring the software to be restarted.

### CVE-2026-80466

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-23T10:17:16.393 |

A vulnerability in the Web-Based Management (WBM) routing configuration allows a low-privileged remote attacker to inject shell commands into routing parameters. Due to insufficient input validation, these values are stored in a configuration file and later processed by a privileged root helper script.

### CVE-2026-115900

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-11-23T09:17:05.157 |

An attacker must possess a valid Worker distribution credential, reach the Leader distribution listener, and send crafted authenticated Worker heartbeats. Where mTLS client authentication is enforced, an accepted client certificate and its private key are also required. Successful exploitation bypasses Leader REST authentication and permits administrative API access.

### CVE-2026-115873

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-23T09:17:04.820 |

A remote attacker must authenticate with Read Only (GroupRead) access to at least one Worker Group and reach the Leader API. A crafted expression can exploit the nested compiler to bypass expression restrictions and execute code with the Leader service account's permissions.

### CVE-2026-134830

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-11-22T22:17:38.227 |

Casdoor before 4.27.1 contains an uncontrolled resource consumption vulnerability in decodeSamlMessage that allows unauthenticated attackers to exhaust memory by sending unbounded DEFLATE-compressed SAML messages. Attackers can send a small, highly compressed SAMLRequest or SAMLResponse to the /api/saml/logout/:owner/:application endpoint, which inflates to gigabytes and crashes or stalls the server.

### CVE-2026-134821

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-22T22:17:36.770 |

Gunicorn 25.2.0 before 27.0.0 contains a memory exhaustion vulnerability in the pure-Python ASGI HTTP/1 parser that buffers protocol lines without size limits. Unauthenticated remote attackers can send request lines, headers, chunk-size lines or trailers lacking CRLF to grow worker memory and consume CPU, causing denial of service.

### CVE-2026-134813

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-11-22T22:17:35.497 |

Faye websocket-driver 0.5.0 before 0.8.0, permessage-deflate before 0.2.0, and websocket-extensions before 0.2.0 contain a decompression bomb vulnerability because messages are fully inflated before maxLength is enforced. Unauthenticated remote clients negotiating permessage-deflate can send highly compressible messages, forcing processIncomingMessage() to allocate excessive memory and crash the server process.

### CVE-2026-134812

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-22T22:17:35.343 |

msgpackr before 2.1.4 contains an inefficient algorithmic complexity vulnerability that allows remote attackers to cause denial of service by repeatedly re-decoding buffered incomplete values. Attackers can stream a large container of small elements in small chunks to UnpackrStream or decodeIter, triggering quadratic decoding cost that blocks the Node.js event loop.

### CVE-2026-134804

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-22T22:17:34.037 |

Portainer 2.39.0 before 2.39.9, 2.40.0 before 2.45.4, and 3.0.0 before 3.1.0 contains an authorization bypass vulnerability that allows Standard users to access other users' containers via the WebSocket attach and exec endpoints. Attackers with shared environment access can use leaked container or exec IDs to hijack sessions over /api/websocket/attach or /api/websocket/exec, gaining interactive root shells.

### CVE-2026-134765

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-22T22:17:31.983 |

Kirby 5.0.0 before 5.6.4 contains a race condition in Kirby\Api\Upload::processChunk() that allows authenticated users with upload permission to bypass SVG sanitization. Attackers can race concurrent chunked uploads sharing a filename to swap a benign SVG with a script-bearing SVG, executing stored cross-site scripting in the site origin.

### CVE-2026-93584

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-23T09:17:08.873 |

An SQL injection vulnerability in OTRS versions 2024.3.1 through 2026.8.1 allows unauthenticated remote attackers to inject arbitrary SQL expressions through the Survey endpoint.

The vulnerability exists in the Kernel::System::Survey::Request::RequestGet() method, which directly incorporates an attacker-controlled survey key into a SQL query without using parameterized statements. Successful exploitation allows attackers to retrieve ticket information and perform boolean-based or time-based blind SQL injection to extract potentially sensitive data accessible to the OTRS database account. Exploitation does not require authentication, a valid survey key, or an existing survey request. The external frontend must be accessible.

### CVE-2026-134836

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-22T22:17:39.237 |

Dashy 4.0.0 before 4.9.12 contains a credential disclosure vulnerability in isLocalRequest that attaches user credentials to lookalike hosts due to prefix-only origin checks. Attackers can lure logged-in users to a crafted ?config= link pointing to a lookalike host, capturing bearer tokens or HTTP auth headers to read configuration and stored API keys, or modify them when the victim is an admin.

### CVE-2026-131750

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-22T16:16:40.857 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Everest Forms Everest Forms everest-forms allows Path Traversal.This issue affects Everest Forms: from n/a through 3.6.4.

### CVE-2026-129024

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-22T16:16:39.513 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Everest Forms Everest Forms everest-forms allows Path Traversal.This issue affects Everest Forms: from n/a through 3.6.4.

### CVE-2026-115901

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-23T09:17:05.293 |

Exploitation requires an identity admitted to a configured trusted IdP application, control of claims selected as the OIDC user identifier, acceptance by configured SSO filters, and a victim with an active Cribl session following a crafted authentication link. Script executes in the Cribl origin, disclosing the victim's session token and permitting access with the victim's privileges; administrator access requires an administrator victim.

### CVE-2026-134793

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-22T22:17:32.177 |

Electerm before 5.9.0 on Windows contains an OS command injection vulnerability that allows attackers to execute PowerShell code via crafted file or folder names containing Unicode quote characters. Attackers can deliver names containing U+2019 through archives, WSL distributions, or SMB shares, which break out of getFolderSizeWin() and calcLocal() quoting when victims request folder sizes, executing code as the electerm user.

### CVE-2026-119069

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-237` |
| Published | 2026-11-23T14:17:22.687 |

When rejecting a publication point midway during processing amd falling back to the stored version of the publication point, Routinator will keep the data it had processed for the publication point so far rather than dropping it.

### CVE-2026-119068

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-23T14:17:22.543 |

An rsync server can send diagnostic data to the client which is mirrored to stdout and collected by Routinator line by line. If an excessive amount of data is sent without a line break, Routinator will eventually run out of memory and crash.

### CVE-2026-134827

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-22T22:17:37.707 |

Lightdash before 3.212.0 contains an insufficiently protected credentials vulnerability in getGitlabInstallationRepoReadAccess that sends the organization GitLab app token to unverified hosts. Project developers can set the dbt connection host_domain to an attacker-controlled server and capture the token when the AI agent reads the repository, gaining access to every reachable repository.

### CVE-2026-134825

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-22T22:17:37.390 |

Gradio 6.27.0 before 6.32.0 contains an authentication bypass vulnerability in gradio/history.py that allows remote unauthenticated attackers to use the operator's locally saved Hugging Face token by sending a forged Host: localhost header. When ssr_mode is enabled, requests proxied through the local Node SSR server pass the loopback check, letting attackers call run history endpoints to list buckets, read records and assets, and write buckets under the operator's account.

### CVE-2026-134753

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-22T15:17:13.483 |

dsniff through 2.5a2 contains an integer underflow in decode_sniffer() in decode_sniffer.c that allows unauthenticated remote attackers to write past the global obuf buffer. Attackers can send a UDP datagram to port 2001 on a monitored segment with a 4096-byte string, disabling base64_pton bounds checks to corrupt memory and crash dsniff.

### CVE-2026-134816

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-22T22:17:35.973 |

sigstore-js @sigstore/oci before 0.8.0 contains a credential exposure vulnerability that leaks registry credentials by replaying OAuth2 password-grant request bodies on cross-origin 307 or 308 redirects. Attackers who can make a trusted token service redirect to their host via open redirect or compromise receive the username and password POSTed by RegistryClient.

### CVE-2026-135055

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-23T11:17:00.207 |

A flaw was found in the GLib DMA-BUF path of WebKitGTK. The UIProcess trusted fds.size() as the DMA-BUF plane count when handling AcceleratedBackingStore::DidCreateDMABufBuffer and copied offsets and strides without verifying that those vectors had the same length. A compromised WebProcess can send mismatched vector lengths, causing an out-of-bounds read in the privileged UIProcess. This can disclose UIProcess memory and crash the UIProcess, and may be used as part of a Web Content sandbox-escape chain.

### CVE-2026-132856

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-347` |
| Published | 2026-11-23T14:17:23.343 |

A vulnerability was discovered in the ZoneAlarm client for Windows that allows a low-privileged local user to run code with SYSTEM privileges. An attacker must first be able to run code on the target system as a local user.

### CVE-2026-134808

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-41` |
| Published | 2026-11-22T22:17:34.697 |

Gogs before 0.14.4 on Windows contains a path equivalence vulnerability in isRepositoryGitPath that allows authenticated users with write access to bypass .git directory protection using NTFS aliases. Attackers can create, rename or upload files via aliases like git~1 or .git::$INDEX_ALLOCATION to overwrite .git/config or hooks and execute commands as the Gogs process.

### CVE-2026-134829

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-22T22:17:38.060 |

Umami 3.3.0 before 3.5.0 contains a race condition in two-factor authentication attempt limiting that allows attackers holding a user's password to bypass lockout. Attackers can send many concurrent POST requests to /api/2fa/verify that pass checkRateLimit before recordFailedAttempt runs, brute-forcing TOTP or backup codes beyond the five-attempt limit.

### CVE-2026-134802

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-22T22:17:33.703 |

VoidAuth before 1.19.2 contains an access control bypass vulnerability that allows authenticated users to evade stricter ProxyAuth domain rules by sending percent-encoded path separators. Attackers can request paths with encoded slashes, backslashes, semicolons, or dot segments that match a broader rule, reaching restricted paths once the reverse proxy or backend decodes them.

### CVE-2026-59442

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-23T11:17:00.790 |

TypesenseFilterExpressionConverter does not correctly translate grouped (parenthesized) filter expressions into the Typesense filter syntax.



As a result, the filter sent to Typesense can have a different meaning than the one the application defined, and some conditions may not be applied as intended.



 An application is affected if it uses the Typesense vector store with filter expressions that contain groups and relies on them to restrict results, for example to enforce tenant isolation or access control.



In that case, a remote user may be able to retrieve documents they should not have access to, and the same filter used for a delete operation may remove documents outside the intended scope.

### CVE-2026-131786

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-22T16:16:43.683 |

Insertion of Sensitive Information Into Sent Data vulnerability in myCred myCred mycred allows Retrieve Embedded Sensitive Data.This issue affects myCred: from n/a through 4.0.3.

### CVE-2026-129085

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-22T15:17:12.093 |

Missing Authorization vulnerability in Aguila Technologies WP Customer Area customer-area allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects WP Customer Area: from n/a through 8.4.5.

### CVE-2026-88850

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-23T10:17:16.633 |

The Web-Based Management (WBM) authorization model does not properly enforce permissions for all PROFIBUS configuration operations. A low-privileged remote attacker can abuse an exposed configuration function to modify root-owned PROFIBUS parameters, including device addressing and SSA settings. This allows unauthorized changes to fieldbus-related configuration and violates the intended privilege boundaries within the management interface.

### CVE-2026-134803

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-11-22T22:17:33.857 |

DBHub before 1.7.0 contains a read-only mode bypass vulnerability that allows MCP clients restricted to readonly execute_sql to run write and DDL statements via backslash-escaped quotes. Attackers can hide stacked statements that clear transaction_read_only or COMMIT inside strings misparsed by scanSingleQuotedString, letting them modify or drop MySQL, MariaDB, or PostgreSQL data.

### CVE-2026-115903

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-23T09:17:05.437 |

An authenticated attacker must reach the Edge file APIs through the Leader or directly on an Edge node. On affected managed Edge deployments with RBAC, Read Only access permits these calls. Disclosure is limited to files readable by the Edge process under its operating-system permissions and capabilities.

### CVE-2026-134819

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-22T22:17:36.467 |

Delta Sharing reference server 1.4.0 before 1.5.0 contains an incorrect permission assignment vulnerability that allows share recipients to read unshared data via container-scoped Azure SAS tokens. Recipients with a valid bearer token can request credentials from the temporary-table-credentials endpoint to read every blob in the storage container, including unshared tables.

### CVE-2026-134818

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-610` |
| Published | 2026-11-22T22:17:36.307 |

oasdiff 1.24.0 before 1.34.1 fails to enforce --allow-external-refs=false when --open is used, because the recordingReader() capture reader in load/capture.go never applies the external-reference policy. Attackers supplying an untrusted OpenAPI spec can use external $ref values to read local files or trigger HTTP requests, with contents uploaded in the review bundle.

### CVE-2026-134817

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-22T22:17:36.147 |

mcp-server-kubernetes before 4.2.0 contains an argument injection vulnerability that allows remote MCP clients to inject kubectl flags by supplying dash-prefixed values as positional operands in tools such as exec_in_pod, kubectl_patch, and kubectl_logs. Attackers connected over SSE or Streamable HTTP transport can supply values like --filename to make kubectl read files from the server host, bypassing file-read restrictions.

### CVE-2026-134810

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-22T22:17:35.030 |

diaspora* before 0.10.0 contains a path traversal (zip slip) vulnerability in ImportService#unzip_photos_file that allows authenticated users to write files outside the extraction folder. Attackers can upload a crafted photos zip archive during account import with ../ entry names to create new files at arbitrary locations writable by the diaspora* process.

### CVE-2026-134794

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-11-22T22:17:32.390 |

HedgeDoc before 1.12.1 contains a prototype pollution vulnerability in the POST /history/:noteId endpoint that allows authenticated users to modify Object.prototype by supplying __proto__ as the noteId. Attackers can send a pinned value to /history/__proto__, which historyPost() in lib/history.js assigns onto the prototype, crashing the Node.js process and causing denial of service for all users.

### CVE-2026-131794

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:44.980 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in YellowPencil YellowPencil Visual CSS Style Editor yellow-pencil-visual-theme-customizer allows Reflected XSS.This issue affects YellowPencil Visual CSS Style Editor: from n/a through 7.6.7.

### CVE-2026-131793

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:44.850 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in IT Path Solutions Contact Form to Any API contact-form-to-any-api allows Stored XSS.This issue affects Contact Form to Any API: from n/a through 3.0.7.

### CVE-2026-131791

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:44.557 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in seowriting SEOWriting seowriting allows Stored XSS.This issue affects SEOWriting: from n/a through 1.15.0.

### CVE-2026-131790

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:44.157 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Liquid Web / StellarWP Gutenberg Blocks by Kadence Blocks kadence-blocks allows Stored XSS.This issue affects Gutenberg Blocks by Kadence Blocks: from n/a through 3.9.1.1.

### CVE-2026-131788

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:43.930 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Liquid Web / StellarWP Kadence kadence allows Stored XSS.This issue affects Kadence: from n/a through 1.6.0.

### CVE-2026-131777

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:41.520 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in mra13 / Team Tips and Tricks HQ Stripe Payments stripe-payments allows Stored XSS.This issue affects Stripe Payments: from n/a through 2.1.4.

### CVE-2026-131772

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:41.293 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in PluginUs.Net HUSKY woocommerce-products-filter allows Stored XSS.This issue affects HUSKY: from n/a through 1.4.8.

### CVE-2026-131755

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:41.073 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Jayasree TU Successful Redirection for Contact Form cf7-redirection allows Reflected XSS.This issue affects Successful Redirection for Contact Form: from n/a through 2.0.

### CVE-2026-131741

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:40.617 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Brainstorm Force CartFlows cartflows allows Reflected XSS.This issue affects CartFlows: from n/a through 3.3.2.

### CVE-2026-131726

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:40.407 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Awesomemotive Coming Soon Page, Under Construction & Maintenance Mode by SeedProd coming-soon allows DOM-Based XSS.This issue affects Coming Soon Page, Under Construction & Maintenance Mode by SeedProd: from n/a through 6.20.12.

### CVE-2026-131698

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:40.100 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Bootstrapped Ventures WP Recipe Maker wp-recipe-maker allows Stored XSS.This issue affects WP Recipe Maker: from n/a through 10.9.2.

### CVE-2026-129081

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:39.817 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Aguila Technologies WP Customer Area customer-area allows Stored XSS.This issue affects WP Customer Area: from n/a through 8.4.5.

### CVE-2026-129066

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T16:16:39.663 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Everest Forms Everest Forms everest-forms allows Stored XSS.This issue affects Everest Forms: from n/a through 3.6.4.

### CVE-2026-134754

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-22T15:17:13.640 |

anacrolix/torrent before 1.62.0 contains an uncontrolled recursion vulnerability in Decoder.readOneValue in bencode/decode.go that allows attackers to crash the process by supplying deeply nested bencode data. Attackers can deliver crafted .torrent files or magnet link metadata with millions of nested lists to cause a fatal stack overflow, or deeply nested v2 file trees to exhaust CPU.

### CVE-2026-134749

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1287` |
| Published | 2026-11-22T15:17:12.877 |

MemberPress Members before 3.3.1, with the Block Permissions add-on enabled, contains a denial of service vulnerability that allows authenticated Author-level users to crash pages by saving a non-string blockPermissionsMessage block attribute. Attackers can store a JSON array in the attribute so wpautop() in get_block_replacement_content() throws a PHP 8 TypeError, causing fatal errors on post, home, search, and REST pages for unauthorized viewers.

### CVE-2026-131775

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T15:17:12.403 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in nK Ghost Kit ghostkit allows Stored XSS.This issue affects Ghost Kit: from n/a through 3.8.1.

### CVE-2026-129083

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-22T15:17:11.937 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WPKoi WordPress Themes WPKoi Templates for Elementor wpkoi-templates-for-elementor allows Stored XSS.This issue affects WPKoi Templates for Elementor: from n/a through 3.7.5.

### CVE-2026-134935

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-23T08:17:14.790 |

The dell-xps-touchpad-haptics package before 1.0.0-4 for Omarchy allows local users to change ownership of a root-owned file by making their own .config/omarchy/dell-haptic.conf file a symlink to that target file.

### CVE-2026-134805

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-22T22:17:34.203 |

Zipline before 4.8.3 contains a server-side request forgery vulnerability that allows authenticated OIDC users to make the server fetch arbitrary URLs via the userinfo picture claim. Attackers who control their picture claim at the identity provider can force fetchToDataURL() to request internal or cloud-metadata URLs and read responses from their stored avatar.
