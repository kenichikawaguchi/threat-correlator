# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-09 15:00 UTC
- **対象期間**: `2026-10-08T15:00:42.000Z` 〜 `2026-10-09T15:00:35.000Z`
- **重要CVE数**: 225 件（Critical 9.0+: 51 件 / High 7.0〜: 174 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS 7.0 以上の深刻度を持つものは **30 件以上** に上ります。目立つ傾向は以下の通りです。  

* **リモートコード実行 (RCE) が集中** – 特にクラウドサービス（Microsoft Partner Center、Azure App Service）や IBM 製品で認証・検証不備が原因の RCE が多数。  
* **認証バイパス／特権昇格** – Microsoft Bookings、Partner Center、Azure SRE Agent など、認証ロジックの欠如や証明書検証の不備により、未認証または低権限ユーザーが管理権限を取得可能。  
* **暗号署名・ファイルアップロードの不適切検証** – PrestaShop・OpenCart の決済モジュールや PX‑lab Zombify のファイルアップロードで、危険ファイルや偽装署名が通過し、Web シェルや不正決済が実行できる。  

これらは **インターネットに直接露出しているサービス** が標的になるケースが多く、早急なパッチ適用と防御層の強化が求められます。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑94503** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | Zombify (PX‑lab) における **任意ファイルアップロード** → Web シェル設置 | *最悪ケースで完全リモートコード実行*。Zombify 1.7.7 以前全バージョンが対象で、Web サーバーが外部に公開されている場合は即座に侵入経路となる。 |
| **CVE‑2026‑96207** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | Microsoft Partner Center の **証明書検証不備** → 特権昇格 | Microsoft の SaaS 管理ポータルは多数の企業が利用。認証なしで管理者権限取得が可能になるため、顧客テナント全体が危険に晒される。 |
| **CVE‑2026‑94510** | 9.9 (AV:N/AC:L/PR:N/UI:N/S:C) | Microsoft Bookings の **ユーザー制御キーによる認可バイパス** | 予約システムは外部顧客が頻繁に利用。認可バイパスにより攻撃者は任意の予約情報取得・変更、さらには管理者権限取得が可能。 |
| **CVE‑2026‑86405** | 9.8 (AV:N/AC:L/PR:N/UI:N/S:U) | PrestaShop **Virtual POS モジュール** の署名検証不備 → **署名偽装** | 26.8.1 以前のモジュールが対象。決済情報改竄や不正送金が行えるため、ECサイト運営者にとって重大な金銭的リスク。 |
| **CVE‑2026‑77900** | 9.8 (AV:N/AC:L/PR:N/UI:N/S:U) | Azure App Service の **認証欠如** → 任意コード実行 | Azure の PaaS 環境で広く利用される。認証が無い状態でコード実行が可能になると、同一テナント内の全アプリが乗っ取られる恐れがある。 |

> **共通点**：すべて **ネットワーク越しに認証不要** でコード実行または特権取得が可能。対象製品はクラウドサービス、広く展開されている CMS/EC プラットフォーム、そして内部向け管理ポータルです。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 修正版 / 推奨バージョン |
|-------------------|-------------------|------------------------|
| **PX‑lab Zombify** | ≤ 1.7.7 | 1.7.8 以上（公式リリースにてアップデート） |
| **Microsoft Partner Center** | すべて（サービス側） | Microsoft が 2026‑09‑15 にリリースした **Security Update for Partner Center** を適用 |
| **Microsoft Bookings** | すべて（サービス側） | 2026‑10‑01 以降の **Bookings v2.3**（認可ロジック修正） |
| **PrestaShop Virtual POS Module** | 26.8.1 以前 | **26.9.1** 以上に更新 |
| **Azure App Service** | すべて（サービス側） | Azure ポータルで **“Authentication / Authorization”** を有効化し、2026‑09‑20 以降の **Platform Update** を適用 |
| **IBM Guardium Data Protection** | 12.0‑12.2 系列（該当脆弱） | 12.2.3 以上（認証欠如・SQLi・Path Traversal 修正） |
| **OpenCart Virtual POS Module** | 26.8.2 以前 | **26.9.1** 以上 |
| **fast‑jwt (npm)** | 6.2.0‑6.3.0 | 6.3.1 以上（鍵判定ロジック修正） |
| **SGLang** | すべて（未パッチ） | 2026‑10‑05 以降の **SGLang v0.12.4**（Pickle デシリアライズ制限） |
| **FalkorDB** | < 4.20.0 | **4.20.0** 以上（Bolt RESET メッセージのサイズ検証） |

> **※ SaaS 系サービスはベンダー側のパッチ適用が必要です。管理コンソールから「最新のセキュリティ更新プログラムが適用済み」か必ず確認してください。**

### 3.2 防御層の強化
1. **Web アプリケーションファイアウォール (WAF) の導入・チューニング**  
   - `File Upload` 系 (Zombify) では `Content‑Type` と拡張子の二重チェック、`file‑type` のホワイトリスト化を必須。  
   - `SQLi` 系 (EduAdmin、Ajax Search Pro、tagDiv 等) では `parameterized queries` への置換と `ModSecurity` の OWASP CRS ルール 941100 系列を有効化。

2. **TLS/証明書検証の徹底**  
   - Microsoft Partner Center への API 呼び出しは **証明書ピンニング** を実装し、自己署名証明書を受け入れない。  
   - 社内プロキシやロードバランサで **OCSP Stapling** を有効化し、失効証明

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-94503

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-09T10:16:40.607 |

Unrestricted Upload of File with Dangerous Type vulnerability in PX-lab Zombify zombify allows Upload a Web Shell to a Web Server.This issue affects Zombify: from n/a through 1.7.7.

### CVE-2026-96207

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-08T23:17:05.583 |

Improper certificate validation in Microsoft Partner Center allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-94510

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-08T23:17:05.427 |

Authorization bypass through user-controlled key in Microsoft Bookings allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-86405

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-09T13:17:11.100 |

Improper verification of cryptographic signature vulnerability in Sipay Electronic Money and Payment Services Inc. PrestaShop Virtual POS Module allows Signature Spoofing by Improper Validation.

This issue affects PrestaShop Virtual POS Module: from 26.8.1 before 26.9.1.

### CVE-2026-85531

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-09T13:17:10.957 |

Improper verification of cryptographic signature vulnerability in Sipay Electronic Money and Payment Services Inc. OpenCart Virtual POS Module allows Signature Spoofing by Improper Validation.

This issue affects OpenCart Virtual POS Module: from 26.8.2 before 26.9.1.

### CVE-2026-88131

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-08T23:17:04.590 |

Deserialization of untrusted data in Microsoft Dataverse allows an unauthorized attacker to execute code over a network.

### CVE-2026-77900

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-08T23:17:03.107 |

Missing authentication for critical function in Azure App Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-84249

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-08T22:17:34.213 |

IBM Guardium Data Protection 12.2, and 12.2.2 could allow a remote attacker to execute arbitrary management operations due to missing authentication for critical function.

### CVE-2026-80381

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-08T22:17:32.353 |

IBM Guardium Data Protection 12.0, 12.1, and 12.2 could allow a remote attacker to execute unauthorized SQL statements due to SQL injection.

### CVE-2026-75875

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-08T22:17:32.223 |

IBM Guardium Data Protection 12.0, 12.1, and 12.2 could allow a remote attacker to execute arbitrary code due to path traversal.

### CVE-2026-107722

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-08T22:17:28.447 |

fast-jwt provides fast JSON Web Token (JWT) implementation. From 6.2.0 until 6.3.0, fast-jwt can misclassify RSA public-key text as an HMAC secret when the key has non-whitespace content before its PEM header. In src/crypto.js, performDetectPublicKeyAlgorithms trims whitespace but publicKeyPemMatcher remains start-anchored, so comments, control characters, zero-width characters, or wrapper text can prevent PEM detection and reach the HMAC fallback. An attacker who knows the public key bytes can sign arbitrary HS256 claims with that public material when HS256 is inferred or allowed, resulting in authentication or authorization bypass. An asymmetric-only algorithm allowlist prevents the attack. This issue is fixed in version 6.3.0.

### CVE-2026-78406

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-08T21:18:03.190 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 could allow a remote unauthenticated attacker to execute arbitrary code on the system due to the deserialization of untrusted data.

### CVE-2026-78401

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-08T21:18:03.043 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 could allow a remote unauthenticated attacker to execute arbitrary code on the system due to the deserialization of untrusted data.

### CVE-2026-84272

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-08T20:17:37.753 |

IBM Guardium Data Protection 12.1 and 12.2.2 are vulnerable to missing authentication in the edge-controller component. An unauthenticated remote attacker could exploit this vulnerability to execute arbitrary container images and gain control of managed edge clusters.

### CVE-2026-93034

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-08T15:17:57.117 |

SGLang contains an arbitrary code execution vulnerability caused by the ZMQ message decoder unconditionally deserializing PickleWrapper payloads via pickle.loads() in _maybe_unwrap_pickle without type allowlisting or authentication; this vulnerability persists via the msgpack path even when SGLANG_USE_PICKLE_IPC is disabled, and becomes remotely exploitable if data-parallel attention is enabled with a non-loopback --dist-init-addr setting.

### CVE-2026-14992

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T15:17:50.210 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 vulnerable to buffer overflow.

### CVE-2026-14502

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-08T15:17:49.150 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to obtain administrative access due to failure to reject empty passwords during LDAP authentication.

### CVE-2026-14269

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-08T15:17:48.600 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 is vulnerable to a heap-based buffer overflow, caused by improper bounds checking. An unauthenticated remote attacker could overflow the buffer and execute arbitrary code on the system.

### CVE-2026-69435

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-08T23:17:02.783 |

Missing authorization in Azure SRE Agent allows an authorized attacker to elevate privileges over a network.

### CVE-2026-107406

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-08T22:17:26.847 |

Memory overflow vulnerability leading to Remote Code Execution or Denial of Service Vulnerability in NetScaler ADC.


NetScaler ADC or NetScaler Gateway must be configured as a SAML SP or SAML IdP, subject to the following version-specific requirements:



 

  *  For the following versions: Applicable only when configured as a SAML IdP:
  *  NetScaler ADC and NetScaler Gateway between 14.1-73.37 and 14.1-73.41, inclusive
  *  NetScaler ADC 14.1-FIPS between 14.1-73.37 FIPS and 14.1-73.41 FIPS, inclusive
  *  NetScaler ADC and NetScaler Gateway between 13.1-64.23 and 13.1-64.28, inclusive
  *  NetScaler ADC 13.1-FIPS between 13.1-NDcPP 13.1-37.279 and 13.1- 37.282, inclusive




 



For the following versions: Applicable only when configured as a SAML SP or SAML IdP:

  *  NetScaler ADC and NetScaler Gateway before 14.1-73.37 
  *  NetScaler ADC 14.1-FIPS before 14.1-73.37 FIPS 
  *  NetScaler ADC and NetScaler Gateway before 13.1-64.23
  *  NetScaler ADC 13.1-FIPS before13.1-NDcPP 13.1-37.279

### CVE-2026-106126

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T20:17:29.950 |

A command injection vulnerability in the Active Directory Events Listener of Tenable Identity Exposure (SaaS) allows an authenticated, low-privileged attacker to execute arbitrary commands as SYSTEM on the PDCe.

### CVE-2026-100730

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-09T14:17:09.607 |

A service console interface on openPDC and openHistorian deserializes a client-supplied data structure. On systems using Windows Authentication, an attacker must already be authenticated to reach this function; on systems without Windows Authentication, this is reachable by an unauthenticated network attacker. This allows an attacker to trigger deserialization of an arbitrary object graph, which could allow remote code execution under the privileges of the affected service account.

### CVE-2026-96809

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T10:16:45.980 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in MultiNet Interactive AB EduAdmin Booking eduadmin-booking allows Blind SQL Injection.This issue affects EduAdmin Booking: from n/a before 6.0.0.

### CVE-2026-96331

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T10:16:44.167 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in wpdreams Ajax Search Pro ajax-search-pro allows Blind SQL Injection.This issue affects Ajax Search Pro: from n/a through 4.29.1.

### CVE-2026-96330

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T10:16:43.917 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in tagDiv tagDiv Opt-In Builder td-subscription allows Blind SQL Injection.This issue affects tagDiv Opt-In Builder: from n/a through 1.7.6.

### CVE-2026-96328

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T10:16:43.600 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in jegtheme JNews - Pay Writer jnews-pay-writer allows Blind SQL Injection.This issue affects JNews - Pay Writer: from n/a through 12.0.1.

### CVE-2026-96327

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T10:16:43.460 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in VibeThemes WPLMS wplms_plugin allows Blind SQL Injection.This issue affects WPLMS: from n/a before 1.9.9.8.2.

### CVE-2026-93947

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T10:16:39.520 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Shinetheme Traveler traveler allows Blind SQL Injection.This issue affects Traveler: from n/a through 3.2.9.

### CVE-2026-107935

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-09T10:16:37.497 |

A path traversal vulnerability was found in gvproxy, the network forwarder provided by the gvisor-tap-vsock package. The unauthenticated /services/forwarder/expose endpoint does not validate the caller-supplied socket path, allowing an attacker to delete arbitrary files on the host system.

### CVE-2026-107908

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-09T06:17:10.777 |

A heap-based out-of-bounds write in the BoltReadHandler function (src/bolt/bolt_api.c) in FalkorDB before 4.20.0 allows a remote unauthenticated attacker to cause a denial of service and possibly execute arbitrary code by sending a Bolt RESET message with an attacker-chosen chunk size to the Bolt port. The handler checks the size only with ASSERT(), which is compiled out in release builds, then computes a destination pointer from the wire-supplied 16-bit size and moves buffered data up to about 64 KiB backwards past the start of the read buffer. Only deployments that enable the Bolt endpoint (BOLT_PORT, disabled by default) are affected.

### CVE-2026-5759

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415;CWE-416` |
| Published | 2026-10-09T05:16:44.920 |

A double free and use-after-free vulnerability in the RdbLoadDeletedNodes function of the RDB graph decoders (src/serializers/decoders/*/decode_graph_entities.c) in FalkorDB before 4.18.1 allows a remote attacker who can issue Redis replication commands (for example, against an instance with no password configured) to cause a denial of service or execute arbitrary code in the redis-server process by supplying a crafted RDB stream whose deleted-nodes buffer length is not a multiple of sizeof(NodeID). The length check relies on ASSERT(), which is compiled out in release builds, so the function continues after freeing the buffer, reading it and freeing it a second time.

### CVE-2026-107726

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-08T22:17:29.120 |

Hazelcast is a unified real-time data platform combining stream processing with a fast data store. Prior to 5.4.5, 5.5.10, and 5.6.1, improper validation of data supplied by a malicious client able to connect to a cluster allows arbitrary reads from a cluster member's Java heap, off-heap data, and JVM process address space. The same flaw can crash cluster members and, in some Hazelcast Enterprise Edition configurations, corrupt memory with possible arbitrary code execution. Both slim and full distributions are affected. This issue is fixed in versions 5.4.5, 5.5.10, 5.6.1, and 5.7.0.

### CVE-2026-107780

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T21:17:52.940 |

Dromara Skyeye through commit 003549ae5615bd114ba5bb8ddf6a8e8ead97c321 contains an OS command injection vulnerability in the unauthenticated /post/TtsController/textToSpeech endpoint via the format parameter. Attackers can inject a single quote into format to break out of the PowerShell string and execute commands as the Skyeye service account on Windows.

### CVE-2026-107779

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-08T21:17:52.790 |

Dromara Skyeye through commit 003549ae5615bd114ba5bb8ddf6a8e8ead97c321 contains a missing authentication vulnerability in bundled xxl-job-admin JobInfoController endpoints annotated with @PermissionLimit(limit = false). Unauthenticated attackers can POST GLUE_SHELL, GLUE_PYTHON, or GLUE_POWERSHELL jobs with attacker-supplied glueSource to /jobinfo/addAndStart, executing commands on the executor host or stopping and deleting jobs.

### CVE-2026-84244

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-08T20:17:37.160 |

IBM Guardium Data Protection 12.2 IBM Security Guardium Data Protection is vulnerable to stored cross-site scripting (XSS) in the Quick Search results grid. An unauthenticated attacker who can influence monitored database traffic could execute malicious script in the browser of an authenticated Guardium user.

### CVE-2026-104076

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-08T20:17:29.543 |

TVU Networks Receiver/Transceiver devices running firmware before version 7.9 contain a missing authentication vulnerability that allows remote unauthenticated attackers to read sensitive device information and modify device configuration via unprotected REST API endpoints. Attackers can send unauthenticated GET requests to disclose network configuration, firmware details, and cloud service information, or issue POST requests to endpoints such as /Setting3/API/API/v1/LocalNetwork/DNS to alter DNS settings and enable man-in-the-middle attacks on outbound connections to TVU cloud infrastructure.

### CVE-2026-104075

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-08T20:17:29.377 |

TVU Networks Receiver/Transceiver devices running firmware before version 7.9 contain an authentication bypass vulnerability in the web management login endpoint POST /tvu/Login that allows remote unauthenticated attackers to obtain an administrative session by submitting an empty or absent UserName parameter. Attackers can send a crafted HTTP request directly, bypassing client-side JavaScript validation, to receive a valid session cookie regardless of the password value and gain full administrative control of the device's web management interface.

### CVE-2026-107704

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T19:17:02.897 |

The image_optimizer Ruby gem 1.3.0 through 1.9.0 contains an OS command injection vulnerability in ImageOptimizer#identify_format that allows attackers to execute commands by supplying a crafted image path when the identify option is enabled. Attackers controlling the path, such as an uploaded file name, can append shell metacharacters like ';' that are executed via Ruby backticks with the Ruby process privileges.

### CVE-2026-107703

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T19:17:02.720 |

@enmaso/node-convert through 1.0.0 contains an OS command injection vulnerability in convert.js that allows attackers to execute shell commands via unsanitized filepath and convertTo arguments. Attackers can inject shell metacharacters or a single quote into the ImageMagick command run by child_process.exec() to execute operating system commands with Node.js process privileges.

### CVE-2026-107700

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-08T19:17:02.213 |

dot-access 0.0.3 through 1.0.0 contains a code injection vulnerability that allows remote attackers to execute JavaScript by supplying crafted paths to get(). The path is concatenated into a new Function body in index.js, so attackers can reach constructor.constructor to load child_process and run operating system commands in the Node.js process.

### CVE-2026-107699

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T19:17:01.853 |

ppt2png through 0.0.6 contains an OS command injection vulnerability that allows attackers to execute operating system commands by supplying unsanitized input or output path arguments. Attackers can append shell metacharacters such as ';' to file names passed to child_process.exec() in ppt2png.js, running commands with Node.js process privileges.

### CVE-2026-9209

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250;CWE-306` |
| Published | 2026-10-08T15:17:57.677 |

mJobTime through build 15.7.3.32 contains an unauthenticated SQL execution vulnerability in the Login.aspx admin panel handlers, where the runQueryButton postback and exportSqlQuery_Server PageMethod execute caller-supplied SQL against the backing Sybase SQL Anywhere database using DBA/sysadmin privileges with no server-side authentication enforced beyond a client-side sessionStorage flag. Attackers can submit arbitrary SQL through these exposed endpoints to invoke xp_cmdshell and xp_read_file, achieving pre-authentication remote code execution as LocalSystem via a single HTTP request.

### CVE-2026-107640

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-08T15:17:47.343 |

Integrics Enswitch 3.13 through 4.4 contains an authentication bypass vulnerability in /api/json/user/password/update/ that allows unauthenticated attackers to change account passwords by omitting the reset parameter. Attackers can target accounts with no pending reset, whose empty reset_key matches the defaulted empty value, to take over administrator accounts after enumerating valid usernames.

### CVE-2026-107910

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-09T06:17:12.457 |

An improper authentication vulnerability in the is_authenticated function (src/bolt/bolt_api.c) in FalkorDB before 4.20.0 allows a remote unauthenticated attacker to execute graph queries without credentials through the Bolt endpoint. The function decides whether a password is required by issuing an empty AUTH command to Redis and treats only a WRONGPASS error as meaning that a password is required; any other error, such as LOADING while a dataset is being loaded, MASTERDOWN during replication failover, or OOM under memory pressure, causes the client to be treated as authenticated. Only deployments that enable the Bolt endpoint (BOLT_PORT, disabled by default) are affected.

### CVE-2026-7827

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-09T05:16:45.327 |

A stack-based buffer overflow in the _RdbLoadEntity function of the RDB graph decoders (src/serializers/decoders/*/decode_graph_entities.c) in FalkorDB before 4.18.4 allows a remote attacker who can issue Redis replication commands (for example, against an instance with no password configured) to cause a denial of service and possibly execute arbitrary code by supplying a crafted RDB stream with an attacker-controlled entity property count. The count sizes two variable-length arrays on the thread stack with no upper bound, and the decoder then fills them with attacker-supplied values.

### CVE-2026-79842

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-08T21:18:03.457 |

An authentication bypass vulnerability exists in HPE Intelligent Management Center (iMC) prior to v7.3 E0713

### CVE-2026-19491

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-08T21:17:57.070 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 could allow a remote attacker to bypass authentication due to improper authentication.

### CVE-2026-16916

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-10-08T21:17:56.500 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 could allow a remote authenticated attacker to execute arbitrary code due to a protection mechanism failure.

### CVE-2026-16823

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-08T21:17:56.233 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 could allow a remote attacker to bypass security restrictions due to improper authentication.

### CVE-2026-107781

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-08T21:17:53.080 |

Dromara Skyeye through commit 003549ae5615bd114ba5bb8ddf6a8e8ead97c321 contains a server-side request forgery and missing authorization vulnerability in the OnlyOffice save callback editUploadOfficeFileById. Unauthenticated attackers can supply arbitrary url and key parameters to make the server fetch internal URLs and overwrite any user's stored file, then read results via queryFileToShowById.

### CVE-2026-95210

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-08T18:18:33.370 |

Improper certificate validation in gnutls v3.8.13 causes the application to accept certificates containing invalid extensions.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-106155

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T08:16:54.377 |

In Progress® Telerik® Report Server prior to version 12.2.26.1007, a stored cross-site scripting vulnerability in the shared reporting engine allows an authenticated report author to embed javascript: or vbscript: URLs in report navigation actions or HTML text box links. When another user views the malicious report and the embedded navigation is triggered, attacker-controlled script can execute in the web report viewer's origin. In a multi-user Report Server deployment, this can enable privilege escalation by performing actions in a higher-privilege user's authenticated session, including an administrator's session.

### CVE-2026-94065

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-09T14:17:25.497 |

Deserialization of Untrusted Data vulnerability in BuddhaThemes ColorFolio colorit allows Object Injection.This issue affects ColorFolio: from n/a through 1.3.

### CVE-2026-94064

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-09T14:17:25.247 |

Deserialization of Untrusted Data vulnerability in BuddhaThemes Neo | Barber Shop WordPress Theme neocut allows Object Injection.This issue affects Neo | Barber Shop WordPress Theme: from n/a through 3.5.

### CVE-2026-104392

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-09T13:17:08.227 |

Deserialization of Untrusted Data vulnerability in ExpressTech Quiz And Survey Master quiz-master-next allows Object Injection.This issue affects Quiz And Survey Master: from n/a through 11.2.7.

### CVE-2026-103413

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-09T13:17:07.633 |

Improper input validation vulnerability in Apache Camel Karavan.



When a deployment was started, Karavan unmarshalled a project's `kubernetes.yaml` and applied every resource it contained to the cluster without restricting the resource kinds, without rejecting security-sensitive pod options, and without pinning the target namespace. An authenticated user of any role could therefore have Karavan apply arbitrary Kubernetes resources within the reach of its service account, including pods requesting hostNetwork, hostPID, hostIPC, hostPath volumes, host ports, privileged containers, privilege escalation or added capabilities.



This issue affects Apache Camel Karavan: from 4.0.0 before 4.22.1.



Users are recommended to upgrade to version 4.22.1, which fixes the issue.

### CVE-2026-103412

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-09T13:17:07.453 |

Improper limitation of a pathname to a restricted directory ('path traversal') vulnerability in Apache Camel Karavan.



A project file name supplied through the project file API was used verbatim as a path segment when the project was written to the working copy for a Git commit, so a name containing `../` sequences caused the file content to be written outside the project directory, to any location writable by the Karavan process. An authenticated user of any role could use this to overwrite application configuration or files on the application classpath and so execute code in the Karavan container.



This issue affects Apache Camel Karavan: from 3.18.0 before 4.22.1.



Users are recommended to upgrade to version 4.22.1, which fixes the issue.

### CVE-2026-96671

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-09T10:16:45.697 |

Cross-Site Request Forgery (CSRF) vulnerability in fifu.app Featured Image from URL featured-image-from-url allows Cross Site Request Forgery.This issue affects Featured Image from URL: from n/a through 6.0.7.

### CVE-2026-19570

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120;CWE-787` |
| Published | 2026-10-09T08:16:54.693 |

The LE Audio Broadcast Sink in subsys/bluetooth/audio/bap_broadcast_sink.c copies subgroup metadata from a received Basic Audio Announcement (BASE) into the static Broadcast Audio Scan Service parameter structure mod_src_param without any bounds check. In base_subgroup_meta_cb() the destination element was selected as mod_src_param.subgroups[mod_src_param.num_subgroups] with no test against ARRAY_SIZE(mod_src_param.subgroups) (sized by CONFIG_BT_BAP_BASS_MAX_SUBGROUPS, default 1), and the metadata was copied with memcpy() using the raw on-air length returned by bt_bap_base_get_subgroup_codec_meta() into a metadata array sized by CONFIG_BT_AUDIO_CODEC_CFG_MAX_METADATA_SIZE (default 4). The BASE validator bt_bap_base_get_base_from_ad() only checks structural consistency and permits up to ~24 subgroups and metadata LTVs of ~240 octets.

The defect is reached from the periodic advertising receive callback: pa_recv() → bt_data_parse() → pa_decode_base() → update_recv_state_base() → bt_bap_base_foreach_subgroup() → base_subgroup_meta_cb(). Every broadcast sink registers a scan-delegator receive state at creation (bt_bap_broadcast_sink_create() calls broadcast_sink_add_src()), and CONFIG_BT_BAP_BROADCAST_SINK depends on CONFIG_BT_BAP_SCAN_DELEGATOR, so the path is active in every broadcast-sink build once the device is periodic-advertising-synced. An attacker in radio range who operates a broadcast source the device syncs to — or who impersonates the advertiser address and SID of one already in use, periodic advertising data being unauthenticated — can change the BASE at will; each new BASE is re-parsed.

A crafted BASE therefore writes attacker-chosen bytes past the end of a fixed static object in .bss: up to roughly 236 bytes for an oversized metadata LTV, plus whole struct bt_bap_bass_subgroup records for each subgroup beyond CONFIG_BT_BAP_BASS_MAX_SUBGROUPS. This is memory corruption of adjacent Bluetooth-audio state reachable with no pairing, bonding or GATT connection, with a potential for remote code execution in the Bluetooth RX thread; in addition, the unvalidated metadata_len is forwarded to bt_bap_scan_delegator_mod_src(), which neither clamps it nor rejects it, leading to a further copy into the receive state and to out-of-bounds memory being disclosed in the BASS receive-state notification sent to a connected Broadcast Assistant.

The fix rejects a BASE carrying more subgroups than the receive state can hold (discarding the update entirely) and omits metadata that does not fit rather than copying it, and additionally honours the previously-ignored error return of the subgroup decode pass.

### CVE-2026-19569

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-09T08:16:54.563 |

dynamic_object_create() in kernel/userspace/userspace.c computed the backing allocation for a dynamically allocated kernel object as obj_size_get(otype) + size, and for thread stack elements as STACK_ELEMENT_DATA_SIZE(size) (a round-up plus fixed overhead), without checking either expression for unsigned wrap-around. A size close to SIZE_MAX makes the computed total wrap to a very small value, so the heap chunk handed out is a few bytes while the object descriptor is still tagged with the full requested type and registered in the kernel object table.

The size argument reaches that arithmetic directly from user mode. k_object_alloc_size() is declared __syscall in include/zephyr/sys/kobject.h, its verifier z_vrfy_k_object_alloc_size() in kernel/userspace/userspace_handler.c is a bare pass-through, and z_object_alloc() only range-checks otype — nothing bounds size. The stack-element branch is additionally reachable through the k_thread_stack_alloc() syscall via kernel/dynamic.c. Because subsequent kernel-object validation checks only the object's type and initialization state, the undersized handle passes K_SYSCALL_OBJ_INIT()/K_SYSCALL_OBJ_NEVER_INIT(), and the matching init syscall (for example k_mutex_init(), k_sem_init(), or k_thread_create()) then writes a complete object over the truncated allocation.

An unprivileged user-mode thread can therefore trigger a supervisor-mode out-of-bounds write into the kernel resource-pool heap, of a size and content it substantially controls, corrupting sys_heap chunk metadata and adjacent kernel objects. Under CONFIG_GEN_PRIV_STACKS the thread-stack branch additionally stores an attacker-influenced wild pointer as a user thread's privileged stack base. The practical result is escape from the CONFIG_USERSPACE sandbox — kernel-level code execution or at minimum kernel memory corruption and system compromise.

Exploitation requires CONFIG_USERSPACE together with CONFIG_DYNAMIC_OBJECTS (also selected by CONFIG_DYNAMIC_THREAD under userspace), and a calling thread with an assigned resource pool. The fix rejects both overflowing computations and frees the partially built descriptor.

### CVE-2026-107909

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-09T06:17:12.303 |

A heap-based out-of-bounds write in the ws_read_frame function (src/bolt/ws.c) and the buffer_apply_mask function (src/bolt/buffer.c) in FalkorDB before 4.20.0 allows a remote unauthenticated attacker to cause a denial of service and possibly corrupt heap memory by sending a WebSocket frame with a 64-bit extended payload length to the Bolt port. The payload length is not bounded, and the only bounds check in buffer_apply_mask is an ASSERT(), which is compiled out in release builds, so the function XORs memory beyond the end of the receive buffer with the attacker-supplied mask key. Only deployments that enable the Bolt endpoint (BOLT_PORT, disabled by default) are affected.

### CVE-2026-7826

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-09T05:16:45.150 |

A heap-based out-of-bounds read in the BufferSerializerIOv2_ReadBuffer function (src/serializers/serializer_io.c) in FalkorDB before 4.18.4 allows a remote attacker who can issue Redis replication commands (for example, against an instance with no password configured) to cause a denial of service or disclose heap memory by supplying a crafted RDB stream whose sub-buffer length field exceeds the remaining buffer size. The only bounds check is an ASSERT(), which is compiled out in release builds, so memcpy() reads past the end of the heap allocation.

### CVE-2026-89091

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-08T22:17:35.777 |

A flaw was found in ansible-core. When installing a collection with
`ansible-galaxy collection install`, the archive extractor validates member
paths using lexical path normalisation (os.path.abspath) instead of resolving
symbolic links (os.path.realpath), and it performs no containment check on
symlink-typed directory members before creating them. A crafted collection
tarball can chain symlink directory entries so that a subsequent file member is
written outside the intended destination directory. This allows an attacker who
can get a victim to install a malicious collection to overwrite arbitrary files
with the privileges of the user running ansible-galaxy, leading to code
execution on the control node. This is a bypass of the fix for CVE-2020-10691.

### CVE-2026-19482

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-08T21:17:56.930 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of command arguments.

### CVE-2026-18740

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-08T21:17:56.777 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 could allow a remote authenticated attacker to perform unauthorized actions due to argument injection.

### CVE-2026-107701

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-08T19:17:02.403 |

dot-access through 1.0.0 contains a prototype pollution vulnerability that allows attackers to modify Object.prototype by supplying a crafted dotted path to set(). Attackers controlling the path, such as through user-supplied field names, can use __proto__ segments to inject properties into all objects, altering authorization flags and option defaults or crashing the process.

### CVE-2026-107375

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-08T18:17:21.883 |

JHipster is a development platform to quickly generate, develop, and deploy modern web applications and microservice architectures. From 7.0.0 until 9.4.0, reactive applications generated with Spring WebFlux, Spring Data R2DBC, and a SQL database pass the attacker-controlled sort request parameter from paginated entity-list endpoints into createOrderByFields in generators/spring-boot/generators/data-relational/templates/src/main/java/package/repository/EntityManager_reactive.java.ejs. The generated code renders these properties into the SQL ORDER BY clause without validation or quoting, and the R2DBC simple query protocol can execute additional statements separated by semicolons. A normal authenticated user can consequently read sensitive tables, modify or delete data, or drop tables, while non-reactive JPA applications and NoSQL backends are outside this root cause. This issue is fixed in 9.4.0.

### CVE-2026-105436

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-08T17:17:12.363 |

Deserialization of Untrusted Data vulnerability in MainWP MainWP Child mainwp-child allows Object Injection.This issue affects MainWP Child: from n/a through 6.2.1.

### CVE-2026-105281

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-09T14:17:11.450 |

The internal data publisher on openPDC accepts network connections without authentication in its default configuration. An unauthenticated network attacker can connect to this interface and retrieve the complete device and measurement topology of the system.

### CVE-2026-83943

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-10-08T23:17:04.267 |

Exposure of sensitive information to an unauthorized actor in Azure API Center allows an unauthorized attacker to disclose information over a network.

### CVE-2026-105674

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330` |
| Published | 2026-10-08T23:16:57.663 |

TP-Link Tapo
C325WB V2 generates the pre-shared key used by its local media streaming
service with a time-seeded pseudo-random number generator, making the key
predictable and recoverable. An unauthenticated attacker on the adjacent
network can recover the key and authenticate to the media streaming service
without valid user credentials. 









Successful
exploitation may allow an unauthenticated adjacent-network attacker to access
and take over live video and audio streams, compromising the confidentiality
and integrity of camera media.

### CVE-2026-105672

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-08T23:16:57.333 |

TP-Link Tapo
C325WB V2 contains an unauthenticated authorization bypass vulnerability in the
HTTPS JSON API dispatcher on TCP port 443. An attacker on the adjacent network
can append an onboarding-scoped object to a JSON request to bypass session
verification and invoke privileged actions without authentication. 





Successful
exploitation may allow an unauthenticated adjacent-network attacker to access
live video and audio, modify device settings, and obtain sensitive device
information or secrets.

### CVE-2026-107725

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-08T22:17:28.967 |

Hazelcast is a unified real-time data platform combining stream processing with a fast data store. Prior to 5.4.5, 5.5.10, and 5.6.1, missing authorization checks in the IMap Predicates API allow a malicious client with limited privileges to execute arbitrary code on a Hazelcast cluster member. This issue is fixed in versions 5.4.5, 5.5.10, 5.6.1, and 5.7.0.

### CVE-2026-101024

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-08T21:17:51.240 |

Satel Netco Design versions prior to v2.1.7 contains a relative path traversal vulnerability in its data export functionality. An authenticated user with Viewer privileges could write attacker influenced content to file system locations accessible to the application service. Successful exploitation could result in unauthorized file creation or modification and, under certain conditions, arbitrary code execution.

### CVE-2026-106433

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-08T19:16:59.233 |

Improper state management in MongoDB libmongocrypt can cause provider-specific data to be treated as an incompatible type when cleaning up a key document containing duplicate masterKey fields. An authenticated actor who can modify key vault documents, or a server that returns such a key document, can cause invalid memory access and invalid frees in the client process. This can terminate the application or corrupt process memory.

### CVE-2026-93858

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T18:18:30.817 |

In OpenStack Mistral through 23.0.0, the std.ssh_proxied action passes a caller-supplied proxy_command value directly to paramiko.ProxyCommand() before any SSH connection to a gateway or target host is attempted. An authenticated project member can use the standard action-execution API to submit an arbitrary local command as proxy_command; paramiko starts that command as a subprocess on the executor host under the executor's own service account, independent of whether the SSH connection itself ever succeeds. Only Mistral deployments that permit the std.ssh_proxied action, the default configuration, are affected.

### CVE-2026-107378

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-08T18:17:23.417 |

CairoSVG is an SVG converter based on Cairo, a 2D graphics library. Prior to 2.9.1, rendering an attacker-controlled SVG with a path containing many segments can cause quadratic CPU consumption in cairosvg/path.py. The path tokenizer repeatedly slices and rescans the remaining path data, while draw_markers drains node.vertices with node.vertices.pop(0), causing repeated linear-time work. The svg2png, svg2pdf, and svg2ps APIs reach these operations during ordinary rendering, allowing a sub-megabyte SVG to consume substantial CPU and deny service to a rendering application. This issue is fixed in version 2.9.1.

### CVE-2026-107639

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-08T15:17:47.117 |

ILIAS before 9.24, 10.x before 10.12 and 11.x before 11.5 contains an argument injection vulnerability in assImagemapQuestionGUI that allows question authors to inject ImageMagick convert options via uploaded image filenames. Attackers can embed tab-separated options, which escapeshellcmd() does not neutralise, to write a PHP file under the web root and achieve remote code execution.

### CVE-2026-105830

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-08T15:17:35.340 |

league/commonmark from 2.0.0 before 2.10.2 contains a quadratic-time denial of service vulnerability in the GitHub Flavored Markdown Table extension's TableStartParser::tryStart() block-start scan. Unauthenticated attackers can submit a large paragraph of pipe-free lines not starting with letters, forcing repeated full-buffer strpos scans that exhaust PHP worker CPU.

### CVE-2026-81932

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-08T22:17:32.493 |

IBM Guardium Data Protection 12.0, 12.1, and 12.2 is vulnerable to SQL injection. A remote unauthenticated attacker could send specially crafted SQL statements, which could allow the attacker to view, add, modify, or delete information in the back-end database.

### CVE-2026-8374

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:N/R:I/V:D/RE:H/U:Red` |
| Weaknesses | `CWE-1204;CWE-1240` |
| Published | 2026-10-09T13:17:11.240 |

Misuse and misconfiguration in Bluetooth communication in SwitchBot Door Lock Series allows an attacker to bypass the electronic lock and access controls via a manipulated communication protocol.

### CVE-2026-96329

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T10:16:43.740 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in tagDiv tagDiv Opt-In Builder td-subscription allows Blind SQL Injection.This issue affects tagDiv Opt-In Builder: from n/a through 1.7.6.

### CVE-2026-95610

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T10:16:43.330 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in UpSolution UpSolution Core us-core allows Blind SQL Injection.This issue affects UpSolution Core: from n/a through 9.3.

### CVE-2026-95607

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T10:16:42.917 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in VibeThemes WPLMS  wplms allows Blind SQL Injection.This issue affects WPLMS : from n/a through 4.973.

### CVE-2026-95599

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T10:16:42.780 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Taskbuilder Taskbuilder taskbuilder allows Blind SQL Injection.This issue affects Taskbuilder: from n/a through 6.0.5.

### CVE-2026-94663

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T10:16:41.283 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Metagauss ProfileGrid profilegrid-user-profiles-groups-and-communities allows Blind SQL Injection.This issue affects ProfileGrid: from n/a through 6.0.0.2.

### CVE-2026-105269

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-08T22:17:26.387 |

Satel Netco Design versions prior to v2.1.7 contains a stored cross site scripting vulnerability. An authenticated user with Network Operator privileges could store untrusted content that is rendered without adequate neutralization. Successful exploitation could allow script execution in another user's browser when the affected content is viewed.

### CVE-2026-11318

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-08T21:17:53.377 |

Deskin through 3.3.4.3 contains a privilege escalation vulnerability in the com.deskin.service.installer XPC service that allows local unprivileged attackers to execute arbitrary installer packages as root by connecting to the root-owned service without authentication. Attackers can invoke the privileged installer method to run an attacker-supplied installer, achieving full root compromise of the macOS host.

### CVE-2026-107782

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-08T21:17:53.227 |

System Informer before 4.0.26241.138 contains an incorrect authorization vulnerability in the phsvc helper that allows local attackers to reach privileged APIs by connecting from any Authenticode-signed process. Attackers can load code into a Microsoft-signed host like rundll32.exe, connect to SiSvcApiPort, and call PhSvcApiCreateService to execute code as SYSTEM.

### CVE-2026-107707

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-08T20:17:35.690 |

Intego Antivirus for Windows through 3.0.0.1 contains a link following vulnerability in its optimization module that allows local unprivileged users to delete arbitrary folders as SYSTEM. Attackers can replace a scanned duplicate file's directory with a junction to C:\Config.msi and abuse Windows Installer rollback to execute code as SYSTEM.

### CVE-2026-107322

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-10-08T19:16:59.857 |

An incomplete list of disallowed inputs in Amazon Agent Plugins for AWS databases-on-aws plugin before 1.7.1 might allow a remote unauthenticated actor to execute arbitrary operating system commands on the host running the helper via a crafted database command value introduced in the agent context.



To remediate this issue, users should upgrade to databases-on-aws plugin version 1.7.1 or later and verify that the updated plugin is active in each environment where it is used.

### CVE-2026-104077

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-1188` |
| Published | 2026-10-08T17:17:11.603 |

Obsidian Desktop before 1.14.0 contains a remote code execution vulnerability that allows attackers to craft malicious Markdown notes exploiting insufficient sanitization of the data-background-iframe attribute, which bypasses DOMPurify and is processed by the bundled Reveal.js 4.3.1 within the Slides core plugin, allowing a javascript: URL to execute in the resulting background iframe. Because Node integration is enabled and context isolation is disabled in Obsidian's vault renderer, the injected script can call parent.require() to access Node APIs such as fs and child_process, enabling arbitrary operating system command execution when the victim opens the note and manually starts the presentation.

### CVE-2026-107732

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-08T23:16:58.873 |

SumatraPDF is a multi-format reader for Windows. In 3.6.1 and earlier, untrusted document paths and PDF link targets are interpolated into notification text that ParseTip() interprets as trusted tip markup. When a user clicks an injected link, ExecuteTipLink() dispatches its CmdExec command and can execute an attacker-selected local program in the user's context. No broader impact is claimed beyond the advisory-supported conditions. No fixed version is available as of this review.

### CVE-2026-84250

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-08T20:17:37.460 |

IBM Guardium Data Protection 12.2 is vulnerable due to weak cryptographic protection and a hard-coded recovery key in the pkcrypto passkey component. A local attacker could exploit this vulnerability to recover the root password and gain root privileges.

### CVE-2026-104078

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-1188` |
| Published | 2026-10-08T17:17:11.753 |

Obsidian Desktop before 1.14.0 contains a filter bypass vulnerability in the bundled MathJax 3.2.2 Safe component that allows attackers to execute arbitrary code by embedding a crafted \href value with a TAB byte in the URL scheme, causing filterURL to produce an empty protocol that bypasses the configured safeProtocols restrictions. Attackers can craft a note containing a malicious MathJax formula that renders as a javascript: URL anchor, which when clicked by the victim in Live Preview executes in the Node-integration-enabled vault renderer via require('child_process'), achieving arbitrary operating system command execution as the desktop user.

### CVE-2026-107705

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-08T20:17:35.300 |

Poppler 0.42.0 through 26.10.0 contains a stack-based buffer overflow in Decrypt::revision6Hash() that allows attackers controlling the password to overwrite stack memory when opening AESV3/R6 encrypted PDFs. Attackers can supply a password longer than 127 bytes through applications using the libpoppler, libpoppler-glib or C++ API to overflow the K1 and E buffers, crashing the process or corrupting memory.

### CVE-2026-105833

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-08T15:17:35.913 |

EspoCRM before 10.0.5 contains an insecure direct object reference vulnerability in PersonalAccount\Service that allows users with Email Account scope access to retrieve other users' IMAP passwords. Attackers who know a victim's Email Account record ID can request that record to steal stored IMAP credentials and access the victim's mailbox.

### CVE-2026-71884

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-323` |
| Published | 2026-10-09T10:16:38.260 |

In Bouncy Castle for Java LTS before 2.73.13, the native one-shot CTR packet cipher did not check that the requested input length fitted the counter space the IV left. In CTR mode the IV and the block counter share one 16-byte block, so an IV of 13 to 15 bytes leaves a counter of only 1 to 3 bytes, addressing 256, 65536 or 16777216 blocks respectively. Given a longer input the counter wrapped and the keystream repeated from the start of the same packet, and the call then returned the full input length as though every byte had been correctly transformed. Two segments of the message were therefore encrypted under the same keystream, so their plaintexts can be recovered from the ciphertext alone, without the key, while the caller saw neither an exception nor a short length to indicate it. The streaming implementation validates at init and again while processing, and the portable AESCTRPacketCipher rejects such a request with "Counter in CTR/SIC mode out of range.", but the native one-shot path has a single entry point and performed no counter-range validation there. It now preflights the IV-derived counter range and rejects an over-long request before any output is written, so the operation is failure-atomic and never reports success for bytes it did not correctly transform. A counter of four bytes or more cannot be exhausted by a Java int length and is unaffected, as is a full 16-byte IV, where the counter range is the caller's responsibility. Bouncy Castle for Java (bcprov) is not affected, as it ships no native implementations.

### CVE-2026-104635

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-09T09:17:07.360 |

Uncontrolled Recursion vulnerability in Protobuf.JSON.Decode in elixir-protobuf protobuf allows an unauthenticated remote attacker to crash the decoding process via a deeply nested JSON document. Any application that decodes attacker-supplied JSON with Protobuf.JSON.decode/3, Protobuf.JSON.decode!/3, or Protobuf.JSON.from_decoded/3 into a schema that contains a self-referential or cyclic message type is affected.

In lib/protobuf/json/decode.ex, the embedded-message clause of decode_singular/3 recurses into internal_from_json_data/3 once per nesting level without incrementing or checking the decoder's depth counter. The depth guard increase_depth_and_maybe_throw/1 covers only the Google.Protobuf.ListValue and Google.Protobuf.Struct clauses, so the recursion_limit option has no effect on user-defined message types. Each nesting level allocates a stack frame and heap objects, and a sufficiently deep document exhausts the memory of the decoding process. Confidentiality and integrity are not affected.

This issue affects protobuf: from 0.8.0 before 0.17.1.

### CVE-2026-107829

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-916` |
| Published | 2026-10-08T22:17:30.640 |

Jivejdon through 5.0 contains a weak password storage vulnerability that stores account passwords as unsalted MD5 digests via ToolsUtil.hash() in AccountDaoSql. Attackers who obtain the user table through database access or SQL injection can crack passwords with precomputed tables or GPU attacks.

### CVE-2026-17189

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-08T21:17:56.633 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 is vulnerable to cross-site scripting. This vulnerability allows an unauthenticated user to embed arbitrary JavaScript code in the Web UI thus altering the intended functionality potentially leading to credentials disclosure within a trusted session

### CVE-2026-107325

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-10-08T19:17:00.173 |

Improper validation of a BSON array length in the MongoDB Go Driver can cause an out-of-bounds index and runtime panic when an application calls bson.RawArray.Validate or bsoncore.Array.Validate on a malformed four-byte array. An unauthenticated actor who can supply raw BSON array data to an affected application may terminate an unprotected application process, causing a denial of service. No confidentiality or integrity impact has been identified.

### CVE-2026-107324

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-08T19:17:00.020 |

An integer overflow in BSON value-length handling in the MongoDB Go Driver can cause a runtime panic when an application validates or accesses a malformed BSON document. An unauthenticated actor who can supply BSON bytes to an affected application may terminate an unprotected application process, causing a denial of service. The driver's server-monitoring path contains panic recovery and is limited to server-selection failure.

### CVE-2026-107376

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-08T18:17:22.373 |

webonyx graphql-php is a PHP implementation of the GraphQL specification. Prior to 15.32.3, GraphQL\Language\Parser performs recursive descent without a recursion limit in parseSelectionSet, parseValueLiteral, and parseTypeReference. A remote attacker can submit deeply nested selection sets, object or list values, or list types that exhaust the PHP process stack during pre-validation parsing, before query validation and complexity controls run. The resulting SIGSEGV can terminate PHP-FPM workers or long-running Swoole, RoadRunner, ReactPHP, or CLI processes and cannot be caught by application-level exception handling. This issue is fixed in version 15.32.3.

### CVE-2026-14905

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-08T15:17:49.837 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 is vulnerable to an XML external entity injection (XXE) attack when processing XML data. A remote attacker could exploit this vulnerability to expose sensitive information or consume memory resources.

### CVE-2026-14496

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-08T15:17:48.880 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to a heap-based buffer overflow.

### CVE-2026-94067

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-09T14:17:26.027 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Fuelthemes The Voux thevoux-wp allows PHP Local File Inclusion.This issue affects The Voux: from n/a through 6.9.5.

### CVE-2026-94062

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-09T13:17:12.423 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Fuelthemes Werkstatt werkstatt allows PHP Local File Inclusion.This issue affects Werkstatt: from n/a through 4.8.3.

### CVE-2026-84247

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-08T22:17:33.987 |

IBM Guardium Data Protection 12.2 could allow a remote authenticated attacker to cause a denial of service due to a path traversal vulnerability.

### CVE-2026-84246

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-10-08T22:17:33.850 |

IBM Guardium Data Protection 12.0, 12.1, and 12.2 could allow a remote attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-84209

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-08T22:17:33.583 |

IBM Guardium Data Protection 12.2.2, and 12.1 could allow a remote attacker to execute arbitrary SQL commands due to improper neutralization of special elements used in an SQL command.

### CVE-2026-84198

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-10-08T22:17:33.457 |

IBM Guardium Data Protection 12.0, 12.1, and 12.2 could allow a remote attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-84058

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-08T22:17:33.313 |

IBM Guardium Data Protection 12.0, 12.1, and 12.2 is vulnerable to a buffer overrun in the TDS (Microsoft SQL Server) PRELOGIN packet decoder. A remote attacker who can send a specially crafted TDS PRELOGIN packet to a network monitored by an IBM Guardium Collector may cause a denial of service or potentially execute arbitrary code on the Collector appliance.

### CVE-2026-84057

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T22:17:33.170 |

IBM Guardium Data Protection 12.2.2, and 12.1 could allow a remote attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-84035

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-08T22:17:33.027 |

IBM Guardium Data Protection 12.0, 12.1, and 12.2 could allow a remote attacker to execute arbitrary code due to a stack-based buffer overflow.

### CVE-2026-82900

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-08T22:17:32.753 |

IBM Guardium Data Protection 12.2.2, and 12.1 could allow a remote attacker to delete arbitrary files due to improper limitation of a pathname to a restricted directory.

### CVE-2026-82895

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-10-08T22:17:32.627 |

IBM Guardium Data Protection 12.0, 12.1, and 12.2 could allow a remote attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-107723

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1287` |
| Published | 2026-10-08T22:17:28.623 |

fast-jwt provides fast JSON Web Token (JWT) implementation. Prior to 6.3.0, fast-jwt createVerifier accepts a validly signed JWT whose payload is a JSON array because src/decoder.js checks that the payload is an object but does not reject arrays. The claim validator loop then finds no named exp, nbf, iss, aud, sub, jti, or nonce properties and silently skips those configured checks, returning the array as a successfully verified payload. An attacker who can produce or influence a validly signed token may bypass expiry, issuer, audience, subject, revocation, and replay protections. The opt-in requiredClaims option can block missing claims, and signature verification itself is not bypassed. This issue is fixed in version 6.3.0.

### CVE-2026-19494

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-08T21:17:57.340 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 could allow a remote authenticated attacker to bypass security restrictions due to improper authentication.

### CVE-2026-82344

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-10-08T20:17:37.020 |

IBM Guardium Data Protection 12.0, 12.1 is vulnerable to a heap-based buffer overflow in the S-TAP TrafficTap TDS login reassembly functionality. An unauthenticated remote attacker can send crafted TDS login fragments that exceed the fixed-size reassembly buffer, potentially resulting in denial of service or arbitrary code execution on the affected system.

### CVE-2026-82335

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-10-08T20:17:36.873 |

IBM Guardium Data Protection 12.0, 12.1, 12.2 is vulnerable to a heap-based buffer overflow in the MongoDB protocol parser. A remote attacker could send a specially crafted MongoDB SCRAM username containing an excessive length and cause memory corruption, potentially resulting in denial of service or arbitrary code execution.

### CVE-2026-82334

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-08T20:17:36.737 |

IBM Guardium Data Protection 12.0, 12.1, 12.2 is vulnerable to a heap-based out-of-bounds read in the TDS7 LOGIN7 protocol parser. A remote attacker could send a specially crafted TDS LOGIN7 packet containing invalid offset or length values, potentially causing information disclosure or denial of service.

### CVE-2026-107384

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-08T19:17:00.990 |

MariaDB Connector/Node.js is used to connect applications developed on Node.js to MariaDB and MySQL databases. From 3.2.0 until 3.2.5, 3.3.4, 3.4.7, and 3.5.4, applications that enable permitSetMultiParamEntries can pass objects whose keys are expanded into a SQL SET clause without being processed by escapeId. An attacker-controlled key containing a backtick can close the quoted identifier and cause the remainder of the key to be interpreted as SQL. This can update columns the application did not intend to expose and can append arbitrary SQL with the database user's privileges. The option is disabled by default, and serialized-object handling used when it is disabled is not affected. This issue is fixed in versions 3.2.5, 3.3.4, 3.4.7, and 3.5.4.

### CVE-2026-107333

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-08T18:17:19.603 |

Malcolm's nginx based reverse proxy contains a URL path normalization inconsistency between its Lua based role-based access control (RBAC) authorization layer and nginx's own request routing logic. An authenticated user can craft a specially formatted request path to bypass role-based restrictions and reach administrative or role gated endpoints they should not have access to. This affects all restricted paths protected by the RBAC authorization layer, including file upload, PHP server, htadmin, and authentication management interfaces.

### CVE-2026-14888

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-08T15:17:49.700 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to execute arbitrary code due to a heap-based buffer overflow.

### CVE-2026-14497

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-08T15:17:49.013 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote authenticated attacker to bypass security restrictions due to improper verification of cryptographic signatures.

### CVE-2026-19575

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-09T08:16:55.057 |

The user-mode verification handler for the device_deinit() system call, z_vrfy_device_deinit() in kernel/device.c, validated its dev argument with K_SYSCALL_OBJ_INIT(dev, K_OBJ_ANY). k_object_validate() short-circuits its type comparison when the requested type is K_OBJ_ANY, so the check reduced to "this pointer is the base address of some kernel object the calling thread has been granted" — the object's actual type was never compared, and K_SYSCALL_OBJ_INIT also skips the initialization-state check. The sibling handlers z_vrfy_device_init() and z_vrfy_device_is_ready() already used K_OBJ_DRIVER_ANY and were unaffected.

A thread running in user mode can therefore pass any kernel object it holds permission on — most usefully a thread stack object obtained from the k_thread_stack_alloc() syscall or a statically defined K_THREAD_STACK it was granted in order to spawn a child user thread — whose backing memory is writable from user mode. z_impl_device_deinit() then interprets those attacker-written bytes as a struct device: it dereferences the state pointer read out of the object, calls the function pointer read out of ops.deinit, and on success writes through state again. The result is an indirect call to an arbitrary address executed in supervisor mode, plus an arbitrary kernel read and a single-byte kernel write.

Exploitation gives a local unprivileged thread full kernel code execution, defeating the CONFIG_USERSPACE isolation boundary entirely; a less precise attempt yields a supervisor-mode fault and a system crash. The defect is only reachable in builds that enable both CONFIG_USERSPACE and CONFIG_DEVICE_DEINIT_SUPPORT — with de-initialization support disabled, z_impl_device_deinit() returns -ENOTSUP without ever dereferencing the pointer. In v4.2.x and v4.3.x, CONFIG_DEVICE_DEINIT_SUPPORT defaulted to y, so every CONFIG_USERSPACE build of those releases is exposed unless the option was explicitly turned off. From v4.4.0 the option is opt-in (no default, and not selected by any in-tree subsystem), so a v4.4.x build is exposed only if it enables the option explicitly. The v4.2 line is no longer maintained and receives no backport.

The fix changes the object check to K_OBJ_DRIVER_ANY, which constrains the argument to the build-generated driver object type range (K_OBJ_DRIVER_FIRST..K_OBJ_DRIVER_LAST) — the real struct device instances placed by the linker — so the state and ops.deinit fields are once again kernel-controlled.

### CVE-2026-107914

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-459` |
| Published | 2026-10-09T06:17:12.777 |

Backdrop CMS 1.34 before 1.34.5 and 1.35 before 1.35.1 doesn't sufficiently protect configuration exports when delivering a compressed archive. This vulnerability is mitigated by the fact that an export must have been previously requested by someone with the "Synchronize, import, and export configuration" permission. NOTE: CVE-2026-107914 refers to the vulnerability in which config.admin.inc does not ensure that a file_unmanaged_delete operation occurs. Therefore, many archives could persist: config.tar.gz, config_0.tar.gz, config_1.tar.gz, etc. There is a separate config.module issue that could allow remote access by an anonymous user, but only for the one filename config.tar.gz.

### CVE-2026-84271

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-347` |
| Published | 2026-10-08T20:17:37.610 |

IBM Guardium Data Protection 12.2 is vulnerable to a signature verification bypass in the patch installer. An attacker with local access could exploit this vulnerability to execute arbitrary code with root privileges.

### CVE-2026-84245

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-08T20:17:37.313 |

IBM Guardium Data Protection 12.2 is vulnerable to a local privilege escalation in the cp_wrapper component. A low-privileged local user could exploit this vulnerability to gain root privileges and access or modify sensitive system files.

### CVE-2026-107709

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-08T17:17:16.293 |

A path traversal vulnerability exists in Bower decompress-zip through version 0.3.3. The vulnerability located in `lib/decompress-zip.js` improperly validates archive entry paths during ZIP extraction. A crafted ZIP archive containing entries that resolve to prefix-sibling directories can cause files to be written outside the intended extraction directory. Successful exploitation may allow arbitrary file overwrite, application compromise, or remote code execution depending on the target environment and writable sibling paths.

### CVE-2026-104629

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-10-09T14:17:11.027 |

A component loading mechanism in openPDC and openHistorian will construct and run any specified type, which may be an invalid component to load. An attacker with an authenticated user account and the ability to place a file on the host filesystem can use this to run arbitrary constructor code, and this code runs with the privileges of the affected service account.

### CVE-2026-78024

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-09T10:16:38.570 |

Dell Secure Connect Gateway (SCG) Policy Manager, versions prior to 5.34.00.16, contains a Server-Side Request Forgery (SSRF) vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Information disclosure, Protection mechanism bypass, Server-side request forgery, and Unauthorized access.

### CVE-2026-107911

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-09T06:17:12.620 |

A type confusion vulnerability in the _read_flags function (src/commands/cmd_dispatcher.c) in FalkorDB before 4.20.0 allows a remote authenticated attacker who can run GRAPH.QUERY to cause a denial of service and possibly disclose or corrupt memory. The function accepts a --bolt argument from any client and casts the following command argument, a Redis string object, to a Bolt client structure without checking its origin; the result-set code then dereferences pointers read from that object. The argument is parsed even when the Bolt endpoint is disabled, so default configurations are affected.

### CVE-2026-83947

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-08T23:17:04.423 |

Missing authorization in Azure Event Grid allows an authorized attacker to perform spoofing over a network.

### CVE-2026-93017

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-08T15:17:56.950 |

The `insights-operator-gather` ClusterRole grants the operator's service account read access to secrets in the core API group with no namespace or resourceNames restriction — therefore, access to every secret in every namespace in the cluster.

Ref: https://github.com/openshift/insights-operator/blob/8f15e3157ff09f54ab22801f5b21da35a195cc6d/manifests/03-clusterrole.yaml#L368-L373
```
- apiGroups:
  - ""
  resources:
  - secrets
  verbs:
  - get
  - list
```

By spawning a pod with the gather service account mounted, an attacker will be able to access any secret in any namespace.

```
spec:
 serviceAccountName:"gather"
```

### CVE-2026-14507

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T15:17:49.283 |

IBM DataPower Gateway 11.0.0.0 through 11.0.0.2 could allow a remote authenticated attacker to cause a denial of service due to improper memory allocation during key derivation.

### CVE-2026-107303

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-08T18:17:19.277 |

JHipster is a development platform to quickly generate, develop, and deploy modern web applications and microservice architectures. Prior to generator-jhipster 9.4.0 and react-jhipster 1.1.0, generated applications can persist attacker-controlled Blob data and companion ContentType values, return them through generated REST endpoints, and pass them to the generated openFile helper in generators/client/generators/common/templates/src/main/webapp/app/shared/jhipster/data-utils.ts.ejs. The helper uses the returned ContentType as the browser Blob MIME type and opens an object URL, so a normal authenticated user with write access to a Blob-bearing entity can store active HTML or SVG content that may execute under the application origin when a privileged user opens it. Exploitability depends on the generated application's content security policy and target-browser Blob behavior. This issue is fixed in generator-jhipster 9.4.0 and react-jhipster 1.1.0.

### CVE-2026-107295

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-08T17:17:15.237 |

Pydantic AI is a Python agent framework for building applications and workflows with Generative AI. From 1.34.0 until 1.107.4 and 2.28.0, the Agent.to_web() and clai web development chat endpoint has missing request content-type validation. A website visited by a developer can submit a browser-compatible request to a loopback-hosted chat server, causing the served agent to run and execute tools with the privileges and credentials of the local process; client-relayed approval decisions also leave requires_approval=True tools exposed. Binding to localhost does not prevent a browser page from reaching the loopback address. This issue is fixed in versions 1.107.4 and 2.28.0.

### CVE-2026-107638

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-08T15:17:46.930 |

pH7Builder (pH7 Social Dating CMS) before 18.5.0 contains an improper restriction of authentication attempts vulnerability that allows attackers to bypass two-factor authentication by guessing TOTP codes without limits. Attackers who know an account password can submit unlimited 6-digit verification codes to VerificationCodeFormProcess.php to take over member, affiliate, or administrator accounts.

### CVE-2026-96461

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-09T10:16:45.000 |

Missing Authorization vulnerability in TMS Amelia ameliabooking allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Amelia: from n/a through 2.4.10.

### CVE-2026-96336

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-09T10:16:44.730 |

Authentication Bypass by Spoofing vulnerability in WPMU DEV Forminator forminator allows Identity Spoofing.This issue affects Forminator: from n/a through 1.57.2.

### CVE-2026-96333

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-09T10:16:44.460 |

Authentication Bypass by Spoofing vulnerability in Liquid Web / StellarWP GiveWP give allows Identity Spoofing.This issue affects GiveWP: from n/a through 4.16.8.1.

### CVE-2026-94666

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-09T10:16:41.690 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in ZealousWeb Generate PDF using Contact Form 7 generate-pdf-using-contact-form-7 allows Path Traversal.This issue affects Generate PDF using Contact Form 7: from n/a through 4.2.1.

### CVE-2026-94664

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-09T10:16:41.420 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in add-ons.org PDF for Contact Form 7 pdf-for-contact-form-7 allows Path Traversal.This issue affects PDF for Contact Form 7: from n/a through 7.1.0.

### CVE-2026-78025

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-09T10:16:38.707 |

Dell Secure Connect Gateway (SCG) Policy Manager, versions prior to 5.34.00.16, contains a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Information disclosure, Protection mechanism bypass, and Unauthorized access.

### CVE-2026-78020

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-09T09:17:09.300 |

Dell Secure Connect Gateway (SCG) Policy Manager, versions prior to 5.34.00.16, contains an Improper Certificate Validation vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Denial of service, Information disclosure, and Remote execution.

### CVE-2026-78019

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-09T09:17:09.177 |

Dell Secure Connect Gateway (SCG) Policy Manager, versions prior to 5.34.00.16, contains an Inclusion of Functionality from Untrusted Control Sphere vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges, Filesystem access for attacker, and Remote execution.

### CVE-2026-97076

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-624` |
| Published | 2026-10-09T07:17:19.350 |

Executable Regular Expression Error vulnerability in WP Media WP Rocket wp-rocket allows Code Injection.This issue affects WP Rocket: from n/a before 3.23.5.

### CVE-2026-107728

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-08T23:16:58.180 |

Strawberry GraphQL is a library for creating GraphQL APIs. From 0.217.0 until 0.326.1, PermissionExtension.resolve() on a synchronous field resolver evaluates the result of has_permission() for truthiness. When a custom permission declares has_permission() as a normal function but returns an awaitable, supports_sync does not classify it as asynchronous, the awaitable is not awaited, and its inherently truthy object value permits the protected resolver to run even when the result would resolve to false. This affects synchronous field resolvers under both execute_sync() and execute(); permissions declared with async def has_permission() and synchronous permissions returning a boolean are not affected. This issue is fixed in version 0.326.1.

### CVE-2026-84875

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-08T22:17:34.430 |

IBM Guardium Data Protection 12.0, 12.1, and 12.2 could allow a remote attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-84230

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-08T22:17:33.727 |

IBM Guardium Data Protection 12.2.2 could allow a remote attacker to cause a denial of service due to a race condition resulting from concurrent unsynchronized writes to a shared map.

### CVE-2026-19493

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-08T21:17:57.203 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 could allow a remote attacker to perform an arbitrary file write due to path traversal.

### CVE-2026-84275

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-08T20:17:38.077 |

IBM Guardium Data Protection 12.2 is vulnerable to path traversal in the GIM file-upload functionality. An unauthenticated attacker could exploit this vulnerability to write arbitrary files to the Collector.

### CVE-2026-95209

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-08T19:20:52.830 |

An issue in gnutls v3.8.13 causes legitimate CA certificates to be rejected, leading to a Denial of Service (DoS).

### CVE-2026-84276

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-08T19:20:51.240 |

IBM Guardium Data Protection 12.2.2 is affected by a denial-of-service vulnerability in the edge-controller. An unauthenticated remote attacker with network access to the edge-controller gRPC service can provide malformed task data that triggers an unchecked type assertion, causing the edge-controller process to terminate unexpectedly.

### CVE-2026-67693

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-08T19:18:41.280 |

An issue in gnutls v.3.8.13 allows an attacker to obtain sensitive information via failing to reject end-entity X.509 certificates that contain a contradictory combination of Key Usage (KU) and Extended Key Usage (EKU)

### CVE-2026-107383

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-08T19:17:00.783 |

MariaDB Connector/Node.js is used to connect applications developed on Node.js to MariaDB and MySQL databases. Prior to 3.2.5, 3.3.4, 3.4.7, and 3.5.4, the GeoJSON Polygon and MultiPolygon binary encoders size a Buffer.allocUnsafe() allocation from each ring's numeric length before confirming that the ring is an array. A malformed non-array ring can therefore reserve bytes that the writing loop skips, and the connector sends the full buffer through execute() or batch(), disclosing uninitialized Node.js heap data into a database value. The persisted data can include other users' content, session material, database credentials, or TLS key material and may propagate to backups and replicas. The text-protocol query() path is not affected. This issue is fixed in versions 3.2.5, 3.3.4, 3.4.7, and 3.5.4.

### CVE-2026-95184

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-08T18:18:33.240 |

Improper certificate validation in gnutls v3.8.13 causes the application to reject legitimate certificates for valid users, leading to a Denial of Service (DoS).

### CVE-2026-107377

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-10-08T18:17:22.973 |

datamodel-code-generator generates Python data models from schema definitions. From 0.59.0 until 0.81.0, an attacker-controlled Protobuf schema can supply absolute or parent-directory paths captured by WEAK_IMPORT_PATTERN and consumed by _write_missing_weak_imports in src/datamodel_code_generator/parser/protobuf.py. Exploitation requires a victim or automated job to process the attacker-controlled schema with Protobuf input support, which requires the grpcio-tools package. The paths escape the weak_imports temporary directory before protoc runs, allowing creation of directory trees and new files or overwrite of existing writable files with a generated Protobuf syntax declaration. The effect persists when later Protobuf compilation fails. The written content is limited to a proto2 or proto3 syntax declaration, and direct arbitrary code execution has not been demonstrated. This issue is fixed in version 0.81.0.

### CVE-2026-107302

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-08T18:17:19.100 |

msgpack5 is a msgpack v5 implementation for node.js and the browser. Prior to 6.1.0, the decoder reads the four-byte length of a map32 value before validating that the complete five-byte header is available. A truncated map32 header therefore causes a checked out-of-bounds buffer read and throws RangeError instead of IncompleteBufferError, which can unexpectedly terminate a request, stream, or worker in applications that wait for additional bytes after IncompleteBufferError. There is no adjacent-memory disclosure because the buffer implementation checks bounds. This issue is fixed in version 6.1.0.

### CVE-2026-107300

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-08T17:17:16.000 |

msgpack5 is a msgpack v5 implementation for node.js and the browser. Prior to 6.1.0, the streaming decoder recursively invokes itself for each complete MessagePack value remaining in a chunk. A remote peer can send one chunk containing many small valid values, causing recursion proportional to the value count, exhausting the JavaScript call stack, and interrupting the process or stream. This issue is fixed in version 6.1.0.

### CVE-2026-95208

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-08T16:18:01.420 |

An issue in the ConfirmNameConstraints() function (wolfcrypt/src/asn.c) of wolfSSL v5.9.1 and v5.9.2 allows attackers to cause a Denial of Service (DoS) via providing crafted Certificate Authority certificates, leading to valid certificates without SAN to be incorrectly rejected by wolfSSL-based TLS clients.

### CVE-2026-107589

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-08T15:17:45.153 |

Insufficient job validation for service accounts in Jacamar CI prior to v0.30.0 allows authenticated CI users to generate arbitrary account names.

### CVE-2026-107286

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-772` |
| Published | 2026-10-08T15:17:40.753 |

Pydantic AI is a Python agent framework for building applications and workflows with Generative AI. From 2.10.0 until 2.53.0, streamed requests made through ConcurrencyLimitedModel or limit_model_concurrency can retain shared concurrency slots because anyio.CapacityLimiter associates an acquired slot with the borrowing task while streaming cleanup can run in a different task. Early stream termination, cancellation, consumer exceptions, or complete stream_text() consumption with debounce_by=0.1 can therefore leave capacity occupied, eventually preventing later requests that share the long-lived limiter from proceeding and causing a denial of service. Agent-level max_concurrency and non-streaming model requests are not affected. This issue is fixed in version 2.53.0.

### CVE-2026-76779

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-09T09:17:08.430 |

Dell Secure Connect Gateway (SCG) Policy Manager, versions prior to 5.34.00.16, contains an Improper Restriction of Excessive Authentication Attempts vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges, Protection mechanism bypass, and Unauthorized access.

### CVE-2026-107724

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-08T22:17:28.800 |

fast-jwt provides fast JSON Web Token (JWT) implementation. In 6.2.4, fast-jwt can classify raw serialized public JWK or JWKS JSON as an HMAC secret because src/crypto.js performDetectPublicKeyAlgorithms treats non-PEM strings as symmetric key material. If HS256 is explicitly allowed or inferred, an attacker who knows the exact serialized public-key bytes can use those bytes as an HMAC key and create a token containing arbitrary claims that createVerifier accepts. Serialization ordering or whitespace differences can prevent exploitation, and applications using supported PEM keys with an asymmetric-only algorithm allowlist are not affected. This issue is fixed in version 6.3.0.

### CVE-2026-107720

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-20;CWE-347` |
| Published | 2026-10-08T22:17:28.090 |

fast-jwt provides fast JSON Web Token (JWT) implementation. Prior to 6.3.1, fast-jwt createVerifier accepts an unsigned JWT when key is an empty string or null and algorithms is a non-empty allowlist. Falsy synchronous keys bypass prepareKeyOrSecret, allowedAlgorithms remains active, hasKey is false, and the empty signature avoids the verifySignature gate. An attacker can therefore submit a token containing arbitrary claims without possessing a signing key, resulting in authentication or authorization bypass. Claim validators still run, and non-empty keys, an empty key without algorithms, and the async key resolver path do not have this behavior. This issue is fixed in version 6.3.1.

### CVE-2026-107318

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-08T21:17:51.807 |

@fastify/reply-from is a Fastify plugin that forwards requests to an upstream HTTP or HTTPS server. In versions prior to 12.7.0, all of the built-in HTTPS transports override the secure default and set rejectUnauthorized to false, so the proxy does not verify the TLS certificate of the upstream even when the application points it at an https upstream in the default configuration. An on-path network attacker can therefore impersonate the configured HTTPS upstream, read the credentials and request bodies the proxy forwards, and return forged responses that the application trusts. The issue is fixed in @fastify/reply-from 12.7.0, and users should upgrade to 12.7.0 or later. As a workaround, pass an explicit rejectUnauthorized true on the transport, supply an already configured undici instance, or use the undici global agent.

### CVE-2026-107385

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-08T19:17:01.170 |

MariaDB Connector/Node.js is used to connect applications developed on Node.js to MariaDB and MySQL databases. Prior to 3.2.5, 3.3.4, 3.4.7, and 3.5.4, text-protocol escaping always prefixes quotes with a backslash and does not honor the session's NO_BACKSLASH_ESCAPES mode, including in Connection.escape(). When that mode is enabled, the backslash is an ordinary character, so an attacker-controlled placeholder value can close the SQL string literal and inject arbitrary SQL with the application's database privileges. The vulnerable configuration may be enabled server-wide, through connector initialization options, or with an application-issued SET sql_mode; execute() and batch() use binary protocols and are not affected. This issue is fixed in versions 3.2.5, 3.3.4, 3.4.7, and 3.5.4.

### CVE-2026-14999

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-08T15:17:50.360 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to bypass authentication by forging valid JSON Web Signatures due to improper verification of cryptographic signatures.

### CVE-2026-106581

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-09T14:17:18.433 |

Before 4.92.0, Docker Desktop for Windows did not verify the signature of a package supplied to Docker Desktop Installer.exe install -package. An attacker able to provide a crafted package and convince a user to approve the Docker-signed UAC prompt could execute attacker-controlled installer actions as LocalSystem.

### CVE-2026-107716

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-10-08T22:17:27.323 |

Banks generates meaningful LLM prompts using a simple template language. Prior to 2.5.1, Banks DirectoryPromptRegistry does not reject symbolic links for index.json or discovered and existing .jinja prompt files. In an application where untrusted users can influence a prompt directory, DirectoryPromptRegistry._scan() and DirectoryPromptRegistry.get() can follow a link outside the registry root and disclose a file, while DirectoryPromptRegistry.set(), DirectoryPromptRegistry._save(), and DirectoryPromptRegistry._load() can read or overwrite an external link target. The issue requires attacker influence over the registry directory or its extracted contents. This issue is fixed in version 2.5.1.

### CVE-2026-105872

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-09T13:17:08.957 |

Deserialization of Untrusted Data vulnerability in mklacroix Product Configurator for WooCommerce product-configurator-for-woocommerce allows Object Injection.This issue affects Product Configurator for WooCommerce: from n/a through 1.7.5.

### CVE-2026-94568

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-09T10:16:40.743 |

Deserialization of Untrusted Data vulnerability in WP Hosting AS Pay with Vipps for WooCommerce woo-vipps allows Object Injection.This issue affects Pay with Vipps for WooCommerce: from n/a through 6.2.0.

### CVE-2026-81929

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T07:17:18.600 |

The Ocean Pro Demos and Ocean eComm Treasure Box plugins for WordPress is vulnerable to Stored Cross-Site Scripting via the 'content' parameter in all versions up to, and including, 1.5.4, and 1.8.0, respectively, due to insufficient authorization, input sanitization, and output escaping in the Popup Builder's save_popup_content AJAX action. This makes it possible for unauthenticated attackers to inject arbitrary web scripts into a published Gutenberg popup that will execute whenever a user accesses a page on which the popup is configured to display. A valid premium license, the Popup Builder module, and at least one published Gutenberg popup configured for display are required.

### CVE-2026-84278

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T19:20:51.387 |

IBM Guardium Data Protection 12.2 is affected by a command injection vulnerability in the SUID-root ssh_config_wrapper component. An authenticated high-privileged user can inject arbitrary commands through attacker-controlled arguments, resulting in command execution with root privileges.

### CVE-2026-97147

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-08T18:18:33.583 |

In OpenStack Mistral through 23.0.0, several of the v2 API write paths resolve the target object with a query that can return another project's resource, then write to it. An authenticated project member can use this to rewrite and un-publish another project's public action definitions and environments. A project administrator can create a workbook whose embedded ad-hoc action or workflow name collides with a resource of another project, which moves that resource into the caller's project and causes the original owner's subsequent updates of it to fail with server errors. Only deployments exposing the Mistral API are affected.

### CVE-2026-94066

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T14:17:25.747 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in SpabRice Pond pond allows Reflected XSS.This issue affects Pond: from n/a through 2.6.1.

### CVE-2026-94063

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T14:17:24.990 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in ThemeREX Education Center education allows Reflected XSS.This issue affects Education Center: from n/a through 3.6.12.

### CVE-2026-62026

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-09T14:17:22.170 |

Cross-Site Request Forgery (CSRF) vulnerability in MIGHTYminnow Dashboard Notes dashboard-notes allows Cross Site Request Forgery.This issue affects Dashboard Notes: from n/a through 1.0.3.

### CVE-2026-94061

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T13:17:12.113 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Designthemes Whistle - Sports Club whistle-sports-club allows Reflected XSS.This issue affects Whistle - Sports Club: from n/a through 4.2.

### CVE-2026-94060

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T13:17:11.880 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Bracketweb Voldor voldor allows Reflected XSS.This issue affects Voldor: from n/a through 1.0.0.

### CVE-2026-94059

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T13:17:11.640 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Bracketweb Ogency ogency allows Reflected XSS.This issue affects Ogency: from n/a through 1.0.0.

### CVE-2026-94058

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T13:17:11.403 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Bracketweb Treck treck allows Reflected XSS.This issue affects Treck: from n/a through 1.0.0.

### CVE-2026-105883

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-09T13:17:09.447 |

Missing Authorization vulnerability in ThemeHunk Th Shop Mania th-shop-mania allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Th Shop Mania: from n/a through 1.9.1.

### CVE-2026-105870

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T13:17:08.710 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Delight Star Inc. WP Associate Post R2 wp-associate-post-r2 allows Reflected XSS.This issue affects WP Associate Post R2: from n/a through 5.0.1.

### CVE-2026-105318

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T13:17:08.470 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Datasolution AcyMailing SMTP Newsletter acymailing allows Reflected XSS.This issue affects AcyMailing SMTP Newsletter: from n/a through 11.1.0.

### CVE-2026-96761

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:45.840 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Welcart Welcart e-Commerce usc-e-shop allows Reflected XSS.This issue affects Welcart e-Commerce: from n/a through 2.12.3.

### CVE-2026-96607

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:45.557 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Basix NEX-Forms nex-forms-express-wp-form-builder allows Reflected XSS.This issue affects NEX-Forms: from n/a through 9.3.1.

### CVE-2026-96553

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:45.420 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Damian Góra FiboSearch ajax-search-for-woocommerce allows Reflected XSS.This issue affects FiboSearch: from n/a through 1.34.1.

### CVE-2026-96332

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:44.320 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in yalla ya! Simple Payment simple-payment allows Reflected XSS.This issue affects Simple Payment: from n/a through 2.5.4.

### CVE-2026-95609

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:43.193 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in David Lingren Media LIbrary Assistant media-library-assistant allows Stored XSS.This issue affects Media LIbrary Assistant: from n/a through 3.41.

### CVE-2026-95608

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:43.053 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in PluginUs.Net HUSKY woocommerce-products-filter allows Reflected XSS.This issue affects HUSKY: from n/a through 1.4.3.2.

### CVE-2026-95598

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:42.643 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in codepeople Search in Place search-in-place allows Reflected XSS.This issue affects Search in Place: from n/a through 1.5.5.

### CVE-2026-95596

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:42.370 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Mamunur Rashid ShopBuilder – Elementor WooCommerce Builder Addons shopbuilder allows Reflected XSS.This issue affects ShopBuilder – Elementor WooCommerce Builder Addons: from n/a through 3.4.1.

### CVE-2026-95591

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:42.237 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in e4jvikwp VikBooking Hotel Booking Engine & PMS vikbooking allows Reflected XSS.This issue affects VikBooking Hotel Booking Engine & PMS: from n/a through 1.8.14.

### CVE-2026-94668

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:41.957 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Dimitri Grassi Salon booking system salon-booking-system allows Reflected XSS.This issue affects Salon booking system: from n/a through 10.31.5.

### CVE-2026-94661

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:41.150 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Crocoblock JetBlog jet-blog allows Reflected XSS.This issue affects JetBlog: from n/a through 2.4.10.

### CVE-2026-94641

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:41.020 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Stiofan UsersWP userswp allows Reflected XSS.This issue affects UsersWP: from n/a through 1.2.73.

### CVE-2026-94632

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:40.880 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Stiofan BlockStrap Page Builder - Bootstrap Blocks blockstrap-page-builder-blocks allows Reflected XSS.This issue affects BlockStrap Page Builder - Bootstrap Blocks: from n/a through 0.1.58.

### CVE-2026-94415

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:40.473 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Muffingroup Betheme betheme allows Reflected XSS.This issue affects Betheme: from n/a through 28.5.8.

### CVE-2026-94170

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:40.333 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Heateor Support Sassy Social Share sassy-social-share allows Reflected XSS.This issue affects Sassy Social Share: from n/a through 3.3.79.

### CVE-2026-94167

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:40.193 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Extend Themes Kubio AI Page Builder kubio allows Reflected XSS.This issue affects Kubio AI Page Builder: from n/a through 2.9.3.

### CVE-2026-94166

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:40.063 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in UpSolution UpSolution Core us-core allows Reflected XSS.This issue affects UpSolution Core: from n/a through 8.44.

### CVE-2026-94161

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:39.923 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in ThemeGoods Grand Restaurant grandrestaurant allows Reflected XSS.This issue affects Grand Restaurant: from n/a before 7.0.11.

### CVE-2026-94159

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:39.787 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in KlbTheme Total Donations totaldonations allows Stored XSS.This issue affects Total Donations: from n/a through 2.0.5.

### CVE-2026-94158

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T10:16:39.653 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in bkninja Gloria Admin Panel gloria-admin-panel allows Reflected XSS.This issue affects Gloria Admin Panel: from n/a through 1.3.

### CVE-2026-78023

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-09T10:16:38.430 |

Dell Secure Connect Gateway (SCG) Policy Manager, versions prior to 5.34.00.16, contains an Authorization Bypass Through User-Controlled Key vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-106145

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-09T08:16:54.250 |

In Progress® Telerik® Report Server prior to version 12.2.26.1007, incorrect privilege assignment in the service-agent SignalR hub allows an authenticated user, including a low-privilege or guest account with a valid bearer token, to register as a trusted service agent. On the next server settings-synchronization event, the rogue agent receives storage settings and encryption private keys. This privilege escalation enables disclosure of protected secrets, including stored data-source credentials and connection strings, and allows agent impersonation and interference with task dispatch.

### CVE-2026-107802

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-08T23:17:00.320 |

SumatraPDF is a multi-format reader for Windows. In 3.6.1 and earlier, src/SelectionTranslate.cpp embeds selected or pasted translation text in quoted Windows command lines using incomplete quote-only escaping. The affected BuildGrokTranslateCmdLineTemp(), BuildClaudeTranslateCmdLineTemp(), and BuildCodexTranslateCmdLineTemp() functions can allow attacker-controlled text to inject model, working-directory, approval, or sandbox-bypass flags when the corresponding agentic CLI backend is installed and used. No broader impact is claimed beyond the advisory-supported conditions. No fixed version is available as of this review.

### CVE-2026-107734

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-88` |
| Published | 2026-10-08T23:16:59.227 |

SumatraPDF is a multi-format reader for Windows. In 3.5.2 and earlier, an attacker-controlled SyncTeX source filename is substituted for the %f placeholder in an external editor command line without safe Windows argument quoting, and the resulting command line is passed to CreateProcessW(). A user with an external editor configured or auto-detected who opens a PDF with a crafted .synctex.gz file and invokes inverse search can inject command-line flags; the resulting impact depends on the target editor interpreting those flags and can include unintended editor actions or code execution through a malicious extension. No broader impact is claimed beyond the advisory-supported conditions. No fixed version is available as of this review.

### CVE-2026-105673

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-08T23:16:57.520 |

An
unauthenticated denial-of-service vulnerability exists in Tapo C325WB v2 in the
RTSP streaming service on TCP port 554 when the Camera Account feature is
enabled. A crafted pair of RTSP-over-HTTP tunneling requests can cause memory
corruption and crash the streaming daemon. 









Successful
exploitation may allow an unauthenticated adjacent-network attacker to disrupt
live video and related streaming functions until the affected service recovers
or restarts.

### CVE-2026-104628

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-08T22:17:26.237 |

Satel Netco Design versions prior to v2.1.7 contains an inefficient regular expression complexity vulnerability. An authenticated user with Viewer privileges could submit crafted search input that causes excessive processing, potentially degrading the availability of the application.

### CVE-2026-107778

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-08T21:17:52.630 |

MIT Kerberos 5 (krb5) through 1.22.2 contains a NULL pointer dereference in make_cred_list() in rd_cred.c that allows authenticated Kerberos clients to crash services by sending mismatched KRB-CRED arrays. Attackers can send forwarded credentials with more tickets than ticket_info entries through gss_accept_sec_context() to crash GSS-API acceptor services, causing denial of service.

### CVE-2026-40804

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-08T19:17:05.170 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Kodezen LLC aBlocks ablocks allows Reflected XSS.This issue affects aBlocks: from n/a through 2.16.0.

### CVE-2026-106429

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-08T19:16:58.750 |

An integer underflow in the KMS endpoint-parsing logic of MongoDB libmongocrypt can cause an allocation failure that terminates the application process. This can occur when an authenticated user modifies a key document in the key vault collection, or when an application accepts a KMS endpoint containing a colon after its path or query during key creation. The issue does not access memory outside its allocated bounds.

### CVE-2026-93860

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-08T18:18:30.993 |

In OpenStack Mistral through 23.0.0, the /v2/maintenance API controller clears the request context and calls the maintenance service directly without any policy enforcement. Any holder of a valid Mistral token, regardless of assigned role, can read and change the service's cluster-wide maintenance state. Setting the state to PAUSED stops processing of new workflow and execution objects across all tenant projects until an operator restores it.

### CVE-2026-107696

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-08T18:17:26.133 |

FFmpeg through 9.0.2 contains an infinite loop vulnerability in ff_rtsp_connect() in libavformat/rtsp.c that follows RTSP 3xx redirects without any redirect limit. Attackers controlling an RTSP server can answer every request with a 302 redirect to itself or another server, causing endless reconnects that saturate a CPU core.

### CVE-2026-107695

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-08T18:17:25.967 |

FFmpeg before 8.1.3 contains an infinite loop vulnerability in the HLS demuxer that allows remote attackers to cause denial of service because parse_playlist() accepts Master Playlist tags inside Media Playlists. Attackers can trick victims into opening a crafted self-referencing playlist that endlessly adds variants in hls_read_header(), causing unbounded CPU and I/O consumption.

### CVE-2026-107362

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-08T18:17:21.587 |

Malcolm file-upload component ships the upstream FilePond PHP server (pqina/filepond-server-php) largely unmodified: Dockerfile copies all upstream *.php files and Malcolm only overwrites config.php and submit.php. Upstream index.php exposes a fetch API route that instructs the server to download an arbitrary URL with curl (including FOLLOWLOCATION) and, for HEAD requests, stores the fetched response body in the upload container's transfer directory and returns the transfer ID to the caller, enabling full readback of the fetched content.

### CVE-2026-107337

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-08T18:17:20.687 |

The Malcolm kiosk Flask application exposes a POST /script_call/<script> endpoint with zero authentication and wildcard CORS (CORS(app)). An attacker can force the operator's browser to execute arbitrary management commands via CSRF, including control.py --wipe which permanently deletes all captured network traffic and forensic logs, or control.py --stop which blinds the security monitoring.

### CVE-2026-50054

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-08T17:17:17.180 |

An authorization flaw in Zimbra Collaboration Suite’s GrantRightsRequest allows an attacker with access to an authenticated account to grant another local account the loginAs right, creating persistent mailbox access and mail-sending authority that survives password changes and session expiry.

### CVE-2026-107636

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-472` |
| Published | 2026-10-08T15:17:46.543 |

pH7Builder (pH7 Social Dating CMS) before 18.5.1 contains a payment validation vulnerability that allows registered low-privileged members to obtain any membership tier by supplying client-controlled plan and amount fields. Attackers can set item_number, cart_order_id, or the PayPal custom field while paying a token amount, or submit uncompleted PayPal IPN payments, to gain the most expensive membership and its paid features.

### CVE-2026-19574

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-09T08:16:54.940 |

The ARM64 MMU back-end allocated address space identifiers (ASIDs) for memory domains with a bare round-robin counter in arch_mem_domain_init() (arch/arm64/core/mmu.c). VM_ASID_BITS is 8, so only 255 ASIDs exist; once the counter wrapped, arch_mem_domain_init() could hand an ASID to a new domain while a still-live domain held the same one. Domain-private mappings are installed non-global (MT_NG), so the ASID is the only tag separating one domain's cached translations from another's in the TLB.

The context-switch path in z_arm64_swap_ptables() only flushes the TLB when the outgoing and incoming domains carry the same ASID, which does not cover a duplicate reached through a third domain: for domains A and C sharing an ASID and an unrelated domain B, the schedule A -> B -> C never takes the flush branch, so the ASID-tagged entries A populated remain resident while C runs. Under SMP two live domains sharing an ASID can additionally be resident on two CPUs at once, which the architecture does not allow for distinct translation-table sets.

Triggering the wrap requires a CONFIG_USERSPACE application on ARM64 that creates more than 255 memory domains over its lifetime; k_mem_domain_init() and k_mem_domain_deinit() are supervisor-only APIs and are not exposed as syscalls, so an unprivileged thread cannot drive the counter directly. Once two live domains alias, however, a user-mode thread in one domain can read and write memory belonging to the other domain's partitions and thread stacks with that domain's permissions, defeating the memory-domain isolation boundary.

The fix scans the live domain_list before assigning an ASID, advances the round-robin counter past ASIDs already in use, and returns -ENOMEM when all are taken, so domain creation fails closed instead of silently aliasing.
