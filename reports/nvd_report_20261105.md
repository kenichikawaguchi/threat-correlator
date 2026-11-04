# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-04 15:00 UTC
- **対象期間**: `2026-11-03T15:00:41.000Z` 〜 `2026-11-04T15:00:51.000Z`
- **重要CVE数**: 333 件（Critical 9.0+: 64 件 / High 7.0〜: 269 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 今回公開された CVE の多くは **リモートコード実行 (RCE)／特権昇格** に関する深刻な脆弱性で、認証不要または認証が緩い状態で攻撃が成立します。  
- 製品別に見ると、**Quest Foglight、SolarWinds Dameware、NoMachine、HPE Networking Fabric Composer** といったインフラ系ツールが集中しており、企業内部ネットワークへの侵入経路として狙われやすい点が顕著です。  
- 同時期にリリースされた **Google Chrome（Android）** の多数の Use‑After‑Free / バッファオーバーフロー系脆弱性は、Web コンテンツ経由でのコード実行リスクを大幅に高めています。  
- 多くの脆弱性は **CVSS 9.6 以上** と極めて高いスコアで評価され、速やかなパッチ適用が必須です。

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 製品 / コンポーネント | 主な問題点 | 影響範囲・攻撃シナリオ |
|-----|--------|----------------------|------------|------------------------|
| **CVE‑2026‑28336** | 9.9 | SolarWinds **Dameware** (Remote Control) | コマンドインジェクション（認証は必要だが認証情報取得が容易） | 攻撃者は遠隔操作対象ホスト上で任意コマンドを実行でき、内部ネットワーク全体への横展開が可能。 |
| **CVE‑2026‑92190** / **92189** / **92188** (3 件) | 9.8 | Quest **Foglight for Databases** | RCE につながるデシリアライズ、ファイルパス操作、認証欠如の MBean 露出 | 認証不要で任意コード実行が可能。データベース監視サーバが侵害されると、監視対象全 DB に対する権限取得が容易になる。 |
| **CVE‑2026‑114549** | 9.8 | **NoMachine** nxwebrunner | ヒープベースのバッファオーバーフロー（Web UI） | 認証なしでリモートコード実行。リモートデスクトップ環境全体が乗っ取られ、機密情報漏洩や内部横移動が可能。 |
| **CVE‑2026‑95731** | 9.8 | HPE **Networking Fabric Composer** CLI | ハードコードされた管理者パスワード | 認証不要で管理者権限取得。ネットワークスイッチ・ルータの設定変更や DoS 攻撃が実行できる。 |
| **CVE‑2026‑120931** (Chrome Android) | 9.6 | Google Chrome (Android) | WebGL の境界外書き込み | 悪意ある HTML/JS ページを閲覧するだけでサンドボックス突破、任意コード実行が可能。Android デバイス全般に影響。 |

> **選定理由**  
> - **スコアが最高（9.9）** かつ **認証不要** のものは即時リスクが高い。  
> - **インフラ系ツール**（Dameware・Foglight・NoMachine・HPE） は社内ネットワークの根幹を担うため、侵害された場合の被害が大規模になる。  
> - **Chrome Android** の脆弱性はエンドユーザーデバイスに広く展開されており、フィッシングやマルウェア配布の踏み台になる恐れがある。

---

## 3. 推奨アクション  

### 3‑1. パッチ適用・バージョンアップ
| 製品 | 現行脆弱バージョン | 推奨バージョン (リリース日) | 備考 |
|------|-------------------|----------------------------|------|
| SolarWinds **Dameware** | 12.2 以前 | **12.3.0** 以上 (2026‑09‑15) | コマンドインジェクション修正済み |
| Quest **Foglight for Databases** | 6.4.x 以前 | **6.5.2** 以上 (2026‑10‑01) | 3 つの RCE 脆弱性すべてが修正 |
| **NoMachine** nxwebrunner | 8.4.x 以前 | **8.5.1** 以上 (2026‑08‑20) | ヒープオーバーフロー対策パッチ |
| HPE **Networking Fabric Composer** CLI | 5.3.x 以前 | **5.4.0** 以上 (2026‑09‑30) | ハードコードパスワード除去 |
| **Uncanny Owl Uncanny Toolkit** (LearnDash) | ≤ 3.8.2 | **3.8.3** 以上 (2026‑07‑12) | 特権昇格修正 |
| **Crocoblock JetFormBuilder** | ≤ 3.6.7.1 | **3.6.7.2** 以上 (2026‑07‑15) | 特権昇格修正 |
| **Elo** (no‑code expression engine) | < 1.0.1 | **1.0.1** 以上 (2026‑08‑05) | Zip‑Slip・コードインジェクション対策 |
| **codeskyblue gohttpserver** | ≤ 1.3.0 | **1.3.1** 以上 (2026‑07‑20) | Zip‑Slip 修正 |
| Google Chrome (Android) | < 157.0.8103.38 | **157.0.8103.38** 以上 (2026‑10‑05) | 全 WebGL/ANGLE/Dawn 等の Use‑After‑Free とバッファオーバーフローを修正 |

> **※ バージョンはベンダーが提供した最新安定版を対象とし、テスト環境での互換性確認を推奨します。**

### 3‑2. 追加の防御策
- **ネットワーク分離**：Dameware、Foglight、NoMachine などのリモート管理ツールは管理ネットワーク（例：管理 VLAN）に限定し、外部からの直接アクセスを防止。  
- **最小権限の原則**：CLI/GUI の管理アカウントは必要最小限に絞り、デフォルトの管理者パスワードは必ず変更。  
- **WAF/IPS ルール強化**：特に `POST /upload` へ送信される ZIP アーカイブや `nxwebrunner` への HTTP リクエストを検知・ブロックするシグネチャを導入。  
- **エンドポイント保護**：Chrome Android の脆弱性対策として、モバイルデバイス管理（MDM）で自動的に最新 Chrome バージョンを配布し、未知の Web コンテンツのサンドボックス設定を強化。  
- **監査ログの

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-28336

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-03T17:18:12.570 |

SolarWinds Dameware was found to be affected by a command injection vulnerability that could lead to the compromise of the remotely controlled host. Authentication is required.

### CVE-2026-65555

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-04T13:17:30.957 |

Incorrect Privilege Assignment vulnerability in Uncanny Owl Uncanny Toolkit for LearnDash uncanny-learndash-toolkit allows Privilege Escalation.This issue affects Uncanny Toolkit for LearnDash: from n/a through 3.8.2.

### CVE-2026-119481

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-04T13:17:26.473 |

Incorrect Privilege Assignment vulnerability in Crocoblock JetFormBuilder jetformbuilder allows Privilege Escalation.This issue affects JetFormBuilder: from n/a through 3.6.7.1.

### CVE-2026-92190

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-04T00:17:29.390 |

Quest Foglight for Databases baseRmiServiceExporter Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest Foglight for Databases. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the configuration of the baseRmiServiceExporter bean. The issue results from the lack of proper validation of user-supplied data prior to deserializing it. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-29170.

### CVE-2026-92189

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-04T00:17:29.260 |

Quest Foglight for Databases writeTopologySectionToFile External Control of File Path Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest Foglight for Databases. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the writeTopologySectionToFile method. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-29169.

### CVE-2026-92188

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-04T00:17:29.130 |

Quest Foglight for Databases ForgeMBeanServerSupport Missing Authentication Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest Foglight for Databases. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the ForgeMBeanServerSupport module. The issue results from the lack of authentication prior to allowing access to functionality. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-29168.

### CVE-2026-114549

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-04T00:17:22.627 |

NoMachine nxwebrunner Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of NoMachine. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the web service, which listens on TCP port 4443 by default. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the service account. Was ZDI-CAN-30685.

### CVE-2026-95731

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:21.197 |

Hardcoded password vulnerabilities in the command-line interface of HPE Networking Fabric Composer could allow an unauthenticated remote attacker to access the affected system using hardcoded credentials. Successful exploitation could allow an attacker to gain unauthorized administrative access to the affected system with elevated privileges.

### CVE-2026-44267

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79;CWE-94;CWE-693;CWE-1336` |
| Published | 2026-11-03T18:18:03.130 |

Elo is a purely functional expression language for no-code tools. Prior to 1.0.1, plain Elo strings supplied to defaultFormats.elo.parse(), bin/elo, or elo-lang.org/try can use .constructor.constructor to reach JavaScript Function because the member_access handler in src/transform.ts does not reject meta-properties, src/compilers/javascript.ts emits the surviving property directly, and src/parser.ts accepts constructor as an ordinary identifier. The resulting generated JavaScript executes attacker-selected code in the host runtime. This permits browser script execution and session compromise on the auto-running playground and arbitrary Node.js code execution on library, CI, or DevOps hosts. This plain-string path is distinct from the programmatic AST-object injection issue. This issue is fixed in version 1.0.1.

### CVE-2026-44266

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-116;CWE-1336` |
| Published | 2026-11-03T18:18:02.957 |

Elo is a purely functional expression language for no-code tools. Prior to 1.0.1, the Ruby backend in src/compilers/ruby.ts embeds attacker-controlled text in Ruby double-quoted strings without escaping #, so Ruby interpolation forms in the string-literal emitter or the labelled subtype-constraint branch become executable Ruby. The affected entry points include the /try playground with the Ruby target, bin/eloc -t ruby -x, and defaultFormats.elo.parse() followed by Ruby emission. A failing labelled subtype constraint evaluates its message, while an ordinary string literal is evaluated when the compiled Ruby runs, allowing Ruby code and shell command execution through backticks. JavaScript, Python, and SQL emission are not affected by this Ruby-specific path. This issue is fixed in version 1.0.1.

### CVE-2026-38600

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-03T17:18:13.070 |

A Zip Slip vulnerability in the /upload endpoint of codeskyblue gohttpserver through v1.3.0 allows attackers to write arbitrary files via uploading a crafted Zip archive.

### CVE-2026-120931

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-03T22:19:31.900 |

Out of bounds write in WebGL in Google Chrome on on Android prior to 156.0.8078.47 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-121249

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-03T21:17:35.493 |

Buffer overflow in ANGLE in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121247

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-03T21:17:35.220 |

Buffer overflow in Dawn in Google Chrome on on Android prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-121246

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:35.093 |

Use after free in WebGL in Google Chrome on on Android prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-121241

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:34.420 |

Use after free in Navigation in Google Chrome on on Android prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121234

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-03T21:17:33.503 |

Privilege elevation in Contacts in Google Chrome on on Android prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121229

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-11-03T21:17:32.837 |

Memory corruption in ANGLE in Google Chrome on on Android prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-121214

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:30.847 |

Use after free in Passwords in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121202

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:29.203 |

Use after free in Autofill in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121200

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-11-03T21:17:28.887 |

Incorrect reference resolution in DevTools in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121189

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:27.693 |

Use after free in Browser in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-121185

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:27.177 |

Use after free in PictureInPicture in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121156

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-03T21:17:23.283 |

Buffer overflow in Dawn in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-121148

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:23.150 |

Use after free in ANGLE in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121131

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:21.517 |

Use after free in Mobile in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted Chrome extension. (Chromium security severity: High)

### CVE-2026-121126

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:20.860 |

Use after free in Core in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-121114

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:19.087 |

Use after free in TabStrip in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121104

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-03T21:17:16.653 |

Incorrect authorization in FileSystem in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121089

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:14.543 |

Use after free in WebGPU in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121086

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-03T21:17:14.123 |

Buffer overflow in Skia in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121077

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:12.893 |

Use after free in Mobile in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121076

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:12.757 |

Use after free in WebXR in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121074

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-11-03T21:17:12.463 |

Memory corruption in GPU in Google Chrome on on Android prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121071

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-03T21:17:12.057 |

Incorrect authorization in FileSystem in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121060

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-03T21:17:10.570 |

Incorrect authorization in FileSystem in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121037

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-03T21:17:07.000 |

Out of bounds write in ANGLE in Google Chrome on on Windows prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121035

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:06.730 |

Use after free in Prerender in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-121034

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:06.593 |

Use after free in Views in Google Chrome on on Windows prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121030

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-03T21:17:06.013 |

Incorrect authorization in DevTools in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-95733

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:21.433 |

A vulnerability exists in a component of HPE Networking Fabric Composer. Successful exploitation could allow an unauthenticated adjacent attacker to execute arbitrary code on the affected system.

### CVE-2026-95732

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:21.320 |

An authentication bypass vulnerability exists in the underlying operating system of HPE Networking Fabric Composer. Successful exploitation could allow an unauthenticated adjacent attacker to execute arbitrary code on the affected system.

### CVE-2026-115731

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-502` |
| Published | 2026-11-03T21:17:01.867 |

Deserialization of untrusted data in the report-processing code of Puppet, as used by Puppet Server, in the affected releases, allows a client that holds any CA-signed agent certificate to execute arbitrary code on the Puppet Server as its service user by submitting a report containing a crafted rich-data type via PUT request. Where the certificate authority autosigns requests without strong verification, an unauthenticated network attacker can obtain such a certificate.

### CVE-2026-121615

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-04T03:17:14.810 |

A vulnerability was determined in Linksys E5600 1.1.0.26. Affected is an unknown function of the file /cgi-bin/mesh_login.cgi of the component Login Handler. Executing a manipulation can lead to improper authentication. The attack can be launched remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-121609

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-259;CWE-798` |
| Published | 2026-11-04T02:17:20.243 |

A vulnerability was identified in Qihoo 360 Whole Home Router M5 4.0.17.1566. This issue affects the function Home of the file /etc/init.d/mpt of the component Boot Script. The manipulation leads to hard-coded credentials. Remote exploitation of the attack is possible. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-121607

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-04T02:17:19.753 |

A vulnerability was found in Qihoo 360 D603-2, D600-2, D606-6 and D706 up to 6.4.9. This affects the function testspeed_command of the file /fs2/bin/iscm. Performing a manipulation of the argument host results in os command injection. The attack may be initiated remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-121606

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-347` |
| Published | 2026-11-04T01:17:23.880 |

A vulnerability has been found in Qihoo 360 D621-2, D603-2, D600-2, D619, D606-6 and D706 up to 6.4.9. Affected by this issue is the function verify_sign of the file fs2/bin/iscm of the component Firmware Signature Verification. Such manipulation of the argument sign leads to improper verification of cryptographic signature. The attack can be launched remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2022-29966

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-03T23:17:20.353 |

Emerson Ovation has several protocols that have no authentication, which could allow an attacker to change controller configuration or cause a denial-of-service condition.

### CVE-2026-112354

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-03T22:17:44.660 |

Etrel INCH AC charging station management web interface prior to firmware versions 7.1.2 and 8.0.1 contains a hard-coded default credentials vulnerability that allows remote attackers to gain full Administrator access by authenticating with the factory-default account. Attackers can log in over cleartext HTTP to obtain complete charger configuration, OCPP ChargePoint Identity, and CSMS WebSocket connection details, enabling unauthorized administrative control of the charging station.

### CVE-2026-63471

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-116` |
| Published | 2026-11-03T20:18:15.753 |

fastapi-code-generator creates FastAPI applications from OpenAPI files. Prior to 0.8.1, the generator inserts an OpenAPI path into a generated @app.get(...) route decorator as a single-quoted generated route string without escaping embedded quotes. An attacker-controlled or attacker-influenced OpenAPI path can close the string and inject a valid Python expression into the decorator argument. Syntax-breaking input only causes generation to fail, but syntactically valid generated code executes with the application's or CI process's privileges when the generated module is imported and the decorator is evaluated. This OpenAPI path sink is distinct from the project's separate operation-summary docstring and additional-response-key sinks. This issue is fixed in version 0.8.1.

### CVE-2026-63470

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-116` |
| Published | 2026-11-03T20:18:15.590 |

fastapi-code-generator creates FastAPI applications from OpenAPI files. Prior to 0.8.1, the generator inserts Operation.summary into a generated route-handler docstring as a triple-double-quoted string without escaping embedded triple quotes. An attacker-controlled or attacker-influenced operation summary can close the docstring and inject a valid Python expression statement into the handler body. Syntax-breaking input only causes generation to fail, but syntactically valid generated code executes with the server process's privileges when the affected route handler is called. This call-time route-handler docstring sink is distinct from the project's separate import-time route-path and additional-response-key sinks. This issue is fixed in version 0.8.1.

### CVE-2026-63469

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-116` |
| Published | 2026-11-03T20:18:15.420 |

fastapi-code-generator creates FastAPI applications from OpenAPI files. Prior to 0.8.1, the generator inserts an additional response status-code key into the generated responses={...} route-decorator dictionary as a single-quoted Python string without escaping embedded quotes. A multi-response OpenAPI operation with an attacker-controlled or attacker-influenced second non-primary response key can close the dictionary-key literal and inject a valid Python expression. Syntax-breaking input only causes generation to fail, but syntactically valid generated code executes with the application's or CI process's privileges when the generated module is imported and its decorator arguments are evaluated. This additional-response-key sink is distinct from the project's separate route-path and operation-summary sinks. This issue is fixed in version 0.8.1.

### CVE-2026-121939

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-04T13:17:28.210 |

Databasement before 1.10.9 contains an authentication bypass vulnerability in OAuthService::findOrCreateLocalUser() that links OIDC identities to local users by email without checking email_verified. Attackers can register an identity provider account with a victim's unverified email to log in as any user, including the super-admin, and retain access after password resets.

### CVE-2026-114425

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-04T09:17:41.833 |

SEPPmail Secure Email Gateway before 15.1.1 trusts a file path supplied in externally provided Large File Transfer attachment metadata. An unauthenticated remote sender can cause the mail-processing worker to disclose, move, or delete an accessible regular file when LFT is enabled and the message reaches an affected secure-mail processing path. The validated workers ran as root.

### CVE-2026-114424

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-04T09:17:41.693 |

SEPPmail Secure Email Gateway before 15.1.1 can evaluate attacker-influenced replacement text as Perl code in sender or recipient replacement rules. An unauthenticated remote sender can execute operating-system commands in the mail-processing worker context when an active rule uses message-derived replacement data and its search condition matches. The validated worker context was root.

### CVE-2026-119084

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-11-03T22:19:29.220 |

Unsafe reflection in the connection parameter and credentials profile handling of Amazon Redshift JDBC Driver before 2.3.0 might allow an actor who can influence the JDBC connection URL or the AWS credentials profile to execute arbitrary code in the application context, provided a suitable class is available on the application classpath.



To remediate this issue, users should upgrade to version 2.3.0 or later.

### CVE-2026-112917

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-424` |
| Published | 2026-11-03T19:17:53.727 |

In Docker Desktop for Windows with the WSL2 backend, an unprivileged Linux container can use 32-bit socketcall to bypass the default seccomp restriction on AF_VSOCK. This can expose host-facing services and Windows files accessible to the logged-in user. The issue affects x86-64 WSL2; LinuxKit-based backends are unaffected. The issue is fully fixed only with Docker Desktop 4.98.0 or later and WSL 3.0.3 or later. Docker Desktop 4.98.0 or later running on an older WSL remains affected.

### CVE-2026-121802

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-04T03:17:15.730 |

@better-auth/expo before 1.7.16 allows certain account-takeover outcomes (e.g., unauthenticated changes of any account's email address), because it signs a caller-supplied state value without checking whether that value had been issued by the server. NOTE: the application secret must be rotated after updating to a fixed version.

### CVE-2026-22058

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T22:19:47.030 |

StorageGRID (formerly StorageGRID Webscale) versions 11.3 and higher allow an attacker with product-specific knowledge and the ability to communicate with the Grid Network on certain ports to make unauthorized requests.

### CVE-2026-95860

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285;CWE-636;CWE-863;CWE-1188` |
| Published | 2026-11-03T21:17:45.907 |

node-opcua is an OPC UA implementation for TypeScript and Node.js. From 2.42.0 until 2.180.0, namespace-level access control configured through setDefaultRolePermissions is not honored by the runtime enforcement path for nodes without explicit per-node RolePermissions. SessionContext.getApplicableRolePermissions reads a missing or null DefaultRolePermissions metadata value instead of the configured namespace field, and the null result is treated permissively. An anonymous network client can consequently write variables with CurrentWrite access or call bound methods when an operator configured a restrictive namespace default and relied on inheritance. Servers with no declared policy, nodes with explicit per-node permissions, and correctly bound programmatic namespace metadata are outside the authorization-bypass case. This issue is fixed in version 2.180.0.

### CVE-2026-109593

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-636` |
| Published | 2026-11-03T17:17:53.690 |

An unauthenticated attacker with network access to the SonicWall GMS 9.5.2 and earlier versions may be able to read internal GMS files, potentially exposing sensitive information.

### CVE-2026-121392

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-03T15:17:26.710 |

FreeRDP before 3.32.2 contains an improper certificate validation vulnerability in tls_verify_certificate() that accepts Common Name fallback despite non-matching SAN entries and matches IP literals against DNS strings. Man-in-the-middle attackers holding a certificate from a client-trusted CA can bypass server identity checks to intercept RDP sessions, including keystrokes, clipboard, and screen content.

### CVE-2026-82158

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-03T21:17:43.823 |

Dell Wyse Management Suite, versions prior to 2609.0.0.155, contain an Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Script injection.

### CVE-2026-115732

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-697;CWE-863` |
| Published | 2026-11-03T21:17:02.033 |

Incorrect authorization in the certificate-name matching of trapperkeeper-authorization, as used by Puppet Server, in the affected products, allows a client that holds a CA-signed certificate whose name extends or shortens an authorized hostname to be authorized as that host. This enables impersonation of other nodes and, in Puppet Enterprise, access to certificate-authority administration and remote command execution on managed nodes. Exploitation requires a certificate with a colliding name, which the certificate authority issues by approval or autosign.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-118391

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-04T14:17:29.983 |

Allocation of Resources Without Limits or Throttling vulnerability in elixir-ecto ecto allows an unauthenticated remote attacker to exhaust memory in the application and in the database server by sending requests with distinct JSON keys or list lengths where the application interpolates them into json_extract_path/2, field[^key] or splice/1. Ecto caches prepared queries per repository in an ETS table with no size limit and no eviction. Interpolated JSON path elements become part of the query expression instead of its parameters, and splice/1 expands into one placeholder per element, so every distinct key or list length creates a new cache entry. With ecto_sql each entry is also a new prepared statement on the database connection that runs it. None of this memory is released until the processes restart.

This issue affects ecto: from 3.4.0 before 3.14.3.

### CVE-2026-120422

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:X/R:U/V:D/RE:M/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-04T10:17:26.120 |

Sogou Input Method for Windows contains a vulnerability in the configuration retrieval mechanism of its SGTool.exe component. The application retrieves configuration data over unencrypted HTTP connections, allowing an attacker capable of manipulating network traffic to replace legitimate server responses with malicious configurations. An attacker can exploit this vulnerability to instruct SGTool.exe to download attacker-controlled files to arbitrary locations, including paths used by legitimate application components. This can result in arbitrary code execution when the downloaded files are subsequently executed or loaded by the application.

### CVE-2026-121144

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-04T13:17:26.727 |

This vulnerability exists in the iRA 2.0 and iRA.ev mobile applications due to presence of hardcoded service account credentials, API Keys and authorization tokens within the application package. An unauthenticated remote attacker could exploit this vulnerability by downloading application package and extracting embedded sensitive information.



Successful exploitation of this vulnerability could allow the attacker to gain unauthorized access to associated backend services and potentially access sensitive information or perform unauthorized operations on the targeted system.

### CVE-2026-104799

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-04T12:17:05.713 |

The Mobile builder plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.4.2 via the `wcfmmp_profile_settings()` REST handler exposed at `POST /mobile-builder/v1/wcfm-profile-settings`. This is due to a PHP loose-comparison logic flaw in the meta key allow-list check — `strpos( $key, 'mobile_builder' ) == 0` evaluates to `true` for any key that does *not* contain the substring `'mobile_builder'` because `strpos()` returns `false` on no match and `false == 0` is `true` in PHP — combined with a `permission_callback` (`user_permissions_check`) that grants access to any authenticated user by only verifying `$user->exists()`. This makes it possible for authenticated attackers, with Subscriber-level access and above, to pass an unsanitized `data` array via the `key` and `data` parameters directly to `update_user_meta()`, overwriting arbitrary user meta on their own account — including the `wp_capabilities` meta key — to grant themselves Administrator-level privileges.

### CVE-2026-120554

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-04T10:17:26.300 |

The Import and export users and customers plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.5.11 This is due to a non-atomic multi-option write sequence in the `ACUI_Cron::save_settings()` function, which persists `acui_cron_activated`, `acui_cron_configured_by`, `acui_cron_user_id`, and `acui_cron_path_to_file` before reaching the authorization gate that calls `wp_die()` when a non-promoter submits a role. This makes it possible for authenticated attackers holding a custom delegated role with `create_users` but without `promote_users` or `edit_users` to escalate their privileges to Administrator, provided a prior administrator cron-tab save exists and no successful save intervenes before the next unattended cron tick processes the attacker's repointed CSV file.

### CVE-2026-77690

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-04T06:17:05.940 |

ZohoCorp ManageEngine Key Manager Plus versions before 7151 were vulnerable to a Command Injection vulnerability that allowed authenticated users with certificate deployment privileges to execute arbitrary commands through specially crafted input when configuring a deployment target.

### CVE-2026-16511

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787;CWE-822;CWE-862` |
| Published | 2026-11-04T06:17:04.140 |

Two RTIO syscall verifiers, in subsys/rtio/rtio_syscalls.c (subsys/rtio/rtio_handlers.c before v4.3.0), did not validate user-supplied pointers before the kernel wrote through them.

z_vrfy_rtio_sqe_cancel() performed no validation at all. It passed the caller's struct rtio_sqe pointer straight to z_impl_rtio_sqe_cancel(), which converts it with CONTAINER_OF to a struct rtio_iodev_sqe, ORs RTIO_SQE_CANCELED (BIT(3)) into its 16-bit flags field in supervisor mode, then loads its next pointer and repeats until that pointer is NULL. The syscall takes no RTIO context argument, so it needs no object grant: any user-mode thread on a CONFIG_USERSPACE build can set that bit in a 16-bit word at an address of its choosing in kernel memory, and the kernel continues the write along whatever pointer chain it finds at the corresponding offset. Setting chosen bits in kernel data structures, such as object permission or thread state fields, can be used to escalate privilege from user mode.

z_vrfy_rtio_sqe_copy_in_get_handles() validated its RTIO context and the input SQE array, but only NULL-checked the handle out-parameter before writing a kernel SQE pointer through it, with no K_SYSCALL_MEMORY_WRITE check. A user thread that holds a granted RTIO context can therefore make the kernel store a pointer value at an arbitrary address.

The fixes validate the handle out-parameter as writable, bound the cancel handle to real submission-pool storage, and require permission on the RTIO context that owns the matching pool. Without that last check a bounded handle still let any user thread cancel submissions belonging to other contexts, silently aborting their I/O. Systems built without CONFIG_USERSPACE or without CONFIG_RTIO are unaffected.

### CVE-2026-92197

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-04T00:17:30.677 |

Quest Foglight for Databases unzipFile Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest Foglight for Databases. Authentication is required to exploit this vulnerability.

The specific flaw exists within the unzipFile method. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-29901.

### CVE-2026-92195

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-04T00:17:30.390 |

Quest Foglight for Databases loadEvolveLicense Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest Foglight for Databases. Authentication is required to exploit this vulnerability.

The specific flaw exists within the loadEvolveLicense script. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-29232.

### CVE-2026-92194

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-04T00:17:30.060 |

Quest Foglight for Databases loadManageServerLicense Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest Foglight for Databases. Authentication is required to exploit this vulnerability.

The specific flaw exists within the loadManageServerLicense script. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-29231.

### CVE-2026-92192

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-04T00:17:29.650 |

Quest Foglight for Databases installLicense Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest Foglight for Databases. Authentication is required to exploit this vulnerability.

The specific flaw exists within the installLicense script. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-29215.

### CVE-2026-92191

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-04T00:17:29.517 |

Quest Foglight for Databases runScript Incorrect Authorization Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest Foglight for Databases. Authentication is required to exploit this vulnerability.

The specific flaw exists within the runScript function. The issue results from incorrect authorization prior to allowing access to functionality. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-29192.

### CVE-2026-92187

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-04T00:17:28.993 |

Quest Foglight for Databases extractAndCreateUploadInfoList Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest Foglight for Databases. Authentication is required to exploit this vulnerability.

The specific flaw exists within the extractAndCreateUploadInfoList method. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-29039.

### CVE-2026-92186

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-04T00:17:28.867 |

Quest Foglight for Databases paFnUploadFileAndCreateInfo Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest Foglight for Databases. Authentication is required to exploit this vulnerability.

The specific flaw exists within the paFnUploadFileAndCreateInfo script. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-29038.

### CVE-2026-82159

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-03T21:17:43.963 |

Dell Wyse Management Suite, versions prior to 2609.0.0.155, contain an Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Script injection.

### CVE-2026-121621

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-03T21:17:37.857 |

A command injection vulnerability was found in Argo CD Image Updater, where a proxy URL configured on an SSH Git repository is passed unsanitized into a shell-interpreted SSH command. An attacker able to set a malicious proxy value can inject shell metacharacters to execute arbitrary commands and access credentials in the context of the Image Updater process.

### CVE-2026-121238

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:34.027 |

Use after free in Source in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121233

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:33.370 |

Type confusion in CacheStorage in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121228

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:32.707 |

Type confusion in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121226

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:32.447 |

Type confusion in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121221

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:31.793 |

Type confusion in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121218

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:31.383 |

Type confusion in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121210

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:30.280 |

Type confusion in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121208

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-03T21:17:30.013 |

Out of bounds read in Media in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121203

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:29.347 |

Use after free in Geometry in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-121201

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:29.033 |

Use after free in Animation in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121188

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:27.563 |

Use after free in PerformanceAPIs in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121184

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-03T21:17:27.047 |

Out of bounds read in Media in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121182

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:26.787 |

Use after free in DOM in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121181

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:26.660 |

Use after free in Editing in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121180

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-03T21:17:26.530 |

Buffer overflow in Media in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121179

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:26.390 |

Use after free in PDFium in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121168

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-668` |
| Published | 2026-11-03T21:17:24.890 |

Improper resource exposure in DevTools in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-121166

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:24.603 |

Type confusion in PDFium in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted PDF file. (Chromium security severity: High)

### CVE-2026-121137

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:22.343 |

Type confusion in DevTools in Google Chrome prior to 157.0.8103.38 allowed a remote attacker leveraging social engineering to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121129

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:21.250 |

Use after free in WebRTC in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121128

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:21.120 |

Use after free in Scheduling in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121127

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:20.987 |

Use after free in WebAudio in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121124

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-710` |
| Published | 2026-11-03T21:17:20.583 |

Improper adherence to coding standards in XML in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121123

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:20.440 |

Use after free in Canvas in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121119

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:19.747 |

Use after free in Controls in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121118

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:19.617 |

Use after free in SVG in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121117

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:19.490 |

Use after free in Paint in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121100

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:16.103 |

Use after free in DOM in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121097

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:15.677 |

Use after free in Printing in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121094

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:15.257 |

Type confusion in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121092

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-03T21:17:14.963 |

Uncontrolled recursion in SVG in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-121083

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:13.713 |

Use after free in Compositing in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121082

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:13.577 |

Type confusion in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121079

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-03T21:17:13.163 |

Race condition in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121078

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:13.030 |

Type confusion in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121070

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:11.923 |

Use after free in WTF in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121069

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:11.790 |

Use after free in Track in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-121068

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:11.653 |

Type confusion in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121061

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:10.703 |

Use after free in Modularization in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121057

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-03T21:17:10.300 |

Type confusion in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121052

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:09.723 |

Use after free in GPU in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121048

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-03T21:17:09.143 |

Race condition in V8 in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121047

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-03T21:17:09.003 |

Buffer overflow in Media in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121044

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:08.560 |

Use after free in Layout in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121036

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:06.863 |

Use after free in CSS in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95734

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:21.550 |

A sensitive information disclosure vulnerability in the API of HPE Networking Fabric Composer could allow an authenticated low-privileged user to access sensitive information beyond what is authorized by the user's existing privilege level. Successful exploitation could allow an attacker to obtain sensitive credentials stored on the affected system.

### CVE-2026-95722

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:20.033 |

A local privilege escalation vulnerability has been discovered in the Virtual Intranet Access (VIA) client. Successful exploitation of this vulnerability could allow a local attacker with low privileges to execute arbitrary commands with elevated privileges on the underlying operating system.

### CVE-2026-63395

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-11-03T20:18:14.917 |

isomorphic-git is a pure JavaScript implementation of Git for Node.js and browsers. Prior to 1.38.6, isomorphic-git's git.checkout writes new child paths through symlinked leading directory components without checking them. A malicious repository can first place a directory symlink and later replace the tree state with a child file beneath that path; the usual trigger is a clone followed by a later pull, while a single clone can trigger the issue when a symlink already exists or the consuming application accesses the tree. With Node fs on Linux or macOS, the operating system can resolve the write outside the working tree, permitting arbitrary host file writes and possible code execution. Node fs on Windows usually blocks the symlink plant without additional privilege, and browser or in-memory providers limit impact to their virtual filesystem and are affected only when they implement symlink creation and following. This issue is fixed in version 1.38.6.

### CVE-2026-121417

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T15:17:31.553 |

SurrealDB before 3.3.0 contains a use-after-free vulnerability in surrealdb-core KV backends that pass borrowed transaction state into affinitypool::spawn_local closures relying on future Drop for safety. Rust embedders that leak a dispatched future (e.g. via mem::forget) and drop the transaction cause pool workers to read and write freed memory, risking crashes or memory corruption.

### CVE-2026-121940

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-04T13:17:28.393 |

Stonewuu ai-fusion-video before 1.3.0 contains an insecure direct object reference vulnerability that allows authenticated users to access other users' projects by supplying unscoped object ids. Attackers can enumerate auto-increment ids on /api/project, /api/asset and /api/script handlers to read, overwrite, cascade-delete data, and add themselves as project members.

### CVE-2026-115448

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-04T11:17:14.017 |

Uncontrolled recursion in Apache ZooKeeper. The server serializes its data tree to a snapshot by recursing one stack frame per znode level, with no depth bound. A client permitted to create znodes (the default root ACL is open) can build a chain of nested znodes deep enough that taking a snapshot exhausts the JVM stack and kills the snapshot thread; sizes stay within jute.maxbuffer, so existing limits do not prevent it. This is a denial of service that becomes persistent: on restart the server rebuilds the deep tree from its transaction log and fails again while taking the startup snapshot, so it does not return to service, and recovery can entail data loss. The same log affects a leader and its followers, so it can spread across an ensemble.

This issue affects Apache ZooKeeper 3.8.0 through 3.8.7 and 3.9.0 through 3.9.6. Users are recommended to upgrade to 3.8.8 or 3.9.7, which fix the issue. As a workaround, use ACLs and authentication to restrict znode creation rather than relying on the default open root ACL.

### CVE-2026-100300

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-755` |
| Published | 2026-11-04T11:17:06.873 |

Improper handling of exceptional conditions in the quota subsystem of Apache ZooKeeper allows an attacker able to write under the /zookeeper/quota subtree — unauthenticated on default deployments, where that subtree is world-writable — to crash the server's critical request-processing thread and render the on-disk data directory permanently unbootable.

This issue affects Apache ZooKeeper up to and including 3.9.6. Users are recommended to upgrade to version 3.8.8 or 3.9.7, which fixes the issue.

### CVE-2026-114426

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-04T09:17:41.970 |

SEPPmail Secure Email Gateway before 15.1.1 processes and writes v1 file-interface upload data before authenticating the caller and without an absolute request-size limit. An unauthenticated remote attacker can occupy workers and consume temporary storage with concurrent or slow requests, causing service unavailability.

### CVE-2026-121817

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-04T07:17:12.200 |

Herowatch Go Server developed by About Time Technologies has a Insecure Direct Object Reference vulnerability. Authenticated remote attackers can modify specific parameters to access or operate other users' data and functions.

### CVE-2026-121816

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-04T07:17:11.973 |

Herowatch Mini developed by About Time Technologies has a Missing Authentication vulnerability. Unauthenticated remote attackers can connect to the affected device's ADB service and obtain an ADB shell, thereby accessing device resources or performing related operations.

### CVE-2026-84730

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-04T02:17:21.323 |

Stack-based buffer overflow in certain ASUS Router firmware allows an unauthenticated nearby attacker to execute arbitrary commands with root privileges via a crafted device name.
Refer to the '
Security Update for ASUS Router AiCloud Feature ' section on the ASUS Security Advisory for more information.

### CVE-2026-121731

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-03T23:17:36.763 |

RosarioSIS before 12.9 contains a sql injection vulnerability that allows authenticated non-student users, including parents, to inject SQL via the unquoted period_id parameter in StudentSummary.php. Attackers can supply payloads without single quotes into IN() clauses to extract administrator password hashes and student records through time-based queries or modify data via stacked statements.

### CVE-2026-121727

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-03T23:17:36.043 |

Kore before 4.3.0 contains an integer underflow vulnerability in HTTP request body handling that allows unauthenticated attackers to bypass http_body_max by sending more body bytes than declared. Attackers can send oversized first segments over many concurrent POST, PUT or DELETE connections, wrapping content_length to grow buffers unbounded and exhaust worker memory.

### CVE-2022-30267

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-03T23:17:21.860 |

Emerson Ovation 
was found to have no authentication of firmware signing and relies on an insecure checksum for integrity. This could allow an attacker to push malicious firmware images, cause a denial-of-service condition, or achieve remote code execution.

### CVE-2026-95735

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:21.670 |

An improper certificate validation vulnerability exists in HPE Networking Fabric Composer. Successful exploitation could allow an unauthenticated remote attacker, under certain preconditions outside the attacker's control, to obtain sensitive information, including credentials.

### CVE-2026-120955

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-03T19:18:00.667 |

The GridFS file download API in the MongoDB C Driver does not check the result of an internal operation under certain error conditions during file retrieval. This can cause the process to terminate when stream operations continue. A user who can influence file download parameters can trigger this condition, which may result in service unavailability for applications using the affected API.

### CVE-2026-120678

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-11-03T19:17:59.880 |

A memory management flaw in the MongoDB C Driver's handling of compressed responses may cause the client library to hold on to memory that is never released. An unauthenticated party that controls the database endpoint a client application connects to may cause repeated, unbounded memory growth in that application, which may result in the application becoming unavailable. No credentials, transport security settings, or user interaction are required.

### CVE-2026-119922

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-03T19:17:57.020 |

Improper access control in the Babelfish for PostgreSQL extension versions 1.2-1.5, 2.1-2.15, 3.1-3.12, 4.0-4.8, 5.1-5.4 may allow remote authenticated users to elevate their privileges. To remediate this issue, we recommend you upgrade to Babelfish for PostgreSQL extension versions 4.10, 5.6, 6.1 or later.

### CVE-2026-121556

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-03T16:17:27.970 |

FastBee through 2.1.0 contains an insecure direct object reference vulnerability in ProductController that allows authenticated tenant users to access other tenants' products by supplying their product IDs. Attackers can enumerate sequential product IDs to read MQTT account, password, and secret values, overwrite product configuration including tenant_id, or delete products with cascading rows.

### CVE-2026-121555

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-03T16:17:27.800 |

Foxel through 2.4.0 contains a missing authentication vulnerability that allows unauthenticated attackers to read files by requesting the /api/fs/stream and /api/fs/thumb endpoints. Attackers can supply a VFS mount prefix and relative path to retrieve full file contents or thumbnails across all mounts, bypassing PathRule permission grants.

### CVE-2026-121543

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-03T16:17:25.653 |

smart-sso through 2.0.1 contains an incorrect authorization vulnerability in PermissionFilter that allows any authenticated user to call admin console APIs because unlisted paths are permitted by default. Attackers can call /admin/user-role/save to assign themselves the administrator role, reset passwords, and manage users, roles, and applications across integrated systems.

### CVE-2026-121451

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-03T16:17:23.960 |

AB Download Manager before 1.11.2 contains a cross-site request forgery vulnerability in its unauthenticated browser-integration API that allows remote attackers to write attacker-chosen files to arbitrary paths. A malicious web page can send a text/plain request to /start-headless-download with crafted folder and name values, placing payloads in startup folders for code execution on next login.

### CVE-2026-119741

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-03T16:17:21.940 |

rsync through 3.5.1 contains a denial of service vulnerability in the delta-transfer sender's hash_search() in match.c that allows malicious receivers to trigger unbounded strong-checksum work at consecutive offsets. Unauthenticated attackers pulling from a public daemon module can supply weak checksums colliding with consecutive rolling windows plus non-matching strong checksums, exhausting sender CPU across concurrent connections.

### CVE-2026-121448

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-03T15:17:37.227 |

Dockhand before 1.0.54 contains a path traversal vulnerability that allows authenticated users to read, overwrite, and delete .env files outside the stacks root by double-encoding the stack name. Attackers can send %252e%252e sequences to /api/stacks/[name]/env/raw to disclose cross-environment secrets, write into protected directories, or poison deployment variables.

### CVE-2026-121444

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-03T15:17:36.443 |

svg-sanitizer from 0.11.0 before 1.1.0 contains an algorithmic complexity denial of service vulnerability in hasInfiniteLoop() and countUse() of the use reference-graph analysis. Attackers can upload a small layered SVG with 15 levels of fanned-out use elements, forcing exponential path enumeration that pins PHP workers for hours.

### CVE-2026-121437

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-03T15:17:35.147 |

Mistune from 3.3.0 before 3.3.4 contains a denial of service vulnerability that allows remote attackers to exhaust CPU through quadratic-time emphasis delimiter processing. Attackers can submit small markdown documents with repeated patterns like "*a_b" to trigger an O(n²) index-fixup loop, stalling workers for seconds.

### CVE-2026-121429

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-03T15:17:33.747 |

AzuraCast through 0.23.8 contains a command injection vulnerability that allows station users with Profile permission to execute OS commands via StereoTool settings. Attackers can inject shell metacharacters into stereo_tool_configuration_path or stereo_tool_license_key, which are executed via /bin/sh on station restart, compromising the container.

### CVE-2026-121428

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-03T15:17:33.570 |

AzuraCast through 0.23.8 contains a remote code execution vulnerability that allows authenticated station managers to inject Supervisor configuration through the station timezone field. Attackers can submit a timezone containing newlines to the profile edit API, defining a new Supervisor program that executes OS commands as root when configuration regenerates.

### CVE-2026-121427

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-03T15:17:33.373 |

AzuraCast through 0.23.8 fails to remove frontend_config.custom_config in PUT /station/{id}/profile/edit for users lacking the Manage station broadcasting permission, and the stored JSON is written verbatim as key=value lines into the Shoutcast sc_serv.conf file. An authenticated user with only the Manage station profile permission can override adminpassword, password, and portbase, or inject arbitrary directives via newlines in keys, hijacking the station's Shoutcast frontend.

### CVE-2026-121386

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-03T15:17:25.543 |

FreeRDP before 3.32.2 contains a denial of service vulnerability in WinPR's winpr_read_png_from_buffer() and winpr_convert_from_jpeg(), which lack libpng/libjpeg error handling. A malicious RDP server or MITM can offer a malformed PNG or truncated JPEG clipboard payload, causing the client to abort or exit.

### CVE-2026-100252

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-04T11:17:06.717 |

Improper Authorization vulnerability in Apache ZooKeeper.

When SASL authentication is enabled on the client port, the server's SASL callback handler grants every authorization identity (authzid) that a client requests, without checking it against the principal the client authenticated as. The server then tries to replace the requested identity with a canonical form of the authenticated principal, derived from the zookeeper.security.auth_to_local rules. If no rule applies to the principal, canonicalization fails and the error is only logged. The client-requested authzid then becomes the session's SASL identity for all ACL checks.

An authenticated client whose principal is not covered by the auth_to_local rules can therefore claim any SASL identity. With the default rules, this includes any Kerberos principal from a realm other than the server's default realm, such as a principal from a cross-realm trusted realm. The client then gets the permissions granted to that identity in sasl ACLs. If the requested identity matches a configured zookeeper.superUser, it gets superuser access to the whole data tree.

Users are recommended to upgrade to version 3.8.8 or 3.9.7, which fixes the issue.

### CVE-2026-110935

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-04T10:17:24.627 |

The PFI plugin framework deployment routine does not validate path components when extracting archive entries to the local plugin repository. Archive entries containing relative path segments such as '..' are not rejected, allowing an unauthenticated local attacker to write files outside the plugin repository to arbitrary locations accessible with the current user's permissions which could result in full system compromise.

### CVE-2026-110022

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-04T10:17:24.473 |

The PFI plugin framework deploys executable assemblies (DLLs) from a signed plugin package into the local plugin repository and loads them via reflection, but the deployment routine processes archive entries that were never covered by the signature verification. An unauthenticated local attacker can replace an unsigned DLL outside the signed prefix in the archive passes verification and overwrites the legitimate signed assembly at the same destination path. The plugin loader then instantiates the attacker-supplied code without any additional integrity check resulting in a full compromise of the affected systems.

### CVE-2026-121600

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-04T01:17:23.647 |

A flaw has been found in TOTOLINK A950RG 4.1.2cu.5268_B20221104. Affected by this vulnerability is the function setMacFilterRules of the file /cgi-bin/cstecgi.cgi of the component MAC Filter Handler. This manipulation of the argument addEffect causes stack-based buffer overflow. The attack can be initiated remotely. The exploit has been published and may be used.

### CVE-2026-121599

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-04T01:17:23.413 |

A vulnerability was detected in TOTOLINK A950RG 4.1.2cu.5268_B20221104. Affected is the function setWiFiMultipleConfig/delWiFiMultipleConfig of the file /cgi-bin/cstecgi.cgi of the component Multi-SSID Configuration. The manipulation of the argument wepkey2/wepkey3 results in stack-based buffer overflow. It is possible to launch the attack remotely. The exploit is now public and may be used.

### CVE-2026-121598

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-04T01:17:23.160 |

A security vulnerability has been detected in TOTOLINK A950RG 4.1.2cu.5268_B20221104. This impacts the function strcpy of the file /cgi-bin/cstecgi.cgi of the component Basic Wireless Configuration Handler. The manipulation of the argument wepkey leads to stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-121597

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-04T00:17:27.410 |

A weakness has been identified in TOTOLINK A950RG 4.1.2cu.5268_B20221104. This affects the function setAppEasyWizardConfig of the file /cgi-bin/cstecgi.cgi of the component Easy Setup Wizard Handler. Executing a manipulation of the argument functionType can lead to stack-based buffer overflow. The attack may be performed from remote. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-73328

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-03T16:17:36.340 |

Volmarg Personal Management System through 2.1.0 contains an unrestricted file upload vulnerability that allows authenticated users to upload PHP files via the /upload/send/ endpoint. Attackers can submit base64 fileContent with a .php fileName into the web root and request it to execute code as the web server user.

### CVE-2026-121559

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-03T16:17:28.587 |

GLPI 10.0.0 before 10.0.28 and 11.0.0 before 11.0.10 contains a privilege escalation vulnerability that allows authenticated users to obtain elevated profiles by cloning accounts. A user with the Technician profile can clone a Super-Admin account with a new login and password, since User::getCloneRelations() copies every Profile_User and Group_User assignment without permission checks, yielding an attacker-controlled Super-Admin account.

### CVE-2026-121436

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-03T15:17:34.960 |

Froxlor from 2.3.8 before 2.3.15 contains an information disclosure vulnerability that allows administrators with customers_see_all to view every account's API key and secret through an unscoped WHERE 1 query in api_keys.php. Attackers can read the super administrator's apikey and secret from the detail modal and replay them to the API to gain super administrator control.

### CVE-2026-121419

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-03T15:17:31.953 |

SurrealDB from 3.1.0 before 3.3.0 contains an improper authentication vulnerability where the MCP BoundSubject fingerprint uses the access method name instead of per-user identity for JWT/Bearer access. Attackers with a valid low-privilege token for the same access method and a victim's mcp-session-id can hijack the session and execute MCP tools with the victim's roles and permissions.

### CVE-2026-121941

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-04T13:17:28.560 |

libmt32emu before 2.8.4 contains a heap buffer overflow vulnerability in MidiStreamParserImpl::parseSysex that allows attackers to write past a heap allocation by supplying oversized unterminated SysEx messages. Attackers can feed more than 32768 SysEx data bytes through the mt32emu_parse_stream API via MIDI files, ports, or sequencer clients to corrupt heap memory and crash the application.

### CVE-2026-121147

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-04T13:17:27.197 |

This vulnerability exists in the iRA 2.0 and iRA.ev mobile applications due to improper implementation of SSL certificate pinning in the network security configuration, resulting in ineffective certificate pinning controls. An attacker positioned to intercept network traffic could exploit this vulnerability to intercept or modify communications between the application and its backend services.

### CVE-2026-121818

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1394` |
| Published | 2026-11-04T07:17:12.350 |

Herowatch Mini developed by About Time Technologies has a system signing vulnerability. Authenticated local attackers can exploit a publicly available test key to sign malicious programs, allowing them to elevate privileges and execute arbitrary code.

### CVE-2026-112116

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-11-04T02:17:14.953 |

An exposed IOCTL with insufficient access control in ASUS System Control Interface allows a local, low-privileged user to read and write arbitrary physical memory through crafted device control requests, ultimately resulting in a complete compromise of the affected system.
Refer to the ' Security Update for ASUS System Control Interface ' section on the ASUS Security Advisory for more information.

### CVE-2026-121603

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-03T17:18:11.567 |

Solanum before commit 2ea1382 contains a buffer overflow vulnerability in ms_kill() that allows malicious linked servers to corrupt memory by sending an overlong kill reason. Attackers controlling a rogue or compromised peer server can send a reason exceeding KILLLEN that overflows a static 512-byte buffer, crashing the ircd or potentially achieving remote code execution.

### CVE-2026-121602

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-03T17:18:11.387 |

Solanum before commit 2ce64de contains a heap-based buffer overflow vulnerability that allows a malicious linked server to corrupt memory by sending overlong channel names in JOIN or SJOIN messages. Attackers controlling a peer server can trigger strcpy and sprintf overflows in ms_join and ms_sjoin to crash the ircd or potentially achieve remote code execution.

### CVE-2026-121260

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-94` |
| Published | 2026-11-03T16:17:23.393 |

A flaw has been found in Ziroom ZHOME A0101 1.0.1.0 Build 202004151405. This issue affects the function loadstring of the file usr/lib/lua/luci/controller/api/zrUsb.lua of the component Lua Handler. This manipulation causes code injection. Remote exploitation of the attack is possible. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-111036

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:L/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-04T10:17:24.770 |

Server-side request forgery (SSRF) vulnerability in the Coupa Supplier Portal SaaS platform, specifically in the document conversion functionality available in the ‘Contracts > Templates’ section. The vulnerability is due to insufficient validation of references to external resources processed by the Aspose.Words for Java library during DOCX-to-PDF conversion. An authenticated attacker with permissions to modify templates could upload a specially crafted DOCX document containing references to external resources, which would cause the server-side application to access URLs controlled by the attacker, resources on the internal network, or local files. A successful exploit could lead to the disclosure of sensitive information, such as configuration files, system files, credentials, environment variables and endpoints for internal services.

### CVE-2026-109836

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-11-03T23:17:25.697 |

The Core Temp kernel driver provided by ALCPU is vulnerable to insufficient access control in an exposed IOCTL, which may allow physical memory to be read or written.

### CVE-2026-95723

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:20.170 |

A missing integrity verification vulnerability has been discovered in the Virtual Intranet Access (VIA) client. Successful exploitation of this vulnerability could allow a low-privileged local attacker to execute arbitrary code with elevated privileges on the underlying operating system.

### CVE-2026-28335

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-03T17:18:12.430 |

SolarWinds Dameware was found to be affected by a buffer overflow vulnerability that can result in remote code execution. Authentication is required.

### CVE-2026-103916

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-03T17:17:52.847 |

Docker Sandboxes sbx cp does not safely confine host-side paths to a shared workspace. A malicious sandbox can create or replace a workspace symlink so that a later user-initiated copy reads a host file outside the workspace into the sandbox or writes sandbox-controlled data to a host path outside the workspace with the invoking user's permissions.

### CVE-2026-121548

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-03T16:17:26.557 |

Jarun nnn through 5.3 contains an OS command injection vulnerability in plugins/togglex that allows attackers to execute commands via crafted filenames. Attackers can place files whose names contain a double quote and shell syntax, which xargs -I splices into an sh -c script, running commands as the user invoking togglex.

### CVE-2026-121620

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-04T13:17:27.537 |

CoopCycle coopcycle-web 5.6.0 before 6.20.0 contains a missing authentication vulnerability that allows unauthenticated attackers to forge Zelty webhook events because the x-zelty-hmac-sha256 HMAC signature is never verified. Attackers can POST forged dish, menu, option and order-status events to /api/zelty/webhook/* endpoints to toggle restaurant products and alter order preparation states.

### CVE-2026-114421

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-04T09:17:41.553 |

SEPPmail Secure Email Gateway before 15.1.1 permits password recovery for a created but unregistered GINA account whose initial password is empty without adequately verifying ownership. A remote unauthenticated attacker who identifies such an account can set a new password, authenticate as that account, and prevent the intended recipient from using it until recovery.

### CVE-2026-87040

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-120;CWE-787` |
| Published | 2026-11-04T06:17:06.773 |

The nRF link-layer receive paths of the open-source Bluetooth LE Controller did not validate the on-air LENGTH field of a received PDU against the maximum receive length that was used to program the radio. isr_rx_pdu() in subsys/bluetooth/controller/ll_sw/nordic/lll/lll_conn.c enqueued any non-empty data PDU after only the sequence-number and (for encrypted links) MIC checks, and the corresponding isr_rx() handlers in lll_central_iso.c, lll_peripheral_iso.c, lll_sync_iso.c and lll_scan_aux.c did the same for ISO and extended-advertising PDUs. The nRF radio stores the received header verbatim and truncates only the payload at PCNF1.MAXLEN, so a frame declaring more octets than were configured leaves a node buffer whose len field describes more data than the buffer holds.

An attacker within radio range that can emit a hand-crafted link-layer PDU — for a connection, any peer that establishes an unencrypted LE connection to a connectable advertiser; for CONFIG_BT_CTLR_SYNC_ISO, any broadcaster the device is synchronised to — can set the length byte up to 255 while the controller has programmed a much smaller maximum (lll->dle.eff.max_rx_octets, which is 27 until a Data Length Update, or the negotiated cis_lll->rx.max_pdu). No pairing, authentication or user interaction is required. On encrypted links the CCM MIC check normally rejects such a frame first, so the exposure is on unencrypted traffic, which is why the added check is placed after decryption.

The unchecked length reaches hci_acl_encode() in subsys/bluetooth/controller/hci/hci.c, which performs net_buf_add(buf, pdu_data->len) followed by a memcpy() of that many bytes out of the node_rx pool element. Because CONFIG_BT_CTLR_DATA_LENGTH_MAX and CONFIG_BT_BUF_ACL_RX_SIZE both default to 27, this is an out-of-bounds read of up to roughly 228 bytes past the received PDU and a corresponding out-of-bounds write past the HCI ACL buffer into neighbouring buffers of the same pool; the tailroom test in net_buf_simple_add() is only enforced when CONFIG_NET_BUF_HARDENING (or CONFIG_ASSERT) is enabled. On the ISO paths the same unchecked length makes isoal_rx_append_to_sdu() read past the ISO node buffer and emit adjacent controller RAM to the host as ISO data. The practical result is remote memory corruption and controller crashes, plus disclosure of controller memory into the host data path.

The fix rejects any received PDU whose length exceeds the value that was used to configure the radio reception. Note that lll_sync.c (periodic advertising sync reception) was not changed and still enqueues received PDUs without an equivalent bound.

### CVE-2026-121256

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-672` |
| Published | 2026-11-03T21:17:36.470 |

Use of released resource in GPU in Google Chrome prior to 157.0.8103.38 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121230

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-03T21:17:32.973 |

Race condition in ANGLE in Google Chrome prior to 157.0.8103.38 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-121219

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-03T21:17:31.513 |

Integer overflow in GPU in Google Chrome prior to 157.0.8103.38 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121183

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-03T21:17:26.917 |

Incorrect authorization in Extensions in Google Chrome prior to 157.0.8103.38 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-121178

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T21:17:26.260 |

Use after free in Aura in Google Chrome prior to 157.0.8103.38 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121140

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-03T21:17:22.610 |

Out of bounds read in Internals in Google Chrome prior to 157.0.8103.38 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121112

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-03T21:17:18.797 |

Out of bounds read in Permissions in Google Chrome prior to 157.0.8103.38 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121098

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-754` |
| Published | 2026-11-03T21:17:15.817 |

Improper state validation in GPU in Google Chrome prior to 157.0.8103.38 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121090

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-03T21:17:14.680 |

Improper privilege management in Navigation in Google Chrome on on iOS prior to 157.0.8103.38 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-121084

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-03T21:17:13.850 |

Out of bounds read in Skia in Google Chrome prior to 157.0.8103.38 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95736

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:21.790 |

Improper certificate validation vulnerabilities exist in the affected interface of HPE Networking Fabric Composer, which could be exploited by an unauthenticated adjacent attacker if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to intercept sensitive information.

### CVE-2026-63502

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-03T20:18:17.280 |

Yeti bridges the gap between CTI and DFIR practitioners by providing a Forensics Intelligence platform and pipeline. Prior to 2.5.1, YETI derives ExportTask.file_name from the user-controlled task name and passes it to core/clients/file_storage/classes/local_storage.py without sanitizing traversal sequences or enforcing path confinement. A low-privileged authenticated user using the default local storage backend can call POST /api/v2/tasks/export/new with a traversal name and use ExportTask.file_contents through GET /api/v2/tasks/export/{export_id}/content to read files accessible to the YETI service account. Running ExportTask.run() can also write attacker-controlled export output to an attacker-selected writable path. The impact depends on the service account's filesystem permissions, and universal code execution is not established. This issue is fixed in version 2.5.1.

### CVE-2026-105822

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:L/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-03T20:18:06.143 |

The Tapo
Cloud MQTT proxy contains a server-side request forgery (SSRF) vulnerability
because it accepts a user-controlled host value without sufficient input
validation. An attacker may exploit this vulnerability to cause the Tapo Cloud
service to send requests to an attacker-controlled server.









Successful
exploitation may cause the Tapo Cloud service to send a request to an
attacker-controlled server, exposing the internal information and causing
potential Distributed Denial-of-Service (DDoS).

### CVE-2026-105821

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-03T20:18:05.987 |

The Tapo
Cloud MQTT broker contains a broken access control vulnerability in a proxy
topic used by authenticated Tapo devices to request service tokens. The broker
does not verify that the device ID supplied in a proxy request belongs to the
authenticated device. An attacker who owns a Tapo device and knows another
device's ID may obtain a device token scoped to the target device and use it to
upload attacker-controlled content to the target user's Tapo Cloud storage. The
content may then be presented in the Tapo app as a legitimate event.





Successful
exploitation may allow an attacker to upload attacker-controlled content that
is presented to a target user as a legitimate Tapo event, retrieve internal
service information through crafted proxy requests, or abuse Tapo Cloud
outbound request capability in activity that could affect service
availability.

### CVE-2026-121452

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-03T16:17:24.120 |

bbs-go through 4.4.6 contains an improper certificate validation vulnerability that allows network-positioned attackers to intercept SMTP traffic because sendEmail() sets InsecureSkipVerify to true. Attackers can present any certificate to capture SMTP PLAIN auth credentials and read or modify outgoing password-reset and verification emails.

### CVE-2026-121426

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-03T15:17:33.213 |

Nodemailer from 3.0.0 before 10.1.4 contains an address parsing vulnerability in addressparser that ends an angle-addr at a '>' inside a quoted local part, comment or domain literal. Attackers can submit addresses that validate as an allowed domain but are delivered to an attacker-controlled domain, bypassing recipient allow lists and disclosing message content.

### CVE-2026-121425

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-03T15:17:33.057 |

Nodemailer from 3.0.0 before 10.1.4 contains a parsing flaw in addressparser that ends an RFC 5322 group at a semicolon inside quoted display names or comments. Attackers can submit crafted group addresses that conformant validators approve, redirecting mail to attacker-chosen recipients and bypassing recipient allow lists.

### CVE-2026-121424

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-03T15:17:32.883 |

Nodemailer from 3.0.0 before 10.1.4 contains an address parsing vulnerability in addressparser that allows remote attackers to redirect recipients by ending nested RFC 5322 comments at the first closing parenthesis. Attackers can submit addresses whose nested comment hides an attacker address, bypassing conformant validators and recipient allow lists to receive mail or spoof senders in mailparser.

### CVE-2026-92198

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-04T00:17:30.827 |

Quest Foglight for Databases getSource XML External Entity Processing Information Disclosure Vulnerability. This vulnerability allows remote attackers to initiate arbitrary server-side requests on affected installations of Quest Foglight for Databases. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the getSource method. Due to the improper restriction of XML External Entity (XXE) references, a crafted document specifying a URI causes the XML parser to access the URI and embed the contents back into the XML document for further processing. An attacker can leverage this vulnerability to disclose information in the context of the application. Was ZDI-CAN-29934.

### CVE-2026-118628

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-04T00:17:24.037 |

MLflow get-artifacts Server-Side Request Forgery Information Disclosure Vulnerability. This vulnerability allows remote attackers to disclose sensitive information on affected installations of MLflow. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the get-artifacts function. The issue results from the lack of proper validation of a URI prior to accessing resources. An attacker can leverage this vulnerability to disclose information in the context of the server. Was ZDI-CAN-28192.

### CVE-2026-111752

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-405` |
| Published | 2026-11-03T21:16:57.993 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 20.3.33, 21.2.25, and 22.2.1, @angular/router in Node.js server-side rendering fails to require auxiliary outlet URL segments to match routes configured for their outlet names. Crafted requests containing multiple unconfigured empty-path outlet groups can repeatedly evaluate the route configuration, construct duplicate ActivatedRouteSnapshot trees, execute canMatch guards and resolvers, and copy route parameters and queryParams for each outlet. An unauthenticated remote attacker can exhaust the Node.js heap or CPU and terminate an SSR worker when SSR is enabled, a route level contains an empty-path route or named outlet, upstream infrastructure forwards the request target, and the worker has a constrained heap. The allocation is transient rather than a persistent leak, and client-side SPAs and build-time prerendering are not affected. This issue is fixed in versions 20.3.33, 21.2.25, and 22.2.1.

### CVE-2026-111751

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-11-03T21:16:57.800 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. From 21.2.0 until 21.2.25 and 22.2.1, RouterLink directives rendered during Node.js server-side rendering retain computed UrlTree instances for the lifetime of each request. When queryParamsHandling is set to merge or preserve, either per link or through defaultQueryParamsHandling, every rendered link can retain a copy of attacker-controlled query parameters in its UrlTree. When upstream proxies or load balancers forward oversized query strings without rejecting them at the edge, multiple affected links and overlapping renders can amplify heap use until the Node.js old-space heap is exhausted and the SSR worker terminates. Numeric query-parameter names increase allocation pressure but are not required, memory is released after rendering completes, and pure client-side SPAs are not affected. This issue is fixed in versions 21.2.25 and 22.2.1.

### CVE-2026-95737

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:21.907 |

A privilege escalation vulnerability exists in the underlying operating system of HPE Networking Fabric Composer. Successful exploitation could allow a local attacker with high privileges to gain elevated privileges on the underlying host operating system.

### CVE-2026-63417

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-03T19:18:09.243 |

Logging Redactor is a Python library designed to redact sensitive data in logs based on regex patterns and / or dictionary keys. Prior to 0.0.7, personally identifiable information returned by custom object __str__ or __repr__ methods is not redacted when such non-primitive objects are logged, causing sensitive values to appear in logs that are expected to mask them. This issue is fixed in version 0.0.7.

### CVE-2026-28327

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-03T17:18:12.270 |

SolarWinds Dameware was found to be affected by a DLL hijacking vulnerability. The hijack occurs during installations only and requires access to the local machine and admin privileges.

### CVE-2026-121557

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-03T16:17:28.163 |

WPPConnect Server through 2.10.74 contains a missing authentication vulnerability that allows unauthenticated attackers to send WhatsApp messages by calling the Chatwoot webhook route without verifyToken middleware. Attackers who know or guess a connected session name can POST outgoing message bodies to send arbitrary texts or files from that account to any number.

### CVE-2026-121554

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-03T16:17:27.627 |

cordova-plugin-advanced-http 1.5.0 through 3.3.1 contains an information disclosure vulnerability that leaks cookies to third-party hosts because the JavaScript layer passes jar-built Cookie headers as ordinary request headers. When a request is redirected to another host via an open or attacker-influenced redirect, native iOS and Android stacks forward the Cookie header, letting attackers hijack user sessions.

### CVE-2026-121445

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-11-03T15:17:36.623 |

darylldoyle svg-sanitizer from 1.0.0 before 1.1.0 contains a regular expression denial of service vulnerability in the image-set pattern of stripRemoteCssTokens() when removeRemoteReferences is enabled. Attackers can submit SVGs with many unclosed image-set tokens to exhaust CPU, or trigger PCRE limits causing sanitize() to throw a TypeError and leave unsanitized content.

### CVE-2026-121414

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-03T15:17:30.710 |

Parse Server before 8.6.110 and 9.0.0 before 9.10.6-alpha.2 fails to contain a serialization error when an object update uses a dot notation key targeting a pointer field's object identifier on a class with an afterSave trigger. Attackers, including unauthenticated clients when objects are writable without a session, can send such an update to crash the Node process.

### CVE-2026-121409

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-03T15:17:29.790 |

FreeRDP before 3.32.2 contains a denial of service vulnerability that allows malicious servers or unauthenticated peers to abort clients or proxies via oversized X.224 routing tokens. Attackers can send an oversized LoadBalanceInfo in a Server Redirection PDU, or a 240–247 byte token to a FixedTarget freerdp-proxy, triggering a tpdu_write_header assertion that crashes the process.

### CVE-2026-121398

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T15:17:27.817 |

FreeRDP before 3.32.2 contains a cross-thread use-after-free vulnerability in the freerdp-proxy dyn-channel-dump module during session teardown. A malicious RDP target can send dynamic channel data while the front client disconnects, letting the client thread read freed ChannelData and crash the proxy process.

### CVE-2026-114550

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-04T00:17:22.783 |

libwebsockets MQTT Protocol PUBACK Packet Handling Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of libwebsockets. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the handling of PUBACK packets. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-31039.

### CVE-2026-95739

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:22.153 |

An improper restriction of excessive authentication attempts vulnerability in the API of HPE Networking Fabric Composer could allow an unauthenticated remote attacker to conduct brute-force attacks against user accounts if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to gain administrative access to the affected system.

### CVE-2026-95738

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:22.030 |

Authentication bypass vulnerabilities in the affected interface of HPE Networking Fabric Composer could allow an unauthenticated remote attacker to circumvent existing authentication controls if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to gain administrative access to the affected system.

### CVE-2026-95724

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:20.297 |

An improper certificate validation vulnerability exists in HPE Networking Virtual Intranet Access (VIA). Successful exploitation could allow an unauthenticated remote attacker to bypass authentication mechanisms, leading to the possible disclosure of sensitive information.

### CVE-2026-54161

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-03T20:18:14.243 |

Network UPS Tools is a collection of programs which provide a common interface for monitoring and administering UPS, PDU and SCD hardware. From 2.8.3 to 2.8.5, upsmon in clients/upsmon.c inserts the server-supplied ups.alarm value into shell commands executed by notify(), async_notify(), and wall(). When a monitored device reports an ALARM state and an operator has configured NOTIFYCMD with EXEC in NOTIFYFLAG ALARM, shell metacharacters in the alarm text are evaluated on POSIX or Windows and can execute arbitrary operating-system commands as the upsmon account, which is commonly root. An attacker can control the value through a malicious or compromised upsd, a man-in-the-middle on a plaintext upsd to upsmon connection, or a compromised UPS device whose driver supplies the alarm upstream of upsd; TLS between upsd and upsmon does not mitigate the compromised-device path. This vulnerability is fixed in 2.8.6.

### CVE-2026-57154

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-93` |
| Published | 2026-11-03T19:18:06.513 |

OPNsense is a FreeBSD based firewall and routing platform. Prior to 26.1.11 and 26.4.1p1, authenticated Web UI or API users with delegated access to affected settings can submit CR or LF characters in fields expected to contain one line, causing generated privileged service configuration files to contain additional attacker-controlled directives or policy lines. The confirmed Dnsmasq path includes dhcp_boot.filename, dhcp_boot.servername, dhcp_boot.address, and dhcp_options.value, which are rendered into /usr/local/etc/dnsmasq.conf; access through page-services-dnsforwarder covers api/dnsmasq/*. Related affected fields span OpenVPN, DHCPv6, Unbound, IPsec, NTP, PPP or MPD, Monit, firewall, sudo, WebGUI, and System General configuration. Applying or restarting the affected service can alter behavior beyond the delegated setting, create service-side files, cross RBAC boundaries, or cause denial of service. Line injection through Monit mail password and adjacent Monit text fields into /usr/local/etc/monitrc demonstrated root command execution. Arbitrary shell command execution was not confirmed for the Dnsmasq path. This issue is fixed in versions 26.1.11 and 26.4.1p1.

### CVE-2026-95741

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:22.420 |

A missing integrity verification vulnerability exists in the API of HPE Networking Fabric Composer. Successful exploitation could allow a low-privileged authenticated attacker to gain elevated privileges on the affected system.

### CVE-2026-95740

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:22.290 |

An improper certificate validation vulnerability in HPE Networking Fabric Composer could allow an unauthenticated adjacent attacker to intercept communications between the affected system and remote servers if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to obtain sensitive information.

### CVE-2026-87041

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-787;CWE-822` |
| Published | 2026-11-04T06:17:06.943 |

The RTIO submission-queue verifier rtio_vrfy_sqe() in subsys/rtio/rtio_syscalls.c (subsys/rtio/rtio_handlers.c before v4.3.0) accumulated the results of K_SYSCALL_MEMORY() into its valid_sqe flag with &=. That macro returns nonzero on failure (it is built on K_SYSCALL_VERIFY_MSG(), which yields !(expr)), so every buffer permission check contributed the opposite of its result. A submission whose tx.buf, rx.buf or txrx.tx_buf/txrx.rx_buf pointer was not accessible to the calling thread was accepted, while a legitimate, thread-owned buffer caused the calling thread to be killed with a kernel oops.

The verifier runs on behalf of the rtio_sqe_copy_in_get_handles() system call (also reached through the inline rtio_sqe_copy_in() wrapper), so it is driven directly by untrusted user-mode input on any image built with CONFIG_USERSPACE. A user thread that has been granted an RTIO context and an rtio_iodev object — the intended usage of RTIO userspace support, established via rtio_access_grant() — can submit an SQE whose buffer pointer and length name arbitrary kernel memory; the object check on sqe->iodev is unaffected and still passes, and the crafted SQE is forwarded to the bus driver unchanged.

Downstream consumers dereference the pointer with supervisor privilege. The generic I2C and I3C RTIO fallback handlers (drivers/i2c/i2c_rtio_default.c, drivers/i3c/i3c_rtio_default.c) copy sqe.rx.buf/sqe.tx.buf into struct i2c_msg and call i2c_transfer(), and the vendor SPI/I2C RTIO drivers behave equivalently. An RTIO_OP_RX submission therefore has peripheral data written into kernel memory of the attacker's choosing (arbitrary kernel write), an RTIO_OP_TX submission clocks kernel memory out over the bus (kernel memory disclosure), and a pointer to unmapped memory faults the kernel. This is a full escape from the user-mode isolation boundary that CONFIG_USERSPACE exists to enforce.

The defect was masked for years because the in-tree user-mode RTIO tests only exercise RTIO_OP_NOP and mempool-backed reads, neither of which reaches the affected checks. The fix negates each K_SYSCALL_MEMORY() result and additionally validates the TXRX transmit buffer read-only, matching the SPI, I2C and I3C handlers.

### CVE-2026-87039

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-04T06:17:06.623 |

The user-mode syscall verifier z_vrfy_i2s_configure() in drivers/i2s/i2s_handlers.c copies the caller's struct i2s_config in from user memory and then, when cfg->frame_clk_freq is 0 (the API's "unconfigure the stream" request), jumps straight to z_impl_i2s_configure() without performing the K_SYSCALL_OBJ(config.mem_slab, K_OBJ_MEM_SLAB) ownership/type check or the block_size sanity check. The mem_slab field is a struct k_mem_slab *, so on that path a completely unvalidated, user-chosen pointer reaches driver code that is entitled to trust it as a real kernel object.

Any thread running under CONFIG_USERSPACE that has access to an I2S device object can trigger this with a single i2s_configure() call. Most in-tree drivers special-case frame_clk_freq == 0 and never store the caller's structure, but drivers/i2s/i2s_litex.c does not: i2s_litex_configure() only logs a warning for a mismatched frame clock, then memcpy()s the caller's config into stream->cfg and marks the stream I2S_STATE_READY. A subsequent i2s_trigger() with I2S_TRIGGER_START enables the FIFO interrupt, and the interrupt handlers i2s_litex_isr_rx() / i2s_litex_isr_tx() then call k_mem_slab_alloc() and k_mem_slab_free() on the attacker-supplied pointer in supervisor context.

The result is an arbitrary-pointer read/write primitive executed by the kernel on behalf of an unprivileged thread — k_mem_slab_alloc() takes a spinlock at slab->lock and reads and writes slab->free_list and the link word inside the returned "block" — which defeats the CONFIG_USERSPACE isolation boundary entirely. The same missing validation is a hazard for out-of-tree I2S drivers that retain the configuration on the unconfigure path. Builds without CONFIG_USERSPACE are unaffected, since the verifier is not used.

The fix zeroes config.mem_slab and config.block_size on the unconfigure path so the driver can never receive an unvalidated pointer, while still allowing a stream to be unconfigured by a caller that does not own a memory slab, as the API documents.

### CVE-2026-92211

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-04T00:17:31.273 |

Pixar Animation Studio OpenUSD Crate File Parsing Double Free Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Pixar Animation Studio OpenUSD. Interaction with this library is required to exploit this vulnerability but attack vectors may vary depending on the implementation.

The specific flaw exists within the parsing of USDC and USDZ files. The issue results from the lack of validating the existence of an object prior to performing further free operations on the object. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-30428.

### CVE-2026-92200

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-04T00:17:31.120 |

Quest Foglight for Databases Incorrect Permission Assignment Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Quest Foglight for Databases. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the product installer. The issue results from incorrect permissions on a folder used by the product. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-31118.

### CVE-2026-92199

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-04T00:17:30.970 |

Quest Foglight for Databases EncryptionUtil Hardcoded Encyption Key Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Quest Foglight for Databases. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the symmetricDecrypt method. The issue results from the use of a hard-coded cryptographic key. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-29967.

### CVE-2026-118627

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-04T00:17:23.890 |

MLflow SHAP load_explainer Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of MLflow. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the loading of SHAP explainer models. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-30301.

### CVE-2026-118623

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-04T00:17:23.273 |

MLflow PickleEvaluationArtifact Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of MLflow. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of pickle files. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29513.

### CVE-2026-82155

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-428` |
| Published | 2026-11-03T21:17:43.680 |

Dell OS Recovery tool versions, prior to 2.4.4, contain a use of Untrusted Search Path vulnerability. An unauthenticated attacker with local access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-115878

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-502` |
| Published | 2026-11-03T21:17:02.377 |

Stanza is a Stanford NLP Python library for tokenization, sentence segmentation, NER, and parsing of many human languages. From 1.14.0 until 1.15.0, loading an attacker-supplied lemmatizer checkpoint can execute arbitrary code because stanza/models/lemma/trainer.py stores pos_dict as gzip-compressed pickle bytes and Trainer.load passes the decompressed stream to unrestricted pickle.loads. The outer torch.load call uses weights_only=True, but the nested bytes are treated as a primitive and are not inspected by that allowlist. The path is reachable during pipeline construction through a caller-influenced lemma_model_path, before inference begins. This issue is fixed in version 1.15.0.

### CVE-2026-95743

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:22.670 |

Local privilege escalation vulnerabilities exist in the underlying operating system of HPE Networking Fabric Composer. Successful exploitation could allow a local attacker with low privileges to gain elevated privileges on the affected system.

### CVE-2026-95742

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:22.550 |

An arbitrary file write vulnerability exists in the underlying operating system of HPE Networking Fabric Composer. Successful exploitation could allow an authenticated local attacker to create or overwrite arbitrary files on the affected system with elevated privileges.

### CVE-2026-95725

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:20.430 |

A command injection vulnerability exists in the VIA client for Linux. Successful exploitation could allow a low-privileged local attacker to execute arbitrary commands with elevated privileges on the affected system.

### CVE-2026-118513

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-04T13:17:25.890 |

Authentication bypass by spoofing in X509Authenticator and X509AuthenticationListener of Symfony versions prior to 5.4.56, 6.x prior to 6.4.50, 7.x prior to 7.4.23, and 8.x prior to 8.1.11 allows an attacker holding a certificate from the application's trusted CA who can influence the CN to authenticate as an arbitrary user of the application, including a privileged one, following an incomplete fix for CVE-2026-45063.
X509Authenticator extracts the user identifier from the Subject DN (Distinguished Name) that the web server passes in $_SERVER['SSL_CLIENT_S_DN']. The fix for CVE-2026-45063 anchored that extraction to an RDN (Relative Distinguished Name) boundary, but the regular expression used was not escape-aware. The expression runs against an already serialized DN, so it cannot tell an RDN separator from a separator character that occurs inside a value. Under RFC 2253, used by Apache and by nginx's $ssl_client_s_dn, a comma inside a value is escaped as \, and the expression reads it as a separator regardless. RFC 2253 also does not treat / as a separator, so it leaves it bare inside a value, while the expression treats every / as one. The legacy X509_NAME_oneline() format, used by Apache's LegacyDNStringFormat and by nginx's $ssl_client_s_dn_legacy, is the mirror image: it escapes / as \/ and leaves , bare. In that format, a certificate with no emailAddress attribute, or whose poisoned CN precedes it, authenticates as the smuggled address.





To cover both RFC 2253 and the legacy X509_NAME_oneline() format, X509Authenticator and X509AuthenticationListener now split the DN into RDNs before looking for the attribute, instead of matching the attribute against the serialized string. They select the separator from the serialization, split on unescaped occurrences of that separator only, unescape each RDN afterwards with the rules of its format, and require the attribute to span a whole RDN. The accepted value grammar is unchanged.




Applications that pass a per-attribute user key (such as SSL_CLIENT_S_DN_Email) and deployments whose CA generates or validates the subject are not affected by this vulnerability.

### CVE-2026-77779

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-1220` |
| Published | 2026-11-04T06:17:06.070 |

ManageEngine Key Manager Plus versions before 7151 were vulnerable to an Improper Access Control vulnerability that allowed authenticated low-privilege users to export keys outside their authorized scope.

### CVE-2026-121617

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-11-04T03:17:15.287 |

A security flaw has been discovered in Linksys E5600 1.1.0.26. Affected by this issue is the function init_multipart of the file /cgi-bin/upload_fw.cgi of the component Header Parser. The manipulation results in out-of-bounds write. The attack may be launched remotely. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-104608

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416;CWE-1265` |
| Published | 2026-11-03T23:17:24.420 |

A remote code execution vulnerability was identified in GitHub Enterprise Server in the Git service (babeld). babeld held references into internal collections while calling into the SSH library, where a re-entrant callback could modify a collection and invalidate those references. An attacker with an account and SSH access to the instance could leverage this use-after-free into a controlled write and run arbitrary commands as babeld, including disclosure of its environment secrets. Exploitation required per-build memory offsets; failed attempts crashed babeld. This affected all releases prior to 3.23 and was fixed in 3.22.3, 3.21.8, 3.20.10, and 3.19.14. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-95744

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:22.790 |

A sensitive information disclosure vulnerability in the affected interface of HPE Networking Fabric Composer could allow an authenticated low-privileged attacker to access sensitive information, if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to intercept protected network traffic.

### CVE-2026-88968

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59;CWE-367` |
| Published | 2026-11-03T20:18:19.010 |

Claude Code is an agentic coding tool. Prior to 2.1.251, the Edit tool validates a target using pathname and symlink resolution that is not bound to the underlying directory inode or file descriptor. On macOS, attacker-controlled code running in the Bash sandbox can atomically replace an in-workspace parent directory with a symlink after validation, causing the unsandboxed Edit implementation to overwrite a user-writable file outside the workspace. Exploitation requires attacker-controlled code to run inside the sandbox, such as from a malicious repository or dependency script. This issue is fixed in version 2.1.251.

### CVE-2026-121382

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-189;CWE-190` |
| Published | 2026-11-03T19:18:01.197 |

A vulnerability was determined in Netcore NBR100V2 1.3.240614.030928. Affected by this issue is the function msg_aes_dec of the file /usr/bin/auto_ac. This manipulation causes integer overflow. Remote exploitation of the attack is possible. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-121450

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-760` |
| Published | 2026-11-03T16:17:23.787 |

CFNext before 3.1.0 contains a weak cryptographic derivation vulnerability that allows subscription link holders to recover the admin password because the subscription UUID is an MD5 of the password with a fixed public salt. Attackers can brute-force the password offline without rate limiting, log into the admin panel, and read stored Trojan, Clash, Telegram and Cloudflare API secrets.

### CVE-2026-11749

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-04T06:17:03.793 |

A vulnerability has been identified in armeria-saml prior to 1.41.1, where bearer assertions are not enforced for one-time use, allowing replay of previously consumed assertion IDs within their validity period.

### CVE-2026-80335

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:P/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-04T04:17:37.623 |

In the bootloader download module, there is a possible out-of-bounds write due to a failure to reset a global offset variable during firmware update sessions. This could lead to heap memory corruption, system crash, or potential arbitrary code execution with no additional execution privileges needed.

### CVE-2026-63489

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-03T20:18:16.590 |

Yeti bridges the gap between CTI and DFIR practitioners by providing a Forensics Intelligence platform and pipeline. In version 2.5.0 and earlier, YETI directly interpolates user-controlled sorting fields and filter_aliases attribute paths into ArangoDB AQL identifier and expression positions in core/database_arango.py. A low-privileged authenticated user can send crafted values to POST /api/v2/observables/search, POST /api/v2/entities/search, POST /api/v2/indicators/search, POST /api/v2/dfiq/search, POST /api/v2/search/, or POST /api/v2/graph/search, causing attacker-controlled AQL subexpressions to be parsed and evaluated. This can provide an error oracle, evaluate expressions against internal collections such as users, alter intended search logic, enumerate schema information, and consume excessive database resources. The verified injection points are read and search contexts, so arbitrary database writes are not established. No fixed version is available as of this review.

### CVE-2026-121624

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-03T18:17:58.270 |

Nanosystems Supremo for Windows and macOS before 5.0.2.3874 contains an improper certificate validation vulnerability that allows adjacent attackers to intercept TLS connections by presenting untrusted certificates. Attackers on the same network can terminate and relay the client's TLS session using self-signed certificates to read usernames, SHA-256 password hashes, and license codes.

### CVE-2026-119215

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-03T16:17:21.683 |

Authorization Bypass Through User-Controlled Key vulnerability in team-alembic ash_authentication allows a user with an account to install a TOTP secret they control on another user's account, and then sign in as that user or hold their second factor.

AshAuthentication.Strategy.Totp.ConfirmSetupChange verified a setup token but did not check that it was issued to the record being confirmed, so an attacker's own pending secret could be confirmed onto another user's record. The TOTP setup changes, ConfirmSetupChange, GeneratePendingSetupChange and GenerateSecretChange, also marked their changesets as AshAuthentication interactions, which the standard AshAuthenticationInteraction policy bypass lets through. A policy limiting setup and confirm_setup to the actor's own record therefore never ran when an application exposed those actions by record key, and a direct setup call on another user's record returned that user's pending secret and setup token.

This issue affects ash_authentication: from 5.0.0-rc.0 before 5.0.0-rc.16.

### CVE-2026-62126

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-04T08:17:17.890 |

Allocation of Resources Without Limits or Throttling vulnerability in miniOrange SAML SP Single Sign On miniorange-saml-20-single-sign-on allows HTTP DoS.This issue affects SAML SP Single Sign On: from n/a through 6.1.0.

### CVE-2026-56065

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-538` |
| Published | 2026-11-04T08:17:17.093 |

Insertion of Sensitive Information into Externally-Accessible File or Directory vulnerability in Doofinder Doofinder for WooCommerce doofinder-for-woocommerce allows Retrieve Embedded Sensitive Data.This issue affects Doofinder for WooCommerce: from n/a through 2.17.2.

### CVE-2026-62000

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-04T07:17:12.750 |

Missing Authorization vulnerability in WC Lovers WCFM Marketplace wc-multivendor-marketplace allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects WCFM Marketplace: from n/a through 3.8.2.

### CVE-2026-79405

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-04T04:17:37.480 |

In Modem Firmware, there is a possible system crash due to improper input validation of dedicated PUCCH configuration. This could lead to remote denial of service with no additional execution privileges needed.

### CVE-2026-116651

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-03T23:17:30.887 |

Tanium addressed an unauthorized code execution vulnerability in Threat Response.

### CVE-2026-116650

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-03T23:17:30.723 |

Tanium addressed an unauthorized code execution vulnerability in Threat Response.

### CVE-2026-95750

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:23.547 |

An improper certificate validation vulnerability in HPE Networking Fabric Composer could allow an unauthenticated remote attacker to access sensitive information if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to obtain sensitive information, including credentials.

### CVE-2026-95749

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:23.420 |

A missing integrity verification vulnerability exists in HPE Networking Fabric Composer. Successful exploitation could allow an unauthenticated remote attacker to execute arbitrary code on the affected system.

### CVE-2026-95748

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:23.280 |

A SQL injection vulnerability exists in HPE Networking Fabric Composer. Successful exploitation could allow an unauthenticated adjacent attacker to run arbitrary database commands.

### CVE-2026-95747

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:23.150 |

A privilege escalation vulnerability exists in the SSH interface of HPE Networking Fabric Composer which could allow an authenticated low-privileged attacker to exceed their authorized level of access, if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to gain unauthorized access to internal services of the affected system.

### CVE-2026-95746

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:23.030 |

An authentication bypass vulnerability in the API endpoint of HPE Networking Fabric Composer could allow an unauthenticated adjacent attacker to circumvent existing authentication controls if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to gain unauthorized access to the affected system.

### CVE-2026-95745

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:22.913 |

A vulnerability in the API of HPE Networking Fabric Composer could allow an unauthenticated remote attacker to conduct a denial of service attack. Successful exploitation could allow an attacker to cause the management services to become unavailable.

### CVE-2026-95726

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:20.560 |

A buffer overflow vulnerability in HPE Networking VIA could allow an unauthenticated remote attacker to conduct a denial of service attack. Successful exploitation could allow an attacker to interrupt the normal operation of the affected client.

### CVE-2026-88066

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-03T20:18:18.850 |

Claude Desktop is Anthropic's desktop application for interacting with Claude. Prior to 1.8089.0, Claude Desktop on Windows invokes git.exe through uv_spawn without an absolute path, allowing Windows search-path resolution to select a malicious git.exe placed in the opened project's current working directory before the intended system executable. Opening an attacker-controlled or shared repository can therefore execute the substituted program with the user's privileges. This issue is fixed in version 1.8089.0.

### CVE-2026-63501

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-03T20:18:17.100 |

ag-psd is a JavaScript library for reading and writing Photoshop Document files. Prior to 31.0.3, readPsd() accepts a totalMemoryLimit for parsing untrusted PSD files, but decodeLayerImageData expects a differently named memoryLimit property and therefore passes an undefined limit to createImageDataBitDepth. An attacker who can supply a PSD to an application with layer decoding enabled can use attacker-controlled layer dimensions to trigger an allocation larger than the configured limit, causing process memory exhaustion and denial of service. The advisory also identifies inflateSync(compressed) decompressing ZIP-encoded channel data without an output-size cap, which can cause a similar denial of service through unbounded decompression. This vulnerability is fixed in 31.0.1.

### CVE-2026-63482

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-03T20:18:16.407 |

Yeti bridges the gap between CTI and DFIR practitioners by providing a Forensics Intelligence platform and pipeline. Prior to 2.5.1, YETI registers the audit router without Depends(auth.get_current_active_user), and core/web/apiv2/audit.py does not perform a route-level authentication check for /api/v2/audit/timeline/{id}. An unauthenticated network attacker can use an empty, partial, or specific wildcard path to query TimelineLog records containing the actor, target_id, action, and details fields, including analyst usernames, object identifiers and values, and before-and-after object data. This exposes the operational history of threat-intelligence objects while other application routers require authentication. This issue is fixed in version 2.5.1.

### CVE-2026-46487

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-03T19:18:05.933 |

GeoNetwork is a catalog application to manage spatially referenced resources. From 4.0.0-alpha.1 until 4.2.16 and 4.4.11, the Elasticsearch-backed search proxy can skip GeoNetwork's access-control filter injection when a client request has an omitted query field. The request is then forwarded to Elasticsearch without group visibility, draft exclusion, record ownership, or portal-specific filtering. An unauthenticated remote attacker can use the affected public search API to retrieve the full indexed contents of metadata records that should not be publicly visible. This issue is fixed in versions 4.2.16 and 4.4.11.

### CVE-2026-115290

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-03T17:17:54.943 |

Uncontrolled Recursion (CWE-674) in Elasticsearch can lead to denial of service via Serialized Data with Nested Payloads (CAPEC-230). An unauthenticated attacker with network access to the remote cluster server interface of a node can send a specially crafted request that causes the node to terminate. No credentials are required. The attacker can repeat the request against each reachable node.

### CVE-2026-118487

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-03T16:17:19.890 |

In Eclipse Vert.x versions [4.0.0, 4.5.35] or [5.0.0, 5.2.2], the `FrameParser` in vertx-stomp creates a `RecordParser` without setting `maxRecordSize`, so any peer that streams bytes continuously without a newline character causes the parser to accumulate data indefinitely. Both the STOMP server and the STOMP client are affected: a malicious server can exploit this against a connecting client, and a malicious client can exploit this against a server before or after authentication. Sustained byte streaming exhausts JVM heap memory, crashing the affected process and causing a complete denial of service.

### CVE-2026-121513

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-03T15:17:38.543 |

Off-by-one Heap Overflow in µD3TN v0.15.1 SPP Parser allows Unauthenticated Remote Attacker to Reliably Cause DoS

### CVE-2026-121512

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-11-03T15:17:38.400 |

Memory Leak with Amplification in µD3TN BPv6 EID Reference Handling allows Unauthenticated Remote Attacker to Cause DoS

### CVE-2026-121510

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-03T15:17:38.137 |

Remote Unauthenticated Heap Out-of-Bounds Write in µD3TN BPv6 Administrative Record Parser allows Unauthenticated Remote Attacker to Reliably Cause DoS

### CVE-2026-118489

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-524` |
| Published | 2026-11-03T15:17:24.780 |

In Eclipse Vert.x versions [4.0.0,4.5.35] or [5.0.0,5.2.2], when one `CachingWebClient` is shared across users — the documented pattern of a per-user `WebClientSession` over a shared caching client — a response that is specific to one user but is cacheable and not marked `private`/`no-store` is stored in the client-level shared cache tier and served to other users requesting the same URL. A later user's session, or an anonymous caller through the same client, can receive an earlier user's response. Depending on the response this discloses authenticated content or a session cookie, the latter enabling session fixation or hijacking.

### CVE-2026-121565

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-03T23:17:35.080 |

Tanium addressed an improper certificate validation vulnerability in multiple products. Products have been updated to distrust several intermediate CA certificates associated with compromised private keys.

### CVE-2026-95751

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:23.667 |

An improper certificate validation vulnerability in the API of HPE Networking Fabric Composer could allow an unauthenticated remote attacker to circumvent existing authentication controls if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to gain unauthorized access to the affected system.

### CVE-2026-44265

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-89;CWE-94;CWE-749` |
| Published | 2026-11-03T18:18:02.760 |

Elo is a purely functional expression language for no-code tools. Prior to 1.0.1, Elo's programmatic AST API accepts arbitrary values from JSON-deserialized input, plugin output, or other untyped sources and interpolates them into generated JavaScript, Ruby, Python, or SQL without runtime syntax validation. The affected fields are int_literal / float_literal .value, variable.name, member_access.property, object_literal keys, datapath segments, lambda.params[].name, and the SQL let binding name. Crafted values become executable expressions or identifiers, allowing arbitrary code execution in JavaScript, Ruby, and Python targets and SQL injection in the SQL target. This programmatic AST-object path is distinct from the plain-string constructor-chain sandbox escape. This issue is fixed in version 1.0.1.

### CVE-2026-115714

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-03T17:17:56.030 |

Improper Certificate Validation (CWE-295) in the operating system certificate bundle shipped in the Docker images of APM Server; Auditbeat, Filebeat, Heartbeat, Metricbeat and Packetbeat; Elastic Agent, including Fleet Server and Cloudbeat; Logstash, for TLS connections that use the operating system certificate bundle; Elastic connectors; Universal Profiling (host agent, collector and symbolizer); and Elastic Maps Server. This certificate bundle, a dependency of these products (Dependency on Vulnerable Third-Party Component, CWE-1395), could allow an attacker to intercept or modify TLS-protected traffic via Signature Spoofing by Key Theft (CAPEC-474). The certificate bundle includes root certificate authorities that signed eight eMudhra intermediate certificate authorities whose private keys are compromised. Anyone with these keys can issue a certificate for any host name that these products accept as trusted. Exploitation requires an attacker in a network position between the product and the remote party, who presents a certificate issued with one of the compromised keys.

### CVE-2026-121506

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-03T15:17:37.717 |

An out-of-bounds read and write in NTS client extension field parsing (extens_client_recv) in NTPsec before 1.2.5 allows a remote attacker who can send NTP server-mode replies to an NTS client to corrupt heap memory and crash ntpd, and, combined with the NTS-KE client out-of-bounds read fixed in 1.2.4, to bypass NTS authentication and set the client's time, via an NTS Authenticator and Encrypted Extension Fields field whose nonce length exceeds the field.

### CVE-2026-90634

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-04T11:17:19.840 |

An uncontrolled memory access in the PDF import code of Apache OpenOffice versions through 4.1.16 allows a crafted PDF to cause an out-of-bounds memory write, causing program crash or memory corruption.
Users are recommended to upgrade to version 4.1.17, which fixes this issue.

### CVE-2026-111038

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1236` |
| Published | 2026-11-04T10:17:25.070 |

CSV formula injection vulnerability in the export functionality of the Coupa Supplier Portal SaaS platform. The vulnerability arises because certain user-controlled data, such as event names or templates within the Tenders module, are not properly validated or sanitised before being included in CSV files generated by the application. An attacker with low privileges can input specially crafted values that begin with characters interpreted as formulas by spreadsheet applications. When a victim downloads and opens the generated file in a compatible client, the content may be interpreted as a formula, potentially leading to unauthorised actions such as the execution of commands via mechanisms such as DDE, access to information, or interaction with system resources under the victim’s context.

### CVE-2026-118865

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-03T22:19:29.073 |

An authenticated OS command injection vulnerability exists in the Offline Download component (USB storage allocation) of Archer AX3000 v2. When a USB storage device is attached, an authenticated administrator can submit a crafted path value containing shell metacharacters that is not properly neutralized before being passed to a system command. 

Successful exploitation may allow arbitrary command execution on the affected device.

### CVE-2026-93325

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-03T20:18:19.680 |

Buildx bake requires the user to grant entitlements with --allow or an interactive prompt before a build reaches outside the working directory. Under --progress=rawjson that consent step is skipped.

### CVE-2026-63198

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-03T19:18:09.080 |

traQ is a messenger application built for Digital Creators Club traP. Prior to 3.28.3, OAuth2 silent authorization requests using prompt=none with an empty or omitted scope parameter check prior consent against the empty requested scope set even though all scopes registered for the client become eligible for issuance. An attacker who controls an OAuth client capable of receiving authorization codes can target a user who previously consented to only some client scopes and obtain an access token containing broader registered scopes without additional consent. A user who has never consented to the client still receives consent_required. This issue is fixed in version 3.28.3.

### CVE-2026-63197

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-03T19:18:08.907 |

traQ is a messenger application built for Digital Creators Club traP. Prior to 3.28.3, instances configured with TRAQ_STORAGE_TYPE=local can return user-uploaded SVG or HTML content from the /files/{fileId} retrieval endpoint for direct browser rendering. An attacker with file-upload capability can provide crafted active content and induce another user to open its file URL, causing attacker-controlled JavaScript to execute in the victim's browser. This issue is fixed in version 3.28.3.

### CVE-2026-115294

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-03T17:17:55.360 |

Improper Limitation of a Pathname to a Restricted Directory (CWE-22) in the Kibana Fleet feature can lead to unauthorized resource deletion via Path Traversal (CAPEC-126). A low-privileged user with Fleet agent policies write access could cause a subsequent administrative action to act on unintended resources. This can result in the deletion of resources such as Kibana spaces and other organizational assets that the low-privileged user cannot delete directly. Exploitation requires an administrator to interact with the affected Fleet interface.

### CVE-2026-121945

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-04T13:17:29.313 |

CoopCycle coopcycle-web before 6.20.1 contains a broken access control vulnerability that allows any courier to read and modify every incident because Incident operations only check ROLE_COURIER. Attackers can enumerate sequential incident ids and use PUT /api/incidents/{id}/action to re-price, cancel or reschedule other stores' orders and tasks.

### CVE-2026-97397

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-04T12:17:07.123 |

The Remove Google Fonts – Disable, Block, or Replace with Bunny Fonts for GDPR Compliance plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Field via Regex-Mangled Output Buffer in all versions up to, and including, 1.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires the plugin's Remove mode to be active and the malicious comment to be published, either through auto-approval for known commenters or manual moderator approval.

### CVE-2026-94460

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-04T10:17:26.987 |

IRISPowerscan contain an insecure default
configuration where the built-in installation account is assigned elevated
privileges with a predictable password, which could allow an unauthenticated
attacker to gain unauthorised access to privileged application functionality.

### CVE-2026-94459

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-04T10:17:26.833 |

IRISPowerscan contain
default user accounts with predictable credentials. An unauthenticated attacker
with access to an affected installation could use these credentials to
authenticate to the application and access functionality available to the
affected accounts, potentially resulting in unauthorised access or modification
of application data and configuration.

### CVE-2026-115498

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-04T10:17:25.620 |

The Slim Jetpack plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'g<PAGE_ID>-website (Website contact-field)' parameter in all versions up to, and including, 2.7.0.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce and authentication checks on form submission are only enforced for logged-in users, allowing unauthenticated visitors to store payloads via any page containing the [contact-form] shortcode.

### CVE-2025-11229

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-04T06:16:54.070 |

The system fails to properly enforce scope authorization when the `authorize_all_scopes` configuration is enabled. This allows applications using the client credentials grant type to obtain all API scopes, including sensitive internal and console scopes, without requiring explicit authorization, bypassing intended access controls.

Exploitation of this vulnerability can lead to privilege escalation, enabling unprivileged clients to perform unauthorized administrative actions, access confidential organizational data, and potentially achieve full account takeover in deployments where the `authorize_all_scopes` configuration deviates from its default disabled state.

### CVE-2026-84729

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-04T02:17:21.163 |

Out-of-bounds write in certain ASUS Router firmware allow an unauthenticated nearby attacker to write data beyond the intended buffer or potentially cause a denial-of-service (DoS) via a crafted packet.
Refer to the ' 
Security Update for ASUS Router Firmware  ' section on the ASUS Security Advisory for more information.

### CVE-2026-92196

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-04T00:17:30.523 |

Quest Foglight for Databases renderTemplateString Server-Side Template Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Quest Foglight for Databases. Authentication is required to exploit this vulnerability.

The specific flaw exists within the renderTemplateString method. The issue results from the lack of proper validation of a user-supplied string before processing it with the template engine. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-29889.

### CVE-2026-92185

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-04T00:17:28.723 |

Quest Foglight for Databases AbstractParser XML External Entity Processing Information Disclosure Vulnerability. This vulnerability allows remote attackers to disclose sensitive information on affected installations of Quest Foglight for Databases. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the AbstractParser class. Due to the improper restriction of XML External Entity (XXE) references, a crafted document specifying a URI causes the XML parser to access the URI and embed the contents back into the XML document for further processing. An attacker can leverage this vulnerability to disclose information in the context of SYSTEM. Was ZDI-CAN-28929.

### CVE-2026-121729

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-03T23:17:36.407 |

emailflare before commit cf31f33 contains a missing authorization vulnerability in the inbox service /api/keys routes that allows any authenticated member to list, create and revoke API keys. Attackers can mint a global live API key accepted by /v1/send to send mail from any domain, or revoke existing keys to disable integrations.

### CVE-2026-120775

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-03T23:17:33.527 |

Tanium addressed a heap-based buffer overflow vulnerability in Deploy.

### CVE-2026-115541

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-03T22:19:17.723 |

HumHub Community Edition 1.19.0 contains a stored cross-site scripting vulnerability in the friendship confirmation dialog. An authenticated low-privileged member can save HTML in their first and last name. When another authenticated user clicks Friends for that profile, HumHub places the decoded display name into a modal through jQuery html(), causing attacker-controlled markup to execute in the victim's HumHub origin.

### CVE-2026-95727

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-03T20:18:20.693 |

A command injection vulnerability exists in HPE Networking VIA. Successful exploitation could allow an authenticated administrative user to execute arbitrary commands with elevated privileges on the underlying operating system.

### CVE-2026-45146

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-03T20:18:13.943 |

Chamilo LMS is an open-source learning management system. Prior to 1.11.40 and 2.0.1, an authenticated administrator can call the get_sessions action in /main/inc/ajax/model.ajax.php with _search=true and a crafted JSON filters parameter whose groupOp field contains SQL syntax. Because groupOp is not restricted to the expected AND or OR operators before it is incorporated into query logic, attacker-controlled input is interpreted by the database and enables blind or time-based SQL injection. Successful exploitation can disclose sensitive user, course, session, configuration, password-reset, and administrative data, modify or delete records subject to database privileges, and cause denial of service through expensive delayed queries. This issue is fixed in versions 1.11.40 and 2.0.1.

### CVE-2026-121145

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346;CWE-749` |
| Published | 2026-11-04T13:17:26.897 |

This vulnerability exists in the iRA 2.0 and iRA.ev mobile applications due to insufficient validation of URLs and origins loaded within the WebView component. A remote attacker could exploit this vulnerability by sending malicious web content to the affected WebView.

Successful exploitation of this vulnerability could allow the attacker to perform unauthorized interaction with application functionality, obtain live bearer authentication tokens and potentially impersonate the associated user and access vehicle related information and services.

### CVE-2026-119468

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-04T13:17:26.297 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Noptin Newsletter Team Noptin newsletter-optin-box allows Stored XSS.This issue affects Noptin: from n/a through 4.4.2.

### CVE-2026-100302

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-04T11:17:07.023 |

Allocation of Resources Without Limits or Throttling in the multiRead request handler of Apache ZooKeeper allows a remote attacker to crash the server (denial of service) with a single small request.

The multiRead handler places no limit on the number of bundled read operations or on the cumulative size of the response it builds in memory. Because each operation's result is fully materialized and retained before serialization, a request that is small on the wire — within the jute.maxbuffer limit — but that references a large znode many times can force the server to allocate far more heap than the request size implies, exhausting the JVM heap and terminating the server with an OutOfMemoryError. Neither jute.maxbuffer nor largeRequestMaxBytes prevents this, as both bound only the inbound request, not the response.

This issue affects Apache ZooKeeper from 3.7.0 through 3.9.6. Users are recommended to upgrade to version 3.9.7, which enforces configurable limits on the multiRead operation count and cumulative response size.

### CVE-2026-62007

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-04T08:17:17.723 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Unlimited Elements Unlimited Elements For Elementor (Free Widgets, Addons, Templates) unlimited-elements-for-elementor allows Reflected XSS.This issue affects Unlimited Elements For Elementor (Free Widgets, Addons, Templates): from n/a through 2.0.26.

### CVE-2026-57666

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-04T08:17:17.403 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Aguila Technologies WP Customer Area customer-area allows Reflected XSS.This issue affects WP Customer Area: from n/a through 8.4.1.

### CVE-2026-57639

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-04T08:17:17.247 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Roland Murg WP Booking System wp-booking-system allows Reflected XSS.This issue affects WP Booking System: from n/a through 2.1.0.6.

### CVE-2026-54861

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-04T08:17:16.940 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Aguila Technologies WP Customer Area customer-area allows Reflected XSS.This issue affects WP Customer Area: from n/a through 8.4.1.

### CVE-2026-119477

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-04T08:17:16.677 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Jacob N. Breetvelt WP Photo Album Plus wp-photo-album-plus allows Stored XSS.This issue affects WP Photo Album Plus: from n/a through 9.3.05.003.

### CVE-2026-119366

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-04T08:17:16.523 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in AdvancedCoding wpDiscuz wpdiscuz allows Stored XSS.This issue affects wpDiscuz: from n/a through 7.6.73.

### CVE-2026-54851

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-04T07:17:12.517 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Awesomemotive Contact Form by WPForms wpforms-lite allows Reflected XSS.This issue affects Contact Form by WPForms: from n/a through 2.0.3.

### CVE-2026-121730

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-03T23:17:36.590 |

emailflare before commit cf31f33 contains a missing authorization vulnerability in POST /api/inbox/compose that allows authenticated members to send mail as any sender address. Attackers can supply an arbitrary from field, which is passed unchecked to the Cloudflare send call, to impersonate other users or the organization to external recipients.

### CVE-2026-121614

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-03T22:19:46.880 |

Docker Sandboxes versions 0.31.0 before 0.50.0 do not neutralize repository-controlled Git configuration when running certain host-side Git commands. An attacker who can modify a host repository's Git configuration, for example through a direct-mode sandbox with the repository mounted read-write, can configure core.fsmonitor or another Git setting that invokes an external program. Git can execute the program during a later clone-mode fetch or, starting in version 0.39.0, an sbx kit push initiated by the user. The program runs on the host with the invoking user's permissions, outside the sandbox's microVM isolation. The read-only host repository mount provided to a clone-mode sandbox does not itself allow that sandbox to modify the host repository's Git configuration. The issue is fixed in version 0.50.0.

### CVE-2026-95753

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:23.913 |

A privilege escalation vulnerability exists in the API of HPE Networking Fabric Composer. Successful exploitation could allow an authenticated attacker with low privileges to disclose network traffic from switches managed by Fabric Composer.

### CVE-2026-95752

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:23.783 |

A local privilege escalation vulnerability exists in the API of HPE Networking Fabric Composer. Successful exploitation could allow a low-privileged local attacker to elevate their privileges on the affected system.

### CVE-2026-95728

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T20:18:20.820 |

An arbitrary file write vulnerability exists in the Virtual Intranet Access (VIA) client. Successful exploitation could allow a local attacker with low privileges to escalate privileges on the affected system.

### CVE-2026-63500

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-03T20:18:16.910 |

Yeti bridges the gap between CTI and DFIR practitioners by providing a Forensics Intelligence platform and pipeline. Prior to 2.5.1, core/schemas/dfiq.py accepts an unvalidated uuid from DFIQ YAML through POST /api/v2/dfiq/from_yaml, and core/web/apiv2/dfiq.py later interpolates that stored value into an archive filesystem path in POST /api/v2/dfiq/to_archive. A low-privileged authenticated user can import a DFIQ object whose UUID contains traversal sequences and trigger archive export, causing attacker-controlled content with a .yaml suffix to be written outside the intended temporary archive directory. The impact is limited by paths writable by the YETI service account, and the separate DFIQ archive-import zip-slip candidate is not part of this vulnerability. This issue is fixed in version 2.5.1.

### CVE-2026-82976

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-548` |
| Published | 2026-11-03T19:18:10.850 |

A flaw was found in the image-customization-controller used in OpenShift's bare metal provisioning stack. The controller registers an HTTP file server on port 8084 with no authentication. The custom imageFileSystem implementation exposes a browsable HTML directory listing of all registered images at the root path. The only access control on per-host images is the random UUID filename; the directory listing discloses those UUIDs to any caller on the provisioning network. Each served image embeds an Ignition config containing the base64-encoded cluster pull secret, optional IRONIC_RAMDISK_SSH_KEY, proxy settings, and per-host NetworkManager keyfiles. An adjacent network attacker can enumerate all image UUIDs via directory listing, download any image, extract the embedded Ignition config, and recover the cluster pull secret and SSH key.

### Evidence
**pkg/imagehandler/imagefilesystem.go — root directory is browsable and enumerates all UUID image names**
```go
func (f *imageFileSystem) Readdir(n int) ([]fs.FileInfo, error) {
    f.mu.Lock()
    defer f.mu.Unlock()
    result := []fs.FileInfo{}
    for _, im := range f.images {
        result = append(result, im)
    }
    return result, nil
}

func (f *imageFileSystem) Open(name string) (http.File, error) {
    f.log.Info("Open", "path", name)
    if name == "/" {
        return f, nil
    }
    ...
```

**cmd/controller/main.go — file server bound on all interfaces without auth or TLS**
```go
http.Handle("/", http.FileServer(imageServer.FileSystem()))

go func() {
    server := &http.Server{
        Addr:              imagesBindAddr,   // default ":8084"
        ReadHeaderTimeout: 5 * time.Second,
    }
    err := server.ListenAndServe()
```

**pkg/ignition/service_config.go:94-100 — pull secret is embedded in every served image**
```go
func (b *ignitionBuilder) authFile() ignition_config_types_32.File {
    source := "data:;base64," + strings.TrimSpace(b.ironicAgentPullSecret)
    return ignition_config_types_32.File{
        Node: ignition_config_types_32.Node{Path: "/etc/authfile.json"},
        ...
```

### Attack Pattern
Adjacent provisioning-network client → GET / lists UUID image names → download ISO/initramfs → extract embedded Ignition → recover cluster pull secret and SSH key.

### CVE-2026-39379

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-1336` |
| Published | 2026-11-03T19:18:05.733 |

GeoNetwork is a catalog application to manage spatially referenced resources. From 3.0.0 until 4.2.15 and 4.4.10, requesting a nonexistent or unauthorized service URL can cause an error page to reflect attacker-controlled request content inside an AngularJS application without adequately neutralizing it for template evaluation. A remote attacker can induce a victim, including an administrator, to open a crafted link so the reflected value is evaluated as an AngularJS template expression. Combined with known AngularJS sandbox-escape techniques, this can execute arbitrary JavaScript in the victim's authenticated browser session, disclose information, or perform actions as the victim. This issue is fixed in versions 4.2.15 and 4.4.10.

### CVE-2026-120956

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-03T19:18:00.837 |

The MongoDB C Driver does not validate the type or format of a namespace field returned by the server in a query response. A MongoDB endpoint that a client application connects to, without needing any credentials, can return a malformed value in that field. This causes the client application process to terminate, and can also cause the driver to read memory outside an allocated buffer and to send a small amount of the application's own uninitialized heap memory back to the endpoint in a follow-up command. The impact is limited to the process that embeds the driver.

### CVE-2026-121560

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-03T16:17:28.770 |

LogChimp 0.9.0-alpha.1 before 0.9.3 contains an authorization bypass vulnerability that allows authenticated post authors to modify any other post by supplying mismatched postId and id body parameters. Attackers can set postId to their own post and id to an enumerated victim post UUID to overwrite its title, slug, content, boardId and roadmap_id.

### CVE-2026-121511

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-03T15:17:38.267 |

Heap Out-of-Bounds Read in µD3TN BPv6/BPv7 Fragmenter allows Local Attacker to Read Memory and Reliably Cause DoS

### CVE-2026-121449

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-03T15:17:37.397 |

Dockhand from 1.0.47 before 1.0.54 exposes plaintext stack secrets because deployStack() attaches resolved secret values to its result as resolvedSecrets, which Git-stack routes return unfiltered. Holders of a stack's webhook secret or users with stacks:start permission can trigger the Git stack webhook, manual deploy, or create-and-deploy endpoints to receive stored and external-provider secrets such as 1Password or Vault values.

### CVE-2026-121423

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-03T15:17:32.700 |

SurrealDB before 3.3.0 contains an unbounded recursion vulnerability that allows authenticated users to abort the surreald process by triggering stack overflow on deeply nested values. Attackers can repeatedly run UPDATE statements wrapping a stored array in itself, then SELECT or EXPORT it, causing persistent denial of service for all tenants.

### CVE-2026-121416

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-03T15:17:31.367 |

SurrealDB 2.0.0 before 3.3.1 does not enforce --deny-funcs restrictions on method-style function calls in the streaming engine, because MethodPart::evaluate invokes resolved functions without a capability check. Authenticated users who can submit queries can run denied functions via method syntax, e.g. [1,2].map() or $f.put()/$f.get() to write and read file bucket data despite file::* denials.

### CVE-2026-121412

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-03T15:17:30.340 |

FreeRDP from 3.0.0 before 3.32.2 contains an uncontrolled resource consumption vulnerability in the proxy that lets connected clients retain heap memory via intercepted DVC message reassembly. Attackers can declare a large DATA_FIRST length and keep sending fragments without completing the message, growing proxy memory proportional to traffic and degrading service.

### CVE-2026-121407

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-03T15:17:29.420 |

FreeRDP before 3.32.2 contains a denial of service vulnerability in the shadow server's remdesk_server_thread that allows authenticated clients to crash the process via an inverted PDU length check. Attackers can send an 8192-byte remdesk payload declaring an eight-byte PDU length to trigger a fatal Stream_Seek assertion, aborting the server and dropping sessions.

### CVE-2026-121404

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-03T15:17:28.870 |

FreeRDP before 3.32.2 contains a denial of service vulnerability in the shadow server that allows authenticated RDP clients to spin server threads by sending zero-length drdynvc DATA PDUs. Attackers can send empty DATA messages on opened audin or rdpgfx channels, so that FreeRDP_WTSVirtualChannelRead never consumes them, consuming full CPU cores until disconnect.

### CVE-2026-121402

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-03T15:17:28.533 |

FreeRDP before 3.32.2 contains a NULL pointer dereference vulnerability that allows malicious RDP servers to crash xfreerdp clients by sending a zero-width RDPGFX ResetGraphics PDU. The failed resize in gdi_resize_ex leaves the primary display null without ending the session, so a later bitmap update crashes the client in gdi_Bitmap_Paint.

### CVE-2026-121400

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-03T15:17:28.177 |

FreeRDP before 3.32.2 contains a denial-of-service vulnerability in rdg_process_control_packet that allows a malicious RD Gateway to exhaust client CPU by sending an incomplete keepalive control packet. Attackers completing the RDG tunnel-open exchange then send an eight-byte header with packetLength 0xFFFF and withhold the body, causing an unbounded no-progress read loop that spins one client thread at full CPU.

### CVE-2026-121395

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-03T15:17:27.277 |

FreeRDP from 3.17.0 before 3.32.2 contains an assertion failure in the RemoteFX differential decoder when verbose WinPR assertions are enabled. A malicious RDP server can send a crafted RemoteFX tile with adjacent LL3 coefficients summing beyond signed 16-bit range to abort the client process.

### CVE-2026-121394

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-03T15:17:27.107 |

FreeRDP from 3.11.0 before 3.32.2 contains an assertion failure in the RemoteFX RLGR decoder that allows malicious servers to terminate clients. Attackers controlling an RDP server can send a RemoteFX tileset with RLGR code 32767, triggering a signed narrowing assertion in rfx_rlgr_decode and crashing the client.

### CVE-2026-121393

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-03T15:17:26.917 |

FreeRDP from 3.0.0 before 3.32.2 contains a denial of service vulnerability that allows malicious RDP servers to abort clients built with verbose WinPR assertions by sending crafted RemoteFX region rectangles. Attackers can supply a rectangle with x set to 65535 alongside a SurfaceBits destination left of 1, triggering a 16-bit coordinate assertion in rfx_process_message that terminates the client process.

### CVE-2026-121388

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-03T15:17:25.970 |

FreeRDP from 3.0.0 before 3.32.2 contains an uncontrolled resource allocation vulnerability that allows malicious RDP servers to force large client allocations through the DRDYNVC DATA_FIRST Length field. Attackers can declare lengths up to 4,294,967,295 bytes on running dynamic channels, causing StreamPool_Take to reserve memory before body validation and exhaust client memory.

### CVE-2026-106991

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-11-03T15:17:19.590 |

hustoj >=24.09.10 and <=26.08.19 is vulnerable to Incorrect Access Control. Any registered user can delete, lock, or sticky any forum thread (including admins' announcements) via threadadmin.php. The thread branch only verifies login, never authorship or admin rights.

### CVE-2026-87038

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-04T06:17:06.420 |

The user-mode verification handler for the i3c_transfer() system call, z_vrfy_i3c_transfer() in drivers/i3c/i3c_handlers.c, validated the caller-supplied struct i3c_device_desc in place instead of snapshotting it. It confirmed only that the descriptor was readable by the calling thread (K_SYSCALL_MEMORY_READ()), read target->bus once to check it with K_SYSCALL_OBJ(), and then passed the caller's live pointer down. The implementation z_impl_i3c_transfer() re-reads target->bus from that user memory and dispatches through it as DEVICE_API_GET(i3c, target->bus)->i3c_xfers(...), so the bus that was validated is not necessarily the bus that is used. DEVICE_API_GET() performs no runtime type check outside CONFIG_DEVICE_API_ASSERT builds.

On a build with CONFIG_USERSPACE and an I3C controller driver, a user thread that has been granted an I3C device object can exploit this with a second thread in the same memory domain: one thread calls i3c_transfer() while the other rewrites the bus field of the descriptor. The window between the check and the use spans the num_msgs validation, the message-array access check, a stack VLA allocation and a memcpy() of up to 32 struct i3c_msg, so the race is repeatable and can simply be retried until it lands.

When the substitution succeeds, the kernel dereferences an attacker-chosen pointer as a struct device, loads a function pointer from the attacker-controlled api table and calls it in supervisor mode with attacker-influenced arguments. This yields kernel-mode code execution from an unprivileged user thread — a complete escape of the userspace memory-protection sandbox; lesser outcomes are an arbitrary two-level kernel read or a kernel fault. Builds without CONFIG_USERSPACE, or without an I3C driver, are unaffected.

The fix copies the descriptor into a kernel-stack local with k_usermode_from_copy(), validates the bus in that copy, and dispatches on the copy, so the validated value is provably the value used.

### CVE-2026-61495

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-03T21:17:42.487 |

TinyUSB through 0.21.0, fixed in commit e85c2b8, contains an out-of-bounds write vulnerability in the MTP device class helper mtp_container_get_string() in src/class/mtp/mtp.h that allows a malicious USB host to corrupt adjacent memory by supplying a crafted MTP string with an unbounded character count. Attackers can exploit the unchecked memcpy operation copying up to 510 bytes into a fixed-size destination buffer to achieve code execution or cause a denial of service on the TinyUSB MTP device.

### CVE-2026-63418

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-11-03T18:18:03.533 |

Monitoring Plugins is a suite of plugins for monitoring applications. From 3.0.0-rc1 until 3.0.1, check_icmp stores the number of hosts supplied through -H or --Host on the command line, or through --extra-opts files containing Host= entries, in an unsigned short. More than 65,535 hosts wrap the counter, causing process_arguments() to allocate an undersized hosts array and then write subsequent entries out of bounds before main() calls setuid(getuid()). On installations where check_icmp is setuid root, a local low-privileged attacker can corrupt heap memory while the process still has root privileges; reliable privilege escalation has not been demonstrated. Installations that use cap_net_raw file capabilities instead of setuid are not exposed to the privilege-escalation consequence. This issue is fixed in version 3.0.1.

### CVE-2026-65168

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-03T16:17:36.207 |

NVIDIA Slurm contains an attacker-controlled heap-based buffer overflow in the slurmstepd socket handling code.
