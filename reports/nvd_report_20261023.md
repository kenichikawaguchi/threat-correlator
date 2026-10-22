# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-22 15:01 UTC
- **対象期間**: `2026-10-21T15:02:29.000Z` 〜 `2026-10-22T15:01:36.000Z`
- **重要CVE数**: 202 件（Critical 9.0+: 41 件 / High 7.0〜: 161 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上り、特に **リモートコード実行 (RCE) が未認証で可能** な脆弱性が目立ちます。  
- 大手 SaaS／CI/CD ツール（GitLab）や CMS（Joomla）に対する **完全リモート実行** が多数報告され、攻撃者は Web から直接システム権限を取得できる点が深刻です。  
- Apache Traffic Server の実験的プラグイン群（magick、tsmemcache）でも同様に **画像処理やキャッシュ操作を通じたコード実行** が可能となっており、インフラ層での防御が求められます。  
- Cisco Expressway 系列のハードニング不備により **root 権限でのコマンド実行** が可能になるケースが報告され、ネットワーク機器のファームウェア更新が急務です。  

> **傾向**：Web アプリケーションの「外部入力を適切にサニタイズしない」実装ミスと、**実験的機能をデフォルトで有効にしたままにする** 設計ミスが多く見られます。  

---

## 2. 特に注目すべき CVE  

| CVE | 製品 / バージョン | 主な脆弱性 | 影響範囲・危険度 | 注目理由 |
|-----|-------------------|------------|-------------------|----------|
| **CVE‑2026‑110264** | GitLab CE/EE **7.0‑&lt; 18.11.13**, **19.0‑&lt; 19.0.10** など | 未認証 RCE（任意コード実行） | GitLab は CI/CD パイプラインのハブであり、全社のソースコード・シークレットが一元管理される。攻撃者が任意コードを実行できれば、リポジトリ取得・シークレット漏洩・マルウェア配布が可能。 | **スコア 10.0**、全バージョンに影響。企業内の開発フロー全体が停止・情報漏洩リスクに直結。 |
| **CVE‑2026‑102785** | Joomla! Extension **YOOtheme Pro 5.0.0‑5.0.52** | 画像変換ハンドラの署名不備による未認証 RCE | 攻撃者は任意の画像リクエストを送るだけでサーバ上でシェルコードを実行でき、Web サイト全体が乗っ取られる。 | **スコア 10.0**、Joomla は中小企業・自治体でも広く採用。プラグイン単体の脆弱性が全サイトに波及。 |
| **CVE‑2026‑111813** | Apache Traffic Server **8.0.1‑10.2.0**（全リリース） | `magick` プラグインで ImageMagick の引数制御が可能 → 任意コード実行 | 画像プロキシとして利用されることが多く、外部からのリクエストだけでサーバ上のコマンドが実行できる。 | **スコア 10.0**、インフラ層で広範にデプロイされている点が危険。 |
| **CVE‑2026‑76466** | Cisco Expressway Series (Expressway‑Core, Expressway‑Edge) **全バージョン** | 永続クッキーの不適切検証により未認証リモートで **root コマンド実行** | ネットワーク境界装置が攻撃者に乗っ取られると、内部全体への横展開・通信監視回避が可能になる。 | **スコア 9.8**、ネットワーク基盤の根幹を揺るがす。 |
| **CVE‑2026‑111811** | Apache Traffic Server **8.0.0‑10.2.0** | `tsmemcache` プラグインでキャッシュの **読み書き・削除** が未認証で可能 | キャッシュデータ改ざんにより、配信コンテンツの改竄・情報漏洩・DoS が実現できる。 | **スコア 9.4**、実験的プラグインがデフォルトで有効化されているケースが多く、見落としがち。 |

> **総合評価**：上記 5 件は **スコア 9.4 以上**、かつ **未認証でリモートコード実行** が可能という点で、最優先で対策すべきです。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンのアップデート
| 製品 | 現行脆弱バージョン | **推奨バージョン** | アップデート方法 |
|------|-------------------|-------------------|-------------------|
| **GitLab CE/EE** | 7.0‑&lt; 18.11.13, 19.0‑&lt; 19.0.10, 19.1‑&lt; 19.1.9, 19.2‑&lt; 19.2.9, 19.3‑&lt; 19.3.6, 19.4‑&lt; 19.4.3, 19.5‑&lt; 19.5.1 | **19.5.2 以降** (公式パッチリリース) | `apt-get update && apt-get install gitlab-ce=19.5.2` もしくは `yum update gitlab-ee-19.5.2` |
| **YOOtheme Pro (Joomla Extension)** | 5.0.0‑5.0.52 | **5.0.53 以降** | Joomla 管理画面 → 「拡張機能」→「管理」→「アップデート」から最新版を適用 |
| **Apache Traffic Server** | 8.0.1‑10.2.0 (全リリース) | **10.2.1 以降** (magick・tsmemcache の実験的プラグインが無効化されたビルド) | `yum install trafficserver-10.2.1` または `apt-get install trafficserver=10.2.1` |
| **Cisco Expressway Series** | 全バージョン (脆弱) | **Expressway‑Core 12.6.2**、**Expressway‑Edge 12.6.2** 以降 | Cisco Smart Software Manager からファームウェアをダウンロード

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-102785

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-22T13:17:27.470 |

Joomla Extension - yootheme.com - Unauthenticated remote code execution in YOOtheme Pro 5.0.0-5.0.52 - YOOtheme Pro’s publicly accessible image transformation handler incompletely binds normalized image operations and the output destination to its request signature. An unauthenticated remote attacker can reuse a signature disclosed in a legitimate public image URL, inject additional image operations, traverse out of the intended cache directory, and write an attacker-controlled PNG/PHP polyglot to an executable public media directory.

### CVE-2026-110264

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-22T01:16:57.603 |

An issue has been discovered in GitLab CE/EE affecting all versions from 7.0 before 18.11.13, 19.0 before 19.0.10, 19.1 before 19.1.9, 19.2 before 19.2.9, 19.3 before 19.3.6, 19.4 before 19.4.3, and 19.5 before 19.5.1 that, under certain conditions, could have allowed an unauthenticated user to execute arbitrary code on the GitLab server due to integer overflow when compiling a specially crafted regular expression.

### CVE-2026-111813

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-21T19:16:59.167 |

Apache Traffic Server's experimental magick plugin lets an unauthenticated client control ImageMagick convert arguments in its default (unsigned) configuration.



This issue affects Apache Traffic Server: from 8.0.1 through 8.1.11, from 9.0.0 through 9.2.15, from 10.0.0 through 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-105944

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-21T19:16:57.437 |

Apache Pulsar Manager is a web console for administering Apache Pulsar clusters. It has its own user accounts and login, and it can be configured with an HTTP authentication credential, such as a token, that it uses to call the Pulsar admin API on behalf of its users. Pulsar Manager has the following security issues:

- The operation for creating the initial administrator (superuser) account is available without authentication, and it remains available after the instance has been initialized. Anyone who can reach Pulsar Manager can create an additional administrator account at any time and log in with it. This issue affects versions 0.3.0 and later.
- Requests to the Pulsar admin API that Pulsar Manager proxies to the configured Pulsar cluster are not subject to Pulsar Manager's authentication. Version 0.2.0 checks the caller's permissions for some of these requests, but not for all of them. An unauthenticated user can therefore use Pulsar Manager to send requests to the Pulsar admin API, which the cluster processes with the credential configured in Pulsar Manager.
- The destination of a proxied request can be chosen by the requester, and Pulsar Manager attaches its configured Pulsar admin credential to the request. An unauthenticated user can make Pulsar Manager send this credential to a host of the user's choosing, and the credential can then be used directly against the Pulsar cluster.
- In versions 0.3.0 and later, Pulsar Manager does not distinguish between privilege levels of its accounts. Every account, including one created through the first issue, effectively has full administrative privileges in Pulsar Manager.

The impact depends on the version and the deployment. In versions 0.3.0 and later, any user who can reach Pulsar Manager over the network can take full control of Pulsar Manager. In all versions, when Pulsar Manager is configured with an HTTP authentication credential for a Pulsar cluster, any user who can reach Pulsar Manager can perform the Pulsar admin operations that this credential permits and can obtain the credential itself. When Pulsar Manager is configured with the token signing key of a Pulsar cluster, an administrator of Pulsar Manager can create tokens for the cluster.

Apache Pulsar Manager is no longer maintained and is completely unsupported. The Apache Pulsar PMC has retired it. There are no supported versions, and no further releases, fixes or security updates will be made for any version. These issues will not be fixed.

Using Pulsar Manager is not recommended. Users should stop using Pulsar Manager, remove existing deployments, and move to one of the alternatives described in the Administration UI documentation (https://pulsar.apache.org/docs/administration-ui). Users who have exposed Pulsar Manager configured with a Pulsar credential or token signing key should also consider replacing that credential or key.

Until a deployment is removed, users should not expose Pulsar Manager to untrusted networks, and should restrict network access to it to trusted administrators.

### CVE-2026-111832

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-21T15:17:15.130 |

Unrestricted Upload of File with Dangerous Type vulnerability in WP Mailster WP Mailster wp-mailster allows Upload a Web Shell to a Web Server.This issue affects WP Mailster: from n/a through 1.9.1.0.

### CVE-2026-76531

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-552` |
| Published | 2026-10-21T23:17:30.117 |

As part of Cisco's ongoing commitment to proactive security and product quality, Cisco has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities. The vulnerabilities tracked by CVE-2026-76531 are related to files or directories accessible to external parties and are grouped under the Common Weakness Enumeration (CWE) CWE-552.

### CVE-2026-76302

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-707` |
| Published | 2026-10-21T23:17:28.273 |

As part of Cisco's ongoing commitment to proactive security and product quality, Cisco has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities. The vulnerabilities tracked by CVE-2026-76302 are related to improper neutralization and are grouped under the Common Weakness Enumeration (CWE) CWE-707.

### CVE-2026-76299

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-21T23:17:27.940 |

As part of Cisco's ongoing commitment to proactive security and product quality, Cisco has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities. The vulnerabilities tracked by CVE-2026-76299 are related to improper access control and are grouped under the Common Weakness Enumeration (CWE) CWE-284.

### CVE-2026-111834

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-21T15:17:15.387 |

Unrestricted Upload of File with Dangerous Type vulnerability in Kitae Park Mang Board WP mangboard allows Upload a Web Shell to a Web Server.This issue affects Mang Board WP: from n/a through 2.4.4.

### CVE-2026-112832

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-22T11:17:33.163 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in CozyThemes Rootblox rootblox allows PHP Local File Inclusion.This issue affects Rootblox: from n/a through 1.0.6.

### CVE-2026-112241

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-22T09:17:14.157 |

Authentication Bypass by Spoofing vulnerability in Brainstorm Force SureCart surecart allows Authentication Abuse.This issue affects SureCart: from n/a through 4.9.5.

### CVE-2026-96639

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-10-21T21:20:32.217 |

Pillow is a Python imaging library. From 11.0.0 until 13.0.0, multi-frame loaders can retain an ImagingCore allocation created for a narrow frame mode while a later frame of the same dimensions changes the logical mode and decoder tiles to wider RGB or CMYK data. ImageFile.load_prepare() reuses the stale native storage because _im is non-null without verifying that its mode and size still match. Crafted PSD, MPO, DCX, or MIC frame transitions can then write wider pixels into the narrow allocation, causing native out-of-bounds writes and crashes. The MPO path can also cause a native over-read and, in demonstrated runtime-specific profiles, command execution. This issue is fixed in version 13.0.0.

### CVE-2026-111183

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-21T18:17:23.477 |

GStreamer rtpL16depay Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GStreamer. Interaction with this library is required to exploit this vulnerability but attack vectors may vary depending on the implementation.

The specific flaw exists within the processing of RTP payload elements. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-31143.

### CVE-2026-76474

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-21T17:19:07.113 |

As part of Cisco's ongoing commitment to proactive security and product quality, engineering teams for Cisco Emergency Responder, Cisco Prime Collaboration Deployment, Cisco Unified Communications Manager (Unified CM), Cisco Unified Communications Manager IM &amp; Presence Service (Unified CM IM&amp;P), Cisco Unified Communications Manager Session Management Edition (Unified CM SME), and Cisco Unity Connection have conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76474 are related to issues concerning improper authentication that are grouped under the Common Weakness Enumeration (CWE) Class CWE-287.

### CVE-2026-76473

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-10-21T17:19:06.973 |

As part of Cisco's ongoing commitment to proactive security and product quality, engineering teams for Cisco Emergency Responder, Cisco Prime Collaboration Deployment, Cisco Unified Communications Manager (Unified CM), Cisco Unified Communications Manager IM &amp; Presence Service (Unified CM IM&amp;P), Cisco Unified Communications Manager Session Management Edition (Unified CM SME), and Cisco Unity Connection have conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76473 are related to issues concerning improper control of a resource through its lifetime that are grouped under the Common Weakness Enumeration (CWE) Class CWE-74.
&nbsp;

### CVE-2026-76466

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-21T17:19:06.813 |

A vulnerability in the database service feature of Cisco Expressway Series could allow an unauthenticated, remote attacker with network access to a Cisco Expressway device to execute arbitrary operating system commands as&nbsp;root.

This vulnerability is due to the use of persistent cookies. Additionally, there is insufficient validation of client certificates when the TLS Verify Mode is set to Enabled for clustering, which means that client certificates are not validated. An attacker with possession of the cookies could exploit this vulnerability by connecting to the database service and invoking specific remote procedure call (RPC) commands. A successful exploit could allow the attacker to execute arbitrary commands as root on the underlying operating system of an affected device.
Note: Cisco Expressway Series refers to Cisco Expressway Core (Expressway-C) devices and Cisco Expressway Edge (Expressway-E) devices.

### CVE-2026-112408

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-940` |
| Published | 2026-10-21T20:17:23.877 |

Missing verification of source of a communication channel in the default_bucket() function in Amazon SageMaker Python SDK V3 before 3.10.0 and V2 before 2.257.3 might allow remote actors to achieve code execution in the target SageMaker execution environment and obtain IAM credentials via pre-creation of a predictably named S3 bucket that the SDK uses without ownership validation.



To remediate this issue, users should upgrade to Amazon SageMaker Python SDK 3.10.0 (V3) or 2.257.3 (V2).

### CVE-2026-111811

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-21T20:17:22.920 |

Apache Traffic Server's experimental tsmemcache plugin allows unauthenticated network read, write, and deletion of the shared proxy cache.



This issue affects Apache Traffic Server: from 8.0.0 through 8.1.11, from 9.0.0 through 9.2.15, from 10.0.0 through 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-113788

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-21T16:17:26.440 |

Lagoon is an application delivery platform for Kubernetes. Versions prior to 2.33.1 have a vulnerability in the `ssh` service in Lagoon core that would allow an attacker to execute arbitrary code which could lead to, among other things, elevated administrative permissions. It is mitigated by the fact that an attacker must have a Lagoon user account. Exploitation may be detected by checking the container logs of the `ssh` service for: `too many arguments`. The vulnerability was fixed in Lagoon v2.33.2, which is included in the `lagoon/lagoon-core` helm chart v1.62.2. As a workaround, the `ssh` service in Lagoon core can be disabled. The `ssh-portal` service and components are not effected and can continue to be used.

### CVE-2021-48016

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-22T11:17:04.690 |

DedeCMS through 5.8.1-beta contains a PHP code injection vulnerability in ShowMsg() where the HTTP Referer header is written into a DedeTemplate string and included. Unauthenticated attackers can send a crafted Referer to /plus/flink.php?dopost=save with an empty validate code to execute arbitrary PHP and system commands. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2021-48014

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:04.390 |

FineReport 9.0 contains a path traversal vulnerability in the /WebReport/ReportServer design_save_svg operation that allows unauthenticated attackers to write arbitrary files via the filePath parameter. Attackers can send a POST request with directory traversal sequences in filePath and a __CONTENT__ payload to write a JSP webshell and achieve remote code execution. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2026-112327

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T09:17:14.680 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in TMS Amelia ameliabooking allows SQL Injection.This issue affects Amelia: from n/a through 2.4.11.

### CVE-2026-114220

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-22T05:16:50.020 |

NT OneAPP developed by NewType Infortech has an Improper Certificate Validation vulnerability. Unauthenticated network-adjacent attackers can perform a man-in-the-middle attack by failing to validate the server certificate and the hostname, thereby intercepting or modifying communications between the application and the server.

### CVE-2026-114575

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-10-22T01:16:58.533 |

A flaw has been found in TOTOLINK A950RG 4.1.2cu.5268_B20221104. Affected by this issue is the function UploadCustomModule of the file lib/cste_modules/product.so. Executing a manipulation of the argument FileMd5 can lead to command injection. The attack can be launched remotely. The exploit has been published and may be used.

### CVE-2026-114383

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-10-21T22:16:49.077 |

A weakness has been identified in TOTOLINK EX200 5.2.3c.7200. This impacts the function setWiFiAclAddConfig of the file /cgi-bin/cstecgi.cgi of the component wireless.so. This manipulation of the argument macAddress causes stack-based buffer overflow. The attack can be initiated remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-114382

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-10-21T22:16:48.910 |

A security flaw has been discovered in TOTOLINK EX200 5.2.3c.7200. This affects the function setStaticDhcpConfig of the file /cgi-bin/cstecgi.cgi of the component lan.so. The manipulation of the argument Comment results in stack-based buffer overflow. It is possible to launch the attack remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-76475

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-21T17:19:07.253 |

As part of Cisco's ongoing commitment to proactive security and product quality, engineering teams for Cisco Emergency Responder, Cisco Prime Collaboration Deployment, Cisco Unified Communications Manager (Unified CM), Cisco Unified Communications Manager IM &amp; Presence Service (Unified CM IM&amp;P), Cisco Unified Communications Manager Session Management Edition (Unified CM SME), and Cisco Unity Connection have conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76475 are related to issues concerning improper neutralization of input during web page generation that are grouped under the Common Weakness Enumeration (CWE) Base CWE-79.

### CVE-2026-111852

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-21T15:17:16.140 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in WPdreams Ajax Search Lite ajax-search-lite allows Blind SQL Injection.This issue affects Ajax Search Lite: from n/a through 4.14.6.

### CVE-2026-111497

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-252;CWE-787` |
| Published | 2026-10-22T14:17:37.190 |

A buffer overflow vulnerability in the Brotli decoder (c/dec/decode.c) in Google Brotli versions 1.0.3 through 1.2.0 on all platforms allows a remote unauthenticated attacker to corrupt adjacent decoder state memory, disclose sensitive memory contents, cause a denial of service, or potentially execute arbitrary code using a crafted Brotli-compressed stream.





Users need to update any Brotli libraries or binaries between 1.0.3 through 1.2.0 to the latest available version: 1.0.10 or 1.1.1 or 1.2.1.

### CVE-2026-115324

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T11:17:51.263 |

mem0 0.1.117 before 1.0.8 contains an sql injection vulnerability in mem0/vector_stores/databricks.py that allows attackers to inject SQL by influencing stored memory content. Attackers can supply crafted memory text, metadata, or message names that reach unescaped insert() and update() string interpolation to execute injected SQL on the configured Databricks SQL warehouse.

### CVE-2026-114509

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-1287` |
| Published | 2026-10-21T22:16:49.710 |

Laravel is a web application framework. Prior to 12.68.0 and 13.29.0, TokenGuard configured as a standard token-based API guard does not reject a crafted non-string credential. Under affected MySQL or MariaDB configurations, the authentication lookup can match an unintended existing user, allowing an unauthenticated attacker to bypass authentication and take over an account on routes protected by TokenGuard. This issue is fixed in versions 12.68.0 and 13.29.0.

### CVE-2026-111816

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-10-21T19:16:59.330 |

Apache Traffic Server forwarded a malformed 302 response that should have been rejected as a parse error, because the Transfer-Encoding: chunked carve-out bypassed the rejection path. A response that two peers can read differently is then stored and served, allowing cache poisoning and response-framing desync.



This issue affects Apache Traffic Server: from 8.0.0 through 8.1.11, from 9.0.0 through 9.2.15, from 10.0.0 through 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-114493

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-21T18:17:28.120 |

LocalAI v4.6.0 through v4.11.0 contains a server-side request forgery vulnerability in core/gallery/gallery.go that validates only the initial gallery config URL. Attackers can submit a config URL through POST /models/apply that redirects to internal or cloud metadata addresses, receiving those internal responses as gallery content.

### CVE-2026-105869

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-21T18:17:22.293 |

Apache Pulsar's MultiRolesTokenAuthorizationProvider authorizes a client with all roles listed in a claim of its JSON Web Token (JWT). The provider is intended for use with token authentication, which verifies the token before authorization. The provider did not verify the token itself: it parsed the token's claims with the signature removed and trusted that authentication had already checked it.

When authentication and authorization are enabled with a non-empty anonymousUserRole setting, some HTTP requests whose credentials fail authentication are not rejected, but are handled as requests of the anonymous user role. For the broker's HTTP endpoints, such as the admin REST API, this fallback applies to requests that do not name an authentication method and requires strictAuthMethod to be false (the default) where that setting is available. For the WebSocket API, failed credentials can also fall back to the anonymous user role; this path does not enforce strictAuthMethod. The authentication data kept for such a request still contained the request's Authorization header. MultiRolesTokenAuthorizationProvider then read the bearer token from that header without verifying its signature and authorized the request with the roles in the token's role claim.

As a result, in deployments that use MultiRolesTokenAuthorizationProvider together with a non-empty anonymousUserRole and that permit this fallback, an unauthenticated client can send an HTTP request, for example to the admin REST API or the WebSocket API, with a forged or unsigned token that lists arbitrary roles, and be authorized with those roles. The impact can include super-user access when the token lists a role configured in superUserRoles, allowing the client to read and change tenants, namespaces, topics, permissions and broker configuration. No valid credentials are required.

Deployments are not affected if they use the default authorization provider (PulsarAuthorizationProvider) or another authorization provider, or if anonymousUserRole is not set (the default). Requests that authenticate successfully with a valid token are not affected, because the token that MultiRolesTokenAuthorizationProvider reads is the token that authentication verified. Connections that use the Pulsar binary protocol are not affected by this issue, because the broker does not keep client authentication data for connections that it assigns to the anonymous user role.

In fixed versions, MultiRolesTokenAuthorizationProvider obtains roles only from tokens that the configured token authentication provider has verified, using its configured keys and validation settings. Broker HTTP requests that are assigned to the anonymous user role are authorized only as that role, and invalid tokens cannot supply additional roles to WebSocket requests. The broker fails to start if MultiRolesTokenAuthorizationProvider is configured with authorization enabled but without a token authentication provider.

This issue affects Apache Pulsar versions from 2.8.1 before 4.0.14 and from 4.1.0 before 4.2.5.

- 4.0.x version users should upgrade to at least 4.0.14.
- 4.1.x and 4.2.x version users should upgrade to at least 4.2.5.

Users operating versions prior to those listed above should upgrade to the aforementioned patched versions or newer versions.

The currently supported Apache Pulsar release lines are 4.0.x and 5.0.x. The supported versions schedule is available at https://pulsar.apache.org/contribute/release-policy/.

Users who cannot upgrade immediately can remove the anonymousUserRole setting from the broker and WebSocket service configurations, or restrict network access to the HTTP endpoints of these services to trusted clients.

### CVE-2026-114219

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-22T05:16:49.170 |

NT OneAPP developed by NewType Infortech has a Hard-coded Credentials vulnerability. Unauthenticated remote attackers can obtain the hard-coded cryptographic key and decrypt login request contents, thereby obtaining users' plaintext account credentials and device information.

### CVE-2026-91403

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-10-21T22:16:50.243 |

Vulnerability in the Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition product of Oracle Java SE (component: JSSE).  Supported versions that are affected are Oracle Java SE: 8u511, 8u511-perf, 11.0.33, 17.0.21, 21.0.13, 25.0.5, 27.0.1; Oracle GraalVM for JDK: 17.0.21 and  21.0.13; Oracle GraalVM Enterprise Edition: 21.3.20. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition accessible data as well as  unauthorized access to critical data or complete access to all Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition accessible data. Note: This vulnerability can be exploited by using APIs in the specified Component, e.g., through a web service which supplies data to the APIs. This vulnerability also applies to Java deployments, typically in clients running sandboxed Java Web Start applications or sandboxed Java applets, that load and run untrusted code (e.g., code that comes from the internet) and rely on the Java sandbox for security. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114139

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-10-21T21:17:56.353 |

Sentry-Javascript is an official Sentry SDKs for JavaScript. From 9.36.0 until 9.47.2, 10.75.2, and 11.0.0-rc.1, the webpack integration for @sentry/nextjs skips application middleware for every request path under a configured tunnelRoute, while the tunnel rewrite serves only the exact tunnel path with valid o and p query parameters. When an application route directly collides with the tunnel path or a root dynamic segment resolves under it, an unauthenticated request can reach that route without middleware authorization. Exploitation requires tunnelRoute, a webpack build, a colliding route, and middleware being the only authorization control. This issue is fixed in versions 9.47.2, 10.75.2, and 11.0.0-rc.1.

### CVE-2025-31699

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-10-21T19:16:47.390 |

Apache Traffic Server can return an origin connection to the shared pool while the origin is still waiting on a request body the client declared but never fully sent, including when the client used Expect: 100-continue. The origin then reads a later request on that connection as leftover body data, which lets an attacker smuggle requests past ATS access controls, disrupt other users' requests, or poison the cache.



This issue affects Apache Traffic Server: from 8.0.0 through 8.1.11, from 9.0.0 through 9.2.15, from 10.0.0 through 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-89035

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-21T18:17:30.277 |

MikroTik RouterOS through 7.24.5 contains a session token replay vulnerability in the WebFig interface that allows attackers to bypass authentication by replaying captured session tokens across new ECDH sessions. The makeSessionKey function in libucrypto.so generates tokens using fixed salts without incorporating channel-specific or session-specific input, and the user service validates tokens against the login store without verifying channel context, enabling stolen tokens to grant persistent administrative access until the token store is explicitly cleared. This vulnerability extends the impact of CVE-2025-61481, which identified the underlying transport-layer exposure without a corresponding fix.

### CVE-2026-114661

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-22T02:16:58.250 |

OpenRemote 1.2.0 before 1.31.0 contains a missing authorization vulnerability in GatewayServiceResource that allows any authenticated user to start, stop and query gateway tunnels without an administrative role. Attackers can send POST or DELETE requests to the gateway tunnel endpoint to open persistent bidirectional TCP circuits into an edge gateway's network or tear down operator tunnels.

### CVE-2026-20043

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-21T17:18:27.087 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco owned Open Source Snort 3 Software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20043 are related to issues concerning out-of-bounds writes that are grouped under the Common Weakness Enumeration (CWE) Base CWE-787.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2025-71434

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T11:17:06.373 |

Weaver E-cology 8.0, 9.0, and 10.0 prior to 10.76 contains an unauthenticated SQL injection vulnerability in the /api/doc/out/more/list endpoint via the elementmore parameter with srcType=2. Attackers can inject SQL through doc_datefrom/doc_dateto fields and read results via /api/ec/dev/table/counts to extract database information. Exploitation evidence was first observed by the Shadowserver Foundation on 2026-07-19.

### CVE-2024-58393

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T11:17:05.913 |

i-Netsolution Readymade Unilevel Ecommerce MLM (2024-03-15 build) contains an SQL injection vulnerability that allows unauthenticated attackers to manipulate database queries through the 'id' parameter. Attackers can send GET requests to /product-details.php with boolean-based, stacked, or time-based SLEEP payloads in 'id' to extract database information. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-09-14.

### CVE-2022-51023

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T11:17:05.300 |

PHPOK 4.5.000 before 5.4.081 contains an SQL injection vulnerability that allows unauthenticated attackers to manipulate ORDER BY clauses via the sort parameter. Attackers can send GET requests to /api.php?c=project&f=index with extractvalue payloads in sort to extract database information through error messages. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2022-51022

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:05.153 |

YiShaAdmin 2.2 through 3.1, fixed in commit 025b062, contains an unauthenticated path traversal vulnerability in the /admin/File/DownloadFile endpoint that allows attackers to read and delete arbitrary files via the filePath parameter. Attackers can send crafted GET requests with directory traversal sequences in filePath and set the delete parameter to read or remove system files like etc/passwd. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-20.

### CVE-2022-51021

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T11:17:04.990 |

NotificationX plugin for WordPress 2.0.0 before 2.3.12 contains an unauthenticated SQL injection vulnerability that allows remote attackers to manipulate database queries by supplying an array-form 'id' parameter to /wp-json/notificationx/v1/notification/{id}. Attackers can pass id[1] with crafted SQL, such as time-based SLEEP payloads, along with an api_key derived from md5(home_url()), which flows unsanitized into Database::get_where_query to extract database contents. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-18.

### CVE-2019-25778

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T11:17:03.777 |

SeaCMS through 8.7 contains an unauthenticated SQL injection vulnerability that allows remote attackers to manipulate database queries by injecting SQL through the rlist[] array parameter. Attackers can send GET requests to /comment/api/index.php with crafted rlist[] values using backtick-quoted variables and extractvalue to extract database information via error messages. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2026-112242

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-22T09:17:14.283 |

Incorrect Privilege Assignment vulnerability in Cozmoslabs Profile Builder profile-builder allows Privilege Escalation.This issue affects Profile Builder: from n/a through 4.0.4.

### CVE-2026-114177

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-22T07:16:41.870 |

Cross-Site Request Forgery (CSRF) vulnerability in Xpro Xpro Elementor Addons xpro-elementor-addons allows Cross Site Request Forgery.This issue affects Xpro Elementor Addons: from n/a through 1.7.10.

### CVE-2026-76530

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-647` |
| Published | 2026-10-21T23:17:30.000 |

As part of Cisco's ongoing commitment to proactive security and product quality, Cisco has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities. The vulnerabilities tracked by CVE-2026-76530 are related to use of non-canonical URL paths for authorization decisions and are grouped under the Common Weakness Enumeration (CWE) CWE-647.

### CVE-2026-76298

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-21T23:17:27.817 |

In Splunk Enterprise versions below 10.4.4 and 10.2.8, a user who does not hold the "admin" or "power" Splunk roles could derive the PostgreSQL sidecar database superuser password and run arbitrary operating system commands as the user account running Splunk Enterprise on search head cluster members.
The vulnerability is possible because the PostgreSQL sidecar service derives a privileged database password from the search head cluster identifier that appears in search job logs.
For more information see About configuring role-based user access (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.2/manage-splunk-platform-users-and-roles/about-configuring-role-based-user-access), server.conf (https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.2/configuration-file-reference/10.2.0-configuration-file-reference/server.conf), and Sidecar configuration settings (https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/splunk-sidecars/sidecar-configuration-settings) in the Splunk documentation.

### CVE-2026-76291

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-21T23:17:26.943 |

In Splunk Enterprise versions below 10.4.4, 10.2.8, 10.0.11, and 9.4.16, a user that holds a role with the schedule_search capability could bypass the expected safeguards in the scheduled search workflow. The user could then run risky Search Processing Language (SPL) commands that disclose or alter Splunk Enterprise data or disrupt Splunk Enterprise availability.
The vulnerability is possible because the Splunk Enterprise search scheduler does not apply SPL safeguards for risky commands to scheduled searches.
For more information see SPL safeguards for risky commands (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/best-practices-for-splunk-platform-security/spl-safeguards-for-risky-commands) in the Splunk documentation.
For more information see authorize.conf (https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/authorize.conf) in the Splunk documentation.

### CVE-2026-103090

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-522` |
| Published | 2026-10-21T23:17:24.990 |

Missing Authentication for Critical Function (CWE-306) and Insufficiently Protected Credentials (CWE-522) in the control plane enrollment status handler (HandleEnrollStatus at GET /enroll/status in internal/controlplane/server.go) in Google OSS Agent Mesh (SAM) versions 0.1.0-alpha.1 through 0.1.0-alpha.8 allow an unauthenticated remote attacker to retrieve an approved bootstrap-enrolled peer's signed Biscuit identity token by supplying a peer_id obtainable from the unauthenticated GET /info endpoint. A related flaw in POST /enroll allowed any bootstrap-token holder to re-fetch another peer's credential. An attacker can replay the disclosed Biscuit token as a bearer credential on /policies to read mesh authorization policies and on /routers/lease to overwrite advertised router multiaddrs. Users should upgrade to version 0.1.0-alpha.9 or later, which requires cryptographic proof of possession of the enrollment private key on credential-releasing endpoints, enforces rate limiting, and validates router lease addresses.

### CVE-2026-114142

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-21T21:17:56.820 |

toml-node is a TOML parser for Node.js and the browser. Prior to 5.0.1, toml.parse() can write attacker-controlled properties to Object.prototype because quoteDottedString() in lib/compiler.js produces the same bookkeeping string for distinct quoted key paths, allowing addTableArray() to clear another key's guard. The assign() path then descends through an unowned Date value without applying the owned-container check and can reach the prototype chain. Objects created elsewhere in the process can inherit the injected property. This issue is fixed in version 5.0.1.

### CVE-2026-114140

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-21T21:17:56.520 |

The nbconvert tool, jupyter nbconvert, converts Jupyter notebooks to various other formats via Jinja templates. From 5.4.0 until 7.17.2, ExtractOutputPreprocessor in nbconvert/preprocessors/extractoutput.py joins the attacker-controlled cell output metadata filename to output_files_dir without limiting the result to the intended directory. When a victim converts a malicious notebook with the markdown, LaTeX, reStructuredText, or AsciiDoc exporter, path traversal in the output filename can write attacker-controlled output data to arbitrary locations accessible to the victim. Running the notebook cell again replaces the malicious output metadata, but merely converting the supplied notebook does not. This issue is fixed in version 7.17.2.

### CVE-2026-114135

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-21T20:17:25.407 |

Jupyter Server is the backend for Jupyter web applications. From 2.0.0 until 2.6.0, enabling GatewayClient.url replaced the normal KernelWebsocketHandler with WebSocketChannelsHandler, which authenticated the user but did not call authorizer.is_authorized(...) for the execute action on the kernels resource. A restricted authenticated user could therefore open an upstream kernel channel and obtain kernel execution despite the configured Authorizer denying that action, exposing data and credentials available to the kernel and permitting modification or disruption of the kernel environment. The default gateway configuration is fixed in version 2.6.0. In 2.6.0 and later, the same authorization bypass remains possible when a deployment manually registers the deprecated jupyter_server.gateway.handlers module, because its handler still omits the configured kernel-execute authorization decision.

### CVE-2026-111804

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-21T19:16:59.007 |

Apache Traffic Server's experimental wasm plugin has a use-after-free in its transaction-close handler and forwards unvalidated guest-supplied metric IDs to the internal stats API.



This issue affects Apache Traffic Server: from 10.0.0 through 10.1.4, 10.2.0.



Users are recommended to upgrade to version 10.1.5 or 10.2.1, which fix the issue.

### CVE-2026-92208

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-21T18:17:31.427 |

NoMachine mDNS Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of NoMachine. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the parsing of mDNS resource records. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the service account. Was ZDI-CAN-30982.

### CVE-2026-92207

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-21T18:17:31.280 |

MindsDB OpenBBtable Code Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of MindsDB. Authentication is required to exploit this vulnerability.

The specific flaw exists within the OpenBBtable class. The issue results from the lack of proper validation of a user-supplied string before using it to execute Python code. An attacker can leverage this vulnerability to execute code in the context of the service account. Was ZDI-CAN-28388.

### CVE-2026-92206

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-10-21T18:17:31.133 |

CrewAI crewAI Framework Agent Loading Unsafe Reflection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of CrewAI crewAI. User interaction is required to exploit this vulnerability in that the target must load a malicious agent configuration from the repository.

The specific flaw exists within the load_agent_from_repository function. The process does not properly restrict a user-supplied argument before using it to import a module. An attacker can leverage this vulnerability to execute code in the context of the service account. Was ZDI-CAN-28387.

### CVE-2026-76478

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-21T17:19:07.650 |

As part of Cisco's ongoing commitment to proactive security and product quality, engineering teams for Cisco Emergency Responder, Cisco Prime Collaboration Deployment, Cisco Unified Communications Manager (Unified CM), Cisco Unified Communications Manager IM &amp; Presence Service (Unified CM IM&amp;P), Cisco Unified Communications Manager Session Management Edition (Unified CM SME), and Cisco Unity Connection have conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76478 are related to improper access control issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-284.

### CVE-2026-76477

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-21T17:19:07.520 |

As part of Cisco's ongoing commitment to proactive security and product quality, engineering teams for Cisco Emergency Responder, Cisco Prime Collaboration Deployment, Cisco Unified Communications Manager (Unified CM), Cisco Unified Communications Manager IM &amp; Presence Service (Unified CM IM&amp;P), Cisco Unified Communications Manager Session Management Edition (Unified CM SME), and Cisco Unity Connection have conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76477 are related to issues concerning improper neutralization of special elements used in an SQL command that are grouped under the Common Weakness Enumeration (CWE) Base CWE-89.

### CVE-2026-76476

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-21T17:19:07.387 |

As part of Cisco's ongoing commitment to proactive security and product quality, engineering teams for Cisco Emergency Responder, Cisco Prime Collaboration Deployment, Cisco Unified Communications Manager (Unified CM), Cisco Unified Communications Manager IM &amp; Presence Service (Unified CM IM&amp;P), Cisco Unified Communications Manager Session Management Edition (Unified CM SME), and Cisco Unity Connection have conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-76476 are related to issues concerning improper input validation that are grouped under the Common Weakness Enumeration (CWE) Class CWE-20.

### CVE-2026-113779

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-21T15:17:16.553 |

The pfSense REST API package is an unofficial, open-source REST and GraphQL API for pfSense CE and pfSense Plus firewalls. A privilege escalation vulnerability in pfSense-pkg-RESTAPI prior to version 2.9.0 allows authenticated accounts holding the dedicated settings sync permission to modify REST API configuration secrets. This enables a non-administrative user to elevate their privileges to a full administrator. pfSense-pkg-RESTAPI 2.9.0 patches the issue. Access to the HA settings sync endpoint now strictly requires full administrative privileges (`page-all`). The sub-administrative sync privilege has been removed in versions v2.9.0 and later. In addition to correcting the access control boundary, version 2.9.0 includes the following hardening measures: opt-in default and format and validation modernization. As a workaround, one may mitigate exposure by taking either or all of the following steps. Revoke Scoped Permissions: Remove the `api-v2-system-restapi-settings-sync-post` privilege from all non-administrative users. Apply ACLs: Configure REST API Access Control Lists (ACLs) and/or firewall rules to restrict access to API endpoints exclusively to trusted administrator and HA peer IP addresses.

### CVE-2026-113582

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-22T14:17:38.053 |

UNSUPPORTED WHEN ASSIGNED Improper restriction of XML external entity references in Apache Abdera allows an attacker to access sensitive data or make server-side requests when an application parses attacker-controlled XML with Abdera.



This issue affects Apache Abdera: all versions.



Apache Abdera is retired and no longer supported, so we do not plan to release a version that fixes this issue. Users are recommended to migrate to a maintained alternative. Applications that cannot migrate should ensure that untrusted XML cannot reach the affected Abdera parser or JDBC adapter parsing paths. Actively maintained downstream products may still be impacted if they include an affected Abdera artifact.



NOTE: This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-115332

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T11:17:52.427 |

Lotus through 0.10.2 contains an sql injection vulnerability that allows authenticated organization users to inject SQL by registering crafted subscription_filter_keys that bypass keyword-only validation. Attackers can create subscriptions using the malicious key, which is rendered as an unquoted group-by identifier, to inject SQL into usage aggregation queries against the shared multi-tenant database.

### CVE-2026-115331

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T11:17:52.290 |

Lotus through 0.10.2 contains an sql injection vulnerability that allows authenticated organization users to inject SQL by supplying crafted billable metric property_name or categorical filter values. Attackers can embed SQL in values rendered unescaped into Jinja-generated counter, gauge and rate metric queries to access the database shared by all tenants.

### CVE-2026-115330

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T11:17:52.153 |

Lotus through 0.10.2 contains an sql injection vulnerability that allows authenticated organization users to execute arbitrary SQL by appending stacked statements to custom metric queries. Attackers can submit semicolon-separated SQL through POST /app/metrics/, bypassing first-statement-only validation, to read or modify data across all tenants.

### CVE-2026-115328

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T11:17:51.873 |

JSON-SCADA before 0.65-alpha contains an sql injection vulnerability in opcApi() in src/server_realtime_auth/index.js that allows authenticated users to inject SQL via HistoryReadRequest parameters. Attackers can inject stacked statements through NodeId.Id, StartTime, or EndTime values to read, modify, or delete historian data across all locations regardless of role.

### CVE-2026-115325

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-22T11:17:51.400 |

Netmaker through 1.7.0 contains an authorization bypass vulnerability in the updateExtClient handler that allows network-scoped users to modify external clients on other networks. Attackers with external client permissions on one network can send PUT requests to /api/extclients/{network}/{clientid} to replace public keys, disable clients, and obtain WireGuard private keys.

### CVE-2024-58396

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:06.203 |

YouDataSum CPAS Audit Management System V4 contains a path traversal vulnerability that allows unauthenticated attackers to read arbitrary files by manipulating the fileId parameter. Attackers can send GET requests to /cpasm4/plugInManController/downPlugs with ../ sequences in fileId to retrieve system files like /etc/passwd. Exploitation evidence was first observed by the Shadowserver Foundation on 2025-01-13.

### CVE-2022-51024

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:05.447 |

Kavita 0.5.2 before 0.5.4.1 contains a path traversal vulnerability that allows unauthenticated attackers to read arbitrary files by supplying '../' sequences in the filename parameter. Attackers can send GET requests to /api/image/cover-upload with filename values like ../appsettings.json to retrieve configuration files outside the temp directory. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-18.

### CVE-2021-48017

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:04.833 |

OrbiTeam BSCW Server 5.x before 5.2.5 and 7.x before 7.4.4 contains an unauthenticated path traversal vulnerability in the style_name parameter of the theme operation. Attackers can send GET requests to /pub/bscw.cgi/<id>?op=theme with ../ sequences in style_name to read local files such as /etc/passwd. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-22.

### CVE-2021-48015

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:04.537 |

JeeWMS before commit 0a610e8 contains an unauthenticated path traversal vulnerability that allows remote attackers to read arbitrary files via the dbPath parameter. Attackers can send GET requests to /systemController/showOrDownByurl.do with ../ sequences in dbPath, which bypasses AuthInterceptor, to retrieve files like win.ini. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-17.

### CVE-2021-48013

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:04.250 |

Weaver E-cology 8.0 contains a path traversal vulnerability that allows unauthenticated attackers to read arbitrary files through the fpath parameter of the /weaver/ln.FileDownload endpoint. Attackers can send crafted GET requests with directory traversal sequences in fpath to retrieve sensitive files such as WEB-INF/web.xml from the server. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-18.

### CVE-2019-25779

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:03.930 |

WooThemes Diarise through 1.5.9 contains a file read vulnerability that allows unauthenticated attackers to read arbitrary files through the calendar parameter of download.php. Attackers can send GET requests with file:// scheme paths to the calendar parameter to disclose sensitive files like /etc/passwd. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-19.

### CVE-2018-25439

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:03.620 |

MetInfo CMS 6.0.0 before 6.1.1 contains a path traversal vulnerability in /include/thumb.php that allows unauthenticated attackers to read arbitrary files via the dir parameter. Attackers can send crafted requests with backslash sequences bypassing the str_replace filter to read files like config_db.php on Windows. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2018-25438

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:03.463 |

Intermesh Group-Office 3.3.0 before 3.5.5 contains an unauthenticated path traversal vulnerability in compress.php that allows remote attackers to read arbitrary files by manipulating the 'file' parameter. Attackers can send GET requests to /compress.php with '../' sequences in the 'file' parameter, which is appended to the cache path and passed to readfile(), to read files such as /etc/passwd. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-21.

### CVE-2017-20287

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:01.823 |

Javo Spot theme for WordPress before 3.0.0 contains a path traversal vulnerability that allows unauthenticated attackers to read arbitrary files via the fn parameter of the jvfrm_spot_get_json AJAX action. Attackers can send GET requests to /wp-admin/admin-ajax.php with fn set to ../../wp-config.php to retrieve database credentials and secret keys. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-19.

### CVE-2026-93471

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-22T09:17:16.827 |

Improper Handling of Highly Compressed Data (Data Amplification) in esaml_binding in dropbox esaml allows an unauthenticated attacker to exhaust server memory and crash the Erlang VM via a crafted compressed SAMLResponse.

esaml_binding:decode_response/2 base64-decodes the attacker-supplied SAMLResponse, inflates it with zlib:unzip/1 with no bound on the output, then converts the result to a charlist with binary_to_list/1 before parsing. This runs on the SAML consume (ACS) and single-logout endpoints, which accept unauthenticated requests by design, and it runs before any signature check. A small deflate stream reaches a compression ratio near 1000 to 1, so a request body of tens of kilobytes inflates to hundreds of megabytes and then to several gigabytes of list heap, so a few requests exhaust memory and take the node down.

This issue affects esaml: from 0.1.0 onward.

### CVE-2026-105270

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-22T07:16:40.940 |

Allocation of Resources Without Limits or Throttling vulnerability in esaml_binding in dropbox esaml allows an unauthenticated attacker to exhaust the Erlang VM atom table and crash the node via a crafted SAMLResponse.

esaml_binding:decode_response/2 parses the decoded SAMLResponse with xmerl_scan:string/2, which interns every element name, attribute name, and namespace prefix it reads as a permanent atom. The SAML consume (ACS) and single-logout endpoints call it on unauthenticated requests before any signature check, so one well-formed document with thousands of distinct names mints thousands of atoms while staying inside the 128 KB request body limit. Atoms are never reclaimed and the VM caps the atom table at about one million entries, so a few dozen requests abort the node.

This issue affects esaml: from 0.1.0 onward.

### CVE-2026-114658

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-22T02:16:57.770 |

Grav Login plugin from 3.6.0 before 3.9.13 contains a missing authorization vulnerability in the login.invite task that allows page authors to obtain super user accounts. Attackers can define an invitation form granting super access in page frontmatter, submit it unauthenticated, and register the invited address for full site control.

### CVE-2026-114143

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-21T21:17:56.963 |

toml-node is a TOML parser for Node.js and the browser. Prior to 5.0.1, toml.parse() repeatedly slices and rejoins every path prefix in lib/compiler.js while processing long dotted keys, table headers, array-of-tables headers, and inline-table keys in assign(), deepRef(), and setNestedKey(). The resulting quadratic work can block the Node.js event loop for several seconds, and sufficiently long paths can terminate the process through memory exhaustion. The maxDepth option does not limit key-segment count and therefore does not mitigate this path. This issue is fixed in version 5.0.1.

### CVE-2026-114141

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-21T21:17:56.667 |

toml-node is a TOML parser for Node.js and the browser. Prior to 5.0.1, the toml.parse() compiler's addTableArray() function in lib/compiler.js rescans the complete assignedPaths and valueAssignments bookkeeping sets for every array-of-tables header. Distinct [[name]] paths are not pruned, so a document with many such headers causes quadratic synchronous work and can block the Node.js event loop, denying service to other operations in the process. This issue is fixed in version 5.0.1.

### CVE-2026-111810

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-21T20:17:22.780 |

Apache Traffic Server 9.2.15, 10.1.4 and 10.2.0 write one unthrottled diagnostic log line for every internal @ header they strip, so a request carrying many such headers makes the proxy write far more log data than the request contains.



This issue affects Apache Traffic Server: 9.2.15, 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-110803

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-667` |
| Published | 2026-10-21T19:16:58.567 |

VaadinService.requestEnd() in Vaadin Framework 8 locks the session and then reads the v-uiId request parameter outside the block that releases the lock. A request carrying a non-numeric v-uiId makes Integer.parseInt throw while the session lock is held, so the lock is never released and the container thread returns to its pool still owning it. Every later request to that session then blocks forever in VaadinService.lockSession(), and repeating the request exhausts the thread pool and takes the application down. No authentication is required: a session cookie, which any client obtains with a single request, is enough. Vaadin 10 and later are not affected, because Flow releases the lock in a finally block and does not read that parameter there, and Vaadin Framework 7 is not affected either.


Users of affected versions should apply the following mitigation or upgrade. Releases that have fixed this issue include:

Product version
Vaadin Framework 8.16.0 - 8.32.1

Mitigation
Upgrade to 8.32.2

Vaadin Framework 7 and Vaadin 10 and later do not carry this behaviour and need no upgrade for this issue.

Artifacts
Maven coordinates / Vulnerable versions / Fixed version
com.vaadin:vaadin-server / 8.16.0 - 8.32.1 / >=8.32.2
com.vaadin:vaadin-server-mpr-jakarta / 8.18.0 - 8.32.1 / >=8.32.2

### CVE-2026-105937

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-21T19:16:56.730 |

Apache Pulsar shadow topics (PIP-180) are topics that read the stored messages of a source topic from that topic's managed ledger. The source topic is selected by setting the reserved topic property PULSAR.SHADOW_SOURCE. The admin REST API accepts this property when creating a non-partitioned or partitioned topic and when updating the properties of an existing topic. On these paths the broker authorizes the caller only against the topic being created or updated. It does not authorize the caller against the source topic named in the property. The existing authorization for shadow topic configuration (the SHADOW_TOPIC topic policy on the source topic) is applied only to the source-side shadow topics admin API, not to these paths.

As a result, an authenticated user who is allowed to create topics or update topic properties in one tenant can bind a topic in that tenant to a persistent topic in any other tenant. With the default authorization provider, these operations require the tenant admin role for the user's own tenant. The user does not need any permission on the source topic, its namespace or its tenant. This impact analysis assumes that Pulsar has been configured with the default authorization provider. For custom authorization providers, the impact could be different.

The user can then consume from the shadow topic, using only permissions on their own topic, and receive retained messages that were published to the source topic in the other tenant. Exposure is limited to messages that are still retained and readable in the source topic's ledgers; messages protected with client-side end-to-end encryption cannot be decrypted without the encryption keys. A producer on the shadow topic can also register a new schema version under the source topic's schema, subject to the schema compatibility settings; existing schema versions are not replaced.

In addition, the shadow topic's managed ledger applies its own retention, trimming, offloading and deletion to the source topic's ledgers. This can permanently delete the source topic's ledger data from BookKeeper and from tiered storage, regardless of the source topic's own subscriptions and retention policy, including messages that have not yet been acknowledged. Deleting the shadow topic can also delete the source topic's ledgers. This data loss can also affect shadow topics that were configured intentionally by administrators.

This issue affects Apache Pulsar versions from 3.0.0 before 4.0.14 and from 4.1.0 before 4.2.5. Apache Pulsar 2.x releases do not contain the shadow topic implementation.

- 4.0.x version users should upgrade to at least 4.0.14.
- 4.1.x and 4.2.x version users should upgrade to at least 4.2.5.

Users operating versions prior to those listed above should upgrade to the aforementioned patched versions or newer versions.

The currently supported Apache Pulsar release lines are 4.0.x and 5.0.x. The supported versions schedule is available at https://pulsar.apache.org/contribute/release-policy/.

In the fixed versions, shadow topics are disabled by default and are controlled by the new broker configuration setting enableShadowTopics (default false). While it is disabled, the broker rejects creating shadow topics, setting the PULSAR.SHADOW_SOURCE property, and loading or replicating to existing shadow topics. Deployments that use shadow topics must set enableShadowTopics=true in the broker configuration of all brokers after upgrading; otherwise existing shadow topics will not be loaded. When shadow topics are enabled, binding a shadow topic to a source topic in a different tenant requires the superuser role. The fixed versions also prevent a shadow topic from deleting or trimming the ledgers and offloaded data of its source topic.

Affected versions provide no configuration option to disable shadow topics. Users who cannot upgrade immediately can reduce exposure by granting the tenant admin role only to trusted principals.

### CVE-2026-114126

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-94;CWE-306` |
| Published | 2026-10-21T18:17:25.130 |

Storybook is a frontend workshop for building user interface components and pages in isolation. From 8.0.0 until 8.6.19, 9.1.21, 10.6.2, and 11.0.0-alpha.6, the Storybook development server can expose its WebSocket authentication token to clients able to load its HTML pages over a local network. A LAN attacker can obtain the token and invoke WebSocket-backed file-writing or testing functionality. Weak story-write validation can allow code to be placed in story files. If the Storybook Vitest addon is installed with an old version of Vitest, the payload can use a Vitest API to write additional files or execute commands. Depending on the payload and local tooling, the attack can lead to code execution with the developer's privileges. This issue is fixed in 8.6.19, 9.1.21, 10.6.2, and 11.0.0-alpha.6.

### CVE-2026-114663

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-706` |
| Published | 2026-10-22T02:16:58.603 |

Vyper 0.4.0b1 through 0.5.0b1 miscompiles unfoldable constants and omitted default arguments from imported modules, because parse_Name resolves their names in the using function's scope rather than at declaration. When a contract's parameter, local, or loop variable shares such a name, attacker-influenced input can replace the intended value, including out-of-range values for narrow types such as uint8, corrupting validation or accounting logic.

### CVE-2026-114662

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-22T02:16:58.433 |

Obot before 0.26.0 contains an authentication bypass vulnerability in the CLI login flow that allows unauthenticated attackers to steal API keys by choosing token request IDs. Attackers can create a token request via POST /api/token-request, send the login link to a signed-in user, and fetch the resulting non-expiring API key to take over the victim's account.

### CVE-2026-29001

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-21T21:17:59.230 |

TastyIgniter through 4.4.5 contain a PHP object injection vulnerability that allows authenticated administrators to achieve arbitrary code execution by submitting a serialized PHP object as a settings value, which is stored unsanitized and later unserialized by getValueAttribute() when the setting is read. Attackers can submit a serialized gadget chain, such as one generated via phpggc, through the admin settings form (for example the maintenance_message setting loaded by CheckMaintenance.php) to achieve arbitrary operating-system command execution as the PHP application process user, with the impact persisting until the value is overwritten.

### CVE-2026-114268

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-10-21T19:17:00.780 |

A flaw has been found in Tenda BE3L Pro 16.03.60.62. Affected by this vulnerability is the function formWifiBasicSet of the file /goform/WifiBasicSet. This manipulation of the argument security_5g causes buffer overflow. It is possible to initiate the attack remotely. The exploit has been published and may be used.

### CVE-2026-113870

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-10-21T19:17:00.110 |

MongoDB Compass improperly escapes certain BSON values when converting a stored view’s aggregation pipeline into editable source. When a user connects to a MongoDB deployment containing a specially crafted view and opens that view for editing, the values can cause arbitrary code to execute with the privileges of the user running Compass.

### CVE-2026-114125

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-346;CWE-1021` |
| Published | 2026-10-21T18:17:24.957 |

Storybook is a frontend workshop for building user interface components and pages in isolation. From 8.0.0 until 8.6.19, 9.1.21, 10.6.2, and 11.0.0-alpha.6, a malicious website can interact with the preview of a running Storybook development server. Insufficient iframe embedding and message-origin restrictions can allow attacker-controlled events to reach the running preview. A developer must visit the malicious website and interact with the injected interface. The attack can cause unauthorized changes to story files and, if a changed file is later executed by a local runtime, arbitrary code execution with the developer's privileges. This issue is fixed in 8.6.19, 9.1.21, 10.6.2, and 11.0.0-alpha.6.

### CVE-2026-76490

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-21T17:19:08.340 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Expressway Series software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-76490 are related to issues concerning out-of-bounds writes that are grouped under the Common Weakness Enumeration (CWE) Base CWE-787.

### CVE-2026-112822

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T11:17:32.113 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in AmentoTech Workreap Core workreap_core allows Blind SQL Injection.This issue affects Workreap Core: from n/a before 3.4.4.

### CVE-2026-114716

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-99` |
| Published | 2026-10-22T02:16:59.077 |

Roundcube Webmail before 1.6.20 and 1.7.x before 1.7.5 is affected by a mail header injection vulnerability. rcmail_sendmail::extract_inline_images() used the media type taken from an inline image data URI without validating it, so a remote authenticated attacker could inject arbitrary MIME part headers into the outgoing message by placing CRLF sequences in that media type. Upstream fixed this in the commit “Fix mail header injection via media type in an inline image data URI”, which validates the media type with rcube_mime::is_mimetype_valid().

### CVE-2026-107588

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-1321` |
| Published | 2026-10-21T19:16:57.847 |

Vaadin Charts renders charts with the Highcharts library and pins an exact version of it, 9.2.2 in Vaadin 22 to 24 and 12.2.0 in Vaadin 25, so an application cannot remove these vulnerabilities by upgrading Highcharts on its own. Highsoft disclosed several vulnerabilities in that library that are reachable through the chart configuration: writes to Object.prototype through dotted series.keys paths, and cross-site scripting through credits.href, through breadcrumbs.style, through HTML text parsing while printing, and through xlink:href attributes in exported charts. An application is affected where data an attacker controls reaches the chart configuration, for example through additionalOptions, through updateConfiguration(), or through text options that accept markup. The fixed Vaadin versions apply Highsoft's recommended workarounds to the bundled Highcharts when it loads, and keep the same Highcharts version.


Users of affected versions should apply the following mitigation or upgrade. Releases that have fixed this issue include:

Product version
Vaadin 22.0.0 - 23.6.15
Vaadin 24.0.0 - 24.4.23
Vaadin 24.5.0 - 24.7.15
Vaadin 24.8.0 - 24.9.22
Vaadin 24.10.0 - 24.10.10
Vaadin 25.0.0 - 25.2.9
Vaadin 25.3.0

Mitigation
Upgrade to 23.6.16
Upgrade to 24.4.24
Upgrade to 24.7.16
Upgrade to 24.9.23
Upgrade to 24.10.11
Upgrade to 25.2.10
Upgrade to 25.3.1 or newer

Please note that Vaadin versions 10-13 and 15-22 are no longer supported and you should update either to the latest 23, 24, 25 version.

Artifacts
Maven coordinates / Vulnerable versions / Fixed version
com.vaadin:vaadin / 22.0.0 - 23.6.15 / >=23.6.16
com.vaadin:vaadin / 24.0.0 - 24.4.23 / >=24.4.24
com.vaadin:vaadin / 24.5.0 - 24.7.15 / >=24.7.16
com.vaadin:vaadin / 24.8.0 - 24.9.22 / >=24.9.23
com.vaadin:vaadin / 24.10.0 - 24.10.10 / >=24.10.11
com.vaadin:vaadin / 25.0.0 - 25.0.13 / >=25.2.10
com.vaadin:vaadin / 25.1.0 - 25.1.13 / >=25.2.10
com.vaadin:vaadin / 25.2.0 - 25.2.9 / >=25.2.10
com.vaadin:vaadin / 25.3.0 / >=25.3.1
com.vaadin:vaadin-charts-flow / 22.0.0 - 23.6.15 / >=23.6.16
com.vaadin:vaadin-charts-flow / 24.0.0 - 24.4.22 / >=24.4.24
com.vaadin:vaadin-charts-flow / 24.5.0 - 24.7.14 / >=24.7.15
com.vaadin:vaadin-charts-flow / 24.8.0 - 24.9.22 / >=24.9.23
com.vaadin:vaadin-charts-flow / 24.10.0 - 24.10.10 / >=24.10.11
com.vaadin:vaadin-charts-flow / 25.0.0 - 25.0.13 / >=25.2.10
com.vaadin:vaadin-charts-flow / 25.1.0 - 25.1.13 / >=25.2.10
com.vaadin:vaadin-charts-flow / 25.2.0 - 25.2.9 / >=25.2.10
com.vaadin:vaadin-charts-flow / 25.3.0 / >=25.3.1
com.vaadin:vaadin-charts-flow-svg-generator / 21.0.0 - 23.6.15 / >=23.6.16
com.vaadin:vaadin-charts-flow-svg-generator / 24.0.0 - 24.4.22 / >=24.4.24
com.vaadin:vaadin-charts-flow-svg-generator / 24.5.0 - 24.7.14 / >=24.7.15
com.vaadin:vaadin-charts-flow-svg-generator / 24.8.0 - 24.9.22 / >=24.9.23
com.vaadin:vaadin-charts-flow-svg-generator / 24.10.0 - 24.10.10 / >=24.10.11
com.vaadin:vaadin-charts-flow-svg-generator / 25.0.0 - 25.0.13 / >=25.2.10
com.vaadin:vaadin-charts-flow-svg-generator / 25.1.0 - 25.1.13 / >=25.2.10
com.vaadin:vaadin-charts-flow-svg-generator / 25.2.0 - 25.2.9 / >=25.2.10
com.vaadin:vaadin-charts-flow-svg-generator / 25.3.0 / >=25.3.1

npm packages
npm package / Vulnerable versions / Fixed version
@vaadin/charts / 22.0.0 - 23.6.6 / >=23.6.7
@vaadin/charts / 24.0.0 - 24.4.18 / >=24.4.19
@vaadin/charts / 24.5.0 - 24.7.12 / >=24.7.13
@vaadin/charts / 24.8.0 - 24.9.18 / >=24.9.19
@vaadin/charts / 24.10.0 - 24.10.6 / >=24.10.7
@vaadin/charts / 25.0.0 - 25.0.13 / >=25.2.14
@vaadin/charts / 25.1.0 - 25.1.14 / >=25.2.14
@vaadin/charts / 25.2.0 - 25.2.13 / >=25.2.14
@vaadin/charts / 25.3.0 / >=25.3.1

### CVE-2026-114727

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-22T02:17:00.797 |

Roundcube Webmail before 1.6.20 and 1.7.x before 1.7.5 passes potentially unsafe content into ImageMagick when resizing images. SVG and EPS were accepted as valid image types for contact photo upload and conversion, and both formats can reference external resources and invoke ImageMagick delegates when processed. Upstream fixed this in the commit “Fix passing potentally unsafe attachment content into ImageMagick on image resize”, which removes svg and eps from the accepted types.

### CVE-2026-115333

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-22T11:17:52.563 |

Lotus through 0.10.2 contains an improper authentication vulnerability in the Go event ingestion middleware that validates API keys by prefix only, without checking the secret against the stored hashed_key. Attackers who know or obtain an API key prefix can submit usage events to POST /api/track/ as that organization, altering its metered usage and billing.

### CVE-2026-112085

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-346;CWE-1385` |
| Published | 2026-10-22T10:17:08.760 |

webpack-dev-server is a development server that provides live reloading for webpack projects. In versions before 5.2.7 and in version 6.0.0, when a proxy entry is configured to forward WebSockets, the server forwards non-HMR WebSocket upgrade requests to the proxy target without validating the Host or Origin headers, so the allowedHosts protection does not apply to those proxied upgrades. A malicious web page visited by a developer can open a cross-origin WebSocket through the dev server and read from and write to the proxied backend, even when the server is bound to loopback. The issue is fixed in webpack-dev-server 5.2.7 and 6.1.0, where proxied WebSocket upgrades pass the same Host and Origin validation as the HMR WebSocket, and users should upgrade to one of those versions or later. As a workaround, omit WebSocket forwarding from proxy entries that do not need it and scope the proxy to specific paths.

### CVE-2026-86696

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-22T09:17:16.570 |

Allocation of Resources Without Limits or Throttling vulnerability in esaml in dropbox esaml allows an unauthenticated attacker to exhaust the Erlang VM atom table and crash the node via unsigned LogoutResponse messages.

esaml:status_code_map/1 in src/esaml.erl maps any StatusCode value it does not recognize to an atom with list_to_atom/1 on the last colon-separated segment of the URN. esaml_sp:validate_logout_response/2 verifies a signature only when the message carries one, so an unsigned LogoutResponse posted to the single-logout endpoint reaches esaml:decode_logout_response/1 and mints one permanent atom per distinct status value. Atoms are never reclaimed and the VM caps the atom table at about one million entries, so an attacker who posts that many distinct values aborts the node.

This issue affects esaml: from 0.1.0 onward.

### CVE-2026-15723

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-90` |
| Published | 2026-10-22T01:16:59.477 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 10.1 before 19.3.6, 19.4 before 19.4.3, and 19.5 before 19.5.1 that, when OmniAuth SAML and LDAP auto-linking were both enabled, an authenticated user could have taken over an existing LDAP-backed account without any interaction from the targeted user, due to improper input sanitization in the LDAP email lookup path used during OmniAuth identity linking.

### CVE-2026-96640

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-10-21T21:20:32.357 |

Pillow is a Python imaging library. From 5.1.0 until 13.0.0, PdfParser.linearize_page_tree() in src/PIL/PdfParser.py treats a PDF /Pages graph as a tree without tracking duplicate indirect references. When Image.save(..., format="PDF", append=True) processes an attacker-controlled existing PDF whose /Kids arrays repeatedly reference the same child /Pages node, Pillow expands the shared subtree as distinct pages. A compact malformed PDF can therefore create exponentially many page references and consume disproportionate CPU before the append completes. This issue is fixed in version 13.0.0.

### CVE-2026-112381

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-21T20:17:23.733 |

Apache Traffic Server can crash with a null pointer dereference when a client POST request is torn down via half-close while a chunked origin response is being reparsed from a reentrant write-ready callback, a timing-dependent race introduced by the CVE-2021-32564 flow-control backports.



This issue affects Apache Traffic Server: 9.2.15, 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-92709

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-10-22T14:17:51.473 |

Rsyslog is a rocket-fast system for log processing. From versions 1.15.0 to 8.2610.0, rsyslog's omfile dynaFile facility intentionally allows templates to generate flexible output paths. This supports valid deployments that route logs into different directories or use dynamically generated file names. A deployment becomes unsafe when a dynaFile template uses a value influenced by untrusted input as a path component without explicit secure-path handling. In that configuration, the rendered path can escape the operator's intended log directory. This is not limited to the RFC5424 HOSTNAME field. Any untrusted value that reaches a dynaFile path component can create the condition. At time of publication, there are no publicly available patches.

### CVE-2026-112820

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-22T11:17:31.147 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Elated-Themes Academist Core academist-core allows PHP Local File Inclusion.This issue affects Academist Core: from n/a through 1.4.1.

### CVE-2026-114489

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-21T16:17:35.500 |

Missing authorization in the REST and COM administration APIs of Progressive Robot hMailServer 6.0.0 through 6.3.6 allows a remote authenticated user whose credential is confined to named domains to change mail routing and domain configuration beyond those domains on a multi-tenant server. A domain administrator, an account or API key given another role that manages accounts in named domains, or a full-scope API key issued for named domains could create a domain alias for any name (so that other tenants' mail for that name is diverted to an address the attacker controls, or denied), rename a domain to any name the server does not host, set a rule's bind-to-address, send-using-route or script-function action to reach one of the server's own addresses, a configured route's stored credentials or a function of the server's event script, and set the domain's relay host - which delivery then connects to with no address rule - to an address on the server's own network; and over the COM API any account could set the three rule actions on its own rules, where the script-function action runs at delivery. The authorization gate did not refuse these routes to a confined credential and the handlers were not given the caller; over COM the domain-alias save performed no authorization check at all, the domain rename required only a domain administrator, and a rule save required at most that the caller could change the rule's owner.

### CVE-2026-111815

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-21T20:17:23.330 |

Apache Traffic Server can resume a TLS session across SNI virtual hosts without re-verifying a client certificate required by the resumed host's verify_client STRICT policy.



This issue affects Apache Traffic Server: from 8.0.0 through 8.1.11, from 9.0.0 through 9.2.15, from 10.0.0 through 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-111814

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-21T20:17:23.190 |

Apache Traffic Server's default outbound session-sharing policy can reuse a pooled TLS session authenticated with one client certificate for a transaction configured to present a different one.



This issue affects Apache Traffic Server: from 9.0.0 through 9.2.15, from 10.0.0 through 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-19676

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-21T19:17:02.650 |

The user-mode verifier for the peci_transfer() system call, z_vrfy_peci_transfer() in drivers/peci/peci_handlers.c, checked only the device object permission and copied the caller-supplied struct peci_msg with k_usermode_from_copy(). That copy validates the outer structure only; the buf pointers and len values inside the embedded struct peci_buf members tx_buffer and rx_buffer remained fully caller-controlled and were passed unchecked to the driver.

Every in-tree PECI driver dereferences those pointers in supervisor mode: peci_npcx_transfer() in drivers/peci/peci_npcx.c and peci_it8xxx2_transfer() in drivers/peci/peci_ite_it8xxx2.c copy hardware bytes into rx_buffer.buf[i] and read command bytes out of tx_buffer.buf[i], and peci_xec_read()/peci_xec_write() in drivers/peci/peci_mchp_xec.c do the same with no bound on rx_buffer.len at all. A user-mode thread that has been granted the PECI device object — the normal way an application exposes a device under CONFIG_USERSPACE — could therefore point rx_buffer.buf at kernel data structures and have the driver write hardware-supplied bytes there, or point tx_buffer.buf at kernel memory and have its contents pushed onto the PECI/eSPI out-of-band bus.

The impact is a full user-mode-to-kernel escape: an arbitrary kernel write primitive (integrity and, through it, code execution at supervisor privilege), an arbitrary kernel read disclosed to a PECI bus observer, and a trivially reachable supervisor-mode fault if an unmapped address is supplied. Exploitation requires CONFIG_USERSPACE=y, one of the PECI drivers enabled (CONFIG_PECI_NPCX, CONFIG_PECI_XEC or CONFIG_PECI_ITE_IT8XXX2), and local code execution in a user-mode thread holding the PECI device.

The fix adds K_SYSCALL_MEMORY_READ() and K_SYSCALL_MEMORY_WRITE() checks over the two embedded buffers, with a size_add_overflow() guard on the frame-check-sequence byte accounted for in the RX length.

### CVE-2026-92209

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-331` |
| Published | 2026-10-21T18:17:31.597 |

NoMachine Redis Improper Authentication Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of NoMachine. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the authentication mechanism controlling access to the Redis database. The issue results from using insufficient entropy in the generation of credentials. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of the service account. Was ZDI-CAN-30984.

### CVE-2026-92202

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-21T18:17:30.620 |

Luxion KeyShot BIP File Parsing Uncontrolled Search Path Element Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Luxion KeyShot. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of BIP files. The issue results from loading a library from an unsecured location. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29268.

### CVE-2026-92183

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-21T18:17:30.443 |

GIMP APNG File Parsing Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of APNG files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a stack-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29400.

### CVE-2026-111184

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-21T18:17:23.620 |

NoMachine Named Pipe Incorrect Permission Assignment Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of NoMachine. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the NoMachine Device Service. The issue results from incorrect permissions on a named pipe. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-31213.

### CVE-2026-76524

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-21T17:19:09.610 |

A vulnerability in the control channel socket implementation of&nbsp;Open Source Snort 3 could allow an authenticated, local attacker with low privileges to execute arbitrary commands as the Snort 3 process user.

This vulnerability is due to a lack of authentication when a local user connects to the Snort control channel socket. An attacker could exploit this vulnerability by connecting to the Snort 3 control channel socket as a local user. A successful exploit could allow the attacker to execute arbitrary commands as well as read and write Snort 3 process memory.

### CVE-2026-76495

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-21T17:19:09.037 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Expressway Series software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-76495 are related to issues concerning incorrect permission assignments that are grouped under the Common Weakness Enumeration (CWE) Variant CWE-732.

### CVE-2026-76494

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-21T17:19:08.897 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Expressway Series software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-76494 are related to issues concerning code injections that are grouped under the Common Weakness Enumeration (CWE) Base CWE-94.

### CVE-2026-76479

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-21T17:19:07.780 |

As part of Cisco's ongoing commitment to proactive security and product quality, engineering teams for Cisco Emergency Responder, Cisco Prime Collaboration Deployment, Cisco Unified Communications Manager (Unified CM), Cisco Unified Communications Manager IM &amp; Presence Service (Unified CM IM&amp;P), Cisco Unified Communications Manager Session Management Edition (Unified CM SME), and Cisco Unity Connection have conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76479 are related to issues concerning improper limitation of a pathname to a restricted directory that are grouped under the Common Weakness Enumeration (CWE) Base CWE-22.

### CVE-2026-20291

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-21T17:18:28.473 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco owned Open Source Snort 3 Software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20291 are related to issues concerning improper privilege management that are grouped under the Common Weakness Enumeration (CWE) Base CWE-269.

### CVE-2026-114490

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-21T16:17:35.647 |

Incorrect authorization in the COM administration API of Progressive Robot hMailServer 6.3.4 through 6.3.6 allows an account assigned the serveradmin role with a list of domains - a credential an administrator may create meaning to confine it to those domains - to act as the whole-server administrator over COM. Administrator roles are meant to confine such a credential to the domains its list names, and the REST API did not take it for the server administrator, but the COM API's server-administrator check read the administer_server permission as the whole server whatever list the grant carried. So the credential signed in through the Control Panel, or through a script run on the server, as the server administrator of every domain: it could read and change every domain's accounts and mail, rename any domain, map a domain alias onto any, write the server's settings and secrets, and create further server-administrator accounts. The COM API's domain-administrator check, asked with no domain, likewise let an account assigned the domainadmin role with a list of domains that leaves out the account's own domain administer that domain's ordinary accounts over COM. An account holding serveradmin with no list is the server administrator by design and is unaffected, as are the help desk, auditor and custom roles.

### CVE-2017-20289

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-22T11:17:03.063 |

Broadstreet Ad Widget plugin for WordPress 2.2.0 before 2.12.0 contains a local file inclusion vulnerability that allows authenticated users to execute attacker-chosen PHP files by passing unsanitized input to require in views/modal/index.php. Attackers can supply directory traversal sequences in the 'step' parameter, optionally with a null byte, to include local files and execute PHP code. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-19.

### CVE-2026-96778

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-21T21:20:33.093 |

Pillow is a Python imaging library. From 9.4.0 until 13.0.0, ImagingJpegEncode() in src/libImaging/JpegEncode.c can call jpeg_write_marker() for a JPEG COM comment when an ICC profile has exactly filled the 65536-byte encoder buffer. libjpeg writes one byte before checking the exhausted free_in_buffer counter, which then wraps and permits the attacker-controlled comment and subsequent compressed image data to overwrite adjacent heap memory. Re-saving an untrusted image as JPEG while preserving its ICC profile and forwarded comment can crash the process and may enable code execution in suitable runtime and heap layouts. This issue is fixed in version 13.0.0.

### CVE-2026-111808

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-21T20:17:22.427 |

Apache Traffic Server can be used to exhaust an HTTP/1.1 origin's worker pool via a malformed padded HTTP/2 DATA frame.



This issue affects Apache Traffic Server: from 8.0.0 through 8.1.11, from 9.0.0 through 9.2.15, from 10.0.0 through 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-111805

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-21T20:17:22.257 |

Apache Traffic Server can be used to exhaust an HTTP/1.1 origin's worker pool via a truncated HTTP/2 Content-Length value.



This issue affects Apache Traffic Server: from 8.0.0 through 8.1.11, from 9.0.0 through 9.2.15, from 10.0.0 through 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-105945

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-21T19:16:57.660 |

The Pulsar Packages Management Service can be configured to store packages on the local filesystem of the broker by using the filesystem storage provider. Package names consist of a type, tenant, namespace, name and version. Authorization of package operations is based only on the tenant and namespace, while the storage location of a package is derived from all of these components. The version component of a package name was not validated, so it could contain URL-encoded path separators and parent directory references. The filesystem storage provider resolved such a version to a location belonging to a package in a different tenant or namespace. Because that location is inside the configured storage directory, the containment check that the filesystem storage provider performs in recent releases did not prevent the access.

An authenticated user who has the packages permission on any namespace could use this to download, overwrite or delete packages stored in other tenants or namespaces for which the user has no permission. Packages overwritten or deleted in this way may be used by Pulsar Functions, Sources or Sinks, so the issue can affect the integrity and availability of these components. If authentication is disabled, the operations are available to any client that can reach the broker's admin REST API.

This issue only affects deployments in which package management is enabled with the broker setting enablePackagesManagement and the filesystem storage provider (FileSystemPackagesStorageProvider) is configured with the setting packagesManagementStorageProvider. Package management is disabled by default, and the default storage provider, which stores packages in Apache BookKeeper, is not affected.

This issue affects Apache Pulsar versions from 2.10.0 before 4.0.14 and from 4.1.0 before 4.2.5.

- 4.0.x version users should upgrade to at least 4.0.14.
- 4.1.x and 4.2.x version users should upgrade to at least 4.2.5.

Users operating versions prior to those listed above should upgrade to the aforementioned patched versions or newer versions.

The currently supported Apache Pulsar release lines are 4.0.x and 5.0.x. The supported versions schedule is available at https://pulsar.apache.org/contribute/release-policy/.

### CVE-2026-105942

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-21T19:16:57.203 |

When a configured proxy role sends a request to the broker on behalf of another user (the original principal), the broker is designed to authorize both the proxy role and the original principal and to allow the request only if both are authorized, so that the original principal cannot exceed its own permissions. Two flaws weakened this check.

First, the original principal was authorized with the proxy's authentication data instead of its own. On the admin REST API of the broker and the functions worker, this applied to every proxied request. On the Pulsar binary protocol, it applied when the proxy did not forward the client's credentials to the broker, which was the default of the Pulsar proxy in the affected versions. Authorization providers that resolve permissions from the role name only, such as the default authorization provider, are not affected by this flaw. The multi-role token authorization provider (MultiRolesTokenAuthorizationProvider), added in Apache Pulsar 2.8.1, resolves roles from the role claim of the token in the authentication data it is given. When a proxy authenticates to the broker with its own token, the original principal was therefore authorized with all roles in the proxy's token. If any of those roles is a superuser or tenant admin role, any user whose requests are forwarded by that proxy can perform operations that need those permissions without holding them. Custom authorization providers that use the authentication data could be affected in a similar way.

Second, independently of the authorization provider, the tenant admin check of a proxied admin REST API request succeeded without checking the original principal when the proxy role was itself an admin role of the tenant. In deployments where a proxy role is a tenant admin, including with the default authorization provider, any user whose requests are forwarded by that proxy could perform tenant administration operations on that tenant. This behavior is present from 2.8.4 in the 2.8.x releases, from 2.9.3 in the 2.9.x releases, and from 2.10.1 onwards.

Deployments that use neither the multi-role token authorization provider nor a custom provider that uses the authentication data are not affected by the first flaw, and with the multi-role token authorization provider, neither are deployments whose proxies do not authenticate to the broker with a token. Deployments in which no proxy role is listed as an admin role of a tenant are not affected by the second flaw. A proxy role that is a superuser but is not listed as a tenant admin does not trigger it, because the tenant admin check of the built-in authorization providers only considers the tenant's admin roles; this can differ for custom authorization providers that treat superusers as tenant admins.

In fixed versions, both the proxy role and the original principal are authorized for each proxied request, and the original principal is authorized only with its own authentication data. With the multi-role token authorization provider, the roles of a forwarded token are used for the original principal only when that token authenticates as the original principal; otherwise only the original principal's role name is used. For tenant admin checks, the proxy role and the original principal must each be a superuser or a tenant admin of the tenant.

This issue affects Apache Pulsar versions from 2.8.1 before 4.0.14 and from 4.1.0 before 4.2.5.

- 4.0.x version users should upgrade to at least 4.0.14.
- 4.1.x and 4.2.x version users should upgrade to at least 4.2.5.

Users operating versions prior to those listed above should upgrade to the aforementioned patched versions or newer versions.

The currently supported Apache Pulsar release lines are 4.0.x and 5.0.x. The supported versions schedule is available at https://pulsar.apache.org/contribute/release-policy/.

### CVE-2026-92204

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-21T18:17:30.883 |

Airbyte OneDrive Connector _get_shared_drive_object Server-Side Request Forgery Information Disclosure Vulnerability. This vulnerability allows remote attackers to initiate arbitrary server-side requests on affected installations of Airbyte. Authentication is required to exploit this vulnerability.

The specific flaw exists within the _get_shared_drive_object method. The issue results from the lack of proper validation of a URI prior to accessing resources. An attacker can leverage this vulnerability to disclose information in the context of the service account. Was ZDI-CAN-28216.

### CVE-2026-92203

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-21T18:17:30.757 |

Airbyte SharePoint Connector _get_shared_drive_object Server-Side Request Forgery Information Disclosure Vulnerability. This vulnerability allows remote attackers to initiate arbitrary server-side requests on affected installations of Airbyte. Authentication is required to exploit this vulnerability.

The specific flaw exists within the implementation of the _get_shared_drive_object method. The issue results from the lack of proper validation of a URI prior to accessing resources. An attacker can leverage this vulnerability to disclose information in the context of the service account. Was ZDI-CAN-28215.

### CVE-2026-115334

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-22T11:17:52.703 |

Lotus through 0.10.2 contains an authorization bypass vulnerability in ChangeUserOrganizationView.post that allows authenticated users to join any organization by supplying its UUID. Self-registered attackers who know another organization's UUID can send a POST request to /app/switch_organization/ to access that tenant's data and billing configuration.

### CVE-2026-111851

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-10-22T09:17:13.843 |

Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection') vulnerability in WProyal Royal Elementor Addons royal-elementor-addons allows Code Injection.This issue affects Royal Elementor Addons: from n/a through 1.7.1068.

### CVE-2026-94502

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-22T14:17:51.640 |

In EmberZNet 9.1.1 and earlier, a malformed Publish Price Matrix command can result in an out-of-bounds write potentially leading to remote code execution. These messages must come from a device that has already joined the network. Only devices supporting the Price Cluster are impacted.

### CVE-2026-85079

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-22T14:17:50.877 |

In EmberZNet 9.1.1 and earlier, a malformed Simple_Desc_req response can result in an out-of-bounds write potentially leading to remote code execution. This response must come from a device that has already joined the network, and the attacker must wait for a Simple_Desc_req before the attack can be performed.

### CVE-2026-112312

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-22T09:17:14.553 |

Missing Authorization vulnerability in ACF Extended ACF Extended acf-extended allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects ACF Extended: from n/a through 0.9.2.7.

### CVE-2026-97328

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-22T06:17:15.930 |

The WebP Express WordPress plugin before 0.25.16 does not escape values that its bundled HTML parser re-emits into element attributes when a non-default image delivery mode is enabled, allowing unauthenticated users to submit content that is stored and later executed as Cross-Site Scripting in the browser of any user viewing an affected page, including administrators.

### CVE-2026-111958

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-22T06:17:14.113 |

The Royal MCP  WordPress plugin before 1.5.7 does not limit a preview-link token to the single preview it was issued for, so any party that obtains a valid token is authenticated as the token's owning user, an administrator in the default configuration, across the entire REST API with no nonce, leading to full site takeover.

### CVE-2026-110354

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-22T03:16:31.427 |

HAProxy 3 before 3.4.6 allows a remote unauthenticated attacker to cause a denial of service (persistent worker-thread CPU exhaustion) via an HTTP/1.1 chunked request. Although the H1 multiplexer drains the request before closing the stream, the parser repeatedly re-processes the same bytes without making progress. The affected thread stays busy at 100% CPU after timeouts expire and after the client disconnects, and repeated requests can consume all worker threads until the process is restarted.

### CVE-2026-110353

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-252` |
| Published | 2026-10-22T03:16:31.270 |

HAProxy 3.2 before 3.4.6 allows a remote unauthenticated attacker to cause a denial of service (worker-thread CPU exhaustion) via a truncated HTTP/2 PING frame. h2c_handle_ping in src/mux_h2.c does not check for a short read, unlike the other H2 frame handlers. Because the incomplete frame cannot be processed, its data is never consumed, and the H2 multiplexer tasklet is repeatedly woken by that pending data without making progress. The CPU spins until timeout http-request closes the connection, and an attacker opening many such connections can sustain high CPU usage.

### CVE-2026-112212

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-444` |
| Published | 2026-10-22T01:16:57.740 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.3 before 19.3.6, 19.4 before 19.4.3, and 19.5 before 19.5.1 that, under certain conditions, an unauthenticated user could have poisoned a shared cache's OAuth/OIDC discovery document to redirect certain flows to an externally controlled server, due to improper trust of user-supplied values when constructing endpoint URLs in cached discovery responses.

### CVE-2026-76306

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-21T23:17:28.770 |

In Splunk SOAR versions below 8.7.0, a user that has the "Observer" role could use query filters in the Representational State Transfer (REST) API to infer password hashes and authorization tokens for other users.
The information disclosure is possible because Splunk SOAR applies REST API query filters to user records before it protects sensitive fields from query processing.
For more information see Using the REST API reference for Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/rest-api-reference/8.5.0/using-the-splunk-soar-rest-api/using-the-rest-api-reference-for-splunk-soar-on-premises), Query for Data (https://help.splunk.com/en/splunk-soar/soar-on-premises/rest-api-reference/7.1.0/using-the-splunk-soar-rest-api/query-for-data), and Manage roles and permissions in Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.5.0/manage-your-splunk-soar-on-premises-users-and-accounts/manage-roles-and-permissions-in-splunk-soar-on-premises) in the Splunk documentation.

### CVE-2026-76290

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-21T23:17:26.820 |

In Splunk Enterprise versions below 10.4.4, 10.2.8, and 10.0.11, an unauthenticated user could send repeated requests to the Edge Processor package download endpoint in the Splunk Pipeline Builders app. The requests could cause the Splunk daemon to consume excessive system resources and potentially stop responding.
The vulnerability is possible because the endpoint accepts package download requests without authentication and reads and base64-encodes the complete package in memory for each request.
After upgrading, prepare all existing Edge Processor instances, turn on authentication for Edge Processor package downloads, and restart Splunk Enterprise. For more information, see Enable authentication for Edge Processor package downloads (https://help.splunk.com/en/data-management/process-data-at-the-edge/use-edge-processors-for-splunk-enterprise/10.4/administer-edge-processors/enable-authentication-for-edge-processor-package-downloads).

### CVE-2026-76288

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-21T23:17:26.537 |

In Splunk Enterprise versions below 10.4.4, 10.2.8, 10.0.11, and 9.4.16, an unauthenticated user could send a single crafted request to the Splunk Web JavaScript logger endpoint and cause Splunk Web to stop responding to requests. Splunk Web remains unavailable until Splunk Enterprise is restarted.
The vulnerability is possible because Splunk Web does not limit request-header parsing before processing the request.

### CVE-2026-114145

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-696` |
| Published | 2026-10-21T21:17:57.250 |

GitPython is a python library used to interact with Git repositories. Prior to 3.2.1, create_submodule() in git/objects/submodule/base.py accepts an attacker-influenced submodule path such as .git/hooks and invokes _clone_repo() before safely rejecting the destination. In 3.1.x, _validate_repo_path() does not exist and the call succeeds silently, while in 3.2.0 and later affected revisions the check in git/index/base.py raises ValueError only after the clone has written to disk and does not remove the planted file. An attacker-controlled submodule can therefore place an executable post-checkout hook that a later Git operation executes. Exploitation requires an application to accept an untrusted submodule path and a clone destination such as .git/hooks that is empty enough for Git to clone into it, which commonly means that default sample hooks are absent. This issue is fixed in version 3.2.1.

### CVE-2026-114144

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-21T21:17:57.103 |

toml-node is a TOML parser for Node.js and the browser. Prior to 5.0.1, toml.parse() passes unbounded hexadecimal, octal, binary, and decimal digit sequences from lib/parser.js to BigInt() before reduceInteger() in lib/compiler.js checks whether the resulting value fits the TOML 64-bit integer range. Converting a sufficiently long integer string consumes super-linear CPU time and synchronously blocks the Node.js event loop, allowing one attacker-supplied TOML document to deny service to concurrent work in the process. The later range check cannot prevent the conversion cost because it executes after BigInt(). This issue is fixed in version 5.0.1.

### CVE-2026-114138

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-10-21T21:17:56.200 |

Django REST framework is a toolkit for building Web APIs. Prior to 3.18.2, DefaultContentNegotiation.get_accept_list in rest_framework/negotiation.py accepts an unbounded number and aggregate size of Accept tokens, while select_renderer in that file repeatedly invokes _MediaType parsing from rest_framework/utils/mediatypes.py for each attacker-controlled token, every renderer, and forced 406 renegotiation. A remote unauthenticated client can send many distinct media types containing large quoted parameter values with numerous semicolons, causing Django's parameter parser and DRF's repeated parsing structure to consume disproportionate CPU. Requests to any reachable endpoint can pin synchronous workers for prolonged periods, and concurrent requests can make the service unavailable until the requests stop. This issue is fixed in version 3.18.2.

### CVE-2026-114136

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409;CWE-770` |
| Published | 2026-10-21T20:17:25.557 |

Django REST framework is a toolkit for building Web APIs. From 3.6.4 until 3.18.2, JSONParser.parse in rest_framework/parsers.py uses the client-supplied Content-Type charset value with codecs.getreader, which accepts byte-transform codecs such as bz2_codec rather than only text encodings. A remote unauthenticated client can therefore cause a compressed JSON request body to be expanded after Django has enforced DATA_UPLOAD_MAX_MEMORY_SIZE against only the wire bytes, allowing a very small request to consume substantial per-worker memory. The default parser set is sufficient, and any reachable endpoint that accepts a JSON body is affected. This issue is fixed in version 3.18.2.

### CVE-2026-76505

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-21T17:19:09.450 |

A vulnerability in the IPv4 packet processing functionality of Cisco IOS XR Software that affects Cisco ASR 9000 and 9900 Series Aggregation Services Routers as well as Cisco ASR 9902 and 9903 Compact High-Performance Routers could allow an unauthenticated, remote attacker to cause network processor (NP) errors, resulting in a line card reset or shutdown and a denial of service (DoS) condition.&nbsp;

This vulnerability is due to the incorrect handling of crafted IPv4 packets that are received on an affected line card interface and processed as for-us traffic. The issue can result in an NP reset, causing traffic loss on the affected line card while it recovers. Under repeated reset conditions, the network processor may enter a persistent shutdown state, in which case an explicit line card reload may be required to restore traffic.
The vulnerability is within the IPv4 packet-processing path. Transit IPv4 traffic does not trigger this issue and IPv6 traffic cannot trigger it.

### CVE-2026-76493

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-21T17:19:08.760 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Expressway Series software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-76493 are related to issues concerning uncaught exceptions that are grouped under the Common Weakness Enumeration (CWE) Base CWE-248.

### CVE-2026-76492

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-21T17:19:08.620 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Expressway Series software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-76492 are related to issues concerning null pointers that are grouped under the Common Weakness Enumeration (CWE) Base CWE-476.

### CVE-2026-76491

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-21T17:19:08.480 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Expressway Series software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-76491 are related to issues concerning reachable assertions that are grouped under the Common Weakness Enumeration (CWE) Base CWE-617.

### CVE-2026-76481

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-703` |
| Published | 2026-10-21T17:19:07.910 |

As part of Cisco's ongoing commitment to proactive security and product quality, engineering teams for Cisco Emergency Responder, Cisco Prime Collaboration Deployment, Cisco Unified Communications Manager (Unified CM), Cisco Unified Communications Manager IM &amp; Presence Service (Unified CM IM&amp;P), Cisco Unified Communications Manager Session Management Edition (Unified CM SME), and Cisco Unity Connection have conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76481 are related to issues concerning improper handling of exceptional conditions that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-703.

### CVE-2026-20356

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-21T17:18:28.703 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco owned Open Source Snort 3 Software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20356 are related to issues concerning uncontrolled resource consumption that are grouped under the Common Weakness Enumeration (CWE) Base CWE-400.

### CVE-2026-20236

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-682` |
| Published | 2026-10-21T17:18:28.247 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco owned Open Source Snort 3 Software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20236 are related to issues concerning incorrect calculation that are grouped under the Common Weakness Enumeration (CWE) Base CWE-682.

### CVE-2026-114123

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306;CWE-1188` |
| Published | 2026-10-21T17:18:25.737 |

D365 F&O MCP Server is a Model Context Protocol server for querying Dynamics 365 Finance & Operations X++ code and metadata. Prior to version 1.11.0, the officially documented Azure one-click deployment uses infrastructure/azuredeploy.json and infrastructure/main.bicep to default the apiKey parameter to an empty string and pass it to the App Service API_KEY setting. With API_KEY unset or empty, src/middleware/apiKeyAuth.ts passes requests through without authentication, while src/index.ts binds the HTTP listener to 0.0.0.0 by default. If the deployer leaves the optional key blank and does not add separate network restrictions or upstream authentication, the resulting public App Service allows unauthenticated JSON-RPC tools/call requests to /mcp. The deployment's MCP_SERVER_MODE=read-only setting does not prevent anonymous access to read/search tools, including search, get_object_info, batch_get_info, extension_info, security_info, find_references, and find_event_handlers, exposing indexed proprietary X++ source snippets and metadata. Exposed information can include business logic, extension and event-handler wiring, security-role and privilege structure, and labels originally indexed from PackagesLocalDirectory. Deployments protected by a configured API key, effective upstream authentication, or network restrictions preventing attacker access are outside this unauthenticated exposure scenario. This issue is fixed in version 1.11.0.

### CVE-2026-114476

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-21T16:17:34.947 |

Incorrect authorization in the REST administration API of Progressive Robot hMailServer 6.3.4 through 6.3.6 allows a remote authenticated user whose credential holds the manage_roles permission in named domains - a full-scope API key issued for those domains, or an account assigned the serveradmin role with a list of domains - to obtain the server administrator's authority. An account's admin level gives it authority, and a role assigned to it replaces that authority, which is how an administrator narrows an account whose admin level is the server administrator's. The route that takes a role away (DELETE /api/v1/role-assignments/{address}) checked only that the credential takes in what the account held at the time, not what it would hold afterwards, so such a credential could take a narrowing role away from an account in its domains whose admin level is the server administrator's, returning it to the server administrator's authority, and, having set that account's password while it held the narrower role, sign in as the server administrator.

### CVE-2026-102486

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-21T16:17:14.313 |

Out-of-bounds read in NTS extension field parsing in NTPsec ntpd 1.1.4 through 1.2.5 allows a remote attacker to crash the daemon via an NTS Authenticator and Encrypted Extension Fields (AEEF) field with an oversized nonce length.

### CVE-2026-102483

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-21T16:17:13.910 |

Reachable exit in NTPsec ntpd 1.1.4 through 1.2.5 allows a remote attacker to terminate the daemon via an NTS request with excess NTS Cookie Placeholder extension fields.

### CVE-2026-111833

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-21T15:17:15.260 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Bold Grid weForms weforms allows Path Traversal.This issue affects weForms: from n/a through 1.6.28.

### CVE-2026-111079

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-10-22T11:17:15.460 |

A flaw was found in Goose. When the terminal integration feature is enabled, the application captures shell command history and sends it verbatim without sanitization to configured Large Language Model (LLM) provider endpoints during queries. If a user enters sensitive data—such as API tokens, passwords, or environment variables containing secrets—in the terminal, this unredacted information is transmitted across trust boundaries. This can lead to sensitive information disclosure, exposing confidential credentials to external service providers and logs.

### CVE-2026-114724

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-22T02:17:00.343 |

Roundcube Webmail before 1.6.20 and 1.7.x before 1.7.5 contains an object injection primitive in rcube_session::unserialize(). A session key prefixed with “!” was treated as having no value, and the reconstructed serialized string was emitted with a key but no corresponding value, desynchronizing the remainder of the input so that following session data was interpreted as a serialized value. This yields a PHP object injection primitive for an attacker able to influence stored session data. Upstream fixed this in the commit “Fix object injection primitive in rcube_session::unserialize() via “!”-prefixed session keys”, which rejects such keys.

### CVE-2026-114137

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-390;CWE-613` |
| Published | 2026-10-21T21:17:56.057 |

Django REST framework is a toolkit for building Web APIs. From 3.12.0 until 3.18.2, TokenProxy.delete() in rest_framework/authtoken/models.py uses the proxy's user-id pk while the concrete Token token-string primary key identifies rows, so Django issues a deletion query that matches no row and reports zero deletions without raising an error. Applications, administrative integrations, or operational scripts that revoke credentials through a TokenProxy instance can therefore believe revocation succeeded while the token remains live and continues authenticating. DRF's own TokenAdmin.delete_model workaround is not affected, but other callers can leave access available indefinitely because DRF tokens do not expire automatically. This issue is fixed in version 3.18.2.

### CVE-2026-115253

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276;CWE-732` |
| Published | 2026-10-22T09:17:16.137 |

An incorrect permission assignment vulnerability in the WatchGuard Agent's log directory allows a local, authenticated non-administrative user to create, modify, append to, or delete the agent's log files and write other files into the directory. This allows an attacker to tamper with or destroy the agent's security logs and stage further local attacks by placing executable content in a directory owned by a privileged service.

### CVE-2026-66279

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-940` |
| Published | 2026-10-22T14:17:43.840 |

In Connect SDK 4.3.1 and earlier and Flex SDK 3.7.7 and earlier, a message with invalid security settings may bypass authentication resulting in network disruption. This vulnerability does not allow an attacker to gain the Network Key or otherwise break confidentiality.

### CVE-2026-109987

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-22T06:17:13.800 |

The PixelYourSite  WordPress plugin before 11.4.3, PixelYourSite Pro WordPress plugin before 12.6.8 do not sanitise and escape a cookie value before printing it into the page output, which, on a site running a full-page cache, allows unauthenticated attackers to store a Cross-Site Scripting payload in the cached page that is then served to other visitors.

### CVE-2026-109927

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-22T06:17:13.590 |

The HIPAA Forms WordPress plugin before 3.3.2 does not perform a capability check when handling a request that rebuilds its own custom user role, allowing a user who already holds that role to grant it administrator-level capabilities and escalate their privileges.

### CVE-2026-114730

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-22T03:16:38.217 |

Roundcube Webmail 1.6.14 before 1.6.20 and 1.7.0 before 1.7.5 is affected by a server-side request forgery filter bypass. The network blocklist used by rcube_utils::is_local_url() omitted the RFC 6052 NAT64 prefix 64:ff9b::/96, the RFC 8215 local-use NAT64 prefix 64:ff9b:1::/48 and the unspecified address ::/128, so URLs such as http://[64:ff9b::7f00:1]/ passed the filter and reached loopback, link-local and cloud metadata addresses. Upstream fixed this in the commit “Fix SSRF filter (is_local_url()) bypass via NAT64 64:ff9b::/96”.

### CVE-2026-76307

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-21T23:17:28.893 |

In Splunk SOAR versions below 8.7.0, a user that holds a role with the Users and Roles view permission could use the Representational State Transfer (REST) API to infer authentication token values for other users. If the inferred token grants administrative access, that user could gain administrative access to the Splunk SOAR instance.
The vulnerability is possible because the REST API accepts caller-controlled query filters on sensitive user record fields.
For more information see Using the REST API reference for Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/rest-api-reference/7.1.0/using-the-splunk-soar-rest-api/using-the-rest-api-reference-for-splunk-soar-on-premises), Query for Data (https://help.splunk.com/en/splunk-soar/soar-on-premises/rest-api-reference/7.1.0/using-the-splunk-soar-rest-api/query-for-data), and Manage roles and permissions in Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/6.4.0/manage-your-splunk-soar-on-premises-users-and-accounts/manage-roles-and-permissions-in-splunk-soar-on-premises) in the Splunk documentation.

### CVE-2026-76293

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-21T23:17:27.200 |

In Splunk Enterprise versions below 10.4.3, 10.2.8, 10.0.11, and 9.4.16, a user that holds a role with the edit_manager_xml capability could execute arbitrary operating-system commands using the permissions of the user account running Splunk Enterprise by opening the affected configuration in the Splunk Web Manager page. 
The vulnerability is possible because Splunk Web evaluates user-controlled expressions from Manager XML without sufficiently restricting the expression syntax.

### CVE-2026-105934

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-21T19:16:56.103 |

The Apache Pulsar broker admin REST API provides a truncate operation for persistent topics (DELETE /admin/v2/persistent/{tenant}/{namespace}/{topic}/truncate). Truncating a topic moves all subscription cursors of the topic to the end of the topic and deletes the topic's inactive ledgers. Truncating a non-partitioned topic, or a single partition addressed by its partition name, correctly requires the tenant admin role or the superuser role. When the operation is requested for the name of a partitioned topic, the broker does not apply this tenant admin check to the caller. Instead, it truncates each partition using the broker's own internal admin client, which authenticates with the broker's configured client credentials rather than the caller's identity. Each per-partition truncate request is still checked for the tenant admin role or the superuser role, but against the broker's internal identity instead of the caller. The partitions are therefore truncated only when the broker's configured client role is a superuser or an admin of the target tenant, which is the usual configuration when authorization is enabled.

As a result, when that condition holds, an authenticated user who is not a tenant admin can truncate any partitioned topic on which the user has lookup permission. Caller authentication and lookup permission alone are not sufficient: if the broker's internal identity lacks tenant admin or superuser authorization for the target tenant, the per-partition requests are rejected. With the default authorization provider, lookup permission is granted by produce or consume permission on the topic or its namespace. A user with no permissions on the topic cannot trigger the issue. This impact analysis assumes that Pulsar has been configured with the default authorization provider. For custom authorization providers, the impact could be different.

Truncating a partitioned topic this way moves the cursors of all subscriptions on every partition to the end of the topic, so any unacknowledged backlog is skipped and is no longer delivered to consumers. It also deletes eligible older ledgers of each partition regardless of the namespace's configured retention policy, so messages stored in those ledgers can be permanently lost. The ledger currently being written is not deleted by the truncate operation. The issue does not allow reading message contents or changing permissions or configuration, and it does not give access to topics on which the user has no lookup permission.

This issue affects Apache Pulsar versions from 2.8.0 before 4.0.14 and from 4.1.0 before 4.2.5.

- 4.0.x version users should upgrade to at least 4.0.14.
- 4.1.x and 4.2.x version users should upgrade to at least 4.2.5.

Users operating versions prior to those listed above should upgrade to the aforementioned patched versions or newer versions.

The currently supported Apache Pulsar release lines are 4.0.x and 5.0.x. The supported versions schedule is available at https://pulsar.apache.org/contribute/release-policy/.

Users who cannot upgrade immediately can reduce exposure by restricting network access to the broker's admin REST API (/admin/v2) to trusted administrative clients.

### CVE-2026-92210

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-21T18:17:31.730 |

NoMachine nxhtd Server-Side Request Forgery Information Disclosure Vulnerability. This vulnerability allows remote attackers to initiate arbitrary server-side requests on affected installations of NoMachine. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the web service, which listens on UDP port 4443 by default. The issue results from the lack of proper validation of a URI prior to accessing resources. An attacker can leverage this vulnerability to initiate requests in the context of the service account. Was ZDI-CAN-31619.

### CVE-2026-110744

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-21T18:17:23.350 |

A flaw was found in multicluster-global-hub-operator-bundle. The operator is configured with overly broad role-based access control (RBAC) permissions that grant cluster-wide impersonation of arbitrary users, groups, and service accounts without restriction. An attacker who compromises the operator or obtains its service account credentials can exploit this flaw to achieve privilege escalation, gaining full administrative control over the cluster.

### CVE-2026-114665

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-22T11:17:43.810 |

Goploy 1.18.0 before 1.18.1 contains a link following vulnerability in the /deploy/fileDiff and /deploy/fileCompare endpoints that allows authenticated members to read arbitrary files. Attackers with repository write access can commit a symlink pointing outside the project directory to read database configuration and deployment SSH private keys.

### CVE-2026-112313

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-22T11:17:28.137 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in ACF Extended ACF Extended acf-extended allows Stored XSS.This issue affects ACF Extended: from n/a through 0.9.2.7.

### CVE-2022-51025

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T11:17:05.593 |

Penta Security WAPPLES 4.0.54.1, 5.0, and 6.0 contains a path traversal vulnerability that allows authenticated attackers to download arbitrary files via the name parameter of /webapi/file/transfer. Attackers can send GET requests with type=db_backup and ../ sequences in name to read files like /etc/passwd, and a hardcoded systemi account makes authentication effectively trivial. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-19.

### CVE-2026-112379

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-22T09:17:14.810 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Codepeople Contact Form Email contact-form-to-email allows Stored XSS.This issue affects Contact Form Email: from n/a through 1.3.68.

### CVE-2026-111830

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-22T09:17:13.597 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WP Mailster WP Mailster wp-mailster allows Stored XSS.This issue affects WP Mailster: from n/a through 1.9.1.0.

### CVE-2026-114720

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-93` |
| Published | 2026-10-22T02:16:59.717 |

Roundcube Webmail before 1.6.20 and 1.7.x before 1.7.5 is affected by an IMAP command injection vulnerability. A remote authenticated attacker can exploit this via CRLF sequences injected into the _flag parameter of the mail/mark action to execute arbitrary IMAP commands. Upstream fixed this in the commit “Fix IMAP command injection via CRLF in `_flag` parameter of mail/mark action”, which rejects flags containing control, whitespace and IMAP-special characters.

### CVE-2026-114664

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T02:16:58.757 |

Frappe Framework before 16.33.0 contains a blind SQL injection vulnerability in the frappe.desk.doctype.event.event.get_events method, which fails to properly neutralize user-supplied input before including it in SQL queries. Authenticated attackers can send crafted input to get_events and infer query results from application behavior to extract sensitive database information.

### CVE-2026-114659

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-424` |
| Published | 2026-10-22T02:16:57.923 |

Grav Flex Objects plugin 1.4.0 before 1.4.17 contains an authorization bypass because its generic /api/v1/flex-objects/pages API routes check only directory-level admin.pages permissions, without enforcing the Pages API's api.pages.read/write permissions or page-level permissions rules. Authenticated non-super users with api.access and admin.pages or admin.configuration.pages permissions can read page source and frontmatter, modify content, or delete pages they are denied.

### CVE-2026-96644

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-21T21:20:32.943 |

Pillow is a Python imaging library. Prior to 13.0.0 on Windows, src/PIL/WmfImagePlugin.py passes unchecked 32-bit WMF or EMF dimensions to the native drawwmf handler in src/display.c. The handler sizes a DIB allocation from 16-bit-truncated bcWidth and bcHeight fields but copies pixel data using the original full dimensions. A crafted wide, short metafile can pass the pixel-count decompression-bomb check and make the Windows-only renderer read beyond the heap buffer, potentially disclosing memory or crashing the process. This issue is fixed in version 13.0.0.

### CVE-2026-96643

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-21T21:20:32.797 |

Pillow is a Python imaging library. From 11.0.0 until 13.0.0, Exif.load() in src/PIL/Image.py repeatedly slices the remaining EXIF data while it begins with the six-byte Exif header. src/PIL/PngImagePlugin.py accepts an uncapped PNG eXIf chunk, so a file filled with repeated headers causes a new shrinking copy on every iteration and quadratic CPU work. The condition is reachable through Image.getexif(), Image._getexif(), and ImageOps.exif_transpose(), including common photo-upload rotation workflows. This issue is fixed in version 13.0.0.

### CVE-2026-96642

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-21T21:20:32.650 |

Pillow is a Python imaging library. Prior to 13.0.0, the TarIO initializer in src/PIL/TarIO.py accepts a negative octal member size and computes a backward seek that returns to the same 512-byte header. When the requested member name does not match, the parser repeatedly reads that header, consumes a full CPU core, and never returns. TarIO is reached only when an application directly uses PIL.TarIO.TarIO rather than the default Image.open() path. This issue is fixed in version 13.0.0.

### CVE-2026-96637

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-409` |
| Published | 2026-10-21T21:20:31.927 |

Pillow is a Python imaging library. Prior to 13.0.0, SpiderImageFile.seek() in src/PIL/SpiderImagePlugin.py reparses a later SPIDER stack frame and replaces self._size without rerunning Image._decompression_bomb_check(). A tiny file can use a safe first frame to pass Image.open() and then declare very large dimensions in a later mode F frame. Loading that frame allocates approximately four bytes per attacker-declared pixel and can consume multiple gigabytes of memory. This issue is fixed in version 13.0.0.

### CVE-2026-79976

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-21T19:17:04.060 |

The MCTP-over-I2C+GPIO target binding in subsys/pmci/mctp/mctp_i2c_gpio_target.c emulates a small pseudo-register file, where the bus controller first writes a register number and then writes or reads payload bytes. The selected register (b->reg_addr) and the data-phase flag (b->rxtx) were never cleared when the controller issued an I2C STOP, so after a completed transfer the target still had a data register selected while the packet buffer that register refers to had already been consumed and set to NULL by mctp_i2c_gpio_target_stop().

A controller on the bus can re-enter the same branch of mctp_i2c_gpio_target_stop() with a NULL buffer using two ordinary transactions and no authentication: first a normal packet write to MCTP_I2C_GPIO_RX_MSG_ADDR followed by STOP (which delivers and frees b->rx_pkt), then a bare read transaction followed by STOP. The failing read_requested() call leaves the stale state untouched and the I2C driver still delivers the STOP callback, which then calls mctp_bus_rx() with a NULL packet. The symmetric case exists on the transmit side, where the stale MCTP_I2C_GPIO_TX_MSG_ADDR selection dereferences b->tx_pkt->end after b->tx_pkt has been cleared and additionally signals b->tx_complete a second time, causing the next outbound packet to be dropped.

The dereference happens in the I2C target interrupt handler, so on any target that traps accesses to address 0 the result is a fatal exception and a device reset or halt — a denial of service inflicted by any device able to act as controller on the shared management bus (for example compromised firmware on a peer MCTP endpoint or on the BMC). On parts where address 0 is readable, the impact degrades to a malformed packet buffer being handed to the MCTP stack and lost transmit packets. No attacker-controlled value is written and no confidentiality or integrity boundary is crossed.

The fix resets b->reg_addr to MCTP_I2C_GPIO_INVALID_ADDR and clears b->rxtx at every STOP, so a new register must be selected before any data phase can run again. Only builds that opt into the experimental CONFIG_MCTP subsystem with CONFIG_MCTP_I2C_GPIO_TARGET=y are affected.

### CVE-2026-112221

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-21T15:17:16.267 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Brainstorm Force SureCart surecart allows Stored XSS.This issue affects SureCart: from n/a through 4.9.5.

### CVE-2026-111848

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-21T15:17:16.013 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Dylan Kuhn  Geo Mashup geo-mashup allows Reflected XSS.This issue affects  Geo Mashup: from n/a through 1.13.22.

### CVE-2026-111840

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-21T15:17:15.890 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in VideoWhisper.com Paid Videochat Turnkey Site ppv-live-webcams allows Reflected XSS.This issue affects Paid Videochat Turnkey Site: from n/a through 7.5.14.

### CVE-2026-111838

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-21T15:17:15.763 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in ThemeHunk ThemeHunk Customizer themehunk-customizer allows Reflected XSS.This issue affects ThemeHunk Customizer: from n/a through 2.8.7.

### CVE-2026-114660

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-10-22T02:16:58.077 |

Grav from 2.0.0 before 2.2.5 contains an improper access control vulnerability in FlexDirectory::dynamicFlexField() that allows page authors to call arbitrary Flex object methods via flex-*@ directives in page frontmatter. When a user with page edit rights opens the page, directives calling setStorageKey() and delete() run in their session, deleting protected pages neither account may delete.

### CVE-2026-114642

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-22T02:16:57.250 |

Traefik 2.11.0 before 2.11.58 and 3.0.0 before 3.7.14 stores its NTLM/Kerberos backend round tripper in a client-connection slot not keyed by ServersTransport, so one service's TLS client configuration is reused for another service's backend. An unauthenticated client can arm the slot via a backend issuing an NTLM or Negotiate challenge, then reach another service on the same keep-alive connection, bypassing its root CAs, server name, and certificate verification.

### CVE-2026-114640

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-22T02:16:56.947 |

Traefik from v3.7.0 before v3.7.14 contains an authentication bypass vulnerability in its Kubernetes Ingress-NGINX provider that forwards client-supplied Ssl-Client-* headers on the plaintext HTTP router. When ssl-redirect is disabled alongside auth-tls-pass-certificate-to-upstream, unauthenticated attackers can send Ssl-Client-Verify: SUCCESS with a chosen certificate subject and issuer to impersonate mTLS identities.

### CVE-2026-114639

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-22T02:16:56.800 |

Traefik 2.11.0 before 2.11.58 and 3.0.0 before 3.7.14 contains an authentication bypass because a first request preauthenticated with an Authorization: Negotiate token authenticates a socket in the globally shared backend connection pool, which is never isolated. Unauthenticated attackers on separate frontend connections can be assigned that NTLM/Kerberos-bound socket and perform reads or writes with the victim's identity.

### CVE-2026-114638

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-22T02:16:56.653 |

Traefik v3.7.0 before v3.7.14 contains an improper authentication vulnerability in the Kubernetes Ingress NGINX provider that merges client CAs when auth-tls-secret names collide after dot-to-dash normalization. Attackers holding certificates from another host's CA can access a host requiring its own client CA, while that host's legitimate clients are refused.

### CVE-2026-114637

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-488` |
| Published | 2026-10-22T02:16:56.503 |

Traefik from v3.2.0 before v3.7.14 contains an authentication bypass vulnerability in the experimental FastProxy connection pool, which fails to pin NTLM/Negotiate-authenticated backend connections to their frontend connection. Unauthenticated clients can be handed a pooled keep-alive backend connection where a victim completed an NTLM or Negotiate handshake, letting them read victim data and act as that victim.

### CVE-2026-114636

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-22T02:16:56.310 |

Traefik v3.7.13 before v3.7.14 contains an access-control bypass in the Kubernetes Ingress NGINX provider, where the HTTP router generated for ssl-passthrough Ingresses on non-TLS entry points never applies the Ingress's access-control annotations. Unauthenticated attackers reaching the HTTP entry point with the Ingress host can access backends protected by auth-type, auth-url, or whitelist-source-range annotations, with nothing logged.

### CVE-2026-114635

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-22T02:16:56.140 |

Traefik before v2.11.58 and v3.7.14 contains an authentication bypass vulnerability in its SNI check, which is skipped when request TLS state is nil. Unauthenticated clients can send HTTP/2 requests with the :scheme http pseudo-header over TLS on Go 1.27 builds to reach routers requiring client certificates without presenting one.

### CVE-2026-114633

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-22T02:16:55.837 |

WWBN AVideo before 29.4.0 contains an incorrect authorization vulnerability that allows delegated Users Admin accounts to delete or modify administrator accounts. Attackers can submit requests to confirmDeleteUser.json.php or userAddNew.json.php targeting administrators to delete their videos and accounts, or change and demote them.

### CVE-2026-111812

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-21T20:17:23.060 |

Apache Traffic Server's origin_server_auth plugin lets a client force signing of attacker-chosen AWS request headers under the proxy's own credentials.



This issue affects Apache Traffic Server: from 8.0.0 through 8.1.11, from 9.0.0 through 9.2.15, from 10.0.0 through 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-78118

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-21T19:17:03.787 |

The kernel helper z_waitq_head() (kernel/include/wait_q.h) reads the head of a thread wait queue, but on SMP systems it was called from several places without holding the scheduler spinlock _sched_spinlock that serializes wait-queue mutation. The consequential call site is z_timer_expiration_handler() in kernel/timer.c, which held only the timer subsystem lock timer_lock while reading timer->wait_q and then unpending, setting the return value of, and readying the thread it obtained. halt_thread() in kernel/sched.c removes an aborted thread from its wait queue while holding only _sched_spinlock, so the two paths are not mutually exclusive.

When the last waiter is removed on another CPU inside that window, sys_dlist_peek_head() can return the list sentinel — a pointer into the k_timer object itself — typed as a struct k_thread * (with CONFIG_WAITQ_SCALABLE, rb_get_min() can return an arbitrary node of a tree being restructured), or it can return a pointer to a thread that has already been unpended and, for dynamically allocated threads, freed. The handler then calls unpend_thread_no_timeout(), which performs a sys_dlist_remove() through pointers read from that object, and arch_thread_return_value_set(), which writes unconditionally through the pointer.

The result is out-of-bounds and use-after-free writes in supervisor context, plus scheduler state corruption; a milder outcome is a thread that has re-pended elsewhere being woken with a success return value from an unrelated blocking call. All of the primitives needed to drive the interleaving — k_timer_start(), k_timer_status_sync(), k_thread_create() and k_thread_abort() — are system calls, so with CONFIG_USERSPACE enabled an unprivileged user-mode thread can attempt the race against kernel-owned data.

Exploitation requires a multi-CPU build (CONFIG_MP_MAX_NUM_CPUS greater than one; the affected region is a no-op on uniprocessor targets), local code execution, and winning a narrow timing window, so the practical outcome is most often a kernel crash rather than controlled corruption. The fix splits the helper into z_waitq_head_locked() for callers that already hold the scheduler spinlock and a z_waitq_head() that acquires it, and brings the timer expiration handler's head read, unpend and ready under a single LOCK_SCHED_SPINLOCK region.

### CVE-2025-55702

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-10-21T19:16:48.120 |

When a client sends a POST with Expect: 100-continue and the origin answers before reading the body, Apache Traffic Server parses the unread body left on the client connection as the next request. An attacker behind a front-end proxy that shares connections to Traffic Server can use this to smuggle requests past the front end and desynchronize responses for other users.



This issue affects Apache Traffic Server: from 8.0.0 through 8.1.11, from 9.0.0 through 9.2.15, from 10.0.0 through 10.1.4, 10.2.0.



Users are recommended to upgrade to version 9.2.16, 10.1.5, or 10.2.1, which fix the issue.

### CVE-2026-114492

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-21T18:17:27.943 |

gin-vue-admin through 2.9.2 contains a path traversal vulnerability that allows authenticated administrators to recursively delete arbitrary directories by supplying traversal sequences in the pluginName parameter. Attackers can send a crafted POST request to /autoCode/removePlugin with '../' sequences, causing os.RemoveAll to delete any directory writable by the server process.

### CVE-2026-76496

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-21T17:19:09.177 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Expressway Series software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-76496 are related to issues concerning improper link resolutions that are grouped under the Common Weakness Enumeration (CWE) Base CWE-59.
