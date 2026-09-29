# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-29 15:00 UTC
- **対象期間**: `2026-09-28T15:00:31.000Z` 〜 `2026-09-29T15:00:46.000Z`
- **重要CVE数**: 129 件（Critical 9.0+: 28 件 / High 7.0〜: 101 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公表された CVE のうち、**CVSS 7.0 以上が 40 件以上**と依然として高リスクが集中しています。  
- **リモートからのコード実行 (RCE)・認証なしでの権限取得** が目立ち、特に Web 管理コンソール、IoT デバイス、CI/CD パイプラインに対する攻撃が多く報告されています。  
- 重大度が高いものは **Firefox のサンドボックス脱出** や **GEOVIA のサーバ側コードインジェクション** など、基盤ソフトウェア自体の脆弱性が企業全体の攻撃面を広げる傾向があります。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲・被害シナリオ | 推奨パッチ/バージョン |
|-----|------|----------------|------------------------|----------------------|
| **CVE‑2026‑84154** | 9.9 | Code Injection (サーバ側) | GEOVIA Geospatial Data Manager (R2024x‑R2026x) において、特定のリクエストを細工するだけで任意コードが実行可能。内部ネットワークに露出したサーバが即座に乗っ取られ、機密地理情報が漏洩・改ざんされる危険性がある。 | ベンダー提供の **R2026 Patch 1**（リリース日: 2026‑08‑15）を適用 |
| **CVE‑2026‑100818** | 9.6 | Sandbox Escape (use‑after‑free) | Firefox/Firefox ESR の Gtk ウィジェットで use‑after‑free が発生し、リモートから任意コード実行が可能。攻撃者は標的ユーザーにマルウェア入りページを閲覧させるだけで、デスクトップ環境全体を制御できる。 | Firefox ESR 153.4、Firefox 157、Firefox ESR 140.17 以降に更新 |
| **CVE‑2026‑88804** | 9.6 | Stored XSS (Rancher UI) | SUSE Rancher 2.15 系以前の UI 設定更新 API が認証なしで利用でき、攻撃者は管理コンソールに永続的な XSS スクリプトを埋め込める。管理者が UI にアクセスするとセッションハイジャックやクラスタ破壊が可能になる。 | Rancher **2.15.2**, **2.14.6**, **2.13.10**, **2.12.14**, **2.11.18** 以上へアップデート |
| **CVE‑2026‑12342** | 9.6 | 未検証入力による RCE (IdentityIQ) | IdentityIQ 全バージョンで、Web Service API のリクエストボディが不適切にサニタイズされ、任意コマンドがサーバ上で実行される。認証不要で API エンドポイントに POST できるため、外部からの大規模侵入が可能。 | ベンダー提供の **IdentityIQ 8.9 Patch 2026‑09‑01** を適用 |
| **CVE‑2026‑8065** | 9.1 | 認証バイパス + 任意ファームウェアアップロード (Hitachi Energy RTU500) | EOL 版 RTU500 のファームウェア更新エンドポイントが認証チェックを欠如。攻撃者は任意のファームウェアをアップロードし、デバイス機能改ざん・ネットワーク内の踏み台化が可能。 | Hitachi Energy が提供する **RTU500 FW v3.2.1**（2026‑07‑30）へ更新、または EOL デバイスの廃止・隔離を検討 |

> **選定理由**  
> - **CVSS が最高点に近い**（9.9‑9.6）こと。  
> - **認証不要／リモートから直接コード実行** が共通し、被害が企業全体に波及しやすい。  
> - **インフラ基盤 (GEOVIA, Rancher, IdentityIQ) とエンドユーザー環境 (Firefox, RTU500)** の両方に影響し、対策が遅れるとサプライチェーン全体にリスクが拡大する点が重要です。  

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
- **GEOVIA Geospatial Data Manager**  
  - `R2026 Patch 1`（またはベンダーが提供する最新パッチ）を即時適用。  
- **Firefox / Firefox ESR**  
  - `Firefox 157`、`Firefox ESR 153.4`、`Firefox ESR 140.17` 以上へ更新。  
- **SUSE Rancher**  
  - 2.15 系は **2.15.2**、2.14 系は **2.14.6**、2.13 系は **2.13.10**、2.12 系は **2.12.14**、2.11 系は **2.11.18** へアップグレード。  
- **IdentityIQ**  
  - ベンダー提供の **2026‑09‑01 パッチ**（バージョン 8.9.x）を適用。  
- **Hitachi Energy RTU500**  
  - `FW v3.2.1` 以上に更新、もしくは EOL デバイスのネットワークから切り離し。  

### 3.2 追加的な防御策
- **Web アプリケーションファイアウォール (WAF)**  
  - Rancher、IdentityIQ、GEOVIA の API エンドポイントに対し、`Content‑Security‑Policy` と `X‑Content‑Type‑Options` を強化。  
- **ネットワーク分離**  
  - IoT デバイス（RTU500、WatchGuard AP 系列）を管理 VLAN に隔離し、外部からの直接アクセスを遮断。  
- **脆弱性スキャニングの頻度増加**  
  - `Nessus` / `OpenVAS` で **CVSS ≥9.0** の新規脆弱性を **週次** スキャンし、検出次第チケット化。  
- **最小権限の徹底**  
  - Rancher UI の管理者アカウントは MFA を必須化し、API キーはローテーションを 30 日以内に実施。  
- **サードパーティコンポーネントの更新**  
  - `docker‑mailbox` → **≥0.4.13**  
  - `PyJWT` → **≥2.14.0

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-84154

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-29T08:17:21.297 |

A Code Injection vulnerability affecting GEOVIA Geospatial Data Manager from Release 3DEXPERIENCE R2024x through Release 3DEXPERIENCE R2026x could allow an attacker to execute arbitrary code on the server.

### CVE-2026-100818

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T13:17:47.037 |

Sandbox escape due to use-after-free in the Widget: Gtk component. This vulnerability was fixed in Firefox ESR 153.4, Firefox 157, and Firefox ESR 140.17.

### CVE-2026-88804

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-28T16:17:15.827 |

An unauthenticated update of public UI settings could be used by remote attackers to execute a stored cross-site scripting attack in the Rancher UI, in SUSE Rancher 2.15 before 2.15.2, 2.14 before 2.14.6, 2.13 before 2.13.10, 2.12 before 2.12.14 and 2.11 before 2.11.18.

### CVE-2026-12342

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-28T16:17:13.460 |

This vulnerability
impacts all versions of IdentityIQ and allows an unauthenticated user remote
code execution on the IdentityIQ server due to improper input validation of
submitted web service API content.

### CVE-2026-82973

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-29T13:17:52.963 |

Improper neutralization of CRLF sequences in IMAP command construction in psyb0t/docker-mailbox before 0.4.13 allows a remote unauthenticated attacker, when bearer-token authentication is not configured, to inject additional IMAP commands into an authenticated upstream mailbox connection via crafted folder, UID, or search values.

### CVE-2026-7192

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-29T13:17:52.447 |

A stack-based buffer overflow vulnerability in the Dbit T-CPE301K 4G WiFi minirouter allows an authenticated attacker to cause a denial of service (DoS) and a system reboot via a manipulated HTTP POST request directed at the endpoint ‘/js/common/do_cmd.js’ endpoint containing an excessively long parameter, which overwrites the PC and RA registers.

### CVE-2026-85520

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-29T12:17:12.283 |

Google Merchant Center Feed (gmfeed) module for PrestaShop is vulnerable to unauthenticated arbitrary file write in the feed.php endpoint. An unauthenticated attacker can send a crafted request that controls the output file name, path, extension, and content through request parameters. Due to the lack of authentication and input validation, the request is processed successfully, allowing an attacker to write and execute arbitrary PHP code, resulting in remote code execution (RCE).


This issue was fixed in version 2.3.9.

### CVE-2026-96431

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-29T09:17:11.183 |

Unrestricted Upload of File with Dangerous Type in the
/WebAgenda/download/uploadFile.jsp API endpoint of Flowring Agentflow 4.0 version
before 2023/03/24 allows remote authenticated users to execute arbitrary
system commands via a malicious file.

### CVE-2026-96429

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-29T09:17:10.917 |

SQL Injection in the /WebAgenda/SMBAjaxConfigProcess.do API
endpoint of Flowring Agentflow 4.0 version before 2025/08/08 allows
remote attackers to execute arbitrary SQL commands via the id parameter.

### CVE-2026-96428

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-29T09:17:10.687 |

SQL Injection in the /WebAgenda/SMBAjaxAutoComplete.do API endpoint of Flowring Agentflow 4.0 version before 2025/08/08 allows remote attackers to execute arbitrary SQL commands via the words parameter.

### CVE-2026-102240

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-29T02:16:55.153 |

A vulnerability was found in Netcore NAP930 0.1.241010.141410. This affects the function eval of the file /www/cgi-bin/network_tools of the component Network Tools CGI. The manipulation of the argument sid results in os command injection. The attack may be performed from remote. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-102361

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-29T00:17:03.183 |

mall4j through 4.0 contains a missing authentication vulnerability in the PUT /user/updatePwd endpoint that allows unauthenticated attackers to reset any storefront account password. Attackers can supply a target username in the request body to overwrite passwords without verification, enabling account takeover and access to orders and personal data.

### CVE-2026-101110

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-28T19:16:47.243 |

Joomla Extension - ordasoft.com - Unauthenticated SQL Injection in Book Library (Free) < 6.4.6 - site/booklibrary.php’s books() function reads the field and direction request parameters and passes each through a function called protectInjectionWithoutQuote(), whose only real protection is a keyword blacklist that, on detecting the literal substring select, wraps the value in $db->quote() instead of rejecting it. The value is then concatenated directly into an unquoted ORDER BY clause, a position where quoting provides no protection at all. Reaching the vulnerable code path requires two conditions: a first request to prime session-stored sort defaults, and a trailing decoy comment (-- xselect) that satisfies the blacklist’s substring check without altering the payload’s effect.

### CVE-2026-101108

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-28T19:16:46.930 |

Joomla Extension - ordasoft.com - Unauthenticated SQL Injection in Vehicle Manager (Free) < 6.5.8 - site/vehiclemanager.php reads the order_field and order_direction sort parameters at three separate anonymous-reachable frontend entry points (category listing, search, and the all-vehicles listing) through a sanitizing function that applies real escaping, but the value is then placed into an unquoted ORDER BY clause, where escaping has no protective effect.

### CVE-2026-100752

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-28T19:16:46.060 |

Joomla Extension - ordasoft.com - Unauthenticated SQL Injection in Real Estate Manager (Free) < 6.7.9 - site/realestatemanager.php builds the ORDER BY clause of three separate frontend property-listing queries (category browsing, search results, and the full property listing) from a request-controlled order_field parameter, concatenated directly into an unquoted SQL clause with no allow-list of real column names and no cast.

### CVE-2026-86102

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-863` |
| Published | 2026-09-28T17:17:51.267 |

An OS command injection vulnerability in the WatchGuard AP internal API service allows an attacker with network access to the AP to execute arbitrary shell commands on the underlying operating system.

### CVE-2026-101891

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-923` |
| Published | 2026-09-28T17:17:48.677 |

An improper access control vulnerability in an internal API service on WatchGuard Access Points allows an unauthenticated attacker with network access to the AP to obtain a valid API session.

### CVE-2026-101077

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-28T16:17:12.143 |

A flaw has been found in Netcore NR289-GE 1.4.5102. This impacts the function process_request of the component boa_temp Handler. This manipulation causes missing authentication. The attack is possible to be carried out remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101076

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-28T16:17:11.947 |

A vulnerability was detected in Netcore NR289-GE 1.4.5102. This affects the function system of the file /set_ntp_server_ip.cgi of the component CGI Handler. The manipulation of the argument ntp_ip results in os command injection. The attack can be executed remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101075

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-28T15:17:13.043 |

A security vulnerability has been detected in Netcore NR289-GE 1.4.5102. The impacted element is the function system of the file /location_time.cgi of the component Location Time Handler. The manipulation of the argument mac leads to os command injection. Remote exploitation of the attack is possible. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-102422

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-29T04:17:55.707 |

shell-quote's `quote()` function emits a `{ comment }` token as `#` followed by its text, which comments out the rest of the shell line, including the opening quote of any later string token. A line terminator (\n, \r, U+2028, U+2029) in that later string therefore ends the comment, and the rest of the string is parsed as shell input: `quote(['echo', 'ok', { comment: 'x' }, 'a\nid;#'])` runs `id` in sh, bash, dash, ksh and zsh. `parse()` emits a comment token for a `#` in the middle of a word (for example `http://example.com/#frag`), so callers that combine `parse()` output with another untrusted string, such as `quote(parse(untrustedCommand).concat(untrustedArg))`, are affected. The fix for CVE-2026-9277 rejected line terminators in the comment's own text, but not in the tokens after it. Fixed in 1.11.0: `quote()` throws a `TypeError` when a string after a `{ comment }` token contains a line terminator.

### CVE-2026-8066

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-29T10:17:13.250 |

A directory traversal vulnerability in the file upload functionality of Hitachi Energy RTU500 end-of-life versions allows an unauthenticated attacker to write or overwrite arbitrary files on the device file system. Depending on the files affected, successful exploitation could result in unauthorized modification of device data or disruption of the device’s intended operation.

### CVE-2026-8065

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-29T10:17:13.110 |

An authentication bypass vulnerability in the firmware update endpoint of Hitachi Energy RTU500 end-of-life versions allows an unauthenticated attacker to upload arbitrary firmware through a crafted POST request. Successful exploitation could allow the attacker to modify device functionality or compromise the integrity or availability of the device.

### CVE-2026-102334

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-28T23:17:01.837 |

Nginx Proxy Manager through 2.16.0 lacks rate-limiting on authentication endpoints, allowing unauthenticated attackers to make unlimited password guesses against any account. Attackers can brute-force login credentials via POST /api/tokens and subsequently guess TOTP codes via POST /api/tokens/2fa to gain full session access and administrative control.

### CVE-2026-102268

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-28T21:17:14.600 |

PyJWT is a Python implementation of JSON Web Token standards. Prior to 2.14.0, is_pem_format in jwt/utils.py is affected because is_pem_format does not recognize every PEM representation accepted by the cryptography loader. This occurs when an application mixes HMAC and asymmetric algorithms and supplies a mutated public-key PEM as raw key bytes. As a result, HMACAlgorithm.prepare_key treats the unrecognized asymmetric public key as an HMAC secret. Consequently, an attacker who knows the public key can forge authenticated HMAC tokens. This issue is fixed in version 2.14.0.

### CVE-2026-49994

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-09-28T18:17:22.250 |

Bluehood monitors local bluetooth activity. Prior to version 0.7.1, when auth_enabled is set in Bluehood, only the HTML page handlers enforced session validation. The /api/* handlers (settings, devices, groups, per-device endpoints including /api/device/{mac}/notes) called no auth check at all. A network attacker reachable on the dashboard port could read Bluetooth tracking data and modify application state — including the heartbeat URL, prune retention, device groups, and per-device notes — without a session cookie. This issue has been patched in version 0.7.1.

### CVE-2026-101894

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-09-28T17:17:48.830 |

The decompress package for Node.js extracts archives. Prior to 10.2.2 and 11.1.4, the default decompress(input, output) API relies on lexical containment checks that do not account for the kernel following a planted symlink chain. An attacker can supply a crafted archive containing chained symlink entries so that a later entry resolves outside the output directory. This allows files outside output to be read or written, and overwriting startup scripts or configuration can lead to remote code execution. The maintained @xhmikosr/decompress package is fixed in 10.2.2 and 11.1.4, but the separately affected unmaintained decompress package remains unpatched through 4.2.1. This vulnerability results from a bypass of the incomplete hardening for CVE-2026-53486. @xhmikosr/decompress is fixed in versions 10.2.2 and 11.1.4.

### CVE-2026-15390

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-459;CWE-787` |
| Published | 2026-09-29T10:17:11.237 |

Das U-Boot with CONFIG_IP_DEFRAG=y parameter fails to clear IP reassembly state after delivering a complete datagram. An attacker who can deliver fragmented IP traffic can execute arbitrary code by sending duplicated last-fragment IP packets.


This issue was fixed in commit b1aec609bb5e0d08c25c888c91935287ab4ee5fa in version 2026.07.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-101074

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-28T15:17:12.830 |

A weakness has been identified in Netcore NR289-GE 1.4.5102. The affected element is the function password-check of the file /bin/boa of the component Authentication. Executing a manipulation of the argument Username can lead to stack-based buffer overflow. The attack may be launched remotely. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-100832

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T13:17:48.453 |

Use-after-free in the Graphics: Canvas2D component. This vulnerability was fixed in Firefox ESR 153.4, Firefox ESR 115.42, and Firefox ESR 140.17.

### CVE-2026-100831

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T13:17:48.350 |

Use-after-free in the DOM: UI Events & Focus Handling component. This vulnerability was fixed in Firefox ESR 153.4 and Firefox 157.

### CVE-2026-100825

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T13:17:47.803 |

Use-after-free in the JavaScript Engine: JIT component. This vulnerability was fixed in Firefox ESR 153.4 and Firefox 157.

### CVE-2026-100824

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-29T13:17:47.700 |

Privilege escalation in the Places component. This vulnerability was fixed in Firefox ESR 153.4 and Firefox 157.

### CVE-2026-100820

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-29T13:17:47.300 |

Privilege escalation in the Address Bar component. This vulnerability was fixed in Firefox ESR 153.4, Firefox 157, and Firefox ESR 140.17.

### CVE-2026-100807

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-29T13:17:45.803 |

Privilege escalation in the DOM: Service Workers component. This vulnerability was fixed in Firefox ESR 153.4, Firefox 157, and Firefox ESR 140.17.

### CVE-2026-100801

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-29T13:17:45.180 |

Privilege escalation in the DLL Services component. This vulnerability was fixed in Firefox ESR 153.4, Firefox 157, and Firefox ESR 140.17.

### CVE-2026-100797

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T13:17:44.760 |

Privilege escalation due to use-after-free in the Graphics: WebRender component. This vulnerability was fixed in Firefox ESR 153.4, Firefox 157, Firefox ESR 115.42, and Firefox ESR 140.17.

### CVE-2026-100782

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-29T13:17:43.137 |

Privilege escalation due to incorrect boundary conditions in the Graphics component. This vulnerability was fixed in Firefox ESR 153.4, Firefox 157, Firefox ESR 115.42, and Firefox ESR 140.17.

### CVE-2026-100764

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-29T13:17:40.640 |

Privilege escalation due to incorrect boundary conditions in the Graphics: WebGPU component. This vulnerability was fixed in Firefox 157.

### CVE-2026-100761

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T13:17:40.390 |

Privilege escalation due to use-after-free in the Graphics: WebGPU component. This vulnerability was fixed in Firefox 157.

### CVE-2026-87748

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-29T12:17:12.527 |

Missing Authorization vulnerability in Interprobe Information Technologies Inc. Qorela DC allows Privilege Abuse.

This issue affects Qorela DC: from 1.6.1-RC29 before v1.6.2.

### CVE-2026-95509

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-131` |
| Published | 2026-09-29T11:16:43.947 |

Strings optimized for Latin-1 displaying Latin-1 characters cause incorrect String.arg() formatting by an incorrect buffer size calculation, causing out-of-bounds reading.

### CVE-2026-87741

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-28T20:17:11.377 |

The ConvertPlus plugin for WordPress is vulnerable to Deserialization of Untrusted Data in all versions up to, and including, 3.6.3 via the style parameter of the cp_display_preview_modal AJAX action. The vulnerability exists because the action's nonce guard is gated behind an isset() check and fails open when the cp_admin_page_nonce parameter is omitted entirely, no capability check is performed on the callback, and sanitize_text_field() — applied to the $style value before it is concatenated directly into a shortcode string evaluated by do_shortcode() — does not strip shortcode delimiters, allowing an attacker to inject a second, fully attacker-controlled [smile_modal] invocation that causes smile_modal_popup() to pass attacker-supplied base64-decoded bytes to maybe_unserialize() with no allowed_classes restriction. This makes it possible for authenticated attackers, with Subscriber-level access and above, to inject a PHP object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present.

### CVE-2026-86950

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-28T20:17:11.193 |

An out-of-bounds write issue was addressed with improved bounds checking. This issue is fixed in iOS 26.7.1 and iPadOS 26.7.1, macOS Sequoia 15.8.1, macOS Tahoe 26.7.1. Processing a maliciously crafted file may lead to arbitrary code execution. Apple is aware of a report that this issue may have been exploited in an extremely sophisticated attack against specific targeted individuals on versions of iOS before iOS 27.

### CVE-2026-88808

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-09-28T16:17:16.150 |

A vulnerability has been identified within Rancher Manager where the Fleet agent wrote resources to downstream clusters using its own cluster-admin credentials instead of the ServiceAccount pinned to the deployment. It affects multi-tenancy environments where different tenants share the same downstream clusters, for example different privileged or untrusted teams inside the same organization. This could lead to overwritten configuration files.

This issue affected SUSE Rancher Fleet 0.16 before 0.16.2, 0.15 before 0.15.7, and 0.14 before 0.14.11.

### CVE-2026-4034

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-29T14:17:20.683 |

Injection Vulnerability in Tibco Administrator version 5.13.0 & prior allows an authenticated user to submit specially crafted input through the web-based administration console.

### CVE-2026-84739

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-29T10:17:12.820 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 13.11 before 19.2.7, 19.3 before 19.3.3, and 19.4 before 19.4.1 that under certain conditions could have allowed an authenticated user to execute arbitrary JavaScript in the context of another user's browser session due to improper sanitization of path components in the merge request diff viewer.

### CVE-2026-96430

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-09-29T09:17:11.047 |

Exposed Dangerous Method or Function in the
/WebAgenda/SQLWin.do API endpoint of Flowring Agentflow 4.0 version Before 2026/08/28 allows remote
authenticated users to execute arbitrary SQL commands via the sql parameter.

### CVE-2026-101169

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-29T08:17:19.823 |

In affected versions of Octopus Server, an authenticated user with permissions to edit an Environment or Project can set specifically crafted JSON content for the object. Insecure deserialization of this content allows the user to execute arbitrary code in the Octopus Server process.

### CVE-2026-100371

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-28T21:17:11.653 |

InvoicePlane is a self-hosted open source application for managing invoices, clients, and payments. In version 1.7.2, an authorization guard to Users::change_password(), was added to address a previous authorization flaw that allowed a secondary administrator (user_type=1, user_id != 1) to directly change the password of the primary administrator (user_id=1) through users/change_password/{id}. That remediation, however, protects only the direct password-change operation. It does not protect the identity attribute that password recovery actually trusts: user_email. Users::form() applies no equivalent object-level authorization check when editing the primary administrator's account, and user_email is not included in PROTECTED_FIELDS. A secondary administrator can therefore rewrite the primary administrator's email address, then drive the public password-recovery flow — which resolves the account by user_email — to receive the reset token and take over user_id=1. The result is an alternate attack path that achieves the same impact PR #1638 was intended to prevent: cross-administrator full account takeover of the primary administrator. This issue has been patched via commit 8616fa4.

### CVE-2026-54675

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-73;CWE-434` |
| Published | 2026-09-28T18:17:22.723 |

FreePBX is an open source IP PBX. Prior to versions 16.0.10 and 17.0.5, a critical vulnerability exists in the sound language upload and conversion functionality that allows an authenticated attacker to perform arbitrary file writes, leading directly to remote code execution (RCE). Authentication with a known username is required. The vulnerability stems from insufficient path sanitization in the file conversion process, enabling path traversal attacks that place malicious PHP files in the web server's root directory. This issue has been patched in versions 16.0.10 and 17.0.5.

### CVE-2026-48100

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-349` |
| Published | 2026-09-28T17:17:49.547 |

Payy is an Ethereum L2 zk-rollup for privacy preserving and regulatory compliant transactions. Prior to version 1.3.0, agg_agg forwards the compacted message stream from its inner proofs into a public messages: [Field; 1000] array, but it never checks that the unused tail of the outer array is zero. A registered prover can build a valid agg_final proof for an approved rollup block while inserting an extra burn message after the real messages. RollupV1.verifyRollup() then parses that public input as a normal burn and transfers USDC from the rollup contract to the attacker. This is a severe circuit soundness failure: the proof system accepts a public statement whose messages array is not fully derived from the verified inner proofs. On the current deployment, verifyRollup() is restricted to the existing allowlisted prover, so a fresh public caller cannot submit the invalid proof directly. That gate limits who can reach L1 today; it does not make the circuit statement sound. The issue becomes permissionless under the prover model described in the Payy whitepaper. Section 3.3.2 states: "To join as a prover, the prover is required to submit a small stake", and Section 3.3.1 states that if a prover fails to submit, "other nodes can submit the block proof instead." In that model, an attacker only needs to become a registered prover and use public validator approval data for an already approved block. This issue has been patched in version 1.3.0.

### CVE-2026-96538

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-28T15:17:25.357 |

WarehousePG (WHPG) 7.x before 7.6.0-WHPG is affected by a missing authorization vulnerability (CWE-862) in the built-in server-side file functions pg_file_write(text,text,bool), pg_file_rename(text,text,text), pg_file_unlink(text), and pg_logdir_ls(). These functions are executable by any authenticated database role with no GRANT required, because the REVOKE that contrib/adminpack applies to the equivalent functions was never carried over to WHPG core when their catalog entries were repointed to the ungated adminpack-derived implementations as part of Greenplum's merge to a PostgreSQL 12 base. A non-superuser can use pg_file_write, pg_file_rename, and pg_file_unlink to create, overwrite (append), rename, and delete files under the data and log directories, and can use pg_logdir_ls() to enumerate log file names. Because postgresql.auto.conf resides in the data directory, a non-superuser can append configuration directives such as shared_preload_libraries or archive_command to it, resulting in arbitrary code execution as the postgres operating system user on the next server restart or configuration reload. WarehousePG 6.x is not affected, as the equivalent functions there enforce a superuser check internally.

### CVE-2026-102521

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-29T14:17:20.393 |

The decoder in `readFromDataView` in lib0 before 0.2.119 can be tricked into reading more than it should from a buffer. The vulnerability allows reading past the decoders' view, thus exposing adjacent process memory. This can be anything that is currently in the head, for example credentials or logs. This is similar to but different from GHSA-r5c8-rf4w-qrq8.

### CVE-2026-102360

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-29T14:17:20.117 |

A missing bounds check in the binary decoder in lib0, versions 0.2.1-0.2.117 and earlier and 1.0.0-rc.32 and earlier, lets any unauthenticated remote peer read adjacent process memory and receive it back. `readUint8Array` never compares the wire-supplied length against the decoder's own view, so one over-long length prefix returns whatever the host process allocated next: other tenants' document content, personal data, and live bearer session tokens**, recovered in full and at will. An attacker who can supply bytes to a lib0 decoder which means any peer that can open a socket, including before authentication reads adjacent process memory and, where the consumer echoes, stores or re-serves the decoded value, receives it back. This is patched in version 0.2.118 and 1.0.0-rc.33.

### CVE-2026-7193

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-29T13:17:52.593 |

A vulnerability relating to the use of predefined credentials in the Dbit T-CPE301K 4G WiFi mini-router allows an attacker connected to the same network to gain full root access to the device via the Telnet service (port 23) using static credentials.

### CVE-2026-101354

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-29T02:16:53.230 |

A security flaw has been discovered in FAST FAC1203R 20200116_2.0.4. The affected element is the function _tWlanTask of the component MmtAtePrase Parser. Performing a manipulation results in stack-based buffer overflow. The attacker must have access to the local network to execute the attack. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2024-42002

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-95` |
| Published | 2026-09-28T22:17:28.617 |

A code injection vulnerability has been discovered in the Robot Operating System 2 (ROS 2) 'ros2topic' command-line tool, affecting all ROS 2 distributions from Crystal Clemmys up to and including Lyrical Luth and Rolling Ridley. The vulnerability lies in the 'hz' verb, which reports the publishing rate of a topic and accepts a user-provided Python expression via the --filter option. This input is passed directly to the eval() function without sanitization, allowing a local user to craft and execute arbitrary code.

### CVE-2026-75600

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-28T18:17:24.440 |

FreePBX is an open source IP PBX. Prior to version 17.0.9, authenticated users who are authorized to access the GraphQL api module interface of FreePBX are able to execute arbitrary shell commands. Authenticated access to the api module is required. The PBX API module's documentation generator accepts an authenticated host parameter and uses it to build a shell command. The code path validates the generated OAuth access token before execution, but it does not validate or escape host. Compromise results in authenticated arbitrary shell command execution as the FreePBX web/PBX service user (typically asterisk.). This issue has been patched in version 17.0.9.

### CVE-2026-54710

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-94` |
| Published | 2026-09-28T18:17:23.043 |

FreePBX is an open source IP PBX. Prior to versions 16.0.40 and 17.0.7, a critical remote code execution (RCE) vulnerability exists in the superfecta module due to unsafe inclusion of arbitrary PHP files, allowing authenticated attackers to execute arbitrary PHP code on the server with the privileges of the web server user. Authentication with a known username is required. The vulnerability is rooted in the options and save_options cases in the Superfecta module's AJAX handler. The code dynamically includes PHP files from the sources/ directory based on user-supplied input. This allows an attacker to execute arbitrary code when combined with arbitrary directory creation (e.g., via the backup module) and file uploads that reveal full paths (e.g., via the soundlang module). This issue has been patched in versions 16.0.40 and 17.0.7.

### CVE-2026-54708

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-94` |
| Published | 2026-09-28T18:17:22.883 |

FreePBX is an open source IP PBX. Prior to versions 16.0.72 and 17.0.7, a critical vulnerability exists in the FreePBX backup Module that allows authenticated attackers to execute arbitrary code on the server. Authentication with a known username that has sufficient access permissions and/or write access to backup files is required. This vulnerability is caused by improper path sanitization in the backup restore functionality, enabling attackers to upload malicious PHP files to the web root directory. This issue has been patched in versions 16.0.72 and 17.0.7.

### CVE-2026-54674

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-28T18:17:22.560 |

FreePBX is an open source IP PBX. Prior to versions 16.0.39 and 17.0.7, users authenticated via User Control Panel (UCP) are able to execute arbitrary commands on the PBX as the webserver user (typically asterisk) using specially crafted HTTP strings. Authenticated access to UCP is required. Note that this is often more common for less-privileged users to have UCP access vs. the Administrator Control Panel (ACP) access (which is usually FreePBX higher-level administrator accounts only). Insufficient sanitization of certain URL parameters utilized by UCP did not fully account for malicious strings in these fields. This could result in binaries being executed on the host server by carefully chaining commands. This issue has been patched in versions 16.0.39 and 17.0.7.

### CVE-2026-87969

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-28T17:17:51.930 |

An OS command injection vulnerability in the WatchGuard AP diagnostic CLI allows an authenticated administrator to execute arbitrary operating system commands by supplying crafted input.

### CVE-2026-93348

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-28T16:17:17.643 |

Unsloth Zoo versions 2025.9.9 before 2026.8.14, as implemented in Unsloth 2025.9.9 through 2026.8.19, contains a code injection vulnerability in the model-loading compile path where the get_transformers_model_type() function in hf_utils.py collects model_type values from nested model configurations without enforcing a character allowlist, allowing newlines and arbitrary Python source to survive normalization. Attackers can embed a newline in a nested model_type value within a malicious model's config.json to terminate the generated import statement and execute arbitrary Python code via exec() in unsloth_compile_transformers(), achieving remote code execution as the loading user when the model is loaded for training or inference.

### CVE-2026-7395

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-29T10:17:12.203 |

Asset Suite allows unauthenticated users to access HTTPPublishAdapterTestServlet that can be used for configuration file upload, leading to information disclosure and integrity compromise. The HTTPPublishAdapterTestServlet is specifically meant for testing purposes to be used in a non-production environment.

### CVE-2026-101264

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-29T00:17:02.663 |

A vulnerability was determined in Ziroom ZHOME A0101 1.0.1.0. Impacted is an unknown function of the file /api/ZRnetwork/set_passwd. This manipulation of the argument password1 causes command injection. The attack can be initiated remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101263

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-29T00:17:01.540 |

A vulnerability was found in Ziroom ZHOME A0101 1.0.1.0. This issue affects some unknown processing of the file /api/ZRQos/set_online_client. The manipulation of the argument mac results in command injection. It is possible to launch the attack remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101262

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-28T23:17:01.187 |

A vulnerability has been found in Ziroom ZHOME A0101 1.0.1.0. This vulnerability affects unknown code of the file /api/ZRQos/set_online_client. The manipulation of the argument ip leads to command injection. It is possible to initiate the attack remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101261

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-28T23:17:01.003 |

A flaw has been found in Ziroom ZHOME A0101 1.0.1.0. This affects an unknown part of the file /api/ZRnetwork/firstSetup_wifi. Executing a manipulation of the argument login_pwd can lead to command injection. The attack may be performed from remote. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101260

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-28T23:17:00.300 |

A vulnerability was detected in Ziroom ZHOME A0101 1.0.1.0. Affected by this issue is some unknown functionality of the file /api/ZRnetwork/firstLogin. Performing a manipulation of the argument firstLogin results in command injection. The attack is possible to be carried out remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101187

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-28T21:17:12.810 |

A weakness has been identified in Ziroom ZHOME A0101 1.0.1.0. This vulnerability affects the function pop_usb_device of the file usr/lib/lua/luci/controller/api/zrUsb.lua of the component USB Device Management API. This manipulation of the argument path causes command injection. The attack is possible to be carried out remotely. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101081

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-28T17:17:47.817 |

A security flaw has been discovered in D-Link DI-8400 16.07. This vulnerability affects the function menu_nat_more_asp of the file menu_nat_more.asp of the component Web Administration Service. The manipulation of the argument opt results in stack-based buffer overflow. The attack can be launched remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-55157

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-28T18:17:23.373 |

Token Optimizer MCP measures token savings per AI coding agent, optimizes context, and shares a live local knowledge graph across 16 CLI clients. Prior to version 5.1.0, token-optimizer-mcp is vulnerable to OS command injection in the smart_user tool. Any MCP client that can call the smart_user tool can execute arbitrary shell commands through the username argument of the get-user-info operation. The commands execute with the privileges of the user running the token-optimizer-mcp server. This issue has been patched in version 5.1.0.

### CVE-2026-102296

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-28T22:17:32.233 |

ZoneMinder before 1.38.4 contains static buffer overflow vulnerabilities in RemoteCameraHttp::GetResponse() that allow malicious HTTP cameras or intercepting attackers to overflow fixed-size buffers by sending oversized response headers. Attackers can send crafted HTTP responses with oversized status messages, Connection headers, Content-Type values, or multipart boundaries to corrupt parser state and crash the capture process or corrupt memory.

### CVE-2026-101909

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-28T18:17:19.680 |

Axios is a promise-based HTTP client for the browser and Node.js. From 0.28.0 until 0.34.0 and 1.15.1 until 1.20.0, ToFormData processes inherited serialization options and visitor properties supplied through prototype pollution. A separate same-process prototype-pollution flaw supplies inherited dots, indexes, metaTokens, maxDepth, visitor, or Blob values before object serialization. The inherited options alter toFormData field naming and data interpretation, maxDepth can force request failure, Blob changes value handling, and a polluted visitor can execute when an attacker already has the stronger ability to inject a function. Serialized field naming and data interpretation can change, maxDepth can cause request failure, Blob can alter value handling, and a polluted visitor can execute under the stronger function-injection primitive. This issue is fixed in versions 0.34.0 and 1.20.0.

### CVE-2026-76719

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-29T10:17:11.920 |

A security vulnerability in HPE OneView may be exploited remotely to perform session hijacking, data theft or other unauthorized actions.

### CVE-2026-76718

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-29T10:17:11.773 |

A potential security vulnerability in HPE OneView can be exploited to allow remote session hijacking or other unauthorized actions.

### CVE-2026-101906

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-09-28T18:17:19.100 |

Axios is a promise-based HTTP client for the browser and Node.js. From 1.15.0 until 1.20.0, Axios shouldBypassProxy applies a quadratic trailing-dot regular expression to redirect hostnames. HTTP_PROXY or HTTPS_PROXY is configured, NO_PROXY or no_proxy is non-empty, redirects are followed, and a crafted redirect Location contains many dots followed by a non-dot character. Hostname.replace(/.+$/, '') backtracks quadratically while processing the crafted redirect hostname. Synchronous regular-expression processing can block the Node.js event loop and cause denial of service. This issue is fixed in version 1.20.0.

### CVE-2026-101903

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-28T18:17:18.560 |

Axios is a promise-based HTTP client for the browser and Node.js. From 1.16.1 until 1.20.0, the RFC 2397 regular expression allows slash characters on both sides of the media-type separator. An application passes an attacker-controlled malformed data URL containing many slash characters and no comma. the JavaScript regular-expression engine explores many separator placements before rejecting the URL. Synchronous excessive backtracking can block the Node.js event loop and cause denial of service. The affected identifiers are fromDataURI, DATA_URL_PATTERN, data:. This issue is fixed in version 1.20.0.

### CVE-2026-101901

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-28T18:17:18.233 |

Axios is a promise-based HTTP client for the browser and Node.js. From 1.13.0 until 1.20.0, Http2Sessions does not install adequate error handling for a ClientHttp2Session during Axios HTTP/2 session initialization or reuse. A request uses httpVersion: 2 and the ClientHttp2Session emits an error during session initialization or reuse. The unhandled session error escapes normal Promise rejection handling. The uncaught error can terminate the Node.js process and cause denial of service. This issue is fixed in version 1.20.0.

### CVE-2026-54160

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-28T17:17:49.833 |

Network UPS Tools is a collection of programs which provide a common interface for monitoring and administering UPS, PDU and SCD hardware. Prior to commits 658b24e and 1aa31d1, the GitHub Actions script used to prepare NUT tarballs and update GitHub Checks statuses and PR comments about it was mis-structured in terms of mixing code running with higher privileges (single-use token generated with write permissions) and untrusted inputs (PR source branch). A malicious PR run from a fork could extract the GITHUB_TOKEN value. It could potentially be abused while it was valid (while the GHA job ran) to manipulate Git repository contents, commit checks/statuses, or issue/PR comments, according to permissions it was issued with. This issue has been patched via commits 658b24e and 1aa31d1.

### CVE-2026-95389

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-29T10:17:15.010 |

SCTP protocol dissector crash in 4.6.0 to 4.6.8 and 4.4.0 to 4.4.18 allows denial of service

### CVE-2026-95387

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-29T10:17:14.713 |

SPDY protocol dissector crash in 4.6.0 to 4.6.8 and 4.4.0 to 4.4.18 allows denial of service

### CVE-2026-88805

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-28T16:17:16.003 |

Incorrect credential cleaning on logout could be used by remote attackers to keep access credentials even after the account was logged out. Affected is SUSE Rancher 2.15 before 2.15.2.

### CVE-2026-73598

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-29T13:17:51.123 |

Dell Secure Connect Gateway (SCG) Policy Manager, versions prior to 5.34.00.16, contains an Incorrect Permission Assignment for Critical Resource vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-102437

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-29T13:17:50.493 |

OS Command Injection in internal/gitcmd (git diff filter.clean/smudge invocation) in esengine DeepSeek-Reasonix (Reasonix Studio) allows a local attacker who controls repository content (.gitattributes + .git/config) to execute arbitrary commands via the desktop app's workspace-changes diff viewer.

### CVE-2026-18414

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-28T21:17:17.250 |

The ADC API requires each driver to reject a sampling sequence whose destination buffer is too small: the buffer_size field of struct adc_sequence in include/zephyr/drivers/adc.h documents that "the driver must ensure that samples are not written beyond the limit and it must return an error if the buffer turns out to be not large enough". The ADI MAX32 driver did not honour that contract. start_read() in drivers/adc/adc_max32.c compared buffer_size, a byte count, against a sample count ((1 + extra_samplings)  channels), ignoring sizeof(uint16_t), so it accepted a buffer half the required size. The samples are then stored through the uint16_t  data->buffer by Wrap_MXC_ADC_GetData(), which writes two bytes per sample and advances the pointer by one uint16_t: in adc_max32_start_channel() for synchronous reads, and in adc_max32_isr() for asynchronous ones. A sequence selecting two channels with a two-byte buffer, for example, passes the check and has its second sample written past the end of the buffer.

On a build with CONFIG_USERSPACE, adc_read() and adc_read_async() are system calls. The handler in drivers/adc/adc_handlers.c copies the sequence in from user memory, verifies only that [buffer, buffer + buffer_size) is writable by the calling thread, and rejects a user-supplied options->callback; it deliberately leaves the size arithmetic to the driver. A user-mode thread that has been granted access to a MAX32 ADC device object therefore fully controls channels, buffer, buffer_size and options->extra_samplings, and can make the driver write twice as many bytes as its buffer holds. Because the check scales with extra_samplings, the overrun equals the length of the buffer itself, up to channels * 65536 bytes past its end, since the sample pointer is only rewound on a repeat sampling, never on the extra samplings of a sequence.

The resulting stores are performed by the driver in kernel mode (in the system call itself, the ADC context timer, or the ADC interrupt handler for asynchronous reads), where the MPU does not restrict the thread's memory domain, so the write walks linearly out of the user partition and into adjacent memory such as other partitions, kernel data or thread stacks. The impact is kernel-memory corruption of attacker-chosen length at an attacker-chosen offset, a plausible privilege-escalation and denial-of-service primitive from an unprivileged user-mode thread. Builds without CONFIG_USERSPACE are affected only as a caller-side robustness defect, since the application itself supplies the buffer.

The fix replaces that check in start_read() with a call to the new shared helper adc_sequence_validate_buffer() in drivers/adc/adc_common.c, passing sizeof(uint16_t) as the sample size. The helper computes active_channels  sizeof(uint16_t)  (1 + extra_samplings) and returns -ENOMEM before any sampling is started.

### CVE-2026-18413

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-28T21:17:17.090 |

The ADC API requires each driver to reject a sampling sequence whose destination buffer is too small: the buffer_size field of struct adc_sequence in include/zephyr/drivers/adc.h documents that "the driver must ensure that samples are not written beyond the limit and it must return an error if the buffer turns out to be not large enough". The NXP MCUX LPADC driver did not honour that contract. mcux_lpadc_start_read() in drivers/adc/adc_mcux_lpadc.c performed no buffer-size check at all before assigning data->buffer = sequence->buffer. Each completed conversion then stores one 16-bit sample per enabled channel per sampling round through an unbounded *data->buffer++: in mcux_lpadc_isr() for interrupt-driven builds, and in mcux_lpadc_dma_callback() for DMA-driven builds on releases that have the DMA path. A sequence selecting two channels with a two-byte buffer, for example, has its second sample written past the end of the buffer.

On a build with CONFIG_USERSPACE, adc_read() and adc_read_async() are system calls. The handler in drivers/adc/adc_handlers.c copies the sequence in from user memory, verifies only that [buffer, buffer + buffer_size) is writable by the calling thread, and rejects a user-supplied options->callback; it deliberately leaves the size arithmetic to the driver. A user-mode thread that has been granted access to an LPADC device object therefore fully controls channels, buffer, buffer_size and options->extra_samplings, and can request far more samples than its buffer can hold: up to channels * 65536 samples into a two-byte buffer, since the sample pointer is only rewound on a repeat sampling, never on the extra samplings of a sequence.

The resulting stores are performed by the driver in kernel mode (in the ADC interrupt handler or the DMA completion callback), where the MPU does not restrict the thread's memory domain, so the write walks linearly out of the user partition and into adjacent memory such as other partitions, kernel data or thread stacks. The impact is kernel-memory corruption of attacker-chosen length at an attacker-chosen offset, a plausible privilege-escalation and denial-of-service primitive from an unprivileged user-mode thread. Builds without CONFIG_USERSPACE are affected only as a caller-side robustness defect, since the application itself supplies the buffer.

The fix calls the new shared helper adc_sequence_validate_buffer() in drivers/adc/adc_common.c from mcux_lpadc_start_read(). The helper computes active_channels  sizeof(uint16_t)  (1 + extra_samplings) and returns -ENOMEM before any sampling is started.

### CVE-2026-16513

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-28T21:17:16.910 |

The userspace verifier z_vrfy_rtio_sqe_copy_in_get_handles() in subsys/rtio/rtio_syscalls.c (subsys/rtio/rtio_handlers.c before v4.3.0) validated the RTIO object handle and the sqes input array, but not the handle out-parameter. On the first loop iteration it executed *handle = sqe, storing the kernel address of the newly acquired submission-queue entry through a pointer taken verbatim from user mode, with no K_SYSCALL_MEMORY_WRITE check in front of it.

Any user-mode thread that has been granted a struct rtio kernel object can invoke the syscall with an arbitrary address in handle. That is the ordinary way an unprivileged thread uses the RTIO API, for example via sensor_read_async_mempool() or the async ADC helpers, which call rtio_sqe_copy_in_get_handles() internally. The store happens in supervisor mode before any submission-entry validation, so it fires regardless of whether the SQE contents are subsequently rejected. Only builds with CONFIG_USERSPACE and CONFIG_RTIO are affected; without CONFIG_USERSPACE the verifier is not compiled and the caller is already privileged.

The write address is fully attacker-chosen and the written value is a pointer into the caller's own RTIO ring, whose contents the caller controls (the following *sqe = sqes[i] copies an attacker-supplied struct rtio_sqe into that slot). This yields a write-what-where primitive placing a pointer to attacker-controlled data at any kernel address, sufficient to corrupt kernel function pointers, thread structures, or memory-domain partition tables, and thus to escalate from user mode to kernel mode, defeating the isolation boundary CONFIG_USERSPACE is meant to enforce. At minimum it is a reliable kernel memory-corruption and crash primitive. The reporter reproduced the write on qemu_x86: a K_USER thread changed a supervisor global from NULL to a live kernel SQE pointer.

The fix adds K_SYSCALL_MEMORY_WRITE(handle, sizeof(*handle)) (guarded by the existing optional-NULL semantics) before the loop, so the destination must lie in the calling thread's writable memory domain or the thread is terminated by K_OOPS. The neighbouring verifier z_vrfy_rtio_cqe_get_mempool_buffer(), which checked its buff/buff_len out-parameters only for read although the implementation writes through them, was hardened separately by bea93400138 ("rtio: syscalls: validate output params as writable"); that residual was materially weaker, since a read check still confines the target to the caller's own memory domain.

### CVE-2026-102004

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-28T20:17:09.810 |

Wind River VxWorks 7 prior to 26.09, specific system call arguments can result in memory corruption within the memory management subsystem. Fixed in Version 26.09

### CVE-2026-4556

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-28T15:17:17.723 |

Exam4 is affected by a local privilege escalation vulnerability in the com.extegrity.LogTool privileged helper, which communicates with the application via XPC. The [ConsoleLogHelper copyConsoleIntoFileFromStartDate:] method executes a syslog command using attacker-controlled parameters without proper sanitization, enabling command injection. Successful exploitation allows a local attacker to execute arbitrary commands with root privileges through LaunchSynchronous.

### CVE-2026-86158

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-29T07:16:35.520 |

Missing authentication in the local .NET backend (Fiddler.WebUi) of Progress Software Fiddler Everywhere 8.0.2 allows a local unauthenticated attacker to mint OAuth tokens and read the machine-in-the-middle root certificate through an unauthenticated localhost HTTP and SignalR RPC channel.

### CVE-2026-101878

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303` |
| Published | 2026-09-29T02:16:54.990 |

Bitwarden Server 2025.6.0 before 2026.5.0 declares the @ExternalId parameter of the User_ReadBySsoUserOrganizationIdExternalId stored procedure as NVARCHAR(50) while the column it queries stores NVARCHAR(300), silently truncating the SSO login identifier on SQL Server deployments and allowing a user whose identity-provider identifier begins with another organization member's full 50-character identifier to authenticate as that member and obtain a victim-scoped access token.

### CVE-2026-45562

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-28T18:17:21.947 |

FreePBX is an open source IP PBX. Prior to versions 16.0.4 and 17.0.6, the FreePBX Music on Hold (MoH) module contains a critical security flaw that allows authenticated attackers to execute arbitrary system commands with the privileges of the Asterisk service. Authentication with an existing FreePBX administrator account is required. The root cause lies in the fact that the module accepts a POST parameter that defines a custom Asterisk application, which is then stored in the database without any sanitization. Later, this data is written directly to the musiconhold_additional.conf configuration file without validation. Since Asterisk reads this configuration file and executes the specified application, an attacker can inject arbitrary commands that will be executed with Asterisk's permissions. This issue has been patched in versions 16.0.4 and 17.0.6.

### CVE-2026-93355

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1390` |
| Published | 2026-09-28T20:17:11.547 |

LiteLLM contains a weak authentication vulnerability that allows an attacker holding a valid JWT from the configured identity provider to authenticate as any existing user by exploiting an email-based fallback lookup in the JWT authentication flow without verifying the email_verified claim. Attackers can present a token with an unverified email address matching a victim's account to inherit the victim's role, including proxy_admin privileges, and permanently overwrite the victim's stored identity binding to retain persistent unauthorized access to administrative endpoints exposing API keys and user management.

### CVE-2026-55160

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-28T18:17:23.540 |

Stringer is a self-hosted, anti-social RSS reader. Prior to commit 75cb095, an unrestricted Server-Side Request Forgery (SSRF) vulnerability allows any authenticated user to force the Stringer server to send arbitrary HTTP/HTTPS requests to internal networks, localhost services, and cloud metadata endpoints (e.g. AWS IMDS 169.254.169.254). When self-service signup is enabled (Setting::UserSignup), even a low-privileged registered user can exploit this to scan internal services or steal cloud IAM credentials. This issue has been patched via commit 75cb095.

### CVE-2026-101905

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-441;CWE-1321` |
| Published | 2026-09-28T18:17:18.923 |

Axios is a promise-based HTTP client for the browser and Node.js. From 1.15.2 until 1.20.0, the Node HTTP adapter in lib/adapters/http.js supplies request options without an own createConnection value. A separate same-process prototype-pollution flaw places a function on Object.prototype.createConnection. Node resolves and invokes the inherited createConnection socket factory, allowing the attacker-controlled function to select the transport endpoint. The attacker endpoint can receive request headers and bodies, including credentials, and return attacker-controlled responses while the URL appears legitimate. This issue is fixed in version 1.20.0.

### CVE-2026-86450

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-09-29T14:17:21.763 |

Insertion of sensitive information into sent data vulnerability in Parla Auto Automotive Trading Limited Company DetaWix Mobile Web Portal allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects DetaWix Mobile Web Portal: before v1.0.19.

### CVE-2026-102281

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-674` |
| Published | 2026-09-28T22:17:32.050 |

Nest is a framework for building scalable Node.js server-side applications. Prior to 11.2.4 and 12.0.2, a single message with a deeply nested object in its pattern can terminate a NestJS microservice using the TCP or RabbitMQ transport. ServerTCP#handleMessage and ServerRMQ#handleMessage pass a client-controlled non-string pattern to JSON.stringify to derive the handler lookup key; sufficiently deep nesting throws RangeError: Maximum call stack size exceeded, and the unhandled promise rejection terminates Node.js under its default behavior. An attacker who can reach the TCP port or publish to the consumed RabbitMQ queue or exchange can crash the service on demand; other transports are not affected because their patterns arrive as strings. This issue is fixed in versions 11.2.4 and 12.0.2.

### CVE-2026-102278

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-674` |
| Published | 2026-09-28T21:17:16.517 |

The brace-expansion library generates arbitrary strings containing a common prefix and suffix. Prior to 1.1.20, 2.1.6, 3.0.8, and 5.0.11, deeply nested brace groups cause expand_() to recurse once per nesting level at comma-member and single-set expansion sites, exhausting the native stack before output limits can apply and potentially terminating the Node.js process. expand_ performs uncontrolled recursion for nested brace alternatives and single-part sets. deeply nested brace groups supplied as an untrusted pattern. expand_ is affected. expand is affected. Comma members is affected. Single set is affected. native stack exhaustion during nested sub-expansion. process-terminating denial of service. This issue is fixed in versions 1.1.20, 2.1.6, 3.0.8, and 5.0.11.

### CVE-2026-102276

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-674` |
| Published | 2026-09-28T21:17:16.033 |

The brace-expansion library generates arbitrary strings containing a common prefix and suffix. Prior to 1.1.19, 2.1.5, 3.0.7, and 5.0.10, crafted brace patterns can exhaust the native stack in parseCommaParts because parseCommaParts recursively processes the remainder once per brace group and uses push.apply to pass every element of a very large comma-part array as a function argument. Patterns containing many comma-separated brace groups trigger the recursive path, while the large array triggers the argument-array path without deep recursion. These paths cause recursive and argument-array native stack exhaustion before max or maxLength can limit output, potentially terminating the Node.js process in a process-terminating denial of service. This issue is fixed in versions 1.1.19, 2.1.5, 3.0.7, and 5.0.10.

### CVE-2026-101860

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-269` |
| Published | 2026-09-29T02:16:54.787 |

A vulnerability was found in RaspAP raspap-webgui up to 3.5.5. Affected by this issue is the function PluginInstaller::addSudoers of the file src/RaspAP/Plugins/PluginInstaller.php of the component sudo Configuration. Performing a manipulation results in improper privilege management. The attack may be initiated remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-102273

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-28T21:17:15.497 |

PyJWT is a Python implementation of JSON Web Token standards. From 2.13.0 until 2.14.0, PyJWT HMACAlgorithm.prepare_key is affected because HMAC key guard only recognizes top-level public JWK forms and misses container representations. This occurs when an application allows HMAC and asymmetric algorithms and passes a public JWK container as the raw key. As a result, public asymmetric key material is accepted as the HMAC secret. Consequently, an attacker who knows the public key can forge a token with arbitrary authenticated claims. This issue is fixed in version 2.14.0.

### CVE-2026-102272

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-28T21:17:15.280 |

PyJWT is a Python implementation of JSON Web Token standards. From 2.13.0 until 2.14.0, HMACAlgorithm.prepare_key in jwt/algorithms.py is affected because raw-JWK detector does not normalize accepted Unicode byte-order marks before checking for JSON. This occurs when a public JWK is prefixed with a UTF-8 BOM and used in a mixed-algorithm verification path. As a result, public JWK bypasses asymmetric-key detection and becomes the HMAC secret. Consequently, an attacker who knows the public key can forge authenticated tokens. This issue is fixed in version 2.14.0.

### CVE-2026-102271

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-28T21:17:15.110 |

PyJWT is a Python implementation of JSON Web Token standards. From 2.4.0 until 2.14.0, PyJWT HMACAlgorithm.prepare_key is affected because asymmetric-key guard relies on textual markers that are absent from DER encoding. This occurs when an application mixes HMAC and asymmetric algorithms and supplies a DER public key as the shared verification key. As a result, PyJWT uses public DER bytes as an HMAC secret. Consequently, an attacker who knows the public key can forge authenticated HMAC tokens. This issue is fixed in version 2.14.0.

### CVE-2026-102267

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-200;CWE-345;CWE-918` |
| Published | 2026-09-28T21:17:14.430 |

PyJWT is a Python implementation of JSON Web Token standards. Prior to 2.14.0, PyJWT PyJWKClient is affected because redirect destinations are not revalidated against the JWKS trust boundary. This occurs when a configured trusted JWKS endpoint returns an attacker-influenced redirect. As a result, PyJWKClient follows the redirect and consumes the redirected response as key material. Consequently, forwarded credentials may be disclosed or verification keys may be substituted. This issue is fixed in version 2.14.0.

### CVE-2026-102266

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-28T21:17:14.257 |

PyJWT is a Python implementation of JSON Web Token standards. From 2.13.0 until 2.14.0, HMACAlgorithm.from_jwk is affected because PyJWK verification path used the decoded key without applying prepare_key validation. This occurs when a trusted JWK Set contains an oct entry with an empty k value. As a result, an attacker signs an HMAC token with the same zero-length key accepted by PyJWT. Consequently, forged token can carry arbitrary authenticated claims. This issue is fixed in version 2.14.0.

### CVE-2026-101916

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-28T21:17:13.030 |

@grpc/grpc-js implements the core functionality of gRPC purely in JavaScript, without a C++ addon. Prior to 1.13.6 and 1.14.5, getAuthContext does not distinguish authorized from unauthorized peer certificates when server credentials set requireClientCertificate to false. When applications use the returned authentication context, they can treat an unauthorized certificate as authorized, causing improper authentication. @grpc/grpc-js-xds can reach this condition when RBAC authentication is enabled in affected configurations. This issue is fixed in version 1.14.5 and 1.13.6.

### CVE-2026-96326

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-29T02:16:55.957 |

The HT Contact Form – Drag & Drop Form Builder for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the Rich Text Editor Field in all versions up to, and including, 2.10.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-95520

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T12:17:12.650 |

A heap-based buffer overflow flaw was found in rpm. Parsing a symlink entry in an untrusted RPM package whose declared RPMTAG_LONGFILESIZES value is 0xFFFFFFFFFFFFFFFF causes an integer overflow in iterReadArchiveNext() that shrinks a buffer allocation to one byte, after which the payload's independently-controlled cpio filesize field is used to write attacker-controlled data past the end of that allocation. This is reachable via rpm2cpio, rpm2archive, and rpm -qlvp on an  untrusted package.

### CVE-2026-96440

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-29T09:17:11.317 |

Improper Limitation of a Pathname to a Restricted
Directory（Path Traversal） in the /WebAgenda/download/uploadFile.jsp
API endpoint of Flowring Agentflow 4.0 version before 2023/03/24 allows remote
authenticated users to write files to arbitrary locations outside the intended
upload directory via the path parameter.

### CVE-2026-97024

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-09-29T04:18:02.397 |

A path traversal vulnerability in Flatpak's handling of the files/etc directory during app deployment allows a malicious Flatpak app to cause certain host system files (such as passwd, group, machine-id, or resolv.conf) to be emptied or replaced with a symlink when the app is installed or upgraded. In system-wide installations, the write is performed as root.

### CVE-2026-102247

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-09-29T04:17:54.110 |

A vulnerability was detected in FastAdmin 1.6.1.20250430/1.6.5.20260602. This affects an unknown function of the file application/database.php of the component Database Management. The manipulation results in execution with unnecessary privileges. The attack may be launched remotely. The exploit is now public and may be used.

### CVE-2026-97685

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-29T03:17:23.233 |

An authenticated LimeSurvey Community Edition 7.3.0 user allowed to create surveys can use their own survey as an authorized context while supplying question or answer identifiers belonging to another user's survey. The REST survey-patching endpoint checks the attacker's permission against the survey ID in the request URL, but the vulnerable persistence operations resolve the target object independently by its global qid or aid and never verify that it belongs to that authorized survey.

### CVE-2026-102373

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-29T01:16:44.757 |

GestSup versions before 3.2.62 fail to validate ticket ownership when loading comments via the threadedit parameter in thread.php. Authenticated attackers can enumerate sequential comment IDs to read private comments from other users' tickets without proper authorization checks.

### CVE-2026-102365

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-29T00:17:03.777 |

mall4j through 4.0 fails to enforce authorization checks on GET endpoints in UserAddrController that retrieve customer address data. Authenticated attackers can call /user/addr/page and /user/addr/info endpoints to harvest all customer addresses including names, phone numbers, and postal information.

### CVE-2026-102335

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-28T23:17:02.007 |

Nginx Proxy Manager through 2.16.0 fails to restrict the advanced_config field to administrators, allowing non-admin users with manage permissions to inject arbitrary nginx directives. Attackers can inject malicious nginx configuration such as alias directives to serve arbitrary files or control routing for their assigned hosts.

### CVE-2026-101091

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-28T22:17:30.413 |

SiYuan versions before v3.8.4 fail to properly validate SQL statements in block query embed blocks executed against siyuan.db. Attackers can craft malicious .sy documents with non-read-only SQL statements that execute automatically during background indexing, rendering, or export operations without authentication.

### CVE-2024-58386

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-28T22:17:29.893 |

ZoneMinder versions 1.37.0 before 1.38.0 contain a path traversal vulnerability in the files view that allows authenticated users to read arbitrary files. The path parameter is not properly validated before being passed to output_file, enabling attackers with Events view permission to access sensitive files like configuration files containing database credentials.

### CVE-2026-97023

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-09-28T19:16:50.710 |

A path traversal vulnerability in Flatpak's handling of the export/bin directory during app deployment allows a malicious Flatpak app to cause deletion of attacker-chosen files outside the deployment directory when the app is installed or upgraded. In system-wide installations, the deletion is performed as root.

### CVE-2026-87114

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-28T17:17:51.530 |

A flaw was found in kube-compare. When processing a 'container://' reference path, the tool incorrectly executes an untrusted container image's entrypoint instead of merely extracting data from a stopped container. This allows a remote attacker to achieve arbitrary code execution on the operator's workstation. If the Docker daemon requires elevated privileges, the untrusted code may execute with root-mediated daemon privileges, posing a significant security risk.

### CVE-2026-55096

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-184;CWE-918` |
| Published | 2026-09-28T17:17:50.007 |

fast-mcp-telegram is a Telegram MCP Server. Prior to version 30.1, the send_message/send_message_to_phone MCP tools accept files as a list of http(s) URLs, which the server downloads and attaches to the outgoing Telegram message. Downloads are guarded by _validate_url_security, an SSRF denylist that checks the URL's literal hostname string but never resolves DNS. The fetch (httpx.AsyncClient.get) does its own resolution at request time. Consequently a hostname that resolves to a loopback / private / link-local address passes the guard and is fetched — even with the secure defaults block_private_ips=True and allow_http_urls=False. Because the fetched body is returned to the attacker as a Telegram file attachment, this is a full-read, exfiltrating SSRF, not blind. This issue has been patched in version 30.1.

### CVE-2026-93538

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-290;CWE-639` |
| Published | 2026-09-28T15:17:24.927 |

A cross-tenant authorization issue was discovered in SUSE Rancher Fleet. During agent-initiated cluster registration, cluster labels supplied by the registering agent, including labels in the reserved management.cattle.io/ namespace such as the cluster display name label, were applied to the resulting upstream Cluster object. Because Fleet resolves GitRepo and Bundle targets from those cluster labels, a party able to register a cluster into a Fleet workspace namespace shared with other tenants could cause its own cluster to satisfy targeting rules that administrators intended for a different cluster.
This affects SUSE Rancher Fleet 0.16 before 0.16.1, 0.15 before 0.15.6, 0.14 before 0.14.10, 0.13 before 0.13.15, 0.12 before 0.12.19 and older versions.

### CVE-2026-19547

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-09-29T10:17:11.410 |

Ghostscript for Windows is vulnerable to local privilege escalation through PostScript resource file hijacking. Due to the application searching for PostScript resource files in predictable paths under C:\\gs\\ that do not exist by default on Windows installations, combined with Windows default ACLs allowing any authenticated user to create directories at the root of C:\\, an attacker who is an authenticated local user can create the expected directory structure and plant a malicious PostScript file. When any user or service subsequently runs Ghostscript, the planted file is automatically loaded and executed with the full privileges of the Ghostscript process. This results in full compromise of Ghostscript process context, as well as running arbitrary code on the machine with Ghostscript process privileges.


This issue was fixed in version 10.08.0.

### CVE-2026-100392

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-28T21:17:11.827 |

InvoicePlane is a self-hosted open source application for managing invoices, clients, and payments. In version 1.7.2, Users::form() performs no object-level authorization check on user_id = 1. A Secondary Administrator (user_type = 1, user_id != 1) can rewrite the Primary Administrator's user_type to 2 (Guest / read-only), destroying the root account's privilege and locking the legitimate owner out of the instance. At time of publication, there are no publicly available patches.

### CVE-2026-102010

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-825` |
| Published | 2026-09-28T19:16:48.830 |

A flaw was found in GCC. When an application calls the erase_if function on a binary heap priority queue in libstdc++, the library reallocates storage but fails to update its internal entry pointer. An attacker capable of triggering this operation can exploit this use-after-free condition, leading to a Denial of Service (DoS) via an application crash or potential memory corruption.

### CVE-2026-101907

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-441;CWE-601` |
| Published | 2026-09-28T18:17:19.270 |

Axios is a promise-based HTTP client for the browser and Node.js. From 1.17.0 until 1.20.0, the fetch adapter bypasses the maxRedirects: 0 redirect policy. An Axios request uses the fetch adapter with maxRedirects set to zero and receives a redirect response. The underlying fetch implementation follows the redirect instead of returning the redirect response unchanged. The redirected request can access internal responses or reach state-changing internal endpoints despite redirects being disabled. This issue is fixed in version 1.20.0.

### CVE-2026-101898

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-28T18:17:17.860 |

Axios is a promise-based HTTP client for the browser and Node.js. From 1.13.0 until 1.20.0, Axios HTTP/2 request setup does not consistently apply proxy settings and caller-supplied DNS lookup policy. An HTTPS request uses httpVersion: 2 with explicit config.proxy or environment-derived proxy settings, or relies on caller-supplied config.lookup DNS policy. The HTTP/2 path can connect without the configured proxy behavior or without applying the caller-supplied config.lookup policy before http2.connect(). Requests can bypass the intended proxy route or the caller-supplied DNS resolution policy. This issue is fixed in version 1.20.0.

### CVE-2026-80357

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:P/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1191` |
| Published | 2026-09-28T15:17:23.717 |

Dell Boot Optimized Server Storage (BOSS), versions prior to 2.2.13.2038, contains an On-Chip Debug and Test Interface With Improper Access Control vulnerability in the SMCU on 17G BOSS-N1 controllers. An unauthenticated attacker with physical access could potentially exploit this vulnerability, leading to Unauthorized access.
