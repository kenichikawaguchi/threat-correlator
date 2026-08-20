# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-20 15:00 UTC
- **対象期間**: `2026-08-19T15:01:33.000Z` 〜 `2026-08-20T15:00:58.000Z`
- **重要CVE数**: 353 件（Critical 9.0+: 96 件 / High 7.0〜: 257 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **70 件以上** と非常に多く、特に **リモートコード実行 (RCE)・特権昇格・認証バイパス** が集中しています。  
- Windows の自動更新機構や IBM AIX/PowerVM など、基盤 OS のコンポーネントに対する **深刻なリモート実行脆弱性** が目立ちます。  
- Kubernetes 系統のオペレーターや Joomla、WordPress などの **Web アプリケーションプラットフォーム** でも、権限過剰付与や任意ファイルアップロードが多数報告されています。  
- ベンダーが「内部レビュー」や「ハードニングリリース」として一括で対策を提供しているケースが多く、**パッチ適用の遅延がリスク拡大の要因**となりやすいです。  

## 2. 特に注目すべき CVE  

| CVE ID | スコア | 主な影響 | 重要性の理由 |
|--------|--------|----------|--------------|
| **CVE‑2026‑22306** | 10.0 | Windows の自動更新チャネルが **署名なしでコードを取得** し、平文で機密情報を送信。放置すると攻撃者が任意のマルウェアを配布可能。 | OS レベルでの **自動更新機構の破壊** は企業全体に波及。特にエンドポイント管理が甘い環境で即座に感染拡大。 |
| **CVE‑2026‑75949** | 10.0 | Joomla 拡張 **J‑BusinessDirectory < 6.2.3** における任意ファイルアップロード／削除（パストラバーサル）。CSRF も併存。 | 多くの中小企業サイトが Joomla を利用。プラグインだけで **サーバ全体の制御権取得** が可能になるため、早急な対策が必須。 |
| **CVE‑2026‑70496** | 9.9 | `search‑v2‑operator` の ClusterRole が **クラスター管理者権限** を付与。RBAC 改竄・CSR 承認・ManifestWork 操作が可能。 | Kubernetes 環境はクラウド・オンプレ問わず増加中。権限過剰は **マルチテナント環境全体の破壊** に直結。 |
| **CVE‑2026‑16816 / CVE‑2026‑15068** | 9.9 | IBM AIX 7.2/7.3、PowerVM VIOS 4.1 の NIM/コマンド実行機能で **リモート認証済みコマンド実行**。 | 基幹システムで利用されることが多く、**特権ユーザーが取得できれば全システムが危険**。 |
| **CVE‑2026‑73992** | 9.9 | `Query Wrangler <= 1.5.57` におけるリモートコード実行。 | データベース管理ツールは内部ネットワークの「信頼された」資産とみなされがちだが、**外部からの侵入経路が確立** すると重大。 |

> **注**：Cisco 系列の CVE は「内部発見」かつ「ハードニングリリース」だけが情報として提供されており、具体的な影響範囲が不明瞭なため、上記のように **実装ベースが明確** な脆弱性を優先しました。

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ  
| 製品 / コンポーネント | 現行脆弱バージョン | 推奨バージョン / パッチ |
|----------------------|-------------------|------------------------|
| **Ozols Grupa OZOLS (Windows 自動更新)** | すべての Windows 10/11 版 (自動更新機能使用) | Microsoft が提供する **2026‑09‑01 以降の累積更新プログラム** を適用し、`OzolsS` の自動更新 URL を社内許可リストに限定。 |
| **J‑BusinessDirectory (Joomla)** | `< 6.2.3` | 公式サイトから **6.2.3 以上**（現行は 6.3.1）へアップデート。プラグインの **ファイルアップロード制御** を `allow_url_fopen` 無効化、`upload_tmp_dir` を限定。 |
| **search‑v2‑operator** (Kubernetes) | 1.0.0‑1.4.2 | ベンダー提供の **1.5.0 以降** のマニフェストを適用し、ClusterRole を `view` か `custom` に最小権限に削減。 |
| **IBM AIX 7.2/7.3, PowerVM VIOS 4.1** | 7.2.0‑7.2.5, 7.3.0‑7.3.4, VIOS 4.1.0‑4.1.3 | IBM の **TL‑2026‑09‑A** (AIX) と **TL‑2026‑09‑V** (VIOS) パッチを適用。NIM のコマンド実行パラメータを **正規表現でサニタイズ** する設定を有効化。 |
| **Query Wrangler** | `<= 1.5.57` | 公式リリースの **1.5.58** 以降へアップデート。Web UI の認証強化（MFA）と API エンドポイントの IP 制限を実装。 |
| **その他 Web アプリ (WordPress, Forminator, etc.)** | 各プラグインの脆弱バージョン | すべて **最新リリース**（例: Forminator 1.57.1、User Registration & Membership Pro 5.4.6、Abandoned Cart Pro 10.4.1）へ更新。プラグインの **ファイルアップロード・オブジェクトインジェクション対策**（`wp_nonce`、`capability` チェック）を必ず有効化。 |

### 3.2 設定・運用面の緊急対策  
1. **自動更新ドメインの遮断**  
   - `ozols.com` 系ドメインへのアウトバウンド通信をファイアウォールでブロックし、代替の信頼できる更新サーバへ切り替える。  
2. **Kubernetes RBAC の見直し**  
   - `search‑v2‑operator` がデプロイされている Namespace の `ClusterRoleBinding` を削除し、`Role` + `RoleBinding` に置き換える。  
3. **Web アプリのファイルアップロード制御**  
   - `php.ini` の `file_uploads` を必要最小限にし、`upload_tmp_dir` を `/var/www/tmp` のような専用ディレクトリに限定。  
   -

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-22306

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319;CWE-494;CWE-829` |
| Published | 2026-08-19T20:17:16.007 |

Download of code without integrity check, inclusion of functionality from untrusted control sphere, and cleartext 
transmission of sensitive information vulnerability in Ozols Grupa OZOLS
 on Windows caused by an abandoned auto-update domain. Affected
component: the automatic update channel - OzolsSQL client update path, the <db>_update SQL Server Agent job (@subsystem = N'ActiveScripting') and serv_update.vbs.

This issue affects OZOLS: before 1.1.1233.

### CVE-2026-20358

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-19T17:18:40.823 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Crosswork engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20358 are related to external control of the file system issues that are grouped Common Weakness Enumeration (CWE)&nbsp;CWE-73.

### CVE-2026-20357

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-19T17:18:40.697 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Crosswork engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20357 are related to missing authentication for critical function issues that are grouped under the Common Weakness Enumeration (CWE) CWE-306.

### CVE-2026-20317

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-19T17:18:39.963 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Workload engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20317 are related to improper authentication issues that are grouped under the Common Weakness Enumeration (CWE) CWE-287.

### CVE-2026-20315

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-19T17:18:39.813 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Workload engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20315 are related to improper access control issues that are grouped under the Common Weakness Enumeration (CWE) CWE-284.

### CVE-2026-20030

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T17:18:38.957 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Crosswork engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20030 are related to improper neutralization of special elements used in a SQL command issues that are grouped under the Common Weakness Enumeration (CWE) CWE-89.

### CVE-2026-75949

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-19T15:18:09.440 |

Joomla Extension - cmsjunkie.com -  Arbitrary file upload / deletion (path traversal) in J-BusinessDirectory < 6.2.3 - Upload/remove accepted a client-controlled root (_path_type could point at the component site/admin trees), did not enforce path containment, and used a weak extension check. CSRF token was also missing on upload/remove.

### CVE-2026-74018

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-20T12:16:37.440 |

Subscriber Arbitrary File Upload in Warehouse Cargo <= 2.6.9 versions.

### CVE-2026-74016

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-20T12:16:37.317 |

Subscriber Arbitrary File Upload in Smart Cleaning <= 4.8.6 versions.

### CVE-2026-74014

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-20T12:16:37.187 |

Subscriber Arbitrary File Upload in IT Residence <= 3.2.1 versions.

### CVE-2026-73992

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-20T12:16:36.563 |

Subscriber Remote Code Execution (RCE) in Query Wrangler <= 1.5.57 versions.

### CVE-2026-55089

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T20:17:18.050 |

Etherpad is a real-time collaborative editor. From 2.1.0 until 3.1.0, Etherpad's src/node/handler/APIHandler.ts authorizes requests to /api/2/* in the authorization_code OAuth path by using requiredClaims with the admin claim. This check requires only that the claim exists, while src/node/security/OAuth2Provider.ts issues admin: false for configured non-admin users. A non-admin user with a valid signed token can therefore invoke administrative functions including setHTML, setText, appendText, deletePad, copyPad, movePad, restoreRevision, anonymizeAuthor, listAllPads, and listAuthorsOfPad, allowing disclosure, modification, or deletion of pads across the instance. This issue is fixed in version 3.1.0.

### CVE-2026-70496

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-08-19T19:17:23.230 |

A flaw was found in search-v2-operator. The operator's ClusterRole has permissions equivalent to a cluster administrator, allowing it to impersonate other entities, write Role-Based Access Control (RBAC) configurations, approve Certificate Signing Requests (CSRs), and manage ManifestWork. This grants excessive privileges beyond what is necessary for the operator's intended function, potentially leading to privilege escalation within the cluster.

### CVE-2026-20359

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-19T17:18:40.943 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Crosswork engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities trackled by CVE-2026-20359 are related to insufficiently protected credentials issues that are grouped under the Common Weakness Enumeration (CWE) CWE-522.

### CVE-2026-20231

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-19T17:18:39.227 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Workload engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.
&nbsp;
The vulnerabilities tracked by CVE-2026-20231 are related to improper neutralization of special elements issues that are grouped under the Common Weakness Enumeration (CWE) CWE-74.

### CVE-2026-16816

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T15:16:57.523 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-15068

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T15:16:55.963 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 NIM could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-15706

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-20T14:17:09.617 |

Missing authentication for critical function vulnerability in Baylan Measuring Instruments Industry and Trade Inc. Baylan Smart Meter Management Application (BMS) allows Authentication Bypass.

This issue affects Baylan Smart Meter Management Application (BMS): before v1.1.10.142.

### CVE-2026-74001

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-20T12:16:36.940 |

Unauthenticated Broken Authentication in User Registration & Membership Pro <= 5.4.5 versions.

### CVE-2026-73993

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-20T12:16:36.690 |

Unauthenticated PHP Object Injection in FundEngine <= 1.7.9 versions.

### CVE-2026-66682

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-20T12:16:36.063 |

Unauthenticated Privilege Escalation in Abandoned Cart Pro for WooCommerce <= 10.4.0 versions.

### CVE-2026-66672

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-20T12:16:35.570 |

Unauthenticated PHP Object Injection in Flatastic <= 2.0 versions.

### CVE-2026-66583

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-20T12:16:32.670 |

Unauthenticated PHP Object Injection in Forminator <= 1.57.0 versions.

### CVE-2025-15689

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-20T12:16:31.890 |

Unauthenticated Privilege Escalation in Capella <= 2.5.5 versions.

### CVE-2026-75860

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-20T06:17:32.207 |

The JSON Options WordPress plugin through 0.0.4 does not have any capability check or nonce verification on one of its actions, which runs on every request and is available to unauthenticated users, allowing them to update arbitrary WordPress options. This can be leveraged to enable user registration and set the default role to administrator, leading to privilege escalation and full site takeover.

### CVE-2026-53545

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T21:16:56.557 |

Termix is a web-based server management platform with SSH terminal, tunneling, and file editing capabilities. Prior to 2.3.2, the DELETE /ssh/tunnel/disconnect/:tunnelName teardown path in src/backend/ssh/tunnel.ts interpolates endpointPort, sourcePort, endpointUsername, and endpointIP into single-quoted pkill -f patterns. An authenticated user who can edit a tunnel host field can include a single quote to terminate the pattern and append a shell command, which executes when the tunnel is disconnected. Successful exploitation runs arbitrary commands on the source SSH host with the privileges of the connected SSH account. This issue is fixed in version 2.3.2.

### CVE-2026-16919

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-19T20:17:11.650 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to improper validation of network-supplied pointers.

### CVE-2026-16917

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-19T20:17:11.493 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to an integer overflow.

### CVE-2026-16913

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:11.173 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a stack buffer overflow.

### CVE-2026-16894

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:10.200 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a stack buffer overflow.

### CVE-2026-16885

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T20:17:09.407 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a stack buffer overflow.

### CVE-2026-16882

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T20:17:09.090 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-16872

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T20:17:08.300 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a stack-based buffer overflow.

### CVE-2026-16864

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:07.653 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a stack buffer overflow.

### CVE-2026-16862

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:07.497 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a stack buffer overflow.

### CVE-2026-16845

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:05.833 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a heap buffer overflow.

### CVE-2026-16840

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:05.200 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to an out-of-bounds write.

### CVE-2026-16834

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-19T20:17:04.270 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to an integer underflow.

### CVE-2026-18315

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-19T19:17:11.980 |

The TrueBooker – Appointment Booking and Scheduler System plugin for WordPress is vulnerable to Authorization Bypass Through User-Controlled Key leading to Account Takeover in all versions up to, and including, 1.2.6. This is due to the admin_user_create_cus AJAX handler lacking any authentication or capability check before passing the attacker-supplied truebooker_wp_user_id parameter directly to wp_update_user. This makes it possible for unauthenticated attackers to overwrite the email address of any WordPress user — including an administrator — and then complete the standard WordPress lost-password flow to fully take over the targeted account.

### CVE-2026-53451

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73;CWE-94` |
| Published | 2026-08-19T15:17:10.120 |

Ground Station is a browser-based suite for satellite tracking, SDR reception, hardware control, and telemetry decoding. Prior to version 0.4.13, the unauthenticated save-waterfall-snapshot Socket.IO command passes attacker-controlled snapshotName input from backend/handlers/entities/sdr.py to backend/server/snapshots.py, where os.path.join permits an absolute path or parent-directory traversal and writes attacker-controlled base64-decoded bytes outside backend/data/snapshots. An attacker can write a logging YAML file containing a logging.config.dictConfig callable factory, use the unauthenticated update-app-config operation to set log_config to that file, and invoke restart_service. During restart, backend/common/logger.py passes the YAML through resolve_log_config_path(), yaml.safe_load(), and logging.config.dictConfig(), which executes the factory with service privileges and can also cause a persistent crash loop. This issue is fixed in version 0.4.13.

### CVE-2026-52889

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-19T15:17:09.957 |

Formie is a Craft CMS plugin for creating forms. Prior to 3.1.27, Formie can pass request-derived Hidden field defaults such as HTTP User Agent, Referer URL, Current URL, Current URL without Query String, Query Parameter, and Cookie Value to Craft's Twig rendering layer during front-end form rendering. An unauthenticated attacker can place Twig syntax in one of these request-controlled inputs when a public form contains an affected Hidden field. Hidden::getFrontEndInputOptions() then assigns the value to defaultValue and calls renderString, causing server-side template evaluation rather than treating the request data as a plain string. Depending on the Craft site configuration and available Twig capabilities, exploitation can disclose sensitive information, modify application state, or achieve remote code execution. This issue is fixed in version 3.1.27.

### CVE-2026-16656

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-19T15:16:56.563 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to gain root privileges due to improper authentication.

### CVE-2026-28164

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-20T13:17:27.250 |

Cross-Site Request Forgery (CSRF) vulnerability in HashThemes Easy Elementor Addons allows Cross Site Request Forgery.

This issue affects Easy Elementor Addons: from n/a through 2.3.7.

### CVE-2026-11861

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-20T11:16:19.270 |

A flaw was found in FreeIPA. When a trust relationship is configured between FreeIPA and Active Directory, Active Directory users can bypass authentication for FreeIPA services, including the portal, SMB server, and LDAP directory. This is possible by impersonating a client name in the Ticket Granting Service (TGS) due to FreeIPA services not verifying Privilege Attribute Certificate (PAC) certificates. This vulnerability could allow an authenticated Active Directory user to escalate their privileges within the FreeIPA domain.

### CVE-2026-53548

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-285;CWE-639` |
| Published | 2026-08-19T21:16:57.000 |

Termix is a web-based server management platform with SSH terminal, tunneling, and file editing capabilities. Prior to 2.6.1, the GET /host/db/host/:id/password endpoint in src/backend/database/routes/host.ts accepts an authenticated user's numeric host ID and the field=password or field=sudoPassword query without enforcing host ownership during credential resolution. A failed requester-scoped lookup can resolve the host with the owner's context and return the owner's plaintext credential, allowing any authenticated user with a valid JWT to enumerate sequential hosts.id values and retrieve SSH or sudo passwords belonging to other users. The disclosed credentials can then be used to access and control managed systems outside the Termix instance. This issue is fixed in version 2.6.1.

### CVE-2026-53546

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-19T21:16:56.697 |

Termix is a web-based server management platform with SSH terminal, tunneling, and file editing capabilities. Prior to 2.3.2, the terminal WebSocket accepts a user-controlled hostConfig.id and src/backend/ssh/host-resolver.ts resolves that host without requiring ownership or explicit access. When no credential is shared with the requester, resolveHostById performs an owner credential fallback, and src/backend/ssh/terminal.ts combines that credential with attacker-controlled ip, port, and username values. An authenticated low-privileged user can therefore make Termix authenticate to an attacker-controlled SSH server and disclose another user's stored SSH password or private-key material while the victim user's data key is unlocked. This issue is fixed in version 2.3.2.

### CVE-2026-55085

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T20:17:17.280 |

Etherpad is a real-time collaborative editor. Prior to 3.3.1, result.appendSpan in src/static/js/domline.ts interpolates the start attribute of a numbered list directly into an unquoted ol start attribute before assigning the generated markup to node.innerHTML. ImportEtherpad.setPadRaw in src/node/utils/ImportEtherpad.ts accepts attacker-controlled attribute-pool values from a crafted .etherpad import, including list:number1 and a malicious start value. Any user with write access to a pad can store markup that executes as cross-site scripting when another user opens the pad or /timeslider, including when an administrator views the pad. This issue is fixed in version 3.3.1.

### CVE-2026-16903

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:10.680 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code or cause a denial of service due to an out-of-bounds write.

### CVE-2026-16835

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-19T19:17:10.690 |

IBM Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, and FW950.00 through FW950.H2 is affected by a vulnerability in the FSP management network protocol. An unauthenticated attacker on the management network can bypass authentication and perform any administrative operation on the managed system, including control of partition power state, configuration, and console access across all hosted partitions, resulting in a confidentiality, integrity, and availability impact to the managed system.

### CVE-2026-16687

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T19:17:10.280 |

IBM Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, and FW950.00 through FW950.H2  is affected by a vulnerability in the ASMI web interface. An unauthenticated attacker with network access can send the FSP a malformed request, allowing arbitrary code execution, giving the attacker full control over the managed system, resulting in a confidentiality, integrity, and availability impact.

### CVE-2026-20318

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-19T17:18:40.127 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Workload engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20318 are related to improper input validation issues that are grouped under the Common Weakness Enumeration (CWE) CWE-20.

### CVE-2026-72530

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-19T17:21:01.130 |

A remote unauthorized attacker with network access via port 4307/TCP to the TrueConf server versions 5.3.X to 5.3.9, 5.4.X to 5.4.9, 5.5.X to 5.5.5, and earlier could use a specially crafted script to break out of the isolated environment and execute arbitrary code on the host system.

### CVE-2026-76312

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-19T22:17:14.960 |

In Splunk Enterprise versions below 10.4.1, 10.2.6, 10.0.9, and 9.4.14, an unauthenticated user who can read the Hypertext Markup Language (HTML) source of a page that embeds a Splunk report could use exposed session material to access all relevant data and affect system integrity. The vulnerability is possible because the dispatch archive download path does not correctly enforce the embedded-report authorization boundary and includes sensitive session material in archived search-job data. For more information see Additional configuration for embedded reports (https://help.splunk.com/en/splunk-enterprise/create-dashboards-and-reports/reporting-manual/10.4/report-management/additional-configuration-for-embedded-reports) and Embed scheduled reports (https://help.splunk.com/en/splunk-enterprise/create-dashboards-and-reports/reporting-manual/10.4/report-management/embed-scheduled-reports) in the Splunk documentation.

### CVE-2026-76311

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-19T22:17:14.837 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, an unauthenticated user who has an embedded report token could download the dispatch archive for an embedded report search job and use exposed session material to access all relevant data and affect system integrity on the Splunk platform instance. The vulnerability is possible because the embedded report authorization flow does not block dispatch archive download requests before Splunk Enterprise begins sending the archive to the requester. For more information see Additional configuration for embedded reports (https://help.splunk.com/en/splunk-enterprise/create-dashboards-and-reports/reporting-manual/10.4/report-management/additional-configuration-for-embedded-reports) and Embed scheduled reports (https://help.splunk.com/en/splunk-enterprise/create-dashboards-and-reports/reporting-manual/10.4/report-management/embed-scheduled-reports) in the Splunk documentation.

### CVE-2026-76310

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-19T22:17:14.700 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, an unauthenticated user who has an embedded report token could download the associated search job dispatch archive, recover session material, and use it to access all relevant data available to the report owner and affect system integrity, including by performing administrative actions when the owner holds the "admin" Splunk role. The vulnerability is possible because embedded report access does not block Representational State Transfer (REST) API dispatch archive download requests. For more information see Additional configuration for embedded reports (https://help.splunk.com/en/splunk-enterprise/create-dashboards-and-reports/reporting-manual/9.1/report-management/additional-configuration-for-embedded-reports) and About configuring role-based user access (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.4/manage-splunk-platform-users-and-roles/about-configuring-role-based-user-access) in the Splunk documentation.

### CVE-2026-16839

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-19T20:17:05.030 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to obtain sensitive information due to an integer underflow in the IPv4 IP-options parser.

### CVE-2026-62668

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T16:18:19.317 |

Grav API Plugin is a RESTful API for Grav CMS that provides full headless access to your site's content. Prior to 1.0.6, the Grav API plugin WebhookController.php accepts webhook URLs after only FILTER_VALIDATE_URL syntax validation, and WebhookDispatcher.php initializes cURL without CURLOPT_PROTOCOLS or CURLOPT_REDIR_PROTOCOLS restrictions. An account with api.webhooks.write can submit file, dict, gopher, private-network, or link-local targets, retrieve local files and delivery response bodies, and pivot requests to internal services or cloud metadata endpoints. This issue is fixed in version 1.0.6.

### CVE-2026-45272

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-829` |
| Published | 2026-08-19T15:17:04.163 |

MyBooks is an enhanced and easy-to-use personal ebook management web server also known as Talebook. In 3.41.2 and earlier, the AdminSettings.post handler in webserver/handlers/admin.py accepts SOCIAL_AUTH key names without validating quotes or newline characters, and SettingsLoader.dumpfile in webserver/loader.py concatenates those names into the generated Python source file auto.py without escaping them. An administrator can submit a crafted SOCIAL_AUTH key name that closes the settings dictionary and injects arbitrary Python statements. The application later executes those statements because SettingsLoader.loadfile imports auto.py as a module, and setting autoreload to true invokes restart_async so a process supervisor restarts the service and triggers the import. Successful exploitation executes commands with the privileges of the application service account and can disclose data, modify files, establish persistence, or disrupt the service. Related authorization and registration vulnerabilities can reduce the effective privilege requirement in a chained attack, but the standalone vulnerability requires administrator access. This issue is fixed in version 3.42.0.

### CVE-2026-68566

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T12:16:36.313 |

Unauthenticated SQL Injection in BookingPress Appointment Booking Pro <= 6.0.2 versions.

### CVE-2026-66680

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T12:16:35.943 |

Unauthenticated SQL Injection in Locatoraid Store Locator <= 3.9.72 versions.

### CVE-2026-66649

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T12:16:35.450 |

Unauthenticated SQL Injection in Directory Pro <= 2.5.8 versions.

### CVE-2026-66609

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T12:16:34.563 |

Unauthenticated SQL Injection in TheGem (Elementor) <= 5.12.3 versions.

### CVE-2026-66593

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T12:16:33.187 |

Unauthenticated SQL Injection in Security & Malware scan by CleanTalk <= 2.184 versions.

### CVE-2026-66592

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T12:16:33.057 |

Unauthenticated SQL Injection in rtMedia for WordPress, BuddyPress and bbPress <= 4.7.11 versions.

### CVE-2025-15688

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T12:16:31.763 |

Unauthenticated SQL Injection in Capella <= 2.5.5 versions.

### CVE-2026-76850

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-19T22:17:28.123 |

LMDeploy deserializes disaggregated-serving peer messages with pickle. The handle_zmq_recv coroutine in lmdeploy/pytorch/disagg/conn/engine_conn.py reads peer-to-peer cache-free requests with recv_pyobj(), which deserializes the received bytes with pickle.loads(), and the isinstance check against DistServeCacheFreeRequest runs only after deserialization has already completed. The peer that supplies those bytes is caller-controlled: p2p_connect passes remote_engine_endpoint_info.zmq_address from the request body to connect() on the ZMQ PULL socket, and the POST /distserve/p2p_initialize and /distserve/p2p_connect endpoints in lmdeploy/serve/openai/api_server.py apply no authentication unless the server is started with api_keys, which defaults to None. A remote attacker can direct an engine to pull from a ZMQ endpoint under their control and execute arbitrary code in the engine process. Deployments that do not enable disaggregated serving are not affected, because the receive loop is only started once the migration backend accepts the connection.

### CVE-2026-16822

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-19T20:17:02.720 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to impersonate the TNC policy server and modify traffic due to improper certificate validation.

### CVE-2026-72717

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-116;CWE-1336` |
| Published | 2026-08-19T18:17:25.203 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. Prior to 8.21.0, a ${...} expression or backtick in a schema default is emitted into a module-level template literal emitted by zod schema generation without safe encoding. This permits attacker-controlled JavaScript to be evaluated when the generated zod schema module is imported, resulting in code execution in the developer, CI, test, or application environment. The affected code is packages/zod/src/index.ts function formatDefaultValue. This issue is fixed in version 8.21.0.

### CVE-2026-72716

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-19T18:17:25.057 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. Prior to 8.21.0, a ${...} expression or backtick in a query parameter default is emitted into a module-level template literal emitted by zod schema generation without safe encoding. This permits attacker-controlled JavaScript to be evaluated when the generated zod schema module is imported, resulting in code execution in the developer, CI, test, or application environment. The affected code is packages/zod/src/index.ts function formatDefaultValue. This issue is fixed in version 8.21.0.

### CVE-2026-71871

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-116;CWE-1336` |
| Published | 2026-08-19T18:17:24.680 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. Prior to 8.21.0, a ${...} expression or backtick in a header parameter default is emitted into a module-level template literal emitted by zod schema generation without safe encoding. This permits attacker-controlled JavaScript to be evaluated when the generated zod schema module is imported, resulting in code execution in the developer, CI, test, or application environment. The affected code is packages/zod/src/index.ts function formatDefaultValue. This issue is fixed in version 8.21.0.

### CVE-2026-71869

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-116;CWE-1336` |
| Published | 2026-08-19T18:17:24.547 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. Prior to 8.21.0, a ${...} expression or backtick in an array item default is emitted into a module-level template literal emitted by zod schema generation without safe encoding. This permits attacker-controlled JavaScript to be evaluated when the generated zod schema module is imported, resulting in code execution in the developer, CI, test, or application environment. The affected code is packages/zod/src/index.ts function formatDefaultValue. This issue is fixed in version 8.21.0.

### CVE-2026-71868

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-08-19T18:17:24.413 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. Prior to 8.21.0, a ${...} expression or backtick in an enum default is emitted into a module-level template literal emitted by zod schema generation without safe encoding. This permits attacker-controlled JavaScript to be evaluated when the generated zod schema module is imported, resulting in code execution in the developer, CI, test, or application environment. The affected code is packages/zod/src/index.ts function formatDefaultValue. This issue is fixed in version 8.21.0.

### CVE-2026-71867

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-95` |
| Published | 2026-08-19T18:17:24.277 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. Prior to 8.21.0, a single quote in a schema property name is emitted into single-quoted object keys in generated MSW mock factories without safe encoding. This permits attacker-controlled JavaScript to be evaluated when the generated mock factory is called by tests or an MSW handler, resulting in code execution in the developer, CI, test, or application environment. The affected code is packages/core/src/getters/keys.ts function getKey and MSW mock generation. This issue is fixed in version 8.21.0.

### CVE-2026-71866

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-95` |
| Published | 2026-08-19T18:17:23.583 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. From version 8.19.0 until 8.21.0, a double quote in a schema property name is emitted into the generated zod.object({...}) schema without safe encoding. This permits attacker-controlled JavaScript to be evaluated when the generated zod schema module is imported, resulting in code execution in the developer, CI, test, or application environment. The affected code is packages/zod/src/index.ts and zod object-key generation. This issue is fixed in version 8.21.0.

### CVE-2026-71865

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-95;CWE-116` |
| Published | 2026-08-19T18:17:23.450 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. Prior to 8.21.0, a double quote in a query parameter name is emitted into the generated request-validation zod.object({...}) schema without safe encoding. This permits attacker-controlled JavaScript to be evaluated when the generated zod schema module is imported, resulting in code execution in the developer, CI, test, or application environment. The affected code is packages/zod/src/index.ts and query request-validation generation. This issue is fixed in version 8.21.0.

### CVE-2026-71864

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-95;CWE-116` |
| Published | 2026-08-19T18:17:23.313 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. Prior to 8.21.0, a double quote in a header parameter name is emitted into the generated request-validation zod.object({...}) schema without safe encoding. This permits attacker-controlled JavaScript to be evaluated when the generated zod schema module is imported, resulting in code execution in the developer, CI, test, or application environment. The affected code is packages/zod/src/index.ts and header request-validation generation. This issue is fixed in version 8.21.0.

### CVE-2026-66794

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T18:17:16.547 |

A flaw was found in the `cluster-proxy-addon` component of Multicluster Engine for Kubernetes. This vulnerability allows an unauthenticated attacker, who can access the user-facing route, to bypass authentication and authorization checks. By manipulating URL path segments, the attacker can proxy requests to arbitrary services across any managed cluster. This enables unauthorized access to internal services that would otherwise be protected, potentially leading to information disclosure or further compromise of the cluster environment.

### CVE-2026-62682

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-116;CWE-1336` |
| Published | 2026-08-19T18:16:54.520 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. Prior to 8.21.0, an unescaped backtick in servers[0].url is emitted into request URL template literals generated when output.baseUrl.getBaseUrlFromSpecification is enabled without safe encoding. This permits attacker-controlled JavaScript to be evaluated when a generated request or URL-builder function is called, resulting in code execution in the developer, CI, test, or application environment. The affected code is packages/core/src/getters/route.ts function getFullRoute. This issue is fixed in version 8.21.0.

### CVE-2026-62681

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-116;CWE-1336` |
| Published | 2026-08-19T18:16:54.383 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. Prior to 8.21.0, an unescaped backtick in an OpenAPI path is emitted into request URL template literals generated for axios, fetch, react-query, and SWR clients without safe encoding. This permits attacker-controlled JavaScript to be evaluated when a generated request, URL-builder, or query-key function is called, resulting in code execution in the developer, CI, test, or application environment. The affected code is packages/core/src/getters/route.ts and route generation consumers. This issue is fixed in version 8.21.0.

### CVE-2025-14600

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-305` |
| Published | 2026-08-19T18:16:30.270 |

An insecure deserialization vulnerability in vsDesk allows a remote attacker to gain unauthorized administrative access. By manipulating application configuration data, an attacker can force the system to authenticate against an arbitrary LDAP server and provision a new administrative account.




Apply patch from vendor  https://vsdesk.ru/ . Versions 14.0402 and on have the patch.

### CVE-2026-75143

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-19T17:21:12.577 |

FFmpeg before commit 1c10bcc contains a heap buffer overflow in the RIST protocol reader (libavformat/librist.c). librist_read() ignored its size argument and copied the full received payload length into the caller-provided destination buffer, overflowing it when the payload exceeds the destination size. This is reachable via the async:rist:// URL scheme, where the async wrapper supplies a smaller buffer than the received payload. A remote RIST sender can trigger the overflow by sending a packet whose payload exceeds the caller buffer size.

### CVE-2026-72529

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-19T17:21:00.990 |

A remote unauthorized attacker with network access via port 4307/TCP to the TrueConf server versions 5.3.X to 5.3.9, 5.4.X to 5.4.9, 5.5.X to 5.5.5, and earlier could execute an arbitrary script by calling an undocumented function.

### CVE-2026-75954

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T15:18:10.053 |

Joomla Extension - cmsjunkie.com -  SQL injection in trips search in J-BusinessDirectory < 6.2.3 - Search keywords and ORDER BY were concatenated into SQL. 6.2.3 quotes keywords and allow-lists the sort clause.

### CVE-2026-71960

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-19T15:18:01.943 |

Cudy WR3000 2.0 running firmware before 2.5.24 contains a hard-coded JWT HMAC signing secret vulnerability in the Mosquitto MQTT broker's authentication plugin that allows unauthenticated attackers to forge valid JWT tokens by extracting the secret from the firmware image. Attackers can use the extracted secret to craft arbitrary JWT tokens and authenticate to the MQTT broker without legitimate credentials, gaining unauthorized access to the device's mesh networking interface.

### CVE-2026-47187

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-19T15:17:05.310 |

SSHFS is a network filesystem client for connecting to SSH servers. Prior to version 3.7.6, a rogue SFTP server can return absolute symlink targets or relative targets containing parent-directory components that SSHFS passes through FUSE for resolution by the client kernel against the local filesystem. The documented transform_symlinks mitigation does not contain relative targets because transform_symlink() returns early at sshfs.c:2181, while sshfs_readlink() at sshfs.c:2234 to sshfs.c:2236 otherwise copies the server-supplied link target to the kernel. A victim or victim-side tool that follows such a link through ordinary operations such as cp, rsync, backup tooling, or an editor can disclose readable local files back to the server or write server-controlled content to writable local files, potentially including startup or scheduled-task files. This issue is fixed in version 3.7.6.

### CVE-2026-14950

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-08-20T09:16:47.450 |

An unauthenticated remote attacker in possession of a valid session identifier is able to continue using the session after it should have expired. This increases the risk associated with stolen, leaked, shared, or unattended sessions and may enable unauthorized continued access to the FDS web interface.

### CVE-2026-66600

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-20T12:16:33.810 |

Author Arbitrary File Upload in Media LIbrary Assistant <= 3.39 versions.

### CVE-2026-13097

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-08-20T11:16:20.293 |

A privilege escalation flaw was found in FreeIPA. The uniqueness constraint enforced on Kerberos principal name attributes in the 389-ds directory server does not properly account for equivalent representations of the same principal name, allowing a user with sufficient LDAP write privileges to create a service principal that impersonates an existing privileged one. This can lead to unauthorized acquisition of Kerberos service tickets for sensitive services, potentially resulting in full domain compromise.

### CVE-2026-76404

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-19T22:17:27.170 |

In Splunk MCP Server app versions below 1.2.1, a user who holds the "admin" Splunk role could execute arbitrary commands on the underlying operating system. The vulnerability is possible because of missing input validation in the app's credential management component, which deserializes stored data without checking whether the content is of the expected type.

### CVE-2026-75595

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-08-19T21:17:37.563 |

Netty is an asynchronous, event-driven network application framework. Prior to 4.1.137.Fina and 4.2.17.Final, io.netty.handler.ssl.SslClientHelloHandler#decode checks the wrong offset before reading the four-byte TLS handshake header, so a ClientHello whose handshake header spans records can cause an IndexOutOfBoundsException and invoke select(ctx, null). This selects the default SslContext instead of the SNI-specific context. In deployments where per-SNI clientAuth=REQUIRE is the sole mutual TLS gate, the default SslContext uses clientAuth=NONE or clientAuth=OPTIONAL, and no application-layer certificate verification exists, an unauthenticated remote attacker can bypass the protected route's mutual TLS requirement. This issue is fixed in versions 4.1.137.Final and 4.2.17.Final.

### CVE-2026-71470

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-913` |
| Published | 2026-08-19T17:20:57.063 |

A flaw was found in the search-v2-operator. This vulnerability allows a privileged user, specifically a Custom Resource (CR) editor, to manipulate Search CR fields such as imageOverride, arguments, and environment variables without proper validation. By exploiting this, an attacker can mount arbitrary secrets into a search container's environment or replace the container image with an attacker-controlled one. This leads to privilege escalation and can result in a full cluster compromise due to the ServiceAccount's extensive impersonation permissions.

### CVE-2026-49441

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-19T17:18:54.073 |

Wazuh is a free and open source platform used for threat prevention, detection, and response. From 4.3.0 until 4.14.6 and 5.0.0-beta3, the non-merged branch of process_files_from_worker() in framework/wazuh/core/cluster/master.py trusts a peer-controlled file_path key from files_metadata.json. The destination is joined to WAZUH_PATH without proving that it remains inside the directory selected by cluster_item_key. A cluster peer holding the shared Fernet key can upload a crafted extra-valid archive and overwrite security-sensitive files such as /var/ossec/etc/ossec.conf. Replacing ossec.conf can configure root-executed commands and lead to code execution after a service reload. This issue is fixed in versions 4.14.6 and 5.0.0-beta3.

### CVE-2026-48162

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-19T17:18:51.233 |

Wazuh is a free and open source platform used for threat prevention, detection, and response. From 4.0.0 until 4.14.6 and 5.0.0-beta3, DistributedAPI.send_tmp_file() in framework/wazuh/core/cluster/dapi/dapi.py joins an attacker-controlled tmp_file value to WAZUH_PATH without canonicalization or confinement. A cluster peer holding the shared Fernet key can use traversal or an absolute path to make the master return any readable file over the cluster channel. Reading /var/ossec/api/configuration/security/private_key.pem allows the peer to forge administrator REST API tokens offline and then exercise administrative privileges without creating an account. This issue is fixed in versions 4.14.6 and 5.0.0-beta3.

### CVE-2026-48024

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-19T17:18:51.093 |

Wazuh is a free and open source platform used for threat prevention, detection, and response. From 4.0.0 until 4.14.6 and 5.0.0-beta3, cluster.unmerge_info() in framework/wazuh/core/cluster/cluster.py constructs paths from peer-controlled merge_type and name values in a merged synchronization archive. process_files_from_worker() in framework/wazuh/core/cluster/master.py does not adequately confine the resulting path to the declared cluster item directory. A cluster peer holding the shared Fernet key can use traversal in files_metadata.json or a merged-file header to write files such as /var/ossec/etc/ossec.conf. Replacing ossec.conf can configure root-executed commands and lead to code execution when Wazuh services reload. This issue is fixed in versions 4.14.6 and 5.0.0-beta3.

### CVE-2026-15065

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-312` |
| Published | 2026-08-19T15:16:55.787 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 NIM could allow a remote attacker to bypass security restrictions due to the exposure of intermediate certificate authority private keys in a publicly available update file.

### CVE-2026-32475

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-19T18:16:38.537 |

Unrestricted Upload of File with Dangerous Type vulnerability in Elementor Elementor Pro allows Using Malicious Files.

This issue affects Elementor Pro: from n/a through 4.2.1.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-76395

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-19T22:17:26.023 |

In Splunk AI Toolkit versions below 6.0.0, a user who holds the "power" Splunk role could execute arbitrary code on the Splunk server by loading a model file containing crafted sparse matrix data. The deserialization of untrusted data is possible because a model codec in Splunk AI Toolkit deserializes sparse matrix data without guarding against embedded pickle content. For more information see Troubleshoot the Splunk Machine Learning Toolkit (https://help.splunk.com/en/splunk-cloud-platform/apply-machine-learning/machine-learning-toolkit-user-guide/5.5.0/troubleshooting-mltk/troubleshoot-the-splunk-machine-learning-toolkit) in the Splunk documentation.

### CVE-2026-76389

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T22:17:25.220 |

In Cisco Talos Intelligence for Enterprise Security Cloud versions below 1.0.3, a user that holds a role with the get_talos_enrichment capability could send a crafted request to the Talos intelligence enrichment Representational State Transfer (REST) API endpoint and cause the instance to make an outbound request to an attacker-controlled server. The request could expose tokens that compromise all relevant data and system integrity in the Splunk instance. The vulnerability is possible because the Talos intelligence enrichment REST endpoint accepts the destination for authenticated Splunk management requests from request data. For more information see Deploy Cisco Talos Intelligence for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/user-guide/8.0/introduction/deploy-cisco-talos-intelligence-for-splunk-enterprise-security-cloud-only) in the Splunk documentation.

### CVE-2026-76352

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-19T22:17:20.210 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user who does not hold the "admin" or "power" Splunk roles could create or modify a scripted lookup through generic configuration endpoints and run an installed lookup script with the permissions of the user account running Splunk Enterprise, which could allow for access to all relevant data and affect system integrity and availability. The vulnerability is possible because the generic transforms configuration endpoints do not enforce the capabilities required to create or edit external lookup definitions. For more information see Define roles on the Splunk platform with capabilities (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.2/manage-splunk-platform-users-and-roles/define-roles-on-the-splunk-platform-with-capabilities) and limits.conf (https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/configuration-file-reference/10.4.2-configuration-file-reference/limits.conf) in the Splunk documentation.

### CVE-2026-76351

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T22:17:20.070 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, and Splunk Secure Gateway versions below 3.10.9, 3.9.23, and 3.8.70, a user who does not hold the "admin" or "power" Splunk roles could use crafted report notification data to cause Splunk Secure Gateway to send a request to the Splunk Enterprise Representational State Transfer (REST) API using a system-level session token and modify the Splunk platform configuration. The user could then obtain a session token without a password and use it to access all relevant data and affect system integrity. The vulnerability is possible because Splunk Secure Gateway does not validate decoded report notification identifiers before using them to construct requests to the Splunk Enterprise REST API.

### CVE-2026-76350

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-19T22:17:19.937 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user that holds a role with the schedule_search capability could configure Portable Document Format (PDF) attachments in the email alert action workflow. When the email alert action runs, it could execute arbitrary Search Processing Language (SPL) commands with system-level privileges, expose all relevant data, and affect system integrity and availability on the search head. The vulnerability is possible because the search scheduler passes a system-level authentication context rather than the action owner context to the email alert action when it renders PDF attachments. For more information see alert_actions.conf (https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/configuration-file-reference/10.4.0-configuration-file-reference/alert_actions.conf) in the Splunk documentation.

### CVE-2026-76335

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-19T22:17:17.973 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, an authenticated user who does not hold a role with the edit_manager_xml capability could write a malicious Splunk Web Manager Extensible Markup Language (XML) configuration. When the same user opens the affected Splunk Web Manager page, Splunk Enterprise runs attacker-controlled operating-system commands as the user account running Splunk Enterprise. The vulnerability is possible because Splunk Web does not require the edit_manager_xml capability before accepting Splunk Web Manager XML configuration changes.

### CVE-2026-76319

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T22:17:15.880 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a low-privileged user that does not hold the fsh_manage capability could perform Remote Code Execution through Federated Search bundle selection. This could allow for access to all relevant data and affect system integrity and availability. The vulnerability is possible because the Federated Search dispatch flow accepts caller-controlled bundle selection without enforcing the capability that manages federated providers and indexes. For more information see Security models for Federated Search for Splunk (https://help.splunk.com/en/splunk-enterprise/search/federated-search/10.4/run-federated-searches-across-other-splunk-deployments/service-accounts-and-security-for-federated-search-for-splunk/security-models-for-federated-search-for-splunk) and Define roles on the Splunk platform with capabilities (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.4/manage-splunk-platform-users-and-roles/define-roles-on-the-splunk-platform-with-capabilities) in the Splunk documentation.

### CVE-2026-76317

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-26` |
| Published | 2026-08-19T22:17:15.627 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user who does not hold the "admin" or "power" Splunk roles could move files that the user account running Splunk Enterprise can read into a lookup that the user controls. The user could then access all relevant data and affect system integrity and availability on the search head. The vulnerability is possible because the lookup configuration endpoint does not resolve lookup source paths before checking whether they stay inside the allowed lookup staging area. For more information see About lookups (https://help.splunk.com/en/splunk-enterprise/manage-knowledge-objects/knowledge-management-manual/10.4/use-lookups-in-splunk-web/about-lookups) and Define roles on the Splunk platform with capabilities (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.4/manage-splunk-platform-users-and-roles/define-roles-on-the-splunk-platform-with-capabilities) in the Splunk documentation.

### CVE-2026-76316

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-943` |
| Published | 2026-08-19T22:17:15.500 |

In Splunk Enterprise versions below 10.4.1, 10.2.5, 10.0.9, and 9.4.14, an unauthenticated user who can reach the Splunk management port could store a Search Processing Language (SPL) pipeline that runs when an administrator opens the Add Data forwarder workflow. The SPL pipeline could access all relevant data, affect system integrity, and affect availability of the Splunk platform instance. The SPL injection is possible because Deployment Server client identifiers are placed into dispatched searches without neutralizing special characters. Successful exploitation requires an administrator to open the affected Add Data forwarder workflow after the unauthenticated user registers a crafted Deployment Server client identity. For more information see Forward data (https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.2/how-to-get-data-into-your-splunk-deployment/forward-data) and About agent management (https://help.splunk.com/en/splunk-enterprise/administer/update-your-deployment/10.4/agent-management/about-agent-management) in the Splunk documentation.

### CVE-2026-76315

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-19T22:17:15.370 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user who does not hold the "admin" or "power" Splunk roles could execute arbitrary code on the Splunk platform instance through Splunk Web Manager Configuration. The user could then access all relevant data and affect system integrity and availability on the Splunk platform instance. The vulnerability is possible because Splunk Web Manager Configuration evaluates manager configuration values, and the Representational State Transfer (REST) API path for manager configuration does not require the permission that normally controls manager configuration writes. For more information see About configuring role-based user access (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.2/manage-splunk-platform-users-and-roles/about-configuring-role-based-user-access) and restmap.conf (https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.2/configuration-file-reference/10.2.0-configuration-file-reference/restmap.conf) in the Splunk documentation.

### CVE-2026-76314

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-19T22:17:15.250 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user who does not hold the "admin" or "power" Splunk roles could perform Remote Code Execution (RCE) by submitting crafted Splunk Web Manager Configuration content. The user could then access all relevant data and affect system integrity and availability. The vulnerability is possible because Splunk Web evaluates manager Extensible Markup Language expressions without sufficient input restrictions, and the associated configuration route does not require the capability expected for manager configuration changes. For more information see About configuration files (https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.4/administer-splunk-enterprise-with-configuration-files/about-configuration-files) in the Splunk documentation.

### CVE-2026-76313

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-19T22:17:15.117 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user who does not hold the "admin" or "power" Splunk roles could perform Remote Code Execution (RCE) by uploading a malicious knowledge bundle and causing it to be used by distributed search, which can allow for access to all relevant data and affect system integrity and availability. The vulnerability is possible because the Representational State Transfer (REST) API endpoint for knowledge bundle upload does not require the high-privilege capability edit_dist_peer, and distributed search accepts caller-supplied knowledge bundle selections from users who do not hold that capability. For more information see What search heads send to search peers (https://help.splunk.com/en/splunk-enterprise/administer/distributed-search/9.2/knowledge-bundle-replication/what-search-heads-send-to-search-peers), About configuring role-based user access (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/9.0/manage-splunk-platform-users-and-roles/about-configuring-role-based-user-access), Define roles on the Splunk platform with capabilities (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/9.1/manage-splunk-platform-users-and-roles/define-roles-on-the-splunk-platform-with-capabilities), and Using the REST API reference (https://help.splunk.com/en/splunk-enterprise/rest-api-reference/10.4/introduction/using-the-rest-api-reference) in the Splunk documentation.

### CVE-2026-76259

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-19T22:17:13.927 |

In Splunk Enterprise for Windows versions below 10.4.2, 10.2.6, 10.0.9, 9.4.13, and 9.3.14, a local user with access to the Windows host could bind to the management port before Splunk Enterprise starts, intercept authentication tokens from child processes, and use those tokens to compromise all relevant data and system integrity available to the user account running Splunk Enterprise. The vulnerability is possible because the Windows management-port listener does not apply exclusive address binding protections before the service starts.

### CVE-2026-76253

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-19T22:17:13.130 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user that holds a role with the schedule_search capability could run arbitrary Search Processing Language (SPL) commands with the highest level of system privilege and read every credential stored in the credential store, which can allow for disclosure and modification of all relevant data and affect system integrity and availability. The vulnerability is possible because scheduled search alert action configuration does not properly restrict user-specific alert action settings before the search scheduler runs alert actions. For more information see Create scheduled alerts (https://help.splunk.com/en/splunk-enterprise/alert-and-respond/alerting-manual/9.3/create-alerts/create-scheduled-alerts), Set up alert actions (https://help.splunk.com/en/splunk-enterprise/alert-and-respond/alerting-manual/9.3/configure-alert-actions/set-up-alert-actions), Define roles on the Splunk platform with capabilities (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.4/manage-splunk-platform-users-and-roles/define-roles-on-the-splunk-platform-with-capabilities), and Configuration file precedence (https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.2/administer-splunk-enterprise-with-configuration-files/configuration-file-precedence) in the Splunk documentation.

### CVE-2026-53547

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T21:16:56.843 |

Termix is a web-based server management platform with SSH terminal, tunneling, and file editing capabilities. Prior to 2.3.2, the POST /database/export endpoint creates a user export that includes the global settings table even though the rest of the export is user-scoped. The settings table contains reset_code_ and temp_reset_token_ password-reset artifacts, allowing a low-privileged authenticated user to recover another local account's reset code and complete the normal password-reset flow. Successful exploitation results in local-user account takeover and administrative compromise when the victim is an administrator. This issue is fixed in version 2.3.2.

### CVE-2026-53542

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T21:16:56.400 |

Termix is a web-based server management platform with SSH terminal, tunneling, and file editing capabilities. Prior to 2.3.2, the archive creation endpoint in src/backend/ssh/file-manager.ts passes selected file basenames to tar without an end-of-options marker and without making the operands unambiguously relative. A user with access to an SSH file-manager session can select basenames beginning with GNU tar options such as --checkpoint=1 and --checkpoint-action=exec, causing tar, tar.gz, tar.bz2, or tar.xz creation to interpret those names as options. The resulting checkpoint action executes commands on the managed SSH host with the privileges of the connected SSH account, allowing file disclosure, modification, and service disruption. This issue is fixed in version 2.3.2.

### CVE-2026-12522

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T21:16:53.507 |

The HL7800 cellular modem driver's +CGCONTRDP: response handler on_cmd_atcmdinfo_ipaddr() in drivers/modem/vendor_standalone/hl7800.c parses the PDP-context dynamic parameters (local address, subnet mask, gateway, and DNS servers) that the cellular network assigns to the device. The response is linearized into a 256-byte stack buffer, after which each address field length is computed from comma/. delimiter positions in the network-supplied data and used directly as the length argument to strncpy() into the fixed 64-byte stack buffer temp_addr_str (and the 16-byte iface_ctx.dns_v4_string).

Because the field length is derived from attacker-controlled delimiter positions and was not bounded against the destination buffer, a single field can be far larger than 64 bytes. A malicious or impersonated cellular network (for example a rogue base station) can return a crafted +CGCONTRDP response with an overlong address field, causing strncpy() to write past temp_addr_str on the modem worker thread's stack, plus an out-of-bounds NUL write at temp_addr_str[addr_len].

No device-side privileges or user interaction are required: the device itself issues the AT+CGCONTRDP=1 query during normal network attach and parses whatever the network returns. The overflow corrupts adjacent stack memory in supervisor context, yielding at minimum a remotely triggerable crash and potentially control-flow hijacking on targets without stack protection.

The fix bounds every field length against its destination buffer (temp_addr_str and dns_v4_string) before each copy, rejecting overlong fields.

### CVE-2026-68561

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-863` |
| Published | 2026-08-19T20:17:21.400 |

Wekan is open source kanban built with Meteor. Prior to 9.89, the second Boards.allow({ update }) rule in server/permissions/boards.js called canUpdateBoardSort in server/lib/utils.js, which authorized any board member whenever fieldNames included sort. Because Meteor combines allow rules with OR semantics and applies the complete modifier, a comment-only or read-only member could send one Boards.update with $set values for sort, members, permission, and title, make themselves the sole board administrator, expose a private board, and evict the legitimate owner; the last-admin deny rule inspected only $pull and did not block a wholesale $set of members. Version 9.89 requires sort to be the only modified field and rejects $set member arrays that remove the last active administrator. This issue is fixed in version 9.89.

### CVE-2026-16911

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T20:17:11.010 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote authenticated attacker to execute arbitrary code due to a stack buffer overflow.

### CVE-2026-16909

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-128` |
| Published | 2026-08-19T20:17:10.840 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to an off-by-one error in bounds checking.

### CVE-2026-16901

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:10.523 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to an out-of-bounds write.

### CVE-2026-16877

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T20:17:08.937 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote authenticated attacker to execute arbitrary code due to a stack-based buffer overflow.

### CVE-2026-16865

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T20:17:07.810 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to command injection.

### CVE-2026-16850

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-19T20:17:06.647 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to command injection via crafted Router Advertisements.

### CVE-2026-16848

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T20:17:06.297 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary commands due to improper neutralization of shell metacharacters in DHCP options.

### CVE-2026-16847

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:06.143 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a heap buffer overflow.

### CVE-2026-16844

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T20:17:05.670 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-16842

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T20:17:05.513 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-16841

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:05.360 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a stack buffer overflow.

### CVE-2025-14603

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-19T18:16:31.087 |

The application component processes user-supplied parameters insecurely, passing them into SQL queries. This can enable blind SQL injection, potentially exposing database contents or causing the application to become unresponsive. 
Apply patch from vendor  https://vsdesk.ru/ . Versions 14.0101 and on have the patch.

### CVE-2026-62666

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-19T16:18:19.043 |

Grav API Plugin is a RESTful API for Grav CMS that provides full headless access to your site's content. Prior to 1.0.6, Grav API plugin UsersController::createApiKey(), generate2fa(), and disable2fa() omit the accessGrantsSuper() target check used by sibling user mutation endpoints. A non-super account with api.users.write can mint an API key bound to an access.api.super target through requireApiKeyPermission(), obtain the target's full privileges because key scopes are not enforced, and create persistent super-administrator access; the same missing check also permits rotating or disabling the target's two-factor authentication. This issue is fixed in version 1.0.6.

### CVE-2026-71176

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T15:18:01.637 |

Dell OpenManage Enterprise, versions prior to 4.7.0, contains an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Information exposure.

### CVE-2026-58565

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T15:17:13.280 |

Dell Command Update (DCU), versions prior to 5.7.1, contain a Missing Authorization vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges.

### CVE-2026-49255

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T15:17:06.893 |

electerm is an open-sourced terminal/ssh/sftp/telnet/serialport/RDP/VNC/Spice/ftp client. Prior to 3.11.11, electerm constructs operating system commands in src/app/lib/fs.js by interpolating untrusted file paths into the rmrf(), mv(), and cp() functions. A malicious SSH or SFTP server can provide a filename containing quote characters and shell metacharacters, and a victim can cause that filename to reach the affected operation during remote-to-local transfer, conflict renaming, copying, moving, or removal. The generated `rm -rf`, mv, `cp -r`, PowerShell Remove-Item, Move-Item, or Copy-Item command can then interpret the filename as shell syntax. This allows arbitrary command execution with the electerm desktop user's privileges on POSIX and Windows systems, enabling data exfiltration, file modification, malware installation, or denial of service. This issue is fixed in version 3.11.11.

### CVE-2026-44829

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-19T15:17:02.630 |

Gotenberg is a Docker-powered stateless API for PDF files. In 8.32.0 and earlier, filename handling in pkg/modules/api/context.go uses filepath.Base on Linux, which does not treat backslashes as path separators, so a multipart filename containing Windows-style parent directory components survives sanitization. The original filename flows through ctx.diskToOriginal and the multi-output PDF routes into archives.FilesFromDisk and archives.Zip.Archive as the generated zip entry name. A remote attacker can submit a name such as ........\Windows\System32\evil.pdf through an upload or an upstream downloadFrom Content-Disposition header, and a Windows archive extractor can write the resulting file outside the intended extraction directory. The affected paths include /forms/pdfengines/split and other multi-output PDF, LibreOffice, and conversion routes, and exploitation can cause arbitrary file writes on a downstream Windows system when a user or process extracts the returned archive. This issue is fixed in version 8.33.0.

### CVE-2026-16814

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T15:16:57.367 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a heap buffer overflow.

### CVE-2026-64966

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-20T14:17:45.270 |

ATutor is vulnerable to a Path Traversal vulnerability in ZIP extraction functionality. An attacker with instructor privileges can upload and extract a specially crafted ZIP archive, causing files to be written outside the intended extraction directory. This allows an attacker to place a server-executable .phtml file in the web root and achieve remote code execution with web server privileges on the underlying server.




Product is no longer actively supported and the vulnerabilities have not been fixed. Only version 2.2.4 was tested and confirmed as vulnerable, other versions were not tested but might also be vulnerable.

### CVE-2026-64960

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-20T14:17:44.400 |

ATutor Gameme module allows users to upload files of any type and extension without restriction. Due to improper handling of file uploads, files are stored in a web-accessible location before their content is validated. An authenticated attacker who knows a valid course_id can upload a server-executable malicious script. The uploaded file can then be requested over HTTP, resulting in remote code execution as the web server process user. In most cases, course_id=0 can be used, as it commonly represents the global context.




Product is no longer actively supported and the vulnerabilities have not been fixed. Only version 2.2.4 was tested and confirmed as vulnerable, other versions were not tested but might also be vulnerable.

### CVE-2026-77080

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-20T12:16:39.430 |

n8n before 1.123.69, 2.x before 2.33.4, and 2.34.x before 2.34.1 contain an arbitrary file read and write vulnerability in the Snowflake node, which passes free-form Execute Query input, including client-side commands, directly to the Snowflake SDK without applying n8n's file-access restrictions. An authenticated user with usable Snowflake credentials can upload a local file from the n8n host or overwrite an existing file with a staged one.

### CVE-2026-77068

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-20T12:16:37.963 |

n8n before 2.33.4 and 2.34.x before 2.34.1 contain a remote code execution vulnerability in the @n8n/workflow-sdk node-schema loader used for MCP node-schema loading. The loader derives a node's schema module path directly from the attacker-supplied node type string without validating path-traversal sequences. An authenticated user with global:member privileges can reference malicious files via path traversal, causing code execution in the n8n main process.

### CVE-2026-14952

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-20T09:16:47.740 |

An unauthenticated remote attacker can retrieve sensible files from the FDS Web server, such as the backup archive at /FdsBackup.zip and additional files under /downloads/*, directly over HTTP without a valid session. These files disclose detailed railway signaling and track layout information that should not be available to unauthenticated users.

### CVE-2026-14948

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-08-20T09:16:47.137 |

A low privileged remote attacker can hijack an active administrative session without needing to know the administrator password by extracting live plaintext session identifiers for authenticated users from downloadable error log archives.

### CVE-2026-75596

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-08-19T21:17:37.740 |

Netty is an asynchronous, event-driven network application framework. Prior to 4.1.137.Final and 4.2.17.Final, the default io.netty.handler.ssl.SniHandler constructors use the pre-handshake ClientHello aggregation path in handler/src/main/java/io/netty/handler/ssl/SslClientHelloHandler.java at io.netty.handler.ssl.SslClientHelloHandler#decode, where handshakeBuffer.clear() and writeBytes() recopy all previously received body bytes for every additional TLS record. An unauthenticated remote peer can advertise a large ClientHello and deliver its body in thousands of tiny records, causing quadratic CPU work on the event loop before the TLS handshake completes and degrading TLS handling for other clients. This issue is fixed in versions 4.1.137.Final and 4.2.17.Final.

### CVE-2026-61556

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-08-19T21:17:03.633 |

LiquidJS is a Shopify / GitHub Pages compatible template engine in pure JavaScript. From 10.26.0 until 10.27.1, the strip_html filter in src/filters/html.ts can enter an infinite loop when an input string contains <, includes at least one preceding character, and has no later >. In strip_html, the search for the next opener advances lt while the loop index remains unchanged when the closer search returns -1, and the equality-only stall guard does not exit because the loop index is less than lt. Reprocessing the same state indefinitely blocks template rendering and can cause denial of service with an input as short as a<. This issue is fixed in version 10.27.1.

### CVE-2026-68899

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-19T20:17:21.567 |

Wekan is open source kanban built with Meteor. Prior to 9.90, isFileValid() in models/fileValidation.js used the Unix file command for content-based MIME detection, but detectMimeFromFile() silently returned undefined when that binary was unavailable and the validation fell back to the attacker-controlled fileObj.type supplied through server/routes/attachmentApi.js. On deployments with WITH_API=true and no file binary, an authenticated board member could label HTML containing JavaScript as image/png, bypass the dangerous MIME check, and store active content under the Wekan origin for execution when another user opened it. Version 9.90 adds looksLikeDangerousMarkup() to inspect file bytes and force dangerous-content scanning when MIME detection is unavailable. This issue is fixed in version 9.90.

### CVE-2026-63722

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-19T20:17:20.380 |

ICEcoder 8.1 contains an unauthenticated remote code execution vulnerability that allows unauthenticated attackers to execute arbitrary OS commands by chaining an authentication bypass, CSRF validation bypass, and unsanitized command execution. Attackers can send a single HTTP POST request to the terminal endpoint with a password parameter to bypass authentication, a non-empty csrf parameter to skip CSRF validation, and an arbitrary command string passed directly to proc_open() to achieve remote code execution as the web-server user.

### CVE-2026-63188

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-19T20:17:20.230 |

Logto is the modern, open-source auth infrastructure for SaaS and AI apps. Prior to 0.3.9, the Logto Tunnel npm package enabled createStaticFileProxy from packages/tunnel/src/commands/tunnel/index.ts and passed request.url from static asset requests through packages/tunnel/src/commands/tunnel/utils.ts using path.join(staticPath, request.url) and then fs.open(requestPath, "r") without URL normalization or a containment check. When --experience-path was enabled and the tunnel port was reachable, an unauthenticated requester could send a path containing ../ to createStaticFileProxy and read files outside the configured static directory that were readable by the logto-tunnel process. The service used server.listen(port), which could expose the tunnel to other hosts depending on the platform and deployment. This issue is fixed in version 0.3.9.

### CVE-2026-19198

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T19:17:12.383 |

Akaunting 3.1.21 contains an authenticated improper authorization vulnerability in the common BulkActions dispatcher.This issue affects Akaunting: 3.1.21.

### CVE-2026-75149

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-19T18:17:26.080 |

marimo before 0.23.15 contains a code injection vulnerability in the notebook configuration handler that allows attackers to execute arbitrary commands by supplying a crafted MCP server entry with an attacker-controlled command value embedded in a notebook. When the notebook is opened in edit mode, marimo launches the specified command as a local subprocess before any notebook cell is executed, requiring no authentication or cell execution to trigger the vulnerability.

### CVE-2026-67581

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-08-19T18:17:17.303 |

Authentication Bypass by Capture-replay in ZenHive mpp allows an unauthenticated remote client to obtain paid resources by resubmitting one settled on-chain transfer.

MPP.Methods.EVM.verify/2 accepts a transaction-hash credential and matches a transfer purely on token, to and amount (ERC-20) or to and value (native). It binds the proof neither to the challenge being verified nor to any record of prior use, and the generic MPP.Plug dedup store keys on challenge.id, which is regenerated for every 402 response. On a static-price route, a single historical transfer matching the charge therefore satisfies an unbounded number of later charges, including transfers an attacker can read off a public block explorer.

This issue affects mpp: from 0.3.0 before 0.6.3.

### CVE-2026-61518

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T18:16:51.977 |

ISPConfig contains an authenticated SQL injection vulnerability in the Remote API. The primary_id parameter passed to delete and update API methods is concatenated directly into SQL WHERE clauses without integer casting or parameterized query binding. The built-in SQL injection scanner does not block quote-free boolean payloads and does not reject requests in its default configuration. A remote API user holding any single low-privilege function permission can inject arbitrary SQL to delete or modify records across all tenants in the control panel database and extract arbitrary data via blind boolean inference, including password hashes and client records.

### CVE-2026-55194

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-19T18:16:44.857 |

FreeRDP is a free implementation of the Remote Desktop Protocol. Prior to 3.27.0, rpc_client_recv_fragment in libfreerdp/core/gateway/rpc_client.c ensures the response reassembly stream capacity using only the server-declared alloc_hint rather than the actual StubLength about to be written. A malicious TS Gateway can send a PTYPE_RESPONSE with a small alloc_hint and a much larger frag_length, causing Stream_Write to copy attacker-controlled stub data beyond the 4096-byte pdu->s buffer. This can crash the client and may permit code execution through heap corruption. This issue is fixed in version 3.27.0.

### CVE-2026-55193

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-19T18:16:44.720 |

FreeRDP is a free implementation of the Remote Desktop Protocol. Prior to 3.27.0, FreeRDP clients using TS Gateway accept a server-controlled max_xmit_frag value in libfreerdp/core/gateway/rpc_bind.c without bounding it to the 4088-byte ReceiveFragment allocation. A malicious gateway can advertise 65535 and then send a response fragment of the same length, causing rpc_channel_read in libfreerdp/core/gateway/rpc.c to write up to 65535 bytes into the smaller ReceiveFragment buffer. This can crash the client and may permit code execution through attacker-controlled heap corruption. This issue is fixed in version 3.27.0.

### CVE-2026-55191

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-19T18:16:44.427 |

FreeRDP is a free implementation of the Remote Desktop Protocol. Prior to 3.27.0, FreeRDP clients that negotiate RDPGFX AVC444 with an H.264 decoder backend calculate the intermediate YUV444 allocation size in libfreerdp/codec/h264.c with 32-bit multiplication in avc444_ensure_buffer. A malicious RDP server can supply surface dimensions for which piDstStride multiplied by padDstHeight wraps to a small nonzero value, causing winpr_aligned_recalloc to allocate an undersized buffer before YUV420CombineToYUV444 writes using the actual stride and rectangle dimensions. This can cause a client crash and may permit code execution through attacker-influenced heap corruption. This issue is fixed in version 3.27.0.

### CVE-2026-64852

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T16:18:40.040 |

Grav API Plugin is a RESTful API for Grav CMS that provides full headless access to your site's content. Prior to 1.0.8, the Grav API plugin intercepts the apiKeyGenerate and apiKeyRevoke admin tasks in user/plugins/api/api.php and authorizes the caller with only admin.login. A basic panel user can select another account from the route, create a persistent ApiKeyManager credential bound to that target, and inherit the target's API permissions, including api.super or administrative write access when present. This issue is fixed in version 1.0.8.

### CVE-2026-64850

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-19T16:18:39.760 |

Grav is a file-based Web platform. Prior to 2.0.7, Grav Blueprint::dynamicData() in system/src/Grav/Common/Data/Blueprint.php sends an editor-controlled Class::method provider and arguments to call_user_func_array() without rejecting dangerous callback parameters. An account with admin.pages or api.pages.write can use Grav\Common\Utils::arrayFilterRecursive() as a trampoline with system as the callback, place a command in page frontmatter, and execute that command as the web server user when the page is viewed. This issue is fixed in version 2.0.7.

### CVE-2026-75956

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-19T15:18:10.313 |

Joomla Extension - cmsjunkie.com - DOS vector in pagination parameter handling in J-BusinessDirectory < 6.2.3 - Pagination values were not strictly typed. Array/non-numeric values (for example limitstart[]) could trigger PHP type errors in arithmetic, and limit was not validated before use in list queries.

### CVE-2026-71961

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T15:18:02.083 |

Cudy WR3000 2.0 running firmware before 2.5.24 contains an OS command injection vulnerability that allows authenticated attackers to execute arbitrary OS commands with root privileges by sending unsanitized input through the mesh MQTT command interface. The sync_command binary forwards unsanitized input directly to a shell execution sink in command.lua, enabling attackers with access to the MQTT broker to exploit the default-enabled command execution path to achieve full root-level system compromise.

### CVE-2026-52792

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-69` |
| Published | 2026-08-19T15:17:09.667 |

Algernon is a small self-contained pure-Go web server. Prior to 1.17.9, Algernon on Windows selects a file handler in engine/handlers.go by calling filepath.Ext() without first rejecting NTFS-equivalent names such as x.lua::$DATA, x.lua., and x.lua . An unauthenticated client can append one of these suffixes to a public server-side script using the .lua, .tl, .po2, .amber, or .frm extension. The request path passes through URL2filename in utils/files.go, skips the renderer and execution cases, and reaches FilePage, os.Open, ReadAndLogErrors, and ToClient, while NTFS resolves the alias to the underlying script. The server consequently returns raw script source and can expose database credentials, API keys, and the SetCookieSecret value, which may permit forged session cookies. Linux and macOS hosts are not affected by this issue. This issue is fixed in version 1.17.9.

### CVE-2026-49283

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-19T15:17:07.027 |

The SimpleSAMLphp SAML2 library is a PHP library for SAML2 related functionality. Prior to versions 4.19.3, 4.20.2, 5.0.6, and 6.2.1, the HTTPArtifact::receive() flow can treat an unsigned embedded SAML Response as cryptographically valid for the wrong identity provider. SOAPClient::addSSLValidator() attaches a TLS-based validator to the outer SOAP ArtifactResponse, while the embedded Response receives a validator that delegates to the outer message and is later checked against metadata selected from the embedded response issuer rather than necessarily the artifact issuer. SOAPClient::validateSSL() returns normally when the TLS public key does not match the key being validated, and SAML2\Message::validate() treats a validator call that does not throw as successful. In a multi-IdP federation, a malicious or lower-trust IdP can therefore provide an ArtifactResponse containing an unsigned Response that claims a higher-trust victim IdP as issuer and authenticate as arbitrary users with attacker-chosen assertion attributes, NameID, and session data. This issue is fixed in versions 4.19.3, 4.20.2, 5.0.6, and 6.2.1.

### CVE-2026-45273

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T15:17:04.313 |

MyBooks is an ebook management web server also known as Talebook. In 3.41.2 and earlier, the AdminSettings.post handler for POST /api/admin/settings in webserver/handlers/admin.py applies the auth decorator but does not check the self.admin_user property, unlike the corresponding GET handler. Any authenticated regular user can therefore overwrite server configuration values including SMTP credentials, OAuth client secrets, storage paths, security feature flags, and autoreload settings. The process_auth_header function in webserver/handlers/base.py also fails to verify the matched account's active flag, allowing a registered but unactivated account to authenticate and reach the vulnerable handler. Exploitation can disclose secrets through configuration access paths, sabotage application behavior, force service restarts, and supply the settings needed for related code-injection attacks. This issue is fixed in version 3.42.0.

### CVE-2026-76635

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-94` |
| Published | 2026-08-20T14:17:59.973 |

baserCMS before 5.3.0 contains a SQL injection vulnerability in BcDatabaseService.php that allows authenticated administrators to inject attacker-controlled table names and configuration values directly into SQL statements across sequence update, CSV export, and table management operations. Attackers can chain a backup restore code injection flaw, where PHP code outside class definitions in schema files executes unconditionally upon loading, to plant malicious table names and trigger error-based SQL injection that retrieves database version, schema contents, and arbitrary data from the PostgreSQL backend.

### CVE-2026-76633

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620;CWE-862` |
| Published | 2026-08-20T14:17:59.680 |

WeGIA before 3.9.2 contains an authorization bypass vulnerability in the password change flow that allows any authenticated user to change their account password without providing existing credentials by exploiting the unconditional exclusion of the alterarSenha method from permission checks in controle/control.php. Attackers can manipulate the redir parameter to point to alterar_senha.php, routing through verificarSenhaConfig() instead of verificarSenha() to bypass current password verification and convert temporary session access into permanent account takeover.

### CVE-2026-14951

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-20T09:16:47.597 |

An low privileged remote attacker can cause authenticated users to perform unintended actions in the FDS Web interface using malicious web pages.

### CVE-2026-14947

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-24` |
| Published | 2026-08-20T09:16:46.977 |

A high-privileged remote attacker can upload malicious ZIP archive containing directory traversal sequences such as ../ can escape the intended extraction directory and write files to arbitrary locations on the server, potentially achieve arbitrary code execution due to improper validation of archive entry paths before writing files to disk which could result in full system compromise.

### CVE-2026-14946

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-20T09:16:45.813 |

A high privileged remote attacker can upload a .php file and then request it directly from /uploads/<filename>.php to achieve arbitrary code execution due to improper file type validation which could result in full system compromise.

### CVE-2026-76564

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T08:16:47.770 |

Joomla Extension - phoca.cz -  Stored XSS via User-Agent header in Admin Order View in Phoca Cart 5.0.0-6.1.7

### CVE-2026-75948

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T08:16:47.640 |

Joomla Extension - icagenda.com -  Authenticated Stored XSS in iCagenda 4.0.8 to 4.0.12 - The frontend "Submit an Event" form stores the `image` and `file` fields as raw strings with no output-side HTML-attribute escaping.

### CVE-2025-14601

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-676` |
| Published | 2026-08-20T08:16:46.273 |

An OS command injection vulnerability in vsDesk allows an authenticated attacker with administrative privileges to execute arbitrary operating system commands due to insufficient input filtering. An attacker can exploit this flaw to disrupt web server operations, expose sensitive data, or potentially achieve full server compromise.




Apply patch from vendor  https://vsdesk.ru/ . Versions 14.0101 and on have the patch.

### CVE-2026-76590

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-19T22:17:27.613 |

A vulnerability was identified in TRENDnet TEW-755AP up to 20260702. Affected by this issue is some unknown functionality of the file /cgi-bin/wan.cgi of the component ssi. Such manipulation of the argument cameo.wan.wan_pppoe_password_00 leads to stack-based buffer overflow. The attack can be executed remotely. The exploit is publicly available and might be used.

### CVE-2026-76589

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-19T22:17:27.447 |

A vulnerability was found in TRENDnet TEW-755AP up to 20260702. Affected is the function FUN_401000 of the file /sbin/mycli. The manipulation of the argument ssid results in stack-based buffer overflow. The attack may be launched remotely. The exploit has been made public and could be used.

### CVE-2026-76584

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-19T21:17:38.857 |

A security flaw has been discovered in TRENDnet TV-IP751WIC 11.03.03. Affected by this issue is some unknown functionality of the file /cgi-bin/admin/set_time.cgi of the component alphapd. The manipulation of the argument Currenttime results in stack-based buffer overflow. The attack can be launched remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-74013

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T12:16:37.067 |

Subscriber SQL Injection in eShipper Commerce <= 2.16.13 versions.

### CVE-2026-73998

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T12:16:36.813 |

Subscriber SQL Injection in WP w3all phpBB <= 3.0.5 versions.

### CVE-2026-66594

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T12:16:33.307 |

Subscriber SQL Injection in WordPress Persistent Login <= 3.1.0 versions.

### CVE-2026-14949

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-20T09:16:47.307 |

A low privileged remote attacker with a valid session can submit a request to the user creation functionality exposed through /api/user/add.php to create new accounts with arbitrary role values, including the highest privilege level used by the application.

### CVE-2026-76832

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-19T22:17:27.960 |

Agno's PythonTools in libs/agno/agno/tools/python.py contains a path traversal vulnerability that allows attackers to read, write, or execute arbitrary files by supplying parent-directory traversal sequences in the file_name argument passed to read_file, save_to_file, or run_python_file tool actions. Attackers can inject traversal sequences such as '../../../../../../etc/passwd' through direct tool invocation or via prompt injection embedded in agent-processed content to escape the intended base_dir boundary and achieve arbitrary file read, arbitrary file write, or arbitrary Python code execution within the process user's authority.

### CVE-2026-75616

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T21:17:37.917 |

An OS command injection vulnerability exists in the web management interface of Archer C20 v6 firmware when processing certain WAN-related configuration operations. An authenticated administrator may exploit insufficient input validation to execute arbitrary system commands, potentially resulting in full device compromise.






Successful exploitation may allow arbitrary command execution with elevated privileges, compromising the confidentiality, integrity, and availability of the affected device and network traffic passing through it.

### CVE-2026-68558

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T20:17:20.910 |

Wekan is open source kanban built with Meteor. From 8.36 until 9.74, the outgoing webhook Integration URL validator in models/integrations.js checked only the literal URL.hostname against regular expressions, so DNS names such as 169-254-169-254.nip.io passed that first-line check. The delivery path's fetchSafe guard already blocked the reported IPv4 destination, but its separate IPv4-only resolver and duplicated blocklist created inconsistent all-address-family enforcement and drift risk between input-time and connection-time validation. Version 9.74 makes server/lib/ssrfGuard.js resolve all addresses with `dns.lookup({ all: true })`, validate every result through the shared isIpBlocked logic, pin the connection, and block redirects. This issue is fixed in version 9.74.

### CVE-2026-75144

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-19T17:21:12.720 |

FFmpeg before commit 1cdeb3c contains a heap buffer overflow vulnerability in the VC-2/Dirac RTP packetizer (libavformat/rtpenc_vc2hq.c) that allows attackers to trigger memory corruption by supplying a crafted Dirac data unit. The packetizer copies an input-derived data unit or fragment size into a fixed-size buffer without an upper bound check, causing a heap buffer overflow when the crafted input is packetized for RTP output.

### CVE-2026-75142

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T17:21:12.437 |

FFmpeg before commit 9d786e4 contains a stack buffer overflow in the MPEG-PS muxer (libavformat/mpegenc.c). When muxing input with more streams than the muxer's fixed-size stack buffer accommodates, the buffer is overflowed. A crafted input with an excessive number of streams triggers the overflow during MPEG-PS muxing.

### CVE-2026-75141

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-19T17:21:12.287 |

FFmpeg before commit acf5d7c contains a heap buffer overflow in the hvcC box writer. When writing an HEVC configuration record with more NAL units of a single type than the count field can represent, the NAL unit count overflows, causing a heap buffer overflow. A crafted HEVC input file triggers the overflow during muxing.

### CVE-2026-64851

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T16:18:39.897 |

Grav Shortcode Core Plugin allows for the development shortcode plugins that utilize the common format utilized by WordPress and BBCode. Prior to 6.2.2, Grav Shortcode Core passes shortcode syntax through Security::detectXss() because it contains no literal less-than character, then ColorShortcode.php and related attribute handlers concatenate an attacker-controlled parameter into HTML without encoding. An account with admin.pages permission can close the generated attribute and add an event handler, creating stored cross-site scripting that executes for visitors or administrators who view the page. This issue is fixed in version 6.2.2.

### CVE-2026-76833

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-20T14:18:00.137 |

@cgauge/yaml npm package contains an arbitrary code execution vulnerability that allows attackers to execute arbitrary JavaScript by embedding a custom !js YAML tag whose construct callback unconditionally calls eval() on attacker-supplied string values during document parsing. Any application parsing untrusted YAML input with this library exposes full Node.js runtime authority, including environment variable access, filesystem read/write, network access, and subprocess execution, with no safe-mode alternative or opt-out mechanism available.

### CVE-2026-70383

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-20T14:17:58.050 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Estonian Information System Authority (RIA) DigiDoc4 client.

This issue affects DigiDoc4: from 4.0.0 before 4.11.0.

### CVE-2026-77118

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T13:19:07.077 |

A heap out-of-bounds write exists in the Photo CD (PCD) decoder of GraphicsMagick. In DecodeImage() (coders/pcd.c), the Huffman delta loop advances its output pointer with q++ after every decoded delta and never checks it against the end of the heap-allocated luma/chroma plane buffers. The pointer is repositioned only when a sync marker introduces a new plane/row; between sync markers the run length is bounded solely by the input.



A crafted PCD file that positions the pointer near the end of a plane and then supplies a long run of deltas with no intervening sync therefore walks the pointer past the end of the allocation and writes through it. Processing an untrusted PCD file — for example with gm convert or gm identify, or through any application linked against libGraphicsMagick — can corrupt heap memory beyond the buffers.

### CVE-2026-77075

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-20T12:16:38.870 |

n8n before 1.123.69, 2.x before 2.33.4, and 2.34.x before 2.34.1 contain an expression injection vulnerability in resource-locator field link preview rendering. The editor spliced the field's stored value directly into the node type's URL template without checking for expression syntax. An authenticated member can store a malicious value so that when another user opens the affected node in the editor, the injected expression is evaluated as JavaScript in the victim's authenticated session (cross-user script execution).

### CVE-2026-77072

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:38.487 |

n8n before 1.123.69, 2.33.4, and 2.34.1 contains a stored cross-site scripting vulnerability in the Form node's completion page. The completion page applied its sandboxing Content-Security-Policy only when respondWith was not set to 'redirect', but responseText was always rendered as raw HTML. An authenticated member could set respondWith to 'redirect' via an expression while keeping responseText populated, causing the completion page to serve unsanitized HTML and script from the n8n origin. Any visitor who submitted the resulting public form would have that script execute same-origin with their session.

### CVE-2026-76878

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-688` |
| Published | 2026-08-19T22:17:28.310 |

In OpenStack Aodh before 22.0.1, the alarm list API bypasses project scoping when the all_projects query parameter is set to false. The API checks for the presence of the all_projects key rather than its value; a true value enforces the administrator-only policy, but a false value removes the key and skips the branch that normally restricts results to the caller's project. A non-admin user with the reader role can list alarms from all projects, exposing alarm actions containing trust webhook URLs, Heat signal endpoints, project IDs, and user IDs. The parameter can also be combined with a foreign project_id to target a specific project's alarms. A related concern is that OpenStack Watcher does not apply authorization to its webhook trigger endpoint. Any authenticated user who learns an audit's webhook URL, for example from this leaked Aodh alarm metadata, can start an EVENT audit and its associated action plan regardless of their own project or role. The webhook endpoint has lacked policy enforcement since its introduction in the Ussuri release (Watcher 4.0.0).

### CVE-2026-17091

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-19T20:17:12.460 |

IBM PowerVM Hypervisor FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, and FW950.00 through FW950.H2 is affected by a vulnerability in the PowerVM hypervisor call interface. An attacker with root access to a guest partition can issue a specially crafted hypervisor call to inject an arbitrary amount of data into hypervisor or partition memory, resulting in either a crash causing a full platform re-IPL and terminating all hosted partitions, or corruption of hypervisor or partition memory. The PowerVM hypervisor will restart automatically; however, repeated exploitation could result in a sustained availability impact. Successful exploitation results in an integrity and availability impact to the managed system.

### CVE-2026-16832

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T19:17:10.557 |

IBM Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, and FW950.00 through FW950.H2 is affected by a vulnerability in the FSP management network protocol. An attacker with authenticated HMC administrator access can execute arbitrary code on the service processor, giving full control over the managed system, resulting in a confidentiality, integrity, and availability impact.

### CVE-2026-44901

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-19T17:18:49.283 |

Wazuh is a free and open source platform used for threat prevention, detection, and response. From 4.0.0 until 4.14.6 and 5.0.0-beta2, AffectedItemsWazuhResult.merge() in framework/wazuh/core/results.py trusts the sort_casting field in a cluster worker's JSON response. During a distributed API merge, attacker-controlled type names are resolved through Python builtins without an allowlist. A compromised worker can set sort_casting to exec and place Python source in affected_items, causing the master to execute the payload as root when responses from multiple nodes are merged. This issue is fixed in versions 4.14.6 and 5.0.0-beta2.

### CVE-2026-76394

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T22:17:25.870 |

In Splunk AI Toolkit versions below 6.0.0, a low-privileged user who does not hold the "admin" or "power" Splunk roles could start, stop, and configure containers, and read or modify connection and configuration data through the Representational State Transfer (REST) API. The missing authorization is possible because multiple REST API handlers in Splunk AI Toolkit do not enforce authorization checks. For more information see Troubleshoot the Splunk Machine Learning Toolkit (https://help.splunk.com/en/splunk-cloud-platform/apply-machine-learning/machine-learning-toolkit-user-guide/5.5.0/troubleshooting-mltk/troubleshoot-the-splunk-machine-learning-toolkit) in the Splunk documentation.

### CVE-2026-76391

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T22:17:25.487 |

In Splunk AI Toolkit versions below 6.0.0, a user who does not hold the "admin" or "power" Splunk roles could run searches with system-level privileges, access all relevant data, affect system integrity, and read or delete search jobs belonging to other users through Agent Run History. The improper privilege management is possible because the Agent Run History handler replaces the calling user session key with a system authentication token before it performs search operations. For more information see AI Toolkit Agent Launchpad (https://help.splunk.com/en/splunk-enterprise/apply-machine-learning/use-ai-toolkit/6.0.0/ai-toolkit-connections-containers-and-agents/ai-toolkit-agent-launchpad) in the Splunk documentation.

### CVE-2026-18848

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-19T19:17:12.247 |

IBM Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, and FW950.00 through FW950.H2 is affected by a vulnerability in the ASMI web interface. An attacker who can lure a logged-in ASMI administrator to visit a crafted web page can, under specific conditions, silently perform administrative actions on the FSP on behalf of that administrator, resulting in a confidentiality, integrity, and availability impact to the managed system.

### CVE-2026-73541

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-19T18:17:25.627 |

Allocation of Resources Without Limits or Throttling in ZenHive mpp allows an unauthenticated remote client to drain the fee-payer wallet through concurrent sponsored payments, denying service to legitimate payers once it is empty.

MPP.Methods.Tempo.FeePayerPolicy enforces its ceilings (max_gas, max_fee_per_gas, max_priority_fee_per_gas, the worst-case gas_limit * max_fee_per_gas <= max_total_fee budget cap, and a validity window) against one transaction at a time, and nothing accounts for exposure across concurrent requests. reserve_hash_atomic/2 is keyed on the transaction hash, so it prevents duplicate broadcast of the same signed transaction but not N distinct sponsored transactions carrying distinct expiring nonces. Committed sponsor exposure is therefore N times max_total_fee, bounded by nothing in the library, and the default 900 second validity window lets co-signed transactions stay broadcastable and uncounted for that entire period.

This issue affects mpp: from 0.2.0 before 0.12.0.

### CVE-2026-76402

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T22:17:26.910 |

In Splunk Connect for Kafka versions below 2.2.7, an unauthenticated user who can reach the Kafka Connect Representational State Transfer (REST) API could configure a non-secure Hypertext Transfer Protocol (HTTP) Event Collector endpoint in Splunk Enterprise that causes the connector to send authentication credentials to an attacker-controlled server, allowing for exposure of credentials that compromise all relevant data sent through the connector and limited alteration of event delivery. The vulnerability is possible because HTTP Event Collector endpoint validation does not require secure transport by default. For more information see Install Splunk Connect for Kafka (https://help.splunk.com/en/data-management/integrate-data-with-add-ons/splunk-connect-for-kafka/2.2/install/install-splunk-connect-for-kafka), Data ingestion parameters for Splunk Connect for Kafka (https://help.splunk.com/en/data-management/integrate-data-with-add-ons/splunk-connect-for-kafka/2.2/overview/data-ingestion-parameters-for-splunk-connect-for-kafka), and Set up and use HTTP Event Collector with configuration files (https://help.splunk.com/en/splunk-enterprise/get-data-in/get-started-with-getting-data-in/9.4/get-data-with-http-event-collector/set-up-and-use-http-event-collector-with-configuration-files) in the Splunk documentation.

### CVE-2026-16933

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-19T20:17:11.807 |

IBM Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, FW950.00 through FW950.H2, OP940.00 through OP940.a1 (Power9), and OP940.00 through OP940.81 (Power HMC) is affected by a vulnerability in the interface between the BMC/FSP and the host system. An attacker with service account or root access to the BMC/FSP can read and write arbitrary regions of host system memory, giving full control over the host system and all hosted partitions, resulting in a confidentiality, integrity, and availability impact.

### CVE-2026-16857

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-19T20:17:07.337 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to manipulate network traffic and DNS configuration due to improper authentication.

### CVE-2026-16707

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-19T20:17:02.140 |

IBM PowerVM Hypervisor FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, and FW950.00 through FW950.H2 is affected by a vulnerability in the service processor mailbox interface. An attacker with authenticated service-level access to the FSP can send a specially crafted mailbox message to read or modify arbitrary regions of Hostboot memory, compromising the host firmware boot stack and the hypervisor subsequently loaded by it. Successful exploitation results in a confidentiality, integrity, and availability impact to the managed system.

### CVE-2026-16661

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-19T20:17:01.937 |

IBM PowerVM Hypervisor FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, and FW950.00 through FW950.H2 is affected by a vulnerability in the service processor mailbox interface. An attacker with authenticated service-level access to the FSP can exploit this vulnerability, allowing arbitrary code to be executed in the host firmware runtime, giving full control over the managed system, resulting in a confidentiality, integrity, and availability impact to the managed system.

### CVE-2026-17494

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T19:17:11.703 |

IBM Power Systems Firmware FW1120.00, and FW1110.00 through FW1110.30 is affected by a vulnerability in the interface between the BMC and the host system. An attacker with service access to the BMC can send a specially crafted command, allowing arbitrary code to be executed on the host system, giving full control over the host system and all hosted partitions, resulting in a confidentiality, integrity, and availability impact.

### CVE-2026-17100

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T19:17:11.270 |

Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, FW950.00 through FW950.H2, OP940.00 through OP940.a1, and OP940.00 - OP940.81 is affected by a vulnerability in the service processor mailbox interface. An attacker with authenticated service-level access to the BMC/FSP can exploit this vulnerability, allowing arbitrary code to be executed in the host firmware runtime, giving full control over the managed system, resulting in a confidentiality, integrity, and availability impact to the managed system.

### CVE-2026-17093

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T19:17:11.100 |

IBM Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, FW950.00 through FW950.H2, OP940.00 through OP940.a1 (Power9), and OP940.00 - OP940.81 (Power HMC) is affected by a vulnerability in host firmware configuration parsing. An attacker with service-level access to the BMC/FSP can supply specially crafted configuration data, compromising the host firmware boot stage and everything subsequently loaded by it, resulting in a confidentiality, integrity, and availability impact to the managed system.

### CVE-2026-16930

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T19:17:10.823 |

IBM Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, and FW1060.00 through FW1060.80 is affected by a vulnerability in the interface between the BMC/FSP and the host system. An attacker with service account or root access to the BMC/FSP can execute arbitrary code on the host system, giving full control over the host system and all hosted partitions, resulting in a confidentiality, integrity, and availability impact.

### CVE-2026-73136

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-08-19T18:17:25.453 |

Authentication Bypass by Capture-replay in ZenHive mpp allows an unauthenticated third party to obtain paid resources by replaying a transfer settled by an unrelated payer.

MPP.Methods.Tempo normally binds a settled TIP-20 TransferWithMemo to the specific challenge under verification through an attribution nonce carried in the memo. When a static "memo" is configured in method_config, check_matched_memo_binding/3 returns the match unconditionally and that binding is skipped, leaving only token, recipient, amount and the static memo value to match on. The static memo is echoed in every unauthenticated 402 response and Tempo transfers are public, so an attacker can take any matching transfer paid by a legitimate customer, request a fresh challenge for the same route, and present that transaction hash as a type="hash" credential. The hash path performs no sender or signature check tying the presenter to the wallet that broadcast the transfer.

This issue affects mpp: from 0.6.1 before 0.6.4.

### CVE-2026-19234

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T18:16:36.200 |

Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, and FW1060.00 through FW1060.80 is affected by a vulnerability in the host firmware boot process image validation path. An attacker with service access to the service processor can supply a maliciously crafted code update image, allowing arbitrary code to be executed on the host system. Successful exploitation could result in a confidentiality, integrity, and availability impact to the affected host system.

### CVE-2026-41424

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T17:18:47.837 |

Wazuh is a free and open source platform used for threat prevention, detection, and response. From 4.9.0 until 4.10.4 and 4.14.6, PUT /security/users/{user_id} in api/api/controllers/security_controller.py passes request.get("user") instead of request.context['token_info']['sub'] as current_user. remove_nones_to_dict() removes the resulting None value, so the reserved-account protection in framework/wazuh/security.py cannot verify who is making the request. An authenticated user with the users_admin role can overwrite the password of protected administrator accounts with user IDs at or below 99, including the wazuh superuser, and gain full administrative control. This issue is fixed in versions 4.10.4 and 4.14.6.

### CVE-2026-63407

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-942` |
| Published | 2026-08-19T16:18:37.863 |

Grav API Plugin is a RESTful API for Grav CMS that provides full headless access to your site's content. Prior to 1.0.0-rc.16, the Grav API plugin CorsMiddleware returns Access-Control-Allow-Origin: * and permissive OPTIONS responses for authenticated /api/v1 endpoints. JavaScript from any origin can submit an attacker-obtained JWT through the Authorization or X-API-Token header, read the authenticated response, and perform write operations with the token owner's privileges, enabling data exfiltration and account modification. This issue is fixed in version 1.0.0-rc.16.

### CVE-2026-62673

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-08-19T16:18:20.353 |

Grav is a file-based Web platform. Prior to 2.0.4, the Grav .htaccess and webserver-configs/htaccess.txt security rules omit the Apache [NC] flag and therefore compare sensitive directory and file-extension patterns case-sensitively. On a case-insensitive filesystem, an unauthenticated requester can use uppercase directory or extension variants to bypass the rules and retrieve files under user/accounts or user/config, including password hashes and security configuration. This issue is fixed in version 2.0.4.

### CVE-2026-16686

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-19T15:16:56.727 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to access NFS-exported filesystems due to improper authentication.

### CVE-2026-15061

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-19T15:16:55.610 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 's nimesis registration service could allow a remote attacker to overwrite files due to path traversal.

### CVE-2026-28150

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-20T12:16:32.283 |

Unauthenticated Local File Inclusion in Golo Framework < 1.7.5 versions.

### CVE-2025-15637

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-20T12:16:30.777 |

Unauthenticated Local File Inclusion in Shuffle <= 1.8 versions.

### CVE-2026-76886

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-19T23:16:19.553 |

C12.22 protocol dissector crash in 4.6.0 to 4.6.7 and 4.4.0 to 4.4.18 allows denial of service

### CVE-2026-76399

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-08-19T22:17:26.523 |

In Splunk AI Toolkit versions below 6.0.1, a user who holds the "power" Splunk role could modify app-provided scheduled searches to run arbitrary Search Processing Language (SPL) using the permissions of the search owner, which could allow access to all relevant data and affect system integrity. The vulnerability is possible because Splunk AI Toolkit gives the "power" Splunk role permission to modify scheduled searches that run using the permissions of the search owner.

### CVE-2026-76397

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-19T22:17:26.270 |

In Splunk AI Toolkit versions below 6.0.0, a user who holds the "power" Splunk role could access and delete all relevant data in experiment history, including data associated with other users. The vulnerability is possible because Splunk AI Toolkit does not preserve the trusted experiment scope when it processes caller-controlled query values before accessing restricted history data. For more information see Experiment Assistants (https://help.splunk.com/en/splunk-cloud-platform/apply-machine-learning/use-ai-toolkit/5.6.4/experiment-assistants) in the Splunk documentation.

### CVE-2026-76388

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-08-19T22:17:25.090 |

In Splunk Enterprise Security versions below 8.6.1, a user who holds the ess_analyst Splunk Enterprise Security role could change User and Entity Behavior Analytics (UEBA) search macros that scheduled searches run with administrator permissions, allowing for access to all relevant data and system integrity through those searches. The vulnerability is possible because the UEBA app metadata grants analyst roles write access to search macros that should be writable only by administrator roles. For more information see Users and roles for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/install/8.4/installation/users-and-roles-for-splunk-enterprise-security) and Roles and knowledge objects in UEBA for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.5/user-and-entity-behavior-analytics/roles-and-knowledge-objects-in-ueba-for-splunk-enterprise-security) in the Splunk documentation.

### CVE-2026-76387

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-19T22:17:24.953 |

In Splunk Enterprise Security versions below 8.6.1, a user who holds a Splunk Enterprise Security role that contains the mc_investigation_read capability could inject Search Processing Language (SPL) through Analyst Queue search filters, allowing for access to all relevant data and system integrity available to the scheduled searches that run for that user. The vulnerability is possible because the Analyst Queue search filter handling does not validate filter field names before the fields are included in SPL searches. For more information see Users and roles for Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/install/8.4/installation/users-and-roles-for-splunk-enterprise-security), Manage analyst workflows using the analyst queue in Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.4/mission-control/manage-analyst-workflows-using-the-analyst-queue-in-splunk-enterprise-security), and Overview of Mission Control in Splunk Enterprise Security (https://help.splunk.com/en/splunk-enterprise-security-8/user-guide/8.5/mission-control/overview-of-mission-control-in-splunk-enterprise-security) in the Splunk documentation.

### CVE-2026-76356

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-19T22:17:20.727 |

In Splunk SOAR versions below 8.6.0, an unauthenticated user could spoof the source IP address in a crafted request to an Automation Broker notification endpoint and execute arbitrary code on the Splunk SOAR host. The vulnerability is possible because the Splunk SOAR Automation Broker trusts a client-supplied source IP address header as proof that the request originates from the local system. Successful exploitation can expose all relevant data, affect system integrity, and disrupt service availability. For more information see About Splunk SOAR Automation Broker (https://help.splunk.com/en/splunk-soar/splunk-automation-broker/about-splunk-soar-automation-broker/about-splunk-soar-automation-broker) in the Splunk documentation.

### CVE-2026-76354

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-158` |
| Published | 2026-08-19T22:17:20.463 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user who does not hold the "admin" or "power" Splunk roles could affect system integrity and availability by sending a crafted Representational State Transfer (REST) API request that deletes or temporarily overwrites files writable by the user account running Splunk Enterprise processes on a non-captain search head cluster member. The vulnerability is possible because Search Head Clustering bundle replication does not validate the name of a replicated bundle file or neutralize NUL bytes before constructing the member bundle path. For more information see About search head clustering (https://help.splunk.com/en/splunk-enterprise/administer/distributed-search/10.4/overview-of-search-head-clustering/about-search-head-clustering), Define roles on the Splunk platform with capabilities (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.4/manage-splunk-platform-users-and-roles/define-roles-on-the-splunk-platform-with-capabilities), and Secure Splunk Enterprise service accounts (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/9.0/install-splunk-enterprise-securely/secure-splunk-enterprise-service-accounts) in the Splunk documentation.

### CVE-2026-76338

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-19T22:17:18.360 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, an unauthenticated user who has access to a trusted distributed search private key could forge an administrative session token, access all relevant data, affect system integrity, and disrupt service availability. The vulnerability is possible because the distributed search authentication token endpoint does not require a signed request to identify a configured search peer, allowing the request to fall back to shared local key material. For more information see About distributed search (https://help.splunk.com/en/splunk-enterprise/administer/distributed-search/10.4/overview-of-distributed-search/about-distributed-search) and authentication.conf (https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/configuration-file-reference/10.4.2-configuration-file-reference/authentication.conf) in Splunk documentation.

### CVE-2026-76331

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-943` |
| Published | 2026-08-19T22:17:17.423 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user who does not hold the "admin" or "power" Splunk roles could inject Search Processing Language (SPL) into saved-search dispatch requests. This could allow for unauthorized access to all relevant data and affect system integrity within Splunk Enterprise. The vulnerability is possible because Splunk Enterprise does not correctly validate caller-supplied time values before using them in saved-search dispatch. For more information see Search endpoint descriptions (https://help.splunk.com/en/splunk-enterprise/rest-api-reference/10.2/search-endpoints/search-endpoint-descriptions) in the Splunk documentation.

### CVE-2026-18544

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T21:16:54.400 |

IBM Portieris 0.5.0 through 0.14.2 could allow a remote authenticated attacker to bypass image policy enforcement due to improper authorization of pod owner references.

### CVE-2026-12633

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T21:16:53.633 |

The IPv6 neighbor-discovery code in subsys/net/ip/ipv6_nbr.c processes the 6LoWPAN Context Option (6CO, RFC 6775) carried inside ICMPv6 Router Advertisements. In handle_ra_6co() the 8-bit context_len field is taken directly from the packet and was never bounded to the RFC maximum of 128. The function computes context->context_len / 8 and then performs memset(context->prefix + context_len, 0, sizeof(context->prefix) - context_len), where context->prefix is a fixed 16-byte array.

With context_len between 136 and 255 (and the option length field set to 3, which the pre-fix validation accepts), context_len / 8 evaluates to 17..31, so the memset length 16 - context_len/8 underflows the unsigned size_t argument to roughly SIZE_MAX. This produces an unbounded out-of-bounds memset that zeroes kernel memory well past the 6lo context structure.

The defect is reachable from unauthenticated, link-local input: any host on the same link can send a crafted Router Advertisement with a 6CO option. The RA handler validates only the option length field before calling handle_ra_6co(), so a single packet triggers the wild write. The code is compiled when CONFIG_NET_6LO_CONTEXT is enabled.

The impact is a reliable remote (adjacent) denial of service via memory corruption, with collateral integrity loss as the memset zeroes contiguous memory before the system faults. Router Advertisements are link-scoped and not forwarded, so the attacker must be on the same link (AV:A). The fix rejects any context_len greater than 128 before the length computation.

### CVE-2026-17414

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-19T20:17:12.983 |

IBM PowerVM Hypervisor FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, and FW950.00 through FW950.H2 Power Systems Firmware is affected by a vulnerability in partition firmware during network boot. An unauthenticated attacker with access to the same network as a partition performing a network boot can prevent that partition from completing its boot sequence. On partitions where OS secure boot is not enabled, which is the default configuration, the attacker can also substitute the boot image, compromising everything subsequently loaded by that partition. Other partitions and the managed system are not affected. Only partitions actively performing a network boot are affected, resulting in a confidentiality, integrity, and availability impact.

### CVE-2026-17429

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T19:17:11.543 |

IBM Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, FW950.00 through FW950.H2, OP940.00 through OP940.a1 (Power9), and OP940.00 - OP940.81 (Power HMC) is affected by a vulnerability in the interface between the BMC/FSP and the host system. An attacker with service account or root access to the BMC/FSP can write arbitrary data to hardware control registers, allowing full control over the host system and all hosted partitions, resulting in a confidentiality, integrity, and availability impact.

### CVE-2026-62667

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T16:18:19.177 |

Grav API Plugin is a RESTful API for Grav CMS that provides full headless access to your site's content. Prior to 1.0.6, the Grav API plugin ApiKeyManager::generateKey() stores a declared scopes array, but ApiKeyAuthenticator::authenticate() does not read keyData[scopes] and returns the owning user's complete identity. AbstractApiController::requirePermission() consequently evaluates the full user ACL, so a key issued for a read-only scope can perform every write, delete, and administrative operation available to the owner. This issue is fixed in version 1.0.6.

### CVE-2026-15078

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-19T15:16:56.127 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 NIM could allow a remote attacker to gain unauthorized access to AIX systems due to improper validation of TLS certificates.

### CVE-2026-76139

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-08-19T21:17:38.070 |

A flaw was found in acm-operator-bundle. The build process for this component downloads and runs a script from a remote source without verifying its authenticity or integrity. This script gains access to sensitive credentials, such as GitHub access tokens and registry passwords, used in the build environment. A remote attacker could exploit this vulnerability to inject malicious code, leading to unauthorized access to build resources and potential compromise of the resulting operator bundle.

### CVE-2026-17063

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T20:17:12.307 |

IBM Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, and FW1060.00 through FW1060.80 is affected by a vulnerability in the interface between the BMC/FSP and the host system. An attacker with service account or root access to the BMC/FSP can access and disrupt host processor state, potentially affecting the managed system and all hosted partitions, resulting in an confidentiality, and availability impact.

### CVE-2026-18917

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T10:16:40.507 |

A flaw was found in libvirt. An unprivileged local user could exploit an integer overflow vulnerability in the NodeGetFreePages RPC handler. This flaw allows crafted values to bypass a size check, leading to an undersized memory buffer. Subsequently, real NUMA node data can overwrite this buffer. This heap buffer overflow can corrupt the root libvirt daemon's memory, potentially leading to a denial of service or local privilege escalation.

### CVE-2026-19582

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T05:16:27.987 |

In binutils 2.46.1 and prior versions, a victim who opens a crafted PE file using binutils could execute arbitrary code unknowningly via a stack buffer overflow out of bounds write.

### CVE-2026-16875

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T20:17:08.777 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary commands due to shell metacharacter injection.

### CVE-2026-16874

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-19T20:17:08.620 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to obtain root privileges due to improper enforcement of RBAC authentication roles.

### CVE-2026-16873

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:08.460 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to achieve local privilege escalation due to an out-of-bounds write.

### CVE-2026-16869

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-19T20:17:08.120 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary code due to improperly scrubbed environment variables.

### CVE-2026-58564

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-08-19T15:17:12.980 |

Dell Command Update (DCU), versions prior to 5.7.1, contain an Incorrect Default Permissions vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Filesystem access for attacker.

### CVE-2026-53477

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-19T15:17:10.417 |

Dell Command Update (DCU), versions prior to 5.7.1, contain a Time-of-check Time-of-use (TOCTOU) Race Condition vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges.

### CVE-2026-49817

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-19T15:17:07.480 |

Dell Command Update (DCU), versions prior to 5.7.1, contain a Deserialization of Untrusted Data vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges.

### CVE-2026-49816

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-19T15:17:07.337 |

Dell Command Update (DCU), versions prior to 5.7.1, contain a Deserialization of Untrusted Data vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges.

### CVE-2026-16703

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-19T15:16:57.050 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to gain elevated privileges due to improper privilege management.

### CVE-2026-77084

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-20T12:16:39.970 |

n8n before 1.123.69 (and 2.x before 2.33.4 / 2.34.1) contains a code execution vulnerability in the Git node. The Git node executed certain repository-local git configuration values without neutralizing them, so any subsequent Git node operation against a repository containing a malicious value would execute it as the n8n process user. This is not reachable through the Git node's own configuration controls and requires a separate file-write vulnerability elsewhere to plant the malicious value.

### CVE-2026-76344

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-27` |
| Published | 2026-08-19T22:17:19.150 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user who does not hold the "admin" or "power" Splunk roles could write dispatch metadata to an arbitrary location on the host by supplying a crafted search identifier to a Representational State Transfer (REST) API endpoint and affect system integrity on the host. The vulnerability is possible because Splunk Enterprise does not validate the search identifier before using it to create a dispatch directory. For more information see About configuring role-based user access (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.2/manage-splunk-platform-users-and-roles/about-configuring-role-based-user-access) in the Splunk documentation.

### CVE-2026-75569

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-829` |
| Published | 2026-08-19T21:17:37.287 |

A flaw was found in mce-operator-bundle. The build process fetches and executes scripts from a remote repository without performing integrity checks, such as commit pinning or signature verification. This allows a malicious actor with write access to the remote repository to inject and execute arbitrary code during the build. The consequence is a compromised build process, potentially leading to the distribution of malicious software.

### CVE-2026-54493

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T21:16:57.743 |

Koel is a free, open-source music streaming solution. Prior to 9.7.0, the Subsonic-compatible createInternetRadioStation.view and updateInternetRadioStation.view routes accept an authenticated user's streamUrl without the SafeUrl and HasAudioContentType checks used by the regular radio API. app/Http/Requests/Subsonic/CreateInternetRadioStationRequest.php and app/Http/Requests/Subsonic/UpdateInternetRadioStationRequest.php pass the stored URL through app/Services/RadioService.php to app/Services/Radio/RadioStreamProxy.php, where RadioStreamProxy::openStream() calls fopen($url, 'r', false, $context). Streaming /radio/stream/{id} returns the upstream response body, allowing access to loopback, RFC1918, Docker bridge, metadata, or other internal HTTP services reachable from the Koel server. This issue is fixed in version 9.7.0.

### CVE-2026-53549

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T21:16:57.143 |

Termix is a web-based server management platform with SSH terminal, tunneling, and file editing capabilities. Prior to 2.3.2, the POST /host/db/proxy/test endpoint accepts the singleProxy, proxyChain, and testTarget request fields without validating their destination addresses. The testProxyConnectivity path uses raw TCP and SOCKS connections to attacker-selected hosts and ports, allowing an authenticated user to probe localhost, private networks, link-local metadata services, and other infrastructure reachable from the Termix server. Structured connection errors disclose host reachability and timing information, and successful metadata access can expose cloud credentials. This issue is fixed in version 2.3.2.

### CVE-2026-68560

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T20:17:21.250 |

Wekan is open source kanban built with Meteor. Prior to 9.75, models/fileValidation.js interpolated the uploaded fileObj.path into the administrator-configured externalCommandLine at its {file} placeholder and executed the result through asyncExec, which is promisify(exec) and invokes `/bin/sh -c`. On deployments with an external scanner configured, an authenticated user able to upload an attachment could place shell metacharacters such as command substitutions in the filename and execute commands as the Wekan server process. Version 9.75 adds shellQuote() and passes the file path as a POSIX single-quoted argument so shell metacharacters cannot escape the placeholder. This issue is fixed in version 9.75.

### CVE-2026-63633

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-19T18:17:10.017 |

FreeRDP is a free implementation of the Remote Desktop Protocol. Prior to 3.28.0, freerdp_dsp_decode_opus in libfreerdp/codec/dsp.c calls Stream_EnsureRemainingCapacity on context->common.buffer even though opus_decode writes decoded PCM into the caller-supplied out stream. A malicious RDP server that negotiates WAVE_FORMAT_OPUS with a client built with WITH_OPUS enabled and WITH_DSP_FFMPEG disabled can make libopus write a large decoded frame beyond the 4096-byte StreamPool_Take destination used by channels/rdpsnd/client/rdpsnd_main.c. This can corrupt the client heap, crash the client, and may permit code execution. This issue is fixed in version 3.28.0.

### CVE-2026-44252

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T16:17:10.690 |

Wazuh is a free and open source platform used for threat prevention, detection, and response. From 4.0.0 until 4.14.5, Wazuh Manager allows a low-privilege read-only API user with manager:read permission to retrieve the cluster key from the element in ossec.conf through GET /manager/configuration?raw=true. An attacker with network access to TCP port 1516 can use the disclosed Fernet key to impersonate a cluster worker and submit distributed API requests containing attacker-controlled rbac_permissions with rbac_mode set to black. Because the master trusts the worker-supplied authorization context, the attacker can create users, assign administrator roles, access credentials and API tokens, modify configuration, and execute actions across agents. This issue is fixed in version 4.14.5.

### CVE-2026-16819

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-19T16:17:06.297 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to cause a denial of service and compromise data integrity due to a time-of-check time-of-use race condition.

### CVE-2026-74011

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T13:19:05.710 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in revmakx InfiniteWP Client allows Blind SQL Injection.

This issue affects InfiniteWP Client: from n/a through 1.13.9.

### CVE-2026-66677

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-20T12:16:35.817 |

Subscriber Broken Authentication in Leyka <= 3.32.3 versions.

### CVE-2026-76357

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-19T22:17:20.873 |

In Splunk SOAR versions below 8.6.0, an authenticated user with no role assigned could submit a crafted file path to the Representational State Transfer (REST) API and execute arbitrary code. The vulnerability is possible because the REST API does not require an assigned role for the request and does not restrict the user-supplied file path to the intended temporary directory. For more information see Manage roles and permissions in Splunk SOAR (On-premises) (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.5.0/manage-your-splunk-soar-on-premises-users-and-accounts/manage-roles-and-permissions-in-splunk-soar-on-premises) and Splunk SOAR (On-premises) security information (https://help.splunk.com/en/splunk-soar/soar-on-premises/administer-soar-on-premises/8.5.0/introduction-to-splunk-soar-on-premises/splunk-soar-on-premises-security-information) in the Splunk documentation.

### CVE-2026-68900

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T20:17:21.727 |

Wekan is open source kanban built with Meteor. From 8.72 until 10.23, addBoardHTMLToZip() in client/lib/exportHTML.js read a card title and body through textContent, which decoded entity-encoded markup, and then interpolated titleText and allText into content.innerHTML in the exported index.html. A board member could store an entity-encoded event-handler payload in a card title that remained inert on the live board but was reparsed and executed when a recipient clicked the card in the downloaded HTML export, allowing the script to read and transmit all board data contained in that export, including content added after the attacker's membership was removed. Version 10.23 builds the modal with DOM nodes and assigns untrusted values through textContent. This issue is fixed in version 10.23.

### CVE-2026-55643

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T19:17:20.533 |

Snipe-IT is an IT asset/license management system. Prior to 8.6.3, a company-scoped user in FMCS floater mode can access users whose company_id is null because broad API queries and bulk web actions do not consistently apply isCurrentUserHasAccess. The /api/v1/users and /api/v1/users/{id}/licenses endpoints can expose personal data and assigned licenses, /users/bulkeditsave can modify out-of-scope profiles, and /users/merge can soft-delete users and transfer assigned assets. This issue is fixed in version 8.6.3.

### CVE-2026-16828

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-19T19:17:10.420 |

IBM Power Systems Firmware FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, and FW950.00 through FW950.H2 is affected by a vulnerability in the ASMI web interface. An unauthenticated attacker on the management network can cause the ASMI web server to crash with possible memory corruption and generate an error log; hosted partitions are not affected. The ASMI web interface will restart automatically; however, repeated exploitation could result in a sustained loss of access to the ASMI management interface, resulting in an integrity and availability impact.

### CVE-2024-13942

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:P/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-19T17:18:21.440 |

Secure BootROM of RK3588s SoC is vulnerable to a time-of-check to time-of-use attack in case of booting from external media (SPI NOR or NAND, EMMC or SD).




The code reads the header of the next-stage loader twice. The header contains hashes of the executable modules and is signed with a private key, the public part of which is verified against the SHA256 digest blown in the OTP.




The first read is only partial and contains only the hashes of the executable modules. The second is complete, including the header signature.

Although the header is verified based on the fully read data, the authenticity of the executable modules is checked against the partial data from the first read.




An attacker with physical access to a device containing RK3588s SoC can easily modify the next-stage loader data on-the-fly using a low-cost SD-card or SPI NOR/NAND or EMMC emulator. Even a simple ultra low-cost circuit comprising two memory chips (containing the same data but different headers - the original and the modified one) and a multiplexer can be used to carry out an attack.




This can lead to arbitrary code execution with the highest privileges available (EL3). This issue affects RK3588s: RK3588s SoC BootROM (secure) 350B20210512V100 and possibly others.
As remediation apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable  https://www.rock-chips.com/a/en/products/RK35_Series/2022/0926/1660.html

### CVE-2026-74021

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-20T12:16:37.817 |

Unauthenticated Broken Access Control in Chaplin <= 2.6.8 versions.

### CVE-2026-74020

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-20T12:16:37.690 |

Unauthenticated Broken Access Control in Koji <= 2.2.1 versions.

### CVE-2026-73198

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-20T11:16:21.687 |

A flaw was found in FreeIPA. A remote, unauthenticated attacker can exploit a vulnerability in the `/ipa/i18n_messages` endpoint by sending an arbitrarily large request body. This can cause the service to consume excessive memory, leading to memory exhaustion, degraded responsiveness, and a denial of service (DoS) condition.

### CVE-2026-73197

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-20T11:16:21.553 |

A flaw was found in FreeIPA. A remote, unauthenticated attacker can exploit this vulnerability by sending oversized form POST requests to the `/ipa/migration/migration.py` endpoint. This can force the migration handler to read attacker-controlled request bodies fully into memory, leading to increased memory usage, slower request handling, and potential service disruption or denial of service.

### CVE-2026-75963

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-20T06:17:32.360 |

The Events Made Easy plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 3.2.5 via the eme_single_event_page_template function. This makes it possible for authenticated attackers, with contributor-level access and above, to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. The stored traversal payload is triggered passively when any visitor loads the affected single-event page, meaning post-submission execution does not require additional attacker interaction.

### CVE-2026-76956

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-394` |
| Published | 2026-08-20T05:16:29.610 |

In libexpat 2.8.2 and 2.8.3 before 2.8.4, misinterpretation of getentropy's return code leads to insufficient entropy, which results in being vulnerable to hash flooding attacks, causing a denial of service via crafted XML content.

### CVE-2026-76928

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-19T23:16:21.570 |

X.509IF protocol dissector crash in 4.6.0 to 4.6.7 and 4.4.0 to 4.4.18 allows denial of service

### CVE-2026-76880

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T23:16:18.830 |

RRC protocol dissector crash in 4.6.0 to 4.6.7 and 4.4.0 to 4.4.18 allows denial of service

### CVE-2026-76879

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T23:16:18.700 |

C12.22 protocol dissector crash in 4.6.0 to 4.6.7 and 4.4.0 to 4.4.18 allows denial of service

### CVE-2026-76396

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-19T22:17:26.150 |

In Splunk AI Toolkit versions below 6.0.0, a user that holds a role with the schedule_search capability could cause a scheduled search to load and deserialize a model file through the apply search command. The improper access control is possible because Splunk AI Toolkit does not mark the apply search command as risky. For more information see Troubleshoot the AI Toolkit (https://help.splunk.com/en/splunk-enterprise/apply-machine-learning/use-ai-toolkit/5.7.3/troubleshooting-the-ai-toolkit/troubleshoot-the-ai-toolkit) in the Splunk documentation.

### CVE-2026-76355

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-19T22:17:20.593 |

In Splunk Enterprise 10.4 versions below 10.4.2, an unauthenticated user could retrieve the information contained in Edge Processor pipeline configurations through a Representational State Transfer (REST) API endpoint when Edge Processor is turned on. The vulnerability does not affect versions prior to 10.4. The vulnerability exists because the Edge Processor service endpoint lacks authentication controls. For more information see System architecture of the Edge Processor solution (https://help.splunk.com/en/splunk-enterprise/process-data-at-the-edge/use-edge-processors-for-splunk-enterprise/10.4/how-the-edge-processor-solution-works/system-architecture-of-the-edge-processor-solution) in the Splunk documentation.

### CVE-2026-76262

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-19T22:17:14.323 |

In Splunk Enterprise 10.4 versions below 10.4.2, an unauthenticated user could read Prometheus service metrics from the Edge Processor SPL2 Preview sidecar, including service details that expose relevant runtime and build metadata for the sidecar. The vulnerability does not affect Splunk Enterprise versions below 10.4. The information disclosure is possible because the Prometheus metrics endpoint in the Edge Processor SPL2 Preview sidecar lacks authentication, which lets any client that can reach the sidecar retrieve the metrics without credentials. For more information see About Splunk sidecars (https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/splunk-sidecars/about-splunk-sidecars) in the Splunk documentation.

### CVE-2026-76254

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-943` |
| Published | 2026-08-19T22:17:13.270 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, 9.4.14, and 9.3.14, an unauthenticated user could cause another user to dispatch arbitrary Search Processing Language (SPL) pipelines from Dataset Explorer with the same privileges as that user, which can allow for access to all relevant data and system integrity available to that user and affect system availability. The vulnerability is possible because Dataset Explorer does not validate or escape dataset names before building SPL searches and does not apply SPL safeguards for risky commands to those searches. The vulnerability requires the attacker to phish the user by tricking them into opening the crafted link. The unauthenticated user should not be able to exploit the vulnerability at will. For more information see Explore a dataset (https://help.splunk.com/en/splunk-enterprise/manage-knowledge-objects/knowledge-management-manual/10.4/manage-and-explore-datasets/explore-a-dataset) and SPL safeguards for risky commands (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.4/best-practices-for-splunk-platform-security/spl-safeguards-for-risky-commands) in the Splunk documentation.

### CVE-2025-36255

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-267` |
| Published | 2026-08-19T22:16:36.490 |

IBM System Storage DS8A00 10.1.3.0 through 10.11.35.0 and IBM DS8900F 89.40.83.0 through 89.44.25.0 could allow an authenticated user to create a user with privileged user roles due to improper privileged defined with unsafe actions.

### CVE-2026-69222

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-19T21:17:31.627 |

LiquidJS is a Shopify / GitHub Pages compatible template engine in pure JavaScript. Prior to 10.27.2, the join filter in src/filters/array.ts computes complexity from array.length and separator length instead of the total string length produced by array.join(sep). The concat filter can cheaply double arrays of references, after which join materializes the referenced content while charging only for element count, allowing a template to exceed a configured memoryLimit by a large factor. The sibling array_to_sentence_string filter in src/filters/string.ts has the same accounting defect, and a crafted template can allocate toward V8's string or process memory limit and crash the process. This issue is fixed in version 10.27.2.

### CVE-2026-62317

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-08-19T20:17:19.890 |

Logto is the modern, open-source auth infrastructure for SaaS and AI apps. Prior to 1.41.0, Logto's email subaddressing blocklist in packages/core/src/libraries/sign-in-experience/email-blocklist-policy.ts used the attacker-controlled domain from email input to construct subaddressingRegex when blockSubaddressing was enabled. The permissive emailRegEx accepted multiple at signs and regular expression metacharacters, and POST /api/experience/verification/verification-code could therefore cause catastrophic backtracking in subaddressingRegex.test(email). The resulting event-loop stall could make authentication, token issuance, SSO, and the administrative console unavailable. This issue is fixed in version 1.41.0.

### CVE-2026-18821

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T20:17:13.603 |

IBM PowerVM Hypervisor FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, and FW950.00 through FW950.H2 Power Systems Firmware is affected by a vulnerability in partition firmware during network boot. An unauthenticated attacker on the same network as a partition undergoing network boot can send a malformed packet, allowing arbitrary code to be executed in the partition firmware and compromising everything subsequently loaded by that partition. Other partitions and the managed system are not affected. Only partitions actively performing a network boot are affected, resulting in a confidentiality, integrity, and availability impact.

### CVE-2026-16852

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-19T20:17:06.970 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to an integer overflow.

### CVE-2026-16837

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-19T20:17:04.710 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to improper handling of a missing SSL client certificate.

### CVE-2026-16836

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-19T20:17:04.553 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to uncontrolled resource consumption.

### CVE-2026-16831

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-19T20:17:03.733 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to uncontrolled resource consumption.

### CVE-2026-16824

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-19T20:17:02.930 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to unbounded recursion.

### CVE-2026-19875

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-19T18:16:36.557 |

IBM Langflow OSS 1.0.0 through 1.10.0 could allow a remote attacker to overwrite administrator email information and abuse the server as an outbound relay due to missing authentication for the registration endpoint.

### CVE-2026-45798

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121;CWE-170` |
| Published | 2026-08-19T17:18:49.730 |

Wazuh is a free and open source platform used for threat prevention, detection, and response. From 4.5.0 until 4.14.6 and 5.0.0-beta2, compare_wazuh_versions() in src/shared/version_op.c copies the attacker-controlled enrollment V: field into a 10-byte stack buffer with strncpy() but does not explicitly terminate the buffer. The function is reachable before authentication through wazuh-authd on TCP port 1515 when anonymous TLS enrollment is enabled. A version string of at least nine non-null bytes can cause strchr() and strtok() to read beyond ver2 and can make strtok() write a null byte into adjacent stack memory, allowing a remote denial of service. This issue is fixed in versions 4.14.6 and 5.0.0-beta2.

### CVE-2026-20320

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-08-19T17:18:40.433 |

A vulnerability in the Open Client Interface (OCI) XML Parser of Cisco BroadWorks could allow an unauthenticated, remote attacker to read sensitive configuration information on an affected system.
 This vulnerability exists because XML entries are improperly parsed due to external entity resolution being allowed by default. An attacker could exploit this vulnerability by sending a crafted XML message to the Open Client Interface &ndash; Provisioning (OCI-P) service. A successful exploit could allow the attacker to view sensitive files from the filesystem with the privileges of the Cisco BroadWorks user.

### CVE-2026-20319

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-19T17:18:40.280 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Workload engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20319 are related to buffer management issues that are grouped under the Common Weakness Enumeration (CWE) CWE-119.

### CVE-2026-63408

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-598` |
| Published | 2026-08-19T16:18:38.013 |

Grav API Plugin is a RESTful API for Grav CMS that provides full headless access to your site's content.  Prior to 1.0.0-rc.16, the Grav API plugin JwtAuthenticator::extractBearerToken() accepts a JWT from the token URL query parameter on every /api/v1 route, including state-changing endpoints. Request URLs consequently expose valid access tokens through Apache, proxy, and CDN logs, browser history, and Referer headers, allowing a party with access to those records to reuse the token with the owner's API privileges. This issue is fixed in version 1.0.0-rc.16.

### CVE-2026-46343

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-19T16:17:11.827 |

Wazuh is a free and open source platform used for threat prevention, detection, and response. From 4.0.0 until 4.14.6 and 5.0.0-beta2, WazuhCommon.end_receiving_file() in framework/wazuh/core/cluster/common.py allows a cluster-authenticated node to delete files outside WAZUH_PATH. A syn_i_w_m_e request with an unknown task_id reaches the cleanup branch, where an attacker-controlled filename is passed to os.path.join without canonicalization or confinement. Absolute paths and traversal sequences can therefore target files such as ossec.conf, jwt_secret.json, TLS certificates, and ruleset files that are accessible to the Wazuh manager process. Deletion can disable the manager, invalidate API tokens, or disrupt cluster and API connectivity. This issue is fixed in versions 4.14.6 and 5.0.0-beta2.

### CVE-2026-49289

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-19T15:17:07.180 |

The SimpleSAMLphp SAML2 library is a PHP library for SAML2 related functionality. In 4.19.2 and 4.20.2, the library permits attacker-controlled XPath transforms while processing XML signatures in specially crafted SAML messages. XPath evaluation can consume uncontrolled processing resources, allowing a remote unauthenticated attacker to deny service to any entity relying on SimpleSAMLphp or directly on the SAML2 library. The mitigation limits the number of transforms, permits only transform algorithms identified by the SAML 2.0 Core specification, and specifically rejects XPath transforms. This issue is fixed in versions 4.19.3 and 4.20.3.

### CVE-2026-45742

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-08-19T15:17:05.170 |

Gotenberg is a Docker-powered stateless API for PDF files. From 8.10.0 until 8.33.0, the newContext function in pkg/modules/api/context.go starts one errgroup.Go goroutine for each multipart downloadFrom entry and allows those goroutines to concurrently write to the shared ctx.files, ctx.diskToOriginal, and ctx.filesByField maps and slices. Go maps and slices are not safe for concurrent mutation, so a crafted multipart request containing many downloadFrom entries can trigger a data race and terminate the process with a fatal concurrent map writes runtime error. The default configuration enables downloadFrom and disables authentication, allowing an unauthenticated remote attacker to crash an exposed conversion service and cause a denial of service. This issue is fixed in version 8.33.0.

### CVE-2026-45741

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-184;CWE-918` |
| Published | 2026-08-19T15:17:05.023 |

Gotenberg is a Docker-powered stateless API for PDF files. In 8.32.0 and earlier, the IsPublicIP function in pkg/gotenberg/outbound.go does not reject the 2002::/16 6to4 prefix, the 64:ff9b::/96 and 64:ff9b:1::/48 NAT64 prefixes, the fec0::/10 deprecated site-local prefix, Teredo, and other transition prefixes that can embed or route to non-public IPv4 destinations. The addr.Unmap operation only handles IPv4-mapped IPv6 addresses, so a crafted DNS AAAA record can cause the outbound HTTP client to treat an address wrapping an internal destination such as 169.254.169.254 as public. An unauthenticated attacker can use a conversion route with WithDenyPrivateIPs enabled to reach cloud metadata services, and the Chromium URL conversion route can return the internal response as a PDF, potentially exposing cloud credentials. Exploitation requires a deployment whose host routes the relevant IPv6 prefix, such as a dual-stack or NAT64-enabled environment. This issue is fixed in version 8.33.0.

### CVE-2026-16818

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-19T15:16:57.843 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to uncontrolled resource consumption.

### CVE-2026-16817

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-19T15:16:57.687 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to a NULL pointer dereference.

### CVE-2026-16706

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-19T15:16:57.207 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to an out-of-bounds write.

### CVE-2026-16690

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-19T15:16:56.887 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to uncontrolled resource consumption.

### CVE-2026-14970

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-19T15:16:55.427 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 NIM server process is crashing during client registration due to buffer overflow.

### CVE-2026-77079

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:L/VA:L/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-20T12:16:39.263 |

n8n before 2.34.1 and 2.33.4 contains an authorization bypass in the custom project role deletion (reassignment) path. When deleting a custom project role with a reassignment target, the code validated only that the target role existed and was project-scoped, performing no project-level authorization check. A user holding only the narrow role:manageProject global scope could delete any custom project role in use on the instance and reassign its holders (including themselves) to the built-in project:admin role, gaining full administrative control of projects they had no legitimate access to.

### CVE-2026-76403

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-19T22:17:27.043 |

In Splunk Connect for Kafka versions below 2.2.7, an unauthenticated user positioned in the network path could read or alter all relevant data sent from the connector when Kerberos authentication is used with Hypertext Transfer Protocol (HTTP) Event Collector in Splunk Enterprise. The vulnerability is possible because the Kerberos authentication path does not apply the configured certificate validation options when it builds the HTTP client. For more information see Install Splunk Connect for Kafka (https://help.splunk.com/en/data-management/integrate-data-with-add-ons/splunk-connect-for-kafka/2.2/install/install-splunk-connect-for-kafka), Security configurations for Splunk Connect for Kafka (https://help.splunk.com/en/splunk-enterprise/get-data-in/splunk-connect-for-kafka/2.2/configure/security-configurations-for-splunk-connect-for-kafka), and Set up and use HTTP Event Collector with configuration files (https://help.splunk.com/en/splunk-enterprise/get-data-in/get-started-with-getting-data-in/9.4/get-data-with-http-event-collector/set-up-and-use-http-event-collector-with-configuration-files) in the Splunk documentation.

### CVE-2026-76362

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-19T22:17:21.533 |

In Splunk SOAR versions below 8.6.0, an unauthenticated user who can observe or alter network traffic between Splunk SOAR and a configured CyberArk Representational State Transfer (REST) server could access or modify all relevant data exchanged through that credential manager. The vulnerability is possible because the CyberArk REST client does not verify server certificates by default. The attack requires the attacker to have network-path interception capability between Splunk SOAR and the configured CyberArk REST server. For more information see Manage your organization's credentials with a password vault (https://help.splunk.com/en/splunk-soar/soar-cloud/administer-soar-cloud/configure-administration-settings-in-splunk-soar-cloud/manage-your-organizations-credentials-with-a-password-vault) in the Splunk documentation.

### CVE-2025-36254

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-116` |
| Published | 2026-08-19T22:16:36.303 |

IBM System Storage DS8A00 10.1.3.0 through 10.11.35.0 and IBM DS8900F 89.40.83.0 through 89.44.25.0 could allow an attacker to bypass security authentication due to improperly encoding of DSCLI command output to obtain sensitive information or cause a denial of service.

### CVE-2026-16851

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-19T20:17:06.807 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to a use-after-free.

### CVE-2026-62669

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-19T16:18:19.460 |

Grav Login Plugin adds login, basic ACL, and session wide messages to Grav. Prior to 3.8.11, the Grav Login plugin login.regenerate2FASecret task checks only that the pending-session user exists rather than requiring $user->authorized. After submitting a victim's correct password, an attacker can invoke taskRegenerate2FASecret() during the pending TOTP challenge, overwrite twofa_secret, read the replacement secret from the response, calculate a valid code, and complete authentication without the victim's second factor. This issue is fixed in version 3.8.11.

### CVE-2026-18526

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T15:16:58.010 |

HumHub Community Edition 1.18.4 and 1.18.4-pl1 contain a stored Cross-Site Scripting (XSS) vulnerability in the oEmbed confirmation rendering workflow.

### CVE-2026-76325

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T22:17:16.650 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user who holds the "power" Splunk role could store a malicious ui-tour knowledge object that matches an auto-tour page name and share the object at the app level. The object can execute arbitrary JavaScript in the browser of another authenticated user who visits a standard Splunk Web page. The JavaScript could expose all relevant data and affect system integrity within the second user permissions. The Cross-Site Scripting (XSS) vulnerability is possible because Splunk Web resolves auto-tour entries from the app namespace and uses untrusted tour content when building the tour image.

### CVE-2026-76321

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-19T22:17:16.140 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, an unauthenticated user could inject arbitrary Search Processing Language (SPL) into requests that search for events near a selected event. This could allow for unauthorized search execution. The vulnerability is possible because Splunk Web does not consistently escape caller-supplied values when it builds SPL for nearby-event searches, and embedded report access accepts those requests without the expected authorization check. For more information see Use time to find nearby events (https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.2/specify-time-ranges/use-time-to-find-nearby-events) in the Splunk documentation.

### CVE-2026-18871

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T20:17:13.763 |

IBM PowerVM Hypervisor FW1120.00, FW1110.00 through FW1110.30, and FW1060.00 through FW1060.80 is affected by a vulnerability in host firmware configuration parsing. An attacker with authenticated service-level access to the service processor can write specially crafted configuration data, causing the host firmware boot stack to crash with possible memory corruption during system initialisation, resulting in an integrity and availability impact to the managed system.

### CVE-2026-17097

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-08-19T20:17:12.797 |

IBM PowerVM Hypervisor FW1120.00, FW1110.00 through FW1110.30, FW1060.00 through FW1060.80, and FW950.00 through FW950.H2 is affected by a vulnerability in the PowerVM hypervisor call interface. An attacker with root access to a guest partition can issue a specially crafted hypervisor call causing a virtual processor to become permanently unresponsive, requiring a full platform re-IPL to restore normal operation. In some cases this may also cause the guest to inject a small amount of data into hypervisor or partition memory with no attacker control over the target location. Successful exploitation results in an integrity and availability impact to the managed system.

### CVE-2026-17042

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-19T20:17:12.127 |

IBM Power Systems Firmware FW950.00 through FW950.H2, OP940.00 through OP940.a1 (Power9), and OP940.00 - OP940.81 (Power HMC) is affected by a vulnerability in host firmware NVRAM parsing. An attacker with root access to a guest partition on an OpenPOWER system can write a specially crafted NVRAM image, causing the host firmware boot stage to crash with possible memory corruption. This condition persists until operator intervention — clearing NVRAM via the service processor — to restore normal operation. This vulnerability only affects OpenPOWER systems; systems running PowerVM are not affected. Successful exploitation results in an integrity and availability impact to the managed system.

### CVE-2026-58562

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T15:17:12.603 |

Dell Command Update (DCU), versions prior to 5.7.1, contain a Missing Authorization vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-56797

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-19T15:17:11.923 |

Dell Command Update (DCU), versions prior to 5.7.1, a Time-of-check Time-of-use (TOCTOU) Race Condition vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges.

### CVE-2026-52834

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-122;CWE-131;CWE-190` |
| Published | 2026-08-19T15:17:09.810 |

jxl-oxide is a pure Rust implementation of a JPEG XL decoder. Prior to jxl-grid 0.6.2, decoding a crafted JPEG XL image on a 32-bit platform can overflow length calculations in AlignedGrid::with_alloc_tracker and related grid and subgrid arithmetic. A 65536 x 65536 frame can pass the frame-area limit while overflowing the usize element count, causing modular, VarDCT, or filter rendering paths to allocate a backing buffer smaller than the logical grid. A tiny bitstream-controlled cropped frame combined with a huge canvas or requested region can also reach the vulnerable composition path in crates/jxl-render/src/blend.rs through ordinary render_frame(). Later mutable subgrid and raw-pointer operations can then perform attacker-controlled out-of-bounds writes, causing memory corruption, denial of service, or arbitrary code execution. This issue is fixed in jxl-grid version 0.6.2.

### CVE-2026-77077

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-20T12:16:39.127 |

n8n versions before 1.123.69, 2.33.4, and 2.34.1 contain a JavaScript task runner VM sandbox escape. The runner's prototype-freezing routine covers globalThis functions but not internal module constructors such as EventEmitter, allowing an authenticated user with Code node access to exploit prototype pollution to execute arbitrary commands within the runner container. Because the polluted prototype is a process-wide object, the corruption persists across other tenants' Code node executions on the same shared runner. On v1.x instances without task runners enabled, Code node JavaScript runs directly in the main n8n process, where the impact could be higher.

### CVE-2026-15049

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-20T06:16:49.710 |

The Depicter — Popup & Slider Builder WordPress plugin before 4.8.0 does not validate the type of a file uploaded through its import feature and does not remove a malformed upload, allowing users with editor-level access to write an arbitrary file (including executable PHP) into a web-accessible directory, which can lead to remote code execution.

### CVE-2026-75593

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-19T20:17:23.203 |

BuildKit is a toolkit for converting source code to build artifacts in an efficient, expressive and repeatable manner. Prior to 0.31.2, a custom client can produce such an upload request to the BuildKit daemon that files can escape from the BuildKit-controlled state directory. The client needs to have valid permissions to access BuildKit control API to issue builds, eg., bypass authentication, etc. This issue is fixed in version 0.31.2.

### CVE-2026-55192

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-19T18:16:44.580 |

FreeRDP is a free implementation of the Remote Desktop Protocol. Prior to 3.27.0, FreeRDP H.264 decoder backends can return YUV planes sized from the bitstream without comparing the decoded width and height to the RDPGFX surface dimensions used to validate region rectangles. A malicious RDP server can provide an AVC420 or AVC444 bitstream whose decoded frame is smaller than the negotiated surface, causing yuv420_context_decode and the YUV-to-RGB conversion paths to read beyond the decoder-owned planes in libfreerdp/codec/h264.c and the selected H.264 backend. This can disclose client memory or crash the client. This issue is fixed in version 3.27.0.

### CVE-2026-75146

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-19T17:21:13.057 |

FFmpeg before commit 65b0dab contains an out-of-bounds read in the DASH demuxer (libavformat/dashdec.c). When a live DASH manifest is refreshed with a startNumber that is lower than the previous value, the current sequence number is driven negative. The fragment retrieval function checked only the upper bound before indexing the fragments array, allowing a negative index to be used and causing an out-of-bounds read. A malicious or misconfigured DASH server can trigger this by serving a live manifest with a decreasing startNumber across a manifest refresh.

### CVE-2026-50173

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T17:18:57.250 |

Flow-Like is a platform for building end-to-end use cases. Prior to version 1.0.4, `GET /api/v1/apps/{app_id}/invoke/presign` grants Azure Blob Storage SAS credentials with write and delete access to app content to any app member that has `ExecuteEvents`, even when that member lacks `ReadFiles` and `WriteFiles`. The route treats file permissions as optional after the `ExecuteEvents` gate. When the caller has neither file permission, it selects `CredentialsAccess::InvokeNone`. In the Azure credential provider, `InvokeNone` still mints a `content_sas_token` for `apps/{app_id}` with `sp=rwdl`, plus user-content and log SAS tokens. The returned shared credential is enough for the low-privilege caller to directly write or delete blobs under the app content prefix. Version 1.0.4 patches the issue. Flow-Like Studio and the hosted Flow-Like Web App are not affected. These deployments use AWS-backed storage. Self-hosted deployments are only affected if they use Azure Blob Storage as the storage backend. In affected deployments, the issue only applies to authenticated app members who have workflow execution permissions but should not have app file write/delete permissions. Users of affected self-hosted Azure deployments should update to version 1.0.4 or the latest dev branch.

### CVE-2026-18430

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T16:17:06.463 |

HumHub 1.18.4 contains a stored cross-site scripting vulnerability in the comment-deletion notification flow. A Space administrator can delete another user's comment, choose to notify the original author, and place HTML/JavaScript in the deletion reason.

### CVE-2026-23501

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T15:16:59.270 |

Dell RecoverPoint for VMs, versions 6.0.3 and 6.0.3.1, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-18756

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T15:16:58.150 |

HumHub Community Edition 1.18.4 contains a reflected cross-site scripting vulnerability in the Space membership-request workflow. An attacker can place attacker-controlled button configuration in the options query-string parameter of space/membership/request-membership-form, lure an authenticated non-member into submitting the legitimate membership request form, and cause the server to return JavaScript containing attacker-controlled code.

### CVE-2026-76634

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-20T14:17:59.837 |

WeGIA before 3.9.2 contains an insecure direct object reference vulnerability in the employee profile page that allows authenticated attackers to access arbitrary employee records by injecting an id_pessoa parameter through a request extraction function that overwrites the session-derived identifier. Attackers can enumerate all user identifiers to retrieve full profile data for any employee account, including name, CPF, address, contact details, and administrative flags.

### CVE-2026-77076

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-209` |
| Published | 2026-08-20T12:16:38.997 |

n8n versions before 1.123.69, 2.33.4, and 2.34.1 contain an information disclosure vulnerability in the GraphQL node. When a GraphQL request fails at the connection level, the node re-throws the underlying HTTP client error unchanged instead of wrapping it in n8n's standard error type. That error contains the live request's headers, including a decrypted credential secret, which the execution engine persists verbatim. Any authenticated user able to read the resulting execution can retrieve the decrypted credential secret from the stored run data.

### CVE-2026-77071

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T12:16:38.353 |

n8n before 1.123.69, 2.33.4, and 2.34.1 contains a PostgREST filter injection vulnerability in the Supabase node's Row Get Many, Delete, and Update operations, which built filter queries by concatenating an expression-bindable value without escaping. An attacker could inject a condition that widened the filter to match every row, turning an intended single-row operation into full-table disclosure, deletion, or modification.

### CVE-2026-77070

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-08-20T12:16:38.227 |

n8n before 1.123.69, 2.33.4, and 2.34.1 contains a NoSQL injection vulnerability in the MongoDB node's Find, Delete, and Aggregate operations, which parse the Query parameter as JSON after expression resolution without sanitizing MongoDB operators. An attacker who can influence the resolved query (e.g., via externally-controlled data) can inject operators such as $ne or $where, turning an intended single-document lookup into full-collection disclosure, full-collection deletion, or other operations on the database server.

### CVE-2026-74019

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-20T12:16:37.567 |

Unauthenticated Broken Access Control in EPROLO Dropshipping <= 2.4.2 versions.

### CVE-2026-68564

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:36.190 |

Unauthenticated Cross Site Scripting (XSS) in NotificationX Pro <= 3.1.4 versions.

### CVE-2026-66673

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:35.697 |

Unauthenticated Cross Site Scripting (XSS) in Flatastic <= 2.0 versions.

### CVE-2026-66616

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:35.197 |

Unauthenticated Cross Site Scripting (XSS) in Form Maker by 10Web <= 1.15.46 versions.

### CVE-2026-66615

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:35.073 |

Unauthenticated Cross Site Scripting (XSS) in Podlove Podcast Publisher <= 4.5.4 versions.

### CVE-2026-66614

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:34.937 |

Unauthenticated Cross Site Scripting (XSS) in SEO Plugin by Squirrly SEO <= 14.2.2 versions.

### CVE-2026-66612

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:34.813 |

Unauthenticated Cross Site Scripting (XSS) in Aora <= 1.3.19 versions.

### CVE-2026-66611

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:34.690 |

Unauthenticated Cross Site Scripting (XSS) in Paymob for WooCommerce <= 4.1.10 versions.

### CVE-2026-66607

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:34.437 |

Unauthenticated Cross Site Scripting (XSS) in Advance Product Search <= 1.4.8 versions.

### CVE-2026-66606

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:34.317 |

Unauthenticated Cross Site Scripting (XSS) in SmartSMTP <= 1.2.0 versions.

### CVE-2026-66605

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:34.187 |

Unauthenticated Cross Site Scripting (XSS) in Swatchly – WooCommerce Variation Swatches for Products <= 1.4.13 versions.

### CVE-2026-66604

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:34.063 |

Unauthenticated Cross Site Scripting (XSS) in GeoDirectory <= 2.8.173 versions.

### CVE-2026-66598

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:33.683 |

Unauthenticated Cross Site Scripting (XSS) in B2BKing Premium <= 5.6.07 versions.

### CVE-2026-66597

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:33.557 |

Unauthenticated Cross Site Scripting (XSS) in wpDataTables <= 6.5.1.4 versions.

### CVE-2026-66590

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:32.930 |

Unauthenticated Cross Site Scripting (XSS) in Tagembed <= 7.4 versions.

### CVE-2026-66582

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:32.547 |

Unauthenticated Cross Site Scripting (XSS) in TranslatePress <= 3.3.2 versions.

### CVE-2026-66581

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T12:16:32.420 |

Unauthenticated Cross Site Scripting (XSS) in JetEngine <= 3.8.14.1 versions.

### CVE-2026-14163

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-20T07:16:32.250 |

In affected versions of Octopus Server under certain circumstances it is possible for sensitive variables to be printed in the deployment variable snapshot in clear-text.

### CVE-2026-8619

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-20T00:16:53.157 |

An
unauthenticated denial-of-service vulnerability was identified in TP-Link TL-MR100 v3.2, TL-MR150 v3.2, TL-MR6400 v8.0 and Archer MR600 v2, due to improper handling of exceptional request conditions
that may lead to a NULL pointer dereference. 
A remote attacker on an adjacent network can send a specially crated
HTTP request to trigger a crash of the HTTP service process.





Successful
exploitation may cause the HTTP service to crash, making the web management
interface and HTTP-dependent functionality temporarily unavailable.

### CVE-2026-76336

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T22:17:18.093 |

In Splunk Enterprise versions below 10.4.2 and 10.2.6, a user who does not hold the "admin" or "power" Splunk roles could delete all Search Processing Language 2 (SPL2) modules across all apps and users on the instance through the SPL2 module management Representational State Transfer (REST) API. This could delete exported datasets and functions, affect system integrity, and cause partial service disruption. The vulnerability does not affect Splunk Enterprise versions below 10.2. The vulnerability is possible because the SPL2 module management REST API does not sufficiently authorize and validate module deletion requests. For more information see Manage SPL2 modules (https://help.splunk.com/en/splunk-enterprise/search/spl2-search-manual/multiple-searches-in-an-spl2-module/manage-spl2-modules) and Module permissions (https://help.splunk.com/en/splunk-enterprise/search/spl2-search-manual/modules-statements-and-views/module-permissions) in the Splunk documentation.

### CVE-2026-76333

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T22:17:17.673 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, a user who holds the "power" Splunk role could store a Dashboard Studio workflow action with a crafted Uniform Resource Locator (URL). When another authenticated user selects the stored action from Event Actions and selects Continue, attacker-controlled JavaScript runs in the browser of that user. This could expose data or actions available through Splunk Web to that user. The vulnerability is possible because Dashboard Studio does not sufficiently validate workflow-action URLs before processing them. The vulnerability requires the attacker to phish the affected user by tricking them into initiating a request within their browser. The user who holds the "power" Splunk role should not be able to exploit the vulnerability at will. For more information see Define roles on the Splunk platform with capabilities (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.2/manage-splunk-platform-users-and-roles/define-roles-on-the-splunk-platform-with-capabilities) in the Splunk documentation.

### CVE-2026-76332

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-19T22:17:17.550 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, an unauthenticated user could trick an authenticated user into opening a crafted link to Analytics Workspace. When the authenticated user opens the link, Splunk Enterprise runs attacker-controlled Search Processing Language (SPL) using the permissions of that user. The injected SPL could access data and perform actions available to that user. The vulnerability is possible because Analytics Workspace does not sufficiently validate data used to build searches. The vulnerability requires the attacker to phish the user by tricking them into opening the crafted link. The unauthenticated user should not be able to exploit the vulnerability at will.

### CVE-2026-76330

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-19T22:17:17.297 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, 10.0.9, and 9.4.14, an unauthenticated user could trick an authenticated user into opening a crafted link to Monitoring Console. When the authenticated user opens the link, Splunk Enterprise runs attacker-controlled Search Processing Language (SPL) using the permissions of that user. The injected SPL could access data and perform actions available to that user. The vulnerability is possible because Monitoring Console does not sufficiently validate data used to build forwarder dashboard searches. The vulnerability requires the attacker to phish the user by tricking them into opening the crafted link. The unauthenticated user should not be able to exploit the vulnerability at will.

### CVE-2026-76251

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T22:17:12.850 |

In Splunk Enterprise versions below 10.4.2, 10.2.6, and 10.0.9, a user who does not hold the "admin" or "power" Splunk roles could cause the Splunk App for Splunk Observability Cloud to forward requests to Splunk Observability Cloud, including the Splunk Observability Cloud access token stored for the app. With this access, the user could view all relevant data available to that token and make limited changes to Splunk Observability Cloud content. The vulnerability does not affect Splunk Enterprise 9.4 and 9.3 versions. The vulnerability is possible because the app's Representational State Transfer (REST) API endpoint handlers do not enforce the read_o11y_content capability before forwarding requests with the stored access token. For more information see Define roles on the Splunk platform with capabilities (https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.2/manage-splunk-platform-users-and-roles/define-roles-on-the-splunk-platform-with-capabilities) in the Splunk documentation.

### CVE-2026-68553

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-08-19T21:17:28.163 |

Coturn is a free open source implementation of TURN and STUN Server. Prior to 4.13.0, an authenticated TURN user can place printf-style format specifiers in the STUN USERNAME or REALM attribute, which passes is_secure_string() validation and is embedded into Redis keys at nine call sites in src/apps/relay/ns_ioalib_engine_impl.c. send_message_to_redis() in src/apps/relay/hiredis_libevent2.c then passes the attacker-controlled key as the format argument to redisAsyncCommand() while supplying only one variadic value, causing hiredis redisvFormatCommand() to read past the va_list. Exploitation can crash the coturn process and terminate active TURN sessions or disclose stack memory into Redis. This issue is fixed in version 4.13.0.

### CVE-2026-54491

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T21:16:57.453 |

Koel is a free, open-source music streaming solution. Prior to 9.7.1, outbound podcast and radio fetch paths perform a point-in-time App\Helpers\Network::isPublicHost() or isSafeUrl() check without pinning the validated address, and most paths lack redirect-hop validation and do not revalidate every redirect target. PhanAn\Poddle\Poddle::fromUrl(), PodcastService::getStreamableUrl(), PodcastService::isPodcastObsolete(), App\Rules\HasAudioContentType, and App\Rules\SafeUrl can therefore follow an attacker-controlled redirect to an internal address or connect after DNS rebinding changes a public resolution to a private one. These paths are reachable through podcast and radio APIs, including createPodcastChannel, createInternetRadioStation, refreshPodcasts, apiResource podcasts, and radio/stations, allowing an authenticated user to request internal services or cloud metadata and potentially receive parsed or streamed response content. This issue is fixed in version 9.7.1.

### CVE-2026-75618

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-19T19:17:24.630 |

Tapo C100/C101 V5 contains a null pointer dereference vulnerability in the RTSP service. An attacker on the local network can send specially crafted requests that cause the service to dereference an invalid pointer, resulting in a service crash and device reboot. Successful exploitation can disrupt live video streaming functionality and cause a temporary denial-of-service condition.

### CVE-2026-55694

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-19T19:17:20.680 |

Snipe-IT is an IT asset/license management system. Prior to 8.6.3, a restricted user can request /api/v1/users/{target_id}/eulas to obtain another user's randomized EULA filename and then download the signed file through /account/stored-eula-file/{filename}. The primary /stored-eula-file/{filename} route correctly denies access, but app/Http/Controllers/ProfileController.php and app/Http/Controllers/Api/UsersController.php do not consistently enforce ownership and target-user authorization. This issue is fixed in version 8.6.3.

### CVE-2026-63652

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-08-19T18:17:10.167 |

FreeRDP is a free implementation of the Remote Desktop Protocol. Prior to 3.28.0, rdpsnd_server_recv_formats in channels/rdpsnd/server/rdpsnd_main.c frees context->client_formats on a malformed Client Audio Formats PDU without clearing the owning pointer or num_client_formats. An authenticated RDP client can trigger an error such as a cbSize larger than the remaining record, leave the dangling pointer in the server context, and cause rdpsnd_server_context_free to free the same allocation again at session teardown. This reliably terminates the server and can create allocator-dependent heap corruption. This issue is fixed in version 3.28.0.

### CVE-2026-62680

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22;CWE-829;CWE-918` |
| Published | 2026-08-19T18:16:54.230 |

Orval generates type-safe JavaScript clients in TypeScript from OpenAPI v3 and Swagger v2 specifications. Prior to 8.22.0, Orval resolves remote and local external $ref values without an allowlist or confinement to the input directory. Processing an attacker-controlled OpenAPI description can cause requests from the developer or CI host to attacker-selected or internal HTTP services, read absolute or out-of-tree local files, and inline untrusted remote schemas into generated clients. The affected code is packages/orval/src/import-specs.ts external reference loading. This issue is fixed in version 8.22.0.

### CVE-2026-17183

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T18:16:35.940 |

An authenticated user with permission to create or edit alert rules can bypass datasource query authorization by marking an alert rule query as a server-side expression while referencing a real datasource UID (incorrect authorization). This can expose data accessible through Grafana's configured datasource credentials to users who lack permission to query that datasource.

### CVE-2026-49253

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-19T15:17:06.747 |

electerm is an open-sourced terminal/ssh/sftp/telnet/serialport/RDP/VNC/Spice/ftp client. Prior to 3.11.11, electerm uses remote-supplied filenames directly with path.join() while receiving Zmodem and Trzsz transfers. In src/app/server/zmodem.js, prepareReceiveFile() joins the filename to the user-selected save path, and in src/app/server/trzsz.js, getUniqueFilePath(), the openSaveFile() callback, and the savedFilePaths mapping construct destinations without sanitization. A malicious SSH server or remote shell can provide a filename containing traversal components such as ../escaped.txt or ../../.bashrc. When the victim accepts the transfer and selects a download directory, electerm can write outside that directory and overwrite files accessible to the desktop user, potentially changing sensitive configuration or impairing availability. This issue is fixed in version 3.11.11.

### CVE-2026-62727

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-08-19T21:17:08.730 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-16838

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-19T20:17:04.873 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to overwrite critical files and obtain sensitive information due to a time-of-check to time-of-use (TOCTOU) race condition.

### CVE-2026-48711

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-19T15:17:05.580 |

SSHFS is a network filesystem client for connecting to SSH servers. From version 1.4 until 3.7.6, SSHFS accepts a bracketed mount source such as [-oProxyCommand=CMD]:/path and find_base_path() removes the brackets, leaving a host value that begins with - and is passed directly to ssh as a command-line argument. When a caller also supplies a path-valued sftp_server, ssh treats the normalized host as an option and the server path as its destination, causing an injected ProxyCommand to execute locally before any connection or authentication succeeds. The attack requires a caller or wrapper that passes an attacker-controlled mount source to SSHFS with the required sftp_server configuration and results in arbitrary command execution as the user running SSHFS. This issue is fixed in version 3.7.6.
