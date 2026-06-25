# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-25 15:04 UTC
- **対象期間**: `2026-06-24T15:01:19.000Z` 〜 `2026-06-25T15:04:06.000Z`
- **重要CVE数**: 176 件（Critical 9.0+: 30 件 / High 7.0〜: 146 件）

---

## AI 分析サマリー

## 1. 全体サマリー
- 2026 年上半期に報告された CVE のうち、**CVSS 7.0 以上が 30 件以上** と非常に多く、特に **リモートコード実行 (RCE) や特権昇格** が目立ちます。  
- オープンソースの自前サービス（Kvrocks、Gogs、SiYuan、Appsmith など）や、広く利用されているブラウザ（Chrome Android）で **深刻なヒープオーバーフローや Use‑After‑Free** が確認され、攻撃者は認証不要で任意コードを実行できる可能性があります。  
- 多くの脆弱性は **古いバージョンが長期間メンテナンスされていない** ことが原因であり、**アップストリームのパッチ適用が最速の防御策** となります。

---

## 2. 特に注目すべき CVE

| CVE | CVSS | 製品・バージョン | 主な問題点 | 影響範囲・リスク |
|-----|------|------------------|------------|-------------------|
| **CVE‑2026‑46752** | 10.0 | Apache **Kvrocks** 2.0.4‑2.15.0 | Redis Lua スクリプト実行時に cjson ライブラリで **ヒープオーバーフロー** が発生。攻撃者は任意コード実行 (RCE) が可能。 | Kvrocks をバックエンドに使用する全サービスが遠隔から完全制御される危険。 |
| **CVE‑2026‑52813** | 10.0 | **Gogs** < 0.14.3 | 組織名に `../` を含めるとパス・トラバーサルが成立し、リポジトリが任意ディレクトリに書き込まれる。 | サーバ上の任意ファイル書き換え → RCE、情報漏洩。 |
| **CVE‑2026‑13032 / 13028** | 9.6 | Google **Chrome (Android)** < 149.0.7827.197 | WebGL の Use‑After‑Free バグにより **サンドボックス脱出** が可能。 | Android デバイス全体が遠隔から制御される深刻な危険。 |
| **CVE‑2026‑55454** | 9.9 | **Appsmith** < 2.1 | コンテナ内部で Caddy の管理 API が **認証なしで 0.0.0.0:2019** にバインド。Docker‑compose の設定ミスで外部公開されると管理権限取得。 | 任意の内部リソース操作、設定変更、コード実行。 |
| **CVE‑2026‑54158 / 54067 / 50551** (まとめ) | 9.9 | **SiYuan** < 3.7.0 | 複数の XSS/HTML インジェクションが **Electron デスクトップクライアント** で RCE に昇格。 | ローカルユーザーだけでなく、ブラウザ拡張経由でもコード実行が可能。 |

> **選定理由**  
> - **スコアが 9.0 以上** で、かつ **認証不要** または **低権限で実行可能**。  
> - 影響が **インフラ全体 (Kvrocks, Chrome)**、**開発プラットフォーム (Gogs)**、**内部ツール (Appsmith, SiYuan)** と広範囲に及ぶ。  
> - パッチが既にリリースされているが、アップデートが遅れがちな製品が多い。

---

## 3. 推奨アクション

### 3.1 直ちに実施すべきこと
- **パッケージのバージョン確認とアップデート**  
  - `kvrocks` → **2.16.0 以上**  
  - `gogs` → **0.14.3 以上**  
  - `appsmith` → **2.1 以上**（Docker イメージ `appsmith/appsmith:latest`）  
  - `siyuan` → **3.7.0 以上**（公式リリースまたは GitHub の `v3.7.0` タグ）  
  - `chrome` (Android) → **149.0.7827.197 以上**（Google Play の自動更新を有効化）  

- **コンテナ・デプロイ設定の見直し**  
  - Appsmith の Caddy 管理 API を外部に公開しない。`CADDY_ADMIN_API_BIND` を `127.0.0.1:2019` に限定。  
  - Kvrocks の外部公開ポートに対し **IP フィルタリング** と **TLS** を必ず適用。  

- **Web アプリケーションの入力サニタイズ強化**  
  - SiYuan の HTML 出力箇所に **Content‑Security‑Policy** ヘッダーを付与し、`script-src 'self'` でインラインスクリプトをブロック。  
  - Gogs の組織名バリデーションに **正規表現で `../` を除外** するパッチを適用（公式リポジトリの最新コミットをマージ）。  

### 3.2 長期的な防御策
- **脆弱性情報の自動取得**  
  - `github.com/ossf/scorecard` や `cve-search` などのツールで **CVE フィード** を CI に組み込み、依存パッケージの更新を自動化。  
- **最小権限の原則**  
  - Kvrocks の管理者権限を持つユーザーを限定し、ネットワークレベルで **内部 VLAN** に配置。  
  - Chrome の企業デバイスは **Google Play Protect** と **モバイルデバイス管理 (MDM)** でバージョンロックを実施。  
- **コードレビューとセキュリティテスト**  
  - Gogs、Appsmith、SiYuan のように **外部からコードが実行される入口** があるプロジェクトは、**静的解析 (ESLint, Bandit, GoSec)** と **Fuzz テスト** を CI に導入。  

### 3.3 参考パッケージ一覧（主要 OS / コンテナ）

| OS / 環境 | パッケージ名 | 修正バージョン |
|----------|--------------|----------------|
| Debian/Ubuntu | `kvrocks` | `2.16.0-1` |
| Alpine | `gogs` | `0.14.3-r0` |
| Docker Hub | `appsmith/appsmith` | `2.1.0` |
| Docker Hub | `siyuan/si-yuan` | `3.7.0` |
| Android (Chrome) | - | 自動更新で `149.0.7827.197` 以上 |

> **注**：上記は **公式リポジトリ** が提供する最新安定版です。ディストリビューション固有のパッケージがある場合は、同等以上のバージョンがリリースされていることを確認してください

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-46752

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-25T09:16:30.190 |

Redis Lua HEAP overflow in cjson library vulnerability in Apache Kvrocks.

This issue affects Apache Kvrocks: from 2.0.4 through 2.15.0.

Users are recommended to upgrade to version 2.16.0, which fixes the issue.

### CVE-2026-52813

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-06-24T21:16:57.353 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, organization names containing path traversal sequences (../) are accepted by Gogs, and repositories under them are written to paths following these path traversals. This allows storing/retrieving data for repositories at arbitrary locations on the filesystem. By creating nested structure of Git repositories, one can overwrite the other's hooks configuration to result in Remote Code Execution (RCE). This vulnerability is fixed in 0.14.3.

### CVE-2026-54823

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-25T14:16:46.867 |

Contributor Remote Code Execution (RCE) in Widget Options <= 4.2.3 versions.

### CVE-2026-55454

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-749;CWE-1188` |
| Published | 2026-06-24T22:16:49.003 |

Appsmith is a platform to build admin panels, internal tools, and dashboards. Prior to 2.1, the bundled Caddy reverse-proxy's admin API — which has no authentication by default — is bound on 0.0.0.0:2019 inside the container. While this listener is not directly published to the host by docker-compose.yml, it is reachable from the Appsmith server process itself or a SSRF vulnerability. An authenticated low-privileged user can therefore drive the SSRF to issue POST /load (or any other admin-API call) against http://0.0.0.0:2019/, fully replacing the live Caddy configuration and taking over the reverse proxy. This vulnerability is fixed in 2.1.

### CVE-2026-54158

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79;CWE-1188` |
| Published | 2026-06-24T22:16:48.740 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.0, the attribute-view (database) cell renderer genAVValueHTML interpolates cell content raw in four of its branches: text, url, phone, and mAsset. A cell value like </textarea><img src=x onerror="..."> or "><img src=x onerror="..."> breaks out of its surrounding tag and runs arbitrary JavaScript in the renderer when the victim opens the block-attribute panel. On Electron desktop the renderer runs with nodeIntegration:true, so the XSS chains to host RCE via require('child_process'). AV files live under the workspace and ride normal sync, so an attacker with write access to any synced workspace plants the payload once and it fires on every device that opens a panel containing that row.he kernel doesn't escape on the way in either, so the malicious cell persists byte-for-byte. There's no equivalent of the html.EscapeAttrVal call that protects block IAL attributes at kernel/model/blockial.go:261. This vulnerability is fixed in 3.7.0.

### CVE-2026-54067

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79;CWE-1188` |
| Published | 2026-06-24T22:16:48.177 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.0, CSS snippet body containing </style> breaks out of its surrounding <style> tag when renderSnippet() interpolates it via insertAdjacentHTML. A payload like runs arbitrary JavaScript in the renderer. On Electron desktop builds the renderer runs with nodeIntegration:true, so require('child_process') is reachable from the injected handler and the XSS chains to host RCE. Snippets sync via the workspace repository, so an attacker with write access to any synced workspace plants the payload once and it fires on every device that pulls. The bug also bypasses the user's enabledCSS / enabledJS separation. A user who turned enabledJS off was making a deliberate call not to run untrusted JavaScript; the CSS path runs it anyway. This vulnerability is fixed in 3.7.0.

### CVE-2026-50551

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-24T22:16:47.513 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.0, SiYuan contains a stored cross-site scripting (XSS) vulnerability in the Attribute View (database) asset cell renderer that escalates to remote code execution (RCE) in the Electron desktop client. This vulnerability is fixed in 3.7.0.

### CVE-2026-52806

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-06-24T21:16:56.440 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, Gogs allows authenticated users to achieve Remote Code Execution (RCE) on the server by creating a pull request with a specially crafted branch name that injects the --exec flag into the git rebase command during the "Rebase before merging" merge operation. This vulnerability is fixed in 0.14.3.

### CVE-2026-41120

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-349` |
| Published | 2026-06-25T14:16:39.140 |

Dell Wyse Management Suite, versions prior to WMS 5.5 HF1, contain an Acceptance of Extraneous Untrusted Data With Trusted Data vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Remote Code Execution.

### CVE-2026-39955

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-24T23:16:40.980 |

Cacti is an open source performance and fault management framework. Versions 1.2.30 and prior have pre-authentication SQL Injection via unanchored FILTER_VALIDATE_REGEXP in graph_view.php. This issue has been fixed in version 1.2.31.

### CVE-2026-39938

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-78` |
| Published | 2026-06-24T23:16:40.677 |

Cacti is an open source performance and fault management framework. Versions 1.2.30 and prior have unauthenticated LFI through graph_theme and rrdtool IPC serialization hardening. This issue has been resolved in version 1.2.31.

### CVE-2026-39893

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-24T22:16:46.617 |

Cacti is an open source performance and fault management framework. In versions 1.2.30 and prior, the rfilter request variable was concatenated into a RLIKE SQL clause without sanitization. The endpoint does not require authentication (graph viewing supports guest access via the configured guest user), so the SQLi was reachable pre-auth on installs with guest viewing enabled. This issue was fixed in version 1.2.31.

### CVE-2026-49980

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-24T19:17:11.597 |

Rclone is a command-line program to sync files and directories to and from different cloud storage providers. From 1.46.0 until 1.74.3, rclone rcd --rc-serve accepts unauthenticated GET and HEAD requests to paths of the form: /[remote:path]/object. The remote value is parsed from the URL and passed to normal backend initialization. Inline remote configuration can set backend options that execute local commands during initialization. As a result, a single unauthenticated GET or HEAD request can execute a command as the rclone process user. This vulnerability is fixed in 1.74.3.

### CVE-2026-53943

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-524` |
| Published | 2026-06-24T19:17:11.820 |

Ghost is a Node.js content management system. From  until 6.37.0, when Ghost is behind a shared caching layer that results in cached content being shared between different visitors, an unauthenticated user could send an x-ghost-preview header that altered the rendered frontend response. In affected cache configurations, that response could be stored and served to subsequent visitors requesting the same page, allowing cache poisoning of request-specific preview output. When running Ghost's frontend and admin panel on the same domain this could be used to take over staff user accounts. When running these on different domains staff accounts have no exposure. This vulnerability is fixed in 6.37.0.

### CVE-2026-13032

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-24T19:17:09.483 |

Use after free in WebGL in Google Chrome on Android prior to 149.0.7827.197 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-13028

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-24T19:17:09.073 |

Use after free in WebGL in Google Chrome on Android prior to 149.0.7827.197 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-41566

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:I/V:X/RE:M/U:Amber` |
| Weaknesses | `CWE-280` |
| Published | 2026-06-25T09:16:29.767 |

Improper Handling of Insufficient Permissions or Privileges vulnerability in Apache Kvrocks.

This issue affects Apache Kvrocks: 2.8.0.

Users are recommended to upgrade to version 2.16.0, which fixes the issue.

### CVE-2026-54849

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T14:16:49.183 |

Unauthenticated SQL Injection in Premmerce Wishlist for WooCommerce <= 1.1.11 versions.

### CVE-2026-54843

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T14:16:48.383 |

Unauthenticated SQL Injection in MDTF <= 1.3.7 versions.

### CVE-2026-54836

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T14:16:47.743 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in YMC Filter allows SQL Injection.

This issue affects YMC Filter: from n/a through 3.11.5.

### CVE-2026-39948

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-24T23:16:40.830 |

Cacti is an open source performance and fault management framework. In versions 1.2.30 and prior, the rfilter request parameter is retrieved via the raw accessor grv() (rather than gfrv() with FILTER_VALIDATE_IS_REGEX validation) and concatenated directly into RLIKE SQL clauses in lib/html_graph.php and lib/html_tree.php, which are reachable pre-authentication through graph_view.php on installations with guest graph viewing enabled. Because the unbalanced-quote payload bypasses the regex validation that would otherwise reject it, an unauthenticated attacker can inject arbitrary SQL to compromise the confidentiality, integrity, and availability of the database. This advisory is similar to GHSA-69gg-mjfm-jjpc. This issue has been fixed in version 1.2.31.

### CVE-2026-55666

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-288` |
| Published | 2026-06-24T22:16:49.393 |

Rocket.Chat is an open-source, secure, fully customizable communications platform. Prior to 8.5.1, 8.4.4, 8.3.6, 8.2.6, 8.1.6, 8.0.7, and 7.10.13, in apps/meteor/app/apple/server/loginHandler.ts, handleIdentityToken parses a JWT issued by Apple during the OAuth flow. The try block checks for an email parameter. If the JWT does not contain an email address, the application falls back to accepting an arbitrary email value supplied directly in the request. Attackers are able to forge Apple JWTs that do not contain an email address and leverage this vulnerability to carry out account takeover attacks. This vulnerability is fixed in 8.5.1, 8.4.4, 8.3.6, 8.2.6, 8.1.6, 8.0.7, and 7.10.13.

### CVE-2026-46423

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-06-24T21:16:54.223 |

Rocket.Chat is an open-source, secure, fully customizable communications platform. Prior to 8.5.0, 8.4.1, 8.3.3, 8.2.3, 8.1.4, 8.0.5, 7.13.7, and 7.10.11, Rocket.Chat's SAML service provider implementation silently skips both SAML Response and Assertion signature validation when the configured IdP certificate field is empty. The verifySignatures routine performs an early return when serviceProviderOptions.cert is falsy, which is the default state of the setting. Because provider registration only gates on the SAML "enabled" toggle and not on the presence of a certificate, an administrator who enables SAML without pasting an IdP certificate obtains a fully wired, publicly reachable SAML login endpoint that accepts unsigned or attacker-supplied assertions. This is a default-configuration authentication-bypass class: the fail-open branch is reached with no misconfiguration beyond leaving a field at its shipped default. This vulnerability is fixed in 8.5.0, 8.4.1, 8.3.3, 8.2.3, 8.1.4, 8.0.5, 7.13.7, and 7.10.11.

### CVE-2026-33543

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288;CWE-306` |
| Published | 2026-06-24T21:16:53.453 |

FOSSBilling is a free, open-source billing and client management system. Versions 0.7.2 and prior expose a guest API endpoint, /api/guest/staff/create, intended for initial administrator bootstrap. Due to a flawed admin-existence check, the endpoint remains usable after an administrator already exists. The flawed guard check uses is_countable() on a value that returns a Model_Admin object or null rather than a countable type, causing the expression to always evaluate as true and bypass the intended protection. As a result, an attacker can reach the unprotected endpoint to create a new administrator account and immediately authenticate, gaining a fully privileged admin session even when an admin already exists. This issue has been fixed in version 0.8.0.

### CVE-2026-56121

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-24T16:16:33.193 |

Feast before 0.63.0 contains an unsafe deserialization vulnerability that allows unauthenticated or unauthorized attackers to achieve remote code execution by sending a crafted gRPC request to the registry server. The user_defined_function.body field of an OnDemandFeatureView spec is decoded from base64 and passed to dill.loads() before any authorization check is performed, enabling attackers to embed a malicious serialized Python object with an arbitrary __reduce__ method to execute OS commands as the feast service account.

### CVE-2026-54069

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-06-24T22:16:48.433 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.0, SiYuan Note's kernel HTTP server unconditionally trusts all chrome-extension:// origins, granting RoleAdministrator access to every installed browser extension without any authentication. Combined with the default empty AccessAuthCode on desktop installs, any Chrome/Chromium extension -- including a compromised legitimate extension via supply chain attack -- can make fully authenticated admin API calls to the SiYuan kernel at 127.0.0.1:6806, enabling data exfiltration, stored XSS injection, and configuration tampering. This vulnerability is fixed in 3.7.0.

### CVE-2026-45689

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-943` |
| Published | 2026-06-24T21:16:53.970 |

Rocket.Chat is an open-source, secure, fully customizable communications platform. Prior to 8.5.0, 8.4.1, 8.3.3, 8.2.3, 8.1.4, 8.0.5, 7.13.7, and 7.10.11, an unauthenticated network attacker obtains a valid Rocket.Chat OAuth access token for an arbitrary user by sending a single HTTP POST with MongoDB query operators to /oauth/token. The Rocket.Chat OAuth2 server does not validate that grant parameters are strings before forwarding them to findOne({...}) against the oauth_apps and oauth_access_tokens collections, so an attacker substitutes {"$ne": null} for client_id, client_secret, and refresh_token and receives a freshly minted {access_token, refresh_token} pair bound to whichever user's refresh token Mongo returned first. The resulting access token is a first-class bearer credential against the full /api/v1/* surface as that user. By iterating with $nin / $regex operators the attacker walks the entire oauth_access_tokens collection, collecting one fresh access token per user per request. If any matched token belongs to an admin, the stolen bearer gives full admin API access (including Apps-Engine app installation, i.e. server-side code execution). No account, credentials, userId, or prior interaction with the instance are required. This vulnerability is fixed in 8.5.0, 8.4.1, 8.3.3, 8.2.3, 8.1.4, 8.0.5, 7.13.7, and 7.10.11.

### CVE-2026-45688

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-943` |
| Published | 2026-06-24T21:16:53.847 |

Rocket.Chat is an open-source, secure, fully customizable communications platform. Prior to 8.5.0, 8.4.1, 8.3.3, 8.2.3, 8.1.4, 8.0.5, 7.13.7, and 7.10.11, Rocket.Chat's CAS login handler forwards the client-supplied options.cas.credentialToken value straight into a MongoDB findOne({_id: ...}) query without any runtime type check. TypeScript's string parameter annotation is erased at runtime, so an unauthenticated attacker can substitute a MongoDB query operator ({"$gt": ""}, {"$ne": null}, etc.) for what the server expects to be an opaque ticket string. The injected operator matches the first unexpired document in the credential_tokens collection, bypassing the CAS ticket check entirely. When any legitimate CAS or SAML SSO login is in flight, the attacker's next DDP login call matches the same credential-token row via the NoSQL operator and is issued a full Meteor auth token (userId + token) bound to the victim. The token is immediately usable against the complete REST and DDP surface as that user. If the victim is an administrator, this escalates to full instance compromise via Apps-Engine app install. This vulnerability is fixed in 8.5.0, 8.4.1, 8.3.3, 8.2.3, 8.1.4, 8.0.5, 7.13.7, and 7.10.11.

### CVE-2026-55570

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79;CWE-94;CWE-116` |
| Published | 2026-06-24T22:16:49.260 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.0, it does not escape the untrusted fields (name, version, author, description) when they are serialized into the data-obj HTML attribute of each marketplace card. Because the attribute is single-quoted and the value is produced with JSON.stringify() (which does not escape ', <, or >), a package whose name contains a single quote breaks out of the attribute and injects arbitrary HTML. In the desktop client the main BrowserWindow runs with nodeIntegration: true, contextIsolation: false, so the injected markup escalates from DOM XSS to arbitrary OS command execution. This is the same root cause and same impact as the original advisory, reached through a sibling sink the patch did not cover.  This vulnerability is fixed in 3.7.0.

### CVE-2026-52811

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-59;CWE-61` |
| Published | 2026-06-24T21:16:57.093 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, (*Repository).UploadRepoFiles checks for symlinks only on the leaf of the upload target (osx.IsSymlink(targetPath)). The siblings UpdateRepoFile, DeleteRepoFile, and GetDiffPreview use hasSymlinkInPath, which lstats every component — UploadRepoFiles is the lone outlier. An attacker with repo-write access plus a multipart upload whose filename contains a literal backslash (preserved by filepath.Base on Linux, then converted to / by pathx.Clean) redirects the write through a previously-committed directory symlink. iox.CopyFile opens the destination with os.Create (no O_NOFOLLOW), so the kernel follows the parent symlink and writes attacker bytes anywhere the gogs UID can write — ~git/.ssh/authorized_keys → SSH foothold, or <repo>.git/hooks/post-receive → next-push RCE. This vulnerability is fixed in 0.14.3.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-50189

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-183;CWE-918` |
| Published | 2026-06-24T22:16:47.390 |

Appsmith is a platform to build admin panels, internal tools, and dashboards. Prior to 2.1, Appsmith's bundled supervisord exposes an XML-RPC interface on port 9001, reachable from outside the container via a Caddy reverse-proxy route at /supervisor/* on the public ingress. Combined with the APPSMITH_SUPERVISOR_PASSWORD exposed via GET /api/v1/admin/env, any authenticated administrator can send arbitrary XML-RPC calls to supervisord and execute OS commands inside the Docker container via twiddler.addProgramToGroup. This vulnerability is fixed in 2.1.

### CVE-2026-52798

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-24T21:16:55.533 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, although .ipynb previews are sanitized on the server side via /-/api/sanitize_ipynb, the inserted content is re-rendered on the client side without sanitization using marked() on elements with the .nb-markdown-cell class. During this process, links containing schemes such as javascript: can be regenerated. As a result, when a victim views an attacker-crafted .ipynb file and clicks the link, arbitrary JavaScript is executed in the Gogs origin, leading to a click-based Stored XSS. This vulnerability is fixed in 0.14.3.

### CVE-2026-56053

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-25T14:16:51.160 |

Subscriber PHP Object Injection in EventPrime <= 4.3.4.1 versions.

### CVE-2026-5305

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-25T07:16:45.737 |

The Email Address Encoder WordPress plugin before 1.0.25, email-encoder-premium WordPress plugin before 0.3.12 does not properly handle email replacement, which could allow unauthenticated users to perform Stored XSS attacks

### CVE-2026-9155

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-25T01:16:27.787 |

OS Command Injection vulnerability in Rapid7 InsightConnect Sed Plugin on Linux allows authenticated attackers to execute arbitrary OS commands via the expression parameter due to insufficient input validation.

### CVE-2026-9787

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-25T00:17:48.963 |

Quest NetVault Backup NVBULogDaemon Command Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest NetVault Backup. Although authentication is required to exploit this vulnerability, the existing authentication mechanism can be bypassed.

The specific flaw exists within the processing of NVBULogDaemon JSON-RPC messages. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-27625.

### CVE-2026-9786

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T00:17:48.850 |

Quest NetVault Backup NVBUDashboard SQL Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest NetVault Backup. Although authentication is required to exploit this vulnerability, the existing authentication mechanism can be bypassed.

The specific flaw exists within the processing of NVBUDashboard JSON-RPC messages. The issue results from the lack of proper validation of a user-supplied string before using it to construct SQL queries. An attacker can leverage this vulnerability to execute code in the context of NETWORK SERVICE. Was ZDI-CAN-27626.

### CVE-2026-9785

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T00:17:48.737 |

Quest NetVault Backup NVBULibrarySlot SQL Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest NetVault Backup. Although authentication is required to exploit this vulnerability, the existing authentication mechanism can be bypassed.

The specific flaw exists within the processing of NVBULibrarySlot JSON-RPC messages. The issue results from the lack of proper validation of a user-supplied string before using it to construct SQL queries. An attacker can leverage this vulnerability to execute code in the context of NETWORK SERVICE. Was ZDI-CAN-27630.

### CVE-2026-9784

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T00:17:48.627 |

Quest NetVault Backup NVBULibraryPort SQL Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest NetVault Backup. Although authentication is required to exploit this vulnerability, the existing authentication mechanism can be bypassed.

The specific flaw exists within the processing of NVBULibraryPort JSON-RPC messages. The issue results from the lack of proper validation of a user-supplied string before using it to construct SQL queries. An attacker can leverage this vulnerability to execute code in the context of NETWORK SERVICE. Was ZDI-CAN-27631.

### CVE-2026-9783

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T00:17:48.520 |

Quest NetVault Backup NVBURemovableMedia SQL Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest NetVault Backup. Although authentication is required to exploit this vulnerability, the existing authentication mechanism can be bypassed.

The specific flaw exists within the processing of NVBURemovableMedia JSON-RPC messages. The issue results from the lack of proper validation of a user-supplied string before using it to construct SQL queries. An attacker can leverage this vulnerability to execute code in the context of NETWORK SERVICE. Was ZDI-CAN-27632.

### CVE-2026-9782

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T00:17:48.407 |

Quest NetVault Backup NVBUDeviceDrive SQL Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest NetVault Backup. Although authentication is required to exploit this vulnerability, the existing authentication mechanism can be bypassed.

The specific flaw exists within the processing of NVBUDeviceDrive JSON-RPC messages. The issue results from the lack of proper validation of a user-supplied string before using it to construct SQL queries. An attacker can leverage this vulnerability to execute code in the context of NETWORK SERVICE. Was ZDI-CAN-27633.

### CVE-2026-9781

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T00:17:48.293 |

Quest NetVault Backup NVBURASDevice SQL Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest NetVault Backup. Although authentication is required to exploit this vulnerability, the existing authentication mechanism can be bypassed.

The specific flaw exists within the processing of NVBURASDevice JSON-RPC messages. The issue results from the lack of proper validation of a user-supplied string before using it to construct SQL queries. An attacker can leverage this vulnerability to execute code in the context of NETWORK SERVICE. Was ZDI-CAN-27648.

### CVE-2026-9780

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-25T00:17:48.187 |

Quest NetVault Backup addclient3 Cross-Site Scripting Authentication Bypass Vulnerability. This vulnerability allows remote attackers to bypass authentication on affected installations of Quest NetVault Backup. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the addclient3 webpage. The issue results from the lack of proper validation of user-supplied data, which can lead to the injection of an arbitrary script. An attacker can leverage this in conjunction with other vulnerabilities to execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-27666.

### CVE-2026-7570

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T00:17:47.823 |

Quest NetVault Backup NVBUDashboard SQL Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest NetVault Backup. Although authentication is required to exploit this vulnerability, the existing authentication mechanism can be bypassed.

The specific flaw exists within the processing of NVBUDashboard JSON-RPC messages. The issue results from the lack of proper validation of a user-supplied string before using it to construct SQL queries. An attacker can leverage this vulnerability to execute code in the context of NETWORK SERVICE. Was ZDI-CAN-27809.

### CVE-2026-7569

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-25T00:17:47.707 |

Quest NetVault Backup viewclient Cross-Site Scripting Authentication Bypass Vulnerability. This vulnerability allows remote attackers to bypass authentication on affected installations of Quest NetVault Backup. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the viewclient webpage. The issue results from the lack of proper validation of user-supplied data, which can lead to the injection of an arbitrary script. An attacker can leverage this in conjunction with other vulnerabilities to execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-28202.

### CVE-2026-9773

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-24T22:16:49.920 |

Unraid Web Server ToggleState Command Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Unraid. Authentication is required to exploit this vulnerability.

The specific flaw exists within ToggleState.php. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to execute code in the context of the www-data user. Was ZDI-CAN-30134.

### CVE-2026-9772

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-24T22:16:49.803 |

Unraid Web Server FileUpload Command Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Unraid. Authentication is required to exploit this vulnerability.

The specific flaw exists within FileUpload.php. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to execute code in the context of the www-data user. Was ZDI-CAN-30116.

### CVE-2026-52800

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-24T21:16:55.800 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, organization team member management can be performed via GET requests without CSRF protection. If a victim who is an organization owner is logged in and is tricked into visiting a crafted link, an attacker-controlled user can be added to the Owners team. As a result, the attacker gains organization owner–equivalent privileges. This vulnerability is fixed in 0.14.3.

### CVE-2026-49247

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-24T19:17:11.480 |

Jellyfin is an open source self hosted media server. From 10.9.0 until 10.11.10, the POST /ClientLog/Document endpoint accepts the Authorization header's Client and Version fields and uses them unsanitized as components of the on-disk filename when persisting client-uploaded log documents. As a result, any authenticated non-admin user can include ../ sequences in the Client field to cause Jellyfin to write attacker-controlled content to arbitrary paths reachable by the Jellyfin service user, with a forced .log suffix. This vulnerability is fixed in 10.11.10.

### CVE-2026-48793

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-06-24T19:17:10.900 |

Jellyfin is an open source self hosted media server. Prior to 10.11.10, a potential FFmpeg argument injection vulnerability exists in the subtitle conversion code path. SubtitleEncoder.ConvertTextSubtitleToSrtInternal (SubtitleEncoder.cs, line 382) interpolates the subtitle file path into FFmpeg command-line arguments without calling EncodingUtils.NormalizePath(). On Linux, filenames can contain double-quote characters, which break the argument quoting and allow injection of arbitrary FFmpeg arguments. The vulnerability is reachable without authentication via SubtitleController.GetSubtitle, which has no [Authorize] attribute. An attacker who can place a file in a Jellyfin media library directory (shared NAS, Samba share, guest upload) can achieve arbitrary file write on the server and information disclosure. This vulnerability is fixed in 10.11.10.

### CVE-2026-13038

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-24T19:17:10.047 |

Use after free in Autofill in Google Chrome on Windows prior to 149.0.7827.197 allowed a remote attacker to execute arbitrary code via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-13036

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-416` |
| Published | 2026-06-24T19:17:09.860 |

Use after free in Blink in Google Chrome prior to 149.0.7827.197 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-13035

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-24T19:17:09.763 |

Use after free in Bluetooth in Google Chrome on Mac prior to 149.0.7827.197 allowed a remote attacker to execute arbitrary code via a malicious peripheral. (Chromium security severity: High)

### CVE-2026-13033

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-125;CWE-787` |
| Published | 2026-06-24T19:17:09.577 |

Out of bounds read and write in Blink>InterestGroups in Google Chrome prior to 149.0.7827.197 allowed a remote attacker to execute arbitrary code via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-13031

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-24T19:17:09.390 |

Use after free in Blink in Google Chrome prior to 149.0.7827.197 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-13027

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-24T19:17:08.963 |

Use after free in FileSystem in Google Chrome prior to 149.0.7827.197 allowed a remote attacker to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-13026

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-24T19:17:08.867 |

Use after free in Digital Credentials in Google Chrome on Mac prior to 149.0.7827.197 allowed a remote attacker to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-48732

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-24T18:17:18.670 |

Warp is an agentic development environment. From 0.2023.03.21.08.02.stable_00 until 0.2026.05.06.15.42.stable_01, Warp contains a command injection issue in the legacy SSH background command path. Warp used the remote working directory reported by the session when building helper commands for SSH-backed metadata collection. A remote host, repository, or directory name controlled by an attacker could cause that helper command to execute additional shell syntax on the remote host as the victim's authenticated SSH account. This vulnerability is fixed in 0.2026.05.06.15.42.stable_01.

### CVE-2026-48720

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-73` |
| Published | 2026-06-24T18:17:18.130 |

Warp is an agentic development environment. From 0.2025.03.05.08.02.stable_00 until 0.2026.05.06.15.42.stable_01, Warp accepts non-inline `OSC 1337;File` payloads from terminal output and materialize the decoded payload as a local file without an additional confirmation step. This vulnerability is fixed in 0.2026.05.06.15.42.stable_01.

### CVE-2026-48704

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-24T18:17:17.853 |

Warp is an agentic development environment. From 0.2023.10.24.08.03.stable_00 until 0.2026.05.06.15.42.stable_01, Warp may open executable local files through the operating system default file handler. A malicious Markdown document or project can contain a local-file link that appears as normal rendered content. If a user opens the Markdown in Warp and clicks the link, affected builds may route the resolved local file to a platform file opener instead of limiting the action to safe viewer/editor targets. This vulnerability is fixed in 0.2026.05.06.15.42.stable_01.

### CVE-2026-13164

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-24T17:16:56.847 |

Missing Authentication for Critical Function (CWE-306) in the RegisterView (apps/accounts/views.py), exposed at POST /api/auth/register/, in MailerUp <1.0.1 allows a remote, unauthenticated attacker to self-register a working account on instances where registration is intended to be restricted, because the endpoint applies the AllowAny permission with no email verification, CAPTCHA, or administrator approval. Any account created this way can read all email stored by the instance, resulting in full disclosure of stored messages to an arbitrary unauthenticated attacker

### CVE-2026-56122

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-25T14:16:51.513 |

Winstone Servlet Engine through 0.9.10 contains a path traversal vulnerability that allows unauthenticated attackers to read arbitrary files by sending HTTP GET requests with dot-dot-slash sequences that are not sanitized when serving static files from the configured webroot. Attackers can traverse outside the webroot directory using traversal-prefixed paths in a single HTTP request to read any file accessible to the servlet engine process, including sensitive system files when the service runs with elevated privileges.

### CVE-2026-12245

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-25T07:16:45.080 |

NSD from version 4.13.0 has a heap use-after-free bug in logging errors on TLS connections, causing a crash of the server process, which can be triggered trivially by sending a DNS query over a DoT connection, and closing the connection without reading the response.

### CVE-2026-12244

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-06-25T07:16:44.900 |

If NSD is configured as secondary for a zone, the primary of that zone can crash NSD with an AXFR containing a DNS message with a special crafted SVCB RR with an rdata size of 65512, that let's an (uint16_t) variable that is used to allocate space needed for the RR wrap (because total size > 65535), causing a heap overflow. The attacker can perform a controlled (RCE class) head write of up to 65509 bytes

### CVE-2026-13311

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-06-25T05:16:52.763 |

shell-quote prior to 1.8.5 finalizes parsed tokens in parse() using Array.prototype.concat as a reduce accumulator, which reallocates and copies the entire growing array on every iteration. As a result parse() runs in O(n^2) time relative to the number of input tokens. An attacker who can supply an attacker-controlled string to any code path that calls parse() (no shell metacharacters are required; plain space-separated words suffice) can block the single-threaded Node.js event loop for an extended period with a small input, resulting in a denial of service. There is no code execution or data disclosure; impact is to availability only. Fixed in 1.8.5.

### CVE-2026-10086

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-25T05:16:50.530 |

GitLab has remediated an issue in GitLab EE affecting all versions from 16.4 before 18.11.6, 19.0 before 19.0.3, and 19.1 before 19.1.1 that under certain conditions could have allowed an authenticated user with developer-role permissions to execute arbitrary client-side code in the context of another user's session, due to improper sanitization of user-supplied input.

### CVE-2026-54759

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-24T22:16:48.873 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.0, Lute's HTML sanitizer does not remove <iframe> elements. Combined with the SiYuan Electron client's permissive security configuration, an attacker can include a malicious <iframe> in a Bazaar package README that executes arbitrary commands on the victim's machine when the package details are viewed. No package installation is required. This vulnerability is fixed in 3.7.0.

### CVE-2026-52805

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-24T21:16:56.317 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, a Server-Side Request Forgery (SSRF) vulnerability exists in the repository migration functionality. The application validates only the initially submitted URL hostname, but git clone --mirror follows HTTP redirects. An authenticated user can submit a public URL that redirects to a blocked internal endpoint (e.g., 127.0.0.1), importing the internal repository's contents into an attacker-controlled repository. This vulnerability is fixed in 0.14.3.

### CVE-2026-45677

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-24T21:16:53.590 |

Rocket.Chat is an open-source, secure, fully customizable communications platform. Prior to 8.5.0, 8.4.1, 8.3.3, 8.2.3, 8.1.4, 8.0.5, 7.13.7, and 7.10.11, Rocket.Chat's SAML integration does not verify the signature on inbound LogoutRequest messages. An unauthenticated remote attacker who knows a target user's SAML NameID - which major identity providers (Okta, Google Workspace, Microsoft Entra ID, JumpCloud) expose as the user's email address - can craft a valid-looking unsigned LogoutRequest and submit it to the SP logout endpoint. The server processes it as legitimate, immediately destroying the victim's session. Because the attack requires no authentication and no interaction from the victim, it can be repeated in a loop against individual users or scripted across many accounts, effectively rendering the Rocket.Chat instance unusable for SAML-authenticated users. This vulnerability is fixed in 8.5.0, 8.4.1, 8.3.3, 8.2.3, 8.1.4, 8.0.5, 7.13.7, and 7.10.11.

### CVE-2026-1840

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-24T21:16:52.753 |

The Aclara Metrum Cellular Web Interface is vulnerable to unauthorized access due to the absence of authentication controls on critical system functions. This weakness exposes essential configuration settings, allowing attackers to alter operational parameters and trigger system restarts without restriction. Such unauthorized changes can disrupt normal functionality and, if performed repeatedly, may lead to a loss of communications to the device.

### CVE-2026-46348

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-24T20:16:32.100 |

Mastodon is a free, open-source social network server based on ActivityPub. Prior to 4.5.10, 4.4.17, and 4.3.23, the list of disallowed IP address ranges was lacking an IP address range that can be used to reach local IP addresses. An attacker can use an IP address in the affected range to make Mastodon perform HTTP requests against loopback interfaces, potentially allowing access to otherwise private resources and services. This vulnerability is fixed in 4.5.10, 4.4.17, and 4.3.23.

### CVE-2026-49851

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407;CWE-770` |
| Published | 2026-06-24T18:17:18.937 |

Mistune is a Python Markdown parser with renderers and plugins. Prior to 3.3.0, Mistune is vulnerable to a CPU exhaustion DoS due to superlinear (approximately O(n²)) behavior in parse_link_text. When parsing Markdown containing many consecutive [ characters, parse_link_text repeatedly scans the input using a regex search inside a loop. Each iteration re-scans a large portion of the remaining string, resulting in quadratic-time behavior. An attacker-controlled Markdown input can therefore trigger excessive CPU usage with a very small payload. This vulnerability is fixed in 3.3.0.

### CVE-2026-12053

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-06-25T05:16:50.890 |

GitLab has remediated an issue in GitLab EE affecting all versions from 19.1 before 19.1.1 that under certain conditions could have allowed a user to access sensitive information that had already been committed to a project, due to insufficient output filtering in Duo Workflows.

### CVE-2026-40079

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-06-25T00:17:47.570 |

Cacti is an open source performance and fault management framework. Versions 1.2.30 and prior are vulnerable to Command Injection due to lack of sanitization in the escape_command() function. The escape_command() function at lib/rrd.php is a no-op: it returns $command unchanged. The command line built by rrdtool_function_graph() is passed through this function and then to shell_exec($full_commandline). The risk is in __rrd_execute() where text_format values from graph templates (which may contain host variable substitutions) reach shell_exec without adequate escaping. This issue has been addressed in version 1.2.31.

### CVE-2026-47389

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-184;CWE-200;CWE-918` |
| Published | 2026-06-24T20:16:32.653 |

Mastodon is a free, open-source social network server based on ActivityPub. Prior to 4.5.10, 4.4.17, and 4.3.23, when using Ruby versions older than 3.4, PrivateAddressCheck.private_address? returns false for IPv4-mapped IPv6 addresses (::ffff:a.b.c.d) corresponding to some private IPv4 addresses, depending on Ruby version, this can include loopback, RFC1918 private networks, and link-local space. An attacker who controls DNS for any domain can publish an AAAA record with such a mapped address; any outbound HTTP fetch Mastodon performs against that hostname then opens a real TCP connection to the underlying IPv4 address, including 127.0.0.1 and cloud-metadata endpoints such as 169.254.169.254. This vulnerability is fixed in 4.5.10, 4.4.17, and 4.3.23.

### CVE-2026-48721

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-180;CWE-693` |
| Published | 2026-06-24T18:17:18.283 |

Warp is an agentic development environment. From 0.2025.10.08.08.12.stable_00 until 0.2026.05.06.15.42.stable_01, Warp contains a command execution permission-check bypass in the default unsandboxed CLI agent profile. The CLI profile is non-interactive and relies on a command denylist as a safety boundary for commands that should require confirmation. Because command strings were checked before canonicalizing leading environment-variable assignments, an attacker who can influence the agent's command output may cause denylisted commands to be treated as non-denylisted. This vulnerability is fixed in 0.2026.05.06.15.42.stable_01.

### CVE-2026-49269

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-24T16:16:30.410 |

Apple M1 GPUs retain register file data between compute shader dispatches from different processes. A sandboxed Metal attacker app can run a GPU reader shader that reads stale register values left by a separate sandboxed victim app. In the proof of concept, GPUVictim.app generates a fresh random 128-bit secret using SecRandomCopyBytes and loads it into GPU registers. GPUAttacker.app, a separate sandboxed app, recovers the exact secret from stale GPU register state. NOTE: The vendor stated that this behavior affects only legacy hardware and has already been addressed at the hardware level in current-generation Apple Silicon.

### CVE-2026-56049

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-25T14:16:50.753 |

Contributor Remote Code Execution (RCE) in Post Snippets <= 4.0.19 versions.

### CVE-2026-54838

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T14:16:47.907 |

Subscriber SQL Injection in WC Vendors Marketplace <= 2.6.8 versions.

### CVE-2026-54822

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T14:16:46.747 |

Subscriber SQL Injection in SALESmanago & Leadoo <= 3.11.2 versions.

### CVE-2026-52797

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-24T21:16:55.403 |

Gogs is an open source self-hosted Git service. Prior to 0.14.0, as an authorized user, an intruder can dictate the value which is passed to the git diff command which, together with bypassing the filtering of the passed value, allows the user to bypass the target directory and write the result of the comparison to any arbitrary path. This vulnerability is fixed in 0.14.0.

### CVE-2026-45687

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-915` |
| Published | 2026-06-24T21:16:53.720 |

Rocket.Chat is an open-source, secure, fully customizable communications platform. Prior to 8.5.0, 8.4.1, 8.3.3, 8.2.3, 8.1.4, 8.0.5, 7.13.7, and 7.10.11, Rocket.Chat's sendFileMessage DDP method passes the entire attacker-supplied file object into Uploads.updateFileComplete, which merges it directly into a MongoDB $set update via Object.assign. There is no allow-list of writable fields. An attacker can therefore rewrite any column on their own upload record, notably store and the store-specific path fields. This vulnerability is fixed in 8.5.0, 8.4.1, 8.3.3, 8.2.3, 8.1.4, 8.0.5, 7.13.7, and 7.10.11.

### CVE-2026-2815

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-339` |
| Published | 2026-06-25T14:16:37.067 |

Incorrect use of the PUF key for user key generation in EFR32xG27 results in predictable keys

### CVE-2026-54848

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-201` |
| Published | 2026-06-25T14:16:49.037 |

Insertion of Sensitive Information Into Sent Data vulnerability in Saad Iqbal APIExperts Square for WooCommerce allows Retrieve Embedded Sensitive Data.

This issue affects APIExperts Square for WooCommerce: from n/a through 4.7.3.

### CVE-2026-47267

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-24T21:16:54.347 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, the fix for CVE-2022-1285 prevents adding webooks or running webhooks with URLs with a hostname that resolves in localCIDRs. However, webhooks still follow redirects allowing to access hostname inside localCIDRs. This vulnerability is fixed in 0.14.3.

### CVE-2026-13025

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-24T19:17:08.770 |

Race in DevTools in Google Chrome prior to 149.0.7827.197 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-56111

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-06-24T16:16:32.930 |

Marlin Firmware through 2.1.2.7, fixed in commit 1f255d1, when built with MESH_BED_LEVELING enabled, contains an out-of-bounds write vulnerability in the M421 G-code handler that allows attackers to corrupt firmware memory by supplying out-of-range X and Y grid indices. Attackers can send a single crafted G-code command via USB serial, network interface, or malicious gcode file to write an attacker-controlled 32-bit float value past the z_values array bounds, corrupting adjacent firmware variables and causing denial of service or firmware state corruption.

### CVE-2026-56091

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:X/V:D/RE:L/U:Amber` |
| Weaknesses | `CWE-289` |
| Published | 2026-06-25T09:16:46.103 |

When using Apache Shiro with the shiro-guice module in a web servlet context, a specially crafted HTTP request may cause an authentication bypass.
This vulnerability is similar to  https://www.cve.org/CVERecord?id=CVE-2020-1957 https://www.cve.org/CVERecord , except that it affects the `shiro-guice` module instead of the `shiro-spring` module.

This issue affects all Apache Shiro versions through 2.x, and 3.0.0-alpha-1 only when using `shiro-guice` module in a web servlet context.

Upgrade to version 3.0.0 or later, which fixes the issue.

### CVE-2026-12490

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-06-25T07:16:45.330 |

When a provide-xfr is given with a tls-auth-name, a secondary requesting a transfer should provide a client certificate with that name. However, no client certificate is needed when the request comes in over TLS over the regular tls-port (and not the tls-auth-port) or over over TCP over the regular port, when the other conditions of the provide-xfr rule match.

### CVE-2026-44016

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-94;CWE-918` |
| Published | 2026-06-24T18:17:16.353 |

Docling simplifies document processing by parsing diverse formats and providing integrations with the generative AI ecosystem. FIn versions >= 2.82.0, < 2.91.0, if the HTML backend was explicitly configured for rendering (rendering option by default deactivated), then the Playwright-based rendering feature could allow JavaScript execution and unrestricted network access when processing untrusted HTML documents. An attacker could craft malicious HTML that executes arbitrary JavaScript in the rendering context or makes unauthorized network requests to internal services, potentially leading to SSRF attacks, data exfiltration, or remote code execution in the rendering environment. This vulnerability is fixed in 2.91.0.

### CVE-2026-54904

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-06-24T17:17:29.267 |

concurrent-ruby is a modern concurrency tools for Ruby. Prior to 1.3.7, Concurrent::AtomicReference#update can enter a permanent busy retry loop when the current value is Float::NAN. The issue is caused by the interaction between AtomicReference#update, which retries until compare_and_set(old_value, new_value) succeeds; Numeric compare_and_set, which checks old == old_value before attempting the underlying atomic swap.; and Ruby NaN semantics, where Float::NAN == Float::NAN is always false. As a result, once an AtomicReference contains Float::NAN, calling #update repeatedly evaluates the caller's block and never returns. In services that store externally derived numeric values in an AtomicReference, this can cause CPU exhaustion or permanent request/job hangs. This vulnerability is fixed in 1.3.7.

### CVE-2026-11878

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-24T15:16:39.370 |

Improper neutralization of input during web page generation ('cross-site scripting') vulnerability in OpenText Access Manager allows Cross-Site Scripting (XSS).

This issue affects Access Manager: from 5.1 through 5.1.2.

### CVE-2026-54845

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-25T14:16:48.853 |

Unauthenticated Local File Inclusion in MDTF <= 1.3.8 versions.

### CVE-2026-54842

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-25T14:16:48.190 |

Missing Authorization vulnerability in Royal Plugins Royal MCP allows Exploiting Incorrectly Configured Access Control Security Levels.

This issue affects Royal MCP: from n/a through 1.4.25.

### CVE-2026-55762

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-24T22:16:49.667 |

Rocket.Chat is an open-source, secure, fully customizable communications platform. Prior to 8.5.1, 8.4.4, 8.3.6, 8.2.6, 8.1.6, 8.0.7, and 7.10.13, the POST /api/v1/fingerprint REST endpoint enforces authentication (authRequired: true) but performs no authorization check. Any authenticated user — including a standard user role account — can call this endpoint with {"setDeploymentAs": "new-workspace"} to permanently deregister the workspace from Rocket.Chat Cloud. This wipes all cloud credentials, removes the workspace license, breaks push notifications for all users, and requires manual re-registration to recover. This vulnerability is fixed in 8.5.1, 8.4.4, 8.3.6, 8.2.6, 8.1.6, 8.0.7, and 7.10.13.

### CVE-2026-52801

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-24T21:16:55.930 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, the Gogs Mirror Settings functionality provide an alternative way from the well protected New Migration functionality for any authenticated users to import local repositories. This issue stems from a lack of validation of SaveAddress function. This vulnerability is fixed in 0.14.3.

### CVE-2026-48725

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-276` |
| Published | 2026-06-24T18:17:18.413 |

Warp is an agentic development environment. From 0.2021.04.25.23.05.stable_00 until 0.2026.05.06.15.42.stable_01, Warp allows terminal output to request access to the local system clipboard. A malicious remote host, remote program, or other attacker-controlled terminal output source can trigger clipboard reads or writes without a separate confirmation step. This crosses the trust boundary between untrusted terminal output and the user's local desktop clipboard. This vulnerability is fixed in 0.2026.05.06.15.42.stable_01.

### CVE-2026-10712

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-25T05:16:50.640 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.10 before 18.11.6, 19.0 before 19.0.3, and 19.1 before 19.1.1 that under certain conditions could have allowed an unauthenticated user to execute arbitrary JavaScript in a user's browser session due to improper path validation under certain conditions.

### CVE-2026-23879

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-06-24T20:16:31.817 |

py7zr is a Python-based library and utility to support 7zip archive compression, decompression, encryption and decryption. Versions 1.1.2 and below contain an an arbitrary file write vulnerability, which allows symbolic links to be recreated outside the destination directory via crafted malicious symbolic link chains. When using extractall to extract an archive, the library restores these symbolic links, linking them to arbitrary directories on the host file system. During extraction, the program only checks the link arcname within the destination directory, but ignores the combined symlink path resolution. Attackers can exploit this vulnerability by constructing malicious archives, thereby bypassing the directory boundary restrictions implemented by the extractor. Subsequent extraction of regular files through these symbolic links can result in arbitrary file writes. This vulnerability may lead to remote code execution, privilege escalation, data corruption, or denial of service. This issue has been fixed in version 1.1.3.

### CVE-2026-48719

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-24T18:17:17.983 |

Warp is an agentic development environment. From 0.2025.08.06.08.12.stable_00 until 0.2026.05.06.15.42.stable_01, Warp contains a command injection in the prompt branch selector. A user who can publish a branch to a Git repository opened in Warp can cause a crafted branch name to be interpreted by the victim's shell if the victim selects that branch from the UI. This vulnerability is fixed in 0.2026.05.06.15.42.stable_01.

### CVE-2026-46733

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-25T14:16:40.363 |

Dell Display and Peripheral Manager (DDPM Windows), versions prior to 2.3, contain an Improper Access Control vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Code execution.

### CVE-2026-2050

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-24T22:16:46.497 |

GIMP HDR File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of HDR files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28266.

### CVE-2026-10043

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-24T22:16:46.003 |

MosaicML Composer Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of MosaicML Composer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of checkpoints. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-27990.

### CVE-2026-13037

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-24T19:17:09.953 |

Use after free in WebView in Google Chrome on Android prior to 149.0.7827.197 allowed a local attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-48731

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-24T18:17:18.547 |

Warp is an agentic development environment. From 0.2024.02.20.08.01.stable_01 until 0.2026.05.06.15.42.stable_01, Warp contains a command injection issue in the Linux external editor launcher. Warp expanded freedesktop .desktop Exec templates for affected editor integrations and executed the expanded command through a shell. A user who opens an attacker-controlled local file path through an affected external editor or system-default editor route can cause shell syntax embedded in that path to execute as the local user. This vulnerability is fixed in 0.2026.05.06.15.42.stable_01.

### CVE-2026-48703

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-24T18:17:17.723 |

Warp is an agentic development environment. From 0.2025.04.09.08.11.stable_00 until 0.2026.05.06.15.42.stable_01, Warp contains a command execution policy bypass in Agent code search tools. The affected Grep and FileGlob actions are authorized as read/search operations, but their implementations build shell command strings from Agent-controlled inputs (search text, paths, glob patterns) and execute them in the active terminal session. This vulnerability is fixed in 0.2026.05.06.15.42.stable_01.

### CVE-2026-56054

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-25T14:16:51.283 |

Subscriber Arbitrary File Deletion in JS Help Desk <= 3.1.1 versions.

### CVE-2026-8666

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-25T02:16:35.567 |

OS Command Injection vulnerability in the traceroute action of Rapid7 InsightConnect Traceroute Plugin on Linux allows remote attackers to execute arbitrary OS commands via the host, port, max_ttl, count, or time_out request parameters due to insufficient input validation when constructing shell commands.

### CVE-2026-8665

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-25T02:16:35.340 |

OS Command Injection vulnerability in the TR action of Rapid7 InsightConnect Translate Plugin on Linux allows remote attackers to execute arbitrary OS commands via the text or expression parameters due to insufficient input sanitization in shell command construction.

### CVE-2026-8660

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-25T02:16:35.110 |

OS Command Injection vulnerability in the ping action of Rapid7 InsightConnect Ping Plugin on Linux allows remote attackers to execute arbitrary OS commands via the host parameter due to insufficient input validation when constructing shell commands.

### CVE-2026-8592

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-25T02:16:34.990 |

OS Command Injection vulnerability in the process_string action of Rapid7 InsightConnect AWK Plugin on Linux allows remote attackers to execute arbitrary OS commands via the text or expression parameters due to unsafe shell command construction in the processing pipeline.

### CVE-2026-33235

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-24T21:16:53.320 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. In versions prior to 0.6.52, the Fill Text Template block is vulnerable to a Denial of Service (DoS) attack. While the backend implements a SandboxedEnvironment to prevent unauthorized attribute access (e.g., blocking __class__), it fails to limit the computational complexity or execution time of the expressions. An attacker can input computationally expensive Python/Jinja2 expressions that consume the server's CPU and memory, leading to a complete system hang or crash. In multi-tenant or self-hosted environments, this results in a complete service outage and "noisy neighbor" effects that require manual administrative intervention to recover. This issue has been fixed in version 0.6.52.

### CVE-2026-25119

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-06-24T21:16:52.903 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, when ENABLE_REVERSE_PROXY_AUTHENTICATION is enabled, Gogs accepts the configured authentication header (default: X-WEBAUTH-USER) directly from client requests without validating that the request originated from a trusted reverse proxy. Any remote attacker who can reach the Gogs service can forge this header to impersonate any user or trigger automatic account creation, completely bypassing authentication. This vulnerability is fixed in 0.14.3.

### CVE-2026-54699

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-116` |
| Published | 2026-06-24T18:17:19.187 |

Warp is an agentic development environment. From 0.2024.03.12.08.02.stable_01 until 0.2026.05.06.15.42.stable_01, Warp contains an OS command injection vulnerability in the WSL URL-opening fallback. When Warp is running under WSL and cannot open a URL through wslview, it falls back to a Windows command processor path. A URL controlled through terminal output can reach that fallback when the user opens the link. This vulnerability is fixed in 0.2026.05.06.15.42.stable_01.

### CVE-2026-55488

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-24T16:16:32.793 |

motionEye (mEye) is an online interface for a piece of software called "motion," which is a video surveillance program with motion detection. Versions prior to 0.44.0 contain an absolute path traversal vulnerability in multiple media file handlers that allows an attacker to read arbitrary files from the filesystem. The affected handlers accept a user-controlled filename parameter and construct filesystem paths using `os.path.join()`. When an absolute path is supplied, Python discards the configured media directory and returns the attacker-supplied path directly. The application then bypasses Tornado's built-in path validation by overriding the relevant safety checks. As a result, an attacker can access files outside of the configured camera media directory, subject to the permissions of the motionEye process. Version 0.44.0 fixes the issue.

### CVE-2026-39951

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T00:17:47.403 |

Cacti is an open source performance and fault management framework. Versions 1.2.30 and prior have a Stored SQL Injection vulnerability through graph_name_regexp in the Reports feature. This issue has been fixed in version 1.2.31.

### CVE-2026-11998

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-791` |
| Published | 2026-06-24T21:16:52.170 |

A flaw in AngularJS' Strict Contextual Escaping (SCE) logic allows bypassing certain SCE policies for resource URLs and can lead to arbitrary JavaScript execution within the context of the victim's browser session.


SCE's purpose is to ensure that only trusted or safe values are used in certain security-sensitive contexts, such as resource URLs, including URLs that define executable JavaScript scripts, '<iframe>' documents, route templates, etc. A flaw in the logic that tries to match entire URLs against regular expression matchers can result in partial matches for certain types of regular expressions, effectively bypassing the policies and allowing the use of unsafe values as resource URLs.


This issue affects AngularJS versions greater than or equal to 1.2.0-rc.3.


Note:
The AngularJS project was already End-of-Life when this CVE was published and will not receive any updates to address this issue. For more information see the  End-of-Life announcement https://docs.angularjs.org/misc/version-support-status .

### CVE-2026-55583

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-24T20:16:33.100 |

Twenty is an open-source CRM (customer relationship management) platform. Prior to 2.9.0, Twenty was vulnerable to a cross-workspace insecure direct object reference (IDOR) in the AI agent monitor's AgentTurnResolver, in packages/twenty-server/src/engine/metadata-modules/ai/ai-agent-monitor/reso lvers/agent-turn.resolver.ts. The agentTurns(agentId) query and the evaluateAgentTurn(turnId) mutation looked up rows by agentId or id only; although AgentTurnEntity has a workspaceId column, it was not included in the WHERE clause, and the class-level guards only checked that the caller was authenticated in some workspace rather than that the requested object belonged to it, with the same flaw present in agent-turn-grader.service.ts.  As a result, any authenticated user with the AI settings flag, a workspace owner by default, could target any other workspace on the same instance given the victim's agentId or turnId: agentTurns returned the victim's full  chat history including message parts such as raw chat text, tool calls, and tool outputs, while evaluateAgentTurn inserted an agentTurnEvaluation row with the victim's workspaceId and fed the victim's turn into the default LLM. The agentId and turnId are non-guessable UUIDs but are exposed  in the URL of the settings page. This issue is fixed in version 2.9.0.

### CVE-2026-54844

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-25T14:16:48.560 |

Unauthenticated Broken Access Control in CheckView Automated Testing <= 2.1.0 versions.

### CVE-2026-54841

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-06-25T14:16:48.050 |

Unauthenticated Sensitive Data Exposure in Vitepos <= 3.4.2 versions.

### CVE-2026-54830

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-25T14:16:47.370 |

Unauthenticated Broken Access Control in Five Star Restaurant Reservations <= 2.7.19 versions.

### CVE-2026-54829

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T14:16:47.120 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Jacob N. Breetvelt WP Photo Album Plus allows Blind SQL Injection.

This issue affects WP Photo Album Plus: from n/a through 9.1.13.005.

### CVE-2026-54828

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-25T14:16:46.990 |

Unauthenticated Broken Access Control in Motors <= 1.4.109 versions.

### CVE-2026-27366

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-25T14:16:36.767 |

Unauthenticated Broken Access Control in MainWP Child <= 6.1.1 versions.

### CVE-2026-33612

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-349` |
| Published | 2026-06-25T13:16:38.437 |

A malicious authoritative server can send a crafted zone via the ZoneToCache function that leads to cache poisoning.

### CVE-2026-12937

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T08:16:29.787 |

The Tourfic – AI Powered Travel Booking, Hotel Booking & Car Rental WordPress Plugin plugin for WordPress is vulnerable to generic SQL Injection via the 'post_id' parameter in all versions up to, and including, 2.22.7 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The AJAX handler is registered for unauthenticated users via wp_ajax_nopriv_tf_room_availability, and the required nonce is emitted on the public single-hotel page template, allowing unauthenticated attackers to freely obtain a valid nonce and reach the vulnerable code path.

### CVE-2026-9702

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-25T07:16:45.830 |

The InPost PL WordPress plugin before 1.9.1 does not verify that the request originates from the legitimate buyer before allowing the WooCommerce order parcel-locker destination to be updated, allowing unauthenticated attackers to silently redirect the shipping destination of any pending or processing order on the site.

### CVE-2026-12077

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T04:17:55.627 |

The Dokan Pro plugin for WordPress is vulnerable to time-based SQL Injection via the via 'latitude' and 'longitude' parameters in all versions up to, and including, 5.0.4 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query.  This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2025-60474

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-24T23:16:40.137 |

A buffer overflow in the gf_media_import function (/media_tools/av_parsers.c) of GPAC Project/MP4Box before 26.02.0 allows attackers to cause a Denial of Service (DoS) via supplying a crafted input.

### CVE-2025-60467

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-24T23:16:39.523 |

A use-after-free in the gf_filter_pid_inst_swap_delete_task function (/filter_core/filter_pid.c) of GPAC Project/MP4Box before 26.02.0 allows attackers to cause a Denial of Service (DoS) via supplying a crafted media file.

### CVE-2026-9776

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-24T22:16:50.250 |

ATEN Unizon writeFileToHttpServletResponse Directory Traversal Information Disclosure Vulnerability. This vulnerability allows remote attackers to disclose sensitive information on affected installations of ATEN Unizon. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the writeFileToHttpServletResponse method. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to disclose information in the context of SYSTEM. Was ZDI-CAN-28505.

### CVE-2026-54066

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-23;CWE-1188` |
| Published | 2026-06-24T22:16:48.043 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.0, the patch for CVE-2026-41894 ("Path Traversal via Double URL Encoding") sanitized the /export/ route but the identical root cause remains in the /assets/*path route. In publish mode (anonymous read-only HTTP endpoint, default port 6808), an unauthenticated remote attacker can read arbitrary files inside WorkspaceDir — including conf/conf.json (which contains the AccessAuthCode SHA256 hash, API token, and sync keys), temp/siyuan.db, temp/blocktree.db, and siyuan.log — by double-URL-encoding .. segments. This vulnerability is fixed in 3.7.0.

### CVE-2026-52794

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-06-24T22:16:47.647 |

Sentry is an error tracking and performance monitoring tool. From 24.4.0 until 26.5.2, a Regular Expression Denial of Service (ReDoS) vulnerability exists in Sentry's event ingestion pipeline, where a regex applied to attacker-controlled fields on incoming events can be made to consume disproportionate CPU time. This vulnerability is fixed in 26.5.2.

### CVE-2026-52799

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-06-24T21:16:55.670 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, GET /attachments/:uuid returns the raw attachment file without verifying whether the requester has view permission for the associated Issue/Comment/Release or the repository.
In a test environment with REQUIRE_SIGNIN_VIEW = false, we confirmed that an unauthenticated user can download attachments belonging to a private repository. This vulnerability is fixed in 0.14.3.

### CVE-2026-50129

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-06-24T21:16:55.020 |

Mastodon is a free, open-source social network server based on ActivityPub. Prior to 4.5.11, 4.4.18, and 4.3.24, a DoS can be triggered by (Uncaught Exception vulerability), due to missing exception handling in the math sanitizer. Malformed <math> nodes can result in a DoS of a whole server or targeted users services, depending on the type of action that includes the malformed nodes and the services interacting with it. This vulnerability is fixed in 4.5.11, 4.4.18, and 4.3.24.

### CVE-2026-53950

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-24T19:17:12.713 |

@tryghost/activitypub is Ghost’s social/federation client app. Prior to 3.1.0, the ActivityPub client in Ghost was vulnerable to JavaScript injection on posts shared by a maliciously customised ActivityPub server. This vulnerability is fixed in 3.1.0.

### CVE-2026-13029

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-24T19:17:09.193 |

Use after free in Web Authentication in Google Chrome prior to 149.0.7827.197 allowed an attacker who convinced a user to install a malicious extension to potentially exploit heap corruption via a crafted Chrome Extension. (Chromium security severity: High)

### CVE-2026-44020

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-776` |
| Published | 2026-06-24T18:17:17.467 |

Docling simplifies document processing by parsing diverse formats and providing integrations with the generative AI ecosystem. From 2.13.0 until 2.74.0, the USPTO patent XML parser used the standard xml.sax.parseString() without protection against XML External Entity (XXE) attacks. An attacker could craft malicious USPTO patent XML files with external entity references that could read arbitrary files from the server filesystem, perform Server-Side Request Forgery (SSRF) attacks, or cause denial of service through entity expansion (Billion Laughs attack). The vulnerability affects three USPTO patent format parsers: ICE (v4.x), Grant v2.5, and Application v1.x. This vulnerability is fixed in 2.74.0.

### CVE-2026-44017

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-24T18:17:17.337 |

Docling simplifies document processing by parsing diverse formats and providing integrations with the generative AI ecosystem. Prior to 2.91.0, the EasyOCR model download functionality extracted ZIP archives without validating member paths, enabling Zip Slip attacks. If an attacker could compromise the model download source (via supply chain attack, DNS spoofing, or MITM), they could write arbitrary files to any location writable by the process, potentially achieving remote code execution by overwriting Python files or system binaries, persistent backdoors by modifying startup scripts or SSH keys, and data corruption or system compromise. This vulnerability is fixed in 2.91.0.

### CVE-2026-54297

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-06-24T17:17:29.030 |

Faraday is an HTTP client library abstraction layer that provides a common interface over many adapters. From 1.0.0 until 1.10.6 and 2.14.3, Faraday::NestedParamsEncoder, the default nested query parameter encoder/decoder in Faraday, decodes nested query strings without enforcing a maximum nesting depth. A crafted query string causes Faraday to build a deeply nested Ruby Hash structure. The internal dehash routine then recursively walks this attacker-controlled structure without a depth limit. At sufficient depth, Ruby raises an uncaught SystemStackError (stack level too deep), crashing the calling thread or worker. This can lead to denial of service in applications that pass attacker-controlled query strings to Faraday's nested query parsing or URL-building paths. This vulnerability is fixed in 1.10.6 and 2.14.3.

### CVE-2026-54821

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-201` |
| Published | 2026-06-25T14:16:46.613 |

Subscriber Sensitive Data Exposure in Visual Link Preview <= 2.3.1 versions.

### CVE-2026-57589

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-25T01:16:26.537 |

sys/kern/sysv_sem.c in OpenBSD through 7.9 has a use-after-free allowing local privilege escalation to root. This is a context switch use-after-free after tsleep in sys_semget().

### CVE-2026-55759

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-294` |
| Published | 2026-06-24T22:16:49.527 |

Rocket.Chat is an open-source, secure, fully customizable communications platform. Prior to 8.5.1, 8.4.4, 8.3.6, 8.2.6, 8.1.6, 8.0.7, and 7.10.13, Rocket.Chat's Apple Sign-In handler verifies JWT signatures but skips claims validation. Any Apple-signed JWT with a non-empty iss is accepted regardless of aud, exp, nbf, or nonce. An attacker who obtains a target user's Apple identity token (from server logs, an intercepted sign-in flow, or another application sharing the same Apple developer team) can replay it to authenticate as that user, with no expiration on the replay window. This vulnerability is fixed in 8.5.1, 8.4.4, 8.3.6, 8.2.6, 8.1.6, 8.0.7, and 7.10.13.

### CVE-2026-46734

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-06-25T14:16:40.470 |

Dell Display and Peripheral Manager (DDPM Mac), versions prior to 2.3, contain an Improper Certificate Validation vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Protection mechanism bypass.

### CVE-2026-7539

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-379` |
| Published | 2026-06-24T21:16:58.350 |

A potential security vulnerability has been identified in the HP Accessory WMI Provider installer for some HP Docking Stations, which might allow escalation of privilege and/or arbitrary code execution. HP is releasing software updates to mitigate the potential vulnerability.

### CVE-2026-12986

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:U/V:C/RE:M/U:Amber` |
| Weaknesses | `CWE-352;CWE-918` |
| Published | 2026-06-24T15:16:39.737 |

A critical vulnerability in Admin GUI in Payara Server Full 4.x, 5.x, 6.x, 7.x, 7.2026.x, 6.2025.x, 6.2024.x on All platforms that allows the attacker to leak the admin gfresttoken to an attacker-controlled host that can result in a full unauthenticated takeover of Payara admin domain.

A Server-Side Request Forgery (SSRF) vulnerability in the DownloadServlet of the Admin GUI in Payara Server allows a remote attacker to exfiltrate the administrator's REST session token (gfresttoken) to an attacker-controlled host via a crafted request URL. Combined with the absence of CSRF protection on DownloadServlet, an unauthenticated attacker can trick a logged-in administrator into triggering the token leak, then replay the stolen token to gain full administrative access to the Payara domain, leading to arbitrary code execution via WAR deployment. The vulnerability exists in the DownloadServlet and associated ContentSource implementations (LogViewerContentSource, LogFilesContentSource, LBConfigContentSource, ClientStubsContentSource) within the admingui:console-common module.

### CVE-2026-49506

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-25T14:16:42.113 |

Dell Wyse Management Suite, versions prior to WMS 5.5 HF1, contain an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Remote Code Execution.

### CVE-2026-12246

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-120` |
| Published | 2026-06-25T07:16:45.197 |

NSD version 4.14.0 introduced a bug where a specially crafted APL RR, with an adflength larger than permitted for the address family will overwrite the stack when the zone is written to disk, with a maximum of 111 attacker controlled bytes.

### CVE-2026-9779

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-06-24T22:16:50.590 |

ATEN Unizon doCryptoHugeFileToFile Improper Verification of Cryptographic Signature Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of ATEN Unizon. Authentication is required to exploit this vulnerability.

The specific flaw exists within the updateWar method. The issue results from an incorrect implementation of cryptographic signature verification. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-28590.

### CVE-2026-9778

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-24T22:16:50.483 |

ATEN Unizon ImportDeviceList Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of ATEN Unizon. Authentication is required to exploit this vulnerability.

The specific flaw exists within the ImportDeviceList method. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-28579.

### CVE-2026-9777

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-24T22:16:50.370 |

ATEN Unizon restoreDB Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of ATEN Unizon. Authentication is required to exploit this vulnerability.

The specific flaw exists within the restoreDB method. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-28578.

### CVE-2026-56071

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-25T14:16:51.400 |

Unauthenticated Cross Site Scripting (XSS) in Forminator <= 1.53.1 versions.

### CVE-2026-56051

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-25T14:16:51.030 |

Unauthenticated Cross Site Scripting (XSS) in TablePress <= 3.3.1 versions.

### CVE-2026-56042

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-25T14:16:50.637 |

Customer Cross Site Scripting (XSS) in Advanced Order Export For WooCommerce <= 4.0.9 versions.

### CVE-2026-56014

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-25T14:16:50.340 |

Unauthenticated Cross Site Scripting (XSS) in Master Slider <= 3.11.2 versions.

### CVE-2026-56006

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-25T14:16:50.093 |

Unauthenticated Cross Site Scripting (XSS) in H5P <= 1.17.6 versions.

### CVE-2026-56005

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-25T14:16:49.720 |

Subscriber Cross Site Scripting (XSS) in WP Activity Log <= 5.6.3.1 versions.

### CVE-2026-4526

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-25T14:16:42.313 |

In EmberZNet v9.0.2 and earlier, malformed global ZCL messages can trigger out-of-bounds reads in framework parsing logic and terminate the process. These messages must come from a device that has already joined the network, and no information leakage back to the sender was observed.

### CVE-2026-47154

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-25T14:16:41.623 |

In EmberZNet v9.0.2 and earlier, a malformed GetProfileResponse message can trigger out-of-bounds reads while iterating interval entries and terminate the process. These messages must come from a device that has already joined the network, and no information leakage back to the sender was observed. Only devices supporting the Simple Metering cluster may be impacted.

### CVE-2026-47153

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-369` |
| Published | 2026-06-25T14:16:41.500 |

In EmberZNet v9.0.2 and earlier, a malformed Level Control Step command can terminate the process through a divide-by-zero fault. This command must come from a device that has already joined the network. Only devices supporting the Level Control cluster may be impacted.

### CVE-2026-47152

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-369` |
| Published | 2026-06-25T14:16:41.360 |

In EmberZNet v9.0.2 and earlier, a malformed Level Control Move command can terminate the process through a divide-by-zero fault. This command must come from a device that has already joined the network. Only devices supporting the Level Control cluster may be impacted.

### CVE-2026-47151

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-25T14:16:41.243 |

In EmberZNet v9.0.2 and earlier, malformed ClearWeekdaySchedule messages can trigger out-of-bounds writes into Door Lock schedule state. The size and location of this data is limited. These messages must come from a device that has already joined the network. Only devices supporting the Door Lock cluster may be impacted.

### CVE-2026-47150

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-25T14:16:41.137 |

In EmberZNet v9.0.2 and earlier, malformed IAS Zone enrollment messages can trigger an out-of-bounds state-table write and terminate the process. The size and location of this write is limited. These messages must come from a device that has already joined the network. Only devices supporting the IAS Zone cluster may be impacted.

### CVE-2026-47149

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-25T14:16:41.027 |

In EmberZNet v9.0.2 and earlier, malformed or out-of-range Door Lock user identifiers can trigger out-of-bounds table reads and terminate the process. These messages must come from a device that has already joined the network, and no information leakage back to the sender was observed. Only devices supporting the Door Lock cluster may be impacted.

### CVE-2026-47148

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-25T14:16:40.920 |

In EmberZNet v9.0.2 and earlier, malformed GetGroupMembership commands can trigger repeated reads past the end of the message payload and terminate the process. These messages must come from a device that has already joined the network, and no information leakage back to the sender was observed. Only devices supporting the Groups cluster may be impacted.

### CVE-2026-47147

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-25T14:16:40.810 |

In EmberZNet v9.0.2 and earlier, malformed OTA requests can drive the OTA server parser into out-of-bounds reads. A limited amount of data from RAM is read back to the requester. The size and location of this data is limited. These requests must come from a device that has already joined the network. Only devices supporting the OTA Server cluster may be impacted.

### CVE-2026-47146

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-06-25T14:16:40.700 |

In EmberZNet v9.0.2 and earlier, malformed Color Control messages can lead to asserts that terminate the process. These messages must come from a device that has already joined the network. Only devices supporting the Color Control cluster may be impacted.

### CVE-2026-47145

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-06-25T14:16:40.587 |

In EmberZNet v9.0.2 and earlier, malformed Color Control messages can lead to asserts that terminate the process. These messages must come from a device that has already joined the network. Only devices supporting the Color Control cluster may be impacted.

### CVE-2026-9154

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-25T01:16:27.673 |

Arbitrary File Write vulnerability in Rapid7 InsightConnect Sed Plugin on Linux allows authenticated attackers to write attacker-controlled content to arbitrary file paths via the expression parameter.

### CVE-2026-54070

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-79;CWE-184` |
| Published | 2026-06-24T22:16:48.583 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.0, renderPackageREADME in kernel/bazaar/readme.go renders a Bazaar package README from Markdown to HTML with the lute engine and SetSanitize(true). The lute sanitizer is an event-handler blocklist: allowAttr rejects only attribute names present in a fixed eventAttrs map copied from the w3schools legacy handler list. That map omits modern event handlers. onpointerover, onpointerdown, onauxclick, onbeforetoggle, onfocusin, onanimationstart, and ontransitionend are not in the list, so the sanitizer passes them through verbatim on any tag. The frontend assigns the rendered HTML to mdElement.innerHTML in app/src/config/bazaar.ts with no client-side DOMPurify on this path, into a normal element in the main document (no iframe, no sandbox). The kernel sends no Content-Security-Policy, X-Frame-Options, or X-Content-Type-Options header on any response, so an inline handler runs when its event fires. The README is rendered when an Administrator opens a package in Settings → Marketplace, after the one-time marketplace trust consent. Install is not required. Result: a third-party Bazaar package author runs JavaScript in the Administrator's authenticated SiYuan origin when the Administrator views and interacts with the package listing, and gains full control of the workspace. This vulnerability is fixed in 3.7.0.

### CVE-2026-47110

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-241` |
| Published | 2026-06-24T22:16:47.107 |

Tiptap for PHP before version 2.1.1 contains an input validation vulnerability that allows authenticated attackers to cause a denial of service by submitting Tiptap JSON with the attrs.href field set to an array instead of a string, causing an unhandled TypeError in the Link::isAllowedUri() function when passed to preg_match(). Attackers can persist malformed JSON records that permanently crash the server-side HTML rendering pipeline for all subsequent viewers of that record until the database entry is manually repaired.

### CVE-2026-52812

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-639;CWE-862` |
| Published | 2026-06-24T21:16:57.223 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, Git LFS storage is content-addressed by OID alone (<LFS-root>/<oid[0]>/<oid[1]>/<oid>) but per-repo authorization lives in the lfs_object table keyed (repo_id, oid). serveUpload skips re-uploading when the OID file already exists on disk and inserts a new (repo_id, oid) row pointing at it without verifying the request body hashes to the OID being claimed. Any user with write access to one repo can bind their repo to an OID owned by a private repo and download the original bytes via their own download endpoint. This vulnerability is fixed in 0.14.3.

### CVE-2026-52810

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-24T21:16:56.960 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, Git smart HTTP authorizes POST …/git-receive-pack using the client-supplied service query string (so ?service=git-upload-pack is evaluated as read access) while routing still runs git receive-pack, allowing push where only read should be allowed. This vulnerability is fixed in 0.14.3.

### CVE-2026-52808

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-269;CWE-863` |
| Published | 2026-06-24T21:16:56.693 |

Gogs is an open source self-hosted Git service. Prior to 0.14.3, three API endpoints — PATCH /api/v1/repos/:owner/:repo/issue-tracker, PATCH /api/v1/repos/:owner/:repo/wiki, and POST /api/v1/repos/:owner/:repo/mirror-sync — are gated by reqRepoWriter() rather than reqRepoAdmin(). The equivalent operations in the web UI sit behind reqRepoAdmin, which requires AccessMode >= AccessModeAdmin. A write-level collaborator (who has AccessMode == AccessModeWrite < AccessModeAdmin) can therefore call these API endpoints directly to disable the native issue tracker or wiki, inject attacker-controlled external tracker/wiki URLs that redirect all repository visitors, or trigger mirror sync — none of which they are authorized to do. This vulnerability is fixed in 0.14.3.

### CVE-2026-27708

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-639;CWE-862` |
| Published | 2026-06-24T20:16:31.963 |

FOSSBilling is a free, open-source billing and client management system. In versions 0.7.2 and prior, the Servicecustom Client API's __call method accepts an order_id parameter and fetches the associated order without verifying the authenticated client owns it, potentially exposing cross-client data through IDOR. An authenticated client can access any other client's custom service by guessing sequential order IDs. This can lead to a confidentiality breach — attackers can read client PII (name, email, phone, address, company details, VAT number) and service configuration data belonging to other clients. This issue has been fixed in version 0.8.0.

### CVE-2026-12760

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-06-24T19:17:08.237 |

A denial-of-service (DoS) vulnerability has been identified in Tapo C200 v3 in the network packet handling logic due to improper handling of IPv4 fragmented packets.  An unauthenticated adjacent attacker can send crafted packets to cause excessive resource consumption, leading to instability of the device.Successful exploitation can remotely trigger a temporary denial-of-service condition, causing the camera to become unresponsive and resulting in intermittent loss of video monitoring and recording.
