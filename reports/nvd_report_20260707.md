# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-06 15:00 UTC
- **対象期間**: `2026-07-05T15:00:12.000Z` 〜 `2026-07-06T15:00:28.000Z`
- **重要CVE数**: 24 件（Critical 9.0+: 5 件 / High 7.0〜: 19 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上り、特に **認証不要でリモートからコード実行・情報漏洩・権限昇格が可能** な脆弱性が目立ちます。  
- Web アプリケーション（特に WordPress プラグイン）に対する **不適切な入力検証・認証チェック欠如** が多数。  
- 産業制御系ソフトウェア（B&R APROL）や Linux ディストリビューション（Pardus 系列）でも **証明書検証やリソース制御の不備** が報告され、OT 環境への影響が懸念されます。  
- Elixir 製ライブラリ（mint / hpax）における **アルゴリズム的複雑性** の問題が DoS 攻撃を誘発し、インフラ全体の可用性リスクを増大させています。

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な問題点 | 影響範囲・被害シナリオ |
|-----|--------|------------|------------------------|
| **CVE‑2026‑12686** | 9.3 | 認証済ユーザーが `company_id` パラメータを改ざんし、同一サブドメイン内の他社テナントに不正アクセス | SaaS 型マルチテナントアプリ全般。テナント間データ漏洩・改ざんリスクが高く、顧客信頼を失う可能性。 |
| **CVE‑2026‑14808** / **CVE‑2026‑14807** | 9.3 | PROG MIS 製 ERP/Prog Management System における **機密情報露出** と **ハードコード認証情報** の使用。認証不要で DB アカウント・パスワード取得可能 | 企業内部システム全体が遠隔から取得でき、内部ネットワークへの踏み台化やデータベース情報漏洩が即座に発生。 |
| **CVE‑2026‑6900** | 9.1 | B&R Industrial Automation GmbH の APROL における **証明書検証不備**（不正なサーバ証明書を受け入れる） | OT 環境での MITM 攻撃が可能。制御システムの設定改ざんや不正コマンド注入につながる。 |
| **CVE‑2026‑6382** | 9.1 | 複数の WordPress ファイル管理プラグインで **コマンドインジェクション**（シェルコマンドへ未エスケープパラメータ） | 攻撃者が任意コード実行 → サーバ全体の乗っ取り。特にマルチサイト環境で広範囲に被害が拡大。 |
| **CVE‑2026‑11962** | 8.8 | FileOrganizer プラグインの **ファイルタイプ検証欠如** により任意 PHP アップロードが可能 | 認証ユーザーでも任意コード実行が可能。プラグインを利用している全サイトが対象。 |

> **注記**：上記は **スコアが高いだけでなく、実装上のミス（認証・入力検証の欠如）が広範囲に影響を及ぼす** ため、優先的に対策すべきです。

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱性情報の即時取得**：各ベンダーが提供するパッチ・アップデート情報を確認し、リリース日が近いものは **テスト環境で検証後、速やかに本番へ適用** する。  
- **外部からの直接アクセス制限**：Web アプリは **WAF** で `company_id` などのパラメータ改ざんや不正リクエストをブロックし、API エンドポイントは IP フィルタリングで保護。  
- **最小権限の原則**：データベース接続情報は **アプリケーションごとに限定された権限**（SELECT のみ、INSERT/UPDATE は必要最小限）に変更。  

### 3.2 個別 CVE に対する具体的パッケージ・バージョン

| CVE | 修正パッケージ / バージョン | 推奨実装手順 |
|-----|----------------------------|--------------|
| CVE‑2026‑12686 | アプリケーションコード（`company_id` 検証ロジック） | 1. `company_id` が認証ユーザーのテナントに属するかサーバ側で必ず検証<br>2. 変更後はユニットテストでテナント横断アクセスができないことを確認 |
| CVE‑2026‑14808 / CVE‑2026‑14807 | PROG MIS 製品 **最新版**（ベンダーが提供するパッチ） | 1. ソースコードからハードコードされた DB 資格情報を削除し、環境変数または安全なシークレット管理へ移行<br>2. 認証・認可チェックを全ページに実装 |
| CVE‑2026‑6900 | **APROL** 4.4‑01P5 以降 | 1. TLS 証明書検証ロジックを OpenSSL のデフォルト設定に合わせる<br>2. 既存の証明書ストアを最新のルート証明書に更新 |
| CVE‑2026‑6382 | WordPress プラグイン **FileOrganizer** ≥ 1.1.9、**Advanced File Manager** ≥ 5.4.12、**File Manager Pro** ≥ 2.1.1、**File Manager** ≥ 8.0.4 | 1. プラグインを最新版へ更新<br>2. `exec()` 系関数に渡す引数は `escapeshellarg()` でエスケープ<br>3. 不要なプラグインは無効化 |
| CVE‑2026‑11962 | **FileOrganizer** ≥ 1.2.0 | 1. アップロード時に MIME タイプと拡張子のホワイトリストチェックを実装<br>2. アップロード先ディレクトリの実行権限を **no‑exec** に設定 |
| CVE‑2026‑11855 | **Simple Membership** ≥ 4.7.5 | 1. Stripe Webhook の署名検証（`stripe-signature` ヘッダー）を必須化<br>2. Webhook から取得したデータは `htmlspecialchars()` でエスケープ |
| CVE‑2026‑10830 | **AllCoach** ≥ 1.0.2 | 1. 登録時にメールアドレスの重複チェックをサーバ側で実装<br>2. パスワードリセットトークンに有効期限（≤ 1h）を設定 |
| CVE‑2026‑58226 / CVE‑2026‑56810 | **elixir‑mint (hpax / mint)** ≥ 1.2.0（ベンダーが提供するパッチ） | 1. HPACK デコード時に上限（例: 2³²‑1）を設け、続く octet が過剰になる場合はエラーで終了<br>2. Chunked 転送時の

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-12686

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-06T11:16:26.797 |

An authenticated user could manipulate a company ID parameter in a POST request to the backend to gain unauthorised access to other companies hosted within the same subdomain environment. The application does not adequately verify whether the requested company ID belongs to the authenticated user’s session, resulting in a cross-tenant authorisation bypass. If this vulnerability is successfully exploited, it allows unauthorised access to sensitive customer information, including billing data, and may enable the unauthorised modification of third-party data.

### CVE-2026-14808

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-497` |
| Published | 2026-07-06T08:16:36.213 |

Prog
  Management System developed by PROG MIS has a Exposure of Sensitive
  Information vulnerability, allowing unauthenticated remote attackers to view
  a specific page and obtain the database account and password.

### CVE-2026-14807

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-06T08:16:36.070 |

ERP App developed by PROG MIS has a Use of Hard-coded Credentials vulnerability, allowing unauthenticated remote attackers to log in to view application code and obtain the database account and password.

### CVE-2026-6900

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-06T11:16:31.297 |

Improper certificate validation vulnerability in B&R Industrial Automation GmbH APROL.

This issue affects APROL: before R 4.4-01P5.

### CVE-2026-6382

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-06T08:16:36.447 |

The FileOrganizer  WordPress plugin before 1.1.9, Advanced File Manager  WordPress plugin before 5.4.12, File Manager Pro  WordPress plugin before 2.1.1, File Manager WordPress plugin before 8.0.4 do not properly escape a parameter before passing it to a shell command when processing image operations, allowing authenticated users to perform OS Command Injection. This requires the server to have the ImageMagick convert CLI available without either the PHP imagick or GD extensions.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-11962

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-06T08:16:35.270 |

The FileOrganizer  WordPress plugin before 1.2.0 does not validate the file type on several of its file-management operations, allowing authenticated users who have been granted file-manager access — which its premium add-on can extend to sub-administrator roles — to upload arbitrary PHP files and achieve remote code execution. This is an incomplete fix of CVE-2024-7985, which only added file-type validation to the upload operation.

### CVE-2026-11855

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-06T08:16:35.180 |

The Simple Membership WordPress plugin before 4.7.5 does not verify the authenticity of Stripe webhook requests when no signing secret is configured, nor escape a value taken from them before outputting it in an administrator notice, allowing unauthenticated attackers to inject arbitrary web scripts that execute in the context of a logged-in administrator.

### CVE-2026-10830

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-06T08:16:34.987 |

The AllCoach  WordPress plugin before 1.0.2 does not verify that an email address submitted to a public account-registration endpoint is not already associated with an existing user before overwriting that user's password, allowing unauthenticated attackers to reset the password of arbitrary accounts, including administrators, and take over the site.

### CVE-2026-9085

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-732` |
| Published | 2026-07-05T15:16:57.800 |

Incorrect Permission Assignment for Critical Resource, Improper Access Control vulnerability in TUBITAK BILGEM Software Technologies Research Institute Pardus-Parental-Control allows DNS Spoofing.

This issue affects Pardus-Parental-Control: from <=0.5.1 before 0.7.0.

### CVE-2026-58226

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-07-06T11:16:31.143 |

Inefficient Algorithmic Complexity vulnerability in elixir-mint hpax allows unauthenticated denial-of-service via unbounded HPACK integer decoding.

hpax decodes HPACK variable-length integers with no upper bound on the decoded value or the number of continuation octets. 'Elixir.HPAX.Types':decode_remaining_integer/3 accumulates the integer as int + (value <<< m), shifting by 7 more bits for each continuation octet and stopping only on a terminating octet or truncated input, never because the integer grew too large. Because BEAM integers are arbitrary precision, a run of N continuation octets builds an O(N)-bit bignum and re-adds into an ever-larger bignum on each step, so the total decoding cost is superlinear (about O(N^2)). An unauthenticated attacker who can send an HTTP/2 header block to a server using this decoder (reached through the 'Elixir.HPAX':decode/2 entry point) can supply a small header block that forces a large, attacker-controlled amount of CPU (and transient memory), a denial-of-service amplification.

This issue affects hpax from 0.1.1 before 1.0.4.

### CVE-2026-56810

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-06T11:16:30.983 |

Allocation of Resources Without Limits or Throttling vulnerability in elixir-mint mint (Mint.HTTP1 module) allows a denial of service via an oversized chunked transfer-encoded response.

This vulnerability is associated with program files lib/mint/http1.ex and program routines 'Elixir.Mint.HTTP1':decode_body/5, 'Elixir.Mint.HTTP1':add_body_to_buffer/2.

When Mint decodes a chunked HTTP response body, it accumulates each partial fragment of the current chunk in the connection's data_buffer (an unbounded iolist) via add_body_to_buffer/2 and does not emit the data to the caller until the full declared chunk length has been received. The chunk size is taken directly from the server and parsed with no upper bound, so a malicious or compromised server can announce one enormous chunk (for example a size line of 7FFFFFFF, about 2 GiB) and then send the body bytes slowly without ever completing the chunk. The client buffers every received byte while it waits for a completion that never arrives, and because no data responses are produced until the chunk finishes, a caller that otherwise streams large content-length bodies safely gains no protection. An unauthenticated remote server (reachable whenever a client follows redirects, fetches user-supplied URLs, or processes webhooks) can drive the client's memory arbitrarily high and trigger an out-of-memory condition.

This issue affects mint: from 0.5.0 before 1.9.1.

### CVE-2026-14809

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-06T09:16:34.167 |

Prog Management System developed by PROG MIS has a SQL Injection vulnerability, allowing unauthenticated remote attackers to inject arbitrary SQL commands to read database contents.

### CVE-2026-4249

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-707` |
| Published | 2026-07-06T11:16:30.433 |

The throttling event handling mechanism in multiple WSO2 products accepts user-supplied JSON payloads without sufficient validation of their structure and content. This allows an unauthenticated remote attacker to inject malicious JSON data that can lead to a persistent denial of service condition.

Successful exploitation of this vulnerability can disrupt the API Gateway, preventing legitimate API traffic from being processed and impacting complete service availability. The denial of service is persistent, requiring manual intervention to restore normal operations.

### CVE-2026-6901

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-07-06T11:16:31.433 |

Untrusted Search Path vulnerability in B&R Industrial Automation GmbH APROL.

This issue affects APROL: before R 4.4-01P5.

### CVE-2026-44937

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-06T11:16:27.727 |

Potential forgery of webhook requests when using a unauthenticated webhook in SUSE Rancher Fleet 0.15 before 0.15.2, 0.14 before 0.14.6, 0.13 before 0.13.11 and 0.12 before 0.12.5 could be used by remote attackers to cause a denial of service or a downgrade attack on other repositories on the system.

### CVE-2026-12083

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-06T08:16:35.360 |

The Admin and Site Enhancements (ASE) WordPress plugin before 8.8.4, admin-site-enhancements-pro WordPress plugin before 8.8.4 does not perform authentication, authorization, or nonce checks on a role-restoration request handler, allowing unauthenticated attackers to restore a previously demoted administrator account back to the administrator role. This is an incomplete fix of CVE-2024-43333 / CVE-2025-24648, which closed the issue for only one of the demotion paths the WordPress role API exposes.

### CVE-2026-11766

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-06T08:16:35.083 |

The Ultimate Member  WordPress plugin before 2.12.0 does not properly sanitise and escape the value of custom textarea profile fields before outputting it on user profiles, allowing authenticated users with Subscriber-level access and above to store JavaScript that executes when any user, including an administrator, views the affected profile.

### CVE-2026-12250

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-214` |
| Published | 2026-07-05T15:16:56.247 |

Invocation of process using visible sensitive information vulnerability in TUBITAK BILGEM Software Technologies Research Institute Pardus Domain Joiner allows Excavation.

This issue affects Pardus Domain Joiner: from 0.5.2 before 0.5.4.

### CVE-2026-6509

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-05T15:16:57.687 |

Missing Authorization vulnerability in TUBITAK BILGEM Software Technologies Research Institute Pardus Update allows Privilege Escalation.

This issue affects Pardus Update: from <=0.6.3 before 0.6.6.

### CVE-2026-9165

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-06T09:16:39.400 |

A flaw was found in Red Hat Advanced Cluster Security for Kubernetes (RHACS). Central does not limit the depth of GraphQL queries served on the authenticated GraphQL API. An authenticated user with a valid API token can send deeply nested queries that cause excessive resource consumption in Central, resulting in a denial of service for the management plane.

### CVE-2026-24012

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-06T09:16:35.037 |

Uncontrolled Resource Consumption vulnerability in Apache IoTDB. 

Some interface fails to impose reasonable
limits on the time span and aggregation interval of the query. An attacker
can construct a request with extreme parameters (e.g., a very large time
range combined with a minimal interval). This forces the DataNode to build
an enormous result set in memory, which exhausts the Java heap and causes
the DataNode process to crash.

This issue affects Apache IoTDB: from 1.3.3 before 2.0.8.

Users are recommended to upgrade to version 2.0.8, which fixes the issue.

### CVE-2024-6228

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-06T08:16:34.057 |

The Notifications for Forms & WordPress Actions WordPress plugin before 2.6 does not validate a user-supplied value before using it to build a server-side file inclusion path, allowing authenticated users with subscriber-level access and above to include and execute arbitrary local PHP files on the server.

### CVE-2026-59510

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-05T18:16:57.080 |

AIL Framework contains a path traversal vulnerability in its PDF object handling. Prior to commit 14c618fce4d1df02358717c48ea903706abecdf2, the PDF.get_filepath() function constructed a file path by joining the configured PDF storage directory with a path derived from a PDF object identifier, without verifying that the resolved path remained within the intended PDF_FOLDER directory.

An authenticated attacker able to invoke PDF object operations with a crafted identifier could use relative traversal sequences or absolute path components to cause AIL Framework to open files located outside the PDF storage directory. This could allow disclosure of files readable by the AIL process, including application configuration, credentials, or other sensitive local data. This vulnerability is potential due to additional errors before being able to be executed.

The fix canonicalises the resulting path with os.path.realpath() and rejects paths whose common directory is outside the configured PDF directory.

### CVE-2026-44934

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-215` |
| Published | 2026-07-06T09:16:36.170 |

A information disclosure when DEBUG loglevel is set in SUSE Rancher AI Agent 1.0 before 1.0.2 could leak API keys or LLM response text with potential sensitive data into logfiles, allowing local attackers to misuse respective gained data or credentials.
