# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-16 15:00 UTC
- **対象期間**: `2026-11-15T15:00:44.000Z` 〜 `2026-11-16T15:00:24.000Z`
- **重要CVE数**: 52 件（Critical 9.0+: 7 件 / High 7.0〜: 45 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公表された CVE のうち **CVSS 7.0 以上が 30 件以上** と、深刻度の高い脆弱性が集中しています。  
- **リモートコード実行 (RCE)・OS コマンドインジェクション** が目立ち、特に 3DEXPERIENCE の *Station Launcher* に関する 3 件は認証不要でシステム全体を乗っ取れる **CVSS 9.9‑10.0** の極めて危険なものです。  
- 同時期に **PHP のリモート/ローカルファイルインクルード**、**認証バイパス**、**権限昇格** が多数報告され、Web アプリケーションやクラウドサービスでも攻撃対象が拡大しています。  
- 多くの脆弱性は **ベンダーがすでにパッチを提供** しているか、**メンテナンスが終了した製品**（例：Batflat CMS）であるため、**速やかなアップデートまたは代替策の検討が必須**です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 製品・コンポーネント | 主なリスク | 影響範囲・理由 |
|-----|------|----------------------|------------|----------------|
| **CVE‑2026‑93664** | 10.0 | 3DEXPERIENCE **Station Launcher** (R2023x‑R2026x) | 未認証リモートコード実行（デシリアライズ） | 最高評価の CVSS 10.0。攻撃者は任意のコードをサーバ上で実行でき、全社システムが即座に乗っ取られる危険性がある。 |
| **CVE‑2026‑77033** | 9.9 | 3DEXPERIENCE **Station Launcher** (R2023x‑R2026x) | OS コマンドインジェクション | 同製品内で別の攻撃経路（コマンドインジェクション）を提供。認証不要で任意コマンド実行が可能。 |
| **CVE‑2026‑19732** | 9.9 | 3DEXPERIENCE **Station Launcher** (R2023x‑R2026x) | OS コマンドインジェクション（別バリエーション） | 上記と同様の深刻度で、複数のエンドポイントが影響を受けるため、全体的なリスクが累積。 |
| **CVE‑2026‑125795** | 9.8 | Estatik **estatik** (≤ 4.3.6) | PHP Remote/Local File Inclusion | PHP の `include/require` に対する不適切なファイル名制御。攻撃者は任意のローカルファイルを読み取り、最悪 RCE に至る可能性。 |
| **CVE‑2026‑111559** | 9.3 | Batflat CMS 1.0‑1.5 (メンテナンス終了) | 任意 PHP コード実行 (Contact エンドポイント) | プロジェクトは既に非メンテナンスで修正が提供されていない。放置すると公開サーバが即座に乗っ取られる。 |

> **注**：上記 5 件は **CVSS ≥ 9.3** かつ **認証不要／低権限での攻撃が可能** という点で共通しており、組織全体のサイバーリスクを急激に高めます。

---

## 3. 推奨アクション  

### 3.1 3DEXPERIENCE Station Launcher (R2023x‑R2026x)  
| アクション | 詳細 |
|-----------|------|
| **バージョンアップ** | 可能であれば **R2027x 以降** へアップグレード。ベンダーが提供する **Security Patch KB‑2026‑93664 / KB‑2026‑77033 / KB‑2026‑19732** を適用。 |
| **ネットワーク分離** | Station Launcher が外部から直接アクセスできないよう、**内部 VLAN** または **WAF** で IP 制限を実装。 |
| **監査ログの強化** | `station-launcher.log` の **不審なシリアライズ/デシリアライズ操作** をリアルタイムで監視し、SIEM に送信。 |
| **バックアップとロールバック** | アップデート前に **データベース・設定ファイル** のフルバックアップを取得し、緊急時にロールバックできる手順を確立。 |

### 3.2 Estatik (WordPress プラグイン)  
| アクション | 詳細 |
|-----------|------|
| **アップデート** | **Estatik 4.3.7 以上** に更新。リリースノートで *Remote File Inclusion* 修正が明記されていることを確認。 |
| **プラグインの最小化** | 使用していないプラグインは **無効化・削除**。特に `estatik` 系以外のサードパーティプラグインが同様のインクルード脆弱性を持つケースが多い。 |
| **ファイルインクルード制御** | `php.ini` の `allow_url_include=0`、`open_basedir` を適切に設定し、外部ファイルのインクルードを防止。 |

### 3.3 Batflat CMS (非メンテナンス)  
| アクション | 詳細 |
|-----------|------|
| **即時移行** | 公式がメンテナンスを終了しているため、**代替 CMS**（例：WordPress, Grav, Hugo 等）への **データ移行** を計画。 |
| **WAF でのブロック** | `/contact` エンドポイントへの **POST** リクエストで `Content-Type: application/json` かつ **PHP コード文字列** が含まれる場合は **403** を返すルールを追加。 |
| **サーバ側の権限最小化** | `www-data` の権限を **最小限** にし、PHP の `disable_functions` に `exec, system, shell_exec, passthru` を追加。 |

### 3.4 Dell PowerStore (ストレージアプライアンス)  
| アクション | 詳細 |
|-----------|------|
| **ファームウェア更新** | Dell が提供する **PowerStore Firmware 4.5.0 以降**（または該当パッチ）を適用。 |
| **ロールベースアクセス制御 (RBAC)** | 低権限ユーザーに対して **管理者権限** が付与されないよう、**ロールの見直し** と **最小権限の原則** を徹底。 |
| **監査ログの有効化** | `auditd` で **権

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-93664

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-16T13:17:23.313 |

A Deserialization of Untrusted Data vulnerability affecting Station Launcher App in 3DEXPERIENCE platform from Release 3DEXPERIENCE R2023x through Release 3DEXPERIENCE R2026x could lead to an unauthenticated remote code execution.

### CVE-2026-77033

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-16T13:17:23.003 |

An OS Command Injection vulnerability affecting Station Launcher App in 3DEXPERIENCE platform from Release 3DEXPERIENCE R2023x through Release 3DEXPERIENCE R2026x could allow an attacker to execute arbitrary commands on the server.

### CVE-2026-19732

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-16T13:17:22.843 |

An OS Command Injection vulnerability affecting Station Launcher App in 3DEXPERIENCE platform from Release 3DEXPERIENCE R2023x through Release 3DEXPERIENCE R2026x could allow an attacker to execute arbitrary commands on the server.

### CVE-2026-125795

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-15T15:16:47.163 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Estatik Estatik estatik allows PHP Local File Inclusion.This issue affects Estatik: from n/a through 4.3.6.

### CVE-2026-111559

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-16T13:17:18.683 |

Batflat CMS does not sanitize data passed to the /contact endpoint. A remote unauthenticated attacker can send a POST request with a crafted message, causing arbitrary PHP code execution with www-data user privileges.


The project is no longer maintained and the issue has not been fixed.

### CVE-2026-129552

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1394` |
| Published | 2026-11-16T12:17:53.337 |

Tensei through 0.11.5 contains an authentication bypass vulnerability in @tensei/auth that falls back to the hard-coded JWT signing key 'auth-secret-key' when JWT_SECRET is unset. Unauthenticated attackers can sign tokens with arbitrary user ids accepted by populateContextFromToken to impersonate any user, including administrators.

### CVE-2026-129550

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-16T12:17:53.033 |

Tensei through 0.11.5 contains a privilege escalation vulnerability in @tensei/auth that allows unauthenticated or authenticated users to assign themselves arbitrary roles via the exposed User Roles field. Attackers can supply a roles array during registration, a POST to the users route, or a PATCH to their own record to gain administrator permissions.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-82156

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-16T04:16:44.230 |

Dell PowerStore contains an authorization-bypass vulnerability. A low-privileged attacker could exploit it, potentially leading to elevation of privilege to administrator.

### CVE-2026-129547

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-16T12:17:52.550 |

Kalmia through 0.2.0 contains an authentication bypass vulnerability in RsPressMiddleware that allows unauthenticated attackers to access private documentation by supplying any non-empty viewToken cookie. Attackers can send requests with a forged viewToken cookie, which is never validated as a JWT, to read all pages and assets of RequireAuth documentation sites.

### CVE-2026-129545

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-16T12:17:52.203 |

Kalmia through 0.2.0 contains a privilege escalation vulnerability that allows low-privileged authenticated users to modify any account via the /kal-api/auth/user/edit endpoint. Attackers holding only read permission can set their admin flag and 'all' permission or reset an administrator's password to fully take over the instance.

### CVE-2026-129540

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-16T02:17:12.100 |

VoAPI 1.0.0 through 1.2.0 contains a sql injection vulnerability that allows authenticated users to inject SQL by supplying crafted column names as search[...] filter keys on list endpoints such as GET /api/log. Attackers can read the HS256 JWT signing secret from the option table and forge a manager role token to take over the /api/m/* management API.

### CVE-2026-129494

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-16T01:17:20.053 |

CloudPaste 1.1.0 through 1.9.1 contains an information disclosure vulnerability that allows unauthenticated attackers to obtain WebDAV storage credentials through the unauthenticated /api/proxy/link endpoint. Attackers who know a public share slug can retrieve the Basic Authorization header containing the WebDAV username and password, then read, modify, or delete files on the WebDAV server.

### CVE-2026-129493

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-16T01:17:19.897 |

Bolo (bolo-solo) 1.7 through 2.6.4 contains an information disclosure vulnerability that allows unauthenticated attackers to read article view passwords via the public GET /articles endpoint. Attackers can retrieve the plaintext articleViewPwd field returned by ArticleProcessor.getArticlesByPage and submit it to read password-protected article content.

### CVE-2026-21176

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-11-16T12:17:58.733 |

Unquoted search path or element in Samsung Device Care prior to version 4.0.80 allows local attackers to execute arbitrary code.

### CVE-2026-21175

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-16T12:17:58.607 |

Incorrect permission assignment for critical resource in Samsung Update prior to version 3.0.111.0 allows local attackers to execute arbitrary code.

### CVE-2026-21167

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-16T12:17:57.577 |

Binding to an unrestricted IP address in Smart Switch prior to version 3.7.74.7 allows adjacent attackers to bypass authentication. User interaction is required for triggering this vulnerability.

### CVE-2026-116288

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-16T12:17:43.347 |

In affected versions of Octopus Server, a user with permission to edit team scoped roles could escalate their privileges to deploy to projects and environments that they were not authorised to so.

### CVE-2026-15707

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-16T12:17:53.653 |

An uncontrolled search path vulnerability (CWE-427) in statically linked OpenSSL libraries within Netskope Client (stAgentSvc.exe) and Endpoint DLP (epdlp.exe) on Windows allows an authenticated local attacker to execute arbitrary code with elevated SYSTEM privileges. The services retain internal build-time paths referencing a secondary drive location. On Windows systems where default volume permissions allow standard users to create root-level directories on secondary drives, an attacker can place a malicious configuration file (openssl.cnf) that is loaded under the NT AUTHORITY\SYSTEM context upon service startup or system reboot. Under default operating system permissions, macOS and Linux are not susceptible, and mobile platforms are unaffected.

### CVE-2026-129784

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-16T11:16:45.537 |

The httpx Ruby gem parses JSON response bodies through its transcoder layer. HTTPX::Response#json delegates to Transcoder::JSON.decode, and when the oj gem is loaded and multi_json is absent, the decoder falls back to json_load, which calls Oj.load(response.to_s) with no mode option. Oj.load defaults to :object mode, in which a response document can allocate any already-loaded Ruby class ("^o":"ClassName") and set its instance variables, or resolve a class or module reference ("^c":"Name"). An attacker who controls, or can influence, the URL an application fetches with HTTPX.get(url).json therefore controls object instantiation in the victim process. With a matching gadget chain, this issue can potentially cause remote code execution. Affects httpx 1.9.0; fixed in 1.9.1.

### CVE-2026-21151

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-16T12:17:55.627 |

Improper privilege management in TransitionPlayer prior to SMR Nov-2026 Release 1 allows local privileged attackers to execute arbitrary code with launcher privilege.

### CVE-2026-129690

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-257` |
| Published | 2026-11-16T14:17:07.197 |

The
vulnerability enables any attacker with admin access to dump credentials of all
accounts stored on the device, which can then be reused for lateral movement or
further compromise. Since
passwords are stored or processed in a recoverable format, this represents a
critical failure in secure credential handling.

### CVE-2026-105925

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:U/V:X/RE:X/U:Green` |
| Weaknesses | `CWE-776` |
| Published | 2026-11-16T08:16:48.180 |

A denial of service vulnerability in the Qt QXmlSimpleReader class of the Qt 5 Core Compatibility APIs module (Qt 6) and the Qt XML module (Qt 5).

### CVE-2026-129091

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-15T19:17:16.730 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Mikado-Themes GrandPrix Core grandprix-core allows PHP Local File Inclusion.This issue affects GrandPrix Core: from n/a through 1.0.

### CVE-2026-102448

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-16T10:16:45.307 |

A vulnerability has been identified in Rexroth IndraWorks. This flaw allows an attacker to execute arbitrary code on the user’s system by parsing a manipulated file, because the file parser fails to properly sanitize the path name(s) or references embedded in the manipulated file. Exploitation requires user interaction, specifically opening a specially crafted file, which then causes the application to traverse outside the target directory and to write files in unauthorized locations, eventually enabling Remote Code Execution (RCE). This can lead to a complete compromise of the system running Rexroth IndraWorks.

### CVE-2026-129703

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-613` |
| Published | 2026-11-16T09:17:13.293 |

In the vulnerability-lookup web application, the authentication decorators for feed-key requests (auth_feedkey_func in website/decorators.py) and API-key requests (auth_func in website/web/api/v1/common.py) called Flask-Login's login_user() function. This caused the HTTP response to a request authenticated solely by a feed key (supplied as the X-FEED-KEY URL parameter) or an API key (supplied as the X-API-KEY header) to set a session cookie that grants full authenticated access to every page in the application, without requiring a password or two-factor authentication.

The practical impact is that any party possessing a leaked feed URL (a common occurrence, as feed URLs are shared with RSS readers) or an API key could obtain a valid web session for the associated account. This session provides access to the user's account page, which exposes the API key and other profile data, and for accounts with the administrator role, access to the /admin interface, enabling full administrative control of the application.

The vulnerability affects all users whose feed key or API key is exposed. No prior authentication, user interaction, or special network conditions are required; a single HTTP request with the token is sufficient to establish the session. The session persists until it expires, and because it is not bound to the original credential (a related CWE-613 issue noted by the developers), revoking the feed key or API key does not invalidate the already-created session.

The fix replaces the login_user() call with assignment to g._login_user, which Flask-Login's current_user property reads for the current request only, without writing any session cookie. The affected views remain unchanged and continue to see the authenticated user for the single request.

### CVE-2026-128835

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-16T14:17:06.413 |

@fastify/busboy is a streaming parser for multipart form data used by Fastify. In versions 1.0.0 through 3.2.5, a multipart part whose header block is never terminated before the next boundary is counted by the vendored Dicer parser as an open part that never ends, so the parser emits neither a finish nor an error event and the request hangs. A single unauthenticated request of roughly one hundred bytes triggers the stall, and through @fastify/multipart the hung handler is not released when the client disconnects, so repeated requests leak handlers and whatever resources they hold, such as files, database connections and concurrency slots, until the process is restarted. The same parser is reached by the formData methods of undici versions 5.25.3 through 6.7.0. The issue is fixed in @fastify/busboy 3.2.6, and users should upgrade to 3.2.6 or later. As a workaround, configure Fastify's handler timeout so hung handlers are eventually terminated and their resources released.

### CVE-2026-124724

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-754` |
| Published | 2026-11-16T14:17:06.113 |

@fastify/busboy is a streaming parser for multipart form data used by Fastify. In versions 1.0.0 through 3.2.5, when a request reaches the configured limit on the number of multipart parts, each further part is skipped without attaching an error listener to the skipped part stream. If the request body ends in the middle of such a skipped part, the vendored Dicer parser emits an error on that stream, and because nothing is listening Node.js raises an unhandled error event and the process exits. A single crafted unauthenticated request is therefore enough to crash the server. The bug is latent in the parser on its own and was first demonstrated through @fastify/multipart versions 10.1.2 through 10.1.4, which keep feeding the request body to the parser after a limit error, and it affects any consumer that sets a finite parts limit and parses request bodies that can be terminated early. The issue is fixed in @fastify/busboy 3.2.6, and users should upgrade to 3.2.6 or later. There is no complete application level workaround because the crash happens inside the parser before application code runs, though consumers that set a finite parts limit should also attach an error listener to the parser stream.

### CVE-2026-124289

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-843` |
| Published | 2026-11-16T14:17:05.990 |

@fastify/multipart is the official Fastify plugin for handling multipart/form-data uploads. In versions 7.4.0 through 10.1.8, when the plugin is registered with the attachFieldsToBody option, the saveRequestFiles helper treats any object in the parsed request body that carries truthy file and buffer properties as an uploaded file. An unauthenticated client can forge such an object through a plain JSON request or a JSON-typed multipart field, so attacker-chosen bytes are written to the temporary directory while upload hooks and the file count and size limits are skipped, and the saved entry keeps the attacker's filename verbatim instead of being reduced to its basename. Because that filename can contain parent directory segments, applications that use it as a write destination, as the project README example does, are exposed to an arbitrary relative-path file write from a single request. The issue is fixed in @fastify/multipart 10.1.9, and users should upgrade to 10.1.9 or later. As a workaround, call saveRequestFiles only after confirming the request is multipart, and reduce each returned filename to its basename or validate it against an allowlist before using it as a destination.

### CVE-2026-110710

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-459;CWE-772` |
| Published | 2026-11-16T13:17:18.527 |

@fastify/multipart is the official Fastify plugin for handling multipart/form-data uploads. In versions 3.0.0 through 10.1.3, temporary files written by the saveRequestFiles helper are removed only by a response hook that runs when the response finishes or errors. When a client completes an upload and then disconnects before the handler writes the reply, for example while the handler scans, hashes or forwards the file, the response only emits a close event, the cleanup hook never runs, and the saved files are left on disk. An unauthenticated client can repeat this cheaply to exhaust disk space and deny service to applications that save uploaded files to disk. The issue is fixed in @fastify/multipart 10.1.4, and users should upgrade to 10.1.4 or later. As a workaround, avoid saving request files for untrusted clients, or clean the saved files from a close handler on the raw response so removal also happens when the client disconnects.

### CVE-2026-125823

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-15T19:17:16.273 |

Allocation of Resources Without Limits or Throttling vulnerability in Jegstudio Gutenverse gutenverse allows HTTP DoS.This issue affects Gutenverse: from n/a through 4.2.2.

### CVE-2026-125799

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-538` |
| Published | 2026-11-15T15:16:47.317 |

Insertion of Sensitive Information into Externally-Accessible File or Directory vulnerability in Looks Awesome Flow-Flow Social Stream flow-flow-social-streams allows Retrieve Embedded Sensitive Data.This issue affects Flow-Flow Social Stream: from n/a through 5.0.5.

### CVE-2026-21153

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-16T12:17:55.883 |

Stack-based buffer overflow in libsecuibc.so prior to SMR Nov-2026 Release 1 allows local attackers to execute arbitrary code.

### CVE-2026-67250

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-16T12:17:59.303 |

A local privilege escalation (LPE) vulnerability in Pebble’s installers could allow a local attacker with low privilege access to place a malicious Dynamic Link Library (DLL) where a privileged executable file will load it.

### CVE-2026-63245

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-16T11:16:46.710 |

A local privilege escalation (LPE) vulnerability in the Audigy Rx driver’s Emupia2k.sys file could allow a local attacker with low privilege access to gain higher privileges, such as administrator rights.

### CVE-2026-124672

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-16T09:17:13.160 |

The Burst Statistics WordPress plugin before 3.7.5 does not verify that a request is actually being routed to its own REST API before unloading every other active plugin for that request, allowing unauthenticated attackers to have requests processed with other plugins' protections (such as REST access restrictions, hidden login pages and two-factor authentication) switched off, and to cause other plugins' scheduled tasks to be discarded.

### CVE-2026-125771

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-15T15:16:46.890 |

Incorrect Privilege Assignment vulnerability in AtlasAiDev MCP Server for WordPress ai-workflow-automation-ai-agent-hub allows Privilege Escalation.This issue affects MCP Server for WordPress: from n/a through 2.0.3.

### CVE-2026-129546

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-16T12:17:52.383 |

Kalmia through 0.2.0 contains an information disclosure vulnerability that allows authenticated read-only users to retrieve Git deployment credentials via documentation API responses. Attackers can query GET /kal-api/docs/documentations or POST /kal-api/docs/documentation to obtain plaintext gitUser and gitPassword values and authenticate to external Git repositories.

### CVE-2026-129606

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-16T06:16:49.183 |

Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') vulnerability in Samsung Open Source mTower allows Overflow Buffers.

### CVE-2026-129539

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-16T02:17:11.940 |

SSCMS 7.2.0 through 7.4.0 contains an arbitrary file read vulnerability that allows any registered user-center account to copy server files by supplying source paths to the layerImageUpload endpoint. Attackers can send siteId 0 with crafted filePaths entries to copy configuration files into their public sitefiles/home upload directory and download them anonymously.

### CVE-2026-125830

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T19:17:16.580 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Belingo belingoGeo belingogeo allows Reflected XSS.This issue affects belingoGeo: from n/a through 1.13.3.

### CVE-2026-125822

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T19:17:16.123 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Nickboss WordPress File Upload wp-file-upload allows Stored XSS.This issue affects WordPress File Upload: from n/a through 5.2.3.

### CVE-2026-125818

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T19:17:15.850 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in AdvancedCoding wpDiscuz wpdiscuz allows Stored XSS.This issue affects wpDiscuz: from n/a through 7.6.75.

### CVE-2026-125817

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T19:17:15.703 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Themeisle Feedzy feedzy-rss-feeds allows Stored XSS.This issue affects Feedzy: from n/a through 5.2.15.

### CVE-2026-125804

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T19:17:15.557 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Meow Apps AI Engine ai-engine allows Stored XSS.This issue affects AI Engine: from n/a through 3.9.3.

### CVE-2026-125798

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T19:17:15.413 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Zaytech Smart Online Order for Clover clover-online-orders allows DOM-Based XSS.This issue affects Smart Online Order for Clover: from n/a through 1.6.6.

### CVE-2026-125760

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T19:17:15.073 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Bit Apps Bit Assist bit-assist allows DOM-Based XSS.This issue affects Bit Assist: from n/a through 1.8.4.

### CVE-2026-128893

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T15:16:47.467 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Marcin Wise Chat wise-chat allows Reflected XSS.This issue affects Wise Chat: from n/a through 3.4.5.

### CVE-2026-125793

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T15:16:47.027 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in flexmls Flexmls® IDX flexmls-idx allows Reflected XSS.This issue affects Flexmls® IDX: from n/a through 4.1.2.

### CVE-2026-125765

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T15:16:46.743 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in ShortPixel ShortPixel Adaptive Images shortpixel-adaptive-images allows Stored XSS.This issue affects ShortPixel Adaptive Images: from n/a through 3.11.6.

### CVE-2026-125733

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T15:16:46.600 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in DevItems ShopLentor woolentor-addons allows Reflected XSS.This issue affects ShopLentor: from n/a through 3.5.7.

### CVE-2026-125447

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T15:16:45.760 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Kaliforms Kali Forms kali-forms allows Reflected XSS.This issue affects Kali Forms: from n/a through 2.4.31.

### CVE-2026-21152

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-16T12:17:55.757 |

Improper input validation in libMyFilterPlugin.camera.samsung.so prior to SMR Nov-2026 Release 1 allows local attackers to potentially execute arbitrary code. User interaction is required for triggering this vulnerability.
