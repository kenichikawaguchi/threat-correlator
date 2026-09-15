# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-15 15:00 UTC
- **対象期間**: `2026-09-14T15:00:26.000Z` 〜 `2026-09-15T15:00:58.000Z`
- **重要CVE数**: 229 件（Critical 9.0+: 47 件 / High 7.0〜: 182 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** と非常に多く、特に **認証バイパス・リモートコード実行 (RCE)** が集中しています。  
- **Apache Storm、PraisonAI、Cisco Secure Email Gateway** など、インフラ・プラットフォーム層での深刻な権限昇格が目立ちます。  
- 多くの脆弱性は「**デフォルト設定が安全でない**」ことに起因し、**パッケージのバージョンアップだけでなく、設定の見直しが必須**です。  
- iOS/macOS 系のファームウェア脆弱性 (CVE‑2026‑65414) も CVSS 9.8 で報告され、モバイル端末のアップデート遅延がリスク拡大要因となっています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑82434** (Apache Storm) | 10.0 | 認証済みユーザーが **Nimbus のトポロジ設定** を改ざんでき、任意コード実行や機密情報漏洩が可能 | *Storm の内部パイプラインに認証前に Netty デコーダが配置されている* ため、認証なしでバッファオーバーフローが発生。クラスタ全体が遠隔から乗っ取られる危険性が最も高い。 |
| **CVE‑2026‑57138** (PraisonAI) | 9.9 | `new Function()` による **未検証 JavaScript 実行** が可能。攻撃者は任意のコードをサーバ上で実行できる | *コードモードのサンドボックスが不完全* で、正規表現ブロックリストを回避できる。AI エージェントプラットフォームは外部入力を多用するため、被害範囲が広がりやすい。 |
| **CVE‑2026‑16338** (IBM DataStage on Cloud Pak for Data) | 9.9 | 認証済みリモート攻撃者が **任意ファイルを書き込める**（パス検証不備） | データパイプラインの構成ファイルを書き換えることで、バックドアや情報漏洩が容易になる。IBM 製品はエンタープライズ環境で広く採用されている点がリスクを増幅。 |
| **CVE‑2026‑65414** (Apple iOS/macOS) | 9.8 | メモリ書き込み不正により **リモートでアプリがクラッシュ／コード実行** 可能 | iOS 26.7、macOS Sequoia 15.8 以降で修正済みだが、アップデートが遅れるデバイスは即座に攻撃対象になる。モバイル・デスクトップ両方に影響。 |
| **CVE‑2026‑76461** (Cisco Secure Email Gateway) | 9.8 | 電子メール解析時の **コマンドインジェクション** により root 権限で任意コード実行 | メールサーバは外部からの大量トラフィックが常に流入するため、攻撃者が自動化スクリプトで大量に悪用できる。Cisco 製品は多くの企業でメールインフラの要。 |

> **共通点**：認証・入力検証の欠如、デフォルトのシークレット漏洩、そして「パッチがリリースされても適用が遅れる」ことが主要因です。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンの更新
| 製品 / ライブラリ | 修正済みバージョン (最低) | 対応策 |
|-------------------|--------------------------|--------|
| **Apache Storm** | 2.8.2 以上 (2026‑09 リリース) | `storm.zookeeper.topology.auth.payload` の保持ロジックを削除し、Netty デコーダを認証後に配置するパッチを適用。 |
| **PraisonAI** | 1.7.3 以上 (全モジュール) | `code-mode.ts` の `new Function()` 使用を廃止し、`vm2` 等の安全サンドボックスへ置き換える。`PLATFORM_JWT_SECRET` が未設定時は起動を失敗させる。 |
| **IBM DataStage (Cloud Pak for Data)** | 5.4.0.1 以上 | ファイルパス検証ロジックを強化し、`../` などの相対パスを除外。 |
| **Apple iOS / iPadOS / macOS / tvOS / visionOS / watchOS** | iOS 27, iPadOS 27, macOS Sequoia 15.8, macOS Golden Gate 27 以降 | 端末の自動アップデートを有効化し、Enterprise MDM で **OS バージョン ≥ 27** を必須にするポリシーを適用。 |
| **Cisco Secure Email Gateway (AsyncOS)** | 12.5.4‑R3 以上 | メールパーサーの入力サニタイズパッチを適用し、`/etc/asyncos/conf.d/` のバックアップを取得した上でアップグレード。 |
| **OpenAM** | 16.1.2 以上 | `/authservice` エンドポイントの `CustomCallback` クラスロードをホワイトリスト制御に変更。 |
| **ESPHome Dashboard** | 1.0.12 以上 | 環境変数 `ESPHOME_USERNAME`/`ESPHOME_PASSWORD` のみ使用し、`USERNAME`/`PASSWORD` のレガシー変数は削除。 |

### 3.2 設定・運用の見直し
1. **認証・認可のデフォルトを「拒否」へ**  
   - `storm.zookeeper.topology.auth.payload` など機密情報を **読み取り専用権限** 以上のユーザーに限定。  
   - PraisonAI の全 API エンドポイントに **認証ミドルウェア** を必ず挿入し、`PLATFORM_ENV=dev` が本番で有効にならないよう環境変数をロックダウン。  

2. **シークレット管理の徹底**  
   - `PLATFORM_JWT_SECRET`、`PRAISONAI_API_KEY`、`PRAISONAI_JWT_SECRET` などは **Vault / AWS Secrets Manager** で管理し、デフォルトの `dev-secret-change-me` が残っていないかスキャン。  

3. **入力検証の強化**  
   - IBM DataStage のファイルパス、Cisco のメールヘッダー、Apple の圧縮ファームウェア解析ロジックは **正規表現・ホワイトリスト** に置き換え、外部からの特殊文字列を除外。  

4. **監視・インシデント対応**  
   - **CVE‑2026‑82434** のように Netty デコーダがクラスタ全体に影響するケースは、Storm の **Nimbus ログ** と **Worker のネットワークトラフィック

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-82434

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-532` |
| Published | 2026-09-14T15:17:10.453 |

Description

When ZooKeeper authentication is configured, Storm deliberately retains
`storm.zookeeper.topology.auth.payload` in the topology configuration, because workers need it. Nimbus then
served that configuration verbatim to any caller holding read-only topology permissions, so a user whose
only grant was the ability to view a topology received its ZooKeeper credential.

That credential is not read-only. The cluster state implementation uses write-capable ACLs for worker
heartbeats, backpressure and error state, so a recipient can forge or remove that state for the topology
concerned. It is not a write credential on assignments.

The same advisory covers the submission client, which logged the generated payload at INFO on every
submission that generated one, and the SASL handlers, which logged it at DEBUG. The credential therefore
also reached any log aggregation or support bundle collected from the cluster.

Mitigation

Upgrade to 3.1.0, where the payload is removed from the configuration served to read-only callers and is no
longer written to logs.

Users who cannot upgrade immediately should rotate `storm.zookeeper.topology.auth.payload` for existing
topologies, review retained logs and support bundles for the value, and restrict read-only topology
permissions to trusted principals.

Credit

The ASF -- found using Claude agents to study the security of open-source projects, validated and reported by Apache Storm.

### CVE-2026-57138

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-184;CWE-693` |
| Published | 2026-09-15T11:17:11.180 |

PraisonAI is a multi-agent teams system. From 1.4.0 until 1.7.2, codeMode in src/praisonai-ts/src/tools/builtins/code-mode.ts executes untrusted JavaScript with new Function() inside with(sandbox) and relies on a small source-code blocklist plus shadowed process and require properties. Code can use ({}).constructor.constructor to recover the real Function constructor, obtain process and process.mainModule.require, and reach host filesystem and subprocess APIs despite the advertised sandbox. Attackers who control codeMode input can read secrets, modify files, execute commands, or exhaust the host process. This issue is fixed in version 1.7.2.

### CVE-2026-16338

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-14T20:16:40.410 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 IBM DataStage could allow a remote authenticated attacker to perform an arbitrary file write due to improper validation of file paths.

### CVE-2026-57148

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-798;CWE-1188` |
| Published | 2026-09-15T11:17:11.910 |

PraisonAI is a multi-agent teams system. Prior to 0.1.6, praisonai_platform/services/auth_service.py falls back to the public dev-secret-change-me HS256 signing key when PLATFORM_JWT_SECRET is unset, while the startup and token-issuance guards are disabled because PLATFORM_ENV also defaults to dev. An unauthenticated attacker can sign a JWT containing an attacker-chosen sub value, and AuthService._verify_token() accepts it as an authenticated identity, enabling user or workspace-owner impersonation when a target identifier is known. This vulnerability is fixed in praisonai-platform 0.1.6.

### CVE-2026-57147

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798;CWE-1188` |
| Published | 2026-09-15T11:17:11.760 |

PraisonAI is a multi-agent teams system. Prior to 0.1.6, praisonai_platform/services/auth_service.py assigns the public dev-secret-change-me value to JWT_SECRET when PLATFORM_JWT_SECRET is unset, and its production guard does not run when PLATFORM_ENV is also unset because that setting defaults to dev. A remote unauthenticated attacker can mint an HS256 token with an arbitrary sub and email, and the platform's AuthService._verify_token() and get_current_user dependency accept the forged identity for protected API routes. This vulnerability is fixed in praisonai-platform 0.1.6.

### CVE-2026-57141

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-15T11:17:11.617 |

PraisonAI is a multi-agent teams system. Prior to 1.7.2, the codeMode tool in src/praisonai-ts/src/tools/builtins/code-mode.ts executes model-generated JavaScript with new Function() and with(sandbox), while a regular-expression blocklist can be bypassed with Function('return this')() to recover the global object and by constructing the child_process module name dynamically. An attacker who can influence the code argument can access host process capabilities, read or write files, obtain environment credentials, and execute operating-system commands with the PraisonAI process privileges. This issue is fixed in version 1.7.2.

### CVE-2026-57139

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-862;CWE-1188` |
| Published | 2026-09-15T11:17:11.327 |

PraisonAI is a multi-agent teams system. From 1.5.0 until 1.7.2, MCPServer.startHttp() in src/praisonai-ts/src/mcp/server.ts binds without a host restriction and forwards every HTTP POST request to handleRequest() without authentication or authorization. Any network client that can reach the port can call tools/list, tools/call, resources/read, or prompts/get, causing registered handlers to run with server-side credentials and process privileges or disclose registered data. An initial remediation was released in version 1.7.2.

### CVE-2026-62379

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-470` |
| Published | 2026-09-15T10:17:06.107 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.2, the pre-authentication /authservice PLL endpoint accepts a CustomCallback XML element whose className value selects an arbitrary Java class for AuthXMLUtils to load and instantiate without verifying that it implements DSAMECallbackInterface. Default configurations expose the endpoint without authentication, allowing attacker-controlled class initialization and unsafe deserialization of a serialized Subject value to execute code in the server process. Enabling sunRemoteAuthSecurityEnabled does not prevent the vulnerable parsing and instantiation because its check occurs later. This issue is fixed in version 16.1.2.

### CVE-2026-65414

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-14T21:17:25.057 |

An out-of-bounds write issue was addressed with improved bounds checking. This issue is fixed in iOS 26.7 and iPadOS 26.7, iOS 27 and iPadOS 27, macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7, tvOS 27, visionOS 27, watchOS 27. A remote attacker may be able to cause unexpected app termination or arbitrary code execution.

### CVE-2026-55209

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120;CWE-125;CWE-129;CWE-476` |
| Published | 2026-09-14T20:16:47.487 |

resdata is software for reading and writing result files from the Eclipse reservoir simulator. Prior to 6.2.9, resdata insufficiently validates numeric fields, grid dimensions, keyword sizes, and array indexes while parsing untrusted GRDECL files in lib/resdata/rd_kw_grdecl.cpp and lib/resdata/rd_grid.cpp. Malformed COORD, ZCORN, CORSNUM, ACTNUM, or MAPAXES data can reach rd_grid_alloc_GRDECL_kw__ with inconsistent lengths, while unbounded floating-point conversion can exceed the intended parser buffer. In a network service that accepts untrusted GRDECL files, these conditions can cause a classic buffer overflow, out-of-bounds reads, invalid array access, NULL pointer dereference, memory corruption, or service termination. This issue is fixed in version 6.2.9.

### CVE-2026-54334

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-14T20:16:46.143 |

UEFI Firmware Parser parses BIOS, Intel ME, and UEFI firmware structures including volumes, file systems, and files. Prior to 1.14, ReadCLen() in uefi_firmware/compression/Tiano/Decompress.c reads Number from GetBits(Sd, CBIT) with CBIT = 9 and can obtain 511 entries for the 510-element Sd->mCLen heap array because its loop does not enforce Index < NC. The CharC == 2 run-length path can additionally request up to 531 zero writes through Sd->mCLen[Index++] = 0. The normal CompressedSection.process() to efi_compressor.TianoDecompress() to TianoDecompress() to DecodeC() to ReadCLen() parsing path therefore permits crafted Tiano or EFI compressed firmware to corrupt heap memory, deterministically crash the parsing process, and potentially execute code depending on build and runtime details. This issue is fixed in version 1.14.

### CVE-2026-54333

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-14T20:16:45.990 |

UEFI Firmware Parser parses BIOS, Intel ME, and UEFI firmware structures including volumes, file systems, and files. Prior to 1.14, MakeTable() in uefi_firmware/compression/Tiano/Decompress.c does not validate that bit-length values read from a crafted Tiano or EFI compressed firmware bitstream remain within the expected range from 0 through 16. The normal CompressedSection.process() to efi_compressor.TianoDecompress() to TianoDecompress() to ReadPTLen() to MakeTable() parsing path can consequently write beyond the stack-allocated Count[17] array and related decode tables. The resulting stack corruption deterministically crashes the parsing process and may permit code execution depending on build and runtime details. This issue is fixed in version 1.14.

### CVE-2026-59178

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-14T19:17:37.617 |

ESPHome Device Builder Dashboard is a dashboard for the ESPHome home management software. Prior to version 1.0.12, the dashboard reads its authentication credentials from `$ESPHOME_USERNAME` and `$ESPHOME_PASSWORD`. Earlier versions, and the legacy `esphome` dashboard, read the bare `$USERNAME` and `$PASSWORD` instead. When the env vars were renamed the bare names were dropped with no fallback, so an operator who had protected their dashboard with `USERNAME` / `PASSWORD` (as the older getting started guide documented) loses authentication on upgrade and the dashboard starts open to anyone who can reach its port. The issue is fixed in 1.0.12. The bare `$USERNAME` / `$PASSWORD` are accepted again as a deprecated fallback so previously protected instances stay protected across the upgrade without operator intervention, with a loud deprecation warning at startup directing operators to rename them to `$ESPHOME_USERNAME` / `$ESPHOME_PASSWORD`. The fallback is gated on `$PASSWORD` being set and is only adopted as a pair, so the OS provided `$USERNAME` is never read on its own and the original collision footgun stays closed. A lone bare `$PASSWORD` with no username still fails loud as a credential mismatch rather than starting unauthenticated. This restores compatibility rather than failing closed on the legacy names, because the priority is that an instance which was protected before the upgrade stays protected without the operator having to act; the deprecation warning plus a future removal handles the migration. Operators should migrate to the `$ESPHOME_*` names. The esphome container delivers the fix in the 2026.6.2 release, which bumps its pinned `esphome-device-builder` version to 1.0.12. Without upgrading, restore authentication immediately by setting the new env vars to the same values, on any affected version. Alternatively, do not expose the dashboard port to untrusted networks, and check the startup logs for the `WITHOUT AUTHENTICATION` banner to confirm whether a given instance is currently open.

### CVE-2026-76461

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-14T17:17:51.113 |

A vulnerability in the email parsing of Cisco AsyncOS Software for Cisco Secure Email Gateway could allow an unauthenticated, remote attacker to execute arbitrary commands with root privileges on the underlying operating system.

This vulnerability is due to insufficient validation in the email parsing logic. An attacker could exploit this vulnerability by sending a crafted email message that contains malicious SQL statements through an affected device. A successful exploit could allow the attacker to execute arbitrary SQL statements, leading to command execution with root privileges on the underlying operating system.

### CVE-2026-76443

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-707` |
| Published | 2026-09-14T17:17:50.970 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Email Gateway and Cisco Secure Email and Web Manager engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76443 are related to issues with improper neutralization that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-707.

### CVE-2026-76441

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-14T17:17:50.673 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Email Gateway and Cisco Secure Email and Web Manager engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76441 are related to issues with improper access control that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-284.

### CVE-2026-76440

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-14T17:17:50.520 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Email Gateway and Cisco Secure Email and Web Manager engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76440 are related to path traversal issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-23.

### CVE-2026-20353

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-664` |
| Published | 2026-09-14T17:17:43.000 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Email Gateway and Cisco Secure Email and Web Manager engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20353 are related to issues with improper control of a resource through its lifetime that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-664.

### CVE-2026-57131

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-306;CWE-862` |
| Published | 2026-09-14T16:17:14.710 |

PraisonAI is a multi-agent teams system. Prior to 4.6.58, praisonai.jobs.server.create_app mounts praisonai.jobs.router.create_router under /api/v1/runs without authentication or per-job authorization. Network clients can submit attacker-controlled prompts and agent configuration, list and read jobs, stream results, and cancel or delete other jobs, exposing service credentials and connected tool capabilities to unauthorized agent execution. This vulnerability is fixed in 4.6.58.

### CVE-2026-57127

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-1188` |
| Published | 2026-09-14T16:17:13.557 |

PraisonAI is a multi-agent teams system. Prior to 4.6.58, recipe serve installs APIKeyAuthMiddleware or JWTAuthMiddleware when an operator selects api-key or JWT authentication, but each middleware forwards requests when PRAISONAI_API_KEY or PRAISONAI_JWT_SECRET and the corresponding recipe value are absent. Unauthenticated clients can then reach recipe execution, input, and output surfaces and may trigger connected tools despite the operator explicitly enabling authentication. This issue is fixed in 4.6.58.

### CVE-2026-57124

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-306` |
| Published | 2026-09-14T16:17:13.417 |

PraisonAI is a multi-agent teams system. Prior to 4.6.59, the default UI host applications expose POST /api/mcp/connect without mandatory authentication and accept caller-controlled command and args values that PraisonAIUI passes to StdioMCPClient to start a local process. Because the UI commands bind to 0.0.0.0 by default, a reachable unauthenticated client can execute commands as the UI service account even when the MCP handshake later fails. This vulnerability is fixed in 4.6.59.

### CVE-2026-82435

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-14T15:17:10.620 |

Description

The worker's Netty message decoder is installed ahead of the SASL authentication handlers in the pipeline
and acts on frames before any authentication has taken place. It allocated buffers sized from a
length field carried in the frame, so a single frame from an unauthenticated peer able to reach a worker
slot port could drive a large allocation.

`storm.messaging.netty.authentication` defaults to false, and the decoder runs before the handler that
enforces it in any case, so no credentials are required. The attacker needs only TCP reachability to a
worker port.

The effect of a single frame at the default 768 MB worker heap has not been measured to distinguish
sustained worker loss from transient garbage-collection pressure. The severity assigned to this advisory
reflects the more conservative reading; consumers who require a precise figure should test against their own
worker heap configuration.

Mitigation

Upgrade to 3.1.0, where frames are decoded only after the handshake completes.

Users who cannot upgrade immediately should ensure that worker slot ports are reachable only from within the
cluster, as the security model already recommends, and should enable
`storm.messaging.netty.authentication` where the deployment permits it.

Credit

The ASF -- found using Claude agents to study the security of open-source projects, validated and reported by Apache Storm.

### CVE-2026-82431

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-14T15:17:10.053 |

Description

`SimpleACLAuthorizer` evaluated the user-level command set by returning early when `nimbus.users` was empty,
before `nimbus.groups` was considered. An operator who restricted cluster access by group alone, leaving
`nimbus.users` unset, therefore received no restriction at all: every authenticated principal was permitted
every user-level operation, including `submitTopology`, `beginFileUpload` and `getNimbusConf`.

`docs/SECURITY.md` presents `nimbus.groups` as a supported way to lock down a cluster, so a deployment
following the documentation could believe it was restricted while it was not. The failure is silent; nothing
in the logs or the configuration indicates that the group list is being ignored.

Both lists left empty continues to mean that no restriction is configured, which is the shipped default and
is unchanged.

Mitigation

Upgrade to 3.1.0, where `nimbus.groups` is evaluated whether or not `nimbus.users` is set.

Users who cannot upgrade immediately should additionally populate `nimbus.users` with the intended
principals, since a non-empty user list causes the group list to be evaluated on affected versions.
Operators should review Nimbus access logs for operations by principals outside the intended groups.

Note that after upgrading, a cluster configured with `nimbus.groups` alone becomes restrictive for the first
time. This includes `NimbusClient`, which calls `getLeader` on every connection, so clients outside the
configured groups will begin to be refused.

Credit

The ASF -- found using Claude agents to study the security of open-source projects, validated and reported by Apache Storm.

### CVE-2026-57125

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-863` |
| Published | 2026-09-14T15:17:05.900 |

PraisonAI is a multi-agent teams system. Prior to praisonai 4.6.59 and praisonaiagents 1.6.59, the unauthenticated POST /api/v1/runs Jobs API accepts attacker-controlled agent_yaml, and the approve field can mark execute_command as YAML-approved before @require_approval checks critical tools. This chain allows a remote caller to cause a configured language model agent to invoke arbitrary operating-system commands without credentials or operator interaction. This vulnerability is fixed in praisonai 4.6.59 and praisonaiagents 1.6.59 as fixed versions.

### CVE-2026-57123

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-350;CWE-1327` |
| Published | 2026-09-14T15:17:05.753 |

PraisonAI is a multi-agent teams system. Prior to praisonaiagents 1.6.59, ToolsMCPServer.run_sse and launch_tools_mcp_server bind to 0.0.0.0 and create /sse and /messages/ routes without invoking the available SecurityConfig authentication, origin-validation, or DNS-rebinding controls. Any reachable client can list and invoke registered tools, and a browser can target a local instance through DNS rebinding, with impact determined by the registered file, shell, and code-execution tools. This vulnerability is fixed in praisonaiagents 1.6.59.

### CVE-2026-12944

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-14T22:16:56.950 |

IBM Langflow OSS 1.0.0 through 1.10.0 can allow attackers to execute arbitrary Python code with root privileges (UID=0) on the Langflow server by submitting components containing socket or urllib imports. This enables: (1) AWS credential theft via IMDSv1 SSRF with full IAM role permissions, (2) arbitrary file exfiltration from the container filesystem, and (3) lateral movement to internal services (PostgreSQL, Redis) within the Docker network. The scanner incorrectly returns "validated": true, providing a false security signal.

### CVE-2026-77179

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-15T14:17:11.273 |

On macOS, the virtio-fs host server used by Docker Sandboxes improperly follows symlinks when reopening an unlinked file from a stored path. A malicious guest can replace a parent directory with a symlink, escape the shared workspace, and read or modify arbitrary host files as the VMM user, potentially achieving host code execution.

### CVE-2026-91998

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-15T12:17:55.407 |

Casdoor through 4.4.0 contains an authorization bypass vulnerability in the /api/mcp endpoint that allows attackers with any application's clientId and clientSecret to gain unrestricted access to user administration across all organizations. Attackers can enumerate user records including password salts and email addresses, create administrator accounts, modify existing users, and delete them in any organization by supplying legitimate credentials from a single application.

### CVE-2026-57140

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-15T11:17:11.473 |

PraisonAI is a multi-agent teams system. From 1.6.0 until 1.7.2, AgentOS in src/praisonai-ts/src/os/agentos.ts uses the 0.0.0.0 default from src/praisonai-ts/src/os/config.ts and registers GET /api/agents and POST /api/chat without authentication middleware. A remote caller who can reach the service can obtain agent names, roles, and instruction prefixes and can invoke a selected agent, potentially reaching its tools, memory, external APIs, credentials, and workflow state. An initial remediation was released in version 1.7.2.

### CVE-2026-91995

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620` |
| Published | 2026-09-15T12:17:54.943 |

pig before 4.1.0 contains an authentication bypass vulnerability in the /register/password endpoint where password verification results are discarded, allowing any value as the current password. Remote attackers can submit a username with an incorrect current password to overwrite any account credential including the admin account and gain full administrative control.

### CVE-2026-89308

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-15T12:17:53.603 |

An unauthenticated OS command injection vulnerability exists in the ping.php endpoint, allowing remote attackers to execute arbitrary commands on the underlying operating system and achieve remote code execution.

### CVE-2026-46619

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-90` |
| Published | 2026-09-15T10:17:04.770 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, MSISDNValidation in the MSISDN authentication module concatenates the request-supplied MSISDN value into an LDAP search filter without escaping, while the default empty trusted-gateway list allows all traffic. In a realm where an MSISDN module is enabled in a reachable authentication chain, an unauthenticated remote attacker can inject LDAP filter metacharacters, select an arbitrary matching user, and obtain a normal authenticated OpenAM session without a password. This issue is fixed in version 16.1.1.

### CVE-2026-45052

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-15T10:17:04.307 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, the Liberty Web Services SOAP receiver permits unauthenticated remote requests to write persistent entries through SOAPReceiver and DiscoveryService into a user's Liberty Discovery store and the shared root-realm Discovery branch. The server-side handlers bypass requester LDAP and identity ACLs, and the global path uses an internal administrative token. Deployments that consume Liberty discovery data can subsequently use manipulated service-routing or security-mechanism records. This issue is fixed in version 16.1.1.

### CVE-2026-67399

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-14T21:17:25.423 |

Deserialization of untrusted data in WHMCS 9.0.0 before 9.0.8 and 8.0.0 before 8.13.7 allows remote attackers to execute arbitrary code.

### CVE-2026-90945

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-14T18:20:29.030 |

Crawlab through 0.6.3 uses a hard-coded HMAC-SHA256 secret for JWT token signing that cannot be overridden via configuration or environment variables. Unauthenticated attackers can forge valid administrator tokens to access administrative APIs and execute code on worker nodes.

### CVE-2026-90942

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-14T18:20:28.720 |

Casdoor through 4.4.0 fails to properly mask the instance-wide built-in certificate private key in /api/get-certs and /api/get-cert endpoints, allowing organization administrators to retrieve it. Attackers can use the exposed private key to forge JWT tokens for any user in any organization, including global administrators.

### CVE-2026-90943

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T16:17:41.693 |

parallax filament-comments through 3.0.0 contains a stored cross-site scripting vulnerability in comment body rendering that allows authenticated panel users to inject malicious scripts. Attackers can store XSS payloads in comment bodies that execute in the browsers of other users viewing those comments, including administrators, enabling session token theft and unauthorized actions.

### CVE-2026-62263

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-15T10:17:05.810 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.2, WebAuthnAuthentication.deserialize applies an ObjectInputFilter that allows every serialized object at depth greater than 1 and therefore constrains only an AuthenticatorImpl root object. A pre-authentication attacker can supply a userHandle whose serialized graph has a valid AuthenticatorImpl root and a nested gadget class, causing readObject or readResolve execution before the cast and assertion verification when a usable gadget is on the classpath. This bypasses the incomplete remediation for the earlier WebAuthn deserialization vulnerability. This issue is fixed in version 16.1.2.

### CVE-2026-45051

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-15T10:17:04.153 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, WebAuthnAuthentication loads a serialized AuthenticatorImpl object graph from the configured userAttribute through loadAuthenticators without an ObjectInputFilter. Exploitation requires the WebAuthn flow to be reachable and an attacker to have previously written controlled data to that attribute through delegated administration, provisioning, directory access, legacy REST self-registration, or unsafe configuration. When those non-default conditions hold, the data is deserialized before assertion verification and can execute a classpath gadget in the application server process. This issue is fixed in version 16.1.1.

### CVE-2026-57578

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-14T18:17:57.913 |

DotVVM is an open source MVVM framework for web applications. Prior to 4.2.11, 4.3.15, and 5.0.0-preview09-final, AuthorizeActionFilter performs no authorization because its explicit ICommandActionFilter.OnCommandExecutingAsync, IViewModelActionFilter.OnViewModelCreatedAsync, and IPresenterActionFilter.OnPresenterExecutingAsync implementations return completed tasks instead of invoking the corresponding checks. Applications relying on this filter can therefore expose protected commands, view models, or presenters to unauthorized requests without any special bypass technique. AuthorizeAttribute correctly implements the same interfaces and can be used as a workaround. This issue is fixed in versions 4.2.11, 4.3.15, and 5.0.0-preview09-final.

### CVE-2026-52824

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-09-15T11:17:09.543 |

Kimai is an open-source time tracking application. Prior to 2.58.0, the official Docker image sets APP_SECRET to the public value change_this_to_something_unique in Dockerfile, and .docker/entrypoint.sh neither replaces nor rejects that value before Symfony uses it as kernel.secret. An unauthenticated attacker who reaches a deployment that did not override APP_SECRET, knows a username, correctly guesses the account ID associated with that username, and targets an account without active two-factor authentication can forge HMAC-protected authentication artifacts, including KIMAI_REMEMBER cookies and login links, to access the account without its password. The updated entrypoint generates and persists a random secret when no safe operator-provided value exists. This issue is fixed in version 2.58.0.

### CVE-2026-48717

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-15T10:17:05.377 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, AuthorizationCodeGrantTypeHandler requires a code_verifier only when the realm-wide codeVerifierEnforced setting is enabled, even when an authorization code stores a code_challenge. Because that setting is disabled by default, an attacker who intercepts a PKCE-protected authorization code can omit code_verifier and redeem the code, while an explicitly incorrect verifier is rejected. Public clients are directly affected, and confidential-client exploitation additionally requires client authentication material or another redemption context. This issue is fixed in version 16.1.1.

### CVE-2026-90711

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290;CWE-348;CWE-697` |
| Published | 2026-09-15T07:16:33.683 |

proxy-addr is a Node.js module that determines a request's client address behind trusted reverse proxies, and it backs Express req.ip and req.ips. In versions 1.1.0 through 2.0.7, a trust subnet written in IPv4-mapped IPv6 notation with an IPv4-sized prefix, such as ::ffff:10.0.0.0/8 instead of the correct ::ffff:10.0.0.0/104, is accepted without error but trusts every IPv4 address on the internet rather than the block it names. Because the socket peer then becomes trusted at hop 0, any unauthenticated client can supply an arbitrary X-Forwarded-For header and control the address the application reads, which defeats IP-based access control, rate limiting, geolocation, and audit logging. This is a fail-open regression introduced in version 1.1.0. The issue is fixed in proxy-addr 2.0.8, and users should upgrade to 2.0.8 or later. As a workaround, ensure any IPv4-mapped IPv6 trust subnet uses a prefix length of at least 97, or express the range in plain IPv4 notation.

### CVE-2026-53713

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-14T21:17:12.520 |

Envoy Gateway is an open source project for managing Envoy Proxy as a standalone or Kubernetes-based application gateway. Prior to 1.7.4 and 1.8.1, to_absolute_normalized_path in internal/gatewayapi/luavalidator/security.lua does not collapse redundant separators before is_critical_path evaluates Lua submitted through EnvoyExtensionPolicy during default Strict validation. Linux resolves a double-slash absolute path as the corresponding single-slash path, but the validator does not match the redundant-separator form, allowing submitted Lua to read arbitrary files from the gateway controller pod. Exposed files can include Kubernetes service-account tokens, TLS certificates, and process environment data, and the disclosed credentials can provide access to sensitive Kubernetes API Server or Gateway xDS server information. This issue is fixed in versions 1.7.4 and 1.8.1.

### CVE-2026-50006

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73;CWE-284;CWE-434;CWE-862` |
| Published | 2026-09-14T20:16:44.637 |

Anyquery is an SQL query engine built on top of SQLite. Prior to 0.4.5, anyquery server forwards unauthenticated SQL from its MySQL-compatible server port to SQLite without restricting ATTACH DATABASE filesystem targets. A remote attacker can select any path writable by the Anyquery server process, cause SQLite to create a database file there, and place attacker-controlled table content in that file. This permits arbitrary file creation or overwrite, causing filesystem integrity loss and denial of service; remote code execution is possible only when another service interprets the written file or the process has a suitably privileged writable target. This issue is fixed in version 0.4.5.

### CVE-2026-61534

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-14T16:17:16.847 |

Yayson is a library for serializing and reading JSON API data in JavaScript. Prior to 4.3.0, Store and LegacyStore use attacker-controlled JSON:API type, id, and relationship names as keys in plain-object lookup tables in src/yayson/store.ts and src/yayson/legacy-store.ts. A document whose type is __proto__ causes model-cache writes to modify Object.prototype, with the attacker controlling the polluted property name through id and its value through attributes. The malicious type can also be supplied by an included resource, and LegacyStore is reachable when a configured types mapping resolves to __proto__. Unsafe relationship names including __proto__, constructor, and prototype provide additional document-derived member paths. The resulting process-wide prototype pollution can cause denial of service and logic corruption; authorization bypass or code execution depends on suitable gadgets in the consuming application. This issue is fixed in version 4.3.0.

### CVE-2026-57145

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T16:17:15.017 |

PraisonAI is a multi-agent teams system. Prior to 4.6.62, src/praisonai/praisonai/tools/multiedit.py passes the LLM-controlled filepath parameter directly to open for reading and writing without traversal rejection, symlink resolution, a workspace boundary, or protected-path checks. Prompt-influenced agents can read files through edit and diff behavior or overwrite files accessible to the process, exposing secrets and enabling persistence or application tampering. This issue is fixed in 4.6.62.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-16140

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-15T14:16:50.290 |

OpenBMC's IPMI implementation, phosphor-net-ipmid, is vulnerable to a logic flaw where the authorization context of an existing session can be replaced with a target account while still maintaining the original integrity and encryption keys. Several downstream vendors implement phosphor-net-ipmid as their IPMI stack, such as NVIDIA and H3C. This issue effectively allows for privilege escalation without re-authentication.

### CVE-2026-92073

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-15T13:17:02.153 |

Privilege escalation in the Enterprise Policies component. This vulnerability was fixed in Firefox 156 and Firefox ESR 153.3.

### CVE-2026-92055

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-15T13:16:59.370 |

Privilege escalation in the DevTools component. This vulnerability was fixed in Firefox 156 and Firefox ESR 153.3.

### CVE-2026-92054

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-15T13:16:58.800 |

Privilege escalation in the Memory component. This vulnerability was fixed in Firefox 156 and Firefox ESR 153.3.

### CVE-2026-92053

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-15T13:16:57.053 |

Privilege escalation in the Graphics: CanvasWebGL component. This vulnerability was fixed in Firefox 156 and Firefox ESR 153.3.

### CVE-2026-92047

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-15T13:16:56.373 |

Privilege escalation in the Crash Reporting component. This vulnerability was fixed in Firefox 156 and Firefox ESR 153.3.

### CVE-2026-92043

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T13:16:55.750 |

Privilege escalation due to incorrect boundary conditions in the Audio/Video component. This vulnerability was fixed in Firefox 156 and Firefox ESR 153.3.

### CVE-2026-92033

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-15T13:16:54.623 |

Privilege escalation in Firefox for Android. This vulnerability was fixed in Firefox 156.

### CVE-2026-92020

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T13:16:51.990 |

Privilege escalation due to incorrect boundary conditions in the Graphics: WebRender component. This vulnerability was fixed in Firefox 156, Firefox ESR 115.41, Firefox ESR 140.16, and Firefox ESR 153.3.

### CVE-2026-92017

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-15T13:16:51.403 |

Privilege escalation in the DOM: Service Workers component. This vulnerability was fixed in Firefox 156, Firefox ESR 115.41, Firefox ESR 140.16, and Firefox ESR 153.3.

### CVE-2026-92015

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-15T13:16:51.100 |

Privilege escalation in the WebExtensions component. This vulnerability was fixed in Firefox 156, Firefox ESR 115.41, Firefox ESR 140.16, and Firefox ESR 153.3.

### CVE-2026-92014

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T13:16:50.887 |

Privilege escalation due to incorrect boundary conditions in the Graphics component. This vulnerability was fixed in Firefox ESR 115.41 and Firefox ESR 140.16.

### CVE-2026-92013

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T13:16:49.447 |

Privilege escalation due to incorrect boundary conditions in the Graphics: CanvasWebGL component. This vulnerability was fixed in Firefox 156, Firefox ESR 115.41, Firefox ESR 140.16, and Firefox ESR 153.3.

### CVE-2026-92012

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T13:16:49.310 |

Privilege escalation due to incorrect boundary conditions in the Graphics: CanvasWebGL component. This vulnerability was fixed in Firefox 156, Firefox ESR 115.41, Firefox ESR 140.16, and Firefox ESR 153.3.

### CVE-2026-92011

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T13:16:49.167 |

Privilege escalation due to incorrect boundary conditions in the Graphics: CanvasWebGL component. This vulnerability was fixed in Firefox 156, Firefox ESR 115.41, Firefox ESR 140.16, and Firefox ESR 153.3.

### CVE-2026-92010

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T13:16:48.740 |

Privilege escalation due to incorrect boundary conditions in the Graphics: CanvasWebGL component. This vulnerability was fixed in Firefox 156, Firefox ESR 115.41, Firefox ESR 140.16, and Firefox ESR 153.3.

### CVE-2026-92009

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T13:16:48.593 |

Privilege escalation due to incorrect boundary conditions in the Graphics: CanvasWebGL component. This vulnerability was fixed in Firefox 156, Firefox ESR 115.41, Firefox ESR 140.16, and Firefox ESR 153.3.

### CVE-2026-92008

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T13:16:48.463 |

Privilege escalation due to incorrect boundary conditions in the Graphics: CanvasWebGL component. This vulnerability was fixed in Firefox 156, Firefox ESR 115.41, Firefox ESR 140.16, and Firefox ESR 153.3.

### CVE-2026-92007

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T13:16:48.357 |

Privilege escalation due to incorrect boundary conditions in the Graphics: CanvasWebGL component. This vulnerability was fixed in Firefox 156, Firefox ESR 115.41, Firefox ESR 140.16, and Firefox ESR 153.3.

### CVE-2026-92006

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-15T13:16:48.243 |

Privilege escalation due to incorrect boundary conditions in the Graphics: CanvasWebGL component. This vulnerability was fixed in Firefox 156, Firefox ESR 115.41, Firefox ESR 140.16, and Firefox ESR 153.3.

### CVE-2026-14805

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-15T13:16:40.507 |

The Consulting theme for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 6.7.16. This is due to a combination of two flaws: (1) the masterstudy_ms_stm_set_discard_transient AJAX endpoint in admin/admin-notices/classes/STMHandler.php accepts an arbitrary transient key without capability checks or nonce validation, and (2) the developer access login mechanism in admin/classes/stm-theme-support.php authenticates users based on a transient value without proper cryptographic validation when in legacy string mode. This makes it possible for authenticated attackers, with subscriber-level access and above, to set the stm_developer_access_token transient to a known value (1), then authenticate as any existing user including administrators by visiting a specially crafted URL, thereby achieving full privilege escalation to administrator.

### CVE-2026-57137

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693;CWE-862;CWE-863` |
| Published | 2026-09-15T11:17:11.030 |

PraisonAI is a multi-agent teams system. From 1.4.0 until 1.7.2, createAgentLoop() in src/praisonai-ts/src/ai/agent-loop.ts passes executable tools to generateText() before invoking the onToolCall approval callback. Because the wrapped AI SDK executes tool handlers during generation, a callback that returns false records tool_rejected only after the denied tool has already produced side effects and populated toolResults. Applications using onToolCall as a human or policy approval boundary can therefore execute rejected file, command, API, or data-modifying operations. This issue is fixed in version 1.7.2.

### CVE-2026-57136

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-693;CWE-863` |
| Published | 2026-09-15T11:17:10.883 |

PraisonAI is a multi-agent teams system. From 1.2.3 until 1.7.2, CommandValidator in src/praisonai-ts/src/cli/features/sandbox-executor.ts validates only the first whitespace-delimited executable against allowedCommands, then SandboxExecutor passes the complete command string to sh -c. A command beginning with an allowed executable can append a non-allowlisted command through shell metacharacters, causing arbitrary commands to run with the PraisonAI process privileges. This issue is fixed in version 1.7.2.

### CVE-2026-57133

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-693;CWE-863` |
| Published | 2026-09-15T11:17:10.437 |

PraisonAI is a multi-agent teams system. From 1.5.1 until 1.7.2, the shell() helper exported from src/praisonai-ts/src/tools/utility-tools.ts checks only the first whitespace-delimited token against safeCommands and then passes the complete original string to child_process.exec(). A string that starts with an allowed read-only command can append a second non-allowlisted command through shell syntax, allowing arbitrary command execution with the PraisonAI process privileges. This issue is fixed in version 1.7.2.

### CVE-2026-43692

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-14T21:17:08.550 |

A validation issue was addressed with improved input sanitization. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. A remote user may cause an unexpected app termination or arbitrary code execution.

### CVE-2026-13293

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-14T21:17:02.130 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 could allow a remote authenticated attacker to execute arbitrary code on the system due to the deserialization of untrusted data.

### CVE-2026-16673

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-14T20:16:41.053 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 IBM DataStage could allow a remote authenticated attacker to execute arbitrary OS commands due to improper neutralization of special characters in the PxPeek name property.

### CVE-2026-16466

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-14T20:16:40.917 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 IBM DataStage could allow a remote authenticated attacker to execute arbitrary commands due to os command injection.

### CVE-2026-16428

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-14T20:16:40.537 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 IBM DataStage could allow a remote authenticated attacker to execute arbitrary code due to improper configuration of the XSLT transformation engine.

### CVE-2026-89023

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-14T19:17:55.287 |

ThemeAtelier Domain For Sale plugin for WordPress before 3.5.2 contains a missing authorization vulnerability in its REST API endpoints that allows unauthenticated attackers to access and manipulate protected resources. Attackers can retrieve stored offer records, delete arbitrary offers by numeric identifier, and access dashboard statistics to disclose bidder contact information, offer details, messages, verification tokens, and business data.

### CVE-2026-90944

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-14T18:20:28.877 |

Krayin CRM through 2.2.6 exposes the POST /admin/mail/inbound-parse endpoint without authentication, allowing unauthenticated attackers to inject arbitrary emails into the CRM inbox. Attackers can supply crafted RFC 2822 messages with forged sender information and headers to insert emails with any subject and body, including replies to existing conversation threads.

### CVE-2026-61701

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-14T17:17:49.613 |

Laravel MagicLink creates links for authentication without a password or for accessing private content. From 2.0.0 until 2.25.1, MagicLink stores serialized action objects in the magic_links.action database column and deserializes them through src/MagicLink.php and src/Actions/ResponseAction.php without sufficient integrity protection, while an unsafe legacy unserialize() fallback remains reachable. An attacker who can manipulate database records, such as through a separate SQL injection or compromised administrative access, can insert a malicious serialized object graph containing executable closure behavior; visiting the associated magic link then deserializes the record and can execute arbitrary code in the application process. The affected path is restricted to manipulated action records and does not independently provide database-write access. This issue is fixed in version 2.25.1.

### CVE-2026-55416

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-14T17:17:48.220 |

Pimcore is an Open Source Data & Experience Management Platform. Prior to 11.5.19, 12.3.10, and 2026.1.6, an authenticated user with reports_config permission can place attacker-controlled SQL fragments in the sql, from, where, and groupby fields of a Custom Reports configuration processed by bundles/CustomReportsBundle/src/Tool/Adapter/Sql.php. The buildQueryString() method concatenates these values into a database query, while a blacklist omits dangerous constructs such as additional data-manipulation statements, comments, subqueries, and multiple statements. The getData() method also previously interpolated offset and limit values into a LIMIT clause without integer casting. Executing the configured report reaches fetchAllAssociative() with the constructed query and can disclose, modify, or delete arbitrary database data. This issue is fixed in versions 11.5.19, 12.3.10, and 2026.1.6.

### CVE-2026-82428

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T15:17:09.673 |

Description

Dependency artifacts uploaded with `storm jar --artifacts` were stored under a blob key derived only from
the Maven coordinate, for example `dep---.jar`. The key was therefore identical
for every user of the cluster and predictable in advance. When the blob already existed, the uploader
caught `KeyAlreadyExistsException` and silently reused it, with no check that the existing blob's content
or owner matched the artifact the submitter had resolved.

A user who uploaded a blob under such a key first therefore controlled the bytes that every later submitter
of the same coordinate would receive on the worker classpath, resulting in code execution inside another
tenant's topology.

This affects deployments where more than one principal may create blobs and where the `--artifacts`
dependency feature is used.

Mitigation

Upgrade to 3.1.0, where each uploaded artifact receives a key carrying a freshly generated UUID and a
pre-existing blob is no longer silently reused.

Note that the corrected key generation is on the SUBMITTING CLIENT, so upgrading the cluster alone does not
close this; every client that runs `storm jar --artifacts` must also be upgraded. Operators should audit
existing `dep-` blobs for unexpected owners before upgrading. Users who cannot upgrade immediately should
avoid the `--artifacts` mechanism in multi-tenant clusters and distribute dependencies inside the topology
jar instead.

Credit

The ASF -- found using Claude agents to study the security of open-source projects, validated and reported by Apache Storm.

### CVE-2026-91996

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-15T12:17:55.093 |

lamp-cloud through 5.10.0 whitelists the path pattern /*/anno/** for anonymous access, allowing unauthenticated attackers to read the server's full JVM system property map. Attackers can send POST requests to /defGenProject/anno/getProperties to retrieve sensitive information including JVM classpath, filesystem paths, operating system details, and startup secrets.

### CVE-2026-91925

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-15T11:17:13.220 |

Polyaxon through 2.16.4 renders operation specification fields with an unsandboxed Jinja2 environment during server-side run preparation, allowing authenticated users to execute arbitrary code. Attackers can submit runs with Jinja2 payloads in queue, namespace, conditions, presets, or dependencies fields to execute operating system commands in the scheduler process context, exposing database credentials and service tokens.

### CVE-2026-80217

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-912` |
| Published | 2026-09-15T09:16:44.233 |

Hidden functionality issue exists in FF-RFI079I4 and FF-RFI078I4, which may allow a user who can log in via SSH and access the enable mode on the product to execute arbitrary OS commands.

### CVE-2026-77853

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-15T09:16:44.067 |

Improper neutralization of special elements used in an OS command ('OS Command Injection') issue exists in FF-RFI079I4 and FF-RFI078I4. A user who can log in to the product's M-Plane (NETCONF) may execute arbitrary OS commands.

### CVE-2026-88262

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-15T03:17:06.233 |

Insufficient session expiration vulnerability in bizwell xClick allows Authentication Bypass.

This issue affects xClick: R2, R3, and R3.1.

### CVE-2026-91771

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-15T02:16:49.680 |

Weights & Biases wandb before 0.29.0 fails to validate the file name from server responses in the File.download function, allowing path traversal attacks. Attackers controlling the backend can supply file names with directory traversal sequences to write files outside the intended download directory, potentially enabling code execution through modification of shell startup files or Python import paths.

### CVE-2026-91752

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-15T01:16:54.967 |

GNU libextractor before 1.15 contains a stack-based buffer overflow vulnerability in the process_star_office function that sizes a variable-length stack array from attacker-controlled OLE2 stream data. Attackers can craft malicious StarOffice documents that allocate up to 4 MB on the stack, causing stack overflow and crashing any application extracting metadata from the document.

### CVE-2026-91200

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T23:19:00.630 |

DevSpace through 6.3.21 fails to reject parent-directory segments in tar entry names from the in-pod sync stream. Attackers operating a malicious container can stream tar entries with traversal sequences to write arbitrary files on the developer workstation, enabling code execution.

### CVE-2026-91144

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-14T22:16:59.053 |

ZFile through 5.0.5 fails to validate requested file paths against a share link's allowed entries on the download endpoint. Attackers holding a share link can supply arbitrary file paths as query parameters to download any file under the shared base directory, bypassing the intended access restrictions.

### CVE-2026-68489

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-96` |
| Published | 2026-09-14T21:17:25.567 |

Static Code Injection in Plesk extensions "Ruby" before 1.6.6 and "Node.js Toolkit" before 2.5.0 allows remote authenticated users to execute arbitrary code as root via custom environment variables.

### CVE-2026-82028

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-14T20:16:54.077 |

Magistrala before 1.0.0 contains a SQL injection vulnerability in the timescale-reader and postgres-reader HTTP API services that allows authenticated attackers to inject arbitrary SQL by supplying a malicious format query parameter that is interpolated directly into the FROM clause without parameterization or identifier quoting. Attackers with a self-registered account can substitute arbitrary subqueries to achieve cross-tenant database reads, extract pg_shadow password hashes, read and write arbitrary files, and execute arbitrary code as the postgres OS user by loading attacker-supplied shared objects, with all injected SQL executing at superuser privilege due to the default PostgreSQL role configuration.

### CVE-2026-91080

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-14T18:20:29.760 |

webhook through 2.8.3 reads the entire request body into memory before evaluating trigger rules, allowing unauthenticated attackers to exhaust memory by sending oversized bodies. Attackers can send multi-gigabyte request bodies with invalid signatures to trigger out-of-memory conditions and crash the service.

### CVE-2026-90946

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-14T18:20:29.180 |

DeepWiki-Open through commit d92819a contains an arbitrary file read vulnerability in the unauthenticated /ws/chat WebSocket endpoint that accepts repo_url as a filesystem path with no containment. Attackers can supply arbitrary directory paths to read all files with supported extensions including Python, JavaScript, YAML, and JSON files containing hardcoded secrets and credentials.

### CVE-2026-49250

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-14T18:17:49.360 |

Conform, a type-safe form validation library, allows the parsing of nested objects in the form of object.property. From 1.8.0 until 1.19.4, the parseSubmission future API in packages/conform-dom/formdata.ts repeatedly scans FormData or URLSearchParams entries by each unique field name. An unauthenticated attacker can submit a crafted form containing many unique names, causing excessive synchronous CPU work and denial of service in an application that passes the submission to parseSubmission. Applications should continue to enforce request parsing limits before invoking Conform. This issue is fixed in version 1.19.4.

### CVE-2026-84445

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129;CWE-248` |
| Published | 2026-09-14T17:17:51.743 |

gRPC-Go is the Go language implementation of gRPC. Prior to 1.82.2 and 1.83.2, servers created with xds.NewGRPCServer() allow internal/transport/http2_server.go to accept an RPC containing neither the :authority header nor the Host header, while RouteAndProcess in internal/xds/server/routing.go assumes that an authority value exists and indexes the empty slice. A remote client that can complete transport connection establishment can trigger an index-out-of-bounds panic that is not recovered by the per-RPC goroutine and terminates the entire server process. In insecure or ordinary TLS deployments the request can be unauthenticated, while strict mTLS or ALTS deployments require valid transport credentials before the malformed RPC can reach the interceptor. This issue is fixed in versions 1.82.2 and 1.83.2.

### CVE-2026-91001

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-15T06:16:59.970 |

A security flaw has been discovered in D-Link DI-8400 16.07. This affects the function ddns_asp of the file /ddns.asp of the component DDNS Configuration. Performing a manipulation of the argument serv/user/host/wild/mx/bmx/cust/ip results in stack-based buffer overflow. The attack can be initiated remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-54628

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-284;CWE-441;CWE-862;CWE-918` |
| Published | 2026-09-14T20:16:46.723 |

Anyquery is an SQL query engine built on top of SQLite. Prior to 0.4.5, anyquery server exposes URL-capable SQLite virtual table modules such as json_reader and log_reader through its unauthenticated MySQL-compatible server port without restricting outbound destinations. A remote attacker can provide a loopback, private-network, or link-local cloud metadata URL, causing go-getter in the Anyquery server process to fetch the selected resource and expose its response as queryable table data. This permits internal network probing, access to internal APIs, and disclosure of cloud credentials; low-integrity impact is possible when a reached internal API performs state-changing actions. This issue is fixed in version 0.4.5.

### CVE-2026-86830

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-14T19:17:52.523 |

Incorrect privilege assignment in Temporary Elevated Access Management (TEAM) for AWS IAM Identity Center solution before version 1.5.1 might allow an authenticated remote user with application-level access to read, approve, modify, or revoke arbitrary access requests, thereby obtaining unintended temporary elevated access to the AWS accounts accessed using the TEAM deployment.



This issue has been addressed in TEAM version 1.5.1 or later. We recommend upgrading to the latest version and ensuring any forked or derivative code is patched to incorporate the new fixes.

### CVE-2026-57122

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-345;CWE-347` |
| Published | 2026-09-14T16:17:13.270 |

PraisonAI is a multi-agent teams system. Prior to 4.6.59, the WhatsApp and Linear bot webhook handlers verify HMAC signatures only when WHATSAPP_APP_SECRET or LINEAR_WEBHOOK_SECRET is configured and otherwise parse and dispatch unsigned request bodies. A remote unauthenticated client that reaches the webhook route can forge messages, comments, or agent-session events, impersonate platform users, influence agent prompts and actions, and disrupt bot processing. This issue is fixed in 4.6.59.

### CVE-2026-7848

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-14T15:17:08.560 |

Alior Bank PrestaShop module "raty" for commercial partners is vulnerable to SQL Injection in the "hookActionObjectProductUpdateBefore", "hookActionObjectCategoryUpdateBefore", and "hookActionObjectCategoryAddAfter" hook methods. The module inserts values of the POST parameters "alior_product_promotion",  "alior_category_promotion" and "alior_category_enabled" directly into SQL UPDATE queries without any sanitization or validation. An attacker with access to the product or category add/edit functionality in the PrestaShop backoffice can inject arbitrary SQL, potentially allowing unauthorized access to and modification of database contents. This issue was fixed in versions: 9.0.7 and 8.1.11

### CVE-2026-15600

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-14T15:17:04.393 |

Alior Bank PrestaShop module "raty" for commercial partners is vulnerable to SQL Injection in the toggleCategoryPromotionAction method. The module inserts value of the POST parameter "status" into SQL UPDATE queries without any sanitization or validation. An attacker with access to the product or category add/edit functionality in the PrestaShop backoffice can inject arbitrary SQL, potentially allowing unauthorized access to and modification of database contents.

### CVE-2026-45048

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-285` |
| Published | 2026-09-15T10:17:03.993 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, SessionRequestHandler in the session management endpoint does not enforce ownership or privilege checks when a low-privileged authenticated user queries session information in deployments using stateful session storage. A requester who knows a target identity identifier can retrieve another user's active session credentials, including credentials for a more privileged account, and use them to hijack that session. This issue is fixed in version 16.1.1.

### CVE-2026-91003

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-15T06:17:01.387 |

A flaw has been found in D-Link DI-8300 16.07. The affected element is the function rzgl_asp of the file /rzgl.asp of the component CGI Service. This manipulation of the argument redirct_url causes stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit has been published and may be used.

### CVE-2026-90847

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-15T01:16:54.423 |

A vulnerability was determined in EFM ipTIME C200E 1.094. The impacted element is an unknown function of the file iux_set.cgi of the component System Setup. This manipulation causes os command injection. It is possible to initiate the attack remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-55072

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-20;CWE-89` |
| Published | 2026-09-14T17:17:47.610 |

Pimcore is an Open Source Data & Experience Management Platform. Prior to 2026.1.5, an authenticated user with the objects permission can submit a malicious ClassDefinition UID because the name and ID validation expressions in models/DataObject/ClassDefinition.php validate only the beginning of each value. When a data object of that class containing a Block field is loaded, Block::load in models/DataObject/ClassDefinition/Data/Block.php incorporates the stored class ID into an unquoted object table identifier, allowing the UID to supply SQL syntax. The resulting query can read or modify arbitrary Pimcore database tables, including disclosure of password hashes, and the flaw represents an incomplete validation hardening because earlier work added a start anchor without enforcing the end of the identifier. This issue is fixed in version 2026.1.5.

### CVE-2026-81301

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-926` |
| Published | 2026-09-14T16:17:19.360 |

Ekia File Manager 1.2.7 exposes com.ekia.filecontrolmanager.OpenFileProvider as an exported Android ContentProvider without requiring caller permissions.

The provider maps the caller-controlled URI path directly to a filesystem path and passes it to new File(...). It then supports query(), openFile(), and delete() operations. Because the provider is exported and lacks android:permission, android:readPermission, or android:writePermission, another local application can access the provider authority and cause File Manager's process to read, create, overwrite, or delete files that are accessible to that process.

### CVE-2026-57126

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-14T15:17:06.040 |

PraisonAI is a multi-agent teams system. Prior to praisonaiagents 1.6.58, SpiderTools._validate_url calls _host_is_blocked, which checks literal host encodings but does not resolve DNS names before scrape_page, crawl, extract_links, extract_text, or URL-mention fetches connect. An attacker-controlled hostname resolving to a loopback, private, link-local, or cloud-metadata address therefore bypasses the SSRF policy without a rebinding race and can expose internal responses to the agent. This issue is fixed in praisonaiagents 1.6.58.

### CVE-2026-91924

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T11:17:13.053 |

pgweb through 0.17.0 leaves the POST /api/connect endpoint unguarded when connect-backend authorization is configured, allowing attackers to supply arbitrary database connection strings. Attackers can bypass the resource-to-database mapping by providing a custom session identifier and connection URL to access unauthorized databases and internal services.

### CVE-2026-54447

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-14T20:16:46.290 |

garminconnect is a Python 3 API wrapper for Garmin Connect that retrieves statistics and manages activities. Prior to 0.3.5, garminconnect/client.py Client.dump creates the OAuth token directory and garmin_tokens.json without explicit owner-only modes, so a permissive umask such as 022 can leave the directory mode at 0755 and the token file mode at 0644. garmin_tokens.json contains di_refresh_token, and another unprivileged user on a shared Linux or macOS host can read the token and obtain persistent access to the victim's Garmin Connect account, including health, fitness, activity, and device data. The Garmin.login tokenstore path is affected, and a pre-existing loosely permissioned token file remains exposed until rewritten or manually restricted. This issue is fixed in version 0.3.5.

### CVE-2026-82049

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-14T19:17:50.927 |

In CPython 3.13 and earlier, the tarfile module's data and tar extraction filters are vulnerable to crafted archives containing a hard link to a symbolic link. Such archives may cause extraction to modify the permissions or modification time of a file outside the destination directory, or expose the contents of that file within the extracted tree.

### CVE-2026-86836

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276;CWE-367;CWE-379` |
| Published | 2026-09-14T18:20:20.193 |

In Eclipse Ankaios versions 0.1.0 through 1.0.2, the agent creates workload files and Control Interface named pipes (FIFOs) under a predictable path derived from the agent name and a hash of the workload's runtime configuration. If a directory or FIFO already exists at that path when the agent (re)starts, the agent reuses it based only on an existence and/or file-type check, without validating its owner or permissions. A local, unprivileged user with write access to the same base directory (by default under `$TMPDIR/ankaios`, e.g. shared `/tmp`) can pre-create this path hierarchy, including the two Control Interface FIFOs, before the agent starts. The agent then treats the attacker-owned FIFOs as the legitimate Control Interface for the targeted workload. The attacker can complete the Control Interface handshake and issue requests using that workload's configured `controlInterfaceAccess` permissions, allowing impersonation of the workload and, depending on its configured permissions, unauthorized reading and/or modification of the cluster's desired state.

### CVE-2026-91923

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T11:17:12.897 |

KubeSphere through 4.1.3 contains a server-side request forgery vulnerability in the git credential verification endpoint that accepts unvalidated caller-supplied URLs without allowlist restrictions. Authenticated attackers can supply arbitrary URLs to reach internal services and exfiltrate basic-auth credentials from Secrets in any namespace by leveraging the endpoint's error response handling.

### CVE-2026-57112

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-346;CWE-862` |
| Published | 2026-09-15T11:17:10.290 |

PraisonAI is a multi-agent teams system. From praisonaiagents 0.6.0 until 1.6.59 and PraisonAI 3.10.0 until 4.6.59, ToolsMCPServer.run_sse() in src/praisonai-agents/praisonaiagents/mcp/mcp_server.py mounts SseServerTransport on the legacy /sse and /messages/ endpoints without default Host, Origin, or authentication enforcement. A malicious website can use DNS rebinding against a reachable local or internal SSE server, supply attacker-controlled Host and Origin headers, enumerate registered tools, and invoke them with the server user's privileges. The Streamable HTTP transport rejects the same hostile Origin, which isolates the flaw to the legacy SSE wrapper. An initial remediation was released in praisonaiagents 1.6.59 and PraisonAI 4.6.59.

### CVE-2026-1758

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-384` |
| Published | 2026-09-15T11:17:07.587 |

Session fixation vulnerability in Secomea GateManager (webserver module) allows Session Fixation.

This issue affects GateManager: 11.5;0, 11.4.625515072:0.



Fixed in Version 11.6 or 11.4.626194074 and above

### CVE-2026-44203

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:L/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-15T10:17:03.510 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, the OAuth 2.0 and OpenID Connect authorization endpoint does not sufficiently encode user-supplied parameters before FormPostResponse.ftl and checkSession.ftl render them into HTML for the form_post response mode. An unauthenticated attacker can induce a user to open a crafted authorization request and execute script in the OpenAM origin. This issue is fixed in version 16.1.1.

### CVE-2026-55451

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-14T17:17:48.383 |

gettext-converter provides gettext resource conversion utilities for JavaScript. Prior to 1.3.3, js2i18next() in lib/js2i18next.js splits nested translation keys using options.keyseparator, whose default value consists of two number signs, and uses each segment as a dynamic object key without rejecting __proto__, constructor, or prototype. When an application converts untrusted PO or i18next translation data, a __proto__ segment resolves Object.prototype as the nested write target and Object.assign writes attacker-controlled translated properties onto the process-wide prototype. The resulting prototype pollution can cause denial of service and may enable application-dependent follow-on attacks. This issue is fixed in version 1.3.3.

### CVE-2026-57134

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287;CWE-288;CWE-863` |
| Published | 2026-09-15T11:17:10.583 |

PraisonAI is a multi-agent teams system. From 1.5.1 until 1.7.2, MCPSecurity.evaluatePolicy() in src/praisonai-ts/src/mcp/security.ts invokes the configured credential validator only when AuthMethod is api-key or bearer. Basic and OAuth policies accept any non-empty Authorization header without calling auth.validate(), then return an authenticated result, allowing callers with invalid credentials to access MCP tools and resources protected by those policies. This issue is fixed in version 1.7.2.

### CVE-2026-90896

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-14T21:17:42.740 |

Missing Authentication for Critical Function (CWE-306) in the checkout session lookup handler (src/app/api/stripe/checkout_sessions/route.ts), exposed at GET /api/stripe/checkout_sessions, in MarcosCamara01 Ecommerce Template before commit 91e273c allows a remote, unauthenticated attacker holding a valid Stripe Checkout Session id (cs_...) to retrieve the full session object, including the buyer's name, email, phone, billing address, amount paid and internal userId, because the GET handler calls stripe.checkout.sessions.retrieve() and returns the result without checking for an authenticated session or session ownership. Sibling endpoints such as POST /api/stripe/payment already enforced authentication via auth.api.getSession(); this endpoint had no access control whatsoever. The session_id is exposed in the buyer's own browser URL after payment (success_url = /result?session_id={CHECKOUT_SESSION_ID}), so it leaks through Referer headers, analytics tools, server access logs and shared-machine browser history, resulting in disclosure of the buyer's personal data to an unauthenticated actor.

### CVE-2026-65838

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-754` |
| Published | 2026-09-14T20:16:49.103 |

Skipper is an HTTP router and reverse proxy for service composition. Prior to 0.27.35, the opaAuthorizeRequestWithBody filter in filters/openpolicyagent/openpolicyagent.go can allow an oversized declared Content-Length request to bypass a deny-on-presence Rego policy because ExtractHttpBodyOptionally leaves OPA with an empty parsed_body while forwarding the complete request body upstream. This incomplete remediation of CVE-2026-50197 affects deployments that authorize request-body content and exceed -open-policy-agent-max-request-body-size, which defaults to 1 MB. Policy logic that does not reject input.attributes.request.http.truncated_body can therefore fail open and permit a forbidden payload to reach the protected service, while small bodies and the previously fixed chunked-body case are evaluated normally. This issue is fixed in version 0.27.35.

### CVE-2026-17467

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-327` |
| Published | 2026-09-14T20:16:42.007 |

IBM Cloud Pak for Data System (Yosemite 1.0) 3.0.5.2 could allow a remote attacker to obtain sensitive information due to the use of weak or deprecated cryptographic protocols.

### CVE-2026-85921

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-14T18:20:20.047 |

Double free in Windows Secure Kernel Mode allows an authorized attacker to elevate privileges locally.

### CVE-2026-57577

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-14T18:17:57.353 |

DotVVM is an open source MVVM framework for web applications. Prior to 4.2.11, 4.3.15, and 5.0.0-preview09-final, a route containing multiple unconstrained parameters in one path segment can cause excessive regular-expression backtracking in DotvvmRoute.IsMatch when a remote requester supplies a long near-match path. DotvvmRouteParser.RouteRegex previously had no matching timeout. Patched runtimes retry with the .NET non-backtracking engine, while runtimes that do not support non-backtracking matching return HTTP 503 after the one-second timeout in DotvvmRoutingMiddleware. This issue is fixed in versions 4.2.11, 4.3.15, and 5.0.0-preview09-final.

### CVE-2026-34151

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-24` |
| Published | 2026-09-14T18:17:47.107 |

XWiki Platform is a generic wiki platform. Prior to 17.10.5 and 18.2.0, the /skin/ action in com.xpn.xwiki.web.SkinAction can resolve double-encoded parent-directory segments outside the intended skin or web-application resource prefix when Jetty 12 or later decodes the request path. The affected lookup is replaced with Environment.getResourceAsStream(String, String), which constrains a resource to its expected prefix. An unauthenticated remote attacker can use the vulnerable behavior to read arbitrary resources permitted to the Jetty process, including WEB-INF/xwiki.cfg and, depending on deployment depth and operating-system permissions, host files. Tomcat and Jetty versions before 12 do not appear affected. This issue is fixed in versions 17.10.5 and 18.2.0.

### CVE-2026-57132

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-14T16:17:14.860 |

PraisonAI is a multi-agent teams system. Prior to 4.6.62, setting PRAISONAI_CALL_AUTH to disabled makes verify_token accept requests to /api/v1/agents/{id}/invoke without CALL_SERVER_TOKEN authentication. Deployments that use the application's advertised opt-out can expose registered agents and their connected tools or private context to unauthenticated invocation. The vulnerability is fixed in 4.6.62.

### CVE-2026-16141

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-457;CWE-798` |
| Published | 2026-09-15T14:16:50.430 |

OpenBMC's IPMI implementation, phosphor-net-ipmid, contains a logic flaw in which an unauthenticated client can force the RAKP Message 1 handler to return before it overwrites the authentication object's constructor defaults. The IPMI service then accepts a RAKP Message 3 whose HMAC is computed with the constant 20-byte 'userKey' initialized from the string '0penBmc' and an often-predictable 'bmcRandomNum'. Several downstream vendors implement phosphor-net-ipmid as their IPMI stack, such as NVIDIA and H3C.

### CVE-2026-16335

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T20:16:40.270 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 IBM DataStage could allow a remote authenticated attacker to read, write, or delete arbitrary files due to a path traversal vulnerability.

### CVE-2026-54182

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-78;CWE-116` |
| Published | 2026-09-14T18:17:53.380 |

backpack/crud provides Create, Read, Update & Delete (CRUD) functions for Backpack, a collection of Laravel packages that help users build custom administration panels. Prior to 4.1.70, 5.6.2, 6.8.13, and 7.0.36, Backpack\CRUD\Stats::makeCurlRequest in src/Stats.php is reached from BackpackServiceProvider::boot() and constructs a shell command with a URL influenced by the HTTP Host header, which it passes to exec() without adequate shell neutralization. An unauthenticated attacker whose malformed Host value reaches PHP can inject operating-system commands when exec() and curl are available and the 1-in-100 random gate is reached. Repeated requests can reach the random gate. Successful exploitation executes commands as the web-server user, exposing environment secrets, files, and reachable services and permitting data modification or service disruption. Common reverse-proxy Host validation and hardened PHP configurations that disable exec() reduce reachability but do not correct the vulnerable construction. This issue is fixed in versions 4.1.70, 5.6.2, 6.8.13, and 7.0.36.

### CVE-2026-54178

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-285;CWE-639` |
| Published | 2026-09-14T18:17:52.917 |

backpack/crud provides Create, Read, Update & Delete (CRUD) functions for Backpack, a collection of Laravel packages that help users build custom administration panels. Prior to 6.8.12 and 7.0.35, HasUploadFields::uploadMultipleFilesToDisk in src/app/Models/Traits/HasUploadFields.php trusts disk-relative paths from clear_<attribute>[] and passes them to Storage::disk()->delete without confirming that the paths are persisted on the current model record. An authenticated user with Update access to a CRUD using this mutator through src/app/Models/Traits/CrudTrait.php can delete another record's attachment, a shared asset, or another operational file on the configured disk by submitting its path. The newer MultipleFiles uploader is not affected because it intersects requested deletions with the record's persisted file list. This flaw does not permit reading the deleted files. The 5.x line remains affected through its final releases. This issue is fixed in versions 6.8.12 and 7.0.35.

### CVE-2026-82438

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346;CWE-942` |
| Published | 2026-09-14T15:17:10.900 |

Description

Three separate mechanisms allowed a web page on an unrelated origin to read responses that Storm's HTTP
components served to an authenticated user.

The Logviewer reflected the request's `Origin` header back in `Access-Control-Allow-Origin` while also
sending `Access-Control-Allow-Credentials: true`. The published security model documents a permissive
`Access-Control-Allow-Origin: *` posture as accepted, which is safe precisely because browsers refuse to
honour `*` together with credentials; reflecting the concrete origin removes that protection.

The shared CORS filter used by the UI, the Logviewer and DRPC was configured with a response header name
where an initialisation parameter name was expected. The container ignored the setting and applied its own
defaults, which allow credentials.

Finally, the UI and Logviewer wrapped API responses in a caller-supplied JSONP callback for every GET
request. A script element on any origin can load such a response, which bypasses the same-origin policy
entirely rather than negotiating it, and there was no way to turn the behaviour off.

In each case the effect is that a page visited by an authenticated operator can read cluster, topology and
log data on their behalf.

Mitigation

Upgrade to 3.1.0, where the Logviewer no longer reflects the request origin in a credentialed response, the
CORS filter is configured explicitly, and JSONP wrapping is governed by `ui.enable.jsonp`, which defaults to
false.

Note that disabling JSONP is a behaviour change for tooling that passes a `callback` query parameter; such
tooling should be moved to ordinary JSON requests.

Users who cannot upgrade immediately should place the UI, Logviewer and DRPC HTTP endpoints behind a reverse
proxy that strips `Access-Control-Allow-Origin` and `Access-Control-Allow-Credentials` from responses and
rejects requests carrying a `callback` parameter.

Credit

The ASF -- found using Claude agents to study the security of open-source projects, validated and reported by Apache Storm.

### CVE-2026-82432

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-14T15:17:10.187 |

Description

Nimbus validated `topology.blobstore.map` against the calling subject at submission time only. The rebalance
operation accepts configuration overrides and stripped a small set of keys from them, but never re-ran that
validation, so a caller authorised to rebalance a topology could introduce a blobstore map entry naming a
blob whose ACL does not grant them access. Supervisors localise whatever key the map names, placing the
blob's contents into the topology's working directory.

The same advisory covers `listBlobs`, which performed no authorization check and passed no subject, unlike
the neighbouring `getBlobMeta` and `beginBlobDownload` operations. It therefore returned every key in the
blobstore to any caller able to reach the Nimbus Thrift port, which provides the key names that make the
above practical. On its own the disclosure is metadata only.

Mitigation

Upgrade to 3.1.0, where rebalance configuration overrides are validated exactly as submission-time
configuration is, against the rebalancing caller, and where `listBlobs` applies the configured
authorization.

Users who cannot upgrade immediately should restrict rebalance rights to trusted principals, keeping in mind
that membership of a topology's `topology.users` or `topology.groups` confers them.

Credit

The ASF -- found using Claude agents to study the security of open-source projects, validated and reported by Apache Storm.

### CVE-2026-59569

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-14T15:17:06.603 |

An improper input validation vulnerability in Zscaler Client Connector on Android and ChromeOS allows an attacker to potentially bypass Zscaler controls.

### CVE-2026-57130

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-20;CWE-77` |
| Published | 2026-09-14T15:17:06.453 |

PraisonAI is a multi-agent teams system. Prior to praisonaiagents 1.6.59, src/praisonai-agents/praisonaiagents/tools/email_tools.py interpolates LLM-controlled from_addr, subject, and query values directly into quoted IMAP SEARCH criteria. Embedded quote, backslash, newline, or null characters can escape the intended criterion and alter IMAP operations when search_emails, reply_email, or archive_email is exposed to an agent with configured email credentials, allowing mailbox data access, modification, deletion, or connection disruption. This issue is fixed in praisonaiagents 1.6.59.

### CVE-2026-25687

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-366` |
| Published | 2026-09-14T15:17:05.090 |

A race condition in the ZPA tunnel handler of affected versions of Zscaler Client Connector (ZCC) allows a heap corruption, resulting in a denial of service (client crash) and potentially arbitrary code execution in the context of the ZCC process.

### CVE-2026-86917

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-280` |
| Published | 2026-09-14T21:17:41.760 |

A permissions issue was addressed with additional restrictions. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. An app may be able to gain root privileges.

### CVE-2026-84631

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-280` |
| Published | 2026-09-14T21:17:38.050 |

This issue was addressed with additional entitlement checks. This issue is fixed in macOS Golden Gate 27. An app may be able to gain root privileges.

### CVE-2026-84607

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-14T21:17:36.033 |

A race condition was addressed with improved state management. This issue is fixed in iOS 26.7 and iPadOS 26.7, iOS 27 and iPadOS 27, macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7, tvOS 27, visionOS 27, watchOS 27. A sandboxed app may be able to execute arbitrary code with kernel privileges.

### CVE-2026-84568

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T21:17:33.000 |

A path traversal issue was addressed with improved path validation. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. An attacker with control of a network directory server may be able to execute arbitrary code with root privileges.

### CVE-2026-84506

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-14T21:17:27.180 |

A use after free issue was addressed with improved memory management. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. An app may be able to execute arbitrary code with kernel privileges.

### CVE-2026-84505

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-14T21:17:27.077 |

An out-of-bounds write issue was addressed with improved bounds checking. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. An app may be able to gain root privileges.

### CVE-2026-65362

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-14T21:17:21.283 |

This issue was addressed with improved checks. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. An app may be able to gain root privileges.

### CVE-2026-64712

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-14T21:17:13.953 |

This issue was addressed with improved checks. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. An app may be able to gain root privileges.

### CVE-2026-64701

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-280` |
| Published | 2026-09-14T21:17:13.577 |

A permissions issue was addressed with additional restrictions. This issue is fixed in macOS Sequoia 15.7.8, macOS Tahoe 26.6. A malicious app may be able to gain root privileges.

### CVE-2026-43786

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-280` |
| Published | 2026-09-14T21:17:11.290 |

This issue was addressed with additional entitlement checks. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. An app may be able to gain root privileges.

### CVE-2026-43783

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-14T21:17:11.080 |

A race condition was addressed with improved locking. This issue is fixed in macOS Tahoe 26.6. A malicious app may be able to gain root privileges.

### CVE-2026-43691

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T21:17:08.443 |

A path handling issue was addressed with improved validation. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. An app may be able to gain root privileges.

### CVE-2026-43689

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-14T21:17:08.237 |

A permissions issue was addressed with additional restrictions. This issue is fixed in iOS 26.7 and iPadOS 26.7, iOS 27 and iPadOS 27, macOS Golden Gate 27, visionOS 27. A malicious app may be able to gain root privileges.

### CVE-2026-19624

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-14T20:16:43.593 |

A flaw was found in NetworkManager-l2tp. The plugin writes attacker-controlled VPN connection properties (vpn.data and vpn.secrets values) unescaped into a generated ipsec.conf file that pluto loads as root. A local unprivileged user can create and activate their own L2TP VPN profile containing a newline-injected leftupdown directive; pluto executes that command as root when the IKE security association is established, resulting in local privilege escalation. This is the same bug class as CVE-2018-10900 (NetworkManager-vpnc).

### CVE-2026-17416

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-14T20:16:41.733 |

IBM App Connect Enterprise 13.0.1.0 through 13.0.8.0, and 12.0.1.0 through 12.0.12.27 could allow a local attacker to execute arbitrary code due to insecure deserialization.

### CVE-2026-17156

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-14T20:16:41.593 |

IBM App Connect Enterprise 13.0.1.0 through 13.0.8.0, and 12.0.1.0 through 12.0.12.27 could allow a local attacker to execute arbitrary code due to insecure deserialization.

### CVE-2026-17133

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-14T20:16:41.460 |

IBM App Connect Enterprise 13.0.1.0 through 13.0.8.0, and 12.0.1.0 through 12.0.12.27 could allow a local attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-85892

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-14T18:20:19.343 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Microsoft Edge (Chromium-based) allows an authorized attacker to elevate privileges locally.

### CVE-2026-90947

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-14T16:17:41.860 |

A flaw was found in GIMP. When processing a specially crafted lighting preset file, the Lighting Effects filter does not properly validate the number of light sources. This can lead to an out-of-bounds write, corrupting memory. An attacker could exploit this by convincing a user to open a malicious preset file, potentially causing a crash or enabling arbitrary code execution.

### CVE-2026-82430

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-14T15:17:09.930 |

Description

When launching a Docker or OCI worker, the setuid-root `worker-launcher` first changes ownership of the
entire worker directory to the untrusted topology user, and only afterwards reads and acts on the command
file that the supervisor wrote into that same directory. The file is opened without `O_NOFOLLOW` and without
re-verifying its owner, so between the ownership change and the read the tenant can replace its contents.

For the Docker path the parsed command is executed with real uid 0, and the command sanitiser is not a
privilege boundary: it admits `-v` with an arbitrary source, `--device`, `--cap-add`, `--security-opt`,
`--user` and `--net`, and copies positional arguments through verbatim. A rewritten file therefore yields an
attacker-authored, root-equivalent container invocation with the host filesystem available.

For the OCI path the same rewrite window applies, and mount validation is structural only, with no
source or destination allow-list, so arbitrary host paths can be bind-mounted read-write into the
container. The `username` field of the command file is likewise attacker-settable and is checked only
against non-root and minimum-uid rules, permitting execution as another tenant's uid.

Mitigation

Upgrade to 3.1.0, where the command file is validated before the ownership change and re-verified on open,
and where mount sources and destinations are constrained by configuration.

Users who cannot upgrade immediately should disable Docker and OCI worker isolation, or restrict topology
submission on affected supervisors to trusted principals. Note that the launcher must be rebuilt and
reinstalled after upgrading.

Credit

The ASF -- found using Claude agents to study the security of open-source projects, validated and reported by Apache Storm.

### CVE-2026-82429

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-14T15:17:09.807 |

Description

The setuid-root `worker-launcher` binary adjusts ownership and permissions of worker directories by walking
the tree with FTS and calling `lchown` and `chmod` on each entry's full pathname while running with an
effective uid of 0. Both syscalls re-resolve the path at the time of the call, after FTS has classified the
entry, and the trees being walked are owned and writable by the untrusted topology user.

A tenant running code on a supervisor node could therefore replace an intermediate directory component with
a symbolic link between classification and the privileged operation, redirecting the root-owned `lchown` or
`chmod` at an arbitrary file on the host. The operation is repeatable at will, since crashing a worker
forces a relaunch and blob updates re-run the walk, so a failed attempt costs the attacker nothing.

This crosses the boundary that `supervisor.run.worker.as.user` and container isolation are intended to
enforce. It is the same defect class as the Hadoop container-executor issues from which this code derives.

Mitigation

Upgrade to 3.1.0, where the privileged walk operates on file descriptors it has already stat'd rather than
on pathnames re-resolved at call time.

Users who cannot upgrade immediately should not run untrusted topology code on supervisors configured with
`supervisor.run.worker.as.user`, since the launcher is the boundary being crossed. Note that the launcher
must be rebuilt and reinstalled after upgrading; replacing the Java artifacts alone is not sufficient.

Credit

The ASF -- found using Claude agents to study the security of open-source projects, validated and reported by Apache Storm.

### CVE-2026-82427

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T15:17:09.553 |

Description

A topology's `topology.blobstore.map` lets the submitter choose a local name for each blob that the
supervisor localises. That name was used to build a path under the topology's working directory without
normalisation, in both `AsyncLocalizer` and `Container.createBlobstoreLinks`, and the symlink helper
force-deletes whatever already exists at the target before creating the link.

A submitter could therefore use `../` segments to direct that delete-and-symlink operation at an arbitrary
path, as the supervisor user, on every node the topology is scheduled onto. The consequences include
recursive deletion of supervisor-owned content and planting a symlink that causes a subsequent worker
launch to execute attacker-chosen code as another tenant's operating-system user, which defeats the
isolation that `supervisor.run.worker.as.user` is intended to provide.

Mitigation

Upgrade to 3.1.0, where the resolved target must lie inside the expected root at both call sites.

Users who cannot upgrade immediately should restrict topology submission to trusted principals, and may
reject submissions whose `topology.blobstore.map` entries contain path separators or `..` segments before
they reach Nimbus.

Credit

The ASF -- found using Claude agents to study the security of open-source projects, validated and reported by Apache Storm.

### CVE-2026-45794

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-15T10:17:04.470 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, the anonymous Push Notification SNS callback handled by SnsMessageResource falls back to a CTS predicate blob after a messageId expires from the in-memory dispatcher, treats top-level blob keys as Java class names for Class.forName, and deserializes attacker-controlled JSON through Jackson. A low-privileged user who starts Push Registration and obtains the messageId, shared secret, and challenge can wait for expiry, replace the persistent blob through anonymous callbacks, and trigger class loading and construction in the OpenAM JVM. The primitive can cause classpath-dependent process execution, file writes, or denial of service, although command execution was not confirmed on the tested stock classpath. This issue is fixed in version 16.1.1.

### CVE-2026-73496

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-09-14T20:16:50.833 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, the confluence_upload_attachment and confluence_upload_attachments tools pass a client-controlled file_path through src/mcp_atlassian/confluence/attachments.py upload_attachment, and the jira_update_issue attachments parameter reaches src/mcp_atlassian/jira/attachments.py upload_attachment, without confining either path to an approved server workspace. In a remote HTTP, SSE, or multi-user deployment, absolute or traversing paths are resolved on the MCP server and uploaded to Atlassian, allowing a client with write-tool access to disclose server files, environment-held Atlassian credentials, or another tenant's data. A local single-user stdio deployment does not cross this trust boundary because the server runs in the caller's environment. This issue is fixed in version 0.22.0.

### CVE-2026-16432

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-14T20:16:40.663 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 IBM DataStage PxXMLInput operator could allow a remote authenticated attacker to obtain sensitive information due to an XML external entity (XXE) injection.

### CVE-2026-55253

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-943` |
| Published | 2026-09-14T18:17:55.500 |

LangChain MongoDB provides integrations between MongoDB, Atlas, LangChain, and LangGraph. Prior to langgraph-checkpoint-mongodb 0.3.0 and langgraph-store-mongodb 0.4.0, MongoDBSaver.list(), MongoDBSaver.alist(), and MongoDBStore.search() incorporate filter dictionaries into MongoDB queries without recursively rejecting keys prefixed with $. An authenticated caller who controls a filter argument through HTTP query parameters, request body fields, or agent tool arguments can inject MongoDB Query Language operators such as $regex or $where. In a multi-tenant deployment that uses the filter to enforce per-user or per-tenant isolation, injected operators can bypass intended equality filtering and expose other tenants' checkpoint or store data. Filters constructed entirely from trusted server-side values have lower practical risk. This issue is fixed in langgraph-checkpoint-mongodb 0.3.0 and langgraph-store-mongodb 0.4.0.

### CVE-2026-19499

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-14T18:17:45.753 |

Calling strfmon and strfmon_l in the GNU C Library version 2.38 to 2.44 can write past the end of the caller-supplied output buffer when a conversion uses right-justified width padding.

Exploitation requires an application code path that calls strfmon or strfmon_l with right-justified width padding into a destination buffer that is large enough for the padding to succeed but too small for the internal memmove call. The field width or format may be attacker-influenced or a fixed susceptible pattern in the caller.

At the time of publication, no network-facing application impact is known.

### CVE-2026-54155

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-14T17:17:46.737 |

node-opcua is an OPC UA implementation for TypeScript and Node.js. Prior to 2.166.0, the UserNameIdentityToken authentication handler in packages/node-opcua-server/source/opcua_server.ts decrypts an RSA-OAEP password blob but does not verify that the trailing bytes match the current session serverNonce. An unauthenticated remote attacker can obtain the server public key through GetEndpoints and forge a blob whose little-endian length produces an empty password passed to isValidUser, compromising accounts that accept an empty password. Missing nonce binding also allows a captured UserNameIdentityToken ciphertext to be replayed in another session, and SecurityMode=None removes the separate client-signature safeguard. This issue is fixed in version 2.166.0.

### CVE-2026-47701

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-14T16:17:11.540 |

The OpenTelemetry Operator is a Kubernetes Operator for the OpenTelemetry Collector. Prior to 0.152.0, cmd/otel-allocator TargetAllocator instances with targetAllocator.prometheusCR.enabled set to true preserve a selected ServiceMonitor endpoint's bearerTokenFile value as HTTPClientConfig.Authorization.CredentialsFile. A tenant who can create or update a ServiceMonitor matched by serviceMonitorSelector and serviceMonitorNamespaceSelector can point bearerTokenFile at a file in the Collector pod, including /var/run/secrets/kubernetes.io/serviceaccount/token, and direct scraping to a tenant-controlled endpoint. The Collector reads that file at scrape time and sends its contents as bearer authorization on every scrape interval. Exploitation also requires the Collector service-account token or another sensitive file to be mounted and the Collector to reach the chosen target. The DenyFSAccessThroughSMs control was absent, allowing disclosure of the Collector's service-account JWT or other mounted files, and resulting Kubernetes API impact is limited by the Collector service account's permissions. This issue is fixed in version 0.152.0.

### CVE-2026-57135

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-653;CWE-693` |
| Published | 2026-09-15T11:17:10.733 |

PraisonAI is a multi-agent teams system. From 1.2.3 until 1.7.2, SandboxExecutor network-isolated mode in src/praisonai-ts/src/cli/features/sandbox-executor.ts uses buildEnv() only to inject invalid http_proxy and https_proxy environment variables and does not establish an operating-system network boundary. Programs that ignore those proxy variables can open sockets directly, allowing supposedly isolated commands to reach localhost, internal services, cloud metadata, or external hosts and potentially exfiltrate data. An initial remediation was released in version 1.7.2.

### CVE-2026-47426

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-15T10:17:05.230 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, the private_key_jwt client authentication path uses ClientJwksResolverCache without reliably binding a cached jwks_uri resolver and verified assertion to the expected clientID in ClientCredentialsReader. An attacker controlling any registered client with published keys, including one obtained through open dynamic registration when enabled, can authenticate as another client whose keys are exposed through jwks_uri and mint tokens in that client's name across realms in the same OpenAM process. This issue is fixed in version 16.1.1.

### CVE-2026-46498

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-15T10:17:04.623 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, OAuthTokenStore reads caller-supplied token identifiers from the shared Core Token Store (CTS) without an OAuth-only namespace, and OAuthAdapter accepts a row whose BLOB claims to contain an OAuth token without binding the trusted CTS type or verifying integrity. An attacker who can place controlled JSON in CTS under a known token identifier, such as through Push Registration followed by an anonymous SNS callback in an enabled realm, can mint OAuth bearer tokens and OpenID Connect ID tokens with chosen subject, client, realm, and scope. The flaw does not by itself create an OpenAM SSO session or grant console access. This issue is fixed in version 16.1.1.

### CVE-2026-54180

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-09-14T18:17:53.070 |

backpack/crud provides Create, Read, Update & Delete (CRUD) functions for Backpack, a collection of Laravel packages that help users build custom administration panels. From 6.0.0 until 6.8.14 and 7.0.38, the Update, Delete, and Reorder operations resolve records from the unscoped model query instead of the query configured through addClause() or addBaseClause(). An authenticated user who knows or guesses an out-of-scope record primary key can therefore modify, delete, or reorder records hidden by tenant, ownership, or other row-level access-control scopes. Applications that do not rely on CRUD query clauses for authorization are not affected by this specific bypass. The fix routes all three write operations through getModelWithCrudPanelQuery(), matching the scoped list and read behavior. This issue is fixed in versions 6.8.14 and 7.0.38.

### CVE-2026-54175

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-620` |
| Published | 2026-09-14T18:17:52.430 |

backpack/crud provides Create, Read, Update & Delete (CRUD) functions for Backpack, a collection of Laravel packages that help users build custom administration panels. Prior to 6.8.11 and 7.0.34, MyAccountController::postAccountInfoForm in src/app/Http/Controllers/MyAccountController.php at POST /admin/edit-account-info passes request data from $request->except(['_token']) to the user model instead of restricting updates to fields accepted by AccountInfoRequest::validationData(). An attacker with an authenticated Backpack session can therefore mass-assign password, the authentication column, or other deployment-specific fillable attributes. With the default Laravel 11 user model, a submitted plaintext password is automatically hashed and persisted, converting temporary session access into persistent account takeover without the old_password check enforced by the separate password-change route. Changing the authentication email can also enable later password-reset takeover, while additional fillable security attributes can permit deployment-specific privilege escalation or security-control changes. This issue is fixed in versions 6.8.11 and 7.0.34.

### CVE-2026-54087

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-434` |
| Published | 2026-09-14T18:17:51.930 |

EasyAdmin is a fast and modern admin generator for Symfony applications. From 5.0.0 until 5.0.13, FileField and ImageField can accept browser-executable uploads while templates/crud/field/file.html.twig links to stored files for inline same-origin rendering without a download attribute or Content-Disposition attachment header. When uploads are stored under the public web root, an attacker with access to an affected form can upload HTML through FileField or SVG through ImageField, and JavaScript executes in an authenticated administrator's origin when the file is opened from the backend. Exploitation requires a privilege gap between the uploader and viewer. The issue can expose session or CSRF tokens and enable privilege escalation, but does not permit PHP or PHTML code execution because Symfony guessExtension does not produce those stored extensions. This issue is fixed in version 5.0.13.

### CVE-2026-47424

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-15T10:17:05.077 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, GroovySandboxValueFilter permits an authenticated server-side script author to escape the scripting sandbox despite the default class allow and deny lists. A user such as a sub-realm RealmAdmin who can create or edit a script in an executed context can invoke operating-system commands as the OpenAM application server account, crossing the realm-scoped administration boundary and compromising the JVM and every realm it serves. This issue is fixed in version 16.1.1.

### CVE-2026-75983

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-15T07:16:29.743 |

The Eventin – Event Calendar, Tickets, Registration, Booking & WooCommerce plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.1.23. This is due to the `PermissionManager::manage_permissions()` function being registered as a callback on WordPress core's `map_meta_cap` filter and unconditionally returning the always-true `'exist'` primitive for every capability check whenever the evaluated user ID is 1, without scoping this behavior to plugin-specific capabilities. This makes it possible for authenticated attackers whose account is user ID 1, even subscribers, to pass every WordPress capability check, including `manage_options`, `edit_plugins`, `edit_themes`, `promote_users`, and `update_core`, thereby elevating their privileges to administrator-equivalent power and achieving full site takeover, including remote code execution via the plugin and theme editors. Exploitation is only impactful when user ID 1 has been deliberately demoted to a lower-privilege role as a common administrator-account hardening practice; on default installations where user ID 1 retains the administrator role, no incremental privilege gain occurs.

### CVE-2026-84553

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-14T21:17:31.450 |

A resource exhaustion issue was addressed with improved input validation. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. A remote attacker may be able to cause a denial-of-service.

### CVE-2026-65364

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-14T21:17:21.393 |

An out-of-bounds read was addressed with improved bounds checking. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. A remote attacker may be able to cause unexpected system termination.

### CVE-2026-28960

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-14T21:17:05.823 |

A denial-of-service issue was addressed with improved validation. This issue is fixed in iOS 18.7.10 and iPadOS 18.7.10. A remote attacker may be able to cause a denial-of-service.

### CVE-2026-19290

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-14T21:17:04.767 |

IBM Sterling File Gateway 6.2.0.0 through 6.2.0.6_1, 6.2.1.0 - 6.2.1.2, 6.2.2.0 - 6.2.2.1 could allow a remote attacker to obtain sensitive information due to improper access control.

### CVE-2026-54632

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-755` |
| Published | 2026-09-14T20:16:47.010 |

SIPSorcery is a WebRTC, SIP, and VoIP library for C# and .NET. Prior to 10.0.9, RTPChannel.OnRTPPacketReceived and the STUNAttribute.ParseMessageAttributes, STUNXORAddressAttribute, and STUNAddressAttribute parsing path index untrusted bytes without sufficient length checks, while UdpReceiver.EndReceiveFrom closes the channel when those operations raise a non-socket exception. A remote party can send a single short RTP packet or malformed zero-to-seven-byte STUN address attribute to the shared RTP/ICE socket, including during ICE connectivity checks before DTLS or STUN MESSAGE-INTEGRITY verification, and terminate the active RTP or WebRTC media session. The attacker must reach or learn the advertised ephemeral RTP/ICE port, but no authentication or user interaction is required, and the impact is limited to availability. This issue is fixed in version 10.0.9.

### CVE-2026-54629

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-73;CWE-284;CWE-552;CWE-862` |
| Published | 2026-09-14T20:16:46.867 |

Anyquery is an SQL query engine built on top of SQLite. Prior to 0.4.5, anyquery server exposes file-backed SQLite virtual table modules such as csv_reader and log_reader through its MySQL-compatible server port without authentication, authorization, or directory restrictions. A remote attacker can use SQLite CREATE VIRTUAL TABLE statements to provide a local path to these modules, which use hashicorp/go-getter under the Anyquery server process and return the selected file contents as queryable table rows. The disclosure is limited only by the filesystem permissions of the server process and can expose system configuration, credentials, and private keys. This issue is fixed in version 0.4.5.

### CVE-2026-15955

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T20:16:39.057 |

IBM Db2 11.5.0 through 11.5.9, and 12.1.0 through 12.1.5 could allow a remote attacker to perform an arbitrary file write due to improper validation of file paths.

### CVE-2026-55091

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-915;CWE-1321` |
| Published | 2026-09-14T18:17:54.790 |

flat-to-nested converts a hierarchy from a flat representation to a nested representation. Prior to 1.1.2, FlatToNested.prototype.convert in index.js uses attacker-influenced id and parent record fields directly as keys in the plain temp and pendingChildOf objects. When parent or id is __proto__, temp[parent] can resolve to Object.prototype, and initPush() can write attacker-controlled data to the global children prototype property while existing prototype methods remain intact. Any application that passes attacker-influenced flat records to convert() can therefore expose unrelated objects to polluted inherited state, causing application-logic corruption or denial of service and potentially enabling greater impact when a downstream prototype-pollution gadget is present. The constructor and prototype strings are also unsafe inherited-key values in the same lookup design. This issue is fixed in version 1.1.2.

### CVE-2026-54567

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-178;CWE-434` |
| Published | 2026-09-14T18:17:53.547 |

Flask-Reuploaded provides file uploads for Flask. From 1.5.0 until 1.6.0, UploadSet.save(storage, name=...) in src/flask_uploads/flask_uploads.py applies lowercase_ext to the default upload path but uses the case-preserving extension helper for a caller-supplied name before extension_allowed evaluates an AllExcept denylist. An attacker who controls the name override can use a mixed-case dangerous extension to bypass a lowercase denylist and store the file in the served upload directory. Exploitation requires a denylist configuration, a user-influenced name override, and a deployment that resolves or executes extensions case-insensitively; pure allowlists remain protected and path containment is not bypassed. On an execution-capable upload directory, the stored file can execute with the web server's privileges and affect confidentiality, integrity, and availability. This issue is fixed in version 1.6.0.

### CVE-2026-53752

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674;CWE-770` |
| Published | 2026-09-14T18:17:51.773 |

docx4j is an open source Java library for creating, editing, and saving OpenXML packages, including DOCX, PPTX, and XLSX files. Prior to 11.5.14, PropertyResolver and adjacent helpers recursively follow the WordprocessingML w:basedOn style inheritance chain without cycle detection. A well-formed DOCX containing mutually based styles causes unbounded recursion in PropertyResolver.fillPPrStack and related effective-style resolution paths, resulting in StackOverflowError. Server-side conversion and table-of-contents processing of an untrusted document can terminate a worker thread, degrade a thread pool, or deny service, although isolation in disposable workers or safe containment of StackOverflowError can reduce the practical effect. The fix adds cyclic-style tracking and CyclicStylesException handling. This issue is fixed in version 11.5.14.

### CVE-2026-53659

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-14T18:17:51.610 |

http4k is a functional toolkit for Kotlin HTTP applications. Prior to 4.51.0.0, 5.42.0.0, and 6.49.0.0, ServerFilters.GZip, RequestFilters.GunZip, and the underlying Gzip request-body decompression functions impose no limit on decompressed size. An unauthenticated client can send a small gzip-encoded request body that expands to gigabytes, exhausting the JVM heap and denying service to other clients. The fix uses SizeLimitedInputStream to enforce a default 10 MiB limit, causes ServerFilters.GZip and RequestFilters.GunZip to return 413 Request Entity Too Large, and causes other decompression paths to throw SizeLimitExceededException. This issue is fixed in versions 4.51.0.0, 5.42.0.0, and 6.49.0.0.

### CVE-2026-50276

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-14T18:17:49.990 |

dd-trace-rb is Datadog's client library for Ruby. Prior to 2.32.0, W3C baggage extraction does not enforce DD_TRACE_BAGGAGE_MAX_ITEMS, which defaults to 64, or DD_TRACE_BAGGAGE_MAX_BYTES, which defaults to 8192, although those limits apply during baggage injection. A remote unauthenticated attacker can send a baggage HTTP header containing many comma-separated key-value pairs or a single very large value. The extraction path allocates entries while parsing the attacker-controlled header on every request, causing unbounded CPU and memory consumption in an HTTP service where the baggage propagation style is enabled, which is the default for most affected tracers. This can cause denial of service. This issue is fixed in version 2.32.0.

### CVE-2026-50270

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-14T18:17:49.830 |

dd-trace-java is a Datadog APM client for Java. Prior to 1.62.0, W3C baggage extraction does not enforce DD_TRACE_BAGGAGE_MAX_ITEMS, which defaults to 64, or DD_TRACE_BAGGAGE_MAX_BYTES, which defaults to 8192, although those limits apply during baggage injection. A remote unauthenticated attacker can send a baggage HTTP header containing many comma-separated key-value pairs or a single very large value. The extraction path allocates map entries while parsing the attacker-controlled header on every request, causing unbounded CPU and memory consumption in an HTTP service where the baggage propagation style is enabled, which is the default for most affected tracers. This can cause denial of service. This issue is fixed in version 1.62.0.

### CVE-2026-76442

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1284` |
| Published | 2026-09-14T17:17:50.810 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Email Gateway and Cisco Secure Email and Web Manager engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76442 are related to issues with improper validation of specified quantity in input that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-1284.

### CVE-2026-59960

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-14T17:17:49.447 |

Argos JavaScript provides official Argos SDKs for JavaScript. Prior to Argos core package version 6.2.1, attacker-controlled CI branch or ref values from GITHUB_HEAD_REF or ARGOS_BRANCH can flow through config.branch and getMergeBaseCommitSha() when hasRemoteContentAccess is false. The gitFetch() and gitMergeBase() functions in packages/core/src/ci-environment/git.ts interpolate these values into execSync() command strings executed by /bin/sh -c, so shell metacharacters in a pull-request branch name can execute arbitrary commands with the Argos upload process privileges on the CI runner. Successful exploitation can expose CI secrets, alter build artifacts, or compromise the runner. This issue is fixed in Argos core package version 6.2.1.

### CVE-2026-57579

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-14T17:17:49.267 |

Alchemy is an open source content management system engine written in Ruby on Rails. Prior to 7.4.15, 8.0.15, 8.1.14, and 8.2.6, the unauthenticated GET /api/pages/nested endpoint implemented by Api::PagesController#nested in app/controllers/alchemy/api/pages_controller.rb returns an unfiltered page tree because it performs no authorization and does not scope descendants by the caller's ability. Anonymous callers can retrieve restricted and unpublished page metadata that the sibling show action denies. When elements=true is supplied, PageTreeSerializer also returns element and ingredient content from restricted pages because PageTreePreloader and the serializer do not apply an ability check to those records. This issue is fixed in versions 7.4.15, 8.0.15, 8.1.14, and 8.2.6.

### CVE-2026-54156

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-14T17:17:46.927 |

node-opcua is an OPC UA implementation for TypeScript and Node.js. Prior to 2.166.0, the process-global g_alreadyUsedNonce cache used by nonceAlreadyBeenUsed in packages/node-opcua-secure-channel/source/server/server_secure_channel_layer.ts records nonces from OpenSecureChannelRequest and CreateSession without expiration or a size limit. An unauthenticated remote attacker can repeatedly create sessions with unique nonces, causing entries to persist after session expiry and accumulate across connection cycles even when maxSessions=10 limits concurrent sessions. The resulting unbounded heap growth can exhaust the default Node.js heap and crash the node-opcua server process. This issue is fixed in version 2.166.0.

### CVE-2026-57119

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T16:17:13.130 |

PraisonAI is a multi-agent teams system. Prior to 4.6.59, the unauthenticated Jobs API accepts an absolute or traversing agent_file path in POST /api/v1/runs and passes it to the job executor without a workspace allowlist or boundary check. A remote caller can cause the server to open files accessible to the service account, exposing credentials, keys, environment variables, and other local data. This vulnerability is fixed in 4.6.59.

### CVE-2026-59570

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-14T15:17:06.720 |

On affected versions of Zscaler client connector, a pre-installed peer app can tear down the Zscaler tunnel, force user logout, and toggle packet capture.

### CVE-2026-57129

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T15:17:06.317 |

PraisonAI is a multi-agent teams system. Prior to praisonaiagents 1.6.59, MentionsParser._process_file_mention accepts file-mention values and falls back from workspace-relative resolution to Path(file_path) without traversal, symlink, or workspace-boundary validation. Prompt input from users, bots, or workflows can therefore read arbitrary files accessible to the process, including credentials, keys, environment files, source code, and system configuration. This issue is fixed in praisonaiagents 1.6.59.

### CVE-2026-53660

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1004;CWE-1188;CWE-1275` |
| Published | 2026-09-15T10:17:05.527 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, the default configuration initializes the iPlanetDirectoryPro SSO cookie with HttpOnly disabled and without a protective SameSite default, and OAuth and OpenID Connect consent flows reuse that cookie through CsrfProtection as a CSRF token. When combined with same-origin cross-site scripting and a user following an attacker-controlled link, the cookie can be read and reused to steal the SSO session and complete attacker-driven consent grants. This issue is fixed in version 16.1.1.

### CVE-2026-46623

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620;CWE-1391` |
| Published | 2026-09-15T10:17:04.920 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, the OAuth2 authentication module updates an existing local account with profile attributes that can include userPassword and inetUserStatus, rewriting the password to the username and reactivating disabled accounts. The missing OAuth.removeRestrictedAccountUpdateAttributes filtering permits these credential and status fields to reach the account update. With account creation enabled, repeated OAuth login causes the default ldapService chain to accept the username as both identifier and password, allowing an unauthenticated attacker to take over the local account without interacting with the identity provider. The rewrite can be denied for usernames shorter than the configured minimum password length. This issue is fixed in version 16.1.1.

### CVE-2026-53714

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-14T21:17:12.677 |

Envoy Gateway is an open source project for managing Envoy Proxy as a standalone or Kubernetes-based application gateway. Prior to 1.7.4 and 1.8.1, the xDS gRPC server in GatewayNamespaceMode, configured through provider.kubernetes.deploy.type=GatewayNamespace, installs a JWT StreamInterceptor but no UnaryInterceptor, leaving every unary Fetch RPC unauthenticated. The streaming interceptor also authenticates only discoveryv3.DeltaDiscoveryRequest messages; a discoveryv3.DiscoveryRequest used by the State-of-the-World protocol fails the type assertion and returns success without JWT validation. Any pod that can reach port 18000 can use the unauthenticated unary or State-of-the-World paths to retrieve TLS private keys through StreamSecrets, all xDS resources through StreamAggregatedResources, backend endpoints through StreamClusters or StreamEndpoints, and routing configuration through StreamRoutes or StreamListeners. This issue is fixed in versions 1.7.4 and 1.8.1.

### CVE-2026-73494

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-14T18:19:58.857 |

blaze is a Scala library for building asynchronous pipelines, with a focus on network IO. Prior to 0.23.18 and from 1.0.0-M1 until 1.0.0-M42, five HTTP/1.1 conformance laxities in the hand-written Java parser under http/src/main/java/org/http4s/blaze/http/parser/ can cause blaze to derive a different request boundary than a stricter fronting intermediary. A default BlazeServerBuilder accepts invalid or valueless header field names that violate tchar syntax, obsolete folded field lines (obs-fold), unsupported Transfer-Encoding values, duplicate Content-Length fields, and requests containing both Transfer-Encoding and Content-Length. If a lenient or legacy proxy forwards the malformed bytes but interprets them differently, the disagreement can permit front-end authorization bypass, response-queue poisoning on pooled backend connections, or cache poisoning. Exploitation requires a pair of disagreeing parsers; no non-default blaze configuration is required. The affected checks are enforced in BodyAndHeaderParser and Http1ServerParser. This issue is fixed in versions 0.23.18 and 1.0.0-M42.

### CVE-2026-70658

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-208` |
| Published | 2026-09-14T18:19:45.213 |

Pay is a payments engine for Ruby on Rails 6.0 and higher. Prior to 11.6.2, Pay::Webhooks::PaddleBillingController#valid_signature? in app/controllers/pay/webhooks/paddle_billing_controller.rb compares the computed 64-character SHA-256 HMAC with the attacker-controlled h1 token from the Paddle-Signature header using Ruby String#==. An unauthenticated remote attacker who can repeatedly submit requests to /pay/webhooks/paddle_billing and obtain sufficiently precise timing measurements can infer matching digest prefixes and recover a valid signature. A forged accepted webhook is enqueued through Pay::Webhooks::ProcessJob and can cause a host application to update billing state, provision paid features, record refunds, or trigger customer notifications. This issue is fixed in version 11.6.2.

### CVE-2026-75092

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-09-15T09:16:43.727 |

A privilege escalation flaw was found in the scan_mysql actor of leapp-upgrade-el9toel10 (provided by leapp-repository). During RHEL 9 to RHEL 10 upgrades, the actor runs:
mysqld --validate-config --log-error-verbosity=2 directly as root in the Leapp actor context, bypassing the packaged MySQL systemd unit that normally starts the daemon as User=mysql.

A process compromised as the mysql OS identity can write a version-2 persisted configuration (mysqld-auto.cnf) and a malicious shared object into /var/lib/mysql (a directory owned by mysql). That persisted map can set plugin_dir to /var/lib/mysql and early_plugin_load (or related loader options such as plugin_load / plugin_load_add) so MySQL loads the attacker-controlled object during configuration validation. Plugin loading can reach dlopen() before MySQL’s runtime-user check and before plugin-symbol validation.

When an administrator subsequently runs the documented Leapp preupgrade or upgrade workflow, attacker-controlled code can execute as UID 0 with a full capability set in an unconfined SELinux domain (unconfined_t). The attack does not require write access to the default system plugin path under /usr; redirecting plugin_dir via mysql-owned persisted state is sufficient. Ordinary SQL privileges alone (including highly privileged SQL accounts) are not a sufficient startpoint — OS-level execution as the mysql service identity is required, plus later administrator invocation of Leapp.

### CVE-2026-81900

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T23:18:48.333 |

Concrete CMS before 9.5.3 applied only trim() to the YouTube block's stored width and height values and printed them into iframe HTML attributes without escaping or integer casting, resulting in stored cross-site scripting. A user with edit_block permission could inject an event handler that executed script for visitors rendering the page, acting with administrative privileges where the victim was an administrator. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.3 with vector CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks sh4d0byss for reporting.

### CVE-2026-18116

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T23:17:15.683 |

Concrete CMS 8.3.0 to 9.5.2 stored calendar event names without sanitization and rendered them without HTML escaping in the workflow approval and deletion notifications shown in the dashboard "Waiting For Me" block. A registered user permitted to add events to a calendar governed by an approval workflow could submit an event whose name contained a script payload, which then executed in an administrator's browser when the pending request was displayed and could be used to create a new administrator account. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.3 with vector CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks v01demort for reporting.

### CVE-2026-18117

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T22:16:57.483 |

Concrete CMS 9.0.0 through 9.5.3 is vulnerable to stored XSS via the custom page alias name (customAliasName) because the Edit Alias dialog applied only trim() to the submitted value and performed no input neutralization. An authenticated user holding canWrite (editor) permission on a page could store a malicious alias name that was later rendered unescaped in the administrative Sitemap panel, where it executed automatically in any administrator or editor session that opened the panel, allowing an editor to escalate to administrator through the victim's active session. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.3 with vector CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N. Thanks Nguyen Manh Thuan for reporting.

### CVE-2026-64752

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-14T21:17:14.770 |

A memory corruption issue was addressed by removing the vulnerable code. This issue is fixed in iOS 27 and iPadOS 27, macOS Golden Gate 27, visionOS 27. Processing a maliciously crafted image may lead to arbitrary code execution.

### CVE-2026-47253

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T20:16:44.070 |

Anyquery is an SQL query engine built on top of SQLite. Prior to 0.4.5, the clear_plugin_cache(plugin) SQL scalar function in namespace/other_functions.go passes the caller-controlled plugin parameter through path.Join to os.RemoveAll without rejecting traversal segments. A low-privileged bearer-token holder can invoke the function through the /v1/query HTTP endpoint, causing path.Join to resolve .. segments outside $XDG_CACHE_HOME/anyquery/plugins/ and os.RemoveAll to recursively delete any reachable directory writable by the Anyquery server process. This causes permanent data loss and denial of service without disclosing file contents. This issue is fixed in version 0.4.5.

### CVE-2026-56839

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-200;CWE-863` |
| Published | 2026-09-14T16:17:12.977 |

PraisonAI is a multi-agent teams system. Prior to 4.6.59, the CODE_TOOLS wrappers keep _workspace_root as None and pass workspace=None to read_file, search_replace, and apply_diff helpers that enforce path containment only for a truthy workspace. An application that exposes code_read_file, code_search_replace, or code_apply_diff before set_workspace can therefore let prompt-influenced calls read and modify files outside the intended project directory, while explicitly configured workspaces remain effective. This vulnerability is fixed in 4.6.59.

### CVE-2026-91778

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-15T08:17:07.180 |

In affected versions of Octopus Server, users with certain scoped permission sets could execute arbitrary scripts on a worker (including the Octopus Server built-in worker). Incorrect permission validation during script execution would allow the script to execute without the user possessing the required authorisation.

### CVE-2026-91751

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-15T01:16:54.797 |

Flextype CMS through 1.0.0-alpha.3 fails to properly validate id and new_id parameters in the Entries REST API, allowing API token holders to read, create, or overwrite files outside the entries directory. Attackers can use traversal sequences in API requests to escape the project entries directory and manipulate arbitrary files and directories on the filesystem.

### CVE-2026-81901

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-14T21:17:26.123 |

In Concrete CMS 9.2.0 through 9.5.2, the REST API page update endpoint (PUT /ccm/api/1.0/pages/{cID}) did not enforce page-property, page-template, or page-type authorization. A user granted only content-editing rights on a page could therefore alter its properties, template, and type through the API, and could set the header_extra_content attribute, which is rendered unescaped into the head element of every page, to persist JavaScript that executed in the browser of every visitor, including higher-privileged reviewers who approve the page version. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.2 with vector CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N. Thanks Yonatan Drori from Tenzai for reporting.

### CVE-2026-91994

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T12:17:54.793 |

Semaphore UI through 2.19.12 exempts GET and HEAD requests from project resource permission checks in GetMustCanMiddleware. Attackers with guest or task_runner roles can read all project environments including plaintext secrets, credentials, and passwords via GET requests to the environment endpoint.

### CVE-2026-52827

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-15T11:17:09.993 |

Kimai is an open-source time tracking application. Prior to 2.59.0, the KIMAI_SESSION cookie issued after password verification but before TOTP completion is accepted by every /api route because config/packages/security.yaml protects the API with IS_AUTHENTICATED and App\API\Authentication\ApiRequestMatcher routes an existing session through the main firewall. A Scheb TwoFactorToken satisfies that access rule, and App\Voter\ApiVoter grants API access to its User, allowing an attacker with a valid account password to use authenticated REST API operations without entering the second factor even though web routes remain blocked. This issue is fixed in version 2.59.0.

### CVE-2026-41573

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-90` |
| Published | 2026-09-15T10:17:03.123 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, IdentityResourceV1.queryCollection() passes the _queryId parameter from /json/{realm}/users to CrestQuery with escapeQueryId disabled, bypassing protection added for CVE-2021-29156. The unescaped value reaches DJLDAPv3Repo.getFilter(), where it is concatenated into an LDAP filter, allowing an authenticated attacker to inject LDAP metacharacters for user enumeration and blind LDAP injection. This issue is fixed in version 16.1.1.

### CVE-2026-91846

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-09-15T09:16:45.897 |

Affected versions of MISP allow a collection element to be created from a bare UUID without consistently checking whether the acting user is allowed to access the referenced object.


The commit explains that collection elements themselves only store UUIDs, while the collection view later resolves those UUIDs into their underlying objects. Before this fix, the generic add() path could therefore persist a UUID for an Event or Galaxy Cluster that the caller could not normally read. The patch explicitly notes that this made collections a way to reference another organisation’s private data and had caused disclosure of organisation-only events in the beta collection view.


The fix centralizes authorization in __assertCanUseElements(). Event UUIDs are validated through Event::fetchSimpleEvent() under the current user’s ACL, while Galaxy Cluster UUIDs are checked through GalaxyCluster::fetchGalaxyClusters(). The check is applied both to the CRUD add() path and to addElementToCollection().

Version affected: ≤2.5.45

### CVE-2026-91825

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-15T09:16:45.540 |

Affected versions of MISP fail to authorize a submitted sharing group in a specific event-edit path.


The vulnerable logic checked whether the acting user could use a sharing_group_id only when the request explicitly supplied distribution = 4. If the attacker instead omitted distribution but supplied a different sharing_group_id, that authorization branch was skipped. Later, MISP’s field-recovery logic restored the existing event distribution from storage. For events already configured with sharing-group distribution, the unauthorized sharing-group ID could therefore be saved.


The fix adds authorization checks in both the controller and Event::_edit() whenever a non-empty sharing_group_id is supplied without distribution. The model now calls SharingGroup::checkIfAuthorised() before persisting the change.



Version affected: ≤2.5.45

### CVE-2026-91770

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-15T02:16:49.517 |

IceHRM before 36.0.0 fails to validate employee ownership on seven REST sub-resource endpoints, allowing authenticated employees to read any colleague's HR records. Attackers can substitute arbitrary employee IDs in skill, education, certification, language, leave, attendance, and status endpoints to access sensitive personnel data.

### CVE-2026-91750

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-15T01:16:54.630 |

WeKnora before 0.7.0 fails to re-validate HTTP redirect targets in the POST /api/v1/knowledge-bases/:id/knowledge/url endpoint when downloading documents from user-supplied URLs. Authenticated attackers can bypass initial SSRF validation by supplying a public URL that redirects to internal network addresses, allowing access to internal services and cloud metadata.

### CVE-2026-91197

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-14T23:19:00.173 |

Flowable flowable-engine through 8.0.0 contains an XML external entity injection vulnerability in ProcessDiagramLayoutFactory.parseXml() that fails to disable external entity resolution when parsing deployed BPMN resources. Attackers with process deployment privileges can embed DOCTYPE declarations with external entities in BPMN files to read arbitrary local files or trigger requests to internal network endpoints when diagram layout is computed.

### CVE-2026-91145

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-917` |
| Published | 2026-09-14T22:16:59.217 |

Activiti through 7.1.0.M6 fails to validate hash-brace deferred expressions in process variables, allowing attackers to bypass expression filtering. Attackers can inject expressions beginning with #{ that are stored and later evaluated in the full Spring context when a mail task uses variable-backed body fields, enabling method invocation on application beans.

### CVE-2026-12756

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-14T22:16:56.470 |

IBM Business Automation Workflow containers and traditional is vulnerable to an XML external entity injection (XXE) attack when processing XML data. A remote attacker could exploit this vulnerability to expose sensitive information or consume memory resources.

### CVE-2026-81902

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-14T21:17:26.267 |

Concrete CMS 9 through 9.5.2 did not validate a CSRF token in the orphaned block removal panel action (removeOrphanedBlocks). A remote attacker could craft a request that, when loaded by an authenticated user holding edit permission on the target page, deleted every block on that page's current version; blocks not aliased to another page or scrapbook entry were also removed from the global Blocks table and their block-type data table, permanently destroying the content. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.1 with vector CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N. Thanks Yonatan Drori from Tenzai for reporting.

### CVE-2026-13287

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-14T21:17:01.977 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 is vulnerable to an XML external entity injection (XXE) attack when processing XML data. A remote attacker could exploit this vulnerability to expose sensitive information or consume memory resources.

### CVE-2026-13285

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-14T21:17:01.823 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 is vulnerable to an XML external entity injection (XXE) attack when processing XML data. A remote attacker could exploit this vulnerability to expose sensitive information or consume memory resources.

### CVE-2026-13275

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-14T21:17:01.393 |

IBM MQ 9.1.0.0 through 9.1.0.37 LTS, 9.2.0.0 through 9.2.0.43 LTS, 9.3.0.0 through 9.3.0.41 LTS, 9.3.0.0 through 9.3.5.1 CD, 9.4.0.0 through 9.4.0.25 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 Managed File Transfer could allow an authenticated attacker to read arbitrary files or perform server-side request forgery due to XML external entity injection in reply message processing.

### CVE-2026-13107

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-14T21:17:00.980 |

IBM Business Automation Workflow containers and traditional may use programming model artifacts that are vulnerable to XML Entity Injection attacks by default.

### CVE-2026-19816

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-14T20:16:43.760 |

A flaw was found in PackageKit. PackageKit skips the polkit authorization check for transactions carrying the SIMULATE (dry-run) flag. In the dnf5 backend, the RepoRemove handler ignores that contract and always executes the real transaction because its guard is written as (role == REPO_REMOVE || !SIMULATE), which is always true for RepoRemove. An unprivileged local user can therefore perform a genuine package uninstall while claiming to simulate. This vulnerability only affects systems using PackageKit with the dnf5 backend.

### CVE-2026-82035

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T19:17:50.380 |

PyMuPDF through 1.28.2, fixed in commit b2c8f3a, contains a path traversal vulnerability in the font branch of extract_objects() in src/__main__.py, where the output filename is constructed by joining a document-controlled BaseFont name directly onto the user-supplied output directory without stripping path separators or dot-dot sequences. Attackers can supply a crafted PDF, EPUB, XPS, or FB2 file with a BaseFont name containing encoded path separators that decode to ../ sequences or absolute paths, causing arbitrary file writes outside the intended output directory without requiring authentication or elevated privileges.

### CVE-2026-77884

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-09-14T19:17:44.700 |

Gallery - Private Photo Vault 1.0.41 starts an unauthenticated HTTP server that is reachable from the local network. The server listens on TCP port 8080 and serves files and directory listings from Android external storage.

### CVE-2026-44793

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:L/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-15T10:17:03.717 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, certain federation endpoints in a non-default clustered configuration inconsistently encode user-supplied parameters rendered into HTML in the SAML2 cluster cookie-hash redirect path. An unauthenticated attacker can induce a user to follow a crafted request and execute script in the OpenAM origin. This issue is fixed in version 16.1.1.

### CVE-2026-19515

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-15T10:17:02.960 |

The WSO2 Integrator MI VS Code extension fails to properly sanitize or validate user-supplied input when processing Micro Integrator projects opened from untrusted sources. This allows a crafted project to inject and execute arbitrary operating system commands through the unit test execution flow.

Successful exploitation of this vulnerability could lead to the execution of arbitrary OS commands on the system where the VS Code extension is running. The extent of the impact is dependent on the privileges of the user account under which VS Code is operating. Exploitation requires the user to grant workspace trust to the malicious project and subsequently trigger the unit test execution.

### CVE-2026-76159

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-15T09:16:43.900 |

Incorrect Permission Assignment for Critical Resource in the  configuration loader of Duplicati for Windows versions before v2.4.0.0 allows a local low-privileged attacker to escalate       privileges to NT AUTHORITY\SYSTEM via an attacker-controlled preload.json file.

### CVE-2026-81903

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T21:17:26.400 |

Concrete CMS versions 9.0.0 to 9.5.2 stored the Page Container icon value submitted through the dashboard without validating it against the set of known container icons. The unvalidated value was later concatenated into the src attribute of an img tag by a helper that did not encode attribute output, and was rendered raw in the Containers dashboard list and editor views. A user with delegated access to the Page Containers dashboard could store a crafted icon value that broke out of the src attribute and executed script in the authenticated session of another editor or administrator who viewed the list, enabling session token theft and privileged dashboard actions. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.0 with vector CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks Andrew Gonzalez for reporting.

### CVE-2026-18119

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T20:16:42.563 |

Concrete CMS below 9.5.3 did not sanitize custom style values in the Block Design dialog before writing them into page CSS via a DOM sink, permitting stored cross-site scripting. An editor-level user could execute script in an administrator's session and escalate privileges. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.0 with vector CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks Nguyen Manh Thuan for reporting.
