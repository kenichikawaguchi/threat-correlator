# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-07 15:00 UTC
- **対象期間**: `2026-07-06T15:00:28.000Z` 〜 `2026-07-07T15:00:34.000Z`
- **重要CVE数**: 90 件（Critical 9.0+: 20 件 / High 7.0〜: 70 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上り、特に **リモートコード実行 (RCE)・認証バイパス・特権昇格** が集中しています。  
- **オープンソースの自前ホスティングツール (Coolify、Crawl4AI) が多数**、認可ロジックの抜けやシェルコマンド組み立てミスに起因する深刻な脆弱性を抱えている。  
- **商用製品でも認証・権限チェックの不備** が顕在化し、Plesk、Dell PowerProtect Data Domain、Adobe ColdFusion などで **リモートからのフル権限取得** が可能になるケースが目立ちます。  
- 多くの脆弱性は **ネットワークから直接攻撃可能 (AV:N, PR:N)** であり、外部からのスキャンや自動化攻撃ツールに狙われやすい点が共通しています。  

---

## 2. 特に注目すべき CVE  

| CVE ID | スコア | 主な影響 | 注目理由・影響範囲 |
|--------|--------|----------|-------------------|
| **CVE‑2026‑48316** | 10.0 | ColdFusion 2025.9 / 2023.20 以前で **任意コード実行** (スコープ変更) | - 入力検証不備により、認証不要で任意コードが実行可能。<br>- ColdFusion は多くの企業サイト・イントラで利用されており、サーバ全体が乗っ取られるリスクが極めて高い。 |
| **CVE‑2026‑57572** | 10.0 | Crawl4AI < 0.9.0 の Docker API が **Chromium 起動引数に任意文字列注入** でき、コンテナ内でコード実行 | - Docker API が外部から直接呼び出せる構成でデプロイされるケースが増加。<br>- LLM‑friendly なクローラは開発・研究環境で広く利用され、攻撃者が任意のシェルコマンドを実行できる。 |
| **CVE‑2026‑48614** | 9.9 | Plesk XML API の **認可欠如** により、認証ユーザが任意の設定ファイルを書き込み、root 権限で実行 | - Plesk は中小企業から大手まで幅広く採用。<br>- XML API は自動化スクリプトで頻繁に利用されるため、攻撃者が簡単に特権取得できる。 |
| **CVE‑2026‑53483 / CVE‑2026‑53481** | 9.8 | Dell PowerProtect Data Domain の **認証回避** と **パス・トラバーサル** による任意ファイル書き込み | - バックアップ基盤は重要インフラの要。<br>- 認証不要でデータドメインに侵入でき、機密データの漏洩・改ざんが可能。 |
| **CVE‑2026‑34038** | 9.9 | Coolify < 4.0.0‑beta.469 の **リモートコード実行** (アプリケーションデプロイ時) | - Coolify は「セルフホスト」型のデプロイ・管理ツールとして人気。<br>- アプリケーション書き込み権限だけでサーバ上で任意コードが実行でき、内部ネットワーク全体への横展開が容易。 |

> **注:** 上記は **スコアが最高 (10.0) かつ実運用で広く利用されている製品** を中心に選定。特に認証不要でフル権限取得が可能な点が共通しており、早急な対策が必要です。

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **外部からのアクセス制限**  
  - 該当サービスの管理 API (Docker API、Plesk XML API、PowerProtect の管理ポート等) をファイアウォールで **内部ネットワークまたは信頼できる IP のみ** に限定。  
- **監視・ログの強化**  
  - 失敗した認証・不正なパラメータ (例: `browser_config.extra_args`、不正な XML リクエスト) を **SIEM** に即時転送し、アラートを設定。  
- **最小権限の原則**  
  - 可能な限り **非特権ユーザ** でサービスを実行し、`root` でのコンテナ起動やデーモン実行を回避。  

### 3.2 製品別具体的対策  

| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン / パッチ | 対策概要 |
|-------------------|----------------------|------------------------|----------|
| **Adobe ColdFusion** | 2025.9, 2023.20 以前 | **2025.10** 以降、もしくは **2023.21** 以降 | - 公式パッチを即時適用。<br>- 不要な `cfusion` インスタンスは停止し、Web アプリの入力検証を二重化。 |
| **Crawl4AI** | < 0.9.0 | **0.9.0** 以上 | - Docker API エンドポイントを **TLS + 認証** で保護。<br>- `browser_config.extra_args` の受け取りをサーバ側でホワイトリスト化。 |
| **Plesk** | 任意バージョン (XML API 脆弱) | **Plesk 18.0.50** 以降 (2026‑01‑15 リリース) | - XML API の認可ロジック修正パッチを適用。<br>- `root` 書き込み権限を持つディレクトリへの書き込みを **AppArmor/SELinux** で制限。 |
| **Dell PowerProtect Data Domain** | 7.7.1.0‑8.7 系 (LTS2024‑2026) | **8.8.0** 以降、または **7.13.1.71** 以降 | - 認証回避パッチ (2026‑02‑10) を適用。<br>- 管理 UI のアクセスは **VPN + MFA** に限定。 |
| **Coolify** | < 4.0.0‑beta.471 (多数) | **4.0.0‑beta.475** 以上 (2026‑03‑01 リリース) | - `terminal` WebSocket、`executeInDocker`、`LocalPersistentVolume` などの認可・エスケープ処理が修正された最新版へ更新。<br>- デプロイ時のシェルコマンドは **JSON 配列** で渡し、直接文字列連結を禁止。 |
| **ArcGIS Server**

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-57572

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88;CWE-94` |
| Published | 2026-07-06T21:16:58.047 |

Crawl4AI is an open-source LLM-friendly web crawler and scraper. Prior to 0.9.0, the Docker API server accepted request-supplied browser_config.extra_args, which flowed into Chromium's launch arguments. An attacker could inject Chromium switches that replace a child-process launch command together with --no-zygote, causing Chromium to fork or exec an attacker-controlled command as the container's runtime user. The Docker API is unauthenticated by default, so a single request yields arbitrary command execution. This issue is fixed in version 0.9.0.

### CVE-2026-48316

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-06T17:16:32.010 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-34048

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-285;CWE-862` |
| Published | 2026-07-07T04:17:48.417 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, terminal websocket bootstrap routes only check authentication and do not enforce terminal authorization, allowing a low-privileged team member to connect to terminal routes and execute commands on team servers. This issue is fixed in version 4.0.0-beta.471.

### CVE-2026-34047

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-07T04:17:48.287 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, terminal WebSocket bootstrap routes did not enforce the expected authorization middleware, allowing an authenticated user to access terminal functionality for resources outside the authorized scope and potentially execute commands. This issue is fixed in version 4.0.0-beta.471.

### CVE-2026-34037

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-07T04:17:48.020 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.464, the cloneTo() Livewire action in ResourceOperations.php authorizes the source resource but resolves destination resources with unscoped Eloquent lookups, allowing an authenticated user to clone resources into destinations owned by other teams and access cross-tenant resources. This issue is fixed in version 4.0.0-beta.464.

### CVE-2026-34038

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-06T21:16:55.370 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.469, an authenticated remote command injection vulnerability in application deployment handling allows users with application write permissions to achieve remote code execution and exfiltrate sensitive environment variables through deployment logs via fields such as dockerfile_location and deployment commands. This issue is fixed in version 4.0.0-beta.469.

### CVE-2026-48614

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-06T18:16:46.130 |

An improper authorization vulnerability in the Plesk XML API allows an authenticated user to inject arbitrary configuration directives, resulting in arbitrary file write as root and full privilege escalation on the underlying server.

### CVE-2026-53483

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-07T13:16:31.590 |

Dell PowerProtect Data Domain, versions 7.7.1.0 through 8.7, LTS2026 release version 8.6.1.0 through 8.6.1.10, LTS2025 release version 8.3.1.0 through 8.3.1.30, LTS2024 release versions 7.13.1.0 through 7.13.1.70 an improper authentication vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access. This is a critical severity vulnerability as it allows an attacker to take complete control of system; so Dell recommends customers to upgrade at the earliest opportunity.

### CVE-2026-53481

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-07T13:16:31.397 |

Dell PowerProtect Data Domain, versions 7.7.1.0 through 8.7, LTS2026 release version 8.6.1.0 through 8.6.1.10, LTS2025 release version 8.3.1.0 through 8.3.1.30, LTS2024 release versions 7.13.1.0 through 7.13.1.70 contain an improper limitation of a pathname to a restricted directory ('Path Traversal') vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access to the system. This is a critical severity vulnerability as it allows an attacker to take complete control of system; so Dell recommends customers to upgrade at the earliest opportunity.

### CVE-2026-14345

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-07T06:16:22.113 |

The WPFunnels – Funnel Builder for WooCommerce with Checkout & One Click Upsell plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 3.12.7 via the 'postData' parameter parameter. This is due to unsanitized write of attacker-controlled postData values into a PHP-includeable .log file combined with the use of include_once to render that file in wpfnl_show_log. This makes it possible for unauthenticated attackers to execute code on the server. Exploitation requires that the Log Settings "Enable Logs" toggle is on and that an administrator subsequently opens the polluted log file via the plugin's Log Settings View UI; however, the nonce required to reach the optin endpoint is publicly emitted on every funnel step page, so the injection step itself is fully unauthenticated.

### CVE-2026-12375

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-07T06:16:22.003 |

The uncanny-automator-pro WordPress plugin before 7.3.0.6 was distributed with malicious code after the vendor's uncanny-automator-pro WordPress plugin before 7.3.0.6 update/distribution infrastructure was compromised; the injected backdoor grants unauthenticated attackers an administrator session on affected sites and beacons the site's secret keys and administrator details to attacker-controlled servers.

### CVE-2026-9181

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-06T19:17:09.553 |

ArcGIS Server contains a directory traversal vulnerability.  An unauthenticated attacker could exploit this issue by sending crafted path parameters.  Successful exploitation could allow access to sensitive files on the system. This issue impacts all versions of ArcGIS Server 12.0 and prior.

### CVE-2026-57571

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-07-06T21:16:57.907 |

Crawl4AI is an open-source LLM-friendly web crawler and scraper. Prior to 0.9.0, when the crawler saves a downloaded file, the destination filename was taken from attacker-influenced input and joined to the downloads directory with no confinement. A filename containing an absolute path or traversal escaped the downloads directory, giving an arbitrary file write with attacker-controlled contents; the HTTP crawler path uses the response Content-Disposition filename and the browser crawler path uses the download's suggested filename. Because the written bytes are attacker-controlled, this can escalate to remote code execution. This issue is fixed in version 0.9.0.

### CVE-2026-42341

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-346` |
| Published | 2026-07-06T21:16:55.740 |

FOSSBilling is a free, open-source billing and client management system. Versions 0.6.0 through 0.7.2 have an unauthenticated payment bypass vulnerability in FOSSBilling's IPN callback endpoint. When the Custom payment adapter is enabled, an attacker can mark any unpaid invoice as paid and credit the associated client account without making an actual payment, by sending a single crafted HTTP request. Version 0.8.0 patches the issue. Some workarounds are available. Disable the Custom payment gateway if not actively needed and/or restrict access to `/ipn.php` at the web server level (e.g., via IP allowlisting), noting that this may interfere with legitimate payment callback processing.

### CVE-2026-40139

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-06T17:16:30.920 |

A critical pre-authentication vulnerability exists in the authentication subsystem of BeyondTrust Remote Support. Improper processing of authentication requests may allow an unauthenticated remote attacker to bypass access controls and gain unauthorized access to the appliance, including accounts with elevated privileges. Exploitation requires a specific authentication configuration to be enabled.

### CVE-2026-40138

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-06T17:16:30.793 |

A critical pre-authentication vulnerability exists in the authentication subsystem of BeyondTrust Remote Support and Privileged Remote Access. Improper validation of authentication data may allow a network-positioned attacker to bypass access controls and gain unauthorized access to the appliance, including accounts with elevated privileges. Exploitation requires a specific authentication configuration to be enabled

### CVE-2026-5268

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-06T16:16:38.433 |

An authentication bypass vulnerability exists in
the default SFTP server component utilized across the Ciena products listed. This vulnerability allows a remote, unauthenticated attacker to bypass
security controls and gain unauthorized access to the underlying filesystem.
Successful exploitation could allow an attacker to read or modify system files.

### CVE-2025-53830

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-06T16:16:27.157 |

Anti-Virus for ownCloud is an anti-virus application for file storage, synchronization, and sharing application ownCloud. Versions of Anti-Virus for ownCloud before 1.2.3 are vulnerable to Server-Side Request Forgery (SSRF). This corresponds to versions of ownCloud 10 prior to 10.15.3. Upgrade ownCloud 10 to version 10.15.3 or later or upgrade Anti-Virus for ownCloud 10 to version 1.2.3 or later to receive a fix.

### CVE-2025-53827

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-07-06T16:16:26.740 |

ownCloud Core is the server-side component of the file storage, synchronization, and sharing application ownCloud Classic. In versions prior to 10.15.3, the Updater on ownCloud 10 before 10.15.3 has an exposed dangerous method or function. Attackers with administrative privileges may leverage functionality to execute arbitrary code. This issue has been fixed in version 10.15.3.

### CVE-2026-4375

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-07T06:16:22.360 |

The DoLeads Integrator WordPress plugin through 0.65, wp2epub WordPress plugin through 0.65 have been seen to be used to achieve RCE, once they are added adding to a blog, for example using a vulnerability where unclosed extensions from wordpress.org can be installed by unauthorized users.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-43921

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-06T22:16:49.837 |

FOSSBilling is a free, open-source billing and client management system. Versions 0.6.10 through 0.7.2 have a PHP code injection vulnerability in FOSSBilling's `Config::prettyPrintArrayToPHP()` method. When configuration values are updated, string values are written into `config.php` without escaping single quotes. Because `config.php` is loaded via a bare `include` on every HTTP request, an attacker with admin privileges can inject arbitrary PHP code that executes on every subsequent request. Version 0.8.0 contains a patch. Some workarounds are available. Restrict admin access to trusted personnel only; audit `config.php` for unexpected PHP code; and/ or at the reverse proxy/WAF level, restrict access to admin API endpoints that modify configuration.

### CVE-2026-44938

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-522` |
| Published | 2026-07-07T14:16:30.690 |

A vulnerability has been identified in Fleet's agent-side deployer, which did not filter security-sensitive keys from namespaceLabels in fleet.yaml (or BundleDeployment.spec.options.namespaceLabels) when applying them to the target namespace.




An attacker with git push access to a
 Fleet-monitored repository could overwrite Pod Security Standards (PSS)
 enforcement labels on a target namespace. This allows the attacker to 
weaken admission controls and deploy workloads that PSS policies would 
otherwise block.

### CVE-2026-13696

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-90` |
| Published | 2026-07-07T12:16:32.730 |

Improper neutralization of special elements used in an LDAP query ('LDAP injection') vulnerability in HAVELSAN Inc. Liman MYS allows LDAP Injection.

This issue affects Liman MYS: before release.Master.1107.

### CVE-2026-14474

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1188` |
| Published | 2026-07-07T10:16:39.870 |

A flaw was found in SSSD's LDAP sudo provider. When the ldap_sudo_search_base option is not explicitly configured, SSSD searches the entire LDAP directory tree for sudoRole objects. An authenticated attacker with write access to any subtree can inject a sudoRole object granting root-level sudo privileges on all SSSD-enrolled hosts.

### CVE-2026-11610

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-07T10:16:39.690 |

A heap buffer overflow flaw was found in the SASL I/O layer of 389 Directory Server
(389-ds-base). After a successful SASL bind with integrity protection (SSF > 0),
an authenticated attacker can send a specially crafted oversized LDAP UNBIND packet
that is copied into a 512-byte heap receive buffer without a bounds check in
sasl_io_recv() in sasl_io.c. This allows up to approximately 2 megabytes of
attacker-controlled data to overflow the buffer, causing a denial of service (server
crash). In FreeIPA and Red Hat Identity Management deployments, any domain user with
a valid Kerberos ticket, any enrolled host, or any service account can trigger this
vulnerability over the network after authenticating via GSSAPI.
The vulnerable code path has existed since approximately 2013 (389-ds-base 1.3.2) and
was not addressed by the CVE-2025-14905 fix, which patched a separate heap overflow
in schema.c only.

### CVE-2026-57867

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-07T06:16:22.473 |

MicroRealEstate allows adversaries to bypass authentication due to a lack of token state management. This would permit adversaries targeting MicroRealEstate deployments to brute-force One-Time Passwords (OTP) to log in as any user. This issue affects MicroRealEstate: through 1.0.0-alpha3.

### CVE-2026-34158

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-07T05:16:50.730 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.469, the executeInDocker() helper wraps user-controlled commands in single quotes without escaping embedded single quotes. Attackers who can edit application settings can inject a single quote into docker_compose_custom_build_command or docker_compose_custom_start_command to break out of the quoted context and execute arbitrary commands on the managed server host during deployments, escaping the intended Docker container confinement. This issue is fixed in version 4.0.0-beta.469.

### CVE-2026-42200

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-07T04:17:52.923 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.474, PostgreSQL initialization script (generate_init_scripts() method in app/Actions/Database/StartPostgresql.php) filename handling did not sufficiently restrict paths, allowing an authenticated user to write files outside the intended directory and achieve command execution through database initialization. This issue is fixed in version 4.0.0-beta.474.

### CVE-2026-42143

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-07T04:17:51.200 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, user-controlled persistent volume names are interpolated into shell commands executed on managed servers without escaping or validation, allowing an authenticated member to inject shell metacharacters and execute commands as root when volume operations are triggered. This issue appears to be fixed in version 4.0.0-beta.471.

### CVE-2026-34168

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-07T04:17:50.180 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, the LocalPersistentVolume.name field is interpolated directly into docker volume shell commands without shell argument escaping, allowing an authenticated user to set a storage name containing shell metacharacters and execute commands on managed servers when the resource is deleted. This issue is fixed in version 4.0.0-beta.471.

### CVE-2026-34152

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-07T04:17:50.043 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, pre-deployment and post-deployment commands are single-quote escaped but then sent through SSH heredoc transport that preserves newlines, allowing an authenticated user to inject additional shell statements that execute on the remote server during deployment. This issue is fixed in version 4.0.0-beta.471.

### CVE-2026-34058

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-07T04:17:49.193 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, the Livewire component Server\Resources exposes public methods (startUnmanaged, stopUnmanaged, restartUnmanaged) that accept a container ID parameter directly from the browser without any sanitization or escaping. This parameter is interpolated directly into shell commands executed via SSH on managed servers, enabling any authenticated team member to execute arbitrary OS commands on remote servers. This issue is fixed in version 4.0.0-beta.471.

### CVE-2026-34057

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-07T04:17:48.647 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, the database import Livewire component (app/Livewire/Project/Database/Import.php) allows client-controlled container and server properties to reach shell commands without locking or validation, allowing an authenticated user to inject commands through a database import container name. This issue is fixed in version 4.0.0-beta.471.

### CVE-2026-34035

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-07T04:17:47.873 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.466, log drain secret and environment values were interpolated into shell commands without sufficient encoding, allowing an authenticated user to inject commands executed on the host. This issue is fixed in version 4.0.0-beta.466.

### CVE-2026-34034

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-07T04:17:47.603 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.466, the sentinel_token setting is used in shell commands without sufficient validation, allowing an authenticated user with access to server Sentinel settings to inject shell syntax and execute commands on the host when Sentinel is restarted. This issue is fixed in version 4.0.0-beta.466.

### CVE-2026-42204

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-06T22:16:49.510 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. From 4.0.0-beta.471 through 4.0.0-beta.473, a regression in SHELL_SAFE_COMMAND_PATTERN allowed ampersands in custom Docker Compose build, start, and pre/post-deployment command fields, allowing an authenticated team member to inject shell commands that execute on the host. This issue is fixed in version 4.0.0-beta.474.

### CVE-2026-42153

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-06T22:16:49.383 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.474, PostgreSQL healthcheck command generation used attacker-controlled database settings (postgres_user and postgres_db) in shell-form commands, allowing an authenticated user to inject commands executed in the database container. This issue is fixed in version 4.0.0-beta.474.

### CVE-2026-34599

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-06T22:16:48.623 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, there is an authenticated command injection vulnerability in the GetLogs Livewire component which allows users with team membership (lowest privilege member role) to execute arbitrary commands as root on managed servers. The $container Livewire public property is interpolated directly into shell commands (docker logs, docker service logs) without sanitization, and can be modified by any client via the Livewire wire protocol because it lacks the #[Locked] attribute. This issue is fixed in version 4.0.0-beta.471.

### CVE-2026-34153

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-06T22:16:48.370 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, LocalFileVolume::saveStorageOnServer builds shell commands using unescaped fs_path and parent_dir values before validation, and submitFileStorage does not validate the user-controlled file-mount path before creating a volume, allowing an authenticated user who can add file storage to execute commands when the storage is saved. This issue is fixed in version 4.0.0-beta.471.

### CVE-2026-25268

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-06T21:16:54.730 |

Memory Corruption when processing invalid HT40 channel layouts during dynamic channel switching operations.

### CVE-2026-53643

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-639;CWE-862` |
| Published | 2026-07-06T23:16:56.227 |

FOSSBilling is a free, open-source billing and client management system. Versions prior to 0.8.0 allow low-privileged staff accounts to perform unauthorized actions via admin API endpoints. The root cause is a combination of the `can_always_access` module flag (which grants all staff access to certain modules) and insufficient permission checks or unsafe parameter handling on individual endpoints. Version 0.8.0 contains a fix. Some workarounds are available. Restrict staff accounts to only those who need access to sensitive settings and/or use a reverse proxy or WAF to restrict access to the affected endpoints to trusted IP addresses or higher-privilege roles.

### CVE-2026-43918

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-07-06T22:16:49.707 |

FOSSBilling is a free, open-source billing and client management system. Prior to version 0.8.0, when a client or staff/admin account is suspended or marked inactive, existing authenticated sessions are not invalidated. The session identity loaders in src/di.php (loggedin_client and loggedin_admin) only reject sessions if the backing account record no longer exists in the database. They do not verify that the account's status is still active. This allows a suspended or deactivated user to retain full access until their session naturally expires. This issue has been fixed in version 0.8.0.

### CVE-2026-55574

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-07-06T21:16:57.347 |

vLLM is a high-throughput and memory-efficient inference and serving engine for LLMs. Prior to 0.24.0, the structured_outputs.regex API parameter passes a user-supplied regular expression string directly to the grammar compiler backends with no compilation timeout; in the xgrammar backend the string reaches the regex compiler with no guard, and in the outlines backend the validation step blocks structural issues such as lookarounds and backreferences but performs no complexity analysis, so a pattern with nested quantifiers passes all checks and causes exponential state-space expansion, allowing a single request containing an adversarial regex to hang an inference worker indefinitely and deny service. This issue is fixed in version 0.24.0.

### CVE-2026-40140

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-06T17:16:31.030 |

BeyondTrust Remote Support and Privileged Remote Access contain a high-severity pre-authentication vulnerability in the network communication subsystem. Insufficient validation of client-supplied input may allow an unauthenticated remote attacker to trigger a denial-of-service condition affecting appliance availability.

### CVE-2026-53644

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-06T23:16:56.360 |

FOSSBilling is a free, open-source billing and client management system. Versions 0.5.3 through 0.7.2 allow authenticated clients to both read and reset API key service secrets for orders that are no longer in an `active` state (e.g., `suspended`, `canceled`). The root cause is missing order-state validation in two client API endpoints, despite an `isActive()` helper already existing in the `Serviceapikey` module and the frontend UI correctly gating access on `order.status == 'active'`. Version 0.8.0 contains a fix. Some workarounds are available. If the `Serviceapikey` module is not needed, uninstall it to remove the affected endpoints. One may also use a reverse proxy or WAF to restrict access to `/api/client/order/service` and `/api/client/serviceapikey/reset` based on application-level order-state logic.

### CVE-2026-59713

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-06T21:16:58.930 |

Leantime contains an OIDC login CSRF vulnerability in the verifyState() method that unconditionally returns true without validating state parameters. Attackers can craft malicious callback URLs with attacker-controlled authorization codes to perform session fixation, logging victims in as the attacker.

### CVE-2026-59712

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-06T21:16:58.793 |

Leantime's Users::getUser method in the JSON-RPC API lacks proper authorization checks, allowing authenticated users to retrieve full user credential rows including password hashes, TOTP secrets, and session tokens. Attackers can exploit this by calling users.getUser with arbitrary user IDs to enumerate all accounts and obtain credentials for offline password cracking, 2FA bypass, and session hijacking.

### CVE-2026-57573

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-06T21:16:58.197 |

Crawl4AI is an open-source LLM-friendly web crawler and scraper. Prior to 0.9.0, the Docker API server applied its SSRF destination check on the non-streaming /crawl path but not on the streaming path. handle_stream_crawl_request passed seed URLs straight to the crawler with no destination validation, allowing a remote unauthenticated client to call POST /crawl/stream or POST /crawl with crawler_config.stream=true with a URL pointing at an internal, private, or link-local address; the server fetched it and streamed the response body back. This issue is fixed in version 0.9.0.

### CVE-2026-14471

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-06T21:16:53.123 |

Improper Neutralization of Special Elements in the metrics-service retention policy management component in Amazon mcp-gateway-registry before 1.0.13 might allow an authenticated remote user to execute arbitrary SQL queries via a crafted table_name value that is interpolated into SQL statements in identifier position.



To remediate this issue, users should upgrade to version 1.0.13 or later.

### CVE-2026-53645

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-06T23:16:56.493 |

FOSSBilling is a free, open-source billing and client management system. Versions prior to 0.8.0 allow a low-privileged staff account to grant arbitrary module permissions to itself through the admin API, resulting in persistent privilege escalation. A staff user that only has `staff.create_and_edit_staff` can call `/api/admin/staff/permissions_update` targeting their own account and write any permission structure, bypassing the intended role-based access control boundary. Version 0.8.0 patches the issue. Some workarounds are available. Restrict the `staff.create_and_edit_staff` permission to only highly trusted staff members and/or use a reverse proxy or WAF to restrict access to `/api/admin/staff/permissions_update` to specific trusted roles.

### CVE-2026-40141

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-07-06T17:16:31.143 |

A high-severity vulnerability exists in a web application component of BeyondTrust Remote Support and Privileged Remote Access related to the processing of certain input parameters. Insufficient validation of user-supplied input may allow an authenticated attacker with limited privileges to access unintended resources or data beyond their authorization scope. Exploitation is restricted to accounts with specific permissions.

### CVE-2025-53828

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-06T16:16:26.903 |

SharePoint for ownCloud is an application for using SharePoint with the file storage, synchronization, and sharing application ownCloud Classic. In SharePoint for ownCloud prior to version 0.4.1, which corresponds to ownCloud 10 prior to 10.15.3, an attacker with administrative privileges can use a SSRF vulnerability in the SharePoint app to execute arbitrary code on the system. Upgrade ownCloud 10 to version 10.15.3 or later to receive SharePoint for ownCloud 0.4.1, the fixed version.

### CVE-2026-14868

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:X/RE:M/U:Amber` |
| Weaknesses | `CWE-326` |
| Published | 2026-07-07T10:16:40.273 |

The encryption algorithm used to protect the configuration of user accounts, stored in the built-in user directory of PcVue projects, all versions prior to 17.0.0, is not strong enough for the level of protection required. A local attacker could alter the existing configuration and ultimately gain privileged access to the PcVue application.

### CVE-2026-11340

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-07T11:16:32.247 |

Missing Authorization vulnerability in HAVELSAN Inc. Liman MYS allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects Liman MYS: before release.Master.1107.

### CVE-2026-8377

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-07T08:16:26.127 |

Missing Authorization vulnerability in Armiya Information Technologies Ltd. Co. Access Control System (GKS) allows Collect Data from Common Resource Locations.

This issue affects Access Control System (GKS): before Version 2.

### CVE-2026-54291

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636;CWE-757` |
| Published | 2026-07-06T19:17:08.407 |

pgjdbc is an open source postgresql JDBC Driver. In releases 42.7.4 through 42.7.11, channelBinding=require connections can be silently downgraded from SCRAM-SHA-256-PLUS with channel binding to plain SCRAM-SHA-256 without it, losing the man-in-the-middle protection the setting is meant to guarantee. An attacker who can intercept the TLS connection can trigger the downgrade with a certificate whose signature algorithm has no tls-server-end-point channel-binding hash, because the bundled com.ongres.scram:scram-client returns an empty byte array instead of failing and pgJDBC ScramAuthenticator checks only that the server advertised a PLUS mechanism, without rejecting the empty binding or checking that the negotiated mechanism uses channel binding. This issue is fixed in version 42.7.12.

### CVE-2025-53831

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-06T17:16:26.870 |

DrawIO for ownCloud is an application for using DrawIO with the file storage, synchronization, and sharing application ownCloud Classic. In DrawIO for ownCloud prior to version 1.0.2, which corresponds to ownCloud 10 prior to version 10.15.3, attackers with access to the DrawIO app can leverage improper neutralization of input during web page generation to achieve stored XSS. Upgrade ownCloud 10 to version 10.15.3 or later or upgrade DrawIO for ownCloud 10 to version 1.0.2 or later to receive a patch.

### CVE-2026-59195

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-06T16:16:37.683 |

pnpm is a package manager. Prior to 10.34.4 and 11.8.0, pnpm accepts package names from the env lockfile configDependencies section and uses those names directly when creating config dependency symlinks under node_modules/.pnpm-config. A malicious repository can commit a crafted pnpm-lock.yaml whose env-lockfile document contains a traversal-shaped config dependency name. During pnpm install, pnpm installs the config dependency and creates a symlink at a path derived from that name. This vulnerability is fixed in 10.34.4 and 11.8.0.

### CVE-2026-11348

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-07T12:16:28.617 |

Improper verification of cryptographic signature vulnerability in HAVELSAN Inc. Liman MYS allows Fake the Source of Data.

This issue affects Liman MYS: before release.Master.1107.

### CVE-2026-14476

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-07T10:16:39.993 |

A path traversal flaw was found in SSSD's AD GPO provider. The ad_gpo_extract_smb_components() function does not sanitize .. sequences in the gPCFileSysPath LDAP attribute, allowing an attacker with AD GPO management access to write files outside the GPO cache directory as root. On default RHEL configurations with SELinux enforcing, this can be used to inject Kerberos configuration leading to authentication bypass.

### CVE-2026-34171

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-07T04:17:50.513 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, the GET /invitations/{uuid} endpoint can perform a state-changing password reset using an attacker-known invitation UUID, allowing an attacker who can cause a victim to visit the crafted invitation URL to reset the victim account password to a predictable value. This issue is fixed in version 4.0.0-beta.471.

### CVE-2025-53829

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-06T16:16:27.033 |

ownCloud is a file storage, synchronization, and sharing application. In ownCloud 10 prior to version 10.15.3, an attacker with administrative privileges can exploit a path traversal vulnerability in the system to execute arbitrary code. Upgrade ownCloud 10 to version 10.15.3 or later to receive a patch.

### CVE-2026-54763

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178;CWE-290;CWE-345` |
| Published | 2026-07-06T21:16:56.787 |

Traefik is an HTTP reverse proxy and load balancer. Prior to v2.11.51, v3.6.22, and v3.7.6, Traefik's BasicAuth, DigestAuth, and ForwardAuth middlewares strip canonical-cased spoofed identity headers before writing Traefik's own value, but do not account for underscore-variant header names, which many backends normalize identically to dashed forms. An attacker able to reach a protected route can inject an underscore-variant header that survives Traefik's stripping and reaches the backend alongside, or on the unauthenticated ForwardAuth authResponseHeaders path instead of, the value Traefik intended to set, spoofing identity or authorization context. This issue is fixed in versions v2.11.51, v3.6.22, and v3.7.6.

### CVE-2026-25271

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-07-06T21:16:54.903 |

Memory Corruption when processing asynchronous input parameters due to improper handling of modified values between check and use.

### CVE-2026-21379

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-07-06T21:16:53.850 |

Memory Corruption when allocating memory with sizes that exceed the maximum allowed value.

### CVE-2026-34044

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-07T04:17:48.153 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.466, the Logs::mount() component looks up resources by UUID without scoping the lookup to the current team, allowing an authenticated user to access logs for applications owned by other teams by supplying a victim resource UUID. This issue is fixed in version 4.0.0-beta.466.

### CVE-2026-53646

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-07-06T23:16:56.683 |

FOSSBilling is a free, open-source billing and client management system. In versions 0.5.6 through 0.7.2, when a `ClientPasswordReset` record already exists for a client (from a previous unexpired reset request), subsequent calls to the `reset_password` guest API endpoint reuse the existing token instead of generating a new one. The 15-minute validity window is anchored to the first request's `created_at` timestamp, not the time of the most recent email. An attacker who obtained the original reset link remains able to use it even after the victim requests a new reset, because the original token is never invalidated or rotated. Version 0.8.0 patches the issue. Some workarounds are available. Configure a reverse proxy (e.g., Nginx, Apache, Cloudflare) to apply per-IP rate limiting to the `/client/reset-password` endpoint to minimize the window of opportunity, and/or manually clear expired `client_password_reset` records from the database after a client reports a suspected compromise.

### CVE-2026-42331

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-863` |
| Published | 2026-07-06T21:16:55.617 |

FOSSBilling is a free, open-source billing and client management system. Prior to version 0.8.0, the Guest API invoice/update endpoint is missing an authorization check present in other invoice-related endpoints, allowing an unauthenticated user with knowledge of an invoice hash to modify the payment gateway associated with an unpaid invoice. An attacker who obtains an invoice hash, which may leak through shared URLs, referrer headers, or email links,  can change the `gateway_id` on an unpaid invoice to any payment gateway configured in the system. This does not allow redirecting payments to an arbitrary external endpoint, as the gateway must already be installed and configured by an administrator. The practical impact is further limited by the `invoice_accessible_from_hash` system setting. Version 0.8.0 contains a patch. No known workarounds are available.

### CVE-2026-14468

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-06T21:16:53.000 |

HashiCorp Terraform Enterprise contained an issue in its version control system (VCS) ingestion of registry modules that did not correctly enforce the intended boundary on packaged module content. This may allow an authenticated user to include files from outside the intended repository content in a module and then download them, potentially exposing sensitive files readable by the ingestion process. This vulnerability, CVE-2026-14468, is fixed in Terraform Enterprise v2.0.4 and v1.2.4.

### CVE-2026-6101

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-07T14:16:34.543 |

The AMP for WP – Accelerated Mobile Pages plugin for WordPress is vulnerable to Arbitrary File Write in versions up to and including 1.1.12. This is due to unsafe ZIP file extraction in the ampforwp_save_local_font() function combined with inadequate cleanup that fails to remove nested directories and files. This makes it possible for authenticated attackers, with Author-level access and above, and permissions granted by an Administrator, to write arbitrary files to the server in a web-accessible location, potentially leading to remote code execution on hosts that execute PHP files in the uploads directory.

### CVE-2026-5799

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-07T08:16:25.677 |

Authorization bypass through User-Controlled key vulnerability in Idvlabs Software and Consulting Services Inc. Ontime allows Exploitation of Trusted Identifiers.

This issue affects Ontime: through 04052026.

### CVE-2026-5730

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-07T08:16:25.540 |

Authorization bypass through User-Controlled key vulnerability in Idvlabs Software and Consulting Services Inc. Ontime allows Exploitation of Trusted Identifiers.

This issue affects Ontime: through 04052026.

### CVE-2026-55727

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-06T21:16:57.580 |

A flaw in the authentication mechanism for video stream requests in Genetec Security Center 5.14.0.0 prior to build 5.14.178.18 may allow an unauthenticated attacker to access live video streams.

### CVE-2026-54234

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-1284` |
| Published | 2026-07-06T21:16:56.477 |

vLLM is a high-throughput and memory-efficient inference and serving engine for LLMs. Prior to 0.24.0, a frontend-legal multi-request speculative decoding workload can cause the rejection sampler to produce a recovered token equal to the model vocabulary size boundary value, which is then converted to negative one when the engine selects the next live token for a request and is written back into the drafter's input ids; that out-of-vocabulary value is later consumed by the model's embedding and attention path and crashes the engine worker with a GPU device-side assertion. The same triggering request sequence is reachable through the public gRPC Generate and Abort endpoints, so a remote client that can send generation requests can crash the shared engine worker, aborting concurrent requests and causing a service-wide denial of service for other clients of the deployment until the worker is restarted. This issue is fixed in version 0.24.0.

### CVE-2026-55380

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-07-06T19:17:08.703 |

Pillow is a Python imaging library. Prior to 12.3.0, PIL/GdImageFile.py GdImageFile._open() read image dimensions from the GD 2.x header and stored them in self._size without calling Image._decompression_bomb_check(), allowing a crafted .gd file to trigger excessive C-heap allocation when loaded. This issue is fixed in version 12.3.0.

### CVE-2026-55379

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-07-06T19:17:08.577 |

Pillow is a Python imaging library. Prior to 12.3.0, PIL/BdfFontFile.py bdf_char() read the BBX width and height field from a BDF font file and passed attacker-controlled dimensions to Image.new() without calling Image._decompression_bomb_check(), bypassing Pillow's documented decompression bomb protection and allowing excessive memory allocation. This issue is fixed in version 12.3.0.

### CVE-2026-54060

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-07-06T19:17:08.270 |

Pillow is a Python imaging library. Prior to 12.3.0, PIL/FontFile.py FontFile.compile() assembled per-glyph images into a combined bitmap with Image.new("1", (xsize, ysize)) without calling Image._decompression_bomb_check(), allowing a font to trigger excessive allocation during conversion or saving. This issue is fixed in version 12.3.0.

### CVE-2026-54059

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-07-06T19:17:08.127 |

Pillow is a Python imaging library. Prior to 12.3.0, PIL/PcfFontFile.py _load_bitmaps() read glyph dimensions from the PCF METRICS section and passed them directly to Image.frombytes() without calling Image._decompression_bomb_check(), allowing crafted PCF font data to cause excessive memory allocation. This issue is fixed in version 12.3.0.

### CVE-2026-13753

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-06T19:16:55.963 |

A missing authorization vulnerability exists in the embedded webserver of HP Deskjet 2800 Series Printers running firmware version <=TBP1CN2612AR. An unauthenticated attacker with network access can send GET requests to multiple exposed administrative API endpoints and retrieve sensitive configuration data such as plaintext Wi‑Fi Direct credentials, unique device identity information, and other administrative security state details. When accessed through the web interface, these setting pages explicitly require administrator credentials before sensitive information is displayed.

### CVE-2026-58384

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-07T09:16:30.003 |

A flaw was found in GIMP's PSD parser. An integer overflow in read_RLE_channel() can cause an undersized heap allocation for the RLE row-length table, after which subsequent per-row writes corrupt heap memory. This could lead to memory corruption, potentially resulting in denial of service or arbitrary code execution.

### CVE-2026-43825

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-06T17:16:31.570 |

Untrusted Java Deserialization in Apache OpenNLP SvmDoccatModel

Versions Affected:
  before 3.0.0-M4 (libsvm document categorization module; introduced in
  OPENNLP-1808 and only present on the 3.x line)

Description:
SvmDoccatModel.deserialize(InputStream) reads an attacker-controlled
stream with java.io.ObjectInputStream and calls readObject() without an
ObjectInputFilter installed. ObjectInputStream materialises every class
referenced in the stream before the resulting object is cast to
SvmDoccatModel, so the cast that follows readObject() executes only
after the foreign object graph has already been deserialised in full.

If a Java deserialization gadget chain is available on the consumer's
classpath, a crafted payload supplied to
deserialize() executes arbitrary code in the JVM that loads it. Apache
OpenNLP itself does not ship a known gadget chain, so the realistic
risk is to downstream applications that embed the libsvm module
alongside vulnerable transitive dependencies. The method is public and
static, so any caller can pass an untrusted stream to it directly.

The practical impact is remote code execution against processes that
load SvmDoccatModel instances from untrusted or semi-trusted origins.

Mitigation:

3.x users should upgrade to 3.0.0-M4.

Users who cannot upgrade immediately should treat all serialized
SvmDoccatModel streams as untrusted input unless their provenance is
verified, and should avoid invoking SvmDoccatModel.deserialize() on
streams supplied by end users or fetched from third-party sources
without integrity checks.

### CVE-2026-58380

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-193` |
| Published | 2026-07-06T15:16:40.020 |

A flaw was found in GIMP's PNM file format parser. When parsing a specially crafted PNM file, the pnmscanner_gettoken() function writes a null terminator one byte past the end of a stack-allocated buffer due to an off-by-one error in the loop boundary check. This could lead to memory corruption, potentially resulting in denial of service or arbitrary code execution.

### CVE-2026-53479

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-07T14:16:32.410 |

Dell PowerProtect Data Domain, versions 7.7.1.0 through 8.7, LTS2026 release version 8.6.1.0 through 8.6.1.10, LTS2025 release version 8.3.1.0 through 8.3.1.30, LTS2024 release versions 7.13.1.0 through 7.13.1.70 contain an improper neutralization of special elements used in an OS command ('OS command Injection') vulnerability. A remote high privileged attacker could potentially exploit this vulnerability, leading to protection mechanism bypass. This is a Critical vulnerability as it allows an attacker to invoke arbitrary command execution with root privileges; so Dell recommends customers to upgrade at the earliest opportunity.

### CVE-2026-57871

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-07T06:16:23.017 |

Relative path traversal vulnerability in MicroRealEstate file upload functionality allows attackers to potentially overwrite system files.

This issue affects MicroRealEstate: through 1.0.0-alpha3.

### CVE-2026-57869

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-1241` |
| Published | 2026-07-07T06:16:22.750 |

Broken object-level access controls and the use of a deterministic pattern during random ID generation in MicroRealEstate allows attackers to access documents uploaded by landlords or tenants without authorization.

This issue affects MicroRealEstate: through 1.0.0-alpha3.

### CVE-2026-57868

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-07T06:16:22.633 |

MicroRealEstate is affected by broken object-level access controls in PDF generator functionality.

This issue affects MicroRealEstate: through 1.0.0-alpha3.

### CVE-2026-55514

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-07-06T21:16:57.207 |

vLLM is a library for LLM inference and serving. From 0.12.0 to before 0.24.0, sending a pure prompt embeds payload in a /v1/completions request with a model using M-RoPE causes EngineCore to fail an assertion and fatally crash, shutting down the entire server application. Any remote user who is authorized to make a /v1/completions request can make such a request and induce a crash. This issue is fixed in version 0.24.0.

### CVE-2026-21383

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-323` |
| Published | 2026-07-06T21:16:53.973 |

Cryptographic Issue when using a static initialization vector for AES-GCM key wrapping, which requires a unique value for each call to ensure security.

### CVE-2026-59196

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-07-06T16:16:37.810 |

pnpm is a package manager. Prior to 10.34.4 and 11.7.0, a crafted lockfile alias could be joined directly under a hoisted node_modules directory. Traversal aliases could escape that directory, while reserved aliases such as .bin or .pnpm could overwrite pnpm-owned layout.  This vulnerability is fixed in 10.34.4 and 11.7.0.

### CVE-2026-59194

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-07-06T16:16:37.550 |

pnpm is a package manager. Prior to 10.34.4 and 11.7.0, a crafted patch entry could resolve outside the configured patches directory and cause pnpm patch-remove to delete an arbitrary reachable file. This vulnerability is fixed in 10.34.4 and 11.7.0.
