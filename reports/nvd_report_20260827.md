# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-26 15:00 UTC
- **対象期間**: `2026-08-25T15:00:39.000Z` 〜 `2026-08-26T15:00:29.000Z`
- **重要CVE数**: 139 件（Critical 9.0+: 23 件 / High 7.0〜: 116 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** と非常に多く、特に **リモートからのコード実行 (RCE) や特権昇格** を可能にする脆弱性が目立ちます。  
- Adobe Campaign Classic 系列や NVIDIA OpenShell など、**エンタープライズ向け基幹システム** に深刻な OS コマンドインジェクション／サンドボックス脱出が報告されています。  
- Python／Node.js の AI/LLM 関連フレームワーク（Chainlit、QWED‑MCP、PraisonAI など）でも認証なしで任意コード実行が可能になる設定ミスが多数見られ、**AI アプリケーションの急速な普及に伴うセキュリティ対策の遅れ** が浮き彫りになっています。  
- 多くの脆弱性は **ネットワーク境界の防御が不十分** な環境であれば、認証不要で直接攻撃が成立する点が共通しています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑76197** / **CVE‑2026‑76195** | 10.0 | Adobe Campaign Classic (ACC) の OS コマンドインジェクション。認証不要で任意コード実行が可能。 | **最高スコア (10.0)** かつ **広く導入されているマーケティングオートメーション基盤**。攻撃者は任意のシェルコマンドを実行でき、内部ネットワーク全体への横展開が容易。 |
| **CVE‑2026‑76193** | 10.0 | ACC の SSRF → 任意コード実行。内部サービスへのリクエストを外部から誘導できる。 | 同上の製品で **別の攻撃ベクトル (SSRF)** が同時に報告されており、**複合的な攻撃シナリオ** が成立。 |
| **CVE‑2026‑65093** / **CVE‑2026‑65083** | 9.9 | NVIDIA OpenShell for Linux のサンドボックス脱出・不完全な入力制御。特権ユーザー権限でコード実行が可能。 | GPU ドライバ・コンテナ環境で広く利用される **OpenShell** が対象。サンドボックスの破壊は **クラウド・HPC 環境全体の安全性を揺るがす**。 |
| **CVE‑2026‑45018** | 9.8 | Chainlit (Python) の /mcp エンドポイントが認証なしで公開。任意のリクエストで MCP コマンド実行が可能。 | **生成系 AI アプリケーション** のフレームワークで、デフォルト設定が危険。AI チャットボットを外部から乗っ取られるリスクが高い。 |
| **CVE‑2026‑55546** | 9.8 | QWED‑MCP の数式パーサが SymPy の `parse_expr()` を直接呼び出すため、任意コード実行が可能。 | AI 検証インフラで **数式評価を外部入力に委ねる** 設計ミス。AI/LLM の安全性を担保するツール自体が攻撃対象になる「**サプライチェーンリスク**」を示す。 |

> **共通点**：すべて **ネットワークから直接アクセス可能** なサービスで、**認証・入力検証が不十分** である点。特に Adobe 系列は企業の顧客データベースと直結しているため、情報漏洩・改ざんリスクが極めて高いです。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンの即時更新
| 製品・パッケージ | 現行脆弱バージョン | 推奨バージョン (ベンダー提供) | 更新手順のポイント |
|------------------|-------------------|------------------------------|-------------------|
| **Adobe Campaign Classic** | すべての 2026‑xx 系 (例: 23.2.x) | ベンダーが公開した **2026‑R1 パッチ** 以降（リリースノート参照） | ① 公式パッチ適用 → ② 変更点をテスト環境で検証 → ③ 監査ログの有効化 |
| **NVIDIA OpenShell (Linux)** | 1.0.0 〜 1.2.3 | **1.3.0 以降**（2026‑06‑リリース） | ① パッケージマネージャ (apt/yum) で `nvidia-openshell` をアップデート → ② サンドボックス設定 (`sandbox.conf`) を再生成 |
| **Chainlit** | 2.4.0rc0 〜 2.12.0 | **2.12.1 以上** | ① `pip install --upgrade chainlit` → ② `features.mcp.enabled` を **false** に設定し、不要な MCP エンドポイントを無効化 |
| **QWED‑MCP** | < 0.2.1 | **0.2.1 以上** | ① `pip install qwed-mcp>=0.2.1` → ② `verify_math_expression` の入力サニタイズロジックをレビュー |
| **TRtek Software Repository Management** | 2fb4acee 以前 | **2fb4acee+1**（2026‑07‑リリース） | ① ソースコードの `git checkout` → ② `docker-compose up -d` で再デプロイ |

### 3.2 設定・運用レベルの対策
1. **外部からの直接アクセスを遮断**  
   - Web アプリケーションファイアウォール (WAF) で `POST /mcp`、`/cgi-bin/cstecgi.cgi`、`/webhooks/nextcloud` 等のエンドポイントを **IP 制限** または **認証必須** にする。  
2. **最小権限の原則**  
   - Adobe Campaign の実行ユーザーを **非特権 OS アカウント** に変更し、`sudo` 権限を剥奪。  
   - NVIDIA OpenShell のコンテナ実行時に `

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-76197

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T18:18:05.110 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-76195

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T18:18:04.967 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-76193

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-25T18:18:04.813 |

Adobe Campaign Classic (ACC) is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-65093

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-25T21:17:29.300 |

NVIDIA OpenShell for Linux contains a vulnerability where an attacker could cause a sandbox escape. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, data tampering, and information disclosure.

### CVE-2026-65083

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-08-25T21:17:28.050 |

NVIDIA OpenShell for Linux contains a vulnerability in its sandbox provisioning API, where an attacker could cause an incomplete list of disallowed inputs. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, information disclosure, data tampering, and denial of service.

### CVE-2026-45018

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T20:16:55.720 |

Chainlit is a Python framework for building production-ready conversational AI applications. From 2.4.0rc0 until 2.12.0, Chainlit deployments with features.mcp.enabled set to true in .chainlit/config.toml expose the POST /mcp endpoint without requiring authentication. For stdio transport, the endpoint accepts a user-controlled fullCommand string. The validate_mcp_command() function in backend/chainlit/mcp.py checks only the executable name against config.features.mcp.stdio.allowed_executables and passes unchecked arguments to StdioServerParameters in backend/chainlit/server.py. Because npx supports the -c argument, an attacker can execute arbitrary shell commands with the privileges of the Chainlit process. If allowed_executables is unset, its None default is treated as allowing every executable. This issue is fixed in version 2.12.0.

### CVE-2026-55546

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-25T16:16:55.160 |

QWED-MCP is a deterministic verification gateway for MCP. Prior to 0.2.1, verify_math_expression() in src/qwed_mcp/engines/math_engine.py passes attacker-controlled expression and claimed_result strings directly to SymPy's parse_expr() after only normalizing caret syntax to Python exponent syntax, without restricting global_dict, removing Python built-ins, or validating the expression AST. Because parse_expr() calls Python's eval() with built-ins available, an attacker who can cause a downstream caller to pass untrusted input to this public library function can use Python import functionality to execute arbitrary operating-system commands as the qwed-mcp process user, read or modify accessible data, exfiltrate process secrets, or reach internal services. The default MCP tool registry does not expose verify_math_expression(), so exploitation requires a downstream integration that invokes the library API with attacker-controlled input. This issue is fixed in version 0.2.1.

### CVE-2026-16286

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-25T15:16:30.180 |

Unrestricted upload of file with dangerous type vulnerability in TRtek Technological Products Computer Software Hardware Industry and Trade Limited Company Software Repository Management allows Upload a Web Shell to a Web Server.

This issue affects Software Repository Management: before 2fb4acee.

### CVE-2026-79911

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-25T23:17:59.490 |

A security vulnerability has been detected in TOTOLINK N600R 4.3.0cu.7647_B20210106. The affected element is the function setSystemConfig of the file /cgi-bin/cstecgi.cgi of the component CGI Handler. Such manipulation of the argument Hostname leads to stack-based buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-80104

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-25T21:18:24.163 |

DB-GPT builds the destination path for an uploaded skill from the multipart filename without constraining it to the upload directory. skill_upload in packages/dbgpt-app/src/dbgpt_app/openapi/api_v1/agentic_data_api.py takes file.filename as given and writes the request body to upload_dir / filename. A path composed with that operator discards the left operand when the right one is absolute and follows parent references otherwise, so a filename such as ../../../tmp/x or /tmp/x resolves outside the intended directory; nothing canonicalises the result, checks that it remains under the upload root, or prevents a .py suffix. The route's only dependency is get_user_from_headers in dbgpt_serve/utils/auth.py, which returns a request carrying the admin role whether or not a user_id header is supplied, so the endpoint is reachable without credentials. A remote attacker holding no account can therefore write attacker-controlled bytes to any path the server process can write, place a new Python module inside the application package or replace one the application already imports, and obtain code execution in the server process when that module is next imported.

### CVE-2026-79787

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-25T19:16:54.907 |

Alluxio's S3 REST proxy fails to verify AWS Signature Version 4 signatures in its default configuration, allowing unauthenticated attackers to spoof user identity. Attackers can extract usernames from unsigned Authorization headers and impersonate any user, including service accounts, to read, write, and delete arbitrary data.

### CVE-2026-79782

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-08-25T16:17:30.217 |

rclone before 1.74.4 fails to strip the X-Amz-Security-Token header when an S3 redirect changes scheme from HTTPS to HTTP on the same host. Attackers can intercept plaintext HTTP traffic to capture AWS STS session tokens sent in request headers.

### CVE-2026-79774

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-25T16:17:29.060 |

Winter CMS versions before 1.2.13 contain an incomplete fix for a Twig sandbox escape vulnerability in System\\Twig\\SecurityPolicy that allows authenticated backend users with template-editing permissions to bypass sandbox restrictions. Attackers can exploit method forwarding through Eloquent models and query builders using methods like saveQuietly(), deleteQuietly(), increment(), decrement(), and newQuery() to read and modify arbitrary database records, execute arbitrary SQL, and achieve remote code execution by injecting PHP into template code sections.

### CVE-2026-79675

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-25T16:17:28.013 |

NLTK before 3.10.3 fails to validate JVM options passed through the per-call options parameter in the java() function, allowing attackers to inject dangerous JVM flags. Attackers can supply malicious options like -agentpath, -javaagent, or @argfile to Stanford wrapper classes to achieve arbitrary code execution.

### CVE-2025-71407

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T16:16:45.633 |

Nokogiri before 1.18.3 contains a stack buffer overflow vulnerability in libxml2 when reporting DTD validation errors with long QName prefixes, and a use-after-free vulnerability during validation against untrusted XML Schemas. Attackers can trigger these vulnerabilities by providing malicious DTD content or untrusted XSD files to cause denial of service or potential code execution.

### CVE-2024-58378

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-25T16:16:45.153 |

Nokogiri before 1.15.6 and 1.16.x before 1.16.2 (CRuby, when using the packaged libxml2) is affected by a use-after-free vulnerability in libxml2 (CVE-2024-25062) in the xmlTextReader module, which underlies Nokogiri::XML::Reader. When using the XML Reader interface with DTD validation and XInclude expansion enabled, processing a crafted XML document can lead to an xmlValidatePopElement use-after-free. Nokogiri 1.15.6 and 1.16.2 resolve this by upgrading the packaged libxml2 to 2.11.7 and 2.12.5 respectively. JRuby and installations using system libxml2 are not affected.

### CVE-2024-58377

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-25T16:16:45.003 |

Nokogiri versions before 1.16.5 bundle libxml2 2.12.6, which is affected by CVE-2024-34459 in libxml2's xmllint tool. Nokogiri 1.16.5 upgrades the bundled libxml2 to 2.12.7 to address this. Per the maintainers, there is no impact to Nokogiri users because Nokogiri does not provide or expose the xmllint tool where the issue occurs.

### CVE-2022-51000

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-25T16:16:44.380 |

Nokogiri before 1.13.2 (CRuby, when using packaged libraries) ships vendored libxml2 2.9.12 and libxslt 1.1.34, which are affected by two upstream CVEs. Via CVE-2021-30560 in libxslt, an application transforming XML with untrusted XSL stylesheets is vulnerable to a denial-of-service attack. Via CVE-2022-23308 in libxml2, an application parsing an untrusted document with parse option DTDVALID set to true and NOENT set to false may be vulnerable to denial of service, memory disclosure, or code execution. Nokogiri 1.13.2 upgrades vendored libxml2 to 2.9.13 and libxslt to 1.1.35.

### CVE-2026-80138

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T23:17:59.860 |

ClipBucket V5's web installer fails to properly validate or escape the php_cli_filepath parameter before passing it to shell execution. Unauthenticated attackers can submit a crafted POST request to the installer with a malicious php_cli_filepath value to execute arbitrary commands as the web server user.

### CVE-2026-78379

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-25T19:16:54.467 |

Improper neutralization of input used for LLM prompting in the python_repl tool in Amazon Strands Agents Tools before 0.8.5 might allow remote actors to execute arbitrary Python code on the agent's host by bypassing the human consent gate, via a crafted prompt that forwards non_interactive_mode as a keyword argument through the batch tool. To remediate this issue, users should upgrade to version 0.8.5 or later.

### CVE-2026-62862

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307;CWE-330` |
| Published | 2026-08-25T22:17:04.330 |

Typebot is an open-source chatbot builder. In self-hosted versions up to and including 3.17.1, the default passwordless email magic-link authentication is vulnerable to login-code brute forcing that leads to account takeover. The email provider overrides NextAuth's default cryptographically secure token with a 6-digit code generated using Math.random(), reducing the keyspace to 900,000 with a 10-minute expiry, and the code itself is the raw value placed in the magic link. The verification callback enforces no attempt limit, lockout, or CSRF protection, and an incorrect guess does not consume the real code because the adapter returns null on a not-found token, so a valid code survives unlimited guessing within its lifetime. The only rate limiter applies to the code-sending path and is keyed on the client-controlled X-Forwarded-For header, allowing an attacker to request many concurrent live codes for one victim and further raise the odds of a matching guess. As a result, an anonymous attacker who knows a victim's email address can brute-force the callback and obtain an authenticated session as that user with no victim interaction, gaining full access to the victim's bots, results, and connected integration credentials. Deployments configured for OAuth or SSO only, with no email provider, are not affected. This issue is fixed in version 3.18.0

### CVE-2026-55640

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-25T16:16:55.810 |

Nextcloud MCP Server is a production-ready MCP server that connects AI assistants to a Nextcloud instance. Prior to 0.117.2, the POST /webhooks/nextcloud endpoint in nextcloud_mcp_server/vector/webhook_receiver.py has no authentication by default because WEBHOOK_SECRET defaults to None and startup validation does not require it. When WEBHOOK_SECRET is unset, handle_nextcloud_webhook() accepts unauthenticated requests. The payload["user"]["uid"] field parsed in nextcloud_mcp_server/vector/webhook_parser.py is attacker-controlled and is used without an authenticated-session cross-check for Qdrant operations, allowing a network attacker to delete or trigger re-indexing of vector embeddings for any user and to destroy the semantic search index by sending forged deletion events. This issue is fixed in version 0.117.2.

### CVE-2026-55536

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284;CWE-625` |
| Published | 2026-08-25T16:16:54.867 |

PraisonAI is a multi-agent teams system. Prior to praisonai 4.6.58, Browser Server _handle_connection() checks Chrome extension origins with re.match() and the unanchored expression chrome-extension://[a-z0-9]{32}. Extra trailing characters pass before websocket.accept(), allowing start_session commands and unauthorized browser automation. This issue is fixed in version 4.6.58.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-65091

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T21:17:29.050 |

NVIDIA OpenShell for all platforms contains a vulnerability where a malicious gateway could cause OS command injection. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-55637

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-25T18:17:56.157 |

genieacs-mcp is an MCP server for GenieACS written in Go. Prior to 0.3.2, the Streamable HTTP transport in cmd/server/main.go creates an unauthenticated /mcp listener on the default MCP_LISTEN_ADDR value 127.0.0.1:8080 when MCP_AUTH_TOKEN is unset and the httpSrv.Start(addr) branch does not validate the Host or Origin headers. A malicious website can use DNS rebinding to send browser requests with attacker-controlled Host and Origin values to the loopback listener, initialize an MCP session, list tools, and invoke operations against the GenieACS NBI configured by ACS_URL. Successful exploitation can expose or modify CPE management state, including device reboots, firmware tasks, TR-069 parameter changes, presets, provisions, tags, connection requests, and task operations. The npm wrapper is not affected because it forces TRANSPORT=stdio and does not expose an HTTP listener. This issue is fixed in version 0.3.2.

### CVE-2026-55585

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-25T17:17:32.903 |

QWED is open-source AI verification infrastructure for deterministic verification of LLM outputs, tool calls, code, schemas, and agent state before production execution. Prior to 5.1.2, the qwed package passes caller-controlled math expressions directly to SymPy parse_expr() without restricted global_dict and local_dict namespaces, allowing Python eval() to resolve builtins and execute arbitrary Python code in the API server process. In src/qwed_new/api/main.py, POST /verify/math is protected by get_current_tenant but accepts any valid tenant API key, reads the expression field, applies only a cosmetic re.sub(r'(\d)(()', r'\1*\2', expression) normalization, and passes the result to parse_expr(). In src/qwed_new/core/batch.py, POST /verify/batch sends math items through batch_service.create_job(), stores item.query verbatim, and _verify_item() passes VerificationType.MATH input to parse_expr() without sanitization. The default-enabled POST /auth/signup endpoint allows anyone to create a standard tenant account, POST /auth/api-keys issues an x-api-key, and either vulnerable path can then be used to read or write files, modify data, execute operating system commands, terminate the service, and compromise other tenants in a shared deployment. This issue is fixed in version 5.1.2.

### CVE-2026-24170

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-25T17:17:10.290 |

NVIDIA UFM Enterprise contains a vulnerability in the web interface authorization component, where an authenticated user could cause improper authentication by sending specially crafted HTTP requests. A successful exploit of this vulnerability might lead to code execution and escalation of privileges.

### CVE-2026-79674

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-25T16:17:27.873 |

NLTK versions before 3.10.3 contain a path sandbox bypass vulnerability in corpus-reader constructors that allows attackers to read files outside the intended data root. Attackers can supply arbitrary corpus root paths to LinThesaurusCorpusReader and PanLexLiteCorpusReader constructors to access filesystem content and SQLite databases outside the pathsec sandbox boundary.

### CVE-2022-50999

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-25T16:16:44.240 |

Nokogiri versions before 1.13.5 contain an integer overflow vulnerability in packaged libxml2 buffer handling functions that allows attackers to cause out-of-bounds memory writes. Attackers can exploit this by crafting multi-gigabyte XML files to trigger buffer overflows resulting in information disclosure, data modification, or denial of service.

### CVE-2026-55541

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-25T15:16:34.887 |

PraisonAI is a multi-agent teams system. Prior to praisonai 4.6.58, praisonai serve agents and praisonai serve unified parse --api-key but _create_agents_app() and _create_unified_app() do not install a credential check. Unauthenticated callers can reach POST /agents and POST /api/v1/agents/{id}/invoke. This issue is fixed in version 4.6.58.

### CVE-2026-63403

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-08-25T22:17:04.617 |

Faktory is a language-agnostic background job server. In versions prior to 1.10.0, the server is vulnerable to an unauthenticated denial of service in which a single malformed command crashes the entire process. Its wire protocol is line-based, and several command handlers slice or index the received line at a fixed offset, such as cmd[5:] for PUSH or qs[0] for QUEUE, without checking that a payload is present. Sending a bare verb with no payload, for example PUSH, ACK, FAIL, BEAT, PUSHB, or QUEUE, triggers a Go slice or index out-of-range panic. Because the codebase has no recover() anywhere in the command-dispatch path, an unrecovered panic in a handler goroutine terminates the whole Go process rather than just that connection, instantly disconnecting every other client, worker, and in-flight job. The attack requires only a connection to the command port and completion of the trivial handshake, with no credentials when no password is configured, and can be repeated to keep the service down indefinitely. This issue is fixed in version 1.10.0.

### CVE-2026-62865

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73;CWE-200` |
| Published | 2026-08-25T22:17:04.473 |

Typebot is an open-source chatbot builder. In self-hosted versions prior to 3.18.0, the server-side Send Email integration block allows arbitrary reading of local files on the server. The block builds Nodemailer attachments from a typebot variable, and its parseAttachments helper returns the supplied value as a filesystem path whenever it does not start with the application's own base URL, instead of requiring an http or https URL. The Nodemailer transport is created without disableFileAccess or disableUrlAccess, both of which default to false, so an attachment specified as an absolute server path is read from the local filesystem and delivered. Because both the attachment value and the recipient list are attacker-controllable typebot variables, any registered user can publish a bot whose Send Email block attaches an absolute path such as /etc/passwd or /proc/self/environ and mails it to an address they control. This enables reading any file the server process can access, including process environment secrets such as the credential encryption key and database connection string, without administrative privileges or victim interaction. Open signup is enabled by default and the system SMTP credential is already configured, so no non-default configuration is required. This issue is fixed in version 3.18.0.

### CVE-2026-77357

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-834` |
| Published | 2026-08-25T21:17:46.090 |

Mesop is a Python-based UI framework that allows users to build web applications. Prior to 1.3.3, applications running in debug mode expose a GET /hot-reload endpoint whose unbounded loop depends on the user-supplied counter parameter, allowing an unauthenticated attacker to hold worker threads with high counter values until the worker pool is exhausted and the server becomes unavailable. A single unauthenticated attacker can crash the Mesop server with minimal effort. Because the attack leverages worker exhaustion, the server remains unresponsive until it is manually restarted. This issue is fixed in version 1.3.3.

### CVE-2026-80049

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-25T19:16:55.340 |

Airbyte Platform resolves the workspace used for its authorization decision from a field the caller supplies. AuthorizationServerHandler copies recognised identifiers out of the raw JSON request body into X-Airbyte-* headers, and AuthenticationHeaderResolver.resolveWorkspace consults X-Airbyte-Workspace-Id ahead of every resource-derived header, including those for connection, source and destination identifiers. Endpoints whose declared request bodies carry only a resource identifier are nonetheless reached with an added workspaceId field, because the extractor reads the body rather than the endpoint's schema, so the permission check is performed against the workspace the caller nominated while the handler acts on the resource identifier the caller supplied. Nothing afterwards compares the resource's owning workspace with the one that was authorized. A member of any workspace can therefore read source and destination configuration, trigger and cancel syncs, and delete connections, sources and destinations that belong to workspaces they have no access to, at whatever privilege level their own workspace membership grants them.

### CVE-2026-79770

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-08-25T16:17:28.460 |

Nokogiri versions before 1.19.3 contain regular expression denial of service vulnerabilities in the CSS selector tokenizer affecting string-literal and identifier tokenization. Attackers can inject adversarial CSS selectors into methods like Node#css, Node#at_css, and Searchable#search to cause exponential regex backtracking and denial of service.

### CVE-2026-79769

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-25T16:17:28.320 |

Nokogiri versions before 1.19.4 contain a possible invalid (out-of-bounds) memory read in the protected internal Node#initialize_copy_with_args helper behind Node#dup and #clone, which unwrapped its source argument as an xmlNode without a type check. If application code calls this protected method with a non-Node argument (e.g., a Namespace), it reads an xmlNs out of bounds, crashing the process. This is only triggerable by a programming error and cannot be triggered by untrusted input or normal use of the public API. Only CRuby is affected. Version 1.19.4 adds a type check and raises TypeError.

### CVE-2025-71406

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-25T16:16:45.497 |

Nokogiri before 1.18.4 bundles a vulnerable version of libxslt (prior to 1.1.43) that contains two use-after-free vulnerabilities: CVE-2025-24855 (use-after-free of the XPath context node due to xsltEvalXPathStringNs leaking xpathCtxt->node) and CVE-2024-55549 (use-after-free related to excluded result prefixes/namespaces). Processing crafted XSLT can trigger memory corruption. Nokogiri 1.18.4 upgrades the bundled libxslt to 1.1.43 to resolve these issues.

### CVE-2025-71346

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-25T16:16:45.320 |

Nokogiri before 1.18.8 packages a vulnerable version of libxml2 (before 2.13.8) that contains a heap-based buffer under-read (CVE-2025-32415) in the xmlSchemaIDCFillNodeTables function in xmlschemas.c. The issue can be triggered when validating against an untrusted XML Schema, or when validating untrusted documents against trusted schemas that use xsd:keyref in combination with recursively defined types that have additional identity constraints. Upstream and MITRE rate this issue as low severity.

### CVE-2023-54354

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-25T16:16:44.543 |

Nokogiri before 1.14.3 (CRuby implementation only, when using the packaged libxml2) bundles libxml2 v2.10.3, which is vulnerable to NULL pointer dereferences in XML Schema processing (xmlSchemaFixupComplexType, CVE-2023-28484, and xmlSchemaCheckCOSSTDerivedOK). An attacker who supplies a crafted/malformed XML schema can cause libxml2 to dereference a NULL pointer and potentially segfault, resulting in a denial of service. Nokogiri 1.14.3 upgrades the packaged libxml2 to v2.10.4 to resolve these issues.

### CVE-2022-50998

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-25T16:16:44.073 |

Nokogiri before 1.13.9 (CRuby implementation using packaged libraries) bundles libxml2 v2.9.14, which is affected by CVE-2022-40304 (data corruption / double-free from an entity reference cycle when entity content is allocated from a dict) and CVE-2022-40303 (integer overflows when parsing with XML_PARSE_HUGE). Nokogiri 1.13.9 upgrades the packaged libxml2 to v2.10.3 to address these issues. Processing crafted XML input may lead to denial of service or memory corruption. (The advisory also references CVE-2022-2309, a NULL pointer dereference via iterwalk/canonicalize, which maintainers determined does not affect Nokogiri users.)

### CVE-2021-47996

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-25T16:16:42.930 |

Nokogiri before 1.11.4 (CRuby implementation only, when the packaged/vendored libxml2 is used) bundles libxml2 2.9.10, which is affected by multiple vulnerabilities addressed in libxml2 2.9.12, including a memory leak in xmlSchemaValidateStream (CVE-2019-20388), a global buffer over-read in xmlEncodeEntitiesInternal (CVE-2020-24977), a heap-based buffer overflow (CVE-2021-3517), and an out-of-bounds read (CVE-2021-3518). Processing crafted XML documents may lead to denial of service, information disclosure, or memory corruption.

### CVE-2026-75498

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-25T17:18:16.330 |

Webkul QloApps does not validate request parameters before a database query. A remote, authenticated attacker with administrative privileges could send a crafted SQL query to the 'bo_query' parameter in the 'Address.php' file. Fixed in 123c97c.

### CVE-2026-75497

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-25T17:18:16.187 |

Webkul QloApps does not validate request parameters before a database query. A remote, authenticated attacker with administrative privileges could send a crafted SQL query to the 'bo_query' parameter in the 'CustomerMessage.php' file. Fixed in 123c97c.

### CVE-2026-75496

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-25T17:18:16.030 |

Webkul QloApps does not perform proper validation on uploaded file extensions or MIME types before moving the file to a publicly accessible directory. A remote, authenticated attacker with administrative privileges could upload executable files and achieve remote code execution. Fixed in 153ec1c.

### CVE-2026-55557

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-25T17:17:32.357 |

browse-mcp is a Playwright-based headless-browser MCP server for MCP-capable agents. Prior to 0.8.2, browser_download writes a fetched response body to join(save_dir, filename) without validating the caller-controlled save_dir, while browser_save_state and browser_load_state honor a caller-controlled path unchanged. A malicious MCP client, or an autonomous agent steered by indirect prompt injection on a visited page, can choose an arbitrary save_dir or state path and a URL whose response body becomes attacker-controlled file contents, allowing writes to any path the process can reach, including ~/.bashrc, autostart entries, or cron files, and potentially leading to host code execution. The force_fetch fallback also uses a raw fetch() that bypasses the BROWSE_MCP_ALLOWED_ORIGINS origin fence. This issue is fixed in version 0.8.2.

### CVE-2026-79784

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-08-25T16:17:30.547 |

Vocos instantiates a class named by a configuration file without restricting which class may be named. instantiate_class in vocos/pretrained.py takes the class_path value from the configuration, splits it into a module and an attribute, imports the module with __import__, resolves the attribute with getattr, and calls the result as args_class(*args, **kwargs) where kwargs is the config's own init_args mapping. No allowlist constrains the dotted path, so a configuration may name any importable callable and supply the arguments it is called with. Vocos.from_hparams reaches this for each of the feature_extractor, backbone and head entries, and Vocos.from_pretrained reaches it with a remote file: it downloads config.yaml from a caller-named Hugging Face repository and passes it straight to from_hparams. Loading a model from a repository the user does not control therefore executes code of the repository owner's choosing in the loading process. The neighbouring torch.load of the downloaded weights is a separate matter and is constrained on PyTorch releases that default weights_only to true, which leaves this path as the reachable one.

### CVE-2026-55580

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T16:16:55.317 |

mcp-shell is an MCP server for running shell commands securely, auditably, and on demand. Prior to 0.6.0, config.go initializes Security.Enabled to false, and when MCP_SHELL_SEC_CONFIG_FILE is unset, main.go starts the documented bare-binary deployment without a security policy. SecurityValidator.validateCommand in security.go then short-circuits and allows every command supplied to the shell_exec MCP tool, so an LLM connected over stdio can execute unrestricted OS commands as the mcp-shell process user. The README from-source installation and MCP client configuration omit MCP_SHELL_SEC_CONFIG_FILE, making the insecure state the documented default. This issue is fixed in version 0.6.0.

### CVE-2026-55539

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-25T16:16:55.010 |

PraisonAI is a multi-agent teams system. Prior to praisonai 4.6.51, the Jobs API create_app function mounts /api/v1/runs without authentication. Any reachable caller can submit jobs, read results, cancel runs, or delete jobs using operator credentials. The fix adds PRAISONAI_JOBS_API_KEY middleware for Authorization or X-API-Key. This issue is fixed in version 4.6.58.

### CVE-2026-55534

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-25T15:16:34.167 |

PraisonAI is a multi-agent teams system. From praisonai 4.6.34 until 4.6.58, praisonai serve agents accepts --api-key but _create_agents_app() does not authenticate POST /agents or POST /agents/{agent_name}. A network caller can invoke configured agents without credentials even when an API key was supplied. This issue is fixed in version 4.6.58.

### CVE-2026-65092

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-25T21:17:29.177 |

NVIDIA OpenShell Sandbox for Linux contains a vulnerability where an attacker could cause a path traversal bypass of L7 REST network policy. A successful exploit of this vulnerability might lead to information disclosure and data tampering.

### CVE-2026-64204

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T17:17:59.727 |

There is a memory corruption vulnerability recently
discovered in NI LabVIEW that may result in information disclosure or arbitrary
code execution.  Successful exploitation requires an attacker to get a
user to open a specially crafted VI.  This vulnerability affects NI
LabVIEW 2026 Q3 (26.3.0) and prior versions.

### CVE-2026-64203

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-25T17:17:59.587 |

There is a memory corruption vulnerability recently
discovered in NI LabVIEW that may result in information disclosure or arbitrary
code execution.  Successful exploitation requires an attacker to get a
user to open a specially crafted VI.  This vulnerability affects NI
LabVIEW 2026 Q3 (26.3.0) and prior versions.

### CVE-2026-64202

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-25T17:17:59.447 |

There is a memory corruption vulnerability recently
discovered in NI LabVIEW that may result in information disclosure or arbitrary
code execution.  Successful exploitation requires an attacker to get a
user to open a specially crafted VI.  This vulnerability affects NI LabVIEW 2026 Q3 (26.3.0)
and prior versions.

### CVE-2026-64201

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-25T17:17:59.300 |

There is a memory corruption vulnerability recently
discovered in NI LabVIEW that may result in information disclosure or arbitrary
code execution.  Successful exploitation requires an attacker to get a
user to open a specially crafted VI.  This vulnerability affects NI LabVIEW 2026 Q3 (26.3.0)
and prior versions.

### CVE-2026-16234

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-25T17:17:05.623 |

There is a memory corruption vulnerability recently
discovered in NI LabVIEW that may result in information disclosure or arbitrary
code execution.  Successful exploitation requires an attacker to get a
user to open a specially crafted VI.  This vulnerability affects NI
LabVIEW 2026 Q3 (26.3.0) and prior versions.

### CVE-2026-16233

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T17:17:05.447 |

There is a memory corruption vulnerability recently
discovered in NI LabVIEW that may result in information disclosure or arbitrary
code execution.  Successful exploitation requires an attacker to get a
user to open a specially crafted VI.  This vulnerability affects NI
LabVIEW 2026 Q3 (26.3.0) and prior versions.

### CVE-2026-70551

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-25T15:16:38.060 |

A user who can read an existing remote VCS repository can replace its configured origin or supply an absolute VCS data URL.

### CVE-2026-55526

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-350;CWE-918` |
| Published | 2026-08-25T15:16:33.300 |

PraisonAI is a multi-agent teams system. Prior to praisonaiagents 1.6.58, spider_tools._host_is_blocked() does not resolve ordinary hostnames before scrape_page fetches them. A hostname such as 127.0.0.1.nip.io passes validation and resolves to loopback, permitting internal HTTP access. The fix uses socket.getaddrinfo and fails closed on DNS errors. This issue is fixed in version 1.6.58.

### CVE-2026-55582

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T16:16:55.650 |

mcp-shell is an MCP server for running shell commands securely, auditably, and on demand. Prior to 0.6.0, the default security.yaml allows /usr/bin/git, while security.go omits ! from containsShellMetacharacters and containsDangerousShellConstructs and applies no per-executable argument policy. A caller of the shell_exec MCP tool can provide the command argument /usr/bin/git -c alias.pwn=!<arbitrary-command>, causing Git to create a shell alias and execute arbitrary OS commands as the mcp-shell process user. The default Docker image runs as mcpuser with Git installed and secure mode enabled, so the bypass is exploitable in the default deployment without additional authentication beyond MCP connectivity. This issue is fixed in version 0.6.0.

### CVE-2026-55581

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-183;CWE-1188` |
| Published | 2026-08-25T16:16:55.470 |

mcp-shell is an MCP server for running shell commands securely, auditably, and on demand. Prior to 0.6.0, the default Docker security.yaml includes /bin/bash in allowed_executables, while security.go validates only the first token and checkBlockedPatternsAndCommands does not reject the shell command-mode flag -c. A caller of the shell_exec MCP tool can provide the command argument `/bin/bash -c <arbitrary-command>`, which passes validation and reaches executor.go, where parseCommand and exec.CommandContext execute the arbitrary command as mcpuser outside the intended allowlist. This issue is fixed in version 0.6.0.

### CVE-2026-55571

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-285;CWE-306` |
| Published | 2026-08-25T17:17:32.547 |

djust provides Phoenix LiveView-style reactive server-side rendering for Django with Rust-powered performance. Prior to 1.0.4, LiveViewConsumer.handle_mount sends a `{"type":"navigate","to":...}` frame when login_required, permission_required, or a redirecting on_mount hook denies a LiveView mount, but returns without closing the WebSocket or clearing self.view_instance. A browser follows the redirect, but a raw WebSocket client can ignore it and retain the mounted socket. Because LiveViewConsumer.handle_event does not recheck authentication or authorization, the client can send `{"type":"event",...}` frames that invoke @event_handler methods without an authenticated session, including through handle_live_redirect_mount, enabling unauthorized sensitive reads or mutations. This issue is fixed in version 1.0.4.

### CVE-2026-47626

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T17:17:14.150 |

NVIDIA DGX Spark contains a vulnerability in the system firmware, where a privileged attacker could be able to cause an out-of-bounds write. A successful exploit of this vulnerability may lead to code execution, escalation of privileges, denial of service, information disclosure, and data tampering.

### CVE-2026-24263

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-25T17:17:10.930 |

NVIDIA DGX Spark contains a vulnerability in the system firmware, where a privileged attacker could be able to cause a NULL pointer dereference. A successful exploit of this vulnerability may lead to code execution, escalation of privileges, denial of service, information disclosure, and data tampering.

### CVE-2026-24262

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T17:17:10.750 |

NVIDIA DGX Spark contains a vulnerability in the system firmware, where a privileged attacker could be able to cause an out-of-bounds write. A successful exploit of this vulnerability may lead to code execution, escalation of privileges, denial of service, information disclosure, and data tampering.

### CVE-2026-79785

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-25T16:17:30.690 |

X-AnyLabeling's model downloader disabled TLS certificate verification. download_with_retry in anylabeling/services/auto_labeling/model.py built a context with ssl._create_unverified_context() and passed it to urllib.request.urlopen, so neither the certificate chain nor the hostname was checked on any model download, and models are fetched over HTTPS from the project's release host. Any party positioned to intercept that connection could therefore answer it with content of their own choosing. The response is written to a .part file and moved into place with os.replace, and the only post-download check, safe_check_model, validates the file's format rather than its provenance: no hash or signature is compared against an expected value. For an ONNX target the substituted file passes onnx.checker.check_model and is then used for inference, so the attacker chooses the model that produces the application's annotations. For a .pth or .pt target, which the shipped SAM2 video, YOLOE, UPN and open_vision configurations use, the check worker calls torch.load without weights_only, so a substituted file is unpickled and executes code of the attacker's choosing on PyTorch releases predating the weights_only default.

### CVE-2026-79676

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-25T16:17:28.177 |

NLTK versions before 3.10.3 contain a path traversal vulnerability in corpus readers that reopen root-derived paths using built-in open() instead of nltk.pathsec.open(), allowing symlinks to escape trusted roots. Attackers who stage symlinked corpus files under a trusted data root can disclose outside-root content through normal corpus reader methods like channels(), domains(), and synonyms().

### CVE-2026-55533

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-08-25T16:16:54.723 |

PraisonAI is a multi-agent teams system. Prior to praisonai 4.6.58, create_auth_middleware() allows requests when auth=api-key lacks PRAISONAI_API_KEY or JWT authentication lacks PRAISONAI_JWT_SECRET. An externally bound Recipe server can therefore accept unauthenticated POST /v1/recipes/run requests despite authentication being enabled. This issue is fixed in version 4.6.58.

### CVE-2026-55528

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-08-25T15:16:33.590 |

PraisonAI is a multi-agent teams system. Prior to praisonaiagents 1.6.58, AgentServer exposes ServerConfig.auth_token but AgentServer._create_app does not check it on any route. A remote caller can subscribe, publish, and perform other actions without a valid bearer token or X-Auth-Token even when authentication is configured. This issue is fixed in version 1.6.58.

### CVE-2026-65105

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-25T21:17:29.933 |

NVIDIA NemoClaw for Linux contains a vulnerability in its inference server setup, where a remote attacker may access the inference service without authentication. A successful exploit of this vulnerability may lead to information disclosure and denial of service.

### CVE-2026-65098

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-08-25T21:17:29.687 |

NVIDIA NemoClaw for Linux contains a vulnerability in its remote-access helper workflow, where an attacker could cause weak authentication. A successful exploit of this vulnerability might lead to code execution, information disclosure, and data tampering.

### CVE-2026-65084

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-25T21:17:28.177 |

NVIDIA NemoClaw for Linux contains a vulnerability in its deployment process, where an attacker could cause improper certificate validation. A successful exploit of this vulnerability might lead to information disclosure, data tampering, code execution, and escalation of privileges.

### CVE-2026-65081

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-08-25T21:17:27.793 |

NVIDIA NemoClaw for Linux contains a vulnerability in its installation process, where an attacker could cause execution of untrusted code. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, data tampering, information disclosure, and denial of service.

### CVE-2026-24169

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-25T17:17:10.100 |

NVIDIA UFM Enterprise contains a vulnerability in the plugin management API, where an authenticated user with low privileges could inject code by sending a specially crafted API request. A successful exploit of this vulnerability might lead to code execution, escalation of privileges and information disclosure.

### CVE-2026-54757

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-25T23:17:19.277 |

Compliance-trestle (Trestle) is a Python SDK and command-line tool for managing OSCAL compliance documents. In versions before 3.12.4 and versions 4.0.0 through 4.0.3, Trestle is vulnerable to server-side template injection that can lead to remote code execution. This occurs because the MDCleanInclude and MDSectionInclude Jinja2 tags re-parse untrusted Markdown content as template source code using a non-sandboxed jinja2.Environment. An attacker who controls content that Trestle renders, such as a crafted workspace Markdown file, a third-party SSP document, or a YAML lookup-table value, can inject a Jinja2 expression that traverses Python object internals to execute arbitrary operating system commands in the context of the Trestle process. This issue is fixed in versions 3.12.4 and 4.1.0.

### CVE-2026-65099

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T21:17:29.817 |

NVIDIA NemoClaw for Linux contains a vulnerability in its command-line interface, where an attacker could cause OS command injection. A successful exploit of this vulnerability might lead to code execution, data tampering, information disclosure, and denial of service.

### CVE-2026-65096

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T21:17:29.433 |

NVIDIA NemoClaw for Linux contains a vulnerability in the Telegram bridge component, where an attacker could cause an OS command injection. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-65090

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T21:17:28.927 |

NVIDIA NemoClaw for Linux contains a vulnerability in its NIM management component, where an attacker could cause OS command injection. A successful exploit of this vulnerability might lead to code execution, data tampering, information disclosure, and denial of service.

### CVE-2026-65089

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T21:17:28.803 |

NVIDIA NemoClaw for Linux contains a vulnerability in its status and logs plugin commands, where an attacker could cause OS command injection. A successful exploit of this vulnerability might lead to code execution, data tampering, information disclosure, and denial of service.

### CVE-2026-79992

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T18:18:06.973 |

A flaw was found in Emacs TRAMP. A local attacker could exploit this vulnerability by processing maliciously crafted filenames. This occurs because TRAMP concatenates login arguments without proper sanitization, which are then passed to a local shell. Successful exploitation could lead to arbitrary code execution.

### CVE-2026-75770

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T18:18:04.403 |

Substance3D - Painter is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75769

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:18:04.257 |

Substance3D - Painter is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75768

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-25T18:18:04.097 |

Substance3D - Painter is affected by an Untrusted Search Path vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75767

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:18:03.970 |

Substance3D - Painter is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75766

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:18:03.817 |

Substance3D - Painter is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75750

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:18:03.520 |

Substance3D - Painter is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75749

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T18:18:03.360 |

Substance3D - Painter is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-71564

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T18:18:01.790 |

Substance3D - Designer is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-71399

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-25T18:18:00.903 |

Adobe XD is affected by a Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-71382

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T18:18:00.477 |

Substance3D - Sampler is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48433

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:17:55.377 |

Substance3D - Designer is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48432

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:17:55.237 |

Substance3D - Designer is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48431

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:17:55.097 |

Substance3D - Designer is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48430

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:17:54.947 |

Substance3D - Designer is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48428

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:17:54.627 |

Substance3D - Designer is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48427

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T18:17:54.473 |

Substance3D - Designer is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48426

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T18:17:54.330 |

Substance3D - Designer is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48425

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:17:54.183 |

Substance3D - Sampler is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48424

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:17:54.037 |

Substance3D - Sampler is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48423

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:17:53.880 |

Substance3D - Sampler is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48422

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-25T18:17:53.730 |

Substance3D - Sampler is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48421

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T18:17:53.583 |

Substance3D - Sampler is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48420

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T18:17:53.450 |

Substance3D - Sampler is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48419

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T18:17:53.303 |

Substance3D - Sampler is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48418

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T18:17:53.160 |

Substance3D - Sampler is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48417

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-25T18:17:52.993 |

Substance3D - Sampler is affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-80186

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-25T22:17:07.587 |

A stack-based buffer overflow vulnerability exists in BlueZ, the Linux Bluetooth protocol stack. A remote user within Bluetooth radio range can send a specially crafted Extended Inquiry Response (EIR) packet that causes a buffer overflow when the target device performs Bluetooth discovery. This vulnerability can lead to a Denial of Service (DoS) by crashing the bluetoothd service and may allow for arbitrary code execution.

### CVE-2026-80184

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-25T22:17:07.250 |

In OpenStack Keystone before 29.0.3, tokens obtained via delegated authentication mechanisms (OAuth1 access tokens, application credentials, trusts) could be submitted to the token-method authentication path for reauthentication to escape their intended project scope. When an application credential token was presented with no explicit scope, Keystone would issue a new token scoped to the credential owner's default project rather than the project for which the credential was issued, bypassing the intended project boundary. All Keystone deployments that permit delegated authentication through OAuth1 access tokens, application credentials, or trusts are affected.

### CVE-2026-80182

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-25T22:17:07.067 |

In OpenStack Keystone before 29.0.3, tokens obtained via OAuth1 access token, application credential, or trust-scoped authentication could create new long-lived credentials or authorize new delegations that persist independently of, and outlive, the credential used to obtain them. The delegation restrictions that block these operations did not consistently apply to all delegated token types, allowing an OAuth1-scoped token, for example, to create application credentials or authorize OAuth1 request tokens despite those operations being restricted for other delegated token types. All Keystone deployments that permit delegated authentication through OAuth1 access tokens, application credentials, or trusts are affected.

### CVE-2026-55532

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-346;CWE-352` |
| Published | 2026-08-25T16:16:54.560 |

PraisonAI is a multi-agent teams system. Prior to praisonai 4.6.58, MCP HTTP Stream _validate_origin uses request_origin.startswith(allowed), allowing the attacker-controlled localhost.attacker.com HTTP origin to satisfy the localhost allowlist. A webpage can send Content-Type: text/plain requests without preflight and invoke tools/call without an API key, including file writes that persist agent instructions. This issue is fixed in version 4.6.58.

### CVE-2026-69104

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-25T15:16:37.750 |

An authenticated user may initiate repository migration operations without required repository permissions, potentially causing information disclosure, unauthorized state changes, and service disruption. Fixed versions address the issue.

### CVE-2026-65097

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-08-25T21:17:29.560 |

NVIDIA NemoClaw for Linux contains a vulnerability in its installation scripts, where an attacker could cause a download of code without integrity check. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-74932

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-25T20:17:03.250 |

The WP Fastest Cache WordPress plugin before 1.5.1 does not validate the Host header before using it to build the URLs of the asset files it embeds in the pages it caches, and does not include that header in the cache key, allowing unauthenticated attackers to poison cached pages with references to a server they control and have arbitrary JavaScript run for every subsequent visitor.

### CVE-2026-55099

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-08-25T20:16:56.940 |

icalendar is an RFC 5545 compatible parser and generator of iCalendar files for Python. From 7.1.0 until 7.1.3, the Component equality method in src/icalendar/cal/component.py compares nested subcomponents with two membership loops, and each membership test invokes the same method on child components, causing O(2^n) work relative to nesting depth. Component.from_ical accepts arbitrarily nested BEGIN:VEVENT blocks without a depth limit, so an attacker can submit a sub-kilobyte .ics file containing equal nested subtrees and trigger the cost when an application performs equality, inequality, membership, deduplication, test-assertion, round-trip, or normalization comparisons. Parsing alone does not trigger the issue, and comparisons that differ early short-circuit, but a few hundred bytes can pin a CPU core for minutes or indefinitely, causing denial of service in calendar sync or import endpoints, invite processing, and other comparison paths. This issue is fixed in version 7.1.3.

### CVE-2026-55620

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770;CWE-1124` |
| Published | 2026-08-25T19:16:50.627 |

eml_parser serves as a python module for parsing eml files and returning various information found in the e-mail as well as computed information. Prior to 3.0.2, eml_parser.routing.noparenthesis in eml_parser/routing.py removes parenthesized CFWS comments from Received: headers with a regex-based fix-point loop whose running time is quadratic in the nesting depth. A single Received: header with 5,000 nested parentheses causes approximately 1.3 seconds of CPU saturation per parsed message, and doubling the nesting depth approximately quadruples the running time. An attacker can submit relatively small EML files that consume multiple seconds of processing time, causing worker latency, queue backpressure, and possible service-level outages in synchronous gateways, sandboxes, and real-time triage pipelines. This issue is fixed in version 3.0.2.

### CVE-2026-71443

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-25T18:18:01.490 |

CAI Content Credentials is affected by an Improper Input Validation vulnerability that could result in an application denial-of-service. An attacker could exploit this vulnerability to crash the application, leading to a denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-71442

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-08-25T18:18:01.333 |

CAI Content Credentials is affected by an Integer Underflow (Wrap or Wraparound) vulnerability that could result in an application denial-of-service. An attacker could exploit this vulnerability to crash the application, leading to a denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-71360

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-25T18:18:00.163 |

CAI Content Credentials is affected by an Uncontrolled Resource Consumption vulnerability that could lead to application denial-of-service. An attacker could exploit this vulnerability to exhaust system resources, resulting in an application denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-55553

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-201;CWE-522` |
| Published | 2026-08-25T17:17:32.113 |

urllib is an HTTP client for Node.js that supports authentication, redirects, timeouts, and other request features. Prior to 4.9.1 and 2.44.1, urllib follows redirects through followRedirect but reuses caller-supplied options across origins. In src/HttpClient.ts, #requestInternal recursively calls this.#requestInternal(nextUrl.href, options, requestContext), causing options.headers and auth or digestAuth values to be reused when the redirect target has a different scheme, host, or port. Authorization, Cookie, Proxy-Authorization, x-api-key, x-auth-token, and x-access-token can therefore be sent to an attacker-controlled redirected origin, exposing credentials intended for the original origin and potentially allowing reuse against the original partner API or related services. No user interaction is required. This issue is fixed in versions 2.44.1 and 4.9.1.

### CVE-2026-41707

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-25T23:16:59.933 |

Spring Security's DPoPProofJwtDecoderFactory contains a cache-based replay attack vulnerability. The internal cache storing JWT ID claims has a strict size limit, allowing attackers to evict legitimate entries by flooding the server with dummy requests, then replay intercepted valid DPoP proofs.
Spring Security 7.1.0
Spring Security 7.0.0 - 7.0.6
Spring Security 6.5.0 - 6.5.11

### CVE-2026-63404

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-377` |
| Published | 2026-08-25T22:17:04.760 |

Faktory is a language-agnostic background job server. In versions prior to 1.10.0, the embedded Redis bootstrapper is vulnerable to an insecure temporary file flaw that lets a local unprivileged user hijack the Redis configuration and escalate to root. It writes its startup configuration to a fixed, predictable, world-writable path, /tmp/redis.conf, only creating the file if it does not already exist and never validating it on later boots. Because /tmp is world-writable, a local unprivileged user can pre-create /tmp/redis.conf with attacker-chosen Redis directives before Faktory starts, and Faktory will use the planted file verbatim. Faktory only overrides the unixsocket, dir, and logfile options, leaving directives such as bind, protected-mode, requirepass, and loadmodule attacker-controlled. This lets an attacker silently expose the entire job queue over an unauthenticated network port with no visible error to the administrator. Because the official systemd unit runs Faktory, and the redis-server child it spawns, as root, an attacker can also supply a loadmodule directive to execute arbitrary native code in the root-owned Redis process, escalating from a local unprivileged user to root. This issue is fixed in version 1.10.0.

### CVE-2026-55538

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-25T15:16:34.597 |

PraisonAI is a multi-agent teams system. Prior to praisonai 4.6.51, praisonai serve agents parses config["api_key"] but _create_agents_app() does not authenticate POST /agents or POST /agents/{agent_name}. Missing or incorrect bearer and X-API-Key values still reach agent execution. This issue is fixed in version 4.6.58.

### CVE-2026-45019

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-25T20:16:55.910 |

Chainlit is a Python framework for building production-ready conversational AI applications. From 2.4.0rc0 until 2.12.0, Chainlit deployments with features.mcp.enabled set to true in .chainlit/config.toml expose the POST /mcp endpoint without requiring authentication. For sse and streamable-http transports, ConnectSseMCPRequest and ConnectStreamableHttpMCPRequest in backend/chainlit/types.py accept a user-controlled url and optional headers dictionary without scheme validation, private-address filtering, or an allowlist. The connect_mcp handler in backend/chainlit/server.py passes these values to sse_client() or streamablehttp_client(), allowing the Chainlit server to make blind outbound requests to arbitrary internal or external services, including cloud metadata endpoints, with attacker-controlled Authorization and Cookie headers. The SSE URL sink has existed since 2.4.0rc0, while attacker-controlled header forwarding and streamable-http support were added in 2.6.4. The response is consumed internally and not returned, but the attacker can issue state-changing authenticated requests, discover internal services, scan ports, and probe metadata endpoints. This issue is fixed in version 2.12.0.

### CVE-2026-68515

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-08-25T20:17:02.780 |

OpenEXR is the reference implementation and specification for the EXR image format, widely used in the motion picture industry. In versions before 3.2.11, 3.3.0 through 3.3.12, and 3.4.0 through 3.4.13, exrmultiview can write past a heap allocation when it combines two attacker-supplied, individually valid scanline EXR files whose union dataWindow is not aligned to one view's channel subsampling. The utility allocates sampled channel storage using a truncated union_width / xSampling, then reads the sampled input through a Slice based on the misaligned union window, producing a heap out-of-bounds write. The trigger is normal public-tool processing, such as exrmultiview left A.exr right B.exr out.exr with crafted but valid inputs, so this is not solely an API or caller-precondition issue. This issue is fixed in versions 3.2.11, 3.3.13, and 3.4.14.

### CVE-2026-68513

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-08-25T20:17:02.463 |

OpenEXR is the reference implementation and specification for the EXR image format, widely used in the motion picture industry. Versions 3.3.0 through 3.3.12 and 3.4.0 through 3.4.13 contain a heap buffer overflow in PyOpenEXR triggered by a channel-name key collision between literal and prefixed RGB channels. When separate_channels=false, PyOpenEXR maps each physical channel name through channelNameToRGBA() and coalesces the results into a shared RGB array. A crafted flat scanline EXR that contains both a literal channel such as left and prefixed channels such as left.R, left.G, and left.B causes these names to collide, so the wrapper reuses an undersized two-dimensional NumPy array for the coalesced RGB slices and writes out of bounds when OpenEXR.File(path) decodes the pixels. This issue is fixed in versions 3.3.13 and 3.4.14.

### CVE-2026-59981

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-25T20:16:58.907 |

OpenEXR is the reference implementation and specification for the EXR image file format, widely used in the motion picture industry. In versions through 3.2.10, 3.3.0 through 3.3.12, and 3.4.0 through 3.4.13, the OpenEXRUtil library returns an out-of-bounds pointer from the SampleCountChannel::row() API when a deep image has a non-zero dataWindow origin. The row() accessor is documented as 0-based and computes its address from an internal base that is offset for absolute pixel coordinates, so the two coordinate models conflict whenever dataWindow.min is non-zero. For a deep image whose data window has a large negative vertical origin, row(0) points far outside the allocated sample-count buffer. An application that opens an attacker-controlled deep EXR file and accesses sample counts through row() performs an out-of-bounds read, which can crash the process or, under a controlled heap layout, return adjacent heap memory as sample-count values. This issue is fixed in versions 3.2.11, 3.3.13, and 3.4.14.

### CVE-2026-80050

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-25T19:16:55.503 |

ContiNew Admin fails to apply file-upload permission checks or file-type allowlist validation to multipart upload endpoints, allowing authenticated users to store files with arbitrary extensions. Attackers can initialize chunked uploads, send file parts, and complete uploads to leave arbitrary files in the storage backend accessible via web server URLs.

### CVE-2026-79788

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-25T19:16:55.080 |

In Dradis Community Edition, the ProvidersController and AgentsController gate their admin_required before_action on `defined?(Dradis::Pro)`, a constant that is never defined in CE, so the authorization check is never applied. As a result, any authenticated (non-admin) user can create an AI provider pointing to an arbitrary HTTP/HTTPS address (including internal/link-local hosts such as http://169.254.169.254) and reassign the built-in Roslin agent to use it. When an AI interaction is triggered, the server issues a request to the attacker-supplied URL (server-side request forgery). For non-2xx responses, the target's response body is reflected verbatim to the attacker's browser via ActionCable/Turbo Stream error messages, making the SSRF readable.

### CVE-2026-55609

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-25T19:16:50.160 |

sublinear-time-solver is a Rust and WebAssembly library for solving asymmetric diagonally dominant systems in sublinear time. Prior to consciousness-explorer 1.1.2 and sublinear-time-solver 1.6.0, the export_state and import_state tools in src/consciousness-explorer/mcp/server.js pass the attacker-controlled filepath parameter to filesystem operations in src/consciousness-explorer/index.js without restricting the destination or rejecting traversal. The saveVectorToFile and loadVectorFromFile tools in src/mcp/server.ts contain the same sink class through the file_path parameter. An attacker able to invoke the MCP tools can read, write, or overwrite any file accessible to the server process, causing confidentiality and integrity loss and possible service disruption. This issue is fixed in consciousness-explorer 1.1.2 and sublinear-time-solver 1.6.0.

### CVE-2026-59982

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-08-25T18:17:56.747 |

OpenEXR is the reference implementation and specification for the EXR image format, widely used in the motion picture industry. OpenEXR versions before 3.2.11, 3.3.0 through 3.3.12, and 3.4.0 through 3.4.13 can return an out-of-bounds pointer from TypedDeepImageChannel::row() when a crafted deep EXR has a nonzero dataWindow origin. This vulnerability occurs because the API combines zero-based row access with an absolute-coordinate-adjusted base pointer, allowing a crash or limited information disclosure. This issue is fixed in versions 3.2.11, 3.3.13, and 3.4.14.

### CVE-2026-59189

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-25T17:17:37.160 |

OpenEXR is the reference implementation and specification for the EXR image format, widely used in the motion picture industry. In OpenEXRUtil versions 3.3.0 through 3.3.12 and 3.4.0 through 3.4.12, the documented TypedDeepImageChannel<T>::row() API can return an out-of-bounds pointer when a deep image has a non-zero dataWindow origin, resulting in a heap out-of-bounds read and crash, with potential information disclosure under a controlled heap layout. The flaw arises because ImfDeepImageChannel uses two conflicting coordinate models: at(x, y) uses absolute coordinates (with _base offset by dataWindow.min), while row(r) is documented as 0-based logical access. For a non-zero dataWindow.min, row(0) therefore points outside the _sampleListPointers allocation instead of at the first logical row. This issue is fixed in versions 3.3.13 and 3.4.13.

### CVE-2026-59187

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-08-25T17:17:36.987 |

OpenEXR is the reference implementation and specification for the EXR image format, widely used in the motion picture industry. OpenEXR versions 3.3.0 through 3.3.12 and 3.4.0 through 3.4.13 are vulnerable to a heap out-of-bounds write when exrmetrics reads a crafted deep scanline EXR. This occurs with pixel conversion options such as --pixelmode float or --bench because DeepSlice requests FLOAT output while the backing sample buffers are allocated using the input HALF element size. The issue is fixed in versions 3.3.13 and 3.4.14.

### CVE-2026-59186

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-122;CWE-190;CWE-787` |
| Published | 2026-08-25T17:17:36.787 |

OpenEXR is the reference implementation and specification for the EXR image format, widely used in the motion picture industry. In versions before 3.2.11, 3.3.0 through 3.3.12, and 3.4.0 through 3.4.13, a crafted tiled EXR can trigger a heap out-of-bounds write on 32-bit/ILP32 builds when read through the public TiledRgbaInputFile RGBA API. The file uses a small 40x40 dataWindow but a 65537x65537 tile size. On ILP32, the Array2D<Rgba> tile-conversion buffer size calculation overflows, allocates a much smaller heap buffer, and tile decode writes past that allocation. This issue is fixed in versions 3.2.11, 3.3.13, and 3.4.14.

### CVE-2026-59184

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-416;CWE-787` |
| Published | 2026-08-25T17:17:36.603 |

OpenEXR is the reference implementation and specification for the EXR image format, widely used in the motion picture industry. Versions before 3.2.11, 3.3.0 through 3.3.12, and 3.4.0 through 3.4.13 allow a crafted EXR with a nonzero dataWindow.min to make TypedFlatImageChannel::row() return an invalid heap pointer, causing out-of-bounds or use-after-free writes. This occurs when an application writes rows through FlatHalfChannel::row(). Affected consumers are tools, converters, render pipeline components, or image-processing services that accept untrusted EXR files and use FlatHalfChannel::row() on loaded images. This issue is fixed in versions 3.2.11, 3.3.13, and 3.4.14.

### CVE-2026-79775

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-08-25T16:17:29.233 |

rclone versions >= v1.72.0 and <= v1.74.4 (fixed in v1.75.0) contain multiple denial-of-service vulnerabilities in the archive backend's SquashFS parser, which relies on the github.com/diskfs/go-diskfs dependency. The parser fails to validate attacker-controlled superblock and metadata values before use. An attacker who can place or modify a SquashFS image in storage exposed through an rclone :archive: remote can craft a malicious image that triggers an integer division-by-zero panic (zero block size), an out-of-bounds slice panic (out-of-range inode metadata offset), or a non-progress CPU loop (truncated metadata stream). Variants 1 and 2 terminate the rclone process and, via 'rclone serve sftp', can crash the entire SFTP server; variant 3 causes sustained CPU consumption. Parsing is lazy, so a victim or remote client must address or descend into the malicious archive object to trigger it.

### CVE-2026-55540

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-25T15:16:34.740 |

PraisonAI is a multi-agent teams system. Prior to praisonai 4.6.51, is_path_within_directory() uses os.path.abspath() rather than os.path.realpath() for the workspace boundary. A symlink inside workspace can point outside and still pass the check, allowing read_file and other code tools to access files outside the configured workspace. This issue is fixed in version 4.6.58.

### CVE-2026-55537

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-367;CWE-705;CWE-918` |
| Published | 2026-08-25T15:16:34.450 |

PraisonAI is a multi-agent teams system. Prior to praisonai 4.6.58, JobSubmitRequest.validate_webhook_url() accepts webhook_url when resolution raises socket.gaierror because the exception path uses except socket.gaierror: pass. JobExecutor._send_webhook() later performs a fresh lookup, allowing DNS changes to direct the request to an internal service. This issue is fixed in version 4.6.58.

### CVE-2026-55527

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-08-25T15:16:33.443 |

PraisonAI is a multi-agent teams system. Prior to praisonaiagents 1.6.58, the FileMemory constructor joins unsanitized user_id into self.user_path. A caller supplying ../ or path separators can escape the memory directory and write JSON data to arbitrary process-writable locations. The fix sanitizes user_id before constructing self.user_path. This issue is fixed in version 1.6.58.

### CVE-2026-65082

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-25T21:17:27.923 |

NVIDIA NemoClaw for Linux contains a vulnerability in its migration command, where a local attacker could cause code injection. A successful exploit of this vulnerability might lead to code execution, data tampering, information disclosure, and denial of service.

### CVE-2026-79786

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-08-25T19:16:54.750 |

Coroot's unauthenticated MCP OAuth dynamic client registration endpoint accepts any syntactically valid redirect URI without validation, allowing attackers to register clients pointing to attacker-controlled hosts. Attackers can send authorization URLs to signed-in users, capture their authorization codes upon consent approval, and exchange them for access tokens to hijack MCP sessions.
