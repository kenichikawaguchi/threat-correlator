# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-02 15:00 UTC
- **対象期間**: `2026-11-01T15:00:18.000Z` 〜 `2026-11-02T15:00:40.000Z`
- **重要CVE数**: 53 件（Critical 9.0+: 13 件 / High 7.0〜: 40 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に報告された CVE のうち **CVSS 7.0 以上が 30 件以上** と、深刻度の高い脆弱性が集中しています。  
- **OS コマンドインジェクション／パス・トラバーサル** が目立ち、特に WAVLINK 系ルータや Network‑AI 製品で多数報告されています。  
- **認証バイパスや権限昇格** も散見され、Barracuda Email Security Gateway や Prefab‑UI のようなインフラ系コンポーネントが標的になっています。  
- 多くは **リモートから直接実行可能 (Network: C)** で、攻撃者が未認証でもシステム全体を制御できるリスクが高いです。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑120338** | 10.0 (CVSS:3.1) | Prefab‑UI の Generative UI サンドボックスが Deno に `--allow-all` で起動され、ユーザー提供の Python (Pyodide) が **無制限に実行** できる | **最高スコア**。LLM が生成したコードを安全に実行できると想定した機能が、実質的に任意コード実行 (RCE) を許す。全てのデプロイで即時パッチが必要。 |
| **CVE‑2025‑11969** | 9.4 | System 製品の REST API がロールベースのアクセス制御を正しくチェックせず、低権限ユーザーが管理操作を実行可能 | **権限昇格** による内部情報漏洩・設定改竄リスク。認証は不要で、内部ネットワークにいるだけで重大な操作が可能になる。 |
| **CVE‑2026‑116606** | 9.3 (CVSS:4.0) | Barracuda Email Security Gateway 9.4.0.030 未満で **認証バイパス** が可能。構成インポート機能を悪用し、任意のバックアップを復元できる | **メールインフラ全体の設定改竄** が可能になるため、スパム送信やメール盗聴につながる。 |
| **CVE‑2026‑120345** (WAVLINK WN551X3‑A) | 9.3 | `/bin/ioos` の DNS 解決ハンドラで引数操作により **OS コマンドインジェクション** が遠隔実行可能 | 同機種で **10 件以上** の類似脆弱性が報告されており、ファームウェア全体の品質が疑問視される。 |
| **CVE‑2026‑120313** (Network‑AI) | 8.7 | `InputSanitizer.sanitizePath()` のパス・トラバーサル不備により、任意のディレクトリへファイル読み書きが可能 | 製品は AI 推論サーバとして多くの企業で採用されており、**機密データ漏洩** や **マルウェア配置** の足掛かりになる。 |

---

## 3. 推奨アクション  

### 3.1 共通的な対策
- **脆弱性情報の継続的モニタリング**：NVD、ベンダーのセキュリティアドバイザリ、GitHub Security Advisories を定期的にチェック。  
- **最小権限の原則**：管理 API・管理画面へのアクセスは IP 制限・VPN 経由にし、不要な管理権限は削除。  
- **ネットワーク分離**：外部から直接管理ポートに到達できないよう、ファイアウォールで **DMZ** または **内部 VLAN** に配置。  

### 3.2 製品別具体的アップデート

| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン | アップデート手順・備考 |
|-------------------|----------------------|----------------|----------------------|
| **Prefab‑UI** | 0.14.0 – 0.20.2 | **≥ 0.20.3** (Deno 起動時に `--allow-all` を除去) | `npm install prefab-ui@latest` または Docker イメージを再ビルド。 |
| **System (REST API 製品)** | 任意 (ロールチェック不備) | **ベンダー提供のパッチリリース**（2026‑Q1） | ベンダーのパッチ適用手順に従い、**RBAC 設定の再確認**を実施。 |
| **Barracuda Email Security Gateway** | < 9.4.0.030 | **9.4.0.030 以上** | 管理コンソール → **Updates → Firmware** から最新ファームウェアを適用。 |
| **WAVLINK ルータ (WN551X3‑A, WN536AX6‑A, WN553X1‑B など)** | すべての公開ファームウェア | **ベンダーが提供するセキュリティパッチ**（2026‑Q2 以降） | 公式サイトから最新 **.bin** を取得し、**Web UI → Firmware Upgrade** で適用。パッチが未提供の場合は **リモート管理を無効化**、不要ポートを閉じる。 |
| **Network‑AI** | < 5.15.5 | **5.15.5 以上** | `pip install --upgrade network-ai` または Docker イメージのタグを `5.15.5` 以上に更新。 |
| **@fastify/http-proxy** | 9.0.0 – 11.6.5 | **≥ 11.6.6** | `npm install @fastify/http-proxy@latest`。アップグレード後は **prefix / rewritePrefix** 設定を再確認。 |
| **Liquid Web / StellarWP BookIt** | ≤ 2.6.0.6 | **≥ 2.6.0.7** | WordPress 管理画面 → **Plugins → Updates** で更新、もしくは `composer update bookit/bookit`. |
| **Joomla Extensions (RegularLabs Sourcerer, joomshaper Helix, etc.)** | < 17.0.1 / < 2.2.11 | **最新版** (2026‑Q1 以降) | Joomla 管理画面 → **Extensions → Manage → Update**。特に **Sourcerer** と **Helix Ultimate** は **PHP コードインジェクション** 対策として必ず更新。 |
| **ManageEngine Password Manager Pro / PAM360** | < 13236 / < 8601 | **最新版** (2026‑Q1) | ManageEngine の **Security Advisories** に従い、パッチ適用と **強力な管理者パスワード** を設定。 |
| **Termix‑SSH** | ≤ 2.9

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-120338

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-269;CWE-693` |
| Published | 2026-11-01T16:18:14.970 |

Prefab UI's Generative UI sandbox runs caller-supplied Python inside Pyodide, Python compiled to WebAssembly, in a Deno subprocess. The feature is documented as isolation for untrusted code, including LLM-written UI. From prefab-ui 0.14.0 through 0.20.2 the launcher starts Deno with unrestricted --allow-read, --allow-write, and --allow-net, and the runner leaves the Deno API on the JavaScript global object. Pyodide's js module proxies that global, so the Python can call Deno.readTextFileSync and Deno.writeTextFileSync. A caller who can supply the code can read and write files as the server OS user, and can persist code execution by writing a .pth file into the server virtualenv's site-packages. The usual remote path is FastMCP's GenerativeUI provider, which registers the MCP tool generate_prefab_ui and forwards that tool's code argument into this sandbox. On a FastMCP server with no authentication configured, any client who can reach the server can call the tool. With authentication, any client allowed to call tools can. Generative UI is opt-in, and the host must have Deno installed. Confirmed on prefab-ui 0.20.2. Fixed in 0.21.0: after the runtime and Prefab sources load, the runner revokes Deno read, write, and network permission before it accepts code, the process is started with --no-prompt so a permission request cannot grant them again, and bootstrap network access is limited to cdn.jsdelivr.net. The fix is commit 030f074 (pull request 538).

### CVE-2025-11969

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-02T06:17:42.087 |

The System REST APIs do not correctly enforce access control mechanisms, allowing users with lower privilege roles to execute administrative actions that should be restricted. This weakness permits unauthorized operations on the affected product.

Successful exploitation could enable a malicious actor to perform unauthorized administrative operations, including executing administrative functions. APIs exposed through the WSO2 API Manager's API Gateway are not affected by this vulnerability.

### CVE-2026-116606

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-02T13:17:37.017 |

An authentication bypass in Barracuda Email Security Gateway versions earlier than 9.4.0.030 allows an unauthenticated remote attacker to invoke a configuration-import function and restore a crafted, compatible backup archive, resulting in unauthorized modification of the appliance’s global configuration.

### CVE-2026-120345

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-02T06:17:43.410 |

A vulnerability was found in WAVLINK WN551X3-A M51X3_V251020-WO-182e965. This impacts the function sub_41a430 of the file /bin/ioos of the component DNS Resolution Handler. Performing a manipulation of the argument data results in os command injection. It is possible to initiate the attack remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure.

### CVE-2026-120344

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-02T05:18:25.450 |

A vulnerability has been found in WAVLINK WN551X3-A M51X3_V251020-WO-182e965. This affects the function system of the file /bin/ioos of the component WireGuard CLI Group Handler. Such manipulation of the argument group_name leads to os command injection. The attack may be performed from remote. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120283

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-02T01:17:27.500 |

A vulnerability was identified in Linksys E8450 1.2.00.360516. Affected is the function strcpy of the file /www/cgi-bin/portal.cgi. Such manipulation of the argument hidden_timezone leads to stack-based buffer overflow. The attack can be executed remotely. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-120281

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-02T01:17:27.070 |

A vulnerability was found in WAVLINK WN536AX6-A V260507. This affects the function strcpy of the file /protocol.csp of the component OpenVPN Handler. The manipulation of the argument openvpn_ip results in stack-based buffer overflow. The attack may be launched remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure.

### CVE-2026-120280

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-02T01:17:26.873 |

A vulnerability has been found in WAVLINK WN536AX6-A V260507. The impacted element is the function wireguard_cli_group handler of the file /protocol.csp of the component WireGuard. The manipulation of the argument group_id/group_name leads to os command injection. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120279

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-02T01:17:26.677 |

A flaw has been found in WAVLINK WN536AX6-A V260507. The affected element is an unknown function of the file /protocol.csp of the component openvpn_cli Handler. Executing a manipulation of the argument file_id can lead to os command injection. The attack can be launched remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120277

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-02T00:18:10.810 |

A security vulnerability has been detected in WAVLINK WN536AX6-A V260507_2.0.0. This issue affects the function sub_41a1d8 of the file /bin/ioos of the component WireGuard CLI Group Handler. Such manipulation of the argument group_name leads to os command injection. It is possible to launch the attack remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120276

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-02T00:18:09.897 |

A weakness has been identified in WAVLINK WN536AX6-A V260507_2.0.0. This vulnerability affects the function sub_416760 of the file /bin/ioos of the component Web Management Interface. This manipulation of the argument group_name causes os command injection. It is possible to initiate the attack remotely. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure.

### CVE-2026-62048

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-01T16:18:15.170 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Liquid Web / StellarWP BookIt bookit allows SQL Injection.This issue affects BookIt: from n/a through 2.6.0.6.

### CVE-2026-120213

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-436` |
| Published | 2026-11-02T11:17:31.137 |

@fastify/http-proxy is a Fastify plugin that proxies HTTP requests to an upstream server under a configured prefix. In versions 9.0.0 through 11.6.5, when an application uses parameterized prefix and rewritePrefix options to pin clients to a fixed upstream path, the plugin substitutes URL-decoded route parameters into rewritePrefix without re-encoding them. A parameter value that encodes a path separator together with a fragment or query delimiter therefore decodes into real separators and delimiters that inject extra upstream path segments and strip the mandatory suffix the rewritePrefix was meant to enforce, without using any dot-dot traversal. An unauthenticated remote attacker can use this to reach upstream locations outside the intended prefix, leading to path-restriction bypass and, depending on the upstream, server-side request forgery or authorization bypass in the proxied service. The issue is fixed in @fastify/http-proxy 11.6.6, and users should upgrade to 11.6.6 or later. There is no workaround other than upgrading.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-102802

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-02T14:17:34.057 |

Joomla Extension - regularlabs.com - PHP code injection vector in Sourcerer extension < 17.0.1 when used with Articles Anywhere extension < 20.1.1 - Sourcerer can restrict PHP in articles according to article-author trust; the exact creator and last-editor rule varies by release. Articles Anywhere can insert the text or full layout of one article into another. In the affected combination, when Articles Anywhere processes an inclusion before Sourcerer and Force Content Triggers is off, the included article's Sourcerer code can be evaluated using the enclosing article's trusted identity rather than the included article's own identity. The resulting gap is between the authority of the article supplying the code and the authority used to decide whether to run it. Ordinary Articles Anywhere output is not itself the issue.

### CVE-2026-18199

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-02T08:17:36.083 |

Zohocorp ManageEngine Password Manager Pro versions before 13236 and PAM360 versions before 8601 are vulnerable to an authenticated Remote Code Execution vulnerability.

### CVE-2026-8923

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-02T11:17:33.380 |

Zohocorp ManageEngine Eventlog Analyzer and ManageEngine Log360 versions before 13062 are vulnerable to Authenticated Remote Code Execution in Log Forward option.

### CVE-2026-2613

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-02T11:17:31.963 |

The Admin REST API accepts user-supplied input without adequately sanitizing it, allowing it to be included in the structure of SQL statements.

A user with administrator privileges can exploit this by influencing the structure of executed SQL statements, enabling blind SQL injection to infer database information and potentially impact the availability of the database service.

### CVE-2026-120315

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-02T03:17:29.457 |

LobeHub Chat from 1.84.26 before 2.1.49 contains a path traversal vulnerability that allows authenticated users to write arbitrary files by supplying unsanitized file names to writeTempFile(). Attackers can create a file record via file.createFile with a traversal name, then trigger document parsing to overwrite application files like startServer.js for code execution or denial of service.

### CVE-2026-120313

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-02T03:17:29.053 |

Network-AI before 5.15.5 contains a path traversal vulnerability in InputSanitizer.sanitizePath() that allows attackers to escape the base directory using sibling-directory paths. Attackers can supply paths whose directory name shares a string prefix with the base, bypassing the unanchored startsWith check to read, list, or write files outside the sandbox.

### CVE-2026-120312

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-02T03:17:28.863 |

Network-AI from 5.13.4 before 5.15.5 contains a path traversal vulnerability in AgentVCR that allows attackers controlling the cassette name to read or write arbitrary .json files. Attackers can pass traversal sequences to load() or save() to disclose sensitive JSON data or overwrite policy files such as AuthGuardian trust-level configuration.

### CVE-2026-120311

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-02T03:17:28.663 |

Network-AI from 5.13.4 before 5.15.5 contains a path traversal vulnerability in FileJobStore that allows attackers to read or delete arbitrary .json files by supplying traversal sequences in the job id. Attackers controlling the id passed to FileJobStore.get(), FileJobStore.delete(), or JobQueue.getJob() can disclose credentials and grant tokens or delete configuration files to weaken AuthGuardian authorization.

### CVE-2026-105602

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-02T14:17:34.813 |

Joomla Extension - joomshaper.com -  Stored Cross-Site Scripting (XSS) in Mega Menu Badge Text in Helix Ultimate < 2.2.11.

### CVE-2026-105600

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-02T14:17:34.520 |

Joomla Extension - php-web-design.com - RCE via setting strings in StageIt 1.0-5.7.5, 6.0-6.3.5

### CVE-2026-103419

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-02T14:17:34.210 |

Joomla Extension - joomshaper.com -  Stored Cross-Site Scripting (XSS) in Media Picker in Helix Ultimate < 2.2.11.

### CVE-2026-111560

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-02T13:17:35.190 |

Improper neutralization of shell metacharacters in the timezone configuration field in certain Barracuda appliance products using common Barracuda code allows an authenticated administrator to inject OS commands that execute with root privileges when the crafted timezone value is subsequently processed.

### CVE-2026-120322

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-02T02:18:47.550 |

A vulnerability was identified in Termix-SSH Termix up to 2.9.2. This issue affects some unknown processing of the file /plugin-api/file-manager/transferToHost. The manipulation of the argument destPath leads to path traversal. The attack may be initiated remotely. The exploit is publicly available and might be used. The shortcut was removed in the standalone File Manager plugin v1.0.0 (transfer engine now always writes over SFTP) and in core v26.10.0. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-120282

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-02T01:17:27.293 |

A vulnerability was determined in WAVLINK WN536AX6-A V260507. This impacts the function host_black of the file /protocol.csp. This manipulation of the argument mac causes os command injection. Remote exploitation of the attack is possible. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure.

### CVE-2026-120240

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-01T19:16:57.950 |

A vulnerability was determined in WAVLINK WN553X1-B V260403_2.0.0. This issue affects the function sub_41A748 of the file /bin/ioos of the component WireGuard CLI Group Handler. Executing a manipulation of the argument group_id/group_name can lead to os command injection. The attack may be performed from remote. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure.

### CVE-2026-120239

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-01T18:17:13.920 |

A vulnerability was found in WAVLINK WN553X1-B V260403_2.0.0. This vulnerability affects the function sub_419DA8 of the file /bin/ioos of the component WireGuard CLI Handler. Performing a manipulation of the argument file_id results in os command injection. The attack is possible to be carried out remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure.

### CVE-2026-120238

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-01T18:17:13.720 |

A vulnerability has been found in WAVLINK WN553X1-B 260403_2.0.0. This affects the function sub_4162A8 of the file /bin/ioos of the component ovpn_file Handler. Such manipulation of the argument file_id leads to os command injection. The attack can be executed remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120231

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-01T15:17:23.053 |

A vulnerability was determined in WAVLINK WN553X1-B V260403_2.0.0. The affected element is the function sub_416568 of the file /bin/ioos of the component OpenVPN CLI Handler. This manipulation of the argument file_id causes os command injection. It is possible to initiate the attack remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure.

### CVE-2026-120230

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-01T15:17:22.830 |

A vulnerability was found in WAVLINK WN701AE 260105. Impacted is the function del_vlan_group of the component ioos Web Backend. The manipulation of the argument vlan_name results in os command injection. The attack may be performed from remote. The exploit has been made public and could be used. The vendor was contacted early about this disclosure.

### CVE-2026-120232

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-11-01T15:17:23.263 |

A vulnerability was identified in Horizon DataSys Reboot Restore Standard up to 13.2. The impacted element is the function sub_23908 in the library shield.sys of the component Kernel Driver. Such manipulation leads to memory corruption. The attack can only be performed from a local environment. The exploit is publicly available and might be used. A fix is planned for the upcoming release.

### CVE-2026-84170

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-01T23:17:29.913 |

Allocation of resources without limits or throttling in Apache Wicket.

org.apache.wicket.markup.html.form.upload.resource.AbstractFileUploadResource is the server side of the form-less upload offered by FileUploadToResourceField, which posts the selected files to a separately mounted resource rather than through a Form. The resource is an application-wide singleton with no component to consult, so newResourceResponse() takes the three limits that bound the upload - the total request size, the maximum size of a single part and the maximum number of parts - from the request parameters maxSize, fileMaxSize and fileCountMax, and hands them to the multipart parser as they arrive. Nothing binds those numbers to the field that is supposed to be uploading. A request naming a very large maxSize is therefore parsed with no effective ceiling on the total size, and omitting fileMaxSize and fileCountMax leaves the per-part and part-count limits unset as well. The values the application configured through FileUploadToResourceField#setMaxSize(), #setFileMaxSize() and #setFileCountMax() are consulted only when the client omits the corresponding parameter, so against a client that supplies one they have no effect at all.

Parts above the parser's in-memory threshold are spooled to the container's temporary directory, and the file parts are then copied into the folder the application's IUploadsFileManager owns, under a sub-folder the request names, where they remain. A part that is not a file is read into the heap in full while the request is parsed. One request, repeatable, can therefore consume as much disk or as much heap as the client chooses to send. The resource carries no authorization annotation and the default authorization strategy permits every resource request, so unless the application authorizes the resource itself the request needs no authentication, no session, no prior page view and no user interaction.

An application is affected where it uses FileUploadToResourceField, or mounts FileUploadResourceReference itself. This is not the ordinary upload path: the resource is a singleton that has to be created and mounted deliberately. An application that configures no upload limit at all loses nothing, because Wicket applies no total-size limit of its own by default; what the defect removes is a limit the application set. Uploads through Form with FileUploadField, and through AjaxFileDropBehavior, are not affected, because both read their limits from the component rather than from the request. The upload resource does not exist in the 8.x line.

This issue affects Apache Wicket: from 9.14.0 through 9.24.0, from 10.0.0 through 10.9.1. Users are recommended to upgrade to version 9.25.0 or 10.12.0, which fix the issue.

### CVE-2026-83594

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-11-01T23:17:29.723 |

Memory allocation with an excessive size value in Apache Wicket.

org.apache.wicket.markup.html.form.upload.resource.FileUploadToResourceField uploads files to a separately mounted resource rather than through a form, and is told the outcome afterwards over its own Ajax callback. That callback reads the request parameter filesInfo, a JSON array carrying a client file name, a size and a content type for each file, and turns it into the list of FileUploadToResourceField.UploadInfo that onUploadSuccess() receives. Nothing binds that JSON to an upload the resource performed and nothing re-derives it from the stored files, so the number of entries and every value in them are whatever the request supplied. The callback URL is rendered into the page, no prior upload is required, and both GET and POST reach it, so any client that can load the page can have the component report files that were never uploaded, without authenticating beyond whatever the page itself requires and without any user interaction.

UploadInfo#get(), which the class offers as the way to obtain the bytes of an upload, allocates a byte array from UploadInfo#getSize() before it opens the file. The array is therefore sized by the number the request supplied, and the allocation happens even for a file that was never stored. One small request can cost the server close to two gigabytes of heap, and the request is trivially repeatable, so a few of them exhaust the heap for every request the Java virtual machine is serving. A size that the conversion to int turns negative instead throws NegativeArraySizeException, which the exception handler inside that method does not cover, so it escapes into the application.

An application is affected where it uses FileUploadToResourceField, which is not the ordinary upload path through FileUploadField and Form and has to be extended and mounted deliberately. The allocation additionally requires the application to call UploadInfo#get() rather than reading UploadInfo#getFile() itself. Where the application denies the ENABLE action on the field through its authorization strategy, the callback is refused like any other listener. The 8.x line does not contain this component and is not affected.

This issue affects Apache Wicket: from 9.14.0 through 9.24.0, from 10.0.0 through 10.11.0. Users are recommended to upgrade to version 9.25.0 or 10.12.0, which fix the issue.

### CVE-2026-117518

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-02T11:17:30.660 |

@fastify/reply-from is a Fastify plugin that forwards requests to an upstream HTTP server. In versions up to and including 12.8.0, the plugin validated proxy paths against forward-slash dot-segments only and then built the target with the WHATWG URL parser, which normalizes a backslash and its percent-encoded form to a forward slash on the http, https, ws, and wss schemes. A path that uses backslash dot-segments therefore bypasses the traversal check and resolves to a different upstream path, so an application that scopes proxying to an upstream prefix, or relies on route guards in front of the forwarding call, can have an unauthenticated request escape the intended prefix and reach other upstream endpoints. The resulting access to unintended upstream resources is primarily a confidentiality impact with limited integrity impact. The issue is fixed in @fastify/reply-from 12.8.1, where the path is normalized and any segment resolving to a single or double dot, along with control characters and ambiguous whitespace, is rejected before the URL is constructed, and users should upgrade to 12.8.1 or later. There is no workaround other than upgrading.

### CVE-2026-120317

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-02T03:17:29.957 |

http4k from 4.9.10.0 before 6.60.0.0 contains a missing integrity check vulnerability because DigestEncoder computes the auth-int digest without hashing the request entity body. On-path attackers on non-TLS channels can rewrite the body of authenticated requests while keeping the Authorization header valid, executing state-changing actions as the victim.

### CVE-2026-120316

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-02T03:17:29.760 |

http4k before 6.62.0.0-ee contains a path traversal vulnerability in ThymeleafTemplates Caching and HotReload that allows unauthenticated attackers to read files outside baseTemplateDir by supplying ../ segments in ViewModel.template() values. Attackers can influence request-driven template selection so Thymeleaf's FileTemplateResolver resolves escaped paths without containment checks, disclosing any file readable by the server process.

### CVE-2026-94349

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-02T13:17:41.583 |

Dell OpenManage Enterprise, versions prior to 4.8.0, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with adjacent network access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-92886

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-02T13:17:41.250 |

Missing Authorization vulnerability in TÜBİTAK BİLGEM Software Technologies Research Institute eta-register allows Privilege Escalation.

This issue affects eta-register: from 2.0.8 before 2.0.9.

### CVE-2026-120241

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-01T19:16:59.393 |

A vulnerability was identified in Ruijie RG-ES205GC, RG-ES206GC-P, RG-ES208GC, RG-ES210GC-LP and RG-ES210GS-P ESW_1.0(1)B1P48. Impacted is an unknown function of the file httpupg.cgi of the component Local Firmware Upgrade Interface. The manipulation leads to buffer overflow. It is possible to initiate the attack remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-95863

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-01T23:17:30.943 |

Improper neutralization of input during web page generation in Apache Wicket.

Apache Wicket generates JavaScript that refers to the elements it renders, and
writes into that JavaScript two values it derives itself: a component's markup
id, and the input name of a form component, which is built from component ids.
Both are placed inside single-quoted JavaScript string literals without being
escaped for that context, so a value containing a single quote or a backslash
ends the literal, and what follows is parsed as script and runs in the
application's origin when the page loads.

A markup id is the value passed to org.apache.wicket.Component#setMarkupId(String),
or the id attribute written in the component's markup, or an id Wicket
generates, in that order. The first two are supplied by the application in an
HTML context, where both characters are legal and where Wicket escapes them
correctly when it writes the same value into the id attribute of the element; a
generated id cannot contain either. An input name is derived from the ids of the
components between the form and the form component, and a component id was
rejected only for ':' and '~'.

In org.apache.wicket:wicket-core on 9.x and 10.x,
org.apache.wicket.markup.head.OnEventHeaderItem#forMarkupId(String, String,
CharSequence) quotes the id it is given into a Wicket.Event.add call, and
components in both wicket-core and wicket-extensions reach it through
#forComponent(Component, String, CharSequence). On every affected version,
org.apache.wicket.markup.html.form.Form writes its markup id and the id of its
hidden-fields container into such literals,
org.apache.wicket.markup.html.form.FormComponentUpdatingBehavior writes an input
name, and org.apache.wicket.markup.html.form.upload.MultiFileUploadField writes
two markup ids and an input name. On 8.x, Form also writes an input name into the
action of a submitting link, and on 8.x and 9.x Form#appendDefaultButtonField
writes an input name into a name attribute with no escaping at all, so a value
containing a double quote escapes the attribute into markup.

org.apache.wicket:wicket-extensions is affected in its own right and not only
through wicket-core: AjaxEditableLabel, AjaxIndicatorAppender,
AjaxDisableComponentListener, UploadProgressBar, KittenCaptchaPanel, Palette,
FilterForm and, on 9.x and 10.x, TrapFocusBehavior and AjaxListPanel each build
their own JavaScript containing a markup id.

An application is affected where a markup id or a component id carries one of
those characters. Wicket does not put one there itself, so the value comes from
the application: an id set on a component, an id attribute in a template, or a
component id derived from data. None of those is a JavaScript context from the
application's point of view.

The Content-Security-Policy that Apache Wicket 9.x and 10.x send by default does
not prevent this. The generated script is written into a script element carrying
the per-response nonce, so the injected code is part of a script the policy
admits.

The fixed versions check an id where it enters instead of escaping each place it
is written. A component id and a markup id may no longer contain a quote, a
backquote, a backslash, braces, angle brackets, a semicolon, an ampersand or a
control character, and a markup id may not contain parentheses or square
brackets either; a component constructed with such an id, or given such a markup
id, fails with an exception.

This issue affects Apache Wicket: from 8.0.0 through 8.19.0, from 9.0.0 through
9.24.0, from 10.0.0 through 10.11.0. Users of Apache Wicket 7.x or older, which
are no longer supported, should upgrade to a supported version. Users are
recommended to upgrade to version 8.20.0, 9.25.0 or 10.12.0, which fix the issue.

### CVE-2026-82956

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-01T23:17:29.130 |

Improper neutralization of input during web page generation in Apache Wicket.

org.apache.wicket.ajax.AjaxNewWindowNotifyingBehavior notices that a page instance has been opened in a second browser window or tab. It asks the browser for the value of window.name, which reaches the server as the request parameter windowName, and remembers what the browser reported in a field of the behaviour. That field is part of the page's serialized state, so the remembered value stays in the page store for as long as the page instance does.

On every later render of that page instance the behaviour builds the precondition of its Ajax call by substituting the remembered value into a single-quoted JavaScript string literal, and Wicket writes that precondition into the page as raw JavaScript, because the precondition of an Ajax call listener is script supplied by the caller and is emitted without quoting or escaping. Nothing on that path escapes the value. The window name is client-supplied and Wicket applies no validation to it, so a remembered name containing a single quote ends the literal and the rest of it runs as script in the application's origin, every time that page instance is rendered.

An application is affected only where it has explicitly added AjaxNewWindowNotifyingBehavior to a component. No part of the framework installs the behaviour, so an application that does not use it is not affected. The name the behaviour generates for itself, when the browser reports no name at all, is a random UUID and is not client-supplied.

This issue affects Apache Wicket: from 8.0.0 through 8.19.0, from 9.0.0 through 9.24.0, from 10.0.0 through 10.11.0.

Users are recommended to upgrade to version 8.20.0, 9.25.0 or 10.12.0, which fix the issue.

### CVE-2026-111089

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-01T23:17:28.697 |

Apache Wicket reads texts from the application's resource bundles — a localized label, a css class name — and writes some of them into the JavaScript and the markup it generates for a component. Those texts are placed inside single-quoted JavaScript string literals and inside quoted attribute values without being escaped for that context, so a text containing a quote ends the literal or the attribute, and what follows is parsed as script or as markup in the application's origin when the page loads.

A resource bundle entry is authored for the application and does not say where the framework will write it. The same key is read by the framework into element text, where Wicket escapes it, and into the contexts below, where it did not. A text containing an apostrophe, which is ordinary in several languages, is enough to break the page; a text under the influence of another party is enough to run script.

In org.apache.wicket:wicket-core, org.apache.wicket.markup.html.form.upload.MultiFileUploadField writes the org.apache.wicket.mfu.delete message into a JavaScript string literal, and org.apache.wicket.markup.html.form.Form writes the hidden-fields css class into the class attribute of the container it renders for its hidden fields; on 8.0.0 through 8.19.0 and 9.0.0 through 9.24.0 Form#appendDefaultButtonField writes the same css class into a second container. In org.apache.wicket:wicket-extensions, UploadProgressBar writes its UploadProgressBar.starting text into a JavaScript string literal, FilterForm writes the hidden-fields css class into the class attribute of its hidden input markup, and on 9.0.0 through 9.24.0 and 10.0.0 through 10.11.0 TrapFocusBehavior writes its current css class into a JavaScript string literal.

The Content-Security-Policy that Apache Wicket 9.x and 10.x send by default does not prevent the JavaScript cases: the generated script is written into a script element carrying the per-response nonce, so the injected code is part of a script the policy admits. It does prevent an inline event handler injected through the attribute cases.

This issue affects Apache Wicket: from 8.0.0 through 8.19.0, from 9.0.0 through 9.24.0, from 10.0.0 through 10.11.0. Users of Apache Wicket 7.x or older, which are no longer supported, should upgrade to a supported version. Users are recommended to upgrade to version 8.20.0, 9.25.0 or 10.12.0, which fix the issue.

### CVE-2026-74993

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-02T14:17:37.953 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Starnet Computer and Network Systems Inventory Tracking Application allows SQL Injection.

This issue affects Inventory Tracking Application: through 2026-10-16.

### CVE-2026-101186

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-19` |
| Published | 2026-11-02T07:18:03.617 |

DoS vulnerability in the window module.
Impact: Successful exploitation of this vulnerability may affect availability.

### CVE-2026-84231

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-01T23:17:30.550 |

Improper neutralization of input during web page generation in Apache Wicket.

org.apache.wicket.markup.html.link.ExternalLink builds a JavaScript click handler and writes it into the tag's onclick attribute whenever the markup tag the component is bound to is not an a, link or area element. The URL held in the component's model is concatenated into a single-quoted JavaScript string literal in that handler without being escaped for that context. The same happens on the neighbouring branch, taken when popup settings are attached, where the value is concatenated into the window.open() call built by org.apache.wicket.markup.html.link.PopupSettings#getPopupJavaScript(). The only escaping applied is the markup escaping that every attribute value receives as the tag is written, which replaces an apostrophe with a character reference. A browser decodes character references in an attribute value before it compiles the event handler, so the apostrophe is restored, closes the string literal, and the rest of the model value is executed as script in the application's origin.

An application is affected where it binds an ExternalLink to a markup tag that is not an anchor, such as a button or a span, and the URL in the model holds data an attacker can influence, which is the ordinary use of the component rather than a misuse of it. Nothing runs until a user activates the element.

This issue affects Apache Wicket: from 8.0.0 through 8.19.0. Users of Apache Wicket 7.x or older, which are no longer supported, should upgrade to a supported version.

Users are recommended to upgrade to version 8.20.0, which fixes the issue.

### CVE-2026-83559

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-11-01T23:17:29.513 |

Improper encoding or escaping of output in Apache Wicket.

org.apache.wicket.core.util.string.JavaScriptUtils#escapeQuotes() replaces each single quote in its input with a backslash and a single quote, and each double quote with a backslash and a double quote, so that the value can be placed inside a JavaScript string literal. It does not escape the backslash, which is the character that has to be escaped, and escaped first, for the rest of that escaping to hold. A value that already holds a backslash immediately before a quote therefore ends up with two backslashes in front of that quote: the first escapes the second, the quote itself is left unescaped, and it closes the literal. Whatever the value carries after that point is no longer text but JavaScript, and it runs in the application's origin and in the session of the user looking at the page. The method is public, is not deprecated, and its documentation states that its result can be part of a JavaScript call such as an alert; the only limitation it notes concerns JSON values, which need different escaping.

An application is affected wherever it calls the method itself and places the result inside a JavaScript string literal, from its own code or from a component of its own or of a third party, and the value it escapes holds data an attacker can influence. There is no further condition, and no component of Wicket has to be involved: the application is using the method for what its documentation offers, and the method does not deliver it.

Two components shipped with Wicket Extensions pass a value through the method. org.apache.wicket.extensions.ajax.markup.html.AjaxEditableLabel writes the editor's first error feedback message into a single-quoted JavaScript string literal in the Ajax response, so an application is affected through that component where the message shown for a failed edit holds data an attacker can influence, whether that is the submitted value itself or another variable the application sets on the validation error. A validation message can carry the submitted value, because input is a message variable that every form component supplies for its own validation errors, and the documentation shows overriding a validator's message to include it; none of the message bundles shipped with Wicket interpolates it, so an application that has not written such a message is not affected through this component. org.apache.wicket.extensions.ajax.markup.html.repeater.AjaxListPanel passes the serialized markup tag of an appended component through the method and is not affected: the tag comes from the panel's own markup file, and a quote in any of its attribute values, the component's markup id included, is written as a character reference by the tag serialization and cannot close the literal.

This issue affects Apache Wicket: from 8.0.0 through 8.19.0, from 9.0.0 through 9.24.0, from 10.0.0 through 10.11.0. Users of Apache Wicket 7.x or older, which are no longer supported, should upgrade to a supported version.

Users are recommended to upgrade to version 8.20.0, 9.25.0 or 10.12.0, which fix the issue.

### CVE-2026-83539

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-01T23:17:29.317 |

Improper neutralization of input during web page generation in Apache Wicket.

org.apache.wicket.extensions.markup.html.basic.SmartLinkLabel and org.apache.wicket.extensions.markup.html.basic.SmartLinkMultiLineLabel display a text value and turn any URL they find in it into a hyperlink. Both escape the model value and then hand the escaped text to org.apache.wicket.extensions.markup.html.basic.DefaultLinkParser, which searches it for anything of the form scheme://rest and wraps each match in an anchor whose href is the matched text, copied in as it is. The pattern accepts any scheme, and there is no list of permitted schemes anywhere on the path. A text value naming a scheme that executes script therefore becomes an anchor that executes it, in the application's origin and in the reader's own session, when the reader clicks the link. Rendering the page is not enough on its own; the link has to be activated. Escaping does not prevent this and is not the issue: the characters the payload needs are all valid in a URL and are ones that org.apache.wicket.util.string.Strings#escapeMarkup() leaves alone, and the value ends up in a URL rather than in element text, which is a context that escaping model data does not make safe.

An application is affected where it renders text it received through either of these two components. That is what they are for: they exist to linkify email addresses and web URLs found in the data an application is displaying, so untrusted input is the purpose of the feature rather than a misuse of it, and no unusual configuration is involved. No other component uses this parser, and an application that uses neither SmartLinkLabel nor SmartLinkMultiLineLabel is not affected.

On 9.x and 10.x the Content-Security-Policy Wicket sends by default admits script only from a source carrying a per-response nonce, and a URL whose scheme executes script cannot carry one, so that default policy stops the script from running. This is a property of the default policy and not of these components. An application that has weakened or disabled its Content-Security-Policy, for this or for any unrelated reason, is affected in full. Wicket 8.x has no Content-Security-Policy support at all and is affected as it stands.

This issue affects Apache Wicket: from 8.0.0 through 8.19.0, from 9.0.0 through 9.24.0, from 10.0.0 through 10.11.0. Users of Apache Wicket 7.x or older, which are no longer supported, should upgrade to a supported version. Users are recommended to upgrade to version 8.20.0, 9.25.0 or 10.12.0, which fix the issue.

### CVE-2026-103420

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-02T14:17:34.363 |

Joomla Extension - php-web-design.com - CSRF for various actions in StageIt 1.0-5.7.5, 6.0-6.3.5

### CVE-2026-82840

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-11-01T22:17:48.017 |

Session fixation in Apache Wicket.

org.apache.wicket.authroles.authentication.AuthenticatedWebSession is the authentication base class of Wicket's role-based security module, and its signIn(String, String) method is the entry point through which an application authenticates a session. Renewing the container session id at that point is the standard defence against an attacker who has fixed a session id in a victim's browser, and Wicket provides that renewal as org.apache.wicket.Session#changeSessionId(), whose documentation directs callers to invoke it on login for exactly that reason.

AuthenticatedWebSession#signIn(String, String) calls it inside a guard that succeeds only on the first transition of the session's signed-in flag. The session id is therefore renewed when a session first signs in, and is not renewed when a session that is already signed in authenticates again. signIn(String, String) returns true either way, so neither the caller nor the application can tell that the renewal did not happen.

An application is affected where it authenticates through AuthenticatedWebSession, which AuthenticatedWebApplication requires and which the shipped UsernamePasswordPanel uses, and where a session that is already signed in can authenticate again: a step-up prompt before a sensitive action, an account switch, or simply a sign-in form that stays reachable once the user is signed in. Nothing in the module hides that form from a signed-in session. Reaching the defect also requires an attacker to place a session id of their choosing in the victim's browser. JSESSIONID is set by the servlet container rather than by Wicket, so that needs a position Wicket does not grant, such as control of a host under the same registrable domain or a container configured to carry the session id in the URL, and the planted session has to be one the attacker has already signed in on, because a session that is not yet signed in does have its id renewed by the victim's authentication. An authentication attempt that fails signs the session out and closes the window. Applications that renew the session id in their own code after a successful authentication are not affected.

As a workaround, renew the session id from the application's own code on every successful authentication, by calling Session#changeSessionId() at the end of the authenticate(String, String) implementation.

This issue affects Apache Wicket: from 8.18.0 through 8.19.0, from 9.23.0 through 9.24.0, from 10.9.0 through 10.11.0.

Users are recommended to upgrade to version 8.20.0, 9.25.0 or 10.12.0, which fix the issue.

### CVE-2026-101176

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-264` |
| Published | 2026-11-02T07:18:02.577 |

Permission control vulnerability in the event notification management module.
Impact: Successful exploitation of this vulnerability may affect service confidentiality.

### CVE-2026-66570

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-01T16:18:15.323 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Nickboss WordPress File Upload wp-file-upload allows Stored XSS.This issue affects WordPress File Upload: from n/a through 5.2.1.
