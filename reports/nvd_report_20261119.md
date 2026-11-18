# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-18 15:00 UTC
- **対象期間**: `2026-11-17T15:00:48.000Z` 〜 `2026-11-18T15:00:47.000Z`
- **重要CVE数**: 641 件（Critical 9.0+: 122 件 / High 7.0〜: 519 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS 7.0 以上は **70 件超** と非常に多く、特に **リモートから認証不要で完全権限取得が可能** な脆弱性が目立ちます。  
- **Oracle Fusion Middleware 系列**（WebLogic、Access Manager、AutoVue など）が集中しており、同一コンポーネント（TopLink Integration、Core）に対する複数の 10.0 判定脆弱性が同時に報告されています。  
- エンタープライズ向け製品だけでなく、**IoT/組み込み系（Mosquitto）やオープンソース監視系（ZoneMinder）・CMS プラグイン（WordPress）** でも認証バイパスや任意コード実行が多数報告され、攻撃対象が広範囲に拡大しています。  

---

## 2. 特に注目すべき CVE  

| CVE | 理由（注目ポイント） | 影響範囲・被害シナリオ |
|-----|----------------------|------------------------|
| **CVE‑2026‑95787** (CVSS 10.0) | AOS‑10 の PAPI プロトコルに認証回避ロジックが存在。<br>**認証不要**で管理者権限取得、設定変更、機密データ閲覧が可能。 | AOS‑10 を導入している組織のネットワーク境界が外部に露出している場合、即座に全権限取得される危険性がある。 |
| **CVE‑2026‑114202** (CVSS 10.0) | ASUS Control Center Express にハードコードされた暗号鍵が残存。<br>偽造トークンで **管理者権限** を取得できる点が深刻。 | ASUS の管理ソフトを社内 PC にインストールしている全環境が対象。特にリモートデスクトップや VPN 経由での攻撃が想定される。 |
| **CVE‑2026‑91569** (CVSS 10.0) | Oracle WebLogic Server（TopLink Integration）に **ネットワーク経由のリモートコード実行** が可能。<br>複数バージョン（12.2.1.4.0、14.1.1.0.0、14.1.2.0.0、15.1.1.0.0）で共通。 | WebLogic を外部に公開している企業は、攻撃者が任意のシェルコードを実行し、内部ネットワーク横移動やデータ窃取が可能になる。 |
| **CVE‑2026‑110811** (CVSS 9.8) | WordPress 用 **Trust Payments Gateway** プラグインが認証バイパス。<br>`new_customer_account()` が生の WP ユーザー作成結果を返すため、**任意アカウント作成** が可能。 | e‑コマースサイトでこのプラグインを使用している全サイトが対象。攻撃者は管理者権限に昇格できる可能性がある。 |
| **CVE‑2026‑28273** (CVSS 9.9) | ZoneMinder の `/api/configs/edit/{name}.json` が **認可チェック不足**。<br>認証済みユーザーでもシステム設定を書き換えられる。 | 監視カメラ映像を管理するインフラで、設定改ざんにより映像取得停止や不正録画が発生するリスク。 |

> **注**：上記は *CVSS 10.0* が多い Oracle 系列と、実務で直ちに影響が出やすい *組み込み・CMS* 系列をバランスよく選出しています。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ（必須）

| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン / パッチ |
|-------------------|-------------------|------------------------|
| **AOS‑10** (PAPI) | すべてのリリース（脆弱箇所はプロトコル実装） | ベンダー提供の **Security Update for AOS‑10 (2026‑Q4)** を即適用 |
| **ASUS Control Center Express** | すべてのバージョン（ハードコード鍵が残存） | **CCEX v2.5.1** 以降（2026‑03 リリース） |
| **Oracle WebLogic Server** | 12.2.1.4.0、14.1.1.0.0、14.1.2.0.0、15.1.1.0.0 | Oracle Critical Patch Update **2026‑04**（WebLogic 12.2.1.4.0 Patch #345**, 14.1.1.0.0 Patch #342**, 14.1.2.0.0 Patch #340**, 15.1.1.0.0 Patch #338**） |
| **Trust Payments Gateway for WooCommerce** | ≤ 1.3.8 | **1.3.9** 以降（2026‑05 リリース） |
| **Unzer Payments** (参考) | ≤ 2.2.1 | **2.2.2** 以降 |
| **ZoneMinder** | < 1.38.4 | **1.38.4** 以上 |
| **Eclipse Mosquitto** | 2.1.0 – 2.1.2 | **2.1.3** 以上 |
| **WeGIA** | < 3.8.7 | **3.8.8** 以上 |
| **Rucio** | 1.14.0 – 41.1.1 | **41.2.0** 以上 |
| **Oracle Database Server (Text / RDBMS)** | 19.3‑19.33、21.3‑21.24、23.4.0‑23.26.4 | **23.4.0‑23.27.0** 以降のパッチセット（2026‑CPU） |
| **Oracle AutoVue** | 21.1.0 | **21.1.1** 以降 |
| **Oracle Hyperion Financial Management** | 11.2.26.0.000 | **11.2.27.0.001** 以降 |

> **※** パッチ適用前に必ずバックアップを取得し、ステージング環境で動作確認を行ってください。

### 3.2 設定・運用面の緊急対策

1. **外部公開ポートの遮断**  
   - WebLogic、AutoVue、Oracle Text などは **T3 / HTTP / HTTPS** が外部から直接到達しないよう、ファイアウォールで制限。  
2. **最小

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-95787

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-18T14:17:45.533 |

Vulnerabilities in the PAPI protocol of AOS-10 could allow an unauthenticated remote attacker to circumvent existing authentication controls. Successful exploitation could allow an attacker to gain administrative access, modify system configurations, and access or manipulate sensitive data.

### CVE-2026-114202

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-18T02:17:39.713 |

Use of Hard-coded Cryptographic Key in ASUS Control Center Express allows a remote user to gain administrative privileges via a forged authentication token.
Refer to the '
Security Update for ASUS Control Center Express Agent  ' section on the ASUS Security Advisory for more information.

### CVE-2026-91569

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:24.980 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: TopLink Integration).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebLogic Server.  While the vulnerability is in Oracle WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-91510

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:22.823 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Access Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Access Manager. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L).

### CVE-2026-91500

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:22.467 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Access Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Access Manager. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L).

### CVE-2026-114835

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:11.710 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Admin Console).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-114824

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:10.373 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Platform Security for Java.  While the vulnerability is in Oracle Platform Security for Java, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-114784

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:05.783 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  While the vulnerability is in Oracle Business Intelligence Enterprise Edition, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-100397

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-17T20:17:35.207 |

Rucio is a scientific data management framework. From 1.14.0 until 35.9.1, 38.6.1, 40.4.2, and 41.1.1, validate_auth_token in lib/rucio/core/authentication.py does not distinguish short-lived SSH challenge nonces from authentication tokens stored in the same token table. An unauthenticated attacker can request /auth/ssh_challenge_token for an arbitrary account by supplying X-Rucio-Account, then present the returned X-Rucio-SSH-Challenge-Token as X-Rucio-Auth-Token to authenticate to other API endpoints as that account, including an administrative account. This issue is fixed in versions 35.9.1, 38.6.1, 40.4.2, and 41.1.1.

### CVE-2026-114980

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:28.903 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security Related Issues).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle AutoVue.  While the vulnerability is in Oracle AutoVue, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-114978

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:28.660 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-114848

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:13.277 |

Vulnerability in the Oracle Text component of Oracle Database Server.  Supported versions that are affected are 19.3-19.33, 21.3-21.24 and  23.4.0-23.26.3. Easily exploitable vulnerability allows low privileged attacker having Create Session privilege with network access via Oracle Net to compromise Oracle Text.  While the vulnerability is in Oracle Text, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Text. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-114822

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:10.103 |

Vulnerability in the RDBMS component of Oracle Database Server.  Supported versions that are affected are 23.4.0-23.26.4. Easily exploitable vulnerability allows low privileged attacker having Create Session privilege with network access via Oracle Net to compromise RDBMS.  While the vulnerability is in RDBMS, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of RDBMS. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-114819

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:09.980 |

Vulnerability in the Oracle Text component of Oracle Database Server.  Supported versions that are affected are 19.3-19.32, 21.3-21.24 and  23.4.0-23.26.3. Easily exploitable vulnerability allows low privileged attacker having Create Session privilege with network access via Oracle Net to compromise Oracle Text.  While the vulnerability is in Oracle Text, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Text. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-28273

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T19:18:00.103 |

ZoneMinder is a free, open source closed-circuit television software application. Prior to 1.38.4, any authenticated user can use the /api/configs/edit/{name}.json endpoint to modify protected configuration settings because ConfigsController::edit() does not enforce the System=Edit authorization requirement and its system-variable protection is ineffective. An attacker can set ZM_PATH_FFMPEG to a command-bearing value and trigger an exec() sink in web/views/image.php or web/includes/Event.php by requesting frame extraction. This permits arbitrary command execution with the privileges of the web server user and can expose private camera feeds, recordings, and database data or establish persistence. This issue is fixed in version 1.38.4.

### CVE-2026-110811

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-18T14:17:26.020 |

The Trust Payments Gateway for WooCommerce (JavaScript Library) plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 1.3.8. The vulnerability exists because the `new_customer_account()` function stores the raw return value of `wp_create_user()` — including a `WP_Error` object returned on username collision — into the order's `tp_userid` post meta before the `is_wp_error()` guard is evaluated; the `add_customer_details_to_thankyou_page()` callback subsequently reads that meta and casts it with `(int)`, causing PHP to coerce any object to integer `1`, after which `wp_set_current_user(1)` and `wp_set_auth_cookie(1)` are called unconditionally. This makes it possible for unauthenticated attackers to authenticate as WordPress user ID 1 — the bootstrap site administrator or, on multisite, a network super-admin — by supplying the `new_username` parameter matching any existing login during checkout and visiting the resulting thank-you page. Exploitation requires the Trust Payments gateway to be active and the attacker to complete a paid order on their own account; the ID 1 administrator username is additionally enumerable via standard WordPress user enumeration techniques.

### CVE-2026-110009

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-18T14:17:25.860 |

The Unzer Payments plugin for WordPress is vulnerable to Authentication Bypass leading to Account Takeover in all versions up to, and including, 2.2.1. The vulnerability exists because the Google Pay Express Checkout endpoint (`/?wc-api=google_pay_express`), handled by `startCheckoutDataWithNormalizedCustomerData`, accepts an attacker-controlled `paymentData.email` value and passes it to `createOrGetGuestCustomer()`, which resolves the submitted email to any existing WordPress user via `get_user_by('email', ...)` and then calls `wp_set_current_user()` and `wp_set_auth_cookie()` for the resolved user ID without verifying ownership of the email address, a password, a nonce, an authentication token, or any proof of payment from the payment provider. This makes it possible for unauthenticated attackers to log in as any existing WordPress user — including administrators — by submitting that user's known email address, receiving valid `wordpress_logged_in_*` session cookies for the targeted account and achieving full site takeover. The endpoint is entirely unprotected with no capability check, nonce validation, or payment-provider signature verification applied, and administrator email addresses are frequently discoverable via the WordPress REST API user enumeration endpoint (`/wp-json/wp/v2/users`), author archive pages, Gravatar lookups, or site contact footers.

### CVE-2026-110486

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191;CWE-787;CWE-908` |
| Published | 2026-11-18T11:17:37.963 |

In Eclipse Mosquitto versions 2.1 through 2.1.2, a listener configured with `protocol websockets` mishandles empty WebSocket data frames. `net__read_ws()` in `lib/net_ws.c` returns the number of framing bytes consumed (the 4 masking-key bytes) for a data frame with a zero-length payload, without writing any bytes to the caller’s buffer. The MQTT packet reader in `packet__read_single()` (`lib/packet_mosq.c`) trusts that return value as a payload byte count. A remote client can therefore advance the read position over an uninitialised heap allocation, causing the broker to process and forward uninitialised heap memory (information disclosure, including heap and libc pointers), and can underflow the unsigned `to_process` counter so that subsequent attacker-controlled frame data is written past the end of the allocation (heap out-of-bounds write). The out-of-bounds write is reachable from the CONNECT packet before any authentication check, so an unauthenticated client can corrupt the heap and crash the broker even when `allow_anonymous false` is set. Combining the disclosure and the write allows remote code execution as the broker’s user by any client able to establish a session.

### CVE-2026-91585

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:19:25.783 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: TopLink Integration).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-91583

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:19:25.663 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: TopLink Integration).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-91570

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:19:25.097 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: TopLink Integration).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-91470

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:19:22.223 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-91456

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-17T22:19:21.990 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61680

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:19:20.367 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.6, web/html/socio/sistema/cadastro_cobrancas_geracao.php performs privileged charge-generation operations without checking for an authenticated session. An unauthenticated remote requester who supplies valid charge-generation parameters can create arbitrary charge records, enabling financial record manipulation and large-scale billing corruption. This issue is fixed in version 3.8.6.

### CVE-2026-61677

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T22:19:20.193 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.7, web/html/socio/sistema/processa_edicao_socio.php updates member information without validating an authenticated session. An unauthenticated remote requester who supplies a target member identifier and replacement member fields can modify arbitrary member records, corrupt personal information, and cause loss of data integrity. This issue is fixed in version 3.8.7.

### CVE-2026-61676

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T22:19:20.023 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.7, web/html/socio/sistema/cadastro_cobranca.php creates billing records without checking for an authenticated session. An unauthenticated remote requester who supplies valid billing parameters can create arbitrary billing entries, enabling financial data manipulation and operational disruption. This issue is fixed in version 3.8.7.

### CVE-2026-61675

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T22:19:19.797 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.7, web/html/socio/sistema/atualiza_pagamentos.php performs payment-status database updates without checking whether the requester has an authenticated session. An unauthenticated remote requester can supply a payment identifier, payment date, and paid value to mark arbitrary payment records as paid or otherwise modify payment information, causing financial record corruption. This issue is fixed in version 3.8.7.

### CVE-2026-127327

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:56.737 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127326

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:56.613 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127325

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:56.490 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127324

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:56.377 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115089

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:41.757 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Application Development Framework).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Planning. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115086

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:41.407 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via RMI to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Planning. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115080

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:40.703 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115048

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:36.870 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115047

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:36.760 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114925

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:22.387 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: REST Services).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Framework. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114924

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:22.273 |

Vulnerability in the Oracle Application Object Library product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Application Object Library.  Successful attacks of this vulnerability can result in takeover of Oracle Application Object Library. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114880

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:16.987 |

Vulnerability in the Document Management and Collaboration product of Oracle E-Business Suite (component: Attachments).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Document Management and Collaboration.  Successful attacks of this vulnerability can result in takeover of Document Management and Collaboration. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114863

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:14.940 |

Vulnerability in the Oracle Universal Work Queue product of Oracle E-Business Suite (component: Media Integration issues).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Universal Work Queue.  Successful attacks of this vulnerability can result in takeover of Oracle Universal Work Queue. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114850

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:13.510 |

Vulnerability in Oracle APEX (component: General).  Supported versions that are affected are 24.1.22, 24.2.21, 26.1.5 and  26.2.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle APEX.  Successful attacks of this vulnerability can result in takeover of Oracle APEX. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114849

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:13.393 |

Vulnerability in Oracle APEX (component: General).  Supported versions that are affected are 24.1.22, 24.2.21, 26.1.5 and  26.2.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle APEX.  Successful attacks of this vulnerability can result in takeover of Oracle APEX. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114826

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:10.630 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-69157

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T21:18:12.620 |

Atomic Server is an open source headless CMS and real-time database. From 0.29.0 to 0.40.2, Atomic Server provisions a well-known /setup invite with write enabled, the Drive root as its target, and usagesLeft set to one. construct_invite_redirect in server/src/plugins/invite.rs discards the redeemer identity, so an unauthenticated request containing an attacker-controlled public-key can create a new Agent and grant it write access to the entire Drive. On a fresh, unclaimed deployment, this permits reading, modifying, or deleting resources, changing permissions, and creating or altering Agents. No complete fixed version was verified as of this review.

### CVE-2026-130801

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T17:18:05.647 |

The device's command parser does not require asymmetric cryptographic signatures to validate incoming APDU packets. This enables an attacker to inject forged, unauthorized commands to manipulate device features and configurations once the initial handshake is bypassed.

### CVE-2026-122147

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-17T16:17:40.643 |

ICRTouch PocketTouch version 1.700 build 2025.3726 defines hard-coded default values for multiple credential fields, including a socket password and configuration and shutdown passwords. An additional email-related password field is initialized without a value.

### CVE-2026-122142

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-17T16:17:40.287 |

ICRTouch Commander administrative login interface does not adequately restrict repeated authentication attempts. The interface also returns distinguishable responses for multiple authentication states, including different behavior when a `siteID` value is supplied.

### CVE-2026-122055

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-17T16:17:39.663 |

ICRTouch PocketTouch version 1.700 build 2025.3726 contains a default socket password set to the literal value password. Where the default value remains unchanged and is accepted by a TouchPoint POS terminal, an attacker with network access to the terminal’s socket service may authenticate using publicly known credentials.

### CVE-2026-91561

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:24.533 |

Vulnerability in the Oracle Service Bus product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via RMI to compromise Oracle Service Bus.  While the vulnerability is in Oracle Service Bus, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Service Bus accessible data as well as  unauthorized access to critical data or complete access to all Oracle Service Bus accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-114856

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:14.213 |

Vulnerability in Oracle REST Data Services (component: General).  Supported versions that are affected are 24.2.0-26.3.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle REST Data Services.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle REST Data Services, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle REST Data Services. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-114785

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:05.907 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Planning.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Planning, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Planning. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-131088

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-17T21:18:08.687 |

Improper input validation in WebAppInstalls in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-131077

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-17T21:18:07.363 |

Out of bounds write in Tint in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-131061

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-17T21:18:05.430 |

Buffer overflow in Color in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-131057

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-17T21:18:04.947 |

Out of bounds read in ANGLE in Google Chrome on on Android prior to 158.0.8127.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131054

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-17T21:18:04.570 |

Out of bounds write in ANGLE in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-131031

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-17T21:18:00.920 |

Out of bounds write in GPU in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-131025

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-17T21:18:00.137 |

Out of bounds read in ANGLE in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130996

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-17T21:17:56.463 |

Out of bounds write in ANGLE in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130994

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:56.223 |

Use after free in WebGL in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130971

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-17T21:17:53.400 |

Out of bounds write in ANGLE in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130910

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-17T21:17:45.100 |

Protection mechanism failure in ANGLE in Google Chrome on on Android prior to 158.0.8127.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-129961

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-18T13:17:26.990 |

LMS (Lan Management System) is vulnerable to Remote Code Execution in its e-mail-based Helpdesk ticket intake. The mail parser does not reject Apache .htaccess configuration files or PHP-executable files when saving ticket attachments. A remote unauthenticated attacker can e-mail a Helpdesk ticket with such an attachment; in the default configuration, anyone can request the uploaded file's URL which executes attacker-supplied code with the privileges of the web server process. No operator interaction or LMS client session is required.


The issue was fixed in commit d5059b1.

### CVE-2026-19707

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-18T10:16:55.237 |

A bug in the Airlock Gateway (8.5.2 and earlier, and 8.6.0)  allows attacker-controlled HTML in a backend response to exploit the Smart Form Protection feature, possibly leading to a Denial of Service (DoS) or Remote Code Execution (RCE) attack against the Airlock Gateway. The issue has been fixed in Airlock Gateway version 8.5.3 and 8.6.1.

For an attack to be executable, the Airlock Gateway needs to have 'Smart Form Protection' (or the corresponding expert settings) enabled on a mapping whose backend returns a response containing certain multi-byte HTML character references. The buffer overflow then happens during the parsing of that HTML response. Such a response can come either from a malicious or compromised backend, or from an otherwise trusted backend that returns attacker-supplied HTML, e.g. an application that stores and serves plain user-provided HTML files.

Successfully exploiting the vulnerability can enable an attacker to perform a DoS attack or, in the worst case, an RCE attack against the Airlock Gateway in front of the affected backend. Compromising the functionality of the Airlock Gateway could in this way also affect the availability and protection of other well-intentioned backends deployed behind the same Gateway.

### CVE-2026-127143

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-18T13:17:25.153 |

LMS (Lan Management System) is vulnerable to privilege escalation in the lmsd daemon. The daemon loads the libraries listed in the LMS database without checking that they come from a trusted location. An attacker with access to the web server process or with write access to the LMS database can register a malicious library and trigger a configuration reload, causing lmsd to load and execute it. Because the example systemd unit does not set a separate user, lmsd runs as root, allowing the attacker to execute arbitrary code with root privileges.
This issue was fixed in commit 89dd3f7. The lmsd component was removed. For existing installations that use lmsd, the recommended solution is to disable and remove this component.

### CVE-2026-130706

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T12:17:15.490 |

NocoDB before 2026.09.0 contains an sql injection vulnerability that allows authenticated Creator or Owner users to inject raw SQL by persisting a crafted formula parsed_tree reused without revalidation. Attackers can bypass the SQLite metadata path guard with an alias to plant the tree, escalating to super administrator or executing OS commands on external PostgreSQL hosts.

### CVE-2026-130682

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-18T12:17:11.990 |

SiYuan before 3.8.10 persists a table block's caption attribute into IAL properties without HTML sanitization, causing stored cross-site scripting upon import or sync. Attackers can inject an entity-encoded caption with an onerror handler that executes in the Electron client's nodeIntegration context to achieve remote code execution.

### CVE-2026-130681

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:11.817 |

SiYuan before 3.8.10 contains a stored cross-site scripting vulnerability, an incomplete fix for CVE-2026-44670, because renderAVAttribute() inserts an Attribute View name unescaped into the database row attribute panel header. Attackers who can persist the name, such as via the setAttrViewName action, can inject an onerror handler that runs OS commands through Node.js when a desktop user opens the panel.

### CVE-2026-130680

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:11.630 |

SiYuan from 3.3.0 before 3.8.10 contains a stored cross-site scripting vulnerability that allows attackers to inject HTML via unescaped checkbox column names in Gallery and Kanban AttributeView renderers. Attackers can share a crafted .sy.zip document whose rendering in the Electron desktop client with nodeIntegration enabled executes Node.js and host OS commands.

### CVE-2026-130679

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:11.450 |

SiYuan before 3.8.10 contains a stored cross-site scripting vulnerability in genAVValueHTML() that allows attackers who can store Attribute View asset values to inject script through an unescaped image src attribute. Attackers can store an image URL containing a double quote and onerror handler that executes OS commands via Node.js in the desktop app when victims open the bound note or row attribute panel.

### CVE-2026-130678

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:11.277 |

SiYuan before 3.8.10 contains a stored cross-site scripting vulnerability that allows attackers to execute script by storing malicious Attribute View column names rendered unescaped in col.ts. Attackers can inject HTML via addAttributeViewKey, .sy.zip import, or sync, and when a victim adds or duplicates the column, insertAdjacentHTML runs JavaScript with Node.js privileges for desktop code execution.

### CVE-2026-126574

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-18T02:17:40.657 |

Missing authorization vulnerability in ASUS Control Center Datacenter and Control Center Enterprise allows remote authenticated users with a low-privileged Viewer role to change the password of an Administrator account, thereby obtaining administrative privileges, via a crafted password update request. 
Refer to the '
Security Update for ASUS Control Center  ' section on the ASUS Security Advisory for more information.

### CVE-2026-114205

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-18T02:17:39.980 |

Incorrect authorization in ASUS Control Center Express allows a remote authenticated user with a low-privileged role to create an administrator account, resulting in administrative control of the management console and of the clients it manages.
Refer to the '
Security Update for ASUS Control Center Express Agent  ' section on the ASUS Security Advisory for more information.

### CVE-2026-91469

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:22.107 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebLogic Server accessible data as well as  unauthorized read access to a subset of Oracle WebLogic Server accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle WebLogic Server. CVSS 3.1 Base Score 9.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H).

### CVE-2026-130735

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:20.010 |

Grav from 2.0.0 before 2.2.18 contains a Twig injection vulnerability that allows media-only accounts and anonymous uploaders to execute Twig by placing delimiters in image titles, alt text, class, id, or file names. Attackers can combine injected Twig with the autoescape tag to serve script to every page visitor, including super admins, or expose unpublished page content.

### CVE-2026-130733

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-140` |
| Published | 2026-11-18T12:17:19.627 |

Grav from 2.0.0 before 2.2.18 contains an authorization bypass vulnerability that allows publishers to overwrite pages their per-page permissions deny by abusing FolderStorage key delimiter collisions and PageStorage folder reconstruction. Attackers can rename a folder like locked*** or save from a page with an unusual prefix width through a front-end Flex pages form, replacing protected content and permissions to access the protected subtree.

### CVE-2026-130730

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-18T12:17:19.130 |

NocoDB before 2026.10.1 contains an authentication bypass vulnerability that allows OAuth token holders to act as full sessions because OAuth access tokens are signed with the instance JWT secret. Attackers can present a narrowly scoped OAuth token to the session strategy, short-lived-token exchange, or NocoSocket handshake to gain the granting user's full privileges.

### CVE-2026-130716

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:17.010 |

NocoDB before 2026.08.0 contains a stored cross-site scripting vulnerability that allows authenticated Creator or Editor users to execute script by injecting markup into fields rendered through URL() formulas. The canvas grid renderer assigns unsanitized formula output to innerHTML, letting attackers steal session tokens from localStorage and take over accounts of users viewing the table.

### CVE-2026-130712

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T12:17:16.390 |

NocoDB before 2026.08.1 contains an authorization bypass vulnerability that allows authenticated Creators to access another tenant's external database by reusing a victim source id when adding a source. Because NcConnectionMgrv2 caches connections by bare source id, attackers can reflect the victim's cached database schema and read, update, and insert records through their own base models.

### CVE-2026-130683

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T12:17:12.160 |

SiYuan before 3.8.10 uses an incomplete deny-list in IsSensitivePath that omits shell-initialization files such as .zshenv and .bash_profile, as well as ~/.local. Authenticated administrators can call /api/file/copyFile with an absolute destination outside the workspace to write payloads there, which execute as the user on the next shell or login.

### CVE-2026-130675

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-697` |
| Published | 2026-11-18T12:17:10.783 |

Craft CMS from 5.0.0 before 5.11.4 contains a remote code execution vulnerability in ImageTransforms::normalizeTransform() that allows attackers to instantiate arbitrary classes by supplying class:null with a __class key. Attackers can reach the method through Craft Commerce's payments/pay redirect template calling customer.photo.getUrl() with a crafted transform to instantiate classes like yii\rbac\PhpManager and execute PHP.

### CVE-2026-130674

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-18T12:17:10.403 |

Craft CMS from 5.0.0 before 5.11.4 contains an incomplete blocklist fix that allows attackers who can author entry type title formats to write arbitrary files using ZipArchive or XMLWriter classes. Attackers can abuse the non-sandboxed renderObjectTemplate() renderer to write attacker-controlled content into the web docroot, achieving remote code execution.

### CVE-2026-130650

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:06.260 |

WWBN AVideo through c3edcc274c389816d434acadac07ee78eaf330c1 contains a cross-site scripting vulnerability because the default node socket server relays autoEvalCodeOnHTML without the PHP-only filter. Unauthenticated attackers can obtain an anonymous socket token and send a spoofed MSG_BATCH message to trigger client eval() in administrators' browsers for account takeover.

### CVE-2026-130648

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:05.910 |

WWBN AVideo from 6.5 contains a stored cross-site scripting vulnerability that allows users with upload permission to inject script by submitting a javascript: scheme videoLink for embed videos. The unvalidated URL is rendered into an iframe src in videoEmbeded.php and PlayerSkins.php, executing for viewers including administrators and enabling creation of new administrator accounts.

### CVE-2025-59907

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-18T11:17:36.947 |

Hardcoded credentials in the executable file. These can be extracted using the “Strings.exe” tool and could allow an attacker unauthorized access to the database and SMTP server.

### CVE-2025-59906

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-18T11:17:35.497 |

Hardcoded credentials in the executable file. These can be extracted using the “Strings.exe” tool and could allow an attacker unauthorized access to the database and SMTP server.

### CVE-2026-131852

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-11-18T00:18:43.127 |

OwnTracks Recorder before 1.0.5 contains a format string vulnerability in json_response() and related output functions that allows unauthenticated attackers to execute code by storing a malicious tid value. Attackers can publish locations via POST /pub or MQTT with printf specifiers in tid, then read them back through GET /api/0/last to leak addresses and write memory.

### CVE-2026-91507

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:22.587 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Access Manager accessible data as well as  unauthorized read access to a subset of Oracle Access Manager accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:N).

### CVE-2026-115139

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:47.437 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-114956

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:26.023 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Planning.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Planning, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Planning accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Planning accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-114934

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:23.437 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Integration Broker).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  While the vulnerability is in PeopleSoft Enterprise PeopleTools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data as well as  unauthorized update, insert or delete access to some of PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-101691

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:04.460 |

Vulnerability in the Oracle Mobile Field Service product of Oracle E-Business Suite (component: Admin UI).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Mobile Field Service.  While the vulnerability is in Oracle Mobile Field Service, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Mobile Field Service accessible data as well as  unauthorized update, insert or delete access to some of Oracle Mobile Field Service accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-130856

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T20:17:51.240 |

53AIHub before 0.5.5 contains a missing authentication vulnerability that allows remote unauthenticated attackers to reinitialize installed instances by calling the public POST /api/init endpoint. Attackers can reset an existing account's password, assign the top creator role, and obtain an access token to take over accounts and use admin-only API routes.

### CVE-2026-130849

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-17T20:17:50.113 |

BZFlag bzfs before 2.4.32 contains a heap out-of-bounds write vulnerability in NetHandler::tcpReceive() that allows remote unauthenticated attackers to corrupt heap memory by sending a TCP message with a body length of exactly 1024. Attackers can overwrite the tcplen receive offset with a negative value to write controlled bytes before the buffer, crashing the server or executing commands as the bzfs user.

### CVE-2026-130840

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-17T20:17:48.737 |

BISHENG before 3.0.0 contains an authentication bypass vulnerability that allows unauthenticated remote attackers to impersonate administrators by abusing a hard-coded default jwt_secret used by AuthJwt. Attackers can forge an HS256 token offline naming user_id 1 with the admin role, send it as access_token_cookie, and gain full administrative access to users, workspaces, knowledge bases and workflows.

### CVE-2026-119293

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-17T20:17:36.417 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. In 1.11.2 and earlier, rtp_common_read() in src/switch_rtp.c uses one session-wide autoadj_tally to learn RTP sources that differ from the address negotiated in SDP. An unauthenticated remote attacker who sends plaintext RTP during call setup can make packets from one or more non-advertised sources reach the threshold before the legitimate endpoint, causing FreeSWITCH to adopt the source of the threshold-crossing packet as the media peer. The attacker can then receive call audio, inject media, and deny media to the legitimate endpoint without being on the media path. FreeSWITCH 1.11.2 adds two opt-in controls, but both default to zero and the release remains affected unless both are configured before RTP session creation. This vulnerability is fixed in 1.11.2.

### CVE-2026-126553

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-17T17:17:59.527 |

Deserialization of Untrusted Data vulnerability in Broadcom AutoSys Workload Automation (Workload Control Center (WCC) modules) on Windows, Linux allows Object Injection.This issue affects AutoSys Workload Automation: from 12.1 through 24.0.01.

### CVE-2026-126552

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-306` |
| Published | 2026-11-17T17:17:59.400 |

Missing Authentication for Critical Function, OS Command Injection vulnerability in Broadcom AutoSys Workload Automation (Workload Control Center (WCC) modules) on Windows, Linux allows OS Command Injection.This issue affects AutoSys Workload Automation: from 12.1 through 24.0.01.

### CVE-2026-126551

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-17T17:17:59.260 |

Use of Hard-coded Cryptographic Key vulnerability in Broadcom AutoSys Workload Automation (Workload Control Center (WCC) modules) on Windows, Linux allows Session Credential Falsification through Forging.This issue affects AutoSys Workload Automation: from 12.1 through 24.2.00.

### CVE-2026-109857

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-18T13:17:23.637 |

CAST Imaging is vulnerable to authentication bypass in the TenantFilter class. The TenantFilter processes the X-ISSUER-LOCATION HTTP header and dynamically registers an OpenID Connect issuer based on its value. An unauthenticated remote attacker can register a malicious identity provider, create users matching existing administrative usernames, and obtain valid JWTs which will be accepted by the application. This results in complete authentication bypass and privilege escalation to administrative access.




The vulnerability has only been confirmed in version 3.6.2 but may also affect other versions. The vendor did not provide the affected version range, but assured that the vulnerability is fixed "in newer versions".

### CVE-2026-130747

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-155` |
| Published | 2026-11-18T12:17:22.197 |

Grav before 1.7.53.7 and 2.x before 2.2.18 contains an authentication bypass vulnerability that allows anonymous visitors to create super-admin accounts because UserCollection::count() uses an unescaped glob() pattern. On installs whose path contains brackets or a backslash, the account count returns zero, so attackers can send requests to POST /api/v1/auth/setup or the classic admin registration form to create or overwrite administrator accounts.

### CVE-2025-62165

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-17T21:17:34.990 |

Pi-hole FTL is the core engine of the Pi-hole network-level advertisement and tracker blocker. From 6.0 until 6.7, CivetWeb permits unauthenticated clients to flood the WebUI login page and API invalid paths without connection or request-rate limits. Repeated requests can consume substantial CPU in request processing and session authentication, making the WebUI sluggish or unresponsive and potentially affecting the wider system and DNS service. Requests to selected invalid or redirecting paths also generate a log entry for each request, allowing network traffic to expand logs and exhaust constrained storage such as an SD card, while other request forms consume CPU without producing a corresponding request log. This vulnerability is fixed in 6.7.

### CVE-2026-111508

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T12:17:01.917 |

Dell PowerStore contains an OS Command Injection vulnerability. Exploitation could lead to arbitrary command execution with root privileges on the appliance.

### CVE-2026-95645

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T09:17:44.810 |

Zohocorp Manageengine DDI Central build below 6500 are affected by a authenticated command injection vulnerability in the Windows DDI Agent's clear_blocked_domains functionality, allowing specially crafted blocked-domain values to trigger arbitrary command execution on Windows systems.

### CVE-2026-95643

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T09:17:44.657 |

Zohocorp Manageengine DDI Central build below 6500 are affected by a authenticated PowerShell command injection vulnerability in the Telnet connectivity feature, allowing specially crafted IPv6 scope identifiers to execute arbitrary commands on managed Windows nodes.

### CVE-2026-126969

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-331` |
| Published | 2026-11-18T00:18:37.280 |

SmarterTools SmarterMail Insufficient Entropy Authentication Bypass Vulnerability. This vulnerability allows remote attackers to bypass authentication on affected installations of SmarterTools SmarterMail. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the generation of Application Passwords. The issue results from using insufficient entropy in the generation of credentials. An attacker can leverage this vulnerability to bypass authentication on the system. Was ZDI-CAN-33568.

### CVE-2026-91618

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-17T22:19:26.123 |

Vulnerability in the Oracle Application Development Framework (ADF) product of Oracle Fusion Middleware (component: Security Framework).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Application Development Framework (ADF).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Application Development Framework (ADF) accessible data as well as  unauthorized access to critical data or complete access to all Oracle Application Development Framework (ADF) accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-127369

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:19:01.630 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Close Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Close Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-127362

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-17T22:19:00.777 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Close Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Close Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115050

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-17T22:18:37.100 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114952

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-17T22:18:25.530 |

Vulnerability in the MySQL Server, MySQL Cluster product of Oracle MySQL (component: Client programs).  Supported versions that are affected are MySQL Server: 8.4.0-8.4.13, 9.7.0-9.7.4, 26.10; MySQL Cluster: 8.0.0-8.0.50, 8.4.0-8.4.13, 9.7.0-9.7.4 and  26.10. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise MySQL Server, MySQL Cluster.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all MySQL Server, MySQL Cluster accessible data as well as  unauthorized access to critical data or complete access to all MySQL Server, MySQL Cluster accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114881

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:17.107 |

Vulnerability in the Document Management and Collaboration product of Oracle E-Business Suite (component: Attachments).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Document Management and Collaboration.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Document Management and Collaboration accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Document Management and Collaboration. CVSS 3.1 Base Score 9.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-114862

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T22:18:14.817 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Weblogic).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise PeopleTools accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114847

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-17T22:18:13.160 |

Vulnerability in Oracle Autonomous Health Framework (component: Developer triaging platform).  Supported versions that are affected are 26.4-26.10. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Autonomous Health Framework.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Autonomous Health Framework accessible data as well as  unauthorized access to critical data or complete access to all Oracle Autonomous Health Framework accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-130870

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T20:17:53.467 |

ClearFlask before 2.7.3 contains an improper authorization vulnerability that allows any account holding an invitation ID to accept it regardless of invited email. Attackers who obtain a forwarded or shared invitation link can redeem it via accountAcceptInvitationAdmin or accountSignupAdmin to become project administrators.

### CVE-2026-130868

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-341` |
| Published | 2026-11-17T20:17:53.150 |

GreaterWMS through 2.1.54 contains a predictable authentication token vulnerability that allows unauthenticated attackers to forge openid tokens by recomputing an unsalted MD5 hash of username and registration timestamp. Attackers who know a username and can bound its registration time can brute-force candidate openid values in the Token header to gain full read and write access to warehouse, staff, customer, supplier and order data.

### CVE-2026-130838

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-488` |
| Published | 2026-11-17T20:17:48.413 |

Radicale 3.3.0 before 3.8.3 contains an authorization bypass vulnerability that allows unauthenticated attackers to inherit group-based rights by reusing group memberships never reset between requests. Attackers can send credential-less requests after a group member logs in to read and write group-shared calendar and address book collections evaluated by the from_file rights backend.

### CVE-2026-130802

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294;CWE-330` |
| Published | 2026-11-17T17:18:05.750 |

The NFC authentication handshake relies on a fixed, static challenge instead of a unique, random value for every session. This allows an attacker to perform a "replay attack," successfully authenticating by simply sending the same pre-recorded response.

### CVE-2026-122150

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-17T16:17:40.853 |

The PocketTouch and TouchPoint POS `CHECKPAYMENT` workflow accepts a caller-supplied clerk number without adequately verifying that the requesting client is authorized to act as that clerk.
An attacker with access to the POS protocol may be able to specify another employee’s clerk identifier and submit payment-related requests under that identity.

### CVE-2026-122149

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T16:17:40.747 |

The PocketTouch and TouchPoint POS protocol includes a `SAVECONFIG` command that appears capable of overwriting till configuration files remotely. 
An attacker with network access to the POS socket service may be able to submit a crafted `SAVECONFIG` command and replace or modify terminal configuration data.

### CVE-2026-122122

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-17T16:17:39.963 |

The order-tracking functionality in ICRTouch ByTable and TouchTakeaway does not adequately verify that a requester is authorized to access the specified order. An unauthenticated remote attacker can modify an order identifier to retrieve information associated with other customers’ orders.

### CVE-2026-114204

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-18T02:17:39.850 |

Use of Hard-coded Cryptographic Key in ASUS Control Center Express allows a remote user to bypass authentication by forging a session token for an account with a recent valid login, resulting in administrative control of the management console and of the clients it manages.
Refer to the ' Security Update for ASUS Control Center Express Agent  ' section on the ASUS Security Advisory for more information.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-21600

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T18:17:57.093 |

This High severity Security Misconfiguration vulnerability was introduced in versions 10.2.0, 11.0.0, 12.0.0, and 12.1.0 of Bamboo Data Center.

This Security Misconfiguration vulnerability, with a CVSS Score of 8.9, allows an authenticated attacker to to get into the system utilizing loopholes exposed from security best-practices being overlooked.

Atlassian recommends that Bamboo Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
 Bamboo Data Center 10.2: Upgrade to a release greater than or equal to 10.2.26

 Bamboo Data Center 12.1: Upgrade to a release greater than or equal to 12.1.13

 Bamboo Data Center 13.0: Upgrade to a release greater than or equal to 13.0.1

See the release notes ([https://confluence.atlassian.com/bambooreleases/bamboo-release-notes-1189793869.html]). You can download the latest version of Bamboo Data Center from the download center ([https://www.atlassian.com/software/bamboo/download-archives]).

This vulnerability was reported via our Atlassian (Internal) program.

### CVE-2026-107515

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-18T14:17:21.760 |

Dell PowerStore contains an Improper Privilege Management vulnerability. An authenticated attacker could exploit this vulnerability, potentially leading to privilege escalation to administrator.

### CVE-2026-125820

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-18T08:17:19.303 |

Deserialization of Untrusted Data vulnerability in Rymera Web Co Product Feed PRO for WooCommerce woo-product-feed-pro allows Object Injection.This issue affects Product Feed PRO for WooCommerce: from n/a through 13.5.8.

### CVE-2025-2235

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-18T08:17:19.020 |

Improper Verification of Cryptographic Signature vulnerability in OpenText™ Connected MX allows Privilege Escalation. The vulnerability could allow a local, low-privileged user of a macOS endpoint to gain root privileges through the Connected MX Agent update process. This issue affects Connected MX macOS Agent: before 25.2.

### CVE-2026-5765

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-18T06:17:30.593 |

The Essential Real Estate plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 5.3.3 via deserialization of untrusted input in the 'saved_search_check_result' function. This makes it possible for authenticated attackers, with Subscriber-level access and above, to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present.

### CVE-2026-92182

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-18T00:18:49.280 |

Netgate pfSense CE XMLRPC Incorrect Authorization Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Netgate pfSense. Authentication is required to exploit this vulnerability.

The specific flaw exists within the XMLRPC endpoint. The issue results from incorrect authorization prior to allowing access to functionality. An attacker can leverage this vulnerability to execute code within the context of the root. Was ZDI-CAN-32353.

### CVE-2026-126979

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-18T00:18:38.590 |

Philips Hue Bridge HomeKit Accessory Protocol chacha20_decrypt Integer Underflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Philips Hue Bridge. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the HomeKit Accessory Protocol service, which listens on TCP port 8080 by default. When parsing pairing requests, the process does not properly validate user-supplied data, which can result in an integer underflow before writing to memory. An attacker can leverage this vulnerability to execute code in the context of the device. Was ZDI-CAN-28332.

### CVE-2026-126978

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-18T00:18:38.467 |

Philips Hue Bridge hap_pair_setup_handler Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Philips Hue Bridge. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the HomeKit Accessory Protocol service, which listens on TCP port 8080 by default. When parsing pairing requests, the process does not properly validate the length of user-supplied data prior to copying it to a fixed-length, heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the device. Was ZDI-CAN-28434.

### CVE-2026-126967

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T00:18:36.993 |

SmarterTools SmarterMail File Edit API Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of SmarterTools SmarterMail. Authentication is required to exploit this vulnerability.

The specific flaw exists within the FileStorageController class. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-30742.

### CVE-2026-126966

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-18T00:18:36.867 |

SmarterTools SmarterMail Missing Authorization Privilege Escalation Vulnerability. This vulnerability allows remote attackers to escalate privileges on affected installations of SmarterTools SmarterMail. Authentication is required to exploit this vulnerability.

The specific flaw exists within the svcDomainAdmin.asmx endpoint. The issue results from the lack of authorization prior to allowing access to functionality. An attacker can leverage this vulnerability to escalate privileges to resources normally protected from the user. Was ZDI-CAN-33566.

### CVE-2026-126962

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-18T00:18:36.357 |

open62541 Subscription Use-After-Free Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of open62541. Authentication is required to exploit this vulnerability.

The specific flaw exists within the handling of subscriptions. The issue results from the lack of validating the existence of an object prior to performing operations on the object. An attacker can leverage this vulnerability to execute code in the context of the service account. Was ZDI-CAN-30231.

### CVE-2026-118630

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-11-18T00:18:36.207 |

Winmate HotTab Exposed Dangerous Function Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Winmate devices. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the HotTab driver. The issue results from an exposed dangerous function. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of the kernel. Was ZDI-CAN-29948.

### CVE-2026-129025

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-17T23:17:48.237 |

Cross-Site Request Forgery (CSRF) vulnerability in Brainstorm Force ZIP AI zip-ai allows Cross Site Request Forgery.This issue affects ZIP AI: from n/a through 0.0.19.

### CVE-2026-91566

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:24.760 |

Vulnerability in the Oracle Service Bus product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Service Bus.  Successful attacks of this vulnerability can result in takeover of Oracle Service Bus. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-91556

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:24.193 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Service Delivery Platform.  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-83362

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:21.600 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in takeover of Oracle Purchasing. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-69187

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266;CWE-863` |
| Published | 2026-11-17T22:19:21.247 |

WeGIA is a web manager for charitable institutions. Prior to 3.9.1, web/controle/control.php authorizes FuncionarioControle requests only by checking whether an authenticated employee has a permission row for resource 11 or 91, while MiddlewareDAO::verificarPermissao() does not compare the stored id_acao value or authorize the requested method. An employee with any such permission and a valid CSRF token from the employee's own session can invoke FuncionarioControle::adicionarPermissao, FuncionarioControle::alterarPermissao, or FuncionarioControle::excluirPermissao to add, change, or remove permissions for arbitrary roles. This can grant higher action levels over sensitive resources, expose or modify protected employee, patient, configuration, and administrative data, or disrupt legitimate access by changing other roles. This issue is fixed in version 3.9.1.

### CVE-2026-61715

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-17T22:19:20.923 |

Servo is a lightweight, high-performance web rendering engine for embedding web technologies in applications. Prior to 0.4.0, a frame with sandbox="" can reach and execute a javascript: URL through declarative refresh because RefreshRedirectDue::invoke() in components/script/dom/document/document.rs can reach JavaScript URL handling in components/script/script_thread.rs without enforcing the sandbox's script prohibition. This gives attacker-controlled content arbitrary JavaScript execution in a frame intended to be scriptless, including nested DOM probe creation and blind browser requests. The frame retains an opaque origin, so the issue does not by itself provide parent DOM access. This issue is fixed in version 0.4.0.

### CVE-2026-61689

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-17T22:19:20.573 |

XWiki Platform is a generic wiki platform. From 4.3-milestone-1 until 16.10.18, 17.10.5, and 18.2.0, the /rest/wikis/{wikiName}/query REST endpoint permits HQL query construction that can combine blind conditions with FROM-clause injection to join BaseObject and StringProperty, bypassing the SELECT-column whitelist. An unauthenticated attacker can recover database values from inaccessible pages, including salted SHA1 password hashes and passwords stored in configuration properties. It should be assumed that, with more complex techniques, this can work even when the attacker cannot read any wiki page. A typical password hash may require roughly 800 requests, and expensive injected queries can also degrade availability. The issue is remediated by disabling HQL and XWQL REST queries by default. This issue is fixed in versions 16.10.18, 17.10.5, and 18.2.0.

### CVE-2026-127418

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:07.340 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Lifecycle Management).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127371

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:01.863 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Close Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127335

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:57.663 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Close Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127334

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:57.550 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127307

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:52.930 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115142

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:47.773 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115133

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:46.767 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Close Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115131

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:46.547 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Application Development Framework).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Planning. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115128

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:46.213 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Planning. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115087

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:41.520 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Planning. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115074

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:40.023 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Close Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115071

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:39.673 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Close Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115070

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:39.550 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Close Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115067

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:39.200 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115054

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:37.597 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115049

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:36.990 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115044

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:36.527 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: EAI).  Supported versions that are affected are 17.0-26.9. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Integration. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115035

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:35.443 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Siebel Remote).  Supported versions that are affected are 17.0-26.9. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114979

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:28.783 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114937

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:23.663 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Updates Environment Mgmt).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114928

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:22.757 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Application Server).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114917

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:21.540 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Personalization).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Framework. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114897

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:19.070 |

Vulnerability in the Oracle iProcurement product of Oracle E-Business Suite (component: Redirection).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iProcurement.  Successful attacks of this vulnerability can result in takeover of Oracle iProcurement. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114896

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:18.947 |

Vulnerability in the Oracle Collaborative Planning product of Oracle E-Business Suite (component: Horizontal View).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Collaborative Planning.  Successful attacks of this vulnerability can result in takeover of Oracle Collaborative Planning. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114859

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:14.450 |

Vulnerability in Oracle Application Testing Suite (component: Test Manager for Web Apps).   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Application Testing Suite executes to compromise Oracle Application Testing Suite.  While the vulnerability is in Oracle Application Testing Suite, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Application Testing Suite. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-114857

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:14.337 |

Vulnerability in Oracle REST Data Services (component: PL/SQL Gateway).  Supported versions that are affected are 24.2.0-26.3.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle REST Data Services.  Successful attacks of this vulnerability can result in takeover of Oracle REST Data Services. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114829

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:10.980 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Job System).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114827

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:10.743 |

Vulnerability in the Oracle Managed File Transfer product of Oracle Fusion Middleware (component: MFT Runtime Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Managed File Transfer.  Successful attacks of this vulnerability can result in takeover of Oracle Managed File Transfer. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114814

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:09.397 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Analytics Actions).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-101657

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:04.107 |

Vulnerability in the Oracle Mobile Field Service product of Oracle E-Business Suite (component: Admin UI).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Mobile Field Service.  Successful attacks of this vulnerability can result in takeover of Oracle Mobile Field Service. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71304

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-17T21:18:12.913 |

Pi-hole FTL is the core engine of the Pi-hole network-level advertisement and tracker blocker. From 6.0 until 6.7, check_client_auth() in src/api/auth.c detects that a matching session identifier has passed valid_until but still assigns user_id before the expired state can be rejected. That assignment sends execution through the authorized branch, renews valid_until for another timeout interval, and leaves the session-expired response unreachable. An attacker who possesses a previously valid session identifier can periodically reuse it to preserve administrative access indefinitely, making the configured session timeout ineffective. This issue is fixed in version 6.7.

### CVE-2026-131106

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-17T21:18:10.970 |

Buffer overflow in Partition in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-131101

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-17T21:18:10.380 |

Out of bounds read in Editing in Google Chrome prior to 158.0.8127.36 allowed a remote attacker leveraging social engineering to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131100

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:10.257 |

Use after free in Loader in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131090

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:08.933 |

Use after free in Geometry in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131087

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-17T21:18:08.573 |

Type confusion in V8 in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-131084

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:08.217 |

Use after free in XML in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131082

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:07.977 |

Use after free in CSS in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131079

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:07.610 |

Use after free in Bindings in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131065

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:05.930 |

Use after free in Autofill in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131060

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-17T21:18:05.310 |

Buffer overflow in Media in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-131059

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:05.187 |

Use after free in Autofill in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131042

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:03.107 |

Use after free in V8 in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131022

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:59.757 |

Use after free in DOM in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131021

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:59.613 |

Use after free in Accessibility in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131008

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:57.950 |

Use after free in GarbageCollection in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-131005

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:57.583 |

Use after free in DevTools in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-131001

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-17T21:17:57.110 |

Buffer overflow in Video in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-130980

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:54.520 |

Use after free in Layout in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130979

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:54.400 |

Use after free in Forms in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130976

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:54.037 |

Use after free in PDFium in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted PDF file. (Chromium security severity: Medium)

### CVE-2026-130975

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:53.913 |

Use after free in WebAudio in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-130957

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-754` |
| Published | 2026-11-17T21:17:51.713 |

Improper state validation in Performance in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130951

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:50.983 |

Use after free in Plugins in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130950

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-17T21:17:50.867 |

Type confusion in V8 in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-130943

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:50.013 |

Use after free in Chromecast in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130923

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-17T21:17:46.677 |

Out of bounds write in V8 in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130915

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:45.723 |

Use after free in CSS in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130909

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:44.970 |

Use after free in Extensions in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130860

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-11-17T20:17:51.863 |

Flagr before 1.2.5 contains an authentication bypass vulnerability that allows unauthenticated remote attackers to access the flag management write API through an insecure default FLAGR_BASIC_AUTH_WHITELIST_PATHS including /api/v1/flags. Because basicAuth.whitelist() in pkg/config/middleware.go matches only path prefixes regardless of HTTP method, attackers can create, modify, enable, disable, and delete flags, variants, segments, constraints, and distributions.

### CVE-2026-130796

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-212` |
| Published | 2026-11-17T20:17:45.610 |

Flowise 3.1.3 through 3.1.4 contains an information disclosure vulnerability that allows unauthenticated attackers to read MCP server bearer tokens via the GET /api/v1/public-chatflows/:id handler. Attackers can use the leaked mcpServerConfig token on the POST /api/v1/mcp/:chatflowId route to invoke chatflows, bypassing API key protection and consuming the owner's model quota.

### CVE-2026-86061

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-639;CWE-862` |
| Published | 2026-11-17T18:17:59.590 |

Teable is an AI spreadsheet for business. Prior to release.2026-07-17T05-20-38Z.2264, the routes for PluginService::regenerateSecret and PluginService::delete carry no @Permissions decorator, and the methods omit plugin ownership checks. An authenticated attacker can directly target another plugin's identifier to rotate and disclose its OAuth secret or delete the plugin, including system plugins. Separately, PermissionGuard authorizes several nested API requests using a caller-controlled parent tableId, baseId, or spaceId, while the services resolve the requested child object only by its globally unique identifier. An authenticated attacker can provide a parent resource the attacker owns together with a victim's child identifier. ViewService::getViewById can then disclose another tenant's view configuration, embedded filter values, field layout, and shareId. DashboardService::updatePluginStorage and the view-position updatePluginStorage path can overwrite another tenant's plugin storage because the plugin installation is not rebound to the authorized base, dashboard, table, or view. This issue is fixed in release.2026-07-17T05-20-38Z.2264.

### CVE-2026-104100

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-22` |
| Published | 2026-11-17T18:17:46.003 |

Teable is an AI spreadsheet for business. Prior to release.2026-07-21T11-27-40Z.2320, a registered user can supply path traversal sequences in the hash field accepted by POST /api/attachments/signature when the default local storage provider is in use. In apps/nestjs-backend/src/features/attachments/plugins/local.ts, LocalStorage.presigned uses the client-controlled hash as the storage filename, and LocalStorage.save resolves that path and copies the uploaded request body without calling assertPathWithinStorage on the write path. The read path uses the jail, but the write path does not, allowing the resolved destination to escape the configured storage directory. Because the backend container runs as uid 0, the attacker can write or overwrite arbitrary root-owned files, which can corrupt the instance or lead to root code execution. Object-storage deployments that do not use LocalStorage.save are not affected by this sink. This issue is fixed in release.2026-07-21T11-27-40Z.2320.

### CVE-2026-67455

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-17T17:18:09.013 |

NVIDIA Model Optimizer for Linux and Windows contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, denial of service, and information disclosure.

### CVE-2026-127142

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-18T13:17:25.013 |

LMS (Lan Management System) is vulnerable to Remote Code Execution via unrestricted upload of dangerous file types in the service ticket feature of the client panel. The application does not verify the type or name of files attached to service tickets. An authenticated attacker can upload an .htaccess file to bypass the access restrictions on the storage directory, together with a PHP script. Visiting the uploaded PHP file's URL leads to arbitrary code execution with the privileges of the web server.


This issue was fixed in commit 89dd3f7.

### CVE-2026-109861

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-18T13:17:24.193 |

CAST Imaging contains a hardcoded authentication token in the "KeyCloakController" class of auth-service.jar. An attacker who gains access to the source code, application package, logs, or configuration files can reuse this token to call auth-service endpoints without authentication. Using the token with the "/api/auth/keycloak/users" endpoint, the attacker can enumerate users across Keycloak realms and retrieve user attributes containing API token hashes, enabling reconnaissance and further exploitation.


The vulnerability has only been confirmed in version 3.6.2 but may also affect other versions. The vendor did not provide the affected version range, but assured that the vulnerability is fixed "in newer versions".

### CVE-2026-107518

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-18T13:17:23.350 |

Dell PowerStore contains a Server-Side Request Forgery (SSRF) vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability to make the appliance connect to attacker-chosen internal systems.

### CVE-2026-130749

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-18T12:17:22.533 |

Grav from 2.0.0 before 2.2.18 contains a resource exhaustion vulnerability that allows unauthenticated attackers to fill the disk by varying the HTTP Host header. Attackers can send requests with distinct Host values to create per-host compiled configuration, blueprint, language and page index caches, causing session, upload and logging failures.

### CVE-2026-130748

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-348` |
| Published | 2026-11-18T12:17:22.367 |

Grav from 2.0.0 before 2.2.18 contains a password reset poisoning vulnerability that allows anonymous attackers to redirect reset links by forging the CloudFront-Forwarded-Proto header. Attackers can send a forgot-password request with a crafted scheme value so the emailed reset link points to their host, capturing the token to take over accounts including super admins.

### CVE-2026-130744

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-18T12:17:21.660 |

Grav from 2.0.0 before 2.2.18 contains a remote code execution vulnerability that allows page editors to escape the Twig sandbox by sending requests with a Host: pages header. Attackers can write configuration YAML through page folders and media .meta.yaml sidecars to register an unsandboxed Twig namespace and run shell commands as the web server user.

### CVE-2026-130743

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-18T12:17:21.487 |

Grav from 2.0.0 before 2.2.18 contains an insecure blueprint trust vulnerability that allows publisher accounts to read secrets and execute PHP by planting or selecting attacker-controlled blueprint files. Attackers can abuse the import@ directive, uploaded YAML media named as the page template, or form.flash_folder to leak password hashes and keys or invoke static PHP methods for code execution.

### CVE-2026-130742

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-11-18T12:17:21.317 |

Grav 2.0.0 before 2.2.18 resolves Flex sort and filter field names by first calling them as public methods, so a field named delete invokes FlexObject::delete() without any permission check. Authenticated users with only list access can send GET /api/v1/flex-objects/user-accounts?sort=delete requests to delete every account, then use the reopened API first-run setup to create a super admin.

### CVE-2026-130741

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-18T12:17:21.150 |

Grav from 2.0.0 before 2.2.18 contains a Twig sandbox bypass vulnerability that allows publishers to read any server file by abusing allowlisted array_key_value() and page accessor setters such as filePath(). Attackers can repoint page objects or overwrite the assets collections to render private keys and the API signing secret, then forge a super-admin API token.

### CVE-2026-130740

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-18T12:17:20.983 |

Grav from 2.0.0 before 2.2.18 contains an information disclosure vulnerability that allows publishers and read-only user managers to read password hashes, 2FA secrets and reset tokens through unfiltered account serialization. Attackers can embed a Flex form for the user-accounts directory in a page or query the Flex API with admin.users.read to obtain super admin credentials and take over the account.

### CVE-2026-130739

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T12:17:20.813 |

Grav from 2.0.0 before 2.2.18 contains a privilege escalation vulnerability that allows user managers and Flex editors to overwrite, create, or delete accounts by supplying client-controlled storage keys. Attackers can abuse the create form username, cross-type form flash replay, or __META storage key rename to gain super-admin accounts or delete account files.

### CVE-2026-130736

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-18T12:17:20.213 |

Grav from 2.0.0 before 2.2.18 contains a remote code execution vulnerability that allows publishers to bypass the media action allowlist using scoped method names in Markdown image URLs. Attackers can chain actions like self::addMetaFile into static calls such as Process::fromShellCommandline to read files and run shell commands as the web server user.

### CVE-2026-130732

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-772` |
| Published | 2026-11-18T12:17:19.440 |

Traefik from 2.11.58 before 2.11.61 contains a resource leak vulnerability that allows unauthenticated attackers to exhaust resources by sending Authorization headers with NTLM or Negotiate schemes. Attackers can open many short-lived connections that each allocate a dedicated backend transport never released, exhausting memory, file descriptors and backend connections.

### CVE-2026-130729

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T12:17:18.980 |

NocoDB before 2026.08.0 contains an authorization bypass in its public shared-view relation endpoints, which verify that a parent record exists but not that it passes the view's row filters. Unauthenticated attackers holding a public share link can supply guessable auto-incrementing ids of filtered-out records to has-many, many-to-many, one-many, or link endpoints to read their child records.

### CVE-2026-130727

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T12:17:18.680 |

NocoDB before 2026.08.0 contains an authorization bypass vulnerability in public shared-view endpoints that fetch records by primary key without applying the view's row filter. Anonymous share link holders can enumerate sequential primary keys on link, has-many, and attachment download endpoints to read excluded records' linked data and download their attachments.

### CVE-2026-130723

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T12:17:18.070 |

NocoDB before 2026.08.0 contains an information disclosure vulnerability that allows unauthenticated attackers to access attachments of filtered-out records through the shared view attachment-download endpoint. Attackers holding a public share link can enumerate sequential primary keys to obtain signed download paths for files on records the view's row filter excludes.

### CVE-2026-130718

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T12:17:17.313 |

NocoDB before 2026.08.0 contains an authorization bypass vulnerability that allows anonymous share link holders to access records excluded by a shared view's row filter, because the read-by-primary-key path ignores the view's filters. Attackers can request the public attachment-download or nested-link listing routes with a record id to mint signed download URLs for hidden files and read linked-record data.

### CVE-2026-130709

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-18T12:17:15.940 |

NocoDB before 2026.09.0 contains a server-side template injection vulnerability that allows authenticated Creator or Owner users to execute JavaScript by abusing Handlebars webhook helpers. Attackers can supply property paths like constructor.constructor to pluck, sortBy, filter, or withSort helpers to reach the Function constructor and run operating-system commands.

### CVE-2026-130708

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-18T12:17:15.790 |

NocoDB before 2026.09.0 contains an improper authorization vulnerability that allows workspace Creator users to read plaintext notification webhook URLs by querying the webhook plugin listing endpoint. Attackers can replay exposed Slack, Teams, Discord and Mattermost webhook URLs directly against messaging providers to post arbitrary messages into organization chat channels.

### CVE-2026-130704

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-18T12:17:15.190 |

NocoDB before 2026.10.0 contains an improper access control vulnerability that allows Creator-role users to attach NocoDB's internal database by supplying is_meta and is_local flags. Attackers can create sources or bases with these flags to expose user, token and integration tables, then read and modify records including user roles.

### CVE-2026-130702

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-18T12:17:14.893 |

NocoDB before 2026.10.0 contains an account takeover vulnerability that allows users with the base creator role to hijack other accounts by resending base invitations. Attackers can trigger baseUserInviteResend to mint a new invite_token, read it from the base member list, and reset the victim's password through signup, taking over owner or super admin accounts.

### CVE-2026-130692

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-18T12:17:13.627 |

NocoDB before 2026.10.1 contains a template injection vulnerability that allows authenticated Creator-role users to execute server-side JavaScript by supplying array-form property paths to Handlebars helpers in webhook templates. Attackers can bypass the string-only prototype guard to reach the function constructor, running operating-system commands with server privileges or exfiltrating process-internal values via outbound requests.

### CVE-2026-130690

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-18T12:17:13.320 |

NocoDB before 2026.10.1 contains an incorrect authorization vulnerability that allows organization Creators to reach routes restricted to other roles because the aclFn middleware never enforced allowedRoles. Attackers can generate a super admin password reset link via org-users endpoints to take over the instance, or read and modify SSO client secrets.

### CVE-2026-130689

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T12:17:13.163 |

NocoDB before 2026.10.0 contains an sql injection vulnerability that allows authenticated users with the Creator role to inject SQL by supplying a crafted formula parsed_tree during table creation. Attackers can set a malicious binary-expression operator that is interpolated into a knex.raw fragment, reading user and token tables and escalating to super administrator on SQLite installs.

### CVE-2026-130686

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-18T12:17:12.677 |

vLLM from 0.6.0 before 0.33.0 lacks a request-wide media budget, allowing remote inference clients to exhaust frontend resources by submitting many remote image URLs in one request. Attackers can send a compact request to /v1/messages or /v1/responses that forces downloading and decoding of every image before prompt-length admission, exhausting memory, CPU, and connections.

### CVE-2026-130685

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-18T12:17:12.503 |

vLLM from 0.28.0 before 0.33.0 contains an improper input validation vulnerability that allows unauthenticated attackers to crash the shared EngineCore by sending out-of-range prompt token ids when served with --skip-tokenizer-init. Attackers can submit a large positive token id to /v1/completions, /v1/embeddings, or /pooling, bypassing the tokenizer-gated vocab check and causing a fatal embedding index error that denies service to all tenants.

### CVE-2026-130677

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-272` |
| Published | 2026-11-18T12:17:11.110 |

Craft CMS from 5.0.0 before 5.11.4 contains an improper session management vulnerability that fails to invalidate existing sessions when 2FA is enabled and allows disabling 2FA without re-authentication. Attackers holding a hijacked or stale session can retain full account access and silently remove 2FA without the password, authenticator code, or recovery code.

### CVE-2026-113497

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-18T09:17:44.293 |

A low-privileged remote attacker can change the password of arbitrary users using the REST API, including administrative accounts. By changing the administrator password, an attacker can obtain full administrative access to the device and modify all configuration settings.

### CVE-2026-131875

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-18T03:17:42.230 |

fqterm before 0.9.11 contains a heap out-of-bounds write vulnerability in FQTermDecode that allows malicious servers to corrupt memory by sending CSI sequences with unbounded parameter indexes. Attackers controlling a telnet or SSH server, or intercepting cleartext telnet, can send over 30 semicolon-separated CSI parameters to write chosen 32-bit values past the decoder object on the heap.

### CVE-2026-88711

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T02:17:41.727 |

Improper neutralization of special elements used in an OS command in certain ASUS Router firmware models allows an remote attacker to to execute arbitrary commands with root privileges by inducing a logged-in administrator to visit a malicious website.
Refer to the ' Security Update for ASUS Router Firmware ' section on the ASUS Security Advisory for more information.

### CVE-2026-131857

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-11-18T00:18:43.923 |

Supergateway 4.2.0 through 4.2.2 contains a denial of service vulnerability in stdio-to-SSE mode that allows unauthenticated attackers to crash the gateway via prototype-inherited sessionId values. Attackers can send a POST message request with sessionId set to toString or constructor, triggering an unhandled TypeError that terminates every attached MCP session.

### CVE-2026-131851

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T00:18:42.930 |

ILIAS before 9.25, 10.13, and 11.6 contains an SQL injection vulnerability in ilPRGAssignmentFilter::toConditions() that allows authenticated users to inject SQL through the StudyProgramme members list Name and Status filters. Attackers holding only the OrgUnit permission to view members can break out of LIKE literals and execute stacked statements, such as overwriting the root password hash to gain administrative control.

### CVE-2026-91509

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:22.703 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via SAML to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Access Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-115164

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:50.317 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via T3, IIOP to compromise Oracle Hyperion Infrastructure Technology.  While the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-115120

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:45.390 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-115088

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:41.637 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Planning.  While the vulnerability is in Oracle Hyperion Planning, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Planning accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Planning accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-114932

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:23.210 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Test Framework).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  While the vulnerability is in PeopleSoft Enterprise PeopleTools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise PeopleTools accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-114918

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:21.660 |

Vulnerability in the Oracle Concurrent Processing product of Oracle E-Business Suite (component: BI Publisher Integration).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Concurrent Processing.  While the vulnerability is in Oracle Concurrent Processing, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Concurrent Processing accessible data as well as  unauthorized access to critical data or complete access to all Oracle Concurrent Processing accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-114916

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:21.423 |

Vulnerability in the Oracle Applications Framework product of Oracle E-Business Suite (component: Security).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Framework.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Applications Framework, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Applications Framework accessible data as well as  unauthorized access to critical data or complete access to all Oracle Applications Framework accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-114860

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:14.573 |

Vulnerability in Oracle Application Testing Suite (component: Test Manager for Web Apps).   The supported version that is affected is 13.3.0.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TLS to compromise Oracle Application Testing Suite.  While the vulnerability is in Oracle Application Testing Suite, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Application Testing Suite accessible data as well as  unauthorized access to critical data or complete access to all Oracle Application Testing Suite accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-103931

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-17T22:18:05.170 |

Instatic is an open source visual content management system for building static websites. Prior to 0.0.14, isSafeUrl() and safeUrl() in src/core/html-sanitize/index.ts remove tabs, newlines, carriage returns, and characters handled by String.prototype.trim(), but leave other leading C0 control characters that browsers discard before parsing a URL scheme. A low-privileged editor can place a dangerous URL behind one of those controls in a URL property or custom HTML attribute, allowing src/core/publisher/escapeProps.ts and the shared URL sanitizer to emit it into rendered content. When an Owner or Admin activates the element in the same-origin admin editor canvas, script executes with the victim's application authority and can drive admin APIs to read protected data, create an owner account, or install a plugin. This issue is fixed in version 0.0.14.

### CVE-2026-69155

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-17T21:18:12.310 |

Atomic Server is an open source headless CMS and real-time database. From 0.30.0 until 0.40.3, an authenticated Agent with folder write access can use POST /upload to store HTML or SVG content that GET /download/{path} serves from the application origin through server/src/handlers/download.rs. The response sets Content-Disposition: inline and lacks forced attachment handling and X-Content-Type-Options: nosniff, allowing the browser to render the uploaded active content as the application. When a victim opens the link, the script can access the JavaScript-readable atomic_session cookie and the Agent private key in same-origin IndexedDB, enabling persistent account impersonation. This issue is fixed in version 0.40.3.

### CVE-2026-130874

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-17T20:17:54.110 |

Seerr before 3.5.2 contains an uncontrolled resource consumption vulnerability that allows unauthenticated attackers to exhaust disk space through unnormalized /imageproxy cache keys. Attackers can request the same TMDB image using many equivalent dot-segment path spellings, storing unlimited duplicate copies that fill the shared SQLite configuration volume and break logins and requests.

### CVE-2026-130867

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T20:17:52.990 |

GreaterWMS through 2.1.54 contains an unauthenticated path traversal vulnerability in the css, js, statics and fonts routes in greaterwms/views.py, which concatenate raw request.path_info without normalization. Attackers can send URL-encoded ../ sequences to read db.sqlite3 and obtain user openid tokens, enabling impersonation of any account.

### CVE-2026-130863

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T20:17:52.363 |

ArtisanCloud PowerX through 1.0.2 contains a missing authorization vulnerability in the IAM role management API that allows authenticated tenant members to escalate privileges. Attackers holding even the lowest built-in role can call the permissions/grant-ids, permissions/grant, or bind/member routes to grant permissions or bind privileged roles, gaining tenant administrative access.

### CVE-2026-130861

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T20:17:52.013 |

UrlHub before 1.20.1 contains a missing authorization vulnerability that allows any authenticated user to create accounts via the POST /admin/user/store route because role:admin middleware only covers view and create actions. Attackers, including self-registered users, can submit a request with role=admin to create an administrator account and gain full administrative control.

### CVE-2026-130857

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-17T20:17:51.407 |

EveryDocs Core before 1.6.1 contains an authorization bypass vulnerability that allows authenticated users to access other users' records through unscoped Model.find(params[:id]) lookups in multiple controllers. Self-registered attackers can enumerate sequential ids to read, modify, or delete other users' documents and stored files, and rename or delete their folders, tags and people.

### CVE-2026-130855

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T20:17:51.097 |

Bonsai through 6.0 contains an incorrect authorization vulnerability that allows authenticated Editor users to access admin pages because AdminAuthHandler accepts both Administrator and Editor roles. Attackers can use UsersController and DynamicConfigController to reset administrator passwords, promote accounts to Administrator, and change global settings to take over the instance.

### CVE-2026-130848

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-17T20:17:49.967 |

Dolibarr ERP CRM through 24.0.3 contains a code injection vulnerability in Website::importWebSite() that allows website editors without PHP permission to execute code by importing templates. Attackers can import a template zip whose javascript.js.php contains PHP code, which the public javascript.js.php endpoint includes, executing code as the web server user.

### CVE-2026-130843

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-17T20:17:49.207 |

HyperFrames before 0.9.30 contains a missing Origin and Host validation vulnerability in the unauthenticated Studio API that allows malicious web pages to write project files. Attackers can send CORS-simple POST requests to /api/projects/:id/files/* or use DNS rebinding to plant package.json scripts or agent configs, leading to command execution.

### CVE-2026-130841

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T20:17:48.903 |

ioBroker.lovelace before 7.0.0 contains a path traversal vulnerability in the onCards() request handler that allows unauthenticated remote attackers to read arbitrary files via unsanitized dot-dot segments. Attackers can send crafted requests to the /cards/_static_/, /hacsfiles/, or /local/custom_ui/ routes to read files including ioBroker configuration and stored credentials.

### CVE-2026-121707

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-11-17T20:17:36.580 |

Effect is a TypeScript framework that consists of several packages that work together to help build TypeScript applications. Prior to 3.22.1, Schema.TemplateLiteral schemas containing at least two Schema.String spans compile each span to the ambiguous lazy wildcard [\s\S]*?. Decoding a non-matching untrusted string causes cubic regular expression backtracking, which can block the JavaScript event loop. The issue affects Schema.decodeUnknown, Schema.decodeUnknownSync, Schema.is, and consumers such as HttpApi and @effect/rpc payload decoding. This issue is fixed in version 3.22.1.

### CVE-2026-119292

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-17T20:17:36.240 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, after FreeSWITCH has learned and closed source learning for an RTP peer, read_rtp_packet() and rtp_common_read() in src/switch_rtp.c reject RTP from an unrecognized source only after packet classification and, for encrypted calls, SRTP processing. An unauthenticated attacker with UDP reachability to an active RTP or SRTP media port can sustain a foreign-source packet flood that occupies the media read path and prevents legitimate media from entering FreeSWITCH on calls that consume incoming media for relay or echo. The resulting one-way audio allows the affected endpoint to continue hearing the other party, but the other party loses that endpoint's audio, leaving SIP signaling established while the call is unusable for conversation. Transmit-only playback was unaffected in testing. A caller can learn the media port from the SDP answer, while a third party must first discover an active port, and no valid SRTP key is required. This issue is fixed in version 1.11.2.

### CVE-2026-21607

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T18:17:57.880 |

This High severity Path Traversal (Arbitrary Read/Write) vulnerability known as CVE-2026-21607 was introduced in versions 10.3.26 and 11.3.12.

This Path Traversal (Arbitrary Read/Write) vulnerability, with a CVSS Score of 8.7 and a CVSS Vector of CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N allows an unauthenticated attacker to disclose protected web application files outside the intended resource location, which has high impact to confidentiality, no impact to integrity, no impact to availability, and requires no user interaction.

Atlassian recommends that Jira Software Data Center customers upgrade to the latest version. If you are unable to do so, upgrade your instance to one of the specified supported fixed versions:

Jira Software Data Center 11.3: Upgrade to a release greater than or equal to 11.3.13
Jira Software Data Center 10.3: Upgrade to a release greater than or equal to 10.3.27

See the release notes (https://confluence.atlassian.com/jirasoftware/jira-software-data-center-release-notes.html). You can download the latest version of Jira Software Data Center from the Jira Data Center Download Archives (https://www.atlassian.com/software/jira/download-archives).

### CVE-2026-21606

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T18:17:57.753 |

This High severity Path Traversal (Arbitrary Read/Write) vulnerability known as CVE-2026-21606 was introduced in versions 10.3.26 and 11.3.12.

This Path Traversal (Arbitrary Read/Write) vulnerability, with a CVSS Score of 8.7 and a CVSS Vector of CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N allows an unauthenticated attacker to disclose protected resources outside declared resource directories, which has high impact to confidentiality, no impact to integrity, no impact to availability, and requires no user interaction.

Atlassian recommends that Jira Software Data Center customers upgrade to the latest version. If you are unable to do so, upgrade your instance to one of the specified supported fixed versions:

Jira Software Data Center 11.3: Upgrade to a release greater than or equal to 11.3.13
Jira Software Data Center 10.3: Upgrade to a release greater than or equal to 10.3.27

See the release notes (https://confluence.atlassian.com/jirasoftware/jira-software-data-center-release-notes.html). You can download the latest version of Jira Software Data Center from the Jira Data Center Download Archives (https://www.atlassian.com/software/jira/download-archives).

### CVE-2026-21605

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T18:17:57.587 |

This High severity Path Traversal (Arbitrary Read/Write) vulnerability known as CVE-2026-21605 was introduced in versions 2.0.0, 3.0.0, 4.0.0, 5.0.0, 6.0.1, 6.1.0, 6.2.0, 6.3.1, 6.4.0, 6.5.0, 6.6.0 ,6.7.0, 6.8.0, 6.9.0, 6.10.0, 6.11.0, 6.12.0, 6.13.0, 6.14.0, 6.15.1, 7.0.1, 7.1.0, 7.2.0, 7.3.1, 7.4.0, 7.5.0, 7.6.0, 7.7.2, 7.8.0, 7.9.0, 7.11.0, 7.12.0, 7.13.0, 7.14.0, 7.15.0, 7.16.0, 7.17.0, 7.18.0, 7.19.0, 7.20.0, 8.0.0, 8.1.0, 8.2.0, 8.3.0, 8.4.0, 8.5.0, 8.6.0, 8.7.1, 8.8.0, 8.9.0, 9.0.1, 9.1.0, 9.2.0, 9.3.1, 9.4.0, 9.5.1, 10.0.2, 10.1.0, 10.2.0, and 11.0.0 of Confluence Data Center.

This Path Traversal (Arbitrary Read/Write) vulnerability, with a CVSS Score of 8.7 and a CVSS Vector of CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N allows an unauthenticated attacker to expose assets in your environment susceptible to exploitation, which has high impact to confidentiality, no impact to integrity, no impact to availability, and requires no user interaction.

Atlassian recommends that Confluence Data Center and Server customers upgrade to the latest version. If you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
 Confluence Data Center 11.0: Upgrade to a release greater than or equal to 11.0.1
 Confluence Data Center 10.2: Upgrade to a release greater than or equal to 10.2.20
 Confluence Data Center 9.2: Upgrade to a release greater than or equal to 9.2.27

See the release notes ([https://confluence.atlassian.com/doc/confluence-release-notes-327.html]). You can download the
latest version of Confluence Data Center and Server from the download center
([https://www.atlassian.com/software/confluence/download-archives]).

The following description summarizes the vulnerability reported internally:

Confluence CssServlet forwards a request-controlled path to ServletRequest.getRequestDispatcher. The dispatcher URL-decodes and normalizes the path, allowing an unauthenticated attacker to use an encoded traversal sequence to access protected web application resources such as /WEB-INF/web.xml. The demonstrated impact is disclosure of protected files that may contain configuration or secrets; no integrity or availability impact was demonstrated.

### CVE-2026-21601

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-17T18:17:57.210 |

This High severity BASM (Broken Authentication & Session Management) vulnerability was introduced in versions 10.0.0 and 11.0.0 of Jira Service Management Data Center. 
	
	This BASM (Broken Authentication & Session Management) vulnerability, with a CVSS Score of 8.7, allows an unauthenticated attacker to perform actions as another user. 
	
	Atlassian recommends that Jira Service Management Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
		
		* Jira Service Management Data Center 10.3: Upgrade to a release greater than or equal to 10.3.27
		
		* Jira Service Management Data Center 11.3: Upgrade to a release greater than or equal to 11.3.13
		
		
	
	See the release notes (https://confluence.atlassian.com/servicemanagement/jira-service-management-release-notes-780083086.html). You can download the latest version of Jira Service Management Data Center from the download center (https://www.atlassian.com/software/jira/service-management/download-archives). 
	
	This vulnerability was discovered by Nagli and reported via our Bug Bounty program

### CVE-2026-21598

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T18:17:56.850 |

This High severity Path Traversal (Arbitrary Read/Write) vulnerability known as CVE-2026-21598 was introduced in versions 10.2.0, 11.0.0, 12.0.0 and 12.1.0.

This Path Traversal (Arbitrary Read/Write) vulnerability, with a CVSS Score of 8.7 and a CVSS Vector of CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N allows an unauthenticated attacker to potentially disclose sensitive information from the deployed Bamboo web application root, which has high impact to confidentiality, no impact to integrity, no impact to availability, and requires no user interaction.

Atlassian recommends that Bamboo Data Center customers upgrade to the latest version. If you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
 Bamboo Data Center 12.1: Upgrade to a release greater than or equal to 12.1.13
 Bamboo Data Center 10.2: Upgrade to a release greater than or equal to 10.2.26

See the release notes ([https://confluence.atlassian.com/bambooreleases/bamboo-release-notes-1189793869.html]). You can download the latest version of Bamboo Data Center from the download center ([https://www.atlassian.com/software/bamboo/download-archives]).

### CVE-2026-21594

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T18:17:56.493 |

This High severity Path Traversal (Arbitrary Read/Write) vulnerability known as CVE-2026-21594 was introduced in versions 10.2.0, 11.0.0, 12.0.0, and 12.1.0.

This Path Traversal (Arbitrary Read/Write) vulnerability, with a CVSS Score of 8.7 and a CVSS Vector of CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N allows an unauthenticated attacker to disclose protected files from the Bamboo web application root, which has high impact to confidentiality, no impact to integrity, no impact to availability, and requires no user interaction.

Atlassian recommends that Bamboo Data Center customers upgrade to the latest version. If you are unable to do so, upgrade your instance to one of the specified supported fixed versions:

Bamboo Data Center 12.1: Upgrade to a release greater than or equal to 12.1.13
Bamboo Data Center 10.2: Upgrade to a release greater than or equal to 10.2.26

See the release notes (https://confluence.atlassian.com/bambooreleases/bamboo-release-notes-1189793869.html). You can download the latest version of Bamboo Data Center from the download center (https://www.atlassian.com/software/bamboo/download-archives).

### CVE-2026-21590

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T18:17:55.573 |

This High severity Information Path Traversal (Arbitrary Read/Write) vulnerability was introduced in versions 9.12.0, 10.3.0, and 11.3.0 of Jira Software Data Center. 
	
	This Path Traversal (Arbitrary Read/Write) vulnerability, with a CVSS Score of 8.7, allows a remote unauthenticated attacker to read files from the Jira web application root. 
	
	Atlassian recommends that Jira Software Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
		
		Jira Software Data Center 9.12: Upgrade to a release greater than or equal to 9.12.40
		
		Jira Software Data Center 10.3: Upgrade to a release greater than or equal to 10.3.26
		
		Jira Software Data Center 11.3: Upgrade to a release greater than or equal to 11.3.12
		
		
	
	See the release notes (https://confluence.atlassian.com/jirasoftware/jira-software-data-center-release-notes.html). You can download the latest version of Jira Software Data Center from the download center (https://www.atlassian.com/software/jira/download-archives). 
	
	This vulnerability was reported via our Bug Bounty program.

### CVE-2026-110782

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-347` |
| Published | 2026-11-17T18:17:46.387 |

The SimpleSAMLphp SAML2 library is a PHP library for SAML2 related functionality. From 6.2.2 until 6.2.4 and 7.0.0-rc2, HTTPArtifact::receive() in src/Binding/HTTPArtifact.php verifies a signed outer ArtifactResponse but returns an unsigned embedded SAML Response before calling verifyMessageSignature(). The signed path verifies with the artifact issuer's metadata keys without requiring the embedded Response issuer to match that artifact issuer. In a multi-IdP federation, an attacker controlling one trusted IdP can therefore return a validly signed outer ArtifactResponse containing an unsigned Response that claims a different IdP, bypassing the binding's embedded-message authentication. End-to-end impersonation requires a service provider using HTTP-Artifact and a downstream consumer that relies on the binding to authenticate the embedded Response rather than independently requiring a signature. This issue is fixed in versions 6.2.4 and 7.0.0-rc2.

### CVE-2026-126558

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-184` |
| Published | 2026-11-17T17:18:00.063 |

OS Command Injection, Incomplete List of Disallowed Inputs vulnerability in Broadcom AutoSys Workload Automation (Workload Control Center (WCC) modules) on Windows, Linux allows OS Command Injection, Command Delimiters.This issue affects AutoSys Workload Automation: from 12.1 through 24.2.00.

### CVE-2026-77224

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-17T15:17:42.260 |

Camunda 7.24.0 before 7.24.14 and 7.23.0 before 7.23.17 contains an XML External Entity (XXE) injection vulnerability in the camunda-external-task-client's DomXmlDataFormat.defaultDocumentBuilderFactory(), which fails to disable external entity resolution when parsing object variables serialized with application/xml. An attacker able to write a process variable can trigger arbitrary file read and out-of-band outbound HTTP requests from every worker JVM that deserializes the variable, enabling exfiltration of credentials, service-account tokens, and private key material from network segments deeper than the engine itself.

### CVE-2026-132121

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1385` |
| Published | 2026-11-18T13:17:27.317 |

Supergateway 2.4.0 through 4.2.2 contains a cross-site WebSocket hijacking vulnerability in stdio-to-WebSocket mode that allows malicious web pages to connect by bypassing missing Origin header validation. Attackers can open the /message WebSocket from a victim's browser, even against localhost-bound gateways, to initialize an MCP session and invoke wrapped stdio MCP server tools with victim privileges.

### CVE-2026-87790

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-23;CWE-73;CWE-427` |
| Published | 2026-11-18T12:17:23.740 |

Latvijas Valsts radio un televīzijas centrs (LVRTC)
eParakstītājs 3.0 version 1.10.0-resolute allows an unauthenticated remote
attacker to cause HTTP GET requests from a user's workstation by convincing the
user to open a crafted signed eDOC file. Automatic certificate validation
retrieves a signer-controlled Authority Information Access (AIA) caIssuers URL
and follows redirects without restricting the destination, enabling blind SSRF
to loopback and private-network services. Additionally, unrestricted loading of
local file URIs (such as file:///dev/zero) causes unbounded memory buffering
resulting in Denial of Service (OutOfMemoryError). In automated server
verification pipelines with UI:N, impact scales up to CVSS 8.6 High.

### CVE-2026-87789

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73;CWE-78;CWE-94;CWE-116` |
| Published | 2026-11-18T12:17:23.593 |

Latvijas Valsts radio un televīzijas centrs (LVRTC)
eParakstītājs 3.0 version 1.10.0 for macOS allows an unauthenticated remote
attacker to execute arbitrary commands with the privileges of the current user
by convincing the user to open a PDF with a crafted filename and select Send.
The application embeds the attachment path in AppleScript source without
neutralizing AppleScript syntax, allowing injected do shell script expressions
to execute.

### CVE-2026-82952

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73;CWE-78;CWE-88` |
| Published | 2026-11-18T12:17:23.333 |

Latvijas Valsts radio un televīzijas centrs (LVRTC)
eParakstītājs 3.0 version 1.10.0-resolute for Linux allows an unauthenticated
remote attacker to execute arbitrary commands with the privileges of the
current user by convincing the user to open and validate a signed PDF with a
crafted filename and select Open with Adobe Reader. The application embeds the
filename in a sh -c command without neutralizing shell command substitution.

### CVE-2026-130738

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-18T12:17:20.643 |

Grav from 2.0.0 before 2.2.18 contains a privilege escalation vulnerability that allows user managers with admin.users.update to take over super admin accounts by disabling the super-granting group. Attackers can set the group's enabled field to false via the Flex user-groups form, then reset the victim's password through the user-accounts form to gain super admin access.

### CVE-2026-130737

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-138` |
| Published | 2026-11-18T12:17:20.453 |

Grav from 2.0.0 before 2.2.18 contains a privilege escalation vulnerability that allows user managers to grant super-admin rights by nesting access maps under a YAML merge key. Attackers with admin.users.create or api.users.write can submit '<<' keys, for example via PATCH /api/v1/users/<self>, that bypass super-grant filtering and gain full site control.

### CVE-2026-130700

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-451` |
| Published | 2026-11-18T12:17:14.580 |

NocoDB before 2026.10.1 contains a consent phishing vulnerability that allows unauthenticated attackers to register OAuth clients with arbitrary HTTPS redirect URIs through the unauthenticated dynamic client registration endpoint. Attackers can impersonate trusted applications on a consent screen lacking unverified-client warnings or redirect host display, obtaining tokens to read and write victim tables and records.

### CVE-2026-101113

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T04:17:12.413 |

Multiple ELECOM wireless LAN routers contain an OS command injection vulnerability that may cause an arbitrary OS command to be executed by an attacker who can access the administrative interface of the affected product.

### CVE-2026-116643

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-289` |
| Published | 2026-11-18T02:17:40.380 |

An SSH certificate authentication bypass vulnerability in GitHub Enterprise Server allowed an authenticated organization member to read and modify another user's private repositories within the trusted certificate authority's scope. Exploitation required an instance using built-in authentication and a valid certificate issued to the attacker by a trusted SSH certificate authority. This vulnerability affected supported GitHub Enterprise Server releases prior to 3.23 and was fixed in versions 3.19.16, 3.20.12, 3.21.10, and 3.22.5. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-116637

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-18T02:17:40.240 |

A site administrator could modify files on the appliance host with root privileges and disclose private repository data due to improper path validation in GitHub Enterprise Server. Exploitation required a crafted pre-receive hook environment. This vulnerability affected supported GitHub Enterprise Server versions prior to 3.23 and was fixed in versions 3.19.16, 3.20.12, 3.21.10, and 3.22.5. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-131850

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T00:18:42.747 |

ILIAS 11.0 before 11.6 contains an sql injection vulnerability in RegistrationCodeRepository::getCodesData() that concatenates unvalidated sort fields into an ORDER BY clause. Authenticated users with read access to the Authentication and Registration administration node can supply SQL expressions as the sort parameter to extract database contents via boolean-based inference.

### CVE-2026-91587

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:26.013 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-91548

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:23.963 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Platform Security for Java.  While the vulnerability is in Oracle Platform Security for Java, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Platform Security for Java accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-127421

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:07.567 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.22. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-127370

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:01.747 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Close Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Close Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Close Management. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-127306

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:52.820 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security Related Issues).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle AutoVue.  While the vulnerability is in Oracle AutoVue, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle AutoVue accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-114876

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:16.533 |

Vulnerability in the Oracle iStore product of Oracle E-Business Suite (component: Shopping Cart).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle iStore.  While the vulnerability is in Oracle iStore, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle iStore accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-114783

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:05.663 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  While the vulnerability is in Oracle Business Intelligence Enterprise Edition, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-69158

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-17T21:18:12.763 |

Atomic Server is an open source headless CMS and real-time database. Prior to 0.40.3, unauthenticated requests to /bookmark can supply a url that server/src/plugins/bookmark.rs passes through fetch_data to fetch_body. Endpoint dispatch in lib/src/db.rs invokes the handler before check_read, and lib/src/client/helpers.rs previously checked only that the URL began with HTTP, without restricting loopback, private, link-local, DNS-rebinding, or redirect targets. The handler reflects fetched content in returned resource fields, making this a full-response server-side request forgery that can expose internal services and plain-GET cloud metadata. The short request timeout limits slow targets, and metadata services requiring a separate token request are outside the demonstrated GET-only path. This issue is fixed in version 0.40.3.

### CVE-2026-130853

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-17T20:17:50.753 |

Nexterm through 1.2.2-BETA contains a privilege escalation vulnerability that allows users with permissions.manage to gain unauthorized permissions because addGroupMember and setUserGroups lack the grantsBeyondCaller check. Attackers can add their own account to custom groups via the group membership endpoints to inherit permissions like users.impersonate and settings.backup.

### CVE-2026-130847

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T20:17:49.803 |

Dolibarr ERP CRM before 24.0.2 contains an improper authorization vulnerability in the Users REST API put() method that allows non-admin API users to set administrator passwords. Authenticated users with user modification and password rights can send a PUT request to the users endpoint with a chosen pass value for a SuperAdmin account and then log in as that administrator.

### CVE-2026-126550

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-532` |
| Published | 2026-11-17T17:17:59.120 |

Insertion of Sensitive Information into Log File, Insufficiently Protected Credentials vulnerability in Broadcom AutoSys Workload Automation (Workload Control Center (WCC) modules) on Windows, Linux allows Reusing Session IDs (Session Replay).This issue affects AutoSys Workload Automation: from 12.1.00 through 24.2.00.

### CVE-2026-130728

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:18.830 |

NocoDB before 2026.08.0 contains a stored cross-site scripting vulnerability that allows any authenticated user to register OAuth clients with javascript: redirect URIs. Attackers can send a consent link to a signed-in victim so either consent button runs script in the NocoDB origin, stealing the session token for account takeover.

### CVE-2026-131871

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-18T03:17:41.610 |

WLA DX 9.7 through 10.7 contains a stack-based buffer overflow vulnerability in parse_data_blocks() in wlalink/analyze.c that copies section namespaces without length checks. Attackers can supply a crafted object or library file with a namespace longer than 255 bytes or unterminated to overflow the 256-byte stack buffer when linked.

### CVE-2026-93459

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-11-18T02:17:42.130 |

Use of externally-controlled format string in certain ASUS Router firmware allows a nearby administrator to read or write memory, potentially resulting in a denial-of-service, via crafted format specifiers sent to the logging/summary function.
Refer to the ' Security Update for ASUS Router Firmware ' section on the ASUS Security Advisory for more information.

### CVE-2026-112115

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-18T02:17:39.437 |

An untrusted search path in ASUS Armoury Crate allows a local, low-privileged user to achieve privilege escalation by executing a crafted library at a high integrity level, via user-controlled environment settings inherited by an elevated process.
Refer to the '
Security Update for Armoury Crate App ' section on the ASUS Security Advisory for more information.

### CVE-2026-91671

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:27.083 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-115173

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:51.377 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  While the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-130839

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-11-17T20:17:48.577 |

ModelScope 1.11.0 to before 1.40.1 contains an unsafe reflection vulnerability in the image-to-3D SyncDreamer pipeline that allows remote attackers to execute code via crafted model configuration. Attackers can publish a model whose syncdreamer.yaml target field makes instantiate_from_config() import and instantiate any class with controlled params, without an allowlist or trust_remote_code check, executing code when victims load it.

### CVE-2026-130724

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-18T12:17:18.217 |

NocoDB before 2026.08.0 contains a server-side request forgery vulnerability that allows authenticated base Editors to make backend HTTP requests by supplying arbitrary URLs to the integration remote fetch operation. Attackers can control the method, headers, and body to reach internal APIs, loopback services, and cloud metadata endpoints, reading responses and echoed decrypted integration secrets.

### CVE-2026-118900

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T05:19:02.153 |

An OS command injection vulnerability exists in the Android application "Imperial Palaces Guide" provided by The Imperial Household Agency. An attacker may be able to execute arbitrary OS commands with the privileges of the application.

### CVE-2026-115179

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:52.050 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Infrastructure Technology executes to compromise Oracle Hyperion Infrastructure Technology.  While the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-21603

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-17T18:17:57.467 |

This High severity Stored XSS vulnerability was introduced in version 10.3.26 of Jira Core Data Center and Jira Software Data Center. 
	
	This Stored XSS vulnerability, with a CVSS Score of 8.4, allows an authenticated attacker to execute arbitrary HTML or JavaScript code on a victims browser. 
	
	Atlassian recommends that Jira Core Data Center and Jira Software Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
		
		* Jira Core Data Center and Jira Software Data Center 10.3: Upgrade to a release greater than or equal to 10.3.27
		
		* Jira Core Data Center and Jira Software Data Center 11.3: Upgrade to a release greater than or equal to 11.3.13
		
		
	
	See the release notes (https://www.atlassian.com/software/jira/download-archives). You can download the latest version of Jira Core Data Center and Jira Software Data Center from the download center (https://www.atlassian.com/software/jira/download-archives). 
	
	This vulnerability was reported via our Penetration Testing program.

### CVE-2026-100971

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T16:17:34.043 |

NVIDIA OpenShell for Linux contains a vulnerability in the L7 path allowlist enforcement component where a local attacker with low privileges could cause path traversal by using semicolon-dot path sequences to bypass allowlist restrictions. A successful exploit of this vulnerability might lead to information disclosure, data tampering, and denial of service.

### CVE-2026-109860

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T13:17:24.060 |

CAST Imaging is vulnerable to Path Traversal vulnerability in "/api/server-folders" and "/api/server-folders/download" endpoints. These file-management endpoints accept user-supplied filesystem paths and allow selected system commands to be executed at the specified location, but they do not enforce sufficient authorization boundaries or restrict access to a predefined set of resources. An authenticated attacker can enumerate server directories via the "ls" command and retrieve arbitrary files outside of the intended application workspace, such as "/etc/passwd", exposing sensitive data.


The vulnerability has only been confirmed in version 3.6.2 but may also affect other versions. The vendor did not provide the affected version range, but assured that the vulnerability is fixed "in newer versions".

### CVE-2026-109858

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T13:17:23.773 |

CAST Imaging has multiple path traversal vulnerabilities in various endpoints. The application does not properly validate the path parameters, allowing an authenticated attacker to use "../" sequences to escape the intended directory and read arbitrary files.


Critically, by reading "/proc/self/environ", the attacker can obtain environment variables containing sensitive credentials such as Keycloak and PostgreSQL passwords, leading to full server compromise and administrative access.


The vulnerability has only been confirmed in version 3.6.2 but may also affect other versions. The vendor did not provide the affected version range, but assured that the vulnerability is fixed "in newer versions".

### CVE-2026-131800

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:A/VC:H/VI:H/VA:N/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T03:17:41.450 |

A stored cross-site scripting vulnerability was identified in GitHub Enterprise Server that allowed an organization member with permission to manage custom-property definitions and edit property values to add an attacker-controlled SSH authentication key to the personal account of another member through HTML stored in a single-select custom-property option. Exploitation required another definition manager in the same organization to attempt to remove the poisoned option while it was in use and save the definition with a valid sudo session. Repository access through the added key depended on the permissions of the victim and independent authorization controls. This vulnerability affected supported GitHub Enterprise Server prior to 3.23 and was fixed in versions 3.19.16, 3.20.12, 3.21.10, and 3.22.5. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-131849

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-18T00:18:42.583 |

Snap7 through 1.4.3 contains a heap-based buffer overflow in TSnap7MicroClient::opReadSZL() that allows malicious PLCs to overwrite client memory by sending oversized multi-slice SZL responses. A rogue or impersonated PLC can keep flagging more data with attacker-controlled DLen slices, overflowing the 65536-byte opData buffer via Cli_ReadSZL() and Cli_ReadSZLList(), crashing the client and corrupting heap memory.

### CVE-2026-131848

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-18T00:18:42.417 |

Snap7 through 1.4.3 contains an out-of-bounds write vulnerability in TSnap7MicroClient::opReadMultiVars() that allows malicious PLCs to overflow client buffers via unchecked DataLength fields. Attackers controlling or impersonating a PLC can return crafted ReadVar responses to Cli_ReadMultiVars() callers, writing up to 65535 bytes per item to corrupt memory and crash clients.

### CVE-2026-91558

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:24.303 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Service Delivery Platform executes to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Service Delivery Platform. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61713

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-17T22:19:20.757 |

Servo is a lightweight, high-performance web rendering engine for embedding web technologies in applications. Prior to 0.3.0, a sandboxed iframe can use declarative refresh to auto-navigate because RefreshRedirectDue::invoke() in components/script/dom/document/document.rs does not enforce the sandboxed automatic-features flag. The bypass occurs with sandbox="", sandbox="allow-same-origin", sandbox="allow-forms", and sandbox="allow-same-origin allow-forms". Attacker-controlled framed content can replace itself without user action, enabling framed phishing, content replacement, redirect loops, and limited denial of service, but the issue does not by itself permit script execution or parent DOM access. This issue is fixed in version 0.3.0.

### CVE-2026-127357

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:00.183 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Close Management accessible data as well as  unauthorized read access to a subset of Oracle Hyperion Financial Close Management accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Financial Close Management. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H).

### CVE-2026-117552

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-17T22:18:52.540 |

Typecho before 1.3.1-rc contains a server-side request forgery vulnerability in the XML-RPC pingback.ping method where checkSafeHost() validates a hostname's resolved IP once but the subsequent outbound request performs an independent DNS resolution, creating a TOCTOU window exploitable via DNS rebinding. An unauthenticated attacker can configure a domain to return a benign IP at validation time and an internal address (loopback, RFC1918, or cloud metadata IP) at request time, causing the server to issue blind SSRF requests to arbitrary internal hosts and ports.

### CVE-2026-131093

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:09.370 |

Use after free in FedCM in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131092

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:09.213 |

Use after free in Mojo in Google Chrome on on Windows prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131078

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:07.487 |

Use after free in Proxy in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted file. (Chromium security severity: Medium)

### CVE-2026-131074

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:07.020 |

Use after free in DeviceBoundSessionCredentials in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-131063

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:05.687 |

Use after free in CameraCapture in Google Chrome on on Windows prior to 158.0.8127.36 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131056

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:04.830 |

Use after free in WebAppInstalls in Google Chrome prior to 158.0.8127.36 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-131051

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T21:18:04.210 |

Incorrect authorization in UI in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-131050

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:04.083 |

Use after free in Mojo in Google Chrome on on Windows prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131044

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:03.343 |

Use after free in Payments in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131039

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:18:01.900 |

Use after free in Mojo in Google Chrome on on Windows prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131013

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-17T21:17:58.563 |

Buffer overflow in Skia in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131004

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:57.463 |

Use after free in FedCM in Google Chrome prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-131000

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-17T21:17:56.990 |

Improper input validation in WebAppInstalls in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130999

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:56.823 |

Use after free in Downloads in Google Chrome on on Windows prior to 158.0.8127.36 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130992

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T21:17:55.977 |

Incorrect authorization in Views in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130987

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-17T21:17:55.370 |

Race condition in Downloads in Google Chrome on on Windows prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process and leveraged social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130982

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T21:17:54.767 |

Incorrect authorization in Omnibox in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130974

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:53.760 |

Use after free in UserEducation in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130969

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T21:17:53.157 |

Incorrect authorization in Omnibox in Google Chrome on on Windows prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process and leveraged social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130960

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:52.070 |

Use after free in Session in Google Chrome prior to 158.0.8127.36 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130956

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-17T21:17:51.590 |

Improper input validation in WebAppInstalls in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130948

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:50.610 |

Use after free in Omnibox in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130945

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:50.247 |

Use after free in VR in Google Chrome on on Android prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130944

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:50.133 |

Use after free in Omnibox in Google Chrome on on Windows prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-130938

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:49.370 |

Use after free in Accessibility in Google Chrome on on Windows prior to 158.0.8127.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130930

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:48.333 |

Use after free in Ozone in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130919

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-17T21:17:46.203 |

Race condition in Printing in Google Chrome prior to 158.0.8127.36 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-130918

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:46.090 |

Use after free in Views in Google Chrome prior to 158.0.8127.36 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-130917

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:45.967 |

Use after free in Browser in Google Chrome prior to 158.0.8127.36 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-130907

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T21:17:44.480 |

Use after free in Autofill in Google Chrome on on Android prior to 158.0.8127.36 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-80322

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:M/U:X` |
| Weaknesses | `CWE-201;CWE-226;CWE-366;CWE-488;CWE-772` |
| Published | 2026-11-17T18:17:58.950 |

Under specific conditions, PingAuthorize in Gateway mode can continue an asynchronous upstream request after its 30-second gateway timeout. If the underlying keep-alive connection is reused for another request before the original response arrives, the late response can be written to the newer exchange. This could cause a subsequent caller to receive response data intended for an earlier request. This behaviour affects all releases and primarily risks unauthorized information disclosure between separate requests.

### CVE-2026-119726

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-668` |
| Published | 2026-11-17T17:17:53.413 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in PocketBook / Obreey Products PocketBook Reader (Android) allows Exposure of Sensitive Information to an Unauthorized Actor.

This issue affects PocketBook Reader (Android): 5.65.0.39561.release (com.obreey.reader).

### CVE-2026-130745

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-18T12:17:21.847 |

Grav from 2.0.0 before 2.2.18 contains an access control bypass vulnerability that allows anonymous visitors to read protected pages because admin and site scopes share a page cache key. Routine editor activity through the API plugin rebuilds the page index without frontmatter.yaml access rules, exposing members-only page content until the cache is rebuilt.

### CVE-2026-130710

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-18T12:17:16.090 |

NocoDB before 2026.09.0 contains a missing authorization vulnerability in the job status polling endpoint of jobs.controller.ts that lacks an @Acl decorator. Unauthenticated attackers with a job id can read buffered status messages and completion payloads, exposing signed export download URLs or new base identifiers.

### CVE-2026-107950

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-18T03:17:40.153 |

An XML External Entity (XXE) vulnerability affects a Storefront REST API in HCL Commerce versions 8, 9.0.1 and 9.1.x.  A remote attacker, using a specially crafted XML, could potentially view internal files or consume memory resources.

### CVE-2026-91543

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:23.737 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Access Manager accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-91533

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:23.510 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Access Manager accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-115166

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:50.547 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-115092

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:42.100 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Application Development Framework).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Planning.  While the vulnerability is in Oracle Hyperion Planning, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Planning accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Planning accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-115082

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:40.963 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-115078

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:40.477 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-115060

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:38.293 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Oracle Hyperion Infrastructure Technology executes to compromise Oracle Hyperion Infrastructure Technology.  While the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-114958

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:26.257 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-114933

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:23.323 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Security).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data as well as  unauthorized update, insert or delete access to some of PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-114904

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:19.947 |

Vulnerability in the Oracle E-Business Suite Integrated SOA Gateway product of Oracle E-Business Suite (component: SOA Provider).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Oracle E-Business Suite Integrated SOA Gateway executes to compromise Oracle E-Business Suite Integrated SOA Gateway.  While the vulnerability is in Oracle E-Business Suite Integrated SOA Gateway, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle E-Business Suite Integrated SOA Gateway. CVSS 3.1 Base Score 8.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-101659

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:04.230 |

Vulnerability in the Oracle Mobile Field Service product of Oracle E-Business Suite (component: Admin UI).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Mobile Field Service.  While the vulnerability is in Oracle Mobile Field Service, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Mobile Field Service accessible data as well as  unauthorized access to critical data or complete access to all Oracle Mobile Field Service accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-119725

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T17:17:53.263 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in PocketBook / Obreey Products PocketBook Reader (Android) allows Exposure of Sensitive Information to an Unauthorized Actor.

This issue affects PocketBook Reader (Android): 5.65.0.39561.release (com.obreey.reader).

### CVE-2026-123419

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-18T14:17:29.660 |

The immonex Kickstart plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 1.19.0 via the 'inx-r-cidata (JSON blob containing 'template' and 'template_folders')' parameter parameter. This makes it possible for unauthenticated attackers to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. The filename-level sanitization that strips dot-slash sequences applies only to the template filename component, not to the attacker-supplied template_folders directory paths, rendering it ineffective against directory traversal via that parameter.

### CVE-2026-116764

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-18T14:17:27.793 |

The The GDPR Framework By Data443 plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 2.5.2. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with subscriber-level access and above, to delete all postmeta rows for every Easy Digital Downloads payment order on the site, destroying order metadata belonging to all customers. Exploitation requires that Easy Digital Downloads 2.x is active and the GDPR Framework's EDD compatibility option is enabled with a delete or delete_and_notify action configured.

### CVE-2026-107519

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-18T13:17:23.490 |

Dell PowerStore contains an integer underflow vulnerability. An attacker could exploit this vulnerability, potentially leading to denial of service of a cryptographic service.

### CVE-2025-15716

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-303` |
| Published | 2026-11-18T08:17:18.870 |

An incorrect implementation of authentication algorithm vulnerability in the SSO API in Synology DiskStation Manager (DSM) before 7.2.2-72806-5 and 7.3.1-86003-1 (7.2.1-69057 is not affected) allows remote attackers to read or write arbitrary files and conduct denial-of-service attacks with prior knowledge of the distinguished name (DN).

### CVE-2026-130644

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T04:17:14.710 |

A path traversal flaw was found in ansible-core. When installing a collection with ansible-galaxy collection install, the install destination directory is derived from the namespace and name fields declared inside the collection artifact's own metadata, which are not validated as well-formed collection identifiers or checked for path containment. A malicious collection artifact -- delivered as a local file, a remote URL, a source directory, a git repository, or as a dependency -- can use a crafted name value to redirect the install destination outside the configured collections path, causing ansible-galaxy to delete an existing directory writable by the invoking user and then write attacker-controlled files to that location.

### CVE-2026-105929

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T02:17:38.693 |

A path traversal vulnerability (CWE-22) was found in ansible-core's ansible-galaxy role installation. An explicit role "name" taken from a role's meta/requirements.yml is used to construct the on-disk installation path without validating that the resulting destination stays within the selected roles directory. A name containing "../" escapes that directory, and an absolute name replaces it entirely. Because ansible-galaxy processes transitive dependencies from an installed role's meta/requirements.yml, a malicious role publisher can cause attacker-supplied files to be written outside the operator's chosen roles directory when the operator installs the role, and, when --force is used, can cause an existing role directory outside that path to be removed and replaced. The impact is bounded by the invoking user's filesystem permissions and requires the operator to install the attacker-influenced content.

### CVE-2026-126977

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1393` |
| Published | 2026-11-18T00:18:38.347 |

Philips Hue Bridge HomeKit Pair-Setup Default Password Authentication Bypass Vulnerability. This vulnerability allows network-adjacent attackers to bypass authentication on affected installations of Philips Hue Bridge. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the HomeKit Authentication service, which listens on TCP port 8080 by default. Crafted data in a pairing request can cause the device to allow authentication using a blank password. An attacker can leverage this vulnerability to bypass authentication on the system. Was ZDI-CAN-28323.

### CVE-2026-91522

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:23.053 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via SAML to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127425

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:07.903 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.22. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle VM VirtualBox accessible data as well as  unauthorized read access to a subset of Oracle VM VirtualBox accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle VM VirtualBox. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:H).

### CVE-2026-127416

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:07.117 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Lifecycle Management).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-127415

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:07.003 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Lifecycle Management).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H).

### CVE-2026-127402

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:05.453 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127372

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:01.977 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Close Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Close Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-127330

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:57.083 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127329

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:56.967 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127328

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:56.850 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127308

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:53.040 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle AutoVue accessible data as well as  unauthorized access to critical data or complete access to all Oracle AutoVue accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-115172

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:51.270 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115157

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:49.523 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115153

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:49.060 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-115151

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:48.790 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via RMI to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115150

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:48.680 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-115130

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:46.437 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Application Development Framework).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Planning accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Planning accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115094

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:42.337 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via RMI to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Planning. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115081

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:40.820 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H).

### CVE-2026-115066

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:39.073 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115062

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:38.527 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115059

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:38.180 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H).

### CVE-2026-115051

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:37.220 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115046

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:36.643 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114976

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:28.380 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Cloud Gateway).  Supported versions that are affected are 22.3-26.9. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114938

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-17T22:18:23.777 |

Vulnerability in the Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition product of Oracle Java SE (component: Compiler).  Supported versions that are affected are Oracle Java SE: 8u511b33-perf, 17.0.21.0.3, 21.0.13.0.3, 25.0.5.0.3, 27.0.1.0.3; Oracle GraalVM for JDK: 17.0.21.0.3 and  21.0.13.0.3; Oracle GraalVM Enterprise Edition: 21.3.20.0.3. Difficult to exploit vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition. Note: This vulnerability can only be exploited by supplying data to APIs in the specified Component without using Untrusted Java Web Start applications or Untrusted Java applets, such as through a web service. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114914

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:21.193 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Endeca).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Purchasing accessible data as well as  unauthorized access to critical data or complete access to all Oracle Purchasing accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114909

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:20.607 |

Vulnerability in the Oracle iProcurement product of Oracle E-Business Suite (component: Requisition Management).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iProcurement.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iProcurement accessible data as well as  unauthorized access to critical data or complete access to all Oracle iProcurement accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114887

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:17.813 |

Vulnerability in the Oracle Mobile Field Service product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Mobile Field Service.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Mobile Field Service accessible data as well as  unauthorized access to critical data or complete access to all Oracle Mobile Field Service accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114871

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:15.947 |

Vulnerability in the Oracle Sales Online product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Online.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Sales Online accessible data as well as  unauthorized access to critical data or complete access to all Oracle Sales Online accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114852

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:13.743 |

Vulnerability in Oracle REST Data Services (component: Core).  Supported versions that are affected are 24.2.0-26.3.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle REST Data Services.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle REST Data Services accessible data as well as  unauthorized access to critical data or complete access to all Oracle REST Data Services accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114825

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:10.503 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).   The supported version that is affected is 12.2.1.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114817

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:09.747 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114815

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:09.513 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Foundation).   The supported version that is affected is 12.2.1.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114813

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:09.280 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Business Intelligence Enterprise Edition accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-114788

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:06.273 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Planning. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-101652

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:03.980 |

Vulnerability in the Oracle Mobile Field Service product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Mobile Field Service.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Mobile Field Service accessible data as well as  unauthorized access to critical data or complete access to all Oracle Mobile Field Service accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-69156

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T21:18:12.470 |

Atomic Server is an open source headless CMS and real-time database. From 0.30.0 until 0.40.3, the Commit application path in lib/src/commit.rs allows an authenticated Agent to assign the server-managed internalId property to an owned resource without character validation. The /download handler in server/src/handlers/download.rs passes that value to filesystem path construction and NamedFile::open without sanitization, containment validation, or a File-class check, so traversal or absolute paths can read files available to the server process. Reading the server configuration can expose the root Agent private key and allow root impersonation with full read, write, and delete access to server data. This issue is fixed in version 0.40.3.

### CVE-2026-122141

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-17T16:17:40.183 |

The wallet top-up functionality in ICRTouch ByTable and TouchTakeaway does not adequately protect state-changing requests against CSRF. An attacker-controlled website can cause an authenticated customer’s browser to submit a wallet top-up request and add an attacker-selected charge to the customer’s active cart.

### CVE-2026-100972

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T16:17:34.173 |

NVIDIA OpenShell for Linux contains a vulnerability in resource-level authorization for create, read, update, and delete operations where an authenticated remote attacker with low privileges could access or modify resources without the required authorization checks. A successful exploit of this vulnerability might lead to information disclosure and data tampering.

### CVE-2026-100963

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-17T16:17:33.753 |

NVIDIA TensorRT for Linux contains a vulnerability where a user could cause an integer overflow issue. A successful exploit of this vulnerability might lead to denial of service and data tampering.

### CVE-2026-118789

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-17T15:17:32.473 |

Farmasimplex retrieves a CIP News file over HTTP and executes embedded SQL statements against the local FarmaCIP database with administrative privileges. An attacker able to tamper with network communications or compromise vendor infrastructure can inject arbitrary SQL commands, leading to unauthorized access to, modification or deletion of database contents and potentially operating system command execution.

### CVE-2026-82150

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-17T20:17:57.863 |

Dell SupportAssist OS Recovery, versions prior to 5.5.16.3, contain an Insufficient Verification of Data Authenticity vulnerability. An unauthenticated attacker with adjacent network access could potentially exploit this vulnerability to bypass manifest signature validation, potentially leading to execution of unauthorized code with elevated privileges.

### CVE-2026-127337

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:57.897 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle AutoVue executes to compromise Oracle AutoVue.  While the vulnerability is in Oracle AutoVue, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle AutoVue accessible data as well as  unauthorized update, insert or delete access to some of Oracle AutoVue accessible data. CVSS 3.1 Base Score 7.9 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-130893

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-18T14:17:40.687 |

Tanium addressed an unauthorized code execution vulnerability.

### CVE-2026-131959

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-18T08:17:19.593 |

GNU Emacs 31.1 contains a code injection vulnerability in its handling of directory-local variables. A crafted .dir-locals.el can supply a (REGEXP FUNCTION t) entry in auto-mode-alist; when a matching file is opened, Emacs calls FUNCTION before set-auto-mode--dir-local-valid-p validates it, executing arbitrary Emacs Lisp with the privileges of the Emacs process. (Emacs 30.2 is unaffected.)

### CVE-2026-126975

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-18T00:18:38.080 |

llama.cpp GGUF File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of llama.cpp. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of GGUF files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute arbitrary code in the context of the current process. Was ZDI-CAN-34558.

### CVE-2026-126974

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-18T00:18:37.943 |

llama.cpp GGUF File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of llama.cpp. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of GGUF files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before writing to memory. An attacker can leverage this vulnerability to execute arbitrary code in the context of the current process. Was ZDI-CAN-34553.

### CVE-2026-126973

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-18T00:18:37.807 |

KDE Gwenview PNG File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of KDE Gwenview. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of PNG files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before allocating a buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29373.

### CVE-2026-126972

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T00:18:37.690 |

KiCad Plugin Directory Traversal Remote Code Execution   Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of KiCad. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the handling of plugin packages. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute arbitrary code in the context of the current user. Was ZDI-CAN-33085.

### CVE-2026-126971

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T00:18:37.570 |

KiCad Project Archive File Handling Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of KiCad. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the handling of project archive files. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute arbitrary code in the context of the current user. Was ZDI-CAN-33212.

### CVE-2026-126970

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-18T00:18:37.417 |

KiCad Altium SCHLIB File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of KiCad. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of SCHLIB files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated object. An attacker can leverage this vulnerability to execute arbitrary code in the context of the current process. Was ZDI-CAN-33213.

### CVE-2026-114931

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:23.097 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Test Framework).  Supported versions that are affected are 8.61-8.63. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise PeopleTools executes to compromise PeopleSoft Enterprise PeopleTools.  While the vulnerability is in PeopleSoft Enterprise PeopleTools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-114861

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:14.693 |

Vulnerability in Oracle Application Testing Suite (component: OpenScript).   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Application Testing Suite executes to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in takeover of Oracle Application Testing Suite. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114828

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:10.863 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Infrastructure Technology executes to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114818

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:09.863 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Hyperion Infrastructure Technology executes to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-114794

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:06.980 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-114793

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:06.863 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Analytics Server).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-114792

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:06.750 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Installation).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-82146

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-17T20:17:57.600 |

Dell SupportAssist OS Recovery, versions prior to 5.5.16.3, contain an Untrusted Search Path vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privilege.

### CVE-2026-82143

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-17T20:17:57.290 |

Dell SupportAssist OS Recovery, versions prior to 5.5.16.3 contain an Improper Authorization vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privilege.

### CVE-2026-93299

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-17T19:18:03.173 |

A maliciously crafted DWG file, when parsed through Autodesk AutoCAD or processed by the installed DWG thumbnail handler, can force an Out-of-Bounds Write vulnerability resulting in heap corruption. A malicious actor can leverage this vulnerability to cause a crash or execute arbitrary code in the context of the current process.

### CVE-2026-85648

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-17T19:18:02.650 |

A maliciously crafted DDS file, when parsed through Autodesk AutoCAD, can force a Heap-Based Buffer Overflow vulnerability. A malicious actor can leverage this vulnerability to cause a crash or execute arbitrary code in the context of the current process.

### CVE-2026-85647

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-17T19:18:02.330 |

A maliciously crafted DWG file containing a malformed embedded image, when parsed through Autodesk AutoCAD, can force a Heap-Based Buffer Overflow vulnerability. A malicious actor can leverage this vulnerability to cause a crash or execute arbitrary code in the context of the current process.

### CVE-2026-85646

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-17T19:18:02.157 |

A maliciously crafted DWF file, when parsed through Autodesk AutoCAD, can force a Heap-Based Buffer Overflow vulnerability. A malicious actor can leverage this vulnerability to cause a crash or execute arbitrary code in the context of the current process.

### CVE-2026-84855

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-17T19:18:02.020 |

A maliciously crafted DGN file, when parsed through Autodesk AutoCAD, can force a Heap-Based Buffer Overflow vulnerability. A malicious actor can leverage this vulnerability to cause a crash or execute arbitrary code in the context of the current process.

### CVE-2026-77943

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-17T19:18:01.410 |

A maliciously crafted DXF file, when parsed through Autodesk AutoCAD, can force an Out-of-Bounds Write vulnerability. A malicious actor can leverage this vulnerability to cause a crash or execute arbitrary code in the context of the current process.

### CVE-2026-77942

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-17T19:18:01.280 |

A maliciously crafted IES file, when parsed through Autodesk AutoCAD, can force an Out-of-Bounds Write vulnerability. A malicious actor can leverage this vulnerability to cause a crash or execute arbitrary code in the context of the current process.

### CVE-2026-18827

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-913` |
| Published | 2026-11-17T19:17:57.630 |

A maliciously crafted DWG file containing an attacker-controlled Excel Data Link connection string, when processed through Autodesk AutoCAD, can cause AutoCAD to execute an attacker-controlled program. A malicious actor can leverage this vulnerability to execute arbitrary code in the context of the current user.

### CVE-2026-18826

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-17T19:17:57.517 |

A maliciously crafted DXF file, when parsed through Autodesk AutoCAD, can force a Type Confusion vulnerability. A malicious actor can leverage this vulnerability to cause a crash or execute arbitrary code in the context of the current process.

### CVE-2026-16780

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-17T19:17:57.157 |

A maliciously crafted DXF file, when parsed through Autodesk AutoCAD, can force a Heap-Based Buffer Overflow vulnerability. A malicious actor can leverage this vulnerability to cause a crash or execute arbitrary code in the context of the current process.

### CVE-2026-104868

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-17T19:17:43.153 |

A maliciously crafted DWG file, when parsed by Autodesk AutoCAD, can trigger an Integer Overflow vulnerability in RLE bitmap decompression, resulting in an undersized heap allocation and subsequent heap buffer overflow. A malicious actor can leverage this vulnerability to cause a crash or potentially execute arbitrary code in the context of the current process.

### CVE-2026-65132

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-17T17:18:08.780 |

NVIDIA Megatron-LM contains a vulnerability in checkpoint loading where an attacker could cause deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, information disclosure, and data tampering.

### CVE-2026-129246

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T17:18:02.297 |

Due to a Debian-specific patch, the directory used to share data between the
LightDM and the users logging in was writable by the lightdm user of the
unprivileged greeter process. A process running under the lightdm identity
could leverage write access to that directory to force the LightDM process
(running as root) to change ownership and permissions on other root-owned
directories and escalate privileges from the lightdm user to root.

### CVE-2026-126547

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T17:17:58.650 |

Missing Authorization vulnerability in Broadcom AutoSys Workload Automation (Workload Control Center (WCC) modules) on Windows, Linux allows Accessing Functionality Not Properly Constrained by ACLs.This issue affects AutoSys Workload Automation: from 12.1 through 24.2.00.

### CVE-2026-100968

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-17T17:17:43.630 |

NVIDIA Megatron-LM contains a vulnerability in dataset loading where an attacker could cause deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, information disclosure, and data tampering.

### CVE-2026-100967

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-17T17:17:43.493 |

NVIDIA Megatron-LM contains a vulnerability where an attacker could cause deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, information disclosure, and data tampering.

### CVE-2026-65106

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-17T16:17:52.717 |

NVIDIA Transformer Engine for Linux contains a vulnerability where a user could cause deserialization by loading  untrusted data. A successful exploit of this vulnerability might lead to code execution, information disclosure, and denial of service.

### CVE-2026-130746

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-524` |
| Published | 2026-11-18T12:17:22.020 |

Grav before 1.7.53.7 and 2.x before 2.2.18 serves page media files, and rendered pages when lazy sessions are enabled, with the visitor's session cookie and a shared-cacheable Cache-Control header. When a shared cache such as Apache mod_cache stores Set-Cookie responses, an attacker can lure a user signed in through the front-end login to open a media URL with a unique query string, then request that URL to receive the cached session cookie and take over the session.

### CVE-2026-125829

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T08:17:19.450 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Rymera Web Co Product Feed PRO for WooCommerce woo-product-feed-pro allows Path Traversal.This issue affects Product Feed PRO for WooCommerce: from n/a through 13.5.8.

### CVE-2026-131820

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-18T02:17:41.427 |

A server-side request forgery vulnerability in GitHub Enterprise Server allowed an authenticated user with repository write access to send requests to internal services through Slack webhook validity checks, potentially leading to remote code execution on the appliance. Exploitation required Secret Protection with secret scanning and validity checks for partner patterns enabled. This vulnerability affected all versions prior to 3.23 and was fixed in versions 3.22.5, 3.21.10, and 3.20.12. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-127392

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:04.287 |

Vulnerability in the Product Lifecycle Analytics product of Oracle Supply Chain (component: Installation Issues).   The supported version that is affected is 3.6.1. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Product Lifecycle Analytics executes to compromise Product Lifecycle Analytics.  While the vulnerability is in Product Lifecycle Analytics, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Product Lifecycle Analytics accessible data as well as  unauthorized access to critical data or complete access to all Product Lifecycle Analytics accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Product Lifecycle Analytics. CVSS 3.1 Base Score 7.7 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L).

### CVE-2026-127349

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:59.203 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  While the vulnerability is in Oracle Hyperion Financial Close Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Close Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-115170

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:51.010 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  While the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-115158

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:49.633 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  While the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-115129

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:46.323 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Planning.  While the vulnerability is in Oracle Hyperion Planning, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Planning accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-115076

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:40.250 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  While the vulnerability is in Oracle Hyperion Financial Close Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Close Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-114874

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:16.303 |

Vulnerability in the Oracle iProcurement product of Oracle E-Business Suite (component: Internal operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iProcurement.  While the vulnerability is in Oracle iProcurement, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle iProcurement accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-114809

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:08.800 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Planning.  While the vulnerability is in Oracle Hyperion Planning, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Planning accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-130875

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-783` |
| Published | 2026-11-17T20:17:54.270 |

tac_plus-ng before commit d8493e0 contains a stack-based buffer overflow vulnerability that allows clients holding the TACACS+ shared key to overflow a stack buffer due to an operator precedence error in author_pak_looks_bogus() and accounting_pak_looks_bogus(). Attackers can send packets whose argument-length table exceeds the payload, causing eval_args() to read past the packet and memcpy() oversized cmd values into cmdline, crashing the daemon or executing code.

### CVE-2026-21596

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-17T18:17:56.737 |

This High severity SSTI (Server-side Template Injection) vulnerability known as CVE-2026-21596 was introduced in version 12.0.0, 12.1.0.

This SSTI (Server-side Template Injection) vulnerability, with a CVSS Score of 7.7 and a CVSS Vector of CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N allows an authenticated attacker to execute arbitrary commands, which has high impact to confidentiality, high impact to integrity, high impact to availability, and requires no user interaction.

Atlassian recommends that Bamboo Data Center customers upgrade to the latest version. If you are unable to do so, upgrade your instance to the specified supported fixed version:
 Bamboo Data Center 12.1: Upgrade to a release greater than or equal to 12.1.13

See the release notes ([https://confluence.atlassian.com/bambooreleases/bamboo-release-notes-1189793869.html]). You can download the latest version of Bamboo Data Center from the download center ([https://www.atlassian.com/software/bamboo/download-archives]).

### CVE-2026-21593

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-17T18:17:56.373 |

This High severity OS Command Injection vulnerability known as CVE-2026-21593 was introduced in version 4.9.0.

This OS Command Injection vulnerability, with a CVSS Score of 7.7 and a CVSS Vector of CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N allows an authenticated attacker to execute arbitrary commands.

Atlassian recommends that Fisheye and Crucible Data Center and Server customers upgrade to the latest version. If you are unable to do so, upgrade your instance to the specified supported fixed version:

Fisheye and Crucible 4.9: Upgrade to a release greater than or equal to 4.9.16

See the Fisheye release notes (https://confluence.atlassian.com/fisheye/fisheye-release-notes-965552419.html) and Crucible release notes (https://confluence.atlassian.com/crucible/crucible-releases-298977378.html). You can download the latest version of Fisheye and Crucible from the Crucible Download Archives (https://www.atlassian.com/software/crucible/download-archives).

### CVE-2026-21592

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T18:17:55.843 |

This High severity Path Traversal (Arbitrary Read/Write) vulnerability known as CVE-2026-21592 was introduced in version 4.9.0.

This Path Traversal (Arbitrary Read/Write) vulnerability, with a CVSS Score of 7.7 and a CVSS Vector of CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:P allows an unauthenticated attacker to disclose protected application configuration files, which has high impact to confidentiality, no impact to integrity, no impact to availability, and requires no user interaction.

Atlassian recommends that Crucible Server customers upgrade to the latest version. If you are unable to do so, upgrade your instance to the specified supported fixed version:
 Crucible Server 4.9: Upgrade to a release greater than or equal to 4.9.16

See the Crucible Server release notes ([https://confluence.atlassian.com/crucible/crucible-releases-298977378.html]). You can download the latest version of Crucible from the Crucible Download Archives ([https://www.atlassian.com/software/crucible/download-archives]).

The following description summarizes the vulnerability reported via our Penetration Testing program:

Crucible do not account for path parameters when validating protected paths requested through the static-resource route. A crafted path segment passes validation, after which Jetty removes the path parameter during dispatch and resolves the request to a protected resource. This can expose files under WEB-INF and permit direct invocation of admin-area JSPs outside the normal interceptor and administrative password checks. An ordinary authenticated user can exploit the issue, and unauthenticated exploitation is possible when anonymous access is enabled.

### CVE-2026-130731

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-18T12:17:19.287 |

NocoDB before 2026.05.3 contains an account takeover vulnerability that allows invited users to complete other invitees' signups because batch invitations share one token across all recipients. Attackers holding a valid batch invite can submit another invitee's email with the shared non-expiring token to set its password and take over that account, including higher-role ones.

### CVE-2026-130717

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-18T12:17:17.160 |

NocoDB before 2026.04.1 fails to clear reset_password_token and reset_password_expires in users.service.ts when a password is changed, leaving earlier reset links valid. Attackers holding an unexpired reset link, such as from prior mailbox access, can set a new password and regain control of the account.

### CVE-2026-127340

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:58.130 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Financial Close Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Close Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Close Management accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-115176

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:51.713 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-115143

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:47.880 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-115117

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:45.053 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized read access to a subset of Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L).

### CVE-2026-115058

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:38.063 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-114866

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:15.293 |

Vulnerability in the Oracle Sales Online product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Online.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Sales Online, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Sales Online accessible data as well as  unauthorized update, insert or delete access to some of Oracle Sales Online accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-114865

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:15.177 |

Vulnerability in the Oracle Sales Online product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Online.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Sales Online, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Sales Online accessible data as well as  unauthorized update, insert or delete access to some of Oracle Sales Online accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-21595

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-17T18:17:56.613 |

This High severity Improper Authorization vulnerability was introduced in versions 10.2.0, 11.0.0, 12.0.0, and 12.1.0 of Bamboo Data Center.

This Improper Authorization vulnerability, with a CVSS Score of 7.6, allows an unauthenticated attacker to gain unintended access and can lead to the exposure of resources or functionality, possibly providing attackers with sensitive information or even execute arbitrary code.

Atlassian recommends that Bamboo Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
 Bamboo Data Center 10.2: Upgrade to a release greater than or equal to 10.2.26

 Bamboo Data Center 12.1: Upgrade to a release greater than or equal to 12.1.13

 Bamboo Data Center 13.0: Upgrade to a release greater than or equal to 13.0.1

See the release notes ([https://confluence.atlassian.com/bambooreleases/bamboo-release-notes-1189793869.html]). You can download the latest version of Bamboo Data Center from the download center ([https://www.atlassian.com/software/bamboo/download-archives]).

This vulnerability was reported via our Penetration Testing program.

### CVE-2026-100975

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-526` |
| Published | 2026-11-17T16:17:34.550 |

NVIDIA OpenShell for Linux contains a vulnerability in the Kubernetes sandbox SSH authentication configuration where a local attacker with low privileges could obtain sensitive authentication information by accessing an SSH handshake secret stored in a plaintext environment variable and reuse the shared secret to gain unauthorized access to other sandboxes. A successful exploit of this vulnerability might lead to information disclosure, data tampering, and denial of service.

### CVE-2026-131575

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-18T14:17:41.943 |

Tanium addressed an insertion of sensitive information into a log file vulnerability in TanOS.

### CVE-2026-130014

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T14:17:35.917 |

The Team VCard generator plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 1.1.0 via the 'photo' parameter parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information.

### CVE-2026-123123

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-18T14:17:29.483 |

An attacker that is able to send a crafted network packet to the affected component may trigger an integer overflow during module size validation. This may cause insufficient bounds checking and result in out-of-bounds memory reads, potentially leading to a denial of service condition due to process termination.

### CVE-2026-115815

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T14:17:26.537 |

The rus to lat advanced plugin for WordPress is vulnerable to blind SQL Injection via the 'name' parameter in all versions up to, and including, 1.1 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-127921

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T12:17:05.150 |

The AppPresser – Mobile App Framework plugin for WordPress is vulnerable to generic SQL Injection via the 'appp_cam_file[name]' parameter in all versions up to, and including, 5.0.0 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. Although the AJAX handler is registered for unauthenticated users, the only authorization gate is a nonce check, and the required nonce is only emitted to logged-in users viewing a page containing the [app-camera] shortcode, making Subscriber-level access the effective minimum requirement for exploitation.

### CVE-2026-119220

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-18T12:17:02.927 |

The Dokan: AI Powered WooCommerce Multivendor Marketplace Solution – Build Your Own Amazon, eBay, Etsy plugin for WordPress is vulnerable to Authorization Bypass in all versions up to, and including, 5.3.3. The vulnerability exists because the `matches_mcp_endpoint()` function applies an unanchored regular expression (`#/(?:woocommerce|dokan)/mcp(?:/|$)#`) against the entire `REQUEST_URI` including the query string, meaning any request that contains the literal substring `/dokan/mcp/` or `/woocommerce/mcp/` anywhere in its URI — including inside a query parameter value — is incorrectly treated as a trusted internal MCP context, causing `scope_product_permissions()` to unconditionally return `true` on WooCommerce's `woocommerce_rest_check_permissions` filter regardless of whether the caller is authenticated. This makes it possible for unauthenticated attackers to read full authenticated WooCommerce REST product records for any published product — including private underscore-prefixed meta, purchase notes, downloadable file URLs for paid digital products, catalog-hidden products, and edit-context representations — across the `/wc/v1`, `/wc/v2`, `/wc/v3`, and `/wc-analytics` REST namespaces. The bypass is triggered by appending a query parameter whose value contains the literal string `/dokan/mcp/` to any WooCommerce REST product endpoint (e.g., `/wp-json/wc/v3/products/{id}?x=/dokan/mcp/`); note that percent-encoding the slashes prevents the bypass, as the unencoded literal slash characters are required for the regex to match.

### CVE-2026-126963

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-18T00:18:36.483 |

Hinemos Agent Improper Certificate Validation Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Hinemos Agent. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the Hinemos Agent service. The issue results from the lack of proper validation of the certificate presented by a server. An attacker can leverage this vulnerability to execute code in the context of the service account. Was ZDI-CAN-28837.

### CVE-2026-91564

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:24.647 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-91551

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:24.080 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Platform Security for Java accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-91516

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-17T22:19:22.937 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Access Manager. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-83365

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:21.723 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in takeover of Oracle Purchasing. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-127427

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-17T22:19:08.130 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.22. Easily exploitable vulnerability allows unauthenticated attacker with network access via RDP to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-127413

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-17T22:19:06.780 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.22. Easily exploitable vulnerability allows unauthenticated attacker with network access via RDP to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-127373

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:02.090 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Close Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-127351

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:59.470 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Close Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-127331

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-17T22:18:57.197 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle AutoVue. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-115155

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:49.297 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115146

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:48.220 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-115101

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:43.220 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Planning. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-115065

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:38.943 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114981

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:29.023 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security Related Issues).   The supported version that is affected is 21.1.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in takeover of Oracle AutoVue. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114977

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:28.533 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Siebel Management Console).  Supported versions that are affected are 17.0-26.9. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-114955

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:25.910 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-114935

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:23.553 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Integration Broker).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-114930

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:22.987 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Application Server).  Supported versions that are affected are 8.61-8.63. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114929

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:22.877 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Application Server).  Supported versions that are affected are 8.61-8.63. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114912

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:20.970 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in takeover of Oracle Purchasing. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114911

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:20.847 |

Vulnerability in the Oracle iProcurement product of Oracle E-Business Suite (component: Approval List and Workflow).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle iProcurement.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iProcurement accessible data. CVSS 3.1 Base Score 7.5 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N).

### CVE-2026-114907

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:20.340 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in takeover of Oracle Purchasing. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114906

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:20.210 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in takeover of Oracle Purchasing. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114901

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:19.587 |

Vulnerability in the Oracle E-Business Suite Integrated SOA Gateway product of Oracle E-Business Suite (component: SOA Provider).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle E-Business Suite Integrated SOA Gateway.  Successful attacks of this vulnerability can result in takeover of Oracle E-Business Suite Integrated SOA Gateway. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114885

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:17.580 |

Vulnerability in the Oracle Mobile Field Service product of Oracle E-Business Suite (component: Admin UI).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Mobile Field Service.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Mobile Field Service accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-114882

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:17.227 |

Vulnerability in the Oracle Product Workbench product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Product Workbench.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Workbench accessible data. CVSS 3.1 Base Score 7.5 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N).

### CVE-2026-114864

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:15.060 |

Vulnerability in the Oracle Sales Online product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Online.  Successful attacks of this vulnerability can result in takeover of Oracle Sales Online. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114846

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:13.040 |

Vulnerability in the Oracle Financial Services Customer Screening product of Oracle Financial Services Applications (component: User Interface).   The supported version that is affected is 8.1.2.10. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Financial Services Customer Screening.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Financial Services Customer Screening accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-114799

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:07.543 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Planning accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-101693

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:04.580 |

Vulnerability in the Oracle Hyperion Financial Data Quality Management, Enterprise Edition product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Data Quality Management, Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Data Quality Management, Enterprise Edition. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-102529

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-17T21:17:36.250 |

HtmlSanitizer is a .NET library for cleaning HTML fragments and documents from constructs that can lead to XSS attacks. Prior to 9.0.967 and 9.1.968-beta, HtmlSanitizer CSS style-declaration sanitization can process an attacker-controlled style attribute with quadratic cost because SanitizeStyleDeclaration repeatedly causes the complete declaration to be serialized while removing disallowed CSS properties. One unauthenticated request can occupy a synchronous application worker for seconds, and concurrent requests can saturate all workers and sustain denial of service. This issue is fixed in versions 9.0.967 and 9.1.968-beta.

### CVE-2026-97699

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-11-17T20:18:00.220 |

Mistune is a Python Markdown parser with renderers and plugins. Prior to 3.3.4, inline image parsing sends nested ![ openers through precedence_scan because the no_link_before and _label_contains_link linearization guards are gated by not is_image. In src/mistune/inline_parser.py, each outer image opener can therefore search the remaining image body, while max_image_depth does not apply because the failed scans do not produce image tokens. Rendering untrusted Markdown with the default HTML renderer and no plugins can perform quadratic CPU work and keep a worker at 100 percent utilization. This issue is fixed in version 3.3.4.

### CVE-2026-97698

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-11-17T20:18:00.033 |

Mistune is a Python Markdown parser with renderers and plugins. Prior to 3.3.4, parse_link_href performs an unbounded parenthesis-balancing scan to the end of the document for each unmatched opening parenthesis reached through an empty [] link label. In src/mistune/helpers.py and src/mistune/inline_parser.py, the empty label bypasses no_close_bracket_before, and no_link_before advances only past the short label, so successive [] ( candidates repeatedly scan the remaining document. Rendering untrusted Markdown with the default HTML renderer and no plugins can perform quadratic CPU work and keep a worker at 100 percent utilization. This issue is fixed in version 3.3.4.

### CVE-2026-128073

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-248` |
| Published | 2026-11-17T20:17:42.827 |

gosaml2 is a Pure Go implementation of SAML 2.0. Prior to 0.12.0, ValidateEncodedResponse() calls decryptAssertions() on an EncryptedAssertion before signature or content validation completes, and EncryptedAssertion.DecryptBytes() in types/encrypted_assertion.go slices decoded ciphertext without first validating the required nonce or initialization-vector length. A CipherValue shorter than the 12-byte AES-GCM nonce causes a slice-bounds panic, and an empty AES-CBC CipherValue passes the modulo block-size check before causing a slice-bounds panic at the 16-byte initialization-vector split. An attacker needs only the service provider's public certificate to wrap a symmetric key, and no valid identity-provider signature or relationship is required. The unrecovered panic can terminate the request goroutine or the service process. This issue is fixed in version 0.12.0.

### CVE-2026-119192

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-17T20:17:36.063 |

Forge, also called node-forge, is a native implementation of Transport Layer Security in JavaScript. Prior to 1.4.1, publicKey.verify() with the default RSASSA-PKCS1-V1_5 scheme in lib/rsa.js parses the recovered DigestInfo with the lenient BER parser asn1.fromDer() and validates its structure with digestInfoValidator without requiring canonical DER bytes. Non-minimal or indefinite lengths, malformed parameter values, and non-canonical object identifier encodings with padded subidentifiers or trailing bytes can leave attacker-controlled data inside an accepted DigestInfo. When the verifying RSA public key uses a low exponent such as e=3, an attacker can use that encoding slack to forge a signature without the private key. The same path is used by X.509 certificate and PKCS#7 signature verification. This issue is fixed in version 1.4.1.

### CVE-2026-110789

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-130;CWE-400` |
| Published | 2026-11-17T20:17:35.790 |

libp2p is a JavaScript implementation of the libp2p networking stack. Prior to 5.1.22, the @libp2p/crypto code reached by the default Identify service accepts a remote peer’s crafted publicKey before peer-id or signature verification and passes it through publicKeyFromProtobuf to the ASN.1 DER decoder. readLength in packages/crypto/src/keys/rsa/der.ts accepts long-form element lengths larger than the remaining buffer, causing readInteger and related readers to loop synchronously over an attacker-claimed length from a very small key blob. Because decoding occurs in one event-loop tick before the remotePeer equality check in packages/protocol-identify/src/identify.ts, the Identify timeout cannot interrupt it, allowing repeated unauthenticated connections to stall all timers and peers and transiently exhaust memory. This issue is fixed in version 5.1.22.

### CVE-2026-119793

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-11-17T19:17:46.530 |

libp2p is a JavaScript implementation of the libp2p networking stack. Prior to 17.0.0, the @libp2p/gossipsub default configuration allows a connected remote peer to submit unsigned subscription RPC metadata for arbitrarily many distinct topic strings. handleReceivedSubscription in packages/gossipsub/src/gossipsub.ts creates a persistent topics-map entry for each accepted topic, while allowedTopics is unset by default, decodeRpc maxSubscriptions limits only one RPC rather than aggregate topic bytes, and peer scoring has no subscription-volume penalty. A single peer can therefore grow the topics map and committed heap toward out-of-memory conditions, and disconnecting additionally causes removePeer to scan all accumulated topic entries. This issue is fixed in version 17.0.0.

### CVE-2026-21599

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T18:17:56.973 |

This High severity Path Traversal (Arbitrary Read/Write) vulnerability known as CVE-2026-21599 was introduced in versions 10.2.0, 11.0.0, 12.0.0, and 12.1.0.

This Path Traversal (Arbitrary Read/Write) vulnerability, with a CVSS Score of 7.5 and a CVSS Vector of CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N allows an authenticated attacker to expose assets in your environment susceptible to exploitation.

Atlassian recommends that Bamboo Data Center customers upgrade to the latest version. If you are unable to do so, upgrade your instance to one of the specified supported fixed versions:

Bamboo Data Center 13.0: Upgrade to a release greater than or equal to 13.0.1
Bamboo Data Center 12.1: Upgrade to a release greater than or equal to 12.1.13
Bamboo Data Center 10.2: Upgrade to a release greater than or equal to 10.2.26

See the release notes (https://confluence.atlassian.com/bambooreleases/bamboo-release-notes-1189793869.html). You can
download the latest version of Bamboo Data Center from the download center
(https://www.atlassian.com/software/bamboo/download-archives).

### CVE-2026-130803

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-17T17:18:05.853 |

The firmware and flash memory store critical cryptographic secrets, such as global AES keys and network master keys, in unencrypted formats. Additionally, active session tokens (Store Pairing Tokens) are written to the flash in plaintext, exposing live network credentials.

### CVE-2026-122153

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-17T16:17:41.060 |

The TouchOffice API `clerkList` endpoint appears to return sensitive clerk authentication data, including clerk PINs and iButton serial numbers. If the endpoint is accessible to callers who do not require access to these values, the API exposes reusable authentication material beyond the minimum information necessary for clerk-list functionality.

### CVE-2026-122145

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-11-17T16:17:40.530 |

ICRTouch PocketTouch version 1.700 build 2025.3726 transmits the POS socket password in plaintext XML over an unencrypted TCP connection. The protocol does not provide transport-layer encryption to protect credentials from interception.

An attacker able to observe network traffic between a PocketTouch device and a TouchPoint POS terminal can recover the socket password from captured packets.

### CVE-2026-122143

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-749` |
| Published | 2026-11-17T16:17:40.400 |

ICRTouch Commander administrative interface performs security-sensitive operations through HTTP GET requests and includes an API key in the request query string. GET requests are commonly retained in browser history, proxy logs, server logs, analytics systems, referrer headers, and other intermediary records.

### CVE-2026-100980

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-17T16:17:35.193 |

NVIDIA OpenShell for Linux contains a vulnerability in its command-line diagnostic interface where an attacker could cause OS command injection because user- or configuration-supplied values are incorporated into a command that is interpreted by two successive shell layers in the remote path while being escaped for only one layer. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, information disclosure, data tampering, and denial of service.

### CVE-2026-100977

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-11-17T16:17:34.810 |

NVIDIA OpenShell for Linux contains a vulnerability in L7 REST policy enforcement where a local attacker with low privileges could exploit inconsistent HTTP interpretation by using cleartext HTTP/2 (h2c) over an HTTP CONNECT tunnel to bypass policy restrictions. A successful exploit of this vulnerability might lead to information disclosure and data tampering.

### CVE-2026-130627

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-17T15:17:40.190 |

The Vert.x HTTP client transport (a2a-java-sdk-http-client-vertx) hand-rolls a POST redirect follower that, when the documented PostBuilder.followRedirects(true) opt-in is enabled, re-issues the redirected request with the full request header map copied verbatim and performs no credential stripping and no same-authority check. A malicious, compromised, or mistyped agent that returns a 30x response with an absolute cross-host Location causes the client to forward the standard Authorization header (Bearer/Basic/OAuth) — plus every other header, including the allowlisted API-key headers — to the attacker-controlled authority. This breaks the project's own cross-transport invariant (SECURITY.md §8, OkHttpPostRedirectHeaderLeakTest) that credentials are stripped on cross-authority redirects even when redirects are followed. The sibling JDK and OkHttp/Android transports strip Authorization; Vert.x uniquely does not. This is a "fix introduced the bug" variant — the follower was added by the GHSA-9rhm hardening PR (3ae82912, refined by a5e76a0b).

### CVE-2026-130626

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-17T15:17:40.053 |

The core JDK HTTP client (a2a-java-sdk-http-client) applies the GHSA-9rhm redirect-neutralization only to the POST path. JdkGetBuilder.get(), JdkGetBuilder.getAsyncSSE(), and JdkDeleteBuilder.delete() call the injected httpClient directly, with no redirect gate. An application that supplies a redirect-capable HttpClient (Redirect.NORMAL/ALWAYS) — which is the SDK-documented way to enable POST redirects — silently follows cross-authority redirects on every credentialed GET/DELETE request. The JDK strips Authorization cross-origin, but forwards the four allowlisted custom credential headers (X-API-Key, API-Key, X-Auth-Token, X-Authentication) to the attacker-controlled authority. This is an incomplete-fix variant of GHSA-9rhm: the fix hardened the default client and added a POST-only two-step opt-in, but never covered GET/DELETE.

### CVE-2026-115826

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T14:17:26.707 |

The Multi Step for Contact Form 7 plugin for WordPress is vulnerable to Insecure Direct Object Reference in all versions up to, and including, 2.9.1 via the '_cf7mls_db_form_data_id' parameter due to missing validation on a user controlled key. This makes it possible for unauthenticated attackers to permanently delete arbitrary stored Contact Form 7 submissions from the database. Exploitation requires the companion CF7 Database plugin to be active and the per-form "Save every step, not just the final submission" option to be enabled.

### CVE-2026-107644

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-18T14:17:22.213 |

The Bizuno Accounting – ERP/Accounting/CRM (for WordPress) plugin for WordPress is vulnerable to Authentication Bypass via Password Reset Token Disclosure in all versions up to, and including, 7.4.5 via the `bizUser` parameter of the `validateReset()` function on the `portal/api/lostPW` endpoint. This is due to `portalCtl::goAPI()` failing to call `loadBusinessCache()` before invoking the handler, which causes `isMailConfigured()` to read an empty business cache and return false regardless of the site's actual mail configuration, causing the fully-qualified reset URL — containing the victim's live reset UUID and numeric user ID — to be embedded directly in the HTML response rather than delivered by email. This makes it possible for unauthenticated attackers to obtain a valid password-reset token for any Bizuno account, including administrators, directly from the HTTP response and submit it to the `portal/api/lostVal` endpoint to rewrite the victim's password and achieve full account takeover. The administrator email address required to initiate the reset is frequently exposed by the plugin's own login error messages and the public `/bizuno/` portal page, making exploitation trivial against most installations.

### CVE-2026-110307

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1025` |
| Published | 2026-11-18T02:17:39.280 |

An incorrect authorization vulnerability was identified in GitHub Enterprise Server that allowed an authenticated user whose numeric user ID matched an enterprise's numeric ID to manage that enterprise's GitHub Apps and generate private keys without enterprise membership. GitHub App ownership checks compared numeric IDs without checking the owner's account type. Exploitation required control of a session for the colliding user account and an enterprise-owned GitHub App. A generated private key could be used to authenticate as the App and access repositories where it was installed, within its granted permissions. On standard fresh installations, the documented collision involved the non-loginable built-in ghost account; the reported GHES reproduction used site administrator impersonation. This vulnerability affected supported GitHub Enterprise Server releases prior to 3.23 and was fixed in versions 3.19.16, 3.20.12, 3.21.10, and 3.22.5. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-112740

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T01:17:49.387 |

A command injection vulnerability was identified in GitHub Enterprise Server that allowed an authenticated site administrator to execute arbitrary commands as the host git user on peer Git server nodes outside the pre-receive hook sandbox by supplying a crafted pre-receive environment download URL. Exploitation required a clustered deployment using custom pre-receive hook environments and at least one peer Git server node. This vulnerability affected all versions of GitHub Enterprise Server prior to 3.23 and was fixed in versions 3.22.5, 3.21.10, 3.20.12, and 3.19.16. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-91586

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:25.900 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N).

### CVE-2026-127426

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:08.020 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.22. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle VM VirtualBox accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-127360

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:00.533 |

Vulnerability in the Oracle Hyperion Financial Close Management product of Oracle Hyperion (component: Reconciliation Manage).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via SMB to compromise Oracle Hyperion Financial Close Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Close Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Close Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115178

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:51.937 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115163

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:50.203 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115160

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:49.860 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115141

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:47.660 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Planning accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Planning accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115140

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:47.550 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Planning accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Planning accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115138

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:47.327 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Planning accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Planning accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115124

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:45.737 |

Vulnerability in the Oracle Hyperion Planning product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Planning.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Planning accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Planning accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-115053

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:37.477 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114940

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:24.050 |

Vulnerability in the Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition product of Oracle Java SE (component: JSSE).  Supported versions that are affected are Oracle Java SE: 8u511b33, 8u511b33-perf, 11.0.33.0.3, 17.0.21.0.3, 21.0.13.0.3, 25.0.5.0.3, 27.0.1.0.3; Oracle GraalVM for JDK: 17.0.21.0.3 and  21.0.13.0.3; Oracle GraalVM Enterprise Edition: 21.3.20.0.3. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TLS to compromise Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition accessible data as well as  unauthorized access to critical data or complete access to all Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition accessible data. Note: This vulnerability can be exploited by using APIs in the specified Component, e.g., through a web service which supplies data to the APIs. This vulnerability also applies to Java deployments, typically in clients running sandboxed Java Web Start applications or sandboxed Java applets, that load and run untrusted code (e.g., code that comes from the internet) and rely on the Java sandbox for security. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114939

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:23.920 |

Vulnerability in the Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition product of Oracle Java SE (component: JGSS).  Supported versions that are affected are Oracle Java SE: 8u511b33, 8u511b33-perf, 11.0.33.0.3, 17.0.21.0.3,  21.0.13.0.3, 25.0.5.0.3, 27.0.1.0.3; Oracle GraalVM for JDK: 17.0.21.0.3 and  21.0.13.0.3; Oracle GraalVM Enterprise Edition: 21.3.20.0.3. Difficult to exploit vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition accessible data as well as  unauthorized access to critical data or complete access to all Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition accessible data. Note: This vulnerability applies to Java deployments, typically in clients running sandboxed Java Web Start applications or sandboxed Java applets, that load and run untrusted code (e.g., code that comes from the internet) and rely on the Java sandbox for security. This vulnerability does not apply to Java deployments, typically in servers, that load and run only trusted code (e.g., code installed by an administrator). CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114903

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:19.823 |

Vulnerability in the Oracle E-Business Suite Integrated SOA Gateway product of Oracle E-Business Suite (component: Web Service Provider).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle E-Business Suite Integrated SOA Gateway.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle E-Business Suite Integrated SOA Gateway accessible data as well as  unauthorized access to critical data or complete access to all Oracle E-Business Suite Integrated SOA Gateway accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114894

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:18.720 |

Vulnerability in the Oracle Universal Work Queue product of Oracle E-Business Suite (component: Media Integration issues).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Universal Work Queue.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Universal Work Queue accessible data as well as  unauthorized access to critical data or complete access to all Oracle Universal Work Queue accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114877

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:16.647 |

Vulnerability in the Oracle iStore product of Oracle E-Business Suite (component: Shopping Cart).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle iStore.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iStore accessible data as well as  unauthorized access to critical data or complete access to all Oracle iStore accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114872

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:16.070 |

Vulnerability in the Oracle Sales Online product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Sales Online.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Sales Online, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Sales Online accessible data. CVSS 3.1 Base Score 7.4 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N).

### CVE-2026-101848

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:05.043 |

Vulnerability in the Oracle Hyperion Financial Data Quality Management, Enterprise Edition product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Financial Data Quality Management, Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Data Quality Management, Enterprise Edition accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Data Quality Management, Enterprise Edition accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-101663

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:04.350 |

Vulnerability in the Oracle Mobile Field Service product of Oracle E-Business Suite (component: Admin UI).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Mobile Field Service.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Mobile Field Service accessible data as well as  unauthorized access to critical data or complete access to all Oracle Mobile Field Service accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-82139

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-17T20:17:56.847 |

Dell SupportAssist OS Recovery, versions prior to 5.5.16.3, contain an Improper Certificate Validation vulnerability. An unauthenticated attacker with local access could potentially exploit this vulnerability, leading to Protection mechanism bypass.

### CVE-2026-82138

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-17T20:17:56.707 |

Dell SupportAssist OS Recovery, versions prior to 5.5.16.3 contain a Download of Code Without Integrity Check vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Code execution.

### CVE-2026-82038

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-17T20:17:56.343 |

Bludit through 3.22.0 contains an improper session invalidation vulnerability that allows demoted users to retain revoked privileges because Login::isLogged() never re-reads the session-stored role. Attackers holding a session issued while their account was an administrator can keep using it after demotion to perform administrator actions such as creating new administrator accounts.

### CVE-2026-21602

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-17T18:17:57.347 |

This High severity Stored XSS vulnerability was introduced in version 10.3.26 of Jira Core Data Center and Jira Software Data Center. 
	
	This Stored XSS vulnerability, with a CVSS Score of 7.4, allows an authenticated attacker to execute arbitrary HTML or JavaScript code on a victims browser. 
	
	Atlassian recommends that Jira Core Data Center and Jira Software Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
		
		* Jira Core Data Center and Jira Software Data Center 10.3: Upgrade to a release greater than or equal to 10.3.27
		
		* Jira Core Data Center and Jira Software Data Center 11.3: Upgrade to a release greater than or equal to 11.3.13
		
		
	
	See the release notes (https://www.atlassian.com/software/jira/download-archives). You can download the latest version of Jira Core Data Center and Jira Software Data Center from the download center (https://www.atlassian.com/software/jira/download-archives). 
	
	This vulnerability was reported via our Penetration Testing program.

### CVE-2026-21591

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-17T18:17:55.700 |

This High severity PrivEsc (Privilege Escalation) vulnerability was introduced in versions 10.2.0, 11.0.0, 12.0.0, and 12.1.0 of Bamboo Data Center.

This PrivEsc (Privilege Escalation) vulnerability, with a CVSS Score of 7.4, allows an authenticated attacker to perform actions as a higher-privileged user.

Atlassian recommends that Bamboo Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
 Bamboo Data Center 10.2: Upgrade to a release greater than or equal to 10.2.26

 Bamboo Data Center 12.1: Upgrade to a release greater than or equal to 12.1.13

 Bamboo Data Center 13.0: Upgrade to a release greater than or equal to 13.0.1

See the release notes ([https://confluence.atlassian.com/bambooreleases/bamboo-release-notes-1189793869.html]). You can download the latest version of Bamboo Data Center from the download center ([https://www.atlassian.com/software/bamboo/download-archives]).

This vulnerability was reported via our Penetration Testing program.

### CVE-2026-112117

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T02:17:39.580 |

A Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') in ASUS System Control Interface , allows a local, low-privileged user to gain full control over arbitrary existing files and folders outside the allowed directories via a crafted path containing dot-segment sequences that satisfies a folder prefix check, which can lead to unauthorized read and modification of protected files and may result in local privilege escalation.
Refer to the '
Security Update for ASUS System Control Interface  ' section on the ASUS Security Advisory for more information.

### CVE-2026-91540

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:23.623 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows high privileged attacker with network access via SAML to compromise Oracle Access Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Access Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Access Manager accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-114888

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:17.930 |

Vulnerability in the Oracle Mobile Field Service product of Oracle E-Business Suite (component: Admin UI).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Mobile Field Service executes to compromise Oracle Mobile Field Service.  While the vulnerability is in Oracle Mobile Field Service, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Mobile Field Service accessible data as well as  unauthorized update, insert or delete access to some of Oracle Mobile Field Service accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-114869

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:15.710 |

Vulnerability in the Applications DBA product of Oracle E-Business Suite (component: AD Utilities).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Applications DBA executes to compromise Applications DBA.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Applications DBA. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-96665

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T14:17:46.103 |

The SendPress Newsletters plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'sp_firstname' parameter in all versions up to, and including, 1.26.1.20 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The public subscriber-management route uses an unsigned, forgeable base64-encoded JSON token, allowing an unauthenticated attacker to impersonate any subscriber and obtain a valid nonce — bypassing the POST handler's only access control check.

### CVE-2026-95789

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-18T14:17:45.807 |

Command injection vulnerability in the affected interface of AOS-10 or AOS-8 could allow an authenticated remote attacker to perform command injection only on certain impacted devices. Successful exploitation could allow an attacker to execute unauthorized arbitrary commands with the privileges of the affected mechanism on the underlying operating system.

### CVE-2026-126131

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T14:17:30.637 |

The WP Instant Feeds plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'data[images][][url]' parameter in all versions up to, and including, 1.3.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The cache-write AJAX endpoint is accessible to unauthenticated users because the only access control is a nonce check against a nonce minted for uid 0 and freely emitted on any front-end page rendering a feed via wp_localize_script, making it harvestable by any unauthenticated visitor.

### CVE-2026-125053

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T14:17:30.060 |

The WEB-Translation – eTranslation Multilingual plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 2.0.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit requires that at least one secondary language is configured in the plugin and that comments are open on the target post; because the stored payload contains no literal HTML brackets at save-time, WordPress core KSES filtering does not remove it, and the malicious script is only materialized when a visitor loads the post under a secondary-language URL slug.

### CVE-2026-116758

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T14:17:27.540 |

The Advanced Country Blocker plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'REQUEST_URI' parameter in all versions up to, and including, 2.3.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected script is stored via the advcb_live_activity transient on the init hook and executed when an administrator views the Live Monitor page, as the stored URI is unsafely concatenated into a double-quoted HTML title attribute and inserted into the DOM via jQuery .html().

### CVE-2026-116519

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T14:17:26.870 |

The Geo Mashup plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'author (comment form) / display_name (profile form)' parameter in all versions up to, and including, 1.13.23 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The comment-author path requires the crafted comment to be approved before the payload is served to visitors; the subscriber-level path requires the plugin's user-location mapping feature to be enabled.

### CVE-2026-107516

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T14:17:21.913 |

Dell PowerStore contains an OS command injection vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability, potentially leading to arbitrary command execution with root privileges.

### CVE-2026-130333

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T13:17:27.153 |

The SNORDIAN's H5PxAPIkatchu plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'xapi' parameter in all versions up to, and including, 0.4.24 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce required to reach the unauthenticated insert endpoint is publicly exposed in the listener.js script URL on every page displaying H5P content, making the injection trivially exploitable by any anonymous visitor.

### CVE-2026-125033

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T13:17:24.860 |

The Smash Balloon Social Post Feed – Simple Social Feeds for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'attachments.data[].description' parameter in all versions up to, and including, 4.15.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This makes it possible for unauthenticated outside Facebook users — any party able to contribute an attachment description to a post ingested by the configured feed (visitor posts, shared posts, or attached content) — to plant payloads that execute against every anonymous visitor of any WordPress page carrying the shortcode, requiring no WordPress account whatsoever.

### CVE-2026-113699

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T13:17:24.727 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in Aidata Bilişim Kurumsal Tic. Ve San. A.Ş. Aidata WR854GVR allows OS Command Injection.

This issue affects Aidata WR854GVR: before V4.0.18_261111.

### CVE-2026-96571

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:24.153 |

The FancyBox for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Anchor 'href' Attribute in all versions up to, and including, 3.4.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the attacker to wrap the payload anchor around a smilie shortcode (e.g., :mrgreen:), which WordPress renders as an &lt;img&gt; element, satisfying the plugin's a:has(img) enrollment selector and disguising the malicious link as an ordinary comment emoticon.

### CVE-2026-130721

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-18T12:17:17.767 |

NocoDB from 2026.06.2 before 2026.08.0 contains an authorization bypass vulnerability that allows authenticated base Editors to write to data-read-only sources by abusing the internal batch endpoint. Attackers can name a writable decoy table on the batch envelope and target a read-only source table in dataUpdate, dataInsert or dataDelete sub-operations to modify or destroy records.

### CVE-2026-130701

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T12:17:14.740 |

NocoDB before 2026.10.1 contains an SQL injection vulnerability because select-field option titles are embedded into MySQL or MariaDB enum/set column definitions with only single-quote doubling, leaving backslashes unescaped. A base creator or owner can end an option title with a backslash to escape the literal and append ALTER TABLE clauses, adding, dropping or renaming columns and altering indexes in the connected database.

### CVE-2026-120686

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:04.010 |

The AMP for WP – Accelerated Mobile Pages plugin for WordPress is vulnerable to Stored Cross-Site Scripting in versions up to, and including, 1.1.19 via comment content rendered on AMP post pages. The plugin registers an output-buffer callback ampforwp_the_content_filter_full() on the 'wp' action (priority 999) that applies a set of tag-agnostic and quote-agnostic regular expressions — notably /onclick=[^>]*/ — to the entire AMP page output after approved comments have already been echoed into it; these regexes do not understand HTML tag or attribute-value boundaries, so a kses-legal comment that places strings like 'onclick="' inside a title attribute value can trigger deletion of the title's closing quote, causing the browser to re-parse what was previously textual content inside the attribute value as live HTML attributes. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page, after an administrator has approved the comment.

### CVE-2026-119635

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:03.240 |

The Groundhogg plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'post_title' merge-tag of the [ghr] shortcode in versions up to, and including, 4.10 The post_title replacement is registered with 'nested' => true, so the nested branch of Replacements::do_replacement() returns the merge value through tackle_replacements() without passing it through escape_merge_tags()/escape_shortcodes(); the callback single_post() calls html_entity_decode(get_the_title(), ENT_QUOTES), converting the entity-encoded text that wp_filter_kses leaves intact on a Contributor's post title back into raw HTML, which is then emitted into the rendered post. This makes it possible for authenticated attackers, with Contributor-level access and above, to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-119161

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:02.770 |

The HTML Forms – Simple WordPress Forms Plugin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'arbitrary POST parameter NAME (the array key, not the value)' parameter in all versions up to, and including, 1.7.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Script execution does not require the Screen Options panel to be opened — injected attributes on the hidden-column checkboxes fire on page load as soon as the Submissions tab is rendered.

### CVE-2026-116536

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:02.353 |

The Custom Twitter Feeds – A Tweets Widget or X Feed Widget plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'atts (JSON object, specifically the inner `feed` key)' parameter in all versions up to, and including, 2.11.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload is first stored in the wp_ctf_feed_caches database table and later written into the ctf_cron_report WordPress option by the scheduled ctf_feed_update cron job, meaning execution is deferred until the cron runs and an administrator subsequently loads the Support page.

### CVE-2026-116530

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T12:17:02.203 |

The Check & Log Email – Easy Email Testing & Mail logging plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'author' parameter in all versions up to, and including, 2.0.17 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires an administrator to approve the comment carrying the shortcode payload, and the target page must render the core Latest Comments block, which passes comment author names through do_shortcode via the_content.

### CVE-2026-111825

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T06:17:28.000 |

The Event Tickets with Ticket Scanner plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'code' parameter in all versions up to, and including, 3.3.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload persists through WooCommerce session data into order-item metadata and executes when rendered in the ticket scanner interface.

### CVE-2026-130121

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T04:17:14.167 |

The AI Puffer - MCP Server for Claude & ChatGPT, with AI Chatbot plugin for WordPress is vulnerable to Stored Cross-Site Scripting via AI-generated comment replies in all versions up to, and including, 2.5.28 due to insufficient sanitization of the AI model's output in the insert_comment_reply_logic() function, which saves replies with wp_insert_comment() and bypasses the kses filtering WordPress normally applies to comment content. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page, by submitting a comment that leads the AI model to reproduce an HTML payload in its automated reply. This is only exploitable when an administrator has configured a Comment Auto-Reply automation task with 'Action on reply' set to 'Approve' (the default is 'Hold for moderation'), and the attacker's comment has been approved.

### CVE-2026-91531

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:23.400 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Access Manager accessible data as well as  unauthorized read access to a subset of Oracle Access Manager accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N).

### CVE-2026-91498

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:22.343 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SAML to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Access Manager accessible data as well as  unauthorized read access to a subset of Oracle Access Manager accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N).

### CVE-2026-69188

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98;CWE-434` |
| Published | 2026-11-17T22:19:21.413 |

WeGIA is a web manager for charitable institutions. Prior to 3.9.1, a user with backup-management permission can upload a crafted gzip-compressed tar archive through web/html/configuracao/importar_dump.php, after which web/controle/control.php accepts a user-controlled modulo value and combines it with nomeClasse for require_once(). By using a phar:// path to the uploaded archive and selecting the whitelisted InternoControle, whose empty resource list is treated as authorized, the user can cause an embedded controller file and its requested method to execute as the web-server process. The attack path depends on the configured BKP_DIR, and enabling phar.readonly or phar.require_hash does not prevent PHP from reading the gzip tar archive through phar://. Successful exploitation permits access to or modification of sensitive data, configuration, credentials, source files, host commands, and services reachable by the web-server account. This issue is fixed in version 3.9.1.

### CVE-2026-127394

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:04.513 |

Vulnerability in the Product Lifecycle Analytics product of Oracle Supply Chain (component: Installation Issues).   The supported version that is affected is 3.6.1. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Product Lifecycle Analytics executes to compromise Product Lifecycle Analytics.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Product Lifecycle Analytics, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Product Lifecycle Analytics accessible data as well as  unauthorized access to critical data or complete access to all Product Lifecycle Analytics accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-115072

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:39.793 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114951

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:25.410 |

Vulnerability in the MySQL Server, MySQL Cluster product of Oracle MySQL (component: Server: Logging).  Supported versions that are affected are MySQL Server: 8.4.0-8.4.13, 9.7.0-9.7.4, 26.10; MySQL Cluster: 8.0.0-8.0.50, 8.4.0-8.4.13, 9.7.0-9.7.4 and  26.10. Easily exploitable vulnerability allows high privileged attacker with network access via multiple protocols to compromise MySQL Server, MySQL Cluster.  Successful attacks of this vulnerability can result in takeover of MySQL Server, MySQL Cluster. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114950

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:25.293 |

Vulnerability in the MySQL Server, MySQL Cluster product of Oracle MySQL (component: Server: Optimizer).  Supported versions that are affected are MySQL Server: 8.4.0-8.4.13, 9.7.0-9.7.4, 26.10; MySQL Cluster: 8.0.0-8.0.50, 8.4.0-8.4.13, 9.7.0-9.7.4 and  26.10. Easily exploitable vulnerability allows high privileged attacker with network access via multiple protocols to compromise MySQL Server, MySQL Cluster.  Successful attacks of this vulnerability can result in takeover of MySQL Server, MySQL Cluster. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114949

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:25.167 |

Vulnerability in the MySQL Server, MySQL Cluster product of Oracle MySQL (component: Server: Replication).  Supported versions that are affected are MySQL Server: 8.4.0-8.4.13, 9.7.0-9.7.4, 26.10; MySQL Cluster: 8.0.0-8.0.50, 8.4.0-8.4.13, 9.7.0-9.7.4 and  26.10. Easily exploitable vulnerability allows high privileged attacker with network access via multiple protocols to compromise MySQL Server, MySQL Cluster.  Successful attacks of this vulnerability can result in takeover of MySQL Server, MySQL Cluster. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114927

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:22.627 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Report Distribution).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114902

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:19.703 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in takeover of Oracle Product Hub. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114884

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:17.460 |

Vulnerability in the Oracle Lease and Finance Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Lease and Finance Management.  Successful attacks of this vulnerability can result in takeover of Oracle Lease and Finance Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114883

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:17.347 |

Vulnerability in the Oracle Teleservice product of Oracle E-Business Suite (component: Service Request Form).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Teleservice.  Successful attacks of this vulnerability can result in takeover of Oracle Teleservice. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-101839

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:04.933 |

Vulnerability in the Oracle Contracts product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Contracts.  Successful attacks of this vulnerability can result in takeover of Oracle Contracts. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-101838

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:04.813 |

Vulnerability in the Oracle Contracts product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Contracts.  Successful attacks of this vulnerability can result in takeover of Oracle Contracts. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-68918

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-17T21:18:12.147 |

Ikaros is a content management system for ACGMN media. Prior to 1.2.0, server/src/main/java/run/ikaros/server/core/tag/TagEndpoint.java does not enforce tag ownership for authenticated users with tag permissions. GET /tags/condition accepts an arbitrary userId and can enumerate another user's tags, DELETE /tag/id/{id} deletes a tag without comparing its owner to the requester, and DELETE /tag/condition omits userId from its filter and can delete every user's tags matching the supplied condition. This issue is fixed in version 1.2.0.

### CVE-2026-65963

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-15;CWE-20` |
| Published | 2026-11-17T21:18:11.677 |

Pi-hole FTL is the core engine of the Pi-hole network-level advertisement and tracker blocker. From 6.6.2 until 6.7, PATCH /api/config accepts unfiltered CivetWeb lua_* options through webserver.advancedOpts, while POST /api/teleporter writes attacker-controlled content from a dhcp.leases archive entry through src/zip/teleporter.c without content validation. An authenticated administrator can place controlled file content on disk, point a Lua execution option at that file, and rely on the advancedOpts configuration change to restart FTL. CivetWeb then executes the file as Lua through the processing in src/webserver/webserver.c, allowing arbitrary commands to run as the pihole operating-system user and persist across restarts while the configuration and file remain. This issue is fixed in version 6.7.

### CVE-2026-95788

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-18T14:17:45.673 |

An unauthenticated buffer overflow vulnerability exists in the underlying operating system of AOS-10 or AOS-8 and could allow an unauthenticated adjacent attacker to conduct a denial of service attack. Successful exploitation could allow an attacker to disrupt the availability of the affected system, with a limited impact to the integrity of the affected component.

### CVE-2026-122042

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129;CWE-787` |
| Published | 2026-11-18T14:17:29.320 |

WarehousePG (WHPG) 6.27.1 through 6.27.7 and 7.2.1 through 7.6.1 are affected by an out-of-bounds write vulnerability (CWE-787) in gpfdist, the file server used to load and unload external tables. When gpfdist attaches a request to a session, it sizes two internal arrays from the client-supplied X-GP-SEGMENT-COUNT header and writes to them at the index given by the X-GP-SEGMENT-ID header, without checking that the index is non-negative and smaller than the count (CWE-129). gpfdist does not authenticate callers unless gpfdists is used with client certificate verification, so an attacker who can reach the gpfdist port can crash it with a single HTTP request, failing every external table load or unload that uses that gpfdist instance. gpfdist is normally reachable only from the cluster's internal network.

### CVE-2026-108761

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T14:17:24.710 |

The UpdraftPlus: WP Backup & Migration Plugin for WordPress is vulnerable to second-order SQL Injection via the user profile description field in all Free versions up to, and including, 1.26.15 and all Premium versions up to, and including, 2.26.15. This makes it possible for authenticated attackers, with subscriber-level access and above, to store a malicious payload that is written into a database backup and executed as SQL when an administrator later restores that backup. Successful exploitation can modify sensitive WordPress data and, on sites where plugin installation is available, lead to remote code execution through the installation and activation of an attacker-controlled plugin.

### CVE-2026-130715

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T12:17:16.860 |

NocoDB before 2026.08.0 contains an sql injection vulnerability that allows authenticated Creator or Owner users to execute database functions by supplying zero-argument function calls as column default values. Attackers can plant functions like version() or inet_server_addr() in PostgreSQL or MySQL column definitions and read results through record APIs, disclosing server addresses, role names, and engine details.

### CVE-2026-130711

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T12:17:16.240 |

NocoDB before 2026.09.0 contains an authorization bypass vulnerability in extract-ids.middleware.ts that allows authenticated users to resolve roles against another base by supplying an MCP token id in the query string. Attackers with Viewer access on one base can mint an MCP token and pass its id to read another base's metadata, including table lists and member email addresses.

### CVE-2026-130697

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-18T12:17:14.430 |

NocoDB from 0.301.4 before 2026.10.0 contains an information disclosure vulnerability that allows authenticated workspace viewers to read pending invitation tokens through the workspace member list. Attackers can redeem an exposed higher-privileged invitation token at signup to claim the invited account and escalate to roles such as workspace owner.

### CVE-2026-130696

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-18T12:17:14.277 |

NocoDB before 2026.10.1 contains a credential exposure vulnerability in the connection-test endpoint that allows authorized integration users to redirect stored credentials by overriding connection host, port, and user fields. Attackers can point the test at a server they control to capture offline-crackable PostgreSQL md5 or MySQL handshakes and recover the stored database password.

### CVE-2026-130673

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T12:17:10.197 |

Craft CMS from 5.0.0 before 5.11.5 contains an sql injection vulnerability that allows authenticated low-privilege users to inject raw SQL by passing nested array parameters into Element::findOne() criteria. Attackers can set the query's where property through endpoints like users/delete-address and users/save-address to perform blind boolean or time-based injection and read database contents.

### CVE-2025-59912

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T11:17:37.600 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in the URL: TareasCrear' parameter in'/Tareas/TareasCrear/

### CVE-2025-59911

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T11:17:37.473 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in the URL: TareasCrear' parameter in'/Tareas/TareasCrear/

### CVE-2025-59910

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T11:17:37.340 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in the URL: ClientesClasificaciones' parameter in'/Clientes/ClientesClasificaciones/

### CVE-2025-59909

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T11:17:37.210 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in the URL: ClientesCamposAdicionales' parameter in'/Clientes/ClientesCamposAdicionales/

### CVE-2025-59908

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T11:17:37.077 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in the URL: 
idCliente' parameter in'/Gestion/DocumentosCrear/

### CVE-2026-131876

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-11-18T03:17:42.397 |

fqterm 0.9.9 before 0.9.11 contains an out-of-bounds memory access vulnerability in its SSH client that trusts unchecked server-supplied length fields for allocations, copies and read positions. Malicious servers or man-in-the-middle attackers can send crafted lengths in getString(), KEXINIT name-lists, key parsing or packet framing before host key verification to crash the client.

### CVE-2026-125276

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-18T03:17:40.883 |

Pleasanter contains an issue with insertion of sensitive information into sent data in the API. If the affected product receives a specially crafted API request sent by a remote authenticated attacker, the authentication credentials of other users, including administrators, such as API keys, may be obtained. As a result, the attacker may perform arbitrary operations on the affected product with the privileges associated with the obtained credentials.

### CVE-2026-111801

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T01:17:49.223 |

An authorization bypass through user-controlled key vulnerability was identified in GitHub Enterprise Server that allowed authenticated users to read review-thread data from private repositories they could not access. An attacker required an authenticated account, a readable repository and pull request to use as the request context, and target review-thread identifiers. The thread-preview endpoint resolved supplied identifiers without restricting them to the authorized pull request, exposing private file paths and, when positioning and diff data were available, source-code excerpts, commit identifiers, and line metadata without victim interaction. This vulnerability affected supported GitHub Enterprise Server releases in the 3.21, 3.22 series and was fixed in versions 3.21.10, 3.22.5. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-131854

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-18T00:18:43.440 |

Ettercap through 0.8.5.1 contains a heap out-of-bounds read vulnerability in dissector_mysql() in src/dissectors/ec_mysql.c that copies seed and password bytes without bounds checks. A malicious MySQL server or client can send truncated greeting or login packets to leak adjacent heap memory through hex-encoded output in the interface and log.

### CVE-2026-131844

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-11-18T00:18:41.757 |

Poppler through 26.11.0 contains an uncontrolled memory allocation vulnerability in the libcurl-based remote file loader that trusts unvalidated HEAD Content-Length values in CurlCachedFileLoader::init(). Malicious HTTP servers can return an enormous Content-Length so CachedFile resizes its chunk cache accordingly, aborting pdfinfo or PDFDocFactory-based applications with std::bad_alloc for denial of service.

### CVE-2026-127428

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:08.243 |

Vulnerability in the MySQL Server, MySQL Cluster product of Oracle MySQL (component: Server: GIS).  Supported versions that are affected are MySQL Server: 8.4.0-8.4.13, 9.7.0-9.7.4, 26.10; MySQL Cluster: 8.0.0-8.0.50, 8.4.0-8.4.13, 9.7.0-9.7.4 and  26.10. Easily exploitable vulnerability allows low privileged attacker with network access via multiple protocols to compromise MySQL Server, MySQL Cluster.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of MySQL Server, MySQL Cluster and  unauthorized read access to a subset of MySQL Server, MySQL Cluster accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H).

### CVE-2026-127423

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:07.787 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.22. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle VM VirtualBox accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H).

### CVE-2026-127422

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:07.677 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.22. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle VM VirtualBox accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H).

### CVE-2026-127414

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:19:06.890 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.22. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle VM VirtualBox accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H).

### CVE-2026-127339

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:58.010 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle AutoVue executes to compromise Oracle AutoVue.  While the vulnerability is in Oracle AutoVue, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle AutoVue accessible data. CVSS 3.1 Base Score 7.1 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N).

### CVE-2026-127319

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:55.777 |

Vulnerability in the Oracle AutoVue product of Oracle Supply Chain (component: Security).   The supported version that is affected is 21.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle AutoVue.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle AutoVue accessible data as well as  unauthorized update, insert or delete access to some of Oracle AutoVue accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-115177

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:51.827 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L).

### CVE-2026-115159

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:49.750 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-115064

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:38.827 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-115063

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:38.677 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-115061

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:38.410 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N).

### CVE-2026-115057

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:37.950 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.26.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-114915

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:21.310 |

Vulnerability in the Oracle E-Business Suite Secure Enterprise Search product of Oracle E-Business Suite (component: Search Integration Engine).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle E-Business Suite Secure Enterprise Search.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle E-Business Suite Secure Enterprise Search accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle E-Business Suite Secure Enterprise Search. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-114913

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:21.080 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Purchasing as well as  unauthorized update, insert or delete access to some of Oracle Purchasing accessible data. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H).

### CVE-2026-114898

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:19.197 |

Vulnerability in the Applications DBA product of Oracle E-Business Suite (component: AD Utilities).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Applications DBA executes to compromise Applications DBA.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Applications DBA accessible data as well as  unauthorized access to critical data or complete access to all Applications DBA accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-114878

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:16.760 |

Vulnerability in the Oracle iStore product of Oracle E-Business Suite (component: Shopping Cart).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iStore.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle iStore accessible data as well as  unauthorized update, insert or delete access to some of Oracle iStore accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-114873

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:16.190 |

Vulnerability in the Oracle iProcurement product of Oracle E-Business Suite (component: Internal operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iProcurement.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle iProcurement accessible data as well as  unauthorized update, insert or delete access to some of Oracle iProcurement accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-114867

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:15.437 |

Vulnerability in the Oracle Sales Online product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Online.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Sales Online accessible data as well as  unauthorized read access to a subset of Oracle Sales Online accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-82142

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T20:17:57.137 |

Dell SupportAssist OS Recovery, versions prior to 5.5.16.3, contain a Missing Authorization vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-130872

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-17T20:17:53.787 |

Pytition before 2.10 contains an insecure direct object reference vulnerability in the show_signatures view that allows registered users to delete other petitions' signatures by supplying foreign signature IDs. Attackers can post sequential signature IDs to their own petition's signatures page to permanently delete signatures from any user-owned petition and trigger confirmation emails to other signers.

### CVE-2026-130851

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-17T20:17:50.437 |

wishthis through 1.2.3 contains an authorization bypass vulnerability in User::ownsWishlist() that allows authenticated users to modify other users' wishes and wishlists. Attackers can supply sequential wish_id and wishlist_id values to the wishes and wishlists API handlers to edit wishes, add wishes, or rename and delete wishlists.

### CVE-2026-62267

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-17T19:18:00.283 |

matrix-hookshot is a Matrix bot for connecting to external services like GitHub, GitLab, JIRA, and more. Prior to 7.3.3, Hookshot can crash in src/Bridge.ts while processing a modern Matrix reply whose m.relates_to.m.in_reply_to.event_id identifies an event that the bot cannot read. Bridge event handling calls botClient.getEvent() for the parent event without catching the resulting M_NOT_FOUND error, allowing the rejected request to escape reply processing and terminate the service. This issue is fixed in version 7.3.3.

### CVE-2026-113781

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-195;CWE-787` |
| Published | 2026-11-17T19:17:45.347 |

ESP-IDF is the Espressif Internet of Things (IoT) Development Framework. Prior to 5.2.8, 5.3.6, 5.5.6, and 6.0.3, the Bluedroid BLE Mesh GATT server read handler bt_mesh_bta_gatts_cb in esp_ble_mesh stores a signed attribute-read callback length in an unsigned 16-bit variable. A negative ATT error code is therefore interpreted as a very large successful length and used for a memory copy from a small stack buffer into the GATT response structure. A remote attacker within Bluetooth LE range who can connect to an exposed PB-GATT provisioning or Mesh Proxy service can trigger a failed attribute read with a crafted request. On devices where the affected attributes are accessible without pairing, exploitation requires neither pairing nor user interaction; access requirements depend on device configuration. The resulting out-of-bounds read and stack-based buffer overflow corrupts the Bluetooth host task stack, causing a crash and device restart and potentially further memory corruption. The issue affects devices built with CONFIG_BT_BLUEDROID_ENABLED=y and BLE Mesh GATT enabled; the NimBLE host path is not affected. This issue is fixed in versions 5.2.8, 5.3.6, 5.5.6, and 6.0.3.

### CVE-2026-126548

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-17T17:17:58.823 |

Server-Side Request Forgery (SSRF) vulnerability in Broadcom AutoSys Workload Automation (Workload Control Center (WCC) modules) on Windows, Linux allows Server Side Request Forgery.This issue affects AutoSys Workload Automation: from 12.1.01 Cum 03 through 12.1.01 Cum 06, from 24.0 through 24.2.00.

### CVE-2026-123050

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-17T15:17:33.763 |

Multiple Farmasimplex healthcare integration modules do not properly validate TLS certificates, allowing an attacker who can intercept network traffic to impersonate trusted healthcare services and perform man-in-the-middle attacks, potentially leading to disclosure or modification of sensitive data.

### CVE-2026-130726

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T12:17:18.523 |

NocoDB before 2026.07.0 contains an SQL injection vulnerability in its MySQL and SQLite clients that inserts the column precision value into generated data-definition statements without numeric validation. Authenticated users with the Creator or Owner base role can supply a crafted precision value when creating or updating a column to close the type declaration and execute arbitrary SQL against the base's data source.

### CVE-2026-130694

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T12:17:13.937 |

NocoDB from 2026.07.0 before 2026.10.0 contains an sql injection vulnerability that allows users with Creator role to inject SQL through unescaped backslashes in the DATETIME_FORMAT formula format argument on MySQL-backed bases. Attackers can place a backslash before a quote to terminate the DATE_FORMAT string literal and read any data reachable by the data source's database user, including tables outside the base.

### CVE-2026-119469

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-18T02:17:40.520 |

Incorrect default permissions in the ASUS DisplayWidget Center allow a local, low-privileged user to achieve arbitrary code execution in the security context of another user via a crafted executable placed in that user-writable directory, which the application launches when the other user runs it and uses a particular feature.Refer to the '
Security Update for ASUS Display Widget Center ' section on the ASUS Security Advisory for more information.

### CVE-2026-126976

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.0/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-18T00:18:38.210 |

llama.cpp MTMD Multimodal GGUF File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of llama.cpp. User interaction is required to exploit this vulnerability in that the target must open a malicious file.

The specific flaw exists within the parsing of audio multimodal projector GGUF files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before allocating a buffer. An attacker can leverage this vulnerability to execute arbitrary code in the context of the current process. Was ZDI-CAN-30980.

### CVE-2026-115077

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:40.367 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.26.0.000. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Infrastructure Technology executes to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-114942

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:24.297 |

Vulnerability in the Oracle Java SE, Oracle GraalVM for JDK product of Oracle Java SE (component: Libraries).  Supported versions that are affected are Oracle Java SE: 21.0.13.0.3, 25.0.5.0.3 and  27.0.1.0.3; Oracle GraalVM for JDK: 21.0.13.0.3. Difficult to exploit vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Java SE, Oracle GraalVM for JDK.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Java SE, Oracle GraalVM for JDK as well as  unauthorized update, insert or delete access to some of Oracle Java SE, Oracle GraalVM for JDK accessible data and  unauthorized read access to a subset of Oracle Java SE, Oracle GraalVM for JDK accessible data. Note: This vulnerability can only be exploited by supplying data to APIs in the specified Component without using Untrusted Java Web Start applications or Untrusted Java applets, such as through a web service. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H).

### CVE-2026-114941

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T22:18:24.177 |

Vulnerability in the Oracle Java SE, Oracle GraalVM for JDK product of Oracle Java SE (component: Compiler).  Supported versions that are affected are Oracle Java SE: 21.0.13.0.3, 25.0.5.0.3 and  27.0.1.0.3; Oracle GraalVM for JDK: 21.0.13.0.3. Difficult to exploit vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Java SE, Oracle GraalVM for JDK.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Java SE, Oracle GraalVM for JDK as well as  unauthorized update, insert or delete access to some of Oracle Java SE, Oracle GraalVM for JDK accessible data and  unauthorized read access to a subset of Oracle Java SE, Oracle GraalVM for JDK accessible data. Note: This vulnerability can only be exploited by supplying data to APIs in the specified Component without using Untrusted Java Web Start applications or Untrusted Java applets, such as through a web service. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H).

### CVE-2026-130835

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T20:17:47.917 |

Storyden before 1.26.17 contains a missing authorization vulnerability in the AccountRemoveRole handler that allows non-administrator users with MANAGE_ROLES to remove administrator roles. Attackers can send DELETE requests to the account roles endpoint to demote other administrators, potentially leaving the instance with no administrator.

### CVE-2026-121716

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-17T20:17:36.727 |

fzf is a command-line fuzzy finder. Prior to 0.74.5, bin/fzf-tmux validates separately supplied layout sizes but does not validate attached -l and -u layout values before Bash arithmetic expansion, allowing command substitution in a crafted operand to execute as the invoking user during option parsing. The same validation failure lets space-bearing popup geometry options -x, -y, -w, -h, and -p reach an unquoted tmux popup option string and inject additional tmux flags. Exploitation requires less-trusted project configuration, a wrapper, or a plugin to supply the poisoned value and requires the victim to invoke fzf-tmux; normal values are usually trusted, and the script has been superseded by built-in tmux options. This issue is fixed in version 0.74.5.
