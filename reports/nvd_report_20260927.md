# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-26 15:01 UTC
- **対象期間**: `2026-09-25T15:00:31.000Z` 〜 `2026-09-26T15:01:47.000Z`
- **重要CVE数**: 206 件（Critical 9.0+: 21 件 / High 7.0〜: 185 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **OS コマンドインジェクション・任意ファイルアップロード・認証バイパス** といった、リモートから直接コード実行や権限取得が可能になる脆弱性が目立ちます。  
- 多くは **オープンソース CMS／プラグイン（MediaWiki、WordPress、Flarum）** や **サーバ管理パネル（Froxlor）** に起因し、デフォルト設定のまま運用している環境での被害が拡大しやすい点が共通しています。  
- いずれも **アップストリームでのパッチがすでにリリース** されているケースが多数で、速やかなバージョン更新と設定見直しが最優先です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑100382** | 10.0 | MediaWiki ExternalData 拡張で OS コマンドインジェクション | **最高スコア (10.0)**。外部データ取得時に任意コマンドが実行でき、サーバ全体の乗っ取りが可能。MediaWiki を多数のサイトで共通利用しているため、被害範囲が広い。 |
| **CVE‑2026‑18143** | 9.8 | WooCommerce 「Request a Quote」プラグインで任意ファイルアップロード | WordPress + WooCommerce は EC サイトの事実上の標準。アップロードバリデーション不備により、PHP シェル等をサーバに配置できる。プラグインは 2.9.2 まで全バージョンが対象。 |
| **CVE‑2026‑92161** | 9.8 | FriendsOfFlarum OAuth の Discord プロバイダーがメール検証をスキップ | Flarum はフォーラム系 SaaS で広く採用。Discord OAuth が **未検証メール** を信頼できるユーザーとして扱うため、任意アカウント取得が可能。 |
| **CVE‑2026‑100716 / CVE‑2026‑100714** | 9.4 | Froxlor のデータエクスポート・Let’s Encrypt 設定でパス走査・コマンドインジェクション | サーバ管理パネル自体が攻撃対象になる珍しいケース。特権ユーザーが設定ミスすると、任意ファイル書き込みやシェル実行が可能。 |
| **CVE‑2026‑100706** | 9.4 | Kyverno (Kubernetes ポリシーエンジン) の URL エンコードバイパス | マルチテナント環境で **名前空間横断** が可能になるため、クラウドネイティブ環境全体の分離が崩壊。K8s クラスタ運用者は必須で対策が必要。 |

> **共通点**：いずれも「入力検証不備」や「デフォルト設定の緩さ」に起因し、**外部から直接コード実行や権限昇格** が可能になる点が危険です。  

---

## 3. 推奨アクション  

### 3.1 パッケージ・プラグインの即時アップデート
| 製品 / パッケージ | 現行脆弱バージョン | 修正バージョン (最低) | アップデート手順のポイント |
|-------------------|-------------------|----------------------|----------------------------|
| **MediaWiki ExternalData Extension** | < 3.7 | **3.7.0 以上** | `composer require mediawiki/externaldata:^3.7` もしくは公式拡張ページから最新版をダウンロードし、`LocalSettings.php` の `wfLoadExtension('ExternalData');` を更新。 |
| **WooCommerce – Request a Quote** | ≤ 2.9.2 | **2.9.3** 以降 | WordPress 管理画面 → プラグイン → 「Request a Quote」→「更新」または公式 ZIP を手動上書き。アップロードディレクトリのパーミッションを `0755` 以下に保つ。 |
| **FriendsOfFlarum OAuth** | < 1.7.4 / < 2.0.0‑beta.4 | **1.7.4** もしくは **2.0.0‑beta.4+** | `composer update fof/oauth`。Discord プロバイダーの `verified` フィールドチェックが追加されたバージョンへ。 |
| **Froxlor** | ≤ 2.3.10 (DataDump) / ≤ 2.3.11 (Let’s Encrypt) | **2.3.12** 以上 | `apt-get update && apt-get install froxlor=2.3.12-1`（Debian/Ubuntu 系）または公式インストーラで上書き。`system.letsencryptchallengepath` の正規表現制約が追加されたことを確認。 |
| **Kyverno** | < 1.19.1 | **1.19.1** 以上 | `kubectl apply -f https://github.com/kyverno/kyverno/releases/download/v1.19.1/install.yaml`。`apiCall.urlPath` のパーセントエンコード検証が修正。 |
| **その他（参考）** | | | |
| MediaFlow Proxy | ≤ 2.4.9 | **2.4.10+** | `/proxy` ルートの `d` パラメータ検証ロジックを最新に。 |
| Zammad | < 7.1.2 | **7.1.2** 以上 | SSO 連携時のメールマッチングロジックが強化。 |
| OpenClaw (npm) | < 2026.8.1 | **2026.8.1+** | `npm install openclaw@latest`。TLS ピン留めと DNS 解決の二重チェックが追加。 |

### 3.2 設定・運用上のベストプラクティス
1. **入力バリデーションの徹底**  
   - OS コマンドやシェルスクリプトに渡す文字列は必ずエスケープ／サニタイズし、ホワイトリスト方式で許可する。  
2. **最小権限の原則**  
   - Web アプリは **web‑user**（例: `www-data`）だけが書き込み可能なディレクトリに限定し、`chmod 755` 以上にしない。  
   - Kubernetes では `Pod

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-100382

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-25T22:17:10.150 |

Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in Wikimedia Foundation Mediawiki - ExternalData Extension allows OS Command Injection.

This issue affects Mediawiki - ExternalData Extension: from * before 3.7.

### CVE-2026-18143

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-26T07:17:02.017 |

The Request a Quote for WooCommerce plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.9.2 via the `afrfq_submit_quote_via_popup()` function. This is due to missing file extension and MIME type validation in the popup upload handler, which uses the raw attacker-supplied filename directly as the destination for `move_uploaded_file()`. This makes it possible for unauthenticated attackers to upload executable files, such as PHP files, to a web-accessible temporary RFQ upload directory when a public quote rule with the multi-page popup flow is enabled.

### CVE-2026-92161

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-25T16:17:29.387 |

FriendsOfFlarum OAuth allows users to log in to Flarum with GitHub, Twitter, Facebook, and other providers. Prior to 1.7.4 and 2.0.0-beta.4, the Discord OAuth provider does not check the verified field returned for an OAuth email before passing the address to Flarum core as trusted through provideTrustedEmail(). When Discord sign-in is enabled, an unauthenticated attacker who knows the email address of a Flarum user can configure a Discord account with that unverified address and a verified phone number, then sign in to cause Flarum to match the trusted address, link the attacker-controlled Discord identity to the existing user, and authenticate as the victim without a password or victim interaction. Exploitation requires that the victim's email address is not already associated with a Discord account, and it can compromise administrator accounts. Other bundled providers were not confirmed to be practically exploitable by this method because their relevant authentication flows return only verified or confirmed email addresses. This issue is fixed in versions 1.7.4 and 2.0.0-beta.4.

### CVE-2026-100716

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-26T14:16:57.583 |

Froxlor is a server administration panel. In versions 2.3.10 and earlier, the customer data-export (DataDump) cron fails to validate intermediate path components of the export destination: Froxlor\FileDir::makeCorrectDir() contains an off-by-one in its path-component walk that skips the first segment below the customer home directory, and the guard in ExportCron.php checks only the final component with is_link(). An authenticated customer whose account has the export feature enabled can schedule an export into a genuine subdirectory of their own webspace, then replace an intermediate path component with a symlink before the root-owned cron runs. The cron's `chown -R` then recursively changes ownership of the linked directory tree — for example /etc — to the customer's UID, yielding host root and cross-tenant compromise. Exploitation is deterministic and requires no race. This is an incomplete fix of GHSA-75h4-... The issue is fixed in Froxlor 2.3.12.

### CVE-2026-100714

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-26T14:16:57.240 |

Froxlor before 2.3.12 does not restrict or escape the system.letsencryptchallengepath setting: unlike sibling settings hardened in GHSA-33mp, the field has no string_regexp or required_otp guard, and its value is concatenated unescaped into the acme.sh command line built in lib/Froxlor/Cron/Http/LetsEncrypt/AcmeSh.php and executed by the root cron via FileDir::safe_exec. Because safe_exec only blacklists shell metacharacters such as ; | & > < \ $ ~ ?, spaces and quotes survive and the value is word-split into additional acme.sh arguments. An administrator, or any actor able to write settings (for example through the settings-import API), can therefore inject acme.sh options such as --renew-hook, --pre-hook or --post-hook to obtain arbitrary command execution as root at the next Let's Encrypt cron run, or use --config-home/--cert-home for arbitrary file writes. Versions up to and including 2.3.10 are affected; the issue is fixed in 2.3.12.

### CVE-2026-100706

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-441` |
| Published | 2026-09-26T14:16:55.843 |

kyverno before 1.19.1 fails to properly validate URL-encoded path segments in Policy apiCall urlPath, allowing namespace tenants to bypass the per-namespace clamp and create objects in other namespaces as the admission-controller ServiceAccount. Attackers can exploit this by using percent-encoded directory traversal sequences to create MutatingWebhookConfiguration objects cluster-wide or PolicyException objects in the kyverno namespace, enabling privilege escalation to cluster admin.

### CVE-2026-48482

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-25T19:16:55.180 |

GLPI is a free asset and IT management software package. From 11.0.0 until 11.0.8, a form administrator can use Form import with a crafted illustration or scene identifier that traverses outside the intended custom-asset directory. The imported file can be written to an executable server location, allowing a malicious script to be invoked remotely. This issue is fixed in version 11.0.8.

### CVE-2026-94130

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-26T14:17:00.880 |

Joomla Extension - joomlaboat.com - Unauthenticated SQL injection in YouTube Gallery extension < 5.7.3 - An SQL injection vulnerability in video search functionality and sorting allowed attackers to inject SQL commands in read queries.

### CVE-2026-100720

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-26T14:16:58.230 |

Froxlor 2.0.0 through 2.3.10 is vulnerable to stored cross-site scripting. When a customer (the lowest-privileged authenticated role) uploads an SSL certificate for one of their own domains, the Certificates API add()/update() methods parse it with openssl_x509_parse() and store the issuer organization (issuer['O']) value verbatim without sanitization. Froxlor's table-listing renderer then emits scalar cells through Twig's `raw` filter, disabling HTML auto-escaping, so when an administrator or reseller opens Domains > SSL certificates the attacker-supplied issuer value executes as script in the privileged user's session. This crosses a privilege boundary from customer to admin and can result in full administrator account takeover; because a Froxlor admin controls webserver, DNS, and PHP configuration applied by a cron job running as root, the issue can be further escalated to command execution as root on the managed server. The issue is fixed in Froxlor 2.3.12.

### CVE-2026-97064

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-09-25T19:17:59.427 |

X-SpringBoot through 6.0 ships with a hardcoded static master login verification code 172839 enabled by default in the database seed. Unauthenticated attackers can authenticate as any user by submitting the public master code to the emailOrMobileLogin endpoint with a known email or mobile number.

### CVE-2026-97063

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-25T19:17:59.267 |

X-SpringBoot through 6.0 returns login verification codes in HTTP responses from unauthenticated endpoints GET /sys/mobile/code and GET /sys/email/code without sending them to account owners. Attackers can request codes using known mobile numbers or email addresses, read them from responses, and authenticate as victims via POST /sys/emailOrMobileLogin/login to hijack accounts.

### CVE-2026-100684

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-26T14:16:52.720 |

Budibase versions 3.41.0 before 3.45.0 contain an authentication bypass in the OIDC/SSO login path of @budibase/server. In sso.authenticate, when no existing user matches the incoming SSO subject, the server looks up pending user invites by the IdP-asserted email address alone — without validating an invite code and without an email_verified check (the email_verified gate protects only the existing-account lookup). An attacker who can register at an IdP that the tenant trusts for OIDC and assert a victim's invited email address (even with email_verified=false) claims the pending invite and inherits all of its granted privileges, including builder and admin.global, with no admin exclusion. This results in takeover of the invited principal and, for admin invites, full tenant compromise (access to all apps, datasources including production credentials, and automations); the invite is consumed, denying onboarding to the legitimate invitee.

### CVE-2026-100607

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-26T14:16:40.983 |

Flowise through 3.1.4 resolves SSO and local-password users solely by email without storing provider or subject identifier bindings, allowing attackers to authenticate as any existing user by claiming their email at any configured SSO provider. Attackers can gain complete account access including chatflows, credentials, and API keys by authenticating through a different SSO provider or local password than the victim's original registration method.

### CVE-2026-100606

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-26T14:16:40.820 |

Flowise through 3.1.4 (Enterprise/platform mode with SSO enabled) contains an authentication bypass in the SSO login path. When an SSO callback arrives with an email matching a user whose status is INVITED, verifyAndLogin (SSOBase.ts:80-94) copies the user record from the database — including the server-stored single-use invitation tempToken — into the data passed to AccountService.register(). The register handler's token lookup, email match, and expiry checks therefore pass trivially against the server's own token instead of a caller-supplied one, and the account and its organization membership are flipped to ACTIVE. As a result, anyone able to authenticate at any configured SSO provider using a pending invitee's email address as the email claim can take over that invitation and obtain the invited user's access to the organization without ever possessing the emailed invitation token, for as long as the invitation is valid (24 hours by default). At the time of the advisory no patched version was available.

### CVE-2026-100389

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-25T21:17:22.483 |

GestSup versions before 3.2.61 contain a remote code execution vulnerability in the basic IMAP connector's attachment handling that fails to skip blocked file extensions. Unauthenticated attackers can send emails with PHP attachments to monitored mailboxes, which are written to the web-accessible upload/ticket directory and executed when accessed.

### CVE-2026-100390

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-25T21:17:22.637 |

Zoraxy versions 3.2.3 through 3.3.4 fail to properly parse IPv6 addresses in the RemoteAddr field when setting forwarded headers. Unauthenticated attackers connecting over IPv6 can supply arbitrary X-Forwarded-For values to spoof their source IP and bypass authorization provider IP-based access controls.

### CVE-2026-84458

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-25T19:17:57.130 |

Zammad is a web based open source helpdesk/customer support system. Prior to 7.1.2, when the "Automatic account link on initial logon" setting is enabled, Zammad binds an incoming third-party (SSO) identity to an existing local account by matching the email address the identity provider reports, without verifying that the provider actually confirmed ownership of that email. An attacker who controls any identity at a configured provider, including, by default, any Azure AD tenant via Zammad's multi-tenant Microsoft 365 /common app registration, can set that identity's email to a victim's address, authenticate, and be logged in as the victim. This bypasses the victim's local password entirely and affects any existing account, including agents and administrators. Zammad will honor the xms_edov ID token claim when email verification is required in the Microsoft 365 setting, treating a missing claim as unverified. This issue is fixed in version 7.1.2.

### CVE-2026-62262

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-25T16:17:26.750 |

Piwigo is a full featured open source photo gallery application for the web. In 17.0.0beta1 and earlier, when rating is enabled, an unauthenticated guest can call pwg.images.filteredSearch.create with a crafted ratings[] value and then open the returned search URL. include/ws_functions/pwg.images.php stores the unvalidated value in the search rules, and include/functions_search.inc.php integer-casts only the lower rating bound while concatenating the raw value as the SQL upper bound. This allows error-based or blind extraction of database information and database-dependent time delays through the public search flow. No fixed version is available as of this review.

### CVE-2026-42322

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-25T16:17:25.420 |

Piwigo is a full featured open source photo gallery application for the web. Prior to 16.4.0, admin/themes_standard_pages.php validates uploaded logo content by MIME type but reuses the attacker-controlled extension from std_pgs_logo when constructing the stored filename. An authenticated administrator can upload image content with a server-executable final extension, causing the file to be placed in the web-accessible logo directory and executed when requested if the web server handles that extension. This can permit arbitrary command execution, data disclosure, modification, persistence, and service disruption. This vulnerability is fixed in 16.4.0.

### CVE-2026-39353

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-98;CWE-693;CWE-732` |
| Published | 2026-09-25T16:17:25.053 |

InvoicePlane is a self-hosted open source application for managing invoices, clients, and payments. Prior to 1.7.2-rc-1, InvoicePlane builds its permitted template list by scanning a PHP template directory that can be written through an administrator-controlled file-write capability. A malicious PHP file placed in the directory is automatically trusted by Mdl_templates and can be selected as public_invoice_template. When a public invoice is rendered, the guest View controller includes the trusted file and executes it with web-server privileges. This issue is fixed in version 1.7.2-rc-1.

### CVE-2026-100551

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-26T03:17:01.487 |

OpenClaw for iOS versions >= 2026.7.1 and < 2026.8.11 do not enforce saved Gateway TLS pins in the Control UI. While native connections enforced the saved Gateway fingerprint, the authenticated Terminal and session Dashboard WebViews omitted it. If a user had accepted a Gateway fingerprint, an attacker able to redirect the same host and port and present a different certificate that is accepted by iOS system trust can serve a replacement Control UI page; opening the Terminal or a session Dashboard then allows that page to read the injected Gateway token or password. The stolen credential can grant operator access, including reading sensitive Gateway state and invoking host-capable tools. This issue is fixed in 2026.8.11.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-100683

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-26T14:16:52.567 |

Budibase (@budibase/server) before 3.45.0 builds MySQL and MSSQL column-rename DDL in packages/backend-core/src/sql/sqlTable.ts by interpolating identifiers directly into a raw query string (backtick-quoted for MySQL, a single-quoted sp_rename literal for MSSQL) without applying the project's quoteMySqlIdentifier / quoteSqlServerIdentifier helpers. An attacker with DDL rights on a connected MySQL/MSSQL datasource can create a column whose name contains a backtick (MySQL) or single quote (MSSQL) plus additional SQL; Budibase's schema introspection stores the name verbatim, and when a Budibase builder later renames that column through the UI (POST /api/tables with _rename.old), the embedded quote character terminates the identifier and the injected SQL is executed. Because the MySQL connection is opened with multipleStatements: true, stacked statements run as Budibase's datasource user, allowing arbitrary reads, writes, or destructive operations on the connected database outside Budibase's row/table permission model. Fixed in 3.45.0.

### CVE-2026-100567

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-26T03:17:03.737 |

OpenClaw is an agent gateway distributed as the npm package 'openclaw'. In versions >= 2026.4.5 and < 2026.8.1, the Gateway validated a single DNS resolution result for a configured remote Chrome DevTools Protocol (CDP) hostname, but the raw WebSocket and Playwright transports performed a later, independent DNS resolution, discarding the DNS pinning enforced at validation time. An attacker who controls an approved CDP hostname or its DNS answers can exploit this check-then-use gap via DNS rebinding to make the Gateway connect to a loopback, private, link-local, cloud metadata, or other SSRF-policy-denied address. The impact depends on the remote CDP configuration, DNS timing, and the services reachable from the Gateway host. The issue is fixed in 2026.8.1; as a mitigation, disable hostname-based remote CDP endpoints or restrict them to trusted, stable infrastructure.

### CVE-2026-100676

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-26T14:16:51.577 |

January, the media proxy/embed service of stoatchat (stoatchat/stoatchat), before version 0.15.5 improperly resolves SVG <image href> values as local filesystem paths when a fetched resource is served as image/svg+xml. An unauthenticated remote attacker who causes the service to proxy an attacker-hosted SVG (e.g. via the /proxy endpoint) can determine whether local files exist through observable response-time differences, and can cause supported local image files to be disclosed after re-encoding. Because each referenced file is read in full with no effective limit on the number or total volume of reads, a single request can also generate an unbounded amount of local filesystem I/O and memory pressure (the published proof of concept drives about 4.34 GB of reads), leading to denial of service. The issue is fixed in 0.15.5.

### CVE-2026-100597

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-26T03:17:08.337 |

OpenClaw (npm package 'openclaw') before 2026.7.1 is vulnerable to a time-of-check time-of-use race condition in OpenShell local mirror filesystem mutation operations. The remove, mkdir, and rename operations could act on a different filesystem target after OpenClaw completed its sandbox path-safety check, if the path is changed concurrently. An attacker able to win the race can cause a sandboxed operation to delete, create, or rename a host path outside the intended mirror root with the permissions of the OpenClaw process user. This does not require an operator to have granted host filesystem access outside the sandbox. The issue is fixed in 2026.7.1.

### CVE-2026-96795

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-25T23:16:55.020 |

Horilla is an HR and CRM software. Prior to 2.0.0, HorillaListView.export_data in horilla_views/generic/cbv/views.py accepts an authenticated user's columns POST parameter, takes field_tuple[1], interpolates it into dynamic_fn_str as Python source, and passes the generated function definition to exec(). A crafted string that remains valid under ast.literal_eval can inject Python syntax into a default argument evaluated during function definition, allowing arbitrary operating-system commands to execute with the application process privileges, including root privileges in the shipped Docker image. This issue is fixed in version 2.0.0.

### CVE-2026-100391

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-25T21:17:22.800 |

MediaFlow Proxy through 2.4.9 contains a server-side request forgery vulnerability in the /proxy routes due to missing and incomplete destination validation in the d query parameter. Remote attackers can supply arbitrary internal URLs including loopback and cloud metadata endpoints to read full responses from the proxy server.

### CVE-2026-61525

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-25T18:17:29.030 |

Zammad is a web based open source helpdesk/customer support system. In 7.0.2 and 7.1.0, zammad's session management for websocket and long-polling connections is susceptible to a path traversal attack. Session identifiers supplied by the client are insufficiently validated before being used to construct internal file paths. When the file-based session store is active (the default configuration), an authenticated attacker can manipulate the session identifier to reference locations outside the intended storage directory, leading to the deletion of arbitrary files and directories on the server. Exploitation requires only a low-privilege authenticated session and a single crafted request. Instances configured to use the Redis-based session store are not affected. This issue is fixed in versions 7.0.3 and 7.1.1.

### CVE-2026-94445

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-25T17:17:19.963 |

A malicious txtar could escape the intended execution context and force arbitrary writes to the playground host's trusted filesystem.



Disjointly, one of the three possible paths to invoke go vet on the playground host did not correctly restrict the execution environment. This permitted a Go process to make a read for an environment configuration file rooted in the playground host's $HOME.



Together, a well-crafted go env file and the go vet invocation could lead to remote code execution in the playground host itself.




This does not affect users of go.dev/play directly; however, it may affect independent deployments of golang.org/x/playground.

### CVE-2026-96812

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-668` |
| Published | 2026-09-25T15:17:57.097 |

Improper Exposure of Resource to Wrong Sphere in the host file helper (gofer) in Google gVisor prior to commit 573a9e73cf844f on Linux platforms with CUSE enabled allows a local attacker with container image deployment privileges to achieve root code execution on the host system. By including a /dev/cuse character device node in a container image, opening the device passes through to the host, allowing the sandboxed attacker to register a host device and exploit CUSE unrestricted ioctl handling to overwrite root udev helper memory.

### CVE-2026-100711

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-26T14:16:56.743 |

froxlor versions before 2.3.12 fail to invalidate existing panel sessions, API keys, and 2FA trust cookies when a user password is changed. Attackers holding hijacked sessions, valid API keys, or 2FA trust tokens retain full account access after password rotation, bypassing incident response actions.

### CVE-2026-100700

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-26T14:16:55.007 |

nodemailer before 10.0.6 contains a denial of service vulnerability in the addressparser free-text fallback regex pattern that exhibits quadratic backtracking behavior. Attackers can supply crafted email header values with long whitespace-free runs to block the Node.js event loop for tens of seconds, causing service unavailability.

### CVE-2026-100692

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-26T14:16:53.860 |

Hugo is a static site generator. In versions after v0.123.0 and before v0.166.0, Hugo's symlink confinement checks stopped at the mount root itself, so a theme or module checked into themes/ (or a vendored module) could contain a symlink at a mount root (for example themes/mytheme/assets -> /some/dir/outside). Files behind such a symlink were readable during a site build through resources.Get, resources.Match and similar functions, and could be published to public/ via static mounts, bypassing the rule that theme and module mount sources must be local paths. Modules fetched via Go modules are not affected because Go module zips cannot contain symlinks, and this is not an escalation for the main project, which may already mount absolute paths by configuration. Fixed in v0.166.0, where symlinked mount roots and symlinked directories between the mount root and the module directory are treated as non-existent for all modules. As a workaround, inspect themes/ and vendored modules for symlinks at mount roots before building, or replace symlinks with explicit mounts.

### CVE-2026-100690

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-26T14:16:53.560 |

Hugo versions from v0.161.0 through v0.165.0 run Node.js tools (css.PostCSS, css.TailwindCSS, js.Babel) under the Node.js permission model to restrict file system reads to the project directory and configured mounts. Because the Node.js permission model validates only the lexical path and follows symbolic links that point outside the allowed set, Hugo did not detect symlinks escaping the sandbox. An attacker who can contribute content to a Hugo project (for example via a pull request) can commit a symlink such as assets/css/x.css -> /etc/passwd together with a PostCSS plugin that reads it, allowing any file readable by the Hugo build process to be disclosed and potentially embedded in the published site. This affects builds using the default security configuration; projects that do not invoke Node.js tools are unaffected. Fixed in v0.166.0, which scans allowed paths and fails the build when a symbolic link resolves outside them.

### CVE-2026-100689

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-26T14:16:53.420 |

GitPython before 3.1.62 does not validate the `path` field read from an untrusted .gitmodules file when updating submodules. While a prior fix (GHSA-hmq2-w58f-27jc) added Submodule._validated_name() to constrain the `name` field, and GitPython's own containment guard Submodule._to_relative_path() is applied in add() and move(), Submodule.update() derives the absolute checkout location from the raw `path` value without that guard. A .gitmodules entry containing directory traversal components (e.g., path = ../../../tmp/escaped) can therefore cause directories to be created via os.makedirs() outside the repository working tree, populated from the submodule URL on the clone path, and removed via shutil.rmtree() when force_remove is used. Exploitation requires an application flow that updates submodules at a non-HEAD commit (such as a historical-commit API); the common clone-then-update flow re-derives the path from a canonical tree lookup and is not affected. The issue is fixed in GitPython 3.1.62.

### CVE-2026-100682

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-26T14:16:52.433 |

Budibase Server before 3.45.0 contains an arbitrary file write vulnerability in the PWA icon upload endpoint that extracts user-supplied ZIP archives without proper symlink validation. Attackers with BUILDER role can craft a malicious ZIP with leaf symlink entries followed by duplicate file entries to write arbitrary files as root, enabling remote code execution.

### CVE-2026-100672

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-26T14:16:50.970 |

The Comments plugin (getgrav/grav-plugin-comments) for Grav CMS through version 1.2.10 registers an admin handler that returns comment data as JSON without any authentication check. The handler branches on isAdmin(), which only indicates that the admin service is registered on the current route rather than that the visitor is authenticated, and it echoes the JSON and calls exit() during the plugins stage, before the classic Admin plugin would render its login screen. On a site using the classic Admin plugin with Comments enabled (the default), an unauthenticated remote attacker can request /admin/comments/page:<n> (e.g. page:0.001) and retrieve every comment from the last 7 days, including each commenter's email address and the absolute server filesystem path of the data file. Sites running the Grav 2.0 Admin Next stack (admin2 + api) are not affected via this path. The issue is fixed in 1.2.11, which requires an authenticated user with admin.comments or admin.super and removes the absolute filePath from the response.

### CVE-2026-100670

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-26T14:16:50.583 |

Grav CMS 2.0.14 through 2.0.24 contains a privilege escalation vulnerability in the group and account blueprints. The access map is gated by a `security@: admin.super` guard that is resolved by the field's exact path, so a submitted flat dot-notation key such as `access.admin.super` (instead of the nested `access[admin][super]`) matches no blueprint rule, survives BlueprintSchema::filterArray() and flattening, and is written by FlexObject::update() via setNestedProperty(), which splits on `.` and reconstructs the nested value. An authenticated backend operator using the flex accounts backend who holds admin.users but not admin.super can therefore grant admin.super to their own account or to a group they belong to and escalate to full super-admin, gaining control over configuration, plugin and theme installation, the file manager, and all accounts. Fixed in 2.0.25, which drops any dotted key whose ancestor path is disabled or marked validate.ignore.

### CVE-2026-100669

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-09-26T14:16:50.427 |

Grav before 2.0.25 ships web server configuration samples whose access-control deny rules are matched case-sensitively. In webserver-configs/web.config (IIS), every deny rule (user_sensitive_folders, user_accounts, user_data, user_error_redirect, user_pages, system, vendor, ignore_folders) sets ignoreCase="false" on its URL Rewrite <match> element, overriding the IIS default of ignoreCase="true"; because these are rewrite matches rather than <requestFiltering> elements, there is no case-insensitive fallback. On IIS running over case-insensitive NTFS, an unauthenticated remote attacker can vary the case of a folder name or file extension (for example GET /user/CONFIG/system.YAML) so that no deny rule matches and the IIS static file handler resolves and returns the underlying file, disclosing sensitive data such as configuration secrets or account password hashes. Whether a bypassed file is actually returned depends on MIME registration: .json is served by default, while .yaml/.yml return HTTP 404.3 on a stock IIS unless a YAML MIME mapping has been added. The same class of gap exists in the bundled webserver-configs/lighttpd.conf, whose user/(config|env), directory, script-extension, root-file and dotfile rules lack the (?i) modifier, though it is lower risk because lighttpd typically runs on case-sensitive filesystems. Deployments served by Apache (.htaccess), nginx, Caddy, or the PHP built-in server are not affected. The issue is fixed in 2.0.25; because the .htaccess installer heal does not touch web.config or lighttpd.conf, operators must re-copy the corrected sample files after upgrading.

### CVE-2026-100665

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-26T14:16:49.677 |

Netty versions from 4.2.11.Final before 4.2.18.Final contain an incomplete hostname verification fix in the QUIC certificate verification path when using a plain X509TrustManager. The BoringSSLCertificateVerifyCallback discards the SSLEngine for plain trust managers, preventing endpoint identification from running even when HTTPS verification is configured. Attackers on the network path can present a certificate chain for the wrong hostname that the plain trust manager accepts, bypassing hostname authentication for QUIC clients.

### CVE-2026-100664

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-26T14:16:49.540 |

Netty's HTTP/3 codec (io.netty:netty-codec-http3) versions 4.2.2.Final through 4.2.17.Final builds the HTTP/3 :authority pseudo-header from the HTTP/1 Host header before considering the authority of an absolute-form HTTP/1 request-target. In HttpConversionUtil.toHttp3Headers(HttpMessage, boolean) — reached via Http3FrameToHttpObjectCodec(false) — a non-empty Host header takes precedence over the request-target authority, contrary to the HTTP/1.1 rule that a server receiving an absolute-form request-target must ignore the Host header. In a Netty-based HTTP/1-to-HTTP/3 gateway, proxy, or protocol bridge, a remote client can send a request such as "GET https://trusted.example/admin HTTP/1.1" with "Host: attacker.example", causing components that validate, authorize, or route on the RFC-defined request-target authority to reach a different decision than the upstream HTTP/3 peer, which receives :authority derived from the conflicting Host header. This authority confusion can affect virtual-host routing, allow-list checks, backend selection, cache keys, and URL generation. The advisory reports integrity impact only (no code execution, memory corruption, or availability impact). Fixed in 4.2.18.Final.

### CVE-2026-100663

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-26T14:16:49.400 |

Netty's HTTP/3 codec (io.netty:netty-codec-http3) from 4.2.2.Final through 4.2.17.Final does not special-case HTTP/1 CONNECT authority-form request-targets when converting HTTP/1 messages to HTTP/3 in HttpConversionUtil.toHttp3Headers. The authority-form target (e.g., "CONNECT trusted.example:443") is parsed as a URI, so its host is emitted as :scheme, :path is set to "/", and the HTTP/1 Host header is used as :authority; if no Host header is present the CONNECT target is dropped. In a Netty-based HTTP/1-to-HTTP/3 proxy or gateway, a remote client can send a CONNECT request whose Host header names a different authority than the request-target, producing a malformed HTTP/3 CONNECT whose tunnel :authority is attacker-controlled. This can bypass tunnel allow-lists, egress policy, backend selection, or audit controls that validate the HTTP/1 CONNECT request-target before forwarding over HTTP/3. The issue is fixed in 4.2.18.Final.

### CVE-2026-100662

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-26T14:16:49.257 |

Netty's HTTP/3 codec (io.netty:netty-codec-http3) versions 4.2.0.Final through 4.2.17.Final contain an uncontrolled resource consumption vulnerability in the QPACK encoder-stream instruction decoder (QpackEncoderHandler, installed on the peer-initiated unidirectional QPACK encoder stream, type 0x02). The handler accepts an attacker-declared string-literal length of up to Integer.MAX_VALUE (~2 GiB) for the Name Length and Value Length fields of the "Insert With Literal Name" instruction (RFC 9204 §4.3.3), with no per-instruction or per-literal length cap and no cumulation-size limit; the existing HTTP/3 limits (maxHeaderListSize, maxUnknownFramePayloadLength, DEFAULT_MAX_FIELD_SECTION_SIZE) are not applied to this handler. A remote, unauthenticated peer with an established HTTP/3 connection to a default Netty HTTP/3 server can declare a very large literal length and then trickle fewer bytes than declared, causing the ByteToMessageDecoder MERGE cumulator to retain and grow the per-connection buffer, and ultimately triggering a large byte-array allocation. This leads to unbounded per-connection heap growth and OutOfMemoryError, resulting in denial of service. Fixed in 4.2.18.Final.

### CVE-2026-100661

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-26T14:16:49.110 |

Netty's HTTP/3 codec (io.netty:netty-codec-http3) versions 4.2.0.Final through 4.2.17.Final contain a denial-of-service vulnerability in the QPACK prefixed-integer decoder (QpackUtil.decodePrefixedInteger), which does not bound the number of continuation bytes it will process. A remote, unauthenticated peer can open a QPACK unidirectional stream (type 0x02 encoder or 0x03 decoder) and send a first byte with all prefix bits set (e.g. 0xFF for a 7-bit prefix or 0x3F for a 5-bit prefix) followed by an endless run of 0x80 continuation bytes. The decoder returns -1 ('need more bytes'), so callers never consume the input, the ByteToMessageDecoder cumulator grows without bound, and each decode() invocation re-scans the whole accumulated buffer, yielding O(N^2) CPU cost. The result is unbounded per-connection heap growth (OutOfMemoryError) and event-loop CPU starvation, reachable in every configuration. Fixed in 4.2.18.Final.

### CVE-2026-100660

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-26T14:16:48.970 |

Netty's HTTP/3 codec (io.netty:netty-codec-http3) from 4.2.0.Final through 4.2.17.Final retains unbounded per-stream QPACK encoder state. QpackEncoder stores a queue and a dynamic-table index tracker for every encoded field section that references the QPACK dynamic table, keyed by the peer-controlled QUIC stream ID, and these entries are released only when the remote decoder sends a Section Acknowledgment or Stream Cancellation instruction — not when the HTTP/3 stream completes. There is no limit on the number of tracked streams, field sections, or retained bytes. A remote, unauthenticated HTTP/3 client can advertise a non-zero QPACK dynamic-table capacity, acknowledge the table insertion so the server reuses a dynamically indexed response header, and then omit all mandatory Section Acknowledgments while issuing sequential requests over a single QUIC connection, bypassing concurrent-stream limits and causing unbounded heap growth until the server exhausts memory (denial of service). Fixed in 4.2.18.Final.

### CVE-2026-100657

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-772` |
| Published | 2026-09-26T14:16:48.540 |

Netty's STOMP codec (io.netty:netty-codec-stomp) contains a ByteBuf leak in StompSubframeDecoder. Once a frame's declared content-length has been fully read, the decoder allocates a chunk buffer from the channel allocator and parks it in an instance field while waiting for the single NUL byte that terminates the frame. If that byte never arrives, the buffer is never released: the replay Signal thrown by skipNullCharacter extends Error rather than Exception, so the decoder's catch(Exception) release path does not run, and StompSubframeDecoder overrides neither handlerRemoved0 nor channelInactive, so the buffer also survives channel teardown. A remote peer can leak one allocator buffer per connection by sending a complete, well-formed frame body and withholding its terminating NUL byte; with the default pooled allocator the memory is never returned to the pool or reclaimed by garbage collection, so the leak accumulates for the lifetime of the process and can lead to memory exhaustion. This affects versions up to and including 4.1.137.Final and versions 4.2.0.Final through 4.2.17.Final; it is fixed in 4.1.138.Final and 4.2.18.Final.

### CVE-2026-100656

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-26T14:16:48.390 |

Netty (io.netty:netty-codec-http) contains an unbounded per-connection queue growth flaw in HttpServerCodec. The codec tracks the HTTP method of each still-unanswered pipelined request; the first 32 entries are bit-packed into a single long, but every additional entry is appended to methodOverflowQueue, an ArrayDeque with no size limit and no rejection path. A remote, unauthenticated attacker who pipelines HTTP/1.1 requests on a single connection while withholding reads on their own end (preventing responses from being flushed) can grow this queue without bound, causing unbounded heap growth and denial of service. Affected versions are 4.2.0.Final through 4.2.17.Final and all releases up to and including 4.1.137.Final; the issue is fixed in 4.2.18.Final and 4.1.138.Final.

### CVE-2026-100644

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-26T14:16:46.583 |

SiYuan before v3.8.4 contains a SQL injection vulnerability in the graph query endpoint where the dailyNoteSavePath parameter is concatenated into SQL without escaping. Unauthenticated attackers on published sites with auth disabled can inject SQL via UNION SELECT to extract arbitrary database rows from all notebooks.

### CVE-2026-100631

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-09-26T14:16:44.397 |

Parse Server is an open source backend server. In versions prior to 8.6.90 and in versions from 9.0.0 prior to 9.10.1-alpha.9, the device token deduplication logic for installation records does not validate the type of client-supplied installation fields before using them to build database queries. An unauthenticated remote attacker who knows only the public application ID can submit non-string values in these fields to inject query operators, causing the deduplication cleanup — which runs with elevated privileges before class-level permissions are evaluated — to delete every device registration in the application or an attacker-chosen subset of them. No account, session token, master key, or user interaction is required. Deleted registrations cannot be recovered on the server, so push notifications cannot be delivered until every client re-registers. Any deployment that exposes the REST API to clients and uses push notifications is affected in its default configuration. Versions 8.6.90 and 9.10.1-alpha.9 fix the issue by rejecting non-string values with a client error and by scoping the deduplication cleanup to the calling application. No workaround other than upgrading is available.

### CVE-2026-100628

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T14:16:43.977 |

capgo.app before 12.128.12 fails to enforce an organization's API key expiration policy when creating app-scoped API keys. In the POST /apikey endpoint, requests that supply app_id but omit org_id, limited_to_orgs, and expires_at resolve the target app and scope the key to it, but never add the app's owner organization to the list of organization IDs passed to validateExpirationAgainstOrgPolicies; because that list is empty, the validation returns early. As a result, an authenticated organization member can create a non-expiring app-scoped API key even when the owning organization has require_apikey_expiration enabled and a max_apikey_expiration_days limit configured. The issue is fixed in version 12.128.12.

### CVE-2026-100625

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-441` |
| Published | 2026-09-26T14:16:43.567 |

Capgo (capgo.app) exposes a native build TUS upload proxy (supabase/functions/_backend/public/build/upload.ts) that authorizes a caller against a single build job identified by the supplied builder_job_id and validates only that job's stored upload_path, but then forwards the user-controlled TUS resource suffix taken from /build/upload/:jobId/* to the builder service while injecting Capgo's privileged builder API key. Because the forwarded suffix is never bound to the authorized job's upload_path or upload_session_key, a caller holding a valid 'all' or 'write' Capgo API key with app.build_native permission for one application can use its authorized proxy path for job A to write to the TUS upload resource of another job B, provided that resource suffix is known or exposed, corrupting that build's artifacts. All versions are affected; no patch was available at the time of advisory publication.

### CVE-2026-100623

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T14:16:43.293 |

Capgo (capgo.app) exposes the legacy membership table public.org_users directly through Supabase PostgREST. The table's row-level security policies "Allow org admin to insert" and "Allow org admin to update" only verify that the caller has admin rights in the target organization (public.check_min_rights('admin', ...)); they do not require a pending invitation in tmp_users, acceptance of an invite token via /private/accept_invitation, any action by the target user, or the membership/role-consistency and anti-escalation checks enforced by the RBAC role-binding path. As a result, an authenticated user who is an admin of an organization can INSERT or UPDATE org_users rows directly to add any existing public.users account as an active member of that organization with user_right="admin", bypassing the invitation and role-assignment workflow entirely. In testing, an account with no prior access to the organization or its apps could, after such a direct insert, read the organization and app and pass check_min_rights. All versions are affected and no patch was available at the time of publication.

### CVE-2026-100622

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T14:16:43.157 |

capgo.app through 12.129.0 fails to verify deletion status when serving cached bundle artifacts from the public file read endpoint. Unauthenticated attackers can download deleted bundles using cached URLs and trigger restoration of deleted objects into R2 storage on cache hits.

### CVE-2026-100619

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-26T14:16:42.740 |

Capgo (capgo.app) blocks direct user inserts into the public.manifest table with a RESTRICTIVE row-level security policy, but that restriction can be bypassed indirectly. A principal holding an app-scoped upload/write/all API key (upload+ rights) or an authenticated user with write+ rights on an app can update public.app_versions.manifest on a version whose storage_provider is 'r2-direct', which is not covered by the bundle content-lock check. The on_version_update async worker trusts record.manifest and, using the service-role Supabase client, inserts the attacker-controlled file_name, file_hash, and s3_path into public.manifest before clearing app_versions.manifest. When a channel points to the crafted version, the /updates endpoint returns the service-role-created manifest entry as a client-facing download_url, enabling OTA manifest poisoning through a trusted async worker path. All versions are affected; no patch was available at the time of publication.

### CVE-2026-100618

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-26T14:16:42.600 |

Capgo (capgo.app) is affected by an authorization flaw in the app icon update path. The PUT /app/:id endpoint accepts a user-controlled `icon` value, normalizes it, and stores it in public.apps.icon_url without verifying that the image path belongs to the target app's own image namespace (e.g. org/{owner_org}/{app_id}/...). Updating apps.icon_url fires the on_app_update trigger, whose worker reads record.icon_url and calls cleanStoredImageMetadata(), which runs with service-role credentials (supabaseAdmin()) and downloads and re-uploads the referenced storage object with upsert: true. As a result, an authenticated holder of an app-limited write API key can cause the privileged worker to rewrite an out-of-scope private image object (for example an organization logo) that the key cannot read or write directly under Supabase Storage RLS. All versions are affected; no patched version was available at the time of the advisory.

### CVE-2026-100617

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-26T14:16:42.467 |

Cap-go capgo.app fails to validate that principals in channel_permission_overrides belong to the organization, allowing authenticated app/org admins to grant channel permissions to non-member users. Attackers with admin privileges can insert override rows with arbitrary external user UUIDs to grant channel-scoped permissions such as channel.promote_bundle to users outside the organization.

### CVE-2026-100615

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-26T14:16:42.193 |

Cap-go capgo.app before 12.267.1 fails to validate target API key privilege during rotation, allowing an apikey_manager to rotate a higher-privileged org_super_admin sibling key and recover its plaintext credential. Attackers with apikey_manager role can enumerate same-owner API keys, rotate a stronger sibling through the PUT endpoint, and obtain the replacement plaintext secret to authenticate as the higher-privileged principal.

### CVE-2026-100614

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-26T14:16:42.050 |

Capgo before 12.244.1 contains a cross-tenant integrity vulnerability in the metadata-cleaning worker that trusts image object keys from mutable database rows without validating ownership. An authenticated attacker can place a victim tenant's image key in a row they control, causing the service-role worker to download and re-upload that object with sanitized metadata. Attackers can silently modify metadata in cross-tenant image objects by supplying known victim keys during authorized row updates, bypassing storage access controls through the confused-deputy metadata worker.

### CVE-2026-100608

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-26T14:16:41.140 |

Flowise through 3.1.4 does not enforce authorization on the BullMQ admin dashboard. When the server runs in queue mode with the dashboard enabled and not in cloud mode (MODE=queue, ENABLE_BULLMQ_DASHBOARD=true, and !isCloud()), the /admin/queues mount is protected only by the verifyTokenForBullMQDashboard middleware, which validates the JWT but performs no role, permission, or workspace/organization scoping check; the mount also lies outside /api/v1/* so the global API gate does not apply. As a result, any authenticated user — including the lowest-privileged member of any tenant — can reach the full Bull-Board UI and view all queues and job payloads across the entire instance, including chat inputs and overrideConfig (which may carry credentials and prompts), chatflow.flowData graph definitions with custom function source code, credential IDs and system prompts, chatIds, files, and the originating orgId/workspaceId. The dashboard's write actions (retry, remove, promote, clean) are likewise usable across tenants. No patched version is available as of the advisory.

### CVE-2026-100603

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-799` |
| Published | 2026-09-26T14:16:40.330 |

ClawHub (openclaw/clawhub) application/backend contains a flaw in the skill report moderation flow: four distinct ordinary authenticated accounts can report a visible skill and trigger automatic hiding (moderationStatus: hidden) of that skill from the catalog without any moderator decision. Because the reporter quota counts only reports filed against visible targets, the same accounts can repeat the process against additional skills; official skills are not exempt. The issue was confirmed at revision cbfee7343ddc867316dd9b3de6fa8856730f9f41; the complete historical affected range was not established. The fix (PR #3681) is included in revision 8c2de6c506bb4efabe3f0c2ffb8370b9e23d4650; self-hosted deployments should update to that revision or a later descendant. The npm CLI and OpenClaw runtime are separate products and are not affected.

### CVE-2026-100599

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-26T03:17:08.667 |

OpenClaw versions 2026.5.1 through 2026.7.0 fail to apply the configured exec approval path to Google Meet node commands. The googlemeet.chrome command accepts caller-supplied audio command arrays and executes them on a paired node without going through the normal system.run approval flow. In deployments with the Google Meet plugin enabled, a paired Chrome node, and the googlemeet.chrome node command allowed, a tool-enabled agent able to invoke that command can execute attacker-selected processes on the paired node, impacting files, credentials, browser profiles, and availability on that node. The issue is fixed in 2026.7.1; as a workaround, remove googlemeet.chrome from allowed node commands or disable the Google Meet plugin.

### CVE-2026-100596

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-26T03:17:08.187 |

OpenClaw versions before 2026.7.1 fail to properly authorize non-owner users executing MCP configuration changes through /mcp set and /mcp unset commands. Attackers can persist arbitrary stdio MCP commands that execute with OpenClaw process privileges when configuration loads, compromising host confidentiality, integrity, and availability.

### CVE-2026-100589

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T03:17:07.110 |

OpenClaw versions before 2026.7.1 contain a sandbox bypass vulnerability in the browser tool that allows sandboxed sessions to access paired node browser actions despite allowHostControl=false configuration. Attackers with control over sandboxed agent input can select a paired node and perform host browser operations, inspecting or manipulating the connected browser profile and its authenticated state.

### CVE-2026-100588

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T03:17:06.963 |

OpenClaw (npm package 'openclaw') before 2026.7.1 does not enforce the administrator scope requirement on browser control when it is reached through the node.invoke method, although direct browser.request access requires administrator scope. In Gateway deployments that honor caller identity and narrower operator scopes, a write-scoped caller with access to a connected browser-capable node can inspect pages, navigate tabs, or interact with browser-visible applications without the configured admin requirement; practical impact depends on the browser profile and signed-in state. Shared-secret token and password callers are considered fully trusted operators under OpenClaw's security model and are not affected. The issue is fixed in 2026.7.1.

### CVE-2026-100587

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-26T03:17:06.810 |

OpenClaw versions before 2026.7.1 fail to properly validate owner authorization in the Codex computer-use installation command. Non-owner channel senders can install arbitrary plugins and execute MCP processes with OpenClaw user privileges, affecting host confidentiality, integrity, and availability.

### CVE-2026-100586

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-26T03:17:06.660 |

OpenClaw Codex before 2026.7.1 fails to properly enforce owner authorization when creating native conversation bindings. Non-owner channel senders with command access can create bindings to the native Codex runtime and execute host-capable turns with access to files, tools, and processes.

### CVE-2026-100580

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-09-26T03:17:05.783 |

OpenClaw (npm package 'openclaw') before 2026.7.1 improperly handles case sensitivity in the model-facing cron tool: a mixed-case payload kind can pass the agent-facing shell-execution guard and later normalize into a command job. An actor able to steer a tool-enabled agent can therefore create a persistent cron job that executes attacker-selected commands with the privileges of the OpenClaw process user, resulting in access to host files and credentials and impact to scheduled service availability. The issue is limited to cron jobs created or edited through the model-facing cron tool; direct CLI and authorized Gateway scheduling surfaces are trusted operator controls. Fixed in 2026.7.1.

### CVE-2026-100575

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-26T03:17:05.030 |

OpenClaw Slack versions before 2026.8.1 fail to properly enforce sender allowlists in multi-person direct messages. Disallowed participants can trigger Slack agents and access tools and data granted to those agents by bypassing configured sender policies.

### CVE-2026-100568

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T03:17:03.887 |

OpenClaw versions before 2026.8.1 fail to properly restrict access to operator command cron jobs, allowing model-visible agent callers to read and execute ownerless command jobs. Attackers can inspect stored environment variables and force-run disabled or unscheduled command jobs to access secrets and execute operator-authored commands.

### CVE-2026-100558

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-26T03:17:02.533 |

OpenClaw versions before 2026.8.1 contain a resource exhaustion vulnerability in the Gateway listener that allows unauthenticated clients to retain response sockets by sending WebSocket upgrade requests without matching connection semantics. Attackers can repeatedly send malformed upgrade requests to exhaust listener resources and cause denial of service without consuming the WebSocket pre-auth connection budget.

### CVE-2026-100557

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T03:17:02.387 |

OpenClaw versions before 2026.8.1 contain an authorization bypass vulnerability in skill tool dispatch that fails to carry the sender's owner status. Non-owner senders authorized to invoke skill commands can access owner-only tools and server credentials reserved for owners.

### CVE-2026-100552

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T03:17:01.640 |

OpenClaw (npm package 'openclaw') before 2026.8.1 does not correctly enforce per-chat tool policies for Codex app-server runtime tools. A conversation-level tools.allow rule filtered OpenClaw tools but did not restrict the shell, process, file, and patch tools owned by the Codex runtime. When a lower-trust conversation was assigned to a Codex runtime and restricted with a per-chat tool allowlist, a participant able to trigger that agent could still reach native command and file tools, bypassing the configured allowlist. The practical impact depends on the runtime's host permissions and sandbox configuration. The issue is fixed in 2026.8.1.

### CVE-2026-100544

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-26T03:17:00.440 |

openclaw's @openclaw/voice-call package before 2026.8.1 launches the configured agent for classic inbound voice calls without propagating the caller's identity or non-owner status. As a result, owner-only tool filtering can fail open and expose the agent's normal tool authority to a remote caller. A caller who is admitted by the configured inbound-call policy (open, pairing, or allowlist) on a deployment with inbound calling enabled can therefore drive tools intended for the trusted owner, potentially reading data, modifying files, executing commands, or controlling connected services depending on the agent's configuration. The issue is fixed in 2026.8.1.

### CVE-2026-100520

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-26T01:17:00.357 |

Laranode versions before 1.2.1 contain a path traversal vulnerability in the POST /filemanager/upload-file endpoint that allows authenticated users to write arbitrary files outside their home directory. Attackers can supply directory traversal sequences in the path parameter to write PHP files into other tenants' web roots and execute code as those tenants.

### CVE-2026-56733

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-863` |
| Published | 2026-09-25T18:17:27.533 |

Zammad is a web based open source helpdesk/customer support system. Prior to 7.0.2 and 7.1.0, this issue concerns a lack of discursive validation within the authorization cascade. It has been determined that the system-level enforcement of access restrictions during the initialization of new identity objects exhibits a discrepancy: Under specific conditions, the granular restrictions of the access key being used are overridden by the latent authorization authority of the parent account. Consequently, this means that the intended separation of functional areas is nullified, resulting in an uncontrolled expansion of administrative discretion. Due to this potential integrity breach of the entire trust environment, an immediate evaluation of the authorization hierarchies is imperative. Impact An attacker can create new administrator accounts despite token restrictions. This grants full access to all system data (tickets, customers, configuration) and allows the attacker to take complete control of the Zammad instance. Abuse Scenario The vulnerability stems from a lack of synergy between the token-based authorization logic and the target system's functional authorization hierarchy, which allows for iterative escalation of the privileged access context. This issue is fixed in versions 7.0.2 and 7.1.0.

### CVE-2026-56725

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-400` |
| Published | 2026-09-25T18:17:26.330 |

Zammad is a web based open source helpdesk/customer support system. Prior to 7.0.2, summary An unauthenticated request to POST /api/v1/import/otrs/import_check blocks a Zammad request worker for roughly two minutes. The import_check and import_status actions are missing the setup_done_response guard that other actions in the same controller carry, so they execute on fully set-up production instances. The action enters a retry loop against a blank OTRS endpoint, sleeping for 30 s + 45 s between attempts. Impact An unauthenticated remote attacker denies service to a production Zammad instance. Each request costs almost nothing and forces ~115 seconds of server-side blocking. A few requests per second saturate the Puma worker pool. The condition persists as long as the traffic continues. No account, valid import configuration, or target knowledge beyond the hostname is needed. CSRF token is trivially obtained from any prior GET response. This issue is fixed in version 7.0.2.

### CVE-2026-89032

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-25T17:17:18.793 |

BerriAI LiteLLM before 1.101.0-rc.1 contains a tenant isolation bypass vulnerability in the semantic cache layer that allows authenticated users to read other tenants' cached responses by exploiting a metadata key mismatch between _get_semantic_cache_tenant_scope() and _get_metadata_variable_name(). Attackers holding a valid virtual key can submit semantically similar prompts on affected routes such as /v1/responses and /bedrock/* to retrieve cached responses containing other tenants' personally identifiable information, financial data, or source code, and can cause agentic front-ends to auto-execute attacker-supplied tool calls under victim credentials by returning cached function_call or tool_calls payloads to a different principal.

### CVE-2026-100693

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-09-26T14:16:54.007 |

Hugo versions from v0.162.0 before v0.166.0 contain a case-sensitive validation flaw in the security.http.urls IP-literal deny rule that allows attackers to bypass restrictions. Attackers can use mixed-case URL schemes in resources.GetRemote calls to fetch from restricted IP addresses like localhost.

### CVE-2026-100686

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-26T14:16:53.000 |

Budibase versions before 3.45.0 fail to validate per-app authorization in the POST /api/global/groups/:groupId/apps endpoint, allowing builders to assign application roles across workspace boundaries. A builder of a single workspace can exploit missing per-app authorization checks to grant themselves admin roles in other workspaces by modifying user group role mappings.

### CVE-2026-100680

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T14:16:52.150 |

Budibase versions before 3.45.0 fail to disable external JSON reference resolution in the OpenAPI/Swagger import validator, allowing authenticated builders to read arbitrary local files. Attackers with builder access can embed file:// references in OpenAPI specifications submitted to the import endpoint to exfiltrate sensitive files including environment variables containing JWT secrets, API keys, and database credentials.

### CVE-2026-100671

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T14:16:50.743 |

Grav is a flat-file CMS. In versions 2.0.19 through 2.0.24 — and in 2.0.0 through 2.0.18 and 1.7.x only where content Twig has been explicitly enabled — page content authored by a user holding only page-write permission is rendered through a Twig sandbox that allowlists get_cookie(), which returns any cookie sent with the current request, including the visitor's session cookie. Because the read occurs server-side via filter_input(INPUT_COOKIE, ...), the HttpOnly, Secure and SameSite attributes offer no protection. Grav then stores the finished post-Twig output in a page-content cache keyed only on page identity and the configuration checksum, with no session, user or request dimension and no bypass for authenticated visitors. A page published by a page-write user can therefore capture the session identifier of the next administrator who views it, after which the cached output serves that identifier to unauthenticated visitors, who can replay the cookie to authenticate as that administrator. Since 2.0.19, security.twig_content.process_enabled defaults to true and Security::applyTwigContentDefault() derives each page's process.twig flag from that gate, so content Twig runs on every page with no frontmatter or operator action. Fixed in 2.0.25; 1.7.x is outside the backport scope.

### CVE-2026-100646

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-26T14:16:46.900 |

SiYuan is a self-hosted personal knowledge management system. In versions up to and including 3.8.3, the kernel's authentication guards (CheckAuth in kernel/model/session.go and IsSessionOriginAllowed in kernel/util/net.go) fail open when the HTTP Origin header is absent, on the incorrect assumption that any browser-initiated cross-site request carries an Origin. Because browsers omit Origin on cross-site top-level GET navigations and no-cors GET subresource loads — and the session cookie is SameSite=Lax — a single cross-site GET issued from any attacker-controlled web page is granted RoleAdministrator, both on default installations with no access-authorization code and on password-protected instances with a live session. Combined with content-type sniffing on the /api/network/proxy endpoint, which allows attacker-controlled HTML to be served under SiYuan's own origin, this permits an unauthenticated remote attacker to execute arbitrary script in the SiYuan origin (http://127.0.0.1:6806), invoke administrator APIs, and exfiltrate the persistent kernel API token. This issue is fixed in version 3.8.4.

### CVE-2026-100645

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-26T14:16:46.743 |

SiYuan versions 3.7.0 before 3.8.4 contain a stored cross-site scripting vulnerability in gallery and kanban database renderers where field descriptions are not escaped in aria-label attributes. In the Electron desktop app with nodeIntegration enabled, attackers can inject JavaScript that calls Node.js child_process APIs to execute arbitrary commands with user privileges.

### CVE-2026-100641

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-26T14:16:46.080 |

SiYuan before v3.8.4 does not HTML-escape stored flashcard block content before interpolating it into the card-manager list markup. Block content returned by /api/riff/getRiffCards is inserted into a card item template in app/src/card/viewCards.ts and assigned to listElement.innerHTML, so content such as <img src=invalid onerror=...> becomes an executable event-handler attribute. Because the SiYuan desktop (Electron) main window is created with nodeIntegration enabled and contextIsolation disabled, an administrator who opens the card manager on a workspace containing attacker-supplied flashcard content (for example introduced through contribution or import) executes the attacker's script in a privileged renderer, which can lead to arbitrary code execution on the host. The affected endpoint remains behind authentication and administrator-role checks; this is an untrusted-content-to-privileged-renderer issue, not an authorization bypass.

### CVE-2026-100640

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T14:16:45.820 |

SiYuan before v3.8.4 contains an authorization omission in the siyuan-get IPC handler that allows remote-kernel renderers to access native clipboard formats by invoking clipboardReadMathML, clipboardReadOffice, and clipboardReadWPS commands with matching plaintext. Attackers controlling remote renderer content can obtain MathML formulas, Office bytes, and WPS bytes from local clipboard during user-mediated paste operations.

### CVE-2026-100639

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-26T14:16:45.633 |

SiYuan v3.8.3 fails to HTML-escape the data-subtype attribute when generating gutter-button markup (app/src/protyle/gutter/button.ts, assigned via innerHTML in app/src/protyle/gutter/index.ts) from content pasted as plain-text Markdown containing a Kramdown inline attribute list (IAL). Because the shared Lute renderer parses Kramdown IAL from text/plain input, an attacker-supplied Markdown snippet using entity-encoded quotes in data-subtype breaks out of the attribute value when the gutter markup is re-parsed by the browser, injecting additional attributes such as autofocus and onfocus. If a victim pastes the crafted Markdown and the affected gutter control receives focus, the injected handler executes; in the Electron desktop application, where the main BrowserWindow enables Node integration and disables context isolation, this results in JavaScript execution with renderer Node.js privileges (remote code execution). Fixed in v3.8.4.

### CVE-2026-100612

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-26T14:16:41.753 |

Capgo (capgo.app) through version 12.261.0 contains an incomplete access-control fix for the public.sso_providers table. Migration 20260826100000_sso_providers_block_direct_active_insert.sql installs a BEFORE UPDATE guard (enforce_sso_provider_client_update_guard()) that freezes only the dns_verified_at, domain, status and enforce_sso columns; provider_id (as well as metadata_url and attribute_mapping) is left writable. Because the table is granted ALL to the anon and authenticated roles with no column-level restriction, and PostgreSQL row-level security policies such as allow_org_admins_update_sso_providers constrain only which row may be updated and not which columns, a user holding the org_admin tier permission org.update_settings can PATCH provider_id over PostgREST to an identity provider under their control. Since provider_id is the trust anchor binding an email domain to an authorized IdP, the attacker can then authenticate through their own IdP while asserting the org owner's email; the server-side provider match succeeds and the merge routine attaches the attacker's SSO identity to the existing owner account, nulls its password, and deletes its other identities and sessions. This results in vertical privilege escalation from org_admin to org owner/super_admin, account takeover, and lockout of the legitimate owner. Exploitation requires that the target organization has an active SSO provider configured and that the attacker already holds org_admin in that organization. No patched version is available.

### CVE-2026-100585

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-26T03:17:06.517 |

OpenClaw (npm package `openclaw`) before 2026.7.1 fails to enforce the owner-only authorization requirement for Claude Code permission prompts delivered through the MCP channel bridge. An authorized non-owner channel sender with channel command access can approve or deny a pending permission request intended for the owner, causing the requested action to proceed without owner consent. The practical impact depends on the pending action and the host capabilities requested by the Claude Code run. The issue is fixed in version 2026.7.1.

### CVE-2026-100561

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-26T03:17:02.987 |

OpenClaw (npm package 'openclaw') versions >= 2026.3.22 and < 2026.8.1 contain an approval-bypass flaw in the exec approval policy: the policy could trust a command-running wrapper without inspecting the command carried in its arguments. After an operator allowlisted or permanently approved a benign wrapper invocation, a later agent turn could substitute an arbitrary inner command and execute it with the OpenClaw process's host privileges without a further approval prompt. Exploitation requires the relevant wrapper to resolve on the host and a prior operator decision allowing that wrapper. Transparent shell carriers and opaque utilities such as process monitors, tracers, namespace tools, and proxy wrappers were affected through related trust-resolution gaps. Fixed in 2026.8.1.

### CVE-2026-100559

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-26T03:17:02.680 |

OpenClaw versions before 2026.8.1 contain a command parser vulnerability where escaped newlines confuse exec allowlist parsing, allowing hidden commands to execute. Attackers can craft input with escaped newlines to bypass allowlist validation and execute additional commands without expected authorization prompts.

### CVE-2026-100372

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-25T20:17:06.143 |

ClipBucket v5 before 5.5.3-#197 contains a path traversal vulnerability in the admin template editor that allows authenticated administrators to overwrite PHP files by supplying directory traversal sequences in the folder parameter. Attackers with manage_template_access permission can traverse outside the layout directory to modify executable PHP files and achieve remote code execution as the web server user.

### CVE-2026-97060

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-25T19:17:59.110 |

X-SpringBoot through 6.0 lacks object-level authorization in user management endpoints, allowing sub-administrators to modify or delete users without ownership verification. Attackers with user-management permissions can reset passwords for any account including the super administrator, rebind roles, or delete users via POST /sys/user/update and POST /sys/user/delete endpoints.

### CVE-2026-84462

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-94;CWE-1336` |
| Published | 2026-09-25T18:17:30.797 |

Zammad is a web based open source helpdesk/customer support system. Prior to 7.1.2, a security filter that protects Zammad's AI Agent configuration can be bypassed by entering specially crafted text into one of an AI Agent's fields. An administrator with permission to create or edit AI Agents could exploit this to run arbitrary commands on the server that hosts Zammad, potentially reading, modifying, or destroying all data stored on that server. No interaction from other users is needed; the malicious code runs automatically the next time the affected AI Agent processes a ticket. This issue is fixed in version 7.1.2.

### CVE-2026-100717

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-26T14:16:57.753 |

froxlor is a server administration panel. In versions 2.3.10 and earlier, Validate::validateUrl rejects carriage return and line feed characters only in the path, query and fragment components returned by parse_url, and never inspects the userinfo (user:pass@) components. This is an incomplete fix for GHSA-c3p2. An authenticated low-privilege customer with subdomain-create rights (no admin or change_serversettings privilege required) can supply a subdomain redirect URL that carries a CR/LF payload in the userinfo portion (e.g. http://user%0areturn 200 "pwned";%0a@evil.com/). The value passes validation, survives IDNA encoding, and is written verbatim into the generated nginx or Apache vhost configuration, allowing the attacker to break out of the emitted directive and inject arbitrary web-server configuration lines. froxlor regenerates and reloads the web-server configuration as root, so the injected directives take effect server-wide and can hijack responses or read local files. The issue is fixed in version 2.3.12.

### CVE-2026-100715

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-26T14:16:57.427 |

Froxlor through 2.3.10 is vulnerable to arbitrary file deletion via symlink following in the FTP data deletion cron task. Cron task 8 (deleteFtpData), queued when an FTP account is deleted, calls FileDir::makeCorrectDir() without the $fixed_homedir argument, so the symlink component walk is skipped, and then executes 'rm -rf' as root on the resulting path with string-level guards only. Because makeCorrectDir() appends a trailing slash, GNU rm dereferences a symlink used either as an intermediate path component or as the final component. An authenticated customer who can write to the FTP home directory can plant a symlink between task insertion and cron execution, causing the root cron job to recursively delete arbitrary directory trees, resulting in cross-tenant data destruction and host denial of service. This issue is fixed in Froxlor 2.3.12.

### CVE-2026-100643

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-26T14:16:46.427 |

SiYuan versions before v3.8.4 fail to properly escape four stored Attribute View values in textarea elements, allowing authenticated attackers to inject JavaScript by modifying field descriptions, template sources, select option descriptions, or footer calculation templates. Attackers can execute stored JavaScript when other users open affected database menus, and in the Electron desktop app with nodeIntegration enabled, this leads to command execution with SiYuan process privileges.

### CVE-2026-100633

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T14:16:44.687 |

SiYuan is a self-hosted personal knowledge management system. In versions 3.8.0 through 3.8.3, the MCP file tool's sensitive-path guard (util.IsForbiddenAbsPath(), invoked from resolvePath()) is applied only to the allowed root of recursive operations and not to each resolved descendant path — an incomplete fix for GHSA-c8r8-95hg-mp34. An authenticated administrator using the in-app Agent or the external MCP server can therefore bypass the protected-workspace-file denylist: file.grep can return matching lines from non-hidden protected descendants (for example conf/conf.json, TLS keys, data/snippets/conf.json, data/templates/, data/.siyuan/publishAccess.json, notebook .siyuan internals, or the kernel log), file.copy can copy protected descendants to an ordinary path where file.read can then retrieve them, and unzip can overwrite protected descendants using ordinary, lexically contained ZIP member names. Because file.grep is globally classified as a safe action, it receives no per-call confirmation, and the confirmation cards for file.copy and unzip show only the allowed root arguments. This issue is fixed in version 3.8.4. Suggested title: SiYuan 3.8.0 through 3.8.3 Sensitive-Path Guard Bypass in Recursive MCP File Operations.

### CVE-2026-100570

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-26T03:17:04.177 |

OpenClaw (npm package 'openclaw') versions >= 2026.3.28 and < 2026.8.1 allow an untrusted workspace .env file to set the CLOUDSDK_PYTHON_ARGS environment variable. When an operator starts OpenClaw in attacker-controlled workspace content and then runs the Gmail setup flow, that value is inherited when gcloud is launched, and the gcloud launcher passes it as arguments to the trusted Python interpreter. A crafted CLOUDSDK_PYTHON_ARGS value can therefore cause Python to execute attacker-supplied code with the OpenClaw host user's permissions, allowing credentials to be read, files to be modified, or other processes to be started. This issue is fixed in version 2026.8.1; as a workaround, run Gmail setup only from trusted workspaces and clear inherited CLOUDSDK_* variables beforehand.

### CVE-2026-100530

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T03:16:58.367 |

OpenClaw versions before 2026.8.1 fail to bind working directory context to reusable exec approvals, allowing approved commands to execute in different directories. Attackers with an allow-always approval can reuse it to run the same command against unreviewed files or repositories with materially different effects.

### CVE-2026-71483

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T22:18:20.173 |

Horilla is an HR and CRM software. Prior to 1.6.0, the search parameter at /employee/employee-filter-view is reflected by jQuery .html() in employee/templates/employee_nav.html without HTML neutralization. An external attacker can craft and deliver a link that causes JavaScript to execute when an authenticated employee or administrator reaches the employee filter, allowing access to browser-visible session data and actions with the victim's application privileges. This issue is fixed in version 1.6.0.

### CVE-2026-55214

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-09-25T19:17:38.160 |

GLPI is a free asset and IT management software package. From 11.0.6 until 11.0.8, an authenticated technician can store active markup in supplier website fields. Any user who opens the affected item's suppliers list triggers the stored cross-site scripting payload. This issue is fixed in version 11.0.8.

### CVE-2026-47679

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-25T19:16:54.967 |

GLPI is a free asset and IT management software package. From 10.0.0 until 10.0.26 and 11.0.8, any logged-in GLPI user can exploit insufficient path validation in the profile-picture update flow to request deletion of an attacker-selected file hosted by the server. This issue is fixed in versions 11.0.8 and 10.0.26.

### CVE-2026-100673

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-26T14:16:51.133 |

The Grav Data Manager plugin (getgrav/grav-plugin-datamanager) versions 1.0.1 through 1.4.4 render stored data entries in the item-detail view (admin/templates/partials/item.html.twig) without escaping, applying Twig's `raw` filter — in some cases after a striptags('<br>') call that PHP's strip_tags() bypasses by preserving allowed tags together with their attributes. An unauthenticated visitor who submits a front-end form whose submissions are saved to user/data can store an HTML payload that executes as JavaScript in the session and origin of an administrator who later opens that entry in the classic admin panel, running with that administrator's privileges and CSRF token. Execution occurs without further interaction for list values (such as checkbox or multi-select fields) and on hover for ordinary text fields. Sites using the Grav 2.0 Admin Next interface are not affected, because it renders the same data through a separate, correctly escaping code path. The issue is fixed in Data Manager 1.4.5.

### CVE-2026-100369

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-25T21:17:21.247 |

CliInvoke and its formerly named `AlastairLundy.CliInvoke` package are .NET libraries for invoking command-line programs and wrapping executable processes. `CliInvoke` versions 2.0.0 through 2.8.4, 2.9.0 through 2.9.3, 2.10.0 through 2.10.4, and 3.0.0-alpha.1 through 3.0.0-beta.1, as well as `AlastairLundy.CliInvoke` versions 2.0.0-alpha.1 through 2.0.0, contain an argument-injection vulnerability in `RunnerProcessFactory` on the 2.x line and `RunnerConfigurationFactory` on the 3.x line. These factories combine runner arguments, a caller-controlled target, and caller-controlled arguments into one `ProcessStartInfo.Arguments` string, allowing a double quote in the target or an argument to terminate an operating-system-level quoted region and inject unintended elements into the runner’s argument vector, potentially resulting in arbitrary command execution when a shell runner is used. The vulnerability is patched in `CliInvoke` versions 2.8.5, 2.9.4, 2.10.5, and 3.0.0-beta.2, and in `AlastairLundy.CliInvoke` version 2.0.2. No complete workaround is available; users unable to upgrade can partially mitigate the issue by removing double quotes from targets and arguments, additionally removing shell metacharacters when using shell runners, or bypassing the vulnerable factory and constructing a `ProcessConfiguration` with an explicit `ArgumentList`.

### CVE-2026-100368

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-25T20:17:05.990 |

CliInvoke is a .NET library for invoking command-line programs, and its `CliInvoke.Specializations` packages provide specialized wrappers for shells such as PowerShell and Windows Command Prompt. `CliInvoke.Specializations` versions 2.2.0 through 2.8.4, 2.9.0 through 2.9.3, 2.10.0 through 2.10.4, 3.0.0-alpha.1 through 3.0.0-alpha.4, and 3.0.0-alpha.8 through 3.0.0-alpha.10, as well as `AlastairLundy.CliInvoke.Specializations` versions 1.0.0-rc.1 through 1.6.1.1, contain an OS command injection vulnerability in their PowerShell and Cmd wrappers. The wrappers pass a caller-controlled target and arguments to `pwsh -Command` or `cmd /c` using a single `ProcessStartInfo.Arguments` string, allowing a double quote in untrusted input to break operating-system-level quoting and cause the shell to execute an additional command with the host process's privileges. The vulnerability is patched in `CliInvoke.Specializations` versions 2.8.5, 2.9.4, 2.10.5, and 3.0.0-beta.1, and in `AlastairLundy.CliInvoke.Specializations` version 2.0.2. No complete workaround is available; users unable to upgrade should reject or remove double quotes from target paths and arguments, additionally reject shell metacharacters in versions 2.2.0 through 2.9.2 and 3.0.0-alpha.1 through 3.0.0-alpha.4, or bypass the PowerShell and Cmd wrappers and invoke target processes directly when handling untrusted input.

### CVE-2026-56731

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T18:17:27.213 |

Zammad is a web based open source helpdesk/customer support system. Prior to 7.0.1, a low-privilege authenticated user may inject arbitrary HTML markup, including JavaScript event handlers, into a ticket title via the standard ticket creation workflow. The title is persisted without sanitization. This issue is fixed in version 7.0.1.

### CVE-2026-100248

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:I/V:X/RE:H/U:Red` |
| Weaknesses | `CWE-1025` |
| Published | 2026-09-25T17:17:07.243 |

The Rattadan Cosmowarp smart contract before 56c6147 can have a comparison to an unintended value of current_admin.

### CVE-2026-100707

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-26T14:16:55.983 |

Kyverno before 1.19.1 contains a namespace isolation bypass in the apiCall context entry of namespaced Policy resources due to inconsistent path interpretation between validation and execution. A low-privilege tenant can use percent-encoded dot-segments in urlPath to bypass namespace checks and read resources from other namespaces using the Kyverno admission controller's ServiceAccount credentials.

### CVE-2026-100705

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-26T14:16:55.703 |

Kyverno before 1.19.1 is vulnerable to server-side request forgery. The default egress blocklist (169.254.169.254, 169.254.169.253, metadata.google.internal, 127.0.0.0/8, ::1/128) and the scoped-token control were wired only into the new CEL http.Get/Post library and were never applied to the legacy apiCall service executor (pkg/engine/apicall/executor.go) or to the GlobalContextEntry external-API path, which handle every non-CEL context[].apiCall.service call. Because these paths use a plain net/http client with no egress filtering and no validation of the configured service URL, a ClusterPolicy or GlobalContextEntry author — or, where a deployed policy templates the service URL from the admission resource, a lower-privileged resource submitter — can cause Kyverno to issue GET/POST requests to an arbitrary host, including the cloud metadata endpoint, loopback, and any in-cluster service, reading cloud instance credentials and reaching internal endpoints with Kyverno's network position. The executor also unconditionally attaches Kyverno's projected ServiceAccount token to the attacker-chosen destination; the token is audience-scoped, limiting its replay value. Fixed in 1.19.1.

### CVE-2026-100704

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T14:16:55.563 |

Kyverno is a policy engine for Kubernetes. In versions 1.14.0 through 1.19.0, the ImageValidatingPolicy (policies.kyverno.io/v1beta1) evaluator never reads the spec.images and spec.allowedValues fields of a PolicyException. Any PolicyException whose policyRefs and matchConditions match a resource causes image signature verification to be skipped for the entire resource rather than only for the listed images or values, so an exception intended to exempt a single trusted image exempts every image on the matched resource(s). As a result, unsigned or untrusted images can be admitted to the cluster without signature verification. This differs from ValidatingPolicy, GeneratingPolicy, and MutatingPolicy, which treat the same field as a partial exemption. The issue is fixed in version 1.19.1.

### CVE-2026-100703

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T14:16:55.420 |

Kyverno 1.16.0 through 1.19.0 registers the globalcontext.Lib CEL library in its policy environment without confining it to the policy's namespace, unlike the sibling libraries (resource.Lib, http.Lib, configMap loader) which are handed the policy namespace. A tenant who can create a namespaced policy (e.g. NamespacedValidatingPolicy, and likewise the namespaced mutating, deleting, generating, and image-validating policy kinds) in their own namespace can call globalContext.get("<entry>", "") and receive the full cached contents of a cluster-scoped GlobalContextEntry, including data cached from namespaces the tenant has no RBAC permission to read. No admission validation rejects such calls. Fixed in 1.19.1.

### CVE-2026-100685

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T14:16:52.860 |

Budibase before 3.45.0 fails to properly scope the GET /api/chat-links endpoint by workspace, allowing builders to enumerate chat identity link records across all workspaces in a tenant. Attackers with builder access to a single workspace can retrieve sensitive chat identity linking data including user IDs and external chat service identifiers from other workspaces they have no permission to access.

### CVE-2026-100678

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-26T14:16:51.857 |

stoatchat before 0.15.5 fails to enforce account-level attempt limits on MFA login challenges, allowing attackers who know a password to guess TOTP codes with only IP-based rate limiting. Attackers can reuse MFA challenge tickets across multiple failed attempts and distribute guesses across IP addresses to bypass rate limiting and gain account access.

### CVE-2026-100653

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-348` |
| Published | 2026-09-26T14:16:47.953 |

vLLM is an inference and serving engine for large language models. In versions from 0.22.1 through 0.28.0, the operator-supplied model revision pin (--revision / --code-revision) is not propagated to several Hugging Face artifact loads for the FunAudioChat and Tarsier2 architectures: the WhisperFeatureExtractor and speech_tokenizer PreTrainedTokenizerFast loads in vllm/model_executor/models/funaudiochat.py and the Qwen2VLConfig.from_pretrained call used by Tarsier2ProcessingInfo in vllm/model_executor/models/qwen2_vl.py. As a result, deployments pinned to a reviewed revision still resolve these behavior-affecting processor, tokenizer, and config artifacts from the repository's default revision, so a later change to the upstream default branch can alter audio preprocessing, speech tokenizer behavior, or Tarsier2 configuration without any change to the operator's configured pin. This is a supply-chain integrity and reproducibility failure for pinned deployments; it is residual to the earlier fix tracked as GHSA-3ww4-5jv9-j5gm / CVE-2026-47155 and does not constitute remote code execution or a trust_remote_code=False bypass. The issue is fixed in version 0.28.0.

### CVE-2026-100638

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-26T14:16:45.480 |

SiYuan versions before v3.8.4 contain a path traversal vulnerability in the setNotebookIcon endpoint that allows authenticated administrators to create arbitrary directory trees and write files outside the workspace boundary. Attackers can supply directory traversal sequences in the notebook parameter to escape the workspace data directory and write conf.json files to arbitrary locations accessible by the kernel process.

### CVE-2026-100637

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-26T14:16:45.320 |

SiYuan versions before v3.8.4 contain a path traversal vulnerability in the checkoutRepo endpoint that allows authenticated administrators to write JSON files outside the workspace. Attackers can supply a sessionID parameter containing directory traversal sequences to overwrite arbitrary JSON files in pre-existing kernel-writable directories outside workspace boundaries.

### CVE-2026-100636

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-26T14:16:45.160 |

SiYuan versions before v3.8.4 contain a path traversal vulnerability in the exportBrowserHTML endpoint that allows authenticated administrators to write arbitrary HTML content to index.html outside the workspace directory. Attackers can supply a folder parameter with directory traversal sequences to escape the export directory and overwrite index.html in any pre-existing kernel-writable location, enabling stored XSS or workspace defacement.

### CVE-2026-100501

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-25T22:17:10.793 |

Flame through 2.4.0 contains an improper restriction of excessive authentication attempts vulnerability in the POST /api/auth login endpoint that allows unauthenticated attackers to brute-force the admin password. Attackers can submit unlimited password guesses without rate limiting, attempt counters, lockouts, or delays to gain full administrator access and modify application configuration.

### CVE-2026-100702

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-26T14:16:55.280 |

Nodemailer before 10.0.2 fails to properly flatten deeply nested arrays in recipient fields such as to, cc, and bcc, allowing attackers to cause stack exhaustion. Attackers can supply a deeply nested JSON recipient array that triggers recursive Array.toString() conversion, exhausting the call stack and terminating the Node.js process.

### CVE-2026-100652

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-26T14:16:47.810 |

vLLM versions 0.22.0 through 0.23.0 fail to validate stop_token_ids against vocabulary bounds in Rust HTTP and gRPC frontends, allowing out-of-vocabulary token IDs to reach MinTokensLogitsProcessor. Attackers can submit requests with min_tokens greater than zero and out-of-vocabulary stop_token_ids to trigger CUDA tensor indexing failures that leave EngineCore in a fatal state requiring service restart.

### CVE-2026-100635

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-26T14:16:45.007 |

SiYuan before v3.8.4 contains an authentication bypass vulnerability in the publish service where session cookies are issued without Secure or SameSite attributes over plaintext HTTP connections. An on-path attacker can observe a valid publish-visitor-session-id cookie from a Basic Auth exchange and replay it to access authenticated publish endpoints without knowing the account password.

### CVE-2026-100574

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-26T03:17:04.887 |

OpenClaw (npm package 'openclaw') before 2026.8.1 contains a server-side request forgery vulnerability in its trusted-host DNS checks. For fetches that use the trusted-host DNS recheck, a trusted hostname that resolves to an unspecified address (0.0.0.0 or ::) bypasses the SSRF destination validation. An attacker who can influence DNS for an allowed hostname can therefore cause a guarded fetch to reach a service bound only to loopback and disclose its response; the practical impact depends on the reachable service and the data it returns. Fixed in 2026.8.1.

### CVE-2026-67410

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-25T17:17:13.093 |

RabbitMQ is a messaging and streaming broker. From 4.2.0 until 4.3.3 and 4.2.9, OAuth2 Client Secret Exposed via Unauthenticated JavaScript Endpoint (CWE-200). when OAuth2 authentication is enabled for the RabbitMQ Management UI and the configured flow, IDP use a client secret, the oauthclientsecret configuration value is included in the JavaScript served by the unauthenticated endpoint /js/oidc-oauth/bootstrap.js. Any user who can reach the management UI port can retrieve the OAuth2 client secret without Files: deps/rabbitmqmanagement/src/rabbitmgmtwmauth.erl, line 186 deps/rabbitmqmanagement/src/rabbitmgmtoauthbootstrap.erl, lines 35-50 deps/rabbitmqmanagement/src/rabbitmgmtdispatcher.erl, lines 45-49 (route registration) Code Path: 1. The route /js/oidc-oauth/bootstrap.js is registered as a plain Cowboy handler (rabbitmgmtdispatcher.erl:46): Credential exposure for the affected configuration: OAuth2 client secret is accessible without any authentication Token theft: Attacker can complete the authorization code flow using stolen authorization codes Client impersonation: Attacker can make requests. Any RabbitMQ deployment with: This issue is fixed in versions 4.3.3 and 4.2.9.

### CVE-2026-67409

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-252` |
| Published | 2026-09-25T17:17:12.943 |

RabbitMQ is a messaging and streaming broker. From 3.13.0 until 4.3.3, 4.2.9, 4.1.14, 4.0.23, and 3.13.18, JWKS Fetch Ignores HTTP Response Status Code - Signing Key Destruction Causes Authentication DoS (CWE-252). the JWKS key fetching mechanism in uaajwt.erl does not validate the HTTP response status code when downloading signing keys from the OAuth2 provider's JWKS endpoint. Non-200 responses (including 4xx and 5xx errors) are processed identically to successful responses. When the JWKS endpoint returns an error response with a valid-JSON body that lacks a keys field, all previously cached signing keys are destroyed, causing a persistent authentication denial of Files: deps/rabbitmqauthbackendoauth2/src/uaajwt.erl, lines 50-63 deps/rabbitmqauthbackendoauth2/src/uaajwks.erl, lines 5-7 deps/rabbitmqauthbackendoauth2/src/rabbitoauth2provider.erl, lines 98-107 Bug 1: HTTP status code ignored (uaajwt.erl:50-63): The Erlang httpc module returns {ok, {{HttpVersion, StatusCode, ReasonPhrase}, Headers, Body}}. The pattern {ok, {, , JwksBody}} matches ANY successful HTTP transaction Persistent authentication DoS: Once keys are destroyed, ALL OAuth2/JWT authentication fails for all users until a new successful JWKS refresh occurs Amplification: A single attacker can deny access to all legitimate OAuth2 users across the entire RabbitMQ. This issue is fixed in versions 4.3.3, 4.2.9, 4.1.14, 4.0.23, and 3.13.18.

### CVE-2026-67236

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-09-25T16:17:27.053 |

RabbitMQ is a messaging and streaming broker. From 4.2.0 until 4.2.8 and 4.3.2, a successful POST /login caused is_authorized/2 to set an auth cookie containing base64-encoded username:password credentials without HttpOnly, Secure, SameSite, or expiration protections. Because base64 is encoding rather than encryption, an attacker with same-origin cross-site scripting, an HTTP-readable network position, or local access to the browser cookie store could recover the actual login credentials; older browsers that treated an absent SameSite attribute as None also sent the cookie cross-site. This issue is fixed in versions 4.2.8 and 4.3.2.

### CVE-2026-44642

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-25T16:17:25.970 |

Piwigo is a full featured open source photo gallery application for the web. Prior to 16.4.0, check_upgrade_access_rights() in admin/include/functions_upgrade.php conditionally escapes the submitted username only when the removed get_magic_quotes_gpc function exists, so PHP 8 and later concatenate an unauthenticated username directly into the upgrade authentication SQL query. When database upgrades are pending, a crafted query result can satisfy the status and password checks, set PHPWG_IN_UPGRADE, and authorize upgrade execution without valid administrator credentials. This can cause unauthorized database integrity changes and service disruption. This vulnerability is fixed in 16.4.0.

### CVE-2026-91841

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-25T18:17:32.923 |

A flaw was found in NetworkManager-vpnc, a VPN plugin for NetworkManager. A local unprivileged user can exploit this vulnerability by injecting a newline character into the CA-File path. This manipulation allows the user to execute arbitrary commands as the root user, leading to local privilege escalation.

### CVE-2026-91840

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-25T18:17:32.793 |

A flaw was found in NetworkManager-vpnc. This vulnerability allows a local unprivileged user to escalate privileges to root. By injecting a newline character into the VPN username field, an attacker can manipulate the vpnc configuration to execute an arbitrary program with root privileges when the malicious VPN connection is activated.

### CVE-2026-91839

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-25T18:17:32.660 |

A flaw was found in NetworkManager-fortisslvpn, the FortiSSLVPN plugin for NetworkManager. The nm-fortisslvpn-service improperly handles carriage-return/line-feed (CR/LF) characters in VPN connection profile credentials. A local unprivileged user can exploit this by crafting a malicious VPN profile to inject additional configuration directives. This can lead to arbitrary code execution with root privileges when the crafted VPN connection is activated.

### CVE-2026-91838

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-25T18:17:32.530 |

A flaw was found in NetworkManager-sstp, the SSTP VPN plugin for NetworkManager. A local unprivileged user can exploit this vulnerability by embedding special characters, known as shell metacharacters, into VPN connection profile fields such as CA certificate or proxy settings. These unescaped characters are then processed by the `pppd` daemon, which runs with root privileges, allowing the attacker to execute arbitrary commands with elevated permissions when a malicious VPN connection is activated.

### CVE-2026-91837

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-25T17:17:18.983 |

A flaw was found in NetworkManager-iodine, the iodine VPN plugin for NetworkManager. A local unprivileged user can exploit a vulnerability in how the 'nameserver' setting is processed when establishing an iodine VPN connection. By embedding shell metacharacters (special characters that can execute commands) in the 'nameserver' value, an attacker can inject and execute arbitrary commands. These commands run with root privileges before the application drops its elevated permissions, leading to local privilege escalation.

### CVE-2026-100709

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-26T14:16:56.417 |

Froxlor through 2.3.10 stores only a numeric user ID in remembered-2FA tokens (panel_2fa_tokens) without recording the account namespace, and the remembered-token lookup during login is not constrained to the customer or administrator account type. Because customer and administrator IDs are allocated from separate namespaces, a remembered-2FA token legitimately issued to a customer with a given ID also matches an administrator with the same ID. An attacker who controls a customer account with a colliding ID, holds a valid remembered-2FA cookie for it, and already knows the target administrator's password can bypass the administrator's TOTP second factor and obtain an authenticated administrator session. This is a second-factor bypass only; it does not defeat password authentication. Fixed in 2.3.12.

### CVE-2026-100610

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-26T14:16:41.460 |

Flowise through 3.1.4 exposes GET /api/v1/upsert-history/:id and PATCH /api/v1/upsert-history without route-level permission checks, and the backing service performs no workspace or ownership validation. getAllUpsertHistory() returns UpsertHistory rows selected solely by an attacker-supplied chatflowid, and patchDeleteUpsertHistory() deletes rows by an attacker-supplied array of record UUIDs. As a result, any authenticated low-privilege user or valid API key can read or delete document-store upsert history belonging to other users and other workspaces whenever the target chatflowId (which is exposed publicly in /chatbot/<chatflowId> share links) or row ids are known. The retrievable flowData and result fields contain embedding, record-manager and vector-store node configuration, including per-node paramValues. No patched version is available.

### CVE-2026-100560

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T03:17:02.833 |

OpenClaw versions before 2026.8.1 contain an authorization bypass vulnerability where Allow Always approvals for exact commands persist as path-only grants on macOS and Linux. Attackers can reuse the same executable with different arguments to execute commands without triggering new approval prompts, potentially accessing files or internal services.

### CVE-2026-100543

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T03:17:00.287 |

OpenClaw (npm package openclaw) before 2026.8.1 could include deterministic hashes computed over the original, unredacted configuration in redacted configuration responses. When the Gateway password had low entropy and the remaining configuration values were reconstructable, these hashes acted as offline password verifiers: a caller able to obtain the redacted configuration (for example via config.get) could test password candidates offline without going through the rate-limited Gateway authentication path. Recovering the password could grant the documented shared-secret operator authority. Secret references were not affected in the same way. The issue is fixed in 2026.8.1.

### CVE-2026-100541

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-09-26T03:16:59.987 |

OpenClaw's Matrix integration (npm package @openclaw/matrix) versions >= 2026.2.2 and < 2026.8.1 lowercase complete Matrix user IDs — including historical localparts and the case-sensitive server-name portion — when deriving the OpenClaw authorization identity. As a result, distinct authenticated Matrix accounts can normalize to the same authorization identity. A Matrix participant controlling a colliding account identifier (a protocol-valid identifier that differs from the configured one only by characters OpenClaw case/Unicode folds; display-name matching is not required) can inherit allowlist, owner-command, exec-approval, or plugin-approval authority configured for another account. The issue is fixed in 2026.8.1.

### CVE-2026-100535

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T03:16:59.103 |

OpenClaw (npm package 'openclaw') versions >= 2026.4.5 and < 2026.8.1 can lose the originating requester's restrictions and untrusted provenance when session-derived text is persisted to session memory. In deployments where session-memory capture and dreaming are enabled, a restricted external sender whose messages are admitted with limited tools can persist instructions that are later supplied to an unattended background (dreaming) agent holding broader file and command capabilities, allowing actions beyond the authority of the original turn and affecting files, commands, or services available to that agent. Exploitation requires the content to be captured, selected for later processing, and followed by the model. The issue is fixed in 2026.8.1.

### CVE-2026-49470

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-25T19:16:58.220 |

GLPI is a free asset and IT management software package. From 11.0.0 until 11.0.8, the time-based one-time password verification endpoint does not limit failed submissions per user. An attacker who has obtained a user's primary authentication credentials can repeatedly submit TOTP values against the MFA verification flow, making brute-force compromise of the second factor and subsequent account takeover possible. This issue is fixed in version 11.0.8.

### CVE-2026-100609

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-26T14:16:41.297 |

Flowise (npm packages `flowise` and `flowise-components`) through 3.1.4 looks up credentials by ID without filtering on the requesting user's workspace (findOneBy({ id: credentialId }) with no workspaceId condition) in several code paths: getAllOpenaiAssistants/getSingleOpenaiAssistant (GET /api/v1/openai-assistants and /api/v1/openai-assistants/:id), uploadFilesToAssistant (POST /api/v1/openai-assistants-file/upload/), deleteAssistant (DELETE /api/v1/assistants/:id, reachable by first importing a poisoned assistant row via POST /api/v1/export-import/import), and the shared helper used by getVoices (GET /api/v1/text-to-speech/voices). An authenticated user of one workspace can supply a credential UUID belonging to another workspace, causing the server to decrypt and use that workspace's OpenAI or ElevenLabs API key on the attacker's behalf. No patched version was available at the time of publication.

### CVE-2026-100540

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T03:16:59.833 |

OpenClaw Feishu before 2026.8.1 fails to validate whether a configured default account is disabled before selecting it for model tool operations. Attackers can exploit multi-account setups where a disabled default account retains credentials to read or modify Feishu resources through a revoked identity.

### CVE-2026-67239

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T17:17:12.030 |

RabbitMQ is a messaging and streaming broker. From 3.13.0 until 3.13.18 and 4.0.23 and 4.1.14 and 4.2.9 and 4.3.3, Stored XSS via TLS peer-certificate DN in stream-management UI (sibling of V-11). lines 102/106/110 render peercertsubject / peercertissuer with raw <%= %> and no fmtstring(). RFC4514 backslash-escaping of </> is HTML-inert and bypassable (<img ... //>). Requires non-default config: a stream TLS listener with verifypeer and an attacker-obtainable trusted cert with a malicious Same as the connection.ejs finding, against operators viewing the stream-connection detail rabbitmqstream + rabbitmqstreammanagement enabled with a TLS listener using verifypeer Attacker can obtain a certificate signed by a CA the listener trusts, with attacker-chosen DN An operator views the. This issue is fixed in versions 3.13.18 and 4.0.23 and 4.1.14 and 4.2.9 and 4.3.3.

### CVE-2026-100605

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-26T14:16:40.620 |

Flowise through 3.1.4 contains missing route-level RBAC checks on chat message endpoints that allow low-privileged API keys to read and delete chat history. Attackers with valid but low-privileged API keys can access GET and DELETE chat message routes without required flow permissions to read chat histories, prompts, model responses, and delete messages.

### CVE-2026-100598

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-26T03:17:08.487 |

OpenClaw (npm package openclaw) before 2026.7.1 incorrectly binds Signal approval reactions. In affected versions, a reaction intended to resolve a structured approval request could instead attach to ordinary outbound text when unrelated outbound messages and a pending approval are present in the same conversation. As a result, an approver's reaction to unrelated text could be interpreted as approving or denying a pending host action; the practical impact depends on the pending request, conversation timing, and the actions available to the OpenClaw process. The issue does not change the authority of correctly identified approvers. This is fixed in version 2026.7.1.

### CVE-2026-88003

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-25T22:18:49.580 |

InvoicePlane is a self-hosted open source application for managing invoices, clients, and payments. Prior to 1.7.2, InvoicePlane fails to revoke administrative privileges after a role downgrade because Admin_Controller trusts the user_type snapshot stored in an existing session instead of revalidating ip_users.user_type. When one administrator downgrades another account, the target's active session continues to authorize administrative requests. The downgraded user can use Users::form() to set user_type back to 1, restoring the database role and making the privilege escalation persistent. This vulnerability is fixed in 1.7.2.

### CVE-2026-91765

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-25T21:17:24.550 |

cleanup_xml_node() in the SOAP XML parser recurses once per XML nesting level with no depth limit. An unauthenticated attacker can post a SOAP request containing tens of thousands of nested elements to any SoapServer endpoint, exhaust the stack and crash the process. The same unbounded recursion exists in the SOAP value decoder and in the WSDL node search helper.

### CVE-2026-57443

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-25T21:17:23.413 |

SCBE-AETHERMOORE is a geometric AI governance and evaluation framework. Starting in version 4.0.2 and prior to version 4.2.1, the AetherBrowser API server (`scripts/aetherbrowser/api_server.py`) exposes the `POST /api/ops/check-email` endpoint without any authentication. Any remote attacker can call this endpoint and trigger execution of the `email_reader.py` subprocess, which connects to configured ProtonMail or Gmail accounts via IMAP and returns email metadata (sender, subject, body snippet) in the JSON response. The server binds to `0.0.0.0:8100` by default with CORS set to `allow_origins=["*"]`, making it reachable from any network or browser origin. Version 4.2.1 patches the issue.

### CVE-2026-10758

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-25T21:17:23.117 |

Esri LERC is an open-source image or raster format which supports rapid encoding and decoding for any pixel type. A Heap based Out-of-Bounds Write via Integer Overflow in LERC versions 4.1.0 and earlier may allow a remote, unauthenticated attacker who can pass specifically crafted attacker controlled imagery to an application that uses LERC to crash the application, leading to a denial of service.

### CVE-2026-5267

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-25T20:17:11.613 |

Ciena Navigator Network
Control Suite (NCS) contains an information exposure vulnerability in an
event-streaming API that does not properly enforce authentication. An
unauthenticated attacker with network access to the affected service could
access the event stream and potentially obtain sensitive information.

### CVE-2026-100208

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-25T20:17:04.760 |

Integer overflow or wraparound in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-53625

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-25T19:17:27.477 |

GLPI is a free asset and IT management software package. From 0.70 until 10.0.26 and 11.0.8, a technician can manipulate the authtype value through the API to change another user's authentication method. Under configurations using the legacy API REST interface or SSO logins, this can change a super-administrator's authentication method and enable account takeover. This issue is fixed in versions 11.0.8 and 10.0.26.

### CVE-2026-53610

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T19:17:27.123 |

GLPI is a free asset and IT management software package. From 11.0.0 until 11.0.8, an attacker can craft a URL for a dashboard that reflects attacker-controlled markup without sufficient output encoding. A user who opens the crafted URL triggers reflected cross-site scripting in the dashboard. This issue is fixed in version 11.0.8.

### CVE-2026-67237

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T17:17:11.883 |

RabbitMQ is a messaging and streaming broker. From 4.2.0 until 4.2.8 and 4.3.2, set_token_auth/2 inserted a bearer token from the Authorization header or access_token cookie into OAuth bootstrap JavaScript without escaping, allowing attacker-controlled token content to execute JavaScript in the management UI origin. The endpoint is exposed before authentication only when management.oauth_enabled is true, and exploitation through the cookie path additionally requires the attacker to plant an access_token cookie on the management host. This issue is fixed in versions 4.2.8 and 4.3.2.

### CVE-2026-50547

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-98` |
| Published | 2026-09-25T16:17:26.300 |

InvoicePlane is a self-hosted open source application for managing invoices, clients, and payments. Prior to 1.7.2, InvoicePlane's Invoices::generate_xml() method appends a database-derived xml_id to the XMLconfigs helper directory and includes the resulting PHP path without validating the identifier. A low-privileged attacker who can influence the e-invoice configuration can use traversal sequences to include an existing PHP file. The standalone advisory establishes local file inclusion; code execution requires a separate file-upload or file-write primitive. This issue is fixed in version 1.7.2.

### CVE-2026-49850

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-98` |
| Published | 2026-09-25T16:17:26.140 |

InvoicePlane is a self-hosted open source application for managing invoices, clients, and payments. Prior to 1.7.2, InvoicePlane exposes Invoices::delete() and Invoices::delete_invoice_tax() as state-changing routes without requiring POST and validating a CSRF token. When an authenticated administrator loads attacker-controlled content that requests an affected route, the application can delete an invoice or invoice tax record. The cross-origin action can remove financial data without the administrator's intent. This issue is fixed in version 1.7.2.

### CVE-2026-84882

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-25T15:17:56.273 |

IBM Guardium Data Protection 12.2 is vulnerable to path traversal in the Universal Connector Oracle Wallet upload component. An authenticated remote attacker could exploit this vulnerability to write arbitrary files to the system.

### CVE-2026-100529

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T03:16:58.217 |

OpenClaw versions before 2026.8.1 contain an authorization scope widening vulnerability in file-transfer allow-always approvals that allows attackers to reuse standing grants for unreviewed paths. Attackers can exploit glob metacharacter interpretation and node display name reuse to access sibling paths or different nodes beyond the operator's original approval scope.

### CVE-2026-100504

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-26T01:17:00.043 |

Ghidra versions through 12.1.4 contain a stack-based out-of-bounds write vulnerability in the decompiler's leftshift128 function when processing negative shift amounts from p-code. Attackers can craft malicious binaries with specific instruction sequences that trigger the overflow when decompiled, corrupting memory and potentially achieving code execution.

### CVE-2026-100419

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-25T22:17:10.613 |

gitoxide gix-fs before 0.23.0 contains a path validation bypass vulnerability in the worktree checkout mechanism that allows attackers to escape the worktree directory via symlink manipulation. During forced checkout with overwrite_existing enabled, attackers can craft malicious repository trees where symlink entries replace validated directories, causing subsequent files to be written outside the worktree through the symlink for code execution or file manipulation.

### CVE-2026-100310

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-09-25T20:17:05.833 |

GNU libextractor before 1.16 loads plugins from an untrusted search path specified by the LIBEXTRACTOR_PREFIX environment variable without proper privilege checks. A local attacker can exploit this by setting LIBEXTRACTOR_PREFIX to a directory containing a malicious plugin that executes arbitrary code with elevated privileges when loaded by a setuid or setgid program.

### CVE-2026-100642

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-26T14:16:46.247 |

SiYuan versions from v2.1.0 before v3.8.4 contain a cross-site request forgery vulnerability in the CheckAuth lock-screen pass-through branch that grants administrator access to loopback requests without validating Origin headers. Attackers can craft malicious web pages that force victims to terminate the kernel process, read workspace configuration and proxy settings, and trigger administrative actions via zero-credential cross-origin requests from the victim's browser.

### CVE-2026-100627

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-26T14:16:43.837 |

Capgo (Cap-go/capgo.app) server backend Supabase functions contain an incorrect authorization flaw in the API-key bundle promotion path. The PUT /bundle endpoint, available to "all" and "write" API keys, dispatches to setChannel, which authorizes with checkPermission(c, 'channel.promote_bundle', { appId: body.app_id }) and omits the request's channel_id. Because the omitted scope field is passed to rbac_check_permission_direct as SQL NULL, and channel-scope override evaluation is gated on p_channel_id IS NOT NULL, per-channel allow/deny overrides are never evaluated. A principal holding app-level channel.promote_bundle (granted by default to the app_developer and app_uploader roles) can therefore promote a bundle to a channel for which an explicit per-channel deny override exists, updating public.channels.version for the supplied channel_id; the target channel is only validated after authorization. The issue is confirmed on main at commit de66fa51e7ff2f50283cc1455c3d80ab3eb0ae43 and likely earlier versions; no patched version is known at the time of publication.

### CVE-2026-100579

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-26T03:17:05.633 |

OpenClaw (npm package 'openclaw') before 2026.7.1 incorrectly trusts requester provenance in message.action. In identity-bearing Gateway deployments (authentication modes that honor caller identity and narrower operator scopes), a write-scoped caller can supply another sender's identifier to the channel authorization checks and invoke a channel action under that spoofed requester identity, reaching operations the channel adapter would have denied to the real caller. Practical impact depends on the enabled channel, the action, and the target account's permissions. Shared-secret token and password callers are full trusted operators under OpenClaw's security model and are out of scope. The issue is fixed in 2026.7.1; as a workaround, restrict message.action to administrators and disable sensitive channel actions that rely on requester identity.

### CVE-2026-100578

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-26T03:17:05.483 |

OpenClaw (npm package `openclaw`) before 2026.7.1 fails to restrict owner-only infrastructure tools exposed through the chat.send endpoint. In Gateway deployments using authentication modes that honor caller identity and narrower operator scopes, a write-scoped non-owner caller can start a chat turn whose tool inventory includes the `gateway` and `cron` tools, causing the agent to invoke owner-only configuration or scheduling operations, including persistent state changes. Practical impact depends on the tools selected by the model and the caller's ability to steer the turn. Shared-secret token and password callers are treated as fully trusted operators under OpenClaw's security model and are outside the scope of this issue. The issue is fixed in 2026.7.1; as a workaround, restrict chat.send to administrators in identity-bearing deployments and remove `gateway` and `cron` from affected agent tool policies.

### CVE-2026-100532

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-26T03:16:58.660 |

@openclaw/whatsapp (npm) before 2026.8.1 exposes the WhatsApp login tool through the generic channel-tool path without preserving the originating sender's owner status, so the owner-only tool boundary is not enforced. An admitted non-owner sender able to steer the tool can request a forced login and receive a new QR code for a configured account, disconnecting the Gateway's WhatsApp account and causing loss of availability; full account relinking additionally requires the attacker to scan the returned QR code with another phone. The issue affects the owner-only tool boundary rather than WhatsApp transport authentication. Fixed in 2026.8.1.

### CVE-2026-100387

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-25T21:17:22.163 |

pgPointcloud through 1.2.5 contains a heap out-of-bounds read vulnerability in dimensional patch WKB deserialization that allows authenticated database users to read adjacent heap memory. Attackers can supply crafted pcpatch values with attacker-controlled size fields to copy heap memory into stored patches for exfiltration or crash the PostgreSQL backend.

### CVE-2026-42324

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-25T16:17:25.793 |

Piwigo is a full featured open source photo gallery application for the web. Prior to 16.4.0, admin/element_set_ranks.php stores administrator-controlled image_order[] values without enforcing the existing sort-field whitelist. The stored album image_order expression is later concatenated into ORDER BY clauses by admin/batch_manager_global.php, admin/batch_manager_unit.php, include/section_init.inc.php, and include/ws_functions/pwg.categories.php. When at least one album contains at least one photo, an authenticated administrator can store a crafted expression and trigger it in a later album or Batch Manager query to disclose, modify, or disrupt database data. This issue is fixed in version 16.4.0.

### CVE-2026-42323

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-25T16:17:25.607 |

Piwigo is a full featured open source photo gallery application for the web. Prior to 16.4.0, admin/batch_manager.php accepts administrator-controlled dimension width, height, and ratio values and filesize values from the Batch Manager filter URL without numeric validation. The URL filter parser stores those values in the bulk_manager_filter session state, and later query construction concatenates them into SQL predicates, unlike the validated POST filter path. An authenticated administrator can use crafted filter values to execute time-based or other SQL expressions and potentially disclose, modify, or disrupt database data. This issue is fixed in version 16.4.0.

### CVE-2026-33639

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-25T16:17:24.867 |

InvoicePlane is a self-hosted open source application for managing invoices, clients, and payments. Prior to 1.7.2, InvoicePlane interpolates the administrator-controlled tax_rate_decimal_places setting into an ALTER TABLE statement for ip_tax_rates in Settings::index() without strict integer validation. A crafted setting value can add clauses to the schema-changing statement and remove or alter required database columns. The resulting schema corruption can permanently modify financial data structures and make the application unavailable. This vulnerability is fixed in 1.7.2.

### CVE-2026-84862

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-25T15:17:56.110 |

IBM Guardium Data Protection 12.2 is vulnerable to insecure deserialization in the Quartz JDBC job store. An authenticated attacker could exploit this vulnerability to execute arbitrary code on the affected system.

### CVE-2026-100719

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T14:16:58.077 |

Froxlor versions before 2.3.12 contain a credential disclosure vulnerability in the DirProtections.listing API command that returns htpasswd password hashes. Authenticated API users can retrieve bcrypt password hashes for protected-directory users, enabling offline cracking attempts and exposure of reused credentials.

### CVE-2026-100718

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-09-26T14:16:57.917 |

Froxlor through 2.3.10 does not enforce the mail.allow_external_domains policy in the EmailSender.add API command. When an administrator has enabled the allowed-sender feature but disabled external allowed-sender domains (mail.enable_allow_sender = 1, mail.allow_external_domains = 0), an authenticated customer with API access can still use EmailSender.add to register an arbitrary external sender address for their mailbox, which is stored despite the policy. This creates a bypass between the UI/administrator configuration and the API, and — where the generated mail configuration consumes the allowed-sender table — allows a customer to authorize sender identities outside their hosted domains, facilitating sender spoofing. Fixed in 2.3.12.

### CVE-2026-100713

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-26T14:16:57.067 |

Froxlor 2.3.10 and earlier contain a time-of-check time-of-use (TOCTOU) race condition in the SSH key synchronization cron (lib/Froxlor/Cron/System/SshKeys.php, SshKeys::generateFiles). The containment/symlink validation performed by FileDir::makeCorrectDir()/makeCorrectFile() is done only at check time; the live filesystem path is re-resolved as root at write time (file_put_contents with FILE_APPEND|LOCK_EX, followed by chmod/chown/chgrp), with a database round-trip and file reads in between, and no path or file-descriptor pinning (no O_NOFOLLOW or openat2(RESOLVE_NO_SYMLINKS)). On installations where the non-default setting system.allow_customer_shell=1 grants customers local shell access, a customer can atomically swap their ~/.ssh directory for a symlink after the check and before the write, causing the root-run cron to append the customer's public key to /root/.ssh/authorized_keys and to chown /root/.ssh to the customer, resulting in full root compromise of the panel host. The cron re-runs on every interval, allowing unlimited attempts. This is a residual race that bypasses the check-time fix introduced for GHSA-mq5v-... . The issue is fixed in Froxlor 2.3.12.

### CVE-2026-100712

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-26T14:16:56.903 |

froxlor through 2.3.10 disables a user's two-factor authentication immediately upon an unauthenticated-triggerable GET request to the 2FA management page (e.g. /customer_index.php?page=2fa&action=delete), with no confirmation, re-authentication, or CSRF token. The global CSRF middleware only covers POST/PUT/PATCH/DELETE requests, and the session cookie is set to SameSite=Lax, so a cross-site top-level navigation (link click or redirect) carries the victim's session and silently clears type_2fa/data_2fa. Both the customer and admin 2FA handlers are affected. An attacker who lures a logged-in panel user into following a crafted link reduces that account to password-only authentication, which can be chained with a compromised password for account takeover. Fixed in 2.3.12.

### CVE-2026-100708

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T14:16:56.153 |

Froxlor before 2.3.13 returns the ssl_key_file column — which stores the raw PEM TLS private-key content — verbatim in the JSON responses of the Certificates.get and Certificates.listing API commands, because the results of the underlying domain_ssl_settings queries are passed through ApiCommand::response() without any field stripping or allowlist. A low-privileged authenticated customer API caller can retrieve the private keys of their own domains' certificates, including Let's Encrypt keys that Froxlor generates server-side and stores root-only (0600) and to which the customer otherwise has no filesystem access; reseller and customers_see_all admin accounts can dump the private keys of other principals through the same sink. Disclosed keys enable domain impersonation, passive decryption of captured TLS traffic, and active machine-in-the-middle attacks.

### CVE-2026-100688

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-26T14:16:53.280 |

Budibase server before 3.45.0 contains a cross-tenant information disclosure vulnerability in the GET /api/applications/:appId/appPackage endpoint that allows authenticated users to read another tenant's application metadata and source code. Attackers can supply a victim tenant's app id to retrieve sensitive application details including navigation structure, role names, internal screen URLs, JavaScript snippets, and user identifiers without authorization checks.

### CVE-2026-100679

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-26T14:16:51.993 |

stoatchat before 0.15.5 fails to validate that MFA tickets belong to the authenticated user, allowing attackers to bypass MFA by using their own valid ticket with another user's session token. Attackers can obtain a ticket from their own account and use it with a victim's session token to disable TOTP, view recovery codes, or perform other sensitive operations without providing the victim's credentials.

### CVE-2026-100675

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-26T14:16:51.440 |

stoatchat versions before 0.15.5 contain a denial of service vulnerability in the acknowledgement worker that processes mass mention messages. Authenticated users can send five crafted role-mention messages to terminate all acknowledgement workers, disabling push notifications and mention badges deployment-wide until the API process restarts.

### CVE-2026-100668

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T14:16:50.273 |

Grav 2.0.0 through 2.0.24 contain a Twig content sandbox escape. The `array` filter (and its identical function form) is on the sandbox allowlist but is registered without the needs_is_sandboxed guard that print_r, vardump, json_encode, yaml_encode and string carry, and its implementation calls toArray() — or falls back to an (array) cast — without consulting the sandbox method allowlist. Because the `grav` Twig global is the raw Pimple-based dependency injection container, a user who can author Twig in page content can evaluate `grav|array` to read the container's private $values array, including the un-redacted Config service; a second array cast returns the entire configuration tree, disclosing plugin credentials, SMTP and OAuth secrets, Redis passwords, proxy URLs and the security.* subtree that the sandbox's redaction is meant to hide. Because the payload is stored in page content, the disclosed configuration is rendered to anonymous visitors. Grav 1.7 is not affected as it has no Twig content sandbox. Fixed in Grav 2.0.25.

### CVE-2026-100654

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-09-26T14:16:48.100 |

vLLM before 0.29.0 accepts user-controlled stop_token_ids on the OpenAI-compatible POST /v1/completions and POST /v1/chat/completions endpoints but validates only that the values are integers, not that each token id is within the model vocabulary/logits range. When min_tokens > 0, the stop token ids are used as logits indices to suppress stop tokens, so an out-of-range id reaches a CUDA indexing operation (index_put_) and triggers a device-side assertion. An authenticated API user can send a single malformed completion request that returns 500 Internal Server Error and puts EngineCore into a fatal state, causing subsequent requests to fail until the service is restarted (denial of service).

### CVE-2026-100651

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-26T14:16:47.663 |

vLLM before 0.29.0 fails to enforce decoder prompt-length validation on the disaggregated serving endpoint /inference/v1/generate. When the request contains a 'features' (multimodal) payload, vllm/entrypoints/serve/disagg/serving.py builds a multimodal EngineInput directly from the caller-supplied token_ids, and GenerateRequest.token_ids (vllm/entrypoints/serve/disagg/protocol.py) is not checked against model_config.max_model_len. For multimodal processors that report skip_prompt_length_check=True (for example Nemotron Parse, Whisper, and FireRedLID), InputProcessor._validate_prompt_len() returns immediately for both encoder and decoder prompts, so an overlong prompt becomes an EngineCoreRequest and reaches the worker input-batch copy into a fixed max_model_len-wide NumPy row. A client able to reach the endpoint on an affected model configuration can therefore submit an overlong token_ids list to trigger a worker failure and denial of service. Fixed in 0.29.0.

### CVE-2026-100650

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-26T14:16:47.523 |

vLLM through 0.29.0 fetches and fully materializes remote or inline media before enforcing its documented media controls (the VLLM_MAX_AUDIO_CLIP_FILESIZE_MB compressed-audio size cap, default 25 MB, and the per-modality --limit-mm-per-prompt item limits). Across four ingress paths — the shared media-acquisition layer (HTTPConnection.get_bytes()/async_get_bytes()), the chat completions audio_url/base64 path, the batch speech runner, and the Rust frontend POST /tokenize route — the server reads the entire HTTP response body, base64-decodes the inline payload, or spawns one fetch/decode task per media part, and only then applies the limit (or, on some paths, never applies it). A remote attacker can therefore cause the API server or batch-runner process to allocate memory and consume outbound bandwidth proportional to an attacker-chosen body size or media item count before the request is rejected, resulting in pre-inference memory and bandwidth exhaustion (denial of service). The chat and batch surfaces require an API key when one is configured; the Rust frontend /tokenize route is unauthenticated by design. There is no code execution or data disclosure impact.

### CVE-2026-100632

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T14:16:44.540 |

Parse Server is an open-source backend server. In versions >= 9.0.0 and < 9.10.1-alpha.8, and in versions < 8.6.89, LiveQuery evaluates the protectedFields class-level permission against an incompletely resolved caller identity: the subscriber's roles are not resolved, and when a subscription does not supply its own session token the event payload is redacted against an anonymous identity even though the read was authorized against the connected user. As a result, field masks defined for a role, for authenticated users, or for a specific user are not applied, so an authenticated subscriber can receive field values that the REST API correctly withholds and can use a masked field to filter or watch a subscription. Only classes with LiveQuery enabled that define protectedFields under a role:, authenticated, or per-user group are affected; masks under the public (*) group are applied correctly. The issue is fixed in 9.10.1-alpha.8 and 8.6.89. As a workaround, additionally define the affected field masks under the public (*) group, or disable LiveQuery for classes whose class-level permissions rely on role-scoped, authenticated, or per-user protectedFields groups.

### CVE-2026-100611

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-26T14:16:41.610 |

Capgo (capgo.app backend, versions ≤ 12.261.0) improperly restricts which roles the apikey_manager organization role may bind to newly created API keys. When an authenticated user holding only apikey_manager (permissions org.manage_apikeys and org.read) calls POST /apikey with a JWT session, the only checks applied are the org.manage_apikeys permission, a fixed deny-list of assignable role names (APIKEY_MANAGER_DENIED_ASSIGNABLE_ROLES in public/apikey/scope.ts), and a priority-rank comparison in createRoleBindingForPrincipal (private/role_bindings.ts). No check verifies that the caller actually holds the permissions conferred by the role being assigned. Because the deny-list omits the deploy roles app_developer, app_uploader, channel_developer and channel_uploader, and apikey_manager is seeded with priority_rank 78 — higher than those roles' ranks (68, 66, 58, 57) — the rank check also passes. As a result, an apikey_manager who cannot upload bundles or promote channels can mint an API key bound to a deploy role and use it to push arbitrary OTA JavaScript updates to all end users of the organization's apps. As of the advisory publication no patched version was available.

### CVE-2026-100602

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-26T14:16:40.187 |

ClawHub (openclaw/clawhub application/backend) contains a missing authorization check in the changelog preview feature. A signed-in caller can invoke the public skills:generateChangelogPreview action for a skill they are not authorized to access; the previous version is read without the file-read authorization enforced on normal content access, and up to 8,000 characters of quarantined content may be submitted to the AI provider and reflected in the preview returned to the caller, disclosing restricted skill content. The issue was confirmed at revision cbfee7343ddc867316dd9b3de6fa8856730f9f41; the complete historical affected range was not established. It is fixed by PR #3682, included in revision 8c2de6c506bb4efabe3f0c2ffb8370b9e23d4650, which was deployed to clawhub.ai on 2026-09-11; self-hosted deployments should update to that revision or a later descendant. The npm CLI and OpenClaw runtime are separate products and are not affected.

### CVE-2026-100595

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T03:17:08.037 |

OpenClaw versions before 2026.7.1 contain an authorization bypass vulnerability in the diagnostics export command that allows non-owner channel senders to access owner-only host diagnostic bundles. Attackers can request and receive diagnostic details about the host, configuration, runtime, and connected services intended only for owners.

### CVE-2026-100594

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T03:17:07.857 |

OpenClaw versions before 2026.7.1 contain an authorization bypass vulnerability in the /export-trajectory endpoint that allows non-owner senders to request and receive owner-only trajectory bundles. Attackers can access prompts, model messages, tool schemas, runtime events, and local path metadata from affected sessions by exploiting insufficient authorization checks.

### CVE-2026-100582

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-26T03:17:06.080 |

OpenClaw channel plugins (@openclaw/msteams, @openclaw/feishu, @openclaw/matrix, and @openclaw/googlechat) before 2026.8.1 do not enforce the configured channel read allowlist for caller-supplied explicit read targets in message, reaction, pin, member, and related metadata read actions. A lower-trust sender or a steered agent with access to a channel read action can therefore retrieve content or metadata from channels or rooms excluded by the operator's read policy; the practical impact depends on the permissions held by the connected bot account. The issue is fixed in 2026.8.1.

### CVE-2026-100555

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-26T03:17:02.087 |

OpenClaw is an npm-distributed gateway application. In versions >= 2026.7.1 and < 2026.8.1, Synology Chat attachment delivery could lose DNS pinning: the Gateway validated a single DNS result for a supplied file URL but then passed the original hostname to the Synology NAS, where it could resolve to a different destination. When attachment delivery accepted a remotely influenced hostname, an attacker could use DNS rebinding to make the NAS fetch a private or otherwise policy-denied resource and return its contents to the addressed conversation (server-side request forgery). Practical impact depends on NAS routing, resolver behavior, and the response available at the private destination. The issue is fixed in 2026.8.1; as a workaround, disable remote URL attachment forwarding in Synology Chat.

### CVE-2026-100538

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T03:16:59.537 |

OpenClaw (npm package 'openclaw') before 2026.8.1 does not apply the originating sender's global or per-agent toolsBySender policy when handling outbound attachments. A sender that has been explicitly denied filesystem read tools can still cause a known local file to be read and returned via a final-response media directive or a message attachment, disclosing local file contents to an admitted requester whose agent turn did not include the read tool. Exploitation requires knowledge or derivation of a useful host path and a delivery flow that accepts local attachments. The issue is fixed in version 2026.8.1.

### CVE-2026-100536

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-26T03:16:59.247 |

OpenClaw versions before 2026.8.1 fail to validate all source fields in structured message attachments, allowing attackers to hide unvalidated host paths behind allowed attachment sources. Attackers can exploit this by providing multiple source fields to bypass sandbox path validation and cause Telegram delivery to read and send known host files that would otherwise be rejected.

### CVE-2026-100531

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-26T03:16:58.513 |

The @openclaw/slack npm package before 2026.8.1 contains an authorization flaw in its Slack download-file handler: when a file lacks the share metadata used to prove it belongs to the requested conversation, the conversation-authorization check fails open. An authenticated caller restricted to a single conversation who knows or obtains a file identifier can therefore download file contents from outside that conversation's scope, disclosing data across configured conversation boundaries. The issue does not allow listing arbitrary Slack files and does not bypass Slack authentication itself. The issue is fixed in version 2026.8.1.

### CVE-2026-57449

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-284;CWE-863` |
| Published | 2026-09-25T23:16:53.990 |

Actual is a local-first personal finance tool. Prior to 26.7.0, Actual Sync Server's CORS proxy is intended to let authenticated users fetch resources only from repositories listed in the official plugin allowlist. When `ACTUAL_GITHUB_TOKEN` is configured, the proxy automatically attaches the server's GitHub token to GitHub requests. The GitHub API allowlist check uses a raw `startsWith()` prefix test for `/repos/{owner}/{repo}` without requiring a path boundary after the repository name. If an allowlisted public plugin repository is `https://github.com/acme/plugin`, the proxy also accepts GitHub API URLs. Those URLs are outside the allowlisted repository but still pass because their API path starts with `/repos/acme/plugin`. The proxy then forwards the request with the server's `ACTUAL_GITHUB_TOKEN`, allowing any authenticated Actual user to read private GitHub resources reachable by that token. Version 26.7.0 fixes the issue.

### CVE-2026-84465

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-295;CWE-347` |
| Published | 2026-09-25T19:17:58.123 |

Zammad is a web based open source helpdesk/customer support system. Prior to 7.1.2, when Zammad checks the digital signature on an incoming S/MIME-signed email, it does not verify that the signing certificate is genuinely trusted, it only checks whether a certificate with a matching name is already stored in the system. An attacker can create their own certificate using the name of a real, previously trusted sender and use it to send a forged email. Zammad will display that email with the same "validly signed" indicator as a genuine message from the real sender, even though the attacker never had access to that sender's actual certificate or private key. This issue is fixed in version 7.1.2.

### CVE-2026-84464

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-639;CWE-863` |
| Published | 2026-09-25T19:17:57.917 |

Zammad is a web based open source helpdesk/customer support system. Prior to 7.1.2, zammad's External Data Source feature, used to look up records from an external system, did not properly verify whether a user was allowed to see a specific ticket, user, group, or organization before including its details in a request to that external system. An authenticated user, including one with only basic customer access, could exploit this by referencing another record's ID, and thereby view details of tickets, customer accounts, teams, or organizations that did not belong to them. This issue is fixed in version 7.1.2.

### CVE-2026-53629

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-25T19:17:28.263 |

GLPI is a free asset and IT management software package. From 9.4.0 until 10.0.26 and 11.0.8, an attacker with the READ right on logs can craft a URL for the history tab that injects attacker-controlled values into a database query. This permits SQL injection through the history tab endpoint. This issue is fixed in versions 11.0.8 and 10.0.26.

### CVE-2026-53626

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-09-25T19:17:27.670 |

GLPI is a free asset and IT management software package. From 11.0.5 until 11.0.8, under certain conditions, permission logic can grant access to a document without confirming that the document is linked to the targeted item. A user can use an unrelated item that the user is permitted to view to read a document linked to an inaccessible item. This issue is fixed in version 11.0.8.

### CVE-2026-56727

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-347;CWE-391` |
| Published | 2026-09-25T18:17:26.630 |

Zammad is a web based open source helpdesk/customer support system. Prior to 7.0.2, summary In Zammad's inbound PGP email processing, the return value of the gpg verification call was silently discarded. Regardless of whether gpg reported a valid, invalid, or missing signature, the handler unconditionally wrote sign: { success: true, comment: "Good signature" } to the article's security preferences. Impact Any sender could tamper with the body of a multipart/signed PGP email, or craft a message with an entirely fabricated or mismatched signature, and Zammad would display it to the recipient as cryptographically verified with a "Good signature" label. Users and agents relying on Zammad's signature indicator to confirm message authenticity and integrity would be misled into trusting modified or forged content. The vulnerability affects all inbound PGP-signed emails processed while the PGP integration is enabled. This issue is fixed in version 7.0.2.

### CVE-2026-93365

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-25T17:17:19.487 |

Bludit CMS through 3.22.0 contains a missing authorization vulnerability that allows authenticated users holding the Author or Editor role to read the full content of private drafts and scheduled posts belonging to any other user, including administrators, by exploiting the content-get-list AJAX endpoint in bl-kernel/ajax/content-get-list.php. Attackers can send an authenticated GET request to the admin AJAX endpoint with the draft parameter set to true, triggering getList() without ownership constraints and returning serialized page objects site-wide, exposing pre-publication material and sensitive notes stored in administrator-owned drafts.

### CVE-2026-67419

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407;CWE-1333` |
| Published | 2026-09-25T17:17:13.830 |

RabbitMQ is a messaging and streaming broker. Prior to 4.3.5, an authenticated user who can bind a queue to a topic exchange and publish to it can use consecutive # segments in a binding key to make both topic matchers revisit the same trie-node and routing-key-suffix states without memoization. The matcher materializes duplicate destinations before deduplication, causing combinatorial CPU work and memory pressure that can disrupt routing for all tenants. This vulnerability is fixed in 4.3.5.

### CVE-2026-67408

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-25T17:17:12.767 |

RabbitMQ is a messaging and streaming broker. From 4.1.0 until 4.3.3, 4.2.9, and 4.1.11, Stream Management Super-Stream Binding Keys Allocation Allows Low-Privilege Node Denial of Service. rabbitMQ 4.3.1 with rabbitmqstreammanagement enabled accepts PUT /api/stream/super-streams/{vhost}/{name} requests from an authenticated management user that can access the target vhost. When the request body contains the binding-keys field, the handler parses the attacker-controlled comma-separated string and builds the full stream-name list before checking whether the user has permission to configure the resulting streams. A low-privileged management user with vhost access but no configure, write, or read permission can therefore force large transient allocations before the resource permission check. In a 768 MB memory-limited container, one HTTP PUT with about 4.5 MB of JSON body killed the RabbitMQ container with Docker state exited true An authenticated low-privileged management user can kill a memory-limited RabbitMQ node with one HTTP This issue is fixed in versions 4.3.3, 4.2.9, and 4.1.11.

### CVE-2026-56724

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-09-25T17:17:09.420 |

Zammad is a web based open source helpdesk/customer support system. Prior to 7.0.2, summary An issue with permission checks in the knowledge base management area has been identified. Under certain conditions, data validation for linked items was not fully enforced. This could have allowed users with limited read permissions to interact with items outside their assigned access scope. Data access has been strengthened in the current version through additional validation routines. This issue is fixed in version 7.0.2.

### CVE-2026-56723

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-25T17:17:09.263 |

Zammad is a web based open source helpdesk/customer support system. Prior to 7.0.2, a customer who can view a ticket cannot see internal ticket articles through the article listing API. However, the same customer can directly request an attachment belonging to an internal article via the attachment download endpoint, bypassing article-level authorization. This results in an inconsistency: The article listing hides internal articles from customers. The attachment download only checks the parent ticket, not the article, so the same customer can download the attachment directly. This issue is fixed in version 7.0.2.

### CVE-2026-93306

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-25T15:17:56.943 |

IBM Server Firmware FW1120.00 through FW1120.01, FW1110.00 through FW1110.31, FW1060.00 through FW1060.81, and FW950.00 through FW950.H3 is affected by a vulnerability in the ASMI web interface. An unauthenticated attacker on the management network can send a malformed HTTPS request to ASMI, causing the web server to crash with possible memory corruption and generate an error log. The ASMI web interface will restart automatically; however, repeated exploitation could result in a sustained loss of access to the ASMI management interface, resulting in an integrity and availability impact.

### CVE-2026-100687

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-26T14:16:53.140 |

Budibase Server before 3.45.0 fails to redact plaintext datasource credentials before broadcasting external table updates to the Builder collaboration websocket room. Attackers with Builder access can intercept unredacted datasource objects containing database passwords and API keys by observing table save or delete operations.

### CVE-2026-100629

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T14:16:44.117 |

Capgo (capgo.app backend) before 12.127.5 contains an authorization flaw in the PATCH /private/role_bindings/:binding_id endpoint. The handler verifies that the newly assigned role's priority rank does not exceed the caller's own rank, but — unlike the DELETE handler — it never checks the rank of the role currently bound to the target binding. An authenticated user holding the org_admin role (rank 90) can therefore change an org_super_admin binding (rank 95) to a lower-privileged role such as org_member (rank 75). Because the prevent_last_super_admin_binding_delete database trigger fires only BEFORE DELETE and not on UPDATE, an org_admin can demote every org_super_admin, leaving the organization with no super administrator. The issue is fixed in 12.127.5.

### CVE-2026-100616

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-26T14:16:42.333 |

capgo.app is an over-the-air update platform for Capacitor apps. In all versions prior to a fix, the row-level security UPDATE policy on the public.orgs table permits an organization admin (a user holding org.update_settings) to update the entire row, including the internal billing pointer column customer_id. The official organization update endpoint (supabase/functions/_backend/public/organization/put.ts) allowlists only a small set of editable settings fields and excludes customer_id, and the private Stripe billing route separately requires the org.update_billing permission. By sending an update directly to Supabase PostgREST, an authenticated org admin without org.update_billing can null or corrupt the organization's Stripe customer pointer, causing plan and billing checks that trust orgs.customer_id to fail and moving the organization from a valid paid plan state to unpaid/no-plan behavior. At the time of the advisory no patched version was available.
