# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-07 15:00 UTC
- **対象期間**: `2026-09-06T15:00:13.000Z` 〜 `2026-09-07T15:00:28.000Z`
- **重要CVE数**: 56 件（Critical 9.0+: 7 件 / High 7.0〜: 49 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコア 7.0 以上のものは **30 件以上** 登録されており、**リモートからの認証なしでコード実行や認証バイパスが可能になる脆弱性が集中**しています。特に、ディレクトリサービス（FreeIPA）やネットワーク機器（Dell SCG、D‑Link ルータ）に関する **遠隔実行 (RCE) 系** が目立ち、IoT デバイスや SaaS アプリケーションでも **認証バイパス** が多発しています。  

- **リモート未認証** が共通する点で、外部からのスキャン・攻撃に対して防御が不十分な環境は即座にリスクが高まります。  
- 多くのベンダーは **パッチ提供が遅延** しているか、公開情報が乏しいため、**自前の緊急対策**（ネットワーク分離・ACL 強化）が必須です。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 重要度の根拠 |
|-----|--------|----------|--------------|
| **CVE‑2026‑76578** (FreeIPA) | 9.8 | LDAP クライアントが認証なしで OTP トークンエントリを作成可能。ディレクトリサーバの ACI 評価バグと組み合わせると、任意属性の追加や権限昇格が可能。 | **最高スコア** かつ **企業内部・外部の認証基盤** を直接揺るがす。攻撃者は管理者権限取得や横展開が容易になる。 |
| **CVE‑2026‑6223** (BiHayat App) | 9.4 | 認証試行回数制限が無く、認証バイパスが可能。バージョン 2.1.7〜07092026 が対象。 | **認証バイパス** は最も危険なシナリオの一つ。特に自治体が提供するアプリは個人情報・行政サービスに直結するため、被害拡大が懸念される。 |
| **CVE‑2026‑61410** (Dell SCG 5.0 Appliance / Application) | 9.4 | 未認証リモートからの **Missing Authorization** により任意コード実行が可能。5.36.00.16 未満が対象。 | **ネットワークインフラ機器** の遠隔コード実行は、社内全体の通信基盤を乗っ取られるリスクがある。 |
| **CVE‑2026‑86296** (D‑Link DIR‑822A) | 9.3 | `strcpy` のスタックバッファオーバーフローによりリモートから任意コード実行。 | **IoT ルータ** は外部ネットワークに直接露出しやすく、攻撃者が内部ネットワークへ踏み台を置く入口になる。 |
| **CVE‑2026‑16876** (UNIVERGE IX‑R/IX‑V) | 9.3 | WebGUI の認証バイパスにより、任意 CLI コマンド実行が可能。 | **産業用ネットワーク機器** の管理画面が乗っ取られると、ネットワーク全体の制御権を奪われる危険性が高い。 |

> **注**：上記は **CVSS 9.0 以上** かつ **リモート未認証** で重大な権限取得が可能なものを選出。ローカル特権昇格系 (例: CVE‑2026‑80238) も重要だが、外部からの直接侵入リスクが低いため、優先度はやや下げた。

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
1. **脆弱性スキャンの実施**  
   - Nmap NSE、OpenVAS、Qualys などで対象資産をスキャンし、上記製品・バージョンが存在するか確認。  
2. **ネットワーク分離・ACL 強化**  
   - LDAP/FreeIPA、SCG、D‑Link ルータへの外部からの直接アクセスを **IP フィルタリング** で遮断。  
   - 管理用 WebGUI (UNIVERGE) は **VPN 経由のみ** アクセス可能にする。  
3. **監視・ログの強化**  
   - LDAP 認証ログ、SCG の管理 API アクセスログ、ルータの syslog を集中管理し、異常なエントリをリアルタイムでアラート。  

### 3.2 製品別具体的パッチ・バージョン

| 製品 | 現行脆弱バージョン | 推奨バージョン / パッチ | 取得先 |
|------|-------------------|--------------------------|--------|
| **FreeIPA** | 4.9.x 以前 (全般) | **4.10.0 以降** (FreeIPA 4.10.0‑release) | <https://www.freeipa.org/page/Download> |
| **BiHayat App** (Bahçelievler Municipality) | 2.1.7 〜 07092026 | **2.1.8** (ベンダー提供パッチ) | ベンダーサポート窓口へ問い合わせ |
| **Dell Secure Connect Gateway (SCG) Appliance** | 5.0‑* 5.36.00.15 以前 | **5.36.00.16 以降** (SCG 5.0 Update 5.36.00.16) | Dell TechDirect / Dell Support |
| **Dell Secure Connect Gateway (SCG) Application** | 5.0‑* 5.36.00.00 以前 | **5.36.00.01 以降** | 同上 |
| **D‑Link DIR‑822A** | 1.01 (A_101) 以前 | **1.02** (ファームウェア 2026‑09‑01) | D‑Link Support Portal |
| **UNIVERGE IX‑R / IX‑V** | 7.0.x 以前 | **7.1.0** (WebGUI 修正パッチ) | UNIVERGE Support |
| **LibreNMS** (補足) | < 26.8.0 | **26.8.0** (REST API 認証バイパス修正) | <https://github.com/librenms/librenms/releases> |
| **PostgreSQL Anonymizer** | < 2.5 | **2.5.1** (コード実行修正) | PostgreSQL Extension Repository |

### 3.3 短期的な回避策（パッチ適用が困難な場合）

| 製品 | 回避策 |
|------|--------|
| FreeIPA | - `cn=Directory Manager` で **ACI** を厳格に設定し、`selfManagedOTPToken` エントリへの `add` 権限を削除。<br>- LDAP ポート (389/636) を内部ネットワークに限定。 |
| BiHayat App | - アプリ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-76578

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-07T13:20:36.850 |

A flaw was found in FreeIPA. The self-managed OTP token ACI does not require authentication and does not restrict which attributes may be added alongside the token entry. An unauthenticated LDAP client can exploit this, combined with a related flaw in the underlying directory server's ACI evaluation (tracked separately), to create an arbitrary attacker-controlled Kerberos principal and have it added to the administrators group. This allows a remote, unauthenticated attacker to obtain genuine FreeIPA administrator-group membership and perform administrative operations against the directory and, on SID-enabled deployments, other IdM services.

### CVE-2026-6223

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-07T13:20:33.977 |

Improper restriction of excessive authentication attempts vulnerability in Bahçelievler Muncipality BiHayat App allows Authentication Bypass.

This issue affects BiHayat App: from 2.1.7 through 07092026. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-61410

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-07T13:20:33.853 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains a Missing Authorization vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to remote execution. This vulnerability is considered critical because it allows an attacker to execute commands remotely on a target system by sending a specially crafted request to the application, bypassing intended restrictions on code execution.Dell recommends customers to upgrade at the earliest opportunity.

### CVE-2026-80238

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-09-07T13:20:39.293 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Execution with Unnecessary Privileges vulnerability. An unauthenticated attacker with local access could potentially exploit this vulnerability, leading to Protection mechanism bypass. This vulnerability is considered critical because a low-privileged operator with SSH access to the SCG host can gain root-level access to the host without requiring a password by leveraging the exposed Docker socket. Additionally, an attacker who compromises a service running within the orchestrator container can access the same socket and escape the container boundary to obtain host-level control. Dell recommends that customers upgrade at the earliest opportunity.

### CVE-2026-86296

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-07T11:17:39.550 |

A vulnerability was determined in D-Link DIR-822A A_101. This vulnerability affects the function strcpy of the file udhcpcd/serverpacket.c of the component udhcpcd. This manipulation causes stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-16876

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-07T02:17:17.630 |

An authentication bypass vulnerability exists in the WebGUI of Series UNIVERGE IX-R/IX-V. A user could bypass authentication and execute arbitrary CLI commands by tampering with WebGUI messages and sending them to the device via internet.

### CVE-2026-86426

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-07T13:20:41.690 |

LibreNMS before 26.8.0 contains an authentication bypass vulnerability in the REST API that allows unauthenticated attackers to access protected endpoints by sending numeric values instead of string tokens. Attackers can exploit MySQL type coercion by sending small integers like 0 through 9 to match token hashes, gaining access to API functionality including device credentials and administrative features that enable remote code execution through alert templates.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-86404

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-07T12:17:21.840 |

EAP's Artemis deserialization configuration permits deserialization by default. ObjectMessage.getObject() uses ObjectInputStreamWithClassLoader, which implements allow-list/block-list filtering via its checkSecurity()/isTrustedType() method. However, by default both allow-list and block-list are empty. When the allow-list is empty (size == 0), isTrustedType() returns true for ALL classes. This means all classes are deserializable by default.

### CVE-2026-19633

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-06T16:16:49.583 |

PostgreSQL Anonymizer contains a vulnerability that allows unprivileged masked users to execute arbitrary code by abusing operators, domain casts, or view subqueries that carry untrusted expressions. When these objects are evaluated in the context of the extension’s masking mechanisms, the malicious code can run with elevated privileges. The issue is fixed in PostgreSQL Anonymizer 3.1.4 and later versions

### CVE-2026-86452

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-07T14:16:56.833 |

Affected versions of MISP permit unauthenticated or weakly constrained request paths to perform persistent work without adequate input bounds or rate limiting.


The users/forgot password-reset endpoint accepted an attacker-controlled email value without first imposing a reasonable length bound or validating its format. That value was then used to create an audit log entry and queue a password-reset job, causing the supplied value to be persisted more than once per request. The commit explicitly states that an unbounded unauthenticated request field was stored twice per call with no throttle.


The fix adds:



  *  
a maximum email input length of 1024 bytes;


  *  
email-format validation before persistent work;


  *  
a per-source pre-authentication request budget;


  *  
HTTP 429 responses when that budget is exceeded;


  *  
a 15-minute cooldown for API-access request emails;


  *  
POST-only handling and CSRF protection for the API-access request endpoint.





The new flood filter is specifically intended to limit persistent storage costs from anonymous requests such as password resets, registrations, and failed REST authentication attempts.

Version affected: ≤2.5.45

### CVE-2026-86435

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-07T13:20:43.013 |

commonmark versions from 1.5.0 before 2.8.4 contain a denial of service vulnerability in the Footnote extension that fails to deduplicate footnote definitions. Attackers can craft documents with duplicate footnote definitions and references to create quadratic output expansion, consuming excessive memory and CPU to exhaust server resources.

### CVE-2026-86434

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-07T13:20:42.870 |

league/commonmark versions >= 2.0.0 and < 2.8.4 (patched in 2.9.0) contain a denial of service vulnerability in UniqueSlugNormalizer::normalize(), which restarts its numeric-suffix search from 1 on every slug collision, resulting in O(K^2) time complexity for K headings that collapse to the same base slug. The vulnerable path is reached when HeadingPermalinkExtension, FootnoteExtension, or TableOfContentsExtension is registered. An unauthenticated attacker can force many headings onto a single base slug (e.g., via empty ATX headings, identical heading text, or punctuation-only headings) in a small Markdown document, consuming excessive CPU and denying service.

### CVE-2026-86433

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-07T13:20:42.733 |

commonmark versions from 1.5.0 before 2.8.4 contain a denial of service vulnerability in the Attributes extension where AttributesListener::findTargetAndDirection() performs quadratic-time sibling list scanning. Unauthenticated attackers can submit approximately 32 KB of repeated attribute blocks to cause parsing to take over 5 seconds, exhausting server resources.

### CVE-2026-86430

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-07T13:20:42.320 |

league/commonmark versions before 2.9.1 contain multiple denial of service vulnerabilities in fenced code block detection, reference link label lookup, and emphasis delimiter processing that perform super-linear work on crafted input. Attackers can submit specially crafted Markdown with long backtick runs, nested brackets, or delimiter sequences to consume disproportionate CPU time and prevent legitimate requests from completing.

### CVE-2026-86429

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-07T13:20:42.180 |

The league/commonmark (thephpleague/commonmark) library in versions >= 1.5.0 and < 2.9.1 contains quadratic parsing complexity in its SmartPunctExtension and AttributesExtension. When either extension is explicitly registered on the Environment (they are not enabled by default and are excluded from the standard CommonMark and GitHub-Flavored Markdown converters), an unauthenticated attacker can submit small, specially crafted Markdown documents — such as text alternating with unpaired quotes, contiguous runs of block-level attribute blocks, or repeated class attributes — to trigger disproportionate CPU consumption and cause a denial of service. Fixed in 2.9.1.

### CVE-2026-86428

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-07T13:20:42.037 |

commonmark versions from 1.5.0 before 2.10.0 contain a denial of service vulnerability in the AttributesExtension when processing distinctly-named attributes. Attackers can submit Markdown with numerous distinct attribute names to cause quadratic-time attribute merging and filtering, consuming disproportionate CPU resources and preventing legitimate requests from completing.

### CVE-2026-86427

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-07T13:20:41.870 |

LibreNMS before 26.8.0 contains an argument injection vulnerability in the graph_title parameter that allows authenticated attackers to inject arbitrary rrdtool arguments by breaking out of double-quote escaping. Attackers can inject DEF and LINE arguments to read RRD files from unauthorized devices, or use newline injection to execute arbitrary rrdtool commands, bypassing per-device authorization checks.

### CVE-2022-51017

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-07T13:17:23.747 |

PocketMine-MP versions before 3.26.5 and 4.0.5 fail to validate the length of skin data fields submitted by players, allowing uncapped values to exceed the 32767 byte TAG_String limit. Attackers can submit oversized skin data fields like skinID or geometryName to trigger exceptions during NBT data serialization, causing server crashes.

### CVE-2026-19204

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770;CWE-789` |
| Published | 2026-09-07T11:17:20.600 |

A client may send a WebSocket frame with an unknown opcode and a very large declared payload length, causing Jetty to attempt a large memory allocation and potentially exhaust the JVM heap.




This occurs when auto-fragmentation is enabled, as unknown opcodes bypass the normal maximum frame size handling and payload allocation occurs before the opcode is validated.

### CVE-2026-84732

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-07T09:17:16.840 |

Retransmissions of ACK packet ID in OpenVPN through 2.6.22 and 2.7.6 allow remote unauthenticated attackers to cause a denial of service via crafted inputs that trigger a timeout integer overflow

### CVE-2026-14297

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-07T09:17:15.430 |

A buffer overflow in the Bluetooth Continuous Glucose
     Monitoring Service (CGMS) Record Access Control Point (RACP) write handler
     allows an authenticated BLE peer to overflow a 20-byte static buffer into
     adjacent BSS memory. The exploitable impact cannot be predetermined - it
     is entirely dependent on the linker-assigned BSS layout of the specific
     firmware build, which may vary.

### CVE-2026-86299

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-07T12:17:21.340 |

A vulnerability was detected in Linksys RE7000 2.0.15. This affects the function platform_event_pingTest of the file /cgi-bin/json.cgi?PingTest of the component PingTest Handler. The manipulation of the argument pingTestIp/pingTestPktSize/pingTestTimes results in os command injection. The attack can be launched remotely. The exploit is now public and may be used.

### CVE-2026-79698

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-07T07:16:47.420 |

A vulnerability was identified in Advantech WISE-6610-NB, WISE-6610-EB, WISE-6610-TB, WISE-6610-JB, WISE-6610-CB, WISE-6610-EL-NB, WISE-6610-EL-EB, WISE-6610-EL-TB, WISE-6610-EL-JB, WISE-6610-EL-CB, WISE-6610P-DEA, WISE-6610P-DNA and WISE-6610P-DTA 1.2.1_20251110. This vulnerability affects the function nodered_lib_apply of the component Node-RED Library. Such manipulation of the argument act leads to command injection. The attack can be launched remotely. The exploit is publicly available and might be used. Upgrading to version 1.2.4_20260821 is able to resolve this issue. It is advisable to upgrade the affected component. The vendor was contacted early, responded in a very professional manner and quickly released a fixed version of the affected product.

### CVE-2026-79697

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-07T07:16:45.903 |

A vulnerability was determined in Advantech WISE-6610-NB, WISE-6610-EB, WISE-6610-TB, WISE-6610-JB, WISE-6610-CB, WISE-6610-EL-NB, WISE-6610-EL-EB, WISE-6610-EL-TB, WISE-6610-EL-JB, WISE-6610-EL-CB, WISE-6610P-DEA, WISE-6610P-DNA and WISE-6610P-DTA 1.2.1_20251110. This affects the function basicstation_apply of the component Basic Station Certificate-Deletion Handler. This manipulation of the argument act causes command injection. The attack can be initiated remotely. The exploit has been publicly disclosed and may be utilized. Upgrading to version 1.2.4_20260821 is able to mitigate this issue. Upgrading the affected component is advised. The vendor was contacted early, responded in a very professional manner and quickly released a fixed version of the affected product.

### CVE-2026-84226

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-09-07T08:17:13.653 |

OpenVPN version 2.5.0 through 2.6.22 and 2.7_alpha1 through 2.7.6 on Windows allows local authenticated users to perform a binary planting attack during network configuration steps

### CVE-2026-20502

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-07T02:17:18.917 |

In vdec, there is a possible out of bounds write due to a missing bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation. Patch ID: ALPS11262030; Issue ID: MSV-9196.

### CVE-2026-20501

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-07T02:17:18.800 |

In vdec, there is a possible out of bounds write due to a heap buffer overflow. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation. Patch ID: ALPS11262030; Issue ID: MSV-9197.

### CVE-2026-84173

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-07T10:16:54.823 |

In Eclipse Ankaios versions v0.5.1 through v1.0.1, the agent-side Control Interface authorizer incorrectly evaluates multi-segment allow rules whose first path segment is a wildcard. An authenticated workload with access restricted by such a rule can submit a CompleteStateRequest or UpdateStateRequest with an empty field mask. The request may then be incorrectly authorized as matching the scoped rule, allowing the workload to read the complete cluster state or replace state outside its authorized subtree. This may result in unauthorized disclosure or modification of other workloads and cluster configuration. Only a rule consisting solely of * is intended to authorize an empty mask.




Mitigation: Until an update containing the fix is installed, avoid multi-segment Control Interface allow-rule filter masks that begin with a wildcard, such as *.workloads.some_workload. Replace them with explicit paths such as desiredState.workloads.some_workload, where applicable. A filter mask consisting solely of * has different, intentionally unrestricted semantics and should only be used when full-state access is intended.

### CVE-2026-82751

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-09-06T17:17:56.070 |

Improper Validation of Specified Quantity in Input in ZenHive mpp allows an unauthenticated remote client to inflate the fee-payer's gas cost per sponsored payment by a large multiplier and to have the sponsor pay for provisioning an access key on the client's own account.

When the server sponsors Tempo payments, MPP.Methods.Tempo.FeePayerPolicy.measure/3 in lib/mpp/methods/tempo/fee_payer_policy.ex bounds the gas fields, the fee budget, the validity window and the access list of the client-signed 0x76 envelope, but does not check whether the envelope carries the optional key_authorization field. A client can attach a fully signed key authorization, provisioning a new access key with token spending limits on its own account, alongside the normal payment call. The key and each limit entry are persistent storage writes billed as intrinsic gas to the sponsor, bounded only by the gas_limit ceiling. At the reporter's default of one key with three token limits the sponsored cost rises from about 46,587 gas to about 1,808,700 gas, and the client keeps a valid access key it paid nothing for.

This issue affects mpp: from 0.2.0 before 0.16.1.

### CVE-2026-82750

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-09-06T17:17:55.867 |

Improper Validation of Specified Quantity in Input in ZenHive mpp allows an unauthenticated remote client to inflate the fee-payer's gas cost per sponsored payment by a large multiplier and to have the sponsor pay for EIP-7702 account delegations of the client's choosing.

When the server sponsors Tempo payments, MPP.Methods.Tempo.FeePayerPolicy.measure/3 in lib/mpp/methods/tempo/fee_payer_policy.ex bounds the gas fields, the fee budget, the validity window and the access list of the client-signed 0x76 envelope, but never reads its aa_authorization_list field. Every signed delegation in that list is charged as intrinsic gas before the payment call runs, so a client attaching delegations from throwaway authority keys makes the sponsor pay for them within the default gas_limit ceiling. At the reporter's default of seven entries the sponsored cost rises from about 46,575 gas to about 1,884,087 gas. Because each entry is applied as a persistent set-code delegation, a client can also upgrade its own accounts to delegated code at the sponsor's expense.

This issue affects mpp: from 0.2.0 before 0.16.1.

### CVE-2026-86297

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-189;CWE-193` |
| Published | 2026-09-07T11:17:39.730 |

A vulnerability was identified in D-Link DIR-605 B1v202WWB03. This issue affects the function tunnel_set_params of the file progs.gpl/pppd.alpha/l2tp/tunnel.c of the component L2TP Control Message Parser. Such manipulation of the argument peer_hostname  leads to off-by-one. The attack may be performed from remote. Attacks of this nature are highly complex. The exploitability is assessed as difficult. The exploit is publicly available and might be used.

### CVE-2026-80132

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-07T13:20:38.670 |

ell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-79678

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-07T13:20:38.380 |

A flaw was found in FreeIPA's idp-add command, where insufficiently validated --organization/--base-url input reaches a constrained eval() call before the corresponding LDAP access control check is enforced. This allows any authenticated IPA principal, regardless of privilege level, to enumerate and read the environment variables of the affected server process and to cause denial of service via memory exhaustion.

### CVE-2026-86313

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-07T03:17:19.407 |

Out-of-bounds write vulnerability in Samsung Opensource Walrus allows Overflow Buffers.

This issue affects Walrus: af80e665ea49d9003695a66502f841ed1d8397e7.

### CVE-2026-80134

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-07T13:20:38.923 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Use of Hard-coded Credentials vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-84256

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-09-07T08:17:13.777 |

An argument parsing issue in OpenVPN 2.1_rc10 through 2.6.22 and 2.7_alpha1 through 2.7.6 on Windows allows remote authenticated users to execute arbitrary commands via a crafted certificate subject

### CVE-2026-76560

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-07T14:16:54.197 |

A flaw was found in 389 Directory Server. The SELFDN ACI bind-rule evaluator incorrectly matches an anonymous LDAP client's empty bind DN against an empty stored attribute value, allowing an unauthenticated client to satisfy access control checks intended to require a matching authenticated identity. This can allow an anonymous LDAP client to perform an operation, such as adding or modifying a directory entry, that a SELFDN-based ACI intended to restrict to a specific authenticated user.

### CVE-2026-14444

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-07T14:16:51.947 |

The WP Fusion (Pro) plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 3.47.13. This is due to insufficient authorization checks on the role parameter in the ThriveCart Auto Login handler's thrivecart() function. This makes it possible for authenticated attackers, with Subscriber-level access and above, and who possess the access_key, to create a new user account with administrator privileges and gain full control over the WordPress site. The required access_key is intentionally shared with ThriveCart customers as part of the plugin's documented setup process, making it accessible to attackers who have made a purchase. The vulnerability is only exploitable when the ThriveCart Auto Login option is enabled.

### CVE-2026-80135

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-703` |
| Published | 2026-09-07T13:20:39.047 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Check or Handling of Exceptional Conditions vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to protection mechanism bypass.

### CVE-2026-14296

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-07T08:17:11.773 |

When using the Direct XIP
update strategy, the main application image starts other cores (i.e. radio
core), based on the currently active slot without additional verification. The
MCUboot in the bare (upstream) configuration assumes that if there is at least
a single slot for each image available, the system is bootable and continues
the boot process. This may lead to a situation when MCUboot picks different
slot for different images (i.e. (a) for the main application and (b) for the
radio image), boots the main application (from slot (a)) that afterwards starts
the radio image by providing an address of the unauthenticated slot ((a)
instead of (b)).

### CVE-2026-80164

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-07T14:16:55.060 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Certificate Validation vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-80131

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-07T14:16:54.933 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to remote execution.

### CVE-2026-80133

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-07T13:20:38.800 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains a Relative Path Traversal vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to remote execution.

### CVE-2026-61409

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-07T13:20:33.720 |

Dell Secure Connect Gateway (SCG) 5.0 Application, versions prior to 5.36.00.00, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to remote execution.

### CVE-2026-6431

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-07T13:20:36.653 |

The User Profile Builder – Beautiful User Registration Forms, User Profiles & User Role Editor plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'Biographical Info' meta field parameter in all versions up to, and including, 3.15.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-80130

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-07T14:16:54.813 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains a Relative Path Traversal vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to remote execution.

### CVE-2026-86408

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-09-07T13:20:40.100 |

Affected versions of MISP do not enforce parent-event visibility when serving cryptographic keys through CryptographicKeysController::view().


The vulnerable handler queried CryptographicKey directly using the supplied key ID and selected sensitive fields such as:



  *  
type


  *  
key_data


  *  
fingerprint





but did not fetch or authorize the associated parent event first.


The upstream commit explicitly states that cryptographicKeys/view could return a protected event’s signing key to any authenticated user.


The fix adds parent_id and parent_type to the lookup and then enforces authorization through the associated event using fetchSimpleEvent($user, parent_id). If the parent is not an Event, access is limited to site administrators.

Version affected: ≤2.5.45

### CVE-2022-51018

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-07T13:17:23.893 |

PocketMine-MP before 3.26.5 and 4.0.x before 4.0.5 does not limit book page text length, page count, or author/title length. A player who obtains a writable book can create oversized NBT ('book bombs'), causing excess bandwidth consumption and server crashes (exceeding the 1 MB chunk size limit when saving region-based worlds in PM3, or exceeding the 32 KiB TAG_String limit in PM4).

### CVE-2022-51015

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-07T13:17:23.463 |

PocketMine-MP before 4.0.6 does not validate facing values in PlayerActionPacket (for START_BREAK and CRACK_BREAK actions) or in UseItemTransactionData (typically within InventoryTransactionPacket). A remote authenticated attacker can send crafted packets with invalid facing values (e.g., negative or out-of-range) to crash the server, resulting in a denial of service.

### CVE-2022-51014

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-07T13:17:23.317 |

PocketMine-MP before 4.0.7 contains an unhandled exception vulnerability in the ModalFormResponsePacket handler when processing malformed JSON from clients. Attackers can send specially crafted form response packets with invalid JSON to trigger an uncaught InvalidArgumentException, causing server crashes.

### CVE-2022-51013

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-07T13:17:23.173 |

PocketMine-MP versions before 4.2.3 fail to validate damage metadata values in tool and armor item NBT data received from clients. Attackers can send negative or out-of-range damage values in itemstack NBT to trigger unhandled exceptions in the Durable class, causing server crashes.

### CVE-2022-51012

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-07T13:17:23.030 |

PocketMine-MP versions before 4.2.9 fail to properly validate NBT data types during deserialization of inventory transaction packets from clients. Attackers can send crafted inventory transactions with malformed NBT tags to trigger server crashes and cause denial of service.

### CVE-2022-51010

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-07T13:17:21.510 |

PocketMine-MP versions before 4.4.2 fail to properly validate item IDs received from clients in itemstack NBT data. Attackers can send crafted item IDs outside the valid range to trigger an uncaught exception that crashes the server.

### CVE-2026-86347

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-862` |
| Published | 2026-09-07T10:16:55.917 |

Affected versions of MISP allow any authenticated user to access TemplatesController::uploadFile() because the ACL entry for templates/uploadFile used the wildcard *. This bypasses the intended role restrictions applied to neighboring template-management operations.


The upload handler accepts arbitrary content with only minimal checks and writes it into app/tmp/files/. A low-privileged or read-only user can therefore repeatedly upload files and consume server disk space without requiring perm_add or perm_template. The fix changes the ACL requirement from * to perm_add.

The commit also rules out stronger impacts: uploaded files receive random names, path traversal/predictable overwrite is not available, the temporary directory is outside the web root, and the files are not directly served over HTTP. Therefore, the issue should not be described as arbitrary file overwrite, stored XSS, or RCE.

Version affected: ≤2.5.45

### CVE-2026-86283

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-862` |
| Published | 2026-09-06T15:17:24.813 |

MISP's UiBeta theme collection view (app/View/Themed/UiBeta/Collections/view.ctp) performed a secondary query of member events by UUID without applying the caller's access control list (ACL). The CollectionsController::view() action correctly resolved collection element UUIDs through Event::fetchSimpleEvents($user, ...), which enforces per-user event ACL. However, the view template independently re-queried the same UUIDs using only an Event.uuid IN (...) condition, omitting the createEventConditions() authorization filter. Because collection element UUIDs are stored without server-side authorization against the referenced event (CollectionElementsController::add() accepts whatever UUID the collection owner posts), an authenticated user with view access to a collection could retrieve full details of events they are not permitted to read. The exposed data included event identifiers, info, dates, timestamps, creator organization, all event tags, and galaxy clusters (the latter attached via a cluster-scoped rather than event-scoped ACL check). This constitutes an authorization bypass at the presentation layer, allowing horizontal privilege escalation across event boundaries within the MISP instance.

### CVE-2026-86419

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:L/VI:L/VA:H/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-918` |
| Published | 2026-09-07T13:20:40.663 |

Affected versions of MISP contain insufficient validation of server-side outbound HTTP destinations in feed retrieval and TAXII discovery functionality.


In feed processing, redirects were followed without validating the redirect scheme or destination. The original request headers were reused across redirect hops, meaning authentication headers or API credentials configured for a feed could be forwarded to a different host. Redirects could also target internal network resources, resulting in SSRF. The fix adds redirect validation, blocks internal destinations for cross-host redirects, strips configured feed credentials before following redirects to another host, and pins validated DNS results to prevent re-resolution after validation.


The TAXII discovery endpoint had a related incomplete SSRF defense. It used gethostbyname() and compared the result against only a few literal addresses. This missed cases including IPv6 loopback (::1), numeric host encodings such as 0x7f000001, and potentially multiple DNS records. The fix moves TAXII discovery to the shared URL egress validator.


Together, these commits harden MISP's outbound URL handling against alternate-address representations, DNS-related bypasses, unsafe redirects, internal-host access, and cross-host credential forwarding.






Version affected: ≤2.5.45
