# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-03 15:00 UTC
- **対象期間**: `2026-09-02T15:01:39.000Z` 〜 `2026-09-03T15:00:34.000Z`
- **重要CVE数**: 129 件（Critical 9.0+: 20 件 / High 7.0〜: 109 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE のうち **CVSS 7.0 以上が 30 件以上** と、攻撃対象が広範囲に及ぶ「**プラグイン・拡張機能の不適切な入力検証**」が目立ちます。  
- WordPress・Joomla などの CMS 系プラグイン、Jenkins のプラグイン、そして Cisco IOS XR 系統のネットワーク機器が多数含まれ、**リモートからのコード実行 (RCE) や認証回避** が共通のリスクです。  
- いくつかは **認証不要 (Unauthenticated)**、あるいは **低権限ユーザーでも利用可能** な設定ミスが根本原因となっており、攻撃者が簡単に初期侵入できる点が特に危険です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑4357** | 10.0 (CVSS 3.1) | WordPress **Embed HTML5 Game** プラグイン (≤ 1.3) で **任意ファイルアップロード** が可能 | *認証不要* で PHP バックドアを設置でき、サイト全体が完全制御下に。WordPress は世界で最も利用される CMS であり、プラグインのインストール数も多いため被害拡大が予想されます。 |
| **CVE‑2026‑77009** | 9.9 (CVSS 3.1) | WordPress **WatchMan‑Site7** プラグイン (≤ 4.2.0) のデバッグコンソールが認証チェックなし | *認証済みユーザー (Subscriber でも可)* が任意 PHP コードを実行できる。低権限ユーザーが取得できる権限でサーバー全体を乗っ取れる点が深刻です。 |
| **CVE‑2026‑20212** | 9.8 (CVSS 3.1) | Cisco Nexus 9000 シリコン One 統合 (TCP 43210/43211) で **root 権限 RCE** | ネットワークコアスイッチでのリモートコード実行は、データセンター全体の可用性・機密性に直結。デフォルトでポートが開放されているため、外部から直接攻撃が可能です。 |
| **CVE‑2026‑78689** | 9.2 (CVSS 4.0) | NGINX **njs** XML モジュールの名前空間パーサーに **メモリ破壊** バグ | NGINX はインターネットフロントエンドの事実上の標準。脆弱な設定が残っていると、リモートからプロセス停止やコード実行が可能です。 |
| **CVE‑2026‑84673** | 8.8 (CVSS 3.1) | Jenkins **Customizable Header** プラグイン (≤ 295.v2544b_ca_19b_97) の **Stored XSS** | CI/CD パイプラインに組み込まれた Jenkins が攻撃者にスクリプト実行権限を与えると、ビルドサーバー全体の機密情報が漏洩・改竄される危険があります。 |

> **※** これらは「認証不要」または「低権限ユーザーで実行可能」かつ「広範囲に展開されている」点で共通しており、早急な対策が求められます。

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱プラグイン・コンポーネントの即時無効化**（特に WordPress・Joomla・Jenkins の該当プラグイン）。  
- **全システムの資産インベントリを更新**し、対象バージョンが含まれるかを自動スキャン（例: `wpscan`, `jenkins-cli`, `nmap` でバナー取得）で確認。  
- **WAF/IPS で該当パス/パラメータをブロック**（例: `/wp-content/plugins/embed-html5-game/*` の POST、`/wp-admin/admin-ajax.php?action=watchman_debug` など）。  
- **ログ監視とインシデントレスポンス手順の整備**：ファイルアップロードログ、PHP エラーログ、NGINX エラーログをリアルタイムでアラート化。  

### 3.2 個別パッケージ・バージョン別対策  

| 製品 / プラグイン | 現行脆弱バージョン | 推奨バージョン / パッチ | 対策手順 |
|-------------------|-------------------|------------------------|----------|
| **WordPress – Embed HTML5 Game** | ≤ 1.3 | **≥ 1.4** (公式リリース) | `wp plugin update embed-html5-game` または手動で最新版をインストール。 |
| **WordPress – WatchMan‑Site7** | ≤ 4.2.0 | **≥ 4.2.1** (開発者が提供するパッチ) | `wp plugin update watchman-site7`。デバッグコンソールが不要なら **無効化** (`define('WATCHMAN_DEBUG', false);`)。 |
| **WordPress – Developer Tools** | ≤ 1.1.3 | **≥ 1.1.4** | 同上、SWFUpload のファイルタイプチェックが追加された版へ更新。 |
| **Jenkins – Customizable Header Plugin** | ≤ 295.v2544b_ca_19b_97 | **≥ 295.v2544b_ca_19b_98** (2026‑06 リリース) | `jenkins-plugin-cli --plugins customizable-header:295.v2544b_ca_19b_98` で更新後、再起動。 |
| **Jenkins – Microsoft Entra ID Plugin** | ≤ 710.v0b_ff8e9cc2d2 | **≥ 710.v0b_ff8e9cc2d3** | 同上、Entra グループ名衝突チェックが追加された版

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-4357

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-02T15:17:38.413 |

The Embed HTML5 Game WordPress plugin through 1.3 does not properly restrict who can upload files via the plugin, as well as what can be uploaded, making it possible for unauthenticated attackers to upload PHP backdoors on affected sites.

### CVE-2026-77009

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-02T15:17:39.410 |

The WatchMan-Site7 WordPress plugin through 4.2.0 does not restrict access to its debugging console, which executes user-supplied PHP code, allowing any authenticated user, such as a subscriber, to run arbitrary code on the server.

### CVE-2026-19117

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-02T19:17:16.490 |

Under specific conditions, an attacker can register an attacker-controlled FIDO2 credential against a target account and then authenticate as
that user. This issue affects on-premises deployments only.

### CVE-2026-20279

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-02T17:17:33.420 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XR Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20279 are related to improper access control issues that are grouped under the Common Weakness Enumeration (CWE) CWE-284.

### CVE-2026-20274

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-664` |
| Published | 2026-09-02T17:17:32.630 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XR Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20274 are related to improper resource control issues that are grouped under the Common Weakness Enumeration (CWE) CWE-664.

### CVE-2026-20212

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1327` |
| Published | 2026-09-02T17:17:31.547 |

A vulnerability in the Silicon One integration for Cisco Nexus 9000 Series Switches could allow an unauthenticated, remote attacker to execute code with&nbsp;root privileges.

This vulnerability exists because TCP ports 43210 and 43211 are accessible in the default Layer 3 (L3) virtual routing and forwarding (VRF). A successful exploit could allow the attacker to connect to an affected device and send crafted input that could be executed as code with&nbsp;root privileges. The exploitation of this vulnerability could also cause the S1HAL process to crash, which could cause the device to reload.

### CVE-2026-53611

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-02T16:17:18.127 |

Looking Glass is a modern, stateless network-diagnostic platform — a single self-contained Go binary that fronts a fleet of routers over SSH and exposes ping / traceroute / BGP lookups through a gRPC (ConnectRPC) API, an embedded SvelteKit web UI, and a lg-cli client. Prior to version 1.3.5, there is an OS Command Injection vulnerability resulting from an unanchored regular expression in the input validation layer. This issue has been patched in version 1.3.5.

### CVE-2025-9314

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-02T15:17:37.127 |

The Developer Tools WordPress plugin through 1.1.3 contains an unauthenticated arbitrary file upload vulnerability in the bundled SWFUpload component

### CVE-2026-53649

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-352;CWE-434;CWE-942` |
| Published | 2026-09-02T18:19:59.973 |

Joro is a web exploitation framework. Prior to version 1.1.1, Joro's default proxy mode exposes a local API on 127.0.0.1:9090 that performs no authentication and applies a wildcard CORS policy. Because plugin uploads use the CORS-safelisted multipart/form-data content type, cross-origin JavaScript on any page the operator visits can reach privileged endpoints - including uploading a native plugin and triggering a restart - directly through the operator's browser, with no preflight or credentials. Since plugins execute on load, this yields unauthenticated remote code execution as the operator's user from a single page visit. This issue has been patched in version 1.1.1.

### CVE-2026-82180

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-295` |
| Published | 2026-09-03T14:17:02.110 |

In Eclipse Arrowhead versions from 5.0.0 to 5.2.1 when the MQTT API is enabled with the certificate authentication policy, CertificateMqttFilter parses an X.509 certificate that the client sends inside the MQTT message payload (the authentication field of MqttRequestTemplate) and treats its Subject DN as the authenticated identity. The certificate is decoded with CertificateFactory.generateCertificate() but its signature is never verified and its issuer chain is never validated against any trust store. Authorisation is reduced to two string comparisons on attacker-supplied data: the DN-qualifier must equal "sy" or "op", and the cloud-name part of the CN must match the server's. Both values are public (the cloud name is in the server's own TLS certificate). An attacker who can publish to the MQTT broker can therefore mint a self-signed certificate with CN=Sysop.<cloud>.<org>.arrowhead.eu, dnQualifier=op, send it as the authentication field, and be authenticated as the cloud's system operator with isSysOp == true. This passes the downstream ManagementServiceMqttFilter (request.isSysOp() → allowed) and gives full management access over MQTT. The HTTP CertificateFilter is not affected — it reads the certificate from jakarta.servlet.request.X509Certificate, which Tomcat populates only after a successful mTLS handshake against the configured trust store.

### CVE-2026-78069

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T13:06:09.327 |

Joomla Extension - j2commerce.com - Missing authorization on Apps controller delegation chain in J2Store 1.0.0-3.3.21, 4.0.0-4.0.21, 4.1.0-4.1.6 - `J2StoreControllerApps`'s `appTask` delegation path instantiates app-plugin controllers with no ACL check anywhere in the code. It currently returns 403 only as a side effect of `fof.xml`'s wildcard-deny resolving under the singularised ACL key `app`, which has no explicit allow rule — not because of any deliberate check. Behind that path, `applocalizationdata::getInstallerTool()` used a caller-influenced table name with no allow-list, both to select a `#__j2store_*` table for truncation and to build a path to SQL files it then executes — a path-traversal-capable file read/execute.

### CVE-2026-76174

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-03T13:06:07.723 |

Unrestricted file upload vulnerability in the CSV file upload functionality of the Ocsreports admin_info endpoint. The application validates files solely based on the name provided by the client, without properly checking their content or securely restricting the permitted file types. This allows a user with administrator privileges to upload PHP files to a directory accessible via the web interface. If the file is subsequently processed by the server, an attacker could execute arbitrary code with the privileges of the account used by the web service.

### CVE-2026-85154

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-03T13:06:22.067 |

WWBN AVideo contains an authentication failure vulnerability where the video_id_hash credential is a non-expiring, non-revocable bearer token that grants full administrator session access to the video owner's account. Attackers who obtain a video_id_hash can replay it indefinitely to authenticate as the video owner with full privileges, and the credential remains valid even after the owner changes their password.

### CVE-2026-78080

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-03T13:06:09.463 |

Joomla Extension - feenders.de - Unauthenticated SQL injection in JooDatabase Lite < 5.1.0 - The cid parameter is used in queries without validation, allowing SQLi vectors.

### CVE-2026-53671

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-682` |
| Published | 2026-09-02T18:20:00.293 |

PREVAIL is a Polynomial-Runtime EBPF Verifier using an Abstract Interpretation Layer. Prior to version 0.2.4, the abstract transformer in prevail treats writes through a T_CTX-typed base register as a silent no-op: do_mem_store in src/crab/ebpf_transformer.cpp only models T_STACK stores, and the checker's T_CTX bounds arm never tests AccessType::write. An attacker can craft an eBPF program that overwrites a context field (e.g., ctx->data), reload that field typed as T_PACKET, and dereference an attacker-controlled address — and prevail will report the program as safe. This issue has been patched in version 0.2.4.

### CVE-2026-53670

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-682` |
| Published | 2026-09-02T18:20:00.140 |

PREVAIL is a Polynomial-Runtime EBPF Verifier using an Abstract Interpretation Layer. Prior to version 0.2.4, in the Prevail eBPF verifier, EbpfTransformer::add() silently skips offset-variable updates when the destination register carries a non-singleton typeset (two or more simultaneously possible pointer types). Subsequent bounds checks use the stale offset and accept out-of-bounds memory accesses, so a crafted BPF program passes verification even though it would corrupt memory at runtime. This issue has been patched in version 0.2.4.

### CVE-2026-76178

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:A/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T13:06:08.293 |

A stored Cross-Site Scripting (XSS) vulnerability in the notification template functionality of the endpoint /ocsreports/?function=notification. A user with administrator privileges can input malicious HTML content which is subsequently stored and displayed without proper sanitisation when other administrators access the template customisation view, allowing JavaScript code to be executed within the application’s security context and potentially compromising the sessions of other users with administrative privileges.

### CVE-2026-78689

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-02T16:17:25.667 |

Description


NGINX JavaScript (njs) has a vulnerability in the XML module's namespace prefix list parser, reachable through the xml.exclusiveC14n() method. An unauthenticated remote attacker can trigger it when an affected NGINX configuration passes an externally controlled XML namespace prefix list to that method. Both the njs and the QuickJS (qjs) engines are affected. A crafted prefix list causes an out-of-bounds write past the end of a heap allocation. With the njs engine, which is the engine used when the js_engine directive is absent, this corrupts adjacent objects and crashes the NGINX worker. With the QuickJS engine, the same call additionally leaks the prefix list on every invocation, causing worker memory to grow across requests. The official nginxinc/nginx-saml reference implementation is affected during SAML signature verification. It reads InclusiveNamespaces/@PrefixList from an untrusted SAML message and passes it to xml.exclusiveC14n() before the signature has been verified, so a valid SAML signature is not required. A crafted SAML Response, Assertion, LogoutRequest, or LogoutResponse is sufficient. Code execution has not been demonstrated and cannot be ruled out for all platforms, as the effect of the out-of-bounds write depends on conditions beyond the attacker's control.  








 Impact


This vulnerability allows remote attackers to cause a denial of service on the NGINX system, either through repeatable worker restarts or through worker memory growth or possibly trigger code execution. There is no control plane exposure; this is a data plane issue only.






Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-66786

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-02T18:21:10.517 |

A flaw was found in submariner. In cert-auth mode, the connection configuration is built using free-form strings from the Custom Resource Definition (CRD) without proper validation. A malicious cluster can exploit this by publishing a CableName that includes newlines and ipsec.conf directives. This allows an attacker to inject arbitrary configuration parameters or execute commands through leftupdown hooks, leading to remote code execution as root on the gateway node.

### CVE-2026-82955

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295;CWE-347` |
| Published | 2026-09-02T15:17:44.860 |

In the current development version of Eclipse aeriOS, which has not yet had an official release, the KrakenD instance included in the API Gateway component had the disable_jwk_security parameter hard-coded to true, with no option to override it through the Helm chart configuration. This setting disables TLS certificate verification when KrakenD retrieves the JSON Web Key Set (JWKS) used to validate bearer tokens, potentially allowing an attacker with the ability to intercept this communication to provide a malicious JWKS and compromise token validation.




The issue has been addressed by making the parameter configurable through the boolean Helm value krakend.config.disableJwkSecurity and setting its default value to false, ensuring that TLS certificate verification is enabled by default.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-85109

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-03T14:17:04.663 |

A vulnerability was determined in Tenda HG10 300001138. This issue affects the function formLogin of the file /boaform/formLogin of the component Boa Web Server. Executing a manipulation of the argument Username can lead to buffer overflow. The attack may be launched remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-80515

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-647;CWE-863` |
| Published | 2026-09-03T14:17:01.830 |

In Eclipse Arrowhead versions from 5.0.0 to 5.2.1 the management-authorization gate that protects every /…/mgmt/… REST endpoint decides whether to apply its check by calling request.getRequestURL().toString().contains("/mgmt/"). Tomcat returns getRequestURL() un-decoded, while Spring MVC's DispatcherServlet routes on the decoded path. Requesting /serviceregistry/%6Dgmt/systems (%6D == m) therefore fails the substring check — the filter falls through without authorising — yet is decoded to /serviceregistry/mgmt/systems and dispatched to the management controller. Spring Security's StrictHttpFirewall (active via spring-boot-starter-security in arrowhead-common) only rejects encoded / \ . % ; and null bytes, so percent-encoded ASCII letters pass through. Any authenticated system — regardless of privilege — can reach every management operation, including POST /authentication/mgmt/identities which creates new sysop accounts, yielding full administrative takeover of the local cloud.

### CVE-2026-80465

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-03T13:06:10.877 |

A vulnerability has been identified in Mendix SAML (Mendix 10 compatible) (All versions < V4.2.3), Mendix SAML (Mendix 11 compatible) (All versions < V4.2.3), Mendix SAML (Mendix 9.24 compatible) (All versions < V3.6.27). Affected versions of the module do not properly validate the SAML response signature. This could allow unauthenticated remote attackers to hijack an account (session) in specific SSO configurations.

### CVE-2026-78064

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T13:06:09.060 |

Joomla Extension - j2commerce.com - Anonymous cart-record tampering via inherited FOF `save` task in J2Store 1.0.0-3.3.21, 4.0.0-4.0.21, 4.1.0-4.1.6 - `fof.xml` grants the `carts` view's tasks a wildcard `true` ACL, and FOF only enforces CSRF tokens on back-end HTML requests, not on front-end `format=raw` requests. `J2StoreControllerCarts` already scoped `remove()` to the caller's own session, but never overrode the generic FOF `save` task, so it remained reachable to insert new cart rows with an attacker-chosen `user_id`/`session_id`, or overwrite an existing row by id.

### CVE-2026-53706

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-682` |
| Published | 2026-09-02T18:20:00.433 |

PREVAIL is a Polynomial-Runtime EBPF Verifier using an Abstract Interpretation Layer. Prior to version 0.2.4, the prevail eBPF verifier accepts ALU32 ADD and SUB instructions that operate on pointer-typed registers without checking the is64 flag. Because ALU32 arithmetic zero-extends the 32-bit result, the upper half of any pointer is silently destroyed at runtime, yet prevail marks the program as verified safe. Any caller that can submit an eBPF program for verification — including unprivileged users on kernels that permit BPF program loading — can produce a program that passes verification but faults or misbehaves at runtime. This issue has been patched in version 0.2.4.

### CVE-2026-20280

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-703` |
| Published | 2026-09-02T17:17:33.580 |

As part of Cisco's ongoing commitment to proactive security and product quality, the&nbsp;Cisco IOS XR Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20280 are related to improper checking or handling of exceptional condition issues that are grouped under the Common Weakness Enumeration (CWE) CWE-703.

### CVE-2026-20278

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-707` |
| Published | 2026-09-02T17:17:33.267 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XR Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20278 are related to improper neutralization issues that are grouped under the Common Weakness Enumeration (CWE) CWE-707.

### CVE-2026-20275

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-682` |
| Published | 2026-09-02T17:17:32.790 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XR Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20275 are related to incorrect calculation issues that are grouped under the Common Weakness Enumeration (CWE) CWE-682.

### CVE-2026-84673

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T16:17:31.940 |

Jenkins Customizable Header Plugin 295.v2544b_ca_19b_97 and earlier allows overwriting the plugin's appearance configuration through Stapler data binding, allowing attackers to configure a custom SVG icon containing inline JavaScript, resulting in a stored cross-site scripting (XSS) vulnerability.

### CVE-2026-84672

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-02T16:17:31.833 |

Jenkins Microsoft Entra ID (previously Azure AD) Plugin 710.v0b_ff8e9cc2d2 and earlier grants Entra group permissions using both the group's unique object ID and its display name, allowing attackers who can create an Entra group with a colliding display name to gain the permissions configured for a privileged group.

### CVE-2026-84671

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-02T16:17:31.737 |

Jenkins File Parameter Plugin 425.v3fa_801681b_5e and earlier allows writing files to arbitrary locations on the Jenkins controller file system through Stapler data binding, which can lead to remote code execution.

### CVE-2026-84670

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-02T16:17:31.640 |

Jenkins Performance Plugin 1015.v09ca_52b_3370e and earlier does not restrict the classes that can be instantiated when deserializing cached performance reports stored in the build directory on the Jenkins controller, allowing attackers with Item/Configure permission to execute arbitrary code on the Jenkins controller.

### CVE-2026-84669

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-02T16:17:31.537 |

A path traversal vulnerability in Jenkins Allure Plugin 2.35.2 and earlier allows attackers with Item/Read permission on jobs that publish Allure report results to read arbitrary files on the Jenkins controller's file system.

### CVE-2026-84668

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-02T16:17:31.440 |

Jenkins SAML Plugin 4.618.v441a_27fa_46d2 and earlier allows overwriting the SAML identity provider metadata file through Stapler data binding, allowing attackers to replace it with attacker-controlled content and authenticate as any user.

### CVE-2026-84650

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502;CWE-566` |
| Published | 2026-09-02T16:17:29.713 |

In Jenkins 2.579 and earlier, LTS 2.568.2 and earlier, transient fields cannot be excluded from deserialization, allowing attackers able to submit configuration updates to specify the values of transient fields that will be deserialized, the impact depending on how those fields are used.

### CVE-2026-84649

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-02T16:17:29.620 |

In Stapler 1839.ved17667b_a_eb_5 through 2107.v8dfcb_e8ed317 (both inclusive), except 2088.2093.vd7c3e58008a_6, included in Jenkins 2.447 through 2.579 (both inclusive), LTS 2.452.1 through 2.568.2 (both inclusive), an HTTP endpoint serving dynamically generated JavaScript resources embeds the user's cross-site request forgery (CSRF) token (crumb) as a string literal, allowing attackers with control over a page hosted on the same site as Jenkins to obtain a valid crumb for the targeted user's session and perform actions on their behalf.

### CVE-2026-84648

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T16:17:29.527 |

In Jenkins 2.579 and earlier, LTS 2.568.2 and earlier, the system log viewer does not escape log record metadata (source, level, and timestamp) resulting in a stored cross-site scripting (XSS) vulnerability exploitable by attackers in control of agent processes.

### CVE-2026-84647

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-02T16:17:29.437 |

In Stapler 2107.v8dfcb_e8ed317 and earlier, except 2088.2093.vd7c3e58008a_6, included in Jenkins 2.579 and earlier, LTS 2.568.2 and earlier, Stapler does not restrict the types of objects that can be instantiated via form data binding to those compatible with the expected field type, allowing attackers with Overall/Read permission to instantiate types related to configuration for which that field type was not intended.

### CVE-2026-84645

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-915` |
| Published | 2026-09-02T16:17:29.193 |

In Jenkins 2.579 and earlier, LTS 2.568.2 and earlier, objects of types marked as storing their configuration in independent top-level configuration files in Jenkins (such as the global configuration and jobs) can appear as nested field values in user-submitted `config.xml` documents and subsequently handle HTTP requests via Stapler, resulting in remote code execution.

### CVE-2026-18329

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636` |
| Published | 2026-09-02T16:17:14.917 |

Description

NGINX JavaScript (njs) and QuickJS (qjs) engines have a vulnerability when a js_access handler performs asynchronous request body processing and an exception is thrown during asynchronous access-control evaluation before an explicit access denial is returned. An unauthenticated attacker can exploit this vulnerability by sending a crafted HTTP request that triggers an error condition in the access validation logic. This may cause the js_access phase to fail open, allowing the request to proceed instead of being denied, resulting in an authentication or authorization bypass and unauthorized access to protected resources.

Impact

This vulnerability may allow remote attackers to bypass js_access controls. There is no control plane exposure; this is a data plane issue only.




Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-85175

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-09-03T13:06:25.270 |

SiYuan versions <= 3.8.1 (fixed in v3.8.2) contain an incomplete blocklist in the IsForbiddenAbsPath() function (kernel/util/path_guard.go), which only blocks conf/conf.json by exact match and does not restrict the TLS private key (conf/key.pem) or CA private key (conf/ca.key) stored in the same conf/ directory. Because the getFile handler skips the blocklist for RoleAdministrator and all authenticated users receive RoleAdministrator in v3.8.1, any user (or any client on a default no-auth-code instance) can retrieve these private keys via POST /api/file/getFile. On deployments with TLS enabled, this allows decryption of captured HTTPS traffic (key.pem) and forging of certificates trusted by clients that imported SiYuan's CA (ca.key).

### CVE-2026-85174

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-03T13:06:25.123 |

SiYuan before v3.8.2 logs API tokens from query parameters in plaintext to an accessible log file when full-text search requests exceed timing thresholds. Authenticated attackers can read the log file via the getFile endpoint to recover admin API tokens and gain permanent administrative access.

### CVE-2026-85169

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-03T13:06:24.310 |

n8n versions before 1.123.73, 2.35.4, and 2.36.2 contain an expression sandbox escape in the $fromAI handler. $fromAI resolved a caller-supplied placeholder name without requiring it to be an own property and admitted reserved keys; against a primitive input value it returned a live host-prototype reference. An attacker with workflow-build privilege can walk the prototype chain to the Function constructor and compile/execute arbitrary code in the main n8n process, leading to remote code execution.

### CVE-2026-85155

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-03T13:06:22.210 |

WWBN AVideo contains a SQL injection vulnerability in the sort column parameter of the get.json.php endpoint with APIName=channels that allows unauthenticated attackers to order results by arbitrary database columns including users.password and users.recoverPass. Attackers can exploit this ordering oracle to infer password hash values and recovery tokens, and trigger SQL errors that disclose the full query statement and database schema.

### CVE-2026-77999

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-472;CWE-602` |
| Published | 2026-09-03T13:06:08.760 |

Joomla Extension - j2commerce.com - Unauthenticated PayPal callback forgery leading to order confirmation fraud in J2Store 1.0.0-3.3.21, 4.0.0-4.0.21, 4.1.0-4.1.6 - The PayPal IPN listener's signature check (`_validateIPN()`) accepted `UNVERIFIED` and any non-`INVALID` response as valid, made its verification request with `CURLOPT_SSL_VERIFYPEER` disabled, and stored its verdict in a field nothing downstream ever checked — so processing continued regardless of the outcome. Separately, the paid-amount comparison only ran when `mc_gross` was a positive number; omitting the field from the POST body (`floatval(null) == 0`) skipped the check entirely. Combined with a merchant-configured `receiver_email` and a sequential, enumerable order id read from the `custom` field, an anonymous POST was enough to move a pending order straight to `CONFIRMED` with no payment, or force another customer's pending order to `FAILED`. `paypalv2.php` performed no amount check under any circumstances.

### CVE-2026-84851

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-03T05:16:46.640 |

An uncontrolled recursion issue exists in Amazon Ion-C versions before 1.1.6 that might allow a remote unauthenticated actor to craft Ion data that exhausts the native call stack and crashes the application using the library, resulting in a denial of service.

### CVE-2026-79756

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-02T17:18:00.087 |

Nuclio is a "Serverless" framework for Real-Time Events and Data Processing. Prior to version 1.17.4, the fix for unauthenticated OS command injection in the nuclio dashboard on the local/Docker platform is incomplete. The fix added validateFunctionName for function names and common.Quote() for the named-resource shell command path, but the list-all resource path (triggered when no specific resource name is provided) still interpolates the resourceNamespace parameter unquoted into a /bin/sh -c command string. An unauthenticated attacker can inject shell metacharacters via the X-Nuclio-Function-Namespace, X-Nuclio-Project-Namespace, or X-Nuclio-Function-Event-Namespace HTTP headers to achieve arbitrary command execution inside the dashboard container. This issue has been patched in version 1.17.4.

### CVE-2026-78222

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-02T16:17:23.557 |

A vulnerability exists in NGINX JavaScript where a malformed HTTP response received by ngx.fetch() can crash an NGINX worker when trusted JavaScript reads Response.statusText. Exploitation requires control or influence over the fetched HTTP response.

Impact:
This vulnerability may allow remote attackers to cause a denial-of-service (DoS) on the NGINX system. There is no control plane exposure; this is a data plane issue only.




Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-77180

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-76` |
| Published | 2026-09-02T16:17:23.407 |

When NGINX Ingress Controller is configured with Ingress annotations, an injection vulnerability exists in the configuration generator of NGINX Ingress Controller. Multiple user-controllable fields are written into the generated NGINX configuration without sanitization. An authenticated attacker with permission to create or modify these annotations may craft values that inject arbitrary NGINX configuration directives. 

Impact:
An authenticated attacker granted write access to NGINX Ingress Controller Ingress annotations through the Kubernetes API may be able to inject arbitrary NGINX configuration directives, create or delete files, or disable services. There is no data plane exposure; this is a control plane issue only.

Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-66842

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-02T16:17:18.910 |

BIG-IP has a vulnerability where an authenticated user of any role may be able to create administrative user accounts through an undisclosed request to Traffic Management User Interface (TMUI).




Impact:

This vulnerability may allow an authenticated attacker with network access to the BIG-IP management interface to escalate privileges by creating administrative accounts on the BIG-IP system. There is no data plane exposure; this is a control plane issue only.




Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-79990

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-02T15:17:42.473 |

Craft CMS GraphQL entry mutation resolvers (saveEntry, deleteEntry) read siteIddirectly from$argumentswithout passing throughArgumentManagerprepareArguments(), which is the function that enforces site-scope filtering via array_intersect against the GraphQL schema’s allowed sites. The query path (ElementResolverprepareElementQuery) correctly calls prepareArguments()`, so queries to unauthorized sites return empty. But mutations bypass this entirely — an attacker with a token scoped to Site A can create, modify, or delete entries in Site B by passing siteId in the mutations argument.

### CVE-2026-79989

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-02T15:17:42.297 |

The vulnerability allows any authenticated user to change their own password without providing the current password or having an active elevated session. It also allows the attacker to change other users’ passwords if the attacker’s account has Edit users permission (which doesn’t allow changing others’ passwords) and lacks Administrate users permission (which is required to change others’ passwords).

### CVE-2026-85031

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-03T13:06:19.767 |

A vulnerability was found in TOTOLINK CP450 4.1.0. The impacted element is an unknown function of the file /cgi-bin/cstecgi.cgi. Performing a manipulation of the argument topicurl results in buffer overflow. Remote exploitation of the attack is possible.

### CVE-2026-84832

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-502` |
| Published | 2026-09-03T13:06:18.887 |

SEPPmail Secure Email Gateway before 15.0.6 deserializes attacker-controlled data in a privileged REST import workflow without adequate validation. An attacker with a privileged API token can execute arbitrary commands with "nobody" privileges.

### CVE-2026-84830

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-269` |
| Published | 2026-09-03T13:06:18.593 |

SEPPmail Secure Email Gateway before 15.0.7 contains a command injection vulnerability that allows authenticated administrators to execute commands with elevated privileges.

### CVE-2026-76176

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-03T13:06:08.007 |

SQL injection vulnerability in the endpoint /ocsreports/index.php?function=admin_double due to improper processing of the values in the ID field included in the selected_grp_dupli[] parameter. An authenticated user with operator privileges can manipulate these values to alter the SQL queries executed by the application and retrieve information stored in the database.

### CVE-2026-76175

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-03T13:06:07.867 |

SQL injection vulnerability in the del_check parameter of the /ocsreports/?function=save_query_list endpoint. Input provided by an authenticated user with operator privileges is incorporated into an SQL query without proper parameterisation or validation, allowing the query to be manipulated and information to be extracted from the database using SQL injection techniques.

### CVE-2026-84452

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-942` |
| Published | 2026-09-02T20:17:41.350 |

Windows ML CLI is a command line tool for building portable, performant, and high-quality AI models for Windows ML. Prior to 0.4.0, the src/winml/modelkit/serve/cli_api.py component exposes WinML CLI commands through a localhost HTTP API without authentication and configures the allow_origins setting as a wildcard in both src/winml/modelkit/serve/cli_api.py and src/winml/modelkit/serve/app.py. A malicious website loaded by a user can send cross-origin requests to /v1/cli/build or /v1/cli/config and set the trust_remote_code parameter to true, which is converted to the --trust-remote-code command-line flag without validation. This reaches AutoConfig.from_pretrained with trust_remote_code=True in src/winml/modelkit/loader/_autoconfig.py and imports Python code from an attacker-controlled model repository, resulting in arbitrary code execution as the server user. This issue is fixed in version 0.4.0.

### CVE-2026-82524

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-02T20:17:39.210 |

UnoPim before 2.1.5 contains an authenticated file upload vulnerability that allows authenticated administrators to upload arbitrary PHP files through the TinyMCE image upload endpoint due to missing file extension and MIME type validation. Attackers can upload a PHP web shell to the public storage disk and execute arbitrary operating system commands on the server by accessing the uploaded file at the URL returned in the server response.

### CVE-2026-20276

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-691` |
| Published | 2026-09-02T17:17:32.957 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XR Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20276 are related to insufficient control flow management issues that are grouped under the Common Weakness Enumeration (CWE) CWE-691.

### CVE-2026-66362

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-76` |
| Published | 2026-09-02T16:17:18.663 |

Description:
When NGINX Plus is configured as the data plane for NGINX Gateway Fabric, an injection vulnerability exists in the NGINX configuration generator component of NGINX Gateway Fabric. User-supplied string values from the Authentication Filter Custom Resource Definition clientID or cookieName fields, or in the clientSecret field of a Secret referenced by an Authentication Filter, are rendered directly into NGINX configuration templates without sanitization or escaping. 

Impact:
An authenticated attacker with permission to create or modify these resources may craft values that inject arbitrary NGINX configuration directives. This is a control plane issue; there is no data plane exposure.

### CVE-2026-9854

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303` |
| Published | 2026-09-03T13:06:26.083 |

A vulnerability exists in SYS600 RBAC mechanism where users having access to the engineering tools could elevate their privileges to administrator level on the underlying Windows host, granting themselves full control over the host machine.

### CVE-2026-9853

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303` |
| Published | 2026-09-03T13:06:25.943 |

A vulnerability exists in SYS600 which allows any user authenticated to the operating system of the server hosting the application to read and modify application objects without being authenticated to the SYS600 system itself.

Only the SYS600 system users should be permitted to view and modify application objects.

### CVE-2026-76642

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-390` |
| Published | 2026-09-03T13:06:08.440 |

util-linux versions through 2.41.5 and 2.42.2 fail to check mount helper exit status before running post-mount hooks, allowing unprivileged users to execute privileged operations on pre-existing filesystems. Attackers can exploit X-mount.idmap or X-mount.owner hooks to clone filesystems with inherited suid bits or modify target inode permissions after a helper fails, achieving privilege escalation.

### CVE-2025-12737

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-03T14:17:00.183 |

The administrative operations within the Carbon Console do not adequately validate specific user-supplied input. This oversight allows a malicious actor with administrative privileges to inject and execute arbitrary code remotely.

Successful exploitation enables a threat actor with administrative privileges and Carbon Console access to execute remote arbitrary code through specific administrative operations, leading to a complete compromise of the affected system.

### CVE-2026-85091

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-03T13:06:20.573 |

zlib versions 1.3.1.2 through 1.3.2 contain a heap buffer overflow vulnerability in the gz_vacate() function when processing non-blocking gzwrite() operations with stale external buffer pointers. Attackers can trigger the overflow by calling gzprintf() or gzvprintf() after a write stall, causing an unchecked memmove() to write beyond the internal input buffer boundary.

### CVE-2026-82404

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-02T17:18:00.223 |

TOON is a compact, human-readable serialization of JSON data for LLM prompts. Prior to 2.3.1, decoding attacker-controlled TOON with a __proto__, constructor, or prototype key wrote through the object prototype chain instead of creating an own property, polluting Object.prototype for the runtime. In packages/toon/src/decode/expand.ts, the expandPaths: 'safe' path and insertPathSafe function made dotted keys such as a.__proto__.x the strongest vector, while plain nested objects, tabular rows, quoted keys, and streaming decode were also affected. The encoder also dropped own __proto__ properties and could invoke an inherited setter during normalization. Services that decode untrusted TOON could experience denial of service or, when a suitable downstream gadget is present, remote code execution. This issue is fixed in version 2.3.1.

### CVE-2026-45730

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-02T17:17:40.847 |

Nuclio is a "Serverless" framework for Real-Time Events and Data Processing. Prior to version 1.16.0, there is a vulnerability in Nuclio Dashboard's project management API, allowing any authenticated user (without membership in the target project) to bypass OPA authorization checks on write paths (PUT /api/projects/{id}, DELETE /api/projects) and modify or delete any project along with all its associated resources (functions, API gateways, etc.). This issue has been patched in version 1.16.0.

### CVE-2021-38489

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-256` |
| Published | 2026-09-03T13:04:10.943 |

HDD password plaintext is stored in a UEFI variable.

### CVE-2026-20277

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-02T17:17:33.110 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XR Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20277 are related to protection mechanism failure issues that are grouped under the Common Weakness Enumeration (CWE) CWE-693.

### CVE-2025-15485

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-02T15:17:36.450 |

The Auto x LINE WordPress plugin through 1.0.0 does not have authorization checks in some of its REST endpoints, allowing unauthenticated users to call them and update the plugin settings, clear logs etc

### CVE-2026-84381

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-02T19:18:08.217 |

HTTPX2 is a next generation HTTP client for Python. Prior to 2.10.0, httpcore2 fails to start TLS in src/httpcore2/httpcore2/_sync/socks_proxy.py and src/httpcore2/httpcore2/_async/socks_proxy.py when the remote origin uses wss through a SOCKS5 proxy because the TLS upgrade condition only recognizes https. HTTPX2 exposes the flaw through Client.websocket() and AsyncClient.websocket() from 2.6.0 through 2.9.1, so the opening handshake, query parameters, Authorization headers, cookies, and subsequent frames can cross the proxy path in plaintext without certificate verification. An attacker controlling or observing that path can read or modify traffic and impersonate the WebSocket server. This issue is fixed in httpcore2 2.10.0 and HTTPX2 2.10.0.

### CVE-2026-49832

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-02T18:19:32.830 |

DSpace open source software is a repository application which provides durable access to digital resources. From versions 8.0-rc1 to before 8.4, versions 9.0-rc1 to before 9.3, and version 10-rc1, Remote Code Execution (RCE) is possible via Velocity Templates used by DSpace for COAR Notify/LDN messages. This issue has been patched in versions 8.4, 9.3, and 10.0.

### CVE-2026-79755

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-02T17:17:59.940 |

Nuclio is a "Serverless" framework for Real-Time Events and Data Processing. Prior to version 1.17.4, on the Nuclio local Docker platform, the function namespace is interpolated—unvalidated—into a double-quoted docker ps --filter "label=nuclio.io/namespace=<value>" command that is executed via the host shell (/bin/sh -c). Because the default auth kind is nop (unauthenticated), a remote attacker can inject arbitrary OS commands that run as root inside the dashboard container, which holds the Docker socket → host compromise. This issue has been patched in version 1.17.4.

### CVE-2026-52833

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-02T17:17:45.630 |

Nuclio is a "Serverless" framework for Real-Time Events and Data Processing. Prior to version 1.16.5, Nuclio's Java runtime generates a build.gradle file during function builds using Go's text/template package. The template renders runtimeAttributes.repositories[] values with the {{ . }} action, which performs no escaping. An attacker can embed a closing brace (}) to break out of the repositories {} block and append arbitrary Groovy statements that execute unconditionally during the Gradle configuration phase. This issue has been patched in version 1.16.5.

### CVE-2026-52831

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-02T17:17:45.347 |

Nuclio is a "Serverless" framework for Real-Time Events and Data Processing. Prior to version 1.16.4, the Nuclio controller builds a curl invocation string for each cron trigger and stores it as the args of a Kubernetes CronJob container (/bin/sh, -c, <command>). Two fields in the trigger specification flow into this string without adequate sanitization: event.headers keys and event.body. This issue has been patched in version 1.16.4.

### CVE-2026-84665

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T16:17:31.147 |

Jenkins SonarQube Scanner Plugin 2.18.3 and earlier does not limit URL schemes for the dashboard links it creates based on SonarQube scanner results, allowing the `javascript:` scheme, resulting in a stored cross-site scripting (XSS) vulnerability exploitable by attackers with Item/Configure permission.

### CVE-2026-78408

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-775` |
| Published | 2026-09-02T16:17:23.687 |

The nsenter --join-cgroup option opens the target cgroup.procs file as root and leaves that file descriptor open across later namespace and credential changes and across execve(). Because the kernel checks later cgroup migrations using the credentials from the original open, a program run in an attacker-controlled target can inherit root's ability to move host processes between cgroups. After a privileged operator uses --join-cgroup against that target, an unprivileged user can migrate and terminate unrelated root processes.

### CVE-2026-73600

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-03T13:06:03.427 |

Dell PowerProtect Data Manager, versions 20.2.0.0 and below, contain a stack buffer overflow vulnerability in file-level restore agent. A high privileged remote attacker could potentially exploit this vulnerability, leading to Information disclosure.

### CVE-2026-84838

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-02T16:17:33.710 |

A flaw was found in rpmuncompress. This command injection vulnerability allows a local attacker to execute arbitrary commands. This occurs when rpmuncompress processes a specially crafted archive filename containing shell metacharacters, which are not properly escaped before being passed to shell command strings. Successful exploitation requires user interaction, where a user or automated workflow invokes rpmuncompress on the malicious file, leading to high impact on the confidentiality, integrity, and availability of data accessible to the invoking user.

### CVE-2026-84837

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-02T16:17:33.560 |

A flaw was found in rpm. An attacker can exploit a command injection vulnerability by influencing the path or filename of a tarball processed by `rpmbuild -t*` to include shell metacharacters. This is particularly relevant in automated build or continuous integration (CI) workflows that ingest externally supplied artifact names. Successful exploitation allows for arbitrary command execution with the privileges of the build user, which could lead to information disclosure or disruption of the build environment.

### CVE-2026-78410

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-02T16:17:23.983 |

A flaw was found in util-linux. Restricted bind mounts take the source path from fstab but do not pin that source before the privileged mount. A local unprivileged user who can replace the authorized source or a writable ancestor can redirect SUID mount(8) to bind another host directory. If the fstab entry also sets X-mount.owner, X-mount.group, or X-mount.mode, root then changes ownership or mode on that redirected inode.

### CVE-2026-78604

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-02T15:17:41.670 |

Incorrect Permission Assignment for Critical Resource (CWE-732) in Elastic Agent can lead to local privilege escalation via Replace Binaries (CAPEC-642). On Windows systems where Elastic Agent is installed in unprivileged mode, resources used by the agent service are created with access controls broader than required. A local user could take advantage of this to cause the service to execute code of their choosing, ultimately obtaining SYSTEM-level privileges on the host.

### CVE-2026-85168

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-03T13:06:24.150 |

n8n versions before 1.123.73, 2.35.4, and 2.36.2 contain a remote code execution vulnerability in the Git node. The node reset a fixed list of command-bearing configuration keys before each operation, but that list did not cover the content-filter and merge-driver key families. A repository with local configuration setting one of those keys together with a matching attribute pattern causes git to execute the configured command during an ordinary Add, Commit, Checkout, or Pull operation. The command runs as the n8n process user.

### CVE-2026-84831

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-03T13:06:18.743 |

SEPPmail Secure Email Gateway before 15.0.7 creates a fully privileged session before required multi-factor authentication enrollment is completed. An attacker with the password for an MFA-required but unenrolled account can access protected functionality without providing a second factor.

### CVE-2023-20576

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-02T20:17:32.950 |

Insufficient Verification of Data Authenticity in AGESA™ may allow an attacker to update SPI ROM data potentially resulting in denial of service or privilege escalation.

### CVE-2026-53635

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-02T17:17:45.770 |

Open edX Platform enables the authoring and delivery of online learning at any scale. Prior to commit 59bb6d6, the view function set_course_mode_price() at lms/djangoapps/instructor/views/instructor_dashboard.py:430 is decorated only with @login_required and performs no course-level permission check. Any authenticated user — including a learner account with zero course roles — can issue a single POST request to overwrite the honor mode price and currency of any course on the platform. The companion frontend modal was removed in a prior cleanup, but the URL route and view remain live, making this an unguarded orphan endpoint. This issue has been patched via commit 59bb6d6.

### CVE-2024-7956

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-02T15:17:36.107 |

A vulnerability exists in the affected products that allows a threat actor to gain access to user’s projects. To exploit this vulnerability the threat actor must have basic user privileges. If exploited, the threat actor can modify and delete the project.

### CVE-2026-6071

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-03T14:17:00.540 |

A remote code execution security issue exists in the affected products when parsing DOE files that could allow a remote attacker to write past the end of an allocated object and execute code within the context of the current process. To exploit this vulnerability, a legitimate user must visit a malicious page or open a malicious file.

### CVE-2026-85150

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-03T13:06:21.910 |

A NULL pointer dereference flaw was found in GStreamer's RTSP support library. The vulnerability occurs while parsing an Authorization or WWW-Authenticate header that uses Digest authentication. Specially crafted whitespace placement around a parameter's terminator can cause an internal length calculation to underflow, leading to a crash of the process parsing the header. On an RTSP server this can be triggered by a remote, unauthenticated attacker sending a single malformed request when the server has authentication enabled; the same flaw can also be triggered against an RTSP client by a malicious or compromised RTSP server. Successful exploitation results in a denial of service (application crash) and has no confirmed impact on confidentiality or integrity.

### CVE-2026-85124

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-03T13:06:21.773 |

@fastify/http-proxy versions before 11.6.2 do not validate proxied HTTP request paths for backslash based dot-segments before forwarding them to the configured upstream. The plain HTTP request handler skips the destination validation that the WebSocket path performs, and the underlying reply-from library only rejects forward-slash traversal, so a request containing backslash dot-segments can escape the boundary set by the prefix and rewritePrefix options. An unauthenticated network attacker can use this to reach upstream paths that were meant to stay hidden behind the proxy, resulting in disclosure of internal endpoints. This is a path traversal issue (CWE-22). Users should upgrade to @fastify/http-proxy 11.6.2 or later.

### CVE-2026-84394

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-09-03T05:16:38.680 |

fast-uri accepts a host that contains an unbalanced or misplaced authority bracket without reporting an error. A host that starts with an opening bracket but does not end with a closing bracket is neither validated as an IP literal nor canonicalized as a domain name, so parse() returns it as the host with error undefined, while Node's URL and the HTTP clients built on it resolve the same string to a different host. An application that reads the parsed host to make a host decision, such as an SSRF denylist, a redirect allowlist, or proxy routing, and then passes the original URL to an HTTP client evaluates its policy against a string that is not the host the request reaches. The same host is carried through normalize, equal, and resolve. This affects fast-uri versions 2.4.5, 3.1.6, and 4.1.3, and is fixed in 2.4.6, 3.1.7, and 4.1.4, where parse() reports a malformed host for any host that contains a bracket but is not a valid IPv6 literal.

### CVE-2026-84292

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-116` |
| Published | 2026-09-02T20:17:39.543 |

fast-uri serializes the port component of a URI without validating it. When recomposing the authority, the userinfo and host components are escaped but the port is concatenated verbatim, so a port value that is not a sequence of digits can inject authority delimiters, demoting the intended host to userinfo and pointing the authority at an attacker-controlled host. Both fast-uri and Node's URL read the result back as the attacker's host with no error, so re-validating the built URI does not catch it. This affects applications that build URIs from parts and assign untrusted data to the port component through the serialize, normalize, or equal functions in their object forms. The issue affects fast-uri versions before 2.4.6, from 3.0.0 before 3.1.7, and from 4.0.0 before 4.1.4. It is fixed in 2.4.6, 3.1.7, and 4.1.4, where recomposeAuthority rejects any port that is not a digit sequence per RFC 3986.

### CVE-2026-78662

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-02T20:17:37.167 |

Previously, a channel registered in the mux's chanList is not usable until it is established. A malicious peer was able flood the channel's incomingRequests, deadlocking the entire connection. Now, we add an atomic established state, set when a channel becomes usable. Until such a time, handlePacket drops every packet other than the open confirmation/failure, without blocking and without tearing down the connection.

### CVE-2026-84382

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-02T19:18:08.353 |

HTTPX2 is a next generation HTTP client for Python. Prior to 2.12.0, the HTTPX2 content decoders in src/httpx2/httpx2/_decoders.py fully inflate each gzip, deflate, br, or zstd network chunk before iter_bytes() or aiter_bytes() yields bounded pieces to the application. A 64 KiB compressed chunk can expand to approximately 64 MiB in one intermediate allocation, so an attacker-controlled or compromised server can cause severe memory pressure or out-of-memory process termination even when the application streams the response. This issue is fixed in version 2.12.0.

### CVE-2026-77124

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-02T18:21:24.753 |

In affected versions of Nexus Repository 3, the script execution endpoint (POST /service/rest/v1/script/{name}/run) did not verify whether script execution had been administratively disabled. An account holding script-execution permission could continue to run previously-created scripts even after an administrator set nexus.scripts.allowCreation=false, undermining the expectation that this setting fully blocks script execution.

### CVE-2026-20281

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-02T17:17:33.730 |

A vulnerability in Cisco Desk Phone 9800 Series, Cisco IP Phone 7800 and 8800 Series, and Cisco Video Phone 8875 that are running Cisco Session Initiation Protocol (SIP) Software could allow an unauthenticated, remote attacker to cause a denial of service (DoS) condition on an affected device.

This vulnerability is due to improper memory management when an affected device processes HTTP packets. An attacker could exploit this vulnerability by sending a continuous stream of crafted HTTP packets to the device. A successful exploit could allow the attacker to cause the affected device to continuously consume memory, resulting in a DoS condition.&nbsp;A manual reboot of the device is required to recover from this condition.
Note: For this vulnerability to be exploitable, the phone must be registered to Cisco Unified Communications Manager (Unified CM) and have Web Access enabled. Web Access is disabled by default.

### CVE-2026-85110

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-03T14:17:05.493 |

A vulnerability was identified in Tenda HG10 300001138. Impacted is the function formWlanSetup of the file /boaform/formWlanSetup of the component Boa Web Server. The manipulation of the argument ssid leads to buffer overflow. Remote exploitation of the attack is possible. The exploit is publicly available and might be used.

### CVE-2023-20577

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-02T20:17:34.093 |

A heap overflow in SMM module may allow an attacker with access to a second vulnerability that enables writing to SPI flash, potentially resulting in arbitrary code execution.

### CVE-2026-84675

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-02T16:17:32.130 |

OS command injection vulnerability in Jenkins TICS Plugin 2025.1.1 and earlier allows attackers able to control build environment variable values to execute arbitrary commands on the agent running the build.

### CVE-2026-18058

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-02T16:17:14.753 |

The mobile Smart Connect dashboard UI was subject to manipulation
by 3rd party apps. When paired with a phishing attack, this manipulation could
result in escalated privileges of an attacker within the system.

### CVE-2026-78590

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-02T15:17:40.433 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') (CWE-22) in the Kibana Fleet feature can lead to the unauthorized deletion of privileged resources via Path Traversal (CAPEC-126). A low-privileged user holding Fleet Settings write access could cause a subsequent administrative action to act on unintended internal resources, resulting in the deletion of privileged resources such as user accounts and other organizational assets. Exploitation requires an administrator to interact with the affected Fleet interface.

### CVE-2026-85166

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-03T13:06:23.867 |

n8n before 2.35.4 and 2.36.x before 2.36.2 does not validate credential references in the inline workflow JSON of nodes that execute an inline sub-workflow (e.g., the Workflow Tool node). A shared-workflow editor, or any user creating/updating a workflow via the REST API, Public API, or MCP, can persist a node referencing a credential they do not own. When the workflow is later executed under an identity that holds the credential, the inline sub-workflow resolves the secret and can send it to an attacker-controlled endpoint, resulting in credential exfiltration.

### CVE-2026-85165

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-03T13:06:23.710 |

n8n versions before 2.36.2 contain an expression sandbox bypass vulnerability where free identifiers in spread, computed-key, switch-case, or class-extension positions resolve against process globals. Authenticated users with workflow-edit permission can mutate host objects through expression evaluation, with changes persisting process-wide until restart.

### CVE-2026-85160

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-03T13:06:22.967 |

AVideo through commit c91b5975d contains a cross-site request forgery and path traversal vulnerability in stopLive.php that allows attackers to delete directories by exploiting missing token validation and unsanitized key parameter concatenation. Attackers can craft an image tag with a traversal payload like key=../../videos to trigger recursive deletion of the videos directory when an admin visits a malicious page.

### CVE-2026-85171

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-03T13:06:24.703 |

n8n before 1.123.73, 2.35.4, and 2.36.2 contains a credential exposure vulnerability in the Strapi, SeaTable, and Mailcheck nodes. These nodes send their decrypted credentials to the authentication endpoint via the raw legacy HTTP helper outside any error handling, causing the plaintext secret to be persisted in execution error data. Any authenticated user can read the plaintext secret from their own execution through the REST API, bypassing the blank-value redaction enforced by the credentials API.

### CVE-2026-85170

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-03T13:06:24.540 |

n8n versions before 1.123.73, 2.35.4, and 2.36.2 pass message content in the Gmail (v1) and Brevo nodes to the mail composer without verifying it is a string. An authenticated user able to run a workflow can supply an expression that resolves to an object carrying a path or href property, causing the composer to read a local file accessible to the n8n process or fetch an internal URL (SSRF) and attach the result to the outgoing message.

### CVE-2026-85164

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-03T13:06:23.567 |

WWBN AVideo through commit c91b5975d contains a server-side request forgery vulnerability in the set_api_userImages API endpoint that fails to validate profileImg and backgroundImg URLs before fetching them. Authenticated API clients can supply internal URLs to fetch cloud metadata or internal services, with responses written to publicly accessible web paths for retrieval.

### CVE-2026-85163

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-03T13:06:23.423 |

AVideo through commit c91b5975d contains a server-side request forgery vulnerability in the EPG parser that allows authenticated uploaders to fetch arbitrary internal URLs. An attacker can supply an internal URL via the epg_link parameter during video upload, which is validated only for syntax and later fetched server-side during EPG generation without SSRF protection checks.

### CVE-2026-85162

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-03T13:06:23.270 |

AVideo through commit c91b5975d contains a cross-site request forgery vulnerability in plugin/Live/saveLive.php that lacks forbidIfNotPost and forbidIfInvalidToken protections. Attackers can craft malicious image tags to overwrite authenticated streamers' RTMP keys, passwords, and titles, hijacking live broadcasts.

### CVE-2026-85093

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-03T13:06:20.883 |

Cheshire Cat AI's GET /memory/collections/{collection_id}/points endpoint fails to apply per-user filtering when retrieving episodic memory points. Authenticated attackers with MEMORY:READ permission can retrieve all users' stored conversation messages and personal data by paginating through the collection using the offset cursor.

### CVE-2026-85089

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-908` |
| Published | 2026-09-03T13:06:20.277 |

FreeRDP versions 3.0.0 through 3.30.0 (before 3.31.0) transmit uninitialized heap memory in Save Session Info PDU reserved padding fields. Three PDU writers in libfreerdp/core/info.c (rdp_write_logon_info_v2, rdp_write_logon_info_plain, and rdp_write_logon_info_ex) use Stream_Seek instead of Stream_Zero for reserved pad bytes (up to 576 bytes), leaving previously freed heap contents in the outgoing PDU. Because the send buffer is allocated with malloc (not zeroed), stale heap data — which may include cleartext credentials from prior sessions — can be sent to the receiving peer. FreeRDP-based servers using rdpUpdate::SaveSessionInfo and freerdp-proxy (which forwards these PDUs) are affected, allowing disclosure of server/proxy process memory to a downstream client.

### CVE-2026-80254

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T13:06:10.737 |

Authorization bypass through user-controlled key issue exists in ShizenBox2 (edge-app). If exploited, an attacker who can log in to the product may change the other user's password.

### CVE-2026-78065

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T13:06:09.200 |

Joomla Extension - j2commerce.com - Guest checkout address disclosure to any authenticated user (IDOR) in J2Store 1.0.0-3.3.21, 4.0.0-4.0.21, 4.1.0-4.1.6 - `editAddress()` redirected non-owners away only when the loaded address row had a **non-empty** `user_id` belonging to someone else. Guest-checkout address rows have an empty `user_id`, so that check never triggered for them — any logged-in account guessing a small, sequential `address_id` got a guest customer's full name, street address, and phone number rendered prefilled into the edit form.

### CVE-2026-76177

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-03T13:06:08.150 |

Server-Side Request Forgery (SSRF) vulnerability in the /ocsreports/?function=tele_activate endpoint due to insufficient validation of the HTTPS_SERV and FILE_SERV parameters. An authenticated user with operator privileges can provide arbitrary values for these parameters, causing the OCS Inventory server to make HTTP/HTTPS requests to external systems or internal resources, which could allow access to internal network services or metadata resources of cloud services.

### CVE-2026-77125

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-02T18:21:25.023 |

A vulnerability was identified in Sonatype Nexus Repository 3 in which two blobstore group management REST API endpoints did not correctly enforce the intended authorization check. A user granted only the nexus:blobstores:create permission could invoke these endpoints to convert an existing blobstore into a group blobstore, an action that should require the nexus:blobstores:update permission instead. This could result in unauthorized modification of blobstore configuration without administrator approval. The nexus:blobstores:create permission is a named permission that must be explicitly granted by an administrator; it is not held by default.

### CVE-2026-49249

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-02T18:19:28.123 |

Boruta is a standalone authorization server that aims to implement OAuth 2.0 and Openid Connect up to decentralized identity specifications. Prior to version 0.10.0, BorutaIdentityWeb.UserSettingsController.update/2 atomizes every key of the user-supplied request body via String.to_atom/1 before any validation. Because String.to_atom interns atoms permanently in the BEAM atom table (default cap 1,048,576 atoms; ERL_MAX_ATOMS), any authenticated end user can send PUT /users/settings with a user[<fresh-key>]=... body containing fresh keys per request and exhaust the global VM atom table. Once the table is full, the BEAM aborts with no more index entries in atom_tab and the entire OIDC server (auth, admin, gateway apps in the umbrella) crashes. The route is protected only by require_authenticated_user and a per-IP rate limit of 10 requests/second; a logged-in end user can hit it. The keys are atomized unconditionally before the downstream Accounts.update_user/6 call, so even failing updates contribute to exhaustion. This issue has been patched in version 0.10.0.

### CVE-2026-84811

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-02T17:18:05.447 |

agentverus-scanner fails to analyze compiled Python bytecode files in companion code directories, allowing attackers to bypass security scanning by shipping malicious __pycache__ entries alongside benign source files. Attackers can execute arbitrary Python bytecode on import while the scanner reports a CERTIFIED verdict with high trust scores in both static and semantic analysis modes.

### CVE-2026-84810

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-02T17:18:05.297 |

claude-skill-antivirus fails to analyze executable files when scanning local skill directories, reading only SKILL.md while ignoring Python source, bytecode, and other artifacts in the scripts directory. Attackers can distribute skills with malicious code in non-manifest files that receive a SAFE verdict with 100/100 trust score despite containing unanalyzed executable payloads.

### CVE-2026-84809

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-02T17:18:05.150 |

Tencent AI-Infra-Guard's skill-scan component excludes compiled Python bytecode files from analysis by hardcoding __pycache__ directories and .pyc/.pyo/.pyd extensions into skip lists across multiple scanning surfaces. Attackers can distribute skills with benign Python source files alongside malicious compiled bytecode that executes on import while the scanner reports a safe verdict, enabling code execution when operators install the skill.

### CVE-2026-79754

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-02T17:17:59.770 |

Nuclio is a "Serverless" framework for Real-Time Events and Data Processing. From version 1.6.19 to before version 1.17.2, Nuclio's Dashboard build pipeline does not sanitize the spec.build.tempDir field before using it to construct a shell command. When the Kaniko container builder is enabled, a user with function-create permission can inject shell metacharacters into this field and achieve arbitrary command execution inside the Dashboard container, which runs with a Kubernetes service account holding wildcard access to Secrets, Pods, Jobs, and Deployments in its namespace. This issue has been patched in version 1.17.2.

### CVE-2026-84667

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-02T16:17:31.340 |

Jenkins ThinBackup Plugin 2.1.4 and earlier allows overwriting the plugin's backup configuration through Stapler data binding, allowing attackers to redirect backup writes to an attacker-specified directory and to include arbitrary files from the Jenkins controller file system in backups.

### CVE-2026-14199

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-290;CWE-863;CWE-1023` |
| Published | 2026-09-02T16:17:14.517 |

Only self-managed Grafana instances with Auth Proxy authentication and identity caching enabled (sync_ttl greater than zero) are affected. The Auth Proxy cache key concatenated the username and forwarded identity attributes without a delimiter, so distinct identities could collide on one key. An authenticated user who shapes their own attributes to collide with a higher-privileged user's, while that user's cache entry is live, is authenticated as that user, up to Administrator (authentication bypass by spoofing).

### CVE-2026-79991

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-02T15:17:42.673 |

Craft CMS GraphQL entry mutation resolvers (saveEntry, deleteEntry) read siteIddirectly from$argumentswithout passing throughArgumentManagerprepareArguments(), which is the function that enforces site-scope filtering via array_intersect against the GraphQL schema’s allowed sites. The query path (ElementResolverprepareElementQuery) correctly calls prepareArguments()`, so queries to unauthorized sites return empty. But mutations bypass this entirely — an attacker with a token scoped to Site A can create, modify, or delete entries in Site B by passing siteId in the mutations argument.

### CVE-2026-80253

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1263` |
| Published | 2026-09-03T13:06:10.587 |

An improper physical access control issue exists in ShizenBox2 (dev-conf). If exploited, an attacker with physical access to the product may execute bootloader commands without authentication.

### CVE-2026-79679

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1391` |
| Published | 2026-09-03T13:06:10.430 |

Use of Weak Credentials vulnerability in B&R Industrial Automation GmbH mapp Audit used in mapp Services.

This issue affects mapp Audit used in mapp Services: before 6.8.0.

### CVE-2026-71221

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-03T13:06:02.887 |

A stack out-of-bounds write vulnerability was found in gfs2-utils. In savemeta, the height value from on-disk inode metadata is used as a loop bound without bounds checking, causing a stack buffer overflow that may lead to arbitrary code execution when processing crafted GFS2 filesystem images.

### CVE-2026-71220

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-03T13:06:02.703 |

A stack out-of-bounds write vulnerability was found in gfs2-utils. In gfs2_edit, the di_height field from on-disk inode metadata is used as an array index without bounds checking, causing a stack buffer overflow that may lead to arbitrary code execution when processing crafted GFS2 filesystem images.

### CVE-2026-78409

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-02T16:17:23.833 |

The X-mount.subdir option uses a detached-tree fast path on Linux 6.15 and later and passes the configured subdirectory to open_tree() with AT_SYMLINK_NOFOLLOW. That flag does not stop intermediate symlink traversal or keep resolution inside the newly mounted filesystem. A local unprivileged user with an fstab-authorized X-mount.subdir entry can attach a host path at the intended mountpoint.
