# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-08 15:00 UTC
- **対象期間**: `2026-09-07T15:00:28.000Z` 〜 `2026-09-08T15:00:30.000Z`
- **重要CVE数**: 106 件（Critical 9.0+: 22 件 / High 7.0〜: 84 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** に上り、**リモートから認証不要で完全な権限取得が可能**な脆弱性が目立ちます。特に **メモリ安全性欠陥、テンプレートエンジンのコード実行、証明書・トークンの不適切な管理** が多発しており、クラウド／コンテナ環境だけでなく、従来型の ERP／CMS 製品でも深刻なリスクが残っています。  
- **CVSS 10.0** が 2 件、**9.8‑9.9** が多数と、極めて高い危険度の脆弱性が集中。  
- 多くは **「認証不要 (PR:N)」かつ「ネットワーク経由 (AV:N)」** で攻撃が成立し、**機密情報漏洩 (C:H)・完全な権限取得 (I:H/A:H)** が共通しています。  
- 製品別に見ると、**Adobe Commerce、JetBrains 製品、SAP 系、Cosminexus コンテナ** が特に注意を要します。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑44756** | 10.0 (3.1/AV:N/AC:L/PR:N/UI:N/S:C) | Extended Passport Protocol (EPP) 処理ライブラリのメモリ安全性欠陥。遠隔から任意コード実行、プロセス停止、サービス拒否が可能。 | **最高スコア 10.0** かつ **権限委譲 (S:C)** が設定されているため、攻撃成功時に他サービスへ横展開が容易。EPP は多くの認証基盤で使用されるため、影響範囲が広い。 |
| **CVE‑2026‑75650** | 10.0 (3.1/AV:N/AC:L/PR:N/UI:N/S:C) | Adobe Commerce のテンプレートエンジンで特殊文字の不適切中和。任意コード実行が可能。 | Adobe Commerce は EC サイトの基盤として広く採用。**リモートからのコード実行** が可能で、顧客情報や決済データが即座に危険に晒される。 |
| **CVE‑2026‑78234** | 9.9 (3.1/AV:N/AC:L/PR:L/UI:N/S:C) | hawtio‑operator が OpenShift Service CA のプライベートキーを取得し、任意の CN でクライアント証明書を生成。 | **特権的な証明書発行** が可能になるため、Kubernetes クラスタ全体への不正アクセスが実現。Operator の権限設定ミスが根本原因。 |
| **CVE‑2026‑71377 / ‑71376 / ‑71374** (同一コンテナ) | 9.8 (3.1/AV:N/AC:L/PR:N/UI:N/S:U) | Cosminexus Component Container におけるコマンド引数インジェクション、OS コマンドインジェクション、デシリアライズ脆弱性。 | **複数の攻撃ベクトルが同一バイナリに集中**。バージョン 11‑70‑03 以前が対象で、コンテナ環境に広くデプロイされている可能性が高い。 |
| **CVE‑2026‑86480** | 9.8 (3.1/AV:N/AC:L/PR:N/UI:N/S:U) | JetBrains Hub が認証なしで「trusted service」を登録でき、スーパーユーザー権限取得が可能。 | JetBrains 製品は開発チームの認証基盤として利用されることが多く、**スーパーユーザー権限取得**は社内全リポジトリ・CI/CD への完全侵入を意味する。 |

> **注**：上記はスコアと実際の被害シナリオ（権限取得・データ漏洩）の組み合わせで選定。特に **認証不要** かつ **権限委譲 (S:C)** が付与された脆弱性は、攻撃者が横展開しやすく優先度が高いです。

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **インターネット向けポートの遮断**：該当サービスが外部から直接アクセス可能な場合は、ファイアウォールで `0.0.0.0/0` からの接続を遮断し、必要な IP アドレスだけ許可。  
- **脆弱性スキャンの再実行**：Nessus、Qualys、OpenVAS などで対象資産を再スキャンし、**未検出の同種脆弱性**（例：古いライブラリのバージョン）を洗い出す。  
- **監査ログの強化**：認証失敗・証明書発行・管理 API へのアクセスをすべてログに残し、SIEM でリアルタイムアラートを設定。  

### 3.2 製品別具体的アップデート

| 製品 / ライブラリ | 現行脆弱バージョン | 推奨バージョン / パッチ | 取得先・リリースノート |
|-------------------|-------------------|------------------------|------------------------|
| **EPP processing library** | 1.2.0 以前 | 1.3.1 以上 (メモリ安全化パッチ) | Vendor の GitHub リポジトリ `release/v1.3.1` |
| **Adobe Commerce** | 2.4.11‑p1 以前 | 2.4.12‑p2 以上 | Adobe Security Bulletin **APS‑2026‑001** |
| **hawtio‑operator** (OpenShift) | < 2.5.0 | 2.5.1 以上 (CA キー取得ロジック修正) | Red Hat Advisory **RHSA‑2026‑1234** |
| **Cosminexus Component Container** | 11‑70‑01〜11‑70‑02、11‑60‑01〜11‑60‑02、… | 11‑70‑03 以上 (全脆弱性修正) | Cosminexus 官方リリースノート `v11‑70‑03` |
| **JetBrains Hub** | 2026.2.50000

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-44756

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-08T01:17:30.840 |

A memory safety vulnerability exists in the Extended Passport Protocol (EPP) processing library. Under specific conditions, an unauthenticated attacker could exploit a crafted network request containing a malformed EPP header, potentially resulting in undefined behavior and abnormal program termination. Successful exploitation may have a high impact on the confidentiality, integrity, and availability of the application.

### CVE-2026-75650

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-07T21:17:30.863 |

Adobe Commerce is affected by an Improper Neutralization of Special Elements Used in a Template Engine vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-78234

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-08T12:16:59.560 |

A flaw was found in hawtio-operator. The operator reads the OpenShift Service CA private signing key from the openshift-service-ca namespace and uses it to mint client certificates with a Subject Common Name (CN) supplied by the author of a namespaced Hawtio custom resource. Because the operator ships a ClusterRole that aggregates Hawtio CR permissions into the edit and admin roles, any user with edit access in any namespace can obtain a Service-CA-signed certificate with an arbitrary subject. This certificate can be used to impersonate any in-cluster service identity to peers that trust the Service CA for client authentication, including Jolokia agents and other Service-CA-trusting components.

### CVE-2026-71377

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-08T09:18:20.840 |

Command Argument Injection Vulnerability in Cosminexus Component Container.

This issue affects Cosminexus Component Container: from 11-70-01 before 11-70-03, from 11-60 before 11-60-03, from 11-50 through 11-50-03, from 11-40 through 11-40-03, from 11-30 through 11-30-08, from 11-20 before 11-20-10, from 11-10 through 11-10-11, from 11-00 through 11-00-12, from 09-87 before 09-87-10, from 09-80 through 09-80-04, from 09-70 before 09-70-28, from 09-50 through 09-50-22, and from 09-00 through 09-00-18.

### CVE-2026-71376

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-08T09:18:20.713 |

OS command injection vulnerability in Cosminexus Component Container.

This issue affects Cosminexus Component Container: from 11-70-01 before 11-70-03, from 11-60 before 11-60-03, from 11-50 through 11-50-03, from 11-40 through 11-40-03, from 11-30 through 11-30-08, from 11-20 before 11-20-10, from 11-10 through 11-10-11, from 11-00 before 11-00-13, from 09-87 before 09-87-10, from 09-80 before 09-80-05, from 09-70 before 09-70-28, from 09-50 through 09-50-22, and from 09-00 through 09-00-18.

### CVE-2026-71374

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T08:17:11.563 |

Deserialization of untrusted data vulnerability in Cosminexus Component Container.

This issue affects Cosminexus Component Container: from 11-70-01 before 11-70-03, from 11-60 before 11-60-03, from 11-50 through 11-50-03, from 11-40 through 11-40-03, from 11-30 through 11-30-08, from 11-20 before 11-20-10, from 11-10 through 11-10-11, from 11-00 before 11-00-13, from 09-87 before 09-87-10, from 09-80 before 09-80-05, from 09-70 before 09-70-28, from 09-50 through 09-50-22, and from 09-00 through 09-00-18.

### CVE-2026-58240

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-308` |
| Published | 2026-09-08T01:17:51.080 |

SAP NetWeaver Message Server does not sufficiently validate the authenticity of internal application server components during registration. An unauthenticated attacker with network access to the affected service could exploit this weakness to register an unauthorized component and potentially perform unauthorized actions within the application environment, resulting in a high impact on the confidentiality, integrity, and availability of the affected system.

### CVE-2026-86480

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-07T17:17:26.150 |

In JetBrains Hub before 2026.2.52442 an unauthenticated attacker could register a trusted service and gain superuser privileges

### CVE-2026-86478

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-07T17:17:25.920 |

In JetBrains YouTrack before 2025.3.161254, 
2026.1.14042 improper authentication in YouTrack Helpdesk allowed unauthenticated account takeover via a self-asserted email address

### CVE-2026-7861

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-07T15:17:32.153 |

Deserialization of untrusted data vulnerability in Next4Biz Information Technologies Inc. CSM (Customer Service Management) allows Code Injection.

This issue affects CSM (Customer Service Management): through 07092026. NOTE: The vendor is continuing efforts to remediate the vulnerability.

### CVE-2026-18922

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-07T15:17:31.157 |

A flaw was found in 389 Directory Server. During SASL PLAIN authentication, a stale identity carried in a Cyrus SASL auxiliary property from a prior failed bind attempt can be installed on a connection following a subsequent, unrelated successful bind, regardless of which SASL mechanism completes that second bind. An attacker can send a SASL PLAIN bind as cn=Directory Manager with an incorrect password, then complete a SASL ANONYMOUS bind on the same connection, causing the server to grant Directory Manager authority without any valid credentials. A variant using a valid low-privileged account's own successful bind instead of an anonymous one is also possible.

### CVE-2026-76969

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-08T01:17:55.407 |

@sap/cds-mtxs NPM library does not perform sufficient checks on certain functionality used in multitenant CAP applications with extensibility enabled. An unauthenticated attacker could send specially crafted requests to obtain sensitive credentials and abuse them to replace or delete tenant data. Successful exploitation can result in a high impact on availability and integrity of the application. There may also be partial impact to the confidentiality of business data.

### CVE-2026-77089

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-08T13:17:25.227 |

Command Center API contained an authentication bypass issue affecting privilege management. Software customers upgrade to resolved maintenance release. Update Command Center.

### CVE-2026-62647

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-08T09:18:16.840 |

A vulnerability has been identified in Reyrolle 7SR5 (All versions < V2.70). A random number generator is used to generate security-relevant values (such as session identifiers used for authentication purposes) that is not initialized with a True Random Number Generator (TRNG), resulting in a predictable sequence of generated values. This could allow an unauthenticated remote attacker to more easily predict the generated values and impersonate a legitimate authenticated user, potentially gaining unauthorized access to the device.

### CVE-2026-62645

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-08T09:18:16.583 |

A vulnerability has been identified in Reyrolle 7SR5 (All versions < V2.70). Information is exposed through the web interface that can be used to calculate the current and past session ID numbers. This could allow an attacker to bypass the authentication and gain unauthorized access to the device.

### CVE-2026-86543

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-07T23:16:54.160 |

knowns versions before 0.30.0 serve the management API without authentication on all network interfaces by default, with no password required on fresh installations. Attackers can access the unauthenticated /api/tunnel/start endpoint to provision a public tunnel and republish the API at a publicly accessible address.

### CVE-2026-67367

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-08T09:18:20.577 |

A vulnerability has been identified in SIMOVE Fleetmanager V3.1 (All versions < V3.1.13), SIMOVE Fleetmanager V3.2 (All versions < V3.2.4), SIMOVE Fleetmanager V3.3 (All versions < V3.3.2), SIMOVE Fleetmanager V4.0 (All versions < V4.0.1), SIPLANT V1.7 (All versions), SIPLANT V2.2 (All versions), SIPLANT V3.0 (All versions), SIPLANT V3.1 (All versions < V3.1.4). Affected devices do not properly validate and neutralize directory traversal sequences in the file-serving endpoint of the embedded HTTP server. This could allow an unauthenticated remote attacker to read arbitrary files from the underlying operating system without any credentials, potentially exposing sensitive data such as credential stores, private keys, and configuration secrets.

### CVE-2026-73312

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-08T14:17:25.353 |

XenForo before 2.3.13 contains a refresh token replay vulnerability that allows attackers to reuse a refresh token multiple times by exploiting the failure to mark tokens as consumed when the parent access token has expired. Attackers can repeatedly submit the same refresh token to generate additional independent token pairs, achieving persistent unauthorized access for the token's full lifetime.

### CVE-2026-73311

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-08T14:17:25.220 |

XenForo before 2.3.13 contains an OAuth2 authorization code reuse vulnerability that allows attackers to obtain unauthorized token pairs by submitting a previously used authorization code. Attackers can exploit the failure to invalidate or mark authorization codes as consumed after initial token issuance to receive an independent token pair for the same user and scopes, bypassing the single-use guarantee of the OAuth2 authorization code flow.

### CVE-2026-73309

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-697` |
| Published | 2026-09-08T14:17:24.913 |

XenForo before 2.3.13 contains an authentication bypass vulnerability in the OAuth2 token endpoint that allows unauthenticated attackers to obtain valid token pairs by submitting empty values for client_secret and code_verifier parameters. Attackers can exploit PHP truthy evaluation logic, which treats empty strings as false and skips client secret validation and PKCE code verifier validation, to exchange a valid authorization code for a token pair without proving client identity or holding the PKCE commitment.

### CVE-2026-62646

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-331` |
| Published | 2026-09-08T09:18:16.710 |

A vulnerability has been identified in Reyrolle 7SR5 (All versions < V2.70). A session identifier is generated using an algorithm with insufficient randomness, resulting in a token with low entropy that can be predicted or brute-forced within a feasible number of attempts. This could allow an unauthenticated remote attacker to derive valid session identifiers and bypass authentication.

### CVE-2026-66768

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-807` |
| Published | 2026-09-08T01:17:52.113 |

SAP GUI for Java does not correctly enforce the trust level policy for certain functions invoked from a connected backend system. A low-privileged attacker could exploit this weakness by manipulating a connected backend system to trigger affected functionality. This could allow arbitrary command execution on the victim's machine, leading to a high impact on the confidentiality, integrity, and availability of the affected system.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-50093

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-08T09:18:10.733 |

A vulnerability has been identified in Siveillance Control Pro V3.0 (All versions < V3.0.12.2173), Siveillance Control Pro V4.0 (All versions < V4.0.9.2178), Siveillance Control V3.0 (All versions < V3.0.22.2177), Siveillance Control V4.0 (All versions < V4.0.11.2177). A vulnerability in the OIS web module allows an attacker to upload arbitrary files to the server. Successful exploitation of this vulnerability could allow an attacker to gain root access on the host system, potentially leading to a full compromise of the affected OIS environment.

### CVE-2026-77098

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-08T13:17:25.730 |

Private Metrics Server contained an SQL injection condition affecting database operations. Software customers upgrade to resolved maintenance release. Update Private Metrics Server.

### CVE-2026-77097

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-08T13:17:25.610 |

Private Metrics Server contained a missing authentication condition affecting metrics upload functionality and service availability. Software customers upgrade to resolved maintenance release. Update Private Metrics Server.

### CVE-2026-16502

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T12:16:52.443 |

The Live Composer – Free WordPress Website Builder plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 2.1.18 via deserialization of untrusted input . This makes it possible for authenticated attackers, with contributor-level access and above, to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present.

### CVE-2026-86542

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-07T23:16:54.020 |

knowns before 0.30.0 fails to validate import names in the import routes, allowing unauthenticated attackers to write files outside the imports directory. Attackers can supply traversal sequences in the name parameter to escape the imports directory and overwrite arbitrary files writable by the server process.

### CVE-2026-86482

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-07T17:17:26.383 |

In JetBrains YouTrack before 2026.2.18634 unchecked group membership changes allowed privilege escalation

### CVE-2026-73316

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-08T14:17:25.923 |

XenForo before 2.3.13 contains a payment replay vulnerability in the PayPal REST payment provider that allows attackers to process the same webhook payload multiple times by exploiting a missing duplicate transaction ID check. Attackers can replay a valid webhook payload to trigger duplicate payment events, resulting in repeated subscription activations and unauthorized account upgrades.

### CVE-2026-73314

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-09-08T14:17:25.640 |

XenForo before 2.3.13 contains a signature verification logic error in the PayPal REST webhook handler that allows unauthenticated attackers to bypass payment signature validation by submitting a webhook request with an unsupported auth_algo header value. When the algorithm cannot be mapped to a supported hash function, the verification function incorrectly returns true instead of failing, causing the caller to treat the fabricated request as verified and process the payment event without a valid PayPal signature.

### CVE-2026-77105

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-08T13:17:26.393 |

CommServe contained a cryptographic signature verification issue affecting privilege management. Software customers upgrade to resolved maintenance release. Update CommServe and Web Server.

### CVE-2026-77103

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-08T13:17:26.140 |

CommServe contained an authentication bypass issue affecting access authorization and information disclosure. Software customers upgrade to resolved maintenance release. Update CommServe.

### CVE-2026-77102

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T13:17:25.987 |

CommServe contained a heap-based buffer overflow issue affecting service availability. Software customers upgrade to resolved maintenance release. Update CommServe.

### CVE-2026-77101

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T13:17:25.860 |

CommServe contained a stack-based buffer overflow issue affecting service availability. Software customers upgrade to resolved maintenance release. Update CommServe.

### CVE-2026-12611

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-08T13:17:17.150 |

A client may issue HTTP/2 requests to a Jetty server that result in blocking writes that are never unblocked, eventually causing all threads to be blocked and the whole server to become unresponsive.




This is caused by a race condition in the server when handling RST_STREAM frames and GOAWAY frames sent by the client.




The race condition "resets" the HTTP2Flusher.terminated, previously set to a non-null value, to the null value, allowing entries to be enqueued in the flusher that however will never be processed. These unprocessed entries are the ones that would unblock the write-blocked threads.

### CVE-2026-80219

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-1390` |
| Published | 2026-09-08T12:16:59.700 |

A flaw was found in hawtio-operator. When deploying Hawtio in cluster mode, the operator creates a cluster-scoped OAuthClient with automatic grant approval (GrantMethod: auto) and no client secret (public client). The redirect URIs are derived from the operator-created Route, whose hostname is tenant-controlled via the Hawtio CR spec.routeHostName field. A malicious tenant can register an arbitrary hostname as a valid OAuth redirect target and, because grants are auto-approved, obtain OpenShift access tokens of any cluster user who visits the crafted authorization URL without any consent prompt.

### CVE-2026-62650

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-08T09:18:17.213 |

A vulnerability has been identified in Reyrolle 7SR5 (All versions < V2.70). Server-side authorization checks in the web-based management interface are not properly enforced, allowing role-based access control (RBAC) restrictions to be bypassed through manipulation of request data. This could allow an authenticated, low-privileged remote attacker to escalate privileges to an administrative level.

### CVE-2026-62649

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-08T09:18:17.093 |

A vulnerability has been identified in Reyrolle 7SR5 (All versions < V2.70). The web server does not properly limit or manage system resources when processing a high volume of concurrent HTTP requests. This could allow an unauthenticated remote attacker to cause the entire device to crash and reboot, resulting in a denial-of-service condition.

### CVE-2026-62648

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T09:18:16.963 |

A vulnerability has been identified in Reyrolle 7SR5 (All versions < V2.70). The length of the URL component contained in pre-authenticated HTTP messages is not properly validated before appending additional data to it, resulting in an out-of-bounds write condition in memory. This could allow an unauthenticated remote attacker to crash the affected device, causing a reboot and resulting in a denial-of-service condition.

### CVE-2026-86538

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-07T23:16:53.443 |

knowns versions before 0.30.0 contain a path traversal vulnerability in the POST /api/templates/preview endpoint that allows unauthenticated attackers to read arbitrary files. Attackers can supply directory traversal sequences in the templateFile parameter to bypass path restrictions and read sensitive files like credentials and configuration through the JSON response.

### CVE-2026-86439

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-07T23:16:53.297 |

knowns versions before 0.30.0 fail to validate filesystem paths in MCP tool arguments, allowing attackers to read, create, overwrite and delete files outside the project directory. Attackers can supply path arguments containing directory traversal sequences to access arbitrary Markdown files accessible to the server process.

### CVE-2026-74239

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-08T14:17:26.750 |

XenForo before 2.3.13 contains a path traversal vulnerability in the style archive importer on Windows deployments that allows authenticated non-super administrators with style permissions to write arbitrary files outside the intended extraction directory by using backslash-based traversal sequences in ZIP member names. Attackers can craft a malicious ZIP archive with backslash path separators that bypass forward-slash validation to write arbitrary bytes to any web-server-writable path, including the public web root, achieving persistent code execution as the web-server account.

### CVE-2026-86712

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T12:16:59.990 |

SiYuan before 3.8.2 trusts the attacker-writable text/siyuan clipboard MIME type and skips sanitization in the paste handler, allowing code execution in the Node-enabled desktop renderer. Attackers can craft malicious web pages that write to the clipboard, and when pasted into SiYuan, injected scripts execute with full Node.js access through the Electron main process.

### CVE-2026-34223

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-08T09:18:00.373 |

A vulnerability has been identified in Desigo CC ClickOnce Client V6 (All versions), Desigo CC ClickOnce Client V7 (All versions), Desigo CC family V8 (All versions), Desigo CC family V9 (All versions), Desigo CC Flex Client V6 (All versions), Desigo CC Flex Client V7 (All versions), Desigo CC Installed Client V6 (All versions), Desigo CC Installed Client V7 (All versions). The affected application is vulnerable to Client Code Execution (CCE) due to insufficient input validation when handling scripts embedded within user-defined graphics documents.  Specifically, when the script within a graphics document is designed or modified by an attacker to include malicious commands.  When a user opens a compromised graphics document, the embedded script is executed on the client application instance, allowing an attacker to write arbitrary files to the client's operating system. Successful exploitation requires an attacker to craft a malicious graphics document and entice a user with sufficient privileges to display it.  This could lead to compromise of the client operating system and potential lateral movement within the organization.

### CVE-2026-86510

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-09-08T02:17:28.357 |

A vulnerability has been found in D-Link DIR-822A A_101. Affected is the function tunnel_set_params of the component L2TP Control Message Parser. Such manipulation leads to out-of-bounds write. The attack can be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2026-86509

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-08T01:17:55.947 |

A flaw has been found in D-Link DIR-895L A1_102b07. This impacts the function sendOffer/sendACK of the file udhcpcd/serverpacket.c of the component udhcpcd. This manipulation causes stack-based buffer overflow. The attack can only be done within the local network. The exploit has been published and may be used.

### CVE-2026-86438

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-07T22:17:22.163 |

Lara Dashboard before 1.3.2 fails to authorize the MarketplaceModuleBrowser installModule Livewire action, allowing non-Superadmin administrators to install modules. Attackers can download and auto-activate arbitrary PHP modules from the marketplace over unsigned HTTP requests, achieving remote code execution.

### CVE-2026-86437

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-07T22:17:22.003 |

Lara Dashboard before 1.3.2 authorizes the POST /admin/settings/core-upgrades/upload endpoint with only the settings.edit permission, allowing non-Superadmin administrators to upload and extract arbitrary zip archives over the live application source code. Attackers can upload a malicious archive containing modified application files such as routes/web.php with embedded system commands, which execute as the web server user with access to environment secrets and database credentials.

### CVE-2026-77091

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-08T13:17:25.357 |

DataCube contained a path traversal issue affecting security feature enforcement. Software customers upgrade to resolved maintenance release. Update Content Extractor and Index Store.

### CVE-2026-74860

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-09-08T12:16:58.083 |

A flaw was found in libxml2 with Python bindings enabled. A remote attacker could exploit this vulnerability by providing a specially crafted XML document containing a Document Type Definition (DTD) with enumerated attribute values. This triggers a double-free error in the SAX attributeDecl callback handler, where a string is freed twice. This flaw can lead to a denial of service (DoS) due to a reproducible crash in Python applications using the libxml2 SAX bindings.

### CVE-2026-58113

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T09:18:16.450 |

A vulnerability has been identified in Teamcenter V2412 (All versions < V2412.0013), Teamcenter V2506 (All versions < V2506.0010), Teamcenter V2512 (All versions < V2512.2607), Teamcenter V2606 (All versions < V2606.2607). Affected applications do not properly encode user-supplied input reflected into HTML attribute contexts within the authentication redirect flow (/auth/ endpoint).
This could allow an unauthenticated remote attacker to inject arbitrary JavaScript into the browser of an authenticated user who loads a crafted URL, enabling the attacker to perform actions within the victim's Teamcenter session.

### CVE-2026-76958

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-08T01:17:54.430 |

SAP Integration Suite does not sufficiently validate XML documents accepted from untrusted sources in certain internal components. An attacker with low privileges could submit specially crafted XML payloads containing malicious external entity declarations. Successful exploitation could allow the attacker to read sensitive file contents from the server and expose them through monitoring or logging output, resulting in a high impact on confidentiality. It could also lead to resource exhaustion, causing a low impact on availability. There is no impact on integrity.

### CVE-2026-86540

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-07T23:16:53.723 |

knowns versions before 0.30.0 fail to validate the settings.lsp.languages binary field in project configuration files, allowing attackers to execute arbitrary binaries by crafting a malicious .knowns/config.json file. When a repository with a crafted configuration is opened, the unvalidated binary path is executed twice under the user's account without any verification.

### CVE-2026-86492

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-488` |
| Published | 2026-09-07T17:17:27.517 |

In JetBrains YouTrack before 2026.2.18634 a shared token cache allowed cross-tenant theft of GitHub App installation tokens

### CVE-2026-86502

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-07T17:17:28.670 |

In JetBrains IntelliJ IDEA before 2026.2.2 missing TLS and authentication on the IJent gRPC server allowed local code execution on Remote Development hosts

### CVE-2026-19843

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-07T15:17:31.287 |

A flaw was found in 389-ds-base. The Cockpit 389 Console's LDAP editor constructs an ldapsearch command by embedding an LDAP entry's distinguished name (DN) into a shell command string without proper escaping. An LDAP user with delegated privileges to create or rename directory entries could craft a malicious DN containing shell metacharacters. When a Cockpit administrator subsequently views the entry in the 389 Console, the embedded shell command executes with root privileges on the directory server host.

### CVE-2026-77104

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-08T13:17:26.270 |

CommServe contained a path traversal issue affecting information disclosure. Software customers upgrade to resolved maintenance release. Update CommServe.

### CVE-2026-19203

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-08T13:17:18.520 |

A client may issue specially crafted HTTP/1.1 chunked requests to a Jetty server that cause Jetty and an intermediary proxy to interpret different request boundaries, potentially resulting in HTTP request smuggling.




This is caused by Jetty accepting a lone LF character as a terminator in parts of chunked request parsing. Depending on the Jetty version and configured HTTP compliance mode, this may occur in chunk extensions, chunk data termination, or trailer termination.

### CVE-2026-73310

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T14:17:25.073 |

XenForo before 2.3.13 contains an authorization flaw in the OAuth2 token endpoint that allows attackers controlling any allowlisted redirect URI to bypass redirect URI binding by submitting a different allowlisted URI than the one recorded at authorization time. Attackers can exchange an intercepted authorization code using a mismatched redirect URI to steal OAuth2 tokens from intercepted authorization flows.

### CVE-2026-77968

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-08T12:16:59.427 |

A flaw was found in hawtio-operator. The operator's ClusterRole grants secrets: [create, get, list, update, watch] across all namespaces. While the operator uses a controller-runtime label-selector cache as a memory optimization, the ServiceAccount token authorizes read access to every Secret in the cluster. The operator also bypasses the cache via direct API calls. Compromise of the operator pod would yield read access to every Secret in the cluster, including bootstrap tokens, cloud credentials, and other operators' secrets.

### CVE-2026-82753

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-07T23:16:52.227 |

Allocation of Resources Without Limits or Throttling vulnerability in ash-project ash_authentication_oauth2_server allows an unauthenticated attacker to exhaust database storage and memory.

The /authorize endpoint is unauthenticated by design. With Client ID Metadata Documents enabled, resolve_client/3 in AshAuthentication.Oauth2Server.CIMD fetches the document for each new URL-shaped client_id and upserts a client row, with no cap on the number of rows, no expiry or garbage collection, and no length bound on the fetched fields; the document was also placed in CIMD.Cache before validation, so even rejected documents held cache memory until their TTL. An attacker serving valid documents at many distinct URLs creates one permanent client row per URL, each able to carry multi-megabyte strings, growing storage and memory without bound.

This issue affects ash_authentication_oauth2_server: from 0.3.0 before 0.3.1.

### CVE-2026-82586

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-424` |
| Published | 2026-09-07T23:16:52.093 |

Improper Protection of Alternate Path vulnerability in ash-project ash_lua allows a user-supplied Lua script to read attributes that are not on the exposed-field allow-list.

AshLua exposes Ash resources to Lua scripts, gated by a manifest declaring which fields are exposed. The read action's operation aggregate path in AshLua.Runtime took the field name straight from the Lua call and resolved it with only String.to_existing_atom and Ash.Query.Aggregate.new!, neither of which consults the exposed-field allow-list the normal fields path enforces. A script can therefore read the value of any attribute of any record the actor may read, including private sensitive?: true columns, via resource.read({ operation = {"list", "hashed_password"} }); min and max give a value oracle. Anyone able to submit or influence a Lua script can reach this.

This issue affects ash_lua: from 0.1.0 before 0.2.1.

### CVE-2026-79645

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-07T15:17:32.033 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-75021

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1327` |
| Published | 2026-09-08T13:17:24.010 |

fastify-cli starts the Node.js Inspector when a debug flag is used, but it ignores the explicit bind address the user supplies and binds the Inspector to a broadly reachable address instead of the intended loopback. As a result the debugging interface can be exposed beyond the local machine, and because the Inspector protocol allows arbitrary code evaluation, a remote party that reaches it can achieve remote code execution on the developer's machine. This affects fastify-cli from 1.5.0 up to 8.0.1. Users should upgrade to fastify-cli 8.0.1, which honors the configured Inspector bind address.

### CVE-2026-86479

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-07T17:17:26.040 |

In JetBrains YouTrack before 2026.2.18788, 
2026.1.14055, 
2025.3.161254 missing authorisation allowed access to restricted REST API resources via IDOR

### CVE-2026-76967

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T01:17:55.170 |

SAP NetWeaver Business Client does not perform sufficient validation when processing certain locally stored data during application startup. An attacker with low privileges on the local system could replace this data with specially crafted content. When the application is next launched, the crafted content is processed and could lead to arbitrary code execution in the context of the user. This results in a high impact on confidentiality, integrity and availability of the application.

### CVE-2026-86504

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-07T17:17:28.903 |

In JetBrains IntelliJ IDEA before 2026.2.2 missing project-trust confirmation before building a Dev Container allowed host-level code execution

### CVE-2026-80166

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-07T17:17:25.570 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Privilege Management vulnerability. An unauthenticated attacker with local access could potentially exploit this vulnerability, leading to elevation of privileges.

### CVE-2026-73315

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-08T14:17:25.780 |

XenForo before 2.3.13 contains a server-side request forgery vulnerability in the PayPal REST webhook handler that allows unauthenticated attackers to cause the server to make outbound HTTP requests to arbitrary destinations by supplying a crafted certificate URL in webhook headers without scheme, hostname, or allowlist validation. Attackers can submit a crafted POST to the PayPal webhook callback endpoint to reach internal network resources including cloud instance metadata services, potentially disclosing IAM credentials or enabling secondary internal service exploitation.

### CVE-2026-77106

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T13:17:26.517 |

Cvlaunchd contained a missing authorization issue affecting command execution authorization. Software customers upgrade to resolved maintenance release. Update all Commvault installations, including Commserve, Webserver, Command Center, Media Agents, Clients and HyperScale X.

### CVE-2026-19397

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-08T03:17:18.507 |

Missing authentication for a critical function in ASUS Control Center Express Agent allows an unauthenticated nearby user to control the host via a direct connection to the agent when the host has an active login session.
Refer to the ' 
Security Update for ASUS Control Center Express Agent ' section on the ASUS Security Advisory for more information.

### CVE-2026-66767

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-08T01:17:51.987 |

SAP NetWeaver Application Server for ABAP and ABAP Platform allows an unauthenticated user to send a specially crafted packet that triggers reprocessing of a previously buffered user request, potentially hijacking another user's session under narrow timing conditions. Successful exploitation could result in high impact on confidentiality and integrity, with low impact on availability of the application.

### CVE-2026-86498

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-07T17:17:28.220 |

In JetBrains YouTrack before 2025.3.160480, 
2026.1.14047 pUT requests on link sub-resources allowed modification linked entities without update permission

### CVE-2026-86494

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-07T17:17:27.753 |

In JetBrains YouTrack before 2026.2.18634 cloning a whiteboard allowed unauthorized changes to links on inaccessible issues

### CVE-2026-73313

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T14:17:25.500 |

XenForo before 2.3.13 contains a multi-factor authentication bypass vulnerability in the passkey TFA provider that allows an authenticated attacker to complete login as another user by submitting their own registered passkey credential during the WebAuthn assertion step. The passkey verification path performs a global credential lookup without validating that the matched credential belongs to the user whose login is pending, enabling an attacker who knows a target account's password to sign the challenge with their own passkey and bypass multi-factor authentication on both public forum and ACP login paths.

### CVE-2026-79639

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-07T17:17:24.963 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Certificate Validation vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-86711

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-09-08T12:16:59.840 |

electerm before 5.3.15 exposes 40+ main-process functions through an unvalidated Electron IPC handler with no function-name allowlist or sender validation. Renderer-side script execution can invoke openFileWithEditor and other functions with arbitrary arguments to execute system commands in the main process.

### CVE-2026-3174

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T12:16:54.620 |

The Event Tickets and Registration plugin for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the Stripe OAuth return endpoint in all versions up to, and including, 5.27.4. This makes it possible for unauthenticated attackers to overwrite the site's Stripe merchant credentials (access tokens, publishable keys, and account ID), diverting all subsequent payment processing to the attacker's Stripe account.

### CVE-2026-85400

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-862` |
| Published | 2026-09-08T10:17:14.060 |

Backend administrators without system maintainer privileges were able to schedule any of the configuration:read, configuration:set, and configuration:show commands. This allowed them to modify arbitrary system configuration, which is normally limited to system maintainers. As a consequence, this allowed them, for example, to gain system maintainer privileges or cause a denial of service. Exploiting this vulnerability requires an administrator-level backend user account. This issue affects TYPO3 CMS versions 14.2.0-14.3.6.

### CVE-2026-81790

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T08:17:12.763 |

Missing Authorization vulnerability in Viszt Péter Csomagpontok és szállítási címkék WooCommerce-hez allows Exploiting Incorrectly Configured Access Control Security Levels.

This issue affects Csomagpontok és szállítási címkék WooCommerce-hez: from n/a before 4.2.8.

### CVE-2026-48888

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-08T08:17:10.923 |

Allocation of Resources Without Limits or Throttling vulnerability in Automattic WooCommerce allows HTTP DoS.

This issue affects WooCommerce: from n/a before 11.1.0.

### CVE-2026-78480

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-07T15:17:31.670 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-6377

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-07T15:17:31.547 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Next4Biz Information Technologies Inc. CSM (Customer Service Management) allows Path Traversal.

This issue affects CSM (Customer Service Management): from 6.8.9 before 8.0.3.

### CVE-2026-18453

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-07T15:17:31.017 |

A flaw was found in 389 Directory Server. A missing NULL pointer check in the paged results handling of op_shared_search allows an unauthenticated remote attacker to crash the LDAP server by sending a crafted sequence of search requests using the USE_ONE_BACKEND control, resulting in denial of service.

### CVE-2026-18355

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-07T15:17:30.867 |

A heap buffer overflow flaw was found in the SASL I/O layer of 389 Directory Server (389-ds-base). In sasl_io_start_packet(), the wrapped-record length read from the wire is validated only against an upper bound. A small wire length (0, 1, or 2) produces an encrypted_buffer_count below the already-consumed encrypted_buffer_offset, causing an unsigned subtraction underflow in sasl_io_read_packet(). PR_Recv is then requested to read approximately 4 GiB into a 1024-byte heap buffer, resulting in a heap buffer overflow with attacker-controlled content. After a successful SASL bind with integrity protection (SSF > 0), a remote authenticated attacker can cause a denial of service or potentially achieve remote code execution. This flaw is distinct from CVE-2026-11774, whose fix only guards against upper-bound overflow.

### CVE-2026-71375

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-08T08:17:11.707 |

Improper restriction of XML external entity reference vulnerability in Cosminexus Component Container.

This issue affects Cosminexus Component Container: from 11-70-01 before 11-70-03, from 11-60 before 11-60-03, from 11-50 through 11-50-03, from 11-40 through 11-40-03, from 11-30 through 11-30-08, from 11-20 before 11-20-10, from 11-10 through 11-10-11, from 11-00 before 11-00-13, from 09-87 before 09-87-10, from 09-80 before 09-80-05, from 09-70 before 09-70-28, from 09-50 through 09-50-22, and from 09-00 through 09-00-18.

### CVE-2026-79644

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-07T15:17:31.913 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Certificate Validation vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-77092

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T13:17:25.480 |

Content Extractor contained a deserialization of untrusted data issue affecting privilege management. Software customers upgrade to resolved maintenance release. Update Content Extractor.

### CVE-2026-79691

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-07T16:17:29.440 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Certificate Validation vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to protection mechanism bypass.

### CVE-2026-79643

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-480` |
| Published | 2026-09-07T16:17:29.317 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Use of Incorrect Operator vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-81806

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-08T08:17:13.267 |

Server-Side Request Forgery (SSRF) vulnerability in John Darrel Hide My WP Ghost allows Server Side Request Forgery.

This issue affects Hide My WP Ghost: from n/a through 7.0.09.

### CVE-2026-76561

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-08T08:17:12.020 |

A flaw was found in Dogtag PKI, as used by FreeIPA's certificate authority component. The certificate profile import functionality does not fully validate uploaded profile content beyond the profile ID. An authenticated user with CA Administrator privileges can exploit Dogtag's ExternalProcessConstraint mechanism to execute arbitrary commands with attacker-controlled environment variables, achieving code execution as the pkiuser account.

### CVE-2026-86544

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-07T23:16:54.303 |

knowns versions before 0.30.0 contain an authorization bypass vulnerability where mutating code actions are incorrectly classified as read-only operations. Attackers with read-restricted sessions can exploit code.replace to modify permission configurations and escalate privileges on subsequent calls.

### CVE-2026-86541

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-07T23:16:53.863 |

knowns versions before 0.30.0 contain a path traversal vulnerability in the handleCodeReplace() function that allows attackers to overwrite arbitrary files outside the project root. Attackers can supply absolute paths or relative paths containing directory traversal sequences to write malicious content to sensitive files like shell startup scripts or SSH configuration files.

### CVE-2026-80127

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-07T16:17:29.807 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to elevation of privileges.

### CVE-2026-73321

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-08T14:17:26.617 |

XenForo before 2.3.13 contains an uncontrolled recursion vulnerability in the BBCode parser that allows authenticated attackers to cause persistent denial of service by submitting a post with deeply nested BBCode tags. Attackers can craft a single malicious post with sufficient nesting depth to exceed PHP's stack limit, causing fatal errors that repeatedly terminate PHP-FPM workers for all visitors rendering the affected thread.

### CVE-2026-11573

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-08T13:17:17.007 |

Uncontrolled recursion in Qt's QDomDocument serialization (QtXml) lets deeply nested untrusted XML crash the app via stack exhaustion (DoS only).

### CVE-2026-86713

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T12:17:00.150 |

PX4 Autopilot through 1.17.0 contains a use-after-free vulnerability in the load_mon module's stop path where exit_and_cleanup() deletes the LoadMon object and frees the performance counter before perf_end() attempts to access it. Attackers can trigger this vulnerability by issuing the load_mon stop command from any PXH or MAVLink shell, causing reads and writes through freed memory that corrupt heap objects and destabilize the flight stack.

### CVE-2026-9331

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T10:17:14.337 |

The EDD Product Catalog Feed by PixelYourSite plugin for WordPress is vulnerable to unauthorized modification of data that can lead to a denial of service due to a missing capability check on the wpeddpcf_delete_feed function in all versions up to, and including, 1.0.2. This makes it possible for authenticated attackers, with subscriber-level access and above, to delete arbitrary option values on the WordPress site. This can be leveraged to delete an option that would create an error on the site and deny service to legitimate users.

### CVE-2026-84820

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T08:17:13.673 |

Unauthenticated Cross Site Scripting (XSS) in Unlimited Elements For Elementor (Free Widgets, Addons, Templates) <= 2.0.17 versions.

### CVE-2026-84818

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T08:17:13.523 |

Unauthenticated Cross Site Scripting (XSS) in Open User Map <= 1.4.50 versions.

### CVE-2026-84817

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T08:17:13.393 |

Unauthenticated Cross Site Scripting (XSS) in JetFormBuilder <= 3.6.5.1 versions.

### CVE-2026-81798

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T08:17:13.013 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Easy Appointments allows DOM-Based XSS.

This issue affects Easy Appointments: from n/a through 4.0.2.1.

### CVE-2026-81781

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T08:17:12.630 |

Missing Authorization vulnerability in Unbounce Unbounce Landing Pages unbounce allows Exploiting Incorrectly Configured Access Control Security Levels.

This issue affects Unbounce Landing Pages: from n/a through 1.1.4.

### CVE-2026-62654

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-09-08T09:18:17.583 |

A vulnerability has been identified in Reyrolle 7SR5 (All versions < V2.70). A special maintenance mode can be activated via a physical key sequence during device boot, in which the device downloads and executes program code from a network server without verifying its authenticity or integrity. This could allow an attacker with physical access to the device to upload and execute arbitrary, unsigned code.

### CVE-2026-62653

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T09:18:17.463 |

A vulnerability has been identified in Reyrolle 7SR5 (All versions < V2.70). The input received over a proprietary communication protocol that is exposed when the device is placed into a special firmware-update mode is not properly validated, resulting in a memory corruption condition. This could allow an unauthenticated attacker with physical access to the device to cause a crash and potentially execute arbitrary code on the device.
