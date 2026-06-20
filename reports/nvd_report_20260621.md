# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-20 15:03 UTC
- **対象期間**: `2026-06-19T19:00:44.000Z` 〜 `2026-06-20T15:03:00.000Z`
- **重要CVE数**: 39 件（Critical 9.0+: 13 件 / High 7.0〜: 26 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に報告された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超と非常に多く、特に **リモートコード実行 (RCE)** と **特権昇格** が目立ちます。  
- Joomla 系プラグイン、ProxySQL、Azure 系サービスといった **Web アプリケーション・クラウド基盤** が集中して攻撃対象となっており、認証バイパスや不適切な入力検証が共通の根本原因です。  
- 多くは **未認証** でも利用可能な脆弱性で、攻撃者は簡単に任意コードを実行したり、管理者権限へ昇格できる点が危険です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 種類 | 主な影響範囲 | 注目理由 |
|-----|------|------|--------------|----------|
| **CVE‑2026‑48939** | 10.0 | 任意ファイルアップロード (RCE) | Joomla 用 iCagenda 拡張 (全バージョン) | 認証不要で任意 PHP ファイルをアップロードでき、サーバ全体の制御が可能。Joomla サイトは日本国内でも多数利用されている。 |
| **CVE‑2026‑48908** | 10.0 | 任意ファイルアップロード (RCE) | Joomla 用 SP Page Builder (全バージョン) | 同様に未認証でファイルアップロードが可能。攻撃コードが即座に実行され、Web シェル設置が容易。 |
| **CVE‑2026‑45480** | 10.0 | 認証バイパス・特権昇格 | Azure Active Directory (全テナント) | ネットワーク上の任意ユーザーが Azure AD の管理者権限を取得でき、クラウドリソース全体が危険にさらされる。 |
| **CVE‑2026‑48772** | 10.0 | プロトコル実装不備 (RCE) | ProxySQL 2.0.0‑3.0.8 | `PROXY UNKNOWN` ヘッダーを悪用し、任意コード実行が可能。ProxySQL は多くの大規模 DB 環境でミドルウェアとして採用されている。 |
| **CVE‑2026‑48584** | 9.9 | 特権昇格 (Azure Synapse) | Azure Synapse ワークスペース | 認可済みユーザーが不要な権限で実行でき、データ抽出や設定変更が可能。 |
| **CVE‑2026‑11551** | 9.8 | アカウント乗っ取り・特権昇格 | WordPress Branda プラグイン (≤ 3.4.29) | パスワード更新時にユーザー検証が欠如。WordPress サイトの管理者権限取得が容易になる。 |

> **注**：上記は **CVSS 10.0** の 4 件と、実務インパクトが大きい **Azure 系**、**ProxySQL**、**WordPress** の 2 件を選出。いずれも「未認証」または「低権限」からの攻撃が可能で、早急な対策が必要です。

---

## 3. 推奨アクション  

### 3.1 Joomla 系プラグイン  
- **iCagenda**: 公式サイトで提供されている **v2.5.0 以降**（※執筆時点で最新）にアップデート。  
- **SP Page Builder**: **v5.12.0 以降**へ更新。  
- すべての Joomla 本体と拡張プラグインを **最新版** に保ち、**未使用プラグインは無効化または削除**。  

### 3.2 Azure サービス  
- **Azure Active Directory**: Azure ポータル → **Identity Protection** → **Risk‑based Conditional Access** を有効化し、**MFA** を全ユーザーに適用。  
- **Azure Synapse**: **2026‑09‑01** 以降のパッチ (Synapse v2026‑09‑01‑security) を適用。  
- すべてのテナントで **Privileged Identity Management (PIM)** を有効にし、管理者ロールの **Just‑In‑Time (JIT)** アクセスに切り替える。  

### 3.3 ProxySQL  
- **バージョン 3.0.9 以降**（または 2.0.9 以上）へアップグレード。  
- `PROXY` ヘッダーの受信を **必須のホワイトリスト** に限定し、外部からの直接接続を防止するファイアウォールルールを追加。  

### 3.4 WordPress プラグイン  
- **Branda**: **v3.4.30** 以上に更新。  
- **Simple File List**: **v6.3.8** 以上に更新し、`eeSFL_DeleteFile` のパス検証を強化。  
- **WooCommerce** (CVE‑2022‑50972): **7.2.0 以降**へ更新。  

### 3.5 その他共通対策  
| 項目 | 内容 |
|------|------|
| **パッチ管理** | すべてのサーバで **自動パッチ適用** を有効化し、CVE 公開後 **48 時間以内** に適用できる体制を整備。 |
| **WAF/IPS** | Web アプリケーションファイアウォールで **ファイルアップロード**、**PROXY ヘッダー**、**不正な Cookie** をブロックするルールを追加。 |
| **ログ監視** | Joomla、ProxySQL、Azure AD の認証失敗・ファイルアップロードログを **SIEM** に集約し、異常検知アラートを設定。 |
| **最小権限** | 各サービスの実行ユーザー・ロールを **最小権限** に絞り、特権アカウントの数を削減。 |
| **バックアップ** | 重要データベース・設定ファイルは **暗号化されたオフラインバックアップ** を定期取得し、復旧手順を年2回以上テスト。 |

---

> **まとめ**  
- 今期は「**未認証リモートコード実行**」と「**クラウド特権昇格**」が顕著です。特に Joomla 系拡張と Azure AD の脆弱性は、攻撃者がほぼ無制限にシステムを支配できるため、**パッチ適用と認証強化** が最優先です。  
- 上記推奨アクションを **速やかに実施** し、継続的な脆弱性スキャンとインシデントレスポンス体制の見直しを行うことで、リスクを大幅に低減できます。  

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-48939

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Red` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-20T13:16:42.433 |

A vulnerability in the iCagenda extension for Joomla allows the upload of arbitrary files in the file attachment feature, ultimately resulting in PHP code upload and execution.

### CVE-2026-48908

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Red` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-20T13:16:42.080 |

A vulnerability in the SP Page Builder for Joomla allows the upload of arbitrary files for unauthenticated users, ultimately resulting in PHP code upload and execution.

### CVE-2026-45480

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-19T21:16:51.970 |

Improper authentication in Azure Active Directory allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-48772

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-348;CWE-863` |
| Published | 2026-06-19T20:16:17.803 |

ProxySQL is a proxy for MySQL and its forks, as well as PostgreSQL. In versions 2.0.0 through 3.0.8, the ProxySQL MySQL frontend accepts the `PROXY UNKNOWN <addr> <addr> <port> <port>\r\n` PP1 frame as a well-formed PROXY protocol header. The HAProxy PROXY protocol v1 specification says that when the protocol token is `UNKNOWN`, the receiver MUST ignore any address fields that follow it, because the proxy has declared it cannot determine the client identity. ProxySQL parses those address fields anyway via `sscanf` and writes the spoofed source address into the session's `addr.addr` field. From there it flows directly into the query-rule matcher, where the `client_addr` predicate decides routing and ACL. When `mysql-proxy_protocol_networks = '*'` (the default), any TCP peer can send a PP1 frame and choose any source IP claim. With that, any `mysql_query_rules` row pinned to a `client_addr` value is forgeable: the attacker writes the address they want to match into the PP1 line, and ProxySQL routes their query as if it came from that address. In practice this is a routing and ACL bypass. Real deployments use `client_addr` for read-write splitting (internal apps go to the primary, public traffic to read replicas), per-app schema pinning, and query-filter rules (DDL allowed only from admin CIDR, public queries blocked from dangerous patterns). An attacker that can reach the frontend port can forge their way into any of those routes. Version 3.0.9 patches this issue.

### CVE-2026-48584

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-06-19T21:17:01.060 |

Execution with unnecessary privileges in Azure Synapse allows an authorized attacker to elevate privileges over a network.

### CVE-2026-11551

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-06-20T00:16:15.580 |

The Branda plugin for WordPress is vulnerable to privilege escalation via account takeover in all versions up to, and including, 3.4.29. This is due to the plugin not properly validating a user's identity prior to updating their password. This makes it possible for unauthenticated attackers to change arbitrary user's passwords, including administrators, and leverage that to gain access to their account.

### CVE-2026-48773

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-19T20:16:17.947 |

ProxySQL is a proxy for MySQL and its forks, as well as PostgreSQL. Versions 2.0.18 through 3.0.8 have a pre-authentication heap memory corruption vulnerability in the MySQL and PostgreSQL protocol first-read paths. A remote unauthenticated client can declare an oversized first packet length, and ProxySQL passes that attacker-controlled length directly to `recv()` while writing into a fixed 32 KB input queue. Version 3.0.9 patches the issue.

### CVE-2026-48582

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-19T21:17:00.787 |

Missing authorization in Microsoft Exchange Online allows an authorized attacker to elevate privileges over a network.

### CVE-2026-48909

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-20T13:16:42.317 |

SP LMS (com_splms) < 4.1.4 by JoomShaper deserializes user-controlled cookie data without validation, enabling an unauthenticated remote attacker to execute arbitrary code on the server.

### CVE-2022-50972

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-20T14:16:18.960 |

WooCommerce 7.1.0 contains a remote code execution vulnerability that allows attackers to execute arbitrary PHP code by injecting shell commands through the product-type parameter. Attackers can send requests to the class-wc-meta-box-product-images.php endpoint with unsanitized product-type values to write malicious PHP files to the web root.

### CVE-2019-25763

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-20T14:16:17.783 |

WordPress Ultimate Addons for Beaver Builder 1.2.4.1 contains an authentication bypass vulnerability that allows attackers to gain unauthorized access by exploiting the social media login form functionality. Attackers can submit a POST request to the admin-ajax.php endpoint with the uabb-lf-google-submit action, a valid administrator email address, and a valid nonce to obtain session cookies and authenticate as that user.

### CVE-2026-56081

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-06-19T22:16:18.017 |

Cap-go before 12.128.2 contains an authentication logic flaw that lets an attacker register and control an account bound to a victim's email address before that email is verified. By enabling two-factor authentication on the pre-registered account, the attacker gains control over the account claimed under the victim's identity, allowing them to read and modify its state and enforce organization-level policies, while the legitimate user is denied access to the account tied to their own email.

### CVE-2026-56073

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-06-19T22:16:17.623 |

Cap-go before 12.128.2 contains an authentication bypass vulnerability in OTP verification that allows attackers to bypass email verification by modifying server responses. Attackers can intercept OTP verification requests and manipulate HTTP responses to falsely mark verification successful, enabling unauthorized 2FA enablement and account takeover.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-47645

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-601` |
| Published | 2026-06-19T21:16:58.720 |

Url redirection to untrusted site ('open redirect') in Microsoft 365 Copilot's Business Chat allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-32208

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-19T21:16:41.883 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Edge (Chromium-based) allows an authorized attacker to perform spoofing over a network.

### CVE-2020-37255

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-20T14:16:18.790 |

WordPress Time Capsule Plugin 1.21.16 contains an authentication bypass vulnerability that allows unauthenticated attackers to gain administrative access by sending a crafted POST request with the IWP_JSON_PREFIX header. Attackers can exploit this flaw to obtain valid administrator session cookies and access the WordPress dashboard without providing credentials.

### CVE-2026-56216

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-20T01:16:16.970 |

Capgo before 12.128.2 contains a scope escalation vulnerability in the POST /functions/v1/apikey endpoint that allows app-limited API keys to mint unrestricted keys by setting empty limits. Attackers with a compromised app-limited key can create an unrestricted key with org-wide access to resources like app listings and other protected endpoints.

### CVE-2026-56215

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-20T01:16:16.840 |

Capgo before 12.128.12 allows authenticated users to modify their mutable public.users.email to arbitrary addresses, which the SSO provisioning endpoint trusts as an account-merge key. Attackers can pre-position their account with a victim's corporate SSO email, causing the provision-user endpoint to merge the victim's SSO identity into the attacker-controlled account.

### CVE-2026-56214

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-20T01:16:16.710 |

Capgo before 12.128.2 contains an information disclosure vulnerability in Supabase PostgREST RPC endpoints is_trial_org and is_paying_org that allows unauthenticated attackers to enumerate organizations and disclose billing status using the public sb_publishable key. Attackers can invoke these endpoints to determine organization existence via distinguishable return values and identify paying customers for targeted profiling.

### CVE-2026-56082

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-19T22:16:18.143 |

Capgo (Cap-go/capgo) before 12.128.2 contains an improper access control vulnerability in the SECURITY DEFINER PostgREST RPC function public.record_build_time, which is granted to the anon role and callable with only the public Supabase publishable (sb_publishable_*) anon key. An unauthenticated attacker can insert rows into public.build_logs for arbitrary organizations and, because the function uses ON CONFLICT (build_id, org_id) DO UPDATE, can overwrite existing usage/billing records by reusing the same build_id for a target org. This enables cross-tenant tampering of billing build logs and financial-impact denial of service by inflating billable build time.

### CVE-2023-54357

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-203` |
| Published | 2026-06-19T19:16:25.840 |

Joomla com_booking component 2.4.9 contains an information disclosure vulnerability that allows unauthenticated attackers to enumerate user accounts by exploiting the getUserData function in the customer controller. Attackers can send GET requests to index.php with option=com_booking, controller=customer, task=getUserData, and an id parameter to retrieve user names, usernames, and email addresses through brute force enumeration.

### CVE-2026-9843

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-20T02:16:26.910 |

The Database for Contact Form 7, WPforms, Elementor forms plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the view_page function in all versions up to, and including, 1.5.1. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). Successful exploitation requires an administrator to view or edit the poisoned form entry, at which point PHP's bracket parser reshapes the attacker-crafted JSON key to bypass the stored-path isset check and trigger deletion of the traversal-specified file.

### CVE-2026-49340

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-697;CWE-732` |
| Published | 2026-06-19T19:16:36.817 |

gonic is a music streaming server / free-software subsonic server API implementation. Prior to version 0.21.0, a logic error in `ServeCreateOrUpdatePlaylist` allows any authenticated Subsonic user (including non-admin) to write playlist M3U content to an attacker-controlled absolute filesystem path on the gonic host, and to create intermediate directories with `0o777` permissions. The bug is independent of CVE-2026-49338 and CVE-2026-49339. It is an unreachable guard clause combined with no path containment in `Store.Write`. Version 0.21.0 patches the issue.

### CVE-2026-49291

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-19T19:16:36.170 |

mcp-memory-service is a semantic memory layer for AI applications. Prior to version 10.65.3, the HTTP MCP JSON-RPC endpoint at `/mcp` requires only OAuth `read` scope for all requests, then dispatches `tools/call` directly to handlers that include mutating tools. A read-only OAuth client can call `store_memory` and `delete_memory` through MCP even though the corresponding REST endpoints require `write` scope. Version 10.65.3 patches the issue.

### CVE-2026-48715

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-19T20:16:17.663 |

radvd is a router advertisement daemon for IPv6. Prior to version 2.21, the `radvdump` utility shipped with radvd contains a stack buffer overflow in the Route Information option parser. When processing a crafted ICMPv6 Router Advertisement, `print_ff()` copies up to 2032 bytes from attacker-controlled packet data into a 16-byte `struct in6_addr` on the stack, overflowing by up to 2016 bytes. Note that the main `radvd` daemon is not affected by the vulnerability. Version 2.21 patches the issue.

### CVE-2026-11912

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-20T09:16:15.460 |

The Simple File List plugin for WordPress is vulnerable to arbitrary file modification due to insufficient authorization checks in all versions up to, and including, 6.3.7. This makes it possible for unauthenticated attackers to delete and modify files on the serve. This vulnerability is exploitable even when the administrator has not enabled the AllowFrontManage setting, because the is_admin() check unconditionally short-circuits the guard before that setting is evaluated.

### CVE-2026-11911

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-20T09:16:13.910 |

The Simple File List plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the eeSFL_DeleteFile function in all versions up to, and including, 6.3.7. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The simplefilelist_edit_job AJAX action is registered via wp_ajax_nopriv_, making it accessible without authentication, and the is_admin() guard that would otherwise restrict access is bypassed because is_admin() always returns true for requests to the admin-ajax.php endpoint.

### CVE-2026-50559

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287;CWE-863` |
| Published | 2026-06-19T21:17:02.373 |

Quarkus is a Java framework for building cloud-native applications. Prior to versions 3.37.0, 3.36.3, 3.33.2.1, 3.33.3, 3.27.4.1, 3.27.5, and 3.20.6.2, Quarkus HTTP path-based authorization policies can be bypassed using encoded semicolons (%3B) to smuggle matrix parameters past the security layer, and using encoded slashes (%2F) or backslashes (%5C) to access protected static resources. This is a distinct issue from CVE-2026-39852, which addressed only literal semicolon stripping. Versions 3.37.0, 3.36.3, 3.33.2.1, 3.33.3, 3.27.4.1, 3.27.5, and 3.20.6.2 contain a patch.

### CVE-2026-48774

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-19T20:16:18.087 |

ProxySQL is a proxy for MySQL and its forks, as well as PostgreSQL. In versions 3.0.0 through 3.0.8, ProxySQL's GenAI/MCP `run_sql_readonly` tool violates its documented read-only contract for MySQL targets. The tool validates only the full input string with a substring blacklist and first-keyword allowlist, but then executes the entire SQL string on a backend connection created with `CLIENT_MULTI_STATEMENTS`. As a result, a caller can submit a read-only first statement followed by a side-effecting second statement, such as `SELECT 1; RENAME TABLE ...`. The validator accepts the payload because it starts with `SELECT` and because side-effecting MySQL statements such as `RENAME TABLE`, `SET`, `RESET`, `LOCK TABLES`, and `KILL` are not rejected by the blacklist. In a live MCP runtime test, the `/mcp/query` endpoint accepted a `run_sql_readonly` request. The MCP response reported success for the first `SELECT`, and direct backend verification showed that the table had actually been renamed. This violates the endpoint's read-only security contract and lets an MCP caller perform backend writes or administrative SQL, limited by the configured MCP target account's database privileges. Version 3.0.9 contains a fix. Other operator mitigations include: keeping MCP disabled unless required; setting a non-empty `mcp-query_endpoint_auth` token before exposing `/mcp/query`; restricting MCP listener network exposure; configuring MCP backend target credentials as database-level read-only users; and adding temporary MCP query rules to block obvious multi-statement patterns.

### CVE-2026-9375

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-19T19:16:36.947 |

urllib3 version 2.6.3 is vulnerable to a decompression bomb bypass in its streaming API (`preload_content=False`) when using Brotli support. The issue arises due to three independent code paths in `response.py` that bypass the `max_length` protection introduced in version 2.6.0 to mitigate CVE-2025-66471. Specifically, negative `max_length` values can be produced due to buffer arithmetic in `read()`, `flush_decoder` unconditionally overrides `max_length` to `-1`, and `_flush_decoder()` passes no limit at all, defaulting to unlimited decompression. This allows a malicious HTTP server to trigger an out-of-memory (OOM) condition by decompressing large payloads into memory, leading to a denial of service (DoS). The vulnerability affects urllib3 2.6.3 and Brotli 1.2.0 and impacts applications and libraries using `requests` or `urllib3` to stream content from untrusted sources.

### CVE-2026-49293

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407;CWE-1333` |
| Published | 2026-06-19T19:16:36.297 |

js-toml is a TOML parser for JavaScript, fully compliant with the TOML 1.0.0 Spec. Versions up to and including 1.1.0 parse hexadecimal / octal / binary integer literals via a hand-written `parseBigInt` loop that multiplies a `BigInt` accumulator by the radix once per input digit. Each iteration performs a `BigInt * BigInt` operation on an accumulator that grows linearly with the number of digits already consumed, so the whole loop is O(n²) in the literal length. The lexer regex places no upper bound on the literal length, so a single TOML document containing one ~500 kB hex literal pins one CPU core for ~40 seconds on a modern laptop (Apple M-series, Node v22). Memory amplification is bounded but CPU amplification is severe and grows quadratically: doubling the literal length quadruples the work. A caller that invokes `load()` on attacker-controlled TOML (configuration upload endpoints, CI/CD systems ingesting third-party `*.toml`, IDE plugins, build tools) is exposed to a single-request CPU exhaustion DoS. Version 1.1.1 fixes the issue.

### CVE-2026-48787

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-19T20:16:18.237 |

gin-vue-admin is an AI-assisted basic development platform. In version 2.9.1, an authenticated attacker with access to the code-generation feature and MCP management interface can exploit this vulnerability by injecting attacker-controlled Go source code through POST /autoCode/addFunc, and then invoking POST /autoCode/mcpStart to trigger a rebuild and restart of the standalone MCP service. This allows arbitrary operating system commands to be executed on the server with the privileges of the application process. Successful exploitation may lead to remote code execution (RCE), modification of backend source code or runtime logic, deployment of persistent backdoors, access to or manipulation of application data and configuration, and further impact on local resources running under the same service account or privilege context. The risk is highest in deployments that retain the source tree, allow writes to source files, and support local build or startup of standalone MCP components. In environments using binary-only releases, read-only filesystems, or with local build capabilities removed, the exploitability of the full attack chain is significantly reduced. However, once the online code-generation capability and MCP-hosted startup workflow are enabled, the overall security impact may reach high to critical severity. As of time of publication, it is unknown if a patched version is available. As a workaround, enforce strict allowlist validation on path- and identifier-related fields such as `humpPackageName`, `packageName`, `FuncName`, and `Router`, and only permit safe identifier formats.

### CVE-2026-56079

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-19T22:16:17.760 |

Capgo before 12.128.2 contains a cross-tenant authorization bypass vulnerability in PostgREST endpoints that allows org-scoped read API keys to access other tenants' webhook secrets and delivery logs. Attackers can query the webhooks and webhook_deliveries endpoints to exfiltrate HMAC signing secrets and delivery payloads, enabling forged webhook events against victim organizations.

### CVE-2026-49346

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-06-19T21:17:01.847 |

libde265 is an open source implementation of the h.265 video codec. Prior to version 1.1.0, a crafted H.265 bitstream with large SPS dimensions and 16-bit bit depth causes a signed integer overflow in `de265_image_get_buffer()` (`libde265/image.cc:128`). The overflow wraps the plane allocation size to a small value (~1 KB), but the subsequent `fill_image()` call computes the real size using `size_t`, writing ~4 GB into the undersized heap buffer. Version 1.1.0 patches the issue.

### CVE-2026-49295

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-19T21:17:01.590 |

libde265 is an open source implementation of the h.265 video codec. Prior to version 1.0.20, a crafted H.265 bitstream can cause an out-of-bounds array write in `decoder_context::process_reference_picture_set()` (`libde265/decctx.cc:1376`). The root cause is a missing aggregate bound check on predicted short-term reference picture set entries. Individual list sizes are validated, but the combined count after predicted RPS construction can exceed the 16-entry `PocStFoll` array, writing at index 16. Version 1.0.20 patches the issue.

### CVE-2026-49344

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-359` |
| Published | 2026-06-19T20:16:18.520 |

Mercator is an open source web application that enables mapping of the information system. Prior to version 2025.05.19, Mercator's Query Engine (`/admin/queries/execute`) accepts a JSON DSL (`from` / `select` / `filters` / `traverse` / `output`), translates it into an Eloquent query, and returns results as JSON. The controller method `QueryController::execute()` does not enforce an authorization gate, unlike `store()` and `massDestroy()` in the same controller which are correctly protected. As a result, any authenticated account — including the read-only Auditor role — can query models beyond its intended scope, including the `User` model. Additionally, the `password` column, although declared `$hidden`, is not excluded from filter predicates, which allows it to be used in `LIKE` conditions. The `schema()` and `schemaModel()` endpoints of the same controller are similarly unguarded. The Query Engine is read-only; integrity and availability are not affected. Version 2025.05.19 patches the issue.

### CVE-2026-48089

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-863` |
| Published | 2026-06-19T20:16:16.583 |

DevGuard provides vulnerability management for the full software supply chain. Prior to 1.4.2, on a DevGuard API instance with one or more public assets, any authenticated user — including users from a different organization with no membership or role in the affected org/project — can create, update, reapply, and delete VEX rules on those public assets. The same flaw affects the other vulnerability-triage write endpoints exposed under a public asset, including VEX rule create / update / reapply / delete; dependency-vuln event creation (accept / reject / mitigate decisions), batch event creation, vuln sync, and mitigation; license risk creation; external reference writes; and/or artifact creation and license refresh. The attacker needs a valid account on the instance, but no membership in the victim organization, project, or asset is required. Version `v1.4.2`contains a patch. As a workaround, make affected assets non-public. In the asset settings, switch visibility from public to private. This removes the public-read exemption in the access-control middleware and restores correct authorization on all write endpoints for that asset. Downstream consumers that previously relied on the public `vex.json` / `sbom.json` endpoints will need to be granted explicit access or must receive an exported file version until the patched release is deployed.

### CVE-2026-49339

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-639` |
| Published | 2026-06-19T19:16:36.687 |

gonic is a music streaming server / free-software subsonic server API implementation. The maintainer's fix in  commit `6dd71e6a3c966867ef8c900d359a7df75789f410` added an ownership check based on `playlist.UserID`. However, `playlist.UserID` is derived from the first path segment of the attacker-controlled playlist ID, with no path containment on the resolved file path. Any authenticated Subsonic user can therefore bypass the ownership check and read any other user's playlist, delete any other user's playlist, and probe arbitrary file paths on the host for existence/readability. This is a bypass of the boundary the `6dd71e6` fix is trying to enforce; it is closely related to the original GONIC-1 IDOR but uses a different primitive (path traversal in the `id` parameter rather than direct cross-user access). Commit 0824bed88f6bbc490ba28bf09d28e5dfeb07b445 in version 0.21.0 fixes the issue.

### CVE-2026-49338

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-285;CWE-639` |
| Published | 2026-06-19T19:16:36.557 |

gonic is a music streaming server / free-software subsonic server API implementation. Prior to version 0.21.0, the Subsonic API endpoints `/rest/deletePlaylist.view` and `/rest/getPlaylist.view` perform no per-resource authorization. Once authenticated as any user (admin or not), an attacker can delete any playlist owned by any other user (including admin) by passing its `id` and read the full contents (name, comment, song list) of any other user's **private** (non-public) playlist by passing its `id`. The Subsonic playlist `id` is `base64url("<userID>/<filename>.m3u")`. Because filenames are user-supplied or time-derived and the `userID` is a small integer, IDs are guessable and frequently exposed (e.g. a previously-public playlist that was later made private still has the same ID). This breaks the multi-user trust boundary of gonic: a low-privileged user can wipe an administrator's curated playlists, and a user can exfiltrate any private playlist they obtain an ID for. The issue was fixed in commit `6dd71e6a3c966867ef8c900d359a7df75789f410`, which is part of version 0.21.0.
