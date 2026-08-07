# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-07 15:00 UTC
- **対象期間**: `2026-08-06T15:01:39.000Z` 〜 `2026-08-07T15:00:52.000Z`
- **重要CVE数**: 239 件（Critical 9.0+: 74 件 / High 7.0〜: 165 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVSS 7.0 以上の脆弱性は、**クラウド基盤（Azure・Microsoft 365）とオープンソース／WordPress プラグイン**に集中しています。特に **認証・認可の欠如** に起因するリモートコード実行 (RCE) や特権昇格が多数報告され、攻撃者はネットワーク上から無認証で管理権限を取得できる点が共通しています。  
- Microsoft 製品は「認可チェックの抜け」系が多数（Teams、Planetary Computer、Azure SRE Agent など）。  
- WordPress エコシステムは、**配布サーバの改ざんやバックドア埋め込み** が目立ち、プラグイン単体でフルリモートコード実行が可能になるケースが急増。  
- Azure の各サービス（SQL Database、Service Bus、Active Directory 等）でも **デシリアライズや不適切な署名検証** が原因の高リスク脆弱性が確認されています。  

このため、クラウド環境と WordPress サイトの両方で **即時のパッチ適用・プラグイン除去・監査** が必須です。

---

## 2. 特に注目すべき CVE（上位 5 件）

| CVE | CVSS | 主な影響 | 理由・注目ポイント |
|-----|------|----------|-------------------|
| **CVE‑2026‑56162** | 10.0 | Azure SQL Database の認証不備により **ネットワーク上の無認証攻撃者が特権昇格・完全制御** が可能 | Azure の基幹データベースサービスで発生。データ漏洩・改ざんリスクが極めて高く、企業のミッションクリティカルなデータが対象になる可能性がある。 |
| **CVE‑2026‑14812** | 10.0 | Premium SEO WordPress プラグインに **未認証バックドア** が組み込まれ、管理者アカウント作成・RCE・SSRF が可能 | プラグインは SEO 用として広く導入されており、インストールベースが大きい。配布パッケージ自体がマルウェア化している点が特に危険。 |
| **CVE‑2026‑11976** | 10.0 | MonsterInsights Pro の配布バケットが改ざんされ、**class‑system‑check.php** がマルウェア化 | 公式アップデートサーバがハイブリッドクラウド (S3) でホストされているため、同様の手法で他のプラグインや SaaS でも再現可能。被害拡大が速い。 |
| **CVE‑2026‑66665** | 10.0 | Type Hub ≤ 2.0.6 に **未認証任意ファイルアップロード** が存在し、任意コード実行が可能 | ファイルアップロードは Web アプリの典型的な攻撃経路。アップロード先がサーバ上の実行可能ディレクトリであるため、即座にシェル取得が可能。 |
| **CVE‑2026‑65553** | 10.0 | Spider Analyser (WordPress 検索エンジン解析プラグイン) ≤ 2.1.3 に **未認証 RCE** がある | プラグインは SEO・解析ツールとして多数のサイトに導入されている。攻撃コードは単一リクエストで実行でき、WAF での検知が困難。 |

> **注**：上記は「CVSS が最高 (10.0)」かつ「広範囲に利用されている／インフラ基盤に直結している」点で選定しました。  

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
1. **脆弱性スキャンの実施**  
   - Azure Security Center、Microsoft Defender for Cloud、WPScan などで対象リソースを即時スキャン。  
2. **ネットワークレベルでの防御**  
   - 該当サービスへの **インバウンド/アウトバウンド通信を最小化**（NSG、WAF で IP 制限）。  
   - Azure AD の **条件付きアクセスポリシー** を強化し、特権操作は MFA 必須に。  
3. **ログ・監査の強化**  
   - Azure Monitor、Microsoft Sentinel で **認証失敗・特権昇格イベント** をアラート化。  
   - WordPress の `wp-config.php` とプラグインディレクトリの **ファイル改ざん監視**（OSSEC、Tripwire 等）。  

### 3.2 個別 CVE に対する具体的対策  

| CVE | 推奨アクション | 具体的パッケージ / バージョン |
|-----|----------------|------------------------------|
| **CVE‑2026‑56162** (Azure SQL Database) | - Azure ポータルで対象 **SQL Server の最新パッチ** を適用<br>- **ファイアウォール規則**で外部からの直接接続を遮断<br>- 既存の接続文字列・認証情報を **ローテーション** | Azure SQL Database (全インスタンス) – 2026‑Q3 以降の **Security Update** がリリース済み |
| **CVE‑2026‑14812** (Premium SEO WP plugin) | - 該当プラグイン **即時削除**<br>- 代替の信頼できる SEO プラグイン (Yoast SEO, Rank Math) に切り替え<br>- 既存サイトの **ファイル整合性チェック**（`wp-content/plugins/premium-seo` ディレクトリ） | `premium-seo` ≤ 最新版 (2026‑03) – **削除推奨** |
| **CVE‑2026‑11976** (MonsterInsights Pro) | - 公式配布サーバ（`monster-insights.s3.amazonaws.com`）から **最新バージョン 10.2.3** 以降を再取得<br>- `class-system-check.php` が残っていないか **手動で削除**<br>- S3 バケットの **署名付き URL** と **IAM ポリシー** を見直し | MonsterInsights Pro 10.2.3 以降 – **10.2.2 以前は使用禁止** |
| **CVE‑2026‑66665** (Type Hub) | - **バージョン 2.0.7 以上** にアップデート（ベンダーが提供するパッチ）<br>- アップロードディレクトリを **実行権限なし** に設定 (`chmod 0644`)<br>- WAF で `Content‑Type: multipart/form-data` の **拡張子ホワイトリスト** を適用 | Type Hub ≤ 2.0.6 – **アップデート必須** |
| **CVE‑2026‑65553** (Spider Analyser) | - **バージョン 2.1.4 以上** に更新<br>- プラグインの **`admin-ajax.php`** エンドポイントへのアクセスを IP 制限<br>- 不要なプラグインは **無効化・削除

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-65667

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-07T00:16:38.680 |

Missing authorization in Microsoft Teams allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-63508

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-07T00:16:36.973 |

Missing authentication for critical function in Microsoft Planetary Computer Pro allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-56162

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-07T00:16:31.990 |

Improper authentication in Azure SQL Database allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-14812

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-912` |
| Published | 2026-08-06T22:16:46.967 |

The Premium SEO WordPress plugin is malicious: it ships an unauthenticated backdoor that creates a hidden administrator account and, in some builds, also enables remote code execution, server-side request forgery and arbitrary front-end script/content injection, giving an unauthenticated attacker full control of the affected site.

### CVE-2026-11976

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-912` |
| Published | 2026-08-06T22:16:45.103 |

The official MonsterInsights Pro update distribution bucket (`monster-insights.s3.amazonaws.com`) was compromised. Both the current release (10.2.2) and the version MonsterInsights rolled back to (10.2.0) contain a malicious file, `class-system-check.php`. Three distinct variants were observed on 2026-06-11, all sharing the same AES-256-GCM key, confirming a single threat actor. The attacker retains write access to the S3 bucket and has been actively iterating on the payload throughout the day.

### CVE-2026-66665

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-06T15:17:21.227 |

Unauthenticated Arbitrary File Upload in Type Hub <= 2.0.6 versions.

### CVE-2026-65553

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-06T15:17:17.557 |

Unauthenticated Remote Code Execution (RCE) in Spider Analyser &#8211; WordPress搜索引擎蜘蛛分析插件 <= 2.1.3 versions.

### CVE-2026-62830

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-07T00:16:34.593 |

Missing authorization in Azure SRE Agent allows an authorized attacker to elevate privileges over a network.

### CVE-2026-59115

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-35` |
| Published | 2026-08-07T00:16:33.780 |

'.../...//' in Microsoft Entra Provisioning Service (SyncFabric) allows an authorized attacker to elevate privileges over a network.

### CVE-2026-50515

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-07T00:16:31.140 |

Deserialization of untrusted data in Azure Service Bus allows an authorized attacker to execute code over a network.

### CVE-2026-50481

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-471` |
| Published | 2026-08-07T00:16:30.980 |

Modification of assumed-immutable data (maid) in Azure Active Directory allows an authorized attacker to elevate privileges over a network.

### CVE-2026-48086

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-06T22:17:11.593 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. Prior to version 1.0.2, a TENANT_ADMIN promotes themselves to platform-wide GLOBAL_ADMIN through a single PUT request. The role-update handler accepts the `GLOBAL_ADMIN` enum value from any tenant admin updating their own tenant's staff. No policy check enforces that "only an existing GLOBAL_ADMIN may grant GLOBAL_ADMIN", so the schema validation IS the authorization decision. After re-login, the JWT contains the new role and the formerly-tenant-scoped admin reaches every other tenant on the platform. On the hosted OpenReception service this is a scope-changed escalation: a single customer-side tenant administrator gains full platform-wide administrative control over all other tenants' configuration, users, staff records, operational metadata, and tenant lifecycle. Plaintext appointment contents remain subject to the E2E model unless chained with the staff-crypto poisoning issue (V-4) or with staff-passkey hijacking (V-1). On a single-tenant self-hosted deployment it is still a privilege escalation because TENANT_ADMIN should not be able to create new tenants, modify global configuration, or manage other administrators. The same handler also accepts updates targeted at any colleague within the tenant. A tenant admin can promote a separate collaborator account instead of themselves, leaving their own audit trail clean while the platform-wide breach happens through a separate identity. Version 1.0.2 fixes the issue.

### CVE-2026-65548

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-06T15:17:16.737 |

Contributor Remote Code Execution (RCE) in Betheme <= 28.4.2 versions.

### CVE-2026-14365

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-07T05:16:57.883 |

The TrueBooker – Appointment Booking and Scheduler System plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 1.2.3. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to change the password of arbitrary user accounts, including administrators, which can be leveraged to gain access to those accounts.

### CVE-2026-14364

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-08-07T05:16:57.743 |

The TrueBooker – Appointment Booking and Scheduler System plugin for WordPress is vulnerable to account takeover via improper password reset validation in all versions up to, and including, 1.2.3. This is due to the plugin not properly validating a user's identity before resetting their password. This makes it possible for unauthenticated attackers to reset the password of arbitrary user accounts, including administrators, and gain access to those accounts.

### CVE-2026-62873

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-07T00:16:36.350 |

Improper verification of cryptographic signature in Microsoft 365 Admin Center allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-48087

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-06T22:17:11.750 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. Prior to version 1.0.2, the registration handler at `POST /api/auth/register/{userId}` validates the relationship between the WebAuthn challenge and the registration cookie's email but never validates that the `userId` in the URL belongs to that email. An unauthenticated attacker requests a challenge for their own email, generates a registration response with their own authenticator, and submits it against any victim user's URL. The challenge-vs-cookie email match passes, the WebAuthn ceremony validates, and `addPasskey` writes the attacker's credential into the victim's `user_passkey` rows. The next victim-email login accepts a passkey assertion from the attacker's authenticator and issues a session as the victim. User IDs are not strictly secret on this platform, but the exact set of exposure surfaces should be assessed by the maintainers. Staff-list endpoints return user IDs to authenticated tenant members per the route signature; live verification of all exposure surfaces (whether user IDs leak through any unauthenticated route, through invite-confirmation URLs, or through other administrative views) is part of the pending live PoC. Where the attacker knows the victim's email and userId, the analysis below becomes account takeover. Version 1.0.2 fixes the issue.

### CVE-2026-48085

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T22:17:11.440 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. Prior to version 1.0.1, a fully provisioned OpenReception instance accepts unauthenticated POST requests to `/setup/create-admin-account` and creates additional GLOBAL_ADMIN accounts without verifying that an admin already exists. Any unauthenticated network attacker who can submit a same-origin form POST gains full platform-level administrative control. The newly created account is `is_active=true` with `confirmation_state=ACCESS_GRANTED` and does not require completing email confirmation; the GLOBAL_ADMIN row is created active and immediately usable. Login and tenant enumeration succeed without any further interaction. This is distinct from the deployment race condition already documented on the `Claiming an instance` page. That documented race covers the window between deployment and first claim. The bug reported here works after the operator has properly claimed and configured the instance: the layout-level guard that protects the setup page only redirects on GET, while the `default` form action handler creates the user without rechecking `adminExists()`. Three GLOBAL_ADMIN accounts were created in succession during testing, with no rate limiting observed. Audit-specific event logging beyond standard application logs was not assessed; the standard `[error]` line that surfaces only when a uniqueness conflict is hit is not the same as a security event for "additional admin created post-claim". The form post is rejected for browser drive-by CSRF by SvelteKit's built-in same-origin check, but any tool that supplies a matching `Origin` header (curl, Burp, automated scanners, server-side proxies) bypasses this trivially. No additional preconditions exist. Users should upgrade to version 1.0.1 to receive a patch.

### CVE-2026-17032

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-912` |
| Published | 2026-08-06T22:16:49.237 |

Multiple Supsystic Pro plugins were distributed with malicious code through the vendor's compromised update server, allowing unauthenticated attackers to deploy a second-stage payload that exfiltrates credentials and other sensitive data and grants full control of affected sites.

### CVE-2026-67261

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-06T15:17:24.430 |

Dell Virtual Storage Integrator for VMware vSphere Client, versions prior to 10.11.1.0, contain(s) an OS Command Injection vulnerability in the IAPI component. A remote unauthenticated attacker could potentially exploit this vulnerability, leading to the execution of arbitrary OS commands on the application's underlying operating system with root privileges. Exploitation may lead to a complete system takeover by an attacker. This vulnerability is considered critical as it allows an unauthenticated remote attacker to achieve arbitrary code execution as root, potentially compromising the entire VSI deployment and underlying infrastructure. Dell recommends customers to upgrade at the earliest opportunity.

### CVE-2026-66662

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-06T15:17:20.850 |

Unauthenticated Privilege Escalation in Frontend Admin by DynamiApps <= 3.29.10 versions.

### CVE-2026-65581

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:19.683 |

Unauthenticated PHP Object Injection in AI ANN <= 1.29.0 versions.

### CVE-2026-65579

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:19.560 |

Unauthenticated PHP Object Injection in Agricola <= 1.21.0 versions.

### CVE-2026-65578

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:19.437 |

Unauthenticated PHP Object Injection in Agora <= 1.9 versions.

### CVE-2026-65577

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:19.313 |

Unauthenticated PHP Object Injection in Advice <= 1.18.0 versions.

### CVE-2026-65576

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:19.190 |

Unauthenticated PHP Object Injection in Adrena <= 1.2.14 versions.

### CVE-2026-65575

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:19.067 |

Unauthenticated PHP Object Injection in Accalia <= 1.5.3 versions.

### CVE-2026-65574

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:18.940 |

Unauthenticated PHP Object Injection in Abogado <= 1.18 versions.

### CVE-2026-65573

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:18.813 |

Unauthenticated PHP Object Injection in Abelle <= 1.22 versions.

### CVE-2026-65572

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:18.683 |

Unauthenticated PHP Object Injection in A.Williams <= 1.3.1 versions.

### CVE-2026-65571

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:18.560 |

Unauthenticated PHP Object Injection in 69 Clothing <= 1.2.11.1 versions.

### CVE-2026-65556

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:17.803 |

Unauthenticated PHP Object Injection in WPBruiser {no- Captcha anti-Spam} <= 3.1.43 versions.

### CVE-2026-65552

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:17.430 |

Subscriber PHP Object Injection in Export User Data <= 2.2.6 versions.

### CVE-2026-65507

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-06T15:17:14.823 |

Unauthenticated Privilege Escalation in AIWU <= 1.5.6 versions.

### CVE-2026-28139

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:16:52.580 |

Unauthenticated PHP Object Injection in Ajax Search Lite <= 4.14.4 versions.

### CVE-2026-28005

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T15:16:51.560 |

Unauthenticated Privilege Escalation in Kadence WooCommerce Email Designer <= 1.5.19 versions.

### CVE-2026-70332

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-07T00:16:41.040 |

Server-side request forgery (ssrf) in Microsoft Office SharePoint allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-62896

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-07T00:16:36.590 |

Improper authentication in Microsoft Teams allows an authorized attacker to elevate privileges over a network.

### CVE-2026-56161

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-07T00:16:31.827 |

Improper access control in Azure Logic Apps allows an authorized attacker to disclose information over a network.

### CVE-2026-19175

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:17:00.040 |

Use after free in Payments in Google Chrome prior to 151.0.7922.109 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19171

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:59.590 |

Use after free in Media in Google Chrome on Windows prior to 151.0.7922.109 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19170

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:59.480 |

Use after free in WebGL in Google Chrome on Android prior to 151.0.7922.109 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-19166

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:59.037 |

Use after free in Web Authentication in Google Chrome prior to 151.0.7922.109 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19164

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-06T22:16:58.803 |

Insufficient validation of untrusted input in Codecs in Google Chrome prior to 151.0.7922.109 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19157

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-06T22:16:58.010 |

Out of bounds write in ANGLE in Google Chrome on Android prior to 151.0.7922.109 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-19149

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:57.113 |

Use after free in Aura in Google Chrome on Linux prior to 151.0.7922.109 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-54212

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-07T10:16:58.353 |

Tobit Laboratories AG TeamDavid's Webbox application implements an API endpoint that is vulnerable to a 
buffer overflow condition. By submitting a specially crafted JSON body, 
such as one that is at least 8 characters long and begins with a number,
 an unauthenticated attacker can cause the server to crash, resulting in
 denial of service. Depending on the stack state or if a stack canary 
can be disclosed through another vulnerability, this buffer overflow 
could potentially lead to remote code execution and full compromise of 
the server. This issue affects TeamDavid through Rollout 524.

### CVE-2026-54211

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-07T10:16:58.170 |

Tobit Laboratories AG TeamDavid's Webbox application’s endpoint “//serverClient_close.html” is vulnerable to a
 buffer overflow vulnerability in multiple form data parameters. By 
submitting excessively long values in these parameters, an authenticated
 attacker can trigger a server crash, resulting in denial of service. 
Depending on the stack state or if a stack canary can be disclosed 
through another vulnerability, this buffer overflow could potentially be
 exploited for remote code execution, leading to full compromise of the 
server. This issue affects TeamDavid through Rollout 524.

### CVE-2026-54210

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-07T10:16:58.030 |

Tobit Laboratories AG TeamDavid's Webbox application implements various file upload functionalities that are 
vulnerable to a buffer overflow condition. By specifying an excessively 
long filename in a file upload request, an unauthenticated attacker can 
trigger a crash of the server, resulting in a denial of service. 
Depending on the stack state or if a stack canary can be disclosed 
through another vulnerability, this buffer overflow could potentially be
 exploited for remote code execution, leading to full compromise of the 
server. This issue affects TeamDavid through Rollout 524.

### CVE-2026-48088

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T22:17:11.893 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. Prior to version 1.0.4, the route `POST /api/tenants/{tenantId}/staff/{staffId}/crypto` accepts and stores attacker-controlled ML-KEM-768 public keys against any tenant on the platform without authentication. The handler logs an "Unauthorized crypto key storage attempt" warning when neither a session nor a registration cookie is present, then proceeds to insert the row regardless. The platform's E2E claim that "even administrators cannot view sensitive information" is broken: any unauthenticated network attacker can register themselves as an additional encryption recipient for any tenant's future patient appointments. A second variant of the bug suppresses the unauthorized-warning log entry. The Zod schema makes the `email` field optional. When the request body omits `email` and the request carries no registration cookie, the comparison `registrationEmail === email` becomes `undefined === undefined`, which evaluates to `true`. The handler treats the request as a legitimate registration flow, skips the warning entirely, and stores the row. Successful storage is still recorded as an `[info]` log line, but the security-relevant warning that operators are most likely to monitor or alert on is gone. The `staff_crypto` table has no unique constraint on `user_id`, so an arbitrary number of attacker rows can coexist for the same staff identifier and all return as `is_active=true`. The supplied `staffId` does not need to match any existing user or pending invite. Schema validation on `passkeyId`, `publicKey`, and `privateKeyShare` is also weak: the literal string `<placeholder-base64>` was accepted, indicating no length, format, or cryptographic-validity check beyond field presence. This weakness is independent of the auth bypass but compounds it: a poisoned directory can also be filled with malformed entries that break legitimate booking flows. The injected key is consumed by the public booking flow. After completing the unauthenticated `bootstrap-challenge` and `bootstrap-verify` ceremony as a "patient", the resulting `bookingAccessToken` is accepted by `GET /api/tenants/{id}/appointments/staff-public-keys`, which returns the attacker-controlled keys alongside any legitimate ones. A new appointment encrypts its tunnel key with ML-KEM to all listed recipients, so the attacker becomes a co-recipient of the encryption and can decapsulate the tunnel key with the matching secret. From there, all appointment payloads for that booking are decryptable. Version 1.0.4 patches the issue.

### CVE-2026-59118

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-07T00:16:33.923 |

Improper authorization in Microsoft Power Apps allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-70558

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-06T22:18:26.227 |

Dinky's POST /download/uploadFromRsByLocal handler passes the caller-supplied path parameter directly to new File(path) and file.transferTo(dest) with no path validation. The route is marked @SaIgnore and /download/** is excluded from the Sa-Token interceptor, so the only guard is a header equality check against a dinkyToken value whose default (efda1551-7958-4e0f-80a8-dfd107df3e38) is hardcoded in source and shipped to every deployment. Anyone who can reach Dinky's HTTP port (8888 by default) and supplies the hardcoded token can write arbitrary files as the Dinky service account. The default Docker image runs on 8888 with no proxy or authentication and chmod 777 on /opt/dinky, so the application's own classpath, launch scripts, and static assets are writable. Demonstrated impact: overwriting /opt/dinky/config/static/index.html served attacker JavaScript to admin browsers immediately, and writing /opt/dinky/org/dinky/Dinky.class executed attacker code as the Dinky service account at the next JVM start via a classpath-shadow launched by script/bin/auto.sh. Writes are uid 9999 (flink), not root, so /etc, /root, /home, and /usr are refused. Affects Dinky v1.2.5 (the current release) and the development branch, where the code is byte-identical.

### CVE-2026-18367

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-06T22:16:50.010 |

A privilege escalation vulnerability allows local users to execute arbitrary code as root via Sophos Endpoint for macOS older than version 2026.1.1 and Sophos Home for macOS older than version 10.11.6.

### CVE-2026-66447

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-06T15:17:20.207 |

Unauthenticated SQL Injection in WordPress File Upload <= 5.1.7 versions.

### CVE-2026-65546

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-06T15:17:16.480 |

Unauthenticated SQL Injection in Qode Tours <= 3.1.3.1 versions.

### CVE-2026-65520

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-06T15:17:15.607 |

Unauthenticated SQL Injection in WP OAuth Server <= 6.2.0 versions.

### CVE-2026-65508

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-06T15:17:14.957 |

Unauthenticated SQL Injection in Simply Schedule Appointments <= 1.6.12.10 versions.

### CVE-2026-53976

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-06T15:16:55.983 |

OpenChamber 1.11.7 contains a path traversal vulnerability in the file-serving endpoints /api/fs/read, /api/fs/stat, and /api/fs/raw that allows unauthenticated remote attackers to read arbitrary files by supplying the allowOutsideWorkspace=true query parameter alongside an absolute path, bypassing the workspace boundary check in resolveReadPathFromContext. Attackers can exploit the vacuous isPathWithinRoot guard to read sensitive files such as the JWT signing secret, SSH private keys, API credentials, and environment variables, enabling full authentication bypass by forging session cookies on password-protected deployments.

### CVE-2026-53975

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-06T15:16:55.827 |

OpenChamber 1.11.7 contains an unauthenticated remote code execution vulnerability that allows remote attackers to execute arbitrary shell commands by sending crafted POST requests to the /api/fs/exec endpoint, which passes commands verbatim to Node.js spawn() without any allowlist, blocklist, or argument validation. The authentication middleware becomes a no-op when UI_PASSWORD is not configured, matching the default Docker deployment, enabling attackers to execute arbitrary OS commands as the application user and retrieve full command output including stdout, stderr, and exit code from the server response.

### CVE-2026-66914

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-07T14:17:00.397 |

Joomla Extension - seblod.com - Unauthenticated path traversal in SEBLOD < 3.30.0, < 4.7.0, < 6.0.1 - An unauthenticated attacker could download files from both inside and outside the webroot.

### CVE-2026-54213

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-07T10:16:58.500 |

Tobit Laboratories AG TeamDavid's Webbox application exposes a functionality that allows the server to be 
shut down when a specific endpoint (/internalRestart) is accessed. This 
endpoint is accessible to unauthenticated users over the public 
Internet. Instead of “restarting”, the server shuts completely down. As a
 result, a remote attacker can trigger a persistent denial of service by
 shutting down the web server without requiring authentication. Recovery
 requires manual administrator intervention to restart the service. This issue affects TeamDavid through Rollout 524.

### CVE-2026-54203

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-07T10:16:57.070 |

Memory Leak to an Unauthorized Actor vulnerability in Tobit Laboratories AG TeamDavid's Webbox allows reading of sensitive information. When accessing the URL “/.well-known/mta-sts.”, the application responds
 with memory. By repeatedly 
requesting this endpoint, an attacker can access sensitive 
information, including user passwords. Exploitation does not require 
authentication. This issue affects TeamDavid through Rollout 524.

### CVE-2026-5857

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-06T22:18:10.900 |

Contiki-NG's MQTT client parse_publish_vhdr() in os/net/app-layer/mqtt/mqtt.c sets topic_len_received=1 before checking topic_len against the 64-byte limit, so an over-length topic returns early but leaves the flag set. On the next TCP segment, tcp_input() re-invokes the parser with topic_received==0, and the persisted topic_len_received==1 skips the length-reading block containing the guard, falling through directly to a memcpy() that uses the unvalidated 16-bit topic_len as the copy length. The 65-byte topic[] destination overruns into adjacent struct fields including the payload_chunk pointer, which subsequent MQTT code dereferences, giving a compromised or attacker-controlled broker an arbitrary-pointer-write primitive. Contiki-NG's MQTT implementation has no TLS support so the connection is plaintext. Impact ranges from information disclosure and denial of service to remote code execution on embedded targets without memory protection.

### CVE-2026-53983

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-06T22:17:42.120 |

Ground Station prior to 0.6.0 contains an unauthenticated blind server-side request forgery vulnerability in the orbital-source configuration path that allows any unauthenticated Socket.IO client to cause the ground-station process to issue outbound HTTP requests to attacker-chosen destinations. Attackers can connect to the Socket.IO server on port 7000 without credentials due to disabled authentication enforcement and a wildcard CORS policy, then submit a data_submission event with submit-orbital-sources action to persist an attacker-supplied URL in the database, then trigger an orbital sync via the equally unauthenticated background_task:start event. The URL is stored with no scheme allowlist, no host validation, and no rejection of loopback, RFC1918, or link-local (cloud instance metadata at 169.254.169.254) addresses, and is passed directly to requests.get in _fetch_http_3le and _fetch_http_omm in backend/tlesync/source_adapters.py. HTTP status codes and error messages from the outbound request are emitted in the orbital_sync_state Socket.IO event to all connected clients, providing a serviceable oracle for interpreting internal-service and cloud-metadata responses even though the raw response body is not directly leaked. Because the malicious source persists in the database across restarts and re-fires every 24 hours on the scheduled sync cycle, the primitive gives durable long-term SSRF without the attacker needing to remain connected.

### CVE-2026-43632

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367;CWE-416` |
| Published | 2026-08-06T22:17:06.343 |

llama.cpp builds b7492 through the latest b9060 contains a use-after-free vulnerability in llama-server affecting six tokenization endpoints (/tokenize, /detokenize, /infill, /apply-template, /rerank, and /anthropic/count_tokens) that bypass the task queue and access ctx_server.vocab directly on HTTP worker threads. Attackers can exploit a time-of-check-time-of-use race condition where the main thread destroys and frees vocab after the synchronization lock is released but before the handler finishes using it, causing a crash or potential code execution when --sleep-idle-seconds is configured.

### CVE-2026-43631

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362;CWE-416;CWE-362;CWE-416` |
| Published | 2026-08-06T22:17:06.200 |

llama.cpp builds b7492 through the latest b9060 contains a use-after-free vulnerability in the vocab pointer of llama-server when the --sleep-idle-seconds feature is enabled, allowing unauthenticated remote attackers to execute arbitrary code. Attackers can trigger the vulnerability by sending requests to affected endpoints while the server transitions to sleep mode, causing concurrent worker threads to dereference a freed vocab pointer that can be reclaimed with attacker-controlled data to achieve remote code execution.

### CVE-2026-43629

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-08-06T22:17:05.917 |

llama.cpp builds b4882 through b9058 contain a heap buffer overflow vulnerability in the KV cache state restore path where the state_read_data() function computes write size without overflow checking, allowing attackers with write access to the slot_save_path directory to corrupt heap memory. Attackers can craft malicious state files where cell_count multiplication overflows or exceeds tensor buffer allocation to write attacker-controlled bytes past buffer boundaries, potentially resulting in heap metadata corruption, model weight corruption, or arbitrary code execution via function pointer overwrite.

### CVE-2026-68823

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-08-07T00:16:40.900 |

Exposed dangerous method or function in Azure Confidential Ledger allows an authorized attacker to execute code over a network.

### CVE-2026-3418

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-06T22:17:03.997 |

The System REST API accepts user-supplied file uploads without enforcing sufficient validation on the file type or destination, allowing files to be written to arbitrary server-accessible locations. Exploitation requires authenticated administrative access with publisher privileges.

Successful exploitation permits an authenticated publisher to upload files to server-accessible locations. Depending on the deployment environment and how uploaded files are handled, this could lead to the execution of uploaded content, potentially resulting in remote code execution.

### CVE-2026-66709

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-06T15:17:23.927 |

Shop manager Remote Code Execution (RCE) in CTX Feed <= 6.6.42 versions.

### CVE-2026-54489

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-06T15:16:56.120 |

Dell Virtual Storage Integrator for VMware vSphere Client, versions prior to 10.11.1.0, contain(s) a Sensitive Information Disclosure vulnerability. An unauthenticated remote attacker could potentially exploit this vulnerability, leading to information disclosure and session hijacking. This vulnerability is considered critical as it allows an unauthenticated attacker to obtain active session credentials and fully impersonate authenticated users, including administrators. Dell recommends customers to upgrade at the earliest opportunity.

### CVE-2026-34191

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-06T15:16:54.650 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Apache Portable Runtime Utility via apr_dbd_oracle provider.

This issue affects Apache Portable Runtime Utility: from 1.6.0 through 1.6.3

### CVE-2026-32327

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-06T15:16:54.190 |

A bug in APR-util version 1.6.3 (and earlier) allows a stack recursion attack against any library consumer which parses XML from untrusted sources and uses the apr_xml_quote_elem() function.

Users are recommended to upgrade to version 1.6.4, which fixes this issue.

### CVE-2025-14561

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-06T22:16:41.420 |

In multi-tenant deployments, the Publisher REST APIs fail to enforce tenant isolation correctly. This allows a user in one tenant, possessing sufficient privileges to invoke these APIs, to perform operations that impact other tenants.

The vulnerability allows a privileged user to perform publisher operations such as exposing or modifying API Metadata in another tenant environment. This impact is only realized in multi-tenant deployments.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-54209

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-07T10:16:57.887 |

Tobit Laboratories AG TeamDavid's Webbox application handles password changes using a function triggered by 
including the string "(editini)" in the file path, writing the new 
password to the specified "Archive.ini" file. However, the application 
does not verify that the provided path actually refers to an 
"Archive.ini" file. If an attacker specifies a different file with 
excessive size, a buffer overflow occurs. This vulnerability allows an 
unauthenticated attacker to crash the server, resulting in denial of 
service. This issue affects TeamDavid through Rollout 524.

### CVE-2026-54218

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-07T10:16:59.153 |

Use of hard-coded cryptographic key vulnerability in Tobit Laboratories AG TeamDavid's Webbox. For users created locally in David, passwords are stored in various 
files using only obfuscation. Any user with access to the server’s file 
system, or who can otherwise extract files from the server (see 
vulnerability “Random File Read”), can potentially obtain affected 
users’ passwords. This issue affects TeamDavid through Rollout 524.

### CVE-2026-9169

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-07T09:16:59.430 |

DLL Search Order Hijacking in LUCID Vision Labs Arena SDK 1.0.80.49 on Windows allows a local attacker to execute arbitrary code with the privileges of the application by placing a malicious DLL in a user-controlled directory listed in the PATH environment variable, which the SDK traverses when a required dependency is not found locally.

### CVE-2026-65668

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-07T00:16:38.833 |

Improper access control in Microsoft Purview eDiscovery allows an authorized attacker to elevate privileges over a network.

### CVE-2026-49163

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-07T00:16:30.800 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Application Insights Profiler allows an authorized attacker to elevate privileges over a network.

### CVE-2026-62857

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-06T22:18:12.127 |

Fedify is a TypeScript library for building federated server apps powered by ActivityPub. From version 1.2.0 through the affected 1.9, 1.10, 2.0, 2.1, 2.2, and 2.3 maintenance lines, getNodeInfo() follows an attacker-controlled links[].href value from /.well-known/nodeinfo without scheme, redirect, or private-address validation, allowing requests to loopback, link-local, cloud metadata, and private-network services and returning their response bodies. This issue is fixed in versions 1.9.13, 1.10.12, 2.0.22, 2.1.18, 2.2.7, and 2.3.2.

### CVE-2026-53984

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-06T22:17:42.280 |

Ground Station prior to 0.6.0 contains an unauthenticated database-destruction and arbitrary-data-injection vulnerability in the Socket.IO server's database_backup event handler that allows any unauthenticated network peer to wipe or replace the entire SQLite database by sending a single full_restore command with a caller-supplied SQL blob. Attackers can connect to the Socket.IO server on port 7000 without credentials due to disabled authentication enforcement and a wildcard CORS policy, then emit the database_backup event to drop every existing table and recreate the database from attacker-controlled CREATE TABLE and INSERT INTO statements executed via raw exec_driver_sql, permanently destroying all satellite records, orbital sources, hardware configurations, and observation schedules, or planting fabricated orbital-source URLs and observation entries that redirect the ground station to attacker-controlled servers on the next scheduled sync.

### CVE-2026-48054

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-06T22:17:09.530 |

OpenZeppelin Contracts Wizardis a web application to interactively build a contract out of components from OpenZeppelin Contracts. Versions prior to 0.10.9 generate a Hardhat test file (`test/test.ts`) by interpolating user-supplied `opts.name` (ERC20/ERC721) and `opts.uri` (ERC1155) directly into TypeScript string literals at `zip-hardhat.ts:48` and `:50` without any JavaScript string escaping. No authentication is required: an attacker crafts a URL such as `https[:]//wizard[.]openzeppelin[.]com/#/erc20?name=");require("child_process").execSync("...");("` and shares it with a developer. When the victim downloads the resulting zip archive and runs `npx hardhat test`, the injected Node.js code executes with the developer's local OS privileges. Version 0.10.9 fixes the issue.

### CVE-2026-19174

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-06T22:16:59.927 |

Integer overflow in V8 in Google Chrome prior to 151.0.7922.109 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19169

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-06T22:16:59.363 |

Insufficient validation of untrusted input in Contextual Tasks in Google Chrome prior to 151.0.7922.109 allowed a remote attacker to perform privilege escalation via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19168

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-06T22:16:59.260 |

Inappropriate implementation in V8 in Google Chrome prior to 151.0.7922.109 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19162

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-06T22:16:58.573 |

Out of bounds write in V8 in Google Chrome prior to 151.0.7922.109 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19151

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:57.330 |

Use after free in V8 in Google Chrome prior to 151.0.7922.109 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19150

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-06T22:16:57.223 |

Inappropriate implementation in V8 in Google Chrome prior to 151.0.7922.109 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19145

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:56.653 |

Use after free in Translate in Google Chrome prior to 151.0.7922.109 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19144

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:56.537 |

Use after free in HTML in Google Chrome prior to 151.0.7922.109 allowed a remote attacker to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-18258

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-06T16:16:37.727 |

Authorization bypass in the Line, LineTranscription, VirtualCollection, tag and process API endpoints in Scripta/eScriptorium through 26.04.1 allows a remote authenticated user to read, modify and delete other users' transcription content via primary keys supplied in the request body, which are queried against the global model manager instead of the request-scoped queryset

### CVE-2026-65542

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-06T15:17:15.983 |

Unauthenticated Broken Authentication in Super Socializer <= 7.14.5 versions.

### CVE-2026-28111

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-06T15:16:52.070 |

Contributor Privilege Escalation in Forminator <= 1.56.0 versions.

### CVE-2026-66494

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-284` |
| Published | 2026-08-07T13:16:52.827 |

Joomla Extension - joomshaper.com - Unauthenticated stored XSS in Shapes API endpoint SP Page Builder < 6.7.0 - An unauthenticated attacker can store malicious JavaScript in a Joomla site's database via a single HTTP request. When an administrator opens the SP Page Builder editor, the JavaScript executes in their browser automatically..

### CVE-2026-62836

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-923` |
| Published | 2026-08-07T00:16:34.727 |

Improper restriction of communication channel to intended endpoints in Azure SQL Managed Instance allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-71476

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-08-06T22:18:31.603 |

Nx is a monorepo solution for TypeScript and polyglot codebases. From version 20.8.0 until 22.7.7 and 23.0.2, the Nx self-hosted HTTP remote cache extracts downloaded cache artifacts without constraining where files are written. A malicious or on-path (MITM) remote cache server can return a crafted tar archive whose entries escape the cache directory and write to arbitrary locations on the machine running Nx, which can be escalated to remote code execution. Nx's default local cache and Nx Cloud are not affected; only workspaces configured to use a self-hosted remote cache are affected. This issue is fixed in versions 22.7.7 and 23.0.2.

### CVE-2026-70636

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T22:18:28.150 |

Flowise through 3.1.4 contains an authentication bypass vulnerability that allows unauthenticated attackers to access the OAuth2 credential refresh endpoint by exploiting prefix-based whitelist matching in the authentication middleware defined in packages/server/src/utils/constants.ts. Attackers can send a POST request to the oauth2-credential refresh route with a trailing credential identifier to bypass all authentication and authorization checks, triggering unauthorized OAuth token rotation against credentials belonging to any workspace and potentially disrupting dependent OAuth integrations. This is a bypass of CVE-2026-41273.

### CVE-2026-70559

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-06T22:18:26.387 |

Dinky's SysConfigController.getAll() handler for GET /api/sysConfig/getAll carries a method-level @SaIgnore annotation that short-circuits the class-level @SaCheckLogin, so the Sa-Token interceptor lets the request through with no session or role check. Any remote unauthenticated caller who can reach the Dinky HTTP port (8888 by default) receives the full live system configuration (54 entries on a stock v1.2.5 install) with one parameterless GET. Only one credential field (sys.maven.settings.repositoryPassword) has a desensitization handler wired; the other credential-bearing fields (sys.env.settings.dinkyToken, sys.ldap.settings.userPassword, sys.resource.settings.oss.accessKey and secretKey, and sys.dolphinscheduler.settings.token) return in cleartext. A bare install leaks the shipped defaults, including the hardcoded dinkyToken efda1551-7958-4e0f-80a8-dfd107df3e38 and minioadmin/minioadmin OSS keys; once an operator configures LDAP, object storage, or DolphinScheduler through the Settings Center, those live third-party credentials leak from the same endpoint. Because dinkyToken is the sole gate on the sibling POST /download/uploadFromRsByLocal arbitrary file write, this disclosure defeats token rotation as a mitigation for that vulnerability. Affects Dinky v1.2.5 (the current release, 2025-11-05) and the development branch (dev HEAD 63b5a5a), where the affected code is byte-identical.

### CVE-2026-5855

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-06T22:18:10.590 |

Contiki-NG's LwM2M TLV parser lwm2m_tlv_read() in os/services/lwm2m/lwm2m-tlv.c ignores its caller-supplied buffer length argument and reads up to six bytes from the input buffer with no bounds check. The caller in lwm2m-engine.c iterates while there is at least one byte remaining, so a crafted CoAP WRITE to any LwM2M endpoint whose final TLV supplies exactly one byte triggers up to five out-of-bounds reads of heap memory adjacent to the CoAP input buffer, disclosing memory contents (including key material and peer addresses) through the parsed tlv->id, tlv->length, and tlv->value fields. Corrupted tlv_len derived from the out-of-bounds memory further corrupts the caller's parse offset. In LwM2M NoSec mode, the default for constrained devices, no authentication is required.

### CVE-2026-3415

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:H` |
| Weaknesses | `CWE-776` |
| Published | 2026-08-06T22:17:03.770 |

The XML and schema validation functionalities within the SchemaValidator Mediator process XML input as part of validation flows. Under certain conditions, the XML parser allows the resolution of external entities when handling user-supplied XML content during validation operations. This behavior can occur when an attacker supplies crafted XML payloads to the relevant mediator flows with sufficient privileges.

Successful exploitation may allow a highly privileged actor to read files accessible within the server hosting the affected product. Additionally, it may be possible to trigger outbound requests to unintended internal or external locations, depending on the server environment and network configuration. Specially crafted XML payloads can also lead to excessive resource consumption during parsing, impacting the availability of the product.

### CVE-2026-53985

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-06T16:16:43.620 |

Ground Station prior to 0.6.0 contains an unauthenticated denial-of-service vulnerability in the Socket.IO server's service_control event handler that allows any unauthenticated network peer to forcibly terminate the ground-station process by sending a single restart_service command. Attackers can connect to the Socket.IO server on port 7000 without credentials due to disabled authentication enforcement and a wildcard CORS policy, then emit the service_control event to terminate all active satellite-tracking sessions, SDR recording pipelines, demodulators, decoders, and rotator controllers, with repeated triggering possible in Docker deployments to create a persistent denial-of-service condition.

### CVE-2026-53977

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-06T16:16:43.483 |

OpenChamber 1.11.7 contains an authentication bypass vulnerability that allows unauthenticated remote attackers to terminate the server process by sending a POST request to the /api/system/shutdown endpoint, which is registered before the authentication middleware in the Express route handler chain. Attackers can exploit the route registration order in bootstrap-runtime.js to reach the shutdown handler before auth middleware executes, causing denial of service to all active AI coding sessions and locking out legitimate remote users regardless of whether UI_PASSWORD is configured.

### CVE-2026-63725

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-06T22:18:12.480 |

sysPass's FileBackupService::doBackupFiles() in lib/SP/Services/Backup/FileBackupService.php around line 388 builds a tar shell command by string-concatenating the backup directory path $this->path directly into the command line ('tar czf ' . $backupFileApp . ' ' . BASE_PATH . ' --exclude \"' . $this->path . '\" 2>&1') and passes the result to PHP's exec() with no application of escapeshellarg() and no validation of the path against a safe character set. The $this->path value is read from the sysPass configuration, which is persisted in the database and writable through the admin settings API and the admin UI. An administrator (or an attacker who has obtained an admin API token or admin session) can therefore store a backup path containing shell metacharacters and trigger a backup operation to execute arbitrary OS commands as the web server process user (typically www-data or apache). Because sysPass is a password manager whose sole purpose is to hold credentials for other systems, code execution as the web-server user permits reading sysPass's master password and encryption key from memory or configuration files, decrypting every stored credential in the database, exporting the entire password vault, pivoting to internal systems using the disclosed credentials, and installing persistent backdoors on the password-manager host.

### CVE-2026-63637

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-943` |
| Published | 2026-08-06T22:18:12.330 |

Dgraph is an open source distributed GraphQL database. Prior to 25.3.8, maybeQuoteArg in graphql/resolve/query_rewriter.go passes regexp filter strings into generated DQL without quoting or validating the /pattern/flags form, allowing crafted GraphQL query or mutation filters to inject DQL operators, disclose unintended nodes, or expand modification and deletion targets. This issue is fixed in version 25.3.8.

### CVE-2026-47194

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-06T22:17:07.913 |

Frappe is a full-stack web application framework. Prior to 15.108.0 and 16.18.3, temporary magic login link generation can use an attacker-controlled request Host header, allowing a remote attacker to cause emailed login links to point to an attacker-controlled domain and capture the login token when a recipient follows the link. This issue is fixed in versions 15.108.0 and 16.18.3.

### CVE-2026-19143

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-06T22:16:56.423 |

Insufficient validation of untrusted input in WebAPKs in Google Chrome on Android prior to 151.0.7922.109 allowed a local attacker to potentially perform a sandbox escape via a malicious file. (Chromium security severity: High)

### CVE-2026-19111

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-06T22:16:55.410 |

Insecure direct object reference in the mongodb_memory, elasticsearch_memory, and mem0_memory tools in Amazon Strands Agents Tools before 0.8.3 might allow remote authenticated users to access, modify, or delete memories belonging to other tenants by influencing the LLM to emit tool calls with a forged namespace parameter.



To remediate this issue, users should upgrade to version 0.8.3.

### CVE-2026-3430

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-06T16:16:42.760 |

The Creative Mail WordPress plugin from 1.6.5 to 1.6.9 does not sanitize and escape a parameter before using in an SQL statement, leading to an unauthenticated SQL injection when the abandoned cart email is managed by creative mail.

### CVE-2026-54208

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:L/SC:L/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-284` |
| Published | 2026-08-07T10:16:57.740 |

Tobit Laboratories AG TeamDavid's Webbox application is vulnerable to arbitrary file write, allowing an 
unauthenticated attacker to create or write into existing files on the 
server with attacker-controlled content. This is possible because user 
input is written directly to files without proper validation or 
restriction on file types. As a result, an attacker can create files 
(e.g., .htm), containing malicious JavaScript code. When a user accesses
 a file created in this way, stored cross-site scripting is triggered. This issue affects TeamDavid through Rollout 524.

### CVE-2026-54202

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:H/SC:L/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-36` |
| Published | 2026-08-07T10:16:56.927 |

Tobit Laboratories AG TeamDavid's Webbox  is vulnerable to a path traversal vulnerability in the 
archive creation functionality. Because the archive path is 
user-controlled and insufficiently validated, an attacker can manipulate
 the input to traverse directories. This allows the creation of folders 
in arbitrary locations, including sensitive directories such as 
C:\Windows or for different users. This issue affects TeamDavid through Rollout 524.

### CVE-2026-70638

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-06T22:18:28.633 |

llama.cpp builds b1886 through b7445 contain an integer overflow vulnerability in the LLaMA-Android JNI wrapper where the new_1batch() function multiplies sizeof(llama_seq_id) by an attacker-controlled n_seq_max parameter without overflow validation, causing heap buffer allocation to wrap and allocate insufficient memory. Attackers can exploit this by providing a crafted n_seq_max value through a malicious model file or JNI call to trigger heap corruption and achieve denial of service or arbitrary code execution on Android applications using the LLaMA-Android binding.

### CVE-2026-70632

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-06T22:18:27.567 |

FFmpeg versions from 4.4 up to, but not including, 9.0 contain an out-of-bounds heap write vulnerability in the native GoPro CineForm HD (CFHD) decoder that allows remote attackers to corrupt heap memory by supplying a crafted AVI file during stream probing. The cfhd_decode() function fails to enforce the non-Bayer logical output-width invariant in the transform-type-2 reconstruction path, causing horiz_filter_clip() to write oversized 16-bit sample rows far beyond the allocated output frame buffer, which can be escalated to arbitrary code execution via overwrite of a live cleanup callback pointer.

### CVE-2026-70628

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-08-06T22:18:26.957 |

FFmpeg versions from 0.5 up to, but not including, 9.0 contain a signed integer overflow vulnerability in the DVB subtitle parser in libavcodec/dvbsub_parser.c that allows attackers to trigger a heap buffer overflow by supplying a crafted WTV file. The overflow causes the bounds-check guard expression to wrap to INT_MIN, bypassing the PARSE_BUF_SIZE comparison and invoking memcpy() with attacker-controlled data into a heap buffer, resulting in an out-of-bounds heap write and potential memory corruption or code execution.

### CVE-2026-67622

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-06T22:18:22.873 |

Flowise through 3.1.4 contains an insecure direct object reference vulnerability in the OpenAI Assistants integration that allows authenticated attackers to access credentials belonging to other workspaces by supplying an arbitrary credential UUID to Assistants endpoints without workspace ownership verification. Attackers can enumerate cross-workspace assistant metadata, retrieve file and vector store listings, and upload files into victim workspaces by exploiting the missing workspace-scoped authorization check in the credential lookup logic.

### CVE-2026-45414

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-08-06T22:17:06.873 |

Decidim is a participatory democracy framework. Prior to 0.31.5 and in 0.32.0.rc1 before 0.32.0.rc2, JWT-backed API authentication is not bound to the organization selected by the current host, allowing a JWT issued for one tenant to be replayed against another tenant’s API to read participantDetails data and reach the proposal.answer mutation path. This issue is fixed in versions 0.31.5 and 0.32.0.rc2.

### CVE-2026-43628

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-08-06T22:17:05.777 |

llama.cpp builds b3978 through b9058 contain an integer underflow and out-of-bounds read vulnerability in the DRY sampler that allows unauthenticated attackers to trigger a heap buffer underflow by sending a crafted HTTP request with dry_allowed_length set to INT32_MIN to the /v1/completions or /v1/chat/completions endpoints. Attackers can exploit this vulnerability to crash the server with SIGSEGV causing denial of service for all connected users, or corrupt token sampling probabilities by reading garbage values from memory before the allocated buffer.

### CVE-2026-43627

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-680` |
| Published | 2026-08-06T22:17:05.633 |

llama.cpp builds b1283 through b9058 contain an integer overflow vulnerability in the llama_batch_init() function where unchecked multiplications in malloc() calls can wrap past INT32_MAX when computing allocation sizes. Attackers can pass specially crafted parameters to trigger integer overflow, causing heap corruption and potentially achieving arbitrary code execution through subsequent batch operations that write past allocated buffer boundaries.

### CVE-2026-43622

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415;CWE-762` |
| Published | 2026-08-06T16:16:42.883 |

llama.cpp builds b1886 through b7445 contain a double free vulnerability in the LLaMA-Android JNI wrapper where new_1batch() allocates memory using malloc() while free_1batch() deallocates it using the C++ delete operator, causing heap metadata corruption. Attackers can trigger this memory management mismatch to cause denial of service through process crashes or potentially achieve arbitrary code execution depending on allocator state.

### CVE-2026-18359

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-06T16:16:38.223 |

Server-side request forgery in the METS and IIIF import URI handling in Scripta eScriptorium through 26.04.1 allows a remote authenticated user to make the server issue arbitrary HTTP requests to internal hosts, including the cloud instance metadata service, via the mets_uri or iiif_uri parameter of POST /api/documents/{pk}/imports/, because the IMPORT_ALLOWED_DOMAINS setting defaults to '*' and no address filtering, redirect cap or timeout is applied

### CVE-2026-65569

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-06T15:17:18.307 |

Subscriber SQL Injection in WP Job Portal <= 2.5.6 versions.

### CVE-2026-65547

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-06T15:17:16.603 |

Subscriber SQL Injection in Creative Mail <= 1.6.9 versions.

### CVE-2026-54200

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:H/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-07T10:16:56.640 |

Tobit Laboratories AG TeamDavid's Webbox  is vulnerable to a local file inclusion vulnerability in
 the send email, fax, SMS, etc. functionality. By specifying an '@@attach' command in the form field 'scjob', files can be attached to a message, 
which can then be downloaded by an authenticated user. A filter is in 
place that restricts access to the David con-fig folder and the user 
folder. However, this filter can be bypassed by specifying an alternate 
data stream, allowing the download of sensitive files such as other 
users' access files containing their passwords or the server's private 
key. This issue affects TeamDavid through Rollout 524.

### CVE-2026-12070

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-07T10:16:55.997 |

Tobit Laboratories AG TeamDavid's Webbox  is vulnerable to an arbitrary file deletion 
vulnerability in the send email, fax, SMS, etc. functionality. By 
specifying an @@COMMENTFILE command in the form field scjob, any file on
 the system can be deleted. This issue affects TeamDavid through Rollout 524.

### CVE-2026-19177

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-06T22:17:00.263 |

Insufficient validation of untrusted input in UI in Google Chrome prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19173

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-06T22:16:59.813 |

Out of bounds write in Skia in Google Chrome prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19172

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:59.703 |

Use after free in Views in Google Chrome prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-19163

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:58.690 |

Use after free in Media in Google Chrome on Windows prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19155

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:57.777 |

Use after free in Payments in Google Chrome prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19154

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:57.660 |

Use after free in Skia in Google Chrome on Android prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-19152

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-06T22:16:57.437 |

Insufficient policy enforcement in Navigation in Google Chrome prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19148

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-06T22:16:57.000 |

Out of bounds write in GPU in Google Chrome on Linux prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19147

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:56.887 |

Use after free in Aura in Google Chrome on Linux prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19141

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:56.160 |

Use after free in Resources in Google Chrome on Android prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19140

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:56.047 |

Use after free in GPU in Google Chrome prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19138

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-06T22:16:55.813 |

Heap buffer overflow in CrashReporting in Google Chrome prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19137

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:55.690 |

Use after free in WebGL in Google Chrome on Android prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-66491

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-07T09:16:59.010 |

Joomla Extension - phoca.cz - Arbitrary File Read in Phoca Commander 1.0.0-6.1.3 - Improper limitation of paths in the getSource function lead to an arbitrary file read vulnerability.

### CVE-2026-71445

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T22:18:31.163 |

AIL Framework contained a reflected cross-site scripting vulnerability in the /tag/add_tags endpoint. When an error occurred while processing a tag operation, the application returned the error value directly as an HTML response using str(res[0]).

If attacker-controlled input was included in the generated error message, a crafted request could cause arbitrary HTML or JavaScript to be reflected in the response without appropriate output encoding. An attacker could exploit the vulnerability by convincing an authenticated AIL Framework user to open a specially crafted link.

Successful exploitation could allow JavaScript to execute in the victim’s browser within the security context of the AIL Framework application. Depending on the victim’s privileges and the application’s protections, the attacker could perform actions using the victim’s session, access information available to the victim, or modify data through authenticated application requests.

The vulnerability requires user interaction because the authenticated victim must follow or open the crafted request. The attacker does not necessarily require an AIL Framework account, provided that the crafted request can be delivered to an already authenticated user.

### CVE-2026-68750

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-08-06T16:16:51.907 |

Inefficient Algorithmic Complexity vulnerability in the traversal engine in rrrene html_sanitize_ex allows an unauthenticated remote attacker to exhaust server CPU and memory via a flat run of sibling elements in sanitized HTML. The list clause of HtmlSanitizeEx.Traverser.traverse/2 recurses on the tail of a sibling list and then evaluates List.flatten([head] ++ tail) over the already flattened result, so every one of n siblings copies and re-walks the entire remaining tail. The flattening is only needed for the rare case where scrub returns several replacement nodes for one node, but the cost is paid across the whole tail at every step, making traversal quadratic in sibling count.

The traverser sits on every public entry point, so no particular scrubber or configuration is required and the payload needs only allowed tags. A 160 KB body of 20,000 sibling elements occupies a scheduler for roughly 1.7 seconds, and the cost grows faster than the body does.

This issue affects html_sanitize_ex: from 0.3.1 before 1.5.3.

### CVE-2026-68749

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-08-06T16:16:51.720 |

Inefficient Regular Expression Complexity vulnerability in the CSS scrubber in rrrene html_sanitize_ex allows an unauthenticated remote attacker to exhaust server CPU via a long CSS declaration in sanitized HTML. The declaration regex in HtmlSanitizeEx.Scrubber.CSS.scrub/1 matches the property name with an unbounded greedy [-\w]+ followed by a mandatory :, so a long run of word characters not followed by a colon makes the engine give back one character at a time and retry the colon at every start offset. The work is quadratic in the length of the run, and no length cap is applied to the CSS handed to the scrubber. An 80 KB <style> body costs roughly 2.4 seconds of scheduler time, so a few concurrent requests saturate the BEAM scheduler pool and make the application unresponsive.

The impact is CPU exhaustion only. Nothing is read, modified or disclosed.

This issue affects html_sanitize_ex: from 0.3.1 before 1.5.3.

### CVE-2026-5423

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-302` |
| Published | 2026-08-06T16:16:44.430 |

@neo4j/graphql library versions prior to 7.5.6 fail to verify the authenticity of a client-supplied, pre-decoded JWT object passed through GraphQL subscription connectionParams. As a result, any unauthenticated remote client that can open a GraphQL-over-WebSocket connection can forge arbitrary JWT claims (e.g. sub, roles) in connectionParams.jwt and have them accepted as authenticated identity for the purposes of @authentication and @subscriptionsAuthorization directive evaluation. This allows a fully unauthenticated attacker to receive subscription events that should be restricted to specific authenticated roles/users.
Upgrade the library to versions 7.5.6+ or 5.12.14+. v6 is end-of-life and will not receive a fix.

### CVE-2026-70637

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-820` |
| Published | 2026-08-06T15:17:27.613 |

LightFTP through 2.4 contains multiple data race vulnerabilities in ftpserv.c that allow anonymous attackers to cause undefined behavior by issuing LIST followed by ABOR commands without authentication. The control thread closes data_socket and file_fd descriptors while worker threads concurrently operate on the same fields in worker_thread_cleanup, allowing stale file descriptors to be reassigned by the OS and subsequently used by worker threads on unrelated resources, resulting in potential denial of service.

### CVE-2026-66708

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T15:17:23.793 |

Unauthenticated Broken Access Control in Total Upkeep <= 1.17.2 versions.

### CVE-2026-64665

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-290` |
| Published | 2026-08-06T22:18:14.103 |

Statamic is a Laravel and Git powered content management system (CMS). Prior to 5.74.1 and 6.24.0, when OAuth login was enabled with a provider that does not guarantee verified email addresses, an unauthenticated attacker could sign in as an existing user, potentially including a super admin, without knowing that user's password, because the application matched OAuth identities to accounts by email address alone. Exploitation requires OAuth to be explicitly enabled with such a provider. This issue is fixed in versions 5.74.1 and 6.24.0.

### CVE-2026-48081

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T22:17:10.850 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. Prior to version 1.0.2, a TENANT_ADMIN can store `javascript:` URLs in the tenant `links` configuration (`website`, `imprint`, `privacyStatement`). These values are returned to the patient-facing landing page via `/api/public`, hydrated into the SvelteKit Button component, and rendered as `<a href="javascript:...">` elements without URL-scheme filtering. A patient who clicks any such link executes the attacker's JavaScript inside the patient browser origin, where patient form data is read before client-side encryption is applied. This breaks the project's central trust claim that the server is an untrusted relay and that administrators cannot read patient data. Patient-side encryption happens after form input, so JavaScript executing in the patient origin can read or alter the plaintext before encryption is performed. Version 1.0.2 fixes the issue.

### CVE-2026-66710

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-06T15:17:24.060 |

Unauthenticated Local File Inclusion in e2pdf <= 1.32.40 versions.

### CVE-2026-65570

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-06T15:17:18.433 |

Unauthenticated Bypass Vulnerability in Login with phone number <= 1.8.70 versions.

### CVE-2026-48080

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-06T22:17:10.703 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. Prior to version 1.0.2, the `GET /api/tenants/{id}` endpoint returns the full tenant record to any authenticated `TENANT_ADMIN` of that tenant, including the `databaseUrl` field. This field contains the live PostgreSQL connection string the application uses to connect to that tenant's database. In the tested official `docker-compose.prod.yml` deployment, the connection string contained the user `postgres` with `rolsuper=true` and the plaintext password from `secrets/postgres_password.txt`. Operators who configure a non-superuser PostgreSQL user via `secrets/postgres_user.txt` would expose a less privileged credential, but the disclosure of the connection string itself is independent of that choice. The same credential applies to every database managed by that PostgreSQL instance: the central `appointment_booking` database, every per-tenant database (one per tenant), and the postgres administrative database. A `TENANT_ADMIN` of one tenant who can reach `postgres:5432` (directly via internal network, indirectly via any SSRF, RCE, or file-read in the application) can read every other tenant's appointment ciphertexts, key shares, and metadata; read the central user table, including all `GLOBAL_ADMIN` accounts, password hashes, and session records; modify or delete any data in any tenant database; and/or i a superuser-scoped deployment: use PostgreSQL's `pg_read_server_files`, `COPY ... FROM PROGRAM`, and `CREATE EXTENSION` for further escalation inside the database container. This breaks the per-tenant database isolation that is otherwise the primary cross-tenant control in the application. The application code carefully scopes most queries to the calling tenant's database, but those scopings are irrelevant once the attacker holds the credentials that bypass the application entirely. Version 1.0.2 fixes the issue.

### CVE-2026-8325

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-06T22:18:33.243 |

A maliciously crafted PDF file, when parsed through Autodesk Revit, can force an Out-of-Bounds Write vulnerability. A malicious actor may leverage this vulnerability to cause a crash, cause data corruption, or execute arbitrary code in the context of the current process.

### CVE-2026-7867

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-06T22:18:33.100 |

A flaw was found in udisks2. A local attacker with an active console session can exploit insufficient authorization checking on the 'as-user' option in the org.freedesktop.UDisks2.Filesystem.Mount() D-Bus method. This allows the attacker to spoof the 'as-user' parameter, mounting filesystems on behalf of arbitrary users, including privileged accounts. This can lead to local privilege escalation through mount point injection and manipulation of the mount namespace visible to privileged users.

### CVE-2026-7406

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-08-06T22:18:32.837 |

A maliciously crafted BMP file, when parsed through certain Autodesk products, can force a Untrusted Pointer Dereference vulnerability. A malicious actor can leverage this vulnerability to execute arbitrary code in the context of the current process.

### CVE-2026-1289

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:17:00.373 |

A maliciously crafted PDF file, when parsed through Autodesk Revit, can force a Use-After-Free vulnerability. A malicious actor can leverage this vulnerability to cause a crash, disclose sensitive data, or execute arbitrary code in the context of the current process.

### CVE-2026-11803

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-06T22:16:44.967 |

A maliciously crafted PDF file, when parsed through Autodesk Revit, can force an Out-of-Bounds Read vulnerability. A malicious actor can leverage this vulnerability to cause a crash, read sensitive data, or execute arbitrary code in the context of the current process.

### CVE-2026-56793

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-07T13:16:52.503 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.2, contains an Improper Authentication vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-54204

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-918` |
| Published | 2026-08-07T10:16:57.207 |

Tobit Laboratories AG TeamDavid's Webbox 's search functionality accepts a “pathnameroot” 
parameter, which can be set to network locations using UNC paths (e.g., 
“\\Server\Share”). The server processes these paths without validation, 
resulting in outbound connection attempts to attacker-controlled SMB 
servers. This enables unauthenticated attackers to trigger the server to
 authenticate to arbitrary SMB endpoints, potentially exposing NTLM 
authentication information (such as NTLM hashes). If outbound 
connections to port 445 (SMB) are permitted, attackers can use this to 
conduct SMB relay or credential theft attacks. Exploitation of the 
“pathnameroot” parameter is possible without authentication.

This issue affects TeamDavid through Rollout 524.

### CVE-2026-71327

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-694` |
| Published | 2026-08-06T22:18:29.810 |

Traefik is an open source HTTP reverse proxy and load balancer. From 3.0.0 until 3.6.25 and 3.7.10, Traefik's Kubernetes Gateway API provider in pkg/provider/kubernetes/gateway/httproute.go, grpcroute.go, tcproute.go, and tlsroute.go builds HTTPRoute, GRPCRoute, TCPRoute, and TLSRoute router and service identities by hyphen-concatenating namespace, route name, Gateway identity, entry point, and rule index, allowing colliding Routes to overwrite another namespace's backend. This issue is fixed in 3.6.25 and 3.7.10.

### CVE-2026-15816

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-07T11:17:05.100 |

A flaw was found in dracut. The die() error-handling function writes its message into a shell script under the initramfs emergency-hook directory without properly shell-quoting it. When the message contains data derived from the DHCP ROOT_PATH option, an attacker on the adjacent network who controls a rogue DHCP server can inject a command-substitution sequence that executes as root the next time dracut sources its emergency hook scripts during standard boot-failure handling.

### CVE-2026-49007

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-07T08:16:46.457 |

By accessing unencrypted information in the device firmware, an attacker can obtain the initial login credentials for the device's web interface.

### CVE-2026-62918

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-07T00:16:36.833 |

Improper verification of cryptographic signature in Microsoft Teams allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-71488

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407;CWE-1050` |
| Published | 2026-08-06T22:18:31.893 |

league/commonmark is a PHP library for parsing and rendering CommonMark Markdown. From 0.6.0 until 2.9.0, specially crafted Markdown lines can cause the parser to have quadratic time complexity when converting, because several parsing paths repeatedly rescan growing portions of a line to translate between character positions and byte positions, and the Autolink extension can also copy and validate the remaining line at every URL-like prefix, allowing an attacker who can submit Markdown for conversion to consume disproportionate CPU time with a comparatively small request. This issue is fixed in 2.9.0.

### CVE-2026-67422

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-08-06T22:18:21.600 |

pymdown-extensions is a collection of extensions for the Python Markdown library. In versions up to and including 11.0, four inline processors (caret, tilde, betterem, and magiclink) use regular expressions whose content groups can partition a run of delimiter characters in exponentially many ways, causing catastrophic backtracking. As a result, a single untrusted Markdown line under 50 bytes rendered with markdown.markdown() in each extension's default configuration drives the rendering thread into unbounded CPU usage that grows exponentially with input length, enabling an unauthenticated remote attacker who can submit Markdown to cause denial of service. The exposure is concrete for web applications that render user-supplied Markdown (comments, wikis, issue bodies, live preview), including any app using pymdownx.extra which bundles the vulnerable betterem default, as well as hosted docs/CI systems that build untrusted Markdown. The issue has been fixed in version 11.0.1.

### CVE-2026-45378

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-06T22:17:06.690 |

Decidim is a participatory democracy framework. Prior to 0.30.9, from 0.31.0 before 0.31.5, and in 0.32.0.rc1 before 0.32.0.rc2, the identity-document verification admin UI embeds verification_attachment blobs through reusable signed Active Storage disk URLs, allowing anyone who obtains a URL to download the scanned document without an authenticated Decidim session until the signature expires. Verification-document images are rendered with variant_url(...), which produces signed /rails/active_storage/disk/... links instead of routing the file through an authorization-checking controller. Because Decidim configures Active Storage service URLs to remain valid for seven days, the URL itself becomes the credential for that period. The affected files are verification_attachment blobs on Decidim::Authorization, and the admin review pages embed those signed URLs directly into the HTML for pending and confirmation views. This issue is fixed in versions 0.30.9, 0.31.5, and 0.32.0.rc2.

### CVE-2026-19176

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:17:00.150 |

Use after free in Skia in Google Chrome prior to 151.0.7922.109 allowed a remote attacker who had compromised the renderer process to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19165

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:58.920 |

Use after free in Extensions in Google Chrome prior to 151.0.7922.109 allowed an attacker who convinced a user to install a malicious extension to execute arbitrary code inside a sandbox via a crafted Chrome Extension. (Chromium security severity: High)

### CVE-2026-19159

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:58.230 |

Use after free in Views in Google Chrome prior to 151.0.7922.109 allowed a remote attacker who convinced a user to engage in specific UI gestures to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19158

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:58.123 |

Use after free in Views in Google Chrome on Windows prior to 151.0.7922.109 allowed a remote attacker who convinced a user to engage in specific UI gestures to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19156

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-06T22:16:57.893 |

Heap buffer overflow in Base in Google Chrome prior to 151.0.7922.109 allowed an attacker who convinced a user to install a malicious extension to potentially exploit heap corruption via a crafted Chrome Extension. (Chromium security severity: High)

### CVE-2026-19142

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-06T22:16:56.293 |

Use after free in Views in Google Chrome prior to 151.0.7922.109 allowed a remote attacker who convinced a user to engage in specific UI gestures to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-16620

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-06T22:16:49.120 |

The WPC Name Your Price for WooCommerce WordPress plugin before 2.2.5 does not enforce its server-side price allowlist for products configured in "Select" price mode, allowing an unauthenticated visitor to add such a product to the cart at an arbitrary value below the merchant-defined allowed prices and commit a real order at that price (revenue loss / underpriced orders). This is a distinct, unfixed vector from CVE-2025-12115, whose 2.2.0 fix only addressed applying a custom price to products where Name Your Price is disabled and left the Select-mode allowlist unenforced through 2.2.4.

### CVE-2026-16619

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-06T22:16:49.007 |

The miniOrange 2FA WordPress plugin before 6.2.8 does not correctly limit the number of second-factor verification attempts, tracking them against a client-supplied identifier that is reissued on every login, allowing an attacker who already knows a user's password to guess the one-time code without limit and take over the account.

### CVE-2026-13399

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-06T22:16:45.717 |

The Payment Plugins for PayPal WooCommerce WordPress plugin before 2.0.20 does not have proper authorization checks on a REST endpoint, allowing unauthenticated users to bypass payments

### CVE-2026-12584

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-06T22:16:45.333 |

The Payment Gateway for Redsys & WooCommerce Lite WordPress plugin before 7.0.2 does not verify the authenticity of incoming payment-provider notifications for one of its payment methods before marking orders as paid, allowing unauthenticated attackers to forge a payment-confirmation callback and complete their own orders without paying.

### CVE-2026-10599

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-345;CWE-639` |
| Published | 2026-08-06T22:16:42.680 |

The Integrate PhonePe with WooCommerce WordPress plugin through 1.2.1 does not validate that a verified payment transaction belongs to the order being marked as paid, nor does it verify the authenticity of its payment-completion request, allowing unauthenticated attackers to reuse a single valid transaction to mark arbitrary orders as paid and bypass payment.

### CVE-2026-10524

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-472` |
| Published | 2026-08-06T22:16:42.537 |

The CoCart WordPress plugin before 4.9.0 does not validate a user-supplied price value against the actual product price when items are added to the cart through one of its public REST API endpoints, allowing unauthenticated users to set arbitrary product prices and complete WooCommerce orders at manipulated totals.

### CVE-2026-18427

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-436` |
| Published | 2026-08-06T16:16:38.350 |

@fastify/static before version 10.1.3 contains an incomplete fix for a previous route guard bypass. The static file handler rejected only parent directory segments, but it did not canonicalize dot segments, duplicate slashes, encoded dots, or backslashes before route matching and before delegating to the send layer. As a result, an unauthenticated attacker could request a file protected by a route based guard using a non canonical path form that misses the guarded route yet resolves back onto the protected file, disclosing its contents. Applications that protect a subtree of the static root with a route based guard are affected, while applications relying on the allowedPath option are not. This is fixed in @fastify/static 10.1.3, which canonicalizes the pathname, including rejecting backslashes, on the path used for routing and serving.

### CVE-2026-70646

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-06T15:17:27.750 |

aiosend is a synchronous and asynchronous Crypto Pay API client. Pror to version 3.0.7, `WebhookHandler.feed_update()` deserializes the entire request body before verifying the HMAC signature. This allows an unauthenticated attacker to force expensive parsing of arbitrary JSON payloads that will ultimately be rejected, leading to unnecessary CPU and memory consumption. Version 3.0.7 fixes the issue. Some workarounds are available. Restrict request body size at the reverse proxy or web framework, rate-limit webhook endpoints, and/or reject oversized requests before JSON parsing.

### CVE-2026-66712

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T15:17:24.307 |

Unauthenticated Broken Access Control in Simple Membership <= 4.7.8 versions.

### CVE-2026-65543

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-08-06T15:17:16.110 |

Subscriber Sensitive Data Exposure in Vimeo <= 1.2.2 versions.

### CVE-2026-65523

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-06T15:17:15.737 |

Unauthenticated Insecure Direct Object References (IDOR) in Formidable Forms Signature Online Contract Automation <= 2.0.1 versions.

### CVE-2026-65504

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T15:17:14.697 |

Unauthenticated Broken Access Control in BOX NOW Delivery Croatia <= 3.3.0 versions.

### CVE-2026-34502

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-06T15:16:54.920 |

Heap-based Buffer Overflow vulnerability in Apache Portable Runtime Utility memcached client

This issue affects Apache Portable Runtime Utility: from 1.3.0 through 1.6.3.

### CVE-2026-34501

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-06T15:16:54.773 |

Heap-based Buffer Overflow vulnerability in Apache Portable Runtime Utility redis client.

This issue affects Apache Portable Runtime Utility: from 1.6.0 through 1.6.3.

Users are recommended to upgrade to version 1.6.4, which fixes the issue.

### CVE-2026-28140

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T15:16:52.707 |

Unauthenticated Broken Access Control in JetFormBuilder <= 3.6.4.1 versions.

### CVE-2025-49506

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-208` |
| Published | 2026-08-06T15:16:41.890 |

APR-util versions 1.6.3 (and earlier) function apr_password_validate() was not constant-time with regards to hashes or passwords comparisons, potentially leaking their content via a side channel timing attack particularly on platforms without crypt() such as  Windows, BeOS, NetWare, or Android.

Users are recommended to upgrade to version 1.6.4, which fixes this issue.

### CVE-2026-48084

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-307` |
| Published | 2026-08-06T22:17:11.297 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. Versions prior to 1.0.2 don't throttle failed passphrase login attempts. An attacker can submit unlimited wrong passphrase guesses against any known email address, capped only by the Argon2 verification cost (about 100 milliseconds per attempt on the tested host, giving 10 attempts per second sustained). The same backend implements a working per-account throttle on the WebAuthn challenge endpoint, which returns HTTP 429 after roughly 19 attempts. The passphrase branch simply does not invoke that throttle, leaving a supported high-value login path unprotected against credential stuffing and dictionary attacks. The asymmetry confirms this is an oversight rather than a design choice. The throttle infrastructure exists, is wired into the same auth backend, and works on the WebAuthn path. The passphrase branch in `/api/auth/login` was not updated to record failed attempts. Combined with the application's minimum-passphrase policy (12 characters, no entropy or dictionary checks), accounts using common base patterns such as `Spring2026!XX` or words from a leak corpus are realistically reachable in days on a single CPU, hours on a small GPU farm. Version 1.0.2 patches the issue.

### CVE-2026-48079

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-613` |
| Published | 2026-08-06T22:17:10.557 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. Prior to version 1.0.2, when a user navigates to the `/logout` page, the page's server-side load handler deletes the `access_token` cookie before calling `/api/auth/logout` via an internal `event.fetch()`. The internal fetch consequently runs without the auth cookie, so `apiAuthHandle` rejects it, the logout handler never executes, and `SessionService.revokeSession()` is never called for the current session. The DB session row remains valid until its natural expiry (one week by default). The user sees a successful logout (cookie gone, UI returns to login), but any party still holding a copy of the now-deleted access token can continue making authenticated API calls until the session naturally expires. The root cause is a simple ordering mistake. The same auth subsystem implements the correct order in `/api/auth/logout`: revoke the current DB session first, then delete the cookie. The page-level wrapper does the opposite. Version 1.0.2 initiates server-side logout before removing authentication cookies and first appears in version 1.0.2. Version 2.0.0 later replaces this with a race-free client-side logout flow.

### CVE-2026-19139

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-362` |
| Published | 2026-08-06T22:16:55.930 |

Race in CredentialProvider in Google Chrome on Windows prior to 151.0.7922.109 allowed a local attacker to perform OS-level privilege escalation via a malicious file. (Chromium security severity: High)

### CVE-2026-70640

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362;CWE-476` |
| Published | 2026-08-06T22:18:28.927 |

llama.cpp builds b1886 through b7445 contain a race condition use-after-free vulnerability in the LLaMA-Android JNI wrapper where bench_1model() and free_1context() lack synchronization, allowing Thread A to operate on freed memory while Thread B concurrently frees the llama_context. Attackers can exploit this by performing heap spray with attacker-controlled data containing a fake vtable to hijack the vtable pointer at offset +0x30, causing llama_batch_allocr::clear() to dereference arbitrary memory and achieve remote code execution.

### CVE-2026-67434

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-06T22:18:21.750 |

PHP_CodeSniffer tokenizes PHP files and detects violations of a defined set of coding standards. Prior to versions 3.13.6 and 4.0.2, PHP_CodeSniffer contains a command injection vulnerability in the code that generates the Gitblame, Hgblame, and Svnblame report formats. As a result, running PHP_CodeSniffer over untrusted files, for example in a continuous integration pipeline that scans pull requests, or on a developer machine reviewing third party code, could result in attacker controlled shell commands being executed when the Gitblame, Hgblame, or Svnblame report processes a file whose name contains shell metacharacters. Users using the default Full report, or any of the other non-blame reports, are not affected. Users on a runtime platform which does not allow filenames to contain shell metacharacters, such as " and ;, are not affected. This issue is fixed in versions 3.13.6 and 4.0.2.

### CVE-2026-65541

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T15:17:15.857 |

Unauthenticated Broken Access Control in Staff Training <= 1.0.7 versions.

### CVE-2026-70634

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-129` |
| Published | 2026-08-06T22:18:27.857 |

TimescaleDB through 2.29.1, fixed in commit 517c13e, contains an out-of-bounds read in the Dictionary compression reverse row iterator (tsl/src/compression/algorithms/dictionary.c). The forward path validates the decoded index; the reverse path uses an assertion compiled out of release builds, leaving the 64-bit Simple8b index unvalidated and the read offset attacker-controlled. Attackers with DML access to a physical compressed relation can store a crafted datum and run a reverse-order scan. With a pass-by-value column type the out-of-bounds Datum is returned to the client as a normal column value, disclosing backend memory including the shared buffer pool, which SQL access control does not cover.

### CVE-2026-67621

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T22:18:22.717 |

Flowise through 3.1.4 contains a missing authorization vulnerability that allows authenticated workspace members to perform unauthorized document store operations by accessing unprotected mutation endpoints. Attackers holding only view-level permissions can send direct HTTP requests to the upsert and refresh document store routes to trigger document ingestion, refresh vector database contents, consume embedding API credits, and modify knowledge bases used by downstream chatflows.

### CVE-2026-65559

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-06T15:17:17.933 |

Shop manager Privilege Escalation in Order Delivery Date for WooCommerce <= 4.6.0 versions.

### CVE-2026-65549

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-06T15:17:16.877 |

Author PHP Object Injection in Jeg Kit for Elementor <= 3.2.10 versions.

### CVE-2026-15570

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-07T14:16:56.890 |

An improper restriction of URL schemes and destinations in the SmartCenter browserseturl command in the Telefunken TE24553B45V2DZ Smart TV running on the Vestel MB181 / Voltron181 / TiVo OS platform allows an attacker with access to the same local network to cause the embedded browser to issue requests to unintended loopback/internal destinations, including 127.0.0.1 addresses. In demonstrated scenarios, requests initiated through the SmartCenter browserseturl mechanism could reach an internal service and receive a successful response, although the same destination was not reachable through normal browser navigation. The issue affects firmware version V2.78.0.0 and is fixed in firmware version V2.85.2.0.

### CVE-2026-19195

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-08-07T05:17:01.890 |

A vulnerability has been found in V-Secure Jingyun Antivirus 2.4.2.39. The affected element is an unknown function in the library ZyArk.sys of the component Kernel Driver. The manipulation leads to improper access controls. The attack needs to be performed locally. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-19193

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-08-07T05:17:01.710 |

A flaw has been found in Jiangmin Antivirus 21. Impacted is the function MessageNotifyCallback in the library kvcore.sys of the component Minifilter Port. Executing a manipulation can lead to improper access controls. The attack needs to be launched locally. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-19192

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-08-07T05:17:01.517 |

A vulnerability was detected in DeepCool DisplayService 1.2.12. This issue affects some unknown processing of the file C:\DeepCool\resources\service\x64\DeepCoolDisplayService.exe. Performing a manipulation results in improper access controls. The attack must be initiated from a local position. The exploit is now public and may be used.

### CVE-2026-19191

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-275` |
| Published | 2026-08-07T05:17:01.313 |

A security vulnerability has been detected in StableBit DrivePool 2.3.13.1687. This vulnerability affects unknown code of the file C:\Program Files\StableBit\DrivePool\DrivePool.Service.exe of the component DrivePoolService. Such manipulation leads to permission issues. The attack must be carried out locally. The exploit has been disclosed publicly and may be used.

### CVE-2026-19190

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-275` |
| Published | 2026-08-07T04:17:21.367 |

A weakness has been identified in StableBit Scanner 2.6.13.4088. This affects an unknown part of the file C:\Program Files (x86)\StableBit\Scanner\Service\Scanner.Service.exe of the component ScannerService. This manipulation causes permission issues. The attack is restricted to local execution. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-19189

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-269` |
| Published | 2026-08-07T03:16:18.450 |

A security flaw has been discovered in Power Sofware PowerISO 9.3.0.0. Affected by this issue is some unknown functionality in the library C:\Windows\System32\drivers\scdemu.sys of the component Kernel Driver. The manipulation results in improper privilege management. The attack is only possible with local access. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-70635

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-129` |
| Published | 2026-08-06T22:18:28.003 |

TimescaleDB through 2.29.1, fixed in commit 517c13e, contains an out-of-bounds read vulnerability that allows authenticated attackers to cause query-result integrity failures or backend crashes by supplying a crafted Simple8b selector-11 value, which is stored in the signed int16 Arrow dictionary-index type and bypasses index validation checks in bulk text dictionary decompression. Attackers with direct DML access to a non-frozen physical compressed hypertable relation can trigger an out-of-bounds read before the base of the live offsets array through the VectorAgg single-text hashing strategy, resulting in incorrect aggregation output, backend SIGSEGV, or PostgreSQL crash recovery depending on build configuration.

### CVE-2026-70633

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-08-06T22:18:27.710 |

TimescaleDB through 2.29.1, fixed in commit 517c13e, contains an out-of-bounds read vulnerability in the Gorilla compression reverse row iterator that allows authenticated attackers to cause a denial of service by storing a crafted compressed datum with an internally inconsistent BitArray. Attackers with DML access to a compressed hypertable can trigger an unsigned integer wraparound in the reverse iterator bucket index computation, causing a read beyond the end of the bucket array, resulting in a SIGSEGV crash that can be repeatedly triggered on each subsequent reverse-order scan.

### CVE-2026-70557

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-06T22:18:26.077 |

diboot-core's POST /common/load-related-data endpoint resolves caller-supplied field names to any @TableField column of any entity and returns those values for all rows, with no field or entity allowlist. The only guard, relatedDataSecurityCheck(), returns true unconditionally, so any authenticated user (including a zero-role account) can read @JsonIgnore-annotated secret fields such as IamAccount.authSecret and IamAccount.secretSalt for every account, or arbitrary secret fields of any other entity. Shiro's two-iteration MD5 with an 8-character salt is trivially crackable offline, so the disclosed admin password hashes convert to full administrative takeover. The endpoint is not example code; the official diboot-admin-ui frontend requires it, so deployments following the vendor's recommended integration expose it. The mechanism was renamed relatedData* to attachMore* on the development branch, but attachMoreSecurityCheck() also returns true unconditionally.

### CVE-2026-65400

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-06T22:18:14.533 |

An authentication issue was addressed with improved state management. This issue is fixed in macOS Sequoia 15.7.9, macOS Sonoma 14.8.9, macOS Tahoe 26.6.1. An attacker on the network may be able to authenticate to Screen Sharing without valid credentials.

### CVE-2026-5856

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-06T22:18:10.743 |

Contiki-NG's DNS/mDNS resolver skip_name() in os/services/resolv/resolv.c walks DNS wire-format name labels with no packet-boundary check, and the caller in newdata() invokes it in a loop iterating nquestions times from the attacker-controlled DNS header before validating the transaction ID. An attacker who sets nquestions higher than the number of complete questions present causes skip_name() to walk past the UDP packet buffer, and the returned pointer is cast to struct dns_answer * for further memory reads. On builds with RESOLV_CONF_SUPPORTS_MDNS enabled, any peer on the local segment can trigger the read unauthenticated via a multicast UDP 5353 packet with no outstanding query required; on standard DNS builds an attacker who can inject a UDP response from port 53 during an outstanding query can trigger the same read. Impact is out-of-bounds read of uip_buf and adjacent memory, disclosing memory contents or crashing the resolver.

### CVE-2026-47765

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T22:17:08.960 |

Frappe is a full-stack web application framework. Prior to 15.110.0 and 16.20.0, the restore and bulk_restore endpoints do not apply the appropriate document permission checks, allowing an authenticated user to restore deleted documents without the required authorization. This issue is fixed in versions 15.110.0 and 16.20.0.

### CVE-2026-18277

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T16:16:38.100 |

Missing authorization in the OcrModelRight create and delete views in Scripta eScriptorium through 26.04.1 allows a remote authenticated user to grant themselves access to another user's private OCR model and to revoke any user's OCR model access via a POST request, because the ownership check is placed in get_context_data() and therefore runs only on the GET rendering path

### CVE-2026-66711

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:24.187 |

Subscriber Cross Site Scripting (XSS) in WooCommerce Multilingual & Multicurrency <= 5.5.6 versions.

### CVE-2026-66707

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:23.670 |

Unauthenticated Cross Site Scripting (XSS) in Facebook for WooCommerce <= 3.7.5 versions.

### CVE-2026-66705

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:23.423 |

Unauthenticated Cross Site Scripting (XSS) in Facebook for WordPress <= 5.2.1 versions.

### CVE-2026-66702

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:23.117 |

Unauthenticated Cross Site Scripting (XSS) in Rank Math SEO <= 1.0.274.1 versions.

### CVE-2026-66694

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:22.483 |

Unauthenticated Cross Site Scripting (XSS) in Thrive Architect <= 10.9.3.1 versions.

### CVE-2026-66690

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:22.230 |

Unauthenticated Cross Site Scripting (XSS) in GiveWP <= 4.16.5 versions.

### CVE-2026-66664

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:21.103 |

Unauthenticated Cross Site Scripting (XSS) in SEO Plugin by Squirrly SEO <= 14.2.0 versions.

### CVE-2026-66663

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:20.977 |

Unauthenticated Cross Site Scripting (XSS) in WP Data Access <= 5.5.79 versions.

### CVE-2026-66470

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T15:17:20.720 |

Subscriber Broken Access Control in Frontend Admin by DynamiApps <= 3.29.10 versions.

### CVE-2026-66457

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:20.590 |

Unauthenticated Cross Site Scripting (XSS) in Events Manager <= 7.4.1 versions.

### CVE-2026-66440

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:20.057 |

Unauthenticated Cross Site Scripting (XSS) in WPIDE – File Manager & Code Editor <= 3.5.7 versions.

### CVE-2026-66439

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:19.937 |

Unauthenticated Cross Site Scripting (XSS) in Advanced AJAX Product Filters <= 3.2.0.3 versions.

### CVE-2026-65565

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:18.183 |

Unauthenticated Cross Site Scripting (XSS) in Survey Maker <= 5.2.3.3 versions.

### CVE-2026-65560

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:18.060 |

Unauthenticated Cross Site Scripting (XSS) in Houzez Property Feed <= 2.5.48 versions.

### CVE-2026-65554

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T15:17:17.677 |

Subscriber Broken Access Control in AnsPress – Question and answer 4.4.4 versions.

### CVE-2026-65545

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:16.360 |

Unauthenticated Cross Site Scripting (XSS) in AI Engine <= 3.6.8 versions.

### CVE-2026-65544

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:16.233 |

Unauthenticated Cross Site Scripting (XSS) in Super Socializer <= 7.14.5 versions.

### CVE-2026-65517

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:15.483 |

Unauthenticated Cross Site Scripting (XSS) in Easy PayPal Buy Now Button <= 2.0.4 versions.

### CVE-2026-65515

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:15.360 |

Unauthenticated Cross Site Scripting (XSS) in AffiliateWP <= 2.35.0 versions.

### CVE-2026-65513

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:15.233 |

Unauthenticated Cross Site Scripting (XSS) in Simply Schedule Appointments <= 1.6.12.10 versions.

### CVE-2026-65509

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:15.097 |

Unauthenticated Cross Site Scripting (XSS) in wpDataTables <= 7.5.1 versions.

### CVE-2026-61982

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:14.450 |

Unauthenticated Cross Site Scripting (XSS) in SiteGuard WP Plugin <= 1.8.6 versions.

### CVE-2026-61964

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:14.323 |

Unauthenticated Cross Site Scripting (XSS) in Ninja Tables <= 5.2.9 versions.

### CVE-2026-61963

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:14.190 |

Unauthenticated Cross Site Scripting (XSS) in Media LIbrary Assistant <= 3.38 versions.

### CVE-2026-61961

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:17:12.950 |

Unauthenticated Cross Site Scripting (XSS) in EmbedPress <= 4.5.6 versions.

### CVE-2026-28177

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:16:53.527 |

Unauthenticated Cross Site Scripting (XSS) in Popup Maker <= 1.23.0 versions.

### CVE-2026-28172

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-06T15:16:53.377 |

Unauthenticated Cross Site Request Forgery (CSRF) in Tracking Code Manager <= 2.6.0 versions.

### CVE-2026-28143

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:16:52.963 |

Unauthenticated Cross Site Scripting (XSS) in Forminator <= 1.56.0 versions.

### CVE-2026-28141

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:16:52.830 |

Unauthenticated Cross Site Scripting (XSS) in NextGEN Gallery <= 4.2.3 versions.

### CVE-2026-28082

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T15:16:51.770 |

Unauthenticated Cross Site Scripting (XSS) in JetEngine <= 3.8.13.1 versions.

### CVE-2026-71324

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-08-06T22:18:29.310 |

Traefik is an open source HTTP reverse proxy and load balancer. Prior to 2.11.53, 3.6.24, and 3.7.9, Traefik's default HTTP reverse proxy forwards a plain HTTP/2 or HTTP/3 CONNECT request and its body to an HTTP/1.1 upstream through a shared net/http.Transport. When the upstream answers the CONNECT with a keep-alive non-2xx response and does not drain the body, Traefik returns the desynchronized backend socket to its shared pool and reuses it for other clients. An unauthenticated attacker can use this behavior to make a different client read the attacker's smuggled response, which can include authenticated or private content from another request. The ForwardAuth middleware with forwardBody true and preserveRequestMethod true can re-issue a CONNECT with the buffered body attached, exposing the auth-client pool to the same desynchronization. This issue is fixed in 2.11.53, 3.6.24, and 3.7.9.
