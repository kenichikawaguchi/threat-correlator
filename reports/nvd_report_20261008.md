# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-07 15:00 UTC
- **対象期間**: `2026-10-06T15:00:44.000Z` 〜 `2026-10-07T15:00:51.000Z`
- **重要CVE数**: 309 件（Critical 9.0+: 79 件 / High 7.0〜: 230 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** と非常に多く、特に **Dell Container Storage Modules 系列** と **HPE/Aruba ClearPass Policy Manager 系列** に集中しています。  
- 多くは **認証なしでリモートからコード実行・権限昇格** が可能になる「Missing Authentication」や「Use‑After‑Free」系の脆弱性。  
- Web 管理 UI に対する **SQL インジェクション**、**パス・トラバーサル**、**認証バイパス** が続出し、管理者権限取得が容易になる点が顕著です。  
- OSS のフロントエンドフレームワーク（Quasar、Handlebars、Backstage）や **Chrome（Android）** でも深刻なリモートコード実行が報告され、フロントエンド側のサプライチェーンリスクが再浮上しています。  

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑105857** | 10.0 | Payload CMS の `@payloadcms/plugin-form-builder` でリモートコード実行 (RCE) | フォーム送信だけで任意コードがサーバ上で実行されるため、**全ての Payload CMS デプロイ** が即座に危険。マルチテナント環境では他テナントへの横展開も可能。 |
| **CVE‑2026‑63692 / CVE‑2026‑63688** (同一製品) | 10.0 | Dell Container Storage Modules (CSM) の gRPC サーバで認証なしのクリティカル機能にアクセス | **認証不要** でストレージ管理権限を取得でき、クラスタ全体のデータ破壊・情報漏洩につながる。Dell のハイブリッドクラウド環境を利用している企業は即時対策が必須。 |
| **CVE‑2026‑79798** | 9.9 | ClearPass Policy Manager の管理 UI で SQL インジェクション (認証済み低権限) | 認証は必要だが **低権限アカウント** で任意 SQL が実行可能。データベースの改竄・認証情報抽出が容易で、内部脅威シナリオで重大。 |
| **CVE‑2026‑106419** | 9.6 | Chrome Android (ANGLE) の Use‑After‑Free によるリモートコード実行 | Android デバイス上の Chrome で **任意の HTML** を閲覧させるだけでサンドボックス突破が可能。モバイルユーザーが多い組織は即時パッチ適用が必要。 |
| **CVE‑2026‑106102** | 10.0 | Quasar Framework (SSR) の `getHead()` で HTML エスケープ不備 → XSS | SSR 環境で **任意スクリプト** が埋め込めるため、フロントエンドアプリ全体が攻撃対象に。Vue.js エコシステムを利用する多数の SaaS が影響を受ける可能性。 |

> **共通点**：すべて「認証不要」または「低権限で実行可能」かつ「リモートから直接コード実行」や「権限昇格」を引き起こす点で、**攻撃者が横展開しやすい** ことが最大のリスクです。

## 3. 推奨アクション  

### 3.1 パッケージ・製品のバージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 修正バージョン (最低) | 対応期限目安 |
|-------------------|-------------------|----------------------|--------------|
| **Payload CMS – plugin‑form‑builder** | < 3.90.0 (または 4.0.0‑canary.34 未満) | 3.90.0 以上、もしくは 4.0.0‑canary.34 以降 | 直ちに |
| **Dell Container Storage Modules (CSM)** | < 1.18.0 | 1.18.0 以上 | 1 週間以内 |
| **Dell Container Storage Modules – CSM‑Authorization‑Storage (gRPC)** | < 1.18.0 | 1.18.0 以上 | 1 週間以内 |
| **HPE/Aruba ClearPass Policy Manager** | すべての 2026 系リリース (具体的バージョンはベンダー提供のパッチ) | 最新パッチリリース (2026‑Q3 以降) | 2 週間以内 |
| **Quasar Framework** | < 2.22.0 | 2.22.0 以上 | 1 週間以内 |
| **Handlebars** | 4.0.0‑4.7.10 | 4.7.11 以上 | 1 週間以内 |
| **Backstage** | < 3.3.1 / 3.4.1 / 4.0.3 / 4.1.0 | 各系列の最新パッチ (2026‑04 以降) | 2 週間以内 |
| **IBM Langflow OSS** | 1.0.0‑1.12.2 | 1.12.3 以上 | 1 週間以内 |
| **Google Chrome (Android)** | < 155.0.8059.39 | 155.0.8059.39 以上 | 直ちに（Chrome の自動更新を有効化） |
| **Dell System Update** | < 2.3.0.0 | 2.3.0.0 以上 | 1 週間以内 |

### 3.2 共通的な防御策
1. **脆弱性情報の自動取得**  
   - NVD、各ベンダーのセキュリティアドバイザリ、GitHub Security Advisories を CI に組み込み、**新規 CVE が公開されたら即時通知**できる仕組みを構築。  

2. **最小権限の原則 (PoLP) の徹底**  
   - ClearPass の管理アカウントや Payload CMS の API キーは **最低限の権限** に絞り、不要な権限は即削除。  

3. **ネットワーク分離とゼロトラスト**  
   - CSM の gRPC エンドポイントは内部ネットワークに限定し、**IP アクセスコントロールリスト (ACL)** を適用。  
   - 外部からの直接アクセスが不要な管理 UI (ClearPass, Dell System Update) は **VPN / Zero‑Trust Access** のみ許可。  

4. **Web アプリケーションファイアウォール (WAF)**  
   - ClearPass、Payload CMS、Quasar SSR のフロントエンドに対し、**SQLi、XSS

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-106102

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-10-06T17:17:24.270 |

Quasar Framework is a framework for building high-performance Vue.js user interfaces. Prior to 2.22.0, the SSR-only getHead() serializer in ui/src/plugins/meta/Meta.js used getAttr() to interpolate values supplied through useMeta() into title, meta, link, and script markup without HTML text or quoted-attribute encoding. injectServerMeta() appended that output to the raw server-rendered response. An attacker who can influence dynamic page metadata, such as a post title, product name, excerpt, or display name, can terminate the intended HTML context and inject executable markup before hydration. The client-side apply() path is not affected because it uses DOM APIs that encode attributes. This issue is fixed in version 2.22.0.

### CVE-2026-105857

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-1321` |
| Published | 2026-10-06T17:17:21.710 |

Payload is a free and open source headless content management system. In @payloadcms/plugin-form-builder versions before 3.90.0 and canary versions before 4.0.0-canary.34, an attacker can craft a form submission that executes code remotely on the server. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-63692

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-06T15:17:19.007 |

Dell Container Storage Modules, versions prior to 1.18.0, contain(s) a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-63688

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-06T15:17:18.890 |

Dell Container Storage Modules (CSM), versions prior to v1.18.0, contains a Missing Authentication for Critical Function vulnerability in the csm-authorization-storage gRPC server. An unauthenticated remote attacker could potentially exploit this vulnerability, leading to unauthorized access to storage backend administrator credentials for all registered storage arrays.

### CVE-2026-79798

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:31.310 |

SQL injection vulnerabilities in the web-based management interface of ClearPass Policy Manager could allow a low-privileged authenticated remote attacker to conduct SQL injection attacks against the ClearPass Policy Manager instance. Successful exploitation could allow an attacker to run arbitrary database commands.

### CVE-2026-67269

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-06T15:17:19.130 |

Dell Container Storage Modules (CSM) Operator, versions prior to 1.18.0 contains an Improper Privilege Management vulnerability in the ContainerStorageModule Custom Resource reconciler. A low privileged remote attacker could potentially exploit this vulnerability, leading to escalation of privileges and gaining root-level access on cluster nodes.

### CVE-2026-105192

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-502` |
| Published | 2026-10-07T10:17:32.647 |

LMCache multiprocess mode, also called distributed mode, opens an unauthenticated ZeroMQ ROUTER so worker processes can register and share KV cache blocks. Messages on that socket are msgpack. Extension code 1 is passed to DeviceIPCWrapper.Deserialize, which calls pickle.loads, while the server is still decoding request arguments and before the handler runs. A single unauthenticated ZMQ DEALER message to the transport port (default 5555) therefore executes code as the user the LMCache process runs as. Official container images run that process as root. The transport binds to localhost unless the operator sets a routable address with --host, which is how multi-node deployments let peers connect.

### CVE-2026-93674

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T01:16:35.187 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-104334

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T01:16:34.223 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote attacker to execute arbitrary code due to improper control of code generation.

### CVE-2026-79805

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:32.013 |

An authenticated path traversal vulnerability exists in ClearPass Policy Manager. Successful exploitation could allow an attacker to read and modify certain files on the underlying operating system.

### CVE-2026-79801

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:31.667 |

A missing integrity verification vulnerability in the client agent software of HPE Networking ClearPass Policy Manager could allow an unauthenticated remote attacker to introduce untrusted code. Successful exploitation could allow an attacker to execute arbitrary code on the affected client system.

### CVE-2026-79796

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:31.083 |

Vulnerabilities have been identified in the affected interface of ClearPass Policy Manager that could potentially allow an unauthenticated remote attacker to circumvent existing authentication controls. Successful exploitation could allow an attacker to gain unauthorized access to the affected system.

### CVE-2026-76754

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:30.853 |

A vulnerability in an affected interface of ClearPass Policy Manager could allow an unauthenticated remote attacker to conduct SQL injection attacks against the ClearPass Policy Manager instance. Successful exploitation could allow an attacker to run arbitrary database commands.

### CVE-2026-76753

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:30.740 |

A format string vulnerability in an affected service interface of HPE Networking ClearPass Policy Manager could allow an unauthenticated remote attacker to corrupt process memory. Successful exploitation could allow an attacker to execute arbitrary code.

### CVE-2026-76752

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:30.623 |

Authentication bypass vulnerabilities exist in the web-based management and API interfaces of HPE Networking ClearPass Policy Manager. Successful exploitation could allow an unauthenticated remote attacker to circumvent existing authentication controls and gain administrative access to the affected system.

### CVE-2026-76751

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:30.513 |

A missing integrity verification vulnerability exists in the OnGuard agent of ClearPass Policy Manager. Successful exploitation could allow an unauthenticated, remote attacker to execute arbitrary code on the affected endpoint with the elevated privileges of the agent.

### CVE-2026-76750

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:30.397 |

Deserialization of untrusted data vulnerabilities exist in the web interface of HPE Networking ClearPass Policy Manager. Successful exploitation could allow an unauthenticated remote attacker to execute arbitrary code on the affected system.

### CVE-2026-76744

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:29.727 |

Buffer overflow vulnerabilities exist in the affected interface of AOS-S. Successful exploitation could allow an unauthenticated remote attacker to execute arbitrary code.

### CVE-2026-76743

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:29.603 |

A vulnerability have been identified in the management interface of AOS-S that could potentially allow an unauthenticated remote attacker to circumvent existing authentication controls if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to gain unauthorized access to the affected system.

### CVE-2026-76742

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-06T20:17:29.490 |

Authentication bypass vulnerabilities exist in the web management interface of AOS-S. Successful exploitation could allow an unauthenticated remote attacker to gain unauthorized access to the affected system.

### CVE-2026-106446

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-843` |
| Published | 2026-10-06T20:17:26.430 |

Handlebars provides the power necessary to let users build semantic templates. From 4.0.0 until 4.7.10, Handlebars.compile() and Handlebars.precompile() accept pre-parsed AST objects while validating only selected PathExpression, NumberLiteral, and BooleanLiteral values. This issue bypasses the AST validation introduced in version 4.7.9 for CVE-2026-33937. An attacker who can supply an object instead of a template string can place JavaScript expressions in unchecked values such as Program.blockParams.length, a non-PathExpression parameter depth, a non-string StringLiteral.value, or a non-string PathExpression.original. The compiler emits those values into generated JavaScript, causing code execution in the server process when compile output renders or wherever precompile output is loaded. Applications that pass only template strings are not affected. This issue is fixed in version 4.7.10.

### CVE-2026-55330

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:14.810 |

In BluetoothCccHandlerCallbackImpl of bluetooth_ccc.cc, there is a possible use-after-free due to a logic error in the code. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-105859

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-10-06T17:17:21.987 |

Payload is a free and open source headless content management system. In versions before 3.90.0 and canary versions before 4.0.0-canary.34, an attacker can submit a request to a specific update endpoint that modifies collection documents without enforcing collection or field-level access control when orderable is enabled on a collection or join field. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-105845

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T16:17:06.540 |

Payload is a free and open source headless content management system. In versions from 3.0.0 before 3.88.0 and canary versions before 4.0.0-canary.27, an untrusted user who can query readable collections through dynamic filters or joins can submit a request that causes SQL injection in the SQLite and Postgres adapters. This issue is fixed in versions 3.88.0 and 4.0.0-canary.27.

### CVE-2026-61421

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-06T15:17:18.767 |

Dell Container Storage Modules, versions prior to 1.18.0, contain(s) an Use of Hard-coded Credentials vulnerability in the CSM Authorization. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-54472

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-06T15:17:18.483 |

Dell Container Storage Modules, versions prior to 1.18.0, contain(s) an Use of Hard-coded Credentials vulnerability in the csm-docs. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Information disclosure.9.8

### CVE-2026-106501

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-200;CWE-201` |
| Published | 2026-10-06T22:17:05.217 |

Backstage is an open framework for building developer portals. Prior to 3.3.1, 3.4.1, 4.0.3 and 4.1.0, the @backstage/plugin-scaffolder-backend package is affected by sensitive information exposure in scaffolder. An authenticated Backstage user who can read another user's Scaffolder task may receive internal execution data. In deployments where that data contains credentials for an external service, this may permit disclosure and unauthorized changes in that external service. This issue is fixed in versions 3.3.1, 3.4.1, 4.0.3 and 4.1.0.

### CVE-2026-76745

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:29.840 |

Memory corruption vulnerabilities exist in AOS-S that are reachable by an unauthenticated adjacent attacker. Successful exploitation could allow an attacker to execute arbitrary code.

### CVE-2026-86360

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-06T19:18:16.430 |

Dell System Update, versions prior to 2.3.0.0, contains an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Filesystem access for attacker. This vulnerability is considered critical because it can be leveraged by an unauthenticated attacker to execute arbitrary code with root privileges. Successful exploitation may allow complete compromise of the vulnerable application and underlying operating system. Dell recommends customers upgrade at the earliest opportunity.

### CVE-2026-106419

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:11.670 |

Use after free in ANGLE in Google Chrome on on Android prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106417

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-06T19:18:11.433 |

Integer overflow in Media in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106414

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-06T19:18:11.090 |

Improper input validation in Mobile in Google Chrome on on iOS prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106401

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-06T19:18:09.617 |

Out of bounds write in Media in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106382

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:07.400 |

Use after free in Chromecast in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-106375

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-459` |
| Published | 2026-10-06T19:18:06.630 |

Incomplete cleanup in Dawn in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106372

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T19:18:06.300 |

Incorrect authorization in UI in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106358

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:04.740 |

Use after free in Navigation in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-106329

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T19:18:01.243 |

Incorrect authorization in FileSystem in Google Chrome prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106323

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T19:18:00.567 |

Missing authorization in Chrome for iOS in Google Chrome on on iOS prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106298

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:57.807 |

Use after free in Chrome Tabs in Google Chrome on on Mac prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106281

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:55.827 |

Use after free in Tint in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106241

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T19:17:51.030 |

Incorrect authorization in Search in Google Chrome on on Android prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106239

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-06T19:17:50.800 |

Integer overflow in WebGL in Google Chrome on on Android prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106234

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:50.250 |

Use after free in Network in Google Chrome prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted Chrome extension. (Chromium security severity: Low)

### CVE-2026-106227

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:49.450 |

Use after free in Core in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106211

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:47.520 |

Use after free in TabStrip in Google Chrome prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106197

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:45.897 |

Use after free in Browser in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-102322

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T19:17:39.420 |

Incorrect Authorization in SiteIsolation in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-67273

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-06T16:17:09.717 |

Dell Container Storage Modules, versions prior to 1.18.0, contain(s) an Improper Neutralization of Special Elements Used in a Template Engine vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2025-64393

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-07T09:17:04.273 |

This vulnerability in Veeam Backup & Replication allows a Backup Viewer to execute arbitrary code as SYSTEM on the backup server.

### CVE-2026-102162

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-06T20:17:11.377 |

On affected Arista Wi-Fi access points with captive portal, or application firewall enabled on at least one SSID, a vulnerability in the wireless gateway service could allow an unauthenticated network-adjacent attacker to send a crafted packet that triggers a stack overflow, resulting in a denial-of-service condition or potentially execute arbitrary code on the device. The wireless gateway service is automatically restarted after a crash, allowing repeated exploitation attempts.

### CVE-2026-96408

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T11:17:20.620 |

A code injection vulnerability exists in the upgrade script of Movable Type, which may allow an unauthenticated attacker to execute an arbitrary Perl script or an SQL query on the affected product.

### CVE-2026-107104

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-07T09:17:05.037 |

This vulnerability exists in the ERP system due to unsafe deserialization of user controlled data in the affected functionality. An unauthenticated remote attacker could exploit this vulnerability by supplying specially crafted data to the vulnerable functionality of the targeted system. 

Successful exploitation of this vulnerability could allow the attacker to execute arbitrary code, manipulate application data or perform other unintended actions on the targeted system.

### CVE-2026-107103

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-07T09:17:04.913 |

This vulnerability exists in the ERP system due to insufficient validation and parameterization of user supplied input in an API endpoint. An unauthenticated remote attacker could exploit this vulnerability by supplying specially crafted input to the vulnerable endpoint.

Successful exploitation of this vulnerability could allow the attacker to perform SQL injection attacks on the targeted system.

### CVE-2026-107102

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-07T09:17:04.780 |

This vulnerability exists in the ERP system due to improper validation of payment callback parameters and inadequate authentication controls in API endpoint. An unauthenticated remote attacker could exploit this vulnerability by manipulating the parameter to cause the application to establish an authenticated session for an arbitrary user without valid payment verification.

Successful exploitation of this vulnerability could allow the attacker to bypass authentication and gain unauthorized access to other user accounts on the targeted system.

### CVE-2026-103416

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-07T09:17:04.647 |

Out-of-bounds write via the TLS 1.3 handshake message cache in NetX Duo in Eclipse ThreadX NetX Duo 6.5.1.202602 allows a handshake message larger than the cache writes past it and on into the rest of the session control block, which holds pointers. A malicious or compromised server can make a TLS 1.3 client produce such a message before certificate authentication completes, so no server certificate is needed to reach it.

### CVE-2026-102782

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-07T09:17:04.527 |

Joomla Extension - ordasoft.com - Unauthenticated SQL injection in OrdaSoft Simple Membership < 7.4.0 - site/simplemembership.php dispatches task=checkLoginPass with no authentication or access control check of any kind. The handler reads a login request parameter through Joomla’s generic, non-sanitizing input filter, which strips HTML/script tags but never touches quotes or SQL syntax, and concatenates it directly into a query string with no escaping or parameterization:

### CVE-2026-59346

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-07T06:16:35.543 |

VMware Workstation and Fusion contain an integer-overflow vulnerability. A malicious actor with local administrative privileges on a virtual machine with VMXNET3 virtual network adapter may exploit this issue to execute code on the host.

Affected versions:
- VMware Workstation: 25H2, 26H1 (fixed in 26H1u1)
- VMware Fusion: 25H2, 26H1 (fixed in 26H1u1)

### CVE-2026-19572

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-07T04:18:09.053 |

A security vulnerability has been identified in FlexNet Publisher lmadmin. The vulnerability exists in a SOAP handler, where a hardcoded authentication bypass could allow an unauthenticated user to obtain a privileged administrator session without providing valid credentials.

### CVE-2026-14911

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-07T03:16:58.670 |

Improper Neutralization of Input During Web Page Generation (“Cross-site Scripting”) in ASUS router modules allows a remote attacker to read DOM information, modify router settings, and cause a denial-of-service condition when an authenticated user visits a crafted URL.Refer to the '
Security Update for ASUS Router Firmware  ' section on the ASUS Security Advisory for more information.

### CVE-2026-19386

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-07T02:16:57.883 |

A stack-based buffer overflow in the ASUS router modules allows an authenticated nearby user to execute arbitrary code via a crafted configuration file upload that exceeds the expected buffer size.Refer to the ' Security Update for ASUS Router Firmware  ' section on the ASUS Security Advisory for more information.

### CVE-2026-76746

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:29.957 |

An unauthenticated buffer overflow vulnerability exists in AOS-S. Successful exploitation could allow an unauthenticated adjacent attacker to expose sensitive memory contents and cause a denial of service on the affected device.

### CVE-2026-102159

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-06T20:17:10.963 |

An access-control flaw in the CV-CUE backend may allow an unauthenticated network attacker to access functionality intended only for internal services. Successful exploitation may expose sensitive location information or disrupt affected services.

### CVE-2026-101158

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T20:17:10.127 |

A missing input validation vulnerability in the Fileserver upload API allows an authenticated attacker with file upload privileges to execute stored cross-site scripting (XSS). Successful exploitation could enable the attacker to hijack another CloudVision user's web session, potentially granting full access to their account and administrative permissions.

### CVE-2026-101157

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T20:17:09.983 |

A stored cross-site scripting (XSS) vulnerability may allow an unauthenticated attacker with adjacent-network access to inject malicious content that executes when an authenticated user views affected content. Successful exploitation may allow the attacker to compromise the victim's authenticated browser session, access sensitive data, modify system state, or disrupt affected services.

### CVE-2026-105851

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-863` |
| Published | 2026-10-06T17:17:20.843 |

Payload is a free and open source headless content management system. In versions from 3.0.0 before 3.90.0 and canary versions before 4.0.0-canary.34, the duplicate operation copies values from a source document even when a field is hidden or its access.read or access.create rule rejects that value for the caller. The disableDuplicate setting does not prevent this access-control bypass. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-104070

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T17:17:12.213 |

The Crayons plugin for SPIP before 3.5.0 contains a missing authorization vulnerability that allows unauthenticated attackers to modify arbitrary editable object fields by omitting the secu_ anti-forgery parameter in crayons_store.php, causing the authorization dispatcher to resolve an unconditionally-true handler instead of the proper modification check. Attackers can chain this flaw to write a malicious .html skeleton file, disclose sensitive configuration files containing the site secret, and forge a signed ajax context to execute the uploaded skeleton, achieving arbitrary PHP code execution as the web-server user.

### CVE-2026-105844

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-06T16:17:06.400 |

Payload is a free and open source headless content management system. In versions from 3.0.0 before 3.88.0 and canary versions before 4.0.0-canary.27, an unauthenticated user can submit prototype-sensitive field paths when @payloadcms/plugin-import-export is enabled, causing unintended application behavior that can lead to remote code execution. This issue is fixed in versions 3.88.0 and 4.0.0-canary.27.

### CVE-2026-107194

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-07T14:17:09.203 |

Sungrow iSolarCloud before 2026 allows authentication bypass and account takeover via "login_type":"5" in a login request, potentially leading to "local blackouts on the whole continent" in Europe. An email address for the user_account property is required; however, a user can view the email address associated with their parent organization.

### CVE-2026-107183

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-07T14:17:09.003 |

llama.cpp before b11393 contains a use-after-free and double free vulnerability in common_chat_peg_mapper::map that allows unauthenticated remote attackers to corrupt heap memory via a dangling current_tool pointer. Attackers can submit a chat_parser in a POST /completion request emitting a tool-id after a tool-close tag to crash llama-server and shape a heap write primitive.

### CVE-2026-105324

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-113` |
| Published | 2026-10-07T02:16:57.433 |

An HTTP header injection vulnerability in start-page-loader.cgi of ADM allows an unauthenticated remote attacker to read arbitrary files on the host system. By sending a crafted HTTP request with injected headers via the state parameter, the attacker can leverage the underlying web server's X-Sendfile mechanism to retrieve sensitive files without authentication.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RWC1 as well as from ADM 5.0.0 through ADM 5.1.4.RL21.

### CVE-2026-106445

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184;CWE-1289` |
| Published | 2026-10-06T20:17:26.293 |

Handlebars provides the power necessary to let users build semantic templates. From 4.0.0 until 4.7.10, Handlebars lookupProperty returns Function.prototype.constructor before applying the prototype-access deny list because constructor is an own property of Function.prototype. When an attacker can render a controlled template with allowProtoMethodsByDefault enabled and an accessible function in the template context, the template can traverse from that function through its prototype to Function.prototype and then obtain the Function constructor through the own-property bypass. This permits attacker-controlled JavaScript to execute with the server application's privileges. This issue is fixed in version 4.7.10.

### CVE-2026-105863

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-915` |
| Published | 2026-10-06T17:17:22.570 |

Payload is a free and open source headless content management system. In versions after 3.0.0 and before 3.90.0, a custom field option that maps a field to a reserved authentication claim name can place unintended values in the authentication token issued at login. This issue is fixed in version 3.90.0.

### CVE-2026-79794

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:30.967 |

A SQL injection vulnerability in the web-based management interface of ClearPass Policy Manager could allow an authenticated remote attacker to conduct SQL injection attacks against the ClearPass Policy Manager instance. Successful exploitation could allow an attacker to run arbitrary database commands.

### CVE-2026-76747

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:30.067 |

Buffer overflow vulnerabilities exist in the affected interface of AOS-S. Successful exploitation could allow an unauthenticated remote attacker to expose sensitive memory contents and cause a denial of service on the device.

### CVE-2026-105794

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-06T15:17:16.260 |

MsQuic is a cross-platform C implementation of the IETF QUIC protocol exposed to C, C++, C#, and Rust. Prior to 2.4.20, 2.5.11, and 2.6.1, MsQuic clients using the OpenSSL or QuicTLS TLS backend do not properly verify that a server certificate matches the intended target server hostname. An on-path attacker can therefore present a certificate that does not match the intended target hostname and spoof the server in a man-in-the-middle attack. The Schannel backend is not affected. This issue is fixed in versions 2.4.20, 2.5.11, and 2.6.1.

### CVE-2026-105793

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-06T15:17:16.123 |

Microsoft UFO is an open-source framework for intelligent automation across devices and platforms. Prior to 3.0.9, the press_key tool in ufo/client/mcp/http_servers/mobile_mcp_server.py accepts a free-form key_code parameter and passes it to `adb shell input keyevent`. The adb client joins the arguments into a remote command string that the Android shell reparses, allowing an authenticated Mobile MCP caller to execute additional commands as the Android shell user on an authorized connected device. Exploitation requires a valid UFO_MCP_API_KEY, adb on the host, and a reachable authorized device, and it does not establish host operating-system execution, Android root execution, or access beyond the Android shell-user privileges. This issue is fixed in version 3.0.9.

### CVE-2026-16516

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-07T03:16:58.830 |

wolfSSH does not validate that the ECDSA curve identifier in a KEXDH_REPLY host key blob matches the algorithm negotiated during key exchange. In ParseECCPubKey() (src/internal.c), the blob's algorithm string is used to derive the curve via NameToId/wcPrimeForId without checking against the negotiated ssh->handshake->pubKeyId, and the RFC 5656 curve identifier string is discarded via GetSkip() rather than compared. An active network man-in-the-middle attacker can substitute a host key blob containing a different ECDSA curve, causing the client to import the key on the wrong curve. Because the attacker controls the private key for the substituted curve, signature verification passes. Exploitation requires an active MitM position and a lax public key check callback (e.g., TOFU, algorithm-name-only check, or fingerprint match against the parsed key).

### CVE-2026-102167

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-06T20:17:11.937 |

On affected Arista Wi-Fi access points, a memory corruption vulnerability exists in access point's wired uplink network endpoints. An unauthenticated attacker can crash the sensor service or potentially achieve remote code execution. Exploitation requires the attacker to be on the same network segment as the access point's wired uplink.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-106448

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-06T20:17:26.743 |

StableLib is a stable library of useful TypeScript and JavaScript code. Prior to 2.0.4, the @stablelib/cbor CBOR map decoding path creates ordinary JavaScript objects and assigns attacker-controlled keys with bracket assignment. A map key named __proto__ invokes the inherited prototype setter instead of creating an ordinary own property, allowing the decoded object's prototype to contain attacker-controlled authorization or feature-flag values. Downstream code that trusts normal property lookup or merges the decoded object can therefore make security-sensitive decisions using inherited attacker data. This issue is fixed in version 2.0.4.

### CVE-2026-103668

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-07T11:17:09.357 |

An SQL Injection vulnerability exists in the Site Search function of Movable Type, which may allow an unauthenticated attacker to execute an arbitrary SQL query on the affected product.

### CVE-2026-15894

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-10-07T09:17:05.157 |

The Bluetooth Mesh On-Demand Private Proxy solicitation handler in subsys/bluetooth/mesh/solicitation.c copies a received Solicitation PDU into a fixed 17-byte stack buffer without bounding the source length. In sol_pdu_decrypt(), out is allocated as NET_BUF_SIMPLE(17) and then filled with net_buf_simple_add_mem(out, in->data, in->len); net_buf_simple_add() guards its tailroom only with __ASSERT_NO_MSG, which is compiled out in production builds, so when in->len > 17 the underlying memcpy writes attacker-controlled bytes past the 17-byte stack buffer. The copy occurs before any decryption or authentication, so no key material is required to trigger it.

The oversized length arises because the mesh scan callback in subsys/bluetooth/mesh/adv.c calls net_buf_simple_restore() before dispatching to bt_mesh_sol_recv(), leaving buf->len covering the entire remaining advertising payload rather than just the Solicitation Service Data. After the parser locates the Service Data AD and consumes the Identification Type byte, the remaining buf->len is the 17-octet Network PDU plus any trailing advertising bytes, and prior to this fix there was no maximum-length check (only a minimum). An attacker can therefore append extra AD structures or padding after the Solicitation Service Data to make buf->len exceed 17.

bt_mesh_scan_cb() is registered directly as the BLE scan callback, so buf is raw, unauthenticated advertising data received over the air. Any device in radio range can send a non-connectable advertisement carrying a crafted mesh Proxy Solicitation to a node that has CONFIG_BT_MESH_OD_PRIV_PROXY_SRV enabled and is currently eligible to be solicited (GATT proxy disabled, On-Demand Private Proxy enabled), with no pairing, bonding, or provisioning. The result is an attacker-controlled stack overwrite — plausibly leading to remote code execution and at minimum a reliable remote denial of service. The fix trims buf->len to the spec-fixed 17 octets (dropping the PDU if fewer remain) before decryption.

### CVE-2026-97188

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-07T07:17:02.663 |

The String locator WordPress plugin before 2.6.8 does not restrict the classes allowed when deserializing the content of a database row saved through its database editor, allowing unauthenticated attackers to store a serialized PHP object that is instantiated when an administrator later opens and saves that row. If a suitable POP chain is present via another installed String locator WordPress plugin before 2.6.8 or , this can lead to arbitrary file deletion, sensitive data disclosure or remote code execution.

### CVE-2026-87782

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-07T07:17:01.847 |

The Koinonia Link WordPress plugin before 1.1.5 does not check that a user is allowed to change roles before saving a role selection submitted with a profile update, allowing any authenticated user, such as a subscriber, to grant themselves the Administrator role.

### CVE-2026-97679

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T01:16:36.643 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command ('Code Injection') related to improper input validation.

### CVE-2026-97678

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-10-07T01:16:36.517 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper input validation.

### CVE-2026-97676

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T01:16:36.387 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in code, resulting in a sandbox escape.

### CVE-2026-97673

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-10-07T01:16:36.117 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper input validation.

### CVE-2026-97655

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T01:16:35.833 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote attacker to execute arbitrary code due to an incomplete blocklist in the code security scanner.

### CVE-2026-93675

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-440` |
| Published | 2026-10-07T01:16:35.320 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote attacker to execute arbitrary code due to an expected dependency confusion.

### CVE-2026-88962

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T01:16:34.377 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper control of code generation.

### CVE-2026-104335

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-07T00:17:20.553 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper access control.

### CVE-2026-105812

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-06T21:17:04.600 |

Improper control of code generation in the agent import functionality of Amazon Bedrock AgentCore Starter Toolkit before 0.3.14 might allow an authenticated same-account actor to execute arbitrary code when a user imports and runs or deploys a Bedrock Agent, via crafted configuration values incorporated into generated Python source without safe literal encoding.



To remediate this issue, users should upgrade to version 0.3.14. Because this issue persists into generated source, upgrading alone is not sufficient: agents imported with an affected version must be re-imported with version 0.3.14 or later and their local and deployed output artifacts replaced.

### CVE-2026-79803

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:31.900 |

A command injection vulnerability exists in the API of ClearPass Policy Manager. Successful exploitation could allow an authenticated remote attacker to escalate privileges and gain administrative control of the affected system.

### CVE-2026-79802

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:31.783 |

A command injection vulnerability exists in the client software of ClearPass Policy Manager. Successful exploitation could allow an attacker who is able to supply crafted input to the affected software to execute arbitrary commands with elevated privileges on the affected host.

### CVE-2026-79800

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:31.553 |

An authenticated path traversal vulnerability exists in the command line interface of ClearPass Policy Manager. Successful exploitation could allow a low-privileged authenticated remote attacker to execute arbitrary code with elevated privileges on the underlying operating system.

### CVE-2026-79799

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:31.430 |

A vulnerability in the web-based management interface of ClearPass Policy Manager could allow an unauthenticated remote attacker to conduct a stored cross-site scripting (XSS) attack against an administrative user of the interface. A successful exploit could allow an attacker to execute arbitrary script code in a victim's browser in the context of the affected interface.

### CVE-2026-79797

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:31.197 |

An improper access control vulnerability exists in the Android client application for HPE Networking ClearPass Policy Manager, where application functionality may be invoked by untrusted sources. Successful exploitation could allow an unauthenticated remote attacker, with user interaction, to obtain sensitive information from the affected user.

### CVE-2026-76748

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:30.173 |

A privilege escalation vulnerability exists in the API of AOS-S. Successful exploitation could allow an authenticated read-only user to escalate their privileges and gain administrative access to the affected system.

### CVE-2026-102406

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-06T20:17:12.480 |

Authorization Bypass Through User-Controlled Key (CWE-639) in Kibana could lead to cross-tenant data interception. In this context, "tenant" refers to a user or team sharing the same Kibana deployment, not a separate Elastic Cloud organization or customer. Kibana's Fleet package installation process allowed a user holding delegated Fleet package-management privileges, without direct Elasticsearch administrative privileges, to claim a data stream identifier already in use by another tenant. Because ownership of that identifier was not verified before Fleet applied the uploaded package's generated index and ingest-pipeline settings to already-existing infrastructure, an attacker could redirect an existing tenant's data stream through infrastructure under their control. This exposed the affected tenant's subsequently ingested data to unauthorized disclosure and modification, and prevented that data from reaching its intended destination. Interception could continue even after the malicious package was removed, requiring separate remediation of the affected infrastructure.

### CVE-2026-106443

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-06T19:18:13.327 |

WeasyPrint helps web developers to create PDF documents. Prior to 70.0, the image-loading path in weasyprint/images.py passes fetched image bytes from HTML img URLs, CSS image values, SVG image references, and data URIs to Pillow's generic image dispatcher without excluding EPS or PostScript formats. On hosts with Ghostscript installed, Pillow EpsImagePlugin invokes the interpreter for attacker-controlled PostScript, which can produce interpreter-permitted effects and can lead to remote code execution when the installed Ghostscript version has a usable sandbox bypass. Hosts without Ghostscript do not reach this rasterization path. This issue is fixed in version 70.0.

### CVE-2026-106423

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:12.130 |

Use after free in Media in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106421

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:11.893 |

Use after free in PDF in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106411

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:10.750 |

Use after free in Parser in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106387

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T19:18:07.960 |

Missing authorization in Mobile in Google Chrome on on iOS prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to obtain sensitive information via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106383

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:07.517 |

Use after free in Media in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106374

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-06T19:18:06.523 |

Type confusion in V8 in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106373

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:06.413 |

Use after free in Fonts in Google Chrome on on Windows prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106371

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T19:18:06.190 |

Incorrect authorization in Transactions Platform in Google Chrome on on Android prior to 155.0.8059.39 allowed a remote attacker to obtain sensitive information via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106357

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:04.630 |

Use after free in WebRTC in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106352

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T19:18:04.033 |

Incorrect authorization in WebProtect in Google Chrome prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to obtain sensitive information via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106350

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T19:18:03.640 |

Incorrect authorization in Browser in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to obtain sensitive information via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106349

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:03.523 |

Use after free in V8 in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106347

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:03.253 |

Use after free in Track in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-106346

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-754` |
| Published | 2026-10-06T19:18:03.140 |

Improper state validation in DevTools in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106342

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-06T19:18:02.680 |

Information leak in Autofill in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to obtain sensitive information via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106341

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-06T19:18:02.570 |

Type confusion in V8 in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106335

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:01.910 |

Use after free in Media in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106334

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-06T19:18:01.797 |

Information leak in Payments in Google Chrome prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to obtain sensitive information via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106318

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:00.120 |

Use after free in Media in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106315

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:59.783 |

Use after free in Modularization in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106314

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T19:17:59.673 |

Incorrect authorization in Bluetooth in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to obtain sensitive information via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106309

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T19:17:59.120 |

Incorrect authorization in Selection in Google Chrome on on iOS prior to 155.0.8059.39 allowed a remote attacker to obtain sensitive information via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106308

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-10-06T19:17:59.007 |

Incorrect reference resolution in Autofill in Google Chrome on on Android prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to obtain sensitive information via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106291

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:56.940 |

Use after free in GarbageCollection in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106283

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:56.047 |

Use after free in Streaming in Google Chrome prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106278

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:55.487 |

Use after free in Select in Google Chrome prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106274

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-10-06T19:17:55.023 |

Incorrect reference resolution in Browser in Google Chrome on on Mac prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to obtain sensitive information via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106269

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:54.443 |

Use after free in CSS in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106268

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:54.330 |

Use after free in WebRTC in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106257

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:52.873 |

Use after free in HTML in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106256

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-06T19:17:52.760 |

Information leak in Passwords in Google Chrome on on Android prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to obtain sensitive information via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106255

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-06T19:17:52.640 |

Race condition in V8 in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106252

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-697` |
| Published | 2026-10-06T19:17:52.297 |

Incorrect comparison in Fonts in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106249

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T19:17:51.940 |

Incorrect authorization in Autofill in Google Chrome on on Android prior to 155.0.8059.39 allowed a remote attacker to obtain sensitive information via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106248

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:51.827 |

Use after free in Bindings in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106240

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-06T19:17:50.913 |

Type confusion in V8 in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106235

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:50.360 |

Use after free in WebAudio in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106225

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T19:17:49.230 |

Missing authorization in Autofill in Google Chrome prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to obtain sensitive information via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106220

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-06T19:17:48.673 |

Information leak in Passwords in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to obtain sensitive information via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106212

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T19:17:47.640 |

Incorrect authorization in Autofill in Google Chrome prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to obtain sensitive information via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106207

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-06T19:17:47.077 |

Race condition in V8 in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106204

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:46.723 |

Use after free in PDF in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted PDF file. (Chromium security severity: High)

### CVE-2026-106203

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-459` |
| Published | 2026-10-06T19:17:46.603 |

Incomplete cleanup in Autofill in Google Chrome on on iOS prior to 155.0.8059.39 allowed a remote attacker leveraging social engineering to obtain sensitive information via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106201

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-06T19:17:46.370 |

Race condition in V8 in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106200

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:46.257 |

Use after free in Track in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106193

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:45.443 |

Use after free in Parser in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106190

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:45.097 |

Use after free in Media in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-101207

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-06T18:16:42.173 |

Dell OpenManage Integration with Microsoft Windows Admin Center, versions prior to 3.7.0, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-106218

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-10-06T17:17:24.433 |

In JetBrains TeamCity before 2026.1.3
2025.11.7 kotlin DSL sandbox escape leading to RCE on the server was possible

### CVE-2026-105850

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-837` |
| Published | 2026-10-06T17:17:20.693 |

Payload is a free and open source headless content management system. In @payloadcms/plugin-ecommerce versions before 3.90.0 and canary versions before 4.0.0-canary.34, use of the Stripe payment adapter can allow a Stripe order confirmation to be processed more than once under certain conditions. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-105797

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-863` |
| Published | 2026-10-06T15:17:16.733 |

SimpleChat is a secure AI conversation application with personal and group workspaces for document-grounded interactions. In versions 0.261.003 and 0.261.027, an authorization ordering flaw in POST /api/user/plugins allows an authenticated low-privileged user to omit the top-level MCP type so that _reject_non_admin_mcp_stdio skips inspection before the type is restored from metadata. The stored personal action can then reach McpPluginFactory.create_connector, and MCPStdioPlugin.connect starts the attacker-selected operating-system process under the application service identity when the action tool is invoked. Exploitation requires personal plugins to be enabled and governance to permit MCP actions, and it can expose or modify secrets and data available to the service or disrupt the service. This issue is fixed in version 0.261.031.

### CVE-2026-105796

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-06T15:17:16.590 |

Kiota is an OpenAPI based HTTP Client code generator. From 0.5.0 until 1.35.0, Kiota's Java and PHP documentation-comment sanitizers delete block-comment terminators rather than neutralizing them, allowing overlapping characters to reform a terminator and place attacker-controlled OpenAPI text outside a generated documentation comment. The Java sanitizer also removes non-ASCII characters after deleting terminators, which can create a new terminator during normalization. Exploitation requires a developer or build pipeline to generate source from the malicious description and then compile and load the Java output or load the PHP output, after which injected code executes in the consuming application or build environment context. The version range is based on the Java defect and does not assert that PHP generation existed in every affected release. This issue is fixed in version 1.35.0.

### CVE-2026-106059

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-07T12:17:09.100 |

GitAhead through 2.7.1 on macOS contains a command injection vulnerability that allows attackers to execute shell commands by crafting repository filenames interpolated unescaped into the Show in Finder AppleScript. Attackers can commit a file whose path contains a double quote followed by a do shell script payload, which runs as the victim user when Show in Finder is chosen.

### CVE-2026-102478

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1289` |
| Published | 2026-10-07T02:16:56.320 |

In affected versions of Octopus Server, an authenticated user with permission to modify roles could bypass the protections preventing access abuse resulting in privilege escalation. It was possible for the built-in role to be weakened and the attacker's account added to a privileged team. This was achievable due to improper validation of unsafe equivalence in inputs.

### CVE-2026-106447

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-06T20:17:26.573 |

StableLib is a stable library of useful TypeScript and JavaScript code. Prior to 2.0.4, the @stablelib/cbor decoder recursively processes nested CBOR arrays, maps, and tags through _decodeValue() without enforcing a maximum nesting depth. A sufficiently deep structure exhausts the JavaScript call stack, causing a decoding exception and potentially terminating an uncaught request worker or process. This issue is fixed in version 2.0.4.

### CVE-2026-102163

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-06T20:17:11.533 |

On affected Arista access points with Wireless Intrusion Prevention System (WIPS) active, an unauthenticated attacker within radio frequency (RF) proximity can send a crafted frame to crash the sensor service, disabling WIPS monitoring on the access point, or potentially achieve remote code execution. No wireless association or authentication is required.

### CVE-2026-102161

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-798` |
| Published | 2026-10-06T20:17:11.230 |

An unauthenticated attacker located on an adjacent private network (or any attacker routed through a reverse proxy/load balancer that forwards client headers) can forge their source IP address and gain administrative session privileges on the CV-CUE backend.

### CVE-2026-96890

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-06T19:18:17.167 |

A Server-Side Request Forgery (SSRF) vulnerability was identified in GitHub Enterprise Server that allowed a repository contributor to cause the appliance to issue requests to attacker-controlled internal hosts, which could be chained to achieve remote code execution on the appliance. The secret scanning validator for GCP service account credentials trusted the token endpoint embedded in a committed credential and issued a request to it without restricting the destination. Exploitation required an authenticated user with permission to push to a repository on an instance with GitHub Advanced Security and secret scanning validity checks enabled, a non-default configuration. This vulnerability affected GitHub Enterprise Server 3.20, 3.21, and 3.22 and was fixed in versions 3.20.9, 3.21.7, and 3.22.2. This vulnerability was reported through the GitHub Bug Bounty program.

### CVE-2026-106104

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-06T18:16:51.687 |

Quasar Framework is a framework for building high-performance Vue.js user interfaces. Prior to 2.23.3, Platform.parseSSR() passed an unbounded User-Agent request header to getMatch() in ui/src/plugins/platform/Platform.js, whose browser-detection expressions combined greedy captures with repeated unbounded scans. Platform belongs to autoInstalledPlugins, so this parsing occurs before routing for every SSR request. A crafted unauthenticated request containing repeated version tokens without a terminating Safari token causes super-linear backtracking and blocks the Node.js event loop, delaying every other SSR request. SPA, PWA, Electron, Cordova, Capacitor, browser-extension, and static-site-generation targets are not affected because they do not parse an attacker-controlled request header through this path. This issue is fixed in version 2.23.3.

### CVE-2026-105862

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-434` |
| Published | 2026-10-06T17:17:22.423 |

Payload is a free and open source headless content management system. In versions before 3.90.0 and canary versions before 4.0.0-canary.34, a collection that allows downloadable SVG uploads can store a malicious SVG that bypasses sanitization and executes attacker-controlled JavaScript when a user downloads and opens the SVG. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-105854

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-10-06T17:17:21.290 |

Payload is a free and open source headless content management system. In versions from 3.0.0 before 3.90.0 and canary versions before 4.0.0-canary.34, a malformed multipart request body can cause multipart Content-Type processing to take an extremely long time, resulting in uncontrolled resource consumption. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-105798

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-06T15:17:16.880 |

SimpleChat is a secure AI conversation application with personal and group workspaces for document-grounded interactions. Prior to 0.261.029, POST /api/group_documents/upload stores an attacker-controlled group document filename that group_workspaces.html later interpolates into inline Share event handlers. The escapeGroupHtml function leaves apostrophes unchanged, while escapeHtml produces an HTML entity that the browser decodes before JavaScript evaluation, so either path permits the filename to terminate the handler string. An authenticated group Owner, Admin, or DocumentManager can persist script that executes in the SimpleChat origin when another group member clicks Share, allowing access to victim-visible data and actions with the victim session. This issue is fixed in version 0.261.029.

### CVE-2026-107181

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-143` |
| Published | 2026-10-07T14:17:08.807 |

Telegram Desktop before 7.2.9 contains an IPC record-separator injection vulnerability in Core::Sandbox that allows remote attackers to inject OPEN: records via crafted tg:// links containing unescaped semicolons. Attackers can reach the interpret: scheme handler to upload local files, including tdata session keys, to an attacker channel, enabling account takeover.

### CVE-2026-102160

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-06T20:17:11.100 |

An operating system (OS) command injection vulnerability in CloudVision CUE backup management may allow an authenticated Super User to submit a crafted backup request and execute arbitrary commands with the privileges of the affected service.

### CVE-2026-101155

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-06T20:17:09.703 |

An authenticated remote attacker with specific permissions can read or write files on the platform filesystem beyond the intended scope through specially crafted requests and/or crafted file uploads to the Software Management Studio Software Repository.

### CVE-2026-101154

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-06T20:17:09.567 |

An authenticated remote attacker with specific permissions can read or write files on the platform filesystem beyond the intended scope through specially crafted requests and/or crafted file uploads to the Network Provisioning Image Repository.

### CVE-2026-106186

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-06T19:17:44.627 |

Uncontrolled search path element in CredentialProvider in Google Chrome on on Windows prior to 155.0.8059.39 allowed a local attacker to potentially execute arbitrary code outside the sandbox via a local program. (Chromium security severity: Low)

### CVE-2026-105868

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-06T17:17:23.283 |

Payload is a free and open source headless content management system. In versions before 3.90.0 and canary versions before 4.0.0-canary.34, local upload configurations that accept XML files can store an XML file and stylesheet that execute JavaScript in the Payload origin when a logged-in user opens the file. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-105856

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T17:17:21.570 |

Payload is a free and open source headless content management system. Prior to 3.90.0 and 4.0.0-canary.34, an attacker with read and create or update access to a collection containing a json field or a blocks field with blocksAsJSON enabled can inject SQL through a crafted field path and operators. Collections without those fields are not affected, and richText fields are not affected. The SQLite packages are fixed in versions 3.90.0 and 4.0.0-canary.34, and the Postgres packages are fixed in version 3.73.0.

### CVE-2026-105806

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T16:17:06.257 |

Payload is a free and open source headless content management system. In @payloadcms/plugin-mcp versions from 3.61.0 until 3.88.0, an authenticated user can manage MCP API keys outside the intended account, enabling privilege escalation through account takeover. This issue is fixed in version 3.88.0.

### CVE-2026-104069

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-06T15:17:12.237 |

HortusFox before 6.2 contains a remote code execution vulnerability in ThemeModule::startImport() where an uploaded ZIP archive is extracted directly into the public web root before any validation of file names, extensions, or content is performed. An authenticated administrator can upload a crafted theme archive containing a PHP file and an .htaccess file to re-enable execution, then request it under the themes directory to execute arbitrary OS commands as the web-server user.

### CVE-2026-106057

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-07T12:17:08.730 |

patool before 4.0.6 contains an OS command injection vulnerability on Windows because shell_quote_nt fails to escape cmd.exe metacharacters or embedded double quotes in archive filenames. Attackers can supply crafted filenames like report&calc.gz for single-file formats run with shell=True to execute commands with patool process privileges.

### CVE-2026-93449

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T01:16:35.057 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper control of code generation.

### CVE-2026-106500

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-362` |
| Published | 2026-10-06T22:17:05.060 |

Backstage is an open framework for building developer portals. Prior to 3.3.1, 3.4.1, 4.0.3 and 4.1.0, the @backstage/plugin-scaffolder-backend package is affected by improper task state validation in scaffolder backend. An authenticated user with permission to create and access Scaffolder tasks may, under specific timing and deployment conditions, affect files accessible to the Backstage backend. If backend application files are writable, the confidentiality, integrity, and availability of the backend may be compromised. This issue is fixed in versions 3.3.1, 3.4.1, 4.0.3 and 4.1.0.

### CVE-2026-106547

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-06T21:17:18.670 |

A heap-based buffer overflow in H5VM_array_fill() in src/H5VM.c in HDF5 before 2.2.0 lets a remote attacker cause an application crash and possibly execute arbitrary code with a crafted HDF5 file. When a dataset's unallocated chunks are read, H5D__fill_init() fills the fill-value buffer from datatype and dataspace metadata in the file. If that metadata is inconsistent with the buffer's allocated size, the write goes past the end of the buffer. The attacker can control the content written through the fill value stored in the file.

### CVE-2026-106486

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-10-06T21:17:17.323 |

Backstage is an open framework for building developer portals. Prior to 0.3.10 in @backstage/plugin-scaffolder-backend-module-bitbucket-cloud and 0.2.25 in @backstage/plugin-scaffolder-backend-module-bitbucket-server, the Bitbucket pull-request Scaffolder actions did not sufficiently validate filesystem paths. An authenticated user who can execute an eligible template and influence an allowed Bitbucket repository could affect paths outside the expected working area, potentially compromising backend confidentiality, integrity, or availability. This issue is fixed in @backstage/plugin-scaffolder-backend-module-bitbucket-cloud 0.3.10 and @backstage/plugin-scaffolder-backend-module-bitbucket-server 0.2.25.

### CVE-2026-106459

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-200;CWE-918` |
| Published | 2026-10-06T21:17:16.450 |

Backstage is an open framework for building developer portals. From 0.3.0 until 0.3.8, the @backstage/plugin-scaffolder-backend-module-sentry package is affected by improper input validation in sentry scaffolder actions. An authenticated internal user who can execute the affected actions may cause the backend to contact unintended destinations and disclose Sentry integration credentials. Subsequent impact depends on network reachability and the privileges granted to the configured token. This issue is fixed in version 0.3.8.

### CVE-2026-106439

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470;CWE-693` |
| Published | 2026-10-06T19:18:12.720 |

Hydra is a framework for elegantly configuring complex applications. From 1.3.4 until 1.3.7 and 1.4.0.dev10, Hydra stores legacy instantiate target blocklists and related execution-policy collections in mutable module-level state. An attacker who controls multiple sibling target entries can resolve hydra._internal.target_policy.UNCONTROLLED_EXECUTION_TARGETS.discard through instantiate(), remove a denied target, and then invoke that target because sibling nodes are processed in insertion order against the same modified policy. The mutation persists in process-global state and can enable code execution with the application's privileges, while a narrow execution whitelist supplied by trusted Python code is not bypassed by the reported direct mutation path. This issue is fixed in versions 1.3.7 and 1.4.0.dev10.

### CVE-2026-16528

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-10-07T02:16:57.730 |

Insertion of Sensitive Information into Log File in certain ASUS router models allows a remote authenticated attacker to obtain DDNS credentials from the system log, potentially enabling modification of DNS settings.Refer to the ' Security Update for ASUS Router Firmware  ' section on the ASUS Security Advisory for more information.

### CVE-2026-106512

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-79;CWE-113` |
| Published | 2026-10-06T19:18:13.637 |

The CakeResponse::download() method in lib/Cake/Network/CakeResponse.php constructs a Content-Disposition header by directly interpolating a caller-supplied filename into a quoted-string value without sanitization. Two distinct injection vectors exist in the unpatched code. First, if the filename contains C0 control characters (CR or LF), PHP refuses to emit the entire Content-Disposition header, silently dropping the attachment disposition. The response body is then served with its own Content-Type (for example text/html for an .html attachment) and renders inline in the browser on the application origin, creating a stored cross-site scripting condition. The commit message notes this is reachable even when the download_attachments_on_load setting is enabled, meaning a victim merely needs to view a page that triggers the download. Second, a double-quote character in the filename terminates the quoted-string value early, permitting injection of additional Content-Disposition parameters. The affected code path covers all callers of CakeResponse::download(), including attribute downloads, proposal downloads, and restSearch exports. An authenticated user who can create or upload an attachment with a crafted filename (for example through MISP attribute naming or proposal attachment naming) can store the malicious filename. When any other authenticated user views the affected page, the unsanitized filename is reflected into the HTTP response header, resulting in header manipulation and potential execution of arbitrary HTML or JavaScript in the context of the application origin. The security impact is equivalent to a stored cross-site scripting vulnerability, allowing session hijacking, data exfiltration, and unauthorized actions on behalf of the victim.

### CVE-2026-106105

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-06T18:16:51.833 |

Quasar Framework is a framework for building high-performance Vue.js user interfaces. Prior to @quasar/ssl-certificate 2.1.0, @quasar/cli 5.0.4, and @quasar/app-vite 3.3.0, the @quasar/ssl-certificate utility cached a combined private key and certificate PEM without explicitly applying owner-only filesystem permissions. Another local user able to read the cache can copy the key and impersonate a development TLS endpoint in an environment that trusts the certificate. The generated certificate was also CA-capable, carried unnecessarily broad key usages, and encoded the IPv6 loopback address as a DNS subject alternative name. This issue is fixed in @quasar/ssl-certificate 2.1.0, @quasar/cli 5.0.4, and @quasar/app-vite 3.3.0.

### CVE-2026-105801

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-116;CWE-150` |
| Published | 2026-10-06T15:17:17.320 |

openapi-python-client generates Python clients from OpenAPI documents. Prior to 0.29.1, the generator does not safely neutralize malicious OpenAPI document content before rendering string, docstring, and f-string contexts in generated Python. The generated Python client can contain attacker-controlled Python that executes when a user imports the client, affecting the importing environment's integrity and potentially its confidentiality and availability. This issue is fixed in version 0.29.1.

### CVE-2026-58069

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-07T09:17:05.550 |

This vulnerability in Veeam Backup & Replication allows an authenticated Cloud Connect tenant to read arbitrary files on the service provider host.

### CVE-2026-97680

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-07T01:16:36.780 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to obtain sensitive information or inject malicious data due to improper access control in the vertex result caching subsystem.

### CVE-2026-106426

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-06T19:18:12.483 |

Race condition in Fonts in Google Chrome prior to 155.0.8059.39 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106412

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-06T19:18:10.860 |

Race condition in Core in Google Chrome on on Mac prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process and leveraged social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106409

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-10-06T19:18:10.523 |

Incorrect reference resolution in WebAppInstalls in Google Chrome on on Mac prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via crafted network traffic. (Chromium security severity: Medium)

### CVE-2026-106393

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:18:08.677 |

Use after free in Storage in Google Chrome prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106378

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-10-06T19:18:06.960 |

Privilege elevation in Sandbox in Google Chrome on on Mac prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106377

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-06T19:18:06.853 |

Race condition in Fonts in Google Chrome prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106293

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-06T19:17:57.230 |

Type confusion in ANGLE in Google Chrome prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106292

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-06T19:17:57.110 |

Buffer overflow in Fonts in Google Chrome prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106247

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-06T19:17:51.713 |

Buffer overflow in ANGLE in Google Chrome prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106238

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-06T19:17:50.690 |

Race condition in Fonts in Google Chrome prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106233

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-06T19:17:50.140 |

Use after free in Metrics in Google Chrome prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-106228

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-10-06T19:17:49.563 |

Confused deputy in Google Lens in Google Chrome prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106194

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T19:17:45.557 |

Missing authorization in WebAppInstalls in Google Chrome prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process and leveraged social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-106191

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T19:17:45.207 |

Missing authorization in Actor in Google Chrome prior to 155.0.8059.39 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-106107

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-10-06T18:16:52.190 |

Quasar Framework is a framework for building high-performance Vue.js user interfaces. Prior to 3.3.0, several @quasar/app-vite SSR and SSG rendering paths interpolated ssrContext.nonce directly into quoted HTML attributes. An application that derives or overrides this value with attacker-controlled data can allow a quote to terminate the nonce attribute and inject additional attributes or markup into generated HTML across development and production SSR or SSG output. Cryptographically generated base64 or base64url nonces are not affected because they lack HTML attribute delimiters. This issue is fixed in version 3.3.0.

### CVE-2026-82211

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-07T07:17:01.373 |

The Nexi XPay Build WordPress plugin through 7.6.2 does not verify the payment result supplied to several of its unauthenticated routes, allowing attackers to mark arbitrary orders as paid or failed, to cancel them, and to obtain order keys which expose guest buyers' details.

### CVE-2026-94114

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-386` |
| Published | 2026-10-06T20:17:34.420 |

Symbolic name not mapping to correct object vulnerability in Apache Commons.



BCEL caches attacker-controlled classes under their self-declared names without validating the requested name, allowing subsequent lookups and name-keyed verification results to refer to a different class.



This issue affects Apache Commons: before 6.13.0.



Users are recommended to upgrade to version 6.13.0, which fixes the issue.

### CVE-2026-86362

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-06T19:18:16.717 |

Dell System Update, versions prior to 2.3.0.0, contains an Improper Access Control vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-86361

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-06T19:18:16.567 |

Dell System Update, versions prior to 2.3.0.0, contains an Incorrect Permission Assignment for Critical Resource vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-67270

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-06T16:17:09.580 |

Dell Container Storage Modules (CSM) versions prior to 1.18.0, contains an Improper Certificate Validation vulnerability in the proxy-server component. An unauthenticated adjacent network attacker could potentially exploit this vulnerability, leading to information exposure of storage backend administrator credentials.

### CVE-2026-19186

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-191;CWE-787` |
| Published | 2026-10-07T09:17:05.290 |

ieee802154_decipher_data_frame() in subsys/net/l2/ieee802154/ieee802154_frame.c computed payload_len = net_pkt_get_len(pkt) - ll_hdr_len - authtag_len without first checking that the received frame is at least ll_hdr_len + authtag_len bytes long. All three variables are uint8_t, so a frame whose payload is shorter than the configured authentication tag makes the subtraction wrap around to a large value (up to 255).

The wrapped length is passed unchanged to ieee802154_decrypt_auth() and on to the CCM operation as cipher_pkt.in_len/out_buf_max, with apkt->tag pointing at frame + ll_hdr_len + payload_len. Because the receive buffer is allocated to the exact length of the frame received from the radio driver, the crypto layer then reads several hundred bytes past the end of the packet buffer and writes the same number of decrypted bytes back over it in place. The frame's authentication tag is only verified after this processing has taken place, so no key material, association or prior authentication is needed — a single crafted short frame from any device in radio range is sufficient. Frame validation in ieee802154_validate_frame() does not prevent it: a data frame is accepted with a one-byte payload.

The result is an out-of-bounds read and an out-of-bounds write of up to roughly 240 bytes into the adjacent network-buffer pool, corrupting other packets or allocator metadata and typically faulting the target. The out-of-bounds content is not attacker-chosen (it is ciphertext XOR keystream over out-of-bounds memory) and the frame is dropped when tag verification fails, so the primary impact is memory corruption and denial of service rather than information disclosure.

Exposure is limited to configurations that enable the experimental CONFIG_NET_L2_IEEE802154_SECURITY option, select a crypto device via CONFIG_NET_L2_IEEE802154_SECURITY_CRYPTO_DEV_NAME, and have established a security session with a level other than IEEE802154_SECURITY_LEVEL_NONE; with security disabled or at level NONE the tag length is zero and no underflow occurs. The fix rejects frames shorter than ll_hdr_len + authtag_len before the subtraction, and adds the matching guard on the transmit side in ieee802154_create_data_frame().

### CVE-2026-59347

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-07T06:16:35.700 |

VMware Workstation and Fusion contain a stack-based buffer-overflow vulnerability in HGFS. A malicious actor with local administrative privileges on a virtual machine may exploit this issue to execute code as the virtual machine's VMX process running on the host.

Affected versions:
- VMware Workstation: 25H2, 26H1 (fixed in 26H1u1)
- VMware Fusion: 25H2, 26H1 (fixed in 26H1u1)

### CVE-2026-106471

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-07T02:16:57.583 |

A flaw was found in Candlepin. The central authorization filter incorrectly grants access when any one of multiple @Verify-annotated parameters is accessible, instead of requiring access to every verified entity. A low-privilege authenticated attacker who can access the first referenced object can bypass authorization checks on subsequent objects. When target resource identifiers are known, this can enable unauthorized disclosure of consumer information and unauthorized modification of entitlements and related subscription resources, including across organizations.

### CVE-2026-97674

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T01:16:36.247 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to execute arbitrary OS commands due to improper neutralization of special elements used in an OS command ('Code Injection'), aka improper control of code generation.

### CVE-2026-93445

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T01:16:34.657 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper control of generation of code.

### CVE-2026-103360

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-07T01:16:34.087 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to obtain sensitive information due to improper limitation of a pathname to a restricted directory.

### CVE-2026-106503

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-178;CWE-284` |
| Published | 2026-10-06T22:17:05.513 |

Backstage is an open framework for building developer portals. Prior to 3.3.1, 3.4.1, 4.0.3 and 4.1.0, the @backstage/plugin-scaffolder-backend package is affected by scaffolder action input authorization bypass. An authenticated user with access to affected Scaffolder templates could bypass configured action restrictions. Depending on integration credentials, this could grant unauthorized access to repositories and related source-control resources. This issue is fixed in versions 3.3.1, 3.4.1, 4.0.3 and 4.1.0.

### CVE-2026-106488

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-06T21:17:17.623 |

Backstage is an open framework for building developer portals. Prior to 0.4.20, the @backstage/plugin-auth-backend-module-oidc-provider package is affected by improper authentication in the oidc provider. Deployments using OIDC email-based identity resolution with a provider that permits unverified email addresses may allow an authenticated provider user to assume another catalog identity. This may grant access and permissions associated with that user. No direct availability impact is demonstrated. This issue is fixed in version 0.4.20.

### CVE-2025-45871

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-06T18:16:41.890 |

LogicalDOC Enterprise up to and for 9.1.1 is vulnerable to blind SQL injection in the WorkflowsDataServlet component, allowing authenticated user to manipulate SQL queries via crafted workflow template name.

### CVE-2026-105865

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-10-06T17:17:22.843 |

Payload is a free and open source headless content management system. In versions before 3.90.0 and canary versions before 4.0.0-canary.34, an authenticated user who can update or delete uploads stored locally can cause file cleanup to remove unintended files outside the configured upload directory, resulting in data loss or service disruption. Deployments that restrict upload management to trusted users are less exposed. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-105858

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-1321` |
| Published | 2026-10-06T17:17:21.847 |

Payload is a free and open source headless content management system. In versions before 3.90.0 and canary versions before 4.0.0-canary.34, a crafted request to the public first-register operation can execute code remotely when local authentication is enabled and no initial user has been created. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-65142

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-06T22:17:07.430 |

NVIDIA Model-Optimizer contains a vulnerability where an attacker may cause deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, denial of service, and information disclosure.

### CVE-2026-106062

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-06T21:17:04.903 |

A heap-based buffer overflow was found in GIMP’s DirectDraw Surface (DDS) loader. When loading a crafted DDS image, buffer sizes derived from width, height, and pitch can be computed using 32-bit arithmetic that overflows. The allocated buffer is too small for the amount of pixel data written through GEGL (CWE-787), following integer overflow in size calculations (CWE-190). This may allow heap corruption and, in the worst case, arbitrary code execution in the context of the GIMP process.

### CVE-2026-101258

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-06T21:17:02.120 |

A flaw was found in Ghostscript. When Ghostscript renders a crafted PostScript or EPS document, it can bypass the -dSAFER sandbox and execute arbitrary shell commands in the context of the Ghostscript process. The issue chains memory corruption in document parsing with disabling of internal path access controls at runtime. An attacker can deliver the document directly or through formats that delegate rendering to Ghostscript (for example EPS import or print conversion workflows). Successful exploitation can compromise confidentiality, integrity, and availability of data accessible to the process running Ghostscript.

### CVE-2026-79808

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:32.367 |

A buffer overflow vulnerability exists in the OnGuard agent of ClearPass Policy Manager. Successful exploitation could allow an authenticated local user to execute arbitrary code with elevated privileges on the affected host or to disrupt the availability of the affected service.

### CVE-2026-79807

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:32.253 |

A missing integrity verification vulnerability in the Windows client software for ClearPass Policy Manager could allow malicious users on a local instance to elevate their user privileges. A successful exploit could allow these users to execute attacker-supplied code with elevated privileges on the local system.

### CVE-2026-79806

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:32.133 |

A privilege escalation vulnerability in the ClearPass Policy Manager OnGuard Linux agent could allow malicious users on a Linux instance to elevate their user privileges. A successful exploit allows a malicious user to escalate to root privileges on the affected Linux client.

### CVE-2026-106442

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-10-06T19:18:13.170 |

Hydra is a framework for elegantly configuring complex applications. From 1.3.4 until 1.3.6 and 1.4.0.dev9, the instantiate() target blacklist introduced for CVE-2026-68508 incompletely checks the effective callable selected by the target field. Execution wrappers such as timeit.timeit, executable deserialization through pickle.loads, aliases, callable-returning helpers, generic dispatch, and deferred calls can obscure or defer the effective target and bypass name-based authorization. An attacker who causes an application to instantiate untrusted Hydra configuration can use these gaps to execute code with the application's privileges. This issue is fixed in versions 1.3.6 and 1.4.0.dev9.

### CVE-2026-106441

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-06T19:18:13.020 |

Hydra is a framework for elegantly configuring complex applications. Prior to 1.3.6 and 1.4.0.dev9, Hydra passes Python logging configuration to logging.config.dictConfig() without applying Hydra's target policy to handler class values or formatter, filter, handler, queue, and listener factories. An attacker who controls Hydra logging configuration can therefore select an importable class or factory and cause it to be invoked with the application's privileges, even in versions where instantiate() is protected because the logging path does not use instantiate(). This issue is fixed in versions 1.3.6 and 1.4.0.dev9.

### CVE-2026-106440

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-10-06T19:18:12.877 |

Hydra is a framework for elegantly configuring complex applications. From 1.2.0 until 1.3.0 and 1.4.0.dev10, the hydra-optuna-sweeper package accepts a configuration-controlled dotted path in hydra.sweeper.custom_search_space, resolves it with hydra.utils.get_method(), and later invokes the returned callable in the Hydra controller process. Because get_method() is a trusted-input lookup helper and does not apply the execution policy used by instantiate(), an attacker who controls Optuna sweep configuration or command-line overrides can select importable Python code for execution with the application's privileges, including bypassing a trusted execution whitelist on affected Hydra 1.4 development releases. This issue is fixed in versions 1.3.0 and 1.4.0.dev10.

### CVE-2026-103435

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-61;CWE-367` |
| Published | 2026-10-07T13:17:16.690 |

Claude Code validated that a target file path resided within the project working directory at permission-check time, but re-resolved the path at write time without repeating that validation. This time-of-check to time-of-use (TOCTOU) gap allowed an attacker who could write to the workspace to atomically replace a project file with a symlink, causing Claude Code to follow the symlink and write its output to an arbitrary file outside the project sandbox. Exploitation required the ability to win a race condition against the write operation and write access to the shared workspace, enabling a lower-privileged attacker to redirect benign edits to sensitive files (e.g., shell configuration) in a higher-privileged session.

Users on standard Claude Code auto-update have received this fix already. Users performing manual updates are advised to update to the latest version.

Thank you to hackerone.com/c_h4ck_0 for reporting this issue.

### CVE-2026-106058

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-07T12:17:08.920 |

GitAhead through 2.7.1 contains an OS command injection vulnerability in src/git/Filter.cpp that allows malicious repositories to execute commands by substituting crafted filenames into clean/smudge filter commands. Attackers can ship files named with $(command) selected via .gitattributes so checkout or staging runs the command through bash -c as the victim.

### CVE-2026-106056

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-07T12:17:08.520 |

Rundeck before 6.2.0 contains an OS command injection vulnerability that allows authenticated users with job run permission to execute commands on Windows nodes by supplying crafted option values. Attackers can inject cmd.exe metacharacters such as && or | into free-text options, which CLIUtils.quoteWindowsCMDArg wraps in ineffective single quotes, running commands with node executor credential privileges.

### CVE-2026-83540

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-613` |
| Published | 2026-10-07T03:16:59.730 |

When password or public key authentication is used with the Windows port of wolfSSHd, the Windows logon token acquired for one authenticated connection is not released before a token is acquired for a subsequent connection, resulting in user login poisoning between connections. A less privileged user with a valid account on the server can exploit this to force a login as a more privileged user. The vulnerability was introduced with the initial Windows port of wolfSSHd in wolfSSH version 1.4.15 and affects all versions through 1.5.0. Non-Windows builds of wolfSSHd are not affected.

### CVE-2026-19396

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-337` |
| Published | 2026-10-07T02:16:58.013 |

A predictable seed in the pseudo-random number generator (PRNG) in the IFTTT pairing token generation of the ASUS RT-BE57 router allows an unauthenticated nearby user to derive the pairing token and read or modify router settings via observed values from an administrator-initiated IFTTT pairing session.Refer to the ' Security Update for ASUS Router Firmware  ' section on the ASUS Security Advisory for more information.

### CVE-2026-93677

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-07T01:16:35.457 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to obtain sensitive information due to exposure of sensitive information to an unauthorized actor.

### CVE-2026-101331

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-07T01:16:33.957 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to obtain sensitive information due to insufficiently protected credentials.

### CVE-2026-106509

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-10-06T22:17:06.463 |

Backstage is an open framework for building developer portals. Prior to 1.14.6, the @backstage/plugin-techdocs-node package is affected by improper validation of mkdocs theme configuration in techdocs. When TechDocs is configured to build documentation locally or in a container, a user with write access to a registered repository can include configuration values in mkdocs.yml that cause arbitrary code execution during the documentation build process. This issue is fixed in versions 1.14.6 and 1.15.4.

### CVE-2026-106505

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-426;CWE-436` |
| Published | 2026-10-06T22:17:05.837 |

Backstage is an open framework for building developer portals. Prior to 1.14.6 and 1.15.4, the @backstage/plugin-techdocs-node package is affected by bypass of mkdocs configuration sanitizer in techdocs backend. Users with the ability to commit changes to a repository that uses TechDocs can circumvent the MkDocs configuration file sanitizer introduced in response to CVE-2026-25153 and execute arbitrary code on the TechDocs backend host during documentation generation. This issue is fixed in versions 1.14.6 and 1.15.4.

### CVE-2026-106498

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863;CWE-918` |
| Published | 2026-10-06T22:17:04.713 |

Backstage is an open framework for building developer portals. Prior to 3.5.1, 3.6.2, 3.7.2, 3.8.2 and 3.9.1, the @backstage/plugin-catalog-backend package is affected by improper url validation in catalog entity placeholder resolution. An authenticated Backstage user could craft a catalog entity with placeholder directives that reference resources outside the entity's source repository. Under certain configurations, this could allow access to data not intended to be available to the user. This issue is fixed in versions 3.5.1, 3.6.2, 3.7.2, 3.8.2 and 3.9.1.

### CVE-2026-43598

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-06T21:17:20.680 |

Improper input validation in the AMD ROCm Communication Collectives Library (RCCL) could allow a compromised peer rank or network-adjacent attacker to dereference an attacker-controlled pointer, potentially resulting in remote code execution.

### CVE-2026-106455

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-06T21:17:15.727 |

Backstage is an open framework for building developer portals. From 0.11.12 until 1.14.7 and 1.15.5, the @backstage/plugin-techdocs-node package is affected by improper validation of mkdocs plugin configuration in techdocs. An authenticated attacker with control over a TechDocs source repository could cause a documentation build to retrieve and publish data from network locations reachable by the build environment. Exposure depends on deployment topology, build mode, and target endpoint protections. Modern cloud metadata services that require tokens or special headers are not directly accessible through the affected behavior. This issue is fixed in @backstage/plugin-techdocs-node versions 1.14.7 and 1.15.5.

### CVE-2026-102165

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-06T20:17:11.800 |

On affected Arista Wi-Fi access points, an unauthenticated attacker with network access to the capture service can send a crafted packet to cause the service to crash or potentially achieve remote code execution. This exploit requires an uncommonly used non-default streaming mode.

### CVE-2026-101027

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:08.233 |

When `[migrations] ALLOWED_DOMAINS` was configured, a hostname matching the allow list was accepted without checking its resolved address against the local-network restrictions. A user who can start repository migrations and control the DNS of an allowed hostname could make it resolve to loopback or private addresses and bypass `ALLOW_LOCALNETWORKS = false`, reaching internal services from the Gitea server. Instances without `ALLOWED_DOMAINS` configured are not affected by this specific bypass.

### CVE-2026-105849

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201;CWE-862` |
| Published | 2026-10-06T17:17:20.470 |

Payload is a free and open source headless content management system. In versions from 3.0.0 before 3.90.0 and canary versions before 4.0.0-canary.34, users with ordinary read access to other authentication documents in a collection with useAPIKey enabled can obtain active API keys and exercise the target accounts' permissions until those keys are rotated or disabled. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-76105

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-330` |
| Published | 2026-10-06T16:17:10.000 |

Dell Container Storage Modules, versions prior to 1.18.0 contain(s) an Use of Insufficiently Random Values vulnerability. An unauthenticated attacker with local access could potentially exploit this vulnerability, leading to Information tampering.

### CVE-2026-61411

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-10-06T16:17:08.693 |

Dell Container Storage Modules, versions prior to 1.18.0, contain(s) an Insertion of Sensitive Information into Log File vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Information disclosure.

### CVE-2026-107162

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-07T13:17:19.963 |

Express Gateway through 1.16.11 contains an authentication bypass vulnerability in the OAuth 2.0 refresh_token grant that fails to validate the token secret or issuing client. Attackers with any valid client credentials and the identifier portion of another user's refresh token can obtain that user's access token and impersonate them against oauth2-protected APIs.

### CVE-2026-42710

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-07T12:17:09.810 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in 10Web Slider by 10Web slider-wd allows Blind SQL Injection.This issue affects Slider by 10Web: from n/a through 1.2.63.

### CVE-2026-42708

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-07T12:17:09.650 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in AF themes WP Post Author wp-post-author allows Blind SQL Injection.This issue affects WP Post Author: from n/a through 4.0.0.

### CVE-2026-42714

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-07T11:17:19.237 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Piggly Dev Pix por Piggly (para Woocommerce) pix-por-piggly allows Blind SQL Injection.This issue affects Pix por Piggly (para Woocommerce): from n/a through 2.1.2.

### CVE-2026-42713

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-07T11:17:19.093 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Gopiplus Post title marquee scroll post-title-marquee-scroll allows Blind SQL Injection.This issue affects Post title marquee scroll: from n/a through 9.9.

### CVE-2026-42721

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-07T10:17:35.870 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in SERVIT Software Solutions affiliate-toolkit affiliate-toolkit-starter allows Blind SQL Injection.This issue affects affiliate-toolkit: from n/a through 3.9.1.

### CVE-2026-42720

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-07T10:17:35.743 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Sarah Giles Dynamic User Directory dynamic-user-directory allows Blind SQL Injection.This issue affects Dynamic User Directory: from n/a through 2.4.

### CVE-2026-93678

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-07T01:16:35.580 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to obtain sensitive information due to improper authorization.

### CVE-2026-106492

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-269;CWE-863` |
| Published | 2026-10-06T21:17:18.220 |

Backstage is an open framework for building developer portals. Prior to 0.16.1 and 0.17.8, the @backstage/backend-defaults package is affected by improper preservation of access restrictions during service credential delegation. An external service credential configured with access restrictions (e.g., read-only) could bypass those restrictions by routing requests through plugin delegation paths. This could allow a restricted service to perform operations beyond its intended scope, including write operations on plugins it was restricted to read-only access for. This issue is fixed in versions 0.16.1 and 0.17.8.

### CVE-2026-101152

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-10-06T20:17:09.243 |

Insufficient validation in the Single Sign-On (SSO) login flow could allow a remote, unauthenticated attacker to craft a URL that, when clicked by a user, causes the identity provider (IdP) to deliver authentication material to an attacker-controlled URL instead of to CloudVision.

### CVE-2026-63697

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-06T19:18:15.447 |

Dell System Update, versions prior to 2.3.0.0, contains an Improper Certificate Validation vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-105855

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-06T17:17:21.430 |

Payload is a free and open source headless content management system. In versions before 3.90.0 and canary versions before 4.0.0-canary.34, the server fails to enforce a field-level access.update restriction on the password field of an authentication collection. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-92532

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-07T11:17:20.287 |

Unrestricted file upload vulnerability in the BugTracker.NET attachment functionality. An authenticated user with administrator privileges could modify the application configuration to store files in a directory accessible via the web interface. Due to the lack of proper file extension validation, an attacker could upload a malicious ASPX file and subsequently execute it on the server. A successful exploit could allow arbitrary code execution with the privileges of the account used by the web service.

### CVE-2026-92531

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-07T11:17:20.080 |

Operating system command injection vulnerability in the SVN integration component of BugTracker.NET. The application incorporates the value of the field corresponding to the repository into an svn.exe command without properly validating it. An authenticated user with administrator privileges could store manipulated arguments in the database and subsequently cause them to be processed by the revision comparison functionality. A successful exploit could allow the execution of arbitrary commands with the privileges of the account used by the application. To exploit this vulnerability, svn.exe must be installed and capable of being invoked by the service.

### CVE-2026-82212

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-07T07:17:01.493 |

The Nexi XPay Build WordPress plugin through 7.6.2 does not correctly validate the security token on its payment notification route, accepting the request when the target order has no stored token, which allows unauthenticated attackers to mark arbitrary orders as paid, or to mark genuinely paid orders as failed.

### CVE-2026-93447

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-07T01:16:34.787 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow an attacker with access to the server secret and Redis write access to submit a malicious serialized cache value. When the value was retrieved, deserialization could have executed attacker-controlled code with the privileges of the service process.

### CVE-2026-93443

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T01:16:34.523 |

IBM Langflow OSS 1.0.0 through 1.12.2 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in code.

### CVE-2026-106118

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-06T19:17:42.640 |

ImageSharp is a 2D graphics library. From 3.0.0 until 4.1.1, tiled TIFF decoding allocates a destination buffer using TileWidth but TiffDecompressorsFactory.Create constructs T4, T6, and Modified Huffman decompressors using the full frame width. TiffDecoderCore.DecodeTilesChunky can therefore direct frame-width fax scanlines into a tile-width buffer when TileWidth is smaller than ImageWidth. The mismatch causes attacker-controlled out-of-bounds writes, heap corruption, and process termination even with legal per-row run codes. This tiled-path vulnerability is distinct from oversized CCITT runs in strip decoding. This issue is fixed in version 4.1.1.

### CVE-2026-106117

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-06T18:16:53.550 |

ImageSharp is a 2D graphics library. From 3.0.0 until 4.1.1, decoding a strip TIFF using CCITT Group 3 or Modified Huffman compression can pass attacker-expanded runs to BitWriterUtils.WriteBits without first checking the current row width. T4TiffCompression.WritePixelRun can accumulate oversized makeup-code runs, and ModifiedHuffmanTiffCompression.Decompress validates the width only after writing. The unchecked writes can overflow the strip buffer, corrupt heap memory, and terminate the process. This strip-path vulnerability is distinct from the tiled decompressor-width mismatch. This issue is fixed in version 4.1.1.

### CVE-2026-106115

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-06T18:16:53.250 |

ImageSharp is a 2D graphics library. From 2.1.0 until 4.1.2, the TIFF CCITT Group 4 encoder allocates Width times rowsPerStrip bytes even though T6BitCompressor.CompressStrip can emit encoded row data and two 12-bit end-of-facsimile-block codes beyond that capacity. TiffCcittCompressor.WriteCode performs unchecked writes, and a decode-and-re-encode flow can inherit TiffCompression.CcittGroup4Fax and one-bit metadata from attacker-supplied input. The resulting out-of-bounds writes can corrupt memory and terminate the process. This issue is fixed in version 4.1.2.

### CVE-2026-106113

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-06T18:16:52.953 |

ImageSharp is a 2D graphics library. From 2.0.0 until 4.1.2, decoding an attacker-supplied 32-bit floating-point TIFF as Image<HalfVector4> and applying HistogramEqualization can produce a non-finite or out-of-range luminance in ColorNumerics.GetBT709Luminance. GrayscaleLevelsRowOperation.Invoke uses the resulting value as an unchecked histogram offset, causing an unsafe out-of-range access and process termination. Adaptive Histogram Equalization and AutoLevel are not affected by this report. This issue is fixed in version 4.1.2.

### CVE-2026-106112

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-06T18:16:52.810 |

ImageSharp is a 2D graphics library. From 4.0.0 until 4.1.2, ICC LUT16 conversion accepts more than four output channels even though ClutCalculator.Calculate and LutEntryCalculator.CalculateLut store intermediate and output values in Vector4. When DecoderOptions.ColorProfileHandling is set to Convert, a malformed embedded profile can direct interpolation and output-LUT operations to write one float per declared channel beyond the four-float destination. This can corrupt memory and terminate the process; the default Preserve mode does not run ICC conversion. This issue is fixed in version 4.1.2.

### CVE-2026-106110

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-06T18:16:52.490 |

ImageSharp is a 2D graphics library. From 2.0.0 until 4.1.2, the TIFF CCITT Group 3 encoder allocates an undersized compressed-data buffer for narrow 1-bit images. TiffCcittCompressor.Initialize does not reserve enough space for the row data and T4 end-of-line codes, and T4BitCompressor.CompressStrip reaches unchecked writes when TiffCompression.CcittGroup3Fax is selected directly or inherited from decoded TIFF metadata. An attacker-controlled encode or decode-and-re-encode flow can write beyond the logical output span, corrupt process memory, and terminate the process. This issue is fixed in version 4.1.2.

### CVE-2026-95140

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-06T17:17:28.087 |

kkFileView v5.0.0 through v5.0.2 contains a directory traversal vulnerability in FileController.java. The fileUpload, createFolder and existsFile endpoints accept a "path" parameter that is concatenated into the upload base path without validation, allowing unauthenticated attackers to create arbitrary directories and write arbitrary files outside the intended fileDir root via a crafted multipart request

### CVE-2026-104850

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-345;CWE-522` |
| Published | 2026-10-06T17:17:15.827 |

MCP TypeScript SDK is the official TypeScript SDK for Model Context Protocol servers and clients. Starting in version 1.12.0 and prior to versions 1.31.0 and 2.2.0, the SDK's OAuth client support let the MCP server a client connected to decide which authorization server received the client's OAuth credentials. Stored and pre-provisioned credentials were not bound to the authorization server they belong to. A malicious or compromised MCP server could name its own authorization server in its protected resource metadata. Without any user interaction, the client would send that server the `refresh_token` and `client_secret` stored from an earlier sign-in (1.x), or the configured `client_secret` or signed assertion of a bundled non-interactive provider (1.x and 2.x). Only those applications that use the SDK as an MCP client over HTTP with an `authProvider`: your own `OAuthClientProvider`, or the bundled `ClientCredentialsProvider`, `PrivateKeyJwtProvider`, `StaticPrivateKeyJwtProvider` or (2.x) `CrossAppAccessProvider` and that may connect to an MCP server the owners does not fully trust while holding credentials for a legitimate authorization server are affected. `@modelcontextprotocol/sdk` 1.31.0 (1.x) and `@modelcontextprotocol/client` 2.2.0 (2.x) patch the issue. A workaround for those who cannot upgrade is available. 2.0.0 and 2.1.0 already accept `expectedIssuer`. On 1.x, the only workaround is to connect OAuth-enabled clients only to MCP servers you trust.

### CVE-2026-105791

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88;CWE-184` |
| Published | 2026-10-06T15:17:15.840 |

Microsoft UFO is an open-source framework for intelligent automation across devices and platforms. Prior to 3.0.9, the run_shell tool in the CommandLineExecutor component of ufo/client/mcp/local_servers/cli_mcp_server.py validates only the first token of the bash_command parameter and permits explorer.exe. On Windows, explorer.exe delegates its following path argument to ShellExecute, so an attacker-influenced agent call can launch an arbitrary executable or script as the desktop user even though the subprocess uses shell=False. Exploitation depends on a user running an affected agent workflow and on inducing the tool call, but successful execution can access or modify that user's files, tokens, and sessions. This issue is fixed in version 3.0.9.

### CVE-2026-107177

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1394` |
| Published | 2026-10-07T13:17:20.827 |

Express Gateway through 1.16.11 contains a hardcoded cryptographic key vulnerability that allows attackers with datastore access to decrypt stored OAuth 2.0 token secrets via the default crypto.cipherKey 'sensitiveKey'. Attackers who can read Redis can decrypt tokenEncrypted values and combine them with stored token IDs to obtain valid bearer tokens for any user.

### CVE-2026-82162

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-175` |
| Published | 2026-10-06T19:18:16.150 |

Dell Command | Configure (DCC), versions prior to 5.2.3.35, contain an Improper Handling of Mixed Encoding vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Elevation of Privileges.

### CVE-2026-106279

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-10-06T19:17:55.603 |

Incorrect reference resolution in Passwords in Google Chrome on on iOS prior to 155.0.8059.39 allowed a local attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a local program. (Chromium security severity: Medium)

### CVE-2026-79809

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:32.483 |

An unauthenticated path traversal vulnerability exists in an API endpoint of ClearPass Policy Manager. Successful exploitation of this vulnerability allows an unauthenticated remote attacker to influence authorization decisions and be assigned an unintended role.

### CVE-2026-106451

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367;CWE-377` |
| Published | 2026-10-06T20:17:27.173 |

yawkat LZ4 Java provides LZ4 compression for Java. From 1.7.0 until 1.11.4, net.jpountz.util.Native.load() uses File.createTempFile to create an exclusive temporary .lck file but derives the native-library path by removing the suffix, then FileOutputStream opens that predictable path without exclusive creation, allowing another local user with access to the same shared temporary directory to create or replace the library file before System.load() uses it. Successful exploitation depends on shared-directory permissions, host protections, and winning the race, and can execute native code as the victim; hardened systems may instead cause library loading to fail and fall back to Java implementations. Configurations using a system library, a private java.io.tmpdir, or Java-only implementations are not affected. This issue is fixed in version 1.11.4.

### CVE-2026-71168

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-06T19:18:15.847 |

Dell System Update, versions prior to 2.3.0.0, contains an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-89417

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-07T09:17:05.817 |

The OMGF | GDPR/DSGVO Compliant, Faster Google Fonts. Easy. plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 's' Search Parameter via comments-atom Feed in all versions up to, and including, 6.3.10 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires that the front-end server serves the retained .tmp file without a Content-Type or X-Content-Type-Options header, enabling MIME-sniffing browsers such as Chromium to execute the injected script — a condition present by default on many Apache and nginx/php-fpm deployments.

### CVE-2026-104677

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T07:16:58.260 |

The WP Coder  WordPress plugin before 4.5.2 does not restrict access to its PHP code-execution feature to administrators, gating it on a content capability that the Editor role holds by default, which allows Editor-level users to save and execute arbitrary PHP code on the server and fully compromise the site.

### CVE-2026-102173

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-07T06:16:33.217 |

The Kirki – Freeform Page Builder, Website Builder & Customizer plugin for WordPress is vulnerable to Stored Cross-Site Scripting via registration metadata in all versions up to, and including, 6.3.1 This is due to insufficient escaping in `ExceptionalElements::image_element()`, which concatenates a user-meta value straight into an `<img src="…">` attribute. This makes it possible for unauthenticated attackers to inject arbitrary web scripts that execute whenever a user accesses a page rendering a Kirki users collection whose image element is bound to one of the nine registration meta fields. Requires public user registration to be enabled and a published page carrying a `kirki-register` element, which prints the required element nonce into the public markup.

### CVE-2026-79811

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:32.720 |

A SQL injection vulnerability in the API of ClearPass Policy Manager could allow a remote authenticated attacker with administrative privileges to conduct SQL injection attacks against the ClearPass Policy Manager instance. Successful exploitation could allow an attacker to execute arbitrary database commands.

### CVE-2026-79810

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-06T20:17:32.597 |

Remote code execution vulnerabilities exist in the affected interface of HPE Networking ClearPass Policy Manager that could allow an authenticated remote attacker with high privileges to execute arbitrary code. Successful exploitation could allow an attacker to execute arbitrary commands on the underlying operating system.

### CVE-2026-103007

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-06T20:17:13.930 |

Incorrect Authorization (CWE-863) in Elasticsearch can lead to Privilege Escalation via a delegated administrative privilege whose scope is not fully enforced during authorization checks. Elasticsearch contains an incorrect authorization weakness in a configurable, non-default privilege that lets an administrator delegate limited role-management capability to another user, scoped to specific indices. The authorization check that enforces this scoping does not correctly account for a role-definition setting that can expand the matched index set. A user holding this delegated privilege with a broadly-scoped index pattern can exploit this inconsistency by updating their own assigned role to gain access to indices that should remain restricted, including internal security data. This can enable further escalation up to full administrative control of the cluster.

### CVE-2026-101153

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-06T20:17:09.400 |

On affected versions of CloudVision Portal (on-premises) or CloudVision Sensor, a path traversal vulnerability exists. An authenticated user with sufficient high privileges could exploit this to extract unintended data from the Sensor.

### CVE-2026-105861

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-346` |
| Published | 2026-10-06T17:17:22.277 |

Payload is a free and open source headless content management system. In versions after 3.0.0 and before 3.90.0, authenticated external URL-based upload retrieval can forward authentication data to a redirected destination that was not verified as trusted, potentially exposing a valid session to an unintended recipient. This issue is fixed in version 3.90.0.

### CVE-2026-46434

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-07T14:17:10.277 |

wger is a free, open-source workout and fitness manager. Prior to version 2.6, a user with only the `gym_trainer` permission can deactivate any account in the same gym, including `gym_manager` and `general_gym_manager` accounts. The `UserDeactivateView` grants access to anyone holding any one of `gym.manage_gym`, `gym.manage_gyms`, or `gym.gym_trainer` (OR logic via `WgerMultiplePermissionRequiredMixin`), and performs no privilege-hierarchy check to prevent a lower-privileged role from disabling a higher-privileged one. Version 2.6 fixes the issue.

### CVE-2026-43976

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-07T14:17:09.887 |

wger is a free, open-source workout and fitness manager. Prior to version 2.6, five gym management views in wger apply a flawed gym-scope guard (`gym_a != gym_b`) that silently passes when both operands are `None`. A trainer with `gym.gym_trainer` and `gym.add_adminusernote` permissions and no gym assignment (`gym=None`) can read private admin notes, uploaded documents, gym contracts, user configuration, and user permission data for **any other unaffiliated user** on the instance. The subsequent querysets filter only on the attacker-supplied `member_id` with no secondary gym-scoped validation, so all records are disclosed. Version 2.6 fixes the issue.

### CVE-2026-107180

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-10-07T13:17:22.003 |

On MISP instances configured to require TOTP enrolment (Security.otp_required), the enforcement of the mandatory two-factor authentication setup applied only to standard browser requests. An authenticated user who had not yet enrolled in TOTP could bypass the forced setup by issuing any non-browser request type, including AJAX/XHR calls, REST API requests, .json format URLs, restSearch queries, or automation actions. Because these machine-readable request shapes cannot follow the redirect that the browser path uses to send the user to the TOTP enrolment page, the guard simply skipped the check and the user retained full access to the instance without completing the required second-factor setup.

The initial fix (commit 8deb0619e) added a guard specifically for AJAX requests. A follow-up fix (commit 6b527ba6e) broadened the guard to cover every non-browser request shape, while preserving the exemption for identities authenticated via API key (logged_by_authkey flag).

Impact: an authenticated user on an otp_required instance can operate with full access indefinitely without enrolling in TOTP, nullifying the instance-level two-factor authentication policy.

Affected version: <2.5.48

### CVE-2026-105138

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-07T13:17:16.977 |

Obot 0.12.0 before 0.26.2 contains an insufficiently protected credentials vulnerability that allows authenticated users to read static secrets set on MCP catalog entries by admins or power users. Basic users granted an entry by access control rules can request GET /api/all-mcps/entries/{entry_id} to obtain plaintext API keys or tokens and abuse them against backend services.

### CVE-2026-107159

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-369` |
| Published | 2026-10-07T12:17:09.283 |

MiniUPnPd through 2.3.11 built with --strict contains a divide-by-zero vulnerability in ProcessSSDPData() that allows unauthenticated local network attackers to crash the daemon. Attackers can send a single multicast M-SEARCH datagram with MX: 0 and a known ST to port 1900, triggering SIGFPE and denying UPnP IGD service.

### CVE-2026-92533

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-24` |
| Published | 2026-10-07T11:17:20.450 |

Path traversal vulnerability in the BugTracker.NET file download component. The parameter used to specify the file name does not properly validate user-supplied paths. An authenticated remote attacker could enter a manipulated path to access files located outside the intended directory. Successful exploitation could allow the attacker to read system files accessible to the account used by the application.

### CVE-2026-5703

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-35` |
| Published | 2026-10-07T09:17:05.673 |

Path traversal vulnerability in the Satel Iberia SenNet Datalogger Serie 200, specifically in the web portal provided by the device, which allows an authenticated user to read any file or list any directory accessible to the system user running the web server. This is possible by modifying the URL to include a path traversal payload. Successful exploitation of this vulnerability could allow an attacker to access critical system files containing confidential information.

### CVE-2026-87971

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-07T07:17:01.950 |

The If-So Dynamic Content  WordPress plugin before 1.10.2 does not validate the URL scheme of a request-supplied value before reflecting it into a link on an admin page, allowing attackers to execute arbitrary JavaScript in the browser of a logged-in user who opens a crafted link.

### CVE-2026-105316

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-07T07:16:59.403 |

The Magee Shortcodes WordPress plugin through 2.1.1 does not sanitise and escape user input in some of its AJAX actions, which are available to unauthenticated users, before reflecting it back in the response, leading to Reflected Cross-Site Scripting.

### CVE-2026-105811

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-06T21:17:04.447 |

Authorization bypass through a user-controlled key in the optional Amazon Q Business Lambda hook sample ( q-business-lambda-hook https://github.com/aws-solutions-library-samples/qnabot-on-aws/blob/main/source/docs/lambda_hooks/README.md ), available with QnABot on AWS versions 7.0.0 through 7.4.5, might allow an authenticated remote user to read arbitrary Amazon S3 objects in the deploying AWS account. This sample solution provides an example Lambda hook and requires separate, manual deployment and additional setup. It is not deployed automatically with QnABot. Customers who have not deployed this optional sample hook are not affected and do not need to take action. 



To remediate this issue, affected customers should update the QnABot on AWS stack to version 7.4.6 or later and then redeploy the Amazon Q Business Lambda hook sample stack. Updating the QnABot on AWS stack alone does not deliver the fix.

### CVE-2026-103009

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-06T20:17:14.247 |

Authorization Bypass Through User-Controlled Key (CWE-639) in Elasticsearch can lead to Information Disclosure via a specially crafted cross-cluster search request that references an unauthorized shard identifier. Elasticsearch contains an authorization bypass weakness in its handling of cross-cluster search requests made through the Remote Cluster Security (RCS) 2.0 model. An authorization check validates a request against one identifying attribute of the target shard, while a separate, independently-supplied identifying attribute in the same request determines which shard is actually accessed. A holder of a cross-cluster API key authorized for one index can craft a request whose two identifying attributes refer to different indices, causing the request to be authorized against an index they can access while actually operating against a different, unauthorized index. This can expose that index's document contents, field mappings, and other metadata, and in limited cases allows modification of retention-lease state on the unauthorized index.

### CVE-2026-102169

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-06T20:17:12.197 |

On affected Arista Wi-Fi access points with Captive Portal enabled, an unauthenticated wireless client connected to a captive-portal-enabled SSID can crash the portal service with a crafted HTTP request. The service automatically restarts, but a sustained low-rate attack can cause a persistent denial of service of the captive portal. Remote code execution is not possible.

### CVE-2026-102168

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-06T20:17:12.067 |

On affected Arista Wi-Fi access points with Captive Portal enabled, an unauthenticated wireless client connected to a Captive-Portal-enabled SSID can crash the portal service with a crafted HTTP request. This results in a temporary denial of service until the service automatically restarts. Remote code execution is not possible.

### CVE-2026-102158

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-10-06T20:17:10.837 |

Improper validation of selected CloudVision CUE application programming interface (API) request parameters may allow an authenticated network user to perform SQL injection against the backend impacting its availability.

### CVE-2026-102155

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-06T20:17:10.400 |

An XML External Entity (XXE) injection vulnerability in the WiFi-server Spectralight application allows any authenticated user to send malicious requests, leading to arbitrary local file disclosure and partial denial of service.

### CVE-2026-83550

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-489` |
| Published | 2026-10-06T19:18:16.280 |

A flaw was found in postgres-exporter. Due to the blank import of `net/http/pprof`, debug endpoints are exposed on the unauthenticated metrics listener. A remote attacker within the cluster network can access these endpoints. This allows for information disclosure, potentially revealing process arguments, full goroutine stacks, and sensitive data like database connection strings or passwords from heap dumps. Additionally, repeated CPU profiling through these endpoints can lead to a denial of service.

### CVE-2026-104944

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-823` |
| Published | 2026-10-06T19:17:40.640 |

TP-Link Tapo
C500 v2.0 contains an out-of-bounds function-pointer dispatch in its TDP
(TP-Link Device Protocol) daemon. A single unauthenticated UDP datagram can
cause an invalid indirect call, crashing the main service and resulting in a
denial-of-service condition.





Successful
exploitation may allow an unauthenticated attacker with network access to the
affected UDP service to repeatedly crash the TDP daemon, disrupting normal
device operation and availability. No authentication, session establishment, or
pairing is required to trigger the condition.

### CVE-2026-106106

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:P/VC:H/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-497` |
| Published | 2026-10-06T18:16:52.030 |

Quasar Framework is a framework for building high-performance Vue.js user interfaces. Prior to @quasar/render-ssr-error 2.2.4 and @quasar/app-vite 3.3.0, renderSSRError() in utils/render-ssr-error/src/index.js used diagnostic data from utils/render-ssr-error/src/env.js to serialize process.env, request headers, and cookies into the HTTP page returned by serve.devError(), while the development server listened on all interfaces by default. Any network-adjacent client that reaches an SSR or SSG render failure through this development-only error path can obtain shell environment secrets. The renderer escaped only one exact lowercase script closing-tag spelling, so case variants and valid closing-tag delimiter variants in reflected diagnostic data could terminate the script element and inject markup; executing the injected code in a developer browser additionally requires the payload to accompany that developer's request. This issue is fixed in @quasar/render-ssr-error 2.2.4 and @quasar/app-vite 3.3.0.

### CVE-2026-106103

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-10-06T18:16:51.523 |

Quasar Framework is a framework for building high-performance Vue.js user interfaces. Prior to @quasar/icongenie 6.1.1, the icongenie generate --profile command accepted folder and name values from a user-supplied profile without constraining the resolved destination to the Quasar project directory. icongenie/lib/utils/get-assets-files.js joined those values with appDir, while icongenie/lib/utils/validate-profile-object.js required only non-empty strings, allowing parent-directory traversal. A developer who runs a crafted profile can cause generated image content to be written or overwritten at any path writable by that user, potentially modifying shell startup files, build scripts, or other executable configuration. This issue is fixed in version 6.1.1.

### CVE-2026-106100

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-915` |
| Published | 2026-10-06T17:17:23.957 |

Payload is a free and open source headless content management system. In @payloadcms/db-mongodb versions before 3.87.0 and canary versions before 4.0.0-canary.20, an authenticated user who can update a document can modify fields that field-level write access control does not permit that user to change. The Postgres and SQLite adapters are not affected. This issue is fixed in versions 3.87.0 and 4.0.0-canary.20.

### CVE-2026-105867

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-06T17:17:23.137 |

Payload is a free and open source headless content management system. In @payloadcms/storage-s3 versions before 3.90.0 and canary versions before 4.0.0-canary.34, an authenticated user can overwrite an existing S3 object belonging to another upload collection when client uploads are enabled for multiple collections sharing a bucket and useCompositePrefixes is false or unset. This bypasses the target collection's access controls and prior file validation. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-105860

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-06T17:17:22.133 |

Payload is a free and open source headless content management system. In @payloadcms/plugin-multi-tenant versions before 3.90.0 and canary versions before 4.0.0-canary.34, the default tenant array field access allows an authenticated user to assign the user's own account to other tenants. Deployments that replace the default behavior with secured tenants arrayFieldAccess.create and tenants arrayFieldAccess.update functions are not affected by this behavior. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-105853

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-06T17:17:21.140 |

Payload is a free and open source headless content management system. In versions from 3.0.0 before 3.90.0 and canary versions before 4.0.0-canary.34, token refresh responses and password reset responses can independently return hidden or read-restricted fields that the requesting user cannot access. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-105847

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-639` |
| Published | 2026-10-06T17:17:20.143 |

Payload is a free and open source headless content management system. In versions from 3.0.0 before 3.90.0 and canary versions before 4.0.0-canary.34, a user who can query a collection with a polymorphic join to sensitive fields can infer hidden or read-restricted values, including password-reset tokens, through polymorphic join filters. This issue is fixed in versions 3.90.0 and 4.0.0-canary.34.

### CVE-2026-70411

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-06T16:17:09.877 |

Dell Container Storage Modules (CSM), versions prior to 1.18.0, contains a Missing Authentication for Critical Function vulnerability in the csm-authorization-tenant gRPC service (TenantService). An unauthenticated adjacent network attacker could potentially exploit this vulnerability, leading to unauthorized creation of tenant entities, cross-tenant role injection, and modification of storage access control flags.

### CVE-2026-26287

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-696` |
| Published | 2026-10-06T16:17:07.180 |

External Secrets Operator reads information from a third-party service and automatically injects the values as Kubernetes Secrets. Starting in version 0.10.0 and prior to version 1.3.2, a bug in the `webhook` generator initialization order incorrectly cleared the label-enforcement flag (`EnforceLabels`) after it was set, resulting in the provider-side check for `external-secrets.io/type=webhook` being skipped (and the operation to succeed while it should have failed with `secret does not contain needed label 'external-secrets.io/type: webhook'. Update secret label to use it with webhook`. Version 1.3.2 contains a patch.

### CVE-2026-56906

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-06T19:18:14.920 |

In ep_free of eventpoll.c, there is a possible use-after-free due to a race condition. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.
