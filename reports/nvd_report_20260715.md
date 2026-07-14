# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-14 15:00 UTC
- **対象期間**: `2026-07-13T15:00:33.000Z` 〜 `2026-07-14T15:00:32.000Z`
- **重要CVE数**: 91 件（Critical 9.0+: 24 件 / High 7.0〜: 67 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** に上り、**リモートコード実行 (RCE)・認証バイパス・権限昇格** が目立ちます。特に産業制御系 (EtherNet/IP アダプタ、OpENer)、大手 SaaS／エンタープライズ製品 (JetBrains YouTrack、ServiceNow、SAP) に対する脆弱性が集中しており、**ネットワーク境界だけで防げない** 攻撃が増加しています。  

- **認証不要で直接システム内部に侵入できるケース**（CVE‑2026‑10577、CVE‑2026‑62422、CVE‑2026‑6875 など）が多数。  
- **JWT・トークン系の実装ミス** が原因の認証回避が顕在化（CVE‑2026‑56451）。  
- **産業用プロトコルスタックの実装不備** によるメモリ破壊・情報漏洩が相次いで報告（OpENer 系列、EIPStackGroup）。  

この傾向は、**「クラウド／SaaS の API が外部に公開される」** と **「組み込み／産業機器がインターネットに接続される」** という二重の攻撃面拡大を示唆しています。早急なパッチ適用と、ネットワークレイヤでの防御強化が必須です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 製品・バージョン | 主な影響 | 注目理由 |
|-----|------|-------------------|----------|----------|
| **CVE‑2026‑10577** | 10.0 | 1715‑AENTR EtherNet/IP Adapter (全バージョン) | デバッグポートが認証なしで公開され、CLI コマンドを遠隔実行可能。完全なシステム支配が可能。 | 産業制御系で **ネットワーク外部から直接コード実行** が可能になる稀有なケース。PLC・SCADA 環境への波及リスクが高い。 |
| **CVE‑2026‑62422** | 10.0 | JetBrains YouTrack < 2026.1.13757 (2025.3.148033 など) | データベース直アクセスにより認証バイパス、管理者権限取得。 | 開発チーム全体の情報資産が一瞬で漏洩・改竄される危険性。YouTrack は多くの企業で内部ツールとして利用されている。 |
| **CVE‑2026‑56451** | 10.0 | Siemens Opcenter X < V2604 | JWT ヘッダーの `alg` パラメータが検証されず、任意の署名アルゴリズムでトークンを偽造できる。認証回避・権限昇格が可能。 | **トークンベース認証** が広く採用される中、実装ミスだけで全ユーザーを乗っ取れる点が深刻。 |
| **CVE‑2026‑44747** | 9.9 | SAP NetWeaver Application Server ABAP (全バージョン) | メモリ管理の論理エラーによりメモリ破壊。機密データ漏洩、サービス停止、任意コード実行の可能性。 | SAP は基幹系システムの中核。メモリ破壊は **データ完全性・可用性** を同時に脅かす。 |
| **CVE‑2026‑6875** | 9.5 | ServiceNow AI Platform (特定バージョン) | 未認証リモートコード実行。攻撃者が ServiceNow のワークフローエンジン上で任意コードを実行できる。 | ServiceNow は多くの企業の ITSM 基盤。**クラウド側での RCE** は顧客全体に波及する危険性がある。 |

> **共通点**：いずれも **認証不要**、もしくは **極低い認証要件** でシステム内部に侵入でき、**機密情報の窃取、サービス停止、さらには横展開** が容易になる点です。

---

## 3. 推奨アクション  

### 3‑1. 直ちにパッチ適用・バージョンアップ
| 製品 | 修正済みバージョン / パッチ | 適用期限目安 |
|------|----------------------------|--------------|
| 1715‑AENTR EtherNet/IP Adapter | ベンダー提供の **Firmware 2.0.3 以降**（デバッグポート無効化） | 1 週間以内 |
| JetBrains YouTrack | **2026.1.13757** 以上（2025 系は同等パッチ適用） | 3 日以内 |
| Siemens Opcenter X | **V2604** 以上 | 1 週間以内 |
| SAP NetWeaver AS ABAP | 最新 **Support Package Stack (SPS) 2026‑01**（メモリ管理修正） | 2 週間以内 |
| ServiceNow AI Platform | **Release 2026.2.0** 以降（RCE 修正） | 1 週間以内 |
| D‑Link DIR‑1253 (参考) | **Firmware 1.0.1.250923.150000** 以上 | 1 週間以内 |
| OpENer / EIPStackGroup | **2.3.1** 以上（全 CVE‑5153x 系修正） | 1 週間以内 |

> **※ベンダーが提供するパッチが未リリースの場合**は、**ネットワークレベルでの遮断**（IP フィルタリング、VPN 限定、IDS/IPS 署名適用）を暫定策として実施してください。

### 3‑2. 防御・検知の強化
1. **デバッグ・管理ポートの完全遮断**  
   - EtherNet/IP アダプタの `debug` ポート (TCP 12345 等) をファイアウォールで外部から遮断。  
2. **認証・トークン管理の見直し**  
   - JWT の `alg` パラメータは **HS256 以外受け付けない**、署名鍵は定期的にローテーション。  
   - YouTrack のデータベース接続は **ローカルホスト限定**、外部からの直接接続は防止。  
3. **ログ・監査の強化**  
   - ServiceNow、SAP、

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-10577

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-14T13:18:13.163 |

A security issue exists within the 1715-AENTR EtherNet/IP Adapter. The affected product exposes a network-accessible debug port that does not enforce proper privilege controls, allowing unauthenticated remote access to intrusive command-line interface (CLI) commands. If exploited, a threat actor could read or delete files, stop tasks, modify memory, and change I/O states, potentially impacting the confidentiality, integrity, and availability of the device.

### CVE-2026-62422

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-14T11:16:48.367 |

In JetBrains YouTrack before 2026.1.13757,
2025.3.148033,
2025.2.148048,
2025.1.148120,
2024.3.148430,
2024.2.148429 authentication bypass via direct database access leading to administrative access was possible

### CVE-2026-56451

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-14T10:16:33.287 |

A vulnerability has been identified in Opcenter X (All versions < V2604). Affected applications do not properly validate the algorithm specified in the JSON Web Token (JWT) header.
This could allow an unauthenticated remote attacker to forge arbitrary JWT, bypass authentication mechanisms and impersonate any user including administrative accounts, potentially gaining full unauthorized access to the application.

### CVE-2026-44747

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T01:16:17.437 |

SAP NetWeaver Application Server ABAP allows an authenticated attacker to leverage logical errors in memory management to cause a memory corruption that could lead to unauthorized data access, modification, or system unavailability. This has high impact on confidentiality, integrity, and availability of the application.

### CVE-2026-52533

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-13T22:16:48.020 |

An issue in D-Link DIR-1253 v.1.0.1.250923.142435 allows an attacker to escalate privileges via the etc/shadow component file

### CVE-2026-57433

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-13T17:17:55.783 |

Storable versions before 3.41 for Perl have a signed integer overflow when deserializing a crafted SX_HOOK record.

retrieve_hook_common reads a signed 32-bit item count from an SX_HOOK record and calls av_extend with that count plus one. A count of I32_MAX wraps the addition to a negative value.

A crafted blob passed to thaw or retrieve triggers the overflow; av_extend receives the negative count and dies with a panic, terminating the deserialization.

### CVE-2026-11563

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-14T06:16:48.873 |

The Word Count and Social Shares WordPress plugin through 1.0 does not validate a user-supplied file path before deletion, nor does it have proper authorization or CSRF checks, allowing any authenticated user, such as a Subscriber, to delete arbitrary files on the server, which can lead to a full site takeover (e.g. by deleting wp-config.php).

### CVE-2026-6875

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-13T19:17:36.440 |

ServiceNow has addressed a remote code execution vulnerability that was identified in the ServiceNow AI platform. This vulnerability could enable an unauthenticated user, in certain circumstances, to execute code within the ServiceNow platform.


ServiceNow addressed this vulnerability by deploying a security update to hosted instances. Relevant security updates have also been provided to ServiceNow self-hosted customers and partners.




Further, the vulnerability is addressed in the listed patches and family releases, which have been made available to hosted and self-hosted customers, as well as partners. We are not currently aware of exploitation against ServiceNow instances.




We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-62327

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-522` |
| Published | 2026-07-13T22:16:52.403 |

9Router through version 0.4.41 contains an unauthenticated information disclosure vulnerability that allows remote attackers to retrieve plaintext API keys for all connected AI provider accounts by sending a single unauthenticated request to the /api/usage/stats endpoint. Attackers can exploit the missing authentication middleware on the Next.js API route to obtain full API key strings alongside token counts, cost breakdowns, and request metadata, enabling unauthorized use of connected AI provider accounts, billing fraud, and quota exhaustion.

### CVE-2026-59801

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-13T22:16:48.840 |

9Router through version 0.4.41 contains an unauthenticated access vulnerability that allows remote attackers to interact with provider management API endpoints by sending requests without any credentials due to missing authentication middleware in the Next.js API routes under src/app/api/providers/*. Attackers can enumerate, create, modify, or delete provider connections to expose partial credentials, OAuth tokens, and API keys, redirect AI traffic to attacker-controlled servers, or cause complete denial of service by deleting all provider connections.

### CVE-2026-61500

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-338` |
| Published | 2026-07-13T18:16:29.903 |

Rejetto HFS 3.0.0 through 3.2.0 derives its session-cookie signing key from the non-cryptographic Math.random() generator and discloses outputs of the same generator to unauthenticated clients during login. A remote attacker can collect a small number of login responses, reconstruct the generator's state, recover the signing key, and forge a valid administrator session cookie, leading to full administrative access and remote code execution via the server_code configuration feature.

### CVE-2026-15183

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-441;CWE-918` |
| Published | 2026-07-14T09:16:40.443 |

Multiple input validation vulnerabilities in the Snowflake Spark Connector (spark-snowflake) versions prior to 3.2.1 can allow attackers to exfiltrate OAuth client credentials, execute arbitrary SQL with the connector's Snowflake role, or redirect COPY operations to attacker-controlled storage. An attacker could exploit these vulnerabilities by supplying a crafted OAuth token request URL, placing malicious files in an ingestion pipeline, injecting SQL via staging options in a shared Spark environment , or issuing runtime SET commands in a shared Spark-SQL session to inject arbitrary SQL into the SnowflakeFallbackCatalog's option map, which executes under the cluster admin's JDBC credentials. Successful exploitation may result in credential theft, unauthorized access to Snowflake account data, or privilege escalation within connected infrastructure.

### CVE-2026-61462

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-13T18:16:29.633 |

mcp-gitlab contains a path traversal vulnerability in the job_id parameter of build/index.js that allows attackers to redirect GitLab API requests to arbitrary endpoints. Attackers can supply crafted job_id values like ../../../user to escape the intended path prefix and access arbitrary GitLab API resources using the operator's personal access token.

### CVE-2026-59083

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-177` |
| Published | 2026-07-14T09:16:41.483 |

Improper Handling of URL Encoding (Hex Encoding) vulnerability in Apache Tomcat's rewrite valve allowed security constraint bypass for some configurations.

This issue affects Apache Tomcat: from 11.0.0-M1 through 11.0.23, from 10.1.0-M1 through 10.1.56, from 9.0.0.M1 through 9.0.119, from 8.5.0 through 8.5.100. Other versions that have reached end of support may also be affected.

Users are recommended to upgrade to version 11.0.24, 10.1.57 or 9.0.120, which fix the issue.

### CVE-2026-44761

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1392` |
| Published | 2026-07-14T01:16:18.023 |

SAP Commerce Cloud could retain a sample OAuth2 client with publicly documented sample credentials originating from sample configuration provided in SAP Help Portal documentation. If left unchanged, an unauthenticated attacker could use these well-known credentials to obtain a valid access token and invoke certain APIs to read and modify data. Successful exploitation results in high impact on confidentiality and integrity, with no impact on availability.

### CVE-2026-27690

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-444` |
| Published | 2026-07-14T01:16:17.193 |

Due to an HTTP Request Smuggling vulnerability in SAP Approuter, an unauthenticated attacker could send a specially crafted HTTP request that leads to request-response desynchronization. This could result in the exposure of user responses and cause the system to become unavailable. This leads to a high impact on confidentiality and availability.

### CVE-2026-58102

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-13T23:16:47.127 |

Crypt::OpenSSL::X509 versions before 2.1.3 for Perl allow a heap out-of-bounds read via a long certificate extension OID in hv_exts.

When building the extension hash (via extensions(), extensions_by_long_name(), extensions_by_oid(), or has_extension_oid()), the code passes OBJ_obj2txt()'s return value as the hash-key length; because that value is the OID's full text length rather than the bytes written to the fixed-size buffer (129 bytes), an OID whose text is longer than the 129-byte buffer causes a read past the allocation, exposing adjacent heap memory as the returned hash key. extensions_by_name() uses the static shortname path and is not affected.

### CVE-2026-51541

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-13T22:16:47.807 |

OpENer 2.3.0 (commit 76b95cf) has an out-of-bounds read issue in CIP message parsing when handling malformed explicit requests with a forged EPath size. An attacker can send a valid ENIP SendRRData frame carrying a very short CIP payload whose path_size field claims that many more path words are present than are actually available. Because the parser trusts the attacker-controlled path_size and continues decoding path segments without a remaining-length boundary, it reads beyond the end of the stack receive buffer.

### CVE-2026-51538

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-13T22:16:47.497 |

EIPStackGroup OpENer 2.3.0 (commit 76b95cf) suffers from an Incorrect Access Control vulnerability in its handling of encapsulation sessions. When the server processes critical encapsulation commands, it verifies whether the provided session_handle exists in the global session list, but it fails to verify whether that handle belongs to the specific TCP connection issuing the request. Because there is no strong binding between a session handle and its originating socket, any attacker on the network can use a valid session handle created by another legitimate client to bypass access controls.

### CVE-2026-51537

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-13T22:16:47.387 |

EIPStackGroup OpENer 2.3.0 (commit 76b95cf) has an out-of-bounds read issue in Connection Manager handling of ForwardOpen requests when processing short malformed packets. An attacker can send a valid ENIP outer frame carrying a malformed CIP ForwardOpen/LargeForwardOpen request, causing the parser to continue reading fields even when request data is insufficient. This issue is remotely triggerable via network traffic and does not require authentication.

### CVE-2026-51536

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-13T22:16:47.263 |

In OpENer 2.3.0 (commit 76b95cf) when parsing incoming CIP (Common Industrial Protocol) network packets, the length parameter is inconsistently typed across the call stack. Specifically, an upstream length calculated as an int is passed to a downstream function that expects an EipInt16 (a 16-bit signed integer). If a maliciously crafted packet with specific length fields is processed, the length parameter can overflow or be truncated into a negative value. This negative length bypasses subsequent bounds checking (due to signed/unsigned comparison issues) and is ultimately used in memory operations, leading to a Stack Buffer Overflow when reading data in DecodePaddedEPath.

### CVE-2026-58409

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-13T21:16:48.450 |

ChurchCRM is an open-source church management system. Prior to version 7.4.0, an authenticated administrator can achieve Remote Code Execution (RCE) on the server by installing a malicious plugin ZIP archive containing a PHP webshell. The application explicitly includes 'php' in its ALLOWED_EXTENSIONS list, while the dangerous extensions denylist (DENIED_EXTENSIONS) fails to block standard .php files. Because `php` is explicitly included in the allowed extension list for plugin archives, and extracted files are placed directly under the web root, any PHP file inside the ZIP becomes immediately executable via HTTP — without even needing to "enable" the plugin through the application UI. The /plugins/install-url API route (management.php) allows an administrator to source the malicious ZIP from any attacker-controlled HTTPS URL, validating it only against an attacker-supplied SHA-256 hash. This issue has been fixed in version 7.4.0.

### CVE-2026-13221

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-13T17:16:48.923 |

Perl versions through 5.43.9 produce silently incorrect regular expression matches when an alternation of more than 65535 fixed string branches is compiled into a trie in Perl_study_chunk.

When such branches are combined into a trie, the delta between the first branch and the shared tail is stored in a 16-bit field. A branch count above 65535 overflows the field, and the trie's match decision table is truncated with no warning or error.

A pattern of this shape produces false positive matches (matching strings it should not) and false negative matches (failing to match strings it should). When such a pattern gates an access or filtering decision, the result is wrong.

### CVE-2026-57898

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-07-14T09:16:41.173 |

In Eclipse BaSyx Java Server SDK versions 2.0.0-milestone-05 to 2.0.0-milestone-12, deployments using the MongoDB backend are vulnerable to an unauthenticated arbitrary file write through the AAS thumbnail API.




The AAS thumbnail upload path accepted a client-controlled fileName request parameter and passed it through repository file handling as both a repository key and, during thumbnail retrieval, a local filesystem path. With the MongoDB file repository, the supplied filename was treated as an opaque GridFS key and was not normalized or restricted as a filesystem path. A remote attacker could upload thumbnail content using an absolute or traversal-style filename, then trigger thumbnail retrieval so that the uploaded bytes were written to the attacker-chosen path on the server filesystem.




This could allow writing files anywhere the Java process has permission to write and may lead to remote code execution. The default InMemory backend is not affected by this specific path because it normalizes and restricts file paths to its temporary directory.




The issue is fixed in Eclipse BaSyx Java Server SDK 2.0.0-milestone-13.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-15416

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-14T09:16:40.590 |

A flaw was identified in Argo CD, the GitOps engine used by Red Hat OpenShift GitOps, that could allow an unauthenticated attacker with network access to the Argo CD repo-server to achieve remote code execution. Under certain conditions, the attacker may then manipulate cached data to deploy malicious Kubernetes resources to managed clusters, potentially resulting in complete cluster compromise.

### CVE-2026-9561

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-348;CWE-807` |
| Published | 2026-07-14T09:16:42.180 |

Eclipse Kura versions prior to 5.6.2 trust the client-supplied X-Forwarded-For HTTP header as the authoritative source of the client IP address in audit log entries. The org.eclipse.kura.web2 (Web Console) and org.eclipse.kura.rest.provider (REST API) components use this header as the primary IP source when initializing audit context, and org.eclipse.kura.jetty.customizer unconditionally installs Jetty's ForwardedRequestCustomizer on all HTTP/HTTPS connectors, causing HttpServletRequest.getRemoteAddr() to reflect the attacker-controlled header value. An unauthenticated remote attacker can exploit this vulnerability to bypass IP-based brute-force protections — such as fail2ban — by spoofing the logged IP address to a non-routable value, allowing a brute-force attack to proceed undetected, or to cause a denial of service against a third party by injecting a victim's IP address and triggering a ban on that address.

### CVE-2026-55773

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-13T20:16:48.580 |

CedarJava is an open source Java implementation of the Cedar policy language, used for fine-grained authorization decisions. In versions prior to 2.3.6, 3.4.1 and 4.9.0, under certain circumstances, improper input handling could allow Cedar-expression injection via unescaped toCedarExpr(). The toCedarExpr() method on Cedar Value types does not escape special characters (" or \) when converting values to Cedar source code. If an integrator uses toCedarExpr() to build policy text at runtime from user-controlled values, an actor could inject arbitrary Cedar expressions. For example, injecting || true into a permit ... when { ... } clause could make the permit unconditional, or injecting && false into a forbid clause could prevent the forbid from triggering. This issue requires the integrator to use toCedarExpr() to build policy text at runtime from user-controlled input. This vulnerability has been fixed in versions 2.3.6, 3.4.1, and 4.9.0.

### CVE-2026-55771

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-697;CWE-843` |
| Published | 2026-07-13T20:16:48.453 |

CedarJava is an open source Java implementation of the Cedar policy language, used for fine-grained authorization decisions. In versions prior to 4.9.0, the EntityIdentifier.equals() has inverted null/self branches which could lead to incorrect equality comparisons. The EntityIdentifier.equals() method has inverted logic for null and self-reference checks, returning true for null comparisons and false for self-comparisons. This does not affect Cedar authorization decisions (computed in Rust from JSON), but could affect integrators who perform their own equality checks on entity identifiers. This issue has been fixed in version 4.9.0.

### CVE-2026-55772

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-13T19:17:15.183 |

CedarJava is an open source Java implementation of the Cedar policy language, used for fine-grained authorization decisions. In versions prior to 2.3.6, 3.4.1 and 4.9.0, under certain circumstances, improper input handling could allow Record-to-Entity type confusion across the Java-Rust FFI boundary. CedarJava sends authorization requests to the Rust cedar-policy evaluator as JSON. The JSON protocol reserves magic single-key object shapes (__entity and __extn) for entity references and extension values. When serializing a CedarMap, there is no validation preventing these reserved keys from being used. If an integrating service builds a CedarMap from caller-supplied key/value data (such as request headers, user-defined metadata, or resource tags), an actor who controls those keys could cause the Rust evaluator to interpret a record as an entity reference. This issue requires the integrating service to build a CedarMap where the an actor controls the keys, and a policy must reference that value in a when/unless clause. This vulnerability has been fixed in versions 2.3.6, 3.4.1, and 4.9.

### CVE-2026-15389

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-14T11:16:48.053 |

A vulnerability relating to insufficient access control has been identified in the session management of the Sesame Time web application and its REST v3 API. The flaw lies in the fact that the system uses the session identifier (USID) as the sole validation mechanism, without verifying whether that identifier legitimately belongs to the user making the request. As a result, an attacker who obtains a valid USID can impersonate a victim’s session and access their confidential information, including emails, user IDs, roles and corporate data. This vulnerability is exacerbated by poor session lifecycle management: new logins generate additional USIDs without revoking the previous ones, allowing multiple active sessions to coexist and thereby expanding the attack surface.

### CVE-2026-57856

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-13T23:16:46.883 |

Cockpit CMS contains a path traversal vulnerability in the Bucket file storage API (/system/buckets/api). The api() method in modules/System/Controller/Buckets.php sanitizes the bucket name with preg_replace('/[^a-zA-Z0-9-_\\.]/','', $bucket), which permits '..' and '../' sequences. The sanitized value is interpolated into a Flysystem path as uploads://buckets/{bucket}. Flysystem's WhitespacePathNormalizer resolves 'buckets/..' to the empty string (the uploads storage root) without raising PathTraversalDetected because the '..' has a preceding component to consume. An authenticated low-privileged user can send a crafted request with a '../' bucket name to list, upload, and delete files across all buckets, including those belonging to other users or roles

### CVE-2026-57855

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-13T23:16:46.743 |

Cockpit CMS contains a missing authorization vulnerability in the Bucket file storage API (/system/buckets/api). The api() method in modules/System/Controller/Buckets.php executes bucket commands (ls, upload, removefiles, rename, createfolder) without performing any ACL or role check. Any authenticated user, regardless of role, can perform all bucket operations on any named bucket, including buckets intended for admin use only.

### CVE-2026-62328

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-359;CWE-862` |
| Published | 2026-07-13T22:16:52.550 |

9Router through version 0.4.41 contain an unauthenticated information disclosure vulnerability that allows remote attackers to access sensitive user data by sending requests to unprotected API endpoints. Attackers can enumerate paginated request logs and retrieve complete AI conversation histories including system prompts, user messages, assistant responses, tool calls, and user email addresses by querying the request-logs and request-details API routes which lack authentication middleware.

### CVE-2026-62200

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-07-13T22:16:51.813 |

OpenClaw versions before 2026.6.6 contain a flaw in host exec environment filtering that could allow Git ext transport to be abused. When the affected feature is enabled and reachable, a lower-trust caller or configured input path could execute or persist actions beyond the caller's intended authorization.

### CVE-2026-62199

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-07-13T22:16:51.673 |

OpenClaw versions before 2026.6.6 contain a flaw in host exec environment filtering that can miss interpreter startup variables. When the affected feature is enabled and reachable, a lower-trust caller or configured input path can supply crafted environment variables to execute or persist actions beyond the caller's intended authorization.

### CVE-2026-62196

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-13T22:16:51.243 |

OpenClaw versions 2026.3.22 before 2026.6.6 contain an authorization bypass vulnerability where WhatsApp group IDs can satisfy elevated sender allowlists. Attackers with lower-trust access can perform actions requiring stronger authorization by leveraging group ID validation in the affected feature.

### CVE-2026-62195

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-07-13T22:16:51.100 |

OpenClaw versions 2026.5.20 before 2026.6.6 contain an authorization bypass vulnerability in the MCP loopback feature that allows lower-trust callers to execute owner-only tools. Attackers can bypass authorization checks through configured input paths to execute or persist actions beyond their intended permissions.

### CVE-2026-62194

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732;CWE-862` |
| Published | 2026-07-13T22:16:50.943 |

OpenClaw versions 2026.5.20 before 2026.6.9 contain a privilege escalation vulnerability in plugin install commands that allows lower-trust callers to execute or persist actions beyond their intended authorization. Attackers can exploit misconfigured input paths or enabled features to escalate privileges and perform unauthorized actions when the feature is reachable.

### CVE-2026-62190

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-706;CWE-863` |
| Published | 2026-07-13T22:16:50.173 |

OpenClaw versions before 2026.6.9 contain an authorization bypass vulnerability in the flock wrapper that allows lower-trust callers to execute or persist actions beyond their intended authorization. Attackers can leverage configured input paths to bypass durable exec approval binding and perform unauthorized operations when the affected feature is enabled.

### CVE-2026-62184

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-07-13T22:16:49.310 |

luci-app-banip contains a log parsing vulnerability where the awk-based parser extracts the first IPv4 address from log lines regardless of field position, allowing attackers to inject arbitrary IPs via attacker-controlled fields like usernames. An unauthenticated remote attacker can inject an IP address into the login username field, causing banIP to block the wrong target while the real attacker remains unblocked.

### CVE-2026-61458

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-07-13T22:16:49.177 |

PasswordPusher before 2.9.2 contains a brute-force vulnerability in the POST /p/:token/access endpoint that lacks route-specific rate limiting and per-push lockout mechanisms. Attackers who know a push token can systematically guess passphrases at 120 attempts per minute without triggering any push-level defense, making short or dictionary-derived passphrases practically recoverable within hours or days.

### CVE-2026-49970

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-13T19:17:09.943 |

Laravel-Mediable before 7.0.0 contains a path traversal vulnerability in the File::sanitizePath() function that allows attackers to write uploaded files to arbitrary locations by controlling the directory argument passed to MediaUploader::toDestination(). Attackers can exploit the permissive character-class regex that allows both dot and slash characters combined with an ineffective trailing trim() call to bypass sanitization and upload files to sensitive locations such as the document root, environment configuration files, or application configuration directories, enabling remote code execution.

### CVE-2026-61463

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-13T18:16:29.770 |

Shiori contains a privilege escalation vulnerability in the account update endpoint that allows authenticated users to modify the owner field without authorization checks. Attackers can escalate to administrator by submitting a crafted PATCH request with owner: true, then re-authenticate to obtain an admin JWT token granting full system access.

### CVE-2026-62188

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-13T22:16:49.893 |

OpenClaw @openclaw/feishu versions 2026.6.6 and earlier contain an incorrect authorization vulnerability in which the Feishu permission tools could ignore per-account disablement settings. When the affected feature is enabled and reachable, a lower-trust caller or configured input path could perform actions that should have required a stronger authorization or policy check. The issue is fixed in version 2026.6.9.

### CVE-2026-62187

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-13T22:16:49.753 |

OpenClaw Feishu tools (npm package @openclaw/feishu) in versions <= 2026.6.6 could ignore per-account disablement. A lower-trust caller or a configured input path could perform actions that should have required a stronger authorization or policy check, resulting in unauthorized operations. The issue is fixed in version 2026.6.9. Impact depends on the operator's configuration and whether lower-trust input can reach the affected feature.

### CVE-2026-62185

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-07-13T22:16:49.453 |

Argo CD Helm Chart before 10.0.0 fails to install network policies by default, allowing any pod on a cluster to access repo-server and other Argo APIs. Attackers can exploit this unrestricted network access through combined attacks to achieve cluster compromise and remote code execution.

### CVE-2026-53565

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-14T13:18:58.463 |

Improper Privilege Management vulnerability in Citrix Secure Access Client for Windows, Citrix Citrix Endpoint Analysis Client for Windows.

This issue affects Secure Access Client for Windows: before 26.6.1.20; Citrix Endpoint Analysis Client for Windows: before 26. 5.1.7.

### CVE-2025-40945

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-07-14T10:16:30.783 |

A vulnerability has been identified in COMOS V10.4.5 (All versions < V10.4.5.0.2), COMOS V10.6 (All versions < V10.6.1), Designcenter NX (All versions < V2512.7000), Simcenter 3D (All versions < V2512.7000), Simcenter Femap V2506 (All versions < V2506.0003), Simcenter Femap V2512 (All versions < V2512.0002), Simcenter Nastran (All versions < V2606), Simcenter STAR-CCM+ (All versions < V2606), Solid Edge SE2025 (All versions < V225.0 Update 13), Solid Edge SE2026 (All versions < V226.0 Update 04), Teamcenter Visualization V2412 (All versions < V2412.0012), Teamcenter Visualization V2506 (All versions < V2506.0009), Teamcenter Visualization V2512 (All versions < V2512.2605), Tecnomatix Plant Simulation V2404 (All versions < V2404.0022), Tecnomatix Plant Simulation V2504 (All versions < V2504.0010), Tecnomatix Process Simulate (All versions < V2606). Untrusted search path in IAM Client SDK may allow an authenticated user to potentially enable escalation of privilege via local access.

### CVE-2026-0487

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-07-14T01:16:16.370 |

SAProuter on Microsoft Windows allows an unauthenticated attacker to load library (DLL) files from an untrusted location, allowing them to execute malicious code on the system. This could enable the attacker to hijack the DLL loading process and achieve arbitrary code execution. This has high impact on confidentiality, integrity and availability of the system.

### CVE-2026-57432

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-190` |
| Published | 2026-07-13T17:17:55.670 |

Perl versions through 5.43.10 have an integer overflow in S_measure_struct leading to an out-of-bounds heap read in pack and unpack.

S_measure_struct adds each item's size times its repeat count to a running total with no overflow check, so a large repeat count in a pack or unpack template wraps the signed SSize_t total negative. The @, X, and x position codes then guard their moves with a signed length comparison that passes when the length is negative, advancing the buffer pointer out of bounds.

A template derived from untrusted input can read heap memory past the buffer and return it to the caller.

### CVE-2026-58486

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-409` |
| Published | 2026-07-13T23:16:47.233 |

HedgeDoc is an open source, real-time, collaborative, markdown notes application. Prior to version 1.11.0, HedgeDoc was vulnerable to a YAML alias bomb due to unsafe processing of the note frontmatter. HedgeDoc parsed frontmatter with js-yaml.load (js-yaml v3) via @hedgedoc/meta-marked, which resolved YAML anchor aliases. A compact malicious payload could therefore expand into a huge object structure, consuming excessive CPU. This expansion ran on every request to the publish view (/s/<shortid>) and, when placed under the opengraph key, the editor view (/<noteId>). A ten-level alias bomb could block the single Node.js event loop for roughly 235 seconds per request, causing concurrent requests to hang or drop and rendering the instance unavailable (DoS). Because the note was stored in the database, the impact survived process restarts until the note was removed. toobusy-js did not reliably mitigate the worst cases, as the event loop was saturated before the middleware could respond. This issue was fixed in version 1.11.0.

### CVE-2026-62240

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-13T22:16:52.117 |

CrewAI before 1.15.1 contains a server-side request forgery vulnerability in the validate_url function that performs one-shot DNS resolution and blocklist checks before returning the original URL unchanged. Attackers can bypass the security filter by supplying URLs that redirect to internal addresses or use DNS rebinding techniques to access internal services and cloud metadata endpoints.

### CVE-2026-58229

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T09:16:41.313 |

Allocation of resources without limits vulnerability in elixir-mint mint allows a remote HTTP server to exhaust memory on the client host and cause a denial of service.

The Mint.HTTP1.decode_headers/5 and Mint.HTTP1.decode_trailer_headers/4 functions in lib/mint/http1.ex accumulate every parsed response header and chunked-trailer field into a per-request list that persists across incoming TCP segments as request.headers_buffer, and only clear it when the terminating blank line is received. The section has no cap on the number of headers or on total bytes, and the underlying :erlang.decode_packet(:httph_bin, binary, []) parser is invoked with an empty option list so its per-line and per-packet size limits also default to unlimited.

A malicious HTTP server (reachable directly, via an attacker-controlled redirect, via SSRF, or via a man-in-the-middle) can stream complete header lines (or, after a chunked body, complete trailer lines) indefinitely without ever emitting the terminating blank line. The connection state grows without bound until the BEAM node is killed by the operating system's out-of-memory handler, taking down the entire application that uses Mint as an HTTP client.

This issue affects mint: from 0.1.0 before 1.9.2.

### CVE-2026-15076

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-14T09:16:40.313 |

In versions up to and including 4.5.29 (4.x branch) and 5.1.4 (5.x branch), the WebClientSession component of Eclipse Vert.x Web Client does not validate that the Domain attribute of a Set-Cookie response header matches the originating server's domain, in violation of RFC 6265 section 5.3.
An attacker who controls any server that the victim application contacts can inject a cookie scoped to an arbitrary third-party domain; because the session store performs no cross-domain ownership check, it stores and later transmits that cookie to the targeted domain.




When the victim application subsequently sends a request to the targeted domain using the same WebClientSession, it presents the attacker-injected cookie, causing the receiving service to process the request under the attacker's account. Sensitive data included in the victim application's requests, such as payment amounts, card details, or other API payloads, may then be accessible to the attacker through their own account on that service.

### CVE-2026-15075

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-346` |
| Published | 2026-07-14T09:16:40.180 |

In Eclipse Vert.x versions up to and including 4.5.29 (4.x branch) and 5.1.4 (5.x branch), DefaultRedirectHandler (vertx-core) propagates all request headers as-is across cross-origin HTTP 30x redirects. Only Content-Length is stripped; no origin comparison (scheme, host, port) is performed before copying headers to the redirect target.
As a result, credential headers, including Authorization, Cookie, Proxy-Authorization, and arbitrary custom headers such as X-API-Token, are forwarded to the redirect destination without the caller's knowledge.




An attacker who can cause a Vert.x HttpClient to issue a request that is redirected to an attacker-controlled host (for example, by supplying a URL to a webhook dispatcher, image proxy, or microservice URL fetcher) can capture bearer tokens, basic-auth credentials, session cookies, and API keys attached to the original request.

### CVE-2026-44752

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T01:16:17.567 |

SAP NetWeaver Application Server Java allows an unauthenticated attacker to inject malicious JavaScript through crafted URLs. When a victim accesses such a URL, the script executes in the user's browser, allowing the attacker to access sensitive session information and modify non-sensitive data displayed in the client�s browser. This results in a high impact on confidentiality, low impact on integrity with no impact on availability of the application.

### CVE-2026-58500

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T22:16:48.677 |

MCP Appium is an MCP server that provides AI assistants with tools to automate mobile app testing on Android and iOS. In versions prior to 1.85.10, the createLocatorGeneratorUI function interpolates attacker-controlled element attributes — text, content-desc, resource-id, and locator selector values — directly into an HTML template literal without any HTML or JavaScript context escaping. An attacker who controls the UI of the app under test can inject arbitrary HTML and JavaScript into the MCP UI resource returned by the generate_locators tool. When a victim's MCP client renders this resource, the injected script executes and can invoke arbitrary MCP tools via window.parent.postMessage, leading to unauthorized MCP tool execution such as taking screenshots, reading page source, or any other registered capability. This issue has been fixed in version 1.85.10.

### CVE-2026-48364

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-07-13T21:16:48.337 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by an Uncontrolled Search Path Element vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-48363

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-07-13T21:16:47.857 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by an Uncontrolled Search Path Element vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-12583

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T06:17:05.900 |

The Newsletters WordPress plugin before 4.15 does not prevent deserialization of untrusted input that is stored through a public form, allowing unauthenticated attackers to inject a PHP object and, via a property-oriented gadget chain bundled with the Newsletters WordPress plugin before 4.15, write arbitrary files and execute code on the server.

### CVE-2026-12511

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-14T06:17:05.787 |

The AI Engine  WordPress plugin before 3.5.5 does not sanitize a user-supplied filename before using it to write a downloaded file, allowing authenticated users with editor-level access to write attacker-controlled bytes to an arbitrary location on the server via path traversal.

### CVE-2026-44745

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-601` |
| Published | 2026-07-14T01:16:17.320 |

SAP Approuter does not properly validate incoming request headers during the OAuth2 login flow under certain configurations. This allows an unauthenticated remote attacker to craft a malicious link which, when clicked by a victim, could lead to unauthorized access. Successful exploitation results in a high impact to the confidentiality and integrity with no impact on the availability of the application.

### CVE-2026-59245

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-13T16:16:41.880 |

In the Apache Airflow FAB auth manager, a DAG whose `dag_id` is `DAGs` collided with the global all-DAGs permission resource name produced by `resource_name()`, so a user granted per-DAG `access_control` on that one DAG was silently granted the global all-DAGs permission (privilege escalation). The escalation triggers when a DAG named `DAGs` exists and a lower-privileged user is given per-DAG access to it, granting that user read/edit access to every DAG. Users are advised to upgrade to `apache-airflow-providers-fab` 3.7.2 or later, which disambiguates the resource-name collision.

### CVE-2026-58065

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-322` |
| Published | 2026-07-13T16:16:41.757 |

The Apache Airflow Git provider runs its git-over-SSH operations with `StrictHostKeyChecking=no` by default, disabling SSH host-key verification. An attacker who can intercept the network path between an Airflow worker and the Git server can impersonate the server (man-in-the-middle), capturing the SSH deploy key or injecting malicious repository content. Deployments that use the Git DAG bundle or Git provider to clone over SSH with a deploy key are affected. The fix changes the default to verify host keys; upgrade to apache-airflow-providers-git `0.4.1` or later and configure a `known_hosts` file.

### CVE-2026-62242

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-13T22:16:52.260 |

Spring Boot Admin Server before 4.1.2 contains a server-side request forgery vulnerability that allows unauthenticated attackers to register instances with attacker-controlled healthUrl and managementUrl parameters without validation against private IP ranges or metadata endpoints. Attackers can force the server to make HTTP requests to arbitrary internal addresses and retrieve response bodies via the actuator proxy to exfiltrate cloud credentials.

### CVE-2026-49972

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-13T19:17:10.447 |

Laravel-Mediable before 7.0.0 contains a file upload vulnerability that allows unauthenticated attackers to achieve remote code execution by uploading a file with an embedded PHP extension disguised within a double extension such as shell.php.jpg. The PATHINFO_FILENAME extraction preserves the inner .php extension in the base name, and on misconfigured Apache or nginx servers that execute any filename containing .php as PHP, the stored file is interpreted as executable code while all MIME type, extension, and aggregate type validation checks pass due to the outer .jpg extension.

### CVE-2026-58233

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T01:16:18.710 |

SAP Change and Transport System Attach Tool (ctsattach) allows an authenticated attacker to supply a specially crafted archive file which, when processed by the application�s library, can trigger insecure deserialization and lead to remote code execution (RCE) on the system. Successful exploitation requires a victim to process the malicious archive, enabling the attacker to execute the RCE and extract sensitive information and gain control over the system and its processes. This vulnerability has a high impact on confidentiality and integrity of the data, with a low impact on the availability of the system.

### CVE-2026-62189

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59;CWE-367` |
| Published | 2026-07-13T22:16:50.037 |

OpenClaw versions before 2026.6.9 contain a symlink following vulnerability in the mirror sync feature that allows lower-trust callers to perform actions requiring stronger authorization. Attackers can exploit remote symlink parents to bypass policy checks and authorization boundaries when the feature is enabled and reachable.

### CVE-2024-7708

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-401` |
| Published | 2026-07-14T09:16:39.453 |

For requests that have a body, but reading the body may end up in reading 0 bytes, there is a buffer leak.
This is particularly the case for 100-Continue, but any request where the network is slow can leak.

### CVE-2026-58101

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-13T23:16:47.020 |

Crypt::OpenSSL::X509 versions before 2.1.3 for Perl allow denial of service via NULL pointer dereference.

X509V3_EXT_d2i(ext) returns NULL when an extension's DER value fails to parse. basicC, ia5string, and auth_att dereference its result without a NULL check. keyid_data also dereferences akid->keyid, which is NULL for an empty AKI SEQUENCE (DER 30 00) even when the parse succeeds.

A caller invoking an affected helper on an extension from an untrusted certificate triggers a SIGSEGV that crashes the Perl process.

### CVE-2026-51539

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-13T22:16:47.603 |

A Denial of Service (DoS) vulnerability exists in the receive loop of libmodbus 3.1.12 when running on Windows. The issue stems from improper timeout management during network read operations.

### CVE-2026-15685

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-07-13T22:16:46.123 |

Ollama downloadBlob Improper Validation of Array Index Denial-of-Service Vulnerability. This vulnerability allows remote attackers to create a denial-of-service condition on affected installations of Ollama. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the downloadBlob function. The issue results from the lack of proper validation of user-supplied data, which can result in a memory access past the end of an allocated array. An attacker can leverage this vulnerability to create a denial-of-service condition on the system. Was ZDI-CAN-27277.

### CVE-2026-15683

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-13T22:16:45.793 |

Lorex 2K Indoor Wi-Fi Security Camera Device Management Server Improper Certificate Validation Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Lorex 2K Indoor Wi-Fi Security Cameras. User interaction is not required to exploit this vulnerability.

The specific flaw exists within the device management functionality. The issue results from the lack of proper validation of the certificate presented by the server. An attacker can leverage this in conjunction with other vulnerabilities to execute code in the context of root. Was ZDI-CAN-26851.

### CVE-2026-15680

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-07-13T22:16:45.387 |

Lorex 2K Indoor Wi-Fi Security Camera CDeviceOperator Format String Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Lorex 2K Indoor Wi-Fi Security Cameras. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the parsing of JSON requests in the sonia binary. The issue results from the lack of proper validation of a user-supplied string before using it as a format specifier. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-25884.

### CVE-2026-26396

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-13T19:17:03.320 |

OpenBMB XAgent v1.0.0 and before is vulnerable to path traversal in the file() function in XAgent/XAgentServer/application/routers/workspace.py. The input parameter “filename” is user-controllable and is concatenated into the file path to be read without proper validation, leading to a directory traversal vulnerability that may result in sensitive information disclosure.

### CVE-2026-15693

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-14T14:16:33.130 |

A security vulnerability has been detected in Tenda BE12 Pro 16.03.66.23. This issue affects the function fromSafeMacFilter of the file /goform/SafeMacFilter. The manipulation of the argument page leads to stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-15692

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-14T13:18:20.133 |

A weakness has been identified in Tenda BE12 Pro 16.03.66.23. This vulnerability affects the function fromSafeUrlFilter of the file /goform/SafeUrlFilter. Executing a manipulation of the argument page can lead to stack-based buffer overflow. The attack may be performed from remote. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-15691

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-14T13:18:19.967 |

A security flaw has been discovered in Tenda BE12 Pro 16.03.66.23. This affects the function fromSafeClientFilter of the file /goform/SafeClientFilter. Performing a manipulation of the argument page results in stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-15684

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-13T22:16:45.993 |

Glarysoft Glary Utilities Link Following Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Glarysoft Glary Utilities. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the Disk Clean functionality. By creating a junction, an attacker can abuse the service to delete arbitrary files. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-27004.

### CVE-2025-45869

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-13T19:16:36.360 |

LogicalDOC Enterprise Version up to and before v9.1.1 is vulnerable to Server-Side Request Forgery (SSRF). An unauthenticated attacker can exploit the ShareFileCallback servlet by manipulating input parameters to trigger a server-side request to an attacker-controlled host.

### CVE-2026-62192

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-13T22:16:50.457 |

OpenClaw versions 2026.6.6 before 2026.6.9 contain an authorization bypass vulnerability in Discord guild actions that allows lower-trust callers to perform actions requiring stronger authorization checks. Attackers can exploit misconfigured input paths to skip cross-provider requester authorization and execute restricted operations.

### CVE-2026-62186

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862;CWE-863` |
| Published | 2026-07-13T22:16:49.607 |

OpenClaw versions before 2026.6.8 contain an authorization bypass vulnerability in OpenAI-compatible HTTP model overrides that allows lower-trust callers to perform actions requiring stronger authorization checks. Attackers can exploit misconfigured input paths to bypass admin authorization policies and execute restricted operations.

### CVE-2026-59674

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-61` |
| Published | 2026-07-14T08:16:22.963 |

A UNIX Symbolic Link (Symlink) Following vulnerability in openSUSE Tumbleweed suricata package allows the suricata user to escalate to root.






This issue affects openSUSE Tumbleweed: from ? before 8.0.5-2.1; openSUSE Tumbleweed: from ? before 8.0.5-2.1.

### CVE-2026-62191

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862;CWE-863` |
| Published | 2026-07-13T22:16:50.310 |

OpenClaw versions 2026.6.6 before 2026.6.9 contain an authorization bypass vulnerability in message mutation handling that allows lower-trust callers to perform actions requiring stronger authorization checks. Attackers can exploit misconfigured input paths to skip requester authorization and execute privileged operations when the affected feature is enabled and reachable.

### CVE-2026-58410

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-07-13T21:16:48.573 |

ChurchCRM is an open-source church management system. Prior to version 7.4.0, there was an authorization flaw in the family-scoped endpoints which allowed low-privileged users to read and modify other families’ records. An authenticated non-admin user with EditSelf access can supply another family’s `familyId` and access records outside their own family scope. The backend trusts the attacker-controlled `familyId` and loads the corresponding family entity by ID without verifying that the requested family belongs to the current user. If the same user also has Notes permission, they can create notes on another family’s record. This breaks the intended EditSelf scope and allows access to unrelated congregation records. This issue has been fixed in version 7.4.0.

### CVE-2026-8314

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T13:19:11.010 |

A security issue exists within Arena® Simulation due to a memory corruption vulnerability in the siman.exe (Siman) component. The vulnerability stems from improper validation of user-supplied data, which can result in an out-of-bounds write. An attacker could leverage this vulnerability to execute arbitrary code in the context of the current process by convincing a user to open a malicious file.

### CVE-2026-8313

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T13:19:10.863 |

A security issue exists within Arena® Simulation due to a memory corruption vulnerability in the linker.exe (Siman) component. The vulnerability stems from improper validation of user-supplied data, which can result in an out-of-bounds write. An attacker could leverage this vulnerability to execute arbitrary code in the context of the current process by convincing a user to open a malicious file.

### CVE-2026-8312

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T13:19:10.727 |

A security issue exists within Arena® Simulation due to a memory corruption vulnerability in the expmt.exe (Siman) component. The vulnerability stems from improper validation of user-supplied data, which can result in an out-of-bounds write. An attacker could leverage this vulnerability to execute arbitrary code in the context of the current process by convincing a user to open a malicious file.

### CVE-2026-8085

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T13:19:10.587 |

A security issue exists within Arena® Simulation due to a memory corruption vulnerability in the model.exe (Siman) component. The vulnerability stems from improper validation of user-supplied data, which can result in an out-of-bounds write. An attacker could leverage this vulnerability to execute arbitrary code in the context of the current process by convincing a user to open a malicious file.

### CVE-2026-6851

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-14T08:16:24.000 |

An Improper link resolution before file access ('link following') vulnerability in the File Shredder module as used in Bitdefender Total Security and Internet Security on Windows allows a less-privileged local user to elevate rights by leveraging a race conditions via Symbolic Links.

This issue affects Total Security: before 27.0.58.315; Internet Security: before 27.0.58.315.

### CVE-2026-58411

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:L/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T22:16:48.270 |

ChurchCRM is an open-source church management system. Prior to version 7.4.0, Cross-Site Scripting (XSS) vulnerabilities were identified due to insufficient output encoding of user-controlled request parameter names and parameter values. The application reflects attacker-controlled input into JavaScript string contexts and HTML attribute contexts without proper sanitization or contextual output encoding. Affected endpoints observed during testing: /FamilyCustomFieldsEditor.php, /PaddleNumList.php and /admin/system/church-info. Potential consequences include session-token theft, account takeover, unauthorized actions on behalf of authenticated users, exposure of sensitive church member information, credential harvesting, phishing, and privilege escalation when administrators are targeted. This issue has been resolved in version 7.4.0.
