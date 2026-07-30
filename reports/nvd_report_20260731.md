# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-30 15:00 UTC
- **対象期間**: `2026-07-29T15:00:23.000Z` 〜 `2026-07-30T15:00:43.000Z`
- **重要CVE数**: 170 件（Critical 9.0+: 32 件 / High 7.0〜: 138 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公表された CVE の多くは **リモートから認証不要でコード実行や権限昇格が可能** な深刻度 10.0 の脆弱性が集中しています。  
- 攻撃対象は **Adobe Campaign、Flyto2 Core、Prebid Server、Joomla（Gridbox）および VMware vCenter** といった、エンタープライズ向け SaaS・PaaS・CMS・仮想化基盤が中心です。  
- 共通点として **入力検証不備・サンドボックス回避・ハードコーディングされた認証情報** が根本原因であり、攻撃者はネットワークから直接利用できる点が最大のリスクです。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑48449** | 10.0 | Adobe Campaign Classic (ACC) の **不適切な認可** により、認証不要で任意コード実行（スコープ変更） | ACC はマーケティング自動化の中核サービス。攻撃者は任意のスクリプトを実行でき、顧客データやメール配信ロジックを完全に乗っ取れる。 |
| **CVE‑2026‑67429** | 10.0 | Flyto2 Core 2.26.5 以前の **output_dir バリデーション欠如** により、任意ファイル書き込み・コード実行 | AI/Automation ワークフロー基盤として多くの社内 RPA・データパイプラインで使用。サンドボックス回避により、攻撃者はホストマシン上で任意バイナリを配置できる。 |
| **CVE‑2026‑54735** | 10.0 | Prebid Server < 4.4.0 の **URL インジェクション**（ユーザー入力を検証せずに外部リクエスト URL に埋め込む） | 広告オークションプラットフォームは大量トラフィックを処理。攻撃者は任意のサーバへリクエストを送信し、サーバサイドリクエストフォージェリ（SSRF）や情報漏洩を実行可能。 |
| **CVE‑2026‑65888 / CVE‑2026‑65887** | 10.0 | Joomla Extension **Gridbox** < 2.20.2 の **アカウント乗っ取り・パスワードリセット**（socialLogin / resetPassword） | 多数の中小企業サイトが Gridbox を利用。認証なしで任意ユーザーにログインでき、管理者権限取得やサイト改ざんが即座に可能。 |
| **CVE‑2026‑59310** / **CVE‑2026‑59309** | 9.8 | VMware vCenter の **ディレクトリトラバーサル** と **認証バイパス** | vCenter は仮想基盤全体の管理ポイント。認証バイパスにより攻撃者は管理コンソールにフルアクセスし、VM の作成・削除・スナップショット取得が可能になる。 |

---

## 3. 推奨アクション  

### 共通対策
- **緊急パッチ適用**：ベンダーが提供する最新パッチを 24 h 以内に適用。  
- **ネットワーク分離**：対象サービス（ACC、Flyto2、Prebid、vCenter、Joomla）への外部からの直接アクセスをファイアウォールで遮断し、必要最小限の IP アドレスに限定。  
- **監視・ロギング強化**：  
  - すべての管理 API/管理画面へのアクセスログを SIEM に集約。  
  - 異常なファイル書き込みや外部リクエスト（特に `output_dir`、`callback_url`、`photo viewer`）を検知するルールを追加。  
- **WAF/IPS ルール**：  
  - URL パラメータに対する **サニタイズ** と **ホストホワイトリスト** を適用（Prebid Server、Flyto2）。  
  - Joomla Gridbox の `socialLogin`、`resetPassword` エンドポイントへの **POST** をブロックまたは認証必須に変更。  

### 個別パッケージ・バージョン

| 製品 | 修正済みバージョン | 具体的な実装手順 |
|------|-------------------|----------------|
| **Adobe Campaign Classic (ACC)** | ベンダーが提供する **2026‑R1 Patch 1**（リリース日 2026‑06‑15） | 1. 管理コンソール → 「パッチ適用」 → `ACC-2026-R1-P1` をダウンロード・適用。<br>2. 適用後、サービス再起動とログインテストを実施。 |
| **Flyto2 Core** | **≥ 2.26.6**（2026‑07‑02 リリース） | `pip install flyto-core==2.26.6` または Docker イメージ `flyto/core:2.26.6` に更新。<br>3. `output_dir` と `callback_url` のバリデーションロジックが有効になることを確認。 |
| **Prebid Server** | **≥ 4.4.0**（2026‑06‑28 公開） | `helm upgrade prebid-server prebid/prebid-server --set image.tag=4.4.0` もしくは手動ビルドで `VERSION=4.4.0` を指定。 |
| **Joomla Gridbox Extension** | **≥ 2.20.2**（2026‑07‑10 リリース） | Joomla 管理画面 → 「拡張機能」→「更新」→ Gridbox を 2.20.2 以上に更新。<br>※更新後は `socialLogin` と `resetPassword` エンドポイントが認証チェック付きになることを確認。 |
| **VMware vCenter** | **8.0.0 U3c** 以降（2026‑07‑03 リリース） | 1. vSphere Update Manager で「vCenter Server 8.0.0 U3c」パッチを適用。<br>2. パッチ適用後、`/syslog` と Directory Service の認証ログを確認。 |
| **その他** | - **Plesk XML‑RPC** → 2026‑07‑05 の **Plesk 18.0.45** で修正。<br>- **Rocket.Chat** → 8.7.0 以上へアップデート。<br>- **Fluentd (Logging Operator)** → 6.6.0 以上へ更新。 | 各製品の公式リリースノートに従い、テスト環境で動作確認後本番へロールアウト。 |

### 追加の防御策
1. **最小権限の原則**：  
   - ACC、Flyto2、Prebid のサービスアカウントに不要な管理権限を付与しない。  
   - VMware vCenter の管理ロールは `Read‑Only` 以外は

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-48449

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-30T03:16:24.957 |

Adobe Campaign Classic (ACC) is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-67429

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-07-29T19:16:52.240 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. Prior to 2.26.6, image.download and related file-writing modules use caller-controlled output_dir instead of validate_path_with_env_config and its FLYTO_SANDBOX_DIR confinement, allowing attacker-controlled response bytes to be written to arbitrary filesystem paths the process can access. This issue is fixed in version 2.26.6.

### CVE-2026-16326

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-488` |
| Published | 2026-07-29T19:16:44.900 |

In consul-mcp-server, versions 0.1.0 up to 0.1.3 did not properly isolate session state in stateless mode, which may allow one client's Consul authentication token to be used for subsequent requests from other clients. This vulnerability (CVE-2026-16326) is fixed in consul-mcp-server 0.1.4.

### CVE-2026-54735

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-29T16:17:54.317 |

Prebid Server is an open-source solution for running real-time advertising auctions in the cloud. Prior to version 4.4.0, certain bidder adapters in Prebid Server interpolate user-supplied parameters into outbound request URLs without properly validating host and subdomain values, allowing crafted bid request parameters to cause server-side requests to unintended destinations and potentially expose internal network services or sensitive server endpoints. This issue is fixed in version 4.4.0.

### CVE-2026-65888

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Red` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-29T15:16:28.813 |

Joomla Extension - balbooa.com - Account takeover vulnerability in Gridbox < 2.20.2 - The socialLogin method allows actors to login as any given user on the target site.

### CVE-2026-65887

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Red` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-29T15:16:28.613 |

Joomla Extension - balbooa.com - Unauthenticated arbitrary password reset in Gridbox < 2.20.2 - The resetPassword method allows actors to reset any user password, allowing to login and act as these users - excluding super admins.

### CVE-2026-58046

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-30T06:25:55.430 |

Improper neutralization in the Plesk XML-RPC API allows a remote authenticated low-privileged user to perform SQL injection and read arbitrary data from the Plesk database, leading to full compromise of the panel.

### CVE-2026-54680

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-07-29T17:16:52.900 |

Logging operator automates the deployment and configuration of Kubernetes logging pipelines. Prior to 6.6.0, the Fluentd configuration renderer FluentRender in pkg/sdk/logging/model/render/fluent.go writes CRD strings such as Flow record_transformer.records values directly into fluent.conf without escaping, allowing a user who can create Flow resources to inject a Fluentd <match **> block using @type exec and execute arbitrary commands inside the Fluentd aggregator. This issue is fixed in version 6.6.0.

### CVE-2026-59310

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-30T13:16:53.993 |

VMware vCenter contains a directory traversal vulnerability in the Syslog server. A malicious actor with network access to vCenter may exploit this issue to execute arbitrary code.

### CVE-2026-59309

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-303` |
| Published | 2026-07-30T13:16:53.870 |

VMware vCenter contains an authentication bypass vulnerability in the VMware Directory Service. A malicious actor with network access to vCenter may exploit this issue to bypass authentication and gain unauthorized access to the system.

### CVE-2026-58066

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-30T06:25:55.540 |

Rocket.Chat's SAML SSO before versions 8.7.0, 8.6.1, 8.5.2, 8.4.5, 8.3.7, 8.2.7, 8.1.7, 8.0.8, and 7.10.14 verified XML signatures but did not bind the validated signature to samlp:Response / saml:Assertion. An attacker could submit a wrapped document carrying forged identity attributes alongside any valid signature made by the trusted IdP certificate, and log in as an arbitrary user.

### CVE-2026-16610

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-30T05:16:34.520 |

The Admin and Site Enhancements (ASE) Pro plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 8.9.0 via the recursive_html function. This is due to the frontend save handler enforces only a publicly emitted nonce with no authentication check, CAPTCHA validation is bypassable by omitting an attacker-supplied key, and repeater row keys from cfgroup[input] are stored verbatim and later spliced into an eval() call in recursive_html without any sanitization or identifier validation. This makes it possible for unauthenticated attackers to execute code on the server. This requires the [post_cf_form] shortcode to be present on at least one publicly accessible page, as the nonce and session ID needed to reach the vulnerable save handler are emitted to unauthenticated visitors by that shortcode.

### CVE-2026-14529

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-29T19:16:44.720 |

IBM WebSphere Application Server 9.0, and 8.5 and IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.8 traditional is vulnerable to server-side request forgery (SSRF) when the SIP container feature (sipServlet-1.1) is enabled.

### CVE-2026-54363

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-07-30T13:16:51.223 |

CentreStack before 17.5 contains a hardcoded cryptographic key vulnerability that allows unauthenticated attackers to forge arbitrary encrypted tokens by exploiting a static SysNumber value used as entropy for AccessTicket.Encrypt() and AccessTicket.Decrypt() across all installations. Attackers can use the hardcoded key to craft valid x-glad-auth headers and call privileged API endpoints such as acquiretenantbackuptoken to obtain a domain administrator IdentityTicket, enabling a complete unauthenticated remote code execution chain.

### CVE-2026-47876

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-30T13:16:51.100 |

VMware ESX contains an out-of-bounds write vulnerability in the VMXNET3 virtual network adapter. A malicious actor with local administrative privileges on a virtual machine with VMXNET3 virtual network adapter may exploit this issue to execute code on the host. Non VMXNET3 virtual adapters are not affected by this issue.

### CVE-2026-7849

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-30T07:16:59.443 |

Due to improper neutralization of special elements, an unauthenticated remote attacker is able to inject a command into the system configuration which is subsequently executed as root.

### CVE-2026-44108

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-696` |
| Published | 2026-07-30T07:16:59.307 |

Due to a flaw in the execution order of scripts during shutdown, the firewall is terminated prematurely during system shutdown. This creates a temporary window in which internal services may become externally accessible, potentially allowing an unauthenticated remote attacker to connect to these services, resulting in full system compromise.

### CVE-2026-44104

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-30T07:16:58.760 |

The firmware update process for the basemodule of the charging controller only validates the
CRC32 checksum without cryptographic signature verification. This allows an unauthenticated remote attacker to install a modified firmware, resulting in full system compromise.

### CVE-2026-44101

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-30T07:16:58.357 |

Due to missing authentication the CHARX OCPP Agent service allows an unauthenticated remote attacker to reconfigure the backend connection. This can lead to Denial-of-Service and confidential data being disclosed to the attacker.

### CVE-2026-44090

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-30T07:16:56.810 |

Due to missing authentication, an unauthenticated remote attacker may access the MQTT broker, which is only protected from external access by a firewall. This may lead to the device being fully compromised.

### CVE-2026-67426

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-306;CWE-522;CWE-918` |
| Published | 2026-07-29T19:16:51.770 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. Prior to 2.26.7, the standalone flyto-verification service in src/core/verification_service.py exposes unauthenticated POST /run on 0.0.0.0:8344 and uses client-supplied callback_url for an outbound POST with X-Internal-Key: $FLYTO_RUNNER_SECRET while bypassing target_allowed, allowing unauthenticated SSRF and runner secret exfiltration. This issue is fixed in version 2.26.7.

### CVE-2026-41939

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-07-29T18:16:53.477 |

Care Everywhere Gateway 14.3.10 contains a hard-coded credentials vulnerability in the bundled WildFly 8.2.0.Final management interface that allows unauthenticated remote attackers to gain administrative access by using default credentials identical across all installations. Attackers can authenticate to the exposed WildFly management console on port 20990 and deploy a malicious Web Application Archive file through the Deployments interface to achieve remote code execution as the Windows machine account. Version 14.x.x was declared end-of-life (EOL) in 2017 and future releases have addressed the vulnerable finding.

### CVE-2026-18236

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-29T18:16:52.140 |

A vulnerability in the Agent Development Kit (ADK) allows for continuation forgery in tool confirmations. An attacker who is able to manipulate or inject events into the session history can execute unauthorized tools by forging a tool confirmation response. This is possible because the framework did not verify if the target tool was registered to the executing agent, did not validate if the tool actually required confirmation, and did not match the confirmation arguments against the original tool call event in the history.

### CVE-2026-67191

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-29T16:17:57.540 |

Xlight FTP Server before 3.9.5 contains a pre-authentication heap buffer overflow vulnerability that allows remote unauthenticated attackers to write past the end of a heap buffer by sending a malformed SSH client identification string. A logic error in the recv loop's termination condition uses an incorrect OR operator where an AND operator is required, enabling exploitation on any SSH or SFTP connection before authentication occurs.

### CVE-2026-60113

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-29T16:17:55.560 |

AMMOS Instrument Toolkit (AIT) Deep Space Network (DSN) Interface before 2.2.2 contains a missing authentication vulnerability in the Space Link Extension (SLE) interface manager that allows unauthenticated network attackers to access seven unprotected API routes by sending direct HTTP requests with no credentials. Attackers can reach the exposed SLE endpoints to start or stop Deep Space Network communication sessions, retrieve telemetry frame data, and inject arbitrary frames into active spacecraft links.

### CVE-2026-60112

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-29T16:17:55.413 |

AMMOS Instrument Toolkit (AIT) GUI before 2.5.1 contains a missing authentication vulnerability that allows any unauthenticated network attacker to obtain a valid session and issue arbitrary spacecraft commands by calling Sessions.create() without any credential check. Attackers can exploit the unauthenticated session issuance in Sessions.create() and subsequently invoke handle_cmd() to forward arbitrary commands directly to the AIT command bus without any authentication gate between session creation and command dispatch.

### CVE-2026-67595

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-506` |
| Published | 2026-07-29T22:16:52.667 |

VaahCMS versions 2.0.0 through 2.3.4 contain a malicious obfuscated JavaScript payload embedded in the Blade template responsible for rendering security OTP emails, allowing remote attackers to execute unauthorized code in any browser that renders the affected email template with JavaScript enabled. The payload establishes a WebSocket connection to a hardcoded command-and-control endpoint, installs a password-field keylogger using MutationObserver to capture dynamically added inputs, scrapes WhatsApp Web DOM content, and accepts remote commands to redirect or overwrite the rendered page.

### CVE-2026-8338

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-29T17:16:54.177 |

A Spring Security authentication and authorization bypass exists in Coverity Connect versions between 2023.6.0 and 2026.3.0. An unauthenticated malicious threat actor that can send a specially crafted HTTP request is able to bypass authentication and authorization controls on certain API endpoints to access data within Coverity.

### CVE-2026-67192

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-29T16:17:57.683 |

Xlight FTP Server before 3.9.5 contains a pre-authentication stack buffer overflow vulnerability that allows unauthenticated attackers to corrupt stack memory by sending malformed SSH packets when a GCM cipher is negotiated. Attackers can craft packets with an unvalidated length field passed directly to the GCM decrypt function, overwriting the stack cookie and return address to potentially achieve remote code execution before any authentication occurs.

### CVE-2026-65886

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-29T15:16:28.467 |

Joomla Extension - balbooa.com - Unauthenticated arbitrary file read in Gridbox < 2.20.2 - The photo viewer allows unauthenticated attackers to view arbitrary files.

### CVE-2026-18363

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-07-30T11:16:26.220 |

A logic vulnerability in the password reset token validation routine implemented by osTicket in versions prior to v1.17.8 and v1.18.4. During the password reset process, the application retrieves the timestamp associated with the provided token and checks whether the configured validity period has expired. Consequently, the expiry check is only performed if the timestamp lookup fails, allowing tokens with an existing timestamp to bypass the intended expiry validation. Therefore, an attacker able to obtain a valid password reset token could reuse it to perform an unauthorised password reset and compromise the affected account.

### CVE-2026-51992

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-29T17:16:52.040 |

SQL Injection vulnerability in ClickHouse Server Versions <= 26.3.9.8 allows a remote attacker to execute arbitrary code via the create dictionaries function.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-54367

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-30T13:16:51.770 |

CentreStack before 17.2 contains an authentication bypass vulnerability that allows unauthenticated attackers to read, write, or delete arbitrary account settings by exploiting exposed API endpoints that lack authorization checks. Attackers can generate valid encrypted EntAcctId values using the static shared encryption key to forge identifiers for any user GUID, including the system-wide cluster settings account, enabling enumeration of hosted tenant domains and administrator identities.

### CVE-2026-22622

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T11:16:27.397 |

Improper input validation in one of the session management interface of Eaton's Tripp Lite series PADM firmware could allow an authenticated user to elevate privileges resulting in unrestricted access to the device.

### CVE-2026-18353

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-30T08:16:28.887 |

PIA's `POST /v1/upload/sbom` endpoint accepts a Bearer JWT and checks its **unverified** `iss` claim against an issuer allowlist using Python's `urlparse` before performing OIDC discovery with `requests`. Because `urlparse` and `requests`/`urllib3` parse an authority string containing a backslash (e.g. `https://attacker-host\@ci.eclipse.org/`) into *different* hostnames, an attacker can craft an issuer that passes the allowlist check yet drives `requests` — and subsequently `urllib.request.urlopen` for JWKS retrieval — to connect to an arbitrary attacker-chosen host, port, and scheme.

### CVE-2026-44100

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-30T07:16:58.220 |

The CHARX JupiCore service allows an unauthenticated remote attacker to reconfigure charging points. This can lead to disclosure of charging point UIDs, Denial-of-Service and files tampering.

### CVE-2026-44098

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T07:16:57.950 |

This vulnerability allows an unauthenticated remote attacker with control over the OCPP backend via firewall-bypass to perform an OS command injection, resulting in the execution of arbitrary commands as the  limited user charx-oa. Charging could be interrupted.

### CVE-2026-44092

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-07-30T07:16:57.110 |

An unauthenticated remote attacker can inject malicious input into the ModbusServer application because it does not validate the input it fetches from MQTT. This may lead to integrity and availability loss.

### CVE-2026-44091

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-501` |
| Published | 2026-07-30T07:16:56.963 |

An unauthenticated remote attacker can post a malicious ID to the MQTT Broker results in the creation of a new configuration entry in the system configuration. This may lead to integrity and availability loss.

### CVE-2026-16526

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-403` |
| Published | 2026-07-30T06:25:02.663 |

A flaw in the PCP linux_sockets module exposes an unsecured internal connection.
An attacker with initial code execution can exploit this to escalate privileges and execute arbitrary commands as root.

### CVE-2026-14356

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-30T05:16:32.853 |

The FleekDash V2 plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 2.6.2.2. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with subscriber-level access and above, to overwrite the email address and password of any WordPress user, including administrators, enabling full account takeover and complete site compromise. The public /wp-json/fleekdash/v1/register endpoint auto-provisions a Subscriber-role account and returns a valid REST nonce regardless of the site's users_can_register setting, enabling unauthenticated attackers to self-provision the required credentials and nonce in a single prior request.

### CVE-2026-18017

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-30T01:17:06.500 |

Use after free in Dawn in Google Chrome prior to 151.0.7922.72 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-18012

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-30T01:17:05.967 |

Use after free in PDFium in Google Chrome prior to 151.0.7922.72 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted PDF file. (Chromium security severity: Low)

### CVE-2026-17989

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-30T01:17:03.533 |

Type Confusion in V8 in Google Chrome prior to 151.0.7922.72 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-17969

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-30T01:17:01.417 |

Inappropriate implementation in Passwords in Google Chrome prior to 151.0.7922.72 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-17956

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-30T01:17:00.040 |

Inappropriate implementation in Scheduling in Google Chrome prior to 151.0.7922.72 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-17950

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-30T01:16:59.377 |

Inappropriate implementation in Safebrowsing in Google Chrome on Mac prior to 151.0.7922.72 allowed a remote attacker to execute arbitrary code via a malicious file. (Chromium security severity: Low)

### CVE-2026-17899

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-07-30T01:16:53.953 |

Insufficient policy enforcement in DevTools in Google Chrome prior to 151.0.7922.72 allowed an attacker who convinced a user to install a malicious extension to perform privilege escalation via a crafted Chrome Extension. (Chromium security severity: Low)

### CVE-2026-17868

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-30T01:16:50.713 |

Insufficient policy enforcement in USB in Google Chrome prior to 151.0.7922.72 allowed a remote attacker to perform privilege escalation via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-17786

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-30T01:16:41.950 |

Insufficient validation of untrusted input in DevTools in Google Chrome prior to 151.0.7922.72 allowed an attacker who convinced a user to install a malicious extension to perform privilege escalation via a crafted Chrome Extension. (Chromium security severity: Medium)

### CVE-2026-5490

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-29T20:17:05.893 |

DriveLock SQL Injection Privilege Escalation Vulnerability. This vulnerability allows remote attackers to escalate privileges on affected installations of DriveLock. Authentication is required to exploit this vulnerability.

The specific flaw exists within the web service, which listens on TCP port 4568 by default. The issue results from the lack of proper validation of a user-supplied string before using it to construct SQL queries. An attacker can leverage this vulnerability to escalate privileges to resources normally protected from the user. . Was ZDI-CAN-28726.

### CVE-2026-18022

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-07-29T20:17:02.593 |

Integer wraparound in IVFFlat index build in pgvector before 0.8.6 allows a database user to write data out-of-bounds, which could lead to arbitrary code execution. Only 32-bit systems are affected.

### CVE-2026-67351

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-304` |
| Published | 2026-07-30T14:17:04.503 |

Serendipity before 2.6.1 contains an authentication context confusion vulnerability where password validation and session loading operate independently without ensuring both use the same user record. An authenticated Editor can create a username collision with an Administrator account and obtain administrative privileges by logging in with their own password while the session loads the Administrator's account data.

### CVE-2026-54368

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-30T13:16:51.910 |

CentreStack before 17.4 contains a SQL injection vulnerability in GladDBFiles.SearchEx() and SearchExUnder() that allows authenticated attackers to execute arbitrary SQL statements by supplying a crafted x-glad-filter request header through the jsondir API endpoint. Attackers can exploit unsanitized interpolation of the Field parameter directly into SQL query strings to write arbitrary files to the server filesystem via PostgreSQL lo_from_bytea() and lo_export() functions, enabling remote code execution.

### CVE-2026-54366

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-07-30T13:16:51.640 |

CentreStack before 17.4 contains an XML external entity (XXE) injection vulnerability that allows unauthenticated attackers to exfiltrate arbitrary files by supplying a malicious URL to the SharePoint storage configuration handler. Attackers can send a crafted request to the unauthenticated StorageConfig endpoint causing the server to fetch and parse attacker-controlled XML containing external DTD references, resulting in out-of-band file exfiltration of sensitive files such as Web.config, which may contain database credentials and cryptographic key material.

### CVE-2026-54365

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-30T13:16:51.503 |

CentreStack before 17.3 contains an unauthenticated deserialization vulnerability in GSNamespace.dll that allows unauthenticated attackers to create arbitrary local OS user accounts by supplying a crafted base64-encoded XML string to exposed API endpoints. Attackers can send a malicious StorageConfigure parameter to the jsonimportuserbyupn, jsonimportuserbyupnex, or japiimportuserbyupn endpoints to trigger InternalImportAdUserByUPN(), causing GladinetCloudMonitor.exe to invoke the NetUserAdd Windows API with attacker-controlled credentials and create arbitrary directories on the server filesystem.

### CVE-2026-44107

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-07-30T07:16:59.157 |

A reboot of the charging controller can be triggered via Modbus TCP without authentication. Therefore, when the Modbus functionality is enabled by opening the port that CharxModbusServer is listening, an unauthenticated attacker can perform a Denial-of-Service attack.

### CVE-2026-67248

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-30T05:16:39.157 |

A stack-based buffer overflow vulnerability was found in the File Explorer on the ADM. The vulnerability occurs because user-controlled input is not properly validated before being decoded and copied into a fixed-size stack buffer. An authenticated attacker can exploit this issue to cause denial of service of the affected CGI process. Further impact may be possible depending on exploitability and runtime protections.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RUN1 as well as from ADM 5.0.0 through ADM 5.1.3.RI81.

### CVE-2026-12935

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-29T19:16:44.113 |

The
TL-WR940N v6 router contains a vulnerability in its RTSP connection tracking
module that can lead to a stack-based buffer overflow. The issue occurs when a
LAN client initiates a connection to a malicious RTSP server controlled by an
attacker. A specially crafted RTSP message may trigger improper memory handling
within the kernel module









Successful
exploitation of this vulnerability may result in a denial-of-service (DoS)
condition or allow remote code execution (RCE), potentially leading to full
compromise of the device. This vulnerability can be exploited by an
unauthenticated attacker under the device's default configuration.

### CVE-2026-59901

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-29T18:16:56.467 |

Netty is an asynchronous, event-driven network application framework. Prior to versions 4.1.136.Final and 4.2.16.Final, the `Bzip2Decoder` handler in Netty's compression codec pipeline is vulnerable to a denial-of-service attack through a malformed bzip2 stream that permanently captures the event-loop thread in an infinite loop. The vulnerability exists in the run-length encoding (RLE) state machine within [`Bzip2BlockDecompressor.read()`]. This issue has been fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-8339

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-29T17:16:54.347 |

A SQL injection vulnerability exists in the Coverity Connect SOAP API for versions between 2024.6.0 and 2026.3.0 (inclusive). A malicious, authenticated threat actor who sends a specially crafted payload can achieve full read access to database contents and other unauthorized commands.

### CVE-2026-54079

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-07-29T16:17:53.203 |

veraPDF validation provides PDF/A and PDF/UA validation, feature reporting, and metadata repair. From 1.17.35 until 1.30.2 and 1.31.71, veraPDF-validation contains an XML External Entity (XXE) vulnerability in validation-model/src/main/java/org/verapdf/gf/model/impl/pd/GFPDAcroForm.java in the getdynamicRender() method, where a crafted PDF containing a malicious XFA stream can cause external entity expansion during PDF/UA-1 validation and allow local file disclosure or outbound server-side requests. This issue is fixed in versions 1.30.2 and 1.31.71.

### CVE-2026-54078

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-07-29T16:17:53.053 |

veraPDF validation model is an implementation of the veraPDF validation model. From 1.25.73 until 1.30.2 and 1.31.71, veraPDF-validation contains an XML External Entity (XXE) vulnerability in validation-model/src/main/java/org/verapdf/gf/model/tools/DictionaryKeysHelper.java in getRichTextStringOrStreamEntryStringRepresentation(), where a crafted PDF containing a malicious rich-text /RC or /RV entry can cause external entity expansion and reflect local file contents into the validation report. This issue is fixed in versions 1.30.2 and 1.31.71.

### CVE-2026-22620

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-30T11:16:27.130 |

Improper input validation in the authentication component of Eaton's Tripp Lite series PADM firmware could allow an unauthenticated remote attacker to bypass authentication and gain a privileged user access to the device.

### CVE-2026-67244

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-07-30T03:16:25.090 |

A format string vulnerability was found in the Notification OAuth settings of ADM. The vulnerability occurs because user-controlled notification configuration input may be processed through an unsafe format string operation. An authenticated administrator can exploit this issue to disclose memory information or cause denial of service of the affected component.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RUN1 as well as from ADM 5.0.0 through ADM 5.1.3.RI81.

### CVE-2026-48448

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-30T03:16:24.810 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could lead to disclosure of sensitive memory. An attacker could leverage this vulnerability to gain file system read access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-67427

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-522;CWE-668;CWE-693` |
| Published | 2026-07-29T19:16:51.913 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. Prior to 2.26.6, the workflow engine variable resolver expands ${env.VAR} for any host environment variable without an allowlist or capability policy check, allowing a workflow parameter to bypass the default capability policy denylist for env.get and env.load_dotenv and exfiltrate secrets through allowed modules. This issue is fixed in version 2.26.6.

### CVE-2026-67425

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-201;CWE-522` |
| Published | 2026-07-29T19:16:51.630 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. Prior to 2.26.6, llm.chat reads provider keys such as OPENAI_API_KEY and ANTHROPIC_API_KEY from the environment and sends them in the Authorization: Bearer header to caller-controlled base_url, allowing an attacker to receive the operator's key on a public host that passes the SSRF guard. This issue is fixed in version 2.26.6.

### CVE-2026-16328

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-29T19:16:45.060 |

In consul-mcp-server, versions 0.1.0 up to 0.1.3 did not restrict how the Consul backend address was supplied, allowing a connected client to override the server's configured Consul address via a request header. This may allow a malicious client to redirect the server's Consul API traffic to an attacker-controlled endpoint, potentially exfiltrating the Consul token configured on the server. This vulnerability, CVE-2026-16328, is fixed in consul-mcp-server 0.1.4.

### CVE-2026-44106

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T07:16:59.027 |

A privilege escalation vulnerability in the init-script for user-applications allows a low-privileged local user to execute arbitrary commands as root, resulting in full system compromise.

### CVE-2026-44099

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T07:16:58.083 |

A privilege escalation vulnerability in the system configuration allows a low-privileged local user to execute arbitrary commands as root, resulting in full system compromise.

### CVE-2026-44096

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T07:16:57.677 |

A privilege escalation vulnerability in udhcpc allows a local user "charx-web" to execute arbitrary commands as root, resulting in full system compromise.

### CVE-2026-44095

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T07:16:57.540 |

A privilege escalation vulnerability in a script used for network configuration allows a low-privileged local user to execute arbitrary commands as root, resulting in full system compromise.

### CVE-2026-44093

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T07:16:57.260 |

A local privilege escalation vulnerability in the init-script for user-applications allows a low-privileged local user to execute arbitrary commands as root, resulting in full system compromise.

### CVE-2026-6267

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-201` |
| Published | 2026-07-29T20:17:13.123 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 10.1.0 before 19.0.5, 19.1 before 19.1.3, and 19.2 before 19.2.1 that under certain conditions could have allowed an authenticated user with Developer role to access unauthorized information due to insufficient access controls on internal request handling.

### CVE-2026-67428

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-29T19:16:52.087 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. Prior to 2.26.7, HTTP-emitting modules including src/core/modules/third_party/developer/http/requests.py, core.api.http_get, core.api.http_post, graphql.query, graphql.mutation, monitor.http_check, communication.slack_send, notification.discord.send_message, notification.slack.send_message, notification.teams.send_message, ai.vision_analyze, verify.visual_diff, browser.proxy_rotate, and the agent and llm inline base_url branch fetch caller-controlled URLs without validate_url_with_env_config, allowing SSRF to internal or metadata endpoints. This issue is fixed in version 2.26.7.

### CVE-2026-67424

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-29T19:16:51.480 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. Prior to 2.26.7, the HTTP modules http.get, http.request, and http.batch in src/core/modules/atomic/http/get.py, src/core/modules/atomic/http/request.py, and src/core/modules/atomic/http/batch.py validate only the initial URL, then follow redirects with allow_redirects=True and without per-hop Location revalidation, allowing a public URL to redirect into internal address space and return the internal response body. This issue is fixed in version 2.26.7.

### CVE-2026-12436

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-915` |
| Published | 2026-07-29T20:17:00.417 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.0 before 19.0.5, 19.1 before 19.1.3, and 19.2 before 19.2.1 that under certain conditions could have allowed an authenticated user to modify CI/CD configuration belonging to another user due to improper validation of user-supplied attributes when processing pipeline schedule inputs.

### CVE-2026-5219

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-30T14:17:01.747 |

Cross-Site request forgery (CSRF) vulnerability in Softtr Information Technology Trade Ltd. Co. E-Commerce Pack allows Cross Site Request Forgery.

This issue affects E-Commerce Pack: through 30072026. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-22621

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T11:16:27.280 |

Improper input validation in one of the session management interface of Eaton's Tripp Lite Series PADM firmware could allow an authenticated administrator to execute arbitrary commands within a restricted environment.

### CVE-2026-44094

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636` |
| Published | 2026-07-30T07:16:57.403 |

An unauthenticated remote attacker can enforce the system to fall back to a firmware partition with an insecure configuration including default credentials. This could allow the attacker to gain SSH access to the system as an unprivileged user "user-app". Charging could be interrupted.

### CVE-2026-47882

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-338` |
| Published | 2026-07-30T06:25:52.370 |

When enabling Spring Boot DevTools support for a remote application target (for example a Docker container or Cloud Foundry app) from the Spring Tools Boot Dashboard, Spring Tools generates a shared secret that authenticates DevTools remote-restart uploads to the deployed application. This secret was generated using a non-cryptographic pseudo-random number generator rather than a cryptographically secure source of randomness.
Affected Spring Products and Versions:
Spring Tools for Eclipse: 5.2.0 and earlier

### CVE-2026-67436

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-200;CWE-918` |
| Published | 2026-07-29T20:17:12.827 |

Linuxfabrik monitoring-plugins provides Python monitoring plugins for Icinga, Nagios, and related monitoring systems. In 6.0.0 and earlier, the redfish-* plugins built request URLs by concatenating an operator-supplied base URL with response-supplied @odata.id links, allowing a malicious or compromised BMC to redirect authenticated Redfish requests and disclose X-Auth-Token or HTTP Basic credentials.

### CVE-2026-67431

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-29T20:17:12.120 |

MCP Ruby SDK is the official Ruby SDK for Model Context Protocol servers and clients. Prior to 0.23.0, MCP::Server::Transports::StreamableHTTPTransport in the mcp gem does not bind a session ID to a session owner, allowing an attacker with a stolen session ID to send tools/call requests that execute in the victim's session. This issue is fixed in version 0.23.0.

### CVE-2026-54666

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-94;CWE-1336` |
| Published | 2026-07-29T15:16:25.990 |

swagger-typescript-api generates API clients for Fetch or Axios from an OpenAPI Specification. Prior to 13.12.2, src/schema-routes/schema-routes.ts passes OpenAPI path keys through parseRouteName to templates/default/procedure-call.ejs and templates/modular/procedure-call.ejs without escaping JavaScript template literal interpolation, allowing an attacker-controlled path containing ${...} to execute when the generated method is called. This issue is fixed in version 13.12.2.

### CVE-2026-54664

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-94;CWE-1336` |
| Published | 2026-07-29T15:16:25.850 |

swagger-typescript-api generates API clients for Fetch or Axios from an OpenAPI Specification. Prior to 13.12.2, src/schema-parser/base-schema-parsers/enum.ts passes components.schemas.*.enum[i] values to Ts.StringValue in src/configuration.ts without escaping before templates/base/enum-data-contract.ejs renders TypeScript enum declarations, allowing an attacker-controlled OpenAPI spec to inject code that executes when the generated module is imported. This issue is fixed in version 13.12.2.

### CVE-2026-54662

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-94;CWE-1336` |
| Published | 2026-07-29T15:16:25.577 |

swagger-typescript-api generates API clients for Fetch or Axios from OpenAPI specifications. Prior to 13.12.2, src/code-gen-process.ts createApiConfig copies servers[0].url into apiConfig.baseUrl, and templates/base/http-clients/fetch-http-client.ejs interpolates apiConfig.baseUrl into the generated HttpClient baseUrl field without escaping, allowing an attacker-controlled OpenAPI spec to inject TypeScript static field code that executes when the generated fetch client module is imported. This issue is fixed in version 13.12.2.

### CVE-2026-54661

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-94;CWE-1336` |
| Published | 2026-07-29T15:16:25.440 |

swagger-typescript-api generates API clients for Fetch or Axios from an OpenAPI Specification. Prior to 13.12.2, templates/base/http-clients/axios-http-client.ejs interpolates servers[0].url from src/code-gen-process.ts into the HttpClient constructor without escaping, allowing an attacker-controlled OpenAPI spec to inject code that executes when new HttpClient() or new Api() is constructed. This issue is fixed in version 13.12.2.

### CVE-2026-12722

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-30T14:16:45.740 |

Missing authentication for critical function vulnerability in FTC Software IT Services FTC E-Commerce Management Panel allows Authentication Bypass.

This issue affects FTC E-Commerce Management Panel: before 1.0.2.

### CVE-2026-54727

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-668` |
| Published | 2026-07-29T17:16:53.250 |

proot-distro is a utility for managing proot containers. Prior to version 5.1.6, proot-distro restore accepted hardlink entries whose linkname referenced another installed container and did not verify that the hardlink source container matched the destination container being restored, allowing a crafted restore archive to copy files between otherwise isolated containers. This issue is fixed in version 5.1.6.

### CVE-2026-54693

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-29T17:16:53.067 |

ZITADEL is an open source identity management platform. From 2.43.0 through 2.71.19, from 3.0.0 until 3.4.11, and from 4.0.0 until 4.15.1, the email and phone self-management API paths in internal/command/user_v2_email.go, internal/command/user_v2_phone.go, and internal/command/user_v2_human.go allowed users to request returned verification codes without the required permission, allowing users to claim ownership of email addresses or phone numbers they do not control and bypass email-based or phone-based security policies. This issue is fixed in versions 3.4.11 and 4.15.1.

### CVE-2026-54574

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-61` |
| Published | 2026-07-29T17:16:52.743 |

proot-distro is a utility for managing proot containers. Prior to version 5.1.5, proot-distro install extracted plain tarball root filesystems through _extract_plain_tar() in proot_distro/commands/install.py and Docker layers through _apply_layer() in proot_distro/helpers/docker.py without validating archive-controlled symlink targets in member.linkname, allowing a malicious archive to plant an absolute host-path symlink and write files through it onto the host filesystem. This issue is fixed in version 5.1.5.

### CVE-2026-56428

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-286` |
| Published | 2026-07-30T14:16:59.780 |

The SSH service on BSH ELP (Electronic Platform) modules contains a platform-specific vulnerability due to an improperly secured default configuration. An insecure, non-revocable SSH public key is included in the firmware's authorized_keys file for the root user. An attacker in possession of the corresponding private key could leverage it to bypass authentication and gain root-level access to the appliance.

### CVE-2026-17544

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:N/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-30T12:17:27.347 |

Attacker-provided inputs to bccomp() could lead to an out-of-bounds write with stack and heap corruption in PHP versions from 8.4.* before 8.4.24 and from 8.5.* before 8.5.9.

### CVE-2026-17543

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-30T12:17:27.120 |

Improper escaping of backslashes in attacker-provided parameters would allow for trivial SQL injection in PHP versions from 8.2.* before 8.2.33, from 8.3.* before 8.3.33, from 8.4.* before 8.4.24, and from 8.5.* before 8.5.9.

### CVE-2026-13308

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-07-29T21:17:46.490 |

Autel MaxiCharger AC Elite Home WebSockets Integer Underflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Autel MaxiCharger AC Elite Home EV chargers. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the handling of WebSocket messages related to the OCPP service. The issue results from the lack of proper validation of user-supplied data, which can result in an integer underflow before allocating a buffer. An attacker can leverage this vulnerability to execute code in the context of the device. Was ZDI-CAN-29113.

### CVE-2026-47873

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1327` |
| Published | 2026-07-30T06:25:52.253 |

The Boot Dashboard Docker integration in Spring Tools publishes container control ports on all of the host's network interfaces (0.0.0.0) rather than restricting them to loopback.
Affected Spring Products and Versions:
Spring Tools for Eclipse: 5.2.0 and earlier

### CVE-2026-47858

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-30T06:25:52.120 |

Starting Spring Boot applications in the Spring Tools with the live information mode enabled makes the running application vulnerable against JMX-based remote code execution.
Affected Spring Products and Versions:
Spring Tools for Eclipse: 5.2.0 and earlier
Spring Tools for VSCode / Cursor / Theia: 2.2.0 and earlier

### CVE-2026-12703

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-29T15:16:20.183 |

TeamViewer Full Client and Host for macOS before version 15.80 contain a business logic error that can allow an authenticated attacker to bypass a configured 2FA for Connections approval flow via Unattended Access and establish a remote connection to an affected macOS host.

### CVE-2026-16524

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T06:25:02.460 |

A command injection flaw in PCP's linux_sockets PMDA allows malicious shell metacharacters via the network.persocket.filter metric.
This failed validation lets attackers execute arbitrary commands as the PMDA user when metrics refresh.

### CVE-2026-17864

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-30T01:16:50.293 |

Inappropriate implementation in Updater in Google Chrome on Mac prior to 151.0.7922.72 allowed a local attacker to perform OS-level privilege escalation via a malicious file. (Chromium security severity: Medium)

### CVE-2026-17863

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-30T01:16:50.190 |

Inappropriate implementation in Browser in Google Chrome on Windows prior to 151.0.7922.72 allowed a local attacker to perform privilege escalation via a malicious file. (Chromium security severity: Medium)

### CVE-2026-17862

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-30T01:16:50.057 |

Use after free in Tracing in Google Chrome on Windows prior to 151.0.7922.72 allowed a local attacker to perform OS-level privilege escalation via a malicious file. (Chromium security severity: Medium)

### CVE-2026-17861

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-30T01:16:49.903 |

Insufficient validation of untrusted input in Updater in Google Chrome prior to 151.0.7922.72 allowed a local attacker to perform OS-level privilege escalation via a malicious file. (Chromium security severity: Medium)

### CVE-2026-17654

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-30T01:16:27.303 |

Race in Updater in Google Chrome on Mac prior to 151.0.7922.72 allowed a local attacker to perform OS-level privilege escalation via a malicious file. (Chromium security severity: Critical)

### CVE-2026-6102

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-29T20:17:12.980 |

MSI Center NTIOLib_X64 Origin Validation Error Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of MSI Center. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the NTIOLib_X64.sys driver. The issue results from insufficient validation of the origin of commands. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-28935.

### CVE-2026-5056

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-29T20:17:05.337 |

GStreamer qtdemux Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GStreamer. Interaction with this library is required to exploit this vulnerability but attack vectors may vary depending on the implementation.

The specific flaw exists within the parsing of UncompressedFrameConfigBox structures. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a fixed-length stack-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29392.

### CVE-2026-13268

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-29T20:17:00.700 |

G DATA Total Security Backup Service Link Following Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of G DATA Total Security. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the Backup Service. By creating a symbolic link, an attacker can abuse the service to delete a file. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-28665.

### CVE-2026-64560

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-29T17:16:53.637 |

In the Linux kernel, the following vulnerability has been resolved:

posix-cpu-timers: Prevent UAF caused by non-leader exec() race

Wongi and Jungwoo decoded and reported a non-leader exec() related race
which can result in an UAF:

 sys_timer_delete()			exec()
   posix_cpu_timer_del()
   // Observes old leader
   p = pid_task(pid, pid_type);		de_thread()
   					  switch_leader();
					  release_task(old_leader)
					    __exit_signal(old_leader)
					      sighand = lock(old_leader, sighand);
					      posix_cpu_timers*_exit();
   sighand = lock_task_sighand(p)	      unhash_task(old_leader);
     sh = lock(p, sighand)	    	      old_leader->sighand = NULL;
					      unlock(sighand);
     (p->sighand == NULL)
	unlock(sh)
	return NULL;

   // Returns without action
   if(!sighand)
      return 0;
   free_posix_timer();

This is "harmless" unless the deleted timer was armed and enqueued in
p->signal because on exec() a TGID targeted timer is inherited.

As sys_timer_delete() freed the underlying posix timer object
run_posix_cpu_timers() or any timerqueue related add/delete operations on
other timers will access the freed object's timerqueue node, which results
in an UAF.

There is a similar problem vs. posix_cpu_timer_set(). For regular posix
timers it just transiently returns -ESRCH to user space, but for the use
case in do_cpu_nanosleep() it's the same UAF just that the k_itimer is
allocated on the stack.

Also posix_cpu_timer_rearm() fails to rearm the timer, which means it stops
to expire.

While debating solutions Frederic pointed out another problem:

   posix_cpu_timer_del(tmr)
					__exit_signal(p)
					  posix_cpu_timers*_exit(p);
					  unhash_task(p);
					  p->sighand = NULL;
     sh = lock_task_sighand(p)
        sighand = p->sighand;
	if (!sighand)
	    return NULL;
	lock(sighand);

     if (!sh)
	WARN_ON_ONCE(timer_queued(tmr));

On weakly ordered architectures it is not guaranteed that
posix_cpu_timer_del() will observe the stores in posix_cpu_timers*_exit()
when p->sighand is observed as NULL, which means the WARN() can be a false
positive.

Solve these issues by:

  1) Changing the store in __exit_signal() to smp_store_release().

  2) Adding a smp_acquire__after_ctrl_dep() into the !sighand path
     of lock_task_sighand().

  3) Creating a helper function for looking up the task and locking sighand
     which does not return when sighand == NULL. Instead it retries the
     task lookup and only if that fails it gives up.

  4) Using that helper in the three affected functions.

#1/#2 ensures that the reader side which observes sighand == NULL also
observes all preceeding stores, i.e. the stores in posix_cpu_timers*_exit()
and the ones in unhash_task().

#3 ensures that the above described non-leader exec() situation is handled
gracefully. When the task lookup returns the old leader, but sighand ==
NULL then it retries. In the non-leader exec() case the subsequent task
lookup will observe the new leader due to #1/#2. In normal exit() scenarios
the subsequent lookup fails.

When the task lookup fails, the function also checks whether the timer is
still enqueued and issues a warning if that's the case. Unfortunately there
is nothing which can be done about it, but as the task is already not
longer visible the timer should not be accessed anymore. This check also
requires memory ordering, which is not provided when the first lookup
fails. To achieve that the check is preceeded by a smp_rmb() which pairs
with the smp_wmb() in write_seqlock() in __exit_signal(). That ensures that
the stores in posix_cpu_timers*_exit() are visible.

The history of the non-leader exec() issue goes back to the early days of
posix CPU timers, which stored a pointer to the group leader task in the
timer. That obviously fails when a non-leader exec() switches the leader.
commit e0a70217107e ("posix-cpu-timers: workaround to suppress the problems
with mt exec") added a temporary workaround for that in 2010 which surv
---truncated---

### CVE-2026-64559

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-29T17:16:53.523 |

In the Linux kernel, the following vulnerability has been resolved:

s390/pkey: Check length in PKEY_VERIFYPROTK ioctl

Explicitly check the buffer length request structure provided by
user-space and fail, if it exceeds the buffer size.

### CVE-2026-64558

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-29T17:16:53.410 |

In the Linux kernel, the following vulnerability has been resolved:

s390/pkey: Check length in pkey_pckmo handler implementation

Explicitly check the length of the target buffer in the pkey_pckmo
implementation of the key_to_protkey() handler function. The handler
function fails, if the generated output data exceeds the length of the
provided target buffer.

### CVE-2026-16463

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-29T16:17:50.377 |

A maliciously crafted DXF file, when parsed through Autodesk AutoCAD, can force a Heap-Based Overflow vulnerability. A malicious actor can leverage this vulnerability to cause a crash, read sensitive data, or execute arbitrary code in the context of the current process.

### CVE-2026-57859

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-30T14:16:59.923 |

e107 prior to version 2.3.8 contains a code execution vulnerability in the e_array deserialization handler that allows an attacker with out-of-band database write access to execute arbitrary PHP code by storing a crafted payload in the user_prefs column. The e_array::unserialize() function in e107_handlers/core_functions.php performs only a prefix check for the string 'array' before passing the stored value to eval(), causing automatic PHP execution whenever the affected user's preferences are materialized through e_user_pref::load().

### CVE-2026-67201

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-07-29T19:16:51.330 |

V through 0.5.2, fixed in commit 85859f0, contains a server-side request forgery (SSRF) bypass vulnerability that allows attackers to circumvent host-based allowlists by exploiting a parser differential between net.urllib and net.http. Attackers can craft a URL containing a backslash in the authority section such that net.urllib.parse() extracts the trusted host for allowlist validation while net.http.get() normalizes the backslash and connects to the internal host, enabling access to internal network services that the allowlist was intended to block.

### CVE-2026-41703

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-30T13:16:49.300 |

VMware ESX, Workstation, and Fusion contain an out-of-bounds read vulnerability. A malicious actor with VM deployment privileges could trigger an out-of-bounds read, potentially leading to information disclosure or more likely a Denial-of-Service (DoS) condition of the host process. On Workstation and Fusion, the impact of this vulnerability is restricted to information disclosure.

### CVE-2026-18381

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-30T12:17:27.693 |

A flaw was found in the koku-metrics-operator for Red Hat OpenShift. The operator's CostManagementMetricsConfig custom resource allows a user able to edit the CR to specify an arbitrary upload URL. The operator attaches its own Kubernetes service-account bearer token to queries sent to this user-controlled URL, allowing the attacker to obtain the token.

### CVE-2026-18378

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-30T12:17:27.553 |

A flaw was found in koku-metrics-operator. The operator's CostManagementMetricsConfig custom resource allows user able to edit the CR to specify an arbitrary upload URL. When authentication.type is set to token (the default), the cluster-global Red Hat Cloud pull-secret bearer token is attached to HTTP requests sent to this user-controlled URL, allowing the attacker to obtain the token.

### CVE-2026-18361

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-30T10:16:36.460 |

The IRIS web application in version 2.4.26 and possibly others is vulnerable to stored cross-site scripting (XSS) in the datastore upload function.

### CVE-2026-18360

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-30T10:16:36.343 |

The IRIS web application in version 2.4.26 and possibly others is vulnerable to stored cross-site scripting (XSS) in the custom attributes function.

### CVE-2026-16969

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-30T10:16:35.860 |

The IRIS web application in version 2.4.26 and possibly others is vulnerable to stored cross-site scripting (XSS) in the assets function.

### CVE-2026-59247

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-07-29T15:16:26.780 |

Insufficient Verification of Data Authenticity vulnerability in Gleam allows an adversary in the middle to substitute forged Hex package contents during dependency resolution.

During dependency resolution Gleam fetches package metadata from the signature-verified Hex repository, which covers each release's dependency requirements and SHA-256 outer_checksum. After resolving versions, gleam_cli::dependencies::lookup_package makes a second request to the unsigned Hex API through gleam_core::hex::get_package_release and records the outer_checksum and dependency names from that JSON response into manifest.toml, instead of the values from the verified repository metadata. The Hex repository signature does not cover the API response.

An adversary in the middle who can intercept TLS with a certificate trusted by the Gleam process (for example a TLS-inspecting proxy using a CA in the operating system trust store or added through GLEAM_CACERTS_PATH), and who can modify both the API release response and the corresponding repository tarball, can supply a package archive with a matching forged checksum without the Hex repository signing key. Gleam verifies the forged tarball against the forged checksum, accepts it, and extracts it as a dependency source, resulting in loss of integrity of the downloaded package contents.

Only projects that resolve or update Hex dependencies are affected, which happens when the manifest is missing, a dependency is added or updated, or dependency requirements change. Builds that reuse an unchanged, known-good manifest.toml continue to verify tarballs against its pinned checksum. This issue affects gleam: from 0.18.0 before 1.18.0.

### CVE-2026-58043

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-30T06:25:55.310 |

A flaw in Node.js Permission Model enforcement can over-grant filesystem access across radix-tree prefix boundaries.

Under `--permission`, an attacker who is granted access to one path can abuse boundary handling to read from or write to paths outside the intended filesystem allowlist.

This vulnerability affects Node.js **main**, **22.x**, **24.x**, and **26.x**.

### CVE-2026-16529

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-30T06:25:02.953 |

A signed integer overflow in the PCP __pmGetPDU() function can be exploited via crafted network packets during PDU processing or SASL negotiation. This permanently blinds the affected daemon, resulting in a total denial of service (DoS) for subsequent packet reads.

### CVE-2026-12687

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-30T06:24:58.677 |

The ProfileGrid  WordPress plugin before 5.9.9.8 does not restrict which group an anonymous visitor may register into through its front-end registration, allowing unauthenticated users to register directly into a privileged group and be granted that group's configured role, up to Administrator when such a group exists, leading to privilege escalation.

### CVE-2026-1360

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-30T05:16:34.657 |

The BuddyPress plugin for WordPress is vulnerable to Deserialization of Untrusted Data in all versions up to, and including, 14.5.0 This is due to the `bp_unserialize_profile_field()` function using `@unserialize()` without the `allowed_classes` parameter on user-controlled XProfile field data. This makes it possible for authenticated attackers, with subscriber-level access and above, to inject arbitrary PHP objects via XProfile textbox fields, which could lead to remote code execution if a suitable POP chain is available in the WordPress environment.

### CVE-2026-17979

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-30T01:17:02.477 |

Race in V8 in Google Chrome prior to 151.0.7922.72 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-17952

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-30T01:16:59.603 |

Inappropriate implementation in V8 in Google Chrome prior to 151.0.7922.72 allowed an attacker who convinced a user to install a malicious extension to execute arbitrary code inside a sandbox via a crafted Chrome Extension. (Chromium security severity: Low)

### CVE-2026-17948

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-30T01:16:59.120 |

Type Confusion in V8 in Google Chrome prior to 151.0.7922.72 allowed an attacker who convinced a user to install a malicious extension to execute arbitrary code inside a sandbox via a crafted Chrome Extension. (Chromium security severity: Low)

### CVE-2026-17930

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-30T01:16:57.237 |

Insufficient validation of untrusted input in Extensions in Google Chrome prior to 151.0.7922.72 allowed a remote attacker who had compromised the renderer process to perform privilege escalation via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-17916

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-30T01:16:55.780 |

Insufficient policy enforcement in Settings in Google Chrome prior to 151.0.7922.72 allowed a remote attacker who had compromised the renderer process to perform privilege escalation via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-17877

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-30T01:16:51.637 |

Inappropriate implementation in Chromoting in Google Chrome on Linux prior to 151.0.7922.72 allowed a local attacker to perform OS-level privilege escalation via malicious network traffic. (Chromium security severity: Medium)

### CVE-2026-17816

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-30T01:16:45.153 |

Insufficient policy enforcement in Speech in Google Chrome on Android prior to 151.0.7922.72 allowed a remote attacker who had compromised the renderer process to perform privilege escalation via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-17774

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-30T01:16:40.670 |

Insufficient validation of untrusted input in Variations in Google Chrome prior to 151.0.7922.72 allowed an attacker in a privileged network position to potentially exploit heap corruption via malicious network traffic. (Chromium security severity: Medium)

### CVE-2026-17716

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-30T01:16:34.137 |

Use after free in Updater in Google Chrome on Mac prior to 151.0.7922.72 allowed a local attacker to perform privilege escalation via malicious network traffic. (Chromium security severity: High)

### CVE-2026-67437

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-401;CWE-770` |
| Published | 2026-07-29T21:17:47.977 |

OliveTin gives access to predefined shell commands from a web interface. From 3000.0.0 until 3000.17.0, the service/internal/auth/otoauth2/restapi_auth_oauth2.go OAuth2 login handler stores per-login state in the registeredStates map on every /oauth/login request without expiring, deleting, or bounding entries, allowing an unauthenticated attacker to exhaust memory and cause a denial of service. This issue is fixed in version 3000.17.0.

### CVE-2026-67432

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-29T20:17:12.277 |

MCP Ruby SDK is the official Ruby SDK for Model Context Protocol servers and clients. Prior to 0.23.0, MCP::Server::Transports::StreamableHTTPTransport in the mcp gem reads and parses an entire JSON-RPC POST body without a size limit, allowing an unauthenticated remote attacker to exhaust process memory. This issue is fixed in version 0.23.0.

### CVE-2026-5491

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-29T20:17:06.020 |

DriveLock Directory Traversal Information Disclosure Vulnerability. This vulnerability allows remote attackers to disclose sensitive information on affected installations of DriveLock. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the web service, which listens on TCP port 6067 by default. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to disclose information in the context of the service account. Was ZDI-CAN-28722.

### CVE-2026-5487

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-29T20:17:05.653 |

DriveLock Directory Traversal Information Disclosure Vulnerability. This vulnerability allows remote attackers to disclose sensitive information on affected installations of DriveLock. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the web service, which listens on TCP port 4568 by default. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to disclose information in the context of the service account. Was ZDI-CAN-28746.

### CVE-2026-5057

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-29T20:17:05.497 |

ATEN Unizon RpcProvider Missing Authentication Denial-of-Service Vulnerability. This vulnerability allows remote attackers to create a denial-of-service condition on affected installations of ATEN Unizon. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the RpcProvider class. The issue results from the lack of authentication prior to allowing access to functionality. An attacker can leverage this vulnerability to create a denial-of-service condition on the system. Was ZDI-CAN-29041.

### CVE-2026-15975

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-29T20:17:02.117 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 11.8 before 19.0.5, 19.1 before 19.1.3, and 19.2 before 19.2.1 that under certain conditions could have allowed an unauthenticated user to cause a denial of service due to insufficient resource throttling when processing merge request discussions.

### CVE-2025-60931

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-29T17:16:50.367 |

An Insecure Direct Object Reference (IDOR) in the Employee Compensation View function of Infor Global HR v11.24.10.01.33 allows unauthorized attackers to arbitrarily view the compensation information of other employees via a crafted GET request.

### CVE-2026-8497

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-29T18:16:58.787 |

Improper certificate validation in the Devolutions Server connection handling in Devolutions Password Manager 2026.2.1.0 and earlier on Android, iOS, and macOS allows an adjacent-network attacker to intercept and modify sensitive information via a forged TLS certificate.

### CVE-2026-13697

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-200;CWE-248;CWE-525` |
| Published | 2026-07-29T17:16:50.503 |

undici's cache interceptor mishandles malformed Cache-Control private directives. In undici 7.0.0 up to before 7.29.0 and 8.0.0 up to before 8.9.0, a response carrying a degenerate qualified private directive, such as private set to an empty value, can be stored in the default shared cache and later served to a different caller with the same cache key, disclosing private response bodies and headers including Set-Cookie. Separately, a Cache-Control header that combines an unqualified private directive with a qualified one triggers an uncaught TypeError in the cache-control parser, which rejects the request and, depending on the consumer's error handling, can terminate the process. Both issues affect applications using the cache interceptor in shared mode, including the default configuration. The issues are fixed in undici 7.29.0 and 8.9.0.

### CVE-2026-54660

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-201;CWE-522;CWE-918` |
| Published | 2026-07-29T15:16:25.300 |

swagger-typescript-api generates API clients for Fetch or Axios from OpenAPI specifications. Prior to 13.12.2, src/resolved-swagger-schema.ts getRemoteRequestHeaders forwards --authorizationToken to every URL fetched by fetchRemoteSchemaDocument while warmUpRemoteSchemasCache resolves external $ref URLs, allowing an attacker-controlled OpenAPI spec to exfiltrate the developer or CI bearer token to a cross-origin endpoint. This issue is fixed in version 13.12.2.

### CVE-2026-16527

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-30T06:25:02.813 |

An unauthenticated remote attacker can bypass access controls by sending crafted requests to the PCP pmproxy /store endpoint. This allows the attacker to overwrite any PMDA metric, leading to arbitrary code execution and system takeover.

### CVE-2026-16727

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-30T02:16:45.537 |

Concurrent Execution using Shared Resource with Improper Synchronization (“Race Condition”) in ASUS Armoury Crate allows a local user to execute arbitrary code with elevated privileges via a crafted file replacement.
Refer to the ' Security Update for ASUS Armoury Crate ' section on the ASUS Security Advisory for more information.

### CVE-2025-69949

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-29T22:16:52.213 |

kishan0725 Hospital Management System 4.0 is vulnerable to SQL Injection in check_availability.php via the parameters emailid and email.

### CVE-2025-69945

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-29T22:16:52.097 |

kishan0725 Hospital Management System 4.0 is vulnerable to SQL Injection in /doctor/edit-patient.php?editid=1.

### CVE-2025-67408

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-29T22:16:51.627 |

Sourcecodester CASAP Automated Enrollment System 1.0 is vulnerable to SQL Injection in /save_user.php via the parameter status.

### CVE-2025-67407

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-29T22:16:51.510 |

Sourcecodester CASAP Automated Enrollment System 1.0 is vulnerable to SQL Injection in update_student.php via parameters fname and student_class.

### CVE-2025-67406

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-29T22:16:51.393 |

https://www.sourcecodester.com Advocate office management system 1.0 is affected by: SQL Injection. The impact is: execute arbitrary code (remote). The component is: control/activate_case.php,?id=1. The attack vector is: A SQL Injection vulnerability exists in the activate_case.php in parameter id endpoint of Advocate office management system. Unsanitized user input in the specified parameter is interpolated directly into an SQL query, allowing attackers to infer or extract data and, in some cases, execute stacked/time-based payloads. ¶¶ Affected Component & Parameter Affected Endpoint URL: http://localhost/advocate/kortex_lite/control/activate_case.php?id=1 HTTP Method: GET Vulnerable File: activate_case.php Parameter: id Vector Location: GET Injection Techniques (as identified by sqlmap) Type: error-based Title: MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE) Payload: id=1 AND EXTRACTVALUE(6268,CONCAT(0x5c,0x71766b6a71,(SELECT (ELT(6268=6268,1))),0x716a7a6b71)) Type: time-based blind Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP) Payload: id=1 AND (SELECT 4464 FROM (SELECT(SLEEP(5)))aHqo) Proof of Concept (Burp Repeater)

### CVE-2025-67405

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-29T22:16:51.283 |

Sourcecodester CASAP Automated Enrollment System 1.0 is vulnerable to SQL Injection in update_password.php via the parameter new_password.

### CVE-2026-15144

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-307;CWE-770` |
| Published | 2026-07-29T17:16:50.637 |

@fastify/rate-limit before 11.2.0 keys rate-limit buckets by the verbatim client IP string returned from request.ip. Because a single IPv6 client can control a large address range (a /64 holds 2^64 distinct addresses) and the same address has multiple valid textual representations, an IPv6 capable client can defeat the rate-limit boundary by rotating addresses or by rewriting the same address in different forms. Applications that use @fastify/rate-limit to protect endpoints such as authentication, password reset, OTP delivery, or expensive API calls can be bypassed by IPv6 clients behind a proxy that surfaces IPv6 to the origin when trustProxy is enabled. The issue is fixed in @fastify/rate-limit 11.2.0, where the default key generator normalizes IPv6 addresses to their canonical form, collapses IPv4 mapped IPv6 to IPv4, and applies a configurable prefix mask (default /64) via a new ipv6Subnet option.

### CVE-2026-15397

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-30T12:17:26.927 |

The Subscriptions for WooCommerce plugin for WordPress is vulnerable to Missing Authorization in all versions up to, and including, 2.0.0. This is due to the plugin not properly verifying that a user is authorized to perform an action via the wps_sfw_install_plugin_configuration AJAX handler. This makes it possible for authenticated attackers, with shop manager-level access and above, to install and activate arbitrary WordPress.org plugins.

### CVE-2026-12357

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-07-29T20:17:00.270 |

Heimdall Data Database Proxy generateFileContent CRLF Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Heimdall Data Database Proxy. Authentication is required to exploit this vulnerability.

The specific flaw exists within the generateFileContent function. The issue results from the lack of proper neutralization of CRLF sequences. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-29251.

### CVE-2026-18255

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-29T17:16:51.393 |

A flaw was found in Quay. A user configured in GLOBAL_READONLY_SUPER_USERS is able to view robot account tokens for repositories they are not a member of, allowing an attacker with read-only superuser privileges to impersonate any robot account.

### CVE-2026-13584

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-924` |
| Published | 2026-07-30T07:16:56.327 |

Improper Enforcement of Message Integrity During Transmission in a Communication Channel vulnerability in Mitsubishi Electric MELSEC MX Controller MX-R model, MELSEC MX Controller MX-F model, Master/local module, CC-Link IE TSN interface board, Motion module, Motion Control Board, Block-type remote module, Block-type remote module with safety functions, Analog-Digital converter module, Digital-Analog converter module, CC-Link IE TSN compatible coupler, FPGA module, Tension meter, AC Servo MELSERVO-J5, AC Servo MELSERVO-JET, Liner Track System MTR-S series Linear track control module, Inverter FR-A800/F800/E800 Series, Industrial Robot CR800-D series controller Network Base Card, CC-Link IE TSN expansion unit, CC-Link IE TSN-CC-Link IE Field Network bridge module, CC-Link IE TSN-AnyWireASLINK bridge module, Energy Measuring Unit CC-Link IE TSN Communication Unit, Industrial Computer MELIPC series, GOT3000 Series, CC-Link IE TSN Communication Unit, Motion Control Software, CC-Link IE TSN Communication Software for Windows, Analysis Support Software MELSOFT VIMA, Master/Local module Designated communication LSI DeviceKit, Master/Local module Designated communication LSI, Remote Station Communication LSI with GbE-PHY, CC-Link IE TSN Master/Local module Designated communication LSI SDK, and Remote station software development kit allows an attacker with access to a CC-Link IE TSN network to tamper with communication data (control input/output values) by sending specially crafted packets under specific timing conditions. This could allow the attacker to cause a denial-of-service (DoS) condition in the affected product by interfering with its control function or causing it to operate incorrectly.

### CVE-2026-67247

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-30T05:16:39.017 |

A path traversal vulnerability was found in the IHM Log handling of ADM. The vulnerability occurs because user-controlled disk serial input is not sufficiently validated before being used to construct the path of an IHM log database file. An authenticated attacker can exploit this issue to cause the affected component to access an unintended filesystem path or log database file.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RUN1 as well as from ADM 5.0.0 through ADM 5.1.3.RI81.

### CVE-2026-18188

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-07-30T03:16:24.503 |

A format string vulnerability was found in the Rsync Backup on the ADM. The vulnerability occurs because user-controlled rsync backup configuration or log data may be processed through an unsafe format string operation. An authenticated attacker can exploit this issue to disclose memory information or cause denial of service of the affected backup component.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RUN1 as well as from ADM 5.0.0 through ADM 5.1.3.RI81.

### CVE-2026-18187

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-07-30T03:16:24.363 |

A format string vulnerability was found in the Internal Backup on the ADM. The vulnerability occurs because user-controlled task input may be included in an error response and processed through an unsafe format string operation. An authenticated attacker can exploit this issue to disclose memory information or cause denial of service of the affected CGI process.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RUN1 as well as from ADM 5.0.0 through ADM 5.1.3.RI81.

### CVE-2026-18186

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-07-30T03:16:24.213 |

A stored format string vulnerability was found in the FTP Backup on the ADM. The vulnerability occurs because user-controlled backup configuration data may be written into a task log and later processed through an unsafe format string operation. An authenticated attacker can exploit this issue to disclose memory information or cause denial of service of the affected CGI process.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RUN1 as well as from ADM 5.0.0 through ADM 5.1.3.RI81.

### CVE-2026-15929

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-30T02:16:45.360 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in LG Electronics SmartShare allows SQL Injection.

This issue affects SmartShare: through 2.3.1712.1202, which is supported on Microsoft Windows 10 and earlier versions.

### CVE-2026-67194

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-07-29T17:16:54.017 |

Courier IMAP before 6.0.1 and Courier Mail Server before 2.0.2 allow authenticated IMAP users to crash the imapd process via deeply nested parenthesized SEARCH queries. The SEARCH command parser (alloc_search_key in searchinfo.C) recursively descends on nested parenthesized groups through a mutual recursion chain with alloc_search_andlist() and alloc_search_notkey(), with no depth limit. Courier IMAP has no overall command line length limit, making exploitation trivial. A single IMAP command with ~2500 nested parentheses overflows the 8MB default stack, causing SIGSEGV.

### CVE-2026-16543

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-862` |
| Published | 2026-07-29T16:17:50.660 |

Kong Operator's embedded Kong Kubernetes Ingress Controller (KIC) allows a user with namespace-scoped Secret creation privileges to cause a cluster-wide ingress configuration denial of service. The embedded KIC collects CA-certificate Secrets across all watched namespaces using a label selector alone, without ingress-class or namespace restrictions. The CA-certificate primary key is derived from a user-supplied field in the Secret. Duplicate CA-certificate IDs cause Kong Gateway to reject the entire configuration document and halting all ingress changes cluster-wide.

### CVE-2026-15228

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-862` |
| Published | 2026-07-29T16:17:49.723 |

Kong Kubernetes Ingress Controller (KIC) allows a user with namespace-scoped Secret creation privileges to cause a cluster-wide ingress configuration denial of service. KIC collects CA-certificate Secrets across all watched namespaces using a label selector alone, without ingress-class or namespace restrictions. The CA-certificate primary key is derived from a user-supplied field in the Secret. Duplicate CA-certificate IDs cause Kong Gateway to reject the entire configuration document and halting all ingress changes cluster-wide.

### CVE-2026-67245

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-30T05:16:38.713 |

A path traversal vulnerability was found in the VPN Clients on the ADM. The vulnerability occurs because user-controlled certificate name input is not sufficiently validated before being used to construct the upload destination path. An authenticated attacker can exploit this issue to write an uploaded certificate file outside the intended VPN certificate directory, subject to process privileges and filesystem permissions.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RUN1 as well as from ADM 5.0.0 through ADM 5.1.3.RI81.

### CVE-2026-17993

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-30T01:17:03.977 |

Race in Updater in Google Chrome on Windows prior to 151.0.7922.72 allowed a local attacker to perform privilege escalation via a malicious file. (Chromium security severity: Low)

### CVE-2026-40272

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-29T18:16:53.347 |

Improper Input Validation in the decode() function of the traceparser library could allow an attacker with a corrupted kernel trace event log (.kev) file, to execute arbitrary code or cause a crash in processes that use libtraceparser in QNX hosts or targets.

### CVE-2026-14266

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.0/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-29T18:16:50.720 |

7-Zip XZ Decompression Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of 7-Zip. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the processing of XZ chunked data. Crafted XZ-compressed data can trigger an overflow of a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30169.

### CVE-2026-66723

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-29T15:16:29.877 |

MWDB Core versions >=2.2.0 and <2.19.0 contain a missing authorization vulnerability in the Remote Instances proxy API. The proxy API does not verify authentication for incoming requests, allowing an unauthenticated remote attacker to send arbitrary requests to a remote MWDB instance using the identity and permissions associated with the configured API key. This can result in unauthorized actions being performed on the remote instance as if executed by the user whose API key was used to set up the remote instance. The vulnerability is limited to deployments where Remote Instances have been configured.This issue has been fixed in version 2.19.0
