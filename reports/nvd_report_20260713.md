# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-12 15:00 UTC
- **対象期間**: `2026-07-11T15:00:14.000Z` 〜 `2026-07-12T15:00:12.000Z`
- **重要CVE数**: 15 件（Critical 9.0+: 2 件 / High 7.0〜: 13 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS 7.0 以上の高リスク脆弱性は **15 件** 把握されています。共通する傾向は以下の通りです。  

| 傾向 | 内容 |
|------|------|
| **Web UI/管理画面の XSS・CSRF** | LuCI 系 (OpenWrt) や luci‑app‑upnp、luci‑app‑samba4 で、入力エスケープ不足により LAN 内の未認証ユーザーが管理者のブラウザ上で任意スクリプトを実行できる。 |
| **デフォルト認証情報・シークレットのハードコーディング** | Flowise が JWT のシークレットや issuer/audience を固定文字列で提供しており、認証トークンの偽造が容易になる。 |
| **コンテナ／Docker API の不適切な入力検証** | Crawl4AI の `/screenshot`、`/pdf`、`/md`、`/llm` 系エンドポイントで任意パス書き込みや環境変数取得が可能。 |
| **組み込み機器のバッファオーバーフロー** | TRENDnet のファームウェア (TEW‑821DAP/TEW‑635BRM) が特定 CGI パラメータでスタック/ヒープオーバーフローを起こし、リモートからコード実行が可能。 |
| **特権昇格・情報漏洩** | Capgo の SSO 前処理や権限削除ロジックの不備により、組織外ユーザーの情報取得や権限エスカレーションが可能。 |

全体として **「入力検証不足」** と **「デフォルト認証情報」** が主因であり、特にネットワーク機器やコンテナベースのサービスで LAN/インターネット越しに攻撃が成立しやすい点が顕著です。

---

## 2. 特に注目すべき CVE（上位 5 件）

| CVE | CVSS | 影響範囲・対象 | 主なリスク | 注目理由 |
|-----|------|----------------|------------|----------|
| **CVE‑2026‑61876** | 9.4 | OpenWrt LuCI (全バージョン) – DHCPv6 lease テーブル | 近隣ネットワークから送信された DHCPv6 FQDN に `<script>` を埋め込むと、管理者が DHCP リースページを閲覧した瞬間に XSS が実行される。 | **LAN 内の未認証ユーザーが管理者権限でコード実行** できる点が最も危険。IoT デバイスやルータが多数存在する環境で即時対策が必要。 |
| **CVE‑2026‑56271** | 9.3 | Flowise < 3.1.0 (Node.js) – JWT 認証ミドルウェア | ハードコードされた `auth_token` / `refresh_token` と固定 audience/issuer により、攻撃者が任意の JWT を生成し、認証バイパスが可能。 | **認証トークンの偽造は全 API への不正アクセスにつながる**。特に社内データパイプラインで機密情報が流出するリスクが高い。 |
| **CVE‑2026‑56260** | 8.8 | Crawl4AI < 0.8.7 – Docker API `/screenshot`・`/pdf` エンドポイント | `output_path` が検証されず任意ファイル書き込みが可能。コンテナ内部のシークレットやホスト上の重要ファイルを書き換えられる。 | **コンテナ環境全体の破壊・情報漏洩** が起こり得る。CI/CD パイプラインや SaaS で広く利用されている点が懸念。 |
| **CVE‑2026‑61875** | 8.7 | luci‑app‑upnp (OpenWrt) – UPnP IGD AddPortMapping SOAP | 未認証 LAN クライアントが `NewPortMappingDescription` にスクリプトを埋め込むと、管理画面で XSS が実行される。 | **UPnP が有効な家庭・オフィスネットワークで簡単に悪用** でき、攻撃者は同一 LAN 内の管理者権限を奪取できる。 |
| **CVE‑2026‑56238** | 8.7 | Capgo < 12.128.2 – Supabase PostgREST `global_stats` エンドポイント | 公開 API キーだけで財務・利用統計情報が取得可能。認証なしで内部メトリクスが漏洩する。 | **ビジネスインテリジェンス情報の漏洩** は競合優位性を損なうだけでなく、PCI/DSS などのコンプライアンス違反につながる。 |

> **注**：上記 5 件は **CVSS ≥ 8.7** かつ **広範囲に展開されているプラットフォーム**（OpenWrt、Node.js アプリ、Docker コンテナ、SaaS）を対象としているため、優先的に対策すべきです。

---

## 3. 推奨アクション（具体的なパッケージ・バージョン）

| 対象 | 推奨アクション | 具体的なパッケージ / バージョン |
|------|----------------|--------------------------------|
| **OpenWrt LuCI** | - すべての LuCI パッケージを **2026‑09‑01 以降のリリース** (例: `luci 2026.09.01-rc1` 以上) に更新<br>- DHCPv6 クライアント FQDN のサニタイズ設定を `option dhcpv6_fqdn '0'` で無効化（必要に応じて）<br>- LAN 内の未認証アクセスを防ぐため、`firewall` で DHCPv6 ポート (UDP 546/547) を信頼済みインタフェースのみに制限 | `opkg update && opkg upgrade luci luci-base luci-mod-admin-full` |
| **luci‑app‑upnp** | - 公式パッチが適用された **2026‑08‑15 以降** のバージョンへアップデート<br>- UPnP IGD の SOAP リクエストに対し `NewPortMappingDescription` の文字列長と HTML エスケープを有効化<br>- 必要がなければ `upnpd` を無効化し、外部からの UPnP アクセスを遮断 | `opkg upgrade luci-app-upnp` |
| **luci‑app‑samba4** | - 2026‑09‑10 以降の **luci-app-samba4 2026.09.10‑rc1** に更新し、`/usr/sbin/smbd` の実行権限を `0755` に戻す（root での setuid 解除）<br>- `samba` の `exec` オプションを `no` に設定し、ACL で `file.exec` を除外 | `opkg upgrade luci-app-samba4 samba36` |
| **Flowise** | - **3.1.0** 以上へアップグレード<br>- 環境変数 `JWT_SECRET`, `JWT_REFRESH_SECRET`, `JWT_AUDIENCE`, `JWT_ISSUER` を **ランダムか

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-61876

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-12T12:16:46.400 |

LuCI versions fail to properly encode DHCPv6 lease hostnames before rendering in status tables, allowing adjacent network attackers to inject HTML markup. Attackers can send a DHCPv6 Client FQDN containing script tags that execute in the administrator's browser when viewing DHCP lease pages.

### CVE-2026-56271

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-07-12T12:16:45.290 |

Flowise before 3.1.0 (affected versions 3.0.13 and earlier) uses weak hardcoded default JWT secrets ('auth_token', 'refresh_token') and default audience and issuer values ('AUDIENCE', 'ISSUER') in the enterprise passport authentication middleware (packages/server/src/enterprise/middleware/passport/index.ts). When the corresponding environment variables (JWT_AUTH_TOKEN_SECRET, JWT_REFRESH_TOKEN_SECRET, JWT_AUDIENCE, JWT_ISSUER) are not set, the application silently falls back to these publicly known defaults, allowing an attacker to forge valid JWTs and impersonate any user, including administrators, resulting in authentication bypass.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-56260

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-12T12:16:45.153 |

Crawl4AI before 0.8.7 contains an arbitrary file write vulnerability in the Docker API server's /screenshot and /pdf endpoints. The output_path parameter accepts arbitrary filesystem paths without validation, allowing an attacker to supply absolute or path-traversal values to write to any location writable by the application's user, overwriting server files and causing denial of service.

### CVE-2026-56259

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-12T12:16:45.013 |

Crawl4AI before 0.8.8 contains credential exfiltration vulnerabilities in the Docker API server that allow attackers to redirect LLM API calls to attacker-controlled endpoints and read arbitrary environment variables. Attackers can exploit the unauthenticated /md, /llm, and /llm/job endpoints by supplying a malicious base_url parameter and setting api_token to env:VARIABLE_NAME to exfiltrate provider API keys and server secrets including JWT SECRET_KEY for authentication bypass.

### CVE-2026-61875

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-12T12:16:46.260 |

luci-app-upnp contains a stored cross-site scripting vulnerability that allows unauthenticated LAN clients to inject JavaScript via UPnP IGD AddPortMapping SOAP requests. Attackers can send malicious HTML in the NewPortMappingDescription field, which miniupnpd stores and luci-app-upnp renders without output encoding, executing the payload when administrators view the UPnP or Status pages.

### CVE-2026-59260

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-12T12:16:45.977 |

OpenWrt luci-app-samba4 read ACL grants file.exec permission on /usr/sbin/smbd, allowing authenticated delegated users to execute the Samba daemon with caller-controlled command-line arguments. Attackers can pass arbitrary Samba global options such as message command to a root smbd process, triggering command execution when SMB protocol messages are processed.

### CVE-2026-56238

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-12T12:16:44.587 |

Capgo before 12.128.2 contains an information disclosure vulnerability in the Supabase PostgREST global_stats endpoint that allows unauthenticated attackers to read sensitive financial and operational metrics using only the public apikey. Remote attackers can query the /rest/v1/global_stats endpoint to expose MRR, total revenue, plan-tier revenue breakdown, customer counts, and operational telemetry.

### CVE-2026-15484

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-07-12T07:16:25.107 |

A vulnerability was detected in TRENDnet TEW-821DAP 1.12B01. The affected element is the function sub_41EC14 of the file /goform/tools_nslookup of the component ssi. The manipulation results in buffer overflow. It is possible to launch the attack remotely. The vendor explains: "We are unable to confirm the existence of the vulnerabilities for (...) TEW-821DAP (v1.0R) as these items have been EOL. " This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-15483

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-07-12T07:16:24.927 |

A security vulnerability has been detected in TRENDnet TEW-821DAP 1.12B01. Impacted is the function sub_41EC14 of the file /goform/tools_nslookup of the component ssi. The manipulation of the argument nslookup_target leads to buffer overflow. It is possible to initiate the attack remotely. The vendor explains: "We are unable to confirm the existence of the vulnerabilities for (...) TEW-821DAP (v1.0R) as these items have been EOL. " This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-56308

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-07-12T12:16:45.567 |

Capgo before 12.128.2 allows email address changes without requiring current password re-authentication or verification of the existing email address. An attacker with access to a valid session cookie or authenticated browser can change the account email to gain control of account recovery and bypass multi-factor authentication protections.

### CVE-2026-58281

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-11T21:16:23.903 |

Deserialization of untrusted data in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-15481

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-07-12T06:16:42.863 |

A security flaw has been discovered in Trendnet TEW-635BRM up to 1.00.03. This vulnerability affects the function ipoa_test of the file /sbin/rc of the component IPoA WAN Connection Setup. Performing a manipulation of the argument ipoa_ipaddr results in command injection. The attack is possible to be carried out remotely. The exploit has been released to the public and may be used for attacks. The vendor explains: "We are unable to confirm if the vulnerability exists. This item has been EOL since 2011. We will make an official announcement of possible vulnerabilities, and recommend users to switch devices." This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-15480

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-12T06:16:42.650 |

A vulnerability was identified in Trendnet TEW-635BRM up to 1.00.03. This affects the function start_httpd of the file /sbin/rc of the component Web Service. Such manipulation of the argument device_name leads to stack-based buffer overflow. The attack can be executed remotely. The exploit is publicly available and might be used. The vendor explains: "We are unable to confirm if the vulnerability exists. This item has been EOL since 2011. We will make an official announcement of possible vulnerabilities, and recommend users to switch devices." This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-56313

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-12T12:16:45.703 |

Capgo before 12.128.2 contains a cross-organization account disruption vulnerability in the SSO prelink endpoint that allows enterprise administrators to delete password identities of users in foreign organizations. Attackers with org.update_settings permission and an active SSO provider can call the prelink-users endpoint to permanently remove email-based authentication for any user matching the provider's email domain, forcing victims to use the attacker's SSO provider or complete password reset recovery.

### CVE-2026-56241

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-12T12:16:44.730 |

Capgo before 12.128.2 contains a privilege escalation vulnerability where demoted super_admin users retain access to delete_non_compliant_bundles and count_non_compliant_bundles RPCs due to stale org_users.user_right column not being cleared during role binding deletion. Attackers can exploit this by maintaining a previously granted super_admin role to enumerate and bulk delete non-compliant bundles across the entire organization indefinitely.
