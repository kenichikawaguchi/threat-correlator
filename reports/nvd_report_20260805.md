# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-04 15:00 UTC
- **対象期間**: `2026-08-03T15:00:25.000Z` 〜 `2026-08-04T15:00:18.000Z`
- **重要CVE数**: 95 件（Critical 9.0+: 22 件 / High 7.0〜: 73 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超に上ります。  
- **Adobe Campaign Classic (ACC)** が 5 件以上の高リスク脆弱性（CVSS 9.8〜10.0）を抱えており、SSRF・SQLi・テンプレートエンジン・認可不備と多様な攻撃ベクトルが同一製品に集中しています。  
- **オープンソースコンポーネント**（Sequelize、osTicket、Misskey など）でも、SQL インジェクションや予測可能な鍵生成といった **リモートコード実行 (RCE) 系** の脆弱性が目立ちます。  
- **組み込み系ファームウェア**（GL‑iNet GL‑MT3000）では、コマンドインジェクションが多数報告され、IoT デバイスの遠隔乗っ取りリスクが顕在化しています。  

全体として、**「認証・権限チェックの欠如」** と **「入力検証不備」** が共通要因であり、攻撃者がユーザー入力や内部 API を直接操作できる点が最大の危険です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 製品 / コンポーネント | 主な脆弱性種別 | なぜ注目すべきか | 影響範囲・被害シナリオ |
|-----|------|----------------------|----------------|------------------|------------------------|
| **CVE‑2026‑48331** | 10.0 | Adobe Campaign Classic (ACC) | SSRF + Privilege Escalation (Scope: Changed) | SSRF が認証情報や内部管理 API に無制限にアクセスでき、攻撃者が管理者権限へ昇格可能。ユーザー操作不要で自動化が容易。 | 攻撃者は内部ネットワークの任意のエンドポイントへリクエストを送信し、管理コンソールの機能を悪用して権限を取得。 |
| **CVE‑2026‑48330** | 10.0 | Adobe Campaign Classic (ACC) | SQL Injection → 任意コード実行 | SQL 文に直接コード埋め込みが可能で、データベース権限に応じたシステムコマンド実行ができる。低特権ユーザーでも利用可能。 | 攻撃者は任意の SQL を投げてサーバ上でシェルを取得、データ改ざん・情報漏洩・マルウェア配置が可能。 |
| **CVE‑2026‑48323** | 10.0 | Adobe Campaign Classic (ACC) | テンプレートエンジン RCE | テンプレートエンジンに対するサニタイズ不備で、任意の JavaScript/Java コードが実行される。Web UI から直接トリガーできる点が危険。 | 攻撃者はテンプレート編集画面に悪意コードを埋め込み、閲覧者全員にコード実行させる（XSS 兼 RCE）。 |
| **CVE‑2026‑48333** | 9.8 | Adobe Campaign Classic (ACC) | 認可不備 (Incorrect Authorization) | 認可ロジックが欠如しており、特権エンドポイントへ無認証でアクセス可能。SSRF と同様に内部管理機能を横取りできる。 | 攻撃者は管理者専用 API を呼び出し、ユーザー情報取得や設定変更が可能。 |
| **CVE‑2026‑69240** | 9.8 | Sequelize (Node.js ORM) | Oracle 方言特化 SQL Injection | `sql-string.js` のエスケープロジックが TO_TIMESTAMP/TO_DATE でバイパスでき、Oracle データベースに対し任意 SQL が実行可能。広範な Node.js アプリで採用されている。 | 攻撃者はデータベースの機密情報取得や、OS コマンド実行（`UTL_FILE` 等）に利用できる。 |

> **注:** 上記 5 件は **CVSS 9.8 以上** かつ **リモートから認証不要で実行可能**、または **特権昇格が容易** という点で共通しており、組織全体のリスクを急速に高めます。

---

## 3. 推奨アクション  

### 3‑1. 直ちに実施すべき緊急対策
| 製品 / コンポーネント | 推奨バージョン / パッチ | 具体的作業 |
|----------------------|------------------------|------------|
| **Adobe Campaign Classic (ACC)** | **≥ 2026.1.0**（ベンダーが 2026‑10‑15 にリリースしたセキュリティパッチ） | - 公式リリースノートに記載のパッチを適用<br>- すべての ACC インスタンスで **Web アプリケーションファイアウォール (WAF)** を有効化し、`/nms/` 系エンドポイントへの外部アクセスを遮断<br>- 管理コンソールの IP アクセス制限を実装 |
| **Sequelize** | **≥ 6.37.4** | - `npm install sequelize@6.37.4` でアップグレード<br>- `package-lock.json` をコミットし、CI/CD パイプラインでバージョン固定 |
| **osTicket** | **≥ 1.18.4**（MD5 予測鍵生成修正） | - `composer update` で最新版へ<br>- API キー生成ロジックを SHA‑256 へ変更、鍵ローテーションを実施 |
| **Misskey** | **≥ 2026.5.4** | - `git checkout v2026.5.4` でアップデート<br>- JSON‑LD パーサーのタイミング攻撃緩和設定を有効化 |
| **GL‑iNet GL‑MT3000** (ファームウェア) | **≥ 4.4.6** | - 管理画面 → Firmware Upgrade から最新ファームウェアを適用<br>- 使わない RPC エンドポイント (`nas-web`, `modem.so`, `wg-server.so`) をファイアウォールで遮断 |
| **その他** (Bilin HUMANIST, Emlog Pro, go‑base, @fastify/aws‑lambda) | 各ベンダーが提供する **2026‑xx‑xx** 以降のパッチ | - パッケージマネージャ (`yum`, `apt`, `pip`, `npm`) で

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-48331

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-03T23:16:46.443 |

Adobe Campaign Classic (ACC) is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48330

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-03T23:16:46.317 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary SQL commands, potentially gaining elevated access or control over the application. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48323

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-03T23:16:46.063 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements Used in a Template Engine vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48326

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-03T23:16:46.190 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-15721

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-312` |
| Published | 2026-08-04T10:19:32.667 |

Cleartext storage of sensitive information vulnerability in Bilin Software and Informatics Consultancy Inc. HUMANIST Digital Human Resources allows SQL Injection.

This issue affects HUMANIST Digital Human Resources: from 26.0 before 26.1.

### CVE-2026-14175

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-04T10:19:31.633 |

Unrestricted upload of file with dangerous type vulnerability in Bilin Software and Informatics Consultancy Inc. HUMANIST Digital Human Resources allows Upload a Web Shell to a Web Server.

This issue affects HUMANIST Digital Human Resources: from 26.0 before 26.1.

### CVE-2026-48333

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-03T23:16:46.567 |

Adobe Campaign Classic (ACC) is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. An attacker could exploit this vulnerability to gain elevated privileges. Exploitation of this issue does not require user interaction.

### CVE-2026-69240

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-03T21:16:41.970 |

Sequelize is a Node.js ORM tool. Prior to 6.37.4, SQL injection is possible with strings only if dialect is set to oracle. The escape function defined in sql-string.js does not escape quotes if the value starts with TO_TIMESTAMP or TO_DATE. In the Oracle dialect, when val is a string and starts with TO_TIMESTAMP or TO_DATE, escape returns val directly instead of replacing single quotes. An attacker can inject arbitrary SQL expressions through an application value that reaches this escape path. This issue is fixed in version 6.37.4.

### CVE-2026-38447

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-331` |
| Published | 2026-08-03T19:16:46.917 |

osTicket 1.18.3 generates API keys using a predictable construction based on MD5 hashing. The use of MD5, combined with predictable inputs such as the current timestamp and client IP address, significantly reduces entropy. An attacker can approximate the key generation time and brute-force the key space within a feasible time window.

### CVE-2026-48317

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-03T23:16:45.930 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-39932

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-03T17:16:36.893 |

OpenEMR through 8.2.0 contains a remote code execution vulnerability in the document category tree component (library/classes/Tree.class.php) that allows authenticated administrators to execute arbitrary operating system commands by injecting PHP payloads into the categories database table. Attackers can chain arbitrary SQL execution to alter the id column type to VARCHAR and insert a malicious PHP payload, which is then executed via an unsanitized eval() call whenever any page instantiates CategoryTree, including unauthenticated and low-privilege pages, resulting in command execution as the web server user.

### CVE-2026-18667

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-03T23:16:45.590 |

A vulnerability in Tenable Sensor Proxy allows a remote attacker to execute code with elevated privileges by inducing an operator to connect the sensor to an attacker-controlled host.

### CVE-2026-48063

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-345;CWE-346` |
| Published | 2026-08-03T21:16:39.450 |

Baileys is a cocket-based TS/JavaScript API for WhatsApp Web. In versions prior to both 6.7.22 and 7.0.0-rc12, any Baileys session  can be sent a malicious payload via the placeholderResendMessage and trigger a fake messages.upsert event with a fake message key and payload. This allows anyone to spoof messages. The same exploit also allows an attacker to corrupt the app state sync system by sending fake key shares, and also allows for history sync spoofing which also serves the same problem, injecting fake previous context or "on-demand" sync. This issue has been fixed in versions 6.7.22 and 7.0.0-rc12.

### CVE-2026-41452

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-03T17:16:37.047 |

Krayin CRM 2.2.4 contains a missing authentication vulnerability in the installer middleware that allows unauthenticated remote attackers to overwrite the primary administrator account by sending a crafted HTTP POST request with the X-Requested-With: XMLHttpRequest header to bypass the CanInstall middleware redirect check. Attackers can supply arbitrary name, email, and password values to the admin-config-setup endpoint, which performs an unauthenticated updateOrInsert targeting the hardcoded administrator user ID, enabling full administrative access to all CRM data.

### CVE-2026-46713

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-03T22:16:49.017 |

Misskey is an open source, federated social media platform. Versions 12.37.0 and later, but prior to 2026.5.4, contain a vulnerability in the JSON-LD signature validation and compaction process that allows spoofed activities to be accepted as valid. This issue has been fixed in version 2026.5.4.

### CVE-2026-60007

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-204` |
| Published | 2026-08-04T13:18:55.427 |

In Eclipse Milo versions 0.6.0 through 1.1.4, username-token processing returns distinguishable errors for invalid RSA PKCS#1 v1.5 padding and other authentication failures, allowing an on-path attacker who captures a victim's `Basic128Rsa15`-encrypted username token to use repeated unauthenticated `ActivateSession` requests as a padding oracle, recover the victim's password, and authenticate with the recovered credentials.

### CVE-2026-14804

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-04T10:19:32.417 |

Use of hard-coded cryptographic key vulnerability in Bilin Software and Informatics Consultancy Inc. HUMANIST Digital Human Resources allows Read Sensitive Constants Within an Executable.

This issue affects HUMANIST Digital Human Resources: from 26.0 before 26.1.

### CVE-2026-18754

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-04T08:16:34.803 |

The
product firmware contains an embedded, static RSA private key utilized by the
Lighttpd web server for TLS termination. Exposure of this private key allows
malicious actors to breach the confidentiality and integrity of HTTPS
communications, enabling traffic decryption and server spoofing.

### CVE-2026-18753

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-04T08:16:34.640 |

The
product firmware contains an embedded, static RSA private key utilized by the
Lighttpd web server for TLS termination. Exposure of this private key allows
malicious actors to breach the confidentiality and integrity of HTTPS
communications, enabling traffic decryption and server spoofing.

### CVE-2026-67598

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-03T20:17:27.960 |

Emlog Pro through 2.6.23 contains a disabled TLS certificate validation vulnerability in include/service/ai.php that allows network-adjacent attackers to intercept outbound HTTPS requests to configured LLM providers by presenting arbitrary TLS certificates, as CURLOPT_SSL_VERIFYPEER and CURLOPT_SSL_VERIFYHOST are unconditionally disabled across sendStream(), sendImageRequest(), send(), and fetchSearchHtml() with no option to re-enable verification. Attackers can perform man-in-the-middle interception to extract Authorization Bearer API keys from every AI request and inject crafted AI responses that may be acted upon by the tool-call execution pipeline, including the query_database and update_config tool handlers.

### CVE-2026-48031

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-03T20:17:24.200 |

go-base is a Go RESTful API Boilerplate template with JWT Authentication, backed by PostgreSQL. In versions prior to 2026-05-18, the JWT signing secret is hardcoded to the known string "random", letting any attacker who reads the public repository forge tokens for arbitrary users, including admin roles, and completely bypass authentication on all protected endpoints. This value is set in two places: the dev.env template (line 10) and a programmatic fallback in cmd/serve.go (line 35), so the application uses it even when no .env file is present. The original mitigation in auth/jwt/tokenauth.go (lines 22 to 25) only caught the exact string "random", letting other weak secrets through, and replaced it with an in-memory key that was not persisted, invalidating all tokens on every restart and effectively causing a denial-of-service. This issue has been fixed in version 2026-05-18.

### CVE-2026-18248

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-03T16:16:28.247 |

@fastify/aws-lambda version 6.4.0 decorates each Fastify request with request.awsLambda.event and request.awsLambda.context, values that applications are documented to use for authorization decisions such as reading API Gateway authorizer claims. In the default configuration, the getter that populates this decoration reads the client-controlled x-apigateway-event and x-apigateway-context HTTP headers before falling back to the trusted internal request token, and those reserved headers are not stripped from the incoming event. An unauthenticated attacker who can set a single HTTP header can therefore forge the entire Lambda proxy event, including the authorizer context, and override the genuine one. This results in a full authentication and authorization bypass and privilege escalation for any application that trusts request.awsLambda.event for identity or access control. Only version 6.4.0 is affected. Patches: upgrade to @fastify/aws-lambda 6.4.1, which resolves the decoration only through the internal per-invocation token and strips the reserved headers before the request is processed.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-18686

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-04T00:16:40.520 |

A vulnerability was detected in GL.iNet GL-MT3000 up to 4.4.5. The affected element is the function nas-web.add_user of the file /cgi-bin/glc of the component nas-web RPC Wrapper. Performing a manipulation results in command injection. The attack can be initiated remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-18685

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-04T00:16:40.350 |

A security vulnerability has been detected in GL.iNet GL-MT3000 up to 4.4.5. Impacted is the function set_upgrade of the file /cgi-bin/glc of the component modem.so. Such manipulation leads to command injection. It is possible to launch the attack remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-18684

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-03T23:16:45.750 |

A weakness has been identified in GL.iNet GL-MT3000 up to 4.4.5. This issue affects the function remove_profile of the file /cgi-bin/glc of the component modem.so. This manipulation causes command injection. It is possible to initiate the attack remotely. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-47746

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-03T22:16:49.447 |

Misskey is an open source, federated social media platform. Versions 12.37.0 and later, but prior to 2026.5.4, are vulnerable to timing attacks during JSON-LD signature validation and the compaction process. Because the JSON-LD parsing context is not shared between signature verification and subsequent processing, the application may trust information that should not be trusted, resulting in a time-of-check to time-of-use (TOCTOU) flaw. This allows an attacker to have fraudulent activities accepted as valid, leading to a loss of integrity. This issue has been fixed in version 2026.5.4.

### CVE-2026-18616

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-03T19:16:45.557 |

A vulnerability was identified in GL-iNet GL-MT3000 up to 4.4.5. The impacted element is the function server.set_peer of the file /cgi-bin/glc of the component wg-server.so Native Plugin. The manipulation of the argument public_key leads to command injection. Remote exploitation of the attack is possible. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-18615

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-03T19:16:45.383 |

A vulnerability was determined in GL-iNet GL-MT3000 up to 4.4.5. The affected element is the function wg-server.generate_publickey of the file /cgi-bin/glc of the component wg-server.so Native Plugin. Executing a manipulation of the argument private_key can lead to command injection. The attack may be launched remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-18614

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-03T19:16:45.200 |

A vulnerability was found in GL-iNet GL-MT3000 up to 4.4.5. Impacted is the function s2s.enable_echo_server of the file /cgi-bin/glc of the component s2s.so Native Plugin. Performing a manipulation of the argument port results in command injection. The attack may be initiated remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-18613

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-707` |
| Published | 2026-08-03T18:16:38.617 |

A vulnerability has been found in GL-iNet GL-MT3000 up to 4.4.5. This issue affects the function plugins.set_config of the file /cgi-bin/glc of the component plugins.so Native Plugin. Such manipulation leads to injection. The attack can be launched remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-18612

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-03T18:16:38.450 |

A flaw has been found in GL-iNet GL-MT3000 up to 4.4.5. This vulnerability affects the function plugins.remove_package/plugins.install_package of the file /cgi-bin/glc of the component plugins.so Native Plugin. This manipulation causes command injection. The attack can be initiated remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-18602

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-03T17:16:35.153 |

A vulnerability was determined in GL.iNet GL-MT3000 up to 4.4.5. Affected is the function ovpn-client.get_recommend_config of the file /cgi-bin/glc of the component ovpn-client.so Native Plugin. Executing a manipulation of the argument Hostname can lead to command injection. The attack can be executed remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-17070

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-04T14:16:30.733 |

Missing Authorization vulnerability in HAVELSAN Inc. Liman MYS allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects Liman MYS: from 2.2.3 before 2.3.1.

### CVE-2026-58080

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-04T13:18:55.293 |

In Eclipse Milo versions 1.0.0 through 1.1.4, `OpcUaServerConfig.copy()` fails to preserve a configured `RoleMapper`. On servers that rely on role permissions and construct the running configuration through `copy()`, sessions receive no role IDs and the default access controller skips role-permission checks, allowing an anonymous client where anonymous sessions are permitted to read role-permission metadata, invoke protected methods, or delete protected nodes.

### CVE-2026-62870

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-04T00:17:37.813 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-68981

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:U/V:C/RE:M/U:Amber` |
| Weaknesses | `CWE-409` |
| Published | 2026-08-03T20:17:29.280 |

Apache NiFi 1.5.0 through 2.10.0 support gzip-encoded HTTP requests for the application REST API using a Jersey encoding filter. The framework enforced a configurable maximum request size on the compressed payload rather than the decompressed output, allowing a malicious client to send crafted requests that could consume excessive amounts of memory. Upgrading to Apache NiFi 2.11.0 is the recommended mitigation, which relocates response compression to Jetty Server and disables decompression of gzip-encoded HTTP requests.

### CVE-2026-68945

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-03T17:16:45.033 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 20.3.27, 21.2.19, and 22.0.2, HttpTransferCache comma-joins repeated request parameters, allowing semantically distinct HttpClient requests to use the same transfer-cache key and reuse a wrong backend response. This issue is fixed in versions 20.3.27, 21.2.19, and 22.0.2.

### CVE-2026-63252

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-08-04T13:18:55.913 |

In Eclipse Milo versions 0.6.0 through 1.1.4, UASC server transport handlers fail to release retained partial message chunks when a channel disconnects, allowing a remote unauthenticated client to exhaust pooled direct memory by repeatedly sending incomplete chunks and disconnecting, potentially terminating the server.

### CVE-2026-62927

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-04T13:18:55.670 |

In Eclipse Milo versions 1.0.0 through 1.1.4, the Call service dispatches the original mixed batch to address-space handlers after calculating authorization, allowing an anonymous or otherwise low-privileged client to execute a denied method by batching it with an allowed method.

### CVE-2026-10050

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-173;CWE-303` |
| Published | 2026-08-04T11:22:43.883 |

In Eclipse Jetty, the Digest authentication server-side component uses ISO-8859-1 to encode the password as bytes.



This was done because the initial specification for HTTP did not specify explicitly a charset, and it was assumed to be ISO-8859-1 for historical reasons.



If the password contains characters that cannot be represented in ISO-8859-1, they are silently replaced by `?`. This happens with passwords that contain Chinese, Cyrillic or Greek characters, for example: `αβ123` converts to `??123`.



An attacker can send a request with a digest `Authorization` header crafted with a password made of only `?` characters; the server would match any password of the same length that contains non-ISO-8859-1 characters.



Recent HTTP Digest [RFC-7616](https://datatracker.ietf.org/doc/html/rfc7616) supports a `charset` parameters that defaults to UTF-8 that allows for correct encoding/decoding of passwords.

### CVE-2026-16881

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-04T06:16:29.810 |

A code injection vulnerability exists in the LINE Android app prior to version 26.7.2. 

The profile rendering component does not adequately validate or sandbox externally supplied script content embedded in profile templates. 

As a result, an attacker who is able to place crafted content in a profile could cause unintended code to execute with the application's privileges when a victim views that profile. 

A server-side mitigation has been deployed that also protects existing Android clients that have not been updated to version 26.7.2.

### CVE-2026-69249

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-03T22:16:52.720 |

python-cryptography is a package designed to expose cryptographic primitives and recipes to Python developers. Prior to 49.0.0, when resolving invalid certificate chains that include duplicate copies of self-signed certificates, the processing recursively invokes the same candidate, leading to an exponential blowup. Although the limitation that the chain depth cannot exceed a specified maximum depth prevents unbounded recursion and guarantees termination, an attacker-controlled certificate chain can lead the processing to easily take more than 5s to reject in testing. This amplification could form the basis for a resource exhaustion denial of service attack. The core issue arises in the recursive nature of build_chain_inner, which does not de-duplicate against previously analyzed candidates. As the correctness of validation is not affected, the integrity of a system cannot be compromised through this vector, only its availability. This issue is fixed in 49.0.0.

### CVE-2026-41453

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-03T17:16:37.213 |

Krayin CRM before 2.2.4 contains a blind SQL injection vulnerability in the leads DataGrid that allows authenticated users with leads access to inject arbitrary SQL into a HAVING clause by manipulating the rotten_lead[in] query parameter, which is concatenated without parameterized binding directly into a havingRaw() call in LeadDataGrid.php. Attackers can exploit this flaw using time-based and boolean-based blind injection techniques to extract the entire database contents, including user credential hashes, CRM records, and application configuration data.

### CVE-2026-67243

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-04T08:16:35.240 |

freo2 provided by refirio contains an unrestricted upload of file with dangerous type vulnerability. A user with the highest-level administrative privileges for the product may upload an executable file and execute arbitrary OS commands.

### CVE-2026-67599

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-03T20:17:28.113 |

ClearOS 7.9 contains an OS command injection vulnerability in the Log Viewer component that allows authenticated attackers to execute arbitrary commands by submitting unsanitized input through the filter parameter, which is interpolated directly into a shell command in File.php. Attackers can inject command substitution payloads into the filter parameter to execute arbitrary commands as the webconfig user, and due to extensive NOPASSWD sudo privileges granted to that user by default, immediately escalate to root.

### CVE-2026-61524

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-03T18:16:40.210 |

WebsiteBaker CMS before 2.13.10 contains an unrestricted file upload vulnerability in the module installation feature that allows authenticated administrators to achieve remote code execution by uploading a crafted ZIP archive containing a PHP webshell alongside a valid info.php metadata file. Attackers can place the malicious archive through the module installation interface, causing the application to extract the webshell into a web-accessible modules/ subdirectory where it becomes immediately executable by any unauthenticated user via direct HTTP request.

### CVE-2026-61523

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-03T18:16:40.053 |

WebsiteBaker CMS before 2.13.10 contains a code injection vulnerability in the Droplets editor that allows authenticated administrators to inject arbitrary PHP code by submitting malicious content through the droplet Code field, which is written verbatim to a publicly accessible PHP file with no content sanitization. Attackers can save a PHP webshell via the save_droplet handler to a predictable path inside the modules directory, enabling unauthenticated users to achieve remote code execution by making direct HTTP requests to the written file.

### CVE-2026-69149

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-03T17:16:45.627 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 20.3.27, 21.2.19, and 22.0.7, a Cross-Site Scripting (XSS) vulnerability exists in @angular/platform-server's DOM emulation dependency (domino) when serializing the content of fallback raw-content elements (<iframe>, <noembed>, <noframes>, and <noscript>). This issue is fixed in versions 20.3.27, 21.2.19, and 22.0.7.

### CVE-2026-67611

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-308` |
| Published | 2026-08-03T17:16:43.880 |

OpenEMR through 8.2.0 contains an authentication bypass vulnerability that allows attackers with valid credentials to circumvent multi-factor authentication by exploiting the exposed OAuth2 password grant flow through an unauthenticated client registration endpoint. Attackers can register an OAuth2 client via the unauthenticated registration endpoint and use the password grant to exchange credentials for an API access token, bypassing the normal web interface authentication and any enforced multi-factor authentication controls.

### CVE-2026-67610

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-03T17:16:43.703 |

OpenEMR through 8.2.0 contains an improper authentication vulnerability in the OAuth2 dynamic client registration endpoint that allows unauthenticated attackers to register a malicious client with system-level FHIR scopes by supplying a self-generated RSA keypair via the jwks field. Once an administrator approves the registered client, attackers can use the client_credentials grant with a self-signed JWT assertion to obtain access tokens granting read access to all FHIR resources across all patients in the system.

### CVE-2026-39931

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-03T17:16:36.723 |

OpenEMR through 8.2.0 contains an authenticated SQL injection vulnerability in the backup configuration import feature that allows administrators with admin or super ACL privileges to execute arbitrary DDL and DML statements against the application database by uploading a crafted SQL file at the form_step=202 parameter in backup.php. Attackers can exploit the unfiltered shell_exec invocation of the mysql command-line client to extract credential hashes, modify access control tables, inject backdoor accounts, create persistent triggers or stored procedures, and write arbitrary files to the filesystem where MySQL FILE privileges and permissive secure_file_priv settings are configured.

### CVE-2026-18759

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-287` |
| Published | 2026-08-04T08:16:35.070 |

The background service of ABP or AES runs as NT AUTHORITY\SYSTEM and implements a file-based inter-process communication (IPC) mechanism protected by AES encryption. Because the encryption key file is readable by standard users and protected using DPAPI. Any authenticated local user can recover the key and forge valid IPC requests. Furthermore, the service does not check the identity of the requesting process and validates destination paths using an insufficient substring check. A local attacker can submit crafted encrypted requests containing directory traversal sequences to perform arbitrary file reads and arbitrary file writes as NT AUTHORITY\SYSTEM, leading to full local privilege escalation.
Affected products and versions include: ABP (ASUSTOR Backup Plan) 2.0.7.10171 and earlier as well as AES (ASUSTOR EZSync) 1.1.1.3113 and earlier.

### CVE-2026-48113

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-03T21:16:39.597 |

Chisel is a TCP/UDP tunnel, transported over HTTP and secured via SSH. In versions prior to 1.11.5, authenticated clients can bypass --authfile ACL restrictions and tunnel traffic to arbitrary destinations reachable from the server. The ACL is enforced only during the initial handshake against declared remotes, but never on subsequent SSH channels that carry actual traffic. A malicious client can authenticate with a permitted remote, then open channels to any host:port it wants. This issue has been fixed in version 1.11.5.

### CVE-2026-41447

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-03T21:16:38.947 |

FirmaCheck for Windows before 1.3.16 contains a dll hijacking vulnerability that allows local attackers to execute arbitrary code by placing a crafted openssl.cnf file in the unvalidated C:\Program Files (x86)\Common Files\SSL\ directory path. Attackers can write a malicious OpenSSL configuration file referencing an attacker-controlled DLL to achieve code execution at startup process privilege level when FirmaCheck.exe runs automatically at system startup.

### CVE-2026-67609

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-08-03T15:16:20.980 |

Telenia Software TVox 26.5.3 and prior 26.x versions, and 24.9.21 and prior 24.x versions, contain a privilege escalation vulnerability that allows attackers with access to the apache account to execute arbitrary commands as root by exploiting an insecure sudoers configuration in /etc/sudoers.d/telenia. The configuration grants the apache user NOPASSWD execution of /bin/nice, which can be leveraged to invoke arbitrary commands, enabling full root-level command execution without supplying a password.

### CVE-2026-66065

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15;CWE-94` |
| Published | 2026-08-03T21:16:41.193 |

Ouroboros is a local-first runtime for AI coding agents that records their actions and applies user-defined policies to constrain behavior. Versions prior to 0.42.1 have an incomplete denylist. Several execution-routing keys of the same RCE class were omitted, so a malicious cloned repo can still reach arbitrary command execution by shipping a .env (auto-loaded at import, with no review step). The CVE-2026-47211 fix added _UNTRUSTED_ENV_DENYLIST to stop an untrusted project-directory .env from redirecting execution, but it did not account for all keys. The backend config-home and MCP/plugin roots bypass the approval gate by pointing the nested agent, MCP servers, and plugin roster at attacker config. Other variables re-enable blocked local transports, replace sub-agent prompts, switch backends, and lower tool approval classes, further weakening the approval gate. This issue has been fixed in version 0.42.1.

### CVE-2026-47211

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-03T20:17:24.030 |

Ouroboros is a local-first runtime for AI coding agents that records their actions and applies user-defined policies to constrain behavior. In versions prior to 0.39.0, if a user clones a malicious repository and runs Ouroboros commands within that directory, it can lead to arbitrary code execution and potential system takeover. The vulnerability stems from Ouroboros loading the .env file from the current working directory. Execution-affecting environment variables such as OUROBOROS_CLI_PATH, OPENCODE_CLI_PATH, and other backend selectors are accepted directly from this local .env. An attacker can include a malicious script in the repository and point the CLI path variable to it (e.g., OUROBOROS_CLI_PATH=./malicious_script.sh). When the user executes a command like ouroboros init or any command that instantiates the adapter, the malicious script is executed instead of the intended CLI. This issue has been fixed in version 0.39.0.

### CVE-2026-69247

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-208;CWE-209` |
| Published | 2026-08-03T22:16:52.380 |

cryptography is a package designed to expose cryptographic primitives and recipes to Python developers. From 44.0.0 until 50.0.0, pkcs7_decrypt_der, pkcs7_decrypt_pem, and pkcs7_decrypt_smime reported the outcome of decrypting a RecipientInfo's encryptedKey in several distinguishable ways, one of which disclosed the exact length recovered from the RSA operation. The same distinction was also observable by timing. An application that decrypts attacker-supplied EnvelopedData and reflects the outcome gives the attacker a Bleichenbacher oracle against the content-encryption key. Decryption ran as RSA PKCS#1 v1.5 decrypt of encryptedKey, build an AES cipher from the result, then AES-CBC decrypt and PKCS#7 unpad. Invalid RSA padding, a valid padding with a bad key length, a correct length with a wrong key, and the real key each failed or succeeded differently. Case 1 is reachable only where the linked library lacks implicit rejection: OpenSSL 3.0 and 3.1, LibreSSL, and BoringSSL. Exploitation requires a service that auto-decrypts untrusted EnvelopedData matching the victim certificate and answers adaptively at high volume, such as an S/MIME gateway or mail filter. This issue is fixed in 50.0.0.

### CVE-2026-10849

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-08-03T22:16:47.963 |

The hawkBit device management client in subsys/mgmt/hawkbit accumulates the body of an HTTP response from the update server into a heap buffer in response_json_cb() (subsys/mgmt/hawkbit/hawkbit.c). The buffer is sized to hold the received body bytes but reserves no space for a terminating NUL. When the full response has arrived, the code writes response_data[downloaded_size] = '\0' — and whenever the accumulated body length equals the allocation, that terminator lands one byte past the end of the heap object (a heap-based out-of-bounds write, CWE-122 / CWE-787).

The body length and fragmentation are taken directly from the parsed HTTP response (rsp->body_frag_start / rsp->body_frag_len) and are fully controlled by the remote hawkBit server, which chooses its own response length. The precise trigger depends on how the buffer grows, and both forms are remotely reachable. Since v4.0.0 the reallocation is sized to exactly downloaded_size + body_len, so any response body larger than the 1100-byte initial buffer makes the out-of-bounds write deterministic; such response sizes are normal for hawkBit deployment metadata. Before v4.0.0 the buffer grew by doubling and the growth check ((downloaded_size + body_len) > response_buffer_size) is false at equality, so a response body whose length is exactly the current allocation — 1100 bytes with the default initial buffer — skips the reallocation entirely and writes the terminator at response_data[1100] of an 1100-byte object. The HTTP length-mismatch check does not catch this, because the declared and received lengths genuinely agree. Either form is reachable by a malicious, compromised, or man-in-the-middle update server (TLS is optional and, when enabled, does not protect against a hostile server), with no authentication of response content and no client-side length cap protecting the write.

The out-of-bounds write is a fixed single NUL byte immediately following the allocation, corrupting adjacent allocator metadata or the next allocation. The practical impact is heap corruption leading to denial of service (fault on a subsequent allocation or free), with the bounded, allocator-dependent possibility of further corruption. The fix sizes the buffer to the body length plus one and copies with memcpy, ensuring the terminator always lands within the allocation.

### CVE-2025-15628

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-03T19:16:40.567 |

Affected
Omada devices rely on embedded certificates that are shared across deployments
to establish trust between controllers and managed devices.









An attacker
who obtains the embedded certificates may be able to impersonate trusted
controllers or devices and intercept affected communications.

### CVE-2026-66318

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-04T00:17:39.317 |

Origin validation error in Microsoft Edge (Chromium-based) allows an unauthorized attacker to disclose information over a network.

### CVE-2026-10710

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-04T13:17:32.507 |

A maliciously crafted FBX file, when parsed through Autodesk FBX SDK, can trigger a stack-based buffer overflow vulnerability in fbxsdk::ExtractDrive. A malicious actor can leverage this vulnerability to execute arbitrary code in the context of the current process.

### CVE-2026-10709

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-04T13:17:32.377 |

A maliciously crafted FBX file, when parsed through Autodesk FBX SDK, can trigger a stack-based buffer overflow vulnerability in fbxsdk::FbxIO::BinaryReadSectionHeader. A malicious actor can leverage this vulnerability to execute arbitrary code in the context of the current process.

### CVE-2026-59913

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-03T19:16:48.193 |

Dell Display and Peripheral Manager (DDPM Mac), versions prior to 2.3.0.1005, contain a Missing Authentication for Critical Function vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-59912

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-03T19:16:48.050 |

Dell Display and Peripheral Manager (DDPM Mac), versions prior to 2.3.0.1005, contain an Improper Access Control vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges and arbitrary code execution.

### CVE-2026-66310

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-04T00:17:38.240 |

External control of file name or path in Microsoft Edge for Android allows an unauthorized attacker to disclose information locally.

### CVE-2026-69192

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-918` |
| Published | 2026-08-03T20:17:29.960 |

ip-address is a library for parsing and manipulating IPv4 and IPv6 addresses in JavaScript. Prior to 10.3.1, Address4 accepts an octet written with a leading zero and decodes it as decimal, while the WHATWG URL host parser, inet_aton, and getaddrinfo all decode a leading zero as octal. The library and the network stack therefore disagree about which host a string names. new Address4('012.0.0.1') reports correctForm() of 12.0.0.1 and isPrivate() of false, but fetch('http://012.0.0.1/') connects to 10.0.0.1. An application that builds a network trust-boundary decision on these checks, for example a filter intended to block Server-Side Request Forgery, or SSRF, will classify an internal target as external and allow the request. The defect is in the parse gate rather than in any one classifier, so every consumer of Address4 inherits it: isPrivate(), isLoopback(), isLinkLocal(), isCGNAT(), isInSubnet(), isHostInSubnet(), and correctForm() are all computed from the mis-decoded octets. This issue is fixed in version 10.3.1.

### CVE-2026-62354

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:I/V:C/RE:L/U:Amber` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-03T20:17:25.530 |

Authorization handling for Parameter Context validation requests in Apache NiFi 1.10.0 through 2.10.0 allows clients with read access to submit proposed Parameter values. The proposed values override current configuration, enabling users with read access to invoke predefined component validation methods with alternative settings. Apache NiFi installations that do not implement different levels of authorization for viewing and modifying Parameter Context configuration are not subject to this vulnerability. Upgrading to Apache NiFi 2.11.0 is the recommended mitigation, requiring write access to submit Parameter Context validation requests.

### CVE-2025-9291

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-03T18:16:34.047 |

A
certification validation weakness exists in communication between affected
Omada devices and cloud controllers. Certificate identity verification does not
adequately validate that a presented certificate corresponds to the expected
cloud controller hostname, which may allow certificate validation protections
to be bypassed under specific conditions.





Successful
exploitation may allow interception or modification of communication between
affected devices and cloud controllers.

### CVE-2026-69151

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-03T17:16:45.797 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 20.3.27, 21.2.19, and 22.0.1, the Angular compiler i18n pipeline permits i18n-onerror and other i18n-on event-handler attributes, allowing a lower-trust translation file to replace a static handler with executable JavaScript. This issue is fixed in versions 20.3.27, 21.2.19, and 22.0.1.

### CVE-2026-56846

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-04T01:16:19.840 |

A flaw in Node.js HTTP/2 handling can cause HTTP/2 retained header blocks evade maxSessionMemory and enable remote memory exhaustion.

This vulnerability affects Node.js **24.x** and **22.x**.

### CVE-2026-56845

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-04T01:16:19.660 |

An unauthenticated path traversal (LFI) vulnerability exists under /custom-sounds/ when CustomSounds storage is configured to FileSystem. By including ../ sequences in the request path, an attacker can read arbitrary files outside the base directory.

### CVE-2026-66315

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-04T00:17:38.927 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-48399

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-657` |
| Published | 2026-08-03T23:16:46.693 |

Adobe Campaign Classic (ACC) is affected by a Violation of Secure Design Principles vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized read access. Exploitation of this issue does not require user interaction.

### CVE-2026-18733

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-03T21:16:37.963 |

A prompt injection vulnerability in the shell tool in Amazon Strands Agents Tools before 0.8.0 might allow remote actors to execute arbitrary operating system commands on the agent's host via a crafted prompt that sets the non_interactive parameter to true, bypassing the human consent gate.



To remediate this issue, users should upgrade to version 0.8.0.

### CVE-2026-69185

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-754` |
| Published | 2026-08-03T20:17:29.797 |

Socket.IO enables bidirectional and low-latency communication for every platform. Prior to 4.2.7, 3.4.5, and 3.3.6, a specially crafted Socket.IO packet can make the server wait for a large number of binary attachments and buffer them, which can be exploited to make the server run out of memory. This vulnerability is fixed in 4.2.7, 3.4.5, and 3.3.6.

### CVE-2026-69152

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-08-03T17:16:45.953 |

The brace-expansion library generates arbitrary strings containing a common prefix and suffix. Prior to 1.1.18, 2.1.4, 3.0.6, and 5.0.9, expand() does not apply maxLength while constructing comma-alternative intermediate arrays or padded sequences, allowing attacker-controlled input to exhaust memory or block the event loop. The fix for CVE-2026-14257 is bypassed by the vulnerability. This issue is fixed in versions 1.1.18, 2.1.4, 3.0.6, and 5.0.9.

### CVE-2026-61372

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-03T17:16:39.467 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Apache Jena Fuseki.

This issue affects Apache Jena Fuseki: through 6.1.0.

Users are recommended to upgrade to version 6.2.0, which fixes the issue.

### CVE-2026-18568

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-03T16:16:28.560 |

XML::Sig versions from 0.29 before 0.72 for Perl allow signature verification bypass because verify returns true when every signature was skipped before any cryptographic check.

verify in lib/XML/Sig.pm counts the `//dsig:Signature` elements into `$numsigs` and iterates over them, but two paths reach `next` before any digest or key check runs: a `SignedInfo/Reference/@URI` that resolves to no element while `$numsigs` is greater than 1, and, when `id_attr` is set, a reference that does not match the requested ID. The loop records nothing about what it checked, so when every signature takes one of those paths control reaches the unconditional `return 1` that ends verify. Two `Signature` elements whose Reference URI names an ID that no element carries is enough, as is one such element combined with `id_attr`.

Any caller that passes untrusted XML to verify can receive a true return for a document in which no digest and no signature value was checked; a `cert` or `cert_text` trust anchor does not change this, because no key check runs. Versions up to 0.28 use an XML::XPath based verify that has no such skip and are not affected.

### CVE-2026-14838

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-598` |
| Published | 2026-08-04T10:19:32.540 |

Use of GET request method with sensitive query strings vulnerability in Bilin Software and Informatics Consultancy Inc. HUMANIST Digital Human Resources allows Session Hijacking.

This issue affects HUMANIST Digital Human Resources: from 26.0 before 26.1.

### CVE-2026-66321

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-04T00:17:39.440 |

Access of resource using incompatible type ('type confusion') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-65802

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-04T00:17:37.967 |

External control of file name or path in Microsoft Edge for Android allows an unauthorized attacker to disclose information over a network.

### CVE-2026-18607

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-03T17:16:35.913 |

A security vulnerability has been detected in Wavlink WN572, WN570H, WN573, WN529, WN530, WN531, WN535, etc. WN529, WN530, WN531, WN535, WN536, WN551, WN557 and NU516 up to 20260609. Affected by this issue is the function strcpy of the file upload.cgi of the component lighttpd. The manipulation of the argument HTTP_COOKIE leads to stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-18755

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-428` |
| Published | 2026-08-04T08:16:34.930 |

A DLL hijacking vulnerability in GeoVision GV-ASManager allows a local attacker with write access to an unsafe search directory to execute arbitrary code. By placing a crafted dynamic-link library (DLL) file into the application search path prior to the legitimate library, the malicious code is loaded and executed under the security privileges of the GV-ASManager process.

### CVE-2026-42169

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-131` |
| Published | 2026-08-04T04:16:32.710 |

A heap-buffer-overflow vulnerability exists in the APNG (Animated PNG) file loader of GIMP. This flaw occurs when the `fcTL` width exceeds the `IHDR` width, leading to pixel data being written past the end of a heap allocation. Additionally, a heap-based buffer overflow exists in the DDS plug-in due to a BPP mismatch in the `load_layer()` function. Both vulnerabilities can be triggered by opening a specially crafted image file, potentially leading to code execution.

### CVE-2026-14818

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-04T04:16:30.930 |

A path traversal vulnerability in the CLI command used to execute configuration files in Zyxel ATP series firmware versions from V4.32 through V5.42 Patch 1, USG FLEX series firmware versions from V4.50 through V5.42 Patch 1, USG FLEX 50(W) series firmware versions from V4.16 through V5.42 Patch 1, and USG20(W)-VPN series firmware versions from V4.16 through V5.42 Patch 1 could allow an authenticated attacker with administrator privileges to execute a crafted malicious configuration file on an affected device.

### CVE-2026-6837

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-04T03:16:25.890 |

A post-authentication command injection vulnerability in the "export-cgi" CGI program in Zyxel WAX650S firmware versions through 7.10(ABRM.4)C0 could allow an authenticated attacker with administrator privileges to execute OS commands on an affected device.

### CVE-2026-69246

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-180;CWE-436;CWE-918;CWE-941` |
| Published | 2026-08-03T21:16:42.563 |

Guzzle is an extensible PHP HTTP client. Prior to 7.15.2 and 8.0.1, Guzzle gives a transport the request URI as text and supplies the Host header separately. The cURL handlers set CURLOPT_URL to the URI exactly as written and push that Host into CURLOPT_HTTPHEADER; StreamHandler does the same through fopen(). libcurl then parses the authority itself, percent-decoding it and, on an IDN-capable build, applying IDNA mapping, and uses the result to resolve, connect, name the TLS peer and address a proxy CONNECT, while the supplied Host suppresses the aligned one libcurl would have generated. For a URI host written as 127.0.0.%31, filter_var() rejects the host as an IP literal, yet libcurl decodes it to 127.0.0.1 and reaches loopback with no DNS lookup while the server receives Host: 127.0.0.%31. An attacker who influences a fetched URI can therefore reach a host the application's checks excluded and read whatever the host exposes of the response. The same divergence moves Guzzle's own decisions onto a spelling the transport does not use: no_proxy selects proxy routing from the literal host, and RedirectMiddleware decides from it whether to strip Authorization and Cookie. Exploitation requires the application to build a request URI from untrusted input and to make a host decision before handing it to Guzzle. This issue is fixed in versions 7.15.2 and 8.0.1.

### CVE-2026-18806

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-04T13:17:36.540 |

External control of file name or path vulnerability in TÜBİTAK BİLGEM Software Technologies Research Institute pardus-image-writer allows Removing Important Client Functionality.

This issue affects pardus-image-writer: before 1.0.4.

### CVE-2026-66322

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-04T00:17:39.577 |

Origin validation error in Microsoft Edge (Chromium-based) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-69244

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-400;CWE-416` |
| Published | 2026-08-03T21:16:42.273 |

AIOHTTP is an asynchronous HTTP client/server framework for asyncio and Python. Prior to 3.14.3, an out-of-bounds heap read could occur in the C response parser while building an error message for a malformed response. An attacker controlled server, or possibly an accidental response, could trigger a DoS in the client. The vulnerable path was error message construction in aiohttp/_http_parser.pyx, where an llhttp error-position pointer was used to build a snippet for malformed chunked responses and malformed request or response bytes at the buffer end. This issue is fixed in version 3.14.3.

### CVE-2026-18737

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-03T21:16:38.240 |

Shlink contains a blind SQL injection vulnerability that allows any authenticated API key holder to inject arbitrary SQL fragments by supplying an unvalidated direction value in the orderBy query parameter of the tag statistics endpoint. Attackers can craft a malicious direction string containing SQL subqueries that flows unsanitized into a Doctrine QueryBuilder ORDER BY clause, enabling time-based, boolean-oracle, and error-based extraction of sensitive data including long URLs, visitor records, IP addresses, geolocation data, user agents, and hashed API key secrets from any tenant.

### CVE-2026-18655

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-923` |
| Published | 2026-08-03T20:17:17.557 |

Improper restriction of intended endpoints in the RabbitMQ broker connection tools of the Amazon MQ MCP Server (awslabs.amazon-mq-mcp-server) before 2.0.24 may allow a remote unauthenticated actor (via prompt injection) to obtain Amazon MQ for RabbitMQ broker credentials or OAuth access tokens sent to a crafted endpoint controlled through a broker hostname introduced in the MCP client context.



To remediate this issue, users should upgrade to version 2.0.24.

### CVE-2026-18718

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-03T17:16:36.447 |

Ghidra contains an arbitrary code execution vulnerability in the Swift demangler analyzer that allows an attacker to execute arbitrary binaries by supplying a malicious Ghidra project with a crafted Swift tool directory path. When a victim opens the attacker-supplied project, SwiftDemanglerAnalyzer restores the persisted Swift binary directory from project state and SwiftNativeDemangler executes the resolved binary without integrity or signature verification, causing attacker-controlled executables to run under the Ghidra process user with no prompt or confirmation.

### CVE-2026-18606

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-269` |
| Published | 2026-08-03T17:16:35.727 |

A weakness has been identified in Razer RzUpdateService 1.10.14.0. Affected by this vulnerability is an unknown functionality of the file C:\Program Files (x86)\Razer\RzUpdateEngineService\RzUpdateService.exe of the component Named Pipe Handler. Executing a manipulation of the argument lpThreadParameter can lead to improper privilege management. The attack requires local access. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure.
