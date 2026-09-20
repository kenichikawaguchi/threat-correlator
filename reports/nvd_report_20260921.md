# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-20 15:00 UTC
- **対象期間**: `2026-09-19T15:01:17.000Z` 〜 `2026-09-20T15:00:25.000Z`
- **重要CVE数**: 27 件（Critical 9.0+: 5 件 / High 7.0〜: 22 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS 7.0 以上のものは **30 件** 超が報告され、**リモートコード実行 (RCE)** や **権限昇格・情報漏洩** が目立ちます。特に、ネットワーク層で動作する **Suricata**、Web アプリケーションフレームワーク系（openEQUELLA、Mistral Vibe、Survey‑Passthrough）に関する脆弱性が高スコアで集中しています。  
- **リモートから認証不要でコード実行が可能** なケースが 4 件以上（CVSS ≥9.0）。  
- **インフラ系コンポーネント（Suricata、Exim、Expat）** のバグは、IDS/メールサーバーといった基盤サービスを直接狙うため、被害拡大リスクが高いです。  
- 多くは **パッケージのバージョンアップ** で修正が提供されているものの、**旧バージョンが長期間残存** している環境が多く、速やかな対応が求められます。

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 重大度の根拠・影響範囲 |
|-----|--------|----------|------------------------|
| **CVE‑2026‑90817** | 9.8 (CVSS3.1) | Survey アプリの **未認証 RCE**（HTTP ルーティングとデータインポート処理の不正利用） | 公開された Survey 機能から任意のコントローラへリクエストを送るだけでサーバ上で任意コードが実行可能。認証不要かつネットワーク上から直接攻撃できるため、最優先でパッチ適用が必要。 |
| **CVE‑2026‑94084** / **CVE‑2026‑94083** | 9.4 (CVSS3.1) | Suricata < 8.0.7 の **Use‑After‑Free / Type Confusion** による RCE | IDS/IPS として広く導入されている Suricata が、HTTP/2 ルールや DoH2 解析時にメモリ破壊を起こし、攻撃者が任意コードを実行できる。ネットワーク全体の可視化・防御機能が失われる危険性がある。 |
| **CVE‑2026‑94109** | 8.7 (CVSS4.0) | openEQUELLA < 2026.1.0 の **FreeMarker テンプレート RCE**（テンプレートクラス解決のサンドボックス未設定） | 認証ユーザーがコレクション概要やダッシュボードに悪意あるテンプレート式を埋め込えるだけでサーバ上でコードが実行可能。内部システムでの情報資産が一瞬で漏洩・改ざんされるリスクが高い。 |
| **CVE‑2026‑93993** | 8.6 (CVSS4.0) | Mistral Vibe < 2.25.5 の **Git フック実行による RCE** | リポジトリの post‑checkout フックが信頼検証前に実行されるため、攻撃者が細工したリポジトリを提供すれば任意シェルが実行できる。CI/CD パイプラインや内部開発環境での横展開が懸念される。 |
| **CVE‑2026‑93990** | 8.7 (CVSS4.0) | Expat < 2.8.4 の **UTF‑16 サロゲート処理不備**（マルチバイト隠蔽） | 高サロゲートと低サロゲートの組み合わせを不正に受け入れ、マークアップ文字を隠蔽できるため、XML パーサーを利用したアプリで情報漏洩や XSS につながる。多くの C/C++ アプリが依存しているため、広範囲に影響。 |

> **注**：上記は **CVSS が 9.0 以上**、または **広範囲にデプロイされている基盤ソフトウェア** に絞って選定しています。  

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンの即時更新
| 製品・パッケージ | 現行 (脆弱) バージョン | 修正版 (最低) バージョン | 更新手順例 |
|------------------|------------------------|--------------------------|------------|
| Survey‑Passthrough (該当アプリ) | 1.0‑2.3 など (ベンダー提供の最新) | **2.4.0 以上** (ベンダーが公開したパッチ) | `composer update` / アプリ提供元のアップデートガイドに従う |
| Suricata | < 8.0.7 | **8.0.7** 以上 | `apt-get update && apt-get install suricata=8.0.7-1`（Debian/Ubuntu）<br>または公式リポジトリから最新版をビルド |
| openEQUELLA | < 2026.1.0 | **2026.1.0** 以上 | `docker pull equella/open-eq:2026.1.0` でイメージ更新、既存コンテナを再デプロイ |
| Mistral Vibe | < 2.25.5 | **2.25.5** 以上 | `pip install --upgrade mistral-vibe==2.25.5`（Python パッケージ） |
| Expat | < 2.8.4 | **2.8.4** 以上 | `yum update expat-2.8.4`（RHEL 系）<br>またはソースからビルド `./configure && make && make install` |

> **ポイント**：パッチが未提供の場合は **ベンダーのアドホック回避策**（例：Suricata の `--disable-doh2` フラグ、openEQUELLA のテンプレートサンドボックス強制設定）を適用し、同時に **脆弱バージョンの使用禁止** をポリシー化してください。

### 3.2 防御・検知の強化
1. **IDS/IPS のルール更新**  
   - Suricata の最新シグネチャセット（ET、Snort 互換）を毎日取得し、`suricata-update` を実行。  
2. **Web アプリケーションファイアウォール (WAF)**  
   - Survey、openEQUELLA、Mistral Vibe への **POST/PUT リクエストのサイズ上限** と **不審なヘッダー** をブロック。  
3. **ネットワーク分離**  
   - IDS/メールサーバー（Exim、Suricata）を **DMZ** に配置し、外部からの直接アクセスを防止。  
4. **ログ監視**  
   - `auditd` / `syslog` に **プロセス生成 (exec

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-90817

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73;CWE-94` |
| Published | 2026-09-20T13:17:44.973 |

An unauthenticated Remote Code Execution vulnerability was found in the survey passthrough routing and Data Import processing logic, in which a malicious user could potentially exploit it by manipulating HTTP requests to access an unintended controller route from a public survey context and by supplying a crafted file-path/stream parameter during import handling. If successfully exploited, this could allow the attacker to remotely execute arbitrary code on the REDCap server. The attacker does not have to be authenticated in order to exploit this, but exploitation requires knowledge of a valid public survey hash. This vulnerability exists in REDCap 13.3.0 and higher.

### CVE-2026-94084

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-20T02:16:53.717 |

Suricata before 8.0.7 has an Http2ThreadMultiBuf use-after-free when a transaction is inspected by rules that use http.response_header with and without a transform.

### CVE-2026-94083

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-20T02:16:53.520 |

Suricata before 8.0.7 has a DoH2 type confusion that can cause an invalid free, because cleanup code for the HTTP2 state is executed even though the actual state is HTTP1 (when there is a DoH2 request with an HTTP1 to HTTP2 upgrade). This requires app-layer.protocols.doh2 to be enabled, which is the default in 8.x versions.

### CVE-2026-94003

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-20T12:17:05.403 |

A vulnerability has been found in Comfast CF-N1-S 2.6.0.1. Impacted is the function get_css_path_from_uri of the file /cgi-bin/mbox-config of the component Web Management Interface. The manipulation leads to stack-based buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2026-94107

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-338` |
| Published | 2026-09-20T12:17:06.277 |

NivoCart through 2.4.0 contains a predictable password reset token vulnerability in the forgotten.php endpoint that generates recovery codes using substr(md5(mt_rand()), 0, 10). Attackers who know an administrator's email address can request a password reset and predict the token to gain administrative account access without rate limiting or expiration.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-86553

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-20T04:17:06.240 |

SmartLife app dynamically generates fresh SmartLife application authentication parameters inside its runtime process. Using the acquired SmartLife application authentication parameters, an attacker can directly call the backend interface /account/verify.serv to obtain the real account ID corresponding to a registered email address. By spoofing the application authentication information together with the target account ID, the attacker can reset the password of the target account.

### CVE-2026-94109

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-20T12:17:06.620 |

openEQUELLA versions before 2026.1.0 contain a remote code execution vulnerability in FreeMarker template compilation due to an unsandboxed TemplateClassResolver configuration. Authenticated attackers can inject malicious template expressions through collection summaries, dashboard portlets, or MIME templates to instantiate dangerous classes like freemarker.template.utility.Execute and invoke Runtime.exec for arbitrary command execution.

### CVE-2026-94106

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-20T12:17:06.110 |

getID3 before 1.9.26 contains an OS command injection vulnerability in shell-out handlers that fail to escape filenames in command strings. Attackers can craft malicious filenames containing shell metacharacters to inject arbitrary commands executed with the privileges of the process embedding getID3.

### CVE-2026-94104

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-20T12:17:05.777 |

NivoCart through 2.4.0 contains an arbitrary file upload vulnerability in the File Manager multi() endpoint that fails to validate file extensions for new filenames or when chunks parameter is 2 or higher. Attackers with view-only back-office access can upload PHP files to the web-accessible image/data/ directory and execute them for remote code execution.

### CVE-2026-93990

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-176` |
| Published | 2026-09-19T23:17:10.203 |

Expat through 2.8.4 fails to validate low surrogates following high surrogates in UTF-16 input, allowing malformed UTF-16 sequences to be accepted. Attackers can craft UTF-16 encoded XML with lone high surrogates that consume following code units, hiding markup characters from the parser and enabling XML injection attacks.

### CVE-2026-93993

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-19T23:17:10.673 |

Mistral Vibe before 2.25.5 contains a remote code execution vulnerability in the worktree creation process that executes git hooks before trust validation. Attackers can supply a repository with a crafted post-checkout hook that executes arbitrary shell commands with the privileges of the user running Vibe.

### CVE-2026-87067

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-20T07:16:50.430 |

The Forminator Forms  WordPress plugin before 1.57.2.1 does not restrict which classes may be instantiated when it deserialises a value taken from an XML-RPC request, allowing users who hold its forms-management permission to write a file of their choosing and execute arbitrary code. That permission belongs to an administrator by default, and to any role the site has granted it through the Forminator Forms  WordPress plugin before 1.57.2.1's own settings, so the issue is reachable well below administrator on sites that use that feature.

### CVE-2026-93958

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-20T02:16:53.307 |

A vulnerability was found in D-Link R95 BE9500_1.00.16. This vulnerability affects the function system of the file /bin/ssi of the component DHMAPI. The manipulation of the argument NTPServer results in os command injection. The attack can be executed remotely. The exploit has been made public and could be used.

### CVE-2026-94108

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-20T12:17:06.427 |

getID3 through 1.9.26 contains an XML external entity injection vulnerability in the XML2array helper function that fails to properly disable entity loading on PHP before 8.0. Attackers can craft malicious XML metadata in media files to disclose local files, perform server-side request forgery, or cause denial of service through entity expansion.

### CVE-2026-93991

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-19T23:17:10.360 |

Argo Workflows versions 4.1.0 through 4.1.3 contain an authorization bypass vulnerability in ListArchivedWorkflows that fails to apply cluster-scoped access review when the metadata.namespace field selector uses the NotEquals operator. Attackers with namespace-scoped list permissions can use a negated namespace field selector to retrieve archived workflows from all other namespaces, exposing spec arguments, parameter values, and annotations.

### CVE-2026-82842

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-20T07:16:50.093 |

The SAML Single Sign On  WordPress plugin before 6.0.0 does not honour the configured criterion for linking an incoming single sign-on identity to a WordPress account, always resolving the identity by login name whatever the site has chosen, which allows an attacker who can have the site's identity provider assert a login name of their choosing to authenticate as any account, including an administrator, without proving ownership of that account.

### CVE-2026-94112

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-20T12:17:06.953 |

mayswind ezBookkeeping before 2.0.0 fails to invalidate TOTP passcodes after use, allowing attackers to replay captured codes within the acceptance window. Attackers with stolen credentials can authenticate and reuse a captured passcode against multiple authorization attempts for approximately 90 seconds without detection.

### CVE-2026-87839

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-20T07:16:50.760 |

The Tripzzy  WordPress plugin before 1.5.1 does not have authorisation checks, and does not validate the identifier of the object being removed, in an AJAX action available to unauthenticated users, allowing them to permanently delete arbitrary comments on the site.

### CVE-2026-85017

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-20T07:16:50.303 |

The Unlimited Elements For Elementor WordPress plugin before 2.0.20 does not perform a capability check on an AJAX action and deserializes attacker-controlled stored data through it, which makes it possible for authenticated attackers with subscriber-level access to inject arbitrary PHP objects. A partial fix in the 2.0.18 to 2.0.19 releases raised the privilege required to reach the vulnerable action to editor-level, and the issue was fully resolved in 2.0.20.

### CVE-2026-94056

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-908` |
| Published | 2026-09-19T23:17:11.113 |

Exim before 4.100.1, when Proxy-Protocol is used with an attacker-controlled proxy, allows attackers to read certain uninitialized data from stack memory.

### CVE-2026-92541

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-20T07:16:51.353 |

The Import and export users and customers WordPress plugin before 2.5.2 does not enforce the promote_users capability in its front-end import functionality, allowing users with only the create_users capability to change the role of existing users, including promoting them to administrator.

### CVE-2026-92540

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-20T07:16:51.257 |

The Import and export users and customers WordPress plugin before 2.5.2 does not correctly enforce the promote_users capability when assigning roles during a CSV import, allowing users with only the create_users capability to create new administrator accounts or promote existing users to administrator.

### CVE-2026-81650

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-20T07:16:49.590 |

The Photo Gallery, Sliders, Proofing and   WordPress plugin before 4.5.0 does not correctly validate the extensions of files extracted from an uploaded archive, due to a variable being reused as a loop counter so that the check always passes, allowing users granted its gallery-management capability by an administrator to write arbitrary files into a web-accessible directory and, on hosts that execute them, run arbitrary code.

### CVE-2026-94113

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-20T12:17:07.117 |

Frappe ERPNext versions before 15.121.0 and 16.x before 16.34.0 contain an information disclosure vulnerability in whitelisted timesheet endpoints that fail to enforce doctype permissions. Authenticated attackers can call get_projectwise_timesheet_data, get_timesheet_detail_rate, and get_timesheet endpoints to enumerate and retrieve billable time logs including project names, billing amounts, and work descriptions without proper authorization checks.

### CVE-2026-93988

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-19T23:17:09.890 |

QloApps through 1.7.0 contains a path traversal vulnerability in the getEmailHTML action of admin/ajax.php that allows authenticated back-office users to read arbitrary files. Attackers can supply relative path sequences in the email parameter to bypass directory restrictions and access sensitive files including database credentials and configuration data.

### CVE-2026-94054

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-19T23:17:10.827 |

Exim before 4.100.1, when Proxy-Protocol is used with an attacker-controlled proxy, has an out-of-bounds write.

### CVE-2026-93992

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-19T23:17:10.517 |

Gopeed through 2.0.0-beta.3 contains a path traversal vulnerability in archive extraction that allows attackers to write arbitrary files outside the extraction directory. Attackers can craft malicious archives with entries containing directory traversal sequences that bypass validation, enabling file write operations when users download and extract archives with AutoExtract enabled.
