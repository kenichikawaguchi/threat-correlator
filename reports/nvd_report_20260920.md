# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-19 15:01 UTC
- **対象期間**: `2026-09-18T15:00:35.000Z` 〜 `2026-09-19T15:01:17.000Z`
- **重要CVE数**: 212 件（Critical 9.0+: 44 件 / High 7.0〜: 168 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
直近で公開された CVE のうち **CVSS 7.0 以上** のものは 30 件を超え、**IBM 製品 (Guardium、MQ、Common Licensing Agent) とオープンソース／WordPress プラグイン** に集中しています。  
- 多くは **認証バイパス／未認証リモートコード実行** といった深刻なリスクを伴い、攻撃者がネットワーク上から直接システムを支配できる点が共通しています。  
- 同一製品 (Guardium Data Protection 12.2) に対して **10 件以上** の脆弱性が同時に報告されており、**パッチ適用の遅延が大きな攻撃面となり得ます**。  
- WordPress エコシステムでも **プラグインレベルの任意ファイルアップロードやオプション書き換え** が続出しており、サイト運営者はプラグインのサプライチェーンリスクを改めて認識すべきです。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | なぜ注目すべきか |
|-----|------|----------|-------------------|
| **CVE‑2026‑10747** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | IBM MQ Appliance のプロトコルメッセージ処理でヒープバッファ **オーバーフロー** が発生。認証前にリモートコード実行または DoS が可能。 | MQ は金融・製造業の基幹メッセージングに必須。認証不要でコード実行が可能なため、内部ネットワークに侵入しただけで広範囲に被害が拡大。 |
| **CVE‑2025‑15399** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | IBM Common Licensing Agent 系列で **CSRF** が成立。認証済みユーザーのブラウザを利用し、管理者権限で任意操作が実行できる。 | ライセンス管理は多くのサーバで自動化されているため、攻撃者が一度管理者のブラウザを誘導すれば、環境全体の設定変更や情報漏洩が起こり得る。 |
| **CVE‑2026‑84064** | 9.9 (AV:N/AC:L/PR:L/UI:N/S:C) | IBM Guardium Data Protection 12.2 の **認証済み SQL インジェクション**（不適切なエスケープ）。任意の SQL を実行でき、データ改ざん・情報漏洩が可能。 | Guardium はデータベース監査・保護の要であり、SQL インジェクションは直接データベースを書き換える危険がある。 |
| **CVE‑2026‑80442** | 9.9 (AV:N/AC:L/PR:L/UI:N/S:C) | Guardium Data Protection 12.2 の **認証済み OS コマンドインジェクション**（exportCertificate 機能）。リモートで任意シェルコマンドが実行可能。 | OS コマンドインジェクションはシステム全体の権限取得に直結し、他の Guardium 機能を踏み台に更なる横展開が容易になる。 |
| **CVE‑2026‑86591** | 9.8 (AV:N/AC:L/PR:N/UI:N/S:U) | WordPress **Botiga Pro** プラグインの REST エンドポイントに認可チェックが無く、未認証ユーザーが任意の `option` を書き換え可能。 | WordPress サイトは数千件規模で稼働中。認可欠如はフルサイト乗っ取り（権限昇格）に直結し、プラグイン更新が遅れると長期的にリスクが残る。 |

> **注**：Guardium 系列は同一バージョン (12.2) に対して多数の脆弱性が報告されているため、**総合的なリスク評価** と **一括パッチ適用** が最重要です。

---

## 3. 推奨アクション  

### 3‑1. 直ちにベンダーパッチを適用
| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン (ベンダーが公表した最小修正版) |
|-------------------|-------------------|----------------------------------------------|
| **IBM MQ Appliance** | 8.1.0 〜 8.1.0.40 (該当脆弱) | 8.1.0.41 以上、または最新の 9.x 系リリース (9.3.5 以降) |
| **IBM Common Licensing Agent** | 9.0.0 〜 9.0.0.2 (該当脆弱) | 9.0.0.3 以上（2026‑03 以降のセキュリティリリース） |
| **IBM Guardium Data Protection** | 12.2 (全脆弱) | 12.2.1 以上（2026‑04 でリリースされた累積パッチ） |
| **pg_partman (PostgreSQL extension)** | < 5.5.0 | ≥ 5.5.0 |
| **kcp** | < 0.31.4 / < 0.32.2 | ≥ 0.32.2 |
| **XWiki Rendering** | < 14.10.2, < 15.0 RC1 | 14.10.2 以上、もしくは 15.0 RC2 以降 |
| **Botiga Pro (WordPress)** | < 1.6.5 | ≥ 1.6.5 |
| **Gravity Forms (WordPress)** | ≤ 3.1.0.4 | ≥ 3.1.0.5 |
| **LMDeploy** | < 0.16.0 | ≥ 0.16.0 |
| **libheif** | 1.22.0‑1.23.2 | ≥ 1.23.3 |
| **Icinga 2** | 2.8‑2.14.9, 2.15.4, 

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-10747

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-18T16:17:04.413 |

IBM MQ Appliance could allow a remote attacker to cause a denial of service or potentially execute arbitrary code due to a heap buffer overflow in protocol message processing before authentication.

### CVE-2025-15399

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-18T16:17:02.387 |

IBM Common Licensing Agent 9.0, Agent 9.0.0.1, Agent 9.0.0.2, ART 9.0, ART 9.0.0.1, and ART 9.0.0.2 is vulnerable to cross-site request forgery which could allow an attacker to execute malicious and unauthorized actions transmitted from a user that the website trusts.

### CVE-2026-84078

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-18T20:17:27.480 |

IBM Guardium Data Protection 12.2 is vulnerable to a missing authentication vulnerability in the LoadBalancerServlet. An unauthenticated user can access privileged load-balancer operations, potentially resulting in unauthorized actions and impact to the integrity and availability of the affected system.

### CVE-2026-84075

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-18T20:17:27.103 |

IBM Guardium Data Protection 12.2 could allow a remote attacker to bypass security restrictions due to missing authentication for the ChangeTrackerServlet.

### CVE-2026-84064

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:26.440 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to execute arbitrary SQL commands due to improper neutralization of special elements used in an SQL command.

### CVE-2026-80442

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-18T20:17:23.343 |

IBM Guardium Data Protection 12.2 is vulnerable to an authenticated OS command injection vulnerability in the exportCertificate functionality. Successful exploitation could allow an attacker to execute unauthorized commands and impact the confidentiality, integrity, and availability of the affected system.

### CVE-2026-61781

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-269` |
| Published | 2026-09-18T20:17:19.003 |

pg_partman is a PostgreSQL extension that manages partitioned tables by time or ID. Prior to 5.5.0, create_partition_time() reads the writable part_config.time_encoder text value and interpolates it without identifier quoting into a dynamically executed SELECT statement. A role with the documented partman_user INSERT and UPDATE privileges can store SQL rather than a function name. When pg_partman_bgw later creates a child partition for a text- or UUID-keyed set, the worker executes the stored SQL with pg_partman_bgw.role privileges, which default to PostgreSQL superuser. The persistent configuration row can repeatedly restore elevated access on later maintenance ticks, and successful exploitation can permit database-wide compromise and operating-system command execution as the PostgreSQL service account. This issue is fixed in version 5.5.0.

### CVE-2026-77240

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-18T17:17:00.360 |

WACRM is a self-hostable CRM template for WhatsApp. In version 0.7.0 and earlier, the profiles_update row-level security policy in supabase/migrations/017_account_sharing.sql permits authenticated users to modify their own account_role and account_id, allowing a viewer to self-promote or move into another tenant and then access or modify tenant resources. Separately, match_ai_knowledge_fts and match_ai_knowledge_semantic in supabase/migrations/030_ai_knowledge.sql run as SECURITY DEFINER, accept a caller-controlled p_account_id, and omit an is_account_member check, allowing an authenticated non-member to read another tenant's knowledge-base chunks. This vulnerability is fixed with commit e01f7ed37184f972ace8fb2da5c3e37e56a6050f.

### CVE-2026-61682

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-290;CWE-302;CWE-348` |
| Published | 2026-09-18T16:17:07.523 |

kcp is a Kubernetes-like control plane for form-factors and use-cases beyond Kubernetes and container workloads. Prior to 0.31.4 and 0.32.2, the kcp front-proxy does not remove inbound X-Remote-User, X-Remote-Group, or X-Remote-Extra-* identity headers before forwarding requests to shards. Any authenticated tenant can inject X-Remote-Group: system:masters, authorization.kcp.io/warrant, authentication.kcp.io/scopes, or a group used for per-workspace required-group gating, and the shard trusts these values as authenticated identity assertions. This allows cross-workspace impersonation, authorization bypass, and arbitrary reading, writing, or deletion of resources, secrets, RBAC data, APIExports, APIBindings, and LogicalClusters. This issue is fixed in versions 0.31.4 and 0.32.2.

### CVE-2026-10858

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-18T16:17:05.310 |

IBM MQ for HPE NonStop 8.1.0 through 8.1.0.40 could allow an authenticated attacker to cause a denial of service or potentially execute arbitrary code due to a heap buffer underflow when processing multi-segment messages.

### CVE-2025-53837

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-18T16:17:03.527 |

XWiki Rendering is a generic rendering system that converts textual input in a given syntax (wiki syntax, HTML, etc) into another syntax (XHTML, etc). Prior to versions 14.10.2 and 15.0 RC1, any user who can edit their own user profile or any other document can execute arbitrary script macros including Groovy and Python macros that allow remote code execution including unrestricted read and write access to all wiki contents. The reason is that rendering output is included as content of HTML macros without further escaping and it is thus possible to close the HTML macro and inject script macros that are executed with programming rights. This has been patched in XWiki 14.10.2 and 15.0 RC1 by making sure that rendering output cannot close the surrounding HTML macro. A possible workaround is available. It is, in principle, possible to add escaping to all places where rendering output is used in wiki documents, but at the moment there is no list of them.

### CVE-2026-86591

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-19T07:16:33.063 |

The Botiga Pro WordPress plugin before 1.6.5 does not perform any authorisation checks on one of its REST routes, allowing unauthenticated users to update arbitrary WordPress options with arbitrary values, which could lead to privilege escalation and a full site takeover.
The same route also allows unauthenticated users to store arbitrary web scripts which are then executed on every page of the site's front end, as well as to move arbitrary posts to the trash.

### CVE-2026-84434

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-19T03:17:15.573 |

The Gravity Forms plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 3.1.0.4 via the upload_file function. This is due to a mismatch between the field validation pipeline and the file persistence pipeline, where hidden file upload fields bypass extension validation and a rejected file's intact upload state is later passed to upload_file() without re-validation. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. Exploitation requires the targeted form to contain a File Upload field with its Visibility set to 'Hidden'; the vulnerability is reachable by unauthenticated attackers on any publicly accessible form meeting this condition.

### CVE-2026-84082

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:27.743 |

IBM Guardium Data Protection 12.2 could allow a remote attacker to execute arbitrary SQL commands due to improper neutralization of special elements used in an SQL command.

### CVE-2026-82967

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-18T20:17:25.513 |

IBM Guardium Data Protection 12.2 is vulnerable to an authentication bypass that allows an unauthenticated remote attacker to bypass IP-based access controls and access the Guardium management interface.

### CVE-2026-82340

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-18T20:17:24.517 |

IBM Guardium Data Protection 12.2 is vulnerable to unauthenticated insecure deserialization and attacker-controlled reflective method dispatch in the Change Audit System (CAS) listener. A network attacker able to reach TCP port 16017 may submit crafted serialized messages and potentially cause unintended code execution in the Guardium appliance.

### CVE-2026-81657

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-18T20:17:23.997 |

IBM Guardium Data Protection 12.2 could allow a remote unauthenticated attacker to execute arbitrary code on the system due to the deserialization of untrusted data.

### CVE-2026-80441

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:23.217 |

IBM Guardium Data Protection 12.2 is vulnerable to an unauthenticated second-order SQL injection vulnerability in the generateInsertQuery functionality of change-tracker-data.sql. A remote attacker could inject malicious SQL that is subsequently processed by the application, potentially resulting in compromise of the confidentiality, integrity, and availability of the affected system.

### CVE-2026-58264

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-18T20:17:18.107 |

FluidSynth is a software synthesizer based on the SoundFont 2 specifications. From 1.1.2 until 2.5.6, the FluidSynth command handler accepts a pitch_bend_range command whose channel argument is not bounds checked before the supplied value is written through the selected synth channel. An out-of-range channel can therefore cause an out-of-bounds heap write, leading to denial of service or possible code execution. The issue is remotely reachable when the TCP server is enabled through new_fluid_server() or fluidsynth -s, and it is locally reachable through malicious commands delivered to the FluidSynth shell on standard input. Applications that do not use the shell, command handler, or TCP server are not affected. This issue is fixed in version 2.5.6.

### CVE-2026-61550

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-18T18:17:08.217 |

Icinga 2 is an open source monitoring system. From 2.8 until 2.14.9, 2.15.4, and 2.16.2, certificate update JSON-RPC message handling does not validate that the sender is a trusted endpoint. An unauthenticated network attacker able to connect to TCP port 5665 can replace the node certificate and trusted CA certificate, impersonate a trusted node, and take control of the node. This issue is fixed in versions 2.14.9, 2.15.4, and 2.16.2.

### CVE-2025-66455

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-18T18:17:04.420 |

LMDeploy is a toolkit for compressing, deploying, and serving large language models. Starting in version 0.9.2 and prior to version 0.16.0, LMDeploy's PyTorch DistServe/PD-disaggregation control plane used `recv_pyobj()` to deserialize messages received through a ZeroMQ PULL socket. PyZMQ implements `recv_pyobj()` using Python pickle deserialization, which can execute arbitrary code while reconstructing an object. The peer address used by the receiver was supplied through the `POST /distserve/p2p_connect` HTTP endpoint. An attacker who could reach an affected DistServe API server could cause the server to connect to an attacker-controlled ZeroMQ endpoint and deserialize a crafted pickle payload. API-key authentication is not enabled unless the operator explicitly configures it. As a result, affected DistServe deployments without API keys allowed unauthenticated remote code execution with the privileges of the LMDeploy serving process. This issue affects the PyTorch backend when PD-disaggregation/DistServe is enabled. Ordinary deployments that do not use the affected disaggregated-serving path do not expose this data flow. The fix was released in LMDeploy 0.16.0. Users who cannot upgrade immediately should prevent untrusted clients from reaching `/distserve/*` endpoints, restrict the DistServe HTTP and ZeroMQ control planes to trusted cluster networks, configure API-key authentication, and block arbitrary outbound ZeroMQ connections from serving nodes. These measures reduce exposure but do not make pickle deserialization safe.

### CVE-2026-84383

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-18T16:17:11.707 |

libheif is a HEIF and AVIF file format decoder and encoder. From 1.22.0 until 1.23.2, a crafted HEIF, HEIC, or AVIF item graph using nested iden and auxl references can make HeifPixelImage::transfer_channel_from_image_as() append duplicate Alpha planes with different bit depths to m_storage. HeifPixelImage::scale_nearest_neighbor() in libheif/image/pixelimage.cc allocates the destination Alpha plane using the first plane's 8-bit depth, then iterates a later 10-bit or 12-bit Alpha component and writes uint16_t samples into the same 8-bit allocation. The output geometry controls the overflow extent and the encoded sample values control the data written, allowing a remote file processed by heif_decode_image() to cause a heap out-of-bounds write. This issue is fixed in version 1.23.2.

### CVE-2026-75031

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-18T16:17:09.043 |

In the interchange/interchange project, a critical remote code execution (RCE) vulnerability was found in the 
“quick question” admin feature. In default installations arbitrary Perl 
code can be injected and executed server-side by unauthenticated users. 
The Perl code normally runs within a Safe container which limits the 
scope of what it can do, unless the non-default AllowGlobal directive is
 configured for the catalog being accessed.CTOR]

### CVE-2026-82832

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T20:17:24.643 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of input during web page generation.

### CVE-2026-93985

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-19T12:16:41.873 |

OpenPanel js-runtime through commit bad75bdd contains a sandbox escape vulnerability in the JavaScript webhook template validator that fails to block computed member access to constructor chains. Attackers with project write access can create webhook templates using computed property notation to access Function constructor and execute arbitrary code in the worker process.

### CVE-2026-93741

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-19T06:16:30.557 |

A security flaw has been discovered in Totolink A3002MU Hh-B20211125.1046. Affected by this vulnerability is the function formWlWds of the file /boafrm/formWlWds. The manipulation of the argument submit-url results in buffer overflow. It is possible to launch the attack remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-93740

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-18T22:17:10.890 |

A vulnerability was identified in Totolink A3002MU Hh-B20211125.1046. Affected is the function formWlEncrypt of the file /boafrm/formWlEncrypt. The manipulation of the argument submit-url leads to buffer overflow. It is possible to initiate the attack remotely. The exploit is publicly available and might be used.

### CVE-2026-75885

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-18T22:17:10.313 |

A flaw was found in the OpenShift console. Unauthenticated access to the `/api/devfile/` and `/api/devfile/samples/` endpoints allows a remote attacker to send crafted devfile payloads. This can lead to Server-Side Request Forgery (SSRF), where the console pod makes requests to internal services and reflects partial responses to the attacker. Additionally, by sending repeated large requests without a specified content length, an attacker can cause unbounded memory growth, leading to a Denial of Service (DoS).

### CVE-2026-93839

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-18T20:17:34.047 |

LightLLM through 1.2.0 contains an authentication bypass vulnerability in the /pd_register WebSocket endpoint that allows unauthenticated attackers to register arbitrary nodes by supplying crafted JSON without peer address validation. Attackers can disclose full user prompts routed to their socket, trigger denial of service by replacing legitimate nodes, or make the PD Master issue requests to internal network addresses.

### CVE-2026-63647

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-639` |
| Published | 2026-09-18T20:17:20.773 |

CordysCRM is an open source AI-powered customer relationship management system that supports private deployment. Prior to 1.7.2, SseController exposes the anonymous /sse/subscribe, /sse/broadcast, and /sse/close endpoints because ShiroFilter.addPublicPathFilters permits the SSE paths, and the endpoints trust the caller-controlled userId instead of deriving an identity from an authenticated principal. An unauthenticated caller can use /sse/subscribe to read another user's workflow events, approval requests, mentions, and alerts, use /sse/broadcast to inject SYSTEM_HEARTBEAT messages into another user's stream, or use /sse/close to terminate another user's channel. This vulnerability is fixed in 1.7.2.

### CVE-2023-54399

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T19:16:40.757 |

Hongjing e-HR before 8.2 contains a SQL injection vulnerability in the /servlet/codesettree endpoint where the categories query parameter is passed to a database query without sanitization after HRMS-encoding is stripped. An unauthenticated remote attacker can supply a crafted UNION SELECT payload to read arbitrary database content, including credential tables such as operuser. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2026-85497

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-916` |
| Published | 2026-09-18T17:17:04.790 |

CareCam CM2507 IP cameras store the device's root-account password using a fixed legacy password hash that provides insufficient resistance to offline cracking. An attacker who obtains the firmware image or password database could recover the associated credential, which may also be reusable across other devices running the same firmware.

### CVE-2026-81321

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-09-18T17:17:01.953 |

CM2507 IP cameras store configured wireless network credentials in cleartext within the device filesystem. An attacker who obtains filesystem access through physical access, a debugging interface, or another vulnerability could recover the configured network identifier and pre-shared key.

### CVE-2026-93659

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T15:17:22.510 |

Concrete CMS Community Store before 2.7.8 renders customer-supplied order fields without HTML escaping in checkout and admin views. Unauthenticated attackers can store script payloads in billing name, email, or phone fields that execute in authenticated manager sessions to create rogue accounts or exfiltrate data.

### CVE-2026-93868

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-338` |
| Published | 2026-09-18T20:17:34.633 |

Cotonti through 1.0.0 derives password recovery validation tokens from md5(microtime()) in users.passrecover.php, creating a predictable token space of approximately one million values per second. Unauthenticated attackers can read the server Date header, precompute candidate tokens within a narrow time window, and probe them against the passrecover authentication endpoint to reset any account password including administrators.

### CVE-2026-93762

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-09-18T18:18:35.053 |

Mongoid contains an unsafe reflection weakness in the query path used for embedded documents. An application that passes an externally supplied field name to certain in-memory query methods may allow an unauthenticated party to obtain unintended disclosure of stored document data and to permanently remove stored records.

### CVE-2026-92229

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-19T03:17:17.040 |

The The Forminator Forms – Contact Form, Payment Form & Custom Form Builder plugin for WordPress is vulnerable to arbitrary shortcode execution in all versions up to, and including, 1.57.2. This is due to the software allowing users to execute an action that does not properly validate a value before running do_shortcode. This makes it possible for unauthenticated attackers to execute arbitrary shortcodes.

### CVE-2026-89274

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-19T03:17:16.587 |

The WP Recipe Maker plugin for WordPress is vulnerable to Arbitrary Shortcode Execution in all versions up to, and including, 10.8.1. The vulnerability exists because `WPRM_Metadata::sanitize_metadata()` recursively calls `do_shortcode()` on every scalar field of the recipe's structured metadata array — including the `reviewBody` field, which is populated verbatim from the `comment_content` of approved `wprm-comment-rating` comments — without sanitizing or stripping shortcode tokens before execution; the subsequent `wp_strip_all_tags()` and `strip_shortcodes()` calls operate only on the output string after execution has already fully occurred, providing no protection against server-side shortcode invocation. This makes it possible for unauthenticated attackers to execute arbitrary registered WordPress shortcodes server-side on every recipe page render, causing shortcode output — such as attachment captions, private post fields, or other data exposed by installed shortcodes — to be embedded in the page's JSON-LD `reviewBody` metadata and disclosed to all visitors who load the recipe page. Successful exploitation requires the attacker's rated comment to pass the site's comment approval threshold, either via auto-approval or moderator action, before the injected shortcode begins executing on page loads.

### CVE-2026-84073

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:26.830 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to execute arbitrary SQL commands due to improper neutralization of special elements used in an SQL command.

### CVE-2026-75878

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-18T20:17:21.363 |

IBM Sterling File Gateway could allow a remote attacker to bypass authentication and obtain a fully authenticated session due to improper authentication via an unvalidated SSO header.

### CVE-2026-92702

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-18T18:18:16.257 |

Cocos AI is a confidential computing system for running AI workloads inside trusted execution environments. In versions up to and including 0.8.2, the intra-handshake attested TLS (aTLS) AMD SEV-SNP verification path does not enforce attestation freshness when the expected reportData value is nil, empty, or omitted, leaving the SEV-SNP policy ReportData unset so the verifier accepts unrelated or stale Evidence not bound to the current connection. A relying party that uses this path without an expected reportData as a trust or authorization decision can be induced to trust an unintended attestation context; a supplied non-empty reportData is still validated. The issue is fixed in version 0.9.0.

### CVE-2026-92701

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346;CWE-354` |
| Published | 2026-09-18T18:18:16.103 |

trusted execution environments. In versions up to and including 0.8.2, the intra-handshake attested TLS (aTLS) Intel TDX verification path does not copy the expected current-session freshness value into the TDX quote-body policy before quote validation, so structurally valid TDX QuoteV4 Evidence is accepted without checking that its REPORT_DATA field matches the reportData expected for the current session. A relying party using this path can therefore accept Evidence with a mismatched or reused reportData and release application data after the handshake, enabling session-misbinding to an unintended attestation context. The issue is fixed in version 0.9.0.

### CVE-2026-59163

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-18T18:17:07.807 |

Mnemosyne is a memory layer for artificial intelligence agents. Prior to v3.10.1, the auth check in mnemosyne/core/sync_server.py parsed the JWT's header and payload using base64 decoding, then passed the token to a jwt library call with options that effectively disabled signature verification. The server accepted any well-formed token regardless of the signature, including tokens with alg: none and tokens signed with the wrong key. The fix in v3.10.1 replaces the broken decode with a from-scratch HS256 verifier using only the Python standard library. For users who cannot upgrade immediately, restrict network access to the sync server endpoint to trusted clients only. Firewall, reverse proxy with mTLS, or localhost bind with SSH tunnel are all viable. The vulnerability is not exploitable against an unreachable endpoint.

### CVE-2026-84031

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T20:17:26.060 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of input during web page generation.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-84106

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T20:17:28.640 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of input during web page generation.

### CVE-2026-84074

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T20:17:26.963 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of input during web page generation.

### CVE-2026-84070

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T20:17:26.560 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of input during web page generation.

### CVE-2026-4327

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-19T08:16:53.887 |

The The Welcomizer plugin for WordPress is vulnerable to Remote Code Execution in all versions up to and including 2.8.1. This is due to missing authorization checks on the twiz_ajax_callback AJAX action's 'savesection' handler combined with the use of eval() to execute user-supplied 'custom logic' code on the frontend. The AJAX handler at twiz-ajax.php verifies a nonce but performs no current_user_can() capability check for the ACTION_SAVE_SECTION case. Furthermore, the nonce is exposed to any authenticated user through the directly-accessible twiz-ajax.js.php file which loads WordPress and outputs the nonce. This makes it possible for authenticated attackers, with Subscriber-level access and above, to inject arbitrary PHP code via the twiz_custom_logic POST parameter when saving a section with output choice 'twiz_logic_output'.

### CVE-2026-88824

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-19T07:16:33.273 |

The Master Blocks  WordPress plugin before 1.5.0 does not have authorisation on one of its REST routes, allowing unauthenticated users to update its settings, including a value that is output unescaped in the admin area, leading to Stored XSS that executes in the session of any administrator visiting a wp-admin page.

### CVE-2026-85680

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-19T07:16:32.960 |

The Ultimate Member  WordPress plugin before 2.13.1 does not escape a value derived from user supplied profile names before outputting it in the page title, and decodes HTML entities in it after its own sanitisation has already run, allowing unauthenticated attackers who register an account to store JavaScript that will execute when any visitor, including an administrator, views their profile.

### CVE-2026-92807

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-19T03:17:17.723 |

The Save as PDF Plugin by PDFCrowd plugin for WordPress is vulnerable to Arbitrary Function Invocation in all versions up to, and including, 4.6.1 via the `pdf_created_callback` shortcode attribute. The `eval_shortcode()` function copies any non-`button_`/non-`email_` shortcode attribute verbatim into a custom options array without sanitization, allowlist enforcement, or capability checks, and `create_button()` AES-encrypts that array — including the attacker-supplied callback value — and embeds the resulting blob in the rendered button HTML; when the blob is later POSTed to the unauthenticated `wp_ajax_nopriv_save_as_pdf_pdfcrowd` endpoint, `save_as_pdf_pdfcrowd()` decrypts it and invokes `$options['pdf_created_callback']` as a PHP callable at line 1722 with no `is_callable()` guard, no allowlist, and no capability check. This makes it possible for authenticated attackers, with Contributor-level access and above, to invoke arbitrary PHP functions or static class methods with plugin option data as the sole argument, enabling disclosure of the site's stored PDFCrowd API key and username or further server-side abuse. Note that the encryption boundary does not mitigate this vector because the server itself encrypts the attacker-chosen callback during shortcode rendering, supplying any authenticated Contributor with a cryptographically valid blob that any unauthenticated visitor can subsequently replay to trigger invocation.

### CVE-2026-93031

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-18T20:17:31.630 |

The WP Cloud Plugins Use-your-Drive, Out-of-the-Box, Share-one-Drive, and Lets-Box plugins for WordPress are vulnerable to Arbitrary File Upload in all versions from 2.0 up to, and including, 3.8.3 via the download_file_to_uploads function. This is due to the import action being registered for unauthenticated users via wp_ajax_nopriv_, a missing capability check in can_import(), and the imported file's extension and contents not being validated against get_allowed_mime_types() before it is written to the uploads directory. This makes it possible for authenticated attackers, with subscriber-level access and above, to upload files that may be executable, which makes remote code execution possible.

### CVE-2026-84084

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-18T20:17:28.010 |

IBM Guardium Data Protection 12.2 could allow a remote attacker to bypass security restrictions due to a cross-site request forgery (CSRF) vulnerability.

### CVE-2026-84034

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-18T20:17:26.190 |

IBM Guardium Data Protection 12.2 is vulnerable to a hardcoded credentials vulnerability in the hardware_assess/obstore binaries. A low-privileged authenticated user can recover hardcoded product master secrets, potentially resulting in unauthorized access to the internal database and compromise of sensitive system information.

### CVE-2026-82887

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-18T20:17:24.893 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-82885

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-18T20:17:24.770 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to gain elevated privileges due to missing authorization in the REST API.

### CVE-2026-81933

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:24.250 |

IBM Guardium Data Protection 12.2 is vulnerable to a SQL injection vulnerability in the Analytic Grid Service Handler. A low-privileged authenticated user can inject SQL statements through the analytic cases grid endpoint, potentially resulting in unauthorized access to sensitive data and impact to the confidentiality, integrity, and availability of the affected system.

### CVE-2026-81656

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:23.867 |

IBM Guardium Data Protection 12.2 is vulnerable to a SQL injection vulnerability in the New Query Builder REST Processor. A low-privileged authenticated user can inject SQL statements through the newQueryBuilder REST endpoint, potentially resulting in unauthorized access to data and impact to the confidentiality, integrity, and availability of the affected system.

### CVE-2026-11725

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-18T20:17:03.167 |

IBM MQ could allow an authenticated attacker to cause a denial of service or potentially execute arbitrary code due to an integer overflow in MQINQ request processing.

### CVE-2026-93759

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-18T18:18:34.640 |

Mongoid does not neutralize a string-typed query criterion supplied to its query builder, and instead passes it to the database as a server-side JavaScript expression. An unauthenticated party able to influence the value an application supplies as a query argument may cause code of their choosing to be evaluated by the database engine. This may result in unintended disclosure of stored field values, unintended selection of documents for application-initiated writes, and reduced database performance.

### CVE-2026-81180

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-18T18:17:15.777 |

SysReptor is a fully customizable pentest reporting platform. Prior to 2026.61, authenticated users of SysReptor Professional can upload image files whose formats cause image processing to invoke Ghostscript, allowing embedded PostScript to operate in the shared temporary directory. An attacker can combine that behavior with a race involving GnuPG configuration files in temporary subdirectories to cause GnuPG to copy attacker-controlled Python code into the application code directory. The injected code executes with the privileges of the SysReptor application process after a worker restart. The Community edition is not affected. Version 2026.58 contains a partial mitigation, and this issue is fully fixed in version 2026.61.

### CVE-2026-33625

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-18T18:17:06.640 |

LMDeploy is a toolkit for compressing, deploying, and serving large language models. Versions 012.1 through 0.12.2 contain a code injection vulnerability in `lmdeploy/pytorch/config.py` line 620 that allows an attacker to execute arbitrary Python code by publishing a malicious HuggingFace model with a crafted `quantization_config.quant_dtype` value. When a user loads the model with lmdeploy, the `quant_dtype` is passed to `eval(f'torch.{quant_dtype}')` without any validation. Version 0.12.3 contains a patch.

### CVE-2026-58197

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-09-18T17:16:57.880 |

ToolHive is a utility designed to simplify the deployment and management of Model Context Protocol servers. Prior to ToolHive CLI 0.30.1 and ToolHive Studio 0.38.0, locally run MCP server containers use the default network permission profile without network isolation, permitting access to host.docker.internal while ToolHive API and MCP proxy endpoints are reachable without authentication. A malicious or compromised MCP server can use the Docker gateway to contact host-local services, other ToolHive-managed MCP proxies, or the ToolHive control plane without escaping the container. This access can expose data and logs, invoke sibling MCP tools, alter process or workload state, and disrupt services. ToolHive Studio additionally sends network_isolation as false and overrides the backend's secure isolation default. This issue is fixed in ToolHive CLI 0.30.1 and ToolHive Studio 0.38.0.

### CVE-2026-11381

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-18T16:17:05.767 |

IBM MQ could allow an authenticated attacker to cause a denial of service or potentially execute arbitrary code due to improper validation of message distribution list structures.

### CVE-2026-11378

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-18T16:17:05.620 |

IBM MQ could allow an authenticated attacker to cause a denial of service or potentially execute arbitrary code due to an integer overflow in distribution list processing.

### CVE-2026-11375

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-18T16:17:05.470 |

IBM MQ could allow an authenticated attacker to cause a denial of service or potentially execute arbitrary code due to a stack buffer overflow when processing XA transaction identifiers.

### CVE-2026-10575

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-18T16:17:04.150 |

IBM MQ could allow an authenticated attacker to cause a denial of service or potentially escalate privileges due to a heap buffer overflow when processing MQPUT operations with malformed distribution headers.

### CVE-2025-14754

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-18T16:17:02.253 |

IBM Cloud Pak for Data 5.1.2 could allow an authenticated user to execute arbitrary commands with elevated privileges on the system due to improper validation of user supplied input.

### CVE-2017-20284

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-18T20:16:58.540 |

Caucho Resin contains a path traversal vulnerability in the documentation webapp (resin-doc) that allows remote unauthenticated attackers to read arbitrary files by supplying a relative path through the inputFile request parameter of the jndi-appconfig tutorial servlet. Attackers can craft requests with directory traversal sequences to the servlet endpoint to read files outside the intended tutorial directory on the underlying system. Exploitation evidence was first observed by the Shadowserver Foundation on 2021-12-10.

### CVE-2021-48008

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T19:16:40.563 |

Chanjet CRM contains an unauthenticated SQL injection vulnerability that allows remote attackers to execute arbitrary SQL queries by manipulating the site_id GET parameter in the webservice endpoint. Attackers can exploit the lack of input sanitization or parameterization through UNION-based injection techniques to extract sensitive data from the underlying database. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-18.

### CVE-2019-25776

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T19:16:39.420 |

Weaver E-cology contains an unauthenticated SQL injection vulnerability that allows remote attackers to execute arbitrary SQL queries by submitting malicious input through the userIdentifiers GET parameter in the mobile plugin endpoint. Attackers can bypass space-based filter controls by wrapping SQL keywords in parentheses to perform UNION-based injection and extract sensitive data including administrator credential hashes from the database. Exploitation evidence was first observed by the Shadowserver Foundation on 2022-07-28.

### CVE-2026-93761

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-18T18:18:34.917 |

An inefficient regular expression complexity issue in the in-memory query evaluation component of the Mongoid library may allow an unauthenticated party to cause excessive processing within an embedding application process. Applications that place user-supplied text into a pattern-matching query condition on an embedded association may become unresponsive.

### CVE-2026-93753

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-18T18:18:34.487 |

deepmerge through 4.3.1 contains a prototype poisoning vulnerability in the mergeObject() function that fails to properly validate keys being written to target objects. Attackers can supply malicious source objects in merge operations to inject attacker-controlled properties into the returned object's prototype, causing applications to inherit unintended values when accessing properties without own-property checks.

### CVE-2026-93752

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-09-18T18:18:34.320 |

CSSOM through 0.5.0 contains a denial of service vulnerability in CSSStyleDeclaration.setProperty() that fails to validate reserved property names. Attackers can supply a stylesheet with a declaration named length to replace the internal counter and trigger excessive memory allocation during cssText serialization, causing process termination.

### CVE-2026-93749

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-09-18T18:18:33.480 |

source-map-js through 1.2.1 fails to validate the per-section offset line value in indexed source maps, allowing attackers to specify arbitrary numeric values. Attackers can supply extremely large offset line values that cause synchronous event loop blocking for extended periods, preventing the service from handling other requests.

### CVE-2026-93748

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-524` |
| Published | 2026-09-18T18:18:33.330 |

http-cache-semantics through 4.2.0 fails to properly validate security-zeroed cache entries when processing client max-stale directives, allowing unauthenticated attackers to retrieve cached responses belonging to other users. Attackers can request the same URL with a large max-stale value to obtain another user's Set-Cookie session credentials from shared-cache entries that were deliberately zeroed for security reasons.

### CVE-2026-62943

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-18T17:16:59.167 |

btrbk is a tool for creating snapshots and remote backups of Btrfs subvolumes. From 0.29.0 until 0.32.7, btrbk's ssh_filter_btrbk.sh constructs allow_stream_match with a start anchor but without an end-of-string anchor for the complete command. A user restricted through an authorized_keys forced command can append a trailing pipe command after a valid btrbk command prefix, bypassing the allowlist and executing arbitrary commands with the privileges of the backup-target SSH account. Deployments that do not use ssh_filter_btrbk.sh in authorized_keys are not affected. This issue is fixed in version 0.32.7.

### CVE-2026-93690

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-09-18T16:17:16.000 |

uri-js through 4.4.1 contains a denial of service vulnerability in the removeDotSegments function that loops infinitely when a path segment begins with Unicode line or paragraph separators. Attackers can trigger this by calling removeDotSegments directly or through normalize/resolve functions with IRI handling enabled, causing the Node.js event loop to block indefinitely until heap exhaustion.

### CVE-2026-93688

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-18T16:17:15.683 |

SGLang through 0.5.19 in prefill/decode disaggregation mode with Mooncake KV transfer backend fails to validate bootstrap_room values, allowing unbounded transfer state allocation. Unauthenticated attackers can reach the decode engine's POST /generate endpoint and submit arbitrary bootstrap_room values to exhaust prefill process memory until out-of-memory termination.

### CVE-2026-93687

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-18T16:17:15.507 |

braces through 3.0.3 contains a stack overflow vulnerability in the recursive AST walkers that lack depth guards. Attackers can supply deeply nested brace patterns under the character limit to exhaust the call stack and terminate the Node.js process with an uncaught RangeError.

### CVE-2026-88259

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-18T16:17:14.207 |

CareCam CM2507 IP cameras do not require authentication for access to its network video streaming service. An unauthenticated attacker with network access to the affected device could retrieve live camera video.

### CVE-2026-86520

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-18T16:17:13.820 |

Bransys ELD is shipped with hardcoded MQTT credentials, which will grant read access to real-time data for every active device across a subset of carriers that were connected to the affected MQTT broker.

### CVE-2026-84398

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-258` |
| Published | 2026-09-18T16:17:12.057 |

CM2507 IP cameras accept an empty password for a privileged account exposed through its ONVIF management service. An attacker with network access to the affected device could access privileged management functions and obtain device, user, media-profile, and stream configuration information.

### CVE-2026-81942

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-18T16:17:10.383 |

PLANET IGS-5225-8P2T4S industrial managed switch V1 and V2 firmware versions before 1.2412b260707 and 2.2412b260519 contain an OS command injection vulnerability in the web server. User-supplied input is passed to system() without sufficient filtering, allowing a remote authenticated attacker to execute arbitrary commands on the underlying operating system and escalate privileges to root.

### CVE-2026-68914

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-674` |
| Published | 2026-09-18T16:17:08.897 |

Mojolicious is a real-time web framework for Perl. Prior to 9.47, the pure-Perl implementation of Mojo::JSON does not limit nesting depth when Cpanel::JSON::XS is unavailable or MOJO_NO_JSON_XS is enabled. An attacker who can supply untrusted JSON to decode_json, from_json, or j can submit deeply nested arrays or objects, causing unbounded recursion, memory exhaustion, and a process crash. Applications using the Cpanel::JSON::XS backend are not affected because that backend already enforces a nesting limit. This issue is fixed in version 9.47.

### CVE-2026-93657

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-18T15:17:22.190 |

hickory-resolver versions before 0.26.2 fail to propagate bogus DNSSEC proof states through the Resolver::lookup() and Resolver::lookup_ip() APIs, allowing invalid records to be returned as successful results. Attackers controlling the answering zone or positioned on the network path can have forged DNS records accepted as validated, bypassing DNSSEC authentication checks.

### CVE-2026-77929

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-18T15:17:13.287 |

ClipBucket v5 before 5.5.3-#182 contains a file upload vulnerability that allows authenticated users to achieve remote code execution by uploading a PHP file with valid image magic bytes through the photo upload endpoint. The FileUpload::manageFile() function in fileupload.class.php fails to update the file extension after MIME validation, allowing an attacker-controlled .php extension to persist on disk and execute as PHP via PHP-FPM when the uploaded file is retrieved.

### CVE-2026-93742

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-19T09:16:34.740 |

A weakness has been identified in Totolink A3002MU Hh-B20211125.1046. Affected by this issue is the function formWsc of the file /boafrm/formWsc. This manipulation of the argument localPin causes command injection. The attack can be initiated remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-88926

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-19T07:16:33.377 |

The VikRentItems Flexible Rental Management System WordPress plugin before 1.2.4 does not sanitise and escape some of its parameters before using them in SQL statements, allowing unauthenticated users to perform SQL injection attacks.

### CVE-2026-93923

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-19T00:16:57.963 |

SiYuan through 3.8.4 fails to escape heading style attributes when rendering outline and bookmark dock HTML, allowing stored cross-site scripting. Attackers can supply crafted notebooks or call administrative endpoints to inject malicious style values that execute in the Electron renderer with full system access.

### CVE-2026-93922

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-19T00:16:57.783 |

SiYuan through 3.8.4 renders notebook names as raw HTML in the Daily Note picker dialog without escaping, allowing stored cross-site scripting in the Electron renderer. Attackers can create notebooks with HTML payloads in names that execute JavaScript with Node.js access when the picker opens, enabling operating system command execution.

### CVE-2026-93739

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-18T22:17:10.710 |

A vulnerability was determined in Totolink A3002MU Hh-B20211125.1046. This impacts the function formWlAc of the file /boafrm/formWlAc. Executing a manipulation of the argument submit-url can lead to buffer overflow. The attack may be performed from remote. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-93738

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-18T21:18:48.660 |

A vulnerability was found in Totolink A3002MU Hh-B20211125.1046. This affects the function formSchedule of the file /boafrm/formSchedule. Performing a manipulation of the argument webpage results in buffer overflow. The attack is possible to be carried out remotely. The exploit has been made public and could be used.

### CVE-2026-68928

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-749;CWE-862;CWE-926` |
| Published | 2026-09-18T21:17:14.377 |

Acode is a powerful text and code editor for Android. From 1.11.6 until 1.12.7, com.foxdebug.acode.rk.exec.terminal.TerminalService is declared as an exported service in src/plugins/terminal/plugin.xml without a binding permission, and src/plugins/terminal/src/android/TerminalService.java does not verify the caller. Any installed Android application can bind the service and send MSG_EXEC with an attacker-controlled cmd value, which the terminal implementation passes to ProcessBuilder with sh -c inside Acode's UID. This allows a zero-permission local application to execute commands with access to Acode private data, remote credentials, Storage Access Framework grants, and runtime permissions without additional interaction at attack time. This issue is fixed in version 1.12.7.

### CVE-2026-81626

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:23.723 |

IBM Guardium Data Protection 12.2 is vulnerable to a SQL injection vulnerability in the Load Balancer Groups component. An unauthenticated user can inject SQL statements through the Load Balancer Servlet endpoint, potentially resulting in unauthorized access to data and impact to the confidentiality, integrity, and availability of the affected system.

### CVE-2026-17619

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:10.077 |

IBM Platform RTM is vulnerable to SQL injection. A remote attacker could send specially crafted SQL statements, which could allow the attacker to view, add, modify, or delete information in the back-end database.

### CVE-2026-61551

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-18T18:17:08.393 |

Icinga 2 is an open source monitoring system. Prior to 2.14.9, 2.15.4, and 2.16.2, parsing deeply nested JSON can exhaust the call stack because nesting depth is not bounded. The affected JSON parsing paths are reachable by unauthenticated network clients through the Icinga 2 service on TCP port 5665, allowing a remote attacker to crash the process, while possible code execution has not been demonstrated. This issue is fixed in versions 2.14.9, 2.15.4, and 2.16.2.

### CVE-2026-93758

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-18T17:17:07.580 |

An insecure direct object reference in the nested attributes handling of the Mongoid object-document mapper may allow a user with basic application privileges to reference a record identifier that is not their own. Processing such a request can cause that record to be looked up without the usual ownership or scoping restrictions, then updated and linked to the requesting user's own record. This may result in unintended disclosure and unauthorized modification of data belonging to other users of the application.

### CVE-2025-61682

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T16:17:03.717 |

Semantic MediaWiki is a free, open-source extension to MediaWiki that lets users store and query data within the wiki's pages. Versions starting in 3.1.0 and prior to 7.0.0 insert the unsanitized value of a data attribute into the DOM as HTML, allowing for stored XSS through wikitext. Version 7.0.0 patches the issue.

### CVE-2026-61821

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-18T20:17:20.220 |

pg_partman is a PostgreSQL extension that manages partitioned tables by time or ID. Prior to 5.5.0, drop_partition_id() and drop_partition_time() use part_config.retention_schema as the target for ALTER TABLE SET SCHEMA and accept any nonempty schema name. A role with partman_user access can select a target schema where the role lacks the normal CREATE privilege, and the background worker performs the relocation with pg_partman_bgw.role privileges, which default to PostgreSQL superuser, bypassing the authorization check that a normal ALTER TABLE SET SCHEMA operation would enforce. This permits unauthorized relocation of retained child tables between schemas. This issue is fixed in version 5.5.0.

### CVE-2026-61820

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:20.067 |

pg_partman is a PostgreSQL extension that manages partitioned tables by time or ID. Prior to 5.5.0, inherit_template_properties() manually surrounds primary-key column names from pg_attribute.attname with double quotes without escaping embedded double-quote characters. A partman_user who owns a template table can create a crafted column name that breaks out of the generated ALTER TABLE ADD PRIMARY KEY identifier when the background worker applies the key to a child partition. The generated SQL then executes with pg_partman_bgw.role privileges, which default to PostgreSQL superuser, permitting database-wide compromise and operating-system command execution as the PostgreSQL service account. The crafted catalog identifier persists until removed and can trigger again during later partition creation. This issue is fixed in version 5.5.0.

### CVE-2026-61819

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:19.927 |

pg_partman is a PostgreSQL extension that manages partitioned tables by time or ID. Prior to 5.5.0, when pg_jobmon is installed and part_config.jobmon is true, exception handlers in multiple pg_partman functions place p_parent_table verbatim inside a SQL string literal used to call pg_jobmon.add_job(). A partman_user can create a parent-table name containing a single quote that terminates the literal and injects SQL when an affected exception path runs. If pg_partman_bgw reaches that path, the injected SQL executes with pg_partman_bgw.role privileges, which default to PostgreSQL superuser, permitting database-wide compromise and operating-system command execution as the PostgreSQL service account. The persistent part_config row can trigger the escalation again on later maintenance ticks. This issue is fixed in version 5.5.0.

### CVE-2026-61818

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:19.780 |

pg_partman is a PostgreSQL extension that manages partitioned tables by time or ID. Prior to 5.5.0, undo_partition() reads part_config.time_encoder as unrestricted text and interpolates it without identifier quoting into a dynamically executed SELECT statement. A role with partman_user access can store SQL rather than a function name, and the SQL executes with the privileges of the caller that invokes undo_partition(). The function is not part of the default background-worker path, which limits the automatic superuser escalation described by the related create-partition vulnerability, but a privileged caller can still have its available confidentiality, integrity, and availability permissions abused. This issue is fixed in version 5.5.0.

### CVE-2026-61817

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:19.163 |

pg_partman is a PostgreSQL extension that manages partitioned tables by time or ID. Prior to 5.5.0, run_maintenance(), show_partitions(), show_partition_info(), undo_partition(), and partition_data_time() interpolate the writable part_config.time_dncoder text value without identifier quoting into dynamic SQL. A role with the documented partman_user privileges can store SQL rather than a decoder function name. When an affected operation later uses the poisoned value, including pg_partman_bgw maintenance for a text- or UUID-keyed set, the SQL executes with the operation's privileges, which can be the default PostgreSQL superuser background-worker role. The persistent row can restore elevated access on later ticks, and successful exploitation can permit database-wide compromise and operating-system command execution as the PostgreSQL service account. This issue is fixed in version 5.5.0.

### CVE-2026-81943

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-09-18T16:17:10.577 |

PLANET IGS-5225-8P2T4S industrial managed switch V1 and V2 firmware versions before 1.2412b260707 and 2.2412b260519 contain active debug functionality in the embedded software. An attacker with privileged access to the device can enable this debug mode to execute arbitrary code on the underlying operating system and gain root-level access.

### CVE-2026-93760

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-09-18T18:18:34.780 |

Mongoid does not restrict which query operators may come from caller-supplied filter data when an application hands that data to its query-building methods. In an application that forwards externally supplied filter parameters in this way, a party with no credentials may influence how the database evaluates the query. This may result in unintended disclosure of stored field values and in reduced database performance.

### CVE-2026-63199

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-18T18:17:09.980 |

Perses is an open-source dashboard and visualization project for observability data. From 0.43.0 until 0.54.0-rc.0, the datasource creation and unsaved datasource proxy paths authorize the caller on a Datasource or GlobalDatasource scope but do not require read permission for the separately grantable associated project or global Secret before resolving it. A low-privilege user with GlobalDatasource:create or corresponding project datasource creation rights can attach a project or global Secret that the user cannot otherwise read, point the datasource at a service controlled by the user, and cause Perses to send the decrypted secret in plaintext, bypassing project and global scope separation. This issue is fixed in version 0.54.0-rc.0.

### CVE-2026-93765

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-09-18T17:17:07.730 |

Mongoid contains an unsafe reflection weakness in the document persistence layer of its object-document mapping code. Input whose keys are passed through from an unauthenticated party by an embedding application can cause unintended internal method invocation instead of the intended array field update. This may result in unintended removal of stored records and in the embedding application becoming unresponsive.

### CVE-2026-63638

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-18T16:17:08.283 |

OpenImageIO is a toolset for reading, writing, and manipulating image files of any image file format relevant to VFX / animation. Prior to 3.0.21.0, 3.1.16.0, and 3.2.0.3-beta1, A crafted cineon image can declare unsupported component bit depth 26. cineoninput::open() maps it to a 32-bit imagespec, but libcineon maps the unsupported depth to an 8-byte value, so cineoninput::read_native_scanline() causes attacker-controlled data to be written beyond the 4-byte-per-pixel caller buffer, resulting in a heap out-of-bounds write and memory corruption. The affected implementation is identified by src/cineon.imageio/cineoninput.cpp, CineonInput::open(), CineonInput::read_native_scanline(), ComponentDataSize(), bit depth 26, and ImageSpec, which define the relevant source path, functions, state, and trigger. This issue is fixed in versions 3.0.21.0, 3.1.16.0, and 3.2.0.3-beta1.

### CVE-2026-57228

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-18T21:17:01.367 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. From 7.0.13 until 7.0.17, the SMTP MIME quoted-printable decoder in src/util-decode-mime.c can read one byte past a heap buffer when a quoted-printable escape sequence is split across traffic chunks and the following chunk contains exactly one byte. Crafted SMTP traffic can trigger the out-of-bounds read and crash Suricata when decode-quoted-printable MIME decoding is enabled. This issue is fixed in version 7.0.17.

### CVE-2026-93838

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-18T20:17:33.900 |

SGLang versions through 0.5.20 contain an unbounded memory allocation vulnerability in handle_staging_req() that fails to validate chunk_idx from ZMQ STAGING_REQ frames in prefill/decode disaggregation deployments. Attackers with access to the decode engine's internal ZMQ rank port can send a frame with an extremely large chunk_idx value, causing the scheduler to allocate memory until the system runs out and terminates the process.

### CVE-2026-93750

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-09-18T18:18:33.633 |

http-cache-semantics through 4.2.0 contains a cache validation vulnerability in the _varyMatches() function that fails to properly validate Vary header wildcards due to byte-for-byte string comparison. Attackers can request URLs previously fetched by other clients to receive cached responses intended for different users, disclosing sensitive information across clients.

### CVE-2026-91127

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-83` |
| Published | 2026-09-18T18:18:02.250 |

File Viewer is a browser-native viewer for Office, PDF, CAD, archive, and other files in private and internal web applications. Prior to @file-viewer/doc 2.3.1 and msdoc-viewer 0.2.2, the legacy DOC renderer emitted document-controlled hyperlink targets into generated HTML after character escaping but without restricting URL schemes. A crafted legacy DOC file could place javascript:, vbscript:, data:, or another unsafe scheme in a rendered link, and script could execute in the embedding application's origin when a user clicked the link. The fix blocks external document links by default, allows only HTTP(S), mail, telephone, safe relative URLs, and internal bookmarks when external links are explicitly enabled, and applies mount-boundary sanitization as defense in depth. This issue is fixed in @file-viewer/doc 2.3.1 and msdoc-viewer 0.2.2.

### CVE-2026-55556

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-18T17:16:57.580 |

Rsyslog is a rocket-fast system for log processing. From 8.2110.0 until 8.2604.0, the optional imhttp module's parse_auth_header function in contrib/imhttp/imhttp.c allocates a zero-byte heap buffer with calloc(0, len) when an HTTP Basic Authorization value exceeds its fixed work buffer, then passes that pointer to apr_base64_decode. An unauthenticated remote attacker can send an oversized encoded credential to an imhttp endpoint configured for Basic Authentication, causing decoded data to overwrite adjacent heap memory before credential validation. Deployments that do not install, load, and use imhttp with Basic Authentication are not affected. The demonstrated impact is a process crash that interrupts log collection, and code execution has not been demonstrated. This issue is fixed in version 8.2604.0.

### CVE-2026-86689

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-18T16:17:14.047 |

Bransys ELD is shipped with hardcoded MQTT credentials, which will grant read access to real-time data for every active device across a subset of carriers that were connected to the affected MQTT broker.

### CVE-2026-93569

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-18T15:17:20.743 |

A flaw was found in Netty. A remote unauthenticated attacker can exploit a vulnerability in Netty's HTTP/1 to HTTP/2 conversion process. When an HTTP/1 request includes both an absolute-form request-target and a conflicting Host header, Netty incorrectly prioritizes the Host header for the HTTP/2 :authority field, discarding the original request-target authority. This inconsistency can allow an attacker to bypass security controls in Netty-based proxies or gateways, potentially leading to unauthorized access, cache poisoning, or misrouting of requests.

### CVE-2026-85658

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-19T08:16:54.770 |

The Paid Membership Plugin, Ecommerce, User Registration Form, Login Form, User Profile & Restrict Content – ProfilePress plugin for WordPress is vulnerable to arbitrary shortcode execution in all versions up to, and including, 4.17.2 This is due to the software allowing users to execute an action that does not properly validate a value before running do_shortcode. This makes it possible for authenticated attackers, with subscriber-level access and above, to execute arbitrary shortcodes.

### CVE-2026-86814

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-19T07:16:33.167 |

The UsersWP  WordPress plugin before 1.5.10 does not verify that a social login provider has confirmed ownership of an email address before using it to resolve an existing account, allowing unauthenticated attackers to log in as any user, including administrators, whose email address they can assert through a provider account of their own.

### CVE-2026-88097

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-18T21:18:45.913 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-84241

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-18T20:17:29.013 |

IBM Guardium Data Protection 12.2 could allow a remote attacker to bypass security restrictions due to improper authorization.

### CVE-2026-84108

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T20:17:28.763 |

IBM Guardium Data Protection 12.2 could allow a remote attacker to execute arbitrary code due to improper neutralization of input during web page generation.

### CVE-2026-84085

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-18T20:17:28.137 |

IBM Guardium Data Protection 12.2 could allow a remote attacker to execute arbitrary OS commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-84081

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-18T20:17:27.613 |

IBM Guardium Data Protection 12.2 could allow a remote attacker to bypass security restrictions due to improper certificate validation.

### CVE-2026-84077

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-18T20:17:27.360 |

IBM Guardium Data Protection 12.2 could allow a remote attacker to bypass security restrictions due to a cross-site request forgery vulnerability.

### CVE-2026-82892

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-18T20:17:25.147 |

IBM Guardium Data Protection 12.2 could allow a remote attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-11727

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-18T20:17:04.050 |

IBM MQ for HPE NonStop 8.1.0 through 8.1.0.40 IBM MQ C client could allow a remote attacker to cause a denial of service or potentially execute arbitrary code due to improper validation of queue manager responses when requesting AMS policy data.

### CVE-2026-11726

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-18T20:17:03.903 |

IBM MQ for HPE NonStop 8.1.0 through 8.1.0.40 could allow an authenticated attacker to obtain sensitive information or cause a denial of service due to improper validation of message header offset values.

### CVE-2026-81179

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-807` |
| Published | 2026-09-18T18:17:15.617 |

SysReptor is a fully customizable pentest reporting platform. Prior to 2026.58, installations that enable password reset by email while configuring ALLOWED_HOSTS with a wildcard accept an attacker-controlled Host header when generating a password reset link. An unauthenticated attacker can request a reset email whose link points to an attacker-controlled system, and a victim who follows that link can disclose the reset token, allowing the attacker to reset the victim's password and take over the account. Exploitation also requires a configured email gateway and an email address for the victim, while some reverse proxy configurations may reject the hostile Host header. This issue is fixed in version 2026.58.

### CVE-2026-62278

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-18T18:17:09.673 |

LubeLogger is a self-hosted, open-source, web-based vehicle maintenance and fuel mileage tracker. Prior to 1.6.8, authenticated non-administrative users could reach HandleTranslationFileUpload and influence the name passed from Controllers/FilesController.cs to RenameFile in Helper/FileHelper.cs. RenameFile constructed newFilePath with string replacement and moved the uploaded file without verifying the resolved absolute path remained under the web root or data directory. A crafted upload name could therefore move an uploaded file outside the intended storage directory, enabling unauthorized file placement or overwrite with the privileges of the application process. This issue is fixed in version 1.6.8.

### CVE-2026-77239

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-18T17:17:00.200 |

WACRM is a self-hostable CRM template for WhatsApp. In version 0.7.0 and earlier, WACRM flow and automation write routes authenticate account viewers but do not enforce the agent role before using a service-role database client that bypasses row-level security. In src/app/api/flows/[id]/route.ts, src/app/api/flows/[id]/activate/route.ts, and src/app/api/flows/route.ts, a viewer can create, edit, activate, or delete flows because membership-only checks are followed by service-role writes. In src/app/api/automations/route.ts and src/app/api/automations/engine/route.ts, a viewer can create active automations and trigger outbound WhatsApp actions without the role required by the underlying write policies. This can permit unauthorized workflow changes, destructive flow deletion, and outbound actions from a role intended to be read-only. This vulnerability is fixed with commit 03e851bea56dcf6bb21ff1b80ba531372bf3269f.

### CVE-2026-61833

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-18T17:16:59.010 |

zot is a container image and artifact registry based on the Open Container Initiative Distribution Specification. Prior to 2.1.18, the bearer authentication handler in pkg/api/authn.go maps every HTTP method other than GET and HEAD to the push action, so DELETE requests are not checked for the distinct delete permission. Bearer-authenticated requests also bypass the fine-grained DistSpecAuthzHandler path in pkg/api/authz.go, while DeleteManifest and DeleteBlob perform no independent delete-permission check. A remote attacker with a bearer token limited to pull and push actions can therefore delete manifests and blobs within the token's repository scope, making images unavailable and allowing repository history to be altered despite the token lacking delete authorization. This issue is fixed in version 2.1.18.

### CVE-2026-61548

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-18T17:16:58.190 |

Rsyslog is a rocket-fast system for log processing. From 7.5.4 until 8.2606.0, the optional mmpstrucdata plugin's parseSD_PARAM function in plugins/mmpstrucdata/mmpstrucdata.c stores RFC5424 parameter values in a fixed pVal[32 * 1024] stack buffer and calls parsePARAM_VALUE without supplying the destination size. A remote unauthenticated attacker whose crafted RFC5424 message reaches an action using mmpstrucdata can provide a structured-data parameter larger than that buffer when MaxMessageSize permits it, causing an attacker-controlled stack overwrite. Deployments that do not install and use the plugin, or whose effective message-size limit remains below the required threshold, are not affected by this issue. The demonstrated impact is a crash and interruption of log collection; code execution is not demonstrated. This issue is fixed in version 8.2606.0.

### CVE-2026-54148

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-18T16:17:06.823 |

http4k is a functional toolkit for Kotlin HTTP applications. Prior to 4.51.0.0, 5.42.0.0, and 6.50.0.0, DigestAuthProvider.verify in http4k-security-digest does not compare the uri parameter in an Authorization: Digest response with the actual request URL. An attacker who captures a valid Digest authentication response can replay it against another URL served by the same realm, bypassing the per-request-URI binding and potentially gaining unauthorized read or write access. This issue is fixed in versions 4.51.0.0, 5.42.0.0, and 6.50.0.0.

### CVE-2026-10027

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-18T16:17:03.873 |

IBM MQ could allow a remote attacker to cause a denial of service or execute arbitrary code due to a buffer overflow when processing malformed compressed data on channels configured with compression enabled.

### CVE-2026-85574

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-19T07:16:32.860 |

The Unbounce Landing Pages WordPress plugin before 1.1.5 does not perform any authorisation check when updating the configuration its front-end proxy relies on, allowing any authenticated user, such as a subscriber, to point that proxy at a host they control and have arbitrary content served from the site's own origin.

### CVE-2026-61721

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-09-18T20:17:18.567 |

FluidSynth is a software synthesizer based on the SoundFont 2 specifications. From 2.5.0 until 2.5.6, the native DLS loader assigns file-controlled wsmp.loop_start and wsmp.loop_length values to samples without calling fluid_sample_validate() or fluid_sample_sanitize_loop(). A crafted DLS file can place sample loop points beyond the sample buffer, causing out-of-bounds reads during audio rendering, undefined behavior, possible memory disclosure, and denial of service. Builds compiled with the CMake option enable-native-dls set to OFF do not expose the affected parser. This issue is fixed in version 2.5.6.

### CVE-2026-84089

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-18T20:17:28.390 |

IBM Guardium Data Protection 12.2 could allow a local attacker to gain elevated privileges due to improper privilege management.

### CVE-2026-84083

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-18T20:17:27.877 |

IBM Guardium Data Protection 12.2 is vulnerable to local privilege escalation via the SUID-root nmap_wrapper binary on the Collector appliance. A local attacker with low-privileged access to the Collector can exploit insufficient argument validation in the SUID binary to execute arbitrary commands as root, resulting in full compromise of the Collector appliance.

### CVE-2026-82893

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-18T20:17:25.273 |

IBM Guardium Data Protection 12.2 could allow a local attacker to gain elevated privileges due to improper privilege management.

### CVE-2026-61714

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125;CWE-787` |
| Published | 2026-09-18T20:17:18.270 |

FluidSynth is a software synthesizer based on the SoundFont 2 specifications. From 2.2.4 until 2.5.6, configuring synth.midi-channels above 16 allows the MIDI player to index _fluid_player_t::channel_isplaying outside its fixed-size heap allocation while tracking active channels. The resulting out-of-bounds reads and writes invoke undefined behavior and may compromise confidentiality, integrity, or availability. No crafted MIDI file is required because the unsafe condition is created by the channel-count configuration itself. Keeping synth.midi-channels at its default value of 16 avoids the vulnerable path. This issue is fixed in version 2.5.6.

### CVE-2026-46655

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-18T17:16:57.373 |

virtio-win provides Windows paravirtualized drivers for QEMU and KVM. From mm210 until mm320, the Viosock driver permits a low-privilege local process to submit an IOCTL_SELECT request with attacker-controlled VIRTIO_VSOCK_SELECT.Fdss[*].fd_count values that overflow the 32-bit sum used by VIOSockSelect for bounds checking. The wrapped sum can pass the FD_SETSIZE check even though an individual descriptor count is much larger than the expected limit. VIOSockSelectCopyFds then iterates using the unchecked count and writes beyond the allocated pPkt->Fds array in the NonPagedPool kernel heap. Successful exploitation can corrupt kernel memory and enable privilege escalation in a Windows guest running the driver. This issue is fixed in mm320.

### CVE-2026-63422

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-09-18T16:17:07.987 |

OpenImageIO is a toolset for reading, writing, and manipulating image files of any image file format relevant to VFX / animation. Prior to 3.0.21.0, 3.1.16.0, and 3.2.0.3-beta1, A valid tiled openexr image whose width is not a multiple of its tile width can trigger an overflow when a caller reads a partial edge-tile rectangle. openexrinput::read_native_tiles() copies each row into the caller buffer using the padded whole-tile scanline_stride rather than user_scanline_bytes for the requested rectangle, resulting in a heap out-of-bounds write and memory corruption. The affected implementation is identified by src/openexr.imageio/exrinput.cpp, OpenEXRInput::read_native_tiles(), partial edge tile, user_scanline_bytes, and scanline_stride, which define the relevant source path, functions, state, and trigger. This issue is fixed in versions 3.0.21.0, 3.1.16.0, and 3.2.0.3-beta1.

### CVE-2026-63419

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-18T16:17:07.687 |

OpenImageIO is a toolset for reading, writing, and manipulating image files of any image file format relevant to VFX / animation. Prior to 3.0.21.0, 3.1.16.0, and 3.2.0.3-beta1, A zbuffer-only tiled iff is exposed with a 16-bit public imagespec while the decoder retains a 32-bit internal pixel size. iffinput::read_native_tile() copies according to m_header.pixel_bytes() rather than imagespec::tile_bytes(true), and a failed read can leave m_buf nonempty so a later call copies partially initialized data into the undersized caller buffer, resulting in a heap out-of-bounds write and memory corruption. The affected implementation is identified by src/iff.imageio/iffinput.cpp, IffInput::read_native_tile(), ImageSpec::tile_bytes(true), m_header.pixel_bytes(), ZBUFFER, and m_buf, which define the relevant source path, functions, state, and trigger. This issue is fixed in versions 3.0.21.0, 3.1.16.0, and 3.2.0.3-beta1.

### CVE-2026-93872

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-18T20:17:35.250 |

Cotonti 1.0.0 passes the base64-decoded cb parameter to unserialize() without allowed_classes restriction in the comments plugin EditAction. Registered users with comment write permissions can instantiate arbitrary PHP objects and potentially achieve file write or code execution through gadget chains.

### CVE-2026-84105

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:28.510 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to obtain sensitive information due to improper neutralization of special elements used in an SQL command.

### CVE-2026-81944

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-18T16:17:11.270 |

PLANET IGS-5225-8P2T4S industrial managed switch V1 and V2 firmware versions before 1.2412b260707 and 2.2412b260519 contain a stack-based buffer overflow in the web server. Insufficient bounds checking on data copied into a stack buffer allows a remote authenticated attacker to cause a denial of service or potentially execute arbitrary code on the underlying operating system.

### CVE-2026-84239

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T20:17:28.887 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to obtain sensitive information due to improper neutralization of special elements used in an SQL command.

### CVE-2026-84076

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-18T20:17:27.230 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to bypass security restrictions due to improper authorization.

### CVE-2026-82896

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-18T20:17:25.393 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to traverse directories on the system due to a path traversal vulnerability.

### CVE-2026-67549

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-122;CWE-131;CWE-787` |
| Published | 2026-09-18T16:17:08.733 |

OpenImageIO is a toolset for reading, writing, and manipulating image files of any image file format relevant to VFX / animation. Prior to 3.1.16.0, A crafted 1-bit contiguous cmyk tiff is exposed through a native uint1 imagespec, so callers allocate a bit-packed buffer. tiffinput::read_native_scanline_locked() nevertheless invokes tiffinput::bit_convert() with 8-bit output and writes one expanded byte per value into that smaller buffer, resulting in a heap out-of-bounds write and memory corruption. The affected implementation is identified by src/tiff.imageio/tiffinput.cpp, TIFFInput::bit_convert(), TIFFInput::read_native_scanline_locked(), PHOTOMETRIC_SEPARATED, 1-bit CMYK, and native uint1 ImageSpec, which define the relevant source path, functions, state, and trigger. This issue is fixed in 3.1.16.0.

### CVE-2026-1255

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-19T09:16:34.030 |

The YS LeadGen plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 2.1.4 due to the 'ysleadgen_get_captured_data' AJAX action being accessible to unauthenticated users. This makes it possible for unauthenticated attackers to retrieve all captured form submission data, including personally identifiable information (PII) such as names, email addresses, and message content submitted through YS LeadGen forms.

### CVE-2026-92404

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-19T07:16:33.790 |

The MgoSync  WordPress plugin before 2.1.7 does not have authorization controls on one of its REST API endpoints, allowing unauthenticated users to retrieve the stored WooCommerce API credentials, including a read/write consumer key and secret, from a configured site.

### CVE-2026-87909

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-19T03:17:15.853 |

The WP Photo Album Plus plugin for WordPress is vulnerable to Remote Code Execution in all versions via the wppa_image_magick function. This is due to insufficient sanitization of the multipart upload filename before concatenation into an ImageMagick command string executed via exec(), with only escapeshellcmd() applied to the whole command rather than quoting individual arguments. This makes it possible for authenticated attackers, with subscriber-level access and above, to execute code on the server. escapeshellcmd() escapes shell metacharacters but does not prevent argument injection because spaces remain as argument separators, and the filename sanitization applied at the database layer is never applied to the physical temporary file path used for ImageMagick processing.

### CVE-2026-71418

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-18T21:18:08.590 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. From 8.0.0 until 8.0.6, DNS-over-HTTP/2 processing in rust/src/http2/http2.rs retains previously processed HTTP/2 DATA frame contents instead of clearing the internal buffer. Multiple DATA frames with the EndOfStream flag set can grow the buffer to its 65 KiB limit while causing all prior contents to be processed again, producing quadratic CPU complexity, degraded packet processing, loss of monitoring visibility, or denial of service. This issue is fixed in version 8.0.6.

### CVE-2026-63452

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-409` |
| Published | 2026-09-18T21:17:04.667 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. From 8.0.0 until 8.0.6, the HTTP/1 parser limits decompression work per transaction but does not limit how many small brotli compression bombs a single flow can submit. With response-body-decompress-layer-limit enabled, repeated compressed responses make the decompression paths in rust/htp perform expensive work for every transaction, degrading packet processing and potentially causing loss of monitoring visibility or denial of service. This issue is fixed in version 8.0.6.

### CVE-2026-63447

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-18T21:17:03.913 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. From 8.0.5 until 8.0.6, the FTP parser in src/app-layer-ftp.c can continue allocating transactions after app-layer.protocols.ftp.max-tx is reached while processing one large chunk of FTP command data. The oversized transaction list is repeatedly processed with quadratic complexity after the too_many_transactions event, allowing crafted FTP traffic to degrade packet processing, reduce monitoring visibility, or cause denial of service. This issue is fixed in version 8.0.6.

### CVE-2026-63446

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401;CWE-407` |
| Published | 2026-09-18T21:17:03.763 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. From 8.0.0 until 8.0.6, AppLayerParserSetTransactionInspectId() in src/app-layer-parser.c uses an inverted guard and marks only already-inspected transactions as inspected. On flows passed by a pass rule or pass-the-flow exception policy, detection is skipped, so completed transactions remain unmarked, are never freed, and are repeatedly rescanned. The per-flow list can grow without bound with quadratic cleanup cost, causing CPU and memory exhaustion. This issue is fixed in version 8.0.6.

### CVE-2026-57227

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-18T21:17:01.217 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. From 7.0.0 until 7.0.17 and 8.0.6, the MQTT parser in rust/src/mqtt/mqtt.rs permits repeated PUBREC or PUBREL messages to be appended to one transaction without a limit. Crafted MQTT traffic can grow transaction state indefinitely, consuming CPU and memory and causing slowdown or denial of service. This issue is fixed in versions 8.0.6 and 7.0.17.

### CVE-2026-92708

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-226` |
| Published | 2026-09-18T20:17:30.150 |

Svelte devalue is a JavaScript library that serializes values into strings when JSON.stringify isn't sufficient for the job. In versions 5.1.0 through 5.9.2, stringify and uneval functions serialize a typed array by emitting its entire backing ArrayBuffer rather than only the view, so serializing a Node Buffer, whose backing store is a process-wide shared pool, discloses up to 64 KB of unrelated process memory, including bytes from other in-flight requests. In a server-side-rendered framework such as SvelteKit or Nuxt, a public page whose load() returns a small Buffer, or that reads a small file, can therefore ship another user's request body or Authorization header in its HTML without authentication. Because this occurs during serialization, it fires on every such render and is not mitigated by the parse/unflatten prototype-pollution and denial-of-service guards, which only apply when parsing untrusted input. As a workaround, convert Node Buffer objects to Uint8Array before serialization. This issue has been fixed in version 5.9.3.

### CVE-2026-11716

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-18T20:17:02.837 |

IBM MQ for HPE NonStop 8.1.0 through 8.1.0.40 could allow an authenticated attacker to cause a denial of service or potentially execute arbitrary code during queue manager startup due to improper validation of cluster migration data.

### CVE-2026-85058

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-18T18:17:17.447 |

Moquette is a lightweight Java MQTT broker. Prior to 0.18.1, PostOffice.publishWill publishes a client-controlled Last Will message through publish2Subscribers without invoking the authorizator.canWrite check used by normal PUBLISH paths. When anonymous access is enabled and topic ACLs restrict writes, a remote client can set an ACL-protected topic as the Last Will Topic during CONNECT and perform an abnormal client disconnect, causing the broker to inject attacker-controlled messages into a topic for which the client lacks write permission. This issue is fixed in version 0.18.1.

### CVE-2026-69184

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-18T18:17:11.477 |

c-ares is an asynchronous resolver library. Prior to 1.34.7, ares_dns_name_parse() enforces backward DNS compression pointers but does not bound the total pointer hops or assembled name length. A malicious DNS server can send a response containing a long descending pointer chain and many resource records whose NAME or RDATA fields refer to the chain, causing repeated decompression work that grows quadratically with message size. A single crafted response can stall the single-threaded c-ares event loop and deny DNS resolution, without causing memory corruption or information disclosure. This issue is fixed in version 1.34.7.

### CVE-2026-32641

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-703` |
| Published | 2026-09-18T18:17:06.467 |

Parseable is a log analytics platform built for high-volume data ingestion and analysis. Prior to 3.0.0, src/handlers/http/middleware.rs uses unwrap() while parsing the x-amz-firehose-common-attributes header before authentication. A remote unauthenticated attacker can supply non-UTF-8 header data, malformed JSON, or invalid derived header values that trigger a Rust panic and interrupt request handling, allowing repeated requests to deny service or cause container restart loops. This issue is fixed in version 3.0.0.

### CVE-2026-91149

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-18T17:17:05.563 |

A flaw was found in Cockpit. An unauthenticated remote attacker can exploit this vulnerability by initiating and sustaining numerous simultaneous connections to the `cockpit-tls` service. This forces the service to create an unbounded number of detached threads, consuming system resources such as memory and file descriptors. The primary consequence is a denial of service (DoS), leading to degradation or complete unavailability of the Cockpit service for legitimate users.

### CVE-2026-77301

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-18T17:17:00.507 |

adm-zip is a JavaScript library for creating and extracting ZIP archives in Node.js. Prior to 0.6.1, getData() in zipEntry.js trusts an entry's central-directory uncompressed size and allocates output memory before validating that value against the actual compressed data and decompression result. A small crafted ZIP can declare a multi-gigabyte uncompressed size, causing Buffer.alloc and decompression handling to commit excessive resident memory before CRC validation reports an error. Applications that read entries from untrusted archives can therefore be terminated by the operating system or suffer service-wide memory exhaustion. This issue is fixed in version 0.6.1.

### CVE-2026-84447

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-18T16:17:12.677 |

libheif is a HEIF and AVIF file format decoder and encoder. In 1.23.1 and earlier, crafted grid, iovl, and iden reference graphs can repeatedly decode the same base image because processed_ids is copied per branch and ImageItem::decode_image() has no shared operation budget. This vulnerability is fixed in 1.23.2.

### CVE-2026-84446

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-09-18T16:17:12.513 |

libheif is a HEIF and AVIF file format decoder and encoder. Prior to 1.23.2, crafted HEIF sequence timing and edit-list data can make Track::init_sample_timing_table() compute a logical m_num_output_samples value that exceeds the uint32_t counters used by Track_Visual::decode_next_image_sample() and Track::get_next_sample_raw_data(). The resulting comparison can never reach the oversized output count, causing non-terminating decode or raw-sample loops and bypassing max_sequence_frames. The same sequence path repeatedly calls Box_stts::get_sample_duration() and allocates Chunk::m_sample_ranges and Track::m_presentation_timeline outside MemoryHandle accounting, allowing severe CPU and memory exhaustion from a small file. This issue is fixed in version 1.23.2.

### CVE-2026-84384

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-18T16:17:11.900 |

libheif is a HEIF and AVIF file format decoder and encoder. From 1.19.0 until 1.23.2, crafted HEIF or AVIF mime metadata and unci image data can cause decompress_brotli() and do_inflate() to grow accumulated output without an effective size limit or MemoryHandle accounting. The brotli path has no output bound, while the zlib path checks only a small temporary buffer in a branch that valid streams do not reach, and overlapping icef units can decompress the same payload repeatedly. HeifContext::interpret_heif_file_images() processes multiple compressed metadata items during file opening, allowing a small file to consume unbounded memory and terminate the process. This issue is fixed in version 1.23.2.

### CVE-2026-81945

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-18T16:17:11.413 |

PLANET IGS-5225-8P2T4S industrial managed switch V1 and V2 firmware versions bfore 1.2412b260707 and 2.2412b260519 contain a stack-based buffer overflow in the web server. Insufficient bounds checking on data copied into a stack buffer allows a remote administrator to cause a denial of service or potentially execute arbitrary code on the underlying operating system.

### CVE-2026-10853

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-09-18T16:17:05.167 |

IBM MQ could allow an authenticated attacker with cluster access to cause a denial of service or potentially execute arbitrary code due to improper validation of cluster command message lengths.

### CVE-2026-10751

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-18T16:17:04.563 |

IBM MQ Java and JMS client libraries could allow an authenticated attacker to execute arbitrary code on client applications due to a deserialization filter bypass in exception handling.

### CVE-2026-10744

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-18T16:17:04.290 |

IBM MQ for HPE NonStop 8.1.0 through 8.1.0.40 could allow an authenticated attacker to cause a denial of service or potentially escalate privileges due to an integer overflow in MQINQ request validation.

### CVE-2025-14753

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-18T16:17:02.120 |

IBM Cloud Pak for Data 5.1.2 could allow a remote attacker to traverse directories on the system. An attacker could send a specially crafted URL request containing "dot dot" sequences (/../) to view arbitrary files on the system.

### CVE-2026-93652

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-18T15:17:21.917 |

Integer overflow in µD3TN v0.15.0 TCPCLv3 handshake causes heap overflow, allowing remote attackers to reliably cause DoS

### CVE-2026-93576

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-18T15:17:21.167 |

A flaw was found in Netty netty-codec-smtp. The component does not properly validate Carriage Return (CR) and Line Feed (LF) characters in the SMTP command-name field. A remote attacker, if an application routes untrusted input into this field, can embed CR/LF characters to inject arbitrary SMTP commands. This can lead to SMTP command smuggling, allowing for unauthorized email relay or spoofing of sender/recipient addresses. While the impact is significant, the real-world exploitability is considered lower as applications typically do not place user-controlled data in the command-name field.

### CVE-2026-93568

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-18T15:17:20.600 |

A flaw was found in Netty. A remote attacker could exploit this vulnerability by sending specially crafted HTTP/2 or HTTP/3 Extended CONNECT requests. Netty's HTTP-object conversion path incorrectly processes these requests as regular HTTP/1.1 CONNECT requests, leading to a loss of critical protocol and path information. This misinterpretation can allow attackers to bypass security policies, such as routing or authorization logic, in applications that rely on Netty for HTTP/2 or HTTP/3 communication, resulting in integrity loss.

### CVE-2026-93567

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-18T15:17:20.450 |

A flaw was found in Netty's HTTP/2 codec. When converting HTTP/1 CONNECT requests to HTTP/2, the component incorrectly uses the Host header instead of the CONNECT authority-form request-target for the tunnel authority. A remote attacker can exploit this by supplying a different Host header, leading to a malformed HTTP/2 CONNECT request. This can bypass security controls such as tunnel allow-lists or egress policies, resulting in integrity loss.

### CVE-2026-93565

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-1035` |
| Published | 2026-09-18T15:17:20.093 |

A flaw was found in Netty RtspDecoder. The `RtspMethods.valueOf()` function incorrectly strips trailing control bytes from method tokens in Real-Time Streaming Protocol (RTSP) requests. A remote attacker can exploit this by sending a specially crafted RTSP request, leading to method-token smuggling. This vulnerability allows an attacker to bypass method-based access controls and can also be used to launder malicious requests through Netty-based RTSP proxies, making them appear legitimate to backend systems.

### CVE-2026-93564

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1035` |
| Published | 2026-09-18T15:17:19.943 |

A flaw was found in Netty. A reference-count leak in the HAProxy PROXY-v2 message decoder allows a remote, unauthenticated attacker to send specially crafted PROXY-protocol v2 headers. This can lead to memory exhaustion, resulting in a Denial of Service (DoS) for the affected system.

### CVE-2026-93558

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1035` |
| Published | 2026-09-18T15:17:19.590 |

A flaw was found in Netty's WebSocketServerExtensionHandler. A remote, unauthenticated attacker can exploit this vulnerability by using HTTP/1.1 pipelining to send requests faster than the application can respond. This leads to an unbounded growth of a per-connection queue, consuming excessive memory. Eventually, this can cause the Java Virtual Machine (JVM) to exhaust its heap, resulting in a Denial of Service (DoS) for the affected server.

### CVE-2026-84036

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-18T20:17:26.313 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to bypass security restrictions due to improper authorization.

### CVE-2026-84975

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-297` |
| Published | 2026-09-18T18:17:17.127 |

PJSIP is a free and open source multimedia communication library written in C. In 2.17 and earlier, the OpenSSL and GnuTLS backends in pjlib/src/pj/ssl_sock_ossl.c and pjlib/src/pj/ssl_sock_gtls.c copy DNS SubjectAltName values with string functions that recalculate their length and truncate an embedded NUL byte. With server verification enabled through --tls-verify-server for the PJSIP TLS/SIPS transport, a certificate containing a DNS SubjectAltName formed from the target hostname prefix followed by an embedded NUL and an attacker-controlled suffix can therefore be accepted for the prefix hostname. An attacker who possesses such a certificate from a trusted issuer and can intercept the connection can impersonate the target server, complete the SIP session, and receive REGISTER credentials. The mbedTLS backend is not affected because it preserves the explicit string length. No fixed version is available as of this review.

### CVE-2026-84444

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-18T16:17:12.357 |

libheif is a HEIF and AVIF file format decoder and encoder. Prior to 1.23.2, when WITH_UNCOMPRESSED_CODEC is enabled, heif_context_add_image_tile() accepts an independently constructed tile whose component-plane dimensions do not match the tile geometry established by the prototype image. ImageItem_uncompressed::add_image_tile() passes that tile directly to unc_encoder::encode_tile(), which lacked the check_component_sizes() gate and sizes its output from the configured tile geometry while copying the tile's actual component-plane dimensions. An oversized component plane can therefore make unc_encoder_component_interleave::encode_tile() copy attacker-controlled data beyond the heap output buffer. This issue is fixed in version 1.23.2.

### CVE-2026-93658

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-281` |
| Published | 2026-09-18T15:17:22.360 |

uutils coreutils versions before 0.10.0 apply setuid or setgid mode to install destinations before finalizing ownership changes, allowing privileged users to leave setuid executables owned by the privileged invoker when ownership changes fail. Attackers can execute leftover setuid files with elevated privileges when ownership change operations fail on capability-restricted systems.

### CVE-2026-15664

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-19T08:16:52.763 |

The Quill Forms | Conversational Multi Step Forms, Surveys & quizzes plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Multiple Choice 'Other' Value in all versions up to, and including, 5.7.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected script executes in the context of the WordPress admin results view, making administrators the primary target when reviewing submitted form entries.

### CVE-2026-76554

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-19T07:16:32.540 |

The WP Import Export Lite WordPress plugin before 3.9.35 does not verify that the user running an import is permitted to create or modify user accounts and assign roles, allowing users granted a delegated WP Import Export Lite WordPress plugin before 3.9.35 permission, who cannot otherwise manage users, to create administrator accounts and to overwrite the credentials and role of existing accounts, including administrators.

### CVE-2026-13354

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-19T03:17:13.553 |

The Asset CleanUp: Page Speed Booster plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content in all versions up to, and including, 1.4.0.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is only exploitable on instances where combine_loaded_css has been enabled.

### CVE-2026-84086

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-18T20:17:28.270 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper limitation of a pathname to a restricted directory.

### CVE-2026-84071

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-18T20:17:26.687 |

IBM Guardium Data Protection 12.2 is vulnerable to OS command injection in the Universal Connector plugin upload functionality. A privileged authenticated attacker can provide a malicious filename that is incorporated into a shell command executed by the application, potentially resulting in arbitrary command execution with root-level privileges.

### CVE-2026-81937

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-18T20:17:24.377 |

IBM Guardium Data Protection 12.2 is vulnerable to a command injection vulnerability in the import remotelog_config file CLI command. A highly privileged authenticated user can inject shell commands through the filename parameter, potentially resulting in arbitrary command execution with root privileges and impact to the confidentiality, integrity, and availability of the affected system.

### CVE-2026-81669

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-18T20:17:24.127 |

IBM Guardium Data Protection 12.2 is vulnerable to a command injection vulnerability in the create csr wildcard CLI command. An authenticated privileged CLI user can inject arbitrary shell commands through the alias input, resulting in command execution with root privileges.

### CVE-2026-93854

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1025` |
| Published | 2026-09-18T19:17:25.440 |

In OpenStack Blazar before 17.0.1, the V2 lease API does not enforce object-level authorization on its update and delete operations (PUT /v2/leases/{lease_id} and DELETE /v2/leases/{lease_id}). The policy authorize() wrapper attempts to load the target lease to build the authorization target from its owner, but it looks up the lease under the keyword "lease_id" whereas the controller methods name the parameter "id" (and the wsme_pecan.wsexpose wrapper delivers it positionally). The lookup returns None, and thus authorization falls back to the requesting user's own project_id/user_id instead of the target lease owner. Any authenticated user who knows a lease ID can therefore modify or delete leases belonging to other users and projects, bypassing the intended ownership check.

### CVE-2026-61552

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-18T18:17:09.263 |

Icinga 2 is an open source monitoring system. From 2.4 until 2.14.9, 2.15.4, and 2.16.2, the /v1/objects API writes attacker-controlled template names into generated configuration without escaping them. An authenticated ApiUser with an objects/create/* permission can inject Icinga 2 DSL configuration, escape the intended object, create additional objects, and exceed the user's assigned privileges. This issue is fixed in versions 2.14.9, 2.15.4, and 2.16.2.

### CVE-2026-76790

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-19T07:16:32.650 |

The Estatik Real Estate Plugin WordPress plugin before 4.3.5 does not sanitise and escape several values decoded from a request parameter before reflecting them back in an unauthenticated AJAX response, leading to Reflected Cross-Site Scripting.

### CVE-2026-93852

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-18T19:17:25.267 |

In OpenStack Blazar before 17.0.1, the V2 lease listing operation (GET /v2/leases) returns leases for every project without enforcing project scoping or an administrator-only policy. Any authenticated user with access to the Blazar REST API can enumerate leases belonging to other tenants, exposing lease IDs, reservation IDs, resource IDs, and reservation metadata. The exposed lease IDs also enable the object-level authorization bypass tracked in the companion request, allowing an attacker to then modify or delete the enumerated leases.

### CVE-2026-93764

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-09-18T18:18:35.330 |

Mongoid may omit encryption rules for fields declared on embedded models when generating the client-side field-level encryption schema. Applications that enable this feature can therefore store values intended to be encrypted in readable form, with no error or warning. A party with routine read access to the database, a backup, or the underlying data files may then see data that was meant to remain unreadable outside the application.

### CVE-2026-93763

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-09-18T18:18:35.193 |

A protection mechanism failure in the object-document mapper's encryption configuration generation can cause fields that an application declared for client-side field-level encryption to be written and kept in cleartext, without any error or warning. A party holding ordinary read access to the database can then read values that were intended to be protected from that party. This may result in unintended disclosure of sensitive information.

### CVE-2026-63458

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-18T18:17:10.643 |

Perses is an open-source dashboard and visualization project for observability data. Prior to 0.54.0-beta.3, an authenticated user with viewer access to one project can supply another project through the project query parameter on project-scoped list endpoints, including /api/v1/projects/{project}/dashboards and /api/v1/datasources. The request-controlled project value is used to select dashboards, datasources, and variables without enforcing the caller's authorization for that selected project, which breaks project-level tenant isolation and exposes complete resource specifications belonging to other projects. This issue is fixed in version 0.54.0-beta.3.

### CVE-2026-63445

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-18T18:17:10.477 |

Perses is an open-source dashboard and visualization project for observability data. Prior to 0.54.0-rc.0, list endpoints used with the file-system database bind the request-controlled project query parameter into the resource Query structure without validating it against directory traversal characters, and the resulting project value is used to select database paths. An authenticated attacker can supply directory traversal segments to leave the intended project directory, read arbitrary YAML or JSON files accessible to the Perses process, and bypass project isolation to enumerate other file-backed resources. This issue is fixed in version 0.54.0-rc.0.

### CVE-2026-62279

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-18T18:17:09.830 |

LubeLogger is a self-hosted, open-source, web-based vehicle maintenance and fuel mileage tracker. Prior to 1.6.8, an authenticated user could submit caller-controlled recordIds to the DuplicateRecordsToOtherVehicles endpoint while naming destination vehicleIds the user could edit. The endpoint authorized the destination vehicles but fetched source records in Controllers/VehicleController.cs without checking UserCanEditVehicle for each existingRecord.VehicleId. This missing source-vehicle authorization allowed service, collision, upgrade, fuel, tax, supply, note, odometer, reminder, plan, inspection, and equipment records belonging to another user to be copied into an attacker-controlled vehicle, exposing record contents and attachment paths and creating persistent copies. This issue is fixed in version 1.6.8.

### CVE-2026-81505

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-18T17:17:02.103 |

Convoy is a cloud native webhooks gateway. Prior to 26.6.8, Convoy's GET /api/v1/projects/{projectID}/sources/{sourceID} endpoint authorizes access to the project in the URL, but Handler.GetSource calls sources.Service.FindSourceByID() and fetches the Source only by sourceID without confirming that its ProjectID matches the authorized project. An authenticated user or project-scoped API key holder can substitute another tenant's Source identifier and receive that Source's complete record, including unredacted AMQP, Kafka, SQS, or Google PubSub credentials. The list endpoint remains project-scoped; the single-item Source lookup is affected. This issue is fixed in version 26.6.8.

### CVE-2026-61672

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-697;CWE-863` |
| Published | 2026-09-18T17:16:58.537 |

Capsule is a multi-tenancy and policy-based framework for Kubernetes. Prior to 0.13.7, ForbiddenListSpec.ExactMatch in pkg/api/forbidden_list.go sorts denied metadata keys case-insensitively and then uses sort.SearchStrings, which assumes byte-order sorting. When an administrator's forbidden list mixes capitalized and lowercase keys or otherwise has different case-insensitive and byte ordering, the binary search can return false for a key that is present. An authenticated tenant owner can then pass the missed key through api.ValidateForbidden and bypass configured namespace, Service, or delegated node metadata restrictions, potentially influencing cluster policies, network exposure, or scheduling outside the tenant boundary. Uniformly lowercase lists whose two orderings coincide are not affected. This issue is fixed in version 0.13.7.

### CVE-2026-93737

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-18T16:17:16.340 |

Azkaban through 4.0.0 omits project permission checks in the ScheduleServlet fetchSchedule action, allowing authenticated users to read any project's schedule configuration. Attackers can supply arbitrary project and flow identifiers to retrieve sensitive schedule details including execution times, cron expressions, flow parameters, and notification email lists without proper authorization.

### CVE-2026-10030

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-18T16:17:04.020 |

IBM MQ Console allows authenticated non-administrative users to create and start queue managers due to improper authorization checks.

### CVE-2026-93660

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-18T15:17:22.667 |

SQLBot through 1.10.1 fails to verify dashboard ownership in update_resource and update_canvas endpoints, allowing authenticated workspace members to modify other users' private dashboards. Attackers can supply arbitrary dashboard IDs to rename dashboards and overwrite component data, canvas styles, and view information belonging to other workspace members.

### CVE-2026-77928

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T15:17:13.143 |

ClipBucket v5 before 5.5.3-#182 contains a blind SQL injection vulnerability that allows authenticated users to extract arbitrary database contents by submitting the msg_id parameter as an array to bypass the clean_requests() sanitization function in ClipBucket.class.php. Attackers can pass unsanitized array elements through the deletion handler in private_message.php into cb_pm::delete_msg(), which interpolates the unescaped message ID directly into a SQL query string, enabling time-based blind SQL injection to retrieve all user credential hashes and email addresses.

### CVE-2026-77927

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T15:17:12.987 |

ClipBucket v5 before 5.5.3-#182 contains a blind SQL injection vulnerability that allows authenticated users to extract arbitrary data from the database by submitting the check_photo parameter as an array to bypass the clean_requests() sanitization function in ClipBucket.class.php. Attackers can pass unsanitized array elements through the bulk deletion handler in manage_photos.php to photo_exists() in photos.class.php, where non-numeric values are interpolated directly into a SQL query, enabling time-based blind SQL injection to retrieve credential hashes and other sensitive data.

### CVE-2026-57223

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-428` |
| Published | 2026-09-18T21:17:00.787 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Prior to 7.0.17 and 8.0.6, the Windows service installation and parameter-update logic in src/win32-service.c can pass an unquoted service ImagePath to CreateServiceA. When Suricata is installed below a path containing spaces and an earlier path component is writable by a local low-privileged attacker, Windows can execute an attacker-controlled program as LocalSystem, resulting in local privilege escalation. This issue is fixed in versions 8.0.6 and 7.0.17.

### CVE-2026-73863

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:L/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-18T17:17:00.020 |

NanoMQ is an MQTT broker. Prior to 0.24.14, NanoMQ's broker-side MQTT v5 nmq_subinfo_decode() function in nng/src/sp/protocol/mqtt/mqtt_parser.c reuses len_of_varint from the outer Properties Length while parsing each SUBSCRIPTION_IDENTIFIER. A remote client can send a SUBSCRIBE packet with a multi-byte Properties Length and repeated subscription identifiers, causing get_var_integer() to begin at an incorrect offset and read beyond the heap message buffer. The flaw is reachable through the broker receive path and can crash the broker, while the separately reported topic-option off-by-one occurs later and is not this vulnerability. This issue is fixed in version 0.24.14.

### CVE-2026-63349

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-269` |
| Published | 2026-09-18T17:16:59.317 |

AnyIO is a high level asynchronous concurrency and networking framework that works on top of either Trio or asyncio. In 4.14.0, AnyIO accepts the POSIX extra_groups argument in anyio.run_process() and anyio.open_process(), but open_process() forwards the group argument to the backend instead of extra_groups. A caller that supplies extra_groups=[] to clear inherited supplementary groups can therefore launch a child that retains the parent process groups, undermining a privilege-dropping boundary. If group is also supplied, the integer group value is passed where an iterable of supplementary groups is expected and the launch can fail with TypeError. This issue affects POSIX applications that rely on AnyIO subprocess helpers to launch less-privileged child processes. This issue is fixed in version 4.14.2.

### CVE-2026-81305

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-18T16:17:10.103 |

CM2507 IP cameras automatically execute a predetermined script from removable media without verifying its authenticity or integrity. An attacker with physical access to the device could supply a malicious script and execute arbitrary code in the security context of the affected device.

### CVE-2026-7006

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-09-18T16:17:09.940 |

Sublime Text for Windows through Build 4192 (Sublime Text 4) and Build 3207 (Sublime Text 3) contains a local privilege escalation vulnerability that allows unprivileged local attackers to execute arbitrary code with elevated privileges by abusing the update staging mechanism. Attackers can place a malicious DLL in the user-writable staging directory under %LOCALAPPDATA%, mark it read-only to bypass cleanup, and have the elevated installer copy it into the protected installation directory, causing the DLL to execute in the context of any higher-privileged user who subsequently launches the application.
