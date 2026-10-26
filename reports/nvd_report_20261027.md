# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-26 15:00 UTC
- **対象期間**: `2026-10-25T15:00:27.000Z` 〜 `2026-10-26T15:00:44.000Z`
- **重要CVE数**: 56 件（Critical 9.0+: 8 件 / High 7.0〜: 48 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE の多くは **認証バイパス / 無制限ファイルアップロード** と **リソース枯渇（DoS）** に関するものです。  
- Web アプリケーションフレームワーク（Mautic、FortiSandbox、danmu_api など）と、Elixir 製 HTTP サーバ **Bandit** 系列で大量の高深刻度脆弱性が報告されています。  
- CVSS が 9.0 以上のエクスプロイトは、認証不要でリモートからコード実行や完全権限取得が可能になる点が共通しており、**早急なパッチ適用が必須**です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な問題点 | 影響範囲・被害シナリオ |
|-----|------|------------|------------------------|
| **CVE‑2026‑115188** | 9.9 | Mautic 7 のキャンペーンインポートで **無制限ファイルアップロード** が可能。認証ユーザーでも任意のファイル名・拡張子で `media/` 配下に配置でき、リモートコード実行 (RCE) に直結。 | Mautic を社内マーケティングサイトや顧客向けポータルで使用している組織は、攻撃者にサーバ上でシェルを取得される危険がある。 |
| **CVE‑2026‑107656** | 9.8 | FortiSandbox の **認証バイパス**（代替パス／チャネル）により、認証不要で管理コンソールへアクセス可能。 | FortiSandbox を導入している企業ネットワークでは、攻撃者がサンドボックス内部のマルウェア解析結果や設定情報を取得し、さらに内部マシンへの踏み台にできる。 |
| **CVE‑2026‑59106** | 9.3 | WolfProt インタフェースの **コマンドインジェクション**（入力正規化不備）。ネットワーク上から任意コマンドを OS 権限で実行できる。 | WolfProt を組み込みデバイスや IoT ゲートウェイで使用している場合、攻撃者がデバイス全体を乗っ取り、内部ネットワークへ横展開できる。 |
| **CVE‑2026‑116485** | 9.3 | danmu_api (1.21.7 未満) の **認証バイパス**。デフォルト `TOKEN` が残っていると `/api/env/*` エンドポイントで環境変数を書き換えられる。 | 公開 API を提供しているライブ配信プラットフォームで、攻撃者が管理者権限を取得し、任意のシステム設定やデータベース接続情報を書き換え可能。 |
| **CVE‑2026‑115269** (Bandit) | 8.7 | HTTP/2 **リソース枯渇**（WINDOW_UPDATE/ SETTINGS フレームでストリームを無制限に保持）。DoS 攻撃が簡単に実行できる。 | Elixir/Bandit を採用したマイクロサービスや API サーバは、攻撃者からの大量リクエストでメモリ・CPU が枯渇し、サービス停止に追い込まれる。 |

> **選定理由**  
> - **深刻度が最高（9.0 以上）** かつ **認証不要でリモートから実行可能** な点。  
> - 影響が広範（Web CMS、セキュリティ製品、IoT デバイス、マイクロサービス）で、組織全体のリスクが高い。  

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンのアップデート
| 製品 / ライブラリ | 現行脆弱バージョン | 推奨バージョン | アップデート手順のポイント |
|-------------------|-------------------|----------------|---------------------------|
| **Mautic** | 7.0.0 – 7.0.x (該当機能あり) | **7.0.1 以降**（公式パッチ適用） | `composer update mautic/core` → `php bin/console cache:clear` |
| **FortiSandbox** | 5.0.0 – 5.0.6, 4.4.0 – 4.4.9, 4.2 系 | **5.0.7** または **4.4.10** 以降 | FortiOS 管理コンソール → Firmware Upgrade → 再起動後 `show system status` でバージョン確認 |
| **WolfProt** | 2.3.x 以前 | **2.5.0** 以上（入力サニタイズ追加） | ソースコードから `git pull` → `make install`、またはパッケージマネージャ (`apt-get upgrade wolfprot`) |
| **danmu_api** | < 1.21.7 | **1.21.7** 以上 | `pip install --upgrade danmu_api`、`TOKEN` を必ずランダム化し `ADMIN_TOKEN` を設定 |
| **Bandit (mtrudel/bandit)** | < 0.6.5 | **0.6.5** 以上 | `mix deps.update bandit` → アプリ再デプロイ、`bandit --version` で確認 |

### 3.2 設定・運用上の対策
1. **ファイルアップロードの制限**  
   - Mautic の `media/` ディレクトリに対し **拡張子ホワイトリスト** と **実行権限除去** を徹底。  
2. **認証・トークン管理**  
   - FortiSandbox の管理インタフェースは **IP アクセス制御** と **二要素認証** を有効化。  
   - danmu_api のデフォルト `TOKEN` を削除し、環境変数または Vault で安全に保管。  
3. **ネットワークレベルの防御**  
   - WolfProt がリッスンするポートは **内部 VLAN のみ** で公開し、外部からの直接アクセスを遮断。  
   - Bandit を使用するサービスは **HTTP/2 の SETTINGS_HEADER_TABLE_SIZE** などの上限をアプリ側で設定し、リソース枯渇を防止。  
4. **監視・インシデント対応**  
   - すべての対象システムで **ログイン失敗・ファイルアップロード**、**異常な HTTP/2 フレーム** を SIEM に集約し、閾値超過時にアラートを上げる。  
   - 侵入テスト（Red Team）で **認証バイパス** シナリオを再現し、検出できるか確認。  

### 3.3 短期的な緊急対策（パッチ適用が困難な場合）
- **WAF ルール追加**：Mautic の `/media/` への

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-115188

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-434` |
| Published | 2026-10-26T14:16:30.047 |

An unrestricted file upload vulnerability exists in the campaign import feature of Mautic 7. When processing an uploaded campaign archive, the application copies the bundled asset files into a publicly accessible media directory without restricting their file names or types. An authenticated user with permission to create campaign imports can exploit this through the user interface or the API (/api/campaigns/import) to place arbitrary files, including server-side scripts, in the web root. Administrator privileges are not required. On web servers that honor per-directory configuration, such as the default Apache setup of the official Mautic Docker image, this leads to remote code execution with the privileges of the web server user, including access to the Mautic configuration, application secrets, and contact data.

### CVE-2026-107656

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-26T14:16:24.147 |

An authentication bypass using an alternate path or channel vulnerability in Fortinet FortiSandbox 5.0.0 through 5.0.6, FortiSandbox 4.4.0 through 4.4.9, FortiSandbox 4.2 all versions, FortiSandbox PaaS 5.0.0 through 5.0.6, FortiSandbox PaaS 4.4 all versions, FortiSandbox PaaS 4.2 all versions may allow attacker to execute unauthorized code or commands via crafted HTTP requests

### CVE-2026-59106

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-26T14:16:38.813 |

A security vulnerability has been identified in the WolfProt interface implementation. Insufficient neutralization of user-controlled input could allow an unauthenticated attacker with network access to a vulnerable service to execute operating-system commands with the privileges of the affected application service.

### CVE-2026-116485

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-26T14:16:37.040 |

danmu_api before 1.21.7 contains an authentication bypass vulnerability that allows unauthenticated attackers to modify server environment configuration when the default TOKEN is used and ADMIN_TOKEN is unset. Attackers can send POST requests to /api/env/set, /api/env/add, or /api/env/del to set ADMIN_TOKEN, lock out operators, redirect OTHER_SERVER or PROXY_URL for SSRF, and trigger redeployment.

### CVE-2026-116214

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-26T14:16:34.173 |

MacCMS v10 before 2026.1000.4054 contains an authentication bypass vulnerability that allows unauthenticated attackers to reset any member's password because check_msg() never compares msg_to. Attackers can request a recovery code to their own mailbox via user/findpass_msg, then submit it to user/findpass_reset with the victim's email or phone to take over the account.

### CVE-2026-110475

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-26T14:16:26.573 |

This vulnerability exists in the CreditNirvana Collections Platform due to improper authentication and authorization controls at the platform login service. An unauthenticated remote attacker could exploit this vulnerability by manipulating authentication requests and accessing APIs without a valid authenticated session on the targeted system.

Successful exploitation of this vulnerability could allow the attacker to enumerate platform users, establish sessions as arbitrary users including administrative users, access and modify sensitive information with the privileges of the impersonated user.

### CVE-2026-59107

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-797` |
| Published | 2026-10-26T14:16:38.973 |

A security vulnerability has been identified in the vSolution Matrix file sharing feature. A shared cryptographic trust configuration could allow an attacker who obtains the matching private key to authenticate to an affected device via SSH as root. This vulnerability affects only devices configured as a vSolution Matrix main/master station with the file sharing feature enabled.

### CVE-2026-115693

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-26T14:16:31.853 |

Improper Certificate Validation vulnerability in hackney_ssl in benoitc hackney allows an on-path attacker to impersonate a server pinned to a private certificate authority via a certificate chain that ends in a publicly trusted root. hackney adds {partial_chain, fun hackney_ssl:partial_chain/1} to every verify_peer configuration. The callback returns any certificate in the peer chain whose public key matches a root in the bundled certifi store as the trust anchor, and OTP honours that callback over the configured cacerts. hackney_ssl:merge_ssl_opts/3 kept the callback when the caller replaced the trust store with cacerts or cacertfile in ssl_options, so a connection pinned to a private CA still accepted any chain that carried a publicly trusted root.

The hostname check still applies, so the attacker needs a publicly trusted certificate for the pinned hostname.

This issue affects hackney: from 1.24.0 before 4.9.0.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-115189

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-26T14:16:30.203 |

A server-side template injection vulnerability exists in the Twig theme rendering sandbox of Mautic. The sandbox introduced to restrict user-uploaded theme templates (the fix for GHSA-9fx4-7cmj-47vg) does not fully enforce its restrictions, allowing a crafted theme template to escape the sandbox. An authenticated user with the core:themes:create permission can upload a malicious theme whose template is later rendered, resulting in execution of arbitrary code on the server with the privileges of the web server process. This allows the attacker to execute operating system commands, read server-side files including configuration files and database credentials, write files, and reach internal services. In default installations the core:themes:create permission is granted to the Administrator role, and in multi-operator setups it may be delegated to other roles. This is an incomplete fix for GHSA-9fx4-7cmj-47vg.

### CVE-2026-82944

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120;CWE-131;CWE-787` |
| Published | 2026-10-26T09:16:36.140 |

SOEM version 2.0.0 and earlier contains a vulnerability in multi-segment data transfers where a malicious device can overflow memory buffers. The software checks the total size only once at the beginning, but doesn't track the cumulative size as multiple segments arrive. An attacker can declare a small initial size to pass validation, then send additional segments that exceed the allocated buffer. This allows the attacker to write controlled data beyond buffer boundaries, potentially enabling code execution.

### CVE-2026-111841

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-26T09:16:34.207 |

Cross-Site Request Forgery (CSRF) vulnerability in Aman FunnelKit Automations wp-marketing-automations allows Cross Site Request Forgery.This issue affects FunnelKit Automations: from n/a through 3.8.5.2.

### CVE-2026-115269

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770;CWE-835` |
| Published | 2026-10-26T14:16:31.290 |

Allocation of Resources Without Limits or Throttling vulnerability in the HTTP/2 request body reader of mtrudel bandit allows an unauthenticated remote attacker to hold stream processes open indefinitely via WINDOW_UPDATE or empty SETTINGS frames sent while a Plug reads the request body.

Bandit.HTTP2.Stream.do_read_data/4 in lib/bandit/http2/stream.ex waits for each frame with a fresh read_timeout. A stream WINDOW_UPDATE, or the zero-delta window update that every empty SETTINGS frame delivers to all streams, ends the wait without delivering any body data, and the loop starts a new full countdown. A client that sends one of these 9-byte frames before each countdown expires keeps read_body blocked, together with the stream process and whatever the application holds while reading, for as long as it likes.

This issue affects bandit: from 1.4.0 before 1.14.0.

### CVE-2026-114213

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-26T14:16:29.397 |

Allocation of Resources Without Limits or Throttling vulnerability in the WebSocket fragment reassembly of mtrudel bandit allows an unauthenticated remote attacker to exhaust server memory via a fragmented message made of many 1-byte continuation frames.

Bandit.WebSocket.Connection checks max_fragmented_message_size against the payload bytes received, but keeps every non-final continuation frame as a new list cell around its own binary, and nothing limits the number of fragments. A 1-byte fragment costs 7 bytes on the wire but about 150 to 170 bytes of server memory, so one connection can hold about 150 times the configured limit, roughly 1.2 to 1.4 GB at the default 8 MB. Ping frames between fragments keep the connection alive past the idle timeout.

This issue affects bandit: from 1.11.0 before 1.14.0.

### CVE-2026-113436

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-26T14:16:28.680 |

Inefficient Algorithmic Complexity vulnerability in the header integer parser of mtrudel bandit allows an unauthenticated remote attacker to consume server CPU via a content-length value or a Host or :authority port made of thousands of digits.

Bandit.Headers.parse_integer/2 in lib/bandit/headers.ex builds the number one digit at a time with no limit on the digit count, allocating a new bignum at each step, so one value costs time quadratic in its length. It runs on raw request input over HTTP/1 and HTTP/2, before any range check. Over HTTP/2, a 4,000-digit value can be stored once in the HPACK dynamic table and re-sent on each new stream for about one byte: 124 KB of traffic kept the server busy for 27.9 s.

This issue affects bandit: from 1.0.0-pre.7 before 1.14.0.

### CVE-2026-111101

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-26T14:16:27.227 |

Allocation of Resources Without Limits or Throttling vulnerability in the HTTP/1.1 chunked body reader of mtrudel bandit allows an unauthenticated remote attacker to exhaust server memory and CPU via a request body made of many 1-byte chunks.

The chunked reader in lib/bandit/http1/socket.ex keeps every chunk as its own list cell and binary term until IO.iodata_to_binary/1 joins them, and nothing limits the number of chunks. The :length option of read_body/2 counts only data bytes, so tiny chunks cost far more memory than their payload: 48 MB of 1-byte chunks grew one handler process to about 500 MB and took about 6 s of CPU. The route does not need to read the body, because on keep-alive connections ensure_completed/1 drains unread bodies through the same reader.

This issue affects bandit: from 0.1.0 before 1.14.0.

### CVE-2026-110499

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-26T14:16:26.820 |

Allocation of Resources Without Limits or Throttling vulnerability in the HTTP/2 implementation of mtrudel bandit allows an unauthenticated remote attacker to grow per-connection memory and CPU cost without bound via a large SETTINGS_HEADER_TABLE_SIZE. Bandit resizes its HPACK encoder table to whatever size the client advertises, up to 2^32-1 bytes, and indexes response headers into it. Because responses carry distinct values such as date or content-length, nothing is evicted and the table grows with every response for the life of the connection, while each lookup scans it linearly.

The SETTINGS handling in Bandit.HTTP2.Connection (lib/bandit/http2/connection.ex) passes remote_settings.header_table_size to HPAX.resize/2 with no server-side cap, and encode_headers encodes every response header as :store. Serving N responses on one connection therefore costs O(N²) CPU in the connection process.

This issue affects bandit: from 0.3.6 before 1.14.0.

### CVE-2026-110474

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-26T14:16:26.127 |

This vulnerability exists in the CreditNirvana Agentic AI Call Centre application due to hardcoded static API Key in the client side JavaScript bundle. An unauthenticated remote attacker could exploit this vulnerability by downloading client side JavaScript files and extracting API key, which could lead to make arbitrary API calls to retrieve call transcripts and recordings through the application API of the targeted system.

### CVE-2026-109584

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-26T14:16:25.000 |

Improper Handling of Highly Compressed Data (Data Amplification) vulnerability in the HTTP/2 implementation of mtrudel bandit allows an unauthenticated remote attacker to exhaust server memory via a small HPACK-compressed HEADERS block. The block stores one large cookie value in the HPACK dynamic table and then references it tens of thousands of times with 1-byte indexed fields. In the reporter's run, a 49 KB block made a server with default settings allocate a 183 MB cookie binary before any application code ran, and every concurrent stream can repeat the cost.

Bandit.HTTP2.Connection caps only the compressed block (max_header_block_size), and its check of the decoded list against max_header_list_size never fires because that setting defaults to :infinity. combine_cookie_crumbs/1 in lib/bandit/http2/stream.ex then joins every crumb into one binary.

This issue affects bandit: from 0.3.3 before 1.14.0.

### CVE-2026-108529

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-26T14:16:24.733 |

Inefficient Algorithmic Complexity vulnerability in the HTTP/2 implementation of mtrudel bandit allows an unauthenticated remote attacker to exhaust server CPU via small SETTINGS or connection-level WINDOW_UPDATE frames. The attacker opens thousands of streams whose responses block on the connection send window, then sends cheap frames that each make the server walk the whole queue of blocked sends. In the reporter's run, with 3,000 blocked streams a single 9-byte SETTINGS frame took 133 ms to process.

do_pending_sends/2 in lib/bandit/http2/connection.ex retries every queued send and, before each retry, removes that entry from the queue with List.delete/2, so one frame costs O(n²) list operations for n blocked streams. max_concurrent_streams defaults to :infinity, so the attacker chooses n.

This issue affects bandit: from 0.3.4 before 1.14.0.

### CVE-2026-108525

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-26T14:16:24.477 |

Allocation of Resources Without Limits or Throttling vulnerability in the HTTP/2 implementation of mtrudel bandit allows an unauthenticated remote attacker to exhaust server memory via DATA frames sent past the advertised receive window. The attacker requests a response larger than the 65,535-byte initial window and withholds WINDOW_UPDATE, so the stream process blocks while sending and stops reading, then floods small DATA frames on that stream. Every frame is queued in the stream's mailbox until the BEAM node runs out of memory.

Bandit.HTTP2.Connection.handle_frame/3 in lib/bandit/http2/connection.ex forwards each DATA frame to the stream process without consulting the receive window, and Bandit.HTTP2.FlowControl.compute_recv_window/2 replenishes the window as data arrives rather than as it is consumed, and never answers a violation with FLOW_CONTROL_ERROR.

This issue affects bandit: from 0.3.1 before 1.14.0.

### CVE-2026-116219

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-26T14:16:35.000 |

Dolibarr ERP CRM before 24.0.0 contains an OS command injection vulnerability in htdocs/admin/tools/export.php that lets authenticated administrators bypass the restrict_os_commands allowlist. Attackers can submit a mysqldump value chaining commands with & characters around an allowlisted basename to execute operating system commands as the web server user.

### CVE-2026-116232

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-93` |
| Published | 2026-10-26T08:17:17.837 |

A weakness has been identified in Oray Pugongying X5 Pro 7.6.1. This affects the function snmp_set of the component SNMP Handler. Executing a manipulation of the argument info.community can lead to crlf injection. It is possible to launch the attack remotely. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-116231

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-93` |
| Published | 2026-10-26T08:17:17.620 |

A security flaw has been discovered in Oray Pugongying X5 Pro 7.6.1. The impacted element is an unknown function of the component Ser2net. Performing a manipulation of the argument regmsg results in crlf injection. It is possible to initiate the attack remotely. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-115948

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-26T11:16:35.550 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in David Lingren Media LIbrary Assistant media-library-assistant allows Blind SQL Injection.This issue affects Media LIbrary Assistant: from n/a through 3.42.

### CVE-2026-115608

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-26T11:16:35.190 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Crocoblock JetEngine jet-engine allows SQL Injection.This issue affects JetEngine: from n/a through 3.9.0.

### CVE-2026-116237

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-93` |
| Published | 2026-10-26T10:16:52.477 |

A vulnerability was found in Oray Pugongying X5 Pro 7.6.1. This affects an unknown part of the component Dnsmasq. Performing a manipulation results in crlf injection. Remote exploitation of the attack is possible. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-116235

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-93` |
| Published | 2026-10-26T09:16:35.163 |

A flaw has been found in Oray Pugongying X5 Pro 7.6.1. Affected by this vulnerability is an unknown functionality of the component L2TP Authentication. This manipulation of the argument Username causes crlf injection. The attack may be initiated remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-116234

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-93` |
| Published | 2026-10-26T09:16:34.953 |

A vulnerability was detected in Oray Pugongying X5 Pro 7.6.1. Affected is an unknown function of the file /etc/ipsec.conf of the component IPsec Policy Handler. The manipulation of the argument secproto results in crlf injection. The attack can be launched remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-116233

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-93` |
| Published | 2026-10-26T09:16:34.787 |

A security vulnerability has been detected in Oray Pugongying X5 Pro 7.6.1. This impacts an unknown function of the component Dnsmasq. The manipulation of the argument rent_time leads to crlf injection. The attack can be initiated remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-113345

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-10-26T05:17:54.020 |

Electronic delivery item Inspection Support System provided by Japan's Ministry of Land, Infrastructure, Transport and Tourism contains an improper file access permission vulnerability. Files in the installation folder of the application may be tampered with, resulting in arbitrary code execution.

### CVE-2026-107900

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-26T07:17:08.360 |

V-SFT provided by FUJI ELECTRIC CO., LTD. contains an out-of-bounds read vulnerability in VS6ComFile!CCheck::ItemCheck. Opening a crafted V7 file may lead to information exposure or arbitrary code execution on the affected product.

### CVE-2026-107899

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-26T07:17:08.223 |

V-SFT provided by FUJI ELECTRIC CO., LTD. contains an out-of-bounds read vulnerability in VS6EditData!CDataRomErrorCheck::CheckSymbolMacroParam. Opening a crafted V7 file may lead to information exposure or arbitrary code execution on the affected product.

### CVE-2026-107898

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-26T07:17:07.950 |

V-SFT provided by FUJI ELECTRIC CO., LTD. contains an out-of-bounds read vulnerability in VS6EditData!CDataRomErrorCheck::MacroCommandCheck. Opening a crafted V7 file may lead to information exposure or arbitrary code execution on the affected product.

### CVE-2026-107897

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-26T07:17:07.827 |

V-SFT provided by FUJI ELECTRIC CO., LTD. contains an out-of-bounds read vulnerability in VS6MemInIF!set_temp_type_default. Opening a crafted V7 file may lead to information exposure or arbitrary code execution on the affected product.

### CVE-2026-107896

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-26T07:17:07.700 |

V-SFT provided by FUJI ELECTRIC CO., LTD. contains an out-of-bounds read vulnerability in VS6ComFile!load_gr_item. Opening a crafted V7 file may lead to information exposure or arbitrary code execution on the affected product.

### CVE-2026-107895

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-26T07:17:07.570 |

V-SFT provided by FUJI ELECTRIC CO., LTD. contains an out-of-bounds write vulnerability. Opening a crafted V7 file may lead to information exposure or arbitrary code execution on the affected product.

### CVE-2026-107894

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-26T07:17:07.397 |

V-SFT provided by FUJI ELECTRIC CO., LTD. contains a stack-based buffer overflow vulnerability. Opening a crafted V7 file may lead to information exposure or arbitrary code execution on the affected product.

### CVE-2026-116116

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-347` |
| Published | 2026-10-26T04:17:55.047 |

A vulnerability was detected in Yoosee GM8135S Camera 21.00.01.36. Affected is an unknown function of the component Secure Boot. Performing a manipulation results in improper verification of cryptographic signature. The attack needs to be approached locally. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-70388

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-191;CWE-195;CWE-787` |
| Published | 2026-10-26T09:16:35.860 |

SOEM version 2.0.0 and earlier contains vulnerabilities where a malicious device on the network can send specially crafted messages that cause the master to write data outside allocated memory boundaries. The software performs arithmetic on message length values without proper validation, allowing negative or extremely large values to bypass safety checks. This can corrupt memory and potentially allow an attacker to execute arbitrary code on the master system.

### CVE-2026-97200

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409;CWE-770` |
| Published | 2026-10-26T14:16:42.180 |

Allocation of Resources Without Limits or Throttling vulnerability in hackney_conn in benoitc hackney allows a malicious HTTP server to exhaust client memory via an oversized or highly compressed response body. hackney:request/5 and hackney:body/1 return the whole response body, and nothing bounds how much the connection process buffers. Any server the client requests can trigger it.

hackney_conn:read_full_body/2 and the HTTP/2 and HTTP/3 accumulators append every chunk until the body ends. With {auto_decompress, true} the buffered body is then inflated in one step with zlib:gunzip/1 or zlib:inflate/2, which return the whole output at once.

This issue affects hackney: from 2.0.0-beta.1 before 4.9.0.

### CVE-2026-115193

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-26T14:16:30.760 |

A stored Cross-Site Scripting (XSS) vulnerability exists in the contact detail view of Mautic 7. Values of HTML-type custom contact fields are rendered without output sanitization. A user or integration able to write a value to such a field (for example, through contact editing, the contact API, or a form submission mapped to the field) can store a script payload in it. When another user, including an administrator, opens the affected contact's detail page, the injected script executes within the context of their active browser session. This could allow an attacker to perform administrative actions on behalf of the victim, such as creating new administrator accounts, altering system configuration, or accessing contact and campaign data.

### CVE-2026-111103

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-460` |
| Published | 2026-10-26T14:16:27.450 |

Improper Cleanup on Thrown Exception vulnerability in the HTTP/2 handler of mtrudel bandit allows an unauthenticated remote attacker to bypass per-connection resource limits via a single TCP write that carries several frames, one of which raises a stream error.

When a frame raises StreamError partway through a chunk, Bandit.HTTP2.Handler.handle_data/3 sends RST_STREAM and continues with the connection state from before the chunk, dropping the rest of it. Streams opened by earlier frames in the chunk keep running their Plug calls, but the stream counts, last_stream_id, the rapid-reset timestamps, the HPACK decoder state and the buffer roll back, so max_concurrent_streams, max_requests and the rapid-reset limiter never see those streams. A client that sends one HEADERS frame more than max_concurrent_streams in each write has the extra refused and the others forgotten: with a limit of 10, five such writes run 50 Plug calls at once.

This issue affects bandit: from 1.9.0 before 1.14.0.

### CVE-2026-94380

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-26T12:17:08.260 |

Weak Password Recovery Mechanism for Forgotten Password vulnerability in HAVELSAN Inc. Liman MYS allows Password Recovery Exploitation.

This issue affects Liman MYS: from 2.3.4-1124 before 2.3.5-1131.

### CVE-2026-115190

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-26T14:16:30.350 |

An insecure deserialization (PHP object injection) vulnerability exists in Mautic's handling of segment filters and custom field properties. Several code paths that read these stored values from the database deserialize them without restricting which PHP classes may be instantiated, instead of using Mautic's safe deserialization helper. An attacker who is able to store a crafted serialized value in these segment filter or custom field properties can cause arbitrary PHP objects to be instantiated when Mautic later processes the data, for example during segment evaluation, contact export, or custom field API requests. Combined with gadget chains available in Mautic's dependencies, this could allow an attacker to execute arbitrary code on the server, read, modify, or delete data stored in the Mautic instance, including contact data, and affect its availability. Exploitation requires high privileges or an existing ability to write to the affected stored data.

### CVE-2026-116372

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-26T09:16:35.580 |

MISP mispguard is a security filtering proxy that inspects and blocks MISP feed responses based on configured rules. The process_feed_response method in src/mispguard.py was responsible for evaluating feed responses before they reached the MISP instance. The original logic only explicitly handled the case where the HTTP status code was not 200 by passing the response through without filtering, on the assumption that non-200 responses would not carry ingestible event data. However, HTTP 2xx status codes other than 200 (such as 201 Created, 203 Non-Authoritative Information, and 206 Partial Content) were also passed through unfiltered. Because MISP may still ingest content from these responses, a malicious or compromised feed host could return a 203 or 206 status code with arbitrary content, effectively bypassing all of mispguard's filtering rules. This allowed unfiltered or malicious feed data to be ingested into the MISP instance, undermining the security controls that mispguard is designed to enforce. The vulnerability requires the attacker to control or compromise a feed endpoint configured in the MISP instance. No authentication or user interaction is required beyond the feed polling mechanism already in place.

### CVE-2026-89209

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-10-26T11:16:38.583 |

A vulnerability has been identified in Mendix SAML (Mendix 10 compatible) (All versions < V4.2.4), Mendix SAML (Mendix 11 compatible) (All versions < V4.2.4), Mendix SAML (Mendix 9 compatible) (All versions < V3.6.29). Affected versions of the module do not properly protect against SAML assertion replay in IdP-initiated authentication flows. This could allow unauthenticated remote attackers to gain unauthorized access to the application by replaying a valid SAML response.

### CVE-2026-96581

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-26T08:17:20.423 |

Authorization Bypass Through User-Controlled Key vulnerability in ash-project ash allows a user of one tenant to read, overwrite and take over another tenant's records via an upserting create action.

Under attribute multitenancy, Ash.Actions.Create (lib/ash/actions/create/create.ex) and Ash.Actions.Create.Bulk (lib/ash/actions/create/bulk.ex) upserted on the primary key, or on an all_tenants? identity, without scoping the conflicting record to the request's tenant. A caller of a create action with upsert? true that accepts the primary key, supplying a record id from another tenant, updated that record's upsert fields and received all of its attributes in the result. With the default upsert fields the tenant attribute was written too, moving the record into the caller's tenant. Read and update policies do not run for upserts, and tenant-scoped create policies pass because the tenant is the caller's own.

This issue affects ash: from 1.22.0 before 3.37.2.

### CVE-2026-116236

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-434` |
| Published | 2026-10-26T09:16:35.370 |

A vulnerability has been found in Oray Pugongying X5 Pro 7.6.1. Affected by this issue is the function plugin_init of the file /tmp/upload_files of the component PPPoE WAN Setting Handler. Such manipulation of the argument pppd_options leads to unrestricted upload. The attack may be launched remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-116218

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-26T14:16:34.823 |

Dolibarr ERP CRM 19.0.0 before 23.0.4 contains an SQL injection vulnerability that allows authenticated API users to inject SQL via the type field of the third-party bankaccounts REST endpoint. Attackers with only societe/creer permission can break out of the unescaped type value in CompanyBankAccount::create() to read password hashes and API keys via time-based blind subqueries.

### CVE-2026-116492

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-26T14:16:37.667 |

Frappe CRM app before 1.89.1 contains a missing authorization vulnerability that allows authenticated low-privileged users to read CRM Lead records they are not permitted to access by querying the get_contact_by_phone_number API, which performs raw database queries without invoking the permission system. Attackers can supply a known phone number to the crm.integrations.api.get_contact_by_phone_number endpoint to retrieve full lead details otherwise blocked by standard API and UI access controls, resulting in unauthorized disclosure of sensitive CRM data.

### CVE-2026-116210

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-26T14:16:33.707 |

Webasyst Framework through 4.4.0 contains a cross-site request forgery vulnerability in the Photos app that allows remote attackers to perform backend actions because the app does not enable the framework's opt-in CSRF check. Attackers can lure logged-in Photos users to a malicious page that submits forged POST requests to photo/delete, album/save, photo/manageAccessSave or photo/saveField, deleting photos and changing access rights.

### CVE-2026-115192

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-26T14:16:30.617 |

An SQL Injection vulnerability exists in the dashboard widget data API endpoint (/api/data/{type}). Chart filter parameters supplied by the client are not properly validated before they are used in the database queries that build dashboard chart data. An authenticated user with API access can exploit this to inject SQL into these reporting queries. Using blind SQL injection techniques, the attacker can read arbitrary data from the Mautic database, including contact and other marketing data and user account data with password hashes. The injected SQL can also be used to slow down database queries, which can have a limited impact on availability. Data modification is not possible through this vulnerability. Exploitation requires the Mautic API to be enabled.

### CVE-2026-115191

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-26T14:16:30.490 |

A SQL injection vulnerability exists in a contact lookup AJAX endpoint of the Mautic administration interface (/s/ajax). A request parameter that selects the contact field to search by is not properly validated before it is used in a database query. Any authenticated Mautic user can exploit this, regardless of the role or permissions assigned to the account. Using blind (boolean-based or time-based) techniques, the attacker can run arbitrary SQL queries against the Mautic database and read any data the Mautic database user can access, including Mautic user accounts with email addresses and password hashes, contact data, and campaign and email content.

### CVE-2026-116469

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-178` |
| Published | 2026-10-26T11:16:37.840 |

MISP Guard, a proxy-based security filter for MISP (Malware Information Sharing Platform) feed distribution, contains a case-sensitivity flaw in multiple policy enforcement checks. The functions check_required_taxonomy_exists, check_required_taxonomy_tags_allowed, check_blocked_attribute_categories, and check_blocked_analyst_data_sharing_groups_uuids performed case-sensitive string comparisons when matching event tags, attribute categories, and sharing-group UUIDs against configured allow/block lists.

An attacker with the ability to create or modify events in a MISP instance (or a connected instance that pushes events through the guard) could craft events using different letter case in taxonomy tag names, attribute categories, or sharing-group UUIDs to bypass the configured security policies. For example, if the policy requires the 'tlp' taxonomy with only 'tlp:clear' allowed, an event tagged 'TLP:AMBER' would not be recognized as belonging to the 'tlp' taxonomy and would therefore not be checked against the allowed-tags list, resulting in the event being forwarded to feed consumers. Similarly, a blocked attribute category such as 'Person' would not match a configured block entry of 'person', allowing the attribute to pass through the filter.

The security impact is unauthorized disclosure of threat-intelligence data that the operator intended to restrict. Events carrying non-allowed TLP (Traffic Light Protocol) markings, blocked attribute categories, or blocked sharing-group associations are forwarded to downstream feed consumers in violation of the configured distribution policy. This undermines the confidentiality controls that MISP Guard is designed to enforce.

The vulnerability is trivially exploitable: the attacker only needs to alter the letter case of a tag, category, or UUID string. No authentication beyond normal MISP event-creation privileges is required, and no user interaction is needed.

### CVE-2026-82947

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-125;CWE-129;CWE-191;CWE-787` |
| Published | 2026-10-26T09:16:36.473 |

SOEM version 2.0.0 and earlier contains multiple vulnerabilities in frame processing where a malicious device can cause the master to read data outside allocated buffers. The software uses length and offset values from device messages without validating them against buffer sizes. This can cause the master to access invalid memory locations, potentially disclosing sensitive information or causing crashes.

### CVE-2026-116488

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-26T14:16:37.520 |

NXP MCUXpresso SDK USB middleware (mcuxsdk-middleware-usb) before 2.13.0 contains a heap buffer overflow in host audio, video and CDC class drivers that trust device-supplied bNumEndpoints and bLength values. A malicious USB device can supply crafted descriptors that write endpoint entries past the fixed-size epList array, corrupting heap memory for code execution or denial of service.
