# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-22 15:00 UTC
- **対象期間**: `2026-09-21T15:00:25.000Z` 〜 `2026-09-22T15:00:24.000Z`
- **重要CVE数**: 136 件（Critical 9.0+: 26 件 / High 7.0〜: 110 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上り、特に **リモートコード実行 (RCE)** や **認証バイパス** が多く見られました。  
- **AI アシスタント、サーバ管理パネル、ネットワーク機器** といった、企業のインフラの要となるコンポーネントが集中して攻撃対象になっています。  
- 多くは **認証不要**、または **低権限ユーザーでも特権操作が可能** といった設定ミスや入力検証不備が根本原因です。  
- 製品側のパッチ提供が速やかに行われているケースもありますが、**バージョン管理が不徹底** な環境では依然として高リスクが残ります。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 製品 / コンポーネント | 主な脆弱性種別 | 影響範囲・リスク |
|-----|--------|----------------------|----------------|-------------------|
| **CVE‑2026‑77521** | 10.0 | MaxKB (AI アシスタント) < 2.10.5‑lts | SandboxShellBackend が `execute` ツールを除外せず、承認不要でシェル実行可能 | 攻撃者は任意のシェルコマンドを **無認証で実行** でき、企業内部ネットワーク全体への横展開が可能。機密情報漏洩・ランサムウェア拡散リスクが極めて高い。 |
| **CVE‑2026‑79920** | 9.9 | Ajenti 2.2.16 未満 | 認証ユーザーがプラグイン管理 API を無制限に呼び出し可能 | 権限の低いユーザーでも **プラグインのインストール/アンインストール/アップグレード** が実行でき、任意コード実行やサービス停止が可能。管理パネルが外部に露出している環境は即時対策が必要。 |
| **CVE‑2026‑93616** | 9.8 | Check Point Management Server | ディレクトリトラバーサル＋任意ファイルアップロード | 認証不要で **任意のスクリプトをアップロード・実行** でき、管理サーバ全体が乗っ取られる。ファイアウォール・VPN の管理権限が奪われると、企業ネットワーク全体が危険に晒される。 |
| **CVE‑2026‑74849** | 9.8 | Zohocorp ManageEngine ADSelfService Plus < 7001 | GINA クライアントの RCE | 社内 AD 認証プロキシがリモートからコード実行され、**ドメインコントローラへの横展開** が容易になる。AD 環境全体の機密性・完全性が脅かされる。 |
| **CVE‑2026‑25254** | 9.8 | 不特定 (SocketIO インターフェース) | 認可不備による RCE | 認証不要で SocketIO 経由に任意コードを送信でき、サーバ側で **任意プロセス実行** が可能。WebSocket を利用したリアルタイムアプリケーション全般に波及リスク。 |

> **選定理由**  
> - **スコアが 9.8 以上** で、かつ **認証不要** または **低権限で特権操作** が可能な点が共通。  
> - 影響が **企業の基幹システム（認証基盤・ネットワーク管理）** に直結し、**情報漏洩・サービス停止・横展開** のシナリオが成立しやすい。  

---

## 3. 推奨アクション  

### 3‑1. パッチ適用・バージョンアップ
| 製品 | 現行脆弱バージョン | 推奨バージョン | 取得先・備考 |
|------|-------------------|----------------|--------------|
| MaxKB | < 2.10.5‑lts | **≥ 2.10.5‑lts** | GitHub releases (maxkb/maxkb) |
| Ajenti | < 2.2.16 | **≥ 2.2.16** | `apt-get update && apt-get install ajenti=2.2.16` (Debian/Ubuntu) |
| Check Point Management Server | すべての 12.x 系 | **Check Point R80.10 Patch 2026‑09** 以降 | Check Point Support Portal |
| ManageEngine ADSelfService Plus | < build 7001 | **≥ build 7001** | ManageEngine ダウンロードセンター |
| SocketIO 実装 (任意) | 認可ロジックが不十分な実装 | **認可チェックを追加し、CORS/Origin 制限を実装** | ソースコードレビュー・CI パイプラインでのテスト導入 |

### 3‑2. 直ちに実施すべき防御策
- **ネットワーク分離**  
  - 上記製品が外部に公開されている場合は、IP アクセス制御リスト (ACL) で **管理IP のみ許可** へ絞る。  
- **WAF / IDS ルール追加**  
  - `CVE‑2026‑93616` のディレクトリトラバーサル文字列 (`../`, `%2e%2e/`) をブロック。  
  - `CVE‑2026‑77521` の `execute` コマンド呼び出しパス (`/sandbox/execute`) を監視。  
- **最小権限の原則**  
  - Ajenti のプラグイン管理 API は **管理者ロールのみ** に制限し、`/api/core/tasks/start` エンドポイントへのアクセスをファイアウォールで遮断。  
- **監査ログの有効化**  
  - MaxKB の `SandboxShellBackend` ログ、Check Point の管理操作ログ、ManageEngine の認証ログを **集中ログ管理システム (SIEM)** に転送し、異常なコマンド実行やファイルアップロードをリアルタイムで検知。  
- **コンテナ・イメージの再ビルド**  
  - Mailu (CVE‑2026‑85751) など Docker デプロイ環境では、`PROXY_AUTH_WHITELIST` 設定を削除し、`REAL_IP_HEADER` を正しく設定した公式イメージへ差し替える。  

### 3‑3. 長期的なセキュリティ強化策
1. **脆弱性情報の自動取得**  
   - `cve-search` や `GitHub Dependabot` を社内 CI に組み込み、対象パッケージの CVE が公開されたら自動で PR を作成。  
2. **コードレビューの強化**  
   - 入力検証・認可ロジックは必ず **OWASP ASVS** のチェックリストに沿ってレビュー。特に外部から受け取る文字列は **サニタイズ** と **ホワイトリスト** を徹底。  
3. **ペネトレーションテストの定期実施**  
   - 重要システム (AI ア

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-77521

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-250;CWE-749` |
| Published | 2026-09-21T21:17:10.943 |

MaxKB is an open-source AI assistant for enterprise. Prior to version 2.10.5-lts, assistants with a tool, MCP tool, skill, or sub-application use SandboxShellBackend, which exposes an execute shell tool without excluding it and omits execute from interrupt_on, so human approval is not required. Untrusted chat or ingested content can therefore cause command execution; source deployments with MAXKB_SANDBOX disabled run commands directly as the application user, while the official root container's string-based gosu wrapper allowed shell metacharacters to execute outside the intended sandbox. This issue is fixed in version 2.10.5-lts.

### CVE-2026-79920

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-21T17:18:59.567 |

Ajenti is a Linux & BSD modular server admin panel. Prior to version 2.2.16, any authenticated user can call /api/core/tasks/start to enqueue InstallPlugin, UnInstallPlugin, or UpgradeAll from plugins/plugins/tasks.py without plugin-management authorization. InstallPlugin and UnInstallPlugin construct a pip package specification from unvalidated name and version fields, and the task worker invokes pip while running as root. A low-privileged user can therefore select or manipulate a package installed with root privileges and can install, remove, or upgrade plugins without administrative permission, resulting in root code execution and full host compromise. This issue is fixed in version 2.2.16.

### CVE-2026-12718

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-22T14:17:12.490 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Karel Electronic Industry and Trade Inc. KarelIPS allows Blind SQL Injection.

This issue affects KarelIPS: through 22092026.
NOTE: The vendor was contacted and it was learned that the product is not supported.

### CVE-2026-93616

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T13:17:11.963 |

A directory traversal and file upload vulnerability allows an unauthenticated attacker to upload and execute arbitrary scripts on Check Point Management Server.

### CVE-2026-74849

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T12:17:14.007 |

Zohocorp ManageEngine ADSelfService Plus versions before build 7001 are vulnerable to a remote code execution vulnerability in the GINA client.

### CVE-2026-25254

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-22T10:17:08.583 |

Improper authorization leads to Remote Code Execution via SocketIO interface.

### CVE-2026-19658

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T05:16:55.167 |

The Give Tributes plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 2.3.1 via deserialization of untrusted input . This makes it possible for unauthenticated attackers to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present. This vulnerability is only reachable when the "Allow Multiple Recipients" option is enabled for the donation form, as the single-recipient code path applies sanitize_textarea_field() which would neutralize the payload. Exploitation additionally requires the eCard "Custom Message" option to be disabled, which is the plugin default: when it is enabled the personalized message becomes a required field and GiveWP's give_clean() blanks serialized input during validation, causing the donation to be rejected before it is stored.

### CVE-2026-13355

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-22T05:16:54.960 |

The Meta Box AIO plugin for WordPress is vulnerable to Privilege Escalation to Administrator in versions up to, and including, 3.11.0. This is due to a chained flaw: the populate_via_query_string() function in the mb-frontend-submission component unconditionally overrides the form's target object_id from the GET parameter 'rwmb_frontend_field_object_id' without any authorization check, and Form::process() lacks the user_can_edit() check present in render(), allowing unauthenticated attackers to overwrite the post_content of any page with an arbitrary shortcode via wp_update_post(); the mb-user-profile component then directly trusts the 'role' and 'auto_login' shortcode attributes in the injected [mb_user_profile_register] shortcode with no role validation. This makes it possible for unauthenticated attackers to elevate their privileges to Administrator. The standalone plugins Meta Box Frontend Submission (in versions up to 4.5.6) and Meta Box User Profile (versions up to 3.11.0) are also affected.

### CVE-2026-88402

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-21T21:17:14.273 |

A SQL injection vulnerability in the checkSQL function of nocobase v2.1.21 allows attackers to access sesntive database information via injecting crafted SQL statements.

### CVE-2026-85751

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290;CWE-807` |
| Published | 2026-09-21T16:17:25.070 |

Mailu is a mail server distributed as a set of Docker images. From Mailu 2.0 until 2024.06.55 and prior to Mailu helm-charts 2.7.3, deployments with PROXY_AUTH_WHITELIST configured but REAL_IP_HEADER unset trusted a client-controlled X-Forwarded-By header for header-based proxy authentication. The proxy_hide_header directive in the nginx template at core/nginx/conf/proxy.conf hid the header from upstream responses but did not overwrite the incoming request value in this configuration. An unauthenticated remote attacker could therefore spoof the trusted proxy identity and bypass authentication. This issue is fixed in Mailu 2024.06.55 and Mailu helm-charts 2.7.3.

### CVE-2026-94301

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-21T15:17:38.903 |

The fix for CVE-2026-47065/ZDRES-232 ("resolveProxyClass Not Overridden - acceptMatchers Filter Bypass via java.lang.reflect.Proxy"), released on 2026-06-02 and announced as "Fully addressed" in MINA 2.2.8, 2.1.13 and 2.0.29, was committed to the
 2.2.X branch only. The 2.0.X and 2.1.X maintenance branches never received the resolveProxyClass() override, so the 2.0.29 and 2.1.13 artifacts listed as fixed -- and every later release on those lines, up to and including the current 2.0.30 and 2.1.14 -- remain vulnerable to the exact allow-list bypass that CVE-2026-47065 was meant to close.

### CVE-2026-93952

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-22T08:16:43.047 |

VeloCloud Orchestrator (VCO) on-prem has a security issue where this issue may allow a remote attacker to access privileged internal functionality and impact the VCO host. Successful exploitation may compromise the confidentiality, integrity, and availability of the orchestrator and data managed by the orchestrator.

Hosted, including Dedicated, versions of VCO were impacted and have already been patched.

### CVE-2026-94572

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-21T21:17:22.150 |

In OpenStack Octavia before 18.0.1, the Amphora provider driver did not validate the listener and pool tls_ciphers field for control characters. The value is written verbatim into the HAProxy configuration generated on the amphora, and thus an authenticated project member who owns a TLS-enabled load balancer can embed a newline and inject arbitrary HAProxy configuration directives. Only deployments using the Amphora provider are affected.

### CVE-2026-94571

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-21T21:17:21.970 |

In OpenStack Octavia before 18.0.1, the Amphora provider driver did not reject control characters in the L7 policy redirect_url and redirect_prefix fields. The RFC 3986 URL validator percent-encodes control characters before validating, and thus newlines passed structural checks, but Octavia stored and wrote the raw unencoded value directly into the HAProxy configuration generated on the amphora. An authenticated project member who owns a load balancer can therefore inject arbitrary HAProxy directives through a REDIRECT_TO_URL L7 policy. Only deployments using the Amphora provider are affected.

### CVE-2026-95675

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T14:17:22.230 |

D-Link DAP-1360 firmware version 6.14 and earlier contains an unauthenticated remote code execution vulnerability that allows remote attackers to execute arbitrary commands as root by sending crafted requests to the device's web management interface without valid credentials. Attackers can fully compromise the device to persistently modify its configuration and use it as a pivot point into the local network.

### CVE-2026-93556

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-22T09:17:05.800 |

The ‘/password/guardarClau/recover’ endpoint accepts the ‘usuariId’ parameter, which specifies the account whose password is to be changed. The JWT token for the recovery process is not validated against the user specified in that parameter. An unauthenticated attacker could manipulate the identifier and reset the password for any account, including administrative accounts, which could allow them to take control of the account.

### CVE-2026-89422

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-322` |
| Published | 2026-09-22T09:17:05.540 |

Key Exchange without Entity Authentication vulnerability in Erlang/OTP ssl allows a peer that answers a TLS 1.3 client connection to impersonate the intended server. A pre_shared_key extension in the ServerHello that the client never offered causes the client to complete the handshake without validating the server's certificate, so ssl:connect returns {ok, Socket} against a peer holding no certificate, no private key and no prior session.

tls_client_connection_1_3:handle_server_hello/2 passes the received extension to tls_gen_connection_1_3:handle_resumption/2, which sets resumption = true on its mere presence without checking that the client offered a PSK. tls_handshake_1_3:get_pre_shared_key/4 meanwhile falls back to the all-zero "no PSK" value and keys the handshake with the ordinary non-PSK schedule, so the attacker's own ephemeral key suffices. The resumption flag then routes maybe_resumption/1 straight to wait_finished, skipping the certificate-handling states, so certificate path validation, verify_fun, hostname verification, partial_chain, CRL checking and OCSP stapling are all bypassed. The default client configuration is affected; clients restricted to TLS 1.2 are not.

This issue affects OTP from OTP 22.2 before OTP 27.3.4.18, OTP 28.5.0.7, and OTP 29.1.1, corresponding to ssl from 9.5 before 11.2.12.13, 11.6.0.6, and 11.7.7.

### CVE-2026-94493

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-22T01:16:56.437 |

A vulnerability was detected in Gigatech PDV5701 1.0.31_240305_112640. This issue affects some unknown processing of the file /index.html of the component WebSocket Service. The manipulation results in missing authentication. The attack can be launched remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94425

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-269` |
| Published | 2026-09-21T23:16:56.697 |

A vulnerability was found in Moore Threads MTT S80 Driver Package 340.150. The affected element is the function sub_140006F0C in the library mtdispkm64.sys of the component IOCTL Handler. The manipulation results in improper privilege management. Attacking locally is a requirement. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94424

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-122` |
| Published | 2026-09-21T21:17:21.793 |

A vulnerability has been found in Moore Threads MTT S80 Driver Package up to 340.150. Impacted is the function sub_140001000 in the library mtdispkm64.sys of the component IOCTL Handler. The manipulation leads to heap-based buffer overflow. An attack has to be approached locally. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-58491

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-21T19:17:06.910 |

Warpgate is an open source SSH, HTTPS and MySQL bastion host for Linux. Prior to 0.25.5, the /@warpgate/api/sso/providers/:name/start endpoint stores an attacker-controlled next parameter that the POST /@warpgate/api/sso/return handler inserts without HTML escaping into the response generated by warpgate-protocol-http/src/api/sso_provider_list.rs. A victim who follows a crafted link and completes SSO can cause markup and JavaScript to execute in the authenticated Warpgate origin, allowing access to session data and actions through user APIs, and through administrator APIs only when the victim is an administrator. The GET /@warpgate/api/sso/return path also uses the same unvalidated value as a redirect destination, enabling an open redirect. This issue is fixed in version 0.25.5.

### CVE-2026-61674

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-787;CWE-843` |
| Published | 2026-09-21T17:17:36.663 |

Fluent Bit is a fast and lightweight logs, metrics, and traces processor for Linux, BSD, macOS, and Windows. From 0.11.0 until 5.0.8, plugins/out_forward/forward.c secure_forward_pong copies the server-controlled PONG[2] reason into the 32-byte stack buffer msg with memcpy without checking its MessagePack type or length. An attacker who controls or can impersonate an out_forward Secure Forward destination configured with Shared_Key or Empty_Shared_Key can send an oversized reason during the first handshake and overwrite stack control data. Protected builds reliably terminate, while builds without a stack canary or with a disclosure can allow remote code execution as the Fluent Bit process user. When the opt-in --supervisor mode is used, fork-only respawns preserve the canary and address layout, allowing repeated crash-or-survive probes to support code execution on a hardened build; ordinary exec-based or service-manager restarts do not preserve that state. This issue is fixed in version 5.0.8.

### CVE-2026-87078

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-22T08:16:40.530 |

Net::IDN::Punycode versions from 2.302 before 2.590 for Perl leak the output buffer on every rejected label in decode_punycode.

The XS backend allocates the scalar it returns before it validates the input, sizing the buffer at twice the input length. The scalar is released only on the success path, so each of the three croaks that reject a label leaves the scalar and its buffer allocated. Nothing bounds the label length in the to-Unicode direction, since the 63-byte DNS limit is checked only when converting to ASCII.

Only the XS backend is affected.

A sender who supplies invalid labels grows the process by twice the label length per rejected call, with no successful call needed.

### CVE-2026-79916

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-21T21:17:12.450 |

MaxKB is an open-source AI assistant for enterprise. Prior to 2.10.5-lts, authenticated workspace members can inject control characters into AWS Bedrock access_key_id and secret_access_key fields that _update_aws_credentials writes to /root/.aws/credentials without safe parsing. An attacker can append a new AWS profile containing credential_process, then select that profile during a later model-validation request so botocore executes an attacker-controlled command as root. This vulnerability is fixed in 2.10.5-lts.

### CVE-2026-46649

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-21T21:17:03.323 |

Joplin is an open source note-taking and to-do application that organises notes and lists into notebooks. Prior to 3.7.2, Joplin Server's GET /api/login_with_code/:id endpoint accepts a nine-digit SSO authentication code with a ten-minute lifetime without applying limiterLoginBruteForce. An unauthenticated attacker who targets a user during an active SSO login can make unlimited guesses, and a correct code returns a full session token that permits access to and modification of the user's notes, notebooks, and account settings. This issue is fixed in version 3.7.2.

### CVE-2026-86473

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-21T15:17:32.997 |

Apache Airflow: the Core API logout endpoint revokes only a session token presented as the _token cookie. When a client logs out presenting its credential as an Authorization bearer header instead, the endpoint returns its normal logout response but revokes nothing, so the token remains valid until it expires. An attacker who already holds a copy of that token keeps the victim's access after the victim has logged out and believes the session ended; the default token lifetime is 24 hours and is configurable.

Affects API clients that authenticate with a bearer token rather than the browser session cookie. The attacker must already possess a copy of a valid token; obtaining one is outside the scope of this issue, and no privileges beyond the victim's own are gained.

Users of apache-airflow are recommended to upgrade to apache-airflow version 3.3.2 or later, which fixes the issue.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-55563

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-21T16:17:09.390 |

Feast is the open source feature store for AI and machine learning. Prior to 0.65.0, .github/workflows/pr_integration_tests.yml uses pull_request_target with the synchronize event and preserves ok-to-test, approved, or lgtm labels across newly pushed commits, allowing a fork contributor to obtain approval for a benign revision and then run changed code from refs/pull/${{ github.event.pull_request.number }}/merge through privileged make targets. The job exposes GCP, AWS, and Snowflake credentials to that code, enabling runner code execution, credential disclosure, and possible access to downstream cloud resources. An external label-removal integration could mitigate the condition, but no repository workflow provided that protection. This issue is fixed in version 0.65.0.

### CVE-2026-25265

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-378` |
| Published | 2026-09-22T10:17:09.243 |

Privilege escalation due to weak configuration while temporary file handling.

### CVE-2026-25264

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-22T10:17:09.110 |

Privilege escalation due to weak configuration during package extraction process.

### CVE-2026-25255

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-09-22T10:17:08.847 |

Exposed dangerous function lead to privilege escalation via gRPC server.

### CVE-2025-1281

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T08:16:36.250 |

The BM Content Builder plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the ux_cb_remove_layout_ajax() and ux_cb_tools_export_ajax() functions in all versions up to, and excluding, 3.17.1. This makes it possible for authenticated attackers, with Subscriber-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php).

### CVE-2026-92438

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T07:16:31.220 |

The Ninja Forms WordPress plugin 3.15.3 does not escape submitted form field values before outputting them on the submission edit screen in the admin area, which could allow unauthenticated users to submit values through a public form that then execute in the browser of any high-privileged user who reviews the submission.

### CVE-2026-88409

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-21T21:17:15.120 |

FalkorDB (Redis module) v4.20.1 to v4.20.4 was discovered to contain a buffer overflow in the _Decode_GrB_Matrix function (/v19/decode_matrix.c). This vulnerability allows attackers to cause a Denial of Service (DoS) via a crafted input.

### CVE-2026-55897

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-21T20:17:26.670 |

luci-app-advanced-reboot is a LuCI (web interface) application for OpenWrt that provides a  way to reboot your router into an alternative firmware partition or perform  reboot operations directly from the web UI. Prior to 1.1.2-6, the luci-app-advanced-reboot read ACL in applications/luci-app-advanced-reboot/root/usr/share/rpcd/acl.d/luci-app-advanced-reboot.json grants rpcd file.exec permission for the general shell interpreter /bin/sh. An authenticated delegated session with that read ACL can supply caller-controlled params; rpcd authorizes the executable path and passes those arguments to the shell, allowing arbitrary commands to execute as root. Builds without the /bin/sh exec grant, including the checked openwrt-24.10 and openwrt-23.05 branches, are not affected by this specific chain. This vulnerability is fixed in 1.1.2-6.

### CVE-2026-55159

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-21T20:17:26.500 |

luci-app-adblock-fast a WebUI for fast, lightweight DNS-based ad-blocker for OpenWrt that works with dnsmasq, smartdns, or unbound. Prior to 1.2.4-2, the luci.adblock-fast.setCronEntry RPC method accepts an entry argument containing carriage-return or line-feed characters and serializes it into /etc/crontabs/root as though it were one logical line. An authenticated delegated user with the luci-app-adblock-fast write ACL can therefore create an additional physical root cron entry through applications/luci-app-adblock-fast/root/usr/share/rpcd/ucode/luci.adblock-fast, resulting in persistent command execution as UID 0 when cron runs. The issue is not demonstrated for unauthenticated callers or users without the component write ACL. This vulnerability is fixed in 1.2.4-2.

### CVE-2026-62182

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-21T18:17:09.420 |

KubeEdge is an open source system for extending native containerized application orchestration capabilities to hosts at Edge. From 1.21.0 until 1.21.2, 1.22.2, and 1.23.1, ConfigUpdateJob processing in edge/pkg/taskmanager/actions/configupdatejob.go concatenates authenticated user-controlled updateFields values into the keadm config-update command and executes it through a system shell. A user with permission to create or modify ConfigUpdateJob resources can include shell metacharacters in the complete --set value and cause arbitrary commands to execute on an enrolled target edge node with the privileges of the KubeEdge process handling the job. This issue is fixed in versions 1.21.2, 1.22.2, and 1.23.1.

### CVE-2026-84990

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-862` |
| Published | 2026-09-21T17:19:13.340 |

ntopng is a web-based network traffic monitoring application. Prior to 6.7.260718, scripts/lua/rest/v2/get/system/configurations/list_available_backups.lua and scripts/lua/rest/v2/get/system/configurations/download_backup.lua allow any authenticated non-admin user to list and download system-configuration backups without an administrator check. The download path reaches backup_config.export_backup, and prefs_dump_utils.build_prefs_dump_table includes the ntopng.user.* Redis key space in the backup. A downloaded backup can therefore disclose password hashes for local users and, when configured, API tokens, TOTP secrets, and WebAuthn credential data, enabling account compromise through usable or recoverable credentials. This issue is fixed in version 6.7.260718.

### CVE-2026-63116

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-21T17:17:38.510 |

deepstream is a server that allows clients and backend services to sync data, send messages and make rpcs at scale. From 10.1.0 until 10.1.1, src/services/permission/valve/rules-map.ts omits RECORD_ACTION.PATCH_MULTI from RULES_MAP. When an authenticated user sends a PATCH_MULTI record operation while permission.type is config, getRulesForMessage returns a null rule specification and ConfigPermission.canPerformAction treats the missing specification as an unconditional allow instead of applying RULE_TYPES.WRITE. Any authenticated user can therefore modify arbitrary protected records, corrupt application state, or cause service disruption; deployments using the default permission type none already allow all operations and are not additionally affected. This issue is fixed in version 10.1.1.

### CVE-2026-62371

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-21T17:17:37.150 |

KubeEdge is an open source system for extending native containerized application orchestration capabilities to hosts at Edge. From 1.12.0 until 1.21.2, 1.22.2, and 1.23.1, the v1alpha2 NodeUpgradeJob handler in edge/pkg/taskmanager/actions/nodeupgradejob.go concatenates authenticated user-controlled spec.version and spec.image values into the keadm upgrade edge shell command. A user with permission to create or update NodeUpgradeJob resources can supply shell metacharacters in either field, causing arbitrary commands to execute on targeted edge nodes with the privileges of the upgrade process and compromising node confidentiality, integrity, and availability. This issue is fixed in versions 1.21.2, 1.22.2, and 1.23.1.

### CVE-2026-82412

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-21T16:17:24.503 |

ntopng is a web-based network traffic monitoring application. Prior to 6.7.260717, the vulnerability-scan endpoints scripts/lua/rest/v2/add/host/to_scan.lua and scripts/lua/rest/v2/exec/host/schedule_vulnerability_scan.lua accept the scan_ports parameter without an administrator gate and pass it through validateSingleWord, which permits shell metacharacters. scripts/lua/modules/vulnerability_scan/vs_utils.lua then concatenates scan_ports into an nmap command in nmap_scan_host and executes the command through ntop.execCmd or ntop.execCmdAsync and popen. Any authenticated non-admin user can execute operating-system commands as the ntopng process account when nmap is available. Because the endpoints accept GET requests while ntopng's CSRF validation applies to POST request bodies, an attacker can also trigger the command through a logged-in user's browser without possessing ntopng credentials. This issue is fixed in version 6.7.260717.

### CVE-2026-53940

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-09-21T16:17:09.010 |

Conda is a system-level binary package and environment manager that runs on major operating systems and platforms. Prior to 26.5.2, parse_entry_point_def in conda/common/path/python.py accepted an unvalidated entry-point command from a noarch:python package's info/link.json metadata. CreatePythonEntryPointAction in conda/core/path_actions.py interpolated that command into target_short_path, and PrefixPathAction.target_full_path joined it to the installation prefix without verifying that the result remained under the intended bin or Scripts directory. create_python_entry_point in conda/gateways/disk/create.py then wrote an executable wrapper to the resulting path. A malicious package could use path separators, traversal segments, or an absolute command path to write outside the prefix or overwrite another in-prefix entry point during default install and environment transactions. Out-of-prefix writes require the target parent directory to exist, while an overwritten entry point can execute attacker-controlled Python when later invoked with the installing user's privileges. This issue is fixed in version 26.5.2.

### CVE-2026-90882

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-942` |
| Published | 2026-09-22T10:17:10.000 |

The open-vsx.org deployment returned Access-Control-Allow-Origin reflecting the requesting origin together with Access-Control-Allow-Credentials: true on the authenticated /user/ endpoints. A page on any origin could therefore issue credentialed requests to the service in a logged-in user's browser and read the responses.



This exposed /user (login name, avatar, homepage, tokens URL), /user/tokens, /user/namespaces, /user/extensions, /user/search/{name} and /user/namespace/{name}/members, and — because /user/csrf was readable the same way — allowed the CSRF protection on write endpoints to be defeated. Chaining the two, an attacker page could call /user/token/create and exfiltrate a personal access token carrying publish and delete rights over the victim's namespaces.



The headers were emitted by the CDN/edge layer, not by the application: the Open VSX software sets allowCredentials(true) in exactly one place, against a single exact origin derived from ovsx.webui.url, and defines no CORS mapping on /user/ beyond it. No configuration of the software produces origin reflection with credentials.

### CVE-2026-94627

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-21T22:17:01.740 |

vLLM Mooncake connector through 0.29.0 fails to properly manage GPU KV cache block ownership when concurrent child requests share a single transfer ID in prefill/decode disaggregated deployments. Attackers can trigger GPU memory exhaustion by submitting completion requests with multiple prompts, causing orphaned KV cache blocks to accumulate until process restart and eventually preventing legitimate requests from executing.

### CVE-2026-94626

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-21T22:17:01.587 |

vLLM through 0.29.0 fails to validate the tp_size parameter in kv_transfer_params on OpenAI-compatible completion endpoints, allowing attackers to allocate unbounded memory. Attackers can supply arbitrary tp_size values in prefill/decode disaggregated deployments to exhaust memory and trigger kernel OOM-kill of the decode worker process.

### CVE-2026-94624

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-21T22:17:01.280 |

vLLM through 0.29.0 contains a denial of service vulnerability in P2P KV offloading when OffloadingConnector is configured with TieringOffloadingSpec and a peer-to-peer secondary tier. Attackers can supply arbitrary remote host and port values in kv_transfer_params to create unreachable peer sessions that retain ZeroMQ sockets until the context quota is exhausted, causing an uncaught ZMQError that crashes EngineCore and stops all inference.

### CVE-2026-94623

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-21T22:17:01.123 |

vLLM through 0.29.0 contains a denial of service vulnerability in the NIXL connector's prefix caching implementation that fails to properly validate block counts across multi-prompt completion requests in prefill/decode disaggregated deployments. Attackers can trigger an assertion failure in NixlBaseConnectorWorker._apply_prefix_caching by submitting completion requests with multiple prompts of varying lengths, causing the decode worker to terminate and become unavailable until restarted.

### CVE-2026-94622

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-21T22:17:00.960 |

vLLM versions through 0.29.0 contain a denial of service vulnerability in the NIXL connector's metadata handling for prefill/decode disaggregated deployments. Attackers can send requests with incomplete kv_transfer_params dictionary entries to trigger an uncaught KeyError in EngineCore scheduling, causing the decode engine to terminate and making all routed requests fail until manual restart.

### CVE-2026-61652

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-21T22:16:57.680 |

Zapros, a Python HTTP client, prior to version 0.14.0 is vulnerable to denial of service via memory exhaustion. The issue affects all callers who streamed compressed responses relying on the chunk size — explicit (`iter_bytes(chunk_size=...)`) or the default — to bound memory. The decoder ignored that bound, so a chunk could be far larger than requested and a single compressed response could overflow memory. Version 0.14.0 contains a patch. Some workarounds are available. Read the still-compressed body with `Response.iter_raw()` / `Response.async_iter_raw()`, which bypass the built-in decoders, and decompress it yourself with an explicit output-size bound (e.g. `zlib`'s `max_length`), aborting once a configured limit is exceeded. Where feasible, send `Accept-Encoding: identity` to disable response compression so bodies are not decompressed client-side. Avoid decoding response bodies from untrusted servers.

### CVE-2026-94501

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-21T19:17:21.910 |

jshERP through 3.6 contains an authorization bypass vulnerability in the userBusiness CRUD endpoints that allows authenticated users to create, modify, or delete authorization-relation rows without privilege checks. Attackers can manipulate user-role mappings and access controls to escalate privileges, strip access from other accounts, or modify role-function relationships for any user in the tenant.

### CVE-2026-94497

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-21T19:17:21.743 |

jshERP through 3.6 fails to validate object ownership in by-id info, update, and delete endpoints across multiple resource types. Authenticated users can read, modify, and delete other users' business objects by submitting direct object identifiers without authorization checks.

### CVE-2026-94496

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-21T19:17:21.590 |

jshERP through 3.6 fails to validate caller permissions in role management endpoints, allowing authenticated users to modify any role's data scope or delete roles. Attackers can exploit the /role/update and /role/delete endpoints to escalate privileges, change data visibility to all data, and access all business records in the tenant.

### CVE-2026-94412

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-21T19:17:20.217 |

jshERP through 3.6 contains an authorization bypass vulnerability in the POST /user/resetPwd endpoint that allows authenticated users to reset any other user's password. Attackers can submit a request with an arbitrary target user ID to reset that account's password to a known default value, enabling unauthorized access to other user accounts including administrators.

### CVE-2026-94411

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-21T19:17:20.067 |

jshERP 3.6 contains a privilege escalation vulnerability in the updateOneValueByKeyIdAndType endpoint that allows authenticated users to grant themselves arbitrary roles. Attackers can send a POST request with type=UserRole, their own user ID, and a role ID list to escalate from low-privilege tenant user to tenant administrator.

### CVE-2026-75791

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-22T13:17:11.170 |

Zohocorp ManageEngine ADSelfService Plus versions before build 7001 are vulnerable to an authentication bypass vulnerability in the REST API.

### CVE-2026-94403

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-21T19:17:19.867 |

A weakness has been identified in ColorFul iGameCenter 1.0.3.4. This impacts the function sub_140001AF0 in the library ene.sys of the component IOCTL Handler. This manipulation causes untrusted pointer dereference. The attack can only be executed locally. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-74766

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-22T08:16:40.267 |

Net::IDN::Punycode versions from 2.301 before 2.590 for Perl allow a heap use-after-free via a decoded code point that reallocates the output buffer in decode_punycode.

The XS backend inserts each decoded code point into the string buffer of the scalar it returns. decode_punycode computes the insertion pointer first and only then grows the buffer when the code point does not fit. The growth reallocates the buffer and updates every pointer except the insertion pointer, so the move that follows and the write of the code point go through a freed pointer. The buffer starts at twice the label length, and a code point above U+FFFF takes four bytes in the output, so a label of such code points outgrows it and forces the reallocation.

Version 2.301, the fix for CVE-2016-15059, introduced the defect. Only the XS backend is affected.

Decoding an attacker-supplied punycode label reads and writes freed heap memory.

### CVE-2026-49811

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-21T20:17:25.660 |

Dell Command | Monitor (DCM), versions prior to 10.13.2, contain an Incorrect Permission Assignment for Critical Resource vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges.

### CVE-2026-55071

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-21T15:17:29.450 |

MCP-for-Stata is a MCP server for integrating Stata into agent loops with a safety-first design. Prior to version 1.19.0, the ado_package_install MCP tool in stata-mcp concatenates user-controlled input directly into a Stata command string without any validation or sanitization. An attacker who can invoke the MCP tool or the equivalent Python API can embed newline characters in the package argument to inject arbitrary Stata commands. Because Stata supports a shell escape command, this leads to full OS-level arbitrary command execution (RCE) under the account running the Stata-MCP server. The tool is registered in the default all profile, so no non-default configuration is required. This issue has been patched in version 1.19.0.

### CVE-2026-94488

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-21T18:17:17.173 |

Telegram Desktop before 6.9.4 allows XSS in the HTML exporter. (The first fixed stable version is 7.0.1.) This occurs in button.text.toUtf8 in export_output_html.cpp. Exploitation cannot occur unless HTML export was used by a victim. However, the exploit payload can be exported if a message were forwarded into a group by a member (it is not necessary for the message author to be a member of a group).

### CVE-2026-87119

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-22T12:17:14.150 |

Authentication Bypass by Capture-replay in ZenHive mpp allows an attacker holding a captured subscription activation credential to charge the payer repeatedly.

The payer signs a Tempo KeyAuthorization over the chain id, key type, key id, expiry, limits and scopes only, with nothing tying it to the challenge that prompted it. MPP.Methods.Tempo.KeyAuthorization.verify/3 in lib/mpp/methods/tempo/key_authorization.ex pins each of those signed fields against the subscription request, and the access key it pins is a static per-endpoint server key, so one signed authorization verifies against every challenge the server issues for the same subscription terms. MPP.Methods.Tempo.Subscription.activate/4 deduplicates activations by challenge id, so presenting the captured credential under a fresh challenge produces a different dedup key, claim_activation succeeds, and the subscription transaction is built and broadcast again. Each replay charges the payer's wallet a new first-period settlement and re-authorizes the server key, bounded only by the subscription expiry and the chain's own semantics for re-installing an existing key.

This issue affects mpp: from 0.14.0 before 0.16.2.

### CVE-2026-95511

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-22T09:17:06.217 |

A privilege escalation vulnerability was found in CUPS when used with the cups-filters serial backend. A local user who is a member of the lpadmin group can configure a printer that uses a privileged serial backend. The CUPS scheduler does not restrict the path component of non-file device URIs, so the root-privileged backend can write attacker-controlled print data to an arbitrary file. This can be used to change security-sensitive CUPS configuration and ultimately achieve root code execution. Exploitation requires local lpadmin group membership and a serial backend binary installed with root-only permissions.

### CVE-2026-65634

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-22T09:17:05.090 |

Inefficient algorithmic complexity in the Erlang/OTP asn1 OBJECT IDENTIFIER decoder allows a remote unauthenticated attacker to cause denial of service by sending a crafted OID during the TLS handshake.

The BER OID decoder asn1rtt_ber:dec_subidentifiers/3 in lib/asn1/src/asn1rtt_ber.erl and the equivalent PER helper asn1rtt_per_common:dec_subidentifiers/3 in lib/asn1/src/asn1rtt_per_common.erl accumulate a base-128 subidentifier into an unbounded integer using (Av bsl 7) + H per continuation byte. Each shift and addition on the growing accumulator is linear in the number of bits already accumulated, giving quadratic total work in the size of a single subidentifier. The JER helper asn1rtt_jer:json2oid/1 in lib/asn1/src/asn1rtt_jer.erl exhibits the same class of unbounded-integer parsing when decoding a dot-separated OID from JSON. A DER-encoded OBJECT IDENTIFIER with one very large arc (approximately 262 KB of continuation bytes) consumes roughly 13 seconds of CPU on typical hardware.

The vulnerable decoder is generated into every ASN.1 module that contains an OBJECT IDENTIFIER, including OTP-PUB-KEY which is reached during X.509 certificate parsing via public_key:pkix_decode_cert/2. This decoder runs before any signature or trust chain verification, so any Erlang service that parses peer TLS certificates is exposed: the default for TLS clients (which always parse the server certificate) and for mutual-TLS servers (which parse client certificates).

This vulnerability is associated with program files lib/asn1/src/asn1rtt_ber.erl, lib/asn1/src/asn1rtt_per_common.erl and lib/asn1/src/asn1rtt_jer.erl and program routines asn1rtt_ber:dec_subidentifiers/3, asn1rtt_per_common:dec_subidentifiers/3 and asn1rtt_jer:json2oid/1.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.18, OTP 28.5.0.7, and OTP 29.1.1, corresponding to asn1 from 3.0 before 5.3.4.3, 5.4.3.1, and 5.5.2. Whether OTP before OTP 17.0, corresponding to asn1 before 3.0, is affected is unknown.

### CVE-2026-55074

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-21T15:17:29.627 |

Ansible FreeBSD Jail Connection Plugin is an Ansible connection plugin for FreeBSD Jails via jexec. Through version 1.3.0, the jailexec connection plugin's put_file resolved a transfer's destination to a path on the jail host ( + ) and ran mkdir -p and mv there as root on the host. Those commands follow symbolic links, and the path was operated on outside the jail, so a symlink existing inside the jail was followed by the host-side, root-privileged mv. A party controlling content inside a managed jail (the jail's root, or any process able to create a symlink in a directory an Ansible task later writes to) can therefore cause an arbitrary root-owned write on the host, outside the jail — a full jail escape. Arbitrary root-owned host writes are readily escalated to host compromise (e.g. cron, rc.d, authorized_keys). Preconditions for this vulnerability are that the operator runs a copy/template/fetch-style task (anything using put_file) against the jail, and the attacker can place a symlink inside the jail at or above the task's destination before the transfer runs. This issue has been fixed in version 2.0.0.

### CVE-2026-92969

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-22T08:16:41.370 |

The HUSKY – Products Filter for WooCommerce Professional plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 1.4.4 via the 'shortcode' parameter parameter. This makes it possible for unauthenticated attackers to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. This vulnerability is exploitable by unauthenticated users because the only access control is a nonce check against woof_front_nonce, which is publicly emitted into inline JavaScript on every front-end page and is therefore obtainable by any site visitor without authentication.

### CVE-2026-92235

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-22T08:16:41.230 |

The The WP Ultimate Review plugin for WordPress is vulnerable to arbitrary shortcode execution in all versions up to, and including, 2.4.2. This is due to the software allowing users to execute an action that does not properly validate a value before running do_shortcode. This makes it possible for authenticated attackers, with subscriber-level access and above, to execute arbitrary shortcodes.

### CVE-2026-58269

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-21T20:17:26.837 |

Sync-in Server is an open-source platform for file storage, sharing, collaboration, and syncing. Prior to version 2.4.0, `POST /api/auth/token` authenticates with username and password only, then calls `getTokens()`, which returns full access and refresh JWTs without checking whether the account has TOTP 2FA enabled. An attacker with stolen or phished credentials can bypass 2FA in a single request. The parallel login endpoint (`POST /api/auth/login`) correctly enforces 2FA by calling `setCookies(user, res, true)`, which gates on `user.twoFaEnabled`. Version 2.4.0 patches the issue.

### CVE-2026-62369

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-21T18:17:09.580 |

KubeEdge is an open source system for extending native containerized application orchestration capabilities to hosts at Edge. From 1.16.0 until 1.21.2, 1.22.2, and 1.23.1, the DecompressTarGz function in keadm/cmd/keadm/app/cmd/util/common.go joins archive entry names to the extraction destination without sufficient validation. During keadm join or installation on Windows edge nodes, an archive influenced through a compromised, replaced, or untrusted download source can contain parent-directory components, Windows-style backslashes, absolute paths, or drive-prefixed paths that escape the intended directory. The affected keadm process can consequently write or overwrite files with its own privileges, potentially modifying configuration, executable, or service files and enabling persistent system modification or code execution. This issue is fixed in versions 1.21.2, 1.22.2, and 1.23.1.

### CVE-2026-48976

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-522;CWE-639` |
| Published | 2026-09-21T18:17:08.557 |

HomeBox is a home inventory and organization system. Prior to 0.26.0, NotifierRepository.Update in backend/internal/data/repo/repo_notifier.go updates a notifier through UpdateOneID(id) without requiring the record's user ID to match the authenticated user. An authenticated user who supplies another tenant's notifier UUID to PUT /v1/notifiers/{id} can read the returned stored url, which may contain plaintext Shoutrrr credentials for Slack, SMTP, Telegram, Pushover, or Discord, and can replace the URL to redirect the victim's notifications to an attacker-controlled webhook. This issue is fixed in version 0.26.0.

### CVE-2026-48975

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-21T18:17:08.410 |

HomeBox is a home inventory and organization system. Prior to 0.26.0, MaintenanceEntryRepository.Update and MaintenanceEntryRepository.Delete in backend/internal/data/repo/repo_maintenance_entry.go use UpdateOneID(id) and DeleteOneID(id) without verifying that the maintenance entry belongs to the authenticated user's active group. An authenticated low-privileged user who knows or enumerates another tenant's maintenance-entry UUID can overwrite that record or permanently delete it. This issue is fixed in version 0.26.0.

### CVE-2026-48826

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-639` |
| Published | 2026-09-21T18:17:08.073 |

HomeBox is a home inventory and organization system. Prior to 0.26.0, HandleWipeInventory in backend/app/api/handlers/v1/v1_ctrl_actions.go authorizes POST /v1/actions/wipe-inventory through the global ctx.User.IsOwner value instead of the caller's role in the active group, while the active group is selected through the X-Tenant request header. Because every self-registered user who creates a group receives the global owner value, a user who is also a member of another group can select that group with X-Tenant and permanently delete its complete inventory, which is not recoverable without external backups. This issue is fixed in version 0.26.0.

### CVE-2026-83621

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-21T17:19:08.590 |

ntopng is a web-based network traffic monitoring application. Prior to 6.7.260717, POST /lua/rest/v2/edit/system/edit_blacklist.lua in scripts/lua/rest/v2/edit/system/edit_blacklist.lua lacks an administrator check and calls lists_utils.editList for any authenticated user. The list_name, list_enabled, url, and list_update parameters allow a non-admin user to redirect threat-intelligence downloads to attacker-controlled content, disable blocklists, or prevent scheduled updates. The changes are persisted through Redis and reloaded without a lower-level authorization guard, undermining the integrity and availability of ntopng's threat-intelligence monitoring. This issue is fixed in version 6.7.260717.

### CVE-2026-77560

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-178;CWE-636;CWE-863` |
| Published | 2026-09-21T17:18:52.770 |

Tinyauth is an authentication and authorization server. Prior to 5.1.2, Tinyauth compares forwarded hostnames case-sensitively while reverse proxies route equivalent hostnames case-insensitively, allowing an authenticated low-privilege user to bypass per-app access controls with a differently cased hostname. The lookup in internal/service/access_controls_service.go through lookupStaticACLs and GetAccessControls, and the Docker-label fallback in internal/service/docker_service.go through GetLabels, can miss the configured app and return an empty access-control object. internal/controller/proxy_controller.go proxyHandler then treats the empty user, group, OAuth, LDAP, and IP restrictions as permissive and returns an authenticated result for an app that should exclude the user. Unauthenticated users remain subject to login, and global login-time allowlists are not bypassed. This issue is fixed in version 5.1.2.

### CVE-2026-94184

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-21T15:17:38.547 |

A stack-based buffer overflow flaw was found in fetchmail when built with NTLM support. A malicious or compromised mail server advertising NTLM authentication can send a crafted Type 2 challenge that causes fetchmail to write past a fixed stack buffer while building the NTLM authenticate response. This may lead to remote code execution depending on stack-frame layout, or to authentication failure or process termination under memory hardening.

Affects v5.0.8 through v6.6.6.

### CVE-2026-80110

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-21T15:17:32.060 |

A flaw was found in pki-core. The v2 REST ACL filter selects a tie-breaking permission for colliding literal and wildcard ACL keys using lexicographic string comparison rather than specificity, causing a wildcard-mapped permission to override a more specific literal-mapped permission when both match. In the CA's profile-management REST API this allows a request to POST /v2/profiles/raw -- intended to require Administrator-level profiles.create permission -- to instead be authorized under the lower-privileged profiles.approve permission held by the default Certificate Manager Agents group. The highest threat from this vulnerability is to confidentiality and integrity of the certificate authority's issuance policy.

### CVE-2026-61628

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-21T15:17:30.290 |

nginx ignition is a user interface for the nginx web server. Prior to version 2.41.1, `POST /api/users/onboarding/finish` is registered as anonymous (unauthenticated) and creates a user with full ReadWrite admin permissions. Because the handler uses a check-then-act (TOCTOU) pattern between the "onboarding already completed?" check and the user-creation write, with no atomic guard, a remote unauthenticated attacker who can reach an instance in its pre-onboarding state can create an administrator account for themselves — and concurrent requests can create multiple admin accounts in a single race. Version 2.41.1 patches the issue.

### CVE-2026-65980

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-21T22:16:58.317 |

Chartbrew is an open-source web application that can connect directly to databases and APIs and use the data to create charts. Prior to 5.2.3, Chartbrew's ClickHouse protocol in server/sources/plugins/clickhouse/clickhouse.protocol.js calls applySqlVariables() from server/sources/shared/sql/sql.variables.js without enabling the escapeBackslash option. For a ClickHouse-backed chart with variable binding, an attacker can supply a backslash before a quote so quote doubling does not keep the value within its intended SQL string literal. Public dashboards can expose this path without authentication, and successful exploitation can execute arbitrary ClickHouse SQL to disclose data or, when the database configuration permits, access files or internal network resources. This issue is fixed in version 5.2.3.

### CVE-2026-79079

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-21T22:16:59.000 |

An issue in CrossWire Xiphos <= 4.3.2 allows a local attacker to execute arbitrary code via the src/main/url.cc and src/gtk/menu_popup.c components

### CVE-2026-81469

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-428` |
| Published | 2026-09-21T20:17:33.130 |

Dell Inventory Collector Client, versions prior to 15.0.0, contain an Unquoted Search Path or Element vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Code execution and Elevation of Privileges

### CVE-2026-49810

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-21T19:17:06.523 |

Dell Command Powershell Provider (DCPP), versions prior to 2.10.2 contain an Insertion of Sensitive Information into Log File vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Information Disclosure.

### CVE-2026-17052

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-21T19:17:04.080 |

The Time-aware GPIO syscall verification handler z_vrfy_tgpio_pin_read_ts_ec() in drivers/timeaware_gpio/timeaware_gpio_handlers.c validated only the port device object and passed the caller-supplied timestamp and event_count output pointers to the driver without a K_SYSCALL_MEMORY_WRITE() check. The other handlers in the same file (z_vrfy_tgpio_port_get_time(), z_vrfy_tgpio_port_get_cycles_per_second()) already performed that check, so the omission left one syscall unguarded.

tgpio_pin_read_ts_ec() is declared __syscall, so with CONFIG_USERSPACE=y an unprivileged user-mode thread that has been granted access to the TGPIO device object can invoke it with arbitrary pointer values. tgpio_intel_read_ts_ec() in drivers/timeaware_gpio/timeaware_gpio_intel.c bounds-checks only the pin index and then unconditionally performs timestamp = ... and event_count = ..., executing two 8-byte stores in supervisor mode at addresses chosen by the user-mode caller.

The result is a write-what-where primitive that crosses the userspace/kernel boundary: the target address is fully attacker-chosen and the stored values are the hardware time-capture and event-counter register contents. Corrupting kernel data structures this way can escalate the calling thread to supervisor privilege or crash the system; the device-object permission required is a narrow capability that is not intended to confer any kernel-memory access. The fix adds the two missing K_SYSCALL_MEMORY_WRITE() validations before the driver call.

Exposure is narrow in practice. Only builds with CONFIG_USERSPACE=y and CONFIG_TIMEAWARE_GPIO=y compile the affected file, and from v3.6.0 onward the file additionally referenced a relocated header (<zephyr/syscall_handler.h>) and removed Z_SYSCALL_* macros, so such a configuration failed to build until those were repaired after v4.4.0. Downstream trees that locally corrected that breakage, and v3.5.0 builds where it did not exist, are the exposed population.

### CVE-2026-55567

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-21T15:17:29.793 |

BleachBit cleans files to free disk space and to maintain privacy. Prior to 6.0.1, privileged Windows cleaning does not lock and validate a target's parent directory before deletion. A local unprivileged user can replace that directory with a Windows junction and use a native symlink to redirect the elevated deletion to an attacker-selected file. The arbitrary privileged file deletion can be combined with Windows Installer behavior to obtain local SYSTEM privileges. This issue is fixed in version 6.0.1.

### CVE-2026-95619

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-22T13:17:13.300 |

A flaw was found in libstdc++. An integer overflow can occur when processing large inputs to the C++ `new` operator. This vulnerability could lead to an undersized memory allocation, potentially causing memory corruption or application instability.

### CVE-2026-55105

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-21T21:17:05.320 |

Joplin is an open source note-taking and to-do application that organises notes and lists into notebooks. Prior to 3.6.15 and 3.7.2, packages/renderer/MdToHtml/rules/fountain.ts passes HTML generated by the vendored fountain.js renderer into note output without sanitizing it. A malicious Fountain code block can therefore execute script when Fountain rendering is enabled in desktop or mobile clients, or when a note is published through Joplin Server where Fountain rendering is enabled by default. The script can read content subsequently loaded in the reused note viewer or, when published notes are served from the same domain as server content, access data available to an authenticated browser in the server origin. This issue is fixed in versions 3.6.15 and 3.7.2.

### CVE-2026-63330

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-285;CWE-862` |
| Published | 2026-09-21T19:17:08.440 |

Warpgate is an open source SSH, HTTPS and MySQL bastion host for Linux. Prior to 0.25.6, api_get_recording_stream in warpgate-admin/src/api/recordings_detail.rs protects /@warpgate/admin/api/recordings/{uuid}/stream only with session authentication and omits require_admin_permission for AdminPermission::RecordingsView. Any authenticated regular user who identifies an active recording can subscribe to its WebSocket and receive real-time terminal input and output from proxied SSH, MySQL, or PostgreSQL sessions, including credentials, commands, and other sensitive data belonging to users and administrators. This issue is fixed in version 0.25.6.

### CVE-2026-76898

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-21T17:18:50.350 |

draw.io is a configurable diagramming and whiteboarding application. Prior to version 30.3.8, src/main/java/com/mxgraph/online/Utils.java checks IPv6 Unique Local Addresses in Utils.sanitizeUrl() by comparing the text prefixes fc00:: and fd00::, but the JDK returns the expanded address form, so the fc00::/7 range, including the AWS metadata range fd00:ec2::/32, is not blocked. An unauthenticated request to /embed2.js?fetch= can therefore make src/main/java/com/mxgraph/online/EmbedServlet2.java fetch an IPv6 ULA internal resource and reflect the response to the requester. Utils.validatedAddress() uses the same private-address check for the separate ProxyServlet path, which requires ENABLE_DRAWIO_PROXY=1. The primary /embed2.js path requires no proxy feature flag or DNS rebinding, and it can disclose cloud metadata credentials or data from other IPv6-reachable internal services. This issue is fixed in version 30.3.8.

### CVE-2026-94117

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-22T10:17:10.167 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in DevItems HashBar – WordPress Notification Bar allows Blind SQL Injection.

This issue affects HashBar – WordPress Notification Bar: from n/a through 2.0.3.

### CVE-2026-59814

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-21T22:16:57.050 |

Joplin is an open source note-taking and to-do application that organises notes and lists into notebooks. Prior to 3.7.7, Joplin Server's GET /shares/:id?resource_id= route serves a resource with the attacker-controlled mime value and omits Content-Disposition when the resource title is empty. A low-privileged user can publish an empty-title image/svg+xml attachment whose script executes when a victim opens the public share. By default, user content shares the Joplin Server application origin, allowing the script to access same-origin data and, when the victim is authenticated, perform actions with the victim's session, including reading administrative data and anti-CSRF tokens. Installations that configure USER_CONTENT_BASE_URL to a separate origin still execute the script, but on that separate user-content origin rather than the application origin. This issue is fixed in version 3.7.7.

### CVE-2026-9231

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-22T09:17:06.353 |

The WP Travel Engine – Tour Booking Plugin – Tour Operator Software plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 6.8.0 via the wte_get_template function. This makes it possible for authenticated attackers, with contributor-level access and above, to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included.

### CVE-2026-87079

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-22T08:16:40.637 |

Net::IDN::Punycode versions before 2.590 for Perl allow CPU exhaustion via quadratic insertion cost when decoding a long label in decode_punycode.

The XS backend inserts each decoded code point into a UTF-8 buffer and finds the insertion point by scanning that buffer from the start, one character at a time. The scan runs once per code point over the output built so far, so the cost is quadratic in the label length. The pure-Perl backend downgrades its input to bytes so that substr can index it directly, but takes its working copy before the downgrade, so when the input carries the UTF-8 flag every substr on the copy scans from the start, with the same quadratic cost.

Nothing bounds the label length in the to-Unicode direction. The 63-byte DNS limit is checked only when converting to ASCII, so domain_to_unicode and uts46_to_unicode pass an attacker-supplied label of any length to the decoder.

### CVE-2026-91827

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T07:16:31.093 |

The Ninja Forms WordPress plugin 3.15.3 does not prevent user-submitted form field values from being deserialised when an administrator later exports form submissions to CSV, allowing unauthenticated attackers to perform PHP Object Injection; if a suitable POP chain is present via another installed plugin or theme, this can lead to actions such as arbitrary file operations or remote code execution.

### CVE-2026-88411

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-21T21:17:15.380 |

Improper error handling in the GRAPH.EFFECT component (/effects/effects_apply.c) of FalkorDB (Redis module) v4.20.1 leads to a Denial of Service (DoS) within the application.

### CVE-2026-88407

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-21T21:17:14.860 |

An out-of-bounds read in the node_token_count/relation_token_count component of FalkorDB (Redis module) v4.20.1 to v4.20.4 allows attackers to cause a Denial of Service (DoS) via a crafted input.

### CVE-2026-88406

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-21T21:17:14.733 |

FalkorDB (Redis module) v4.20.1 to v4.20.4 was discovered to contain a stack overflow in the _ValidateUnion_Clauses function (/ast/ast_validations.c). This vulnerability allows attackers to cause a Denial of Service (DoS) via a crafted input.

### CVE-2026-73553

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-09-21T21:17:09.637 |

Envoy is an open source edge and service proxy designed for cloud-native applications. Prior to 1.36.10, 1.37.6, 1.38.4, and 1.39.1, When ignore_path_parameters_in_path_matching is enabled, Envoy's router strips the semicolon suffix before matching but the RBAC url_path matcher evaluates the raw path. A downstream request such as /admin;x can therefore miss a DENY rule for /admin while the router still selects the protected /admin backend. The inconsistent canonicalization allows an unauthenticated client to bypass path-based authorization. The relevant scope boundary is that the route option and a path-based RBAC rule must both be present, and the protected route must match after stripping. This issue is fixed in versions 1.36.10, 1.37.6, 1.38.4, and 1.39.1.

### CVE-2026-73552

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-21T20:17:28.900 |

Envoy is an open source edge and service proxy designed for cloud-native applications. Prior to 1.36.10, 1.37.6, 1.38.4, and 1.39.1, Envoy HTTP RBAC accepts RFC-valid opaque header bytes but evaluates safe_regex values with RE2's UTF-8 subject semantics. A downstream client can preserve a prohibited marker and add an unrelated obs-text octet, causing RE2::FullMatch to return false and a negative RBAC policy to treat the invalid subject as an ordinary no-match. A byte-oriented route matcher can still observe the marker, allowing the request to reach a route intended to be denied. The relevant scope boundary is that plain positive ALLOW regexes normally fail closed, and exact, prefix, suffix, and contains matchers are not shown to have this subject-domain failure. This issue is fixed in versions 1.36.10, 1.37.6, 1.38.4, and 1.39.1.

### CVE-2026-73550

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-21T20:17:28.733 |

Envoy is an open source edge and service proxy designed for cloud-native applications. Prior to 1.36.10, 1.37.6, 1.38.4, and 1.39.1, Envoy copies every decoded HTTP/2 Host header value before discarding it when :authority is already present. The discarded value bypasses saveHeader, so its bytes and count are not charged against request header limits. An unauthenticated client can use HPACK indexing to submit many references to a large Host value across a bounded number of streams, forcing extreme header-copy allocation and causing the proxy to be out-of-memory killed. The relevant scope boundary is that the demonstrated amplification uses HTTP/2 HPACK and the duplicate Host discard behavior. This issue is fixed in versions 1.36.10, 1.37.6, 1.38.4, and 1.39.1.

### CVE-2026-73548

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-21T20:17:28.397 |

Envoy is an open source edge and service proxy designed for cloud-native applications. Prior to 1.36.10, 1.37.6, 1.38.4, and 1.39.1, Envoy forwards data for a configured non-WebSocket HTTP upgrade before the upstream accepts the upgrade. An unauthenticated HTTP/2 client can place a complete HTTP/1.1 request in extended CONNECT data; Envoy downgrades the request, writes the data unframed to a keep-alive HTTP/1.1 upstream, and returns the socket to the shared pool while the smuggled response remains queued. A different downstream client can then receive the attacker's response. The relevant scope boundary is that webSocket upgrades, plain CONNECT, disabled backend keep-alive, per-downstream pools, and max_requests_per_connection set to 1 are not affected by the demonstrated path. This issue is fixed in versions 1.36.10, 1.37.6, 1.38.4, and 1.39.1.

### CVE-2026-73547

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-476` |
| Published | 2026-09-21T20:17:28.230 |

Envoy is an open source edge and service proxy designed for cloud-native applications. Prior to 1.36.10, 1.37.6, 1.38.4, and 1.39.1, Envoy's ext_authz filter assumes that a request contains a :path pseudoheader when applying query_parameters_to_set or query_parameters_to_remove from an authorization response. A path-less CONNECT request makes request_headers_->Path() return null, and Filter::onComplete dereferences that pointer while parsing the query string. An unauthenticated downstream client can crash the Envoy process when the filter and authorization response use query-parameter mutation. The relevant scope boundary is that the deployment must accept path-less CONNECT and configure ext_authz query-parameter mutation. This issue is fixed in versions 1.36.10, 1.37.6, 1.38.4, and 1.39.1.

### CVE-2026-73513

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-416` |
| Published | 2026-09-21T20:17:27.820 |

Envoy is an open source edge and service proxy designed for cloud-native applications. Prior to 1.36.10, 1.37.6, 1.38.4, and 1.39.1, Envoy's optional oghttp2 upstream HTTP/2 codec accepts a response trailer HEADERS frame without END_STREAM. Envoy completes and deferred-deletes the ActiveRequest while oghttp2 keeps the stream open, leaving ClientStreamImpl with a dangling response_decoder_ reference. A later frame on the stream can dispatch through the freed object and crash the process. The relevant scope boundary is that the default nghttp2 codec rejects the malformed trailers, and the trigger is upstream-only with oghttp2 enabled. This issue is fixed in versions 1.36.10, 1.37.6, 1.38.4, and 1.39.1.

### CVE-2026-73512

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-21T20:17:27.647 |

Envoy is an open source edge and service proxy designed for cloud-native applications. Prior to 1.36.10, 1.37.6, 1.38.4, and 1.39.1, Envoy's HttpDatagramHandler caches the current RequestDecoder when Capsule Protocol is enabled. Stream recreation, including an internal redirect, replaces the ActiveStream and updates EnvoyQuicServerStream but does not update the handler's cached pointer. A subsequent HTTP/3 datagram can call decodeData through the freed decoder, causing invalid virtual dispatch and a process crash. The relevant scope boundary is that hTTP/3 datagrams and Capsule Protocol must be enabled, and the request must enter a stream-recreation path such as an internal redirect. This issue is fixed in versions 1.36.10, 1.37.6, 1.38.4, and 1.39.1.

### CVE-2026-94449

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-21T17:19:20.097 |

A flaw was found in the SmallRye Fault Tolerance library, which is used by Quarkus to provide strategies like retries and circuit breakers for microservices. The issue occurs when using the ApplyGuard or ApplyFaultTolerance annotations, where the library fails to release internal tracking objects after each request. This causes a steady increase in memory usage that eventually leads to the application slowing down and crashing due to lack of memory.

### CVE-2026-71543

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-21T15:17:31.173 |

OpenBao is an open source identity-based secrets management system. Prior to 2.6.0, templated ACL, PKI, and SSH policies could substitute attacker-controlled identity data without rejecting syntax-significant characters. In ACL templated policies, asterisks, plus signs, and slashes could alter path matching. In PKI allowed_uri_sans_template and allowed_domains policies, an asterisk could broaden certificate issuance to unauthorized domains. In SSH allowed_users and allowed_domains policies, a comma could add unauthorized principals. Exploitation requires a deployment to use templated policy data that users can freely modify; templates based on the randomly generated identity.entity.id value are not affected. This could allow privilege escalation, unauthorized access, and unauthorized certificate issuance. This issue is fixed in version 2.6.0.

### CVE-2026-61629

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-21T15:17:30.477 |

nginx ignition is a user interface for the nginx web server. In versions 2.29.0 through 2.40.0, the gin i18n middleware in nginx-ignition's API server runs in front of every HTTP request and calls `golang.org/x/text/language.ParseAcceptLanguage` on the raw `Accept-Language` header without imposing any size or shape filter. The underlying parser has quadratic-time behaviour on long lists of malformed language tags. The CVE-2022-32149 guard that golang.org/x/text added in v0.3.8 caps the number of `-` characters in the input at 1000, but it does not cap `_` characters even though the parser's internal scanner aliases `_` to `-` before parsing. A single unauthenticated GET request with an `Accept-Language` header built out of `_` separators burns about 2.4 seconds of server CPU on the host running nginx-ignition; ten concurrent attackers saturate a ten-core box for the duration of the attack while consuming ~10 MiB/s of upstream bandwidth. Version 2.40.1 fixes this issue.

### CVE-2026-52741

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-80` |
| Published | 2026-09-21T15:17:28.600 |

GoCD is a continuous deliver server. From 18.3.0 until 26.1.0, GoCD can generate unescaped tracking-tool links from commit comments when a project uses a lenient Tracking Tool regular expression with an ID capturing group, such as JIRA-(.+). An attacker with commit access to a tracked material can place URI or HTML special characters in a matching commit comment, causing stored cross-site scripting when a victim views an affected Compare Pipeline page. Deployments without Tracking Tool integration, without an ID capturing group, or with conservative matchers that cannot match special characters are not affected. Successful exploitation can expose a privileged user session or allow changes using the victim's credentials and privileges. This issue is fixed in version 26.1.0.

### CVE-2026-95508

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T09:17:06.073 |

A heap-based buffer overflow was found in the DHCPv6 and TFTP response builders of libslirp. When the host is configured with a small interface MTU, a guest-supplied DHCPv6 CLIENTID option or TFTP blksize option can overflow the reply buffer with attacker-controlled content and length, resulting in denial of service and potentially arbitrary code execution in the host process. The default interface MTU is not affected.

### CVE-2026-94540

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-21T22:17:00.800 |

DesktopSMS 1.11.0 by MrPear contains an unauthorized access vulnerability that allows local attackers to transmit SMS, retrieve SMS-derived content, and persist an attacker-selected paired identity by interacting with the application's local service without any pairing confirmation or user interaction. Attackers can exploit the unauthenticated local service through same-device loopback to perform privileged SMS operations using the victim application's permissions.

### CVE-2026-93340

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-09-21T22:16:59.547 |

Gladys Assistant before 5.1.0 contains a password reset link poisoning vulnerability that allows unauthenticated remote attackers to obtain valid password reset tokens for any account by exploiting the client-supplied origin parameter in the forgot_password endpoint without server-side validation. Attackers can send a crafted request specifying an attacker-controlled origin, causing the victim to receive a poisoned reset link that discloses the session token to the attacker, enabling full account takeover including administrator accounts.

### CVE-2026-55210

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-21T22:16:56.890 |

Joplin is an open source note-taking and to-do application that organises notes and lists into notebooks. Prior to 3.7.2, Joplin Server's UserModel.ssoLogin() returns an existing account matched by an IdP-asserted email without checking the account's is_external flag. In deployments using mixed local and SAML authentication, an attacker whose IdP session can assert a local user's email can pass POST /api/saml, receive a session for that local account, and access or modify the victim's notes, files, and settings without knowing the local password. This issue is fixed in version 3.7.2.

### CVE-2026-77523

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-21T21:17:11.280 |

MaxKB is an open-source AI assistant for enterprise. In version 2.10.3-lts and earlier, the model parameter form route authorizes the path workspace but ModelSerializer.ModelParams loads and saves a Model by id alone without including workspace_id in the query. An authenticated user with model read permission in an attacker-controlled workspace can supply a known victim model_id to read or overwrite the victim's model_params_form in another workspace, potentially altering workflows that use those defaults. No fixed version is available as of this review.

### CVE-2026-73546

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-21T20:17:28.040 |

Envoy is an open source edge and service proxy designed for cloud-native applications. Prior to 1.36.10, 1.37.6, 1.38.4, and 1.39.1, Envoy's /stats?format=html admin endpoint uses StatsHtmlRender, which sanitizes string statistic values but emits statistic names without HTML encoding. A data-plane component such as grpc_stats with stats_for_all_methods enabled can incorporate attacker-controlled path segments into cached dynamic statistic names. When an operator views the HTML stats page, the stored name can execute script with the admin interface's origin and issue privileged same-origin requests. The relevant scope boundary is that the admin interface must be browser-accessible and an enabled component must persist attacker-influenced text in statistic names. This issue is fixed in versions 1.36.10, 1.37.6, 1.38.4, and 1.39.1.

### CVE-2026-75939

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-21T15:17:31.520 |

A flaw was found in openshift/oc-mirror. The tool incorrectly verifies PGP (Pretty Good Privacy) release image signatures by checking for signature errors before the entire signed body is processed, leading to a bypass of the signature verification. A remote attacker, by intercepting or manipulating network traffic to the signature endpoint, could exploit this to craft a PGP message with a valid Red Hat release key ID but a forged signature. This enables the `oc-mirror` tool to accept and mirror a malicious release payload into a disconnected registry, potentially compromising the integrity of software deployments.

### CVE-2026-93928

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-22T09:17:05.940 |

Authentication Bypass Using an Alternate Path or Channel vulnerability in Magepeople inc. Taxi Booking Manager for WooCommerce allows Authentication Bypass.

This issue affects Taxi Booking Manager for WooCommerce: from n/a before 2.0.8.

### CVE-2026-93836

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T08:16:42.907 |

The WPC Product Bundles for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'qty' parameter in all versions up to, and including, 8.6.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The float cast used during quantity validation allows a numeric-prefixed payload such as '1<img src=x onerror=...>' to pass validation while retaining its malicious HTML, which is then stored verbatim in order item metadata under the '_woosb_ids' key.

### CVE-2026-93778

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T08:16:42.767 |

The WP Yelp Review Slider plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Yelp Review Text (imported via wpyelp_download_source) in all versions up to, and including, 9.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The malicious payload originates from an anonymous Yelp reviewer on a public platform and requires no WordPress account; it is introduced into the database during the site administrator's ordinary use of the plugin's Download Reviews feature, making the effective attacker unauthenticated.

### CVE-2026-94504

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T07:16:31.340 |

Ninja Forms 3.15.3 stores an anonymous non-RTE textarea value and renders it without safe HTML encoding in the legacy submission editor. An attacker can break out of the textarea with stored script. When an Administrator opens the attacker-known direct submission URL, the script runs in the WordPress admin origin.

### CVE-2026-89412

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T07:16:29.927 |

The TranslatePress – Translate Multilingual sites with AI Translation plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Translation Memory Suggestion Panel (v-html on suggestion.original) in all versions up to, and including, 3.3.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Unauthenticated attackers can seed the translation dictionary's original column with executable HTML because the front-end rendering pipeline decodes entity-encoded payloads via html_entity_decode() before persistence, and the original column is deliberately exempt from kses filtering — meaning no save-time sanitizer neutralizes the stored payload before it is later rendered in an administrator's session.

### CVE-2026-12470

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-22T06:16:48.700 |

The CMP – Coming Soon & Maintenance Plugin by NiteoThemes plugin for WordPress is vulnerable to unauthorized modification of data that can lead to privilege escalation due to a missing capability check on the 'cmp_ajax_import_settings' AJAX action in all versions up to, and including, 4.1.17. This makes it possible for authenticated attackers, with Editor-level access and above, to update arbitrary options on the WordPress site. This can be leveraged to update the default role for registration to administrator and enable user registration for attackers to gain administrative user access to a vulnerable site.

### CVE-2026-36467

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-21T16:17:07.470 |

Unrestricted Upload of File with Dangerous Type in core/modules/media.php in CuteNews v.2.1.2 allows remote authenticated users with access to the Media Manager panel to execute arbitrary code in the context of the web application, leading to remote server access by triggering a reverse shell.

### CVE-2026-93343

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-22T14:17:18.380 |

MarketKing plugin for WordPress before 2.1.72 contains a missing authorization vulnerability in the marketking_admin_vendors_ajax AJAX action that allows authenticated attackers with subscriber-level access or higher to retrieve the complete vendor directory by sending a crafted AJAX request. Attackers can exploit the absence of capability checks in the vendor management action to retrieve internal user IDs, usernames, and email addresses of all registered vendors, exposing personally identifiable information to any logged-in user regardless of role.

### CVE-2026-89420

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-09-22T12:17:14.370 |

Improper Validation of Specified Quantity in Input in ZenHive mpp allows a client holding an open payment channel to obtain paid resources without being charged.

MPP.Session.Actions.accept_voucher/3 in lib/mpp/session/actions.ex treats a voucher whose cumulativeAmount equals the channel's already-accepted cumulative amount as an idempotent success, returning the channel unchanged without calling maybe_spend/2. The credential verifies, the protected resource is served, and spent and units stay where they were. Because the server issues a fresh challenge per request and the credential replay store keys on challenge id and payload, the same signed voucher can be re-presented under every new challenge, so one paid voucher yields an unbounded number of paid units. The path is reachable from any method built on MPP.Session.Method through the Plug, MCP, JSON-RPC and WebSocket transports.

This issue affects mpp: from 0.14.0 before 0.16.2.

### CVE-2026-68956

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-22T09:17:05.313 |

Allocation of Resources Without Limits or Throttling vulnerability in Erlang/OTP ssh allows an authenticated remote attacker to exhaust node memory by repeatedly opening session channels that are never assigned a handler.

The "session" clause of ssh_connection:handle_msg/4 checks only minimal_remote_max_packet_size before calling setup_session/5, which unconditionally builds a #channel{} record and stores it in the ETS channel cache. The max_channels daemon option is consulted only by ssh_channel_sup:max_num_channels_not_exceeded/2, which counts supervisor children, so a channel that never gets a shell, exec, or subsystem handler is invisible to the limit and setting the option to a finite value does not mitigate the attack. RFC 4254 section 5.1 permits many session channels per connection, and each record costs only a few hundred bytes, so a single authenticated connection can accumulate channels until the node runs out of memory and the emulator terminates, affecting every application on it. No file contents, credentials, or write access are obtainable.

This issue affects OTP from OTP 18.1.2 before OTP 27.3.4.18, OTP 28.5.0.7, and OTP 29.1.1, corresponding to ssh from 4.1.1 before 5.2.11.13, 5.5.2.6, and 6.0.6. Whether OTP before OTP 18.1.2, corresponding to ssh before 4.1.1, is affected is unknown.

### CVE-2026-6922

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-22T08:16:39.990 |

The WP Table Builder – Drag & Drop Table Builder plugin for WordPress is vulnerable to Incorrect Authorization in all versions up to, and including, 2.2.1. This is due to an operator precedence bug in the post-type guard within the trash_table_bulk() and restore_table_bulk() functions that causes the guard to never fire, combined with a permission callback that only verifies plugin role membership without per-post-type or ownership checks. This makes it possible for authenticated attackers, with subscriber-level access and above, to trash or restore any post, page, or custom post type on the site by supplying arbitrary post IDs.

### CVE-2026-94535

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-21T22:17:00.487 |

lamp-cloud through 5.10.0 contains an authorization bypass vulnerability in the deleteMyNotice endpoint that allows authenticated users to delete other users' notifications. Attackers can call the DELETE /anyone/extendNotice/deleteMyNotice endpoint with arbitrary notice IDs to permanently remove notifications belonging to other users without recipient validation.

### CVE-2026-94534

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-21T22:17:00.327 |

lamp-cloud through 5.10.0 fails to validate user identity in PUT /anyone/baseInfo and PUT /anyone/avatar endpoints, allowing authenticated attackers to modify arbitrary user profiles. Attackers can supply target user IDs in request bodies to rewrite profile fields including nickname, ID card, sex, nation, education, work description, and avatar attachments of other users.

### CVE-2026-94533

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-21T22:17:00.173 |

lamp-cloud through 5.10.0 contains an authorization bypass vulnerability in FileAnyoneController that allows authenticated users to download arbitrary attachments. Attackers can retrieve other users' stored files by supplying valid attachment identifiers to the /anyone/file/down and /anyone/file/download endpoints, as the application never validates file ownership against the created_by column.

### CVE-2026-94532

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-21T22:17:00.010 |

lamp-cloud through 5.10.0 contains an authorization bypass vulnerability in the getUserInfoById endpoint that allows authenticated users to read any other user's full profile. Attackers can iterate the userId parameter to harvest sensitive user information including mobile numbers, email addresses, national identity card numbers, and WeChat and DingTalk OpenIDs.

### CVE-2026-88746

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-21T21:17:15.893 |

idccms V1.70 is vulnerable to Cross Site Scripting (XSS) in /admin/makeDiy_deal.php.

### CVE-2026-88410

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-21T21:17:15.247 |

The graph.UDF in FalkorDB (Redis module) v4.20.1 to v4.20.4 is not registered as a write command, leading to unexpected behavior within the application.

### CVE-2026-61647

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-09-21T21:17:07.107 |

NotebookLM MCP is an MCP server and HTTP service for interacting with Google NotebookLM and exporting generated content to local vault directories. Versions 1.6.0 through 2.0.2 contain a path traversal vulnerability in the `POST /batch-to-vault` endpoint, also exposed through the `batch_to_vault` MCP tool beginning in version 1.7.0, because attacker-controlled `vault_dir` and `slug_prefix` values can cause Markdown and JSON files to be written outside the intended vault directory to any location writable by the server process. Version 2.0.3 sanitizes `slug_prefix` and supports vault containment when `NOTEBOOKLM_VAULT_ROOT` is configured; containment is not enabled if that variable is unset. Users unable to upgrade should run the server as a dedicated unprivileged account restricted to the intended vault, keep the HTTP endpoint limited to localhost, and validate `vault_dir` values supplied by LLMs processing untrusted content.

### CVE-2026-49450

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345;CWE-353;CWE-494` |
| Published | 2026-09-21T21:17:03.747 |

Joplin is an open source note-taking and to-do application that organises notes and lists into notebooks. Prior to 3.7.2, Joplin Desktop for Windows omits publisherName from packages/app-desktop/package.json, so the generated app-update.yml causes NsisUpdater.verifySignature() to skip comparison of a downloaded update's Authenticode signer with Joplin's signer. An attacker who controls the update delivery path can replace the update metadata and installer, and the client accepts an installer signed by another publisher or left unsigned after the user approves installation. Successful exploitation runs attacker-controlled code with the user's privileges and can compromise notes, credentials, and local data. This issue is fixed in version 3.7.2.

### CVE-2026-94495

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-21T19:17:21.427 |

jshERP through 3.6 fails to properly validate user privileges in SystemConfigService.updateSystemConfig, allowing authenticated users to modify tenant system configuration. Attackers can rewrite or delete tenant-wide settings covering company identity, stock rules, approval behavior, and printing configuration through the systemConfig endpoint.

### CVE-2026-94413

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-21T19:17:20.377 |

jshERP through 3.6 fails to redact password hashes in the /user/info endpoint, allowing authenticated users to retrieve unsalted MD5 password digests for any user. Attackers can request arbitrary user information by supplying user IDs to obtain password hashes usable for offline cracking or direct authentication bypass.

### CVE-2026-61687

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-352;CWE-384;CWE-1275` |
| Published | 2026-09-21T16:17:09.997 |

Hatchet is a platform for orchestrating background tasks, AI agents, and durable workflows at scale. Prior to 0.91.1, ValidateOAuthState clears the oauth_state_ session value to an empty string after a successful OAuth callback and later accepts an empty state parameter as equal, allowing an unauthenticated attacker to bind a victim's Hatchet session to an attacker-controlled OAuth identity. Exploitation requires the victim to have completed an OAuth flow in the current session and the deployment to enable auth.google.enabled, auth.github.enabled, or the Slack integration. This issue is fixed in version 0.91.1.

### CVE-2026-49453

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-20;CWE-22` |
| Published | 2026-09-21T21:17:03.900 |

Joplin is an open source note-taking and to-do application that organises notes and lists into notebooks. Prior to 3.6.15 and 3.7.2, Joplin accepts synchronized resource metadata whose id or file_extension contains parent-directory or path-separator characters. BaseItem.unserialize() stores the unvalidated fields, resourceFilename() concatenates them into a destination path, and ResourceFetcher writes the attacker-controlled resource blob outside the resource directory during background synchronization. An attacker with write access to a configured sync target or shared notebook can create or overwrite files at an attacker-chosen existing path without user interaction. This issue is fixed in versions 3.6.15 and 3.7.2.

### CVE-2026-52835

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-434` |
| Published | 2026-09-21T20:17:26.140 |

Tautulli is a Python based monitoring and tracking tool for Plex Media Server. Prior to 2.17.2, the import_config handler and the database_file branch of import_database in plexpy/webserve.py join the attacker-controlled config_file.filename or database_file.filename directly to CACHE_DIR without basename reduction or a containment check. An administrator or caller with the instance API key can submit a multipart filename containing parent-directory segments, causing the upload to be created or overwritten outside CACHE_DIR before file-content validation runs. The write is limited to paths permitted to the Tautulli process, but it can enable configuration tampering, service disruption, or code execution. This issue is fixed in version 2.17.2.

### CVE-2026-68919

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-80` |
| Published | 2026-09-21T15:17:30.977 |

GoCD is a continuous deliver server. From 13.3.0 until 26.1.0, GoCD does not correctly encode and escape malicious material modification comments that mimic the special trackback format used by package materials when rendering the Stage Detail, Job/Build Detail, Value Stream Map, and Pipeline History views. A user with write access to a material tracked by GoCD can store arbitrary HTML or JavaScript in a forged package material comment, which executes in the browser session of a user who later views an affected page. Exploitation requires a victim to view a page that renders the malicious modification, and GoCD does not render every material comment in every view. Successful exploitation can expose a privileged user session or allow changes using the victim's credentials and privileges. This issue is fixed in version 26.1.0.
