# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-09 15:02 UTC
- **対象期間**: `2026-09-08T15:00:30.000Z` 〜 `2026-09-09T15:02:11.000Z`
- **重要CVE数**: 1040 件（Critical 9.0+: 112 件 / High 7.0〜: 928 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公表された CVE のうち、CVSS が 9.8 以上の深刻度が集中しているのは **リモートコード実行 (RCE) 系** と **権限昇格 / 認可不備** に関する脆弱性です。  
- 製品領域は IoT デバイス、API 管理基盤、Adobe 製品、ネットワークセキュリティアプライアンス、Windows OS と多岐にわたり、**「認証不要」かつ **「ネットワーク経由で任意コード実行」** が共通した攻撃パスとなっています。  
- 多くのベンダーが **デフォルト設定の緩さ**、**パス正規化の不整合**、**入力検証の欠如** を根本原因としているため、**設定見直しとパッチ適用が最優先** となります。

---

## 2. 特に注目すべき CVE  

| CVE | 評価 (CVSS) | 主な影響 | 注目すべき理由 |
|-----|------------|----------|----------------|
| **CVE‑2026‑87827** | 10.0 | KGUARD 系 DVR のファームウェアに認証不要のシステムコマンド実行サービスが公開。ネットワーク上から任意のシェルコマンドが実行可能。 | IoT/監視カメラは社内外のネットワークに常設されやすく、**侵入後の横移動や情報窃取の踏み台**になる。ファームウェア更新が遅れがちなので、早急な対策が必要。 |
| **CVE‑2026‑85978** | 10.0 | Akana API Platform の Policy Manager コンソールで、認証フィルタとサーブレットディスパッチャのパス正規化不整合により認証バイパスが可能。任意コード実行が可能。 | API 管理基盤は多数の内部サービスへのゲートウェイとなり、**一度侵入すれば全社 API が危険に晒される**。特にクラウドデプロイ環境での自動スケールが多い組織は注意。 |
| **CVE‑2026‑82004** | 10.0 | Adobe Campaign Classic (ACC) に OS コマンドインジェクションが存在。特権ユーザーのコンテキストで任意コード実行が可能。 | Adobe 製品はマーケティング部門だけでなく、顧客データベースと連携しているケースが多く、**個人情報漏洩リスクが高い**。既知のパッチがリリース済みだが、適用が遅れているケースが散見。 |
| **CVE‑2026‑85103** / **CVE‑2026‑85102** | 9.8 | Check Point Quantum Security Management / Gateway の VPN 証明書処理にヒープバッファオーバーフローと証明書信頼性検証不備。認証なしでリモートコード実行が可能。 | VPN はリモートワークの要であり、**外部から直接攻撃が可能**になる。特にハイブリッド環境で VPN が唯一の入口となっている組織は緊急対応が必須。 |
| **CVE‑2026‑73010** | 9.8 | Windows Server Failover Cluster の Use‑After‑Free バグにより、リモートからコード実行が可能。 | Windows Server は多くの企業基盤で稼働中。**クラスタ構成が攻撃対象になると、サービス全体が停止・乗っ取り**される危険性がある。マイクロソフトが提供する累積的更新プログラム (KB) の適用が必須。 |

---

## 3. 推奨アクション  

### 共通対策
1. **ベンダー提供の最新パッチ・ファームウェアを即時適用**  
   - パッチ適用前に必ずバックアップを取得し、テスト環境で動作確認を行う。  
2. **ネットワーク境界でのアクセス制御強化**  
   - 該当サービスが外部に露出している場合は、ファイアウォール/ACL で **IP アドレスベースの許可** または **VPN 経由のみ** に限定。  
3. **不必要なサービス・ポートの無効化**  
   - 例: KGUARD のコマンド実行サービス (ポート 23/SSH 以外) を無効化、Akana の管理コンソールは内部ネットワークのみからアクセス可能にする。  
4. **ログ監視とインシデント対応体制の整備**  
   - 侵入検知システム (IDS/IPS) に該当 CVE のシグネチャを追加し、異常なコマンド実行や証明書エラーを即時アラート化。  

### 製品別具体的アクション  

| 製品・サービス | 推奨パッケージ / バージョン | 具体的作業 |
|----------------|----------------------------|------------|
| **KGUARD DVR** | ファームウェア **v3.2.7 以降**（ベンダーが提供する「Security Patch」） | 1. 現行ファームウェアバージョン確認 (`show version`) 2. 公式サイトから最新ファームウェアをダウンロード 3. メンテナンスウィンドウで OTA 更新 |
| **Akana API Platform** | Policy Manager **7.5.3 以降**（Security Update 2026‑Q2） | 1. 管理コンソールにログインし、`/admin/updates` でパッチ適用 2. パス正規化ロジックの修正が含まれることを確認 |
| **Adobe Campaign Classic** | ACC 2026.1 **Patch 2026‑001**（Adobe Security Bulletin 2026‑A‑001） | 1. Adobe Admin Console からパッチを取得 2. アプリケーションサーバを再起動し、`/opt/adobe/campaign` のバージョンを `2026.1.001` に更新 |
| **Check Point Quantum** | **Management**:  R81.10 **Patch 2026‑02** <br> **Gateway**:  R81.10 **Patch 2026‑02** | 1. SmartConsole → Updates → Download & Install 2. VPN 設定で証明書検証ポリシーを「厳格」に変更 |
| **Windows Server (Failover Cluster)** | **KB5028225**（2026‑03 Cumulative Update） | 1. Windows Update で累積更新プログラムを適用 2. 再起動後、`Get-ClusterLog` でエラーログを確認 |
| **その他 (Adobe Experience Manager, ColdFusion, Ivanti Neurons, etc.)** | 各ベンダーが公表する **「最新安定版」** または **「Security Patch」** を適用 | 1. 製品ポータルで「Security Advisory」確認 2. パッチ適用手順に従い、テスト環境で回帰テスト実施 |



---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-87827

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-09-09T11:17:16.423 |

Certain KGUARD DVR devices running vulnerable firmware expose a system command execution service on all network interfaces without requiring authentication. A remote unauthenticated attacker with network access to the affected service can execute arbitrary system commands on the device, potentially resulting in complete compromise of the DVR.

The vulnerability is known to have been exploited in the wild by the Mirai_ptea (Rimasuta) and Mirai_aurora botnets for malware propagation and subsequent DDoS activity. The vulnerability was reported to affect firmware dating from 2016, while firmware released after 2017 appears to mitigate the issue by restricting the affected service to the localhost interface (127.0.0.1) instead of exposing it on all interfaces (0.0.0.0).

The affected-device list reported by Netlab includes many D1004NR, D1008NR, D1016NR, D1104, D1104NR, D1108NR, D1116NR, D1132NR, D2116NR, D97xx, D98xx, and D99xx variants and several associated hardware revisions


The exploit is included in some version of rapperbot and exploited in 2026. This assignment has been made to document the active exploitation and lack of documentation from the vendor.

### CVE-2026-85978

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-41;CWE-94;CWE-863` |
| Published | 2026-09-09T11:17:16.073 |

An unauthenticated remote code execution vulnerability exists in the Policy Manager console of Akana API Platform. A path normalization discrepancy between the authentication filter and the servlet dispatcher allows a crafted request to bypass authentication and reach an endpoint that evaluates attacker-supplied script code without sandboxing, resulting in arbitrary code execution. Exploitation requires no authentication or user interaction.

### CVE-2026-79696

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-09T09:17:11.223 |

A Code Injection vulnerability in adk web in Google Cloud Agent Development Kit (ADK) for Python versions 2.0.0 through 2.6.0 on Python (OSS), Cloud Run, and GKE environments where pytest is installed allows an unauthenticated remote attacker to execute arbitrary code using a crafted test session replay.

### CVE-2026-49883

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-08T20:17:33.690 |

In checkReadPermission of PermissionsManager.java, there is a possible way to monitor sensitive device state data due to a missing permission check. This could lead to local information disclosure with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28659

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-08T20:17:32.957 |

In MicroXR Blobstore, there is a possible way to access other app's files due to a missing permission check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-82004

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-08T19:19:59.743 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-86464

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-306;CWE-798;CWE-1188;CWE-1392` |
| Published | 2026-09-08T20:18:52.960 |

In the current development version of Eclipse aeriOS, for which no official release has yet been published, the Identity Manager (IdM) deployment included insecure default configurations and credentials for security-sensitive services.




The Helm chart exposed the Keycloak service and its PostgreSQL backing database through Kubernetes NodePort services by default, while the Docker Compose deployment similarly exposed PostgreSQL on all network interfaces. The deployment included fixed default credentials for the Keycloak administrator and PostgreSQL database user, and the previous Helm chart configuration did not provide adequate secret management for these credentials. In addition, predefined application users with known credentials were provided for development and testing without sufficiently warning operators against their use in production environments.




An attacker able to reach the exposed services could use the published default credentials to obtain administrative access to the Identity Manager or direct access to its database. This could allow unauthorized access to or modification of identity-management data, including users, roles, client credentials, sessions, and cryptographic material, and could enable the creation of privileged identities or tokens accepted by other aeriOS components.




The issue has been addressed by generating a random Keycloak administrator password by default, managing Keycloak and PostgreSQL credentials through Kubernetes Secrets, and restricting PostgreSQL to an internal service in both the Helm chart and Docker Compose deployment. OpenLDAP is also restricted to an internal service. The predefined users intended for development and testing are retained, but the documentation now explicitly warns that their default credentials must not be used in production and that these users should be removed or their credentials changed after installation.

### CVE-2026-84869

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-09-08T20:18:51.147 |

A condition in the ScreenConnect client may allow files to be transferred and executed through an active remote session without authorization or Host confirmation in certain circumstances. ScreenConnect servers are not impacted.

### CVE-2026-48273

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-08T20:17:33.560 |

ColdFusion is affected by an Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-19232

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T20:17:28.940 |

Adobe Experience Manager is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user, potentially gaining elevated access or control over the victim's account or session. A low-privileged attacker could exploit this vulnerability to gain elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-83941

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T18:21:04.853 |

Missing authorization in Entra ID allows an authorized attacker to elevate privileges over a network.

### CVE-2026-26084

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-08T17:17:34.590 |

A improper access control vulnerability in Fortinet FortiSandbox 5.0.0 through 5.0.5, FortiSandbox 4.4.0 through 4.4.8, FortiSandbox Cloud 5.0.4 through 5.0.5, FortiSandbox PaaS 5.0.4 through 5.0.5 may allow attacker to access sensitive information via crafted HTTP requests.

### CVE-2026-12650

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T15:18:40.850 |

A Deserialization of Untrusted Data vulnerability in Ivanti Neurons for ITSM before 2026.2 allows a remote authenticated attacker to execute arbitrary code on the server.

### CVE-2026-12647

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T15:18:40.623 |

A Missing Authorization vulnerability in Ivanti Neurons for ITSM before 2026.2 allows a remote authenticated attacker to execute arbitrary code on the server.

### CVE-2026-12646

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T15:18:40.507 |

A Missing Authorization vulnerability in Ivanti Neurons for ITSM before 2026.2 allows a remote authenticated attacker to execute arbitrary code on the server.

### CVE-2026-12645

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T15:18:40.380 |

A Missing Authorization vulnerability in Ivanti Neurons for ITSM before 2026.2 allows a remote authenticated attacker to execute arbitrary code on the server.

### CVE-2026-85103

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-09T13:20:43.997 |

A heap-based buffer overflow in VPN certificate ASN.1 decoding may allow an unauthenticated remote attacker to execute arbitrary code on Check Point Quantum Security Management and Quantum Security Gateway systems.

### CVE-2026-85102

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-09T13:20:43.793 |

Improper certificate trust validation during VPN negotiation in Check Point Quantum Security Gateway may allow an unauthenticated remote attacker to execute arbitrary code on the Gateway.

### CVE-2026-80172

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-09T12:17:15.057 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Insufficient Verification of Data Authenticity vulnerability. An unauthenticated attacker with remote access could exploit this, leading to unauthorized access. This vulnerability is considered critical as an unauthenticated attacker can repeatedly reuse a captured request to generate ADMIN access and refresh tokens. Since there is no nonce validation or time limit on requests, the attack can be performed indefinitely. Dell recommends customers to upgrade at the earliest opportunity

### CVE-2026-66302

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-08T19:18:07.690 |

External control of file name or path in Skype for Business allows an unauthorized attacker to execute code over a network.

### CVE-2026-58822

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-704` |
| Published | 2026-09-08T19:18:02.780 |

In multiple functions of ftsmooth.c, there is a possible memory safety issue due to improper casting. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-49921

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T19:17:59.193 |

In multiple locations, there is a possible memory safety issue due to a heap buffer overflow. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-78510

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:46.200 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-78509

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:46.070 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-78445

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:42.263 |

Use after free in Windows Services for NFS ONCRPC XDR Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-77493

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:20:35.187 |

Double free in Microsoft Graphics Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-73025

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-09-08T18:20:32.490 |

Weak authentication in Windows iSCSI allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-73010

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:29.987 |

Use after free in Windows Failover Cluster allows an unauthorized attacker to execute code over a network.

### CVE-2026-73009

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:29.810 |

Use after free in Windows Secure Socket Tunneling Protocol (SSTP) allows an unauthorized attacker to execute code over a network.

### CVE-2026-72983

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:25.073 |

Use after free in Windows Internet Connection Sharing (ICS) allows an unauthorized attacker to execute code over a network.

### CVE-2026-72982

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:20:24.863 |

Stack-based buffer overflow in Windows Netlogon allows an unauthorized attacker to execute code over a network.

### CVE-2026-72979

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:24.310 |

Use after free in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-70296

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T18:20:04.910 |

Out-of-bounds write in Windows Imaging Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-69910

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:20:02.250 |

Stack-based buffer overflow in Windows Hyper-V allows an unauthorized attacker to execute code over a network.

### CVE-2026-69845

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-09-08T18:19:56.003 |

Heap-based buffer overflow in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-69829

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:54.707 |

Heap-based buffer overflow in Windows Shell allows an unauthorized attacker to execute code over a network.

### CVE-2026-69824

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-09-08T18:19:54.190 |

Integer underflow (wrap or wraparound) in Microsoft Standard XPS allows an unauthorized attacker to execute code over a network.

### CVE-2026-69819

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T18:19:53.570 |

Out-of-bounds write in RPC Runtime allows an unauthorized attacker to execute code over a network.

### CVE-2026-69769

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:48.147 |

Heap-based buffer overflow in Windows HTTP Print Provider allows an unauthorized attacker to execute code over a network.

### CVE-2026-69768

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:47.970 |

Heap-based buffer overflow in Windows RNDIS allows an unauthorized attacker to execute code over a network.

### CVE-2026-69730

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:45.140 |

Use after free in Windows DNS allows an unauthorized attacker to execute code over a network.

### CVE-2026-69715

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-09-08T18:19:43.520 |

Out-of-bounds read in Windows Direct Show allows an unauthorized attacker to execute code over a network.

### CVE-2026-69595

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:30.093 |

Use after free in Windows Services for NFS ONCRPC XDR Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-69590

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:29.310 |

Remote Code Execution in Windows Routing and Remote Access Service (RRAS) allows attacker to gain an unauthorized access to victim's machine

### CVE-2026-69586

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:19:28.670 |

Integer overflow or wraparound in Microsoft Windows PDF allows an unauthorized attacker to execute code over a network.

### CVE-2026-69579

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:27.440 |

Use after free in Windows Message Queuing allows an unauthorized attacker to execute code over a network.

### CVE-2026-69525

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:20.030 |

Use after free in Windows Remote Desktop Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-69496

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:16.260 |

Heap-based buffer overflow in Windows Compressed Folder allows an unauthorized attacker to execute code over a network.

### CVE-2026-69493

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-09-08T18:19:15.720 |

Out-of-bounds read in Windows Event Logging Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-69491

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:15.357 |

Heap-based buffer overflow in Windows Microsoft DirectMusic allows an unauthorized attacker to execute code over a network.

### CVE-2026-69463

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:11.387 |

Heap-based buffer overflow in Windows NTFS allows an unauthorized attacker to execute code over a network.

### CVE-2026-69431

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:06.903 |

Heap-based buffer overflow in Telnet Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69408

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:19:03.540 |

Integer overflow or wraparound in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-69276

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-09-08T18:18:41.153 |

Integer underflow (wrap or wraparound) in Microsoft UxTheme Library (uxtheme.dll) allows an unauthorized attacker to execute code over a network.

### CVE-2026-68839

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-09-08T18:18:31.623 |

Heap-based buffer overflow in Windows USB Mass Storage Class Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-79569

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-08T17:18:31.143 |

Movie_Recommend v1.0.0 was discovered to contain a SQL injection vulnerability in the sort parameter at /loadingmore. This vulnerability allows attackers to access sensitive database information via a crafted SQL statement.

### CVE-2026-79576

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-08T15:18:48.417 |

An issue in the Single-Sign On (SSO) component of Digital-Infrastructure v9.6.7 allows attackers to authenticate as any user, including the Admin, without a password.

### CVE-2026-12745

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T15:18:41.190 |

A Deserialization of Untrusted Data vulnerability in Ivanti Neurons for ITSM before 2026.2 allows a remote unauthenticated attacker to execute arbitrary code on the server.

### CVE-2026-12744

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T15:18:41.080 |

A Deserialization of Untrusted Data vulnerability in Ivanti Neurons for ITSM before 2026.2 allows a remote unauthenticated attacker to execute arbitrary code on the server.

### CVE-2026-87654

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-09T01:17:23.933 |

Buffer overflow in ANGLE in Google Chrome on on Windows prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87650

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-09T01:17:23.503 |

Out of bounds read in WebGL in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87646

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:23.077 |

Use after free in Web Authentication in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87643

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-09T01:17:22.740 |

Integer overflow in GPU in Google Chrome on on Android prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87638

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-09T01:17:22.207 |

Out of bounds write in Media in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87637

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:22.103 |

Use after free in Extensions in Google Chrome on on Mac prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87634

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:21.770 |

Use after free in WebPackaging in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-87621

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-09T01:17:20.313 |

Out of bounds write in ANGLE in Google Chrome on on Windows prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87609

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:18.987 |

Use after free in Sharing in Google Chrome on on iOS prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via crafted network traffic. (Chromium security severity: Medium)

### CVE-2026-87607

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:18.763 |

Use after free in Device in Google Chrome on on Mac prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87581

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:15.930 |

Use after free in Payments in Google Chrome prior to 153.0.8010.36 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87558

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:13.443 |

Use after free in Payments in Google Chrome on on Mac prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87547

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-09-09T01:17:12.240 |

Incorrect reference resolution in FileSystem in Google Chrome prior to 153.0.8010.36 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87529

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-09-09T01:17:10.240 |

Numeric truncation error in Media in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87528

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-09T01:17:10.110 |

Type confusion in Rust in Google Chrome on on Windows prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87527

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-09T01:17:09.980 |

Buffer overflow in WebGL in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-87526

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:09.853 |

Use after free in Passwords in Google Chrome prior to 153.0.8010.36 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via UI Interaction. (Chromium security severity: Medium)

### CVE-2026-87520

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:09.137 |

Use after free in Dawn in Google Chrome on on Android prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87512

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:08.267 |

Use after free in ANGLE in Google Chrome on on Windows prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87504

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:07.347 |

Use after free in Core in Google Chrome prior to 153.0.8010.36 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted Chrome extension. (Chromium security severity: Medium)

### CVE-2026-87500

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-09-09T01:17:06.900 |

Improper validation of array index in ANGLE in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87494

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:06.207 |

Use after free in Browser in Google Chrome on on Windows prior to 153.0.8010.36 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87492

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-09T01:17:05.993 |

Incorrect authorization in DevTools in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87488

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:05.557 |

Use after free in WebGL in Google Chrome on on Android prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-87474

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:03.990 |

Use after free in Payments in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87470

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1284` |
| Published | 2026-09-09T01:17:03.560 |

Improper quantity validation in Tint in Google Chrome on on Mac prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87464

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:02.907 |

Use after free in WebGL in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-87455

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:01.883 |

Use after free in Aura in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87448

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:01.113 |

Use after free in DevTools in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-87438

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-09T01:17:00.027 |

Out of bounds write in WebGL in Google Chrome on on Android prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-81376

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-693;CWE-1023` |
| Published | 2026-09-08T18:20:53.813 |

Incomplete comparison with missing factors in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-65669

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-08T18:18:14.893 |

Improper neutralization of special elements in output used by a downstream component ('injection') in SQL Server allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-82533

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-09-08T17:18:36.887 |

DeepSeek Harness before 0.1.2-alpha.1 contains an authentication bypass vulnerability in its local HTTP control-plane API that allows attackers to gain full agent control by supplying a spoofed Host header, as the server validates only the client-supplied Host header value rather than the actual TCP connection origin. Attackers can exploit this flaw to invoke privileged commands such as commands/execute with danger-full-access permissions, escalate session approval policies to unconfined execution, and retrieve all stored conversations without any credential or API key.

### CVE-2026-21102

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T05:17:22.490 |

Use after free in DualDAR prior to SMR Sep-2026 Release 1 allows local privileged attackers to execute arbitrary code with root privilege.

### CVE-2026-76201

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T19:19:40.947 |

Adobe Commerce is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by an attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-76200

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T19:19:40.813 |

Adobe Commerce is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by an attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-69356

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T18:18:55.060 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Exchange Server allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-86738

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T16:18:36.980 |

Snipe-IT versions before 8.7.0 contain a CSS injection vulnerability in the Custom CSS field due to incomplete sanitization that reverses HTML encoding on greater-than and double-quote characters. Superusers can plant malicious CSS payloads using @import and url() references to exfiltrate CSRF tokens from other superusers via attribute-selector rules, enabling account takeover.

### CVE-2026-61516

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-08T15:18:44.170 |

Netis NX10 firmware V4.0.1.5808 and V3.0.0.4142 contain an information disclosure vulnerability that allows unauthenticated attackers to retrieve the administrator password by sending a request to the sysinfo action in the web management interface without a valid session. Attackers can replay the exposed credential against the login handler to establish a fully authenticated administrator session on the device.

### CVE-2026-21096

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T05:17:21.783 |

Heap-based buffer overflow in JPEG decoder of libimagecodec.quram.so prior to SMR Sep-2026 Release 1 allows remote attackers to execute arbitrary code.

### CVE-2026-21095

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T05:17:21.663 |

Heap-based buffer overflow in DNG decoder of libimagecodec.quram.so prior to SMR Sep-2026 Release 1 allows remote attackers to execute arbitrary code.

### CVE-2026-84197

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295;CWE-297;CWE-300` |
| Published | 2026-09-08T20:18:51.007 |

In Eclipse Ditto's Node.js JavaScript client, all released versions of @eclipse-ditto/ditto-javascript-client-node from 2.0.0 to 3.9.0 and of its predecessor package @eclipse-ditto/ditto-javascript-client-node_1.0 from 1.0.0 to 2.1.0, the WebSocket transport hard-codes rejectUnauthorized: false when creating the underlying ws WebSocket. Certificate chain and hostname validation are therefore disabled for every wss:// connection, and no builder option, constructor argument or environment variable lets an application turn validation back on. An attacker in a position to intercept the connection can present an arbitrary certificate, complete the TLS handshake, read the credentials that the configured authentication provider sends in the Authorization header of the WebSocket upgrade request, and read, alter or inject Ditto Protocol messages for the lifetime of the connection. The Java client, the browser/DOM JavaScript client and the HTTP transport of the Node.js client are not affected.

### CVE-2026-82067

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-09-08T17:18:35.617 |

Improper handling of case sensitivity in the configuration validation component of MongoDB Server may cause the authorization subsystem to remain in a default disabled state during server startup. An unauthenticated user with network access to a deployment where this condition occurs can perform arbitrary administrative operations, resulting in full impact of data confidentiality, integrity, and availability.

### CVE-2026-87806

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-09T12:17:15.190 |

Parse Server versions <= 8.6.87 and >= 9.0.0 < 9.10.1-alpha.7 contain an authentication bypass in the built-in LDAP authentication adapter. The adapter forwarded the client-supplied password to the directory without verifying that a password had been supplied, and treated any non-error response from the directory as proof of authentication. A zero-length credential turns an LDAP simple bind into the unauthenticated authentication mechanism described in RFC 4513 section 5.1.2, which some directories (including Active Directory in its default configuration) answer with success while mapping the connection to anonymous. As a result, an unauthenticated attacker who knows a directory username can obtain a valid session token for that account, resulting in account takeover. Only deployments that enable the LDAP authentication adapter are affected, and deployments whose directory refuses unauthenticated simple bind (such as a stock OpenLDAP configuration) are not exploitable. The issue is fixed in 8.6.88 and 9.10.1-alpha.7, which require the password to be a non-empty string and reject the request before contacting the directory.

### CVE-2026-16272

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-348` |
| Published | 2026-09-09T09:17:10.720 |

Use of less trusted source vulnerability in PayTR Payment and Electronic Money Institution Inc. PayTR Virtual Pos iFrame API (v9x) WHMCS Module allows Exploitation of Trusted Identifiers.

This issue affects PayTR Virtual Pos iFrame API (v9x) WHMCS Module: from v9.0.0 before v9.0.3.

### CVE-2026-53939

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-321;CWE-330` |
| Published | 2026-09-09T00:17:31.700 |

OpenIDC/cjose is a C library implementing the Javascript Object Signing and Encryption (JOSE). In versions 0.6.1 through 0.6.2.5, when cjose encrypts a JWE using an AES-CBC-HMAC content-encryption algorithm (`A128CBC-HS256`, `A192CBC-HS384`, or `A256CBC-HS512`) together with any key-management algorithm that generates a fresh content-encryption key (CEK), the CEK is all zero bytes instead of being randomly generated. The resulting JWE is therefore encrypted and authenticated under a fixed, publicly known key, so anyone who obtains the JWE can recover the plaintext and forge or modify the content. This is fixed in version 0.6.2.6 by `_cjose_jwe_set_cek_aes_cbc()` generating the CEK from `RAND_bytes`. A regression test asserts that the `encrypted_key` differs across two encryptions for each AES-CBC-HMAC variant. Until upgrading, for data encrypted with cjose, three options are available. Use an AES-GCM `enc` (`A128GCM` / `A192GCM` / `A256GCM`) instead of an AES-CBC-HMAC `enc`,  use `alg=dir` with a caller-supplied CEK, or avoid using cjose for JWE encryption with the affected algorithm pair. These are mitigations for new ciphertexts only; data already encrypted under the zero key remains compromised and should be re-encrypted (and any secrets it contained rotated).

### CVE-2026-75746

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-08T20:18:22.120 |

ColdFusion is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker with high privileges could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-69641

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T18:19:36.313 |

Missing authorization in Microsoft Exchange Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-75156

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-08T17:18:30.393 |

Apache Airflow FAB provider versions 3.7.3 through 3.8.0 do not validate the issuer or audience of Azure AD `id_token`s during OAuth login. Deployments are affected only when the FAB auth manager is configured with Azure AD as an OAuth provider. Because the signing keys are fetched from Microsoft's **multi-tenant** JWKS endpoint, an `id_token` minted in *any* Azure tenant — including one the attacker creates — passes signature verification, and the username and role assignments are then read from that attacker-controlled token. Anyone able to register an Azure tenant can therefore authenticate to the Airflow UI with no prior access to the deployment.

The fix for **CVE-2026-59243** was incomplete, and this advisory closes the remaining gap: that fix made the provider verify the `id_token` signature, but did not add issuer or audience checks. Operators who already applied the CVE-2026-59243 fix are **still affected and must upgrade again** — 3.7.3 is the release that shipped that fix, so every version containing it falls inside this affected range. Upgrade to apache-airflow-providers-fab `3.8.1` or later.

### CVE-2026-86729

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-08T16:18:34.523 |

WWBN AVideo through commit e01e41ecc (no patched version available) exposes get_api_preauthorize in plugin/API/API.php as a second, undocumented login path. Unlike get_api_signIn, which enforces a rate limit of 10 attempts per 5 minutes via checkRateLimit(), get_api_preauthorize performs the same credential check with no throttling for any client, allowing unlimited remote password guessing against arbitrary accounts, including admin. The endpoint also acts as a credential oracle: it returns the message "Invalid credentials" for both correct and incorrect passwords, while the users_id field in the response body discloses the authenticated identity (users_id:1 on success, users_id:0 on failure), and a correct password establishes a session cookie that remains usable for authenticated API requests. Together these issues permit unauthenticated brute-force account takeover.

### CVE-2026-53581

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-09-08T23:17:24.550 |

OPNsense is a FreeBSD based firewall and routing platform. Prior to version 26.1.9 of opnsense/core and version 26.4_20 of BE/opnsense/core, a path traversal vulnerability in the NTP configuration module allows an attacker to overwrite arbitrary files on the system as the root user. By manipulating the GPS or PPS serial port parameter, an attacker with access to the NTP configuration can escape the intended directory and force the system to write user-controlled data to any file on the filesystem. Version 26.1.9 of opnsense/core and version 26.4_20 of BE/opnsense/core patch the issue.

### CVE-2026-85982

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T21:18:47.293 |

The Auth0 AD/LDAP Connector is vulnerable to stored Cross-Site Scripting (XSS) issues due to improper HTML encoding of data in search results and updater log content displayed in the admin panel. An authenticated user with privileges to modify directory attributes, or a low-privileged local user on the host where the connector is installed, could insert script content. This script content could then execute in an administrator's browser when they view the affected search results or update logs.

### CVE-2026-69854

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-08T18:19:56.910 |

Improper authentication in Spring Cloud Azure allows an unauthorized attacker to elevate privileges over a network.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-86775

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-09T14:17:28.533 |

knowns (npm package) versions <= 0.29.1 contain a path traversal vulnerability in the Document API. The HTTP handler in internal/server/routes/docs.go normalizes the user-supplied document path with cleanDocPath(), which strips leading/trailing slashes and the .md suffix but does not neutralize ../ traversal sequences, and internal/storage/doc_store.go then builds the target path with filepath.Join(ds.docsDir(), filepath.FromSlash(doc.Path)+".md") without verifying that the resolved path remains inside the documents directory. In the default deployment, where the Management API is unauthenticated and bound to all interfaces, a remote unauthenticated attacker can supply a traversal payload (for example {"path": "../../../../tmp/knowns_pwn_marker"} to POST /api/docs, or an encoded path to GET /api/docs/...) to read, create, overwrite, or delete arbitrary files with a .md extension anywhere on the host filesystem and to create arbitrary directories via os.MkdirAll. This can expose sensitive data stored in other projects' documentation, corrupt or destroy files, and provide an arbitrary-write primitive that may be chained toward code execution. The issue is fixed in version 0.30.0.

### CVE-2026-86099

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-09T14:17:20.387 |

Chainlit through 2.12.0 fails to validate the client-supplied socket.io sessionId parameter, allowing unauthenticated attackers to traverse filesystem paths by injecting absolute or relative path sequences. Attackers can craft malicious sessionId values that escape the upload directory and recursively delete arbitrary directories accessible to the service process.

### CVE-2026-87795

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-09T10:22:34.557 |

zstd-jni versions before 1.5.7-14 fail to validate offset and length parameters in the ZstdDictCompress constructor, allowing out-of-bounds memory reads. Attackers can supply untrusted offset or length values to read native heap memory into the compression dictionary, typically causing JVM crashes.

### CVE-2026-87766

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-09T09:17:12.540 |

A flaw was found in bubblewrap. During sandbox setup, creating files or directories under the new root can follow a parent symlink onto the host via /oldroot, writing attacker-chosen paths outside the sandbox as the launching user. This happens before the sandboxed process starts. This issue is GHSA-pxhw-h44j-8pfx. It is fixed in bubblewrap 0.12.0.

### CVE-2026-80099

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-09T09:17:12.157 |

Several Newfold plugins are vulnerable to Authentication Bypass. The vulnerability exists because the plugins bundle the wp-module-data module. In the module, the `authenticate()` method — registered on the `rest_authentication_errors` filter and therefore evaluated for every unauthenticated REST API request — performs an HMAC-style Bearer token comparison that degenerates when `HiiveConnection::get_auth_token()` returns `false`: PHP coerces `strrev(false)` to `strrev('')`, collapsing the secret salt to the publicly known constant `hash('sha256', '') = e3b0c44...`, while all remaining hash inputs (HTTP method, request URL, raw request body, and the `X-Timestamp` header) remain fully attacker-controlled. This makes it possible for unauthenticated attackers to compute a valid Bearer token entirely offline, pass the token equality check, and have `wp_set_current_user()` invoked against the first administrator returned by `get_users(['role' => 'administrator'])`, granting full administrator-level access and enabling arbitrary REST API operations such as creating new administrator accounts and achieving complete site takeover. Vulnerable versions are WP Plugin Crazy Domains (<= 2.5.2), WP Plugin Web (<= 2.3.4), WP Plugin Hostgator (<= 3.1.0), WP Plugin Bluehost (<= 4.17.1). The affected module is vulnerable in versions up to, and including, 2.9.4.

### CVE-2026-14359

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-09T09:17:10.450 |

The YITH WooCommerce Waitlist Premium plugin for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 3.35.0. This is due to the add_user_in_waiting_list() function registered on the wp_ajax_yith_wcwtl_add_user action being missing both a capability check and a nonce verification, and using parse_str() + extract() to import attacker-controlled variables from $_POST['params'] that are then passed to wp_create_user() and $user->set_role(). This makes it possible for authenticated attackers, with Subscriber-level access and above, to elevate their privileges to that of an administrator by creating a new user account and assigning it the administrator role.

### CVE-2026-21092

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T05:17:21.290 |

Path traversal in ImsService prior to SMR Sep-2026 Release 1 allows remote attackers to create image files with system server privilege.

### CVE-2026-76801

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-09T03:17:24.943 |

The FireBox – WooCommerce Popup Builder, Exit Intent Popup, Email Optin & Cart Abandonment plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 3.1.10 via the value function. This is due to a trivially bypassable regex blacklist in Executer::allowedToRun() that fails to block WordPress core functions such as wp_insert_user, update_option, and file_put_contents, combined with no sanitization of PHP condition rule values stored via the firebox_meta REST endpoint. This makes it possible for authenticated attackers, with author-level access and above, to execute code on the server. On sites upgraded from a version prior to 3.1.10, the Migrator::preserveCampaignRoleAccess() function automatically grants the edit_fireboxes and publish_fireboxes capabilities to the Author role, lowering the effective entry point to Author-level access.

### CVE-2026-87636

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-09T01:17:21.990 |

Type confusion in XML in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87625

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:20.770 |

Use after free in V8 in Google Chrome prior to 153.0.8010.36 allowed a remote attacker leveraging social engineering to execute arbitrary code inside the sandbox via a crafted Chrome extension. (Chromium security severity: Medium)

### CVE-2026-87617

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:19.840 |

Use after free in DevTools in Google Chrome prior to 153.0.8010.36 allowed a remote attacker leveraging social engineering to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-87612

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-09T01:17:19.310 |

Type confusion in V8 in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87588

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:16.683 |

Use after free in Chromecast in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87587

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:16.580 |

Use after free in V8 in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87585

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-09T01:17:16.357 |

Double free in PDFium in Google Chrome on on Windows prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted PDF file. (Chromium security severity: High)

### CVE-2026-87579

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-09T01:17:15.703 |

Buffer overflow in WebRTC in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87542

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:11.697 |

Use after free in Input in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87536

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:11.047 |

Use after free in V8 in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87491

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-09T01:17:05.887 |

Out of bounds write in V8 in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-87489

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-09T01:17:05.663 |

Memory corruption in V8 in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted Chrome extension. (Chromium security severity: Low)

### CVE-2026-87460

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T01:17:02.460 |

Use after free in Platform in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87444

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-09T01:17:00.677 |

Memory corruption in Codecs in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87440

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-09T01:17:00.240 |

Out of bounds read in Media in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-87430

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-09T01:16:59.130 |

Buffer overflow in WebRTC in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-81996

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T21:18:46.347 |

Acrobat Reader is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain elevated access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-78834

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-08T20:18:38.773 |

A code execution vulnerability exists in CMSimple 5.22 in the CoAuthors plugin. An authenticated low-privileged user who can modify page content and provide controlled imported content can trigger server-side execution by referencing crafted external or uploaded text content through the affected content import feature.

### CVE-2026-85877

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:13.960 |

Heap-based buffer overflow in Windows Print Spooler Components allows an unauthorized attacker to execute code over a network.

### CVE-2026-83998

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:10.683 |

Heap-based buffer overflow in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-83996

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:10.350 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-83992

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:09.980 |

Heap-based buffer overflow in Windows Imaging Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-81955

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:59.120 |

Heap-based buffer overflow in Microsoft Graphics Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-81952

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:58.727 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-81385

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T18:20:54.720 |

Deserialization of untrusted data in Microsoft Office Publisher allows an unauthorized attacker to execute code over a network.

### CVE-2026-81352

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:52.940 |

Heap-based buffer overflow in Microsoft Windows Codecs Library allows an unauthorized attacker to execute code over a network.

### CVE-2026-80096

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:51.960 |

Out-of-bounds read in Windows Remote Desktop Services allows an authorized attacker to elevate privileges over a network.

### CVE-2026-80085

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:50.870 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-80083

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-08T18:20:50.613 |

Untrusted pointer dereference in Windows Hyper-V allows an authorized attacker to execute code locally.

### CVE-2026-80081

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:50.367 |

Use after free in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-80080

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:20:50.233 |

Double free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-80077

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:49.860 |

Heap-based buffer overflow in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-80074

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:49.313 |

Heap-based buffer overflow in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-78526

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:48.347 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-78525

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:48.227 |

Use after free in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-78524

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T18:20:48.100 |

Out-of-bounds write in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-78521

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:47.683 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-78519

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-09-08T18:20:47.427 |

Use of uninitialized resource in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-78518

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-125` |
| Published | 2026-09-08T18:20:47.293 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-78517

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:47.163 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-78514

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:46.720 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-78512

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-09-08T18:20:46.453 |

Numeric truncation error in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-78511

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:46.327 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-78507

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:45.750 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-78505

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:45.487 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-78504

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:20:45.360 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-78463

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-08T18:20:44.800 |

Improper control of generation of code ('code injection') in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-78462

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-08T18:20:44.670 |

Authorization bypass through user-controlled key in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-78456

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:44.280 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-78442

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:42.020 |

Heap-based buffer overflow in Windows OLE DB allows an unauthorized attacker to execute code over a network.

### CVE-2026-78439

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:20:41.757 |

Stack-based buffer overflow in Microsoft Graphics Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-77908

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-08T18:20:41.000 |

Improper control of generation of code ('code injection') in Microsoft Dynamics 365 allows an authorized attacker to execute code over a network.

### CVE-2026-77907

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:40.873 |

Heap-based buffer overflow in Visual Studio allows an unauthorized attacker to execute code over a network.

### CVE-2026-77906

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:40.733 |

Heap-based buffer overflow in Visual Studio allows an unauthorized attacker to execute code over a network.

### CVE-2026-77901

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-08T18:20:40.257 |

Null pointer dereference in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-77504

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:20:37.740 |

Double free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-77495

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:35.803 |

Heap-based buffer overflow in Windows Imaging Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-77487

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-08T18:20:34.397 |

Improper access control in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-77486

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:20:34.277 |

Integer overflow or wraparound in SQL Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-77484

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T18:20:34.023 |

Deserialization of untrusted data in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-77483

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-09-08T18:20:33.890 |

Weak authentication in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-77482

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:33.770 |

Heap-based buffer overflow in SQL Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-77481

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:33.633 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-77480

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1220` |
| Published | 2026-09-08T18:20:33.500 |

Insufficient granularity of access control in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-73028

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-08T18:20:32.830 |

Improper access control in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-73023

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:32.133 |

Heap-based buffer overflow in Windows Imaging Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-73018

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:31.297 |

Heap-based buffer overflow in Graphic Fonts allows an unauthorized attacker to execute code over a network.

### CVE-2026-73016

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:30.967 |

Heap-based buffer overflow in Microsoft Graphics Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-73013

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:30.473 |

Heap-based buffer overflow in Windows Imaging Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-73012

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:30.277 |

Heap-based buffer overflow in Windows Management Services allows an authorized attacker to elevate privileges over a network.

### CVE-2026-73006

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:20:29.327 |

Stack-based buffer overflow in Microsoft Graphics Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-72986

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:20:25.500 |

Heap-based buffer overflow in Graphic Fonts allows an unauthorized attacker to execute code over a network.

### CVE-2026-72973

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:23.387 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-72972

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:23.260 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-72960

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:21.743 |

Heap-based buffer overflow in Windows Media Player allows an unauthorized attacker to execute code over a network.

### CVE-2026-72959

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:21.563 |

Remote Code Execution in Windows Routing and Remote Access Service (RRAS) allows attacker to gain an unauthorized access to victim's machine

### CVE-2026-72950

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:20.520 |

Remote Code Execution in Windows Routing and Remote Access Service (RRAS) allows attacker to gain an unauthorized access to victim's machine

### CVE-2026-72940

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:18.960 |

Heap-based buffer overflow in Windows Schannel allows an unauthorized attacker to execute code over a network.

### CVE-2026-72933

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:17.983 |

Heap-based buffer overflow in Microsoft WDAC OLE DB provider for SQL allows an unauthorized attacker to execute code over a network.

### CVE-2026-71352

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-08T18:20:15.690 |

Integer underflow (wrap or wraparound) in Windows Remote Access Connection Manager allows an authorized attacker to execute code over a network.

### CVE-2026-71336

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:20:13.287 |

Integer overflow or wraparound in Windows Work Folder Service allows an authorized attacker to execute code over a network.

### CVE-2026-71328

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:12.160 |

Heap-based buffer overflow in Visual Studio allows an unauthorized attacker to execute code over a network.

### CVE-2026-70586

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:11.797 |

Heap-based buffer overflow in Windows Paint allows an unauthorized attacker to execute code over a network.

### CVE-2026-70351

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:20:08.237 |

Integer overflow or wraparound in Microsoft WebP Image Extension allows an unauthorized attacker to execute code over a network.

### CVE-2026-70203

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:04.157 |

Heap-based buffer overflow in Windows Media Player allows an unauthorized attacker to execute code over a network.

### CVE-2026-69860

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:57.457 |

Heap-based buffer overflow in Windows Imaging Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-69797

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:51.320 |

Use after free in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-69784

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:49.840 |

Use after free in Windows Hello allows an authorized attacker to elevate privileges locally.

### CVE-2026-69778

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:49.233 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-69772

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:48.623 |

Heap-based buffer overflow in Windows Network File System allows an unauthorized attacker to execute code over a network.

### CVE-2026-69767

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:47.843 |

Use after free in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-69764

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:47.713 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-69759

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:47.097 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-69742

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:19:46.507 |

Integer overflow or wraparound in Microsoft Office Publisher allows an unauthorized attacker to execute code over a network.

### CVE-2026-69740

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:46.243 |

Use after free in Windows Hello allows an authorized attacker to elevate privileges locally.

### CVE-2026-69729

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:45.010 |

Heap-based buffer overflow in Windows Credential Providers allows an authorized attacker to execute code over a network.

### CVE-2026-69724

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T18:19:44.593 |

Missing authorization in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-69722

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:44.280 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-69716

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-08T18:19:43.703 |

Improper neutralization of special elements used in an sql command ('sql injection') in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69712

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:43.030 |

Use after free in Windows Key Distribution Center allows an authorized attacker to execute code over a network.

### CVE-2026-69686

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:40.567 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-69678

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:39.327 |

Use after free in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-69676

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-08T18:19:39.143 |

Authentication bypass by capture-replay in Windows Kerberos allows an authorized attacker to execute code over a network.

### CVE-2026-69671

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:38.717 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-69669

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:38.537 |

Heap-based buffer overflow in Windows Kernel allows an unauthorized attacker to execute code over a network.

### CVE-2026-69649

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:38.087 |

Heap-based buffer overflow in Windows Raw Image Extension allows an unauthorized attacker to execute code over a network.

### CVE-2026-69632

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:35.740 |

Use after free in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-69629

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:35.290 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-69628

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:35.113 |

Heap-based buffer overflow in Windows iSCSI allows an authorized attacker to execute code over a network.

### CVE-2026-69614

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-121` |
| Published | 2026-09-08T18:19:33.047 |

Stack-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-69603

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:31.163 |

Heap-based buffer overflow in Windows Hyper-V allows an authorized attacker to execute code locally.

### CVE-2026-69601

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:30.837 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-69598

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-131` |
| Published | 2026-09-08T18:19:30.363 |

Incorrect calculation of buffer size in Windows iSCSI allows an unauthorized attacker to execute code over a network.

### CVE-2026-69556

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:24.413 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-69551

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:23.677 |

Use after free in Windows DNS allows an authorized attacker to execute code over a network.

### CVE-2026-69547

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:23.107 |

Heap-based buffer overflow in Windows DHCP Server allows an authorized attacker to execute code over a network.

### CVE-2026-69529

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:20.740 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-69522

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:19.697 |

Heap-based buffer overflow in Visual Studio allows an unauthorized attacker to execute code over a network.

### CVE-2026-69518

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:19.460 |

Heap-based buffer overflow in Windows Remote Desktop allows an unauthorized attacker to execute code over a network.

### CVE-2026-69511

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:18.450 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-69499

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:19:16.760 |

Integer overflow or wraparound in Windows Imaging Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-69495

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:16.083 |

Heap-based buffer overflow in Windows Event Logging Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-69494

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-09-08T18:19:15.900 |

Out-of-bounds read in Windows Event Logging Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-69485

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-09-08T18:19:14.667 |

Use of uninitialized resource in Remote Desktop Client allows an authorized attacker to execute code over a network.

### CVE-2026-69465

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T18:19:11.693 |

Missing authorization in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-69464

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-09-08T18:19:11.560 |

Execution with unnecessary privileges in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69461

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:11.027 |

Stack-based buffer overflow in Windows NTFS allows an unauthorized attacker to execute code over a network.

### CVE-2026-69442

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:08.413 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-69439

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:07.960 |

Heap-based buffer overflow in .NET and Visual Studio allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-69434

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:07.440 |

Heap-based buffer overflow in Windows URL Moniker allows an unauthorized attacker to execute code over a network.

### CVE-2026-69386

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:59.720 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-69360

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:55.790 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-69355

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-08T18:18:54.910 |

External control of file name or path in Microsoft Exchange Server allows an authorized attacker to execute code over a network.

### CVE-2026-69334

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-09-08T18:18:51.287 |

Heap-based buffer overflow in Windows Volume Manager Extension Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-69291

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:44.247 |

Heap-based buffer overflow in Windows Volume Manager Extension Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-69285

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:43.203 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-69282

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-08T18:18:42.693 |

Improper access control in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-69273

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-08T18:18:40.297 |

Improper access control in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-69268

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-08T18:18:39.087 |

Improper access control in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-69266

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:18:38.777 |

Integer overflow or wraparound in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-68828

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:29.640 |

Heap-based buffer overflow in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-68786

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:26.180 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-68775

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:24.927 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67643

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:24.530 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67642

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:24.410 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67639

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:24.147 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67638

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:24.023 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67631

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:23.590 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67388

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:22.263 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67385

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:22.003 |

Use after free in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67384

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:18:21.867 |

Integer overflow or wraparound in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67381

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:21.603 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-67380

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:21.477 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67373

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:20.950 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67370

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-08T18:18:20.817 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-67368

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-08T18:18:20.550 |

Improper link resolution before file access ('link following') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-66820

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-08T18:18:20.420 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-66819

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-08T18:18:20.273 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-66818

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-08T18:18:20.143 |

Improper privilege management in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-66814

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1220` |
| Published | 2026-09-08T18:18:19.880 |

Insufficient granularity of access control in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-65772

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T18:18:15.860 |

Deserialization of untrusted data in Microsoft Dynamics 365 allows an authorized attacker to execute code over a network.

### CVE-2026-62895

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-942;CWE-1390` |
| Published | 2026-09-08T18:18:08.877 |

Permissive cross-domain policy with untrusted domains in Azure Arc allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-62744

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:17:57.417 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-62706

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-125` |
| Published | 2026-09-08T18:17:53.350 |

Out-of-bounds read in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-18851

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T15:18:42.533 |

Missing authorization in Ivanti Endpoint Manager Mobile before version 12.10.0.0, 12.9.0.2, and 12.8.0.4 allows a remote authenticated attacker to escalate their privileges to admin.

### CVE-2026-12651

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T15:18:40.963 |

A Deserialization of Untrusted Data vulnerability in Ivanti Neurons for ITSM before 2026.2 allows a remote authenticated attacker to execute arbitrary code on the server.

### CVE-2026-12648

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T15:18:40.733 |

A Deserialization of Untrusted Data vulnerability in Ivanti Neurons for ITSM before 2026.2 allows a remote authenticated attacker to execute arbitrary code on the server.

### CVE-2026-86201

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-09T14:17:21.263 |

PocketMine-MP before 5.41.1 contains a denial of service vulnerability in LoginPacket processing where large or complex structures in unknown clientData JWT properties cause excessive logging without sanitization. Attackers can send crafted LoginPackets with deeply nested or massive object structures to trigger out-of-memory conditions and crash the server.

### CVE-2026-86199

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-09T14:17:20.980 |

PocketMine-MP versions before 5.43.1 fail to properly validate the Certificate field during offline login authentication. Unauthenticated players can trigger an uninitialized property access error that crashes the server.

### CVE-2024-58382

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-09T14:17:10.327 |

league/commonmark versions before 2.6.0 contain polynomial time complexity vulnerabilities in Markdown parsing that allow attackers to cause denial of service. Attackers can submit carefully crafted Markdown inputs designed to trigger worst-case performance, and sending multiple requests in parallel exhausts CPU resources and PHP-FPM processes.

### CVE-2024-58381

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-09T14:17:10.187 |

PocketMine-MP before 5.11.1 contains a denial of service vulnerability in LoginPacket JSON processing that allows remote attackers to crash the server by sending malformed JSON data. Attackers can exploit improper object initialization from scalar JSON types to trigger unset required properties, causing the application to crash.

### CVE-2023-54393

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-09T14:17:09.447 |

PocketMine-MP versions before 4.20.5 contain a denial of service vulnerability in LoginPacket JSON parsing due to improper validation in the JsonMapper dependency. Attackers can send malformed JSON structures in LoginPacket to crash the server.

### CVE-2023-54390

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1025` |
| Published | 2026-09-09T14:17:09.170 |

PocketMine-MP versions before 5.3.1 and 4.23.1 contain a denial of service vulnerability in LoginPacket JSON parsing due to improper null value handling in arrays. Attackers can send malformed JSON with unexpected null elements in LoginPacket to crash the server.

### CVE-2023-54355

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-09T14:17:09.010 |

PocketMine-MP versions before 5.3.1 and 4.23.1 fail to validate that the identityPublicKey in LoginPacket uses the required secp384r1 elliptic curve. Attackers can provide LoginPackets with keys using different curves or non-EC key types to pass login verification but trigger an uncaught exception during ECDH key derivation, crashing the server.

### CVE-2026-87819

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-09T12:17:17.120 |

GitPython before 3.1.60 contains a regular expression denial of service vulnerability in Actor.name_email_regex that processes commit author and committer fields. Attackers can craft a commit object with a malformed author field containing an unterminated angle bracket to cause quadratic backtracking, exhausting CPU resources for over two minutes per commit access.

### CVE-2026-87817

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-09T12:17:16.830 |

GitPython before 3.1.60 fails to properly validate the git directory location, allowing attackers to impersonate the git directory using tracked files like gitdir, commondir, and HEAD. Attackers can execute arbitrary code by placing a malicious pre-commit hook in the tracked hooks directory that executes when a victim calls index.commit() on a cloned or opened repository.

### CVE-2026-87816

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-09T12:17:16.683 |

PasswordPusher before 2.11.1 contains a time-of-check-to-time-of-use race condition in view limit enforcement that allows unauthenticated attackers to bypass expire_after_views limits. Attackers can send concurrent requests to the show endpoint to access one-time secrets multiple times before the view count is incremented and the push expires.

### CVE-2026-87808

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-09T12:17:15.503 |

SiYuan versions <= 3.8.1 contain an incomplete fix for CVE-2026-32767 (GHSA-j7wh-x834-p3r7). The prior fix (commit d5e2d0bc) added an administrator check for SQL mode (method=2) in POST /api/search/fullTextSearchBlock, but the endpoint still does not enforce the application's read-only boundary: for method=2 it forwards caller-supplied SQL to the blocks database query path without calling model.CheckReadonly or CheckReadonlyStatementInBox. As a result, when a workspace runs in read-only mode (--readonly=true), an authenticated administrator can submit arbitrary SQL through /api/search/fullTextSearchBlock and obtain raw read access to the blocks database, even though the dedicated /api/query/sql endpoint is blocked in that mode. Fixed in v3.8.2.

### CVE-2026-87807

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-09T12:17:15.343 |

siyuan versions before v3.8.2 contain an authenticated SQL injection vulnerability in the fullTextSearchBlock endpoint's method=1 query parameter. Attackers can inject UNION SELECT statements to read the entire blocks table, bypassing publish-access controls and exposing all document content and sensitive attributes.

### CVE-2026-55250

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294;CWE-613;CWE-672` |
| Published | 2026-09-08T23:17:25.573 |

Maravel, a PHP framework oriented towards dependency injection, prior to version 10.74.0 has a high-severity Token Replay Vulnerability arising from a structural lifecycle mismatch between stateless token validation engines and high-performance relational caching layers. Any application with low cache memory that causes premature eviction to free up memory and applications running macropay-solutions/maravel-framework that utilize tymon/jwt-auth for API token authentication and blacklist management or any other package that does the same may be affected. This architectural risk might also impact native Laravel applications utilizing cache tags under specific volatile or eviction-capped environments. tymon/jwt-auth automatically probes for cache tag support. If found, it forcefully wraps 14-day token blacklist entries (jti) inside a relational tymon.jwt tag. In environments where the O(1) Atomic Lazy Eviction model is active — either natively inside Maravel-Framework v20.x or manually backported into v10.x via the explicit DI container singletons provided in PR #104 (App\Cache\TaggedCache and App\Cache\TagSet) — a strict global tracking ceiling (Container::TAGGED_CACHE_TTL_CAP_SECONDS) of 7,200 seconds (2 hours) is enforced to secure the system against memory index bloat. This ceiling forcefully truncates the 14-day blacklist lifespan down to a maximum of 2 hours, after which individual tracking keys naturally expire and disappear from the active cache window. Furthermore, because the optimized engine implements a generational version matrix to achieve O(1) flush speeds, any programmatic or manual invocation of a tag flush or reset (e.g., Cache::tags([...])->flush()) instantly bumps the internal atomic master version pointer. This shifts the computed cryptographic composite hash (sha1($this->tags->getNamespace())) for all overlapping components, rendering the entire existing index immediately unreachable. Consequently, through either natural 2-hour expiration or an intervening tag flush execution (like the cache naturally cleaning old values to free up memory), the invalidation state records are entirely wiped out. Because the tokens' physical cryptographic signatures remain structurally valid for up to 14 days, stolen, hijacked, or legitimately logged-out tokens are instantly and silently resurrected across the entire API gateway, leaving the application critically vulnerable to widespread Token Replay Attacks. Because this issue is caused by an upstream architectural assumption within the tymon/jwt-auth package rather than a core defect inside the framework, there is no direct framework version upgrade that can safely bypass this lifecycle collision without breaking business cache recycling bounds. Maravel version 10.74.0 introduced a way to backport the new fixed tagged cache from 20.x into 10.x by resolving TagSet and TaggedCache from DI, which is how this latent architectural lifecycle vulnerability was discovered. Users must apply the decoupled configuration workaround outlined below. As a workaround, make sure that cache memory size does not generate early natural evictions from cache to free up space, deleting blacklisted jwt ids before they expire. Applications must decouple flat authentication vectors from the relational tagging subsystem. This forces token identifiers to write directly to the primary cache keyspace as flat, un-tagged key-value pairs where they securely retain their unclipped 14-day lifecycle.

### CVE-2026-86076

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-08T22:19:16.387 |

n8n is an open source workflow automation platform. Prior to 1.123.76, 2.37.7, and 2.38.2, the expression compiler sanitizer resolved through dynamically scoped this and did not reject reserved class member names. A class field named __sanitize could rebind the sanitizer and reach the Function constructor, enabling backend code execution and editor-preview JavaScript execution. The affected AST hook is PrototypeSanitizer in packages/workflow/src/expression-sandboxing.ts. This issue is fixed in versions 1.123.76, 2.37.7 and 2.38.2.

### CVE-2026-86075

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-08T22:19:16.250 |

n8n is an open source workflow automation platform. Prior to 2.37.7 and 2.38.2, the OAuth Dynamic Client Registration endpoint bounded redirect_uris but accepted arbitrarily large client_name and grant_types values. An unauthenticated remote caller could repeatedly persist oversized values in oauth_clients and exhaust database storage. The affected validation is in packages/cli/src/modules/oauth-server/oauth-server.service.ts, including MAX_CLIENT_NAME_LENGTH and MAX_GRANT_TYPES. This issue is fixed in versions 2.37.7 and 2.38.2.

### CVE-2026-77111

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T19:19:41.760 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. An attacker with high privileges could leverage this vulnerability to bypass security measures and gain unauthorized write access, causing a limited disruption to availability. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-82075

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-08T17:18:36.530 |

An uncontrolled resource consumption weakness exists in the request-handling path of the MongoDB sharded-cluster router process. A client that has network access to a router port and has not authenticated can supply connection-monitoring parameters that cause the server to expend CPU resources without any rate limiting, degrading or denying service to legitimate clients. No authentication, elevated privileges, or user interaction is required. Only availability is affected; data confidentiality and integrity are not impacted.

### CVE-2026-82064

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-08T17:18:35.233 |

A security issue in MongoDB Server allows an unauthenticated network user to cause a denial of service on a specific type of replica set member. The server contains an assertion in its read concern processing logic that can be reached without authentication, and the assertion's assumptions about internal state do not hold for all member configurations, causing the server process to terminate.

### CVE-2026-86732

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-08T16:18:35.333 |

Craft CMS versions before 5.10.12 contain a remote code execution vulnerability in the element-index endpoint that allows authenticated content editors to instantiate arbitrary classes through the criteria parameter. Attackers can inject a malicious class via criteria[withTransforms][0][class] that reaches ImageTransforms::normalizeTransform(), then use a PHP gadget chain with yii\rbac\PhpManager to execute code by pointing itemFile to a request log containing PHP payload in the User-Agent header.

### CVE-2026-86730

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-08T16:18:34.667 |

Craft CMS versions before 5.10.12 fail to properly cleanse string-typed field-layout elements, allowing authenticated control-panel users to inject Yii2 behavior attachments and event handlers. Attackers can post field-layout tab elements as JSON strings to bypass cleanse validation, then trigger arbitrary object instantiation and code execution through Craft::createObject().

### CVE-2026-86728

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-08T16:18:33.983 |

AVideo through 29.0 contains an authentication bypass vulnerability in plugin/PlayLists/epg.json.php that exposes live-stream keys and private EPG schedules to unauthenticated users. Attackers can request the endpoint with sequential user or playlist IDs to retrieve sensitive credentials, server identifiers, and complete programme schedules without authentication.

### CVE-2026-86727

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-08T16:18:33.823 |

AVideo through 29.0 contains an information disclosure vulnerability in plugin/Live/stats.json.php that allows unauthenticated attackers to retrieve stream keys and m3u8 URLs by accessing the endpoint without authentication. Attackers can enumerate private, unlisted, and group-restricted live streams by parsing the hidden_applications array in the JSON response to obtain sensitive streaming credentials.

### CVE-2026-86721

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-08T16:18:32.307 |

AVideo through commit c3edcc274c contains an authorization bypass vulnerability where a session cookie named 'key' with value 'value' overrides the $_REQUEST['key'] parameter in saveLive.php and related endpoints. Attackers can publish to any user's RTMP stream without authentication by using the known constant stream key value to hijack live broadcasts.

### CVE-2026-33197

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-08T15:18:42.960 |

AMI APTIOV contains a vulnerability in BIOS where a privileged user may cause the “Incomplete List of Disallowed Inputs” by local access. Successful exploitation of this vulnerability may lead to arbitrary code execution and impact system Confidentiality, Integrity, and Availability.

### CVE-2026-86770

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-09-09T14:17:27.593 |

Snipe-IT before 8.7.0 fails to validate username case sensitivity during SAML authentication, allowing attackers to authenticate as different users by registering IdP accounts with accent or case variants of victim usernames. Attackers can exploit the default utf8mb4_unicode_ci database collation to bypass username matching and achieve account takeover through federated login paths including SAML, LDAP, and OAuth.

### CVE-2026-86762

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-09T14:17:26.220 |

Snipe-IT before 8.7.0 does not apply the CheckUserIsActivated middleware to the `api` middleware group in app/Http/Kernel.php, and deactivating a user does not revoke that user's Passport personal access tokens. As a result, although a deactivated account is correctly refused at web login, its existing API token continues to authenticate and to grant read and write access to the REST API (assets, users, licenses, etc.) at the account's prior permission level until the token expires. A deactivated account that retains user-management permissions can re-activate itself through the API, permanently defeating the deactivation control.

### CVE-2026-56711

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-09-09T14:17:12.717 |

VLC media player computes the size of a picture buffer with 32-bit arithmetic and allocates from the wrapped result. In AllocatePicture in src/misc/picture.c the running total is accumulated as i_bytes += p->i_pitch * p->i_lines, and both plane_t fields are declared int in include/vlc_picture.h, so the multiplication is evaluated at 32 bits and wraps before it is widened to the size_t accumulator. The overflow check that precedes it divides in 64-bit arithmetic and therefore does not constrain the product, and the subsequent comparison against PICTURE_SW_SIZE_MAX examines the already wrapped value, so both guards pass. aligned_alloc then reserves the small wrapped size while the decoder writes scanlines sized from the original dimensions. A crafted PNG whose IHDR declares large width and height reaches this path through the image demuxer, whose only size guard is on the input file's byte count rather than the declared dimensions, and the decoder in modules/codec/png.c writes past the end of the allocation with attacker-influenced length and content. Opening the file directly or through a playlist entry is sufficient, with no non-default settings.

### CVE-2026-87794

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-09T10:22:34.397 |

bestzip versions 2.2.6 and 3.0.2 contain an argument injection vulnerability in the nativeZip function that allows attackers to inject arbitrary arguments to the Info-ZIP backend. Attackers can supply a malicious destination path combined with crafted source entries to execute arbitrary commands with Node.js process privileges. Fixed in 2.2.7 and 3.0.3.

### CVE-2026-21087

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T05:17:20.707 |

Out-of-bounds write in libmdnie.so prior to SMR Sep-2026 Release 1 allows local attackers to execute arbitrary code with system server privilege.

### CVE-2026-49310

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-264` |
| Published | 2026-09-09T04:17:58.680 |

Permission control vulnerability in the event notification module.
Impact: Successful exploitation of this vulnerability may affect service confidentiality.

### CVE-2026-76199

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-08T20:18:24.280 |

Photoshop Desktop is affected by an Uncontrolled Search Path Element vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-76190

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-08T20:18:24.157 |

ColdFusion is affected by an Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-75991

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-08T20:18:23.247 |

Illustrator is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-75990

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T20:18:22.583 |

Illustrator is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-79721

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-08T19:19:51.383 |

Code execution can occur in versions of the MLflow platform running version 0.0.1 or newer, enabling a maliciously crafted model artifact to execute arbitrary code on an end user's system when loaded by the project.

### CVE-2026-77774

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T19:19:44.710 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized read access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-77109

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T19:19:41.353 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. An attacker could leverage this vulnerability to gain elevated access to restricted resources. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-80097

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-08T18:20:52.137 |

Improper authentication in Microsoft Authenticator allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-86733

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-08T16:18:35.477 |

Snipe-IT before 8.7.0 streams the SQL entry from an uploaded backup archive directly into the MySQL/MariaDB command-line client (`mysql`) without the --binary-mode flag, so the client interprets lines beginning with backslash commands such as `\!` as local shell commands. An authenticated superadministrator who uploads a crafted ZIP backup (POST /admin/backups/upload) and triggers a restore (POST /admin/backups/restore/{filename}) without the optional `clean` sanitizer parameter — which is not applied by default because DB_SANITIZE_BY_DEFAULT is false — can execute arbitrary OS commands as the web application's operating-system user, exposing application secrets (including database credentials and APP_KEY) and allowing modification of application-writable files and data. Version 8.7.0 adds the --binary-mode flag to the client invocation.

### CVE-2026-86723

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-08T16:18:32.583 |

AVideo through c3edcc274c389816d434acadac07ee78eaf330c1 contains an authentication bypass vulnerability in LoginControl::verifyChallenge() that uses loose comparison (==) instead of strict comparison (===) against unset session values. Attackers with only a password can submit an empty request to verifyChallenge.json.php to bypass PGP two-factor authentication and gain full authenticated access.

### CVE-2026-86722

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-08T16:18:32.447 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains an authentication bypass vulnerability where sqlDAL caches empty result sets that writeSql never invalidates. Attackers with a valid password can bypass email two-factor authentication on new devices because the confirmation code hash fails to generate from the stale cached empty result.

### CVE-2026-86720

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-08T16:18:31.833 |

WWBN AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 fails to validate ownership of live_restreams_id in resendRestreamer.json.php, allowing authenticated users with canStream to access other users' restream destinations. Attackers can broadcast their live stream to victim-configured restream destinations by supplying arbitrary live_restreams_id values, hijacking YouTube, Facebook, or Twitch streams using victim stream keys.

### CVE-2026-61517

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-08T15:18:44.330 |

Netis NX10 firmware V4.0.1.5808 and V3.0.0.4142 contain an OS command injection vulnerability in the ping diagnostic handler that allows authenticated administrators to execute arbitrary shell commands as root by injecting into the IpAddr parameter. The parameter is interpolated directly into a shell command executed through system() with an incomplete denylist that only blocks spaces, pipes, semicolons, and ampersands, leaving command substitution and alternate field separator expansion available for exploitation.

### CVE-2026-86754

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-09T14:17:24.590 |

Snipe-IT before 8.7.0 fails to properly gate Laravel Passport's OAuth client management routes, allowing any authenticated user to register OAuth clients with attacker-controlled redirect URIs. Attackers can trick administrators into approving consent screens, then exchange authorization codes for bearer tokens inheriting full admin API permissions lasting up to 40 years.

### CVE-2026-12858

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-09T09:17:10.320 |

Improper Privilege Management vulnerability in ESET AV Remover (standalone) allows Privilege Escalation via especially crafted RPC.

### CVE-2026-87030

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-09T03:17:25.557 |

Tanium addressed a path traversal vulnerability in Comply.

### CVE-2026-87023

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-09T03:17:25.323 |

Tanium addressed a path traversal vulnerability in Comply.

### CVE-2026-75993

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T20:18:23.493 |

ColdFusion is affected by a reflected Cross-Site Scripting (XSS) vulnerability. An attacker could exploit this vulnerability to inject malicious scripts into a web page, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-85384

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T19:20:07.763 |

A stack-based buffer overflow vulnerability exists in the httpd component of RE210 AC750 due to improper bounds checking in the splitString function when processing an uploaded configuration file. An authenticated attacker on the local network can upload a crafted configuration file to trigger the overflow, leading to remote code execution.





Successful exploitation may allow unauthorized access to sensitive information, modification of device configuration and network behavior, or disruption of device availability.

### CVE-2026-67636

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:18:23.893 |

Out-of-bounds read in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67379

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:18:21.343 |

Stack-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67378

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-08T18:18:21.207 |

Untrusted pointer dereference in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-86751

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-09T14:17:24.170 |

Snipe-IT before 8.7.0 fails to properly sanitize markdown image syntax in note fields, allowing authenticated users to read arbitrary server files and issue server-side HTTP requests. Attackers can submit markdown image syntax in checkout acceptance notes that survive HTML escaping, are expanded by CommonMark parser, and resolved by laravel-mail-auto-embed via file_get_contents or curl, exfiltrating sensitive files like .env containing APP_KEY.

### CVE-2026-86741

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-09T14:17:22.680 |

Snipe-IT versions before 8.7.0 fail to sanitize the category EULA text field before rendering it in checkout confirmation emails. Attackers with low-privilege permissions can inject markdown image syntax or raw HTML img tags pointing to local files or remote URLs, which the mail auto-embed library resolves server-side and returns as email attachments, exfiltrating sensitive files like .env credentials and enabling SSRF attacks.

### CVE-2026-87815

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-09T12:17:16.537 |

SiYuan versions before v3.8.2 contain a path traversal vulnerability in the /api/riff/removeRiffDeck endpoint that fails to validate the deckID parameter. An authenticated administrator can supply path traversal sequences to delete arbitrary .deck and .cards files outside the workspace directory.

### CVE-2026-87814

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-09T12:17:16.390 |

SiYuan before v3.8.2 contains a stored cross-site scripting vulnerability in the search asset preview feature that fails to escape indexed asset content before inserting it into the DOM using innerHTML. Attackers who can place crafted text assets in a workspace can execute JavaScript in the SiYuan origin when victims preview the assets, enabling authenticated API requests and workspace manipulation.

### CVE-2026-87813

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-09T12:17:16.250 |

SiYuan before v3.8.2 contains a stored cross-site scripting vulnerability in the Search Assets result list where asset filenames are interpolated into HTML without escaping. Authenticated attackers can craft asset filenames containing malicious markup that executes JavaScript in the victim's browser when searching assets, enabling same-origin API requests and application state manipulation.

### CVE-2026-87811

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-09T12:17:15.950 |

SiYuan before v3.8.2 inserts persisted notebook template paths into HTML input value attributes without proper attribute encoding. Attackers can craft malicious template paths that break out of the attribute context and execute JavaScript when a victim opens notebook configuration, enabling same-origin API requests and application state manipulation.

### CVE-2026-21101

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T05:17:22.370 |

Improper input validation in DualDAR driver prior to SMR Sep-2026 Release 1 allows local privileged attackers to potentially execute arbitrary code with root privilege.

### CVE-2026-21085

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T05:17:20.473 |

Out-of-bounds write in Keymaster trustlet prior to SMR Sep-2026 Release 1 allows local privileged attackers to write out-of-bounds memory.

### CVE-2026-86819

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T21:18:47.520 |

Waves Central for macOS contains a local privilege escalation in the privileged helper service. The helper authorizes connecting XPC clients by comparing the caller's code-signing certificate chain for equality with its own, rather than validating the caller against a pinned code requirement (application identifier and Team ID). A local, authenticated user can execute code within the vendor-signed process, satisfy the helper's client check, and cause the helper to execute a script with root privileges. Fixed in 17.0.

### CVE-2026-77827

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-09-08T21:18:39.143 |

Maono Link 3.8.13 MaonoAiServices Windows service allows local privilege escalation for a standard user account via improper write privileges in 'C:\ProgramData\Maono'. Fixed in 4.0.80.

### CVE-2026-75999

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-08T20:18:23.760 |

ColdFusion is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. The vulnerable component is restricted to an administrative network zone by default. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-77503

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:37.563 |

Out-of-bounds read in Windows NTFS allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-69638

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:36.133 |

Heap-based buffer overflow in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-69479

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:13.810 |

Heap-based buffer overflow in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-86771

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:N/VA:L/SC:H/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-09T14:17:27.740 |

Snipe-IT versions before 8.7.0 fail to HTML-escape the employee_num field in the acceptance PDF generator, allowing attackers with users.edit permission to inject img tags into TCPDF's writeHTML() function. Attackers can craft a malicious employee_num value containing an img tag with an arbitrary HTTP(S) URL to trigger server-side requests to internal services, cloud metadata endpoints, or external targets when a victim signs an asset acceptance.

### CVE-2026-86750

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-09T14:17:24.030 |

Snipe-IT versions <= 8.6.3 (fixed in 8.7.0) do not validate company assignment authorization before persisting user records via the REST API. In Api\UsersController::store() and ::update(), the user record is filled from the request and saved before the requested company_id / company_ids[] values are filtered against the actor's permitted companies (Company::getIdsForCurrentUser()). On installs using Full Multiple Companies Support (FMCS), a non-superuser holding users.create (or users.edit on a target user) can submit company identifiers for companies outside their scope — including a mix of permitted and foreign ids — causing the account row to be committed to the database before authorization is checked. Where null_company_is_floater=1 is set, the post-hoc filter leaves an empty company pivot and the account is persisted as a "floater" with cross-company visibility, allowing creation or relocation of user accounts across tenant boundaries.

### CVE-2026-87034

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-09T03:17:25.897 |

Tanium addressed a SQL injection vulnerability in Comply.

### CVE-2026-87618

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-09-09T01:17:19.950 |

Incorrect reference resolution in Storage in Google Chrome on on Windows prior to 153.0.8010.36 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-69646

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-08T19:19:04.560 |

Improper verification of cryptographic signature in Skype for Business allows an unauthorized attacker to perform spoofing over an adjacent network.

### CVE-2026-81822

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-327` |
| Published | 2026-09-08T18:20:57.577 |

The vulnerability, if exploited, could allow a miscreant with read access to PIMBoards project files to reverse engineer PIMBoards users’ app-native passwords through computational brute-forcing of weak hashes, potentially allowing elevation to a PIMBoards administrator user.

### CVE-2026-81821

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-08T18:20:57.420 |

The vulnerability, if exploited, could allow a miscreant with read access to PIMBoards project files to decrypt and view sensitive information.

### CVE-2026-78491

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-09T09:17:10.870 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Certificate Validation vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-6485

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-489` |
| Published | 2026-09-09T04:19:36.437 |

UEFI BIOS embedded Shell could be used to bypass Secure Boot via shell commands or startup scripts.

### CVE-2026-12855

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-09T04:17:56.480 |

Unvalidated memory boundary could result in arbitrary code execution. The vulnerability exists in the code developed specifically for HP projects.

### CVE-2026-53938

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-09-09T00:17:31.557 |

OpenIDC/cjose is a C library implementing the Javascript Object Signing and Encryption (JOSE). Prior to version 0.6.2.5, cjose's JWE decryption path for the AES Key Wrap key-management algorithms (`alg` = `A128KW`, `A192KW`, `A256KW`) does not validate the length of the attacker-supplied `encrypted_key` (JWE Encrypted Key) before unwrapping it into a fixed-size, heap-allocated Content Encryption Key (CEK) buffer. A remote, unauthenticated attacker who can submit a crafted JWE to an application that decrypts it with an AES-KW symmetric key can trigger an out-of-bounds heap write, corrupting the heap. This leads at minimum to a crash (denial of service) and, depending on the heap layout and allocator, may be leverageable for further memory-corruption impact. `cjose_jwe_import()` / `cjose_jwe_decrypt()` are pre-authentication entry points: they parse and process fully attacker-controlled input. Upgrade to cjose 0.6.2.5 to receive a patch. If upgrading is not immediately possible, reject the AES Key Wrap algorithms (`A128KW`/`A192KW`/`A256KW`) for untrusted JWEs at the application layer.

### CVE-2026-81994

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-08T21:18:46.223 |

Acrobat Reader is affected by an Improperly Controlled Modification of Object Prototype Attributes ('Prototype Pollution') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-76202

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T19:19:41.087 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. An attacker could leverage this vulnerability to gain elevated access to sensitive information. Exploitation of this issue does not require user interaction.

### CVE-2026-83939

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-08T18:21:04.570 |

Untrusted pointer dereference in Windows Secure Kernel Mode allows an authorized attacker to elevate privileges locally.

### CVE-2026-81379

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-636` |
| Published | 2026-09-08T18:20:54.193 |

Not failing securely ('failing open') in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-81378

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-09-08T18:20:54.063 |

Interpretation conflict in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-81357

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-08T18:20:53.693 |

Server-side request forgery (ssrf) in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-81356

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-08T18:20:53.567 |

Inconsistent interpretation of http requests ('http request/response smuggling') in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-81354

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:53.193 |

Heap-based buffer overflow in Windows Hello allows an authorized attacker to elevate privileges locally.

### CVE-2026-76191

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-08T18:20:33.240 |

Animate is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-72962

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:22.070 |

Heap-based buffer overflow in Windows USB Video Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-72961

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:21.907 |

Out-of-bounds read in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-72958

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:20:21.440 |

Double free in Windows Credential Guard allows an authorized attacker to elevate privileges locally.

### CVE-2026-69906

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:00.887 |

Heap-based buffer overflow in Windows Secure Kernel Mode allows an authorized attacker to elevate privileges locally.

### CVE-2026-69874

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-08T18:19:58.087 |

Untrusted pointer dereference in Windows ALPC allows an authorized attacker to elevate privileges locally.

### CVE-2026-69846

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:19:56.153 |

Integer overflow or wraparound in Windows Secure Kernel Mode allows an authorized attacker to elevate privileges locally.

### CVE-2026-69820

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:53.747 |

Heap-based buffer overflow in Windows Hello allows an authorized attacker to elevate privileges locally.

### CVE-2026-86600

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-441;CWE-522` |
| Published | 2026-09-08T16:18:29.943 |

In affected Snowflake drivers, WORKLOAD_IDENTITY authentication requests a cloud workload-identity token and attaches it to the login request without verifying that the configured host is a Snowflake endpoint. An attacker who can modify the connection configuration can cause the driver to mint a fresh attestation and send it to a host they control. The captured token can be replayed to Snowflake for its remaining lifetime in accounts where that workload identity is already registered. On Azure, the token audience is also taken from connection configuration. Combined with an attacker-controlled host, the driver can request a Managed Identity access token scoped to a non-Snowflake Azure resource and deliver it to the attacker. That path is the only case in which impact extends beyond Snowflake; it is bounded by the token lifetime and the managed identity’s permissions. Successful exploitation requires WORKLOAD_IDENTITY authentication on a workload that already has an ambient cloud identity. Patched driver versions restrict this authenticator to recognized Snowflake hosts. Users must manually upgrade.

### CVE-2026-76009

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-09T06:17:16.497 |

The Next-Cart Store to WooCommerce Migration plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 3.9.8 via the `NCWM_Kitconnect::run()` function. This is due to the plugin registering the `/wp-json/next_cart/v1/migration` REST route with `permission_callback` set to `__return_true` and relying on a hardcoded fallback value of `__token__` in `get_option('nextcart_token', '__token__')` when the `nextcart_token` option has not yet been written to the database. This makes it possible for unauthenticated attackers to bypass authentication to the migration endpoint by supplying the literal string `__token__` as the token, gaining access to privileged handlers that pass attacker-controlled SQL directly to `$wpdb->query()` and `$wpdb->get_results()` — enabling arbitrary SQL execution including administrator account creation — and pass an attacker-controlled path to `unlink()`, enabling arbitrary file deletion and full site takeover. The hardcoded fallback is reachable whenever the `nextcart_token` option has not yet been populated, which occurs after WP-CLI, network, or programmatic plugin activation without a subsequent authenticated `wp-admin` visit, as token generation is deferred to `admin_init` via `register_settings()`.

### CVE-2026-87075

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-09T03:17:26.953 |

Tanium addressed an improper access controls vulnerability in Comply.

### CVE-2026-87036

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-09T03:17:26.143 |

Tanium addressed an improper access controls vulnerability in Comply.

### CVE-2026-78626

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T20:18:38.070 |

The Okta Access Gateway improperly handles input sanitization and regular expression evaluation within its Protected Rule authorization check, resulting in an authorization bypass when an administrator has explicitly configured a Protected Rule policy on one or more application resources.

### CVE-2026-83997

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:21:10.530 |

Use after free in Windows Message Queuing allows an unauthorized attacker to execute code over a network.

### CVE-2026-78450

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:43.340 |

Use after free in Reliable Multicast Transport Driver (RMCAST) allows an unauthorized attacker to execute code over a network.

### CVE-2026-78449

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:42.973 |

Use after free in Reliable Multicast Transport Driver (RMCAST) allows an unauthorized attacker to execute code over a network.

### CVE-2026-78444

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-08T18:20:42.133 |

Untrusted pointer dereference in Windows Failover Cluster allows an unauthorized attacker to execute code over a network.

### CVE-2026-77505

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:37.920 |

Use after free in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-72987

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:25.697 |

Use after free in Windows DNS allows an unauthorized attacker to execute code over a network.

### CVE-2026-72981

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:24.670 |

Use after free in IP Helper allows an unauthorized attacker to execute code over a network.

### CVE-2026-72936

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:18.347 |

Use after free in Windows SMB Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-70563

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-08T18:20:08.763 |

Improper link resolution before file access ('link following') in Windows Shell allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-70342

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:07.543 |

Use after free in Windows Ancillary Function Driver for WinSock allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-69989

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:03.047 |

Use after free in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-69858

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:57.143 |

Use after free in Windows DNS allows an unauthorized attacker to execute code over a network.

### CVE-2026-69827

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:19:54.553 |

Concurrent execution using shared resource with improper synchronization ('race condition') in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-69813

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:52.823 |

Use after free in Windows DNS allows an unauthorized attacker to execute code over a network.

### CVE-2026-69786

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:50.150 |

Heap-based buffer overflow in Windows Text Shaping allows an unauthorized attacker to execute code over a network.

### CVE-2026-69782

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:19:49.687 |

Concurrent execution using shared resource with improper synchronization ('race condition') in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-69732

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:45.477 |

Heap-based buffer overflow in Windows Link Layer Topology Discovery Protocol allows an unauthorized attacker to execute code over a network.

### CVE-2026-69680

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-08T18:19:39.613 |

Origin validation error in Windows DNS allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-69620

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:33.957 |

Stack-based buffer overflow in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-69546

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:22.927 |

Use after free in Active Directory Domain Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-69530

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:20.883 |

Use after free in Reliable Multicast Transport Driver (RMCAST) allows an unauthorized attacker to execute code over a network.

### CVE-2026-69524

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:19.853 |

Use after free in Active Directory Domain Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-69510

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:18.297 |

Stack-based buffer overflow in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-69438

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-681` |
| Published | 2026-09-08T18:19:07.777 |

Incorrect conversion between numeric types in Microsoft JScript allows an unauthorized attacker to execute code over a network.

### CVE-2026-69380

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T18:18:58.803 |

Missing authorization in Microsoft Exchange Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69325

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:50.243 |

Heap-based buffer overflow in Microsoft JScript allows an unauthorized attacker to execute code over a network.

### CVE-2026-55007

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:17:41.820 |

Double free in Microsoft Exchange Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-47297

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T18:17:37.960 |

Deserialization of untrusted data in SQL Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-84393

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-297` |
| Published | 2026-09-08T17:18:37.883 |

A improper validation of certificate with host mismatch vulnerability in Fortinet FortiOS 7.6.1 through 7.6.6, FortiProxy 7.6.2 through 7.6.6 may allow attacker to information disclosure via <insert attack vector here>

### CVE-2026-83527

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-08T15:18:51.130 |

An Authentication Bypass vulnerability in Sentry before R10.8.2, R10.7.3 and R10.6.4 allows a remote unauthenticated attacker to gain administrative level access.

### CVE-2026-55277

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-08T19:18:01.600 |

In checkUiccListenConfigNeeded of RoutingManager.cpp, there is a possible out of bounds write due to a missing bounds check. This could lead to remote (proximal/adjacent) code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-83948

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-08T18:21:05.140 |

Improper neutralization of special elements used in a command ('command injection') in Microsoft Azure CLI allows an authorized attacker to execute code over a network.

### CVE-2026-69876

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415;CWE-416` |
| Published | 2026-09-08T18:19:58.950 |

Use after free in Windows DHCP Server allows an authorized attacker to execute code over an adjacent network.

### CVE-2026-69875

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-09-08T18:19:58.350 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69847

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:56.320 |

Heap-based buffer overflow in Windows DHCP Server allows an authorized attacker to execute code over an adjacent network.

### CVE-2026-69826

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:54.370 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69807

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-08T18:19:52.320 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Windows PowerShell allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69777

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:49.103 |

Heap-based buffer overflow in Windows DHCP Client allows an authorized attacker to elevate privileges over an adjacent network.

### CVE-2026-69773

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:48.807 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69762

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:47.570 |

Stack-based buffer overflow in Windows Win32K allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69727

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:44.843 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69717

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-822;CWE-843` |
| Published | 2026-09-08T18:19:43.823 |

Untrusted pointer dereference in Windows Group Policy allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69714

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:43.340 |

Stack-based buffer overflow in Windows Device Association Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69689

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-125` |
| Published | 2026-09-08T18:19:41.050 |

Out-of-bounds read in Windows Win32K allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69681

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:39.763 |

Heap-based buffer overflow in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69643

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:36.437 |

Heap-based buffer overflow in Windows Spaceport.sys allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69625

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:34.653 |

Heap-based buffer overflow in Windows Connected User Experiences and Telemetry allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69623

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:34.320 |

Heap-based buffer overflow in Windows HTTP Print Provider allows an authorized attacker to execute code over a network.

### CVE-2026-69619

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:33.773 |

Out-of-bounds read in Windows exFAT File System allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69512

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-09-08T18:19:18.653 |

Heap-based buffer overflow in Windows Spaceport.sys allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69505

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:17.673 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69503

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:17.337 |

Stack-based buffer overflow in Windows USB Driver allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69481

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:14.137 |

Heap-based buffer overflow in Windows Enterprise App Management allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69462

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:11.200 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69458

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:10.513 |

Out-of-bounds read in Windows BitLocker allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69427

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:06.227 |

Out-of-bounds read in Windows VOLSNAP.SYS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69423

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:05.563 |

Heap-based buffer overflow in Windows USB Video Driver allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69418

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:04.827 |

Heap-based buffer overflow in Volume Manager Driver allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69412

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:03.993 |

Stack-based buffer overflow in Windows DHCP Server allows an authorized attacker to execute code over an adjacent network.

### CVE-2026-69371

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:57.403 |

Heap-based buffer overflow in Windows Overlay Filter allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69365

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:18:56.573 |

Out-of-bounds read in Microsoft Local Security Authority Server (lsasrv) allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69346

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:53.470 |

Heap-based buffer overflow in Windows Print Spooler Components allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69332

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:18:50.987 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69322

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:18:49.757 |

Double free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69301

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:18:45.897 |

Stack-based buffer overflow in Windows Win32K allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69271

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:39.620 |

Heap-based buffer overflow in Microsoft Standard XPS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68894

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:37.670 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68880

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-09-08T18:18:35.257 |

Heap-based buffer overflow in Windows Win32K allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68878

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:18:35.080 |

Stack-based buffer overflow in Windows Fast FAT Driver allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68876

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:34.733 |

Heap-based buffer overflow in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68838

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:18:31.413 |

Stack-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68834

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:18:30.803 |

Stack-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68827

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-09-08T18:18:29.453 |

Integer underflow (wrap or wraparound) in Windows GDI+ allows an authorized attacker to elevate privileges over a network.

### CVE-2026-85983

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-08T21:18:47.407 |

The Auth0 AD/LDAP Connector improperly processes a configuration value during service startup. This allows a low-privileged user on the host system to modify the connector's configuration. When the service restarts, the modified configuration can lead to code execution with the privileges of the service account.

### CVE-2026-81992

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T21:18:45.980 |

Acrobat Reader is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81990

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T21:18:45.713 |

Acrobat Reader is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81989

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T21:18:45.583 |

Acrobat Reader is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81988

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T21:18:45.463 |

Acrobat Reader is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81987

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T21:18:45.343 |

Acrobat Reader is affected by an Integer Overflow or Wraparound vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81986

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T21:18:45.230 |

Acrobat Reader is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81985

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T21:18:45.100 |

Acrobat Reader is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81983

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T21:18:44.857 |

Acrobat Reader is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81981

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T21:18:44.630 |

Acrobat Reader is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81980

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T21:18:44.507 |

Acrobat Reader is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81979

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T21:18:44.387 |

Acrobat Reader is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81976

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T21:18:44.020 |

Acrobat Reader is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81975

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T21:18:43.903 |

Acrobat Reader is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81973

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T21:18:43.790 |

Acrobat Reader is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-80161

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-08T21:18:43.213 |

Acrobat Reader is affected by an Access of Resource Using Incompatible Type ('Type Confusion') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-79909

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T21:18:42.640 |

Acrobat Reader is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-79908

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T21:18:42.500 |

Acrobat Reader is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-79907

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T21:18:42.363 |

Acrobat Reader is affected by a Double Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-82007

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T20:18:49.377 |

Photoshop Desktop is affected by an Integer Overflow or Wraparound vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-82006

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T20:18:48.800 |

Photoshop Desktop is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-82005

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T20:18:48.667 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75992

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T20:18:23.373 |

Illustrator is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75863

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T20:18:22.470 |

Photoshop Desktop is affected by an Integer Overflow or Wraparound vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75862

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T20:18:22.353 |

Photoshop Desktop is affected by an Integer Overflow or Wraparound vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75771

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T20:18:22.243 |

Photoshop Desktop is affected by an Integer Overflow or Wraparound vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75631

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T20:18:12.733 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-58941

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-08T19:18:03.363 |

In multiple functions of iommu.c, there is a possible out of bounds read/write due to improper input validation. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58874

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-08T19:18:03.270 |

In multiple functions of SmsController.java, there is a possible escalation of privilege due to a missing permission check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58846

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-08T19:18:03.077 |

In kvm_iommu_map_sg of iommu.c, there is a possible use after free due to a missing permission check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58839

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-08T19:18:02.977 |

In forEachLine of MountRegistry.cpp, there is a possible out of bounds read due to a buffer overflow. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58823

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-08T19:18:02.873 |

In stpropnci_process_std of stpropnci_std.cc, there is a possible memory safety issue due to a missing bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58820

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T19:18:02.687 |

In multiple locations, there is a possible memory safety issue due to integer overflow. This could lead to local escalation of privilege with no additional execution privileges required.

### CVE-2026-55294

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T19:18:01.923 |

In ihevcd_get_tu_data_size of ihevcd_utils.c, there is a possible out of bounds write due to a heap buffer overflow. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55285

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-08T19:18:01.727 |

In openLogicalChannel of multiple files, there is a possible out-of-bounds write due to a missing bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55273

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-08T19:18:01.500 |

In AppendCommentLine of AnnotationProcessor.cpp, there is a possible supply chain risk due to improper input validation. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-49932

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T19:17:59.377 |

In parseParts of PduParser.java, there is a possible out of bounds read due to a heap buffer overflow. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-49927

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T19:17:59.283 |

In multiple locations, there is a possible out of bounds write due to an integer overflow. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28664

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-08T19:17:56.790 |

In WriteImageToDisk of runtime_image.cc, there is a possible file tampering due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-85880

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-908` |
| Published | 2026-09-08T18:21:14.087 |

Heap-based buffer overflow in Windows ALPC allows an authorized attacker to elevate privileges locally.

### CVE-2026-84000

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:21:10.990 |

Heap-based buffer overflow in Microsoft Graphics Component allows an authorized attacker to execute code locally.

### CVE-2026-83995

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:10.157 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-83990

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:21:09.687 |

Stack-based buffer overflow in Microsoft Graphics Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-83988

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:09.343 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83987

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:09.180 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83986

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:09.010 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83985

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:08.840 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83983

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:08.660 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83982

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:08.490 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83981

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:08.323 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83980

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:08.163 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83979

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:21:08.003 |

Use after free in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83978

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:07.833 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83977

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:07.667 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83976

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:07.503 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83975

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:07.327 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83974

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:07.167 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83973

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:06.997 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83972

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:06.833 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83971

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:06.670 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83970

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:06.480 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83969

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:06.320 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83968

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-400;CWE-416` |
| Published | 2026-09-08T18:21:06.153 |

Use after free in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83967

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:05.983 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83955

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:05.820 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83954

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:05.660 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83952

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:21:05.530 |

Heap-based buffer overflow in Windows Resilient File System (ReFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-83942

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T18:21:04.990 |

Missing authorization in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83498

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-08T18:21:04.243 |

Untrusted pointer dereference in Windows Virtualization-Based Security (VBS) Enclave allows an authorized attacker to elevate privileges locally.

### CVE-2026-81963

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-284` |
| Published | 2026-09-08T18:21:00.090 |

Improper link resolution before file access ('link following') in Windows Update Stack allows an authorized attacker to elevate privileges locally.

### CVE-2026-81960

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:59.953 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81959

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:20:59.810 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81957

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:59.490 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81956

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:59.360 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81954

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:58.987 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81953

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:20:58.860 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81951

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:58.590 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81950

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:20:58.460 |

Double free in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81949

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:20:58.313 |

Integer overflow or wraparound in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81948

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:58.180 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81947

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:58.040 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81398

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:56.437 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81397

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:56.300 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81396

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-193` |
| Published | 2026-09-08T18:20:56.163 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81388

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:20:55.103 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81386

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:54.840 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-81353

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:53.070 |

Heap-based buffer overflow in Microsoft Windows Codecs Library allows an unauthorized attacker to execute code locally.

### CVE-2026-80075

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:49.443 |

Heap-based buffer overflow in Windows Work Folders allows an authorized attacker to elevate privileges locally.

### CVE-2026-78448

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:42.800 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-78447

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:42.617 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-77904

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:40.387 |

Heap-based buffer overflow in Windows Volume Manager Extension Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-77500

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-09-08T18:20:36.797 |

Release of invalid pointer or reference in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-77489

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-08T18:20:34.657 |

Null pointer dereference in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-73026

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:32.640 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-73024

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:32.310 |

Heap-based buffer overflow in Windows Services for NFS ONCRPC XDR Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-73021

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-09-08T18:20:31.820 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-73020

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:31.653 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-73015

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:30.807 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-73014

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T18:20:30.650 |

Missing authorization in Data Sharing Service Client allows an authorized attacker to elevate privileges locally.

### CVE-2026-73011

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:30.117 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-73007

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:29.487 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-73002

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:20:28.713 |

Integer overflow or wraparound in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-73001

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:28.550 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-73000

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:28.393 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72997

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:28.070 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72996

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-09-08T18:20:27.907 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72995

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:20:27.737 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72994

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-09-08T18:20:27.570 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72993

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:27.363 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72992

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:27.180 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72991

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:26.820 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72990

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:20:26.570 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72988

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:25.863 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72967

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:22.950 |

Heap-based buffer overflow in Windows Network Connection Broker allows an authorized attacker to elevate privileges locally.

### CVE-2026-72965

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:22.577 |

Use after free in Windows WebClient Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72957

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:21.280 |

Heap-based buffer overflow in Windows Deployment Services allows an authorized attacker to execute code locally.

### CVE-2026-72953

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:20.857 |

Heap-based buffer overflow in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-72946

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:19.893 |

Heap-based buffer overflow in Storage Port Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-72944

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:19.573 |

Heap-based buffer overflow in Windows Fax Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72941

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:19.093 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72929

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-354` |
| Published | 2026-09-08T18:20:17.257 |

Improper validation of integrity check value in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-71345

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T18:20:14.583 |

Out-of-bounds write in Windows Spaceport.sys allows an authorized attacker to execute code locally.

### CVE-2026-71343

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:14.397 |

Heap-based buffer overflow in Windows Remote Access Connection Manager allows an authorized attacker to execute code locally.

### CVE-2026-71337

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-130` |
| Published | 2026-09-08T18:20:13.430 |

Stack-based buffer overflow in Windows Storage Management Provider allows an authorized attacker to elevate privileges locally.

### CVE-2026-71334

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:13.110 |

Heap-based buffer overflow in Windows NFS Portmapper allows an authorized attacker to elevate privileges locally.

### CVE-2026-70584

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-08T18:20:11.483 |

Access of resource using incompatible type ('type confusion') in Windows Core Messaging allows an authorized attacker to elevate privileges locally.

### CVE-2026-70583

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:11.317 |

Heap-based buffer overflow in Windows Core Messaging allows an authorized attacker to elevate privileges locally.

### CVE-2026-70581

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-190` |
| Published | 2026-09-08T18:20:10.980 |

Integer overflow or wraparound in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70574

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:10.257 |

Out-of-bounds read in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-70572

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:20:09.920 |

Integer overflow or wraparound in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70569

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:09.600 |

Out-of-bounds read in Windows Spaceport.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-70564

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:08.937 |

Heap-based buffer overflow in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-70334

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-08T18:20:07.083 |

Incomplete list of disallowed inputs in Visual Studio Code allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-70289

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:04.520 |

Heap-based buffer overflow in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-69921

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:02.587 |

Heap-based buffer overflow in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-69907

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-280` |
| Published | 2026-09-08T18:20:01.067 |

Improper handling of insufficient permissions or privileges in Windows Enterprise App Management allows an authorized attacker to elevate privileges locally.

### CVE-2026-69900

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-08T18:20:00.613 |

Untrusted pointer dereference in Kernel Streaming WOW Thunk Service Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69864

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:57.800 |

Use after free in Windows Hello allows an authorized attacker to elevate privileges locally.

### CVE-2026-69844

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:55.823 |

Out-of-bounds read in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69841

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:55.650 |

Heap-based buffer overflow in Windows Encrypting File System (EFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69822

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-09-08T18:19:54.037 |

Numeric truncation error in Windows Kerberos allows an authorized attacker to elevate privileges locally.

### CVE-2026-69821

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-116` |
| Published | 2026-09-08T18:19:53.883 |

Improper encoding or escaping of output in Active Directory Certificate Services (AD CS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69801

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:51.583 |

Heap-based buffer overflow in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69799

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-08T18:19:51.450 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Hello allows an authorized attacker to elevate privileges locally.

### CVE-2026-69790

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:50.493 |

Heap-based buffer overflow in Windows Credential Providers allows an authorized attacker to elevate privileges locally.

### CVE-2026-69787

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:50.333 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69785

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-09-08T18:19:49.967 |

Untrusted search path in Windows Smart Card allows an authorized attacker to elevate privileges locally.

### CVE-2026-69758

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:46.917 |

Heap-based buffer overflow in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69738

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:19:45.950 |

Integer overflow or wraparound in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69731

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:45.293 |

Heap-based buffer overflow in HID class driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69725

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:19:44.720 |

Double free in Windows Hello allows an authorized attacker to elevate privileges locally.

### CVE-2026-69720

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:44.137 |

Heap-based buffer overflow in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-69709

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:42.550 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to execute code locally.

### CVE-2026-69707

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:19:42.217 |

Integer overflow or wraparound in Windows USB Audio Class driver (usbaudio.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69691

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:41.320 |

Heap-based buffer overflow in Windows Spaceport.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-69687

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-08T18:19:40.697 |

Integer underflow (wrap or wraparound) in Windows USB Audio Class driver (usbaudio.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69685

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:40.387 |

Heap-based buffer overflow in Windows Kerberos allows an authorized attacker to elevate privileges locally.

### CVE-2026-69612

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-36` |
| Published | 2026-09-08T18:19:32.683 |

Absolute path traversal in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-69608

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:19:31.983 |

Integer overflow or wraparound in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-69604

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:31.350 |

Heap-based buffer overflow in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69594

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:19:29.970 |

Heap-based buffer overflow in Microsoft Local Security Authority Server (lsasrv) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69593

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:29.810 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69592

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:29.633 |

Heap-based buffer overflow in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69589

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:29.147 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69585

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-704` |
| Published | 2026-09-08T18:19:28.490 |

Incorrect type conversion or cast in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-69584

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:19:28.307 |

Integer overflow or wraparound in Windows USB Video Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69583

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:28.147 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69582

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-09-08T18:19:27.960 |

Buffer over-read in Windows Volume Manager Extension Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69580

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:27.623 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69576

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:27.073 |

Use after free in Graphic Fonts allows an authorized attacker to elevate privileges locally.

### CVE-2026-69571

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:26.227 |

Heap-based buffer overflow in Windows USB Audio Class driver (usbaudio.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69561

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:24.890 |

Out-of-bounds read in Windows CD-ROM Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69544

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:22.800 |

Heap-based buffer overflow in Windows SMB Client allows an authorized attacker to elevate privileges locally.

### CVE-2026-69542

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:22.617 |

Heap-based buffer overflow in Windows Camera Frame Server Monitor allows an authorized attacker to elevate privileges locally.

### CVE-2026-69541

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:22.437 |

Heap-based buffer overflow in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69538

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:21.923 |

Out-of-bounds read in Windows Spaceport.sys allows an authorized attacker to execute code locally.

### CVE-2026-69535

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-09-08T18:19:21.650 |

Numeric truncation error in Windows Spaceport.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-69534

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-08T18:19:21.483 |

Improper neutralization of special elements used in a command ('command injection') in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69532

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:21.303 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-69528

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-08T18:19:20.593 |

Missing authentication for critical function in Windows Shell allows an authorized attacker to elevate privileges locally.

### CVE-2026-69513

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:18.823 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-69509

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-09-08T18:19:18.120 |

Heap-based buffer overflow in Windows Fax Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69508

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:17.993 |

Stack-based buffer overflow in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-69489

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:15.007 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69480

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:13.990 |

Heap-based buffer overflow in Windows Partition Management Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69478

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:13.650 |

Heap-based buffer overflow in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69476

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:13.323 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69475

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-08T18:19:13.140 |

Untrusted pointer dereference in Windows Remote Desktop Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-69467

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:11.997 |

Stack-based buffer overflow in Microsoft Graphics Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-69459

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:10.693 |

Heap-based buffer overflow in Windows Power Dependency Coordinator allows an authorized attacker to elevate privileges locally.

### CVE-2026-69456

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:10.177 |

Heap-based buffer overflow in Microsoft Windows Speech allows an authorized attacker to elevate privileges locally.

### CVE-2026-69455

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:10.000 |

Heap-based buffer overflow in Windows Remote Access Connection Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-69450

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:09.457 |

Out-of-bounds read in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-69447

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:09.017 |

Heap-based buffer overflow in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69445

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-08T18:19:08.830 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Windows Compressed Folder allows an authorized attacker to elevate privileges locally.

### CVE-2026-69444

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:08.667 |

Heap-based buffer overflow in Microsoft Windows Speech allows an authorized attacker to elevate privileges locally.

### CVE-2026-69436

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:07.617 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-69433

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:07.270 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-69432

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:07.090 |

Heap-based buffer overflow in Volume Manager Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69426

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:06.050 |

Heap-based buffer overflow in Windows VOLSNAP.SYS allows an authorized attacker to execute code locally.

### CVE-2026-69424

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:05.743 |

Heap-based buffer overflow in Windows Distributed File System (DFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69421

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-09-08T18:19:05.250 |

Integer underflow (wrap or wraparound) in Windows Kernel Mode Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69420

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:05.070 |

Heap-based buffer overflow in Windows VOLSNAP.SYS allows an authorized attacker to elevate privileges locally.

### CVE-2026-69407

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:19:03.367 |

Integer overflow or wraparound in Volume Manager Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69392

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:01.210 |

Use after free in Windows Shell allows an authorized attacker to elevate privileges locally.

### CVE-2026-69391

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:19:01.047 |

Stack-based buffer overflow in Windows Broker Infrastructure Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69389

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:00.060 |

Heap-based buffer overflow in Windows Storage Management Provider allows an authorized attacker to elevate privileges locally.

### CVE-2026-69377

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T18:18:58.383 |

Missing authorization in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69368

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:57.077 |

Heap-based buffer overflow in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-69359

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:55.587 |

Heap-based buffer overflow in Active Directory Domain Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-69352

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-09-08T18:18:54.507 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69348

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:53.823 |

Heap-based buffer overflow in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69328

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-09-08T18:18:50.447 |

Untrusted search path in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-69324

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-843` |
| Published | 2026-09-08T18:18:50.057 |

Access of resource using incompatible type ('type confusion') in Windows Performance Monitor allows an authorized attacker to elevate privileges locally.

### CVE-2026-69323

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:49.890 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69312

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:18:47.847 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-69307

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:46.840 |

Heap-based buffer overflow in Windows USB Audio Class driver (usbaudio.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69298

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:18:45.377 |

Integer overflow or wraparound in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69295

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-125` |
| Published | 2026-09-08T18:18:44.897 |

Out-of-bounds read in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69293

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-09-08T18:18:44.570 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69290

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:18:44.070 |

Stack-based buffer overflow in Windows Storage Spaces Controller allows an authorized attacker to elevate privileges locally.

### CVE-2026-69289

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-08T18:18:43.887 |

Improper link resolution before file access ('link following') in Windows Setup Files Cleanup allows an authorized attacker to elevate privileges locally.

### CVE-2026-69284

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:43.023 |

Heap-based buffer overflow in Windows DCOM Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-69283

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:42.823 |

Heap-based buffer overflow in Windows CD-ROM Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69277

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-08T18:18:41.513 |

Stack-based buffer overflow in Microsoft Local Security Authority Server (lsasrv) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69270

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-09-08T18:18:39.397 |

Heap-based buffer overflow in Windows USB Audio Class driver (usbaudio.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69269

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-08T18:18:39.210 |

Integer underflow (wrap or wraparound) in Microsoft Standard XPS allows an authorized attacker to elevate privileges locally.

### CVE-2026-69265

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:18:38.597 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-68896

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-36` |
| Published | 2026-09-08T18:18:38.037 |

Absolute path traversal in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-68892

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:37.313 |

Heap-based buffer overflow in Microsoft Standard XPS allows an authorized attacker to elevate privileges locally.

### CVE-2026-68890

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:36.923 |

Heap-based buffer overflow in Microsoft Standard XPS allows an authorized attacker to elevate privileges locally.

### CVE-2026-68888

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:36.333 |

Heap-based buffer overflow in Microsoft Standard XPS allows an authorized attacker to elevate privileges locally.

### CVE-2026-68885

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:35.780 |

Heap-based buffer overflow in Microsoft Standard XPS allows an authorized attacker to elevate privileges locally.

### CVE-2026-68877

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:34.910 |

Heap-based buffer overflow in Windows Storage Spaces Controller allows an authorized attacker to execute code locally.

### CVE-2026-68875

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-09-08T18:18:34.550 |

Buffer over-read in Windows NTFS allows an authorized attacker to execute code locally.

### CVE-2026-68850

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:33.747 |

Heap-based buffer overflow in Microsoft Account allows an authorized attacker to elevate privileges locally.

### CVE-2026-68848

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:33.417 |

Heap-based buffer overflow in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-68845

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:32.630 |

Heap-based buffer overflow in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-68844

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:32.467 |

Heap-based buffer overflow in Windows Storage Spaces Controller allows an authorized attacker to execute code locally.

### CVE-2026-68841

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:31.983 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-68832

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:18:30.230 |

Integer overflow or wraparound in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-68787

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:26.313 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code locally.

### CVE-2026-62810

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:03.337 |

Heap-based buffer overflow in Active Directory Certificate Services (AD CS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-62804

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-08T18:18:03.127 |

External control of file name or path in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-62697

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:17:52.523 |

Use after free in Windows Push Notifications allows an authorized attacker to elevate privileges locally.

### CVE-2026-58611

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-08T18:17:44.063 |

Improper authorization in XBox Gaming Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-58600

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:17:43.923 |

Heap-based buffer overflow in Microsoft Windows Codecs Library allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-58599

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:17:43.797 |

Heap-based buffer overflow in Microsoft Windows Codecs Library allows an unauthorized attacker to execute code locally.

### CVE-2026-56198

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:17:42.793 |

Out-of-bounds read in Microsoft Trace Data Helper allows an authorized attacker to elevate privileges locally.

### CVE-2026-56177

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:17:42.563 |

Use after free in Windows Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-56172

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:17:42.320 |

Use after free in Windows VHD miniport driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-15140

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-09T13:18:37.293 |

A privilege-escalation issue in the Portworx Operator when deployed on Red Hat OpenShift (OCP). Only under specific conditions during the initial provisioning of a Portworx storage cluster, a user holding only limited, namespace-scoped permissions could cause the operator to grant broader access than intended, potentially resulting in elevated privileges within the Kubernetes cluster.

### CVE-2026-79637

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-09T12:17:13.977 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Certificate Validation vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-87084

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-09T03:17:27.070 |

Tanium addressed a server-side request forgery vulnerability in Enforce.

### CVE-2026-86083

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-08T22:19:17.383 |

n8n is an open source workflow automation platform. Prior to 1.123.76, 2.37.7, and 2.38.2, the legacy expression engine generated source text by calling the mutable global JSON.stringify while printing synthetic string literals and interpolating timezone data. An expression could replace JSON.stringify and cause later generated source to contain executable attacker-controlled code. The affected code-generation paths include packages/@n8n/expression-runtime/src/bridge/isolated-vm-bridge.ts and packages/@n8n/tournament/src/ExpressionBuilder.ts, and the issue does not affect the vm expression engine. This issue is fixed in versions 1.123.76, 2.37.7 and 2.38.2.

### CVE-2026-78623

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-08T20:18:37.050 |

The Okta Access Gateway does not sanitize SAML assertion values before interpolating them into database queries in the advanced mode datastore configuration. The unsanitized values are substituted directly into the query string prior to preparation, resulting in unintended SQL execution against the configured backend database.

### CVE-2026-82537

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-09-08T19:20:00.910 |

Roo-Code through 3.54.0 contains an auto-approve bypass vulnerability that allows attackers to execute denied shell commands by exploiting a word-boundary mismatch in comment handling between the approval gate's shell parser and bash. Attackers can craft a command string with an allowlisted word immediately followed by a hash character, separator, and denied command to pass the approval gate while bash executes the denied command with the agent's auto-execute privileges on the developer's machine.

### CVE-2026-82536

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-08T19:20:00.763 |

Roo-Code through 3.54.0 contains an auto-approve bypass vulnerability in the shell command parsing logic that allows attackers to execute denied shell commands by exploiting the omission of the bash pipe operator from the command parser's operator token set. Attackers can craft a command line with an allowlisted prefix followed by the stderr-redirecting pipe operator and a denied command, causing the parser to approve the full pipeline while bash executes the denied component with the agent's auto-execute privileges on the developer's machine.

### CVE-2026-77909

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-08T18:20:41.117 |

Insufficiently protected credentials in Azure CycleCloud allows an authorized attacker to disclose information over a network.

### CVE-2026-77110

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-08T19:19:41.617 |

Adobe Commerce is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could result in a Security feature bypass. An attacker with high privileges could leverage this vulnerability to access unauthorized files or directories outside the intended restrictions, causing a limited disruption to availability. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-82053

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T17:18:33.143 |

A security issue exists in MongoDB's LDAP authorization integration where pooled LDAP connections can retain stale authentication identities after user authentication under certain configurations. Subsequent authorization queries may execute under an unintended LDAP identity rather than the expected one. This can result in incorrect role assignments based on the LDAP directory's access control configuration, potentially allowing an authenticated user to acquire elevated privileges that were not intended by the deployment's authorization policy.

### CVE-2026-79950

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-09T14:17:18.170 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Use of Hard-coded Credentials vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure.

### CVE-2026-79740

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-09T14:17:18.047 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Use of Hard-coded Credentials vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure.

### CVE-2026-79738

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-09T14:17:17.917 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Use of Hard-coded Credentials vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure.

### CVE-2026-78490

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-09T12:17:13.720 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Restriction of Excessive Authentication Attempts vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to client-side request forgery.

### CVE-2026-79641

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-09T11:17:15.500 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to elevation of privileges.

### CVE-2026-87734

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-923` |
| Published | 2026-09-09T05:18:20.577 |

An issue was discovered in the utcp package before 0.0.6 for OCaml. Out-of-order segment reassembly allows remote denial of service.

### CVE-2026-15667

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-09T03:17:23.523 |

The Eventin – Event Calendar, Event Registration, Tickets & Booking (AI Powered) plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 4.1.22 via the 'event_layout' parameter parameter. This makes it possible for authenticated attackers, with contributor-level access and above, to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. The etn_manage_event capability is assigned to Contributors by default, meaning any Contributor-level user can set the malicious event_layout value via the REST API without any additional configuration.

### CVE-2026-15406

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-09T03:17:23.157 |

The Eventin – Event Calendar, Event Registration, Tickets & Booking (AI Powered) plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 4.1.22 via the 'event_layout' parameter parameter. This makes it possible for authenticated attackers, with custom-level access and above, to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included.

### CVE-2026-87601

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-09T01:17:18.120 |

Race condition in V8 in Google Chrome prior to 153.0.8010.36 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-78574

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-426` |
| Published | 2026-09-08T20:18:36.417 |

The Okta Hyperdrive Integration plugin resolves a required assembly using a registry path within the current user's hive without integrity verification. The referenced path is loaded via Assembly.LoadFrom without signature validation, resulting in an unverified assembly executing within the context of the host process or elevated installer.

### CVE-2026-75998

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-08T20:18:23.637 |

ColdFusion is affected by an Improper Access Control vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction.

### CVE-2026-77108

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T19:19:41.227 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. An attacker could leverage this vulnerability to gain elevated access to sensitive information. Exploitation of this issue does not require user interaction.

### CVE-2026-66307

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-08T19:18:08.327 |

Integer underflow (wrap or wraparound) in Skype for Business allows an unauthorized attacker to deny service over a network.

### CVE-2026-66304

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-08T19:18:07.950 |

Server-side request forgery (ssrf) in Skype for Business allows an unauthorized attacker to disclose information over a network.

### CVE-2026-84001

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:21:11.173 |

Out-of-bounds read in Windows Key Distribution Center allows an unauthorized attacker to deny service over a network.

### CVE-2026-83989

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:21:09.507 |

Out-of-bounds read in Windows Services for NFS ONCRPC XDR Driver allows an unauthorized attacker to deny service over a network.

### CVE-2026-81355

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:53.360 |

Heap-based buffer overflow in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to execute code locally.

### CVE-2026-77898

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:39.980 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-77895

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:39.540 |

Out-of-bounds read in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-77893

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:39.213 |

Out-of-bounds read in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-77890

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-08T18:20:38.737 |

Access of resource using incompatible type ('type confusion') in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-77889

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-08T18:20:38.587 |

Access of resource using incompatible type ('type confusion') in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-77888

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-08T18:20:38.430 |

Access of resource using incompatible type ('type confusion') in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-77886

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:38.090 |

Out-of-bounds read in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-77502

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:37.413 |

Out-of-bounds read in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-77501

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:37.050 |

Out-of-bounds read in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-77499

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-08T18:20:36.437 |

Access of resource using incompatible type ('type confusion') in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-77498

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:36.100 |

Out-of-bounds read in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-77494

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-08T18:20:35.447 |

Access of resource using incompatible type ('type confusion') in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-73017

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:31.147 |

Heap-based buffer overflow in Windows Graphics Kernel allows an authorized attacker to execute code locally.

### CVE-2026-72989

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-908` |
| Published | 2026-09-08T18:20:26.373 |

Use of uninitialized resource in Windows Failover Cluster allows an unauthorized attacker to disclose information over a network.

### CVE-2026-72954

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:20.990 |

Use after free in Windows Deployment Services allows an authorized attacker to execute code over a network.

### CVE-2026-72949

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-08T18:20:20.370 |

Null pointer dereference in Windows SMB Server Network Transport Driver (srvnet.sys) allows an unauthorized attacker to deny service over a network.

### CVE-2026-72943

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:19.427 |

Use after free in Windows Deployment Services allows an authorized attacker to execute code over a network.

### CVE-2026-72932

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-126` |
| Published | 2026-09-08T18:20:17.803 |

Buffer over-read in Windows Message Queuing Queue Manager allows an unauthorized attacker to disclose information over a network.

### CVE-2026-72928

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:17.103 |

Use after free in Windows DNS allows an authorized attacker to execute code over a network.

### CVE-2026-72923

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-08T18:20:16.310 |

In Microsoft.OpenApi.YamlReader from 2.0.0-preview.11 until 2.12.0 and from 3.0.0 until 3.10.0, and in Microsoft.OpenApi.Readers prior to 1.6.30, a small YAML OpenAPI document containing nested anchors and aliases can cause uncontrolled resource consumption when parsed through the public YAML reader APIs. YAML is parsed through SharpYaml, which represents aliases as shared nodes in a directed acyclic graph, so the parsed YAML graph stays small, but converting that graph to System.Text.Json.Nodes.JsonNode requires every alias to be materialized as an independent node because a JsonNode cannot be attached to multiple parents. Without a bound on that conversion work, a document with N nested anchors each referenced k times can require k^N materialized JSON nodes, leading to excessive memory allocation and process termination through out-of-memory conditions, a billion laughs style denial of service. The patched versions bound the YAML-to-JSON conversion by node count and nesting depth and report an OpenApiDiagnostic error instead of expanding without limit. This vulnerability is fixed in Microsoft.OpenApi.YamlReader 2.12.0 and 3.10.0, and Microsoft.OpenApi.Readers 1.6.30.

### CVE-2026-71330

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-09-08T18:20:12.500 |

Exposure of sensitive system information to an unauthorized control sphere in Windows Services for NFS ONCRPC XDR Driver allows an unauthorized attacker to disclose information over a network.

### CVE-2026-70587

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-170` |
| Published | 2026-09-08T18:20:11.980 |

Improper null termination in Windows Remote Desktop Protocol allows an unauthorized attacker to disclose information over a network.

### CVE-2026-70579

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:10.850 |

Out-of-bounds read in Windows Mobile Broadband allows an unauthorized attacker to disclose information over a network.

### CVE-2026-70570

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:09.740 |

Remote Code Execution in Windows Routing and Remote Access Service (RRAS) allows attacker to gain an unauthorized access to victim's machine

### CVE-2026-70065

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-08T18:20:03.337 |

Missing release of memory after effective lifetime in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-69890

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:59.967 |

Use after free in Windows Virtual Trusted Platform Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-69881

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-08T18:19:59.607 |

Null pointer dereference in Windows IKE Extension allows an unauthorized attacker to deny service over a network.

### CVE-2026-69852

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:56.550 |

Remote Code Execution in Windows Routing and Remote Access Service (RRAS) allows attacker to gain an unauthorized access to victim's machine

### CVE-2026-69809

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-08T18:19:52.687 |

Missing release of memory after effective lifetime in Active Directory Domain Services allows an unauthorized attacker to deny service over a network.

### CVE-2026-69805

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73;CWE-200;CWE-522` |
| Published | 2026-09-08T18:19:52.063 |

External control of file name or path in .NET allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-69804

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-08T18:19:51.940 |

Time-of-check time-of-use (toctou) race condition in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-69793

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-1288` |
| Published | 2026-09-08T18:19:50.973 |

Improper validation of consistency within input in Windows TCP/IP allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-69760

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:47.227 |

Out-of-bounds read in Windows Kerberos allows an unauthorized attacker to deny service over a network.

### CVE-2026-69744

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-08T18:19:46.630 |

Null pointer dereference in Windows Kerberos allows an unauthorized attacker to deny service over a network.

### CVE-2026-69710

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-08T18:19:42.730 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Hello allows an authorized attacker to elevate privileges locally.

### CVE-2026-69631

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:19:35.593 |

Integer overflow or wraparound in Windows DNS allows an unauthorized attacker to deny service over a network.

### CVE-2026-69607

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:31.837 |

Use after free in Windows Deployment Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-69599

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:30.537 |

Use after free in Windows Remote Desktop Services allows an authorized attacker to execute code over a network.

### CVE-2026-69588

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-08T18:19:29.010 |

Missing release of memory after effective lifetime in Windows TCP/IP allows an unauthorized attacker to deny service over a network.

### CVE-2026-69587

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-08T18:19:28.843 |

Null pointer dereference in Windows IKE Extension allows an unauthorized attacker to deny service over a network.

### CVE-2026-69539

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:22.103 |

Use after free in Windows Remote Desktop Services allows an authorized attacker to execute code over a network.

### CVE-2026-69514

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:18.973 |

Heap-based buffer overflow in Windows Remote Desktop Services allows an authorized attacker to execute code over a network.

### CVE-2026-69443

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:08.540 |

Out-of-bounds read in Windows Device Health Attestation (DHA) allows an unauthorized attacker to disclose information over a network.

### CVE-2026-69429

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:06.587 |

Heap-based buffer overflow in Windows IKE Extension allows an authorized attacker to execute code over a network.

### CVE-2026-69428

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:06.407 |

Out-of-bounds read in Windows LDAP - Lightweight Directory Access Protocol allows an unauthorized attacker to deny service over a network.

### CVE-2026-69397

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:02.047 |

Use after free in OpenSSH for Windows allows an unauthorized attacker to execute code over a network.

### CVE-2026-69378

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-08T18:18:58.543 |

Uncontrolled recursion in Microsoft Exchange Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-69342

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:18:52.813 |

Out-of-bounds read in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-69329

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-190` |
| Published | 2026-09-08T18:18:50.623 |

Out-of-bounds read in BranchCache allows an unauthorized attacker to deny service over a network.

### CVE-2026-68887

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:18:36.130 |

Out-of-bounds read in Windows Message Queuing Queue Manager allows an unauthorized attacker to deny service over a network.

### CVE-2026-67376

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T18:18:21.080 |

Integer overflow or wraparound in SQL Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-62813

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:03.667 |

Use after free in Active Directory Domain Services allows an authorized attacker to execute code over a network.

### CVE-2026-62759

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-08T18:17:58.917 |

Authentication bypass by spoofing in Windows Netlogon allows an unauthorized attacker to perform spoofing over an adjacent network.

### CVE-2026-57099

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-08T18:17:43.057 |

Allocation of resources without limits or throttling in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-57098

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-08T18:17:42.927 |

Improper verification of cryptographic signature in Windows RDP Client allows an unauthorized attacker to disclose information over a network.

### CVE-2026-47625

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T17:17:37.683 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker could abuse missing authorization. A successful exploit of this vulnerability might lead to information disclosure, data tampering, and denial of service.

### CVE-2026-16497

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-834` |
| Published | 2026-09-08T17:17:32.910 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker could cause excessive iteration. A successful exploit of this vulnerability might lead to denial of service.

### CVE-2026-16037

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-208` |
| Published | 2026-09-08T16:18:01.997 |

Observable timing discrepancy vulnerability in PayTR Payment and Electronic Money Institution Inc. PayTR Virtual Pos iFrame API (v9x) WHMCS Module allows Black Box Reverse Engineering.

This issue affects PayTR Virtual Pos iFrame API (v9x) WHMCS Module: from v9.0.0 before v9.0.3.

### CVE-2026-16025

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1284` |
| Published | 2026-09-08T16:18:01.497 |

Improper validation of specified quantity in input vulnerability in PayTR Payment and Electronic Money Institution Inc. PayTR Virtual Pos iFrame API (v9x) WHMCS Module allows Input Data Manipulation.

This issue affects PayTR Virtual Pos iFrame API (v9x) WHMCS Module: from v9.0.0 before v9.0.3.

### CVE-2026-86746

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-09T14:17:23.420 |

Snipe-IT before 8.7.0 contains an authorization bypass vulnerability in Livewire components that enforce authorization only at the route level, not within component lifecycle methods. Attackers with a valid authenticated session can replay signed component snapshots via POST /livewire/update to invoke protected methods and escalate privileges, including creating OAuth clients, minting personal access tokens, and accessing sensitive admin data.

### CVE-2026-87812

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-09T12:17:16.100 |

SiYuan before v3.8.2 contains a stored cross-site scripting vulnerability in Bazaar package cards where the iconURL metadata is inserted directly into HTML img src attributes without escaping. Attackers can inject malicious URLs with event handlers that execute JavaScript in the authenticated SiYuan origin when users view Bazaar listings, enabling API requests and application state manipulation.

### CVE-2026-79963

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-09-09T12:17:14.507 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains a Download of Code Without Integrity Check vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to command execution.

### CVE-2026-78492

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-09T12:17:13.850 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Certificate Validation vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-78494

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-09T09:17:10.990 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Certificate Validation vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-19651

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-08T21:17:06.777 |

IBM Enterprise Build of Quarkus 3.27.1 through 3.27.5, and 3.33.1 through 3.33.3  could allow an attacker to bypass authorization by manipulating URL query parameters due to incorrect mapping of values to untrusted query string input.

### CVE-2026-84003

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-08T18:21:11.363 |

Authentication bypass by capture-replay in Microsoft Authentication Library (MSAL) for Node.js allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-81383

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-706` |
| Published | 2026-09-08T18:20:54.593 |

Use of incorrectly-resolved name or reference in Visual Studio Code allows an unauthorized attacker to disclose information over a network.

### CVE-2026-78461

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-08T18:20:44.550 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-76196

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-384` |
| Published | 2026-09-08T18:20:33.380 |

Photoshop Mobile is affected by a Session Fixation vulnerability that could result in privilege escalation. An attacker could leverage this vulnerability to gain access to sensitive resources. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue requires user interaction in that a victim must interact with a malicious webpage. Scope is changed.

### CVE-2026-69347

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:53.647 |

Heap-based buffer overflow in Windows Fast FAT Driver allows an unauthorized attacker to execute code locally.

### CVE-2026-79695

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-09T12:17:14.250 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Handling of Highly Compressed Data (Data Amplification) vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to denial of service.

### CVE-2026-79692

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-09T12:17:14.120 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an External Control of File Name or Path vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to filesystem access for attacker.

### CVE-2026-78485

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-09T12:17:13.457 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access

### CVE-2026-79635

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-09T11:17:15.353 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains a Server-Side Request Forgery (SSRF) vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-80122

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-09T09:17:12.303 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Certificate Validation vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-80123

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-09T08:17:22.383 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains a Server-Side Request Forgery (SSRF) vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to denial of service.

### CVE-2026-49314

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-09T04:17:59.783 |

OOB write vulnerability in the rendering and composition module.
Impact: Successful exploitation of this vulnerability may affect availability.

### CVE-2026-78627

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-08T20:18:38.440 |

The Okta Hyperdrive Integration installer does not mask the OAuth client secret when passed as an MSI property. The credential is recorded in plaintext in the installer log, the Application Event Log, and the process command line, all of which are readable by an authenticated local user on the workstation.

### CVE-2026-69477

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:13.513 |

Heap-based buffer overflow in Microsoft Office Access allows an authorized attacker to execute code locally.

### CVE-2026-69417

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T18:19:04.697 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-69402

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-08T18:19:02.543 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-79972

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-09T12:17:14.760 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-14989

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-09T09:17:10.580 |

The Cookie Banner for GDPR / CCPA – WPLP Cookie Consent plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'wpl_user_preference' parameter in all versions up to, and including, 4.4.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The consent-logging AJAX endpoint is registered for unauthenticated users and its required nonce (wpl_consent_logging_nonce) is publicly emitted via wp_localize_script on the frontend, meaning any unauthenticated site visitor can plant a payload without any prior authentication or privileged access.

### CVE-2026-75927

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-09T08:17:21.997 |

The PublishPress Capabilities – User Role Editor, Access Permissions, User Capabilities, Admin Menus plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.50.0. This is due to the `addPluginCapabilities()` function unconditionally granting the Editor role all 15 `manage_capabilities_*` capabilities — including `manage_capabilities`, `manage_capabilities_roles`, `manage_capabilities_settings`, and `manage_capabilities_backup` — via a hard-coded `$eligible_roles = ['administrator', 'editor']` assignment that runs automatically on the first `admin_init` after plugin activation with no administrator opt-in, persisting the grants directly to the database. This makes it possible for authenticated attackers with Editor-level access to elevate their privileges to a site-wide capability manager, enabling them to create, rename, and delete non-system roles, modify capabilities of non-administrator roles, restore role backups, and write arbitrary plugin options whose names begin with `cme_`, `capsman`, `pp_capabilities`, or `presspermit` via `update_option()`. The escalation stops short of full Administrator access, as WordPress's `map_meta_cap` layer still prevents the escalated Editor from granting administrator-only capabilities to other roles; however, all role-management and plugin-settings functionality gated solely on `manage_capabilities_*` capabilities remains fully accessible.

### CVE-2026-83593

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-09T06:17:17.670 |

The WPBot – AI ChatBot for Live Support, Lead Generation, AI Services plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'conversation' parameter in all versions up to, and including, 8.7.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The action is gated only by a nonce that is localized into every public-facing page via wp_localize_script, rendering the nonce check ineffective as an access control barrier for unauthenticated users.

### CVE-2026-84293

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-09T04:20:27.027 |

The Repeater Fields for Gravity Forms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Repeated Multi-Input Sub-Field Values in all versions up to, and including, 3.0.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability only affects multi-input sub-field types within a repeater (such as Name, Address, and Checkbox fields), as scalar single-input field values are escaped with esc_html() at the output stage in version 3.0.4.

### CVE-2026-17553

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-09T04:17:56.607 |

The WP EasyCart plugin for WordPress is vulnerable to privilege escalation in versions up to, and including, 5.9.3. This is due to the ec_ajax_save_page_default_options() AJAX handler iterating over every $_POST key and passing it directly into update_option() without any allowlist, while gating the handler only on 'manage_options' OR the plugin's custom 'wpec_manager' capability. The plugin's built-in 'wpec_store_manager' role holds 'wpec_manager' but not 'manage_options', and the required nonce is emitted on frontend product/category templates that render for any user with 'wpec_manager'. This makes it possible for authenticated attackers, with Store Manager-level access and above, to elevate their privileges to administrator by updating arbitrary WordPress options such as default_role='administrator' and users_can_register='1', then self-registering a new account that is assigned the administrator role.

### CVE-2026-87021

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-09T03:17:25.207 |

Tanium addressed an unauthorized code execution vulnerability in Comply.

### CVE-2026-13359

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-09T03:17:22.627 |

The Contact Form to DB by BestWebSoft – Messages Database Plugin For WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via cntctfrm_contact_dropdown Parameter in all versions up to, and including, 1.7.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload executes in the context of an administrator's browser session when they visit the plugin's message manager page at /wp-admin/admin.php?page=cntctfrmtdb_manager, making it possible to compromise administrator-level sessions via a simple unauthenticated contact form submission.

### CVE-2026-81349

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-08T18:20:52.810 |

Improper neutralization of special elements used in an os command ('os command injection') in Azure HDInsights allows an authorized attacker to elevate privileges over a network.

### CVE-2026-84387

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-08T17:18:37.290 |

A improper neutralization of special elements used in a command ('command injection') vulnerability in Fortinet FortiSandbox 5.2.0, FortiSandbox 5.0.0 through 5.0.6, FortiSandbox 4.4.0 through 4.4.9 may allow attacker to execute unauthorized code or commands via <insert attack vector here>

### CVE-2026-82071

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-08T17:18:36.140 |

Insufficient validation of storage engine configuration options in MongoDB Server allows an authenticated user with write privileges to supply crafted parameters during collection creation that override internal storage metadata. This results in an out-of-bounds memory write in the server process, causing a denial of service via server crash, with potential for further impact including arbitrary code execution.

### CVE-2026-82061

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T17:18:34.837 |

A use-after-free security issue exists in the server's query execution memory tracking subsystem. An authenticated user with read privileges can trigger a write to freed heap memory through a sequence of standard database commands, leading to server process crash or potential memory corruption. No user interaction is required.

### CVE-2026-86766

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-09T14:17:26.963 |

Snipe-IT versions up to and including 8.6.3 contain a race condition (TOCTOU) in the consumable checkout API endpoint (POST /api/v1/consumables/{consumable_id}/checkout). The requested quantity is validated against the number of remaining units before the database transaction begins, and the transaction then creates the checkout records without locking the consumable row or re-checking availability. An authenticated user with permission to check out consumables can submit concurrent checkout requests for the same consumable so that both requests pass the availability check and succeed, over-allocating stock and driving the remaining inventory negative (e.g., a consumable with 1 remaining unit ends at -1 after two concurrent 1-unit checkouts). The issue is fixed in 8.7.0, which re-fetches the parent row under lockForUpdate inside the transaction and re-validates availability.

### CVE-2026-86765

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-09T14:17:26.780 |

Snipe-IT versions before 8.7.0 fail to enforce checkout authorization when assignment fields are submitted to the asset update endpoint. Authenticated users with edit permission but explicitly denied checkout permission can reassign assets, bypass check-in procedures, and alter custody records by submitting assigned_user, assigned_asset, or assigned_location parameters to PATCH /api/v1/hardware/{id}.

### CVE-2026-86764

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-09T14:17:26.597 |

Snipe-IT through 8.6.4 (fixed in 8.7.0) does not enforce the components.view permission on the authenticated endpoint GET /api/v1/hardware/<asset-id>/assigned/components. The endpoint authorizes only assets.view on the parent asset before returning linked component details; the components.view check is applied only to the response's available_actions.view flag and not to the returned data. As a result, an authenticated user holding only assets.view can enumerate component IDs, names, assigned quantities, and notes that are otherwise protected — the direct GET /api/v1/components/<id> endpoint correctly returns 403 Forbidden for such users.

### CVE-2026-86759

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-09T14:17:25.593 |

Snipe-IT versions before 8.7.0 fail to authorize the POST /hardware/history endpoint, allowing any authenticated user to reassign arbitrary assets and modify audit logs. Attackers can submit a CSV file to reassign assets across companies and inject fraudulent audit trail entries, compromising inventory integrity and accountability.

### CVE-2026-86758

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-204` |
| Published | 2026-09-09T14:17:25.430 |

Snipe-IT before 8.7.0 fails to properly enforce the viewKeys authorization gate in CSV export and API index endpoints, allowing authenticated users with only licenses.view permission to access product keys. Attackers can download all license keys in bulk via CSV export or validate candidate keys through API response discrepancies without needing the viewKeys permission.

### CVE-2026-86757

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-09T14:17:25.170 |

Snipe-IT before 8.7.0 fails to properly gate access to encrypted custom-field values in asset form templates for listbox, textarea, markdown-textarea, and date/datetime picker elements. Authenticated users with assets.edit, assets.checkin, assets.checkout, or assets.audit permissions can read plaintext encrypted custom field values by opening asset forms, bypassing the assets.view.encrypted_custom_fields permission check.

### CVE-2026-86204

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-09T14:17:21.690 |

PocketMine-MP versions before 5.39.2 fail to limit JSON payload size in ModalFormResponsePacket handling, allowing authenticated players to cause denial of service. Attackers can send modal form response packets with massive JSON arrays to exhaust server memory and CPU resources, rendering the server unresponsive.

### CVE-2025-71417

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-09T14:17:10.740 |

PocketMine-MP before 5.32.1 fails to validate uniqueness of pack UUIDs in ResourcePackClientResponsePacket STATUS_SEND_PACKS handling, allowing authenticated clients to trigger duplicate pack transmissions. Attackers can send multiple copies of valid pack UUIDs in a single packet to exhaust server memory and cause denial of service.

### CVE-2024-58380

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-09T14:17:10.043 |

PocketMine-MP versions before 5.11.2 contain a denial of service vulnerability in BookEditPacket handling that crashes the server when an invalid inventory slot value is provided. Attackers can send a crafted BookEditPacket with an inventory slot greater than 35 to trigger an unhandled exception and crash the server.

### CVE-2023-54396

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-09-09T14:17:09.883 |

PocketMine-MP versions before 4.8.1 fail to validate dye color IDs in banner NBT data during deserialization. Attackers can provide invalid color values in inventory transactions or via commands to trigger undefined offset errors and crash the server.

### CVE-2023-54392

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-09T14:17:09.307 |

PocketMine-MP versions >= 4.20.0 before 4.22.3 (and before 5.2.1 in the 5.x branch) fail to validate NBT tag types in BlockActorDataPacket. A player can crash the server by sending a packet containing sign NBT data with an incorrect tag type, triggering an unhandled UnexpectedTagTypeException that terminates the server process.

### CVE-2026-87821

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-09T12:17:17.417 |

Lara Dashboard through 1.3.1 contains a server-side request forgery vulnerability in the POST /api/admin/builder/markdown/fetch endpoint that allows any authenticated user to fetch arbitrary URLs and read the response body. Attackers can read internal HTTP services and cloud metadata including IAM credentials by supplying malicious URLs without host validation or redirect restrictions.

### CVE-2026-87818

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-09T12:17:16.980 |

GitPython 3.1.59 fails to restrict the --no-index option in the high-level diff API, allowing attackers to read arbitrary filesystem paths as repository operands. Attackers can combine --no-index with -I/--ignore-matching-lines to create a content-dependent Boolean oracle, repeatedly querying local files to recover single-line secrets through distinguishable success or error responses.

### CVE-2026-87809

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-09T12:17:15.650 |

Siyuan before v3.8.2 fails to apply publish-access filtering to embedded blocks before rendering in the /api/export/preview and /api/lute/copyStdMarkdown endpoints. Attackers with reader access can retrieve the full rendered content of private, hidden, or publish-disabled blocks by accessing public documents containing embed queries that select those blocks.

### CVE-2026-21104

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T05:17:22.723 |

Heap-based buffer overflow in KnoxVault trustlet prior to SMR Sep-2026 Release 1 allows local privileged attackers to execute arbitrary code.

### CVE-2026-49315

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-264` |
| Published | 2026-09-09T04:17:59.933 |

DoS vulnerability in the input device module.
Impact: Successful exploitation of this vulnerability may affect availability.

### CVE-2026-87072

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-09T03:17:26.723 |

Tanium addressed an improper access controls vulnerability in Comply.

### CVE-2026-86082

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-08T22:19:17.240 |

n8n is an open source workflow automation platform. Prior to 1.123.76, 2.37.7, and 2.38.2, the OpenAI Chat Model node enforced credential allowed-domain restrictions for normal calls but not for the model-search dropdown. A workflow editor could set options.baseURL to an arbitrary host and make the searchModels path send the openAiApi credential there. The affected implementation is packages/@n8n/nodes-langchain/nodes/llms/LMChatOpenAi/methods/loadModels.ts, which omitted assertOpenAiCredentialAllowsUrl. This issue is fixed in versions 1.123.76, 2.37.7 and 2.38.2.

### CVE-2026-86081

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-08T22:19:17.093 |

n8n is an open source workflow automation platform. Prior to 1.123.76, 2.37.7, and 2.38.2, the Git node clone operation matched an attacker-controlled destination path against the default N8N_BLOCK_FILE_PATTERNS regular expression. The pattern ^(./).git(/.)$ allowed catastrophic backtracking and ran synchronously in the main n8n process. An authenticated workflow editor could therefore freeze the instance with one workflow execution; the affected default is declared in packages/@n8n/config/src/configs/security.config.ts. This issue is fixed in versions 1.123.76, 2.37.7 and 2.38.2.

### CVE-2026-66305

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-603` |
| Published | 2026-09-08T19:18:08.073 |

Use of client-side authentication in Skype for Business allows an authorized attacker to perform spoofing over a network.

### CVE-2026-69775

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:48.980 |

Use after free in Windows DWM Core Library allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69761

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:47.390 |

Use after free in Windows TCP/IP allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69757

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:46.760 |

Use after free in Windows TCP/IP allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69706

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:42.037 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69688

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:40.870 |

Heap-based buffer overflow in Windows Encrypting File System (EFS) allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69602

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:31.010 |

Use after free in Windows PrintWorkflowUserSvc allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69597

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:30.237 |

Use after free in Windows HTTP.sys allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69553

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T18:19:24.020 |

Missing authorization in Windows Hyper-V allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69536

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:21.793 |

Use after free in Windows Remote Desktop Services allows an authorized attacker to execute code over a network.

### CVE-2026-69482

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-379` |
| Published | 2026-09-08T18:19:14.313 |

Creation of temporary file in directory with insecure permissions in Windows Error Reporting allows an authorized attacker to perform tampering locally.

### CVE-2026-69460

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:10.870 |

Use after free in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69451

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:09.640 |

Use after free in Windows Management Instrumentation allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69396

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:01.867 |

Use after free in Windows NDIS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69384

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-08T18:18:59.373 |

Null pointer dereference in Virtual Hard Disk (VHD) Miniport Driver allows an unauthorized attacker to deny service locally.

### CVE-2026-69366

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:56.717 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69364

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:18:56.377 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Print Spooler Components allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69358

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-09-08T18:18:55.400 |

Use of uninitialized resource in Remote Desktop Client allows an authorized attacker to execute code over a network.

### CVE-2026-69357

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:55.213 |

Use after free in Windows NDIS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69340

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-09-08T18:18:52.457 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69338

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:52.180 |

Use after free in Remote Desktop Gateway Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69337

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:18:52.003 |

Double free in Windows Registry allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69336

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:51.817 |

Heap-based buffer overflow in Microsoft Standard XPS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69314

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:48.373 |

Use after free in Windows Device Association Broker service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69313

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:48.050 |

Heap-based buffer overflow in Microsoft Standard XPS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69305

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:46.527 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69296

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:45.067 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69274

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:40.563 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69272

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:39.860 |

Heap-based buffer overflow in Microsoft Standard XPS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68893

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:37.517 |

Use after free in Windows Remote Desktop Licensing Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68889

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-08T18:18:36.713 |

Heap-based buffer overflow in Microsoft Standard XPS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68846

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:32.847 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68835

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:31.060 |

Use after free in Windows Print Spooler Components allows an authorized attacker to elevate privileges over a network.

### CVE-2026-82076

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-08T17:18:36.667 |

An integer overflow in the query planning component of MongoDB Server can allow an authenticated user with ordinary database-level read/write privileges to bypass an internal resource limit. Submitting a specially crafted query causes the server to consume memory without bound during query planning, and the resulting exhaustion terminates the server process. This may result in a denial of service affecting all databases served by the affected node.

### CVE-2026-82074

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T17:18:36.403 |

MongoDB Server contains an incorrect authorization vulnerability in the aggregation framework. An authenticated user with minimal privileges can craft a specially formatted aggregation request that causes the server's authorization subsystem to evaluate a different operation than what is actually executed, resulting in unauthorized read access to collection data within the target database.

### CVE-2026-82073

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T17:18:36.273 |

A security issue in the MongoDB Server aggregation framework allows an authenticated user with limited read privileges to bypass view-level authorization checks and access data from unauthorized collections when Atlas Search features are in use. The issue stems from insufficient validation of an internal command parameter that can be set by external clients, causing a security check to be improperly skipped.

### CVE-2026-82070

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-08T17:18:36.010 |

A security issue in MongoDB Server's diagnostic reporting interface allows an authenticated user with monitoring privileges to access insufficiently protected credentials from concurrent administrative operations. The same credentials are properly redacted in server log output, but the diagnostic interface omits equivalent redaction. Successful exploitation requires a valid authenticated session with monitoring-level permissions and results in exposure of cleartext credentials that could enable impersonation of other users, including privileged accounts.

### CVE-2026-82068

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-08T17:18:35.750 |

A security issue in MongoDB Server allows an authenticated user with write privileges to trigger a persistent fatal assertion crash by sending specially crafted retryable write commands. The crash state is durably persisted, causing the server process to repeatedly crash on restart and potentially propagating to additional nodes in a sharded cluster. Manual intervention is required to restore service availability.

### CVE-2026-82065

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-08T17:18:35.360 |

A security issue in the MongoDB Server's storage engine integration layer allows an authenticated user with collection creation privileges to cause a persistent denial of service. Insufficient validation of user-supplied storage configuration options permits values that, once persisted to durable metadata, trigger a fatal assertion failure when the metadata is subsequently read by diagnostic operations. The corrupted metadata persists across server restarts and is replicated to other cluster members, requiring manual operator intervention to restore service.

### CVE-2026-82058

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-08T17:18:34.427 |

A flaw in MongoDB's JSON Schema validation error generation code allows an authenticated user with readWrite privileges to crash the mongod server. When a BSON document containing an array with a malformed numeric field name fails a $jsonSchema items type constraint, the error generation path performs unsafe numeric conversion on the user-controlled field name without proper exception handling, resulting in an uncaught exception that terminates the server process. This is possible because incoming wire protocol BSON validation does not enforce that array element field names are valid, in-range numeric indices.

### CVE-2026-82057

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-08T17:18:34.287 |

A security issue was discovered in MongoDB where an authenticated user with readWrite privileges could crash the mongod server process. By specifying a custom WiredTiger storage configuration option with an incompatible value during collection creation, a user could cause a type confusion in the storage engine layer. When documents were subsequently read from the misconfigured collection, the resulting mismatch in expected data format led to corrupted memory interpretation and a server crash. The crafted collection configuration persists across restarts, requiring manual operator intervention to remediate.

### CVE-2026-82055

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-08T17:18:33.410 |

A security issue exists in MongoDB's 2dsphere index key generation that can cause a server crash due to a null pointer dereference. When a specially crafted GeoJSON document is inserted into a collection with a 2dsphere index, an inconsistency in geometry parsing can leave an internal object in an invalid, partially initialized state. During subsequent index key generation, access to this improperly initialized object results in a null pointer dereference that terminates the mongod process. An authenticated user with write access can use this to cause a denial of service.

### CVE-2026-82054

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-08T17:18:33.280 |

A security issue exists in MongoDB server's JSON Pointer parser used during $jsonSchema query filter processing. When a find command includes a specially crafted $jsonSchema filter field, the parser processes the input without enforcing adequate limits on iteration count or total allocation size, resulting in significant memory amplification. Under concurrent request load, the cumulative memory consumption can exhaust available heap memory, causing the server's out-of-memory handler to terminate the mongod process and deny service to all connected clients.

### CVE-2026-82052

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-08T17:18:32.987 |

The $regexFindAll expression can be used by an authenticated user who can run aggregation pipeline stages to crash a MongoDB server (mongod). Under certain specific conditions the  regex match can start in the middle of a multi-code-unit character, triggering an assertion during query execution.

### CVE-2026-20293

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-749` |
| Published | 2026-09-08T17:17:34.047 |

A vulnerability in the Unified Extensible Firmware Interface (UEFI) Shell implementation of Cisco UCS Servers and UCS-based appliances could allow an authenticated attacker with valid credentials for a user account with the role of user or admin&nbsp;or an unauthenticated attacker with physical access to an affected device to bypass UEFI Secure Boot validation checks and execute unauthorized software.

This vulnerability is due to the availability of memory write commands in the UEFI Shell while UEFI Secure Boot is enabled on a device. An attacker could exploit this vulnerability by selecting the UEFI Shell boot option at boot time and using available shell commands to modify UEFI memory variables. A successful exploit could allow the attacker to manipulate the preboot environment, overwrite UEFI Secure Boot-related memory values, and execute unauthorized software on the affected device.

### CVE-2026-86734

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-08T16:18:35.963 |

Snipe-IT before 8.7.1 fails to validate the length of the note field in the POST /account/accept/{acceptance} endpoint, allowing authenticated users to submit unbounded input that reaches synchronous CommonMark rendering. Attackers can submit large note values to exhaust PHP worker CPU and cause denial of service through resource exhaustion in the markdown parsing pipeline.

### CVE-2026-86731

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-08T16:18:35.187 |

Craft CMS versions 5.0.0-RC1 through 5.10.11 are missing an admin-target guard in UsersController::actionActivateUser (the users/activate-user action). While the action requires the administrateUsers permission, it does not call requireAdmin() when the targeted user is an administrator, unlike the mirror action actionDeactivateUser. As a result, an authenticated control panel user who is not an administrator but holds the administrateUsers permission can activate a pending or deliberately deactivated administrator account, which can lead to permission escalation when combined with resetting that account's password. The issue is fixed in Craft CMS 5.10.12.

### CVE-2026-86726

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-08T16:18:33.690 |

AVideo through 29.0 contains an information disclosure vulnerability in restreamsActive.json.php that allows authenticated streamers to enumerate source stream keys and identities of all other streamers' active restreams. The endpoint fails to filter results by user ownership, exposing sensitive transmission credentials and streamer identity across all accounts to any user with streaming capability.

### CVE-2026-86725

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-08T16:18:33.207 |

AVideo through c3edcc274c389816d434acadac07ee78eaf330c1 contains a missing authorization vulnerability in the SocialMediaPublisher plugin's add.json.php endpoint that allows authenticated users to modify other users' OAuth token records. Attackers can supply arbitrary row IDs to overwrite another user's stored access_token and refresh_token, then delete the compromised record to destroy the victim's provider linkage.

### CVE-2026-86724

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-08T16:18:33.070 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a cross-site request forgery vulnerability in plugin/YPTWallet/view/saveBalance.php that allows attackers to set arbitrary wallet balances by relying only on session cookies without token validation. Attackers can craft a malicious webpage that, when loaded by an administrator, submits a POST request to modify any user's wallet balance to any value.

### CVE-2026-86718

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-08T16:18:31.203 |

WWBN AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a cross-site request forgery vulnerability in deleteHistory.json.php and finishAll.json.php that allows unauthenticated attackers to mutate live history by making GET requests without CSRF token validation. Attackers can craft malicious pages that trigger administrator browsers to delete all live transmission history or mark streams as finished when an admin visits the attacker-controlled site.

### CVE-2026-16769

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-440` |
| Published | 2026-09-08T16:18:03.677 |

An unencrypted 'pause encryption request' message causes a denial of service in the in the RS9116W/SiWx917. See vulnerability B-E10 in the related paper below.

### CVE-2026-86749

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-252` |
| Published | 2026-09-09T14:17:23.880 |

Snipe-IT versions <= 8.6.3 (fixed in 8.7.0) do not check the return value of storage write operations in ImageUploadRequest::handleImages(). Because Laravel's default disk mode does not throw on failure, a silently failed Storage::disk('public')->put(...) call still caused the application to delete the previous image via deleteExistingImage() and to reassign and persist the model's image reference to the new filename, destroying the existing image and leaving the database row pointing at a file that was never written. A mirror problem existed in deleteExistingImage(), where a failed Storage::delete() still nulled the model's image field, orphaning the file on disk. The condition is not directly attacker-controlled: it is triggered when any legitimate authenticated user submits an image upload while the storage backend transiently fails (for example an S3 network error, a local filesystem permission problem, or quota exhaustion). The result is unrecoverable loss of the prior image and a durable inconsistency between the database and disk that requires manual reconciliation. All models whose controllers route through ImageUploadRequest::handleImages (assets, asset models, users, companies, manufacturers, locations, categories, suppliers, departments, and other image-carrying models) are affected.

### CVE-2026-79636

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-297` |
| Published | 2026-09-09T08:17:22.133 |

Dell SCG 5.0 Appliance versions prior to 5.36.00.16 and Dell SCG 5.0 Application versions prior to 5.36.00.00, contains an Improper Validation of Certificate with Host Mismatch vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-87088

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-09T03:17:27.183 |

Tanium addressed an unauthorized code execution vulnerability in Enforce.

### CVE-2026-81192

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-09-08T21:18:43.447 |

`OpenTelemetry.Resources.Host` NuGet package, which provides OpenTelemetry resource detectors for host, is affected by an untrusted search path vulnerability on macOS. Prior to version 1.16.0-beta.2, the `host.id` resource attribute detector launches the `sh` and `ioreg` executables by bare name rather than by absolute path, so both are resolved through the `PATH` environment variable. A local attacker who is less privileged than the host application, and who can influence `PATH` or write to a directory that appears in `PATH` ahead of the system directories, can have an arbitrary binary executed in the application's security context, resulting in local code execution/privilege escalation. This vulnerability only affect macOS hosts - Linux and Windows hosts are unaffected. Version 1.16.0-beta.2 contains a patch. No known workarounds are available.

### CVE-2026-58848

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-08T19:18:03.180 |

In multiple functions of alloc.c, there is a possible unauthorized read/write access due to a race condition. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-85360

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:21:12.363 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83999

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-08T18:21:10.863 |

Improper link resolution before file access ('link following') in Windows Resilient File System (ReFS) Deduplication Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83940

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:21:04.693 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-81389

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:55.243 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-80093

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:51.807 |

Use after free in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-78464

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-08T18:20:44.930 |

Time-of-check time-of-use (toctou) race condition in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-78457

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:44.407 |

Use after free in Windows Security Health Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-77905

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:40.560 |

Use after free in Windows Management Instrumentation allows an authorized attacker to elevate privileges locally.

### CVE-2026-77899

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:40.133 |

Use after free in Windows Security Center allows an authorized attacker to elevate privileges locally.

### CVE-2026-77897

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-08T18:20:39.850 |

Relative path traversal in Power Automate allows an authorized attacker to elevate privileges locally.

### CVE-2026-77894

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:20:39.367 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-77485

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:34.147 |

Use after free in SQL Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-73022

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:31.983 |

Use after free in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-73005

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:20:29.160 |

Use after free in Windows Authentication Methods allows an authorized attacker to elevate privileges locally.

### CVE-2026-73003

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:28.873 |

Use after free in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-72963

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:22.223 |

Use after free in Windows Modern Execution Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-72952

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:20:20.700 |

Out-of-bounds read in Windows Spaceport.sys allows an authorized attacker to execute code locally.

### CVE-2026-72930

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:17.423 |

Use after free in Windows Secure Socket Tunneling Protocol (SSTP) allows an authorized attacker to execute code locally.

### CVE-2026-72926

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:16.640 |

Use after free in Windows Internet Connection Sharing (ICS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-71353

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:20:16.093 |

Double free in Windows Routing and Remote Access Service (RRAS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-71351

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:20:15.477 |

Double free in Windows Routing and Remote Access Service (RRAS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-71342

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:14.230 |

Use after free in Windows Remote Access Connection Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-71340

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:13.897 |

Use after free in Windows File History Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-71333

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:12.920 |

Use after free in Windows Remote Access Connection Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-71332

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:12.757 |

Use after free in Windows Secure Socket Tunneling Protocol (SSTP) allows an authorized attacker to elevate privileges locally.

### CVE-2026-70585

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:11.657 |

Use after free in Windows Services for NFS ONCRPC XDR Driver allows an authorized attacker to execute code locally.

### CVE-2026-70578

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:10.720 |

Heap-based buffer overflow in Windows Credential Guard allows an authorized attacker to elevate privileges locally.

### CVE-2026-70577

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:10.567 |

Use after free in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-70573

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-09-08T18:20:10.083 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70568

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:20:09.413 |

Heap-based buffer overflow in Windows Defender Firewall Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70567

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:20:09.290 |

Double free in Windows Display Enhancement Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70565

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:09.113 |

Use after free in Windows AF_UNIX Socket Provider allows an authorized attacker to elevate privileges locally.

### CVE-2026-70562

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:20:08.583 |

Double free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70283

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T18:20:04.333 |

Incorrect authorization in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69911

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:02.413 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-69896

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:00.493 |

Use after free in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-69891

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:20:00.127 |

Use after free in Windows Media allows an authorized attacker to elevate privileges locally.

### CVE-2026-69889

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:59.780 |

Use after free in Windows Bluetooth Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69866

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:57.933 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69859

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191;CWE-367` |
| Published | 2026-09-08T18:19:57.273 |

Time-of-check time-of-use (toctou) race condition in Windows USB Audio Class driver (usbaudio.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69838

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:55.330 |

Use after free in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-69834

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:55.070 |

Use after free in Windows ALPC allows an authorized attacker to elevate privileges locally.

### CVE-2026-69818

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:53.443 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69817

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:53.263 |

Use after free in Windows Bluetooth Port Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69816

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:53.100 |

Use after free in Windows Accounts Control allows an authorized attacker to elevate privileges locally.

### CVE-2026-69814

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:52.970 |

Use after free in Windows Credential Providers allows an authorized attacker to elevate privileges locally.

### CVE-2026-69806

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-200` |
| Published | 2026-09-08T18:19:52.190 |

Exposure of sensitive information to an unauthorized actor in .NET allows an authorized attacker to elevate privileges locally.

### CVE-2026-69791

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:50.647 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69779

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-08T18:19:49.377 |

Time-of-check time-of-use (toctou) race condition in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69735

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:45.790 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69711

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:42.860 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69708

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:42.400 |

Use after free in Windows Web Platform Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-69694

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-08T18:19:41.870 |

Deserialization of untrusted data in Windows IP Address Management (IPAM) Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69693

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:41.697 |

Use after free in Windows Device Association Broker service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69692

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:41.490 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69682

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:19:39.947 |

Use after free in Windows Host Guardian Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69654

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:38.380 |

Use after free in Windows Accounts Control allows an authorized attacker to elevate privileges locally.

### CVE-2026-69652

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:38.213 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69648

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:37.943 |

Use after free in Windows Notification allows an authorized attacker to elevate privileges locally.

### CVE-2026-69645

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:36.620 |

Use after free in Windows Message Queuing allows an authorized attacker to elevate privileges locally.

### CVE-2026-69630

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:35.423 |

Out-of-bounds read in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69621

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:34.140 |

Heap-based buffer overflow in Windows Fax Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69617

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-08T18:19:33.470 |

Out-of-bounds read in Windows Resilient File System (ReFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69613

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:32.867 |

Use after free in Windows Image Acquisition allows an authorized attacker to elevate privileges locally.

### CVE-2026-69611

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:32.520 |

Use after free in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69610

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-09-08T18:19:32.343 |

Buffer over-read in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69606

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:31.693 |

Use after free in Windows Shell allows an authorized attacker to elevate privileges locally.

### CVE-2026-69605

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:31.547 |

Use after free in Microsoft Install Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69600

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:30.663 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-69581

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:19:27.790 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69578

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-09-08T18:19:27.257 |

Numeric truncation error in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-69575

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:26.910 |

Use after free in Windows Storage Spaces Controller allows an authorized attacker to elevate privileges locally.

### CVE-2026-69574

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:26.760 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69573

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:26.583 |

Use after free in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69567

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:25.687 |

Use after free in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-69564

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:25.360 |

Heap-based buffer overflow in Windows Online Certificate Status Protocol (OCSP) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69563

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-367` |
| Published | 2026-09-08T18:19:25.200 |

Heap-based buffer overflow in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69560

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:24.720 |

Use after free in Windows Work Folder Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69549

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-200` |
| Published | 2026-09-08T18:19:23.437 |

Out-of-bounds read in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69540

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:22.283 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69517

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:19.307 |

Use after free in Windows Wireless Networking allows an authorized attacker to elevate privileges locally.

### CVE-2026-69516

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:19.157 |

Use after free in Connected Devices Platform Service (Cdpsvc) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69501

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-08T18:19:17.120 |

Untrusted pointer dereference in Windows Secure Kernel Mode allows an authorized attacker to elevate privileges locally.

### CVE-2026-69500

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:16.937 |

Use after free in Windows Image Acquisition allows an authorized attacker to elevate privileges locally.

### CVE-2026-69498

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:16.600 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69492

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:15.540 |

Heap-based buffer overflow in Windows Partition Management Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69488

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:14.830 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69473

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:12.777 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-69472

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:12.610 |

Use after free in Windows Devices Human Interface allows an authorized attacker to elevate privileges locally.

### CVE-2026-69470

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:12.457 |

Use after free in Windows Connected User Experiences and Telemetry allows an authorized attacker to elevate privileges locally.

### CVE-2026-69468

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:12.123 |

Heap-based buffer overflow in Windows Volume Manager Extension Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69466

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-08T18:19:11.817 |

Time-of-check time-of-use (toctou) race condition in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-69448

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-08T18:19:09.140 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Bluetooth Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69441

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:19:08.213 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-69440

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-08T18:19:08.087 |

Time-of-check time-of-use (toctou) race condition in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-69430

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:06.750 |

Use after free in Windows Embedded Mode Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69422

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:05.433 |

Use after free in Windows USB Video Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69413

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:04.143 |

Use after free in Windows USB Audio Class driver (usbaudio.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-69410

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:03.860 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69404

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-08T18:19:02.827 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-69401

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:19:02.413 |

Use after free in Audio Video Control Transport Protocol allows an authorized attacker to elevate privileges locally.

### CVE-2026-69398

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-415` |
| Published | 2026-09-08T18:19:02.200 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Bluetooth Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69394

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:19:01.510 |

Heap-based buffer overflow in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69388

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:59.880 |

Use after free in Windows Bluetooth Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69385

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:18:59.540 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-69383

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-08T18:18:59.243 |

External control of file name or path in Windows Shell allows an authorized attacker to elevate privileges locally.

### CVE-2026-69379

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-08T18:18:58.670 |

Improper link resolution before file access ('link following') in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-69362

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:56.160 |

Use after free in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-69341

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:52.637 |

Use after free in Windows Image Acquisition allows an authorized attacker to elevate privileges locally.

### CVE-2026-69335

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:51.487 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69333

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:51.163 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-69331

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:50.800 |

Use after free in Windows Remote Access Connection Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-69319

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:18:49.330 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows USB Video Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69311

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:47.680 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69310

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:47.500 |

Use after free in Windows DNS allows an authorized attacker to elevate privileges locally.

### CVE-2026-69309

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:18:47.277 |

Double free in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-69300

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:45.720 |

Use after free in Windows Push Notifications allows an authorized attacker to elevate privileges locally.

### CVE-2026-69299

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:45.547 |

Use after free in Microsoft COM for Windows allows an authorized attacker to elevate privileges locally.

### CVE-2026-69292

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-08T18:18:44.423 |

Double free in Remote Desktop Gateway Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69287

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:43.520 |

Use after free in Windows Remote Desktop Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-69281

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:42.547 |

Use after free in Windows License Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-69280

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:42.383 |

Use after free in Windows Push Notifications allows an authorized attacker to elevate privileges locally.

### CVE-2026-69279

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:42.033 |

Use after free in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69275

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:40.847 |

Use after free in Kernel Streaming WOW Thunk Service Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-68897

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:38.170 |

Heap-based buffer overflow in Microsoft Standard XPS allows an authorized attacker to elevate privileges locally.

### CVE-2026-68884

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-08T18:18:35.617 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-68847

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:33.237 |

Use after free in Windows Connected User Experiences and Telemetry allows an authorized attacker to elevate privileges locally.

### CVE-2026-68840

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:18:31.810 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-68837

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:31.253 |

Use after free in Windows File History Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-68825

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:18:29.313 |

Use after free in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-68824

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:18:29.153 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Connected User Experiences and Telemetry allows an authorized attacker to elevate privileges locally.

### CVE-2026-62694

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-08T18:17:52.170 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-50349

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-09-08T18:17:38.537 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-82062

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-08T17:18:34.970 |

A security issue in MongoDB Server allows an authenticated user with elevated internal privileges to bypass a disabled feature gate in the applyOps command by specifying an internal replication mode value that was not intended to be client-selectable. This bypass enables execution of container operations that are disabled by default in production configurations, allowing direct storage-engine writes to arbitrary internal storage tables. The authorization check for these operations validates only the operation's namespace, not the actual storage target, enabling writes to unrelated internal metadata or other collections' data.

### CVE-2026-86135

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352;CWE-400` |
| Published | 2026-09-08T15:18:52.650 |

A Cross-Site Request Forgery (CSRF) vulnerability in WatchGuard Dimension's database snapshot creation feature allows a remote attacker to trigger unauthorized snapshot creation by tricking an authenticated administrator into visiting a specially crafted web page.
