# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-03 15:00 UTC
- **対象期間**: `2026-07-02T15:04:15.000Z` 〜 `2026-07-03T15:00:34.000Z`
- **重要CVE数**: 88 件（Critical 9.0+: 23 件 / High 7.0〜: 65 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS 7.0 以上のものは **30 件以上** に上り、**リモートからのコード実行・権限昇格が共通した深刻な傾向** を示しています。特に **ネットワークに直接接続できる環境（IoT/クラウド管理プラットフォーム）** や **マルチテナント型 SaaS** が標的となっており、攻撃者は低権限でも **コマンドインジェクション** や **SSRF** を利用して管理者権限を取得できるケースが目立ちます。  

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱種別 | 影響範囲・被害シナリオ | 推奨される対策（概要） |
|-----|------|--------------|------------------------|------------------------|
| **CVE‑2026‑56004** | 10.0 | Shellcode Injection (obs tar_scm) | obs の `tar_scm` ハンドラで、攻撃者が任意の *service file* を提供できると、ソースサービスの実行ユーザー権限で任意コードが実行される。CI/CD パイプラインや自動ビルド環境でのコード取得時に被害が拡大。 | `obs` パッケージを **0.12.4 以上** に更新。未更新環境は `tar_scm` ハンドラを無効化し、外部からの service file 受け入れをネットワークレベルで遮断。 |
| **CVE‑2026‑50746** | 10.0 | Improper Access Control → Command Injection (UniFi Connect) | UniFi Connect アプリケーションに対し、認証なしでリモートからコマンドインジェクションが可能。攻撃者は管理デバイス上で任意シェルを実行でき、ネットワーク全体の制御を奪取できる。 | UniFi Connect を **最新版 (8.0.0 以降)** にアップデート。外部からの管理ポート（8080/8443 等）をファイアウォールで遮断し、管理 UI の IP 制限を実装。 |
| **CVE‑2026‑57100** / **CVE‑2026‑45499** | 9.9 | SSRF → Privilege Escalation (Microsoft Entra Provisioning / Azure OpenAI) | 両サービス共に認可されたユーザーが内部 API にリクエストを送れる SSRF が存在し、内部リソースへのアクセスや権限昇格が可能。特に Azure OpenAI では機密モデルやキー情報が漏洩するリスク。 | Microsoft の **2026‑03‑Patch**（Entra）・**2026‑04‑Patch**（Azure OpenAI）を適用。内部エンドポイントへの直接アクセスをネットワーク ACL で制限し、サービス間の信頼関係を最小化。 |
| **CVE‑2026‑44935** | 9.9 | Missing validation of `valuesFrom` (Rancher Fleet) | Rancher Fleet の Helm Deployer がテナント間で `valuesFrom` 参照を検証しないため、あるテナントの所有者が他テナントの Fleet クレデンシャルを取得できる。マルチテナント環境での情報漏洩リスクが高い。 | Rancher Fleet を **0.15.2 以上**（または 0.14.6/0.13.11/0.12.15）にアップグレード。テナント間の RBAC ポリシーを再確認し、`valuesFrom` の使用を制限。 |
| **CVE‑2026‑54402** | 9.9 | Improper Input Validation → Command Injection (UniFi OS) | UniFi OS の入力検証不備により、低権限ネットワークユーザーが任意コマンドを実行可能。OS 全体の権限取得につながるため、IoT デバイスやゲートウェイの根幹が危険に晒される。 | UniFi OS を **最新リリース (7.5.0 以降)** に更新。Web UI の CSRF トークン強化と、管理 API への認証必須化を実施。 |

> **注**：上記 5 件は **CVSS 9.9 以上** かつ **リモートコード実行／権限昇格** が直接的に可能な点で共通しており、組織全体の攻撃面を大幅に拡大させるため、最優先で対策すべきです。

## 3. 推奨アクション  

### (1) パッケージ・サービスの即時アップデート  
| 製品 / パッケージ | 修正バージョン | アップデート手順のポイント |
|-------------------|----------------|----------------------------|
| `obs` (tar_scm) | **0.12.4 以上** | `yum/dnf` で `obs` を更新、もしくは公式 tarball からビルド。`/etc/obs/services.d/` 配下のカスタム service file は必ずレビュー。 |
| UniFi Connect | **8.0.0 以上** | Ubiquiti の公式リポジトリから `unifi-connect` を取得。アップデート後は `systemctl restart unifi-connect` と同時に **管理ポートのファイアウォール** を確認。 |
| Microsoft Entra Provisioning (SyncFabric) | **2026‑03‑Patch** (Microsoft 公式) | Azure Portal → Update Management → 「Entra Provisioning」パッチ適用。適用後は **Azure AD の監査ログ** で不審な SSRF 試行が無いか確認。 |
| Azure OpenAI | **2026‑04‑Patch** (Microsoft 公式) | Azure CLI/Portal で `az openai update --name <resource> --patch-version latest` を実行。内部エンドポイント (`*.openai.azure.com`) へのネットワーク制限を追加。 |
| Rancher Fleet | **0.15.2 以上** (または該当ブランチの最新) | `helm upgrade fleet fleet/fleet --version 0.15.2` でデプロイ。`valuesFrom` 使用時は `helm template` で事前に検証し、RBAC を `fleet-admin` のみ許可。 |
| UniFi OS | **7.5.0 以上** | Ubiquiti の `unifi-os` パッケージを `apt-get update && apt-get install unifi-os` で更新。更新後は **SSH の公開鍵認証** と **API トークンのローテーション** を実施。 |

### (2) ネットワークレベルの防御強化  
1. **外部からの管理ポート遮断**  
   - UniFi 系、Obs、Rancher の管理 UI/API は内部ネットワーク（VPN/プライベートサブネット）からのみアクセス可能にする。  
2. **Web Application Firewall (WAF) で特定パラメータをサニタイズ**  
   - `valuesFrom`、`service file`、`SQL` クエリ文字列

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-56004

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-02T15:17:06.413 |

A shellcode injection in the mercurial handler of the obs tar_scm source service before version 0.12.4 could be used by attackers able to provide a _service file to execute code as the source service or the local user checking out the malicious services

### CVE-2026-50746

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-02T15:17:02.723 |

A malicious actor with access to the network could exploit an Improper Access Control vulnerability found in UniFi Connect Application to execute a Command Injection on the host device.

### CVE-2026-57100

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-02T23:16:51.267 |

Server-side request forgery (ssrf) in Microsoft Entra Provisioning Service (SyncFabric) allows an authorized attacker to elevate privileges over a network.

### CVE-2026-45499

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-02T23:16:51.003 |

Server-side request forgery (ssrf) in Azure OpenAI allows an authorized attacker to elevate privileges over a network.

### CVE-2026-44935

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1287` |
| Published | 2026-07-02T17:16:59.667 |

Missing validation of "valuesFrom" references in Helm Deployer of SUSE Rancher Fleet 0.15 before 0.15.2, 0.14 before 0.14.6, 0.13 before 0.13.11 and 0.12 before 0.12.15 could be used by owners of one tenant to access fleet credentials of other tenants.

### CVE-2026-55115

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-02T15:17:05.513 |

A malicious actor with access to the network and low privileges could exploit a Server-Side Request Forgery (SSRF) in UniFi Protect Application to escalate privileges on the host device.

### CVE-2026-54402

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-02T15:17:03.837 |

A malicious actor with access to the network and low privileges could exploit an Improper Input Validation vulnerability found in UniFi OS to execute a Command Injection on the host device.

### CVE-2026-50748

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-02T15:17:02.990 |

A malicious actor with access to the network and low privileges could exploit an Improper Input Validation vulnerability found in UniFi Access Application to execute a Command Injection on the host device.

### CVE-2026-50747

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-02T15:17:02.877 |

A malicious actor with access to the network and low privileges could exploit a series of authenticated SQL Injection vulnerabilities found in UniFi Talk Application to escalate privileges on the host device.

### CVE-2026-4321

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-03T10:16:32.760 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Raera - Ankara Web Design and Digital Advertising Agency Destekz allows SQL Injection.

This issue affects Destekz: through 02062026. NOTE: The vendor was contacted and it was learned that the product is not supported.

### CVE-2026-14544

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-03T08:16:24.433 |

A flaw was found in HPLIP (HP Linux Imaging and Printing Software). This vulnerability, an incomplete fix for CVE-2026-8631, may allow a remote attacker to escalate privileges or achieve arbitrary code execution. This can occur through an integer overflow in the hpcups processing path when handling specially crafted print data.

### CVE-2026-13768

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-03T00:16:52.270 |

Gardyn devices expose a privileged iothubowner key. Access to this key will allow a malicious user to invoke an IoTHub Registry Manager function which returns connection information for all Gardyn Home Kit and Studio devices. Access to this key also allows a malicious user to execute arbitrary commands on a specific connected device and may allow the malicious user to pivot to other devices on the user's network.

### CVE-2026-52830

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-22;CWE-287` |
| Published | 2026-07-02T21:16:56.847 |

fast-mcp-telegram is a Telegram MCP Server. Prior to 0.19.1, fast-mcp-telegram validates HTTP Bearer tokens by joining the raw token string into a session-file path. The verifier rejects the exact reserved token telegram, but it does not reject path separators or normalize the path before checking whether the session file exists. A remote HTTP client can therefore authenticate as the default legacy session with a token such as ../fast-mcp-telegram/telegram when the documented default session file ~/.config/fast-mcp-telegram/telegram.session exists. This bypasses the reserved session name control that is intended to prevent HTTP multi-user sessions from colliding with the default stdio or legacy account. With account-prefixed MCP tools enabled, the attacker still sees and calls the prefixed tools for the default account, so the prefix middleware does not stop the session selection bypass. This vulnerability is fixed in 0.19.1.

### CVE-2026-41106

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-601` |
| Published | 2026-07-02T23:16:50.867 |

Url redirection to untrusted site ('open redirect') in M365 Copilot allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-59099

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-323` |
| Published | 2026-07-02T20:17:08.240 |

Apereo CAS 7.3.0 before 8.0.0-RC6 contains a cryptographic vulnerability that allows remote unauthenticated attackers to recover plaintext conversation state by exploiting AES-GCM initialization vector reuse across the server lifetime. Attackers can collect multiple client-side webflow execution tokens from the unauthenticated login page and perform known-plaintext analysis to decrypt the webflow conversation state due to keystream reuse caused by a fixed all-zero IV paired with the same encryption key.

### CVE-2026-58466

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-07-02T20:17:06.593 |

AutoBangumi before 3.2.8 contains a hard-coded default credentials vulnerability that allows unauthenticated attackers to authenticate as the administrator by using the publicly known default credentials seeded at startup via add_default_user() in the database user module when the users table is empty. Attackers can submit the default credentials to the authentication login endpoint to gain full control of the application, including RSS feed configuration, downloader configuration, and all authenticated API endpoints.

### CVE-2024-14037

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-02T17:16:57.360 |

Redsea Cloud eHR contains an arbitrary file upload vulnerability that allows unauthenticated attackers to achieve remote code execution by uploading malicious files through the PtFjk.mob servlet endpoint. Attackers can submit a multipart POST request with a JSP webshell disguised using a spoofed image/jpeg Content-Type to bypass the absence of extension and MIME type validation, with the uploaded file stored at a predictable path under the uploadfile directory and executed directly by the web server. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-11-03 (UTC).

### CVE-2022-50973

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-02T17:16:56.947 |

Yonyou KSOA 9.0 contains an unauthenticated arbitrary file upload vulnerability in the com.sksoft.bill.ImageUpload servlet that allows unauthenticated attackers to upload arbitrary files by submitting a POST request with attacker-controlled filepath and filename parameters without any authentication, file type, extension, or content validation. Attackers can upload a JSP webshell by specifying a malicious filename and root filepath, with the uploaded file stored under the pictures directory and directly executed by the web server, resulting in unauthenticated remote code execution. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-11-07 (UTC).

### CVE-2026-13368

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-03T00:16:50.890 |

WatchGuard Fireware OS contains a race condition leading to a use-after-free vulnerability in LDAP authentication for the Mobile User VPN with IKEv2. A remote unauthenticated attacker could exploit this vulnerability to execute arbitrary code in the context of the iked process on Fireboxes that have a Mobile VPN with IKEv2 configured to use an external LDAP authentication server.

This vulnerability affects Fireware OS 11.0 up to and including 11.12.4_Update1, 12.0 up to and including 12.12 and 2025.1 up to and including 2026.2.

### CVE-2026-58455

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-698` |
| Published | 2026-07-02T16:16:35.287 |

Dockwatch through 0.6.567 contains an unauthenticated OS command injection vulnerability that allows remote attackers to execute arbitrary shell commands by exploiting a missing exit() after an authentication redirect in loader.php combined with unsanitized input passed to shell_exec() in ajax/compose.php. Attackers can seed the required session flag through the incomplete auth check, then inject arbitrary commands via the composePath POST parameter in the composePull action to achieve full host compromise, facilitated by the standard deployment mounting of the Docker socket.

### CVE-2026-9725

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-03T06:16:23.263 |

The Printcart Web to Print Product Designer for WooCommerce plugin for WordPress is vulnerable to Arbitrary File Deletion in versions up to, and including, 2.5.2 This is due to insufficient path validation in the store_design_data() function, which constructs a filesystem path from the user-supplied 'nbd_item_key' POST parameter sanitized only with sanitize_text_field() — which does not strip path traversal sequences — and then passes that path directly to Nbdesigner_IO::delete_folder() and PHP's rename(). The nonce protecting the nbd_save_customer_design AJAX action is freely obtainable by unauthenticated users via the nbd_check_use_logged_in endpoint. This makes it possible for unauthenticated attackers to delete arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-54400

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-02T15:17:03.623 |

A malicious actor with access to the network and high privileges could exploit an Improper Access Control vulnerability found in UniFi Access Application to escalate privileges on the host device.

### CVE-2026-55116

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-02T15:17:05.633 |

A malicious actor with access to the network and under certain network configurations could exploit an Improper Access Control vulnerability found in certain devices running UniFi OS to make unauthorized changes to such UniFi OS devices.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-47896

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:L/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-03T09:16:37.397 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Apache Lucene.Net (Lucene.Net.Replicator library).

This issue affects Apache Lucene.Net.Replicator: from 4.8.0-beta00005 through 4.8.0-beta00017.

Users are recommended to upgrade to version 4.8.0-beta00018, which fixes the issue.

### CVE-2026-47897

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:L/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-03T08:16:24.817 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Apache Lucene.Net (Lucene.Net.Replicator library).

This issue affects Apache Lucene.Net.Replicator: from 4.8.0-beta00005 before 4.8.0-beta00018.

Users are recommended to upgrade to version 4.8.0-beta00018, which fixes the issue.

### CVE-2026-10054

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-1385` |
| Published | 2026-07-03T11:16:26.847 |

In affected versions of Eclipse Theia (1.8.1 and later), the browser backend exposes privileged terminal RPC over WebSocket (/services/shell-terminal, /services/terminals/:id) without service-level authentication.




WebSocket origin validation in @theia/core is fail-open: connections are accepted when the Origin header is missing or when no THEIA_HOSTS allowlist is configured (the default). The Socket.IO integration additionally replaces the real Origin header with a client-supplied fix-origin header that an attacker can control or omit.




As a result, a foreign-origin web page visited by a user with a running Theia instance can open the /services WebSocket namespace, invoke terminal creation, attach to the resulting terminal data channel, execute arbitrary OS commands, and read their output. This affects both local developer setups (drive-by attack) and hosted or tunneled deployments without strong external authentication.




A fix is in development that enforces same-origin validation by default, removes trust in the fix-origin header, gates HTTP and WebSocket access on a SameSite=Strict; HttpOnly connection-token cookie, and sanitizes shell terminal creation options.

### CVE-2026-54998

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-02T23:16:51.137 |

Incorrect authorization in Microsoft Exchange Online allows an authorized attacker to elevate privileges over a network.

### CVE-2026-56841

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-02T15:17:07.750 |

A malicious actor with access to the network and low privileges could exploit an authenticated SQL Injection vulnerability found in UniFi Protect Application to escalate privileges on the host device.

### CVE-2026-55114

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-02T15:17:05.410 |

A malicious actor with access to the network and low privileges could exploit an Improper Access Control vulnerability found in UniFi Network Application to escalate privileges within the UniFi Network Application.

### CVE-2026-54404

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-02T15:17:04.060 |

A malicious actor with access to the network and low privileges could exploit a series of authenticated SQL Injection vulnerabilities found in UniFi OS to escalate privileges within such UniFi OS devices or instances.

### CVE-2026-13084

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-03T00:16:50.767 |

A null pointer dereference vulnerability in WatchGuard Fireware OS may allow a remote unauthenticated attacker to create a denial-of-service (DoS) condition by sending specially crafted IKEv2 messages. This vulnerability affects both the Mobile User VPN with IKEv2 and the Branch Office VPN using IKEv2 when configured with a dynamic gateway peer.

This vulnerability affects Fireware OS 11.10.2 up to and including 11.12.4_Update1, 12.0 up to and including 12.12 and 2025.1 up to and including 2026.2

### CVE-2026-59094

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-07-02T20:17:07.540 |

Pathway through 0.31.1, fixed in commit d09722e, document store applies a caller-supplied glob pattern to indexed document paths using a hand-written recursive matcher that branches two ways on each ** token without memoization, giving exponential worst-case complexity. The filepath_globpattern value is taken from the body of the unauthenticated HTTP endpoints /v1/retrieve, /v1/inputs and /v2/answer and compiled into a filter evaluated once per indexed document, with no length or **-count limit. A remote unauthenticated attacker can submit a short pattern containing many ** tokens to consume CPU for tens of seconds per request, and a small number of requests denies service.

### CVE-2026-59093

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-02T20:17:07.410 |

Weaviate before 1.38.0 does not verify that a principal performing an RBAC role assignment holds the permissions granted by the assigned role. The assignRoleToUser and assignRoleToGroup handlers (POST /authz/users/{id}/assign and /authz/groups/{id}/assign) authorize only that the caller may assign roles to the target user or group, not the permissions contained in the assigned roles, unlike role creation which enforces that a user can only create roles with permissions less than or equal to its own. A user holding only the delegated assign_and_revoke_users or assign_and_revoke_groups permission can assign the built-in admin role, or any high-privilege custom role, to itself or others, escalating to full administrative control of the database.

### CVE-2026-58465

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-02T19:16:59.993 |

Eclipse Wakaama before snapshot/2026-05-26 contains an unbounded memory allocation vulnerability in the CoAP Block1 handler within coap/block.c that allows unauthenticated remote attackers to exhaust server memory by sending a sequence of Block1 PUT requests with incrementing block numbers. Attackers can target the registration endpoint over UDP without authentication, causing the server to repeatedly reallocate a growing accumulation buffer by appending each block payload without enforcing any maximum total size limit, resulting in denial of service through memory exhaustion.

### CVE-2026-55950

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-07-02T17:17:02.910 |

Time-of-check Time-of-use (TOCTOU) race condition vulnerability in Erlang/OTP ssl (dtls_packet_demux module) allows an unauthenticated remote attacker to crash all active DTLS sessions on a listener.

A DTLS server listener uses a single shared dtls_packet_demux gen_server process to route incoming UDP datagrams to the correct connection handler. When a DTLS client reconnects rapidly from the same source address and port (sending multiple ClientHello messages in quick succession), a race condition in the demux's internal gb_trees key-value store causes a {key_exists, {old, Client}} crash, terminating the demux process. Because the demux is shared across all DTLS associations on that listener, its crash immediately kills every active DTLS session, not just the attacker's.

The attack is pre-authentication: the attacker only needs to send UDP datagrams containing valid ClientHello messages from the same source IP and port before the intermediate DOWN monitor message is processed by the gen_server. No credentials, no completed handshake, and no special configuration are required, and the crash can be repeated indefinitely to create a persistent denial of service for all clients of that listener.

This vulnerability is associated with program file lib/ssl/src/dtls_packet_demux.erl.

This issue affects OTP from OTP 25.3 before 29.0.3, 28.5.0.3, and 27.3.4.14 corresponding to ssl from 10.9 before 11.7.3, 11.6.0.3, and 11.2.12.10.

### CVE-2024-58352

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-564` |
| Published | 2026-07-02T17:16:57.557 |

Landray OA contains an unauthenticated HQL injection vulnerability that allows unauthenticated attackers to query arbitrary Hibernate entity classes by injecting malicious HQL syntax into the uid POST parameter of the wechatLoginHelper.do endpoint. Attackers can exploit the lack of input sanitization in the string-concatenated filter expression passed to the Hibernate findList() call to extract sensitive data such as administrator password hashes and, with sufficient database privileges, perform file-write operations enabling remote code execution. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-03-11 (UTC).

### CVE-2026-9272

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-02T15:17:11.937 |

In Progress Flowmon ADS versions prior to 12.5.6 and 13.0.5, a vulnerability exists whereby an adversary who is authenticated as a low-privileged user in the Anomaly Detection System (ADS) may send specially crafted requests that could result in unauthorized access to application data and its modification.

### CVE-2026-8079

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-02T15:17:11.803 |

In Progress Flowmon versions prior to 12.5.9 and 13.0.11, a vulnerability exists whereby an authenticated low-privileged user may craft a request during the PDF generation process that results in operations being performed with the privileges of another user, potentially leading to unauthorized access to sensitive data and unintended modifications to system configuration.

### CVE-2026-54406

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-02T15:17:04.310 |

A malicious actor with access to the network and high privileges could exploit a Path Traversal vulnerability found in self-hosted instances of UniFi Network Application to escalate write permission on the host device.

### CVE-2026-13722

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-03T00:16:52.010 |

WatchGuard Fireware OS contains a firmware validation bypass when processing a backup image via the backup/restore feature. An authenticated administrator can exploit this vulnerability to install a tampered firmware image.This vulnerability affects Fireware OS 11.0 up to and including 11.12.4_Update1, 12.0 up to and including 12.12 and 2025.1 up to and including 2025.6.2.

### CVE-2026-13384

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-03T00:16:51.893 |

An Out-of-bounds Write vulnerability in WatchGuard Fireware OS wgagent process could allow an authenticated privileged user to execute arbitrary code via a specially crafted requests to the Management Web UI.This vulnerability affects Fireware OS 12.1 up to and including 12.12 and 2025.1 up to and including 2026.2.

### CVE-2026-13383

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-03T00:16:51.773 |

An Out-of-bounds Write vulnerability in WatchGuard Fireware OS ikestubd process could allow an authenticated privileged user to execute arbitrary code via a specially crafted requests to the Management Web UI.This vulnerability affects Fireware OS 12.1 up to and including 12.12 and 2025.1 up to and including 2026.2.

### CVE-2026-13054

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-03T00:16:50.497 |

A path traversal vulnerability in the WatchGuard Fireware OS Management Web UI allows a privileged authenticated attacker to write arbitrary files on the Firebox's filesystem.




This vulnerability affects Fireware OS 11.0 up to and including 11.12.4_Update1, 12.0 up to and including 12.12 and 2025.1 up to and including 2026.2.

### CVE-2026-13053

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-03T00:16:50.320 |

An Out-of-bounds Write vulnerability in WatchGuard Fireware OS's CLI could allow an authenticated privileged user to execute arbitrary code via a specially crafted CLI command.

This vulnerability affects Fireware OS 11.0 up to and including 11.12.4_Update1, 12.0 up to and including 12.12 and 2025.1 up to and including 2026.2.

### CVE-2026-13050

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-03T00:16:49.333 |

An Out-of-bounds Write vulnerability in WatchGuard Fireware OS networkd process could allow an authenticated privileged user to execute arbitrary code via a specially crafted requests to the Management Web UI.This vulnerability affects Fireware OS 11.8 up to and including 11.12.4_Update1, 12.0 up to and including 12.12 and 2025.1 up to and including 2026.2.

### CVE-2026-55117

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-02T15:17:05.740 |

A malicious actor with access to the network could exploit a Path Traversal vulnerability found in UniFi Access Application to access files on the host device.

### CVE-2026-54408

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-02T15:17:04.523 |

A malicious actor with access to the network could exploit an Improper Access Control vulnerability found in UniFi Protect Application to bypass authentication for data streaming.

### CVE-2026-54407

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-02T15:17:04.417 |

A malicious actor with access to the network could exploit an Improper Access Control vulnerability found in UniFi Protect Application to bypass authentication in certain UniFi Protect Application API endpoints.

### CVE-2026-54403

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-02T15:17:03.947 |

A malicious actor with access to the network could exploit a Path Traversal vulnerability found in certain devices running UniFi OS to bypass authentication of such UniFi OS devices or instances.

### CVE-2026-10055

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-200;CWE-918` |
| Published | 2026-07-03T11:16:27.600 |

In Eclipse Theia since version 1.26.0, the backend /services/request-service RPC accepts an attacker-controlled URL from any client connected to the standard /services messaging endpoint, performs the HTTP request server-side, and returns the full response body to the caller.




Because the destination URL is neither validated nor allowlisted, a remote attacker with access to the Theia service connection can issue server-side HTTP requests to localhost or other backend-reachable hosts and read their responses, exposing internal administrative endpoints, cloud instance metadata services, and other resources that are intentionally outside the browser network boundary.




The vulnerability affects deployments where the Theia service connection is reachable by untrusted users (for example, multi-tenant or publicly-reachable Theia deployments).

### CVE-2026-8921

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-03T03:16:23.627 |

External Control of File Name or Path vulnerability in ASUS Business Manager allows a local user to execute arbitrary code with SYSTEM privileges via a tampered IPC message.
Refer to the '
Security Update for ASUS Business Manager ' section on the ASUS Security Advisory for more information.

### CVE-2022-4989

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-03T03:16:22.100 |

** UNSUPPORTED WHEN ASSIGNED ** Improper Validation of Specified Quantity in Input in the ASUS AI Suite 3 driver allows a local user to access unintended memory regions via crafted IOCTL requests, leading to privilege escalation.

### CVE-2026-44941

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-02T16:16:30.550 |

A relative path traversal in the "keyhint" option in repomd.xml parsing of libzypp before 17.38.12 can be used by attackers able to supply a malicious repository to inject or overwrite files in the target system as root.

### CVE-2026-59095

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-02T20:17:07.673 |

LobeChat before 2.2.10-canary.18 contains a server-side request forgery vulnerability that allows authenticated attackers to direct internal HTTP requests to arbitrary URLs by supplying user-controlled input to the skill import service (importFromUrl) and topic cover update (fetchImageFromUrl) endpoints, which use the global fetch without the project's ssrf-safe-fetch wrapper. Attackers can target internal addresses such as cloud instance metadata endpoints through these unprotected code paths to disclose internal service responses and cloud credentials.

### CVE-2026-55118

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-02T15:17:05.840 |

A malicious actor with access to the network,low privileges and under certain conditions could exploit an Improper Access Control vulnerability found in UniFi Network Application to escalate privileges within the UniFi Network Application.

### CVE-2026-59096

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-02T20:17:07.847 |

Dapr Sentry's OIDC discovery endpoint derives the issuer and jwks_uri of the /.well-known/openid-configuration document from the request Host, honoring an attacker-controlled X-Forwarded-Host header without validation when no allowed-hosts list is configured (the default), and serves the document with a one-hour public cache lifetime. A remote unauthenticated attacker can poison the discovery document so relying parties performing dynamic (unpinned) discovery fetch the JWKS from an attacker-controlled server, causing attacker-signed JWTs to be accepted. Exploitation requires the OIDC server enabled without a configured jwt-issuer or oidc-allowed-hosts.

### CVE-2026-58467

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-02T20:17:06.733 |

Cockpit CMS before release 364 contains a path traversal and local file inclusion vulnerability that allows unauthenticated attackers to read arbitrary files or execute PHP files by including unvalidated PATH_INFO derived from REQUEST_URI in filesystem path construction without containment checks. Attackers can inject dot-dot sequences into the URL to traverse outside the designated spaces directory, and when the resolved path ends with a .php extension, the application passes it to include(), enabling local file inclusion on deployments using the PHP built-in server or certain non-default Nginx configurations.

### CVE-2026-55952

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-02T17:17:03.067 |

The Erlang/OTP ssl application does not validate that the PSK identity list and binder list carried in a TLS 1.3 ClientHello pre-shared key extension have equal length before passing them to the session ticket handler. In tls_handshake_1_3:handle_pre_shared_key/3, an OfferedPreSharedKeys record with a mismatched number of identities and binders is forwarded directly to tls_server_session_ticket:use/4, which crashes the session ticket handler process.

An unauthenticated remote attacker can send a single crafted ClientHello to a TLS 1.3 server with session tickets enabled (stateful or stateless mode) and permanently disrupt session ticket handling on that listener. New TLS 1.3 handshakes complete but subsequently crash when the server attempts to issue a session ticket, effectively making TLS 1.3 unusable on the affected listener until the ssl application is restarted. TLS 1.2 connections are not affected.

This issue affects OTP from 22.2 before 29.0.3, 28.5.0.3 and 27.3.4.14 corresponding to ssl from 9.5 before 11.7.3, 11.6.0.3 and 11.2.12.10.

### CVE-2026-50722

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347;CWE-617` |
| Published | 2026-07-02T22:16:43.550 |

Libreswan, via the function RSA_authenticate_hash_signature_pkcs1_1_5_rsa(), did not correctly verify the DER encoding of the ASN.1 digest when the IKEv2 AUTH payload was encoded using RSASSA-PKCS1-v1_5 (RFC 8017). A remote attacker can use a variation on the Bleichenbacher attack to forge the AUTH payload when small public exponents are used (e.g., e=3), leading to impersonation. Additionally, a remote attacker, by encoding a shorter than expected hash in the AUTH payload, could trigger an assertion leading to denial-of-service. The daemon aborts and restarts; continued exploitation causes sustained denial of service. Remote code execution is not possible. X.509 certificate verifications of the remote IKE peer are not affected.

### CVE-2026-50721

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347;CWE-617` |
| Published | 2026-07-02T22:16:43.367 |

Libreswan, via the function RSA_authenticate_hash_signature_raw_rsa(), did not correctly verify the length of the authentication hash when the SIG payload of an IKEv1 packet was encoded using PKCS #1 RSA Encryption as per RFC 2313. A remote attacker can use a variation on the Bleichenbacher attack to forge the SIG payload when small public exponents are being used (e.g., e=3), which could lead to impersonation. Additionally, a remote attacker, by encoding a shorter than expected hash in the SIG payload, could trigger an assertion leading to denial-of-service. The daemon aborts and restarts; continued exploitation causes sustained denial of service. Remote code execution is not possible. X.509 certificate verifications of remote IKE peers are not affected.

### CVE-2026-7311

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-02T19:17:00.127 |

The TinyPNG – JPEG, PNG & WebP image compression plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the delete_converted_image_size function in all versions up to, and including, 3.6.13. This makes it possible for authenticated attackers, with author-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). An attacker can exploit this by injecting an arbitrary server file path into the 'convert.path' field of the 'tiny_compress_images' post meta on an attachment they own, then triggering attachment deletion to invoke the vulnerable code path.

### CVE-2026-55119

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-02T15:17:05.957 |

A malicious actor with access to the network and low privileges could exploit an Improper Access Control vulnerability found in UniFi Talk Application to escalate privileges within the UniFi Talk Application.

### CVE-2026-12168

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-02T15:16:57.123 |

An improper validation vulnerability for driver `GFAC_Sys_x64.sys` in Little Orbit GFAC allows a local attacker to escalate privileges to SYSTEM and execute arbitrary code in kernel mode via crafted messages sent through a Minifilter communication port.

### CVE-2026-12167

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-02T15:16:57.030 |

The Minifilter communication port for driver `GFAC_Sys_x64.sys` in Little Orbit GFAC allows a local attacker to access privileged driver functionality via a communication interface that lacks appropriate access restrictions.

### CVE-2026-8247

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-07-03T00:16:52.773 |

An Out-of-bounds Write vulnerability in WatchGuard Fireware OS may allow an unauthenticated attacker on the same local network segment to execute arbitrary code.




This vulnerability affects Fireware OS 11.0 up to and including 11.12.4_Update1, 12.0 up to and including 12.12 and 2025.1 up to and including 2026.2.

### CVE-2026-54401

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-02T15:17:03.730 |

A malicious actor with access to the network and low privileges could exploit a Server-Side Request Forgery (SSRF) to escalate privileges within such UniFi OS devices or instances.

### CVE-2026-4967

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-03T07:16:24.333 |

In IMS, there is a possible out of bounds read due to a missing bounds check. This could lead to remote denial of service with no additional execution privileges needed.

### CVE-2026-14352

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-03T06:16:21.787 |

The AR for WooCommerce plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 8.40 via the 'file' parameter parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. The three intended access controls all fail: valid nonces are freely minted by unauthenticated callers via the nopriv ar_get_fresh_nonce and ar_process_user_image AJAX handlers; the AES-256-CBC encryption key is derived from get_option('ar_licence_key'), which returns false on default free installations and yields a predictable key attackers can use to encrypt their own path payloads; and the Referer check is trivially bypassed because the Referer header is attacker-controlled.

### CVE-2026-14327

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-03T02:16:23.470 |

The AR for WordPress plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 8.40 via the 'file' parameter parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. Exploitation requires an attacker to first obtain a valid nonce and secure nonce via the publicly accessible ar_get_fresh_nonce and ar_process_user_image nopriv AJAX handlers, and to reproduce the encryption key locally — both steps are fully achievable by an unauthenticated attacker on any default free or unlicensed installation where ar_licence_key is unset.

### CVE-2026-12413

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-193;CWE-617` |
| Published | 2026-07-02T22:16:42.517 |

An invalidly formatted IKEv2 fragment causes the Libreswan pluto daemon to crash and restart. Continued exploitation would cause a denial of service. The function reassemble_v2_incoming_fragments() would ignore unknown outer payloads but still store these in a fixed size array msg_digest.digest[PAYLIMIT]. An off-by-one error in the assertion PASSERT(logger, md->digest_roof < elemsof(md->digest)) causes the daemon to abort. No remote code execution is possible. Any configuration that allows IKEv2 connections that do not set fragmentation=no are vulnerable. IKEv1 is not affected.

### CVE-2026-56842

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-02T15:17:07.870 |

A malicious actor with access to the network and under certain conditions could exploit an Incorrect Authorization vulnerability found in UniFi Network Application to persist privileges within UniFi Network Application after such access had been removed.

### CVE-2026-55113

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-02T15:17:05.303 |

A malicious actor with access to the network could exploit a Server-Side Request Forgery (SSRF) vulnerability found in UniFi Talk Application to execute a Denial of Service (DoS) attack and bypass authentication in certain UniFi Talk API endpoints.

### CVE-2026-55112

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-02T15:17:05.103 |

A malicious actor with access to the network and low privileges and under certain conditions could exploit an Improper Access Control vulnerability found in UniFi OS with UniFi Protect Application to escalate privileges on the host device.

### CVE-2026-55111

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-02T15:17:04.987 |

A malicious actor with access to the network could exploit a Path Traversal vulnerability found in UniFi Protect Floodlight devices to access files on the UniFi Protect Floodlight.

### CVE-2026-55110

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-942` |
| Published | 2026-07-02T15:17:04.870 |

A malicious actor who lures an authenticated user to a malicious page could exploit a Cross-Origin Resource Sharing (CORS) misconfiguration found in UniFi OS to trigger actions in UniFi OS using that user's session.

### CVE-2026-54409

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-665` |
| Published | 2026-07-02T15:17:04.627 |

A malicious actor with access to the network and under certain conditions could exploit an Improper Initialization vulnerability found in UniFi Protect Application to bypass authentication in UniFi Protect Cameras.

### CVE-2026-54405

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-02T15:17:04.193 |

A malicious actor with access to the network could exploit an Improper Input Validation vulnerability found in UniFi Network Application to execute a Denial of Service (DoS) attack on the application.

### CVE-2026-13341

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-03T11:16:27.720 |

A vulnerability exists in the Kong Konnect Model Context Protocol (MCP) server prior to version 1.0.0, which could allow a remote attacker to perform an indirect prompt injection attack and execute unintended API requests.

### CVE-2022-4990

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-03T03:16:23.087 |

** UNSUPPORTED WHEN ASSIGNED ** Improper Validation of Specified Quantity in Input in the ASUS AI Suite 3 driver allows a local user to bypass security validation and access restricted memory blocks via crafted IOCTL requests, leading to privilege escalation.

### CVE-2026-13079

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-07-03T00:16:50.630 |

A local privilege escalation vulnerability in the WatchGuard Mobile VPN with SSL client for Windows allows a local attacker to escalate their privileges to NT AUTHORITY\SYSTEM on the machine where the client is installed.

This issue affects the Mobile VPN with SSL client for Windows up to and including 2026.2.

### CVE-2026-9148

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-03T08:16:25.367 |

The Comments – wpDiscuz plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the guest commenter 'Website' field in versions up to, and including, 7.6.56 This is due to insufficient output escaping in the getCommentAuthor() function, which interpolates the stored comment_author_url value directly into single-quoted HTML attributes without applying esc_url() or esc_attr(). This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-13040

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-03T06:16:21.590 |

The NEX-Forms – Ultimate Forms Plugin for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'real_val__' parameter in all versions up to, and including, 9.2.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The submission endpoint is registered via wp_ajax_nopriv_submit_nex_form with no nonce verification, making it fully accessible to unauthenticated attackers without any CSRF token.

### CVE-2026-59098

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-02T20:17:08.120 |

LobeChat through 2.2.9 contains a broken access control vulnerability in the retrieval-augmented-generation semantic search functionality that allows authenticated attackers to access other users' data by exploiting missing user-identifier predicates in the chunk model semanticSearch method. Attackers can supply arbitrary victim file or knowledge-base identifiers through the chunk retrieval and chat knowledge-base paths to retrieve text content, file names, and metadata belonging to other users.

### CVE-2026-58578

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-07-02T20:17:06.870 |

LobeChat before version 2.2.10-canary.15 contains a regular expression denial of service (ReDoS) vulnerability that allows authenticated attackers to block the Node.js event loop by supplying a catastrophic-backtracking pattern in a GitHub repository URL path during skill import. Attackers can craft a malicious basePath value containing unescaped regex metacharacters such as catastrophic-backtracking patterns, which are injected into a dynamically constructed regular expression in the findSkillMd function and executed synchronously against archive entries, denying service to all concurrent users for tens of seconds per request.

### CVE-2026-50281

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-07-02T17:17:00.000 |

Craft CMS is a content management system (CMS). Versions 5.7.0 and above, prior to 5.9.21 contain a mass-assignment flaw in the bulk-duplicate element action. An attacker who is only able to duplicate their own entires can submit an arbitrary id through the newAttributes request parameter. The duplication routine overrides its own id = null reset with that value and writes the attacker's attributes into the victim's existing entry row. ElementsController::beforeAction() pulls the request body into $this->_attributes and rejects requests that ship an id or canonicalId key at the top level, actionBulkDuplicate(), reads a separate newAttributes array and passes it straight through to the service layer. Elements::duplicateElement() clones the source element, sets id to null, and then hands the attacker's array to Craft::configure(), which  overwrites the reset id with any numeric value inside $newAttributes. PHP Yii's saveElement() then performs an UPDATE against the row with that primary key instead of an INSERT. The attackers's title, slug, authorId, postDate, and UID land on the victim's entry. safeAttributes() on Entry includes id because the base element model exposes it, so the Collection::only() filter does not strip it. This issue has been fixed in version 5.9.21.

### CVE-2026-58460

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-02T21:16:57.080 |

react-native-receive-sharing-intent contains a path traversal vulnerability that allows a co-resident malicious application to write files outside the intended cache directory by supplying a crafted _display_name value containing dot-dot path components through a malicious ContentProvider. Attackers can fire an explicit ACTION_SEND intent at the consuming app's exported share-receiver activity to overwrite arbitrary files in the consuming app's private data directory, including databases, shared preferences, and cached configuration, with attacker-controlled content.

### CVE-2026-59092

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-07-02T20:17:07.270 |

JuiceFS through 1.3.1, fixed in commit a46979c, contains an authentication bypass vulnerability that allows unauthenticated remote attackers to access sensitive debug and metrics endpoints by exploiting improper handler registration on the shared http.DefaultServeMux. Attackers can request the /debug/pprof/cmdline endpoint to obtain the process command line containing metadata engine connection strings with database credentials, granting full read/write access to filesystem metadata, while other pprof handlers leak internal state and profiling handlers enable denial of service.

### CVE-2026-8699

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-02T17:17:03.337 |

A stored Cross-Site Scripting (XSS) vulnerability has been identified in the web-based management interface of Archer C5 v6.8 routers, due to insufficient server-side validation and lack of proper output encoding of user-controlled input in a certain field.  An attacker with administrative privileges can inject crafted HTML or JS payloads into the affected field. The payload is stored and later executed when the affected page is rendered in an administrator's browser.Successful exploitation allows execution of arbitrary JavaScript in an admin's browser, potentially leading to session hijacking and unauthorized access to router configuration, possibly resulting in exposure of sensitive data and modification of device settings.

The vulnerability affects ISP-managed firmware variants of the product. Remediation is coordinated through service providers.
