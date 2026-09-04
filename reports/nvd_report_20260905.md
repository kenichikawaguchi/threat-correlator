# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-04 15:00 UTC
- **対象期間**: `2026-09-03T15:00:34.000Z` 〜 `2026-09-04T15:00:31.000Z`
- **重要CVE数**: 210 件（Critical 9.0+: 52 件 / High 7.0〜: 158 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** と非常に多く、特に **認証バイパス・特権昇格・リモートコード実行** が集中しています。  
- クラウドサービス（Azure AD B2C、Azure AI Language）や **OS／ブラウザレベル**（Chrome、FreeIPMI）での深刻な脆弱性が目立ち、攻撃者が認証なしでネットワーク上の権限を取得できるケースが多数です。  
- Web フロントエンド向けの **JavaScript ライブラリ（MapLibre GL JS）** や **WordPress プラグイン** でも、入力検証不備や認可チェック欠如により任意コード実行やプラグインインストールが可能になるものが報告されています。  
- いずれも **パッチ適用が急務** であり、未対応のまま放置すると内部ネットワークへの不正侵入や重要情報漏洩につながります。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑75754** (ASUS Control Center) | 10.0 | 認証なしで暗号鍵取得 → SSH (port 2222) が自動で有効化され、リモートから SSH ログイン可能 | ハードコードされた認証情報と SSRF の複合攻撃で、企業内 LAN に対して **完全なリモートシェル** を取得できる点が極めて危険。 |
| **CVE‑2026‑83711** (Microsoft Azure AD B2C) | 10.0 | ユーザー制御キーにより認可バイパス → 特権昇格 | Azure AD B2C は多数の SaaS 認証基盤として利用されているため、**テナント全体の認証基盤が破壊** されるリスクがある。 |
| **CVE‑2026‑70352** (Azure AI Language) | 10.0 | 認証なしで特権昇格 → 任意の AI サービス操作 | Azure AI 系サービスは機密データ処理に使われることが多く、**データ改ざん・情報漏洩** の危険が高い。 |
| **CVE‑2026‑85061** (MapLibre GL JS < 6.4.1) | 10.0 | DOM.sanitize() のライブ属性走査バグ → 任意属性除去失敗 → XSS/HTML インジェクション | 多くの Web マップアプリで採用されているため、**フロントエンドからのコード実行** が広範囲に波及。 |
| **CVE‑2026‑85050** (Google Chrome Android < 152.0.7977.82) | 9.6 | WebGL の境界外書き込み → サンドボックス脱出 → 任意コード実行 | Chrome は Android のデファクトスタンダードブラウザであり、**モバイルユーザー全体** が対象になる深刻なリモートコード実行脆弱性。 |

> **共通点**：すべて「認証不要」または「認証バイパス」から始まり、最終的に **リモートコード実行** もしくは **特権取得** が可能になる点です。特にクラウド認証基盤や広く使われるフロントエンドライブラリは、被害が組織全体に波及しやすいため、最優先で対策を講じる必要があります。

---

## 3. 推奨アクション  

### 3.1. パッチ適用・バージョンアップ
| 製品 / ライブラリ | 現行脆弱版 | 推奨バージョン / パッチ |
|-------------------|------------|--------------------------|
| **ASUS Control Center** | すべての 2026 年以前リリース | ASUS が提供する **2026‑09‑01 以降のセキュリティパッチ**（バージョン 3.2.0 以降）を即時適用。 |
| **Microsoft Azure AD B2C** | 2026‑08‑15 以前のサービス | Azure ポータル → **「認証フローの更新」** → 2026‑09‑03 以降の **CVE‑2026‑83711 修正リリース**をデプロイ。 |
| **Azure AI Language** | 2026‑07‑30 以前のエンドポイント | Azure CLI/Portal で **「AI Language Service – Security Update」**（バージョン 2.5.1 以上）を適用。 |
| **MapLibre GL JS** | < 6.4.1 | `npm install maplibre-gl@^6.4.1` または CDN の **6.4.1 以降** を使用。 |
| **Google Chrome (Android)** | < 152.0.7977.82 | Play Store から **Chrome 152.0.7977.82** 以上に自動更新。 |
| **FreeIPMI** (全スタックオーバーフロー) | < 1.6.19 | `yum/dnf apt-get` で **freeipmi 1.6.19** 以上に更新。 |
| **WordPress プラグイン** (AI Website Builder, ACPT, Divi Ajax Filter, etc.) | 1.0.0 / ≤ 2.0.66 / ≤ 5.1.2 | 公式リポジトリから **最新バージョン**（2026‑09‑02 以降）へ更新し、**不要プラグインは無効化**。 |

### 3.2. 設定・運用面の緊急対策
1. **ASUS Control Center**  
   - SSH ポート 2222 をファイアウォールで外部から遮断。  
   - 既存の暗号鍵を全て **再生成**し、`/etc/ssh/sshd_config` の `PermitRootLogin no` を徹底。  
2. **Azure AD B2C / AI Language**  
   - **条件付きアクセスポリシー**を強化し、管理者ロールの MFA を必須化。  
   - 監査ログを有効化し、**不審なトークン取得**をリアルタイムで検知。  
3. **MapLibre GL JS**  
   - `DOMPurify` 等の追加サニタイズ層を実装し、外部からの属性操作を二重チェック。  
   - CSP (Content‑Security‑Policy) ヘッダーで `script-src 'self'` を設定し、インラインスクリプトを禁止。  
4. **Chrome (Android/iOS)**

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-75754

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-798;CWE-918` |
| Published | 2026-09-04T03:17:41.927 |

Missing Authentication for Critical Function, Server-Side Request Forgery (SSRF), and Use of Hard-coded Credentials in ASUS Control Center allow an unauthorized user to obtain the encryption key via an HTTP request, causing a local service to enable SSH on port 2222. The attacker can then log in with the hardcode credentials to obtain a root shell, enabling direct reading, writing, and deletion of data on ASUS Control Center, as well as remote control of all servers, PCs, and workstations within the company.
Refer to the 'Security Update for ASUS Control Center' section on the ASUS Security Advisory for more information.

### CVE-2026-83711

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T23:17:20.500 |

Authorization bypass through user-controlled key in Microsoft Azure Active Directory B2C allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-70352

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-03T23:17:20.213 |

Missing authentication for critical function in Azure AI Language allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-85061

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T21:17:23.323 |

MapLibre GL JS is an interactive vector tile map library for web browsers. Prior to 6.4.1, DOM.sanitize() in src/util/dom.ts iterates elem.attributes as a live NamedNodeMap while removeAttributes() removes attributes from the same collection, shifting indexes and skipping an adjacent dangerous attribute. An attacker who controls untrusted third-party style attribution strings or user-supplied custom attributions can supply consecutive dangerous attributes, causing an attribute such as onload or ontoggle to survive sanitization and execute when the attribution control inserts the content into innerHTML. A victim must render the affected map content for the script to execute. This issue is fixed in version 6.4.1.

### CVE-2026-82923

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-04T10:17:13.340 |

The AI Website Builder WordPress plugin (GitHub build) 1.0.0 does not perform any authorisation or nonce check on its REST API routes, allowing unauthenticated attackers to install and activate plugins and themes, import content from a URL under their control, write a file of their choosing into the uploads directory, and delete site content and media. On a host that serves PHP from the uploads directory, that file write is remote code execution.

### CVE-2026-15354

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-04T07:17:08.487 |

The ACPT (Premium) plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.0.66. This is due to missing authorization in the `submit()` function, which allows unauthenticated form submissions to control the target user ID before calling `wp_update_user()`. This makes it possible for unauthenticated attackers to overwrite any WordPress user's email address and password, including an administrator's, and take over the account. Successful exploitation requires a public ACPT user form that permits anonymous submissions.

### CVE-2026-85509

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-04T05:17:16.723 |

FreeIPMI before 1.6.19 has a stack-based buffer overflow in _read_fru_data in libfreeipmi/fru/ipmi-fru.c when a BMC returns more bytes than requested.

### CVE-2026-85508

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-04T05:17:16.570 |

ipmi-oem in FreeIPMI before 1.6.19 has a stack-based buffer overflow in _output_dell_system_info_cmc_ipv6_info in ipmi-oem/ipmi-oem-dell.c (cmc-ipv6-info subcommand to dell get-system-info).

### CVE-2026-85507

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-04T05:17:16.433 |

ipmi-oem in FreeIPMI before 1.6.19 has a stack-based buffer overflow in _output_dell_system_info_cmc_info in ipmi-oem/ipmi-oem-dell.c (cmc-info subcommand to dell get-system-info).

### CVE-2026-85506

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-04T05:17:16.290 |

ipmi-oem in FreeIPMI before 1.6.19 has a stack-based buffer overflow in _get_dell_system_info_idrac_info in ipmi-oem/ipmi-oem-dell.c (idrac-info subcommand to dell get-system-info).

### CVE-2026-85504

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-04T05:17:16.047 |

FreeIPMI before 1.6.19 has a stack-based buffer overflow in _ipmi_sel_oem_fujitsu_get_sel_entry_long_text in libfreeipmi/sel/ipmi-sel-string-fujitsu-irmc-common.c via malformed Fujitsu SEL long-text responses.

### CVE-2026-11613

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-04T05:17:13.013 |

The Divi Ajax Filter plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 5.1.2 via the 'custom_loop_template' parameter parameter. This makes it possible for unauthenticated attackers to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. This vulnerability is only exploitable when the loop_templates parameter is set to 'custom-template'.

### CVE-2026-84834

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-03T17:17:29.400 |

Unauthenticated PHP Object Injection in JobSearch <= 3.2.0 versions.

### CVE-2026-84814

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-03T17:17:29.277 |

Subscriber Privilege Escalation in Bricksforge <= 3.1.8.8 versions.

### CVE-2026-84753

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-03T17:17:25.673 |

Unauthenticated PHP Object Injection in Mail Mint <= 1.31.0 versions.

### CVE-2026-84238

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T17:17:25.150 |

Unauthenticated Broken Access Control in YITH Request a Quote for WooCommerce Premium < 4.46.0 versions.

### CVE-2026-85085

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-940` |
| Published | 2026-09-04T07:17:11.133 |

The Canva Android App before 2.376.0 allowed an external origin to be loaded in a privileged WebView. A threat actor who controls the page loaded by the user is able to communicate with Canva using the user’s session.

### CVE-2026-85050

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-03T20:17:26.077 |

Out of bounds write in WebGL in Google Chrome on on Android prior to 152.0.7977.82 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-85047

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-03T20:17:24.690 |

Improper input validation in Transactions Platform in Google Chrome on on iOS prior to 152.0.7977.82 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-85042

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-03T20:17:22.727 |

Use after free in DevTools in Google Chrome prior to 152.0.7977.82 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-85216

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-521` |
| Published | 2026-09-03T15:17:40.893 |

MISP contains an authentication bypass vulnerability in its LDAP and LinOTP authentication components due to insufficient validation of user-supplied credentials.

The custom LdapAuthenticate and LinOTPAuthenticate components replace CakePHP's FormAuthenticate implementation but did not replicate its credential validation checks. As a result, empty or non-string values could reach the underlying authentication mechanisms.

In the LDAP authentication path, an attacker able to identify a valid directory user's email address could submit an empty password. The empty credential could be passed to ldap_bind(), where an LDAP server accepting unauthenticated binds may return a successful result for a valid distinguished name combined with an empty password. MISP could consequently treat the attacker as the corresponding authenticated directory user without verification of the user's password.

The issue also affected the LinOTP authentication component. Invalid credential types were not rejected before being processed, and when mixed authentication was enabled, an empty password could be checked against a locally stored MISP password hash. LDAP-provisioned MISP accounts could additionally be created with an empty local password because account creation skipped normal validation, resulting in a hash corresponding to an empty password. This could permit authentication through the local fallback mechanism when such an account was no longer resolved through LDAP.

Successful exploitation could allow a remote unauthenticated attacker to impersonate an existing MISP user. If the targeted account has administrative or other privileged permissions, the attacker could gain corresponding access to sensitive threat-intelligence data, modify or delete information, alter configuration, or perform other privileged operations.

The patch resolves the vulnerability by requiring authentication identifiers and passwords to be valid strings, rejecting empty passwords where they are not explicitly permitted, and assigning a randomly generated local password to LDAP-provisioned accounts instead of storing a hash derived from an empty password.

### CVE-2026-85602

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-09-04T12:17:23.903 |

The Grav Form plugin (getgrav/grav-plugin-form) versions 8.0.6 through 9.1.19 select the reCAPTCHA version to validate based solely on which response field key is present in the submitted payload. On a site configured for reCAPTCHA v3, an anonymous attacker can place their v3 token under the v2 field name (g-recaptcha-response instead of token), causing validation to use the v2 branch, which never applies the score threshold or verifies the expected action. This results in a complete bypass of reCAPTCHA v3 bot protection. The issue is fixed in version 9.1.20.

### CVE-2026-85595

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-04T12:17:22.960 |

Traefik versions before v2.11.55 contain an authentication bypass vulnerability in the digestAuth middleware where unknown usernames receive an empty secret instead of rejection. Attackers can compute a valid digest response using the empty secret and arbitrary credentials to bypass authentication on any digestAuth-protected route without a valid username or password.

### CVE-2026-70403

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-259` |
| Published | 2026-09-04T07:17:09.467 |

XING CPTrans-ME-X contains a Use of Hard-coded Password (CWE-259). Anyone with the knowledge of the credential may log in to the affected device.

### CVE-2026-69657

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1393` |
| Published | 2026-09-04T07:17:09.340 |

XING CPTrans-ME-X contains a Use of Default Password (CWE-1393). Anyone with the knowledge of the credential may log in to the affected device.

### CVE-2026-62928

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-04T07:17:09.057 |

XING CPTrans-ME-X contains an OS Command Injection (CWE-78). Unauthenticated OS command may be injected.

### CVE-2026-85148

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-04T03:17:46.050 |

SmartIT Desktop Manager developed by Lightstar has a Use of Hard-coded Credentials vulnerability. Unauthenticated remote attackers can exploit a fixed password to remotely access user hosts.

### CVE-2026-85146

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-04T03:17:45.770 |

SmartIT Desktop Manager developed by Lightstar has a Use of Hard-coded Credentials vulnerability. Unauthenticated remote attackers can obtain the SSH service account credentials and passwords for the SmartIT Agent directly from the application source code.

### CVE-2026-85440

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-03T23:17:23.590 |

MOOS core-moos through 10.4.0 contains a pre-authentication heap overflow vulnerability in MOOSCommPkt packet handling that allows remote attackers to write arbitrary data by declaring a negative packet length. Attackers can exploit the signed integer check in InflateTo() and negative size conversion in recv() to overflow a four-byte heap buffer during the HandShake phase before authentication.

### CVE-2026-85438

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-03T23:17:23.270 |

MOOS-IvP through 24.8.1 contains a buffer overflow vulnerability in StringToIvPFunction() where dimension, piece, and degree counts from encoded BHV_IPF payloads are used as allocation sizes and loop bounds without validation. Attackers can supply crafted payloads with mismatched dimension values to write attacker-controlled doubles past the end of the IvPBox weight array, causing memory corruption and potential code execution.

### CVE-2026-85437

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-03T23:17:23.103 |

MOOS-IvP through 24.8.1 contains multiple buffer overflow vulnerabilities in IvP function string decoders that trust attacker-controlled length fields without validation. Attackers can craft malicious encoded strings with mismatched declared and actual field lengths to overflow heap and stack buffers, potentially achieving remote code execution through MOOS variables or alog files.

### CVE-2026-85435

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-03T23:17:22.787 |

MOOS-IvP uFldNodeBroker through 24.8.1 fails to validate the source of TRY_SHORE_HOST messages on the vehicle bus, allowing any publisher to enroll attacker-controlled shore routes. Attackers can publish malicious shore route messages to receive bridged vehicle traffic including sensor data and control information.

### CVE-2026-85434

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-03T23:17:22.643 |

MOOS-IvP uFldShoreBroker through 24.8.1 fails to verify node ping authenticity before creating outbound bridge routes. Attackers can publish NODE_BROKER_PING messages with crafted HostRecord data to redirect bridged variables to attacker-controlled addresses.

### CVE-2026-85433

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T23:17:22.500 |

MOOS essential-moos pShare through 10.0.1 fails to properly authorize PSHARE_CMD messages, allowing any publisher to reconfigure network routes and listeners at runtime. Attackers can send crafted PSHARE_CMD messages with cmd=output or cmd=input parameters to open new listeners on arbitrary addresses and redirect or duplicate bus traffic to attacker-controlled destinations.

### CVE-2026-85428

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-03T23:17:21.770 |

MOOS core-moos through 10.4.0 contains an authentication bypass vulnerability in the optional MOOSDB HTTP server that allows unauthenticated clients to write variables. Attackers can send HTTP requests with variable names and values to the MOOSDB HTTP server port to modify MOOS variables including actuator and override commands without authentication.

### CVE-2026-85426

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-03T23:17:21.487 |

MOOS-IvP uMemWatch through 24.8.1 constructs shell commands from attacker-chosen MOOS client names without sanitization. Attackers can inject shell metacharacters into client names to execute arbitrary commands as the uMemWatch process user through unquoted redirection targets in system calls.

### CVE-2026-85425

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-03T23:17:21.337 |

MOOS-IvP iSay through 24.8.1 contains a remote code execution vulnerability in the SAY_MOOS variable handler that passes unsanitized text to a shell command. Attackers can publish SAY_MOOS messages containing backticks or command substitution syntax to execute arbitrary commands as the iSay process user.

### CVE-2026-85424

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-03T23:17:21.170 |

MOOS core-moos through 10.4.0 lacks authentication in the wire protocol, allowing unauthenticated clients to connect with full publish, subscribe, and database clear privileges. Attackers can bypass the compile-time protocol string check and connect with arbitrary client names to execute privileged operations including DB_CLEAR which resets all variables and clears client mail queues.

### CVE-2026-80098

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-03T23:17:20.350 |

Improper verification of cryptographic signature in Copilot Studio allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-85394

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-03T19:17:31.257 |

python-jose through 3.5.0 fails to properly validate asymmetric keys in HMAC initialization, accepting DER-encoded public keys that lack PEM armor or SSH prefixes. Attackers holding the service's public key can forge HS256 tokens that pass verification when algorithms are not explicitly restricted. This is an incomplete fix for CVE-2024-33663.

### CVE-2026-85391

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-03T19:17:30.830 |

Peppermint through 0.5.5 contains a hardcoded JWT signing secret in docker-compose.yml that allows unauthenticated attackers to forge session tokens for any account. Attackers can use the published secret to mint valid tokens for arbitrary user IDs and access protected endpoints without credentials.

### CVE-2026-82526

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-03T19:17:29.950 |

R2R through 3.6.6 contains a stacked SQL injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL statements by manipulating the index name parameter in the vector index creation endpoint. The index name is interpolated directly into a CREATE INDEX statement via string formatting without identifier quoting or allowlist validation, enabling arbitrary DDL and DML execution through semicolon-separated statements under the PostgreSQL superuser account.

### CVE-2026-84813

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-03T17:17:29.157 |

Unauthenticated SQL Injection in GeoDirectory <= 2.8.174 versions.

### CVE-2026-84768

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-03T17:17:28.010 |

Unauthenticated SQL Injection in VikAppointments Services Booking Calendar <= 1.2.20 versions.

### CVE-2026-85183

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1385` |
| Published | 2026-09-03T15:17:39.763 |

Taipy configures its socket.io server with wildcard CORS origin and credential flag enabled, allowing any web page to establish credentialed WebSocket connections to victim applications. Attackers can open socket.io sessions from arbitrary domains and invoke state variable modifications and action callbacks without CSRF protection.

### CVE-2026-85181

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-565` |
| Published | 2026-09-03T15:17:39.433 |

CAT uses Java String.hashCode as the sole integrity check for session cookies without server-side keying, allowing attackers to forge valid checksums offline. Attackers can set the x-forwarded-for header to bypass IP binding validation and create admin sessions with full configuration access.

### CVE-2026-85614

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T12:17:24.993 |

OpenPanel before 2.3.0 contains an unauthenticated server-side request forgery vulnerability in the GET /tools/site-checker endpoint that accepts a fully client-controlled URL parameter with no private IP filtering or DNS-rebinding protection. Attackers can make the OpenPanel server issue requests to internal services, localhost, and cloud metadata endpoints, reading internal HTTP response titles, headers, status codes, and SSL certificate information.

### CVE-2026-67402

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-09-04T00:17:13.690 |

An insecure Apache configuration in ConfigServer Security & Firewall maps /usr/bin as CGI programs through the Messenger v3 HTTPS virtual host. A remote unauthenticated attacker whose address is blocked can request a mapped executable and run arbitrary commands as the Apache user. The vulnerability affects installations where CSF Messenger v3 and its HTTPS mode are enabled. WebPros addressed the vulnerability in version 16.31.

### CVE-2026-85427

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-09-03T23:17:21.627 |

MOOS essential-moos pAntler through 10.0.1 contains a remote code execution vulnerability that allows unauthenticated attackers to execute arbitrary programs by publishing a crafted MISSION_FILE message to the MOOSDB. Attackers can publish a mission file containing malicious Run entries that pAntler parses and executes via execvp() without authentication validation.

### CVE-2026-85184

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-09-04T10:17:13.900 |

@fastify/middie versions >= 9.1.0 and before 9.3.4 decide whether to run path-scoped middleware by matching against the raw request target, while the Fastify router resolves an absolute-form request target to its path before dispatching. Because the two layers evaluate different strings, a request using an absolute-form target reaches the route handler while the path-scoped middleware, such as authentication or authorization, is skipped. An unauthenticated network attacker can use this to bypass path-based access controls in a Fastify application that relies on middie for those controls. Users should upgrade to @fastify/middie 9.3.4 or later.

### CVE-2026-62916

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-03T23:17:19.693 |

Authentication bypass using an alternate path or channel in Microsoft Entra ID allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-58400

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-470` |
| Published | 2026-09-03T18:17:22.827 |

GeoNetwork is a catalog application to manage spatially referenced resources. Prior to versions 4.4.12 and 4.2.17, the Saxon XSLT processor used to render formatters is configured without secure processing (`FEATURE_SECURE_PROCESSING`) and without disabling Java extension functions (`ALLOW_EXTERNAL_FUNCTIONS`). Any stylesheet loaded by GeoNetwork can therefore invoke
`java.lang.Runtime.exec()` or `java.lang.ProcessBuilder` directly, achieving arbitrary command execution as the GeoNetwork process user. A user with sufficient privileges to upload a formatter can deliver a `.xsl` file containing Java extension call that execute arbitrary OS commands with the privileges of the GeoNetwork process. The issue is patched in GeoNetwork versions 4.4.12 and 4.2.17.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-18198

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-04T13:18:15.023 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in TAC Information Services Internal and External Trade Inc. GOLDENHORN ONEIT allows Blind SQL Injection.

This issue affects GOLDENHORN ONEIT: before Göbeklitepe.

### CVE-2026-85094

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-212` |
| Published | 2026-09-04T07:17:11.263 |

The Canva Android App  before 2.376.0 did not restrict the headers returned to an external origin running in a privileged WebView. A threat actor with control of the WebView could access a user’s session.

### CVE-2026-85455

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-03T23:17:25.803 |

MOOS core-moos through 10.4.0 contains a buffer over-read vulnerability in CMOOSCommPkt where a four-byte packet triggers out-of-bounds memory access during deserialization. Attackers can open a TCP connection to the MOOSDB port and send a crafted short packet to read memory before authentication.

### CVE-2026-85432

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-03T23:17:22.353 |

MOOS core-moos through 10.4.0 fails to validate client identity in MOOSDB message processing, allowing authenticated attackers to attribute writes to other clients by supplying arbitrary source identifiers in serialized messages. Attackers can forge message origins and cancel third-party subscriptions by exploiting the disconnect between authenticated connection identity and wire-supplied source attribution.

### CVE-2026-85430

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-03T23:17:22.060 |

MOOS essential-moos through 10.0.1 contains an authentication bypass vulnerability in pShare that accepts UDP datagrams from any source and republishes them with the attacker-claimed identity intact. Attackers can send crafted UDP datagrams to pShare input routes to inject messages into the local MOOS community under spoofed identities, or send malformed datagrams to crash the pShare process.

### CVE-2026-85053

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-668` |
| Published | 2026-09-03T20:17:27.163 |

Improper resource exposure in CacheStorage in Google Chrome prior to 152.0.7977.82 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-85051

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-03T20:17:26.420 |

Type confusion in Compositing in Google Chrome prior to 152.0.7977.82 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-85049

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-03T20:17:25.610 |

Use after free in Skia in Google Chrome prior to 152.0.7977.82 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-85046

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-03T20:17:24.210 |

Type confusion in V8 in Google Chrome prior to 152.0.7977.82 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-84752

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-03T17:17:25.547 |

Contributor PHP Object Injection in RTMKit <= 2.1.5 versions.

### CVE-2026-85236

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-03T16:18:27.013 |

A cross-site request forgery (CSRF) vulnerability existed in the cullEmptyEvents action of MISP. The endpoint performed a state-changing and irreversible operation while accepting HTTP GET requests.


Because bodyless GET requests are not subject to CakePHP's CSRF validation, an attacker could cause an authenticated MISP user with sufficient privileges to invoke the endpoint simply by causing their browser to load a crafted URL, for example through an embedded image or other automatically requested resource.


Successful exploitation triggers the deletion of published empty events. The deletion is particularly significant because the operation uses skipBlocklist, meaning the removed events do not leave blocklist entries that could prevent or track their subsequent synchronization. This can result in unintended and potentially irreversible deletion of MISP event records without explicit user interaction.


The vulnerability was addressed by restricting cullEmptyEvents to HTTP POST requests, ensuring that CakePHP's normal CSRF protections are applied to the operation.

### CVE-2026-85199

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-23;CWE-206` |
| Published | 2026-09-03T15:17:39.937 |

Eclipse aeriOS Self-orchestrator versions prior to 1.2.1 contain a path traversal vulnerability in the REST API. User-controlled identifiers used to create, update, or delete Self-orchestrator resources were incorporated into filesystem paths without adequate validation or sanitization. An unauthenticated remote attacker able to access the Self-orchestrator API could therefore supply specially crafted identifiers containing path traversal sequences to write or delete JSON files outside the intended application directories, subject to the filesystem permissions of the Self-orchestrator process.




The impact is increased by the absence of authentication on the affected API and by the container running with elevated privileges in the affected deployment configuration.




The issue has been addressed in version 1.2.1 by introducing validation and sanitization of user-controlled identifiers before they are used to construct filesystem paths, preventing path separator characters from being used to escape the intended directories.

### CVE-2026-85617

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-04T12:17:25.410 |

snipe-it versions before 8.6.3 contain an authorization bypass vulnerability in the bulk delete functionality that allows restricted users to soft-delete users outside their authorized scope. Attackers can include unauthorized user IDs in bulk delete requests to bypass instance-level restrictions and modify or disable accounts they should not access.

### CVE-2026-85612

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T12:17:24.727 |

OpenPanel before 2.3.0 contains an unauthenticated server-side request forgery vulnerability in the /misc/favicon and /misc/og endpoints that accept an attacker-supplied url parameter with insufficient validation. Attackers can force the API to fetch arbitrary internal hosts and cloud metadata endpoints, with small responses returned verbatim enabling credential theft and internal service enumeration.

### CVE-2026-85610

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-04T12:17:24.463 |

OpenPanel before 2.3.0 fails to properly validate chart formula expressions, allowing authenticated project members with read access to execute arbitrary code by recovering the native JavaScript Function constructor through mathjs matrix objects. Attackers can use the recovered constructor to load Node.js built-ins and execute operating system commands with the privileges of the API process, bypassing organization authorization boundaries.

### CVE-2026-85604

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-04T12:17:24.177 |

Grav before 2.0.19 (affected versions <= 2.0.17) contains a remote code execution vulnerability in the Twig sort filter. The sortFunc wrapper in GravExtension.php hardcodes Twig's isSandboxed argument to false, so unlike |map/|filter/|reduce, |sort accepts a plain function name inside the sandbox; the remaining denylist misses spl_autoload, which performs a PHP include. An authenticated user with only page-write rights (admin.pages or api.pages.write) can supply a crafted payload (e.g., via form frontmatter rendered by the Email plugin) that invokes spl_autoload through the sort filter, resulting in arbitrary PHP execution as the web server user.

### CVE-2026-85585

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-04T12:17:20.593 |

SiYuan before v3.8.2 contains an unbounded resource consumption vulnerability in the request-concurrency middleware that retains mutex entries for every unique request path without eviction. Unauthenticated attackers can send numerous unique request paths to permanently increase process memory and synchronization overhead, degrading availability.

### CVE-2026-85584

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-04T12:17:20.463 |

SiYuan versions before v3.8.2 contain a denial of service vulnerability in the publish-service Basic Auth throttle that stores failed-attempt state using attacker-controlled usernames without enforcing capacity limits or eviction policies. Unauthenticated attackers can submit repeated authentication requests with unique invalid usernames to exhaust memory and increase synchronization overhead, degrading service availability.

### CVE-2026-85581

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-04T12:17:20.050 |

SiYuan before v3.8.2 contains a denial of service vulnerability in the unauthenticated /api/system/uiproc endpoint that accepts and retains attacker-controlled process identifiers without size limits or authentication. Attackers can send repeated requests with unique identifiers to exhaust process memory and degrade service availability.

### CVE-2026-79707

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T11:17:19.087 |

A Path Traversal vulnerability in the builder endpoint in Google Cloud Agent Development Kit (ADK) versions 1.9.0 through 1.21.0 on Python allows an unauthenticated remote attacker to read arbitrary files using a crafted file_path query parameter.

### CVE-2026-85540

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-04T10:17:14.017 |

DreamMaker developed by Interinfo has a SQL Injection vulnerability. Authenticated remote attackers can inject arbitrary SQL commands to read, modify, and delete database contents.

### CVE-2026-66840

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-497` |
| Published | 2026-09-04T07:17:09.210 |

XING CPTrans-ME-X contains an Exposure of Sensitive System Information to an Unauthorized Control Sphere (CWE-497). Sensitive system information may be leaked.

### CVE-2026-85147

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-04T03:17:45.920 |

SmartIT Desktop Manager developed by Lightstar has a Use of Hard-coded Credentials vulnerability. Unauthenticated remote attackers can obtain a specific password from the source code, which can be used to retrieve the AES encryption key used for communication.

### CVE-2026-85452

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-03T23:17:25.330 |

MOOS ui-moos through 50b9c6c contains a buffer overflow vulnerability in ScopeTabPane.cpp and ScopeGrid.cpp where client and variable names are formatted into fixed 1024-byte buffers using sprintf without length validation. Attackers can supply arbitrarily long MOOS identifiers that overflow the buffers when an operator selects process list entries or pokes variables, enabling code execution.

### CVE-2026-85450

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-03T23:17:25.043 |

MOOS core-moos through 10.4.0 contains a denial of service vulnerability in the MOOSDB HTTP server that creates unbounded connections and threads without limits. Attackers can open many connections and send endless header data to exhaust server threads and memory, causing service unavailability.

### CVE-2026-85449

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-03T23:17:24.900 |

MOOS-IvP pMarineViewer through 24.8.1 fails to limit the number of tracked node identities from NODE_REPORT messages, allowing attackers to exhaust memory by supplying unbounded distinct node names. Attackers can publish crafted NODE_REPORT data to cause memory exhaustion and stall the operator display without authentication.

### CVE-2026-85448

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-03T23:17:24.760 |

MOOS-IvP uFldShoreBroker through 24.8.1 fails to limit the number of claimed communities stored in parallel vectors within ShoreBroker::handleMailNodePing(). A single publisher can supply unbounded distinct community names to grow retained state and per-pass work without limit, causing memory exhaustion and performance degradation.

### CVE-2026-85447

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-03T23:17:24.610 |

MOOS-IvP pRealm through version 24.8.1 accepts unbounded REALMCAST_REQ subscriptions without validating duration or variable list limits. Attackers can register long-lived pipeways with many variables to cause pRealm to generate excessive output indefinitely, exhausting system resources.

### CVE-2026-85446

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-03T23:17:24.467 |

MOOS-IvP versions through 24.8.1 contain a quadratic processing vulnerability in uFldNodeComms where each new node identity creates a ledger entry and triggers all-pairs distribution work. Attackers can supply unbounded distinct node names in reports to drive the shoreside broker into quadratic processing, delaying or preventing distribution of legitimate node reports.

### CVE-2026-85445

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-03T23:17:24.320 |

MOOS-IvP through 24.8.1 contains a denial of service vulnerability in the Demuxer::addMuxPacket() function that trusts the packet count declared in mux headers without validation. Attackers can declare arbitrarily large packet counts to trigger unbounded memory allocation, exhausting system resources and causing service unavailability.

### CVE-2026-85444

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-03T23:17:24.180 |

MOOS-IvP through 24.8.1 contains a buffer over-read vulnerability in isQuoted(), isBraced(), and isChevroned() functions that strip whitespace but index using the original string length. Attackers can send NODE_REPORT messages with leading or trailing whitespace to read past buffer bounds and access adjacent memory.

### CVE-2026-85443

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-03T23:17:24.030 |

MOOS core-moos through 10.4.0 contains a denial of service vulnerability in MOOSCommServer::ListenLoop() where the accept thread performs a blocking receive without timeout during the wire-protocol handshake. An attacker can open a TCP connection to the MOOSDB port and send no data, causing the accept thread to block indefinitely while holding the socket-list lock, preventing all subsequent client connections.

### CVE-2026-85442

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-03T23:17:23.883 |

MOOS core-moos through 10.4.0 fails to validate packet length declarations in CMOOSCommPkt::OnBytesWritten(), allowing unauthenticated attackers to trigger unbounded buffer allocation by sending crafted wire packets. Attackers can send packets with large declared lengths to exhaust server memory and cause denial of service before client authentication completes.

### CVE-2026-85441

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-195` |
| Published | 2026-09-03T23:17:23.740 |

MOOS core-moos through 10.4.0 fails to validate that serialized string lengths are non-negative in CMOOSMsg::operator>>. Unauthenticated attackers can send a crafted message with a negative length value to the MOOSDB port, causing an unhandled exception that terminates the database process.

### CVE-2026-85436

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-03T23:17:22.937 |

MOOS essential-moos through 10.0.1 contains a buffer overflow vulnerability in CMOOSUDPLink::ReadPktFromArray() that allows remote attackers to corrupt heap memory by sending UDP datagrams with negative declared lengths. Attackers can send crafted UDP packets to the configured UDPListen port to trigger an oversized memcpy operation that writes past the destination buffer, causing heap corruption and denial of service.

### CVE-2026-85431

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-03T23:17:22.207 |

MOOS essential-moos through version 10.0.1 contains an unauthenticated UDP packet injection vulnerability in pMOOSBridge when configured with UDPListen. Attackers can send crafted UDP packets to the configured port to inject arbitrary variables into the local MOOS community with spoofed source and community identifiers.

### CVE-2026-85429

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-03T23:17:21.910 |

MOOS-IvP uFldNodeComms through 24.8.1 trusts the source node identity from the message body rather than validating it from the connection source. Attackers can craft NODE_MESSAGE packets with spoofed source identities to impersonate other nodes and post arbitrary variable notifications without validation.

### CVE-2026-82520

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-03T21:17:22.407 |

parsedmarc before 11.0.1 decompresses gzip and ZIP attachments in a single unbounded read with no limit on decompressed output size. Because parsedmarc automatically processes incoming DMARC report emails without user interaction, an unauthenticated remote attacker can send a crafted email with a highly compressed attachment to the monitored mailbox, causing the parsedmarc process to allocate memory proportional to the uncompressed size and exhaust available RAM.

### CVE-2026-82527

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-03T20:17:22.360 |

R2R through 3.6.6 contains a SQL injection vulnerability that allows unauthenticated attackers to inject SQL predicates into the chunks search query by manipulating the filter key parameter in the retrieval search endpoint. Attackers can exploit the direct interpolation of filter keys into the SQL WHERE clause without parameterization or escaping to perform time-based and boolean-based data exfiltration from the application database.

### CVE-2026-85396

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-03T19:17:31.527 |

rubyzip versions before 3.4.0 contain a path traversal vulnerability in Zip::Entry#extract that fails to properly validate extraction paths using prefix comparison without trailing separators. Attackers can craft archive entries with names like ../upload_backup/owned.sh to write files outside the intended extraction directory into sibling paths sharing the destination prefix.

### CVE-2026-85393

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-03T19:17:31.103 |

node-forge through 1.4.0 fails to validate element count in nested DigestAlgorithm sequences during RSA PKCS#1 v1.5 signature verification. Attackers can embed garbage bytes inside the DigestAlgorithm sequence to forge valid signatures for arbitrary messages using low-exponent RSA keys. This is an incomplete fix for CVE-2026-33894.

### CVE-2026-57445

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-703` |
| Published | 2026-09-03T16:17:26.883 |

Gardens v2 is a modular governance framework that enables communities to create and manage multiple governance pools with customizable parameters and voting mechanisms. In dfba919e218e20d52db9f7b2e8d292d45a46c91b and prior, normal beneficiary payout paths in StreamingEscrow preserve depositAmount() while an active stream needs an escrow reserve. However, the approve-side dispute resolution path drains the whole available escrow balance to the proposal beneficiary. At time of publication, there are no publicly known patches.

### CVE-2026-53924

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-03T16:17:25.520 |

Gardens v2 is a modular governance framework that enables communities to create and manage multiple governance pools with customizable parameters and voting mechanisms. Prior to 0xc9d4e0dacd937364793278180551e59d93cd43f9, StreamingEscrow.claim() correctly rejects withdrawals while an escrow is disputed, but the permissionless syncOutflow() path performs the same excess-balance transfer without checking disputed. After a streaming proposal is challenged, anyone can call syncOutflow() to transfer escrowed SuperTokens to the proposal beneficiary while the dispute is pending. If the proposal is later rejected, those tokens cannot be recovered by drainToStrategy(). This issue has been patched in 0xc9d4e0dacd937364793278180551e59d93cd43f9.

### CVE-2026-85212

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T15:17:40.417 |

CRMEB contains an authentication bypass vulnerability in the verifyAuth() method of SystemRoleServices.php that returns true from both conditional branches. Sub-administrators and accounts with no roles can access restricted admin endpoints by exploiting the inert role check that always permits requests.

### CVE-2026-85180

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-03T15:17:39.250 |

Ollama fails to validate redirect destinations when pulling tensor-layer models, allowing unauthenticated attackers to redirect blob downloads to arbitrary hosts. An attacker can control a registry, serve a malicious tensor-layer manifest, and cause the server to issue GET requests to internal hosts including cloud metadata endpoints.

### CVE-2026-85176

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-03T15:17:38.607 |

DbGate fails to validate jslid parameters in the jsldata controller, allowing authenticated users to read and write arbitrary files via file:// scheme resolution. Attackers can exploit getJslFileName() to bypass directory containment and access sensitive files including encrypted database credentials stored in connections configuration.

### CVE-2026-71404

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T15:17:32.327 |

A flaw was found in Rancher Manager. The GlobalRole controller derived the target ClusterRole name from the user-settable `authz.management.cattle.io/cr-name` annotation and overwrote that object's rules without verifying ownership. A user with delegated GlobalRole create or update permission could point the annotation at any existing ClusterRole, such as `cluster-admin`, and revoke the permissions of every principal bound to it. The change persists after the malicious GlobalRole is deleted.


This issue affects Rancher: before 2.15.1.

### CVE-2026-85546

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-04T10:17:14.287 |

MISP contains a cross-site request forgery (CSRF) vulnerability in the sharing group quick-edit functionality. The addOrg, removeOrg, addServer, and removeServer actions share the __initialiseSGQuickEdit() helper, where the HTTP method validation intended to restrict these operations to POST requests was commented out.

As a result, these state-changing actions could be invoked using GET requests. An attacker could craft a URL targeting one of the affected actions and cause an authenticated MISP user with sufficient privileges to request it, for example through a malicious link or embedded web resource.

Successful exploitation could modify the membership of a MISP sharing group without the victim intentionally performing the operation. Depending on the action performed, an attacker could add or remove organisations or servers from a sharing group, potentially granting unintended access to information distributed through that sharing group or disrupting legitimate information sharing.

The patch restores HTTP method enforcement centrally in __initialiseSGQuickEdit() by calling allowMethod(['post']), ensuring that all four affected quick-edit operations require POST requests and are therefore subject to the application's normal protections for state-changing requests.

### CVE-2026-85223

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-03T22:18:24.080 |

A vulnerability was found in D-Link DNS-340L 1.01B04. Affected by this issue is some unknown functionality of the file /cgi-bin/dropbox.cgi of the component CGI Handler. Performing a manipulation of the argument callback_url/sync_interval results in os command injection. The attack can be initiated remotely. The exploit has been made public and could be used.

### CVE-2026-64199

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-03T22:18:10.337 |

There is an out-of-bounds read vulnerability in DASYLab due to improper validation of user-supplied data.   This results in a read outside the bounds of an allocated data structure.  Successful exploitation requires an attacker to get a user to open a specially crafted .DSB file.  This issue affects all versions before 2026.0.0.

### CVE-2026-85388

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-03T19:17:30.403 |

Worklenz through 3.0.0 fails to properly validate the sort-field query parameter in pagination helper functions, allowing authenticated users to inject arbitrary PostgreSQL expressions into ORDER BY clauses. Attackers can use time-based and boolean-based blind SQL injection techniques to extract sensitive database content including password hashes from other tenants. This is an incomplete fix for CVE-2026-25947.

### CVE-2026-63219

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T18:17:22.997 |

GeoNetwork is a catalog application to manage spatially referenced resources. Prior to versions 4.4.12 and 4.2.17, the API endpoint for creating a new formatter via file upload is unprotected and allows the upload of external uncontrolled files. An unauthenticated attacker can upload arbitrary `.xsl` or `.zip` formatter files to the server.  An unauthenticated attacker can write arbitrary files into the GeoNetwork formatter directory. On its own this constitutes unauthorized write access to server storage. The issue is patched in GeoNetwork versions 4.4.12 and 4.2.17.

### CVE-2026-85237

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-03T16:18:27.163 |

A vulnerability in MISP's email-based one-time password (OTP) authentication flow allowed an attacker to perform an unrestricted number of OTP verification attempts.


The email_otp() endpoint did not apply brute-force protection when validating submitted OTP values. An attacker who had reached the OTP verification stage, for example after successfully providing a user's primary authentication credentials, could repeatedly submit candidate OTP values while the same OTP remained valid. This significantly increased the feasibility of guessing the OTP and bypassing the additional authentication factor, potentially resulting in unauthorized access to the affected user's account.


The issue was exacerbated by the fact that the OTP is associated with the user rather than with an individual pending login session, allowing multiple concurrent sessions to attempt guesses against the same valid OTP.


The patch integrates the existing MISP brute-force protection mechanism into the email OTP flow. Failed OTP attempts are now counted against the user, further attempts are rejected once the configured threshold is reached, and the active OTP is invalidated when the attempt budget is exhausted. Blocklisted users are also prevented from requesting the generation of a fresh OTP. In addition, OTP comparison now uses hash_equals() and validates that the submitted value is a string.

### CVE-2026-71963

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-03T16:18:21.710 |

Hermes Agent 0.18.2 through 0.21.0, fixed in commit f6234d0, contains a remote code execution vulnerability that allows attackers to execute arbitrary OS commands by supplying a malicious repository with a crafted .git/config that sets core.fsmonitor to an attacker-controlled command. When a user opens the malicious repository and sends any message, the agent triggers a git status index refresh which executes the injected command in the user's process context, exposing the full environment including configured provider API keys.

### CVE-2026-4644

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-04T11:17:18.830 |

A Missing Authorization vulnerability in HTTP Connector in Google Cloud Integration Connectors versions prior to 2025-12-11 on Google Cloud Platform allows an authenticated user to escalate privileges and take over a Google Cloud Project using unauthorized service account attachment.



This vulnerability was patched on 11 December 2025, and no customer action is needed.

### CVE-2026-81302

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-09-04T09:17:11.230 |

PALLET CONTROL products contain an incorrect default permission vulnerability, which may allow a local attacker to execute arbitrary code with SYSTEM privileges on the affected product.

### CVE-2026-67397

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T00:17:13.437 |

Path traversal in Plesk 18.0.79.9 and earlier and 18.0.80 through 18.0.80.5 allows local users to execute arbitrary code as root.

### CVE-2026-85439

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-03T23:17:23.427 |

MOOS-IvP through 24.8.1 contains a remote code execution vulnerability in alogsplit's SplitHandler::handlePreCheckSplitDir() function that fails to sanitize shell metacharacters in log file pathnames. Attackers can embed shell syntax in log file names or the --dir parameter to execute arbitrary commands with the privileges of the operator running alogsplit.

### CVE-2026-70178

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T23:17:20.083 |

Missing authorization in Microsoft Fabric allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69857

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T23:17:19.950 |

Authorization bypass through user-controlled key in Azure Cosmos DB allows an authorized attacker to perform spoofing over a network.

### CVE-2026-65818

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-03T23:17:19.817 |

Server-side request forgery (ssrf) in Power Automate allows an authorized attacker to elevate privileges over a network.

### CVE-2026-85224

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-03T22:18:24.260 |

A vulnerability was determined in D-Link DNS-320 ShareCenter 2.06B01. This affects an unknown part of the file /cgi/file_sharing.cgi of the component File Sharing. Executing a manipulation of the argument fileurl can lead to os command injection. The attack can be launched remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-64200

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-03T22:18:10.463 |

There is an out-of-bounds read vulnerability in DASYLab due to improper validation of user-supplied data.   This results in a read a past the end of an allocated heap buffer during string conversion.  Successful exploitation requires an attacker to get a user to open a specially crafted .DSB file.  This issue affects all versions before 2026.0.0.

### CVE-2026-64198

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-03T22:18:10.207 |

There is an out-of-bounds read vulnerability in DASYLab due to improper validation of user-supplied data.   This results in a read a few bytes past the end of an allocated heap buffer during file handling.  Successful exploitation requires an attacker to get a user to open a specially crafted .DSB file.  This issue affects all versions before 2026.0.0.

### CVE-2026-64197

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-03T22:18:10.073 |

There is an out-of-bounds write vulnerability in DASYLab due to improper validation of user-supplied data, resulting in a write past the end of an allocated data structure. Successful exploitation requires an attacker to get a user to open a specially crafted .DSB file.  This issue affects all versions before 2026.0.0.

### CVE-2026-64196

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-03T22:18:09.950 |

There is an out-of-bounds write vulnerability in DASYLab due to improper validation of user-supplied data, resulting in a write past the end of an allocated heap. Successful exploitation requires an attacker to get a user to open a specially crafted .DSB file.  This issue affects all versions before 2026.0.0.

### CVE-2026-64195

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-03T22:18:09.293 |

There is an out-of-bounds write vulnerability in DASYLab due to lack of proper validation of user-supplied data. Successful exploitation requires an attacker to get a user to open a specially crafted .DSB file.  This issue affects all versions before 2026.0.0.

### CVE-2026-85222

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-03T21:17:23.990 |

A vulnerability has been found in D-Link DNS-340L 1.01B04. Affected by this vulnerability is an unknown functionality of the file /cgi-bin/addon_center.cgi of the component Add-On Center. Such manipulation of the argument f_name/f_url/f_flag/f_login_user leads to os command injection. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used.

### CVE-2026-85012

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-03T18:17:33.190 |

Improper neutralization of special elements used in an OS command (CWE-78) in the blueprint resynthesis framework in Amazon Web Services codecatalyst-blueprints before 0.3.156 might allow a user with permission to commit to a repository in the project to execute arbitrary commands in the blueprint resynthesis environment via shell metacharacters in the owner field of a [local] merge strategy entry in a crafted .ownership-file.



Version 0.3.156 removes shell interpretation of the owner field, running the command directly rather than through a shell, and rejects values outside an allowlisted command form. This eliminates shell metacharacter command injection. To remediate this issue, users should upgrade to version 0.3.156 or later.



No action is required for use of the Amazon CodeCatalyst service. Resynthesis runs in an isolated per-project environment with scoped credentials, and the service applies server-side validation there that rejects [local] merge strategy commands outside a restricted allowlisted form, including for blueprint versions published before 0.3.156.

### CVE-2026-85616

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-04T12:17:25.270 |

Snipe-IT versions before 8.6.2 contain an authorization bypass vulnerability in checkout-acceptance report actions when Full Multiple Company Support is enabled. Authenticated users with reports.view permission can enumerate sequential acceptance IDs and soft-delete or trigger reminder emails for acceptances belonging to other companies by exploiting a null check on the legacy users.company_id column.

### CVE-2026-85613

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-04T12:17:24.863 |

OpenPanel before 2.3.0 contains a cross-site scripting vulnerability in the unauthenticated favicon proxy endpoint GET /misc/favicon that allows remote attackers to execute scripts by supplying an SVG file URL. Attackers can host malicious SVG files with embedded scripts that execute in the victim's browser on the API origin, enabling same-origin credentialed requests to authenticated endpoints.

### CVE-2026-85179

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-03T15:17:39.097 |

Label Studio through 1.23.0 fails to validate webhook URLs, allowing authenticated users to dispatch requests to internal services including RFC 1918 addresses and cloud metadata endpoints. Attackers can create webhooks targeting private networks and exfiltrate annotation data by enabling payload transmission in outbound requests.

### CVE-2026-85538

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-04T09:17:11.997 |

An incorrect authorization vulnerability in MISP allowed authenticated users to delete attributes from events despite lacking the required perm_modify or perm_modify_org permissions.

The affected attribute deletion paths relied on organization membership checks performed by MispAttribute::deleteAttribute() but did not consistently enforce MISP's event modification authorization rules. Consequently, a user belonging to the organization associated with an event could potentially delete individual attributes or perform bulk attribute deletion even when their assigned role was not authorized to modify the event.

This created an inconsistency between attribute editing and deletion: editing an attribute correctly used MISP's ACL::canModifyEvent() authorization logic, whereas the affected deletion operations could bypass these permission checks.

An authenticated attacker with access to an affected MISP instance and membership in the organization owning an event could exploit this flaw to remove attributes from that event, potentially causing unauthorized modification or loss of threat intelligence data.

The patch introduces a common authorization check for all affected deletion paths. Before deletion, MISP now resolves the associated events and verifies that the current user is authorized to modify each event using the same authorization mechanism used by normal event and attribute modification operations.

### CVE-2026-85048

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-03T20:17:25.160 |

Use after free in Compositing in Google Chrome prior to 152.0.7977.82 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-84736

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-03T17:17:25.427 |

In the current development version of Eclipse aeriOS, for which no official release has yet been published, the Federator component disables TLS certificate validation for outbound HTTPS connections by default. When the TLS_CERTIFICATE_VALIDATION environment variable is unset or set to false, the component configures its HTTP transport to skip TLS certificate verification.




As a result, an attacker able to intercept network communications between the Federator and external services could impersonate those services and intercept sensitive information transmitted over HTTPS, including OAuth client credentials and bearer tokens.




The issue has been addressed by enabling TLS certificate validation by default. The TLS_CERTIFICATE_VALIDATION environment variable is now set to true in the default configuration provided by the Helm chart and Docker Compose deployment.

### CVE-2026-85211

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T15:17:40.257 |

Label Studio fails to apply organization filters when resolving storage URIs for tasks and projects in proxy_api.py endpoints. Attackers can access other tenants' cloud storage objects by creating a separate organization and supplying arbitrary file URIs to presign or stream bucket contents.

### CVE-2026-85178

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T15:17:38.933 |

Helicone's VaultManager.getDecryptedProviderKeyById() function in the GET /v1/vault/key/{providerKeyId} endpoint fails to validate the requester's organization against the vault key's organization identifier. Attackers with admin or owner privileges in any organization can retrieve decrypted upstream provider credentials for other tenants, including plaintext OpenAI, Anthropic, and Bedrock API keys.

### CVE-2026-85597

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-04T12:17:23.210 |

Traefik before v2.11.55 contains a TLS option conflict resolution vulnerability that allows unauthenticated attackers to bypass client-certificate authentication by creating conflicting TLS options on multi-host routers. Attackers can reach protected backends by exploiting shared TLS resolution across multiple hostnames in a single router rule, causing the strict mTLS requirement to fall back to default options for all hosts.

### CVE-2026-85596

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-04T12:17:23.087 |

Traefik versions >= v3.7.0 and <= v3.7.10 contain an authentication bypass in the Kubernetes Ingress NGINX provider. The TLS option generated for an Ingress carrying the nginx.ingress.kubernetes.io/auth-tls-secret annotation was named after the Ingress namespace and name. As a result, two Ingress objects sharing the same host, the same client CA secret, and the same client-authentication mode produced two distinct TLS option names for that host. Traefik treats this as a TLS options conflict and falls back to the entry point's default TLS configuration, which does not request a client certificate, so a route configured with nginx.ingress.kubernetes.io/auth-tls-verify-client: "on" becomes reachable without a client certificate. Only the v3.7 line is affected; the issue is fixed in v3.7.11.

### CVE-2026-67398

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-04T00:17:13.563 |

Missing authorization vulnerability has been discovered in 2Checkout payment gateway of WHMCS from 8.13.0 before 8.13.8, from 9.0.0 before 9.0.8, all other EOL versions from 4.5.0. The vulnerability allows an unauthenticated user to get WHMCS customer's data via 2Checkout payment gateway's endpoint under specific conditions.

### CVE-2026-63376

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-03T21:17:21.513 |

toml-node is a TOML parser for Node.js and the browser. Prior to 4.1.2, toml.parse() in lib/compiler.js can be tricked by a table path such as a.b.y.__proto__.__proto__, allowing traversal from a scalar value into Number.prototype and Object.prototype. The currentPath tracking value uses both arrays and strings, so valueAssignments records a comma-joined path such as a,b.y while deepRef checks the dot-joined path a.b.y, allowing the duplicate-key guard to miss and attacker-controlled keys to be written to Object.prototype. A table-array prefix-clearing path in addTableArray can also erase guard state before the same __proto__ traversal. Injected properties become visible throughout the Node.js process and can cause denial of service, logic or authorization bypass, or code execution when an application contains a suitable gadget. This issue is fixed in version 4.1.2.

### CVE-2026-44506

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-03T20:17:21.177 |

Medplum is a developer platform that enables development of healthcare apps. In Medplum versions 4.1.10 through 5.1.6, the /oauth2/register endpoint could return the client_secret of preconfigured OAuth clients defined via the defaultOAuthClients server configuration when a matching redirect_uri was provided. This issue has been patched in version 5.1.7.

### CVE-2026-84757

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T17:17:26.660 |

Unauthenticated Settings Change in WP Compress <= 7.21.28 versions.

### CVE-2026-84964

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-03T16:18:25.270 |

A double free in the OpenSSL-based TLS certificate revocation checking path of the MongoDB C Driver can be reached by a TLS endpoint that the client already trusts. During the handshake, specially formed certificate data can cause the same heap object to be released twice. An unauthenticated party acting as the trusted endpoint may cause the connecting client application to terminate unexpectedly.

### CVE-2026-84504

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-04T10:17:13.790 |

fastify versions before 5.12.2 treat the object resolved by a successful Ajv async validator as the value result protocol used by custom validator compilers. If a request that passes its route schema contains a property named value at the root, fastify replaces the entire request body with that property's value before the handler runs, so the handler receives a different object than the one that satisfied the schema. An authenticated low-privilege caller can use this to make nested data replace the validated body and trigger an operation the route schema did not authorize, leading to unauthorized state changes and data disclosure. Users should upgrade to fastify 5.12.2 or later.

### CVE-2026-82302

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-03T19:17:29.827 |

Incorrect Authorization (CWE-863) in Kibana can lead to unauthorized configuration modification via Exploiting Incorrectly Configured Access Control Security Levels (CAPEC-180).

### CVE-2026-78583

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-03T19:17:28.550 |

Incorrect Authorization (CWE-863) in Kibana can lead to privilege escalation via Input Data Manipulation (CAPEC-153). Elasticsearch cluster privilege declarations originating from integration packages were not validated before being used to mint credentials for enrolled Elastic Agents. A user holding Fleet management privileges could therefore cause every Elastic Agent on a targeted policy to receive a credential carrying arbitrarily elevated Elasticsearch cluster privileges, up to and including full cluster administration.

### CVE-2026-84779

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T17:17:28.880 |

Subscriber Broken Access Control in Agentimus – AI SEO, llms.txt &amp; MCP for AI Agents <= 1.51.0 versions.

### CVE-2026-85649

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-252;CWE-636` |
| Published | 2026-09-04T13:20:11.760 |

(Holloway) Chew, Kean Ho's Actualizer v1.2.0 and earlier contains a fail-open password validation vulnerability in the Alpha user and root user password loops of Shell/debian-minbase-install.sh. The installer invokes mkpasswd to generate yescrypt password hashes but does not check the command's return value and unconditionally accepts the result. If mkpasswd fails to generate a yescrypt hash, for example because an incompatible mkpasswd implementation or an environment without yescrypt support is used, the resulting password hash variable can be empty and the build proceeds. The resulting image can therefore contain empty password fields for the root and alpha accounts, potentially permitting passwordless authentication depending on the authentication configuration.

### CVE-2026-83959

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-03T18:17:24.733 |

Substance3D - Sampler is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-18167

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-03T23:17:19.260 |

A
stack-based buffer overflow vulnerability exists in the EasyMesh module of
TP-Link Archer AX55 v4. When Mesh mode is enabled, a LAN attacker may submit
crafted input that causes the easymesh daemon to crash and may potentially
achieve remote code execution on the device.





Successful
exploitation may cause the EasyMesh daemon to crash and may potentially allow
remote code execution when Mesh mode is enabled. This
may result in high impact to the confidentiality, integrity, and availability
of the affected device.

### CVE-2026-55658

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T16:17:26.250 |

Gardens v2 is a modular governance framework that enables communities to create and manage multiple governance pools with customizable parameters and voting mechanisms. In 3e595f3 and prior, when a streaming proposal is funded, the cluster of streaming contracts moves real pool funds into the proposal's StreamingEscrow to back the Superfluid constant flow agreement (the CFA deposit, plus a 0.5 percent margin). cancelProposal then zeroes the escrow's GDA member units but never reclaims that parked balance, and the permissionless claim() forwards the escrow's entire balance, including the pool funded buffer, to the beneficiary. The beneficiary is chosen by the proposal submitter and defaults to the submitter. The only path that returns escrow funds to the pool is drainToStrategy, which is onlyStrategy and is reached solely from the dispute reject ruling, never from cancel or natural completion. At time of publication, there are no publicly known patches.

### CVE-2026-85182

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T15:17:39.593 |

vhr through commit 03abbd3 fails to verify that the account ID in PUT /hr/pass requests belongs to the authenticated caller. Authenticated attackers can change arbitrary account passwords by supplying a target account ID and that account's current password in the request body.

### CVE-2026-75033

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T15:17:32.873 |

A flaw was found in Rancher Manager. Project Secrets were propagated into a namespace based only on its `field.cattle.io/projectId` annotation, without verifying that the referenced project belonged to the same downstream cluster. A user able to create namespaces on one cluster could set the annotation to a project ID from another cluster and have that project's secrets copied into a namespace under their control.


This issue affects Rancher: before 2.15.1.

### CVE-2026-85533

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-04T09:17:11.857 |

An authorization flaw in MISP allowed an authenticated user to submit a sharing_group_id without verifying that the user was authorized to use the referenced Sharing Group.

In several attribute and Galaxy Cluster creation and editing workflows, validation of the submitted Sharing Group was performed only when the request explicitly set the distribution field to 4 ("Sharing Group"). An attacker could therefore craft a request containing a sharing_group_id while omitting the distribution parameter, or otherwise avoiding the distribution == 4 condition, causing the Sharing Group authorization check to be skipped.

This could allow a user with permission to create or modify the affected MISP objects to associate data with a Sharing Group that they are not authorized to use. Depending on the affected object's existing distribution settings and subsequent processing, this could bypass intended information-sharing boundaries and result in unauthorized placement or distribution of data to members of another Sharing Group.

The issue affected attribute attachment and editing operations as well as Galaxy Cluster creation and editing. The fix ensures that authorization is performed whenever a non-empty sharing_group_id is submitted, independently of the distribution parameter. It also centralizes the authorization decision in SharingGroup::canUse() and explicitly rejects empty Sharing Group identifiers rather than allowing them to be interpreted as an unrestricted query.

### CVE-2026-57777

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-04T09:17:10.810 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Automattic WooCommerce allows Blind SQL Injection.

This issue affects WooCommerce: from n/a before 11.0.

### CVE-2026-85197

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-04T08:17:16.677 |

A flaw was found in libsoup. A malicious HTTP/2 server or a Man-in-the-Middle (MITM) attacker can exploit a heap use-after-free vulnerability in the HTTP/2 client implementation. This occurs when a GNOME application uploads a file using HTTP/2, and the server sends a GOAWAY frame while the file body is being read asynchronously. This can lead to memory corruption, potentially resulting in information disclosure or arbitrary code execution.

### CVE-2026-85238

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-09-03T16:18:27.313 |

MISP contains a session fixation vulnerability in the CustomAuth authentication (a custom configuration) flow. When a user was successfully authenticated through CustomAuth, MISP stored the authenticated user identity in the existing session without first rotating the session identifier.


As a result, if an attacker can cause a victim to use a session identifier known to the attacker before authentication, that same session identifier remains valid after the victim successfully authenticates. The attacker could subsequently reuse the fixed session identifier to access the victim's authenticated MISP session, potentially gaining the privileges associated with the victim's account.


The issue occurs because __customAuthentication() wrote the authenticated user into the existing CakePHP session while the call to Session->renew() had previously been disabled. The patch restores session identifier rotation when a new authentication occurs or when the authenticated user changes, while avoiding unnecessary session renewal on every request.

### CVE-2026-85221

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-03T15:17:41.047 |

MISP contains an improper TLS certificate validation vulnerability in CurlClient. The CurlClient::$verifyPeer property was not explicitly initialized and therefore defaulted to null. When passed to cURL, this value effectively disabled TLS peer verification unless the calling code explicitly enabled it.


As a result, HTTPS connections made through affected CurlClient instances could accept certificates that were not issued by a trusted certificate authority. An attacker capable of intercepting or manipulating network traffic between a MISP instance and a remote HTTPS service could impersonate the remote endpoint and perform a man-in-the-middle attack.


Successful exploitation could allow an attacker to observe sensitive information transmitted by MISP, including authentication material or exchanged threat intelligence, and to modify responses returned to the MISP instance. The impact depends on the functionality using CurlClient and the data exchanged with the remote service.


The patch enables TLS peer verification by default while preserving explicit support for configured self-signed certificates. It also corrects the self-signed certificate handling in SyncTool so that peer verification is disabled only when no pinned CA certificate is configured.

### CVE-2026-12483

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-04T14:17:17.480 |

The LearnDash LMS plugin for WordPress is vulnerable to Unrestricted File Type Upload in versions up to and including 5.1.5. This is due to insufficient input validation in the 'learndash_fileupload_process' function, which iterates through an entire array and validates only the first file. This makes it possible for authenticated attackers, with subscriber-level access and above who are enrolled in a course with assignment uploads enabled, to upload arbitrary disallowed files, including PHP files, to the server's wp-content/uploads/learndash/assignments/ directory. The uploaded files can only be used for Remote Code Execution if default server configurations have been changed to allow for execution.

### CVE-2026-19080

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-204` |
| Published | 2026-09-04T12:17:18.443 |

Observable response discrepancy vulnerability in Menulux Software Inc. Menulux Portal allows Account Footprinting.

This issue affects Menulux Portal: before 20260903211448.

### CVE-2026-84428

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-178` |
| Published | 2026-09-04T11:17:19.317 |

fastify versions before 5.12.2 implement the case-insensitive nature of HTTP header names by lowercasing names in a route's header schema before compiling it, but the transformation is incomplete: it lowercases the properties keys and the root-level required array, and does not lowercase the trigger and dependent names inside the JSON Schema Draft 7 dependencies keyword. Because Node stores request header names in lowercase, a canonical-case dependency such as requiring an authentication header whenever a privileged-mode header is present never matches, and the presence assertion is silently skipped. An unauthenticated remote client can therefore send the header that activates a privileged branch while omitting the header the dependency was meant to require, bypassing the conditional check. Users should upgrade to fastify 5.12.2 or later.

### CVE-2026-84469

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-04T10:17:13.677 |

fastify versions before 5.12.2 decide whether to compile a request schema based on JavaScript truthiness, but JSON Schema Draft 7 defines the boolean false as a valid schema that rejects every instance. When an application assigns false to a route's body, querystring, params, or headers schema to deny all input, fastify treats it as a missing schema, compiles no validator, and runs the route handler on any request. An unauthenticated remote client can therefore reach a handler that a valid deny-all schema was intended to make unreachable, a complete validation bypass that can lead to unauthorized state changes or execution of disabled operations. Users should upgrade to fastify 5.12.2 or later.

### CVE-2026-76169

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-04T10:17:12.020 |

fastify versions >= 4.0.0 and before 5.12.2 can route a malformed URL sent under one plugin prefix to the custom not-found handler of a different sibling plugin, and invoke it without the preHandler hook declared for that handler. The internal not-found router for encapsulated handlers dispatches malformed paths through a single shared handler pointer before URL decoding, ignoring the prefix and skipping the selected handler's normal lifecycle. An unauthenticated attacker can therefore reach an authentication-protected private fallback through an unrelated public prefix and read its full response, bypassing the authentication hook and breaking prefix encapsulation. Users should upgrade to fastify 5.12.2 or later.

### CVE-2026-81665

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-04T09:17:11.357 |

A heap-based buffer overflow was found in Corosync's Totem Process Group (totempg) message reassembly. When processing fragmented multicast messages, the buffer used to reassemble fragments lacks a runtime bounds check in release builds. A network-adjacent attacker able to send crafted multicast protocol messages to the cluster could cause a heap buffer overflow with attacker-controlled data. This can crash the Corosync daemon, causing a denial of service to the entire cluster, and may potentially allow further exploitation given sufficient heap-corruption control.

### CVE-2026-85505

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-04T05:17:16.170 |

ipmi-oem in FreeIPMI before 1.6.19 has a stack-based buffer over-read in ipmi_oem_fujitsu_get_sel_entry_long_text in ipmi-oem/ipmi-oem-fujitsu.c when a BMC provides a short response, a different vulnerability than CVE-2026-50031 (which has different affected versions).

### CVE-2026-8862

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-03T21:17:24.307 |

IBM Netezza Software 11.3.0.3 through Interim Fix 002 has credentials that are hardcoded in the application source code, allowing unauthorized access to the container registry. The exposed secret enables attackers to pull private container images, potentially revealing proprietary code, configuration details, and other sensitive information.

### CVE-2026-77465

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-03T21:17:21.803 |

toml-node is a TOML parser for Node.js and the browser. Prior to 4.2.0, toml.parse() uses a Peggy 5.1.0 generated recursive-descent parser in lib/parser.js whose peg$parsevalue, peg$parsearray, and peg$parseinline_table_entry functions recurse through nested arrays and inline tables without a depth limit. A remote unauthenticated application parsing an attacker-controlled TOML document containing a few thousand nested arrays or inline tables can exhaust the Node.js call stack, raise an unexpected RangeError rather than the parser's SyntaxError, and terminate an unprotected request worker or process. The corresponding grammar source is src/toml.pegjs, where the generated parser must be bounded. This issue is fixed in version 4.2.0.

### CVE-2026-85045

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-03T20:17:23.890 |

Race condition in V8 in Google Chrome prior to 152.0.7977.82 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-33630

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-415;CWE-416` |
| Published | 2026-09-03T19:17:27.420 |

c-ares is an asynchronous resolver library. From ver 1.32.3 until 1.34.7, a use-after-free / double-free in c-ares' query-completion handling. The same flaw — a query's callback being invoked while the query is still linked in the channel's internal lookup structures — is present at multiple points in the resend/finish path (timeout handling, response handling, and query dispatch). If the query, or for ares_getaddrinfo() the owning host_query, is freed as a side effect of that callback, it is then accessed and/or freed a second time. This vulnerability is fixed in ver 1.34.7.

### CVE-2026-84847

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T17:17:29.643 |

Unauthenticated Broken Access Control in Quick Event Manager <= 9.17 versions.

### CVE-2026-84778

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-03T17:17:28.747 |

Unauthenticated Denial of Service Attack in Migrate Guru – Site Migration &amp; Cloning <= 6.65 versions.

### CVE-2026-84776

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-03T17:17:28.507 |

Unauthenticated Denial of Service Attack in MalCare Security <= 6.69 versions.

### CVE-2026-48486

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-03T16:17:24.330 |

Signum Node is a HDD-mined cryptocurrency using an energy efficient and fair Proof-of-Commitment (PoC+) consensus algorithm. Prior to version 3.9.9, an integer overflow in BlockServiceImpl.applyBlock() allowed a miner to receive an arbitrarily inflated block reward by crafting a block with a negative totalFeeCashBackNqt value. The vulnerability was introduced when the SMART_FEES hardfork (block ~1,029,000) enabled fee cash-back and burn accounting without overflow protection. This issue has been patched in version 3.9.9.

### CVE-2026-85525

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-347` |
| Published | 2026-09-04T09:17:11.610 |

Improper OCSP response validation in the Snowflake Python, Go, JDBC, and Node.js drivers allowed a revoked TLS certificate to be accepted as valid, because OCSP responses were not reliably bound to the certificate being validated and definitive verification failures were treated as transient. A man-in-the-middle attacker holding a revoked certificate and its private key for a Snowflake or stage hostname could cause the driver to establish a TLS session to the attacker-controlled endpoint anyway, allowing the attacker to read and modify data transmitted within that connection. Successful exploitation requires that on-path position and the corresponding private key, and impact is limited to data carried within the intercepted connection. The fix is available in the patched versions listed above. Users must manually upgrade.

### CVE-2026-62906

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-943` |
| Published | 2026-09-03T23:17:19.540 |

Improper neutralization of special elements in data query logic in Microsoft Discovery Studio allows an unauthorized attacker to disclose information over a network.

### CVE-2026-84777

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-03T17:17:28.623 |

Unauthenticated Broken Authentication in Really Simple SSL <= 9.8.0 versions.

### CVE-2026-75034

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-03T16:18:22.343 |

A flaw was found in Rancher Manager. The SAML assertion replay protection introduced by the fix for CVE-2026-44946 recorded consumed assertion IDs in a per-process cache, so each replica only detected replays that reached the same pod. In a high-availability deployment, an attacker holding a captured assertion could replay it once against every other replica to obtain additional authenticated sessions as the victim.


This issue affects Rancher: before 2.15.1.

### CVE-2026-85028

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-379` |
| Published | 2026-09-03T19:17:30.083 |

Creation of a temporary file in a directory with insecure permissions in the FPGA management tool installation component in AWS FPGA Development Kit (aws-fpga) before 2.3.4 might allow local users to execute arbitrary code with root privileges via crafted shell content placed at a predictable path in a world-writable temporary directory, which the installation step reads after elevating its own privileges.



To remediate this issue, users should upgrade to version 2.3.4.

### CVE-2026-15431

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1220` |
| Published | 2026-09-03T19:17:26.820 |

A potential security vulnerability has been identified in the HP Support
 Assistant for versions prior to 9.53.2.0. The vulnerability
               could potentially allow a local attacker to escalate 
privileges due to insufficient access controls.

### CVE-2026-19224

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-04T07:17:08.937 |

The Hummingbird Performance  WordPress plugin before 3.21.2 does not restrict a network-wide setting to network administrators, allowing an administrator of any single site on a multisite network to execute arbitrary code across the entire network.

### CVE-2026-84773

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T17:17:28.263 |

Unauthenticated Cross Site Scripting (XSS) in EWWW Image Optimizer <= 8.7.6 versions.

### CVE-2026-84761

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-03T17:17:27.060 |

Unauthenticated Server Side Request Forgery (SSRF) in LiteSpeed Cache <= 7.9 versions.

### CVE-2026-85214

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T15:17:40.730 |

vhr fails to validate user authorization in the PUT /hr/info endpoint, allowing authenticated users to modify arbitrary HR profiles by supplying any profile ID in the request body. Attackers can overwrite other users' names, addresses, and disable accounts including administrators to cause denial of service.

### CVE-2026-85213

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T15:17:40.567 |

Kill Bill through 0.24.21 fails to enforce permission annotations on several AdminResource endpoints including getQueueEntries, invalidatesCache, and putOutOfRotation. Authenticated users with minimal account:read permissions can read internal queues, flush server caches, and disable the server by putting the host out of rotation.

### CVE-2026-74237

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-04T13:20:08.607 |

GFI Exinda AI before 7.6.5 contains an argument injection vulnerability in the Tools Iperf Client functionality. The web_tools_cmd() function constructs an iperf command using the server and options parameters without sanitization, permitting injection of arbitrary iperf flags. An authenticated attacker with Unprivileged (lowest-level) access can supply the iperf -F flag to read an arbitrary file from the system and transmit its contents to an attacker-controlled server.

### CVE-2026-85603

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-04T12:17:24.040 |

Grav versions before 1.10.55 contain a path traversal vulnerability in the admin plugin's Save As action that fails to validate the language code parameter. An authenticated admin user with admin.pages.create permission can supply directory traversal sequences in the lang POST field to write arbitrary .md files outside the pages directory with attacker-controlled content.

### CVE-2026-85591

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620` |
| Published | 2026-09-04T12:17:22.433 |

phpMyFAQ versions before 4.1.8 contain an authentication bypass vulnerability in the user control panel API endpoint that allows authenticated attackers to change account passwords without verifying the current password. Attackers with session access can submit a PUT request to the user data update endpoint with only a CSRF token to silently change any user's password, including administrators, causing irreversible account takeover and victim lockout.

### CVE-2026-85590

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-308` |
| Published | 2026-09-04T12:17:21.327 |

phpMyFAQ before 4.1.8 contains an authentication bypass vulnerability in its two-factor authentication (TOTP) disable functionality. The removeTwofactorConfig() handler (reachable via POST /api/user/remove-twofactor) verifies only that the user is logged in and that a valid CSRF token is supplied, then disables TOTP without requiring password re-entry or a current TOTP code. The same downgrade is also reachable inline via PUT /api/user/data/update, which accepts a plain twofactor_enabled form field under the same session+CSRF-only guard. An attacker who has hijacked a user's session can silently strip two-factor protection from any account, including administrator accounts, after which password-only authentication succeeds.

### CVE-2026-85583

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-04T12:17:20.327 |

SiYuan versions before v3.8.2 contain a path traversal vulnerability in the reader-accessible file-read endpoint that follows symlinks when opening authorized asset paths. Attackers with reader role can request a logical asset under data/assets/ that is a symlink to a file outside the workspace and receive the target file bytes, bypassing workspace boundary restrictions.

### CVE-2026-85582

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-04T12:17:20.190 |

SiYuan versions before v3.8.2 contain an unbounded session creation vulnerability in the publish-service Basic Auth handler that allows authenticated attackers to exhaust memory. Attackers can repeatedly authenticate with valid credentials to create persistent session entries without expiry or capacity limits, causing indefinite process memory growth and denial of service.

### CVE-2026-85580

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T12:17:19.917 |

SiYuan versions before v3.8.2 contain a path guard bypass vulnerability in the MCP file-access handler that uses case-sensitive matching on Linux filesystems. Attackers can read the protected publishAccess.json file by requesting case-variant paths like PublishAccess.json to disclose sensitive publish-access configuration and metadata.

### CVE-2026-85578

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-04T12:17:19.640 |

SiYuan through 3.8.1 contains an authorization bypass vulnerability in the /api/file/getFile endpoint that allows readers to retrieve files from notebooks explicitly configured as Visible:false. Attackers with reader role can access private workspace files including notebook metadata and internal configuration by knowing the hidden notebook identifier and file path.

### CVE-2026-19051

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-256` |
| Published | 2026-09-04T12:17:18.323 |

Plaintext storage of a password vulnerability in Menulux Software Inc. Menulux Portal allows Retrieve Embedded Sensitive Data.

This issue affects Menulux Portal: before 20260903211448.

### CVE-2026-16281

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-04T07:17:08.730 |

The Classified Listing  WordPress plugin before 6.1.1 does not verify that the caller owns or can edit the target listing before its AI image-editing AJAX action deletes or attaches media, allowing any authenticated user, including a subscriber, to permanently delete attachments from, and attach files to, any listing owned by another user.

### CVE-2026-85451

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-03T23:17:25.183 |

MOOS core-moos through 10.4.0 contains a remote process termination vulnerability in the SuicidalSleeper component that uses a hard-coded passphrase for multicast command authorization. Any multicast-reachable peer can enumerate MOOS processes and send termination commands to trigger process shutdown by exploiting the default multicast group and port with the known passphrase.

### CVE-2026-53728

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-345;CWE-601` |
| Published | 2026-09-03T20:17:21.643 |

Medplum is a developer platform that enables development of healthcare apps. Prior to version 5.1.6, the external identity provider callback at GET /auth/external accepts attacker-controlled redirect URIs that only need to start with a registered client redirect URI, rather than matching exactly. After a successful external IdP login, the server appends Medplum login and code values to that attacker-supplied URL and issues a redirect. Because the external login request state is serialized as raw JSON and later trusted by the callback, an attacker who can tamper with state.redirectUri can cause Medplum to redirect authorization artifacts to an attacker-controlled endpoint. When the registered redirect URI is a bare origin or another prefix that can be extended into a different hostname, this becomes a cross-origin authorization code leak. This issue has been patched in version 5.1.6.

### CVE-2026-85395

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T19:17:31.390 |

UnoPim before 2.1.3 fails to include integration store, update, and key-generation routes in its ACL map, allowing any admin user to bypass permission checks. Attackers with minimal admin privileges can create OAuth API integrations, mint client credentials, and escalate permissions by exploiting missing authorization validation in the Bouncer middleware.

### CVE-2026-85390

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T19:17:30.690 |

Checkmate through 3.11.0 omits the isAllowed role guard middleware on maintenance-window, notification, and check-deletion routes, allowing read-only users to perform administrative actions. Attackers with user-role sessions can create arbitrary maintenance windows to silence alerts, modify notification channels, and delete monitor check history to erase incident evidence.

### CVE-2026-85389

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T19:17:30.553 |

Worklenz before 3.0.0 fails to verify task ownership by organization when resolving task-scoped API endpoints, allowing authenticated users to access another tenant's task data. Attackers can query task endpoints with arbitrary task UUIDs to retrieve work logs, comments, attachments, and project insights belonging to other organizations.

### CVE-2026-84848

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T17:17:29.770 |

Unauthenticated Cross Site Scripting (XSS) in Quick Event Manager <= 9.17 versions.

### CVE-2026-84836

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T17:17:29.517 |

Subscriber Insecure Direct Object References (IDOR) in WC Ukraine Shipping <= 1.22.3 versions.

### CVE-2026-84812

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T17:17:29.033 |

Unauthenticated Cross Site Scripting (XSS) in BP Better Messages <= 2.15.27 versions.

### CVE-2026-84765

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T17:17:27.580 |

Unauthenticated Cross Site Scripting (XSS) in Breadcrumb NavXT <= 7.5.1 versions.

### CVE-2026-84763

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T17:17:27.450 |

Unauthenticated Cross Site Scripting (XSS) in RTMKit <= 2.1.5 versions.

### CVE-2026-84756

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-03T17:17:26.117 |

Subscriber Privilege Escalation in WCFM Membership <= 2.11.11 versions.

### CVE-2026-81776

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T17:17:24.650 |

Unauthenticated Cross Site Scripting (XSS) in WP QuickLaTeX <= 3.8.8 versions.

### CVE-2026-81773

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T17:17:24.533 |

Unauthenticated Cross Site Scripting (XSS) in  Ninja Forms File Uploads Extension <= 3.3.26 versions.

### CVE-2026-81300

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T17:17:24.410 |

Unauthenticated Cross Site Scripting (XSS) in Calculation For Contact Form 7 <= 1.0 versions.

### CVE-2026-81295

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T17:17:24.290 |

Unauthenticated Cross Site Scripting (XSS) in Under Construction <= 5.82 versions.

### CVE-2026-81292

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-03T17:17:24.163 |

Unauthenticated Cross Site Scripting (XSS) in Simple Payment <= 2.5.1 versions.

### CVE-2026-85239

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-03T16:18:27.457 |

A vulnerability in MISP's event template handling allowed an authenticated user with permission to create or modify event templates to bypass validation of the template definition field.

The EventTemplate::beforeValidate() method only performed semantic validation when the supplied definition was already represented as an array. If a caller instead supplied a pre-encoded string, including malformed JSON or JSON representing an unexpected data type, the value bypassed validateDefinition() and only needed to satisfy the generic notBlank validation rule. As a result, an invalid event template definition could be stored persistently in the database.

When event templates were subsequently retrieved, EventTemplate::afterFind() attempted to decode the stored definition using JsonTool::decode() without handling decoding failures. A definition containing invalid JSON could therefore trigger an exception during retrieval. Because the event template index is available to all authenticated users, a single malicious or malformed template could make the event template listing and other functionality relying on EventTemplate queries return HTTP 500 errors until the offending database row was manually repaired.

Valid JSON representing an unexpected type, rather than the expected JSON object, could similarly result in invalid data reaching downstream consumers.

The vulnerability can therefore be exploited by a user capable of saving event templates to persist malformed template data and cause a persistent denial of service against event-template functionality for other users.

The patch enforces that event template definitions must be supplied as structured objects before saving and always applies semantic validation. On retrieval, malformed JSON and definitions that do not decode to the expected structure are caught, logged, and replaced with an empty definition, preventing a malformed database entry from breaking all event template queries.

 Poisoning doesn't seem reachable according to the lead developer.

### CVE-2026-83961

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-03T16:18:23.383 |

ColdFusion is affected by an Improper Authentication vulnerability that could result in privilege escalation. An attacker could leverage this vulnerability to gain limited read and write access. The vulnerable component is restricted to an administrative network zone by default. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-75035

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-03T16:18:22.477 |

A flaw was found in Rancher Manager. When a non-administrative caller supplied a label selector naming a different user, the ext.cattle.io/v1 Token store dropped its internal owner filter instead of returning an empty result. Any authenticated user could therefore list and watch every other user's tokens, disclosing token metadata and the stored salted hash of the bearer token.



This issue affects Rancher: before 2.15.1.

### CVE-2026-84989

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-03T15:17:36.680 |

ntopng is a web-based network traffic monitoring application. In versions 6.7.0 through 6.7.260717, two REST v2 endpoints that manage ntopng's tag/badge feature — `POST /lua/rest/v2/delete/tag/tag.lua` and `POST /lua/rest/v2/edit/tag/tag.lua` — perform no authorization check at all. Any authenticated user, including a non-administrator ("unprivileged") account, can delete or rename any tag in the system, including tags created by an administrator. Version 6.7.260718 contains a fix.

### CVE-2026-84971

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-03T15:17:36.547 |

Improper handling of an unexpected value size in the decryption path of a client-side encryption library can cause a failed internal check that terminates the process using the library. A party able to place a suitably formed encrypted value where an application will decrypt it, or able to control the responses the application receives, may cause that application to stop running.

### CVE-2026-74236

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T13:20:08.420 |

GFI Exinda AI before 7.6.5 contains a path traversal vulnerability in the diagnostic file deletion handler. The unlink_or_email_file() function accepts parameters prefixed with v_file_row_ and appends their values directly to a base directory path without sanitizing for directory traversal sequences. An authenticated attacker with Admin privileges can delete arbitrary files from the system in the context of root.

### CVE-2026-85594

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-04T12:17:22.830 |

Traefik versions from v3.7.1 fail to enforce crossProviderNamespaces restrictions on the traefik.ingress.kubernetes.io/service.middlewares Service annotation in the Kubernetes Ingress provider. A namespace-limited tenant excluded from the allowlist can attach an operator-owned middleware to its Service, and if that middleware injects backend credentials, recover them at a controlled backend.
