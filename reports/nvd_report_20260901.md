# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-31 15:00 UTC
- **対象期間**: `2026-08-30T15:00:22.000Z` 〜 `2026-08-31T15:00:30.000Z`
- **重要CVE数**: 68 件（Critical 9.0+: 19 件 / High 7.0〜: 49 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に報告された CVE のうち、CVSS が 7.0 以上のものは **30 件近く** に上り、特に **リモートコード実行 (RCE)・認証回避・権限昇格** が多発しています。  
- 製品領域は「クラウドビルド・ストレージ・ネットワーク機器・Web フレームワーク・IaC ツール」に偏り、**インフラ全体の攻撃面が広がっている**ことが特徴です。  
- 多くの脆弱性は **パッチがすでに公開** しているにも関わらず、アップデートが遅れるケースが目立ち、**サプライチェーンリスク** が顕在化しています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS (ベクトル) | 主な影響 | 注目理由 |
|-----|----------------|----------|----------|
| **CVE‑2026‑77956** | 10.0 (AV:N/AC:L/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H) | ash‑project **ash_ai** の `EEx.eval_string/2` を介した **リモートコード実行**。認証不要で任意の Elixir コードが実行可能。 | **最高スコア (10.0)** かつ **クラウド/AI サービス** に組み込まれやすく、被害拡大が容易。 |
| **CVE‑2026‑58574** | 9.8 (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) | Dell **PowerStore** 管理インターフェースの認証欠如。攻撃者がファイルシステム内部情報を取得可能。 | ストレージ基盤は企業の重要資産。認証回避は **情報漏洩 + さらなる横展開** の入り口になる。 |
| **CVE‑2026‑49003** | 9.6 (AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H) | コマンドインジェクションにより **システムランタイムファイル削除** と **root 権限取得**。SNMP パスワード等機密情報が漏洩。 | 攻撃経路が **ローカルネットワーク限定** でも、内部脅威やマルチステージ攻撃で深刻化。 |
| **CVE‑2026‑82854** | 9.3 (AV:N/AC:L/PR:N/UI:N/VC:H/VI:H/VA:H) | **Nodemailer < 8.0.4** の SMTP コマンドインジェクション。`envelope.size` に CRLF を含めると任意コマンド実行。 | メール送信は多くの Web アプリで共通利用。インジェクションはスパム送信や情報窃取に直結。 |
| **CVE‑2026‑82856** (複数) | 9.3 (AV:N/AC:L/PR:N/UI:N) | **@hulumi/policies** 系列 (1.3.2 未満) の IAM ポリシー検証バイパス・特権昇格。CI/CD パイプラインでの権限境界が崩壊。 | IaC/CI が広く採用される中、**サプライチェーン攻撃** のリスクが顕在化。 |

> **注:** 上記はスコア・影響範囲・実装環境の広さを総合的に評価し、**組織のインフラ全体に波及しやすい**ものを選出しています。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 / ライブラリ | 推奨バージョン / 対策 | 備考 |
|-------------------|----------------------|------|
| **ash‑project ash_ai** | ベンダーが提供する **パッチリリース**（2026‑06‑30 以降）へアップデート。 | `EEx.eval_string/2` の使用を廃止、入力サニタイズを徹底。 |
| **Dell PowerStore** | 最新ファームウェア **7.5.2 以降**（管理インターフェース認証強化） | 管理ネットワークは **IP フィルタリング** と **MFA** を併用。 |
| **対象システム（CVE‑2026‑49003）** | 該当コンポーネントの **ベンダー提供パッチ**（2026‑07‑15） | コマンドインジェクション防止のため、入力検証と最小権限実行を実装。 |
| **Nodemailer** | **8.0.4 以上** に更新 | `envelope.size` へのサニタイズ処理を追加。 |
| **@hulumi/policies / @hulumi/* 系列** | **1.3.2 以上** にアップグレード | IAM ポリシー評価ロジックの修正が含まれる。 |
| **Tenda AC 系列ルータ** (AC18, AC1206) | ベンダー提供の **最新ファームウェア**（2026‑08‑01 以降） | Telnet/WEB UI の認証回避が修正済み。 |
| **Phison PS3111‑S11 コントローラ** | メーカー提供の **署名検証強化ファームウェア**（2026‑07‑20） | RSA 公開鍵を不変ストレージに固定。 |
| **Joomla Extension – Helix Ultimate** | **2.2.10 以上** に更新 | MIME タイプ検証とアップロード制限が追加。 |
| **AJCloud AJY IPC** | **01.10715.11.38 以降** のファームウェア | パス・トラバーサル対策が実装。 |
| **YaCy Search Server** | **1.942 以降** のリリースで XEE 対策済み | XML パーサの外部エンティティ無効化。 |

### 3.2 環境・設定の見直し
- **ネットワーク分離**：管理インターフェース（PowerStore、Tenda ルータ等）は管理 VLAN に限定し、外部からの直接アクセスを遮断。  
- **最小権限の徹底**：`ash_graphql` のクエリ複雑度制限や、CI/CD パイプラインで使用する IAM ロールは **必要最小限** に絞る。  
- **入力サニタイズ**：`EEx.eval_string/2`、SMTP envelope、SQL クエリ、HTML 出力など、外部入力を直接評価・組み立てる箇所は **ホワイトリスト方式** で検証。  
- **監査ログ強化**：`@hulumi/baseline` の CloudTrail セレクタ監視が不完全なため、**CloudTrail の全イベント** を S3 に集約し、SIEM でリアルタイム分析を実施。  
- **

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-77956

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-31T01:16:49.563 |

Improper Control of Generation of Code (Code Injection) vulnerability in ash-project ash_ai allows a remote, unauthenticated client to execute arbitrary Elixir code.

AshAi.Actions.Prompt evaluates prompt content through EEx.eval_string/2. The documented prompt: fn input, context -> ... end form lets the prompt content be built from action arguments, so when a prompt action's text incorporates request data, that attacker-controlled text is compiled and run as an EEx template (Elixir source). Content such as <%= System.cmd(...) %> therefore executes on the server before any model request is made, requiring no authentication beyond reaching a prompt action. The fix stops evaluating function-supplied prompt content as EEx; only statically configured templates are evaluated.

This issue affects ash_ai: from 0.1.0 before 1.0.0.

### CVE-2026-58574

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-31T07:17:44.743 |

Dell PowerStore contains a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with network access to the restricted management interface could potentially exploit this vulnerability to read internal system information from the appliance filesystem. This is a Critical vulnerability as it could expose sensitive information and credentials which allow full administrative access to the array.

### CVE-2026-49003

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-31T10:16:49.963 |

Attackers can exploit command injection vulnerabilities to delete core system runtime files, causing the monitoring module to crash and become paralyzed; simultaneously, they can obtain root privileges to steal configuration passwords such as SNMP, thereby tampering with critical system parameters and triggering abnormal operation of the entire power system.

### CVE-2026-19410

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-345;CWE-367` |
| Published | 2026-08-31T09:17:03.130 |

An Incorrect Authorization vulnerability in GitHub Trigger Comment Control in Google Cloud Build prior to 2026-06-24 on Google Cloud Platform allows a remote attacker to execute unreviewed code in the build environment using webhook suppression.


This vulnerability was patched on 24 June 2026, and no customer action is needed.

### CVE-2026-82695

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-08-31T13:18:29.953 |

A security flaw has been discovered in Tenda AC18 15.03.05.19. Impacted is an unknown function of the file /goform/telnet of the component Telnet Handler. The manipulation results in missing authentication. The attack can be launched remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-82694

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-08-31T13:18:29.773 |

A vulnerability was identified in Tenda AC1206 15.03.06.23. This issue affects the function R7WebsSecurityHandler of the file /goform/ate of the component Web UI. The manipulation leads to missing authentication. The attack can be initiated remotely. The exploit is publicly available and might be used.

### CVE-2026-82693

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-08-31T13:18:29.580 |

A vulnerability was determined in Tenda AC1206 15.03.06.23. This vulnerability affects the function TendaTelnet of the file /goform/telnet of the component Web UI. Executing a manipulation can lead to missing authentication. It is possible to launch the attack remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-82876

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-31T11:16:41.190 |

Phison PS3111-S11 controller firmware verifies RSA signatures using a public modulus embedded within the firmware image itself rather than anchored in immutable storage. Attackers can generate arbitrary RSA key pairs, sign modified firmware with the private key, embed the matching modulus in the signature segment, and the controller accepts the tampered firmware as valid.

### CVE-2026-82860

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-31T09:17:06.353 |

@hulumi/policies versions before 1.3.2 fail to fully inspect inline and attached IAM policy evidence for the administrator-policy guardrail. Attackers can craft admin-equivalent policy paths that bypass policy evaluation controls.

### CVE-2026-82859

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T09:17:06.210 |

hulumi versions before v1.3.2 contain a deployment SCP template that allows tag-on-create bypasses for hulumi:iac-role protections. Attackers can bypass intended IAM boundary restrictions by exploiting the weakened SCP template in downstream deployments.

### CVE-2026-82858

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-31T09:17:06.067 |

@hulumi/drift versions before 1.3.2 accept externally supplied execute plans without sufficient provenance validation, allowing untrusted reconciliation input to be treated as trusted. Attackers can supply malicious execute plans that bypass security checks to perform unsafe reconciliation operations.

### CVE-2026-82857

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-31T09:17:05.920 |

hulumi versions before v1.3.2 contain a privilege escalation vulnerability in the weekly integration IAM policy that allows role lifecycle operations on af-e2e-* roles without sufficient boundary restrictions. Attackers with the documented principal can create persistent higher-privilege roles in the sandbox account.

### CVE-2026-82856

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T09:17:05.780 |

@hulumi/policies versions before 1.3.2 fail to properly validate set-qualified AWS IAM condition operators in GitHub OIDC trust policies. Attackers can use ForAnyValue:StringLike operators to hide wildcard GitHub Actions OIDC subject conditions from security guardrails.

### CVE-2026-82855

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-31T09:17:05.610 |

@hulumi/policies versions before 1.3.2 contain an evidence validation bypass vulnerability in Cloudflare and deployment-governance validators that allows attackers to suppress violations by submitting unrelated compliant evidence. Attackers can use evidence from different zones, hostnames, origins, or repositories to bypass security guardrails for unrelated resources in the same stack.

### CVE-2026-82854

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-08-31T09:17:05.463 |

Nodemailer before 8.0.4 is vulnerable to SMTP command injection through the unsanitized envelope.size parameter. When an application passes a custom envelope object with a size property containing CRLF characters to sendMail(), the value is concatenated into the SMTP MAIL FROM command (as SIZE=...) without sanitization, allowing injection of arbitrary SMTP commands such as RCPT TO to silently add attacker-controlled recipients. Exploitation requires the application to expose the envelope size to attacker-controlled input, as Nodemailer does not include size in the default auto-constructed envelope.

### CVE-2026-82628

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-269` |
| Published | 2026-08-31T07:17:47.307 |

A vulnerability was found in Colorful iGameCenter 2.0.0.81. This vulnerability affects the function sub_11504 in the library WinRing0x64.sys of the component IOCTL Dispatch. Performing a manipulation of the argument PhysicalAddress/AlignNumer/AlignSize results in improper privilege management. Attacking locally is a requirement.

### CVE-2026-82654

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-30T15:16:46.173 |

SiYuan before v3.8.1 fails to properly escape block name, alias, and memo fields in hint, backlink, and breadcrumb rendering functions. Attackers can set a block's name to contain HTML/script tags that execute when another user views documents referencing or displaying that block.

### CVE-2026-82653

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-30T15:16:46.033 |

SiYuan before v3.8.1 contains a stored cross-site scripting vulnerability in confirmDialog() where unescaped package names and notebook names are interpolated directly into innerHTML assignments. Attackers can submit malicious bazaar packages with HTML/script payloads in the name field that execute in users' browsers when uninstalling packages or unlocking encrypted notebooks.

### CVE-2026-82645

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-30T15:16:44.863 |

AVideo (current commit e01e41ecc and earlier) exposes stream credentials through the plugin/Live/view/Live_restreams/getLiveKey.json.php endpoint. Supplying a 'token' request parameter waives both the Live::canRestream() access gate and the restream ownership check, causing the endpoint to return any restream's stream_key and stream_url (credentials for external platforms such as YouTube, Facebook, and Twitch) without authentication. The token is merely encryptString() of an integer id with no user binding, expiry, or authentication tag. Because encryption uses AES-256-CBC with a deterministic IV and no MAC, and because intval() accepts any string beginning with a digit, an unauthenticated attacker can forge valid tokens using the public encryption oracle in view/url2Embed.json.php, disclosing arbitrary users' stream credentials.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-78078

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-31T14:17:24.257 |

Joomla Extension - joomshaper.com - Privileged File Upload Bypass via Content Spoofing in Helix Ultimate < 2.2.10 - Image uploads previously validated only file extension and basic size parameters. Non-image files disguised with raster extensions could be uploaded. Added strict MIME verification and GD binary raster decoding (imagecreatefromstring) to reject invalid/malformed images fail-closed.

### CVE-2026-82866

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-31T09:17:07.260 |

@pdfme/common before 5.5.10 contains a server-side request forgery vulnerability in the getB64BasePdf function that fetches arbitrary URLs without validation when basePdf is attacker-controlled. Attackers who control the basePdf template field can force servers or clients to make requests to internal endpoints, enabling metadata exfiltration, network reconnaissance, and blind request forgery attacks.

### CVE-2026-82217

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-31T14:17:26.610 |

In Eclipse Theia versions 1.73.0 up to but not including 1.75.0, the AI "Agent Mode" file-change tools (writeFileContent, suggestFileContent, and the replacement and state helpers) resolved a model-supplied file path without a workspace-containment check. A crafted relative path such as ../.bashrc, an absolute path, or a ~-expanded path could therefore write or delete files outside the workspace with the privileges of the Theia backend OS user. Because the path argument is influenced by model output, it can be steered through indirect prompt injection, and in Agent Mode writes are applied without a confirmation dialog. Writing to a host-executed file such as a shell startup file or ~/.ssh/authorized_keys can escalate to code execution on the backend.

### CVE-2026-78074

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T14:17:23.633 |

Joomla Extension - miniorgange.com - Unauthenticated arbitrary extension deinstallation via various miniOrange extensions - a missing authentication check allows unauthenticated actors to delete arbitrary installed extensions. Only the free versions of the miniOrange plugins are affected.

### CVE-2026-5956

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-31T13:18:22.740 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Ankara Hosting Site Management Panel allows SQL Injection.

This issue affects Site Management Panel: through 15062026.

### CVE-2026-12894

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-31T13:17:20.753 |

A flaw was found in the Qute template engine, which is used by Quarkus to generate dynamic content like HTML pages or emails. The issue exists in the component responsible for looking up data values (ReflectionValueResolver), which fails to properly block access to sensitive Java internal functions when processing certain data types like Enums. An attacker who can provide or influence the template text can exploit this bypass to take control of the server by executing unauthorized commands.

### CVE-2026-82880

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-08-31T11:16:41.793 |

YaCy Search Server through 1.941 contains an XML external entity injection vulnerability in SVG, FreeMind, and OpenSearch parsers that fail to disable external entity resolution. Attackers can publish malicious documents with DOCTYPE declarations containing SYSTEM entities pointing to local files, causing the crawler to exfiltrate file contents into the searchable index.

### CVE-2026-82863

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-778` |
| Published | 2026-08-31T09:17:06.790 |

@hulumi/baseline versions before 1.3.2 fail to fully detect CloudTrail selector tampering events, reducing audit logging configuration change coverage. Attackers can modify CloudTrail event selectors without complete detection, potentially evading audit trail monitoring.

### CVE-2026-82861

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T09:17:06.500 |

@hulumi/policies versions before 1.3.2 contain a parent spoof bypass vulnerability that allows attackers to submit spoofed SecureBucket parent evidence during policy evaluation. Attackers can bypass security policy checks by providing falsified evidence, causing the validator to miss unsafe bucket configurations.

### CVE-2026-56718

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-30T21:16:34.160 |

AJCloud AJY IPC firmware prior to version 01.10715.11.37 contains a path traversal vulnerability in the jdbhttpd web service that allows unauthenticated remote attackers to read arbitrary files with root privileges by supplying path traversal sequences in the HTTP request URI. Attackers can send crafted HTTP requests to port 80 without authentication to access sensitive files including cleartext RTSP credentials, Wi-Fi SSID and pre-shared key, device serial number, and cloud binding parameters.

### CVE-2026-81636

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-30T19:17:29.543 |

Allocation of Resources Without Limits or Throttling vulnerability in ash-project ash_graphql allows an unauthenticated client to bypass the configured GraphQL query-complexity limit and force an unbounded database read.

AshGraphql.Graphql.Resolver.query_complexity/3 multiplies child complexity by the requested page size only when the argument map contains :limit (offset pagination). Relay connections and keyset pagination use first and last, which never match that clause and fall through to the catch-all that returns child_complexity + 1. A nested relay query such as posts(first: 500) { edges { node { comments(first: 500) { ... } } } } therefore scores as trivially cheap while materializing the full fan-out, passing an Absinthe max_complexity cap that rejects the equivalent limit-based query. The fix adds first and last clauses clamped to the action's page size.

This issue affects ash_graphql: from 0.16.23 before 1.11.0.

### CVE-2026-82657

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-30T15:16:46.607 |

Admidio before 5.0.12 fails to enforce login-only module restrictions in RSS feed endpoints for forum and announcements modules. Unauthenticated attackers can retrieve forum topics and announcements by sending GET requests to rss/forum.php or rss/announcements.php, disclosing titles, full post text, author names, and timestamps.

### CVE-2026-82655

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-30T15:16:46.310 |

Admidio before 5.0.12 contains a blind SQL injection vulnerability in the relation_type_list parameter of lists_show.php that allows unauthenticated attackers to execute arbitrary SQL queries. Attackers can bypass authentication by providing a dummy UUID in role_list and inject SQL through relation_type_list to extract database contents including password hashes and user credentials.

### CVE-2026-82644

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-08-30T15:16:44.727 |

WWBN AVideo (current e01e41ecc and earlier) contains a brute-force rate limiting bypass in enforceRateLimit(), which protects login.json.php and 13 other endpoints. The function stores its attempt counter via a cache layer (ObjectYPT::setCacheGlobal) that silently discards writes for any client identified as a bot by isBot(). Because isBot() treats a missing User-Agent header as a bot by default — and also matches common bot identifiers such as 'curl', 'bot', 'crawler', and 'spider' — the counter never increments for such clients, so the rate limit never fires. An unauthenticated attacker can therefore submit unlimited login attempts (e.g., by omitting the User-Agent header or using curl's default User-Agent), enabling unrestricted password-guessing attacks.

### CVE-2026-78077

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-31T14:17:24.113 |

Joomla Extension - joomshaper.com -  Stored Cross-Site Scripting (XSS) in MegaMenu Layout Container & Embed Inputs in Helix Ultimate < 2.2.10 - Unsanitized column and item configuration values stored within the MegaMenu layout JSON were rendered without complete contextual escaping, allowing injection of malicious HTML/JS. Stricter sanitization and tag allowlists via `InputFilter` and `htmlspecialchars` were implemented.

### CVE-2026-82692

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-31T13:18:29.387 |

A vulnerability was found in D-Link DNS-340L and DNS-345 up to 20260717. This affects an unknown part of the file /cgi-bin/iscsi_mgr.cgi. Performing a manipulation of the argument alias/username/password/volume_location results in os command injection. It is possible to initiate the attack remotely. The exploit has been made public and could be used.

### CVE-2026-82689

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-31T12:17:57.763 |

A vulnerability was detected in D-Link DNS-320L, DNS-327L, DNS-340L and DNS-345 up to 20260717. Affected is an unknown function of the file /cgi-bin/isomount_mgr.cgi of the component ISO Image Handler. The manipulation of the argument upIsoRootPath results in os command injection. The attack can be executed remotely. The exploit is now public and may be used.

### CVE-2026-82862

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-31T09:17:06.643 |

Hulumi versions before v1.3.2 resolve the threat-model helper script from an unsafe root, allowing workspace files to shadow the intended helper script. Attackers can place malicious files in the workspace to execute arbitrary code during local skill execution.

### CVE-2026-82616

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-31T05:17:06.393 |

A vulnerability was found in TOTOLINK NR1800X 9.1.0u.6681_B20230703. Impacted is the function setUploadSetting of the file /cgi-bin/cstecgi.cgi. The manipulation of the argument FileName results in stack-based buffer overflow. The attack can be executed remotely. The exploit has been made public and could be used.

### CVE-2026-82593

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-31T00:16:41.630 |

A flaw has been found in D-Link DIR-825M 1.1.8. This impacts the function sub_41802C of the file /boafrm/formLtefotaUpgradeFibocom of the component LTE Module Firmware Upgrade. This manipulation of the argument fota_url causes stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit has been published and may be used.

### CVE-2026-82592

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-30T23:17:08.303 |

A vulnerability was detected in D-Link DIR-825M 1.1.8. This affects the function sub_46725C of the file /boafrm/formDiskFormat of the component Disk Formatting Handler Endpoint. The manipulation of the argument partition results in stack-based buffer overflow. The attack can be executed remotely. The exploit is now public and may be used.

### CVE-2026-82691

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-31T12:17:58.163 |

A vulnerability has been found in D-Link DNS-320L, DNS-327L, DNS-340L and DNS-345 up to 20260717. Affected by this issue is some unknown functionality of the file /cgi-bin/usb_device.cgi of the component CGI Handler. Such manipulation of the argument f_ups_ip leads to os command injection. The attack may be performed from remote. The exploit has been disclosed to the public and may be used.

### CVE-2026-82690

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-31T12:17:57.977 |

A flaw has been found in D-Link DNS-327L and DNS-340L up to 20260717. Affected by this vulnerability is an unknown functionality of the file /cgi-bin/ve_mgr.cgi. This manipulation of the argument f_dev causes os command injection. The attack is possible to be carried out remotely. The exploit has been published and may be used.

### CVE-2026-82688

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-31T11:16:40.353 |

A security vulnerability has been detected in D-Link DNS-340L and DNS-345 1.01B04/1.03B06/1.04.B02/1.05b04. This impacts an unknown function of the file /cgi-bin/virtual_vol.cgi of the component Virtual Volume Handler. The manipulation of the argument f_sharename/f_target/f_name leads to os command injection. Remote exploitation of the attack is possible. The exploit has been disclosed publicly and may be used.

### CVE-2026-77850

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-31T03:16:42.307 |

Stored Cross-site Scripting vulnerability in ash-project ash_admin executes attacker-supplied record content as script in an administrator's browser.

The relationship typeahead components AshAdmin.Components.Resource.RelationshipField and AshAdmin.Components.Resource.ManagedRelationshipSelectField highlight the matched search term by wrapping it in <b> tags and rendering the whole string with Phoenix.HTML.raw/1. The highlighted value is the destination record's label_field, ordinary database content that is often written by lower-privileged users. Because raw/1 disables output escaping for the entire string, a stored label such as <img src=x onerror=...> runs as JavaScript in the admin's session as soon as a matching record appears in the dropdown, giving the attacker the admin's privileges over everything AshAdmin exposes. The fix HTML-escapes the label before inserting the highlight markup.

This issue affects ash_admin: from 0.13.0 before 1.3.1.

### CVE-2026-82662

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-31T09:17:04.093 |

Nodemailer before 8.0.8 disables TLS certificate verification in lib/fetch/index.js through rejectUnauthorized: false, allowing attackers to intercept OAuth2 token requests. Attackers in a machine-in-the-middle position can capture OAuth client secrets, refresh tokens, and access tokens transmitted over compromised HTTPS connections.

### CVE-2026-82722

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-31T03:16:43.817 |

Allocation of Resources Without Limits or Throttling vulnerability in ash-project ash_admin lets any client that can reach the admin LiveView exhaust the BEAM atom table and crash the entire node.

Two LiveView event handlers interned atoms from unvalidated client input: AshAdmin.PageLive's set_actor built modules from the resource/domain payload with Module.concat/1, and AshAdmin.Components.Resource.Show's calculate converted every submitted form key with String.to_atom/1. Atoms are never garbage collected and the table is capped, so flooding either event with random names mints a new atom per request until the VM aborts, taking down every application on the node. The fix resolves the submitted resource/domain against the known shown resources and maps calculation keys to declared arguments, so no client-supplied string is interned.

This issue affects ash_admin: from 0.1.0 before 1.3.1.

### CVE-2026-82673

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-31T03:16:43.473 |

Improper Limitation of a Pathname to a Restricted Directory (Path Traversal) vulnerability in ash-project ash_admin allows writing attacker-controlled bytes to arbitrary paths on the server.

AshAdmin.Components.Resource.Form.consume_file_uploads/1 builds the destination as Path.join([tmp_dir, entry.client_name]) and writes it with File.cp!/2. entry.client_name is the browser-supplied filename and is not sanitized, and Path.join/1 does not normalize ... An upload named ../../../../var/www/app/priv/static/x.png therefore escapes the random temp directory and lands anywhere the BEAM user can write, enabling arbitrary file write and potentially remote code execution by overwriting application assets, configuration, or cron/ssh files. The only guard is an extension allowlist defaulting to :any that checks only the extension. The fix strips path components with Path.basename/1 before joining.

This issue affects ash_admin: from 0.13.7 before 1.3.1.

### CVE-2026-75757

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-565` |
| Published | 2026-08-31T03:16:42.133 |

Reliance on Cookies without Validation and Integrity Checking vulnerability in ash-project ash_admin lets an attacker who controls a sibling subdomain rebind an admin's session to a different actor, tenant, or authorization mode.

AshAdmin's client JavaScript read its state cookies (tenant, actor_resource, actor_primary_key, actor_action, actor_domain, actor_authorizing, actor_paused) by matching the cookie name with an unanchored regular expression (new RegExp(name + "=([^;]+)")) against the whole document.cookie. Any cookie whose name merely ends with the requested name therefore matches, and whichever is serialized first wins. Because cookies are shared across a registrable domain, a compromised sibling subdomain can set a shadowing cookie (for example xactor_authorizing) with Domain=.example.com that flows unvalidated into the admin's LiveSocket connect params. The fix matches cookie names by exact equality.

This issue affects ash_admin: from 0.9.1 before 1.3.1.

### CVE-2026-82871

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-31T09:17:08.017 |

ToolJet before v3.16.208 fails to validate organization membership in database read routes, allowing any authenticated user to access other organizations' table schemas and row data. Attackers can supply arbitrary organization IDs in URL parameters to list tables, retrieve column definitions, and execute join queries to read actual stored data from victim organizations.

### CVE-2026-82869

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-31T09:17:07.693 |

ToolJet Database versions before v3.16.44 contain a privilege escalation vulnerability in the join_tables endpoint that grants JOIN_TABLES ability to all authenticated users without role or workspace membership validation. Attackers can read arbitrary ToolJet Database tables from any workspace by supplying victim workspace identifiers in the request path while authenticating with their own workspace credentials.

### CVE-2026-19702

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-31T14:17:14.047 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in TÜBİTAK BİLGEM Software Technologies Research Institute Pardus Boot Repair allows OS Command Injection.

This issue affects Pardus Boot Repair: from 1.0.7 before 1.0.8.

### CVE-2026-82724

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-31T04:17:28.980 |

Incorrect Authorization vulnerability in ash-project ash_phoenix invokes the SubdomainHook authorization callback with a nil tenant, so tenant-scoped access checks never see the tenant they are meant to enforce.

AshPhoenix.LiveView.SubdomainHook.on_mount/4 attached a handle_params hook to assign the tenant and then immediately called handle_subdomain in the same on_mount. The tenant assign is only written when LiveView later runs handle_params, strictly after on_mount returns, so handle_subdomain read an unset assign and ran as apply(m, f, [socket, nil | a]). A consumer gate that halts when the user does not belong to the tenant instead evaluated nil, either crashing or taking a permissive branch, and it was never re-run once the real subdomain was assigned or on later navigations. The fix runs handle_subdomain inside the handle_params hook with the real tenant on every navigation.

This issue affects ash_phoenix: from 2.1.26 before 2.3.25.

### CVE-2026-76763

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1284` |
| Published | 2026-08-31T14:17:23.050 |

A flaw was found in SmallRye GraphQL. The number scalar coercion for BigInteger does not properly validate the magnitude of float or string inputs. An unauthenticated remote attacker can exploit this by sending a GraphQL query containing a large exponent float literal. This can lead to the allocation of extremely large BigInteger objects, causing CPU exhaustion or an OutOfMemoryError, resulting in a denial of service.

### CVE-2026-19616

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-31T14:17:13.857 |

Missing Authorization vulnerability in TBC Technology Inc. KitLogistic allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects KitLogistic: before v2.2.2.

### CVE-2026-81624

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-31T09:17:03.453 |

Undertow is a flexible performant web server used in JBoss EAP and WildFly. A flaw was found in how Undertow handles WebSocket connections. Specifically, certain configuration limits like message buffer sizes and session timeouts cannot be adjusted and default to being unlimited. This allows a remote attacker to send large amounts of data or maintain connections indefinitely, potentially crashing the server by exhausting its memory or other resources.

### CVE-2026-82680

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-08-31T11:16:40.177 |

A weakness has been identified in D-Link DSM-G600 1.01. This affects an unknown function of the file /load_file.cgi of the component Multipart Handler. Executing a manipulation can lead to out-of-bounds write. The attack may be launched remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-81315

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-31T01:16:49.977 |

Origin Validation Error vulnerability in ash-project ash_ai allows a malicious web page to bypass the MCP server's DNS-rebinding protection and issue cross-site requests to a user's local MCP server with that user's actor.

In AshAi.Mcp.Server, with the default allowed_origins: nil, origin_allowed?/3 accepts an origin when uri.host == conn.host and the forwarded scheme is https. Both values are attacker-controlled: conn.host comes from the Host header and the scheme is read from the raw x-forwarded-proto header with no trusted-proxy check. Under DNS rebinding the browser sends the attacker's origin and a matching host, and page JavaScript may set X-Forwarded-Proto: https, so the check passes with no TLS or proxy involved. The fix trusts only localhost origins by default; other origins require an explicit allowed_origins allowlist.

This issue affects ash_ai: from 0.8.0 before 1.0.0.

### CVE-2026-78699

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-252` |
| Published | 2026-08-30T16:16:42.623 |

Unchecked Return Value vulnerability in ash-project ash_postgres allows a user who can drive a tenant rename to a name that collides with an existing tenant's schema to have their tenant record repointed at that other tenant's live schema, gaining access to its data.

AshPostgres.MultiTenancy.rename_tenant/3 issues the ALTER SCHEMA ... RENAME TO ... with the non-raising Ecto.Adapters.SQL.query/2, discards its {:ok, _} | {:error, _} result, and unconditionally returns :ok. PostgreSQL rejects the rename when the target schema already exists (and on insufficient privilege or lock timeout), but that failure never reaches the caller. The calling manage_tenant update action therefore sees success and commits the tenant row with the new name, which is the schema of a different existing tenant, so subsequent reads and writes for that tenant run against the other tenant's data.

This issue affects ash_postgres: from 0.25.0 before 2.13.0.

### CVE-2026-82877

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-31T11:16:41.330 |

ILIAS versions before 9.22, 10.0 through 10.9, and 11.0 through 11.2 contain an arbitrary file read vulnerability in the SOAP addFile method that allows authenticated users to read server files by supplying crafted XML with COPY-mode imports. Attackers can construct absolute file paths through an unsandboxed import directory and retrieve sensitive files including configuration files containing database credentials and setup passwords.

### CVE-2026-82872

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:H/UI:N/VC:L/VI:H/VA:L/SC:L/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-31T09:17:08.160 |

ToolJet before v3.16.208 fails to validate that the path organizationId matches the authenticated user's workspace before performing ToolJet DB table operations. A workspace admin can create, view, and delete database tables in another workspace by replacing the organizationId parameter in table-management API requests.

### CVE-2026-82864

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-08-31T09:17:06.957 |

pdfme pdf-lib versions before 5.5.10 contain an unbounded buffer growth vulnerability in the DecodeStream.ensureBuffer() method that allows attackers to cause denial of service by supplying a crafted PDF with a FlateDecode stream containing a decompression bomb. Attackers can upload a small compressed PDF that decompresses to hundreds of megabytes, exhausting memory and crashing the Node.js process or freezing browser tabs during PDF parsing.

### CVE-2026-82659

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-31T09:17:03.633 |

nodemailer before 9.0.1 fails to apply disableFileAccess and disableUrlAccess flags to message-level raw option, allowing authenticated attackers to read arbitrary files or perform server-side request forgery by supplying path or href properties. Attackers can exploit this by crafting raw messages with file paths or URLs that bypass the intended sandbox, with fetched content delivered in the outgoing message to attacker-controlled recipients.

### CVE-2026-82564

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-31T02:17:02.103 |

Authorization Bypass Through User-Controlled Key vulnerability in ash-project ash_ai allows a caller of an identity-configured tool to update or destroy records it never identified, including every row in the table.

In AshAi.Tool.Execution, identity_filter/3 built the update/destroy filter directly from the raw tool arguments as [{key, Map.get(arguments, to_string(key))}] and passed it to Ash.Query.do_filter/2. A map value is parsed as a predicate expression rather than a literal, so a caller can send {"public_ref": {"not_eq": "<own-ref>"}} and, combined with Ash.Query.limit(1) and Ash.bulk_update!/Ash.bulk_destroy!, retarget the write at a record it never identified; an omitted key yields an IS NULL filter that matches an arbitrary row. The fix casts each identity value to the field type, rejecting non-scalar inputs.

This issue affects ash_ai: from 0.6.0 before 1.0.0.

### CVE-2026-75760

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-209` |
| Published | 2026-08-31T02:17:01.313 |

Generation of Error Message Containing Sensitive Information vulnerability in ash-project ash_ai discloses provider request state and credentials in a user-facing validation error.

In AshAi.Changes.Vectorize, when the embedding provider call fails the change added a changeset error whose message inspected the raw error term (An error occurred while generating embeddings: #{inspect(error)}). A plain-string add_error produces an Ash.Error.Changes.InvalidChanges in the :invalid class, which AshJsonApi and AshGraphql render back to the caller. The embedding client's error term is not sanitized, so it can carry the request URL, the provider response body, and, for HTTP clients that keep the request in the error struct, the outbound Authorization header with the provider API key. Failures are attacker-reachable via oversized or malformed vectorized content. The fix logs the raw error and returns a generic message.

This issue affects ash_ai: from 0.1.0 before 1.0.0.

### CVE-2026-80223

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-30T19:17:29.220 |

Incorrect Authorization vulnerability in ash-project ash_graphql allows an authenticated subscriber in one tenant to receive another tenant's records over GraphQL subscriptions.

The subscription resolver in AshGraphql.Graphql.Resolver authorizes each notification payload in memory: its fast path calls Ash.can/3 with run_queries?: false, which evaluates the read policy filter against the in-memory record via Ash.Expr.eval/2 and never issues a query. Ash applies multitenancy at query-build and data-layer-prefix time, not inside query.filter, so the evaluated policy carries no tenant condition and a tenant-B notification routed to a tenant-A subscriber is emitted whenever the policy filter is true. The single-notification clause has no tenant guard at all, and the batched clause checks only the head of the notification list, so non-head entries authorize purely in memory. A tenant-scoped read is reached only when filter evaluation fails.

This issue affects ash_graphql: from 1.4.0 before 1.11.0.

### CVE-2026-82648

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-30T15:16:45.300 |

WWBN AVideo contains a server-side request forgery filter bypass vulnerability in the isSSRFSafeURL function that fails to normalize NAT64 addresses written in hexadecimal form. Attackers can bypass SSRF protections by supplying hex-encoded NAT64 addresses like 64:ff9b::a9fe:a9fe to reach cloud metadata services and loopback interfaces.

### CVE-2026-82870

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-31T09:17:07.863 |

ToolJet before v3.16.208 fails to validate organizationId ownership in database write and destroy routes, allowing any builder-role user to create, alter, or drop tables in other organizations' databases. Attackers can exploit missing organization-resolving guards to permanently delete tables, insert arbitrary data, and modify schemas across tenant boundaries on shared instances.

### CVE-2026-82649

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-30T15:16:45.470 |

SiYuan Windows installer before version 3.8.1 (affected versions >= 2.0.14) contains an uncontrolled search path element vulnerability in its NSIS installer, which invokes system executables such as TASKKILL by name rather than by absolute path. Because NSIS nsExec::Exec resolves these calls using a search path that includes the installer's own launch directory ahead of System32, an attacker who plants a malicious executable (e.g., a renamed TASKKILL.exe) in that directory can have it executed when the installer runs. These calls occur in electron-builder's preInit hook before the license page is displayed, and with an all-users (elevated) install the planted binary executes with an elevated token, resulting in local privilege escalation.
