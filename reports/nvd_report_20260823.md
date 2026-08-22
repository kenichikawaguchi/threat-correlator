# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-22 15:01 UTC
- **対象期間**: `2026-08-21T15:00:19.000Z` 〜 `2026-08-22T15:01:14.000Z`
- **重要CVE数**: 106 件（Critical 9.0+: 31 件 / High 7.0〜: 75 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE のうち **CVSS 7.0 以上は 30 件以上** と、重大度の高い脆弱性が集中しています。  
- **リモートコード実行 (RCE)・サーバーサイドリクエストフォージェリ (SSRF)・権限昇格** が目立ち、特にコンテナ/VM 管理ツール（Incus）やクラウドサービス（Azure SQL、Google Cloud）で深刻な影響が報告されています。  
- 多くは **入力検証不備やシンボリックリンク・メタデータ処理の不適切** が原因で、認証済みユーザーでも **ホスト OS の root 権限取得** が可能になるケースが多数です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|--------------------|
| **CVE‑2026‑61539** | 10.0 | Xinference 2.5.0 以前の Llama‑3 ツール呼び出しで `eval()` に攻撃者制御文字列が流入 | **リモートコード実行** が無認証で可能。AI 推論 API を外部に公開している環境は即時対策が必須。 |
| **CVE‑2026‑69502** | 10.0 | Azure SQL Database の SSRF によりネットワーク上の他サービスへリクエストを送信、権限昇格が可能 | **クラウド基盤全体への波及リスク** が高く、マルチテナント環境での情報漏洩・横方向移動を招く。 |
| **CVE‑2026‑63343**  (Incus) | 9.9 | メタデータ API に symlink を含む画像を配置すると、ホスト上の任意ファイルを **root で読み書き** できる | **コンテナ/VM 管理サーバー全体が危殆化**。同様の脆弱性が Incus 系列で多数報告されているため、最優先でアップデートが必要。 |
| **CVE‑2026‑76904** | 9.8 | GeoTools 30.5‑33.5 の OGC フィルタで **SQL Injection** が発生 | 地理情報システムを外部に提供しているサービスはデータベース改ざん・情報漏洩の危険がある。 |
| **CVE‑2026‑78003** | 9.8 | WordPress 用 Mailgun プラグイン 2.2.0 までの **SSRF**（パス・トラバーサル） | WordPress サイトは多数運用されているため、プラグインの脆弱性は **広範囲な被害** を引き起こす可能性が高い。 |

> **共通点**：いずれも「外部からの入力を適切にサニタイズせず、内部リソースやシステムコマンドに直結させている」点に起因しています。  

---

## 3. 推奨アクション  

### 3.1. ソフトウェア・パッケージのアップデート
| 製品 / パッケージ | 現行脆弱バージョン | **推奨バージョン** | 備考 |
|-------------------|-------------------|-------------------|------|
| **Xinference** | ≤ 2.5.0 | **2.5.1 以上** | `llama3_tool_parser.py` の `eval()` 呼び出しを除去したパッチが含まれる。 |
| **Azure SQL Database** | すべて（サービス） | **Microsoft が提供する最新パッチ**（2026‑04‑04 以降） | ネットワーク制御（VNet、Private Endpoint）と **外部向け URL フィルタリング** を併用。 |
| **Incus** | 1.14.13‑1.14.14、2.0.0‑2.0.9、7.1.0‑7.2.0 など | **7.3.0 以上** | 7.3.0 でメタデータ・イメージ処理のシンボリックリンク検証が強化。 |
| **GeoTools** | 30.5‑33.5、34.4 以前 | **33.6 以上** または **34.5 以上** | OGC フィルタ実装の SQL エスケープが修正。 |
| **Mailgun for WordPress** | ≤ 2.2.0 | **2.2.1 以上** | `add_list()` の入力検証が追加。 |
| **JSONata** | < 1.8.8 / < 2.2.0 | **1.8.8 以上 / 2.2.1 以上** | オブジェクトプロトタイプ汚染の防止パッチ。 |
| **FreeRTOS‑Kernel** | < 11.3.1 | **11.3.1 以上** | MPU ポートでのタスク権限チェックが修正。 |
| **Phalcon (PHP)** | ≤ 5.15.0 | **5.15.1 以上** | `resolveFilter` の文字列サニタイズが追加。 |
| **llama.cpp** | < b8585 | **b8585 以上** | RPC サーバの use‑after‑free 修正。 |
| **xShop (Laravel)** | 3.0.3 | **3.0.4 以上** | ファイルアップロードの MIME/拡張子チェック強化。 |

### 3.2. 環境・設定レベルの対策
1. **最小権限の原則**を徹底  
   - Incus のプロジェクト権限や Azure SQL の接続文字列は、必要最小限の権限に絞る。  
2. **ネットワーク境界の強化**  
   - Azure SQL、Google Cloud Integration などは **Private Link / VPC Service Controls** を有効化し、外部からの直接アクセスを遮断。  
   - WordPress サイトは **Web Application Firewall (WAF)** で SSRF パス・トラバーサルをブロック。  
3. **入力検証・サニタイズの実装**  
   - カスタムプラグインや独自 API（例：Xinference のツール呼び出し）では、外部から受け取る文字列を **JSON パースや正規表現でホワイトリスト化** する。  
4. **監査ログの有効化と SIEM 連携**  
   - Incus のメタデータ API、Azure SQL の `sp_whoisactive` など、特権操作のログを取得し、異常検知ルールを設定。  
5. **定期的な脆弱性スキャン**  
   - コンテナイメージ・VM テンプレートは **Trivy / Clair** でスキャンし、特に `metadata.yaml`、`backup.yaml`、`raw.lxc` などの設定ファイルの改

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-61539

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-21T21:17:00.867 |

Xinference is an inference API for running open-source, speech, and multimodal models. In 2.5.0 and earlier, Xinference passes attacker-influenced Llama3 tool-call output to eval() in xinference/model/llm/tool_parsers/llama3_tool_parser.py and xinference/model/llm/utils.py. Requests to /v1/chat/completions with a tools field flow through xinference/api/restful_api.py, xinference/model/llm/transformers/core.py, handle_chat_result_non_streaming(), and _post_process_completion() before extract_tool_calls() or _eval_llama3_chat_arguments() evaluates the model-generated Python expression. An unauthenticated remote attacker can influence that output through a crafted prompt and execute commands in the Xinference server process context. This issue is fixed in version 2.7.0.

### CVE-2026-69502

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-21T16:18:07.090 |

Server-side request forgery (ssrf) in Azure SQL Database allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-62283

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-21T21:17:01.183 |

Nezha Monitoring is a self-hostable, lightweight, servers and websites monitoring and O&M tool. Nezha versions 1.14.13 through 1.14.14 and 2.0.0 through 2.0.9 do not bind stream identifiers created by CreateStream in service/rpc/io_stream.go to their creating user, and `GET /ws/terminal/:id` and `GET /ws/file/:id` only check whether the supplied UUID exists. An authenticated RoleMember who obtains a live stream UUID from logs, browser history, referer data, or telemetry can attach to another user's terminal or file-manager session, read and write target-server files, and execute shell commands. This issue is fixed in version 2.0.10.

### CVE-2026-63343

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-21T15:16:46.577 |

Incus is a system container and virtual machine manager. Prior to version 7.3.0, a malicious image containing a `metadata.yaml` symlink pointing to an arbitrary host path allows an authenticated Incus user to read or overwrite any file on the host as root via the instance metadata API. The `exec-output` and `templates/` paths were patched in a prior release using `Lstat` rejection and `os.OpenRoot` confinement; `metadata.yaml` was not included in either patch and remains exploitable. Version 7.3.0 patches the issue.

### CVE-2026-63125

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-61` |
| Published | 2026-08-21T15:16:46.427 |

Incus is a system container and virtual machine manager. Prior to version 7.3.0, an unprivileged, project-confined Incus user (a non-admin TLS/RBAC identity with `can_create_images` and `can_create_instances`) can execute arbitrary code as root on the host. A crafted image ships `backup.yaml` as a symlink to a host file. When the root daemon writes the instance's backup file, it follows the symlink. Version 7.3.0 patches the issue.

### CVE-2026-62941

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-21T15:16:46.287 |

Incus is a system container and virtual machine manager. Prior to version 7.3.0, when copying an instance across projects, the project restriction check (`AllowInstanceCreation`) runs BEFORE the source instance's configuration is merged into the request. Dangerous configuration keys (including `security.privileged`, `raw.lxc`, `raw.apparmor`) from the source instance are merged AFTER the check passes, bypassing all project restrictions on the target project. Version 7.3.0 patches the issue.

### CVE-2026-62940

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-21T15:16:46.147 |

Incus is a system container and virtual machine manager. Prior to version 7.3.0, when migrating an instance to another cluster member, user-supplied configuration overrides (including security-critical keys like `security.privileged` and `raw.lxc`) are applied without any project restriction enforcement, allowing a restricted project user to escalate to a privileged container and escape to the host. Version 7.3.0 patches the issue.

### CVE-2026-62867

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-21T15:16:46.003 |

Incus is a system container and virtual machine manager. Prior to version 7.3.0, improper validation of user-provided `block.create_options` in storage volume configuration leads to argument injection in the constructed filesystem creation command line. This allows a project-scoped user to inject arbitrary arguments into the binary executed as root. Version 7.3.0 patches the issue.

### CVE-2026-48769

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-21T15:16:41.347 |

Incus is a system container and virtual machine manager. Prior to version 7.2.0, an arbitrary file write exists in the Incus client when a malicious image server returns a crafted `Incus-Image-Hash` header. This can lead to arbitrary command execution as root on the server. Version 7.2.0 patches the issue.

### CVE-2026-48755

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-21T15:16:41.077 |

Incus is a system container and virtual machine manager. Prior to version 7.1.0, improper validation of user-provided backup compression algorithm leads to argument injection in the constructed command line. This leads to an arbitrary file write on the host, possibly leading to arbitrary command execution. Version 7.1.0 patches the issue.

### CVE-2026-48753

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-21T15:16:40.800 |

Incus is a system container and virtual machine manager. Prior to version 7.1.0, the S3 protocol upload endpoint is vulnerable to path traversal and allows creation of arbitrary files on the host. This behavior could lead to arbitrary command execution. Version 7.1.0 fixes the issue.

### CVE-2026-48752

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-21T15:16:40.667 |

Incus is a system container and virtual machine manager. Prior to version 7.2.0, a specially crafted image or instance backup can be used to read or create/write arbitrary files on the host; possibly leading to arbitrary command execution. Version 7.2.0 patches the issue.

### CVE-2026-48751

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-21T15:16:40.527 |

Incus is a system container and virtual machine manager. Prior to version 7.2.0, instance snapshots ignore the `restricted.containers.lowlevel=block` setting; allowing for arbitrary command execution on the Incus server by abusing lowlevel hooks such as `raw.lxc` and `raw.qemu`. Version 7.2.0 patches the issue.

### CVE-2026-48750

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-21T15:16:40.390 |

Incus is a system container and virtual machine manager. Prior to version 7.2.0, the `record-output` parameter of the `/instances/$name/exec` endpoint stores the output of the command in the `exec-output` directory of the instance. If `exec-output` is a symlink, file named `exec_UUID.stdout` and `exec_UUID.stderr` can be written to an arbitrary location where the `.stdout` file will contain arbitrary content. This behavior can be abused for arbitrary command execution. Version 7.2.0 contains a patch.

### CVE-2026-48749

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-21T15:16:40.247 |

Incus is a system container and virtual machine manager. Prior to version 7.2.0, a specially crafted image can be used to read or create/write arbitrary files on the host; possibly leading to arbitrary command execution. Version 7.2.0 fixes the issue.

### CVE-2026-78003

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-22T09:16:53.543 |

The Mailgun for WordPress plugin for WordPress is vulnerable to Server-Side Request Forgery (SSRF) via path traversal in versions up to and including 2.2.0. This is due to insufficient input validation in the add_list() function, which accepts user-controlled array keys from $_POST['addresses'], passes them through sanitize_text_field(). This makes it possible for unauthenticated attackers to make authenticated POST requests to any Mailgun API endpoint using the WordPress site's API key, including creating inbound email-forwarding routes that can intercept password reset emails, leading to administrator account takeover.

### CVE-2026-76904

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-21T21:17:06.143 |

GeoTools is an open source Java library that provides tools for geospatial data. Starting in version 30.5 and prior to versions 33.6, 34.5, and 33.6, an SQL Injection Vulnerability is present when executing OGC Filters with PostGIS DataStore implementation: `jsonArrayContains` function; Requires PostGIS 12 or greater with a String or JSON field. For PostGIS 12 and greater `jsonArrayContains(<column>, <pointer>, <value>)` function writes `<value>` into generated SQL without escaping. Patches are available in versions 33.6, 34.5, and 33.6. No known workaround is available. To limit scope of SQL Injection the PostGIS connection pool should be configured with limited rights.

### CVE-2026-77810

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-21T20:16:45.530 |

In the Neptune connector, a user with access to Neptune through Athena Federated Query could gain access to properties in the Lambda supplying the compute for the connector. To remediate this issue, users should upgrade to aws-athena-query-federation v2026.30.1 or later.

### CVE-2026-77812

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-311` |
| Published | 2026-08-21T15:16:47.557 |

DJI drones transmit DUML (DJI Universal Markup Language) protocol messages over BLE (Bluetooth Low Energy) without encryption. When a client attempts to connect to the drone over Wi-Fi, or when the drone is switched to QuickTransfer mode, the DJI Fly application exchanges DUML messages with the drone over BLE, including the Wi-Fi credentials. An attacker within BLE range can passively sniff this traffic and recover the credentials in cleartext, including the drone's Wi-Fi PSK, SSID, and trusted identifier UUID. Obtaining these credentials allows the attacker to join the drone's internal Wi-Fi network, interact with network services exposed by the drone, and decrypt Wi-Fi traffic exchanged between the drone and the legitimate user.

* An attacker within BLE range recovers the Wi-Fi SSID and PSK in cleartext, and can then join the drone's network 
* The same capture also exposes the session UUID identifier, which is the only thing the drone uses to tell a trusted client from an unknown one, so the attacker can replay it and skip the physical confirmation of new connected devices.
* The credentials do not change between sessions unless the operator manually resets the Wi-Fi settings, so one capture stays valid indefinitely
* The attack is fully passive, with nothing transmitted and no connection made, so neither the operator nor the drone has any indication the session was observed
* A BLE sniffer and presence during one normal DJI Fly connection are needed

Affected models are DJI Neo until 01.00.0400, DJI Neo 2 until 01.00.0500, DJI Flip until 01.00.1200, DJI Air 3 until 01.00.1600, DJI Air 3S until 01.00.1400, DJI Avata 2 until 01.00.0400, DJI Avata 360 until 01.00.0300, DJI Mavic 3 until 01.00.1400, DJI Mavic 3 Classic until 01.00.0800, DJI Mavic 3 Pro until 01.01.0700, DJI Mavic 4 Pro until 01.00.0500, DJI Mini 2 until 01.07.0200, DJI Mini 3 until 01.00.0500, DJI Mini 3 Pro until 01.00.0900, DJI Mini 4 Pro until 01.00.1100, and DJI Mini 5 Pro until 01.00.0600.

Remediation requires a firmware update from the vendor. There is no user-side mitigation that fully addresses the vulnerability without upgrading.

### CVE-2026-77087

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-21T15:16:47.290 |

Paperclip before 0.3.1 in default local_trusted mode fails to validate Host headers, allowing attackers to execute arbitrary commands via DNS rebinding. An attacker can craft a malicious webpage that, when visited by a developer running Paperclip locally, uses DNS rebinding to make authenticated API requests and execute commands through the process adapter.

### CVE-2026-77946

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-22T11:16:54.447 |

A vulnerability was determined in TRENDnet TEW-821DAP 2.2.01b05. Affected by this vulnerability is the function uci_safe_get of the file /cgi-bin/apply_time.cgi of the component NTP Timezone Configuration Handler. Executing a manipulation of the argument system.ntp.server/system.ntp.enable_server/cameo.time.time_zone/cameo.cameo.syslog_server can lead to stack-based buffer overflow. The attack may be launched remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-12710

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-22T09:16:53.340 |

A Missing Authorization vulnerability in the QueryEngineTask of Google Cloud Application Integration (versions from 2025-04-28 to 2026-04-04) allows an external attacker to access sensitive internal data.




The issue was patched on April 4, 2026; no customer action is required.

### CVE-2026-77415

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-21T21:17:07.553 |

JSONata is a JSON query and transformation language. Prior to 1.8.8 and 2.2.1, crafted JSONata expressions could chain several object-integrity weaknesses to execute arbitrary code. The chain could overwrite $clone to mutate objects through evaluateTransformExpression, expose and deconstruct JSONata functions or lambdas through $merge.*, replace proc.arguments.forEach used by applyProcedure, and forge internal lambda state. These primitives allowed an attacker to reach prototype getters, prototype and constructor access, and process.getBuiltinModule with child_process, executing code with the privileges of the host process. This issue is fixed in versions 1.8.8 and 2.2.1.

### CVE-2026-77414

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-21T21:17:07.410 |

JSONata is a JSON query and transformation language. Prior to 1.8.8 and 2.2.1, the src/jsonata.js environment.lookup function used a bypassable hasOwnProperty check. Crafted expressions could use $hasOwnProperty, $spread, $string, prototype access, and $constructor to reach the object prototype and invoke process.getBuiltinModule with child_process, executing arbitrary code with the privileges of the host process. This issue is fixed in versions 1.8.8 and 2.2.1.

### CVE-2026-77413

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-21T21:17:07.267 |

JSONata is a JSON query and transformation language. Prior to 1.8.8 and 2.2.0, the src/functions.js lookup function lacked an Object.prototype.hasOwnProperty check and allowed crafted expressions to access inherited prototype members. An attacker able to supply an expression could use inherited prototype setters and getters, constructor access, valueOf, and process.getBuiltinModule to reach the child_process module and execute arbitrary code with the privileges of the host process. This issue is fixed in versions 1.8.8 and 2.2.0.

### CVE-2026-77234

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-21T18:16:51.507 |

Improper input validation in FreeRTOS-Kernel before 11.3.1 might allow an unprivileged task on MPU-enabled ports to execute code in privileged kernel context. To remediate this issue, users should upgrade to version 11.3.1 or later.

### CVE-2026-59989

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-08-21T21:17:00.713 |

Phalcon is a high-performance, full-stack PHP framework. In 5.15.0 and earlier, resolveFilter in phalcon/Mvc/View/Engine/Volt/Compiler.zep builds the join filter by inserting the raw separator and array token values into generated PHP without passing them through expression(). An attacker who can influence Volt template source can place quote-breaking content in a join argument, inject PHP into the compiled cache file, and execute it when Phalcon\Mvc\View\Engine\Volt::render() loads the template. This issue is fixed in version 5.16.0.

### CVE-2026-39909

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-21T17:16:30.810 |

llama.cpp before b8585 contains a use-after-free vulnerability in the RPC server's GRAPH_RECOMPUTE handler that allows unauthenticated remote attackers to achieve arbitrary read and write access by storing a computation graph, freeing referenced buffers, and reclaiming freed memory with attacker-controlled content. Attackers can send RPC requests to trigger re-execution of stored graphs with dangling pointers, enabling full remote code execution without requiring authentication or user interaction.

### CVE-2026-75932

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-21T16:18:17.717 |

Jet Admin allows an attacker to create a malicious app and connect it to a target user's custom domain, edit the authentication configuration, and reroute traffic to the attacker-controlled app. Once connected to the target domain, the attacker's workspace is populated with the victim's OAuth Client ID and Client Secret if the victim is using an OAuth provider.

### CVE-2026-49849

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-21T22:16:38.300 |

xShop is an open-source shop developed in Laravel. An Unrestricted File Upload vulnerability in xShop version 3.0.3 allows an authenticated administrator to upload executable files (e.g., .php). By uploading a specially crafted php file, an attacker can achieve Remote Code Execution (RCE) on the server, leading to a full system compromise. Version 3.0.4 fixes the issue.

### CVE-2026-62674

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-21T18:16:49.460 |

Omnigent is an open-source AI agent framework and meta-harness for orchestrating coding agents. Prior to 0.3.0, PUT /sessions/{session_id}/agent checks LEVEL_EDIT permission for a session but does not reject a bound shared or template agent whose agent.session_id is None. An authenticated user with edit access to a session can replace that shared agent bundle through omnigent/server/routes/sessions.py, add a stdio MCP server, and cause later sessions that use the shared agent to launch an attacker-controlled command through omnigent/tools/mcp.py. The command executes with the Omnigent runner process permissions and can expose files, credentials, workspace data, internal services, and runner availability. This issue is fixed in version 0.3.0.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-19883

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-22T03:16:20.833 |

The WPeMatico RSS Feed Fetcher plugin for WordPress is vulnerable to unauthorized modification of data that can lead to privilege escalation due to a missing capability check on the wpematico_import_settings function in all versions up to, and including, 2.8.24. This makes it possible for authenticated attackers, with subscriber-level access and above, to update arbitrary options on the WordPress site. This can be leveraged to update the default role for registration to administrator and enable user registration for attackers to gain administrative user access.

### CVE-2026-48050

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-306;CWE-400` |
| Published | 2026-08-21T23:16:25.070 |

Arc is an open, SQL-native time-series database for telemetry. Versions prior to 26.06.1 register Go's `net/http/pprof` handlers at `/debug/pprof/*` via `app.Use(pprof.New())` in `internal/api/server.go`, and `/debug/pprof` is added to `PublicPrefixes` in `cmd/arc/main.go`. The auth middleware short-circuits before the token check on prefix match, so the endpoints are reachable without any authentication. Version 26.06.1 contains a patch. Some workarounds are available. Block `/debug/pprof*` at a reverse proxy / load balancer in front of Arc, restrict Arc's API port to known-trusted networks via firewall rules, and/or patch the running build: comment out `app.Use(pprof.New())` in `internal/api/server.go` and rebuild.

### CVE-2026-53528

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-21T22:16:39.290 |

LeafWiki is a self-hosted wiki. Versions 0.3.0 through 0.10.0 have a path traversal vulnerability in LeafWiki’s asset rename functionality. An authenticated user with editor permissions could move files that are accessible to the LeafWiki server process into a page’s asset directory. This could allow sensitive local files, such as the application database, to become downloadable as page assets. Users should update to version 0.10.1 or greater. As an additional mitigation, operators should ensure that the LeafWiki process runs with the least privileges necessary and does not have filesystem access to sensitive files outside the application’s required directories. Until a patch is applied, operators may reduce risk by restricting editor access to trusted users only and by limiting the filesystem permissions of the LeafWiki process.

### CVE-2026-53527

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-21T22:16:39.147 |

LeafWiki is a self-hosted wiki. Versions 0.1.0 through 0.10.0 have a privilege escalation vulnerability in the user update API. An authenticated user could update their own account role and escalate privileges from a regular user, such as `viewer`, to `admin`. Exploitation requires a valid authenticated LeafWiki user account. Instances without public registration and with only trusted users are at lower practical risk. Users should update to version 0.10.1 or greater. Until a patch is available, operators should restrict account creation and ensure that only trusted users have accounts on affected LeafWiki instances. If possible, access to the user update API should be restricted to trusted users or administrators only.

### CVE-2026-33240

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T22:16:36.863 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, there was a Reflected Cross-Site Scripting (XSS) vulnerability in the foreign key search criteria API. This issue has been fixed in version 3.2.3.

### CVE-2026-31936

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-21T22:16:36.553 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, users can access to unauthorized object information through the search operation. This issue has been fixed in version 3.2.3.

### CVE-2026-62316

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-346` |
| Published | 2026-08-21T21:17:01.350 |

Microsoft UFO open-source framework for intelligent automation across devices and platforms. Prior to 3.0.8, ufo/client/mcp/http_servers/linux_mcp_server.py binds a FastMCP streamable HTTP server to localhost:8010 but does not validate the Host, Origin, or Sec-Fetch-Site headers. An attacker-controlled web page can use DNS rebinding to reach the local /mcp endpoint, enumerate tool schemas through tools/list, and invoke execute_command with a valid UFO_MCP_API_KEY to read files or execute allowed operating system commands as the victim's user. This issue is fixed in version 3.0.8.

### CVE-2026-50538

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-08-21T21:16:59.807 |

LibVNCClient is a library for easy implementation of a VNC client. In versions 0.9.12 through 0.9.15, a malicious (or man-in-the-middle) VNC server can force a connecting `libvncclient` to write attacker-controlled data past the end of its framebuffer. This is an out-of-bounds heap write with attacker-controlled length, contents, and offset. It needs no authentication (the attacker
is the server), works in a default build with default settings, and fires from a single `FramebufferUpdate` the moment the victim connects. It crashes any client unconditionally (denial of service); we also demonstrated it overwriting an application callback pointer and redirecting execution to attacker-chosen code (code execution) under the default configuration. Commit 540332be3e0acc566fa64da6f1b4680c72c724dd patches the issue.

### CVE-2026-62677

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-21T18:16:49.887 |

Omnigent is an open-source AI agent framework and meta-harness for orchestrating coding agents. Prior to 0.3.0, an authenticated user can upload a session-scoped agent bundle with an absolute or traversal-containing os_env.cwd value because omnigent/spec/parser.py stores the value verbatim and omnigent/spec/validator.py does not constrain it. On a runner where OMNIGENT_RUNNER_WORKSPACE is unset, omnigent/runner/resource_registry.py preserves the attacker-controlled path and omnigent/inner/os_env.py uses the resolved path as the environment root and copytree source. The _assert_within_cwd check then treats that attacker-selected root as trusted, allowing sys_os_read, write, edit, and shell tools to access runner files and environment secrets outside the intended workspace. This issue is fixed in version 0.3.0.

### CVE-2026-62675

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-21T18:16:49.603 |

Omnigent is an open-source AI agent framework and meta-harness for orchestrating coding agents. Prior to 0.3.0, multipart POST /v1/sessions accepts an authenticated user's agent bundle and omnigent/server/bundles.py validate_agent_bundle does not reject a tools..callable dotted Python path. omnigent/runner/tool_dispatch.py _resolve_spec_callable imports the specified module and _execute_spec_callable_tool invokes the resolved function, allowing a bundle to select subprocess.check_output and execute a local command with the runner process permissions. This can expose runner files, environment variables, credentials, workspace data, internal services, and availability without administrator access. This issue is fixed in version 0.3.0.

### CVE-2026-71513

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-22T14:16:33.417 |

NLTK before 3.10.3 contains a remote code execution vulnerability in AllowlistUnpickler that validates only the pickle module string and not the global name, allowing attackers to resolve dotted names by attribute traversal to callables outside the allowlisted namespace. Attackers can craft untrusted transition-parser models that execute arbitrary commands when TransitionParser.parse loads the model through allowlisted_pickle_load.

### CVE-2026-62243

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-08-22T13:16:39.687 |

Netty (io.netty:netty-handler) versions from 4.2.0.Final through 4.2.16.Final and versions through 4.1.136.Final disable TLS hostname verification on the SslProvider.OPENSSL client path when a plain (non-extended) X509TrustManager is used and Unsafe-based trust-manager wrapping is unavailable (Java 25+). In this configuration the OpenSSL client does not perform hostname verification, allowing a man-in-the-middle attacker to present a certificate issued for a different hostname that is accepted without validation. Fixed in 4.2.17.Final and 4.1.137.Final.

### CVE-2026-59808

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-22T13:16:38.977 |

AVideo through commit 9c39d8c8 contains an authentication bypass vulnerability where deduplicateByEncoderQueueId() returns video_id_hash credentials for any video by encoder_queue_id without ownership verification, and useVideoHashOrLogin() converts this hash into passwordless login as the video owner. Attackers with upload permission can retrieve an administrator's video_id_hash by omitting the videos_id parameter, then use that hash in an unauthenticated request to gain administrative session access and modify system configuration.

### CVE-2026-59256

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-22T13:16:38.817 |

WWBN AVideo through commit 9c39d8c8 contains an authorization bypass vulnerability where getToken() creates tokens without binding to user identity or purpose, and plugin/Gallery/view/sections.php issues valid tokens to unauthenticated visitors. Attackers can retrieve a token from the Gallery endpoint and use it to bypass authorization checks in other subsystems like view/hls.php to access restricted video content.

### CVE-2026-53530

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248;CWE-400;CWE-1285` |
| Published | 2026-08-21T22:16:39.590 |

RaTeX is a KaTeX-compatible math rendering engine written in Rust. Prior to version 0.1.11, the public parser entrypoint `ratex_parser::parse(&str)` panics on the 9-byte input `\verbéxé` (i.e. `\verb` followed by the non-ASCII delimiter `é`). When handling a `\verb` command, the parser slices the verbatim argument with byte indices (`arg[1..arg.len() - 1]`); if the delimiter character is multibyte UTF-8, index `1` lands inside that character and Rust panics with *“byte index 1 is not a char boundary”*. Because RaTeX’s release profile sets `panic = "abort"` (`Cargo.toml:48`), the panic aborts the entire process — not just the current request/thread — making this a hard denial of service for any service that renders untrusted LaTeX. Version 0.1.11 fixes the issue.

### CVE-2026-77354

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-789` |
| Published | 2026-08-21T21:17:07.130 |

kin-openapi is a Go project for handling OpenAPI files. From 0.124.0 until 0.142.0, openapi3filter.sliceMapToSlice in openapi3filter/req_resp_decoder.go converts attacker-controlled sparse indexes from a deepObject query parameter into a dense slice by allocating entries from zero through the largest supplied index, after which buildResObj creates another slice of the same length. This allocation occurs before schema validation, so maxItems does not prevent it. An unauthenticated client can send a small query such as param[items][50000000]=x to an endpoint whose deepObject schema contains an array, forcing multi-gigabyte heap allocation and causing an OOM kill or restart loop. Other request-body encodings and styled parameters that do not produce bracketed integer indexes are not affected. This issue is fixed in version 0.142.0.

### CVE-2026-67359

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-21T20:16:39.583 |

Joomla Extension - j2commerce.com - Order content disclosure J2Store 1.0.0-3.3.20, 4.0.0-4.0.20, 4.1.0-4.1.5 - An unauthenticated visitor could supply any order_id as a query parameter to render the full checkout confirmation page for that order, including line items, prices, and totals.

### CVE-2026-50288

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-21T20:16:36.067 |

SpecifyJS is a declarative TypeScript user interface framework. Prior to version 0.2.136, when `new URL()` throws a parse error, the `assertSecureUrl` function returned without throwing, silently allowing the request to proceed without HTTPS validation. Starting in version 0.2.136, the catch block now throws an error instead of silently returning.

### CVE-2026-77815

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-21T15:16:47.883 |

to_abs_path in scripts/iib/tool.py normalised the requested path with os.path.normpath, which collapses dot segments but does not resolve symbolic links. A symlink placed inside a scanned directory therefore satisfies the containment comparison performed by is_path_trusted in scripts/iib/api.py while pointing outside that directory, and FileResponse follows the link when serving the response, so a link created in an image directory and targeting a file such as /etc/passwd discloses that file. Whether the check applies depends on get_enable_access_control in scripts/iib/tool.py: it returns true when IIB_ACCESS_CONTROL is set to enable, false when set to disable, and otherwise true when the host Stable Diffusion WebUI was started with share, ngrok, listen or server_name, falling back to false. Confinement is therefore active in the network-exposed WebUI deployments that rely on it, while a standalone run with no such option serves every readable file regardless of this flaw. The fix resolves the path with os.path.realpath.

### CVE-2026-77814

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-21T15:16:47.733 |

is_path_trusted in scripts/iib/api.py compares the requested path against each allowed parent directory with path.startswith(parent_path), without appending a path separator. A directory whose name merely begins with an allowed path therefore satisfies the comparison, so where /data/images is allowed a request for /data/images_private/secret.txt is treated as trusted and served by FileResponse, disclosing files the confinement was meant to exclude. Whether the check applies depends on get_enable_access_control in scripts/iib/tool.py: it returns true when IIB_ACCESS_CONTROL is set to enable, false when set to disable, and otherwise true when the host Stable Diffusion WebUI was started with share, ngrok, listen or server_name, falling back to false. Confinement is therefore active in the network-exposed WebUI deployments that rely on it, while a standalone run with no such option serves every readable file regardless of this flaw. The fix compares against parent_path joined with os.sep.

### CVE-2026-66917

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-22T12:16:25.680 |

Joomla Extension - joomgalleryfriends.net - Stored XSS in JoomGallery < 4.4.0 - An authenticated, privileged can store an XSS payload in any image causing JS execution in every visitor's browser.

### CVE-2026-34741

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-21T22:16:37.143 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, authentication bypass allows unauthenticated remote attackers to execute arbitrary PHP files from the env-production directory on a new iTop instance in the production environment. This issue has been fixed in version 3.2.3.

### CVE-2026-74252

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T20:16:41.000 |

Joomla Extension - j2commerce.com - Stored XSS in Guest checkout in J2Store 1.0.0-3.3.20, 4.0.0-4.0.20, 4.1.0-4.1.5 - J2Commerce 4.1.5 is vulnerable to Stored Cross-Site Scripting (XSS) through the guest checkout billing address fields. An unauthenticated attacker exploits a filter bypass in Joomla's Input::getArray() combined with PHP's variables_order=EGPCS (Cookie overrides POST in $_REQUEST ) to store unsanitized HTML in fields such as billing_first_name.

### CVE-2026-57998

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-22T13:16:38.263 |

better-npm-audit through 3.11.0, and the 4.0.0-rc.2 prerelease, builds its npm audit command by interpolating the user-supplied --registry option into a command string in src/handlers/handleInput.ts without validation or quoting, then passes that string to child_process.exec() in index.ts, which spawns a shell. A registry value containing shell metacharacters such as a semicolon, pipe, or command substitution executes arbitrary operating system commands with the privileges of the process running the audit.

### CVE-2026-41451

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-21T18:16:48.400 |

UAC (Unix-like Artifacts Collector) versions prior to 3.3.0 contain a command injection vulnerability in the user substitution logic within parse_artifact.sh where usernames and home directories from /etc/passwd are substituted directly into command strings without escaping before execution via eval. Attackers can inject shell metacharacters such as command substitution syntax or semicolons through crafted usernames or home directory paths in /etc/passwd entries to execute arbitrary commands on the analyst's host system.

### CVE-2026-41450

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-21T18:16:48.257 |

UAC (Unix-like Artifacts Collector) versions prior to 3.3.0 contain a command injection vulnerability in the _command_collector function where foreach command output lines are substituted directly into command strings via sed without proper escaping before being evaluated with eval. Attackers can exploit this by crafting malicious filenames or artifact definitions containing shell metacharacters such as command substitution syntax or semicolons to execute arbitrary commands on the analyst's host system.

### CVE-2026-41449

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-21T18:16:48.103 |

UAC (Unix-like Artifacts Collector) versions prior to 3.3.0 contain a command injection vulnerability in the _run_command function that allows attackers to execute arbitrary commands by injecting shell metacharacters into untrusted data such as usernames, process names, or filenames. Attackers can exploit this vulnerability through crafted evidence inputs, mounted images with hostile filenames, or tampered artifact definitions to achieve remote code execution on the analyst's host when processing evidence.

### CVE-2026-17250

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-21T18:16:47.450 |

A
stack-based buffer overflow vulnerability exists in the firmware update
functionality of TL-MR6400 v7 due to unsafe processing of
attacker-controlled metadata within a firmware image. 





Successful
exploitation may allow an authenticated attacker to trigger memory corruption
and execute arbitrary code on the affected device.

### CVE-2026-75933

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T16:18:17.873 |

Jet Admin allows an authenticated attacker to inject JavaScript via the sign-in page's scripts and styles option. Injected script is executed in the context of any visiting user's domain.

### CVE-2026-60084

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-22T13:16:39.407 |

SiYuan versions before v3.7.4 contain an arbitrary file deletion vulnerability in the /api/search/removeTemplate endpoint that accepts an unvalidated path parameter passed directly to os.RemoveAll. Authenticated admin attackers can supply absolute filesystem paths to recursively delete any file or directory the kernel process has permission to remove, anywhere on the host filesystem.

### CVE-2026-48106

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-345;CWE-924` |
| Published | 2026-08-21T23:16:25.360 |

Arc is an open, SQL-native time-series database for telemetry. Prior to version 26.06.1, Arc Enterprise's cluster replication receiver at `internal/cluster/replication/receiver.go` validates only the wire-format envelope (length, opcode) of inbound messages. The `MsgReplicateSync` payload itself is accepted without any application-layer authentication — no HMAC, no signature, no per-message nonce. The replication stream is protected at the transport layer by TLS / mTLS, but there is no protection against application-layer message tampering or replay once a peer is on the cluster network. This is fixed in 2026.06.1. Some workarounds are available. Restrict cluster network access to known-trusted peers via strict firewall rules, audit replication logs for unexpected `MsgReplicateSync` traffic, and/or disable cluster mode until the fix is available.

### CVE-2026-48105

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-345;CWE-913` |
| Published | 2026-08-21T23:16:25.220 |

Arc is an open, SQL-native time-series database for telemetry. Prior to version 26.06.1, Arc Enterprise's Raft FSM (`internal/cluster/raft/fsm.go:applyRegisterFile`) accepts attacker-chosen file paths in manifest-registration proposals without validating them against the configured storage backend. The only check is that the path is non-empty. There is no parent-traversal (`..`) rejection, no allowlist of legitimate prefixes, no scheme restriction (`s3://` vs local), and no length bound. This is fixed in 2026.06.1. Some workarounds are available. Restrict cluster network access to known-trusted peers via strict firewall rules, audit the cluster manifest for unexpected paths (any path not matching the configured storage backend root is suspect), and/or disable cluster mode until the fix is available.

### CVE-2026-77236

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-21T18:16:51.800 |

Missing minimum size validation in secure context allocation in FreeRTOS-Kernel before 11.3.1 might allow local users to corrupt secure-world heap metadata via an out-of-bounds write with an undersized stack size parameter. To remediate this issue, users should upgrade to version 11.3.1 or later.

### CVE-2026-77235

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-21T18:16:51.657 |

Missing privilege verification in the secure context cleanup handler in FreeRTOS-Kernel before 11.3.1 might allow local users to cause a use-after-free condition in secure-world memory via the SVC handler for secure context deallocation. To remediate this issue, users should upgrade to version 11.3.1 or later.

### CVE-2026-22681

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-21T16:17:16.767 |

OpenViking before 0.3.4 contains a server-side request forgery vulnerability that allows authenticated low-privilege attackers to access internal network services by submitting arbitrary URLs to the resources API endpoint. Attackers can POST a crafted URL to /api/v1/resources, causing the server to issue outbound HEAD and GET requests with redirects enabled to loopback, RFC 1918, link-local, or cloud metadata addresses, then read back responses through normal content APIs to enumerate and interact with internal services.

### CVE-2026-63135

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T21:17:01.493 |

YOURLS is a self-hosted, customizable URL shortener written in PHP. From 1.5.1 until 1.10.4, YOURLS stores the HTTP Referer header through yourls_get_referrer(), yourls_sanitize_url_safe(), and yourls_log_redirect(), then aggregates the value in yourls-infos.php and passes the derived domain through yourls_get_domain(), yourls_stats_pie(), and yourls_google_array_to_data_table(). The chart builder concatenates labels into inline JavaScript without JavaScript-string escaping, so an unauthenticated attacker can poison the statistics of an existing short URL with a crafted referrer. When an administrator or public stats-page viewer opens the affected statistics page, attacker-controlled JavaScript executes in the YOURLS origin and can access admin-visible data, the API signature token, and privileged same-origin actions. This issue is fixed in version 1.10.4.

### CVE-2026-61824

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-08-21T21:17:01.017 |

Defuddle cleans up HTML pages. Prior to 0.19.1, site extractors interpolate page-derived image alt and src values, og:image values, and video descriptions into HTML strings without context-appropriate escaping, and buildExtractorResponse() returns this contentHtml without the main pipeline's DOM-based sanitization. The affected paths include src/extractors/x-article.ts, src/extractors/substack.ts, and src/extractors/youtube.ts. A malicious page or attacker-controlled content on a matching domain can inject event-handler attributes or javascript URLs that execute when a victim or downstream application renders the extracted HTML. This issue is fixed in version 0.19.1.

### CVE-2026-76876

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-21T20:16:44.680 |

Craftplan before 0.5.1 contains a broken access control vulnerability that allows unauthenticated attackers to read sensitive credentials by exploiting an unconditional authorization policy on the Settings resource. Attackers can send a GET request to the settings API endpoint with a valid record ID to retrieve decrypted SMTP passwords, email API keys, and email API secrets due to the read policy using an always-allow authorization check that bypasses all identity verification.

### CVE-2026-54682

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T19:17:03.610 |

DiscordChatExporter saves Discord chat logs to a file. Prior to 2.47.2, HTML exports generated with markdown formatting disabled pass attacker-controlled content through FormatMarkdownAsync and FormatEmbedMarkdownAsync in DiscordChatExporter.Core/Exporting/MessageGroupTemplate.cshtml and render it without HTML entity encoding. The affected fields include message.Content, message.ForwardedMessage.Content, message.ReferencedMessage.Content, embed.Title, embed.Description, field.Name, and field.Value. A Discord webhook or bot can store a script payload in these fields, and the payload executes when a user exports the channel with markdown formatting disabled and opens the resulting HTML, allowing the script to read the export or alter its displayed content. This issue is fixed in version 2.47.2.

### CVE-2026-77237

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-843` |
| Published | 2026-08-21T18:16:51.950 |

Missing queue-set type validation in xQueueAddToSet() in the FreeRTOS-Kernel before 11.3.1 might allow an unprivileged task on MPU-enabled ports with configUSE_QUEUE_SETS=1 to read privileged kernel memory. To remediate this issue, users should upgrade to version 11.3.1 or later.

### CVE-2026-64679

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-08-21T21:17:01.920 |

Atlantis is a self-hosted golang application that listens for Terraform pull request events via webhooks. From 0.19.8 until 0.45.0, Atlantis does not consistently validate user-controlled workspace values supplied through accepted repository-level atlantis.yaml configuration or authenticated /api/plan input before joining them into local workspace paths. Traversal segments can escape the intended per-pull workspace directory and cause clone preparation or other working-directory code paths to call os.RemoveAll, os.MkdirAll, or related filesystem operations on out-of-bounds directories before Terraform rejects the invalid workspace name. This can create, delete, or reuse writable paths with the privileges of the Atlantis process, causing integrity loss or denial of service. This issue is fixed in version 0.45.0.

### CVE-2026-31880

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T21:16:57.403 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, there is a Reflected Cross-Site Scripting (XSS) vulnerability in the universal search. This issue has been fixed in version 3.2.3.

### CVE-2026-31803

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T21:16:57.250 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, 3.2.3, there is a Reflected Cross-Site Scripting (XSS) vulnerability in pages/tagadmin.php. This issue has been fixed in version 3.2.3.

### CVE-2026-30890

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T21:16:57.103 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, there is a Reflected Cross-Site Scripting (XSS) vulnerability in the synchro import script. This issue has been fixed in version 3.2.3.

### CVE-2026-30826

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T21:16:56.830 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, there is a Reflected Cross-Site Scripting (XSS) vulnerability in the testing OQL query functionality. This issue has been fixed in version 3.2.3.

### CVE-2026-49360

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:L/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-21T23:16:25.617 |

Recce is a data-validation toolkit for enhanced dbt (data build tool) PR review. Prior to version 1.50.0, OSS server deployments that expose the server to an untrusted network without authentication are vulnerable to unauthenticated SQL execution through the query run API. When Recce is configured with a DuckDB-backed project, an attacker can use DuckDB filesystem primitives to read and write files accessible to the Recce server process. The impact depends on how Recce is deployed, but may include disclosure of local files, tampering with Recce/dbt artifacts, modification of browser-served static files leading to stored XSS, and modification of application files if those paths are writable. If Recce is run as root, file access occurs with root privileges inside that host or container. This issue has been patched in Recce `v1.50.0`. Users should upgrade to Recce `v1.50.0` or later. The patch restricts unsafe file read/write behavior for DuckDB-backed query execution and hardens the affected query path. Other warehouse adapters have also been reviewed for similar exposure. Users who cannot upgrade immediately should avoid exposing `recce server` to the public internet or any untrusted network. Recommended mitigations include enabling authentication or placing Recce behind an authenticated reverse proxy/VPN, running Recce as a non-root user, using a read-only application filesystem where possible, and ensuring that sensitive files or credentials are not available to the Recce process.

### CVE-2026-68508

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-470` |
| Published | 2026-08-21T21:17:02.963 |

Hydra is a framework for elegantly configuring complex applications. Prior to 1.3.4, hydra.utils.instantiate() resolves and calls Python objects selected by configuration through _resolve_target() in hydra/_internal/instantiate/_instantiate2.py, allowing attacker-controlled target values and arguments to choose dangerous callables. A consuming application, library, CLI workflow, or model loader that passes untrusted configuration, CLI overrides, or model metadata into hydra.utils.instantiate() can therefore execute arbitrary code in its own process, including reading or modifying files and credentials or terminating the process. Version 1.3.4 adds target blocking with an explicit HYDRA_INSTANTIATE_ALLOWLIST_OVERRIDE escape hatch. This issue is fixed in version 1.3.4.

### CVE-2026-54071

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-21T19:17:02.720 |

BabelDOC is a document translation tool. Prior to 0.6.3, BabelDOC's vendored PDF parser in babeldoc/pdfminer/cmapdb.py deserializes untrusted pickle data when CMapDB._load_data() loads CMap files. PDF-controlled Encoding or CMapName values and embedded PostScript usecmap operators can reach this sink after path separators are decoded, while _normalize_cmap_name() removes only a leading slash. Absolute paths or traversal sequences can escape the trusted CMap directories through os.path.join(), select an attacker-writable .pickle.gz file, and cause pickle.loads() to execute arbitrary Python code with the privileges of the BabelDOC process. This issue is fixed in version 0.6.3.

### CVE-2026-34948

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-21T23:16:24.153 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, only classes present in the SELECT clause are protected by the silos access check in OQL. This issue has been fixed in version 3.2.3.

### CVE-2026-54457

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-552;CWE-918` |
| Published | 2026-08-21T21:17:00.267 |

TensorZero is an open-source LLMOps platform that unifies an LLM gateway, observability, evaluation, optimization, and experimentation. Prior to 2026.6.0, the TensorZero Gateway /internal/object_storage endpoint accepts a caller-supplied JSON storage_path parameter that dynamically overrides the [object_storage] configuration. Selecting the filesystem storage type allows arbitrary files on the gateway filesystem to be read, including credential files. Selecting the s3_compatible storage type causes outbound object-storage requests to attacker-chosen internal or cloud-metadata endpoints. Exploitation requires access to the gateway, which can be authenticated or unauthenticated depending on deployment configuration. This issue is fixed in version 2026.6.0.

### CVE-2026-55622

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-21T15:16:42.003 |

Incus is a system container and virtual machine manager. Prior to version 7.2.0, missing authorization checks exist for instance copying where an attacker knowing the name of a project that they don't have access to and the name of an instance in that project can copy the instance to a new project. This issue could allow an attacker to access secrets in instances they are not authorized to access. Version 7.2.0 patches the issue.

### CVE-2026-55621

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-21T15:16:41.863 |

Incus is a system container and virtual machine manager. Prior to version 7.2.0, missing authorization checks exist for custom volume copying where an attacker knowing the name of a project that they don't have access to and the name of a custom volume in that project can copy the custom volume to a new project. This issue could allow an attacker to access secrets in custom volumes they are not authorized to access. Version 7.2.0 patches the issue.

### CVE-2026-2996

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-22T14:16:32.807 |

The Advanced Product Fields (Product Addons) for WooCommerce plugin for WordPress is vulnerable to Improper Input Validation in all versions up to, and including, 1.6.21. This is due to a logic flaw in the 'validate_cart_data' function. This makes it possible for unauthenticated attackers to bypass required paid addons and complete purchases at the base product price only, effectively stealing products by paying a fraction of the intended total. The vulnerability was partially patched in version 1.6.19.

### CVE-2026-76905

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-21T21:17:06.320 |

kin-openapi is a Go project for handling OpenAPI files. From 0.10.0 until 0.141.0, openapi3filter.convertParseError in openapi3filter/validation_error_encoder.go dereferences e.Parameter.In without checking whether e.Parameter is nil. A malformed non-string scalar field in a multipart/form-data request body produces a nested ParseError with a nil RequestError.Parameter, and applications that render the validation error through openapi3filter.ConvertErrors or ValidationErrorEncoder panic. An unauthenticated client can repeatedly send such requests to deny service when the application lacks a recovery boundary. JSON request bodies and applications that do not use these error-rendering helpers are not affected. This issue is fixed in version 0.141.0.

### CVE-2026-63421

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-480` |
| Published | 2026-08-21T21:17:01.643 |

Keystone is a content management system for Node.js. Prior to 6.5.3, the findMany resolver in packages/core/src/lib/core/queries/resolvers.ts compares the signed take argument directly with graphql.maxTake, allowing a remote unauthenticated GraphQL client to provide a negative take value whose magnitude exceeds the configured bound. The bypass also applies to relationship queries and can return more records than the developer intended, potentially exhausting service resources. This issue is fixed in version 6.5.3.

### CVE-2026-30866

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-306` |
| Published | 2026-08-21T20:16:34.453 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, unauthenticated users can access uploaded sensitive via sniffed url. This issue has been fixed in version 3.2.3.

### CVE-2026-27490

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-330;CWE-331` |
| Published | 2026-08-21T20:16:34.157 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, inline images that are accessible without being authenticated are protected by a weak 24-bit pseudo-random secret. This issue has been fixed in version 3.2.3.

### CVE-2026-27462

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-204` |
| Published | 2026-08-21T20:16:33.870 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, iTop returns different responses for valid/invalid usernames depending on multiple factors in the reset password mechanism, leading to user enumeration. This issue has been fixed in version 3.2.3.

### CVE-2026-63462

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-21T19:17:31.927 |

Unleash is an open-source feature management platform. Prior to 7.5.2, 7.6.5, and 8.0.2, the shared OpenAPI validation error path in src/lib/error/bad-data-error.ts passes a raw request value from lodash.get to JSON.stringify in genericErrorMessage and fromOpenApiValidationErrors without guarding stack exhaustion. An unauthenticated attacker can send a roughly 10 KB JSON value nested thousands of levels deep to POST /edge/validate, POST /edge/issue-token, or another OpenAPI-validated endpoint, causing RangeError: Maximum call stack size exceeded in openAPIValidationMiddleware and terminating the Node process because no uncaughtException handler recovers it. Replaying the request can sustain a complete service outage. This issue is fixed in versions 7.5.2, 7.6.5, and 8.0.2.

### CVE-2026-71862

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-08-21T18:16:50.730 |

Checkmate is an open-source, self-hosted tool designed to track and monitor server hardware, uptime, response times, and incidents in real-time with beautiful visualizations. From 3.3.0 until 3.9.2, enabling the global showURL setting causes the unauthenticated GET /api/v1/status-page/:url endpoint to return complete monitor objects from server/src/controllers/statusPageController.ts. The response includes the secret field used by HttpProvider.ts as an HTTP Authorization credential, even though BaseStatusPage.tsx does not display that value, allowing visitors to extract credentials from the JSON response and use them against monitored services. This issue is fixed in version 3.9.2.

### CVE-2026-55241

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-08-21T18:16:48.790 |

Checkmate is an open-source, self-hosted tool designed to track and monitor server hardware, uptime, response times, and incidents in real-time with beautiful visualizations. Prior to 3.9.1, the public POST /api/v1/auth/register route in server/src/api/routes/authRoutes.ts passes multipart profileImage uploads through in-memory Multer parsing before registration validation, without file-size, file-count, or MIME-type limits in server/src/api/middleware/upload.ts. An unauthenticated attacker can submit concurrent oversized files that are buffered before invalid registration or invite-token checks reject the request, exhausting memory and crashing or destabilizing the backend. This issue is fixed in version 3.9.1.

### CVE-2026-54789

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-08-21T16:17:19.000 |

mod_auth_openidc is an OpenID Certified authentication and authorization module for the Apache 2.x HTTP server that implements the OpenID Connect Relying Party functionality. Prior to 2.4.19.4, an out-of-bounds read and a one-byte out-of-bounds write exist in the state-cookie parser of `mod_auth_openidc`. The issue is fixed in version 2.4.19.4 by stopping the scan at the string terminator so a value-less token is rejected. No in-product workarounds are available. As a stop-gap, an upstream reverse proxy or WAF that rejects or normalizes malformed `Cookie` headers (tokens lacking `=`) can reduce exposure, but upgrading is the recommended remediation.

### CVE-2026-53525

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-208` |
| Published | 2026-08-21T23:16:26.363 |

WeeChat (Wee Enhanced Environment for Chat) is a free chat client. In versions 0.3.1 through 4.9.0, the WeeChat relay authentication uses non-constant-time string comparison functions (weechat_strcasecmp and strcmp) to verify password hashes and plaintext passwords. An attacker can exploit timing differences to extract the server-computed hash character by character, then authenticate using the correct hash without knowing the password. Version 4.9.1 fixes the issue.

### CVE-2026-62960

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-610` |
| Published | 2026-08-21T20:16:38.700 |

Git for Windows is the Windows port of Git. Prior to 2.55.0.windows.4, a malicious remote Git server can advertise a bundle URI that reaches transport_get_remote_bundle_uri(), fetch_bundle_uri_internal(), and copy_uri_to_file() in bundle-uri.c during clone or fetch when transfer.bundleuri=true. Non-HTTP(S) values are treated as local filesystem paths, and file URI prefixes are removed, so a bare UNC path or file URI targeting an attacker-controlled share causes Windows to initiate an outbound SMB connection. This can expose NTLM authentication material to the attacker-selected host. This issue is fixed in version 2.55.0.windows.4.

### CVE-2026-30819

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T20:16:34.313 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, iTop has a reflected Cross-Site Scripting (XSS) vulnerability in its dashboard revert functionality with the parameter dashboard_id in /pages/ajax.render.php. This issue has been fixed in version 3.2.3.

### CVE-2026-53499

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-21T23:16:26.070 |

FORT Validator is a Resource Public Key Infrastructure (RPKI) relying-party validator that produces validated route-origin data. FORT Validator versions through 1.6.7 contain an origin-validation error in their RRDP processing: a delegated CA under the same Trust Anchor Locator (TAL) can reference a victim CA’s public RRDP notification and snapshot URLs, causing FORT’s URL-based download cache to report success after deleting the victim’s local snapshot. Following a routine victim publication, this can silently remove the victim’s VRPs and other signed objects from FORT’s output, potentially enabling route hijacking or loss of reachability. Version 1.6.8 contains a patch that rejects cross-origin RRDP snapshot and delta URLs; as a workaround, administrators can disable HTTP/RRDP with  --http.enabled=false  while keeping rsync enabled, although this can leave data unavailable or stale where rsync is not supported.

### CVE-2026-58003

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-22T13:16:38.673 |

WWBN AVideo through commit 9c39d8c8 contains a cross-site request forgery vulnerability in the releaseVideoNow.json.php endpoint that lacks authenticity checks and accepts GET requests. Attackers can craft a malicious cross-site GET request carrying an administrator's session cookie to permanently publish any embargoed video by manipulating the videos_id parameter.

### CVE-2026-58002

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-22T13:16:38.540 |

WWBN AVideo through commit 9c39d8c8b4c1f75540788d6b391740852ceb0732 contains an authorization bypass vulnerability in the Users_affiliations add.json.php endpoint that allows authenticated users to forge two-party consent records by supplying the counterparty's agreement timestamp. Attackers can create a forged affiliation with status='a' and then reassign video ownership to arbitrary users through the videoAddNew.json.php endpoint, which trusts the forged affiliation as an authorization term.

### CVE-2026-47735

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-200;CWE-918` |
| Published | 2026-08-21T23:16:24.917 |

Arc is an open, SQL-native time-series database for telemetry. Prior to version 26.06.1, Arc's user-SQL validator (`internal/api/query.go:ValidateSQLRequest`) blocked only `read_parquet(` and `arc_partition_agg(` via regex denylist. The broader DuckDB I/O function family — `read_csv_auto`, `read_csv`, `read_json`, `read_json_auto`, `read_text`, `read_blob`, `glob`, `parquet_metadata`, `parquet_schema`, `read_xlsx`, etc. — was not blocked. RBAC table-reference extraction inspected only `FROM`/`JOIN` clauses, so scalar table functions in the `SELECT` list slipped past both layers. This is fixed in 2026.06.1 via a structural sandbox at the DuckDB layer. After lockdown, DuckDB refuses to open any file outside the allowlist and refuses further `INSTALL`/`LOAD`. Already-loaded extensions remain callable. Some workarounds are available. Restrict API access to known-trusted networks via firewall rules or, as a temporary mitigation, add `read_csv*`/`read_json*`/`glob` etc. to `dangerousSQLPattern` in `internal/api/query.go`.

### CVE-2026-77220

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-825` |
| Published | 2026-08-21T21:17:06.737 |

PDFio before 1.6.5 contains a dangling pointer vulnerability in the dictionary string-formatting function that stores a pointer to a stack-local buffer in the document dictionary without copying the string value. In multi-threaded or pooled-request environments, attackers or concurrent users can trigger stack memory reuse across requests, causing cross-tenant document content corruption by silently overwriting one caller's dictionary string values with another caller's data.

### CVE-2026-30865

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T21:16:56.970 |

Combodo iTop is a web based IT service management tool. Prior to 3.2.3, there is a Reflected Cross-Site Scripting (XSS) vulnerability in the dashboard save functionality. This issue has been fixed in version 3.2.3.

### CVE-2026-62676

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-184` |
| Published | 2026-08-21T18:16:49.743 |

Omnigent is an open-source AI agent framework and meta-harness for orchestrating coding agents. Prior to 0.3.0, the shared shell-command parser in omnigent/policies/builtins/_shell.py fails to recognize combined interpreter flags, the timeout, nice, setsid, and stdbuf wrappers, command substitutions, and a single background control operator. A gated git push or gh write hidden with these forms produces no parsed operation, causing the github.py write_repos and write_branches allowlist and the working_dir.py workspace confinement policies to abstain and allow the command. An authenticated or prompt-injected agent can therefore push to an unauthorized repository or branch or escape the intended workspace. This issue is fixed in version 0.3.0.

### CVE-2026-17252

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-21T18:16:47.803 |

A
stack-based out-of-bounds write vulnerability exists in the login request
handling functionality of the administrative web interface of TP-Link TL-MR6400 v7 routers. An unauthenticated adjacent attacker can trigger the vulnerability
by sending a specially crafted malformed HTTP request. 





Successful
exploitation may cause the web service process to crash, resulting in a
denial-of-service condition and temporary loss of access to the router's web
management interface.

### CVE-2026-17251

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-21T18:16:47.660 |

A NULL
pointer dereference vulnerability exists in the HTTP request parsing
functionality of 
TL-MR6400 v7. An unauthenticated remote attacker can
trigger the vulnerability by sending a specially crafted HTTP request
containing a malformed session cookie header. 





Successful
exploitation may cause the HTTP service process to crash, resulting in a
denial-of-service condition and temporary loss of management or CGI
functionality until service recovery.

### CVE-2026-54134

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-21T19:17:03.197 |

OctoPrint provides a web interface for controlling consumer 3D printers. Prior to 1.11.8 and 2.0.0rc3, OctoPrint's custom Tornado upload handler and Flask with Werkzeug parse request parameters differently, allowing an attacker with FILE_UPLOAD permission to inject reserved internal upload fields through query parameters or parser differentials despite the earlier GHSA-m9jh-jf9h-x3h2 fix. The affected endpoints are /api/files/{local|sdcard}, /api/languages, /plugin/backup/restore, and /plugin/pluginmanager/upload_file. An attacker can make OctoPrint treat an arbitrary host file as a temporary upload, move it into a downloadable upload directory, disclose configuration secrets or other readable files, and remove runtime files in a way that can affect a later restart. This issue is fixed in versions 1.11.8 and 2.0.0rc3.
