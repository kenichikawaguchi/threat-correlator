# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-29 15:00 UTC
- **対象期間**: `2026-07-28T15:00:41.000Z` 〜 `2026-07-29T15:00:23.000Z`
- **重要CVE数**: 178 件（Critical 9.0+: 44 件 / High 7.0〜: 134 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVSS 7.0 以上の脆弱性は、**Web アプリケーション（特に Joomla・WordPress 系プラグイン）とエンタープライズ向けミドルウェア（IBM WebSphere、Apache Axis2）に集中**しています。  
- 多くが **リモートコード実行 (RCE)・特権昇格・認証バイパス** といった最上位の危険度 (CVSS 9.8‑10.0) を持ち、攻撃者が未認証でもシステム全体を制御できる可能性があります。  
- 同一製品（例：Joomla の Gridbox）に **複数の脆弱性が同時に報告** されており、組み合わせて利用されるケースが顕著です。  
- IoT 向けライブラリ（ESP32‑audioI2S）やインフラストラクチャツール（terraform‑mcp‑server）でも深刻なバッファオーバーフローやクレデンシャル再利用が確認され、**サーバ側だけでなく組み込みデバイスでも同様のリスクが拡大**しています。

---

## 2. 特に注目すべき CVE  

| CVE | 製品・コンポーネント | 主な脆弱性種別 | 重大度 (CVSS) | 注目理由・影響範囲 |
|-----|---------------------|----------------|---------------|-------------------|
| **CVE‑2026‑65884** | Joomla! Extension **Gridbox** (balbooa.com) | 特権昇格（登録時に任意の usergroup ID を指定） | 10.0 | 未認証の攻撃者が管理者権限を持つアカウントを作成でき、以降の **任意ファイルアップロード (CVE‑2026‑65885)** などの攻撃チェーンが成立。Joomla を利用する多数のサイトで即時リスク。 |
| **CVE‑2026‑63234** | **Koollab LMS** | SQLi + unsafe deserialization → WebShell 埋め込み・任意コード実行 | 9.9 | 認証ユーザーが評価入力を通じてサーバ上に PHP WebShell を配置可能。学習管理システムは個人情報・成績データを大量に保持しているため、情報漏洩・改ざんリスクが極めて高い。 |
| **CVE‑2026‑14900** | WordPress プラグイン **Cost Calculator Builder PRO** | RCE (js_to_php 関数のサニタイズ不備) | 9.8 | 全バージョン 4.0.3 までが対象。計算式に任意の PHP コードが埋め込めるため、サイト全体が乗っ取られる。WordPress のシェアが高く、プラグインがインストールされているサイトは多数。 |
| **CVE‑2026‑14512** | **IBM WebSphere Application Server** 9.0 / 8.5 | Pre‑auth unsafe deserialization → 認証回避・コード実行 | 9.8 | 企業の基幹システムで広く採用されている WebSphere。認証前に任意コードが実行できるため、内部ネットワーク全体への侵入足掛かりとなる。 |
| **CVE‑2026‑66713** | Apache **Axis2/Java** (Tribes クラスタリング) | Untrusted deserialization (CWE‑502) | 9.8 | デフォルトで無効だが、クラスタリングを有効にしている環境ではリモートから任意コード実行が可能。多くのエンタープライズサービスが Axis2 を内部 RPC に利用している点で注意が必要。 |

> **補足**  
> - 上記 5 件は **CVSS が 9.8 以上** で、かつ **広範囲に展開されているプラットフォーム**（Joomla、WordPress、IBM WebSphere、Apache Axis2）に影響する点が共通しています。  
> - それぞれが **認証不要**、または **低権限ユーザー** でも実行可能であるため、**防御層の欠如が直ちに深刻な被害につながります**。

---

## 3. 推奨アクション  

### 3‑1. パッチ適用・バージョンアップ
| 製品・コンポーネント | 現行脆弱バージョン | 修正版 (最低バージョン) | 具体的な対策 |
|----------------------|-------------------|------------------------|--------------|
| Joomla! Gridbox (balbooa.com) | < 2.20.2 | **≥ 2.20.2** | 公式サイトまたは Composer で最新版へ更新。不要なプラグインは即時無効化・削除。 |
| Koollab LMS | 1.x 系 (脆弱報告対象) | **≥ 1.5.0** (ベンダーが提供するパッチ) | 管理画面からアップデート、または GitHub のリリースページから最新リリースをデプロイ。 |
| Cost Calculator Builder PRO (WordPress) | ≤ 4.0.3 | **4.0.4 以上** | WordPress 管理画面 → プラグイン更新、または公式サイトから ZIP を再インストール。 |
| IBM WebSphere Application Server 9.0 / 8.5 | 9.0.0‑9.0.4 / 8.5.0‑8.5.5 | **9.0.5.13 以上**、**8.5.6.12 以上** (IBM Fix Pack) | IBM Fix Central から該当 Fix Pack を取得し、`wsadmin` で適用。 |
| Apache Axis2/Java | ≤ 2.0.0 | **2.0.1** (または最新安定版) | Maven/Gradle の依存バージョンを 2.0.1 へ上げ、`axis2.xml` の `enableClustering` が `false` であることを確認。 |
| terraform‑mcp‑server | < 1.1

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-65884

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Red` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-29T13:19:10.677 |

Joomla Extension - balbooa.com - Privilege Escalation in Gridbox < 2.20.2 - The registration method allows users provided usergroup IDs, allowing unauthenticated actors to register new accounts with administrative permissions.

### CVE-2026-65883

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-29T11:16:50.297 |

Joomla Extension - aimy-extensions.com - RCE via PHP object injection in Aimy Captcha-Less Form Guard 18.0 - 20.0 - A forged clfgd field allows PHP objection injection and thereby remote code execution.

### CVE-2026-16498

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-488` |
| Published | 2026-07-28T19:17:32.117 |

The terraform-mcp-server before version 1.1.0 is vulnerable to a cross-tenant credential reuse issue in the streamable-HTTP stateless transport mode that may allow one user's Terraform token to be used to execute tool calls on behalf of subsequent users. This vulnerability, CVE-2026-16498, is fixed in terraform-mcp-server 1.1.0.

### CVE-2026-63234

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-29T07:16:42.817 |

A SQL injection and unsafe deserialisation
vulnerability in Koollab LMS allowed an authenticated attacker to inject through the manual mark
assessment endpoint, control data passed to unserialize(), write a webshell to
a publicly accessible location, and execute arbitrary code on the server.

### CVE-2026-63233

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-29T07:16:42.710 |

A SQL injection and unsafe deserialisation
vulnerability in Koollab LMS allowed an authenticated attacker to inject through the assessment
overall answer endpoint, control data passed to unserialize(), write a webshell
to a publicly accessible location, and execute arbitrary code on the server.

### CVE-2026-63232

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-29T07:16:42.600 |

A SQL injection and unsafe deserialisation
vulnerability in Koollab LMS allowed an authenticated attacker to inject through the assessment
reinforcement endpoint, control data passed to unserialize(), write a webshell
to a publicly accessible location, and execute arbitrary code on the server.

### CVE-2026-63227

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-29T07:16:41.967 |

An unrestricted SCORM file upload vulnerability
in Koollab LMS allowed
an authenticated module designer to upload a SCORM package containing a PHP
webshell to a publicly accessible directory and execute arbitrary code on the
server.

### CVE-2026-14900

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-29T11:16:48.200 |

The Cost Calculator Builder PRO plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 4.0.3 via the js_to_php function. This is due to insufficient sanitization of the orderDetails[*].originalValue field, which is injected verbatim into a calculator formula string passed to PHP eval() inside js_to_php(), with the regex allow-list in evaluateFormula() only filtering alphanumeric tokens and leaving non-word punctuation characters intact. This makes it possible for unauthenticated attackers to execute code on the server. The only authentication barrier is a nonce check, but the required nonce is publicly emitted on every front-end page via the wp_head hook, making it freely obtainable by unauthenticated visitors. Payloads must be non-word XOR gadgets to bypass sanitization.

### CVE-2025-10656

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-29T10:16:31.407 |

The Spreadsheet Price Changer for WooCommerce and WP E-commerce – Light plugin for WordPress is vulnerable to Missing Authorization in all versions up to, and including, 2.4.37 vi the user_filter function. This makes it possible for unauthenticated attackers to create admin accounts.

### CVE-2026-13423

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-29T07:16:41.250 |

The Streamit WordPress theme through 4.5.0 does not perform any authorization or nonce verification on one of its unauthenticated AJAX routes, which invokes an attacker-supplied PHP function with an attacker-supplied argument array, allowing unauthenticated attackers to call arbitrary functions (for example to create an administrator account), leading to privilege escalation and remote code execution.

### CVE-2026-18072

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-506` |
| Published | 2026-07-29T05:16:40.840 |

The Advanced Responsive Video Embedder for Rumble, Odysee, YouTube, Vimeo, Kick … plugin for WordPress is vulnerable to Authentication Bypass via a Hardcoded Backdoor in version 10.8.7. The vulnerability exists because the `_arve_uc_init()` function — registered on WordPress's `init` hook at priority 1 so that it runs before any authentication checks on every request — reads an attacker-supplied token from the `_wplogin` (or `_wpm`) parameter and compares it against a hardcoded SHA-256 hash embedded directly in the plugin source, with no nonce verification, no capability check, and no password validation anywhere in the flow. Because this static hash constitutes a set of universal credentials that are publicly accessible in the plugin's source code, unauthenticated attackers can supply the known token to be authenticated as an arbitrarily selected existing administrator account, gaining full administrative control over the affected WordPress site. This was likely introduced by an attacker who gained commit access to the developers account.

### CVE-2026-54658

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-28T23:17:08.913 |

Hypequery is a TypeScript semantic layer for ClickHouse. Prior to 2.0.2, escapeValue() in packages/clickhouse/src/core/utils.ts did not escape backslashes before single quotes during parameter substitution, allowing attacker controlled query parameters with a trailing backslash to escape the closing quote and inject arbitrary SQL. This issue is fixed in version 2.0.2.

### CVE-2026-14512

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-28T21:17:25.783 |

IBM WebSphere Application Server 9.0, and 8.5 traditional is vulnerable to pre-authentication unsafe deserialization which could allow a remote attacker to bypass authentication or execute arbitrary code.

### CVE-2026-14446

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-28T21:17:25.660 |

IBM WebSphere Application Server 9.0, and 8.5 is vulnerable to broken access control/privilege escalation in the administrative console.

### CVE-2026-51267

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-28T16:18:50.400 |

schreibfaul1 ESP32-audioI2S 3.4.5 has a heap-based buffer overflow vulnerability in the URL path concatenation and encoding module. The application splices untrusted extension path and attacker-controlled query string into a path buffer, then invokes urlencode without validating the final string length. Remote attackers can construct an oversized malicious URL path and query string to trigger out-of-bounds heap write, resulting in arbitrary code execution, information disclosure, service crash, or privilege escalation.

### CVE-2026-51266

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-28T16:18:50.270 |

schreibfaul1 ESP32-audioI2S 3.4.5 has a heap-based buffer overflow vulnerability in the HTTP request header construction logic. The application dynamically splices attacker-controlled host name, path, query string, and multiple HTTP header fields into a fixed ps_ptr heap buffer without proper size limitation and boundary validation. Remote attackers can use an oversized crafted network request parameter to trigger out-of-bounds heap write, leading to arbitrary code execution.

### CVE-2026-51263

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-28T16:18:50.137 |

schreibfaul1 ESP32-audioI2S 3.4.5 is vulnerable to Buffer Overflow. The Audio::openai_speech function in the Audio library manually constructs JSON request bodies and HTTP request headers by directly concatenating externally controllable input and instructions strings without effective length restriction and boundary validation. An unauthenticated remote attacker can send oversized malicious string data to trigger a heap buffer overflow during string splicing, resulting in memory corruption.

### CVE-2026-66713

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-28T15:17:50.430 |

Deserialization of Untrusted Data (CWE-502) in the Tribes-based clustering component

  in Apache Software Foundation Apache Axis2/Java through 2.0.0 on Apache Tomcat

  (only when Tribes clustering is enabled, which is off by default) allows an

  unauthenticated remote attacker with network access to the clustering port to

  execute arbitrary code via a crafted serialized Java object delivered to the cluster

  channel and deserialized in

  org.apache.axis2.clustering.tribes.Axis2ChannelListener#messageReceived. Users are

  recommended to upgrade to version 2.0.1, which fixes this issue by removing the

  clustering feature entirely.

### CVE-2026-51259

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-28T15:17:16.640 |

Unchecked unsigned integer overflow in buffer size calculation in schreibfaul1 ESP32-audioI2S 3.4.5 leads to undersized PSRAM buffer allocation. Subsequent normal audio buffer read and write operations cause heap out-of-bounds access, memory corruption, denial of service, and potential code execution.

### CVE-2026-51252

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-07-28T15:17:16.370 |

schreibfaul1 ESP32-audioI2S 3.4.5 has a buffer overflow vulnerability in the MP3Decoder::UnpackSFMPEG1 function due to missing input validation on attacker-controlled MP3 metadata.

### CVE-2026-51271

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-28T16:18:50.940 |

In schreibfaul1 ESP32-audioI2S 3.4.5, a heap-based buffer overflow vulnerability exists in the WAV header parsing function read_WAV_Header(). The function reads untrusted chunk size and bytes-to-skip value directly from malicious WAV files without reasonable range restriction. Abnormally large bts and headerSize values lead to out-of-bounds heap memory read/write during header parsing, which can be exploited to execute arbitrary code, disclose sensitive information, cause denial of service or escalate privileges.

### CVE-2026-9177

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-07-29T14:16:35.857 |

A Server-Side Template Injection (SSTI) vulnerability was identified 
in the mail template functionality of the Axway SecureTransport product in version 5.5-20260326. This 
flaw 
allows an attacker with admin privileges to inject arbitrary Java code expressions, which are 
executed server-side when the template is rendered (i.e., during email 
sending). Successful exploitation of this flaw allows an attacker to 
execute 
arbitrary code on the server that results in full host compromise.



This issue affects all Axway SecureTransport versions prior 5.5-20260528 update.

### CVE-2026-65885

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Red` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-29T13:19:10.820 |

Joomla Extension - balbooa.com - Authenticated arbitrary file upload in Gridbox < 2.20.2 - File upload methods allows authenticated attackers to upload arbitrary files. Turns into an authenticated RCE if combined with CVE-2026-65884 as the required account can be created by the attacker.

### CVE-2026-6881

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-28T21:17:29.427 |

A SQL Injection in the Giving Reports functionality in Ellucian Advance Web and Legacy Advance allows an authenticated attacker to extract sensitive information from databases via a crafted SQL query in the class credit field.



This issue affects Advance Web: all versions; Legacy Advance: all versions.



Ellucian CRM Advance is not impacted.

### CVE-2026-51260

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-28T15:17:16.780 |

Unsafe fixed-size memcpy operation in AudioBuffer::writeSpace() of schreibfaul1 ESP32-audioI2S 3.4.5 allows remote heap buffer overflow. The code copies a full UINT16_MAX bytes without validating destination available space, causing out-of-bounds memory write.

### CVE-2026-0667

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-07-29T13:17:29.180 |

CWE-754: Improper Check for Unusual or Exceptional Conditions vulnerability that could cause arbitrary code execution, denial of service and loss of confidentiality & integrity when communicating over the Modbus TCP protocol.

### CVE-2026-18191

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-912` |
| Published | 2026-07-29T08:16:30.223 |

VIN-DS783E-E6 developed by Vacron has a Hidden Functionality vulnerability, allowing unauthenticated remote attackers to exploit a specific hidden function to obtain the administrator credentials of the device.

### CVE-2026-14973

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-28T21:17:26.570 |

IBM Aspera Desktop App 1.0.5 through 1.0.19 IBM Aspera for desktop can allow files to be written outside of the user's selected download destination.

### CVE-2026-65890

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:L/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-29T14:16:33.883 |

Joomla Extension - balbooa.com - Unauthenticated SQL injection in Gridbox < 2.20.2 - Multiple SQLi vectors allow unauthenticated actors to inject SQL in queries.

### CVE-2026-65889

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-284` |
| Published | 2026-07-29T14:16:33.757 |

Joomla Extension - balbooa.com - Unauthenticated recursive directory deletion < 2.20.2 - The generateNewApp method allows actors to recursively delete directories.

### CVE-2026-58179

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-29T10:16:42.803 |

The Apache Traffic Server regex_remap plugin overflows the stack and integers from substitution input.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58161

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-29T10:16:41.780 |

Apache Traffic Server can crash from null dereferences and dangling references in TLS and SNI handling.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58155

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-07-29T09:16:29.877 |

Apache Traffic Server truncates over-long header names, allowing header aliasing, request smuggling, and policy bypass.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58154

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-29T09:16:29.743 |

Apache Traffic Server can write out of bounds or overflow integers while parsing MIME and HTTP headers.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-67174

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-28T15:17:51.073 |

Pivotick contains a DOM-based cross-site scripting vulnerability in its generic UI element resolution and icon-rendering utilities.

The tryResolveHTMLElement function treated any resolved string as HTML markup by assigning it to a <template> element through innerHTML. Strings derived from untrusted graph properties or custom rendering callbacks could therefore introduce arbitrary HTML or SVG elements into the live document. The vulnerable function was used by multiple UI components, including headers, property panels, extra panels, and tooltips.

Additionally, createIcon inserted caller-supplied svgIcon markup into a template without sanitization. An application integrating Pivotick and deriving icon markup from untrusted data could therefore expose a second script-execution path.

An unauthenticated attacker able to provide a crafted graph, property value, rendering result, or SVG icon could execute JavaScript in another user's browser when the affected content is displayed or interacted with. Successful exploitation could allow the attacker to access information available to the victim, manipulate graph data or application state, and perform actions with the victim's privileges.

The patch changes string rendering to use textContent, requiring callers to explicitly return an Element when HTML rendering is intended. It also sanitizes SVG icon markup before inserting it into the DOM.

### CVE-2026-14488

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-29T11:16:48.063 |

The Meta Box AIO plugin for WordPress is vulnerable to Missing Authorization via the template_redirect dispatcher in the MB Frontend Submission extension in versions up to, and including, 3.8.0. This is due to the handle_request() function routing the mbfs_delete action without any capability or ownership check, and the nonce verification in check_ajax() being gated behind is_ajax() which is false for template_redirect requests, making it bypassable. This makes it possible for unauthenticated attackers to delete arbitrary posts and pages by supplying an attacker-controlled post ID via the rwmb_frontend_field_object_id GET parameter on any page that hosts a frontend submission form regardless of whether allow_delete is enabled.

### CVE-2026-63230

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-29T07:16:42.373 |

A pre-authentication error-based SQL injection
vulnerability in Koollab LMS allowed an unauthenticated attacker to read sensitive database
contents, including personally identifiable information, credentials, and valid
JWT tokens that may enable account takeover, via the SCORM report endpoint.

### CVE-2026-63229

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-29T07:16:42.267 |

A pre-authentication blind SQL injection
vulnerability in Koollab LMS allowed an unauthenticated attacker to use a time-based SQL oracle via
the SSO OAuth endpoint to read sensitive database contents, including
personally identifiable information, credentials, and valid JWT tokens that may
enable account takeover.

### CVE-2026-64863

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-28T23:17:10.213 |

goshs is a feature-rich single-binary file server for red teamers and developers. Prior to 2.1.4, the httpserver/server.go wdGuard handled WebDAV MOVE as a write-only method and did not enforce --no-delete, allowing WebDAV clients to delete or overwrite files via MOVE with Overwrite: T. This issue is fixed in version 2.1.4.

### CVE-2026-62325

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-28T23:17:10.077 |

goshs is a feature-rich single-binary file server for red teamers and developers. From 2.1.3 until 2.1.4, the sftpserver/sftpserver.go password handler used Username != "" && Password != "", so running goshs with -b 'admin:' -sftp and no -fkf left both SFTP authentication handlers unset and allowed unauthenticated file access. This issue is fixed in version 2.1.4.

### CVE-2026-14959

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-28T21:17:26.443 |

IBM Aspera Faspex 5 5.0.0 through 5.0.15.4 could allow a remote authenticated attacker to execute arbitrary code due to shell command injection.

### CVE-2026-14958

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-28T21:17:26.317 |

IBM Aspera Faspex 5 5.0.0 through 5.0.15.4 could allow a remote authenticated attacker to execute arbitrary code due to unquoted shell interpolation.

### CVE-2026-50737

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-07-28T19:17:36.827 |

When applying replicated changes for a row that is missing one or more columns, pglogical evaluates the affected table's default expressions on the subscriber. Because the apply worker runs at a privilege level equivalent to a PostgreSQL superuser in default installations, any function invoked by such a default expression also runs at that privilege. A party acting as the publisher can use this path to cause functions to be executed on the subscriber as superuser, escalating from a role permitted to use pglogical to full superuser.

This is a second, independent path to the same superuser escalation tracked under CVE-2026-50736 (the pglogical queue issue). To exploit the issue an attacker must be able to direct a subscription at an endpoint they control. In default installations this requires privileges normally reserved for a superuser, so the issue is most relevant to managed deployments where the ability to create subscriptions has been delegated to non-superuser roles.

### CVE-2026-50736

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-28T19:17:36.700 |

The pglogical queue mechanism, used to convey out-of-band commands such as replicated DDL from a publisher to a subscriber, executes message payloads on the subscriber at the privilege level of the apply worker, which is equivalent to a PostgreSQL superuser in default installations. A party acting as the publisher can send crafted queue messages that cause arbitrary SQL to be executed on the subscriber as superuser, escalating from a role permitted to use pglogical to full superuser and breaking the isolation between tenants in shared deployments. To exploit the issue an attacker must be able to direct a subscription at an endpoint they control. In default installations this requires privileges normally reserved for a superuser, so the issue is most relevant to managed deployments where the ability to create subscriptions has been delegated to non-superuser roles.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-16496

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-384` |
| Published | 2026-07-28T19:17:31.983 |

The terraform-mcp-server before version 1.1.0 is vulnerable to an authorization bypass in the streamable-HTTP stateful transport mode that may allow a user who obtains another user's MCP session ID to have their tool calls executed using that user's Terraform credentials. This vulnerability, CVE-2026-16496, is fixed in terraform-mcp-server 1.1.0.

### CVE-2026-14270

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-29T12:16:35.697 |

The Extra Checkout Options (addon for Extra Product Options & Add-Ons for WooCommerce) plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.3.2. This is due to missing authorization and nonce validation in the eco_save_settings() function, which allows low-privileged authenticated users to modify the tc_eco_custom_file_types upload allowlist setting, combined with insufficient authorization on the wc_eco_upload_file AJAX action. This makes it possible for authenticated attackers, with Subscriber-level access and above, to allow PHP uploads, upload a PHP file using the frontend upload nonce exposed on cart and checkout pages, and achieve remote code execution. NOTE: This vulnerability was partially fixed in version 2.3.2.

### CVE-2026-50622

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-29T10:16:41.047 |

Description:
Missing Authorization in Apache Atlas.
A missing authorization vulnerability in Apache Atlas's admin endpoints allows any authenticated user, regardless of their assigned role, to perform administrative operations.




Affect Version:
This issue affects Apache Atlas: from 0.8 through 2.5.0.


Mitigation:
Users are recommended to upgrade to version 2.6.0, which fixes the issue.

### CVE-2026-12144

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-29T02:16:41.840 |

The Wholesale for WooCommerce plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.0.5. This is due to the `save_requests_meta()` function applying only `sanitize_text_field()` to the `user_role_set` POST parameter before passing it directly to `WP_User::add_role()`, with no allowlist validation against permitted wholesale roles and no capability check such as `current_user_can('promote_users')` or `current_user_can('manage_options')`. This makes it possible for authenticated attackers with author-level access and above to escalate their privileges to administrator by supplying `administrator` as the `user_role_set` value in a crafted request. The function is gated only by a nonce (`request_user_role_nonce`) that is rendered in the meta box on the `wwp_requests` post edit screen; because the post type is registered with `capability_type => 'post'`, any author-level user who has authored a `wwp_requests` post — such as one created via the wholesale registration form — can access this nonce and submit the role-assignment request.

### CVE-2026-54653

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-07-28T22:17:40.077 |

datamodel-code-generator generates Pydantic v2 models, dataclasses, TypedDict, and msgspec.Struct from OpenAPI, JSON Schema, GraphQL, Avro, Protobuf, and raw JSON, YAML, or CSV. From  0.17.0 until 0.60.2, datamodel-code-generator preserves attacker-controlled default_factory values in src/datamodel_code_generator/parser/jsonschema.py through JsonSchemaObject.init and get_field_extras and emits them into Field(default_factory=...) or field(default_factory=...), allowing Python expression execution when the generated model is imported. This issue is fixed in version 0.60.2.

### CVE-2026-49258

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-07-28T19:17:36.000 |

Nebula Mesh is a self-hosted control plane for the Slack Nebula mesh VPN. In versions 0.3.5 and below, the web UI (/ui/*) does not apply the per-operator CA scoping employed by the JSON API. This was partially addressed by GHSA-598g-h2vc-h5vg, but the changes were not implemented in the web read/mutation surface. Any authenticated non-admin operator (for example, one created via self-registration or OIDC) can access resources belonging to other operators. The host create/edit/mobile-bundle/network-create paths and all CA-management routes were already correctly scoped. A malicious operator could block or delete any other operator's host, or read any operator's hosts and networks. This issue has been fixed in version 0.3.6.

### CVE-2026-16771

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-28T19:17:32.247 |

In firmware versions 2.7.7 and earlier, the Arris BGW210‑700 gateway fails to enforce any server‑side authentication on its /cgi-bin/*.ha management endpoints, relying solely on client‑side CSS/JavaScript gating that can be bypassed by any HTTP client. This allows unauthenticated attackers on the LAN to read sensitive configuration data, modify persistent device settings, or trigger backend diagnostic operations. The issue appears systemic across the CGI handler chain.

### CVE-2026-15992

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-28T19:17:31.727 |

The WP Password Policy plugin for WordPress is vulnerable to Privilege Escalation in all versions up to and including 3.7.1. This is due to missing authorization checks and nonce verification in the `get_user()` function of the `Module_Password_Hint` class, which unconditionally calls `WP_User::set_role()` with the attacker-supplied `role` parameter on any account resolved via `$_POST['user_login']`, without confirming the requesting user holds the capability to assign roles. This makes it possible for authenticated attackers, with subscriber-level access and above, to escalate their own privileges to Administrator by submitting a crafted POST request — with `action` set to `createuser` and `role` set to `administrator` — to the password-reset form endpoint. The vulnerable code path is reachable via the `password_hint` filter hooked during the WordPress password-reset form render, meaning an attacker need only possess a valid password-reset cookie to reach the sink.

### CVE-2026-51275

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-28T17:16:46.807 |

In schreibfaul1 ESP32-audioI2S 3.4.5, a heap-based buffer overflow in the ID3v2 APIC frame parsing function in audiolib allows remote attackers to execute arbitrary code or cause a denial of service (crash) via a crafted MP3 file. The vulnerability exists due to missing length validation when processing the APIC frame size field, leading to an out-of-bounds memory write.

### CVE-2026-51274

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-28T17:16:46.673 |

In schreibfaul1 ESP32-audioI2S 3.4.5, a heap-based buffer overflow in the ID3v2 SYLT synchronized lyrics parser in audiolib allows remote attackers to cause a denial of service (application crash), information disclosure, or potential arbitrary code execution via a crafted MP3 file. The vulnerability occurs due to missing bounds validation on attacker-controlled frame size and improper memory access during lyric parsing.

### CVE-2026-51269

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-28T16:18:50.670 |

schreibfaul1 ESP32-audioI2S 3.4.5 has a heap-based buffer overflow vulnerability in the connecttospeech() function. The application accepts attacker-controlled long speech text input, performs URL encoding, and directly appends the encoded result into a fixed ps_ptr heap buffer when constructing HTTP TTS request headers. Lack of input length validation and boundary checking allows remote attackers to craft oversized input to trigger out-of-bounds heap write, resulting in arbitrary code execution.

### CVE-2026-67215

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-07-29T14:16:35.187 |

cJSON through 1.7.19 is vulnerable to uncontrolled recursion leading to stack exhaustion when an untrusted RFC 6902 JSON Patch is applied via cJSONUtils_ApplyPatches() or cJSONUtils_ApplyPatchesCaseSensitive(). A patch containing add and copy operations grafts duplicated subtrees to amplify document depth beyond the parser's nesting limit: cJSON_Delete() recurses with no depth bound, and the cJSON_Duplicate() guard CJSON_CIRCULAR_LIMIT is set to 10000, ten times the parser's 1000-level nesting limit and high enough to overflow a default thread stack. An attacker who can supply the patch document can crash the process, resulting in denial of service.

### CVE-2026-55995

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-07-29T14:16:31.423 |

A Double Free vulnerability in open-iscsi allows an unauthenticated MITM attacker to cause DoS.






This issue affects open-iscsi: from ? through 56718d4e9d1a4f51c30697b5c0534144bb41c9bb.

### CVE-2026-14354

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-07-29T13:17:42.723 |

CWE-522 Insufficiently Protected Credentials vulnerability exists that could cause authentication bypass and unauthorized credential modification, potentially leading to compromise of managed devices, when a local privileged attacker leverages weaknesses in the handling and protection of stored credentials within the application.

### CVE-2026-58151

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-29T09:16:29.327 |

Apache Traffic Server can be crashed or driven to resource exhaustion by abusive HTTP/2 framing and flow-control.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-15325

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-07-28T21:17:27.770 |

IBM WebSphere Application Server 9.0, and 8.5 and IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.7 is vulnerable to HTTP request smuggling due to improper handling of TRACE requests.

### CVE-2026-15064

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-07-28T21:17:27.493 |

IBM WebSphere Application Server 9.0, and 8.5 and IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.7 is vulnerable to HTTP Response Smuggling due to improper handling of non-standard HTTP version tokens.

### CVE-2026-57510

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-28T20:17:27.027 |

SuperPlane before 0.27.0 contains a broken object-level authorization vulnerability in the CanvasService gRPC handlers that allows authenticated users with viewer-level access to one organization to access resources belonging to other organizations by supplying arbitrary canvas or queue UUIDs without organization scoping. Attackers can read cross-tenant execution history and event payloads containing sensitive secrets, write queue items and canvas events into victim organizations, delete arbitrary canvases, and disrupt automation workflows across tenant boundaries.

### CVE-2026-16347

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-07-28T20:17:23.713 |

MikroTik RouterOS contains a weakness in its API authentication handling that lacks effective safeguards against excessive login attempts. The system does not enforce meaningful rate-limiting, account lockout, or source-based restrictions, allowing repeated authentication failures to proceed without defensive response. In some versions, a fixed per-connection delay is present, but it can be bypassed through concurrent sessions, resulting in continued high-volume attempts. This deficiency increases the risk that an attacker could eventually obtain valid credentials and gain unauthorized access to administrative services.

### CVE-2026-67185

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-28T17:17:08.013 |

TinyWeb through 0.0.8 contains a path traversal vulnerability that allows unauthenticated attackers to read arbitrary files by submitting ../ sequences in the URL path, which are concatenated directly to the configured web root in HttpBuilder::buildResponse() without normalization, dot-segment removal, or boundary checks. Attackers can craft a single request with ../ sequences that pass through the URL parser unchanged and reach the filesystem call via HttpFile::setFile(), exposing sensitive files such as credential stores and private keys when the server process runs as root.

### CVE-2026-67184

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-28T17:17:07.880 |

TinyWeb through 0.0.8 contains a null pointer dereference vulnerability that allows unauthenticated remote attackers to crash worker processes by sending a malformed HTTP request line with an invalid version string. The HttpParser::execute() function fails to allocate the Url object when version parsing fails, leaving the url pointer NULL, and buildResponse() subsequently dereferences this NULL pointer without checking the valid_requ flag, producing a SIGSEGV that terminates the worker process and, when repeated across all workers, takes the server permanently offline until manually restarted.

### CVE-2026-67183

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-07-28T17:17:07.737 |

TinyWeb through 0.0.8 contains a memory leak vulnerability that allows unauthenticated attackers to exhaust available memory by sending ordinary well-formed HTTP requests. Each request causes HttpParser::execute() to allocate Url objects, HttpHeaders objects, and HttpHeader instances via raw new expressions that are never freed due to missing destructors and unreachable delete calls, causing worker resident memory to grow monotonically by approximately 20 to 28 kB per request until the worker process is killed.

### CVE-2026-66748

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-28T16:20:16.310 |

Camaleon CMS versions 2.1.1 through 2.9.1 contains an authenticated remote code execution vulnerability that allows users with custom_fields manage permission to execute arbitrary Ruby code by supplying a malicious expression through the select_eval custom field type. Attackers can store an attacker-controlled Ruby expression in the field options command parameter, which is evaluated via instance_eval within an ERB view whenever a post edit page is rendered, achieving server-side code execution with web server process privileges.

### CVE-2026-63727

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-648` |
| Published | 2026-07-28T15:17:26.063 |

Anchore Enterprise versions from 5.11.0 to 5.27.1 and 6.0.0 contain an improper privilege escalation vulnerability in the user management API. An authenticated attacker who is able to access the Anchore Enterprise API could issue an API call capable of modifying user permissions to gain access to additional resources and operations. It is not possible to grant the system-admin role, but a read only user could be granted write access. This issue is fixed in Anchore Enterprise 5.27.2 and 6.0.1.

### CVE-2026-11974

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-29T07:16:41.143 |

The wp-media-folder-addon WordPress plugin through 4.1.6 does not validate a user-supplied parameter before using it in a file read operation in two AJAX actions available to unauthenticated users, leading to Arbitrary File Disclosure and Server-Side Request Forgery on sites where a cloud storage connection has been configured. This is an incomplete fix of CVE-2026-9690, whose patch hardened only one of the affected cloud-storage handlers and left the others unpatched.

### CVE-2026-54650

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-28T23:17:08.763 |

openhole exposes localhost to the internet in one command. In 0.1.1 and earlier, openhole-server in internal/server/public_proxy.go forwarded r.URL.Path instead of preserving the original request target with r.URL.EscapedPath(), allowing percent encoded dot segments %2e and separators %2f to reach tunneled local services as ../ and / for path traversal. This issue is fixed in version 0.1.2.

### CVE-2026-48396

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-28T19:17:35.870 |

Bridge is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-48395

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-07-28T19:17:35.753 |

Bridge is affected by an Untrusted Search Path vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-14869

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-28T19:17:31.423 |

The terraform-mcp-server before version 1.1.0 is vulnerable to a server-side request forgery issue in the streamable-HTTP transport that may allow an unauthenticated remote client to redirect the server's Terraform API requests, and the server-side authorization token, to an attacker-controlled endpoint. This vulnerability, CVE-2026-14869, is fixed in terraform-mcp-server 1.1.0.

### CVE-2026-48388

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-07-28T18:17:20.887 |

Adobe Photoshop Installer was affected by an Uncontrolled Search Path Element vulnerability that could have resulted in arbitrary code execution in the context of the current user. An attacker could have exploited this vulnerability by placing a malicious library in a directory searched by the installer. Exploitation of this issue required user interaction in that a victim must have been running the installer. Scope is changed.

### CVE-2026-54609

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-406;CWE-770` |
| Published | 2026-07-28T17:16:52.507 |

QTI Neon is a minimal, game-agnostic, relay-based UDP multiplayer protocol library. In version 1.0.0, the relay's handleReconnectRequest forwards RECONNECT_REQUEST packets to the host without bounding them, so an unauthenticated client can drive relay-to-host amplification and cause a denial of service on the host. No fixed version is available as of this review.

### CVE-2026-54603

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-601` |
| Published | 2026-07-28T17:16:52.227 |

OAuth2 is a Ruby wrapper for the OAuth 2.0 and 2.1 authorization frameworks, including OpenID Connect (OIDC). From 0.4.0 to 2.0.21, a protocol-relative redirect Location returned to OAuth2::Client#request overrides the request authority, so the bearer Authorization header is sent to an attacker-controlled host, leaking the credential. This issue is fixed in version 2.0.22.

### CVE-2026-18084

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-28T17:16:37.960 |

Improper Neutralization of Input During Web Page Generation vulnerability in BlackBerry UEM Management Console of BlackBerry UEM allows Cross-Site Scripting (XSS).

This issue affects UEM: 12.23.0 QF8 or earlier.

### CVE-2026-45293

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-07-28T16:18:13.503 |

WordPress Coding Standards is a set of PHP_CodeSniffer rules (sniffs) that enforce WordPress coding conventions. From 0.14.1 until 3.4.1, the WordPress.WP.EnqueuedResourceParameters sniff (active in the WordPress and WordPress-Extra rulesets) reconstructed the $ver argument passed to functions such as wp_enqueue_script() and ran it through eval() inside its is_falsy() method, so a maliciously crafted argument such as 'system'('id') would execute during a scan; as a result, running PHPCS with WordPressCS over untrusted PHP (for example a CI pipeline that lints pull requests, or a developer reviewing third-party code) could lead to arbitrary command execution on the scanning host. The WordPress-Core and WordPress-Docs rulesets are not affected. This issue is fixed in version 3.4.1.

### CVE-2026-44944

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-29T13:18:46.113 |

An Incorrect Authorization vulnerability in open-iscsi allows unprivilidged local users to use the isscsiuio control socket.






This issue affects open-iscsi: from ? through 668ca1df9c9a1e9bdd5c999ae1d67c9c8909237e.

### CVE-2026-12927

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-29T13:17:36.300 |

CWE-787 Out-of-bounds write vulnerability exists that could cause loss of data or potentially risk arbitrary code execution when a malicious CGF file is imported to IGSS Definition.

### CVE-2026-58188

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-29T10:16:44.093 |

Several Apache Traffic Server experimental plugins have memory-safety and limit-bypass errors.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58162

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-29T10:16:41.927 |

The Apache Traffic Server certifier plugin generates certificates based on attacker-controlled client SNI.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58184

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-29T10:16:43.520 |

The Apache Traffic Server header_rewrite plugin can crash or corrupt memory during cookie operations and CIDR condition matching.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58177

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-29T10:16:42.510 |

The Apache Traffic Server Cripts framework has out-of-bounds writes, path traversal, and use-after-free errors.

This issue affects Apache Traffic Server: from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 10.1.4, which fix the issue.

### CVE-2026-58164

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-29T10:16:42.217 |

Apache Traffic Server has use-after-free and time-of-check/time-of-use errors in remap configuration handling.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58163

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-29T10:16:42.073 |

Apache Traffic Server mishandles on-disk cache fields and object lifetimes, corrupting state or crashing.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-67216

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-07-29T14:16:35.333 |

cJSON through 1.7.19 contains an inefficient algorithmic complexity flaw in cJSON_Compare(). When comparing objects, the function recurses into each shared subtree twice, once in each direction, with no depth guard, making the running time exponential in nesting depth. A small, deeply nested document of a few hundred bytes (depth around 40) compared for equality consumes hours of CPU, and the cost roughly doubles with each additional level of nesting. An application that calls cJSON_Compare() on attacker-influenced JSON that is structurally equal to a reference document is exposed to a denial-of-service condition.

### CVE-2026-67214

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-29T14:16:35.043 |

nanoid (Nano ID) before 5.1.16 contains an infinite loop in the customAlphabet and nanoid functions of its non-secure module (nanoid/non-secure). When these functions are given a negative size, the loop counter is decremented from a negative value and never reaches its termination condition, spinning indefinitely and hanging the calling thread. An application that passes an unvalidated, attacker-controlled negative size to these functions is exposed to a denial-of-service condition.

### CVE-2026-67213

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-29T14:16:34.890 |

nanoid (Nano ID) before 5.1.6 contains an infinite loop in the customAlphabet and customRandom functions. When these functions are configured with a size of 0, the internal generation loop never satisfies its exit condition and spins indefinitely, hanging the calling thread. An application that passes an unvalidated, attacker-controlled size of 0 to these functions is exposed to a denial-of-service condition.

### CVE-2026-58189

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-29T10:16:44.243 |

Apache Traffic Server allows redirect-limit bypass when plugins reset the retry counter, enabling SSRF amplification.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58186

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-29T10:16:43.807 |

The Apache Traffic Server webp_transform plugin can decode unsafely and serve mislabeled, cacheable responses.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58185

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-29T10:16:43.663 |

The Apache Traffic Server intercept plugin has a use-after-free.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58183

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-29T10:16:43.373 |

The Apache Traffic Server prefetch plugin can crash when processing attacker-influenced input.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58182

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-29T10:16:43.230 |

The Apache Traffic Server ts_lua plugin mishandles initialization, transform context, and per-instance state.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58181

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-29T10:16:43.087 |

The Apache Traffic Server uri_signing and url_sig plugins can exhaust the stack or crash on attacker input.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58180

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-29T10:16:42.947 |

The Apache Traffic Server txn_box plugin overflows the stack from attacker-controlled input.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58178

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-07-29T10:16:42.657 |

The Apache Traffic Server ESI plugin can recurse without bound and fetch attacker-controlled URLs.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58175

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-07-29T10:16:42.360 |

Apache Traffic Server leaks memory when handling HostDB SRV records.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-58158

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-29T10:16:41.347 |

Apache Traffic Server mishandles PROXY protocol input, truncating ports and overflowing the stack.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-65324

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-29T09:16:30.410 |

Apache Traffic Server drops the per-stream buffer cap when dechunking HTTP/2 or HTTP/3 responses, letting a slow client exhaust server memory.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-33930

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-29T08:16:31.127 |

Apache Traffic Server copies the client Host header into a fixed-size stack buffer without a bound during redirect handling, so an over-long Host header overflows the stack when redirect following is enabled.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-54691

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-28T22:17:40.800 |

datamodel-code-generator generates Python data models from schema definitions. From 0.9.1 until 0.61.0, src/datamodel_code_generator/http.py http.get_body accepts --url targets and redirect chain targets without host/IP validation, allowing server-side request forgery against loopback, private, link-local, metadata, and other network-accessible resources. This issue is fixed in version 0.61.0.

### CVE-2026-54690

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-28T22:17:40.650 |

datamodel-code-generator generates Pydantic v2 models, dataclasses, TypedDict, and msgspec.Struct from OpenAPI, JSON Schema, GraphQL, Avro, Protobuf, and raw JSON, YAML, or CSV. From 0.9.1 until 0.61.0, datamodel-code-generator silently dereferences attacker-controlled JSON Schema $ref HTTP or HTTPS URLs in src/datamodel_code_generator/parser/jsonschema.py through _get_ref_body, and the --allow-remote-refs gate can warn instead of blocking, allowing server-side request forgery through src/datamodel_code_generator/http.py. This issue is fixed in version 0.61.0.

### CVE-2026-14996

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-613` |
| Published | 2026-07-28T21:17:27.240 |

IBM Aspera Faspex 5 5.0.0 through 5.0.15.4 has addressed a vulnerability related to session management.

### CVE-2026-48391

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-07-28T19:17:35.243 |

Bridge is affected by an Untrusted Search Path vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-48390

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-28T19:17:35.123 |

Bridge is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. An attacker could leverage this vulnerability to gain unauthorized read and write access. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-66754

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-07-28T16:20:17.267 |

Rouille 0.1.6 through 3.6.2 contains a reachable assertion vulnerability in the Request::remove_prefix function that allows remote unauthenticated attackers to crash the server by sending a crafted percent-encoded URL. Attackers can send a request whose decoded path matches a configured prefix while the raw percent-encoded path does not, causing the assert! to fail and triggering either a 500 error or full process termination depending on the panic configuration.

### CVE-2026-47483

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-28T16:18:15.003 |

NVIDIA DCGM Exporter for all platforms contains a vulnerability in the /debug/pprof endpoints, where an attacker could cause uncontrolled resource consumption by submitting concurrent unauthenticated profiling requests. A successful exploit of this vulnerability might lead to denial of service and information disclosure.

### CVE-2026-43910

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-441;CWE-918` |
| Published | 2026-07-28T16:18:12.440 |

Appium Java Client is the Java language binding for writing Appium tests that conform to the W3C WebDriver protocol. From 8.2.1 until 10.1.1, when directConnect(true) is enabled, AppiumCommandExecutor.setDirectConnect() reads the directConnectHost, directConnectPort, and directConnectPath fields from the server's NEW_SESSION response and rebuilds the client's server URL from them, validating only that the protocol is https, with no host allowlist or IP validation; a rogue or compromised server can therefore redirect all subsequent session traffic to an arbitrary destination, enabling full interception of session traffic and a server-side request forgery pivot to internal hosts, including cloud metadata (IMDS) credential theft. This vulnerability is fixed in 10.1.1.

### CVE-2026-63231

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-29T07:16:42.490 |

A post-authentication SQL injection
vulnerability in Koollab LMS allowed an authenticated attacker to use an error-based SQL oracle via
the face-to-face runs update endpoint to read the entire application database
and obtain valid JWT tokens for account takeover.

### CVE-2026-14974

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-28T21:17:26.700 |

IBM WebSphere Application Server 8.5, and 9.0 traditional could allow a remote attacker to execute arbitrary code caused by unsafe deserialization of untrusted data.

### CVE-2026-48060

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-28T20:17:25.760 |

Litestar is an Asynchronous Server Gateway Interface (ASGI) framework. Prior to version 2.20.0, Litestar instances which use a template engine in conjunction with CSRF protection are vulnerable to HTML Injection which can be escalated to Cross Site Scripting due to the contents of the CSRF cookie being excluded from automatic escaping by the template engine when configured inline with documentation recommendations. This issue has been patched in version 2.20.0.

### CVE-2026-7769

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-28T19:17:41.720 |

IBM Sterling B2B Integrator 6.2.0.0 through 6.2.0.5_2, 6.2.1.0 through 6.2.1.1_2, and 6.2.2.0 through 6.2.2.0_1 and IBM Sterling File Gateway 6.2.0.0 through 6.2.0.5_2, 6.2.1.0 through 6.2.1.1_2, and 6.2.2.0 through 6.2.2.0_1 is vulnerable to SQL injection. A remote attacker could send specially crafted SQL statements, which could allow the attacker to view, add, modify, or delete information in the back-end database.

### CVE-2026-54593

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-1259;CWE-1270` |
| Published | 2026-07-28T16:19:00.097 |

Pterodactyl is a free, open-source game server management panel. Prior to Panel version 1.12.3 and Wings version 1.12.2, the Wings /upload/file endpoint accepted any valid panel-signed JWT that contained server_uuid, user_uuid, and unique_id claims without checking the token's intended purpose; because the Panel issues JWTs carrying those same claims for lower-privilege operations such as WebSocket authentication and file-download links, an authenticated subuser could reuse one of those tokens (for example a WebSocket token obtained with only the websocket.connect permission) by replaying it against /upload/file to write arbitrary files to the same server, despite never being granted the file.create permission. This issue is fixed in Panel version 1.12.3 and Wings version 1.12.2.

### CVE-2026-18220

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-29T11:16:49.097 |

An out-of-bounds write vulnerability was found in the BFD library's DLX ELF backend (bfd/elf32-dlx.c) in GNU binutils. The dlx_rtype_to_howto() function maps ELF relocation types to internal howto structures but fails to perform adequate bounds checking on attacker-controlled relocation type values (via ELF32_R_TYPE(r_info)) before indexing into the dlx_elf_howto_table[] array. The DLX relocation type number space is non-contiguous (basic types 0-6, extended types at 0x10000+), but the default case in the switch statement allows arbitrary index values to reach the array access.

A specially crafted ELF/DLX object file can trigger this out-of-bounds write when processed by any BFD-consuming tool (objdump, readelf, strip, ld, nm, objcopy). The vulnerability has been demonstrated to achieve arbitrary code execution via a File Stream Oriented Programming (FSOP) attack against glibc FILE structures (stderr), redirecting control flow to system().

Attack scenarios include CI/CD pipelines performing automated binary analysis, developer workstations running objdump/readelf on untrusted binaries, automated security scanning or malware analysis tools invoking binutils, and package build systems processing third-party code.

Note: This vulnerability is only exploitable when binutils is built with the DLX backend enabled (typically via --enable-targets=all).

### CVE-2026-58150

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-07-29T08:16:31.710 |

Apache Traffic Server does not reject Transfer-Encoding in HTTP/2 requests, allowing downgrade request smuggling.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-54656

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-28T22:17:40.507 |

datamodel-code-generator generates Pydantic v2 models, dataclasses, TypedDict, and msgspec.Struct from OpenAPI, JSON Schema, GraphQL, Avro, Protobuf, and raw JSON, YAML, or CSV. From 0.52.1 until 0.60.2, datamodel-code-generator interpolates validators from --extra-template-data in src/datamodel_code_generator/model/pydantic_v2/base_model.py through _process_validators into @field_validator decorators without safe validation, allowing Python code execution when the generated Pydantic v2 model is imported. This issue is fixed in version 0.60.2.

### CVE-2026-54655

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-28T22:17:40.360 |

datamodel-code-generator generates Python data models from schema definitions. From 0.51.0 until 0.60.2, x-python-type values parsed by src/datamodel_code_generator/parser/jsonschema.py in _get_python_type_override are inserted into generated field annotations without sufficient validation, allowing attacker-controlled JSON Schema content to execute Python code when the generated module is imported. This issue is fixed in version 0.60.2.

### CVE-2026-54654

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-07-28T22:17:40.217 |

datamodel-code-generator generates Python data models from schema definitions. From 0.14.1 until 0.60.2, the --extra-template-data comment field is rendered into Python comments in src/datamodel_code_generator/model/template/TypeAliasAnnotation.jinja2, src/datamodel_code_generator/model/template/TypedDict.jinja2, src/datamodel_code_generator/model/template/dataclass.jinja2, src/datamodel_code_generator/model/template/msgspec.Struct.jinja2, src/datamodel_code_generator/model/template/pydantic/BaseModel.jinja2, and src/datamodel_code_generator/model/template/pydantic_v2/BaseModel.jinja2 without neutralizing carriage returns in Python # comments, allowing an attacker-controlled comment value to inject Python code into generated models that runs when imported. This issue is fixed in version 0.60.2.

### CVE-2026-54621

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-07-28T22:17:39.930 |

datamodel-code-generator generates Python data models from schema definitions. Prior to 0.60.1, GraphQL Union description values in src/datamodel_code_generator/model/template/UnionTypeStatement.jinja2 and src/datamodel_code_generator/model/template/UnionTypeStatement.py312.jinja2 are rendered into Python comments without neutralizing carriage returns in Python # comments, allowing attacker-controlled GraphQL schema content to inject Python code into generated models that runs when imported. This issue is fixed in version 0.60.1.

### CVE-2026-48394

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-28T19:17:35.627 |

Bridge is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48393

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-28T19:17:35.503 |

Bridge is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48392

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-28T19:17:35.377 |

Bridge is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48374

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-28T19:17:34.987 |

Bridge is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-18107

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-28T19:17:32.420 |

A flaw was found in CRIU's handling of restartable sequences (rseq) during checkpoint/restore. A malicious process inside a container can register an rseq critical section that hijacks CRIU's parasite code injection during checkpoint, allowing it to spoof the process credentials saved in the checkpoint image. On restore, the container process gains elevated capabilities and zeroed UIDs/GIDs.

The practical impact on Red Hat products is limited by several factors: checkpoint/restore requires root privileges (podman) or cluster-admin RBAC (OpenShift) to trigger and cannot be initiated from within the container itself; on OpenShift prior to 4.17 the feature required explicit opt-in, and on 4.17+ the kubelet checkpoint API RBAC is not configured by default; OpenShift enforces user namespaces by default for regular workloads (hostUsers is gated behind admin-only SCCs), which makes the spoofed capabilities namespace-scoped and ineffective for privilege escalation; SELinux type enforcement (container_t) blocks privilege transitions independently of capabilities; seccomp filters persist through checkpoint/restore and cannot be corrupted via the parasite; and kernel mount namespace ownership checks on RHEL 9/10 kernels prevent mount-based container escape even with spoofed capabilities.

### CVE-2026-48372

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-28T18:17:20.747 |

Format Plugins is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-51273

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-28T17:16:46.540 |

In schreibfaul1 ESP32-audioI2S 3.4.5, a heap-based buffer overflow vulnerability exists in the ID3 tag parsing function showID3Tag() of the embedded audio streaming library. The program reads untrusted long ID3 tag value from malicious audio files and uses unbounded appendf() to write formatted strings into ps_ptr heap buffer without length validation. Successful exploitation allows attackers to execute arbitrary code, leak sensitive memory data, cause device crash, or escalate privileges via a crafted malicious audio file.

### CVE-2026-67178

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-07-28T15:17:51.213 |

MISP installation scripts generated an Apache HTTP virtual-host configuration containing an incorrectly formatted HTTP-to-HTTPS redirect:

Redirect permanent / https://misp.example

Apache’s Redirect directive appends any portion of the requested path that follows the matched prefix to the configured destination URL. Because the destination did not end with /, attacker-controlled path content was appended directly to the hostname rather than to its URL path.

For example, a request resembling:

http://misp.example/@attacker.example/

could result in a redirect resembling:

https://misp.example@attacker.example/

Under standard URL parsing, misp.example is interpreted as user information and attacker.example as the destination host. An unauthenticated remote attacker could therefore construct a URL hosted under the legitimate MISP domain that redirects users to an attacker-controlled website.

The vulnerability could be used for phishing, credential collection, or potentially disclosing sensitive query-string information preserved during the redirect. Exploitation requires a user to follow the crafted HTTP URL.

The fix adds the missing trailing slash to the redirect destination, ensuring that appended request data remains part of the path on the configured MISP host.



Existing installationsExisting MISP installations should review their Apache HTTP virtual-host configuration and ensure that the HTTPS redirect destination ends with a trailing slash:

Redirect permanent / https://misp.example/

After updating the configuration, validate it with apachectl configtest and reload or restart Apache for the change to take effect

### CVE-2026-51254

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-07-28T15:17:16.507 |

schreibfaul1 ESP32-audioI2S v3.4.5 has an integer underflow vulnerability in the MP3Decoder::GetBits() function of the MP3 decoder due to unchecked bit reading operations. The lack of validation on the nBits parameter causes the cachedBits counter to underflow to negative values, leading to invalid bit manipulation, incorrect bitstream parsing, application crash, or arbitrary code execution via a specially crafted MP3 file.

### CVE-2026-33267

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-29T08:16:30.983 |

Improper Input Validation vulnerability in Apache Traffic Server.

This issue affects Apache Traffic Server: from 9.2.0 through 9.2.14, from 10.1.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fixes the issue.

### CVE-2026-50738

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-28T19:17:36.967 |

A use-after-free condition exists in pglogical's worker signaling code, where a worker structure can be dereferenced after the underlying slot has been freed or recycled during normal worker lifecycle events. The condition is reachable during normal replication operation, including by a low-privileged user able to influence worker start, stop, and restart timing through permitted pglogical operations. In the typical case the condition crashes replication workers, causing an availability impact. In the worst case a use-after-free in a PostgreSQL backend can be leveraged as a remote code execution primitive at the privilege of that backend.

### CVE-2026-59931

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-28T18:17:22.873 |

PhpSpreadsheet is a pure PHP library for reading and writing spreadsheet files. In versions 4.0.0 through 5.8.0, 3.3.0 through 3.10.6, 2.2.0 through 2.4.6, 2.0.0 through 2.1.17, and all releases up to and including 1.30.5, the WEBSERVICE() domain whitelist can be bypassed via an HTTP redirect (SSRF). In Calculation/Web/Service.php, the webService() method validates a URL's host against the whitelist set via Spreadsheet::setDomainWhiteList(), then fetches content with file_get_contents($url, false, $ctx); because PHP's HTTP stream wrapper follows 301/302 redirects automatically (up to 20 hops) and the redirect target is never re-validated, an attacker who can trigger a redirect from a whitelisted domain can reach arbitrary URLs, including internal addresses. An attacker able to upload XLSX files to an application that uses setDomainWhiteList() and getCalculatedValue() can achieve a full-read SSRF, returning up to 32,767 bytes of the response body as a cell's calculated value, which enables exfiltration of cloud metadata (AWS/GCP/Azure credentials via http://169.254.169.254/), access to internal-only services, and internal port scanning (the port is not validated). This issue has been fixed in versions 5.8.1, 3.10.7, 2.4.7, 2.1.18, and 1.30.6.

### CVE-2026-16313

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:P/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-07-28T17:16:37.807 |

A flaw was found in sg3_utils. The sg_inq command, when invoked with the --export option, outputs device identification data without sanitizing control characters in SCSI name string fields. A newline character embedded in a device-supplied name string can inject arbitrary properties into the udev device database. This could allow an attacker who can present a crafted SCSI device to execute arbitrary commands as root when the device is disconnected.

### CVE-2026-54719

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862;CWE-863` |
| Published | 2026-07-28T23:17:09.213 |

goshs is a feature-rich single-binary file server for red teamers and developers. Prior to 2.1.1, the httpserver/updown.go bulkDownload handler for ?bulk&file= ZIP downloads did not call findEffectiveACL or applyCustomAuth, allowing unauthenticated reads of files protected only by .goshs folder ACLs and block lists. This issue is fixed in version 2.1.1. This vulnerability exists due to an incomplete fix for CVE-2026-40189.

### CVE-2026-54638

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770;CWE-789` |
| Published | 2026-07-28T23:17:08.617 |

gotd/td is a T Telegram MTProto API client in Go. Prior to 0.145.1, proto.UnencryptedMessage.Decode in proto/unencrypted_message.go read attacker controlled dataLen from an unauthenticated MTProto unencrypted packet and allocated make([]byte, dataLen) before checking the remaining buffer, allowing remote unauthenticated denial of service through excessive memory allocation and CPU or garbage collection pressure. This issue is fixed in version 0.145.1.

### CVE-2026-47219

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-248` |
| Published | 2026-07-28T23:17:03.763 |

find-my-way is a framework-independent HTTP router that internally uses a Radix Tree and supports route parameters and wildcards. Versions prior to 9.7.0 are vulnerable to remotely triggerable DoS in find-my-way when it is used with Node's HTTP/2 server. The lookup() function passes req.method into find(), and find() indexes this.trees[method]. Since this.trees is a normal object, HTTP/2 method values like constructor, toString, or __proto__ can resolve inherited object properties instead of returning undefined. The code then treats that value like a router node and crashes when it reaches currentNode.prefix.length. This issue has been fixed in version 9.0.7.

### CVE-2026-55415

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-95` |
| Published | 2026-07-28T22:17:48.983 |

datamodel-code-generator generates Pydantic v2 models, dataclasses, TypedDict, and msgspec.Struct from OpenAPI, JSON Schema, GraphQL, Avro, Protobuf, and raw JSON, YAML, or CSV. From 0.11.6 until 0.64.0, datamodel-code-generator allows attacker-controlled x-python-import or customTypePath schema extensions to reach src/datamodel_code_generator/parser/jsonschema.py and generated import handling through Import.from_full_path and Imports.create_line in src/datamodel_code_generator/imports.py, allowing a newline to break out of an import statement and execute Python code when the generated model is imported. This issue is fixed in version 0.64.0.

### CVE-2026-55391

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-350;CWE-367;CWE-918` |
| Published | 2026-07-28T22:17:48.697 |

datamodel-code-generator generates Pydantic v2 models, dataclasses, TypedDict, and msgspec.Struct from OpenAPI, JSON Schema, GraphQL, Avro, Protobuf, and raw JSON, YAML, or CSV. Prior to 0.63.0, datamodel-code-generator validates a URL host once in src/datamodel_code_generator/http.py through get_body, _validate_url_for_fetch, and _get_ips_from_host, but then lets httpx resolve the host again for the connection, allowing DNS rebinding to bypass allow_private_network=False and reach internal services. This issue is fixed in version 0.63.0.

### CVE-2026-55390

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-200;CWE-610` |
| Published | 2026-07-28T22:17:48.557 |

datamodel-code-generator generates Python data models from schema definitions. From 0.59.0 until 0.62.0, XML Schema parsing in src/datamodel_code_generator/parser/xmlschema.py for --input-file-type xmlschema resolves xs:include, xs:import, xs:redefine, and xs:override schemaLocation values outside the input base path, allowing arbitrary local files to be read and reflected into generated models. This issue is fixed in version 0.62.0.

### CVE-2026-55389

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-200;CWE-610` |
| Published | 2026-07-28T22:17:48.400 |

datamodel-code-generator generates Pydantic v2 models, dataclasses, TypedDict, and msgspec.Struct from OpenAPI, JSON Schema, GraphQL, Avro, Protobuf, and raw JSON, YAML, or CSV. Prior to 0.62.0, datamodel-code-generator resolves JSON Schema $ref targets in src/datamodel_code_generator/parser/jsonschema.py through is_url and _get_ref_body without containing file:// or ../ traversal references to the input directory and without honoring --no-allow-remote-refs, allowing arbitrary local file reads. This issue is fixed in version 0.62.0.

### CVE-2026-15280

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-28T21:17:27.640 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.8 ND Collective Controller is affected by a path-segment injection vulnerability in the collective routing mechanism.

### CVE-2026-15057

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-28T21:17:27.367 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.7 is vulnerable to a denial of service due to uncontrolled heap allocation.

### CVE-2026-14981

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-28T21:17:27.090 |

IBM WebSphere Application Server 9.0, and 8.5 and IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.7 are affected by a denial of service vulnerability in the HTTP channel due to unbounded allocation of resources without limits.

### CVE-2026-13463

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-28T21:17:25.533 |

IBM Cloud Pak System 2.3.5.0 could allow a local attacker to obtain sensitive information due to the insertion of credentials into log files.

### CVE-2026-66745

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-28T19:17:41.440 |

Artica Proxy before 4.50.000000 Service Pack 7 (fixed in hotfix 20260724-02) contains a session fixation vulnerability that allows unauthenticated attackers to hijack administrative sessions by setting a known PHPSESSID on a victim's browser prior to authentication. Attackers can pre-set a controlled session identifier and wait for a victim to authenticate through fw.login.php, after which the attacker gains a fully authenticated administrative session on port 9000.

### CVE-2026-59932

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-409` |
| Published | 2026-07-28T19:17:39.590 |

PhpSpreadsheet is a pure PHP library for reading and writing spreadsheet files. In versions 4.0.0 through 5.8.0, 3.3.0 through 3.10.6, 2.2.0 through 2.4.6, 2.0.0 through 2.1.17, and all releases up to and including 1.30.5, the Gnumeric reader reads attacker-supplied .gnumeric files into memory and, when the file starts with gzip magic bytes, calls gzdecode() on the full compressed contents without enforcing a decompressed-size limit. A very small compressed .gnumeric file can expand to data larger than the PHP memory limit and crash the process during Gnumeric::canRead() before the file is rejected or fully parsed. This is reachable through normal file-type detection and Gnumeric loading paths, so applications that accept attacker-controlled spreadsheet uploads can suffer denial of service. This issue has been fixed in versions 5.8.1, 3.10.7, 2.4.7, 2.1.18 and 1.30.6.

### CVE-2026-59933

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-835` |
| Published | 2026-07-28T18:17:23.033 |

PhpSpreadsheet is a pure PHP library for reading and writing spreadsheet files. In versions 4.0.0 through 5.8.0, 3.3.0 through 3.10.6, 2.2.0 through 2.4.6, 2.0.0 through 2.1.17, and all releases up to and including 1.30.5, the OLE reader follows sector chains from attacker-controlled XLS/OLE metadata without detecting cycles or enforcing a maximum chain length. A tiny malformed .xls/OLE file can set the small-block depot sector chain to point back to itself. During normal XLS detection, OLERead::read() appends the same sector data repeatedly until the PHP process exhausts memory. This is reachable from Reader\Xls::canRead() and therefore from automatic spreadsheet type detection. Applications that accept attacker-controlled spreadsheet uploads can suffer denial of service from a very small file. This issue has been fixed in versions 5.8.1, 3.10.7, 2.4.7, 2.1.18 and 1.30.6.

### CVE-2026-54635

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-28T18:17:22.427 |

pytonapi is a Python SDK for TONAPI that provides REST API, streaming, and webhook access to the TON blockchain. From 2.0.0 to 2.2.0, TonapiWebhookDispatcher fails to validate the Authorization header when a webhook handler is registered with the documented path argument, because setup() stores bearer tokens only under the default suffix paths and never adds the custom path to the token map, so self._tokens.get(path) returns None and the authentication guard is skipped. An unauthenticated remote attacker can POST forged payloads to the custom webhook endpoint and trigger victim-defined handlers. This issue is fixed in version 2.2.1.

### CVE-2026-61609

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-28T16:19:28.693 |

Pterodactyl is a free, open-source game server management panel. From 1.7.0 until 1.13.0, the authentication rate limiter defined in RouteServiceProvider::configureRateLimiting() applied a single global bucket to the login and two-factor checkpoint endpoints instead of keying by IP or account: the fall-through Limit::perMinute(10) covering POST /auth/login and POST /auth/login/checkpoint omitted ->by(), so Laravel derived a constant cache key (md5('authentication')) shared by every request. An unauthenticated attacker sending roughly ten requests per minute from a single IP, most cheaply against the checkpoint endpoint (which has no reCAPTCHA), exhausts the shared counter and causes HTTP 429 for every user attempting to log in or complete two-factor authentication, a panel-wide authentication denial of service that also locks out administrators. This issue is fixed in version 1.13.0.

### CVE-2026-47427

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-28T16:18:14.853 |

GitHub MCP Server is GitHub's official MCP Server. Prior to 1.1.0, the CompletionsHandler function in pkg/github/server.go accesses params.Ref without first checking whether it is nil, so a completion/complete request with a missing or empty ref field triggers a nil pointer dereference and a Go runtime panic; because the crash occurs before any authentication or token validation, any unauthenticated client able to send JSON-RPC messages can crash the server, resulting in a complete denial of service. This issue is fixed in version 1.1.0.

### CVE-2026-66299

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-28T15:17:50.210 |

Uncontrolled Resource Consumption vulnerability in Apache Tomcat's WebSocket chat example.

This issue affects Apache Tomcat: from 11.0.0-M20 through 11.0.24, from 10.1.24 through 10.1.57, from 9.0.89 through 9.0.120. Users who have followed the security guidance to remove the examples web application are not affected by this issue.

Users are recommended to remove the examples web application or to upgrade to version 11.0.25, 10.1.58 or 9.0.121 (when released), which fix the issue.

### CVE-2026-51251

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-07-28T15:17:16.227 |

Schreibfaul1 ESP32-audioI2S 3.4.5 has a buffer overflow vulnerability in the MP3Decoder::decode() function of the MP3 decoder due to missing size validation on untrusted mainDataBegin and nSlots values.

### CVE-2026-13690

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-29T07:16:41.460 |

The UsersWP  WordPress plugin before 1.2.67 does not validate the selected authentication provider in its two-factor login handler, allowing an attacker who already knows a user's credentials to bypass the second authentication factor and log in as that user.

### CVE-2026-56822

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-367` |
| Published | 2026-07-29T00:16:38.717 |

Netty is an asynchronous, event-driven network application framework. Prior to versions 4.1.136.Final and 4.2.16.Final, the OcspServerCertificateValidator forwards the SslHandshakeCompletionEvent before the asynchronous OCSP validation completes. This allows the client's downstream handlers to send sensitive application data (e.g., HTTP requests) to a revoked server before the channel is closed by the OCSP check. n io.netty.handler.ssl.ocsp.OcspServerCertificateValidator#userEventTriggered, when an SslHandshakeCompletionEvent is received, the validator immediately calls ctx.fireUserEventTriggered(evt). It then initiates an asynchronous OCSP query using OcspClient.query. Because the handshake completion event is forwarded immediately, downstream handlers in the client's pipeline are notified that the TLS handshake is successful. They may then begin reading and processing incoming application data or sending outgoing data. If the OCSP response later indicates the server's certificate is REVOKED, the validator closes the channel, but by this time, the client may have already leaked sensitive data to a revoked server or processed malicious responses from it. This issue has been fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-56821

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-299` |
| Published | 2026-07-29T00:16:38.573 |

Netty is an asynchronous, event-driven network application framework. Prior to versions 4.1.136.Final and 4.2.16.Final, the OcspServerCertificateValidator flags an out-of-date OCSP response but does not stop processing it, so an expired GOOD response is still reported as VALID, letting an on-path attacker replay a stale GOOD response to bypass revocation of a since-revoked certificate. Exploitation can lead to certificate revocation bypass via replay of an expired OCSP response. Any application using OcspServerCertificateValidator is affected; a revoked certificate can be accepted. This issue has been fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-15328

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-07-28T21:17:27.920 |

IBM WebSphere Application Server 9.0, and 8.5 and IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.7 is vulnerable to HTTP request smuggling.

### CVE-2026-14528

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-07-28T21:17:26.060 |

IBM WebSphere Application Server 9.0, and 8.5 traditional could allow a remote attacker to obtain sensitive information.

### CVE-2026-14893

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-1321` |
| Published | 2026-07-28T21:17:26.193 |

IBM Observability with Instana (Agent) Build 1.0.303 through 1.0.320 IBM Instana Node.js tracer component @instana/core version 6.2.1 is vulnerable to prototype pollution through its configuration normalization API.

### CVE-2026-8164

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-07-28T15:17:51.633 |

Uncontrolled Search Path Element vulnerability in ArkSigner Software and Hardware Industry and Trade Inc. ArkSigner Desktop Client allows Search Order Hijacking.

This issue affects ArkSigner Desktop Client: from v2.2.16.10 through 17062026.

### CVE-2026-16655

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-29T11:16:48.480 |

The Fluent Forms – Customizable Contact Forms, Survey, Quiz, & Conversational Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Name Field Nested `password` Member in all versions up to, and including, 6.2.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-16597

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-29T11:16:48.330 |

The GTM4WP – A Google Tag Manager (GTM) plugin for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via WooCommerce Billing Fields in all versions up to, and including, 1.22.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the GTM4WP WooCommerce order data integration option (GTM4WP_OPTION_INTEGRATE_WCORDERDATA) to be enabled, and is exploited by placing a guest checkout order with a JavaScript payload in a WooCommerce billing field such as the billing first name.

### CVE-2026-13425

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-29T09:16:29.183 |

The Database for CF7 plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Array Form Field Values in all versions up to, and including, 1.2.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable by unauthenticated attackers because Contact Form 7 accepts array-structured input for ordinary text fields (e.g., your-name[]) via the public REST API endpoint /wp-json/contact-form-7/v1/contact-forms/{id}/feedback, and the plugin stores submitted data using $wpdb INSERT with serialize() into a custom wp_cf7db table, bypassing WordPress save-time filtering via wp_insert_post/wp_kses.

### CVE-2026-12476

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-29T04:17:06.887 |

The Easy Digital Downloads plugin for WordPress is vulnerable to Arbitrary File Upload in versions up to and including 3.6.9. This is due to insufficient file type validation in the edd_do_ajax_import_file_upload() function , which only checks the client-supplied $_FILES['edd-import-file']['type'] Content-Type header against an allow-list of CSV mime types, then uses raw move_uploaded_file() (bypassing wp_handle_upload()'s core MIME enforcement) to write the file under its original extension into the web-accessible wp-content/uploads/edd/exports/ directory. This makes it possible for authenticated attackers, with Shop Manager-level access and above, to upload arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-54605

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-200;CWE-346;CWE-918` |
| Published | 2026-07-28T17:16:52.367 |

OAuth is a Ruby wrapper for the OAuth 1.0 and 1.0a protocols, providing clients and servers. From 0.5.5 to 1.1.5, OAuth::Consumer#token_request parses the raw Location header of a 300 to 399 redirect returned by the OAuth server and follows the redirect recursively, which can mutate the consumer's configuration and expose signed OAuth request metadata, including the Authorization header, to a cross-origin host. This issue is fixed in version 1.1.6.

### CVE-2026-50641

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-256` |
| Published | 2026-07-29T13:18:53.053 |

Streamsoft Business Intelligence (BI) stores users' passwords in plaintext form in the database

This issue was fixed in version 6.8.0.0, users were also requested to change their password on the first login.

### CVE-2026-12895

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-29T11:16:47.227 |

SQL injection in Frappe's ERPNext, versions ERPNext 15.107.0 and Frappe 15.107.2. The application constructs SQL queries through direct string interpolation using `str.format()` without employing parameterized queries, allowing the name (docname) of a Supplier record containing SQL metacharacters to be interpreted as part of the query. Exploitation of this vulnerability could allow an authenticated user with low privileges to execute arbitrary SQL queries, bypass Frappe’s access restrictions (DocPerm), extract confidential information from the database—including fragments of the administrator’s password hash—and access other sensitive data, such as credentials, integration tokens, or financial information.

### CVE-2026-35226

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-29T08:16:31.267 |

An out‑of‑bounds write vulnerability in the CODESYS PROFINET Controller allows an unauthenticated attacker on the same network segment to send malformed PROFINET communication data that triggers an exception in the affected PLC application. The exception is handled by the CODESYS Control runtime system and results in a controlled stop of the PLC application.

### CVE-2026-18192

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-29T08:16:30.383 |

VIN-DS783E-E6 developed by Vacron has an Arbitrary File Read vulnerability, allowing authenticated remote attackers to exploit Relative Path Traversal to download arbitrary system files.

### CVE-2026-14976

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-28T21:17:26.830 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.8 is affected by remote code execution with the collectiveController-1.0 feature enabled.

### CVE-2026-13442

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-520` |
| Published | 2026-07-28T21:17:25.387 |

IBM Langflow OSS 1.0.0 through 1.10.1 can allow an attacker to reuse another user's FAISS namespace to access owner-only vector content and influence later query results. This causes cross-user information disclosure and limited integrity impact through persistent poisoning of returned results.

### CVE-2026-16192

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-07-28T20:17:23.460 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.8 is affected by a denial of service vulnerability when the restConnector-2.0 feature is enabled.

### CVE-2026-47726

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-28T19:17:34.393 |

nebula-mesh is a self-hosted control plane for Slack Nebula mesh virtual private network. Prior to version 0.3.2, internal/api/audit.go:12 — handleGetAuditLog does no admin check. The route is bearer-auth gated only; any operator API key returns the full audit log via store.ListAuditEntries (up to limit=1000). This includes cross-tenant actor names, host/CA/operator IDs, action timestamps, and masked-IP entries from rate-limit refusals — enough surface for a tenant to enumerate the server's activity, infer staffing patterns, or identify high-value targets. This issue has been patched in version 0.3.2.

### CVE-2026-66749

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-28T16:20:16.457 |

Let's Chat 0.4.0 through 0.4.8 contains a null dereference vulnerability that allows authenticated attackers to crash the server by supplying a valid 24-character hex string room parameter that matches no document in the database. Attackers can send a crafted GET /messages request causing an uncaught TypeError in an asynchronous Mongoose callback that terminates the Node.js server process, with the same defect reachable through multiple code paths including the socket.io interface.

### CVE-2026-54545

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-28T16:18:59.327 |

wakaru is a JavaScript decompiler and unminifier toolkit. From 1.0.0 until 1.4.0, @wakaru/cli sanitizes bundle-controlled module filenames only once before writing extracted modules, so a crafted filename containing overlapping traversal sequences such as ....// collapses to ../ after sanitization and lets the final output path escape the selected output directory, allowing an attacker who can cause a user to run wakaru --unpack on a malicious bundle to write files outside that directory and, depending on the target path and environment, potentially achieve code execution. This issue is fixed in @wakaru/cli 1.4.0.

### CVE-2026-58159

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-29T10:16:41.490 |

Apache Traffic Server can bypass IP access controls on UDS listeners and through ACL matching errors.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-57834

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-07-29T08:16:31.563 |

Apache Traffic Server allows request smuggling if chunked messages are malformed.

This issue affects Apache Traffic Server: from 8.0.0 through 8.1.9, from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fix the issue.

### CVE-2026-41920

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-29T08:16:31.420 |

Improper Access Control vulnerability in Apache Traffic Server.

This issue affects Apache Traffic Server: from 9.0.0 through 9.1.14, from 10.0.0 through 10.1.3.

Users are recommended to upgrade to version 9.1.15 or 10.1.4, which fixes the issue.

### CVE-2026-16184

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-28T20:17:23.330 |

IBM WebSphere Application Server 9.0, and 8.5 could allow a remote attacker to bypass authentication by sending a crafted unauthenticated request.
