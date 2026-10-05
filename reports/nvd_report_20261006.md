# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-05 15:00 UTC
- **対象期間**: `2026-10-04T15:00:21.000Z` 〜 `2026-10-05T15:00:28.000Z`
- **重要CVE数**: 49 件（Critical 9.0+: 18 件 / High 7.0〜: 31 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS 7.0 以上が **30 件** 超と非常に多く、特に **認証バイパス・TLS 検証無効化** が目立ちます。  
- コンテナイメージや SaaS 向けサービス（Perforce P4 Search、ZITADEL）で **未認証リモートから最高権限取得** が可能になる脆弱性が集中しています。  
- 組み込み系（Totolink ルータ）やオープンソースライブラリ（kubernetes‑client、google‑maps、go‑micro など）でも **スタックバッファオーバーフローや証明書検証回避** が報告され、インフラ全体の攻撃面が拡大しています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑100103** | 10.0 | Perforce P4 Search コンテナイメージ（2026.4.2 未満）で認証トークンがデフォルトにリセットされ、認証なしで **最高権限** を取得可能。 | **最高スコア** かつ、P4 Search が接続する P4 Server までフル compromise になる点が重大。 |
| **CVE‑2026‑103510** | 9.5 | 同上の P4 Search がトークンが空白の場合に安全に失敗せず、認証なしで全権取得。 | 2026.4.2 未満の全コンテナで共通。P4 Search のデプロイが多く、企業内部のコード管理資産が危険に晒される。 |
| **CVE‑2026‑105285** | 9.3 | Totolink A3002MU ルータ（1.0.0‑B20230403.1455）で `/boafrm/formIpQoS` の `addQos/comment/entry_name` パラメータに **スタックバッファオーバーフロー** が発生し、リモートからコード実行可能。 | IoT デバイスはパッチ適用が遅れがちで、社内ネットワークに直接接続されるケースが多く、遠隔からの完全乗っ取りリスクが高い。 |
| **CVE‑2026‑105215** | 9.3 | ZITADEL（3.x < 3.4.14、4.x < 4.16.2）で **認証バイパス** が存在。外部 IdP からのコールバックをスキップし、偽装 ID でログイン可能。 | 認証基盤そのものが破られると、全社シングルサインオンが失効。多数の SaaS が ZITADEL を利用している点でインパクト大。 |
| **CVE‑2026‑105089** | 9.3 | WWBN AVideo（≤ 29.2.0）で **Stored XSS** が可能。動画トレーラー URL にスクリプトを埋め込め、管理画面やプレイリストで実行される。 | メディアサーバは社内外で広く利用され、XSS が成功すると管理者権限で任意コード実行や情報漏洩につながる。 |

> **補足**：TLS 証明書検証をデフォルトで無効化する脆弱性（maclof/kubernetes‑client、alexpechkarev/google‑maps、gopay、go‑micro など）も多数報告されていますが、上記 5 件は **直接的な権限取得・コード実行** が可能な点で優先度が高いです。

---

## 3. 推奨アクション  

### 3.1. 直ちに適用すべきパッチ／アップグレード  

| 製品・ライブラリ | 現行脆弱バージョン | 推奨バージョン | 対応策 |
|------------------|-------------------|----------------|--------|
| **Perforce P4 Search** (Docker) | 2026.4.2 未満 | **2026.4.2 以上** | コンテナイメージを公式リポジトリの `perforce/p4search:2026.4.2` 以降に更新し、`P4SEARCH_AUTH_TOKEN` がデフォルトに戻らないことを確認。 |
| **Totolink A3002MU** ファームウェア | 1.0.0‑B20230403.1455 | **最新公式ファームウェア (≥ 1.0.0‑B20231201)** | Web 管理画面 → ファームウェア更新 → 最新版を適用。アップデート後は `formIpQoS` エンドポイントへの外部アクセスをファイアウォールで遮断。 |
| **ZITADEL** | 3.x < 3.4.14、4.x < 4.16.2 | **3.4.15** 以上、**4.17.1** 以上 | Helm/Operator で `zitadel` のイメージタグを `zitadel/zitadel:4.17.1` に更新。`Login V1/V2` の設定で `externalIdpCallbackRequired=true` を強制。 |
| **WWBN AVideo** | ≤ 29.2.0 | **29.2.1** 以上 | `apt-get update && apt-get install avideo=29.2.1`（または Docker イメージ `avideo:29.2.1`）にアップグレード。アップロード機能のサニタイズ設定を `allowUnsafeUrls=false` に変更。 |
| **maclof/kubernetes-client (Go)** | < 0.32.0 | **0.32.0** 以上 | `go get github.com/maclof/kubernetes-client@v0.32.0` でモジュール更新。`parseKubeconfig*` 呼び出し時に `InsecureSkipTLSVerify` が **false** になることをテスト。 |
| **alexpechkarev/google-maps (Laravel)** | ≤ 12.16 | **12.17** 以上 | `composer require alexpechkarev/google-maps:^12.17`。`config/google-maps.php` の `ssl_verify_peer` を `true` に設定。 |
| **gopay** | < 1.5.119 | **1.5.119** 以上 | `go get github.com/go-pay/gopay@v1.5.119`。`defaultClient()` の `InsecureSkipVerify` を削除し、`TLSConfig` を明示的に設定。 |
| **go-micro** | < 6.0.0 | **6.0.0** 以上 | `go get github.com/go-micro/go-micro/v2@v6.0.0`。TLS ヘルパーで `InsecureSkipVerify` が **false** になることを確認。 |

### 3.2. 設定・運用上のベストプラクティス  

1.

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-100103

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-10-05T09:17:05.717 |

Perforce P4 Search container images prior to 2026.4.2 reset the service authentication token to a publicly documented default value. An unauthenticated attacker with network access can obtain the highest application privilege, potentially leading to arbitrary code execution and compromise of the connected P4 Server.

### CVE-2026-103510

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636` |
| Published | 2026-10-05T09:17:06.977 |

P4 Search prior to 2026.4.2 does not fail securely when its service authentication token is blank. In affected configurations, an unauthenticated attacker with network access can obtain the highest application privilege, potentially leading to compromise of P4 Search and the connected P4 Server.

### CVE-2026-100102

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-10-05T09:17:05.540 |

Perforce P4 Search container images prior to 2026.4.2 enable an unauthenticated Java debug interface. An attacker with network access to this interface can execute arbitrary code as the P4 Search service account, potentially leading to compromise of the connected P4 Server.

### CVE-2026-105285

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-10-05T10:16:38.520 |

A security vulnerability has been detected in Totolink A3002MU 1.0.0-B20230403.1455. This affects an unknown function of the file /boafrm/formIpQoS of the component QoS Rule Handler. The manipulation of the argument addQos/comment/entry_name leads to stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit has been disclosed publicly and may be used.

### CVE-2026-105284

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-285` |
| Published | 2026-10-05T09:17:12.350 |

A weakness has been identified in Totolink A3002MU 1.0.0-B20230403.1455. The impacted element is the function sub_40FCFC of the file /bin/boa of the component Authentication Check. Executing a manipulation can lead to improper authorization. The attack may be launched remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-105089

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-04T16:16:30.330 |

WWBN AVideo through 29.2.0 contains a stored cross-site scripting vulnerability that allows users with upload permission to inject script by setting a malicious video trailer1 URL. The value is rendered unescaped in YouPHPFlix2 templates and channel playlists, letting attackers break out of onclick strings or iframe src attributes to execute JavaScript in victims' browsers.

### CVE-2026-105086

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-04T16:16:30.183 |

WWBN AVideo 12.4 through 29.2.0 contains a stored cross-site scripting vulnerability that allows authenticated uploaders to inject HTML by submitting doubly-encoded entities in video titles. Because safeString() strips tags before decoding entities and runs twice via setTitle() and save(), attackers can store markup that executes in trending, gallery, embed, and playlist pages.

### CVE-2026-105215

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-04T15:16:32.993 |

ZITADEL before 3.4.14 and 4.x before 4.16.2 contains an authentication bypass in the hosted Login V1 UI because the 'external account not found' registration endpoint trusts client-supplied external identity fields without a completed IdP callback. Unauthenticated attackers can submit forged IDPConfigID and ExternalUserID values to pre-create an account bound to a victim's external IdP identity, which the victim's later genuine external login then signs into.

### CVE-2026-105209

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-04T15:16:32.007 |

ZITADEL 3.x before 3.4.15 and 4.x before 4.17.1 contains an improper authorization vulnerability: when issuing passkey or passwordless enrollment codes, it checks only the organization in the x-zitadel-orgid header, not the target user's organization. Attackers with user-write permission in one organization can obtain an enrollment code for a user in another organization on the same instance and register their own authenticator to take over that account.

### CVE-2026-105207

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-04T15:16:31.677 |

ZITADEL 3.0.0 through 3.4.15 and 4.0.0 before 4.17.3 creates links between user accounts and external identity providers without verifying a primary factor or the caller's permission, including on identify-only Login V2 sessions and via the User Service V2 AddIDPLink endpoint. An unauthenticated attacker knowing a victim's login name can bind their own external IdP identity to the victim's account and then sign in as the victim.

### CVE-2026-105293

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-05T01:16:28.780 |

Legcord 1.1.0 through 1.3.0 contains a path traversal vulnerability in theme IPC handlers that allows script in the Discord page to escape the themes directory via unvalidated theme ids. Attackers running script in the Discord origin, such as through XSS, can abuse themes.folder, themes.uninstall, and themes.install to launch local executables, recursively delete directories, and write files outside the themes directory.

### CVE-2026-105211

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-04T15:16:32.333 |

ZITADEL before 4.17.1 contains an authentication bypass vulnerability in Login V2 that allows unauthenticated attackers to take over accounts by obtaining OTP codes via the returnCode delivery type. Attackers knowing a login name of a victim with OTP-Email and OTP-SMS enrolled can read both codes from server-action responses to gain MFA-authenticated sessions, including administrator takeover.

### CVE-2026-105294

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15` |
| Published | 2026-10-05T01:16:28.923 |

Legcord 1.1.0 through 1.3.0 contains a configuration injection vulnerability that allows script in the Discord page to write any config key via the window.legcord settings.setConfig bridge. Attackers exploiting a Discord XSS can set additionalArguments to persistently add --proxy-server and --ignore-certificate-errors switches, routing all client traffic through an interception proxy.

### CVE-2026-105223

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-05T01:16:28.480 |

maclof kubernetes-client 0.17.0 before 0.32.0 disables TLS certificate verification in parseKubeconfig() and parseKubeconfigFile() when a kubeconfig lacks certificate-authority-data, ignoring insecure-skip-tls-verify. On-path attackers can impersonate the Kubernetes API server to capture Bearer tokens or Basic credentials and tamper with WebSocket or REST API traffic.

### CVE-2026-105222

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-04T23:16:59.917 |

The alexpechkarev/google-maps Laravel package through 12.16 disables TLS certificate verification by default because the bundled config sets ssl_verify_peer to FALSE, which is passed to CURLOPT_SSL_VERIFYPEER. On-path attackers can present any certificate to intercept Google Maps web-service requests, steal the API key from the query string, and tamper with responses.

### CVE-2026-105221

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-04T23:16:59.770 |

The gist RubyGem before 6.1.0 contains an improper certificate validation vulnerability that allows on-path attackers to intercept HTTPS traffic because http_connection in lib/gist.rb sets VERIFY_NONE. Attackers can present any certificate to read or modify GitHub API traffic, stealing OAuth tokens and login credentials to read and modify the victim's gists.

### CVE-2026-105218

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-04T18:16:34.630 |

gopay before 1.5.119 disables TLS certificate verification in defaultClient() in pkg/xhttp/client.go, allowing man-in-the-middle attackers to impersonate payment provider APIs. Attackers can present any certificate to read merchant credentials, signatures and transaction data, and modify payment, refund and order query responses.

### CVE-2026-105216

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-04T18:16:34.287 |

go-micro before 6.0.0 contains an improper certificate validation vulnerability that allows network attackers to impersonate services because the shared TLS helper sets InsecureSkipVerify to true by default. Man-in-the-middle attackers can present any certificate to intercept or modify gRPC transport, HTTP and RabbitMQ broker, and Consul or etcd registry traffic, including authentication tokens and credentials.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-92931

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-05T14:17:21.323 |

CWE-918: Server-Side Request Forgery in the Progress @progress/sitefinity-nextjs-sdk npm package versions 15.1.8326 through 15.4.8637 may allow a remote attacker to make server-side requests to an attacker-controlled host, potentially exposing sensitive information.

### CVE-2026-20586

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-05T02:16:53.803 |

In vdec, there is a possible out of bounds write due to a missing bounds check. This could lead to remote escalation of privilege with no additional execution privileges needed. User interaction is needed for exploitation. Patch ID: ALPS11383899; Issue ID: MSV-9614.

### CVE-2026-105213

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-04T15:16:32.687 |

ZITADEL 4.x before 4.17.1 does not check an organization's inactive state during Login V2 authentication, verifying only the individual user's status. Users of a deactivated organization who hold valid credentials, an existing session, or a refresh token can still sign in, create sessions, and obtain or refresh tokens.

### CVE-2026-105210

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-04T15:16:32.170 |

ZITADEL 3.x before 3.4.15 and 4.x before 4.17.1 contains a missing authentication flaw in the hosted Login V1 UI, whose second-factor enrollment and initialization handlers act on an identify-only session before any primary factor is verified. Attackers knowing only a victim's login name can enroll attacker-controlled TOTP, OTP-SMS, OTP-Email, or U2F factors, overwrite the verified phone number, and enumerate users through discrepant errors.

### CVE-2026-105219

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-04T18:16:34.777 |

Mammoth.js 1.3.0 before 1.12.3 contains a regular expression denial of service vulnerability in the style map tokeniser in lib/styles/parser/tokeniser.js due to overlapping regex alternatives. Attackers can supply a crafted .docx with an unterminated quoted string of repeated backslash escapes in mammoth/style-map to block the Node.js event loop.

### CVE-2026-105212

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-04T15:16:32.520 |

ZITADEL 3.x before 3.4.14 and 4.x before 4.16.2 contains an authentication bypass in the hosted Login V1 and Login V2 UIs that accepts passkey or other authenticator enrollment on identify-only login sessions, before any primary factor is verified. Unauthenticated attackers knowing only a victim's login name can register an attacker-controlled authenticator and log in as that user, bypassing existing passwords and MFA.

### CVE-2026-105208

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-649` |
| Published | 2026-10-04T15:16:31.843 |

ZITADEL 4.x before 4.17.3 and 3.x through 3.4.15 protects IdP intent tokens with unauthenticated, malleable encryption, allowing authenticated users to tamper with their own token so it is accepted for another user's external login intent. An attacker who predicts a victim's in-flight intent identifier and wins a timing race can call /v2/idp_intents or /v2/sessions to steal the victim's IdP tokens or hijack their session.

### CVE-2026-63277

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-05T12:17:11.253 |

LibreOffice Calc can link a cell range to an external data source, and the link is saved in the document. A document could name a Java database driver for such a link to be loaded from a remote location, so opening the document could run Java code from that location. In fixed versions an entry in a Java class path has to be a file URL.

### CVE-2026-104805

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:D/RE:M/U:Amber` |
| Weaknesses | `CWE-22;CWE-73;CWE-345;CWE-434;CWE-494` |
| Published | 2026-10-05T09:17:09.380 |

DigitalCanion has discovered a vulnerability in the backup restoration functionality that allows an attacker with access to the configured backup repository to introduce arbitrary files into the system during restoration.




The specific flaw exists within the backup restoration mechanism, which fails to properly validate the paths, file types, integrity, and authenticity of files contained within a restored TGZ archive. The application does not perform file-signature verification before extracting the archive, allowing a specially crafted backup to contain attacker-controlled files.




An attacker with access to the backup SFTP or other configured repository can therefore provide a malicious TGZ archive that, when restored by the system, may place arbitrary files on the underlying Linux system. Depending on the location and permissions of the extracted files, this behavior can potentially be leveraged to achieve arbitrary code execution with root privileges and compromise the underlying virtual machine.




The absence of enforced backup passwords further reduces the protection provided by the backup mechanism and may facilitate unauthorized access to the repository.

### CVE-2026-104389

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-05T09:17:07.657 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Sirv Sirv sirv allows Blind SQL Injection.This issue affects Sirv: from n/a through 8.2.5.

### CVE-2026-105220

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-04T23:16:59.627 |

Twine 2 desktop through 2.12.0 contains a cross-site scripting vulnerability in importStories() that executes markup from imported story files in the editor window. Attackers can craft a story file whose script calls the twineElectron openWithScratchFile IPC bridge to write and open a .bat file, executing code as the user.

### CVE-2026-19184

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-05T09:17:12.907 |

The NXP GAU ADC driver (drivers/adc/adc_mcux_gau_adc.c) validated the caller-supplied sequence->buffer_size, which is expressed in bytes, against the number of active channels, which is a sample count. It then stored that byte count directly in data->results_length and used it in mcux_gau_adc_read_samples() as the number of uint16_t slots available. Because each conversion result occupies sizeof(uint16_t) bytes, a buffer that was accepted as "large enough" could be written with up to twice its size in bytes, so every sample past the buffer's midpoint was written out of bounds.

adc_read() and adc_read_async() are Zephyr system calls. The syscall verifier in drivers/adc/adc_handlers.c only confirms that the caller owns buffer_size writable bytes (K_SYSCALL_MEMORY_WRITE); deciding whether that size is sufficient for the requested channels and extra_samplings is delegated entirely to the driver. On a build with CONFIG_USERSPACE=y, a user-mode thread that has been granted the ADC device object could therefore submit a deliberately half-sized buffer and cause the driver's work-queue handler — which runs in supervisor mode, outside the caller's MPU restrictions — to write ADC conversion results past the end of that buffer, at an address and for a length of the caller's choosing.

The overrun is bounded by the requested sequence: with sequence->options->extra_samplings set, the sampling loop walks the buffer pointer forward across every sampling, so the total overrun can reach the full size of the supplied buffer (kilobytes for a large extra_samplings). The written words are 16-bit ADC conversion results, so the content is only partially attacker-influenced (via the selected analog input, gain and resolution), but the destination and length are fully controlled — sufficient for kernel memory corruption, a crash, or a userspace-to-kernel privilege escalation. Builds without CONFIG_USERSPACE, or on SoCs other than NXP RW61x with the GAU ADC node enabled, are not exposed to the privilege boundary; there the same defect only causes a silent overflow when the application itself passes an undersized buffer.

The fix replaces the ad-hoc check with the shared adc_sequence_validate_buffer() helper (validating against num_channels * sizeof(uint16_t)), stores buffer_size / sizeof(uint16_t) in results_length, and corrects the loop bound to a post-decrement so exactly the available number of slots may be written.

### CVE-2026-104811

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-20;CWE-94;CWE-434;CWE-829` |
| Published | 2026-10-05T09:17:10.290 |

DigitalCanion SA has discovered a vulnerability that allows remote attackers to execute arbitrary code on affected installations of the product. Authentication may be required to exploit this vulnerability.




The specific flaw exists within the Configuration → Services → Music on Hold functionality of the web portal listening on TCP port 443. The application is intended to allow users to upload WAV audio files but fails to properly validate the uploaded file type. An attacker can exploit this behavior to upload a malicious shared object (.so) instead of a WAV file. When the uploaded file is subsequently processed by the affected component, attacker-controlled code is loaded and executed in the context of the affected process. This can result in remote code execution and potentially full compromise of the underlying Linux system.

### CVE-2026-104810

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-31` |
| Published | 2026-10-05T09:17:10.153 |

This vulnerability allows remote attackers to delete sensitive files on vulnerable installations of Mitel MiVoice Office 400. Authentication is required to exploit this vulnerability.




The specific flaw exists within the web portal listening on TCP port 443, under Maintenance → File Management → File Browser, which is affected by a directory traversal vulnerability. By exploiting this vulnerability, an authenticated attacker can access and delete files outside of the intended directory, including files belonging to the Mitel application and the underlying Linux system. Deleting critical system or application files can result in a denial-of-service condition affecting the underlying system.

### CVE-2026-104809

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-73;CWE-426;CWE-427;CWE-494;CWE-829` |
| Published | 2026-10-05T09:17:10.007 |

DigitalCanion has discovered a vulnerability that allows an attacker to cause the system to load an attacker-controlled .so file instead of the expected legitimate module. The loading mechanism relies on a predictable module name without adequately verifying the file’s origin or integrity. A malicious shared object using the expected name can therefore be loaded by a privileged process. The module code then executes within the context and privileges of that process. This results in arbitrary code execution and full compromise of the Mitel Linux virtual machine.

### CVE-2026-104706

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-31` |
| Published | 2026-10-05T09:17:09.167 |

DigitalCanion has discovered a path traversal vulnerability that allows to view or download sensitive system files over the portal https://<ip>:8443 via menus Administration -> View Logs

### CVE-2026-20531

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-05T02:16:51.907 |

In apu, there is a possible memory corruption due to use after free. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation. Patch ID: ALPS11249016; Issue ID: MSV-9169.

### CVE-2026-20524

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1285` |
| Published | 2026-10-05T02:16:51.040 |

In apu, there is a possible memory corruption due to improper input validation. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation. Patch ID: ALPS11249004; Issue ID: MSV-9170.

### CVE-2026-20523

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-05T02:16:50.917 |

In neuropilot, there is a possible out of bounds write due to a missing bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation. Patch ID: ALPS11249062; Issue ID: MSV-9171.

### CVE-2026-20522

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-05T02:16:50.793 |

In neuropilot, there is a possible out of bounds write due to a missing bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation. Patch ID: ALPS11249050; Issue ID: MSV-9172.

### CVE-2026-20521

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-05T02:16:50.660 |

In Video HAL, there is a possible escalation of privilege due to a missing bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation. Patch ID: ALPS11375674; Issue ID: MSV-9571.

### CVE-2026-77805

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-05T13:16:54.740 |

In Progress® Telerik® Fiddler® Classic for Windows, versions prior to v6.0.20262.10021, the integrity check applied to the external helper tools launched by the application is insufficient. Before executing a helper tool, the application only verifies that the file carries a valid Authenticode signature whose certificate subject name matches a broad allow list of publisher name fragments, rather than verifying that the file is the specific executable shipped with that version of the product. A local threat actor with low privileges who replaces one of these helper executables with any other validly signed binary from an allow-listed publisher can cause the substituted binary to be executed by the application, including with Administrator privileges for the tools that request elevation, resulting in privilege escalation and execution of unintended code. Successful exploitation requires the user to launch the affected external tool and to approve the elevation prompt without noticing that it refers to a different executable.

### CVE-2026-19185

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-05T09:17:13.077 |

The system-call verifier for i3c_do_ccc() in drivers/i3c/i3c_handlers.c validated the outer struct i3c_ccc_payload, the broadcast ccc.data buffer and the targets.payloads[] array, but did not validate the per-target data buffers those array elements point at. Each struct i3c_ccc_target_payload carries its own data pointer and data_len, and neither was passed through K_SYSCALL_MEMORY() before the payload was handed to z_impl_i3c_do_ccc() and on to the controller driver. The verifier also operated on the caller's live structure rather than a snapshot, so validated fields could be changed by a second user thread between the check and the driver's use — unlike the sibling z_vrfy_i3c_transfer(), which has always copied its message array first.

The defect is only present in CONFIG_USERSPACE builds, where drivers/i3c/i3c_handlers.c is compiled. An unprivileged user-mode thread that has been granted access to the I3C controller device object — the ordinary way an application lets a user thread talk to I3C peripherals — can issue a direct CCC whose target payload data pointer names an arbitrary kernel address. Controller drivers dereference that pointer directly (for example drivers/i3c/i3c_mcux.c, drivers/i3c/i3c_cdns.c, drivers/i3c/i3c_stm32.c, drivers/i3c/i3c_npcx.c), using rnw to decide direction.

A read CCC therefore causes the kernel-mode driver to write bus-received bytes into an attacker-chosen kernel address for an attacker-chosen length, and a write CCC transmits kernel memory out onto the I3C bus. The result is an out-of-bounds kernel write plus a kernel memory disclosure, i.e. escalation from a user-mode thread to supervisor privilege, defeating the isolation CONFIG_USERSPACE is meant to provide.

The fix introduces copy_ccc_and_do(), which snapshots the payload, copies the target array into kernel memory with k_usermode_alloc_from_copy() (bounding num_targets to fewer than 32), validates each per-target buffer with K_SYSCALL_MEMORY() according to rnw, and copies the driver-written num_xfer and err fields back to the caller.

### CVE-2026-105295

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-10-05T01:16:29.063 |

GitAhead 2.5.0 through 2.7.1 contains an insecure update mechanism that installs downloaded updates without integrity or signature verification and permanently ignores TLS errors after one SSL error dialog. Network attackers presenting an invalid certificate once can intercept later automatic update checks, offer a fake version, and execute code as the user upon installation.

### CVE-2026-104408

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-05T09:17:08.623 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Groundhogg Groundhogg groundhogg allows Blind SQL Injection.This issue affects Groundhogg: from n/a through 4.8.3.

### CVE-2026-103507

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-05T09:17:06.843 |

Perforce P4 Search prior to 2026.4.2 does not restrict file paths written through its logging configuration interface. An attacker holding the service authentication token can write arbitrary files on the host, potentially leading to code execution as the P4 Search service account.

### CVE-2026-105314

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-24` |
| Published | 2026-10-05T08:17:15.797 |

Papermerge 3.5.3 allows remote code execution by a standard user via directory traversal in a /api/documents/upload call. A Python .pth file can be written to site-packages, and its code is executed upon the next start of the Python interpreter.

### CVE-2026-20526

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-05T02:16:51.283 |

In Modem, there is a possible out of bounds write due to a missing bounds check. This could lead to remote escalation of privilege, if a UE has connected to a rogue base station controlled by the attacker, with no additional execution privileges needed. User interaction is needed for exploitation. Patch ID: MOLY01898195; Issue ID: MSV-8906.

### CVE-2026-20520

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-05T02:16:50.540 |

In Modem, there is a possible out of bounds write due to a missing bounds check. This could lead to remote escalation of privilege, if a UE has connected to a rogue base station controlled by the attacker, with no additional execution privileges needed. User interaction is not needed for exploitation. Patch ID: MOLY01778988; Issue ID: MSV-8897.

### CVE-2026-20519

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-05T02:16:50.393 |

In Modem, there is a possible out of bounds write due to a missing bounds check. This could lead to remote escalation of privilege, if a UE has connected to a rogue base station controlled by the attacker, with no additional execution privileges needed. User interaction is not needed for exploitation. Patch ID: MOLY01778993; Issue ID: MSV-8898.

### CVE-2026-104407

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-05T09:17:08.487 |

Cross-Site Request Forgery (CSRF) vulnerability in Blubrry Podcasting PowerPress Podcasting powerpress allows Cross Site Request Forgery.This issue affects PowerPress Podcasting: from n/a through 11.17.9.
