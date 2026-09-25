# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-25 15:00 UTC
- **対象期間**: `2026-09-24T15:00:37.000Z` 〜 `2026-09-25T15:00:31.000Z`
- **重要CVE数**: 217 件（Critical 9.0+: 27 件 / High 7.0〜: 190 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に報告された CVE のうち、CVSS 7.0 以上の深刻度を持つものは **30 件以上** に上ります。共通する傾向は以下の通りです。

* **リモートからのコード実行 (RCE) が多発** – 特に Web アプリケーションや PaaS、組み込みデバイスの管理インタフェースで、認証不要または認証情報の不適切な扱いに起因する RCE が目立ちます。  
* **LLM / Chat‑ML への入力サニタイズ不備** – LLM を組み込んだツール（例: Decepticon）で、特殊トークンがエスケープされずに実行コードに変換されるケースが初めて報告されました。  
* **Linux カーネル内部の整数アンダーフロー・ゼロチェック不備** が複数報告され、特権昇格や情報漏洩につながります。  
* **サードパーティプラグイン（WordPress、Zimbra 等）** の権限チェック欠如が原因で、認証なしに管理操作や XSS が可能になる脆弱性が多数確認されています。  

このように、**認証・入力検証の欠如** が攻撃者に広範囲な権限取得を許す構造的な問題として顕在化しています。早急なパッチ適用と、入力サニタイズ・最小権限の徹底が求められます。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑61732** (Decepticon) | 10.0 | LLM メッセージに ChatML トークンが無検証で埋め込まれ、攻撃者が任意のプロンプトやコードを実行可能 | **最高スコア** かつ、AI/LLM を利用したツールで初めて報告された「プロンプトインジェクション」系脆弱性。BYOK 環境でも被害が拡大する恐れ。 |
| **CVE‑2026‑93425** (Dokploy) | 9.9 | `patch.readRepoDirectories` がユーザ入力 (`repoPath`) をシェルコマンドに直接渡すため、任意コマンド実行 (RCE) が可能 | PaaS の自動デプロイ機能で **認証不要** にコマンド実行が可能になるため、クラウド環境全体への波及リスクが大きい。 |
| **CVE‑2026‑93643** (OnlyOffice / Zimbra) | 9.8 | 公開ブリーフケース文書の `save` フィールドを悪用し、パストラバーサル＋コマンド実行 (zimbra ユーザ権限) | 文書共有機能という**業務上必須**な機能が直接攻撃対象になる点が危険。 |
| **CVE‑2026‑92609** (Apache Qpid Broker‑J) | 9.8 | セッション固定により、認証後の管理セッションを乗っ取れる | メッセージング基盤で広く利用される **Qpid** が対象で、**企業内部ネットワーク** での権限昇格リスクが高い。 |
| **CVE‑2026‑13249** (Honeywell PD45 Industrial Printer) | 9.8 | 認証不要の任意ファイルアップロードにより、管理インタフェースで RCE が可能 | 産業用プリンタは **OT（Operational Technology）** 環境に直結。攻撃が物理設備や生産ラインに波及する可能性がある。 |

> **共通点**：すべて「認証不要」または「認証情報の不適切な扱い」に起因し、攻撃者がリモートから直接コード実行や権限取得を行える点です。特にインフラ系（Qpid、Dokploy、Honeywell）と AI 系（Decepticon）の組み合わせは、今後の攻撃シナリオで注目すべきです。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 / ライブラリ | 修正版バージョン | 対策期限 (目安) |
|-------------------|------------------|-----------------|
| **Decepticon** | ≥ **1.1.17** | 直ちにアップデート |
| **Dokploy** | ≥ **0.29.13** | 1 週間以内 |
| **OnlyOffice Document Server** | 7.2.5 以降 (公式パッチ) | 1 週間以内 |
| **Apache Qpid Broker‑J** | ≤ **10.1.0** (10.1.1 で修正) | 2 週間以内 |
| **Honeywell PD45 (F10.19.010040)** | Firmware **F10.19.010050** 以上 | 1 か月以内 |
| **Linux カーネル (各ディストリビューション)** | カーネル **6.8.0‑rc5** 以降 (各ディストリビューションの security update) | 速やかに適用 |
| **WordPress プラグイン** (Automation Web Platform, Bookly, Customer Reviews) | 各プラグイン **4.8.7** 以上、**28.3** 以上、**5.120.1** 以上 | 1 週間以内 |
| **Zimbra (Classic / Modern)** | 9.2.0‑patch‑2026‑01 以降 | 1 週間以内 |
| **ServiceNow AI Platform** | 2026‑R2 Patch (SQLi, auth bypass) | 2 週間以内 |
| **IBM Guardium Data Protection** | 12.2.1 Patch (tar command injection) | 1 週間以内 |

### 3.2 設定・運用上の緩和策
1. **入力サニタイズの徹底**  
   * Decepticon・http4s‑scala‑xml など、外部から受け取る文字列は必ず **ChatML/ XML エスケープ** を実装。  
   * Dokploy の `repoPath` には **`shlex.quote`** もしくは同等の安全な引数展開を使用。

2. **最小権限の適用**  
   * Qpid Broker‑J の管理 API は **IP フィルタリング** と **MFA** を必須化。  
   * Honeywell プリンタの管理インタフェースは **VPN 内部からのみアクセス** できるようにし、デフォルトの管理アカウントは無効化。

3. **ネットワーク分離**  
   * 高リスクサービス（Dokploy、OnlyOffice、Qpid）を **DMZ** に配置し、外部からの直接アクセスを遮断。  
   * LLM を組み込むシステムは **外部 LLM API へのリクエストをプロキシ経由** にし、リクエスト内容をロギング・検査。

4. **監視・インシデント対応**  
   * すべての対象製品で **ファイルアップロード・シェルコマンド実行ログ** を集中管理（SIEM）し、異常

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-61732

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-24T18:17:15.860 |

Decepticon is an autonomous hacking agent for red teams. Versions prior to 1.1.17 wrap web crawl results — the output of agent reconnaissance against target services — into LLM messages without neutralizing ChatML special-token literals. Under the BYOK (Bring Your Own Key) deployment model, users configure their own LLM credentials to any OpenAI-compatible endpoint. Most open-source and self-deployed model providers (vLLM, SGLang, Ollama, LM Studio, text-generation-webui, etc.) do not filter special-token literals from user content in their default configurations. Those literals are parsed into structural role-boundary token IDs, meaning an attacker string planted in a target web page forges a new operator turn the model treats as authoritative, bypassing Decepticon's agent guardrails and resulting in arbitrary command execution inside the Kali Linux sandbox. Version 1.1.17 patches the issue.

### CVE-2026-93425

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-24T16:17:25.990 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, the patch.readRepoDirectories tRPC procedure passes the user-controlled repoPath value from apps/dokploy/server/api/routers/patch.ts into a shell command in packages/server/src/services/patch-repo.ts without safe argument quoting. An authenticated organization member with service:read permission can inject shell metacharacters into repoPath and execute arbitrary commands through child_process.exec as root in the Dokploy container. The supplied service identifier is used only to resolve the server and does not constrain repoPath. Because the standard deployment mounts /var/run/docker.sock, container-root command execution can be used to control Docker and compromise the host and its managed applications. This issue is fixed in version 0.29.13.

### CVE-2026-93643

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-863` |
| Published | 2026-09-25T14:17:23.550 |

When OnlyOffice/Document Editing is available, an unauthenticated remote attacker with access to an existing supported public Briefcase document can abuse unsigned save fields to perform path-traversal writes and execute commands as zimbra.

### CVE-2026-92609

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-384` |
| Published | 2026-09-25T08:16:41.203 |

Session fixation in HTTP management authentication allows remote attackers to gain unauthorized access to an authenticated management session via reuse of a session identifier retained across successful authentication.

This issue affects Apache Qpid Broker-J: through 10.1.0.

Users are recommended to upgrade to version 10.1.1, which fixes the issue.

### CVE-2026-14281

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-25T07:16:53.540 |

The Automation Web Platform – Notifications and OTP for WooCommerce, Advanced Country Code plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.8.6. This is due to missing permission enforcement on the publicly accessible REST route `POST /wp-json/wawp/v1/signup/<op>` and the absence of a key allowlist in the `finish_registration_logic` function, which copies the attacker-controlled `wawp_custom_fields` parameter directly into `update_user_meta()` — allowing sensitive meta keys such as `wp_capabilities` and `wp_user_level` to be set by the caller. This makes it possible for unauthenticated attackers to register a new account with the administrator role and gain full administrative access to the site. When OTP verification is enabled at signup, the OTP session token (`otp_transient`) is returned in plaintext in the HTTP response body, and the `handle_magic_link_request()` handler marks that token as verified on any unauthenticated GET request containing it without ever checking the OTP code value — making the OTP step trivially bypassable with no inbox or SMS access required.

### CVE-2026-13249

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-306;CWE-434` |
| Published | 2026-09-24T19:17:13.080 |

An unauthenticated Remote Code Execution via Arbitrary File Upload vulnerability in the web management interface in Honeywell PD45 Industrial Printer version F10.19.010040, allows upload of attacker controlled files without requiring authentication.


An attacker could potentially exploit this vulnerability, leading to the execution of malicious files and commands. Honeywell also recommends updating to the most recent firmware version, Honeywell PD45 Industrial Printer firmware F10.22.030745, which includes a fix for this vulnerability.

### CVE-2026-97413

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:18.990 |

In the Linux kernel, the following vulnerability has been resolved:

RDMA/rtrs-srv: Fix integer underflow in process_read and process_write

usr_len is read from a network-supplied message field (le16_to_cpu)
and used to compute data_len = off - usr_len without validating that
usr_len <= off. A malicious RDMA client can send usr_len > off causing
an integer underflow, resulting in data_len wrapping to a huge size_t
value which is then passed to the rdma_ev callback as a memory length,
leading to out-of-bounds memory access.

Fix by reading and validating usr_len <= off before rtrs_srv_get_ops_ids()
in both process_read() and process_write(), ensuring the early return
path acquires no reference and has no resource leak.

### CVE-2026-93207

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:15.357 |

In the Linux kernel, the following vulnerability has been resolved:

SUNRPC: Zero rpc_gss_wire_cred at svcauth_gss_decode_credbody() entry

svcauth_gss_decode_credbody() writes the caller's
rpc_gss_wire_cred field by field and assigns gc_ctx.len only on
the success tail.  The caller storage is svcdata->clcred, which
lives in the per-svc_rqst gss_svc_data and is reused across
requests.  Early decode failures leave partially decoded state
mixed with residue from the prior request.

The trailing body_len tightness check is the sharpest case:
xdr_stream_decode_opaque_inline() has already written gc_ctx.data
with a borrowed inline pointer into the current request's XDR
pages, but gc_ctx.len retains its prior value.  Once the request
pages are released the pooled clcred carries a dangling pointer
paired with a stale length.

Zero the caller's rpc_gss_wire_cred at function entry so that
every early-return path leaves a deterministic all-zero cred.
On the trailing tightness-check path, gc_ctx.len is now zero
instead of stale, which neuters length-driven consumers such as
gss_svc_searchbyctx() that would otherwise walk the dangling
data pointer.

### CVE-2026-81549

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-24T15:17:39.897 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to obtain sensitive information due to improper validation of the X-Forwarded-Proto header.

### CVE-2026-93647

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T14:17:23.673 |

An unauthenticated calendar sender can place active markup in a COUNTER message's RFC From address. Selecting the message in Zimbra Classic triggers stored XSS, allowing the attacker to access mailbox data and act as the victim.

### CVE-2026-93642

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T14:17:23.423 |

An unauthenticated sender can forge a share notification that triggers stored XSS when a signed-in Zimbra Modern recipient clicks Accept Share, allowing the attacker to access mailbox data and act as the victim.

### CVE-2026-93641

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T14:17:23.290 |

An unauthenticated sender can forge a share notification that triggers stored XSS when a signed-in Zimbra Classic recipient clicks Accept Share, allowing the attacker to access mailbox data and act as the victim.

### CVE-2026-95832

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-25T13:17:24.063 |

Improper Neutralization of Special Elements in Output Used by a Downstream Component in the colour control escape code handler in kitty from 0.47.3 before 0.49.0 allows a program writing to the terminal to execute an arbitrary command in the user's shell, because color_control() in kitty/window.py answers a query for an unrecognised field name by placing that field name into the reply, and write_escape_code_to_child() in kitty/screen.c then writes the reply to the pseudoterminal master, where it is not distinguishable from input typed by the user, without neutralising it for the shell that reads it. The payload is reduced to printable ASCII before the field name is echoed, which is the restriction introduced in 0.47.3 as the fix for CVE-2026-54057, and the record and field separators ; and = are consumed as delimiters, but every other printable character survives, which is sufficient to compose a shell command. A newline is available from handle_remote_ssh() in kitty/window.py, which writes the bytes yielded by get_ssh_data() in kittens/ssh/utils.py, the first of which begin with a newline, to the pseudoterminal master before any credential carried in the request is checked. The reply is framed as an OSC sequence carrying the escape code number, the field name, and the literal value ?. This results in execution of an attacker-chosen command with the privileges of the user running the terminal.

### CVE-2026-93291

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-24T20:17:34.463 |

Omni C20 lacks proper certificate validation which could allow an attacker to perform a man-in-the-middle attack which could allow them to execute arbitrary code.

### CVE-2026-86860

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-24T19:17:18.733 |

ServiceNow has remediated a missing authorization vulnerability that was identified in the ServiceNow AI Platform. This vulnerability could enable an unauthenticated user, in certain circumstances, to extract instance data beyond what was intended, resulting in privilege escalation.





ServiceNow deployed a security update to hosted instances and ServiceNow provided the update to our partners and self-hosted customers. We are not currently aware of malicious exploitation against ServiceNow instances. We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-13016

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-24T19:17:11.820 |

ServiceNow has remediated a SQL injection vulnerability that was identified in the ServiceNow AI Platform. This vulnerability could enable an unauthenticated user, in certain circumstances, to execute arbitrary SQL statements against the instance's underlying database and gain access to, or modify, instance data beyond what was intended. 





ServiceNow deployed a security update to hosted instances and ServiceNow provided the update to our partners and self-hosted customers. We are not currently aware of malicious exploitation against ServiceNow instances. We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-61742

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-346` |
| Published | 2026-09-24T18:17:16.173 |

DBHub is a database MCP server for Postgres, MySQL, SQL Server, Oracle, MariaDB, SQLite. Versions prior to 0.22.5 expose an unauthenticated HTTP MCP endpoint when started with the documented HTTP transport mode, for example `--transport http --port 8080`. The HTTP server attempts to protect browser-origin access by checking whether the `Origin` hostname equals the `Host` hostname, then reflecting the validated `Origin` into `Access-Control-Allow-Origin`. This does not stop DNS rebinding. After an attacker-controlled hostname rebinds to a victim-accessible DBHub HTTP server, both `Origin` and `Host` can contain the attacker-controlled hostname, so DBHub accepts the request and dispatches MCP tool calls. As a result, a malicious website can deterministically invoke DBHub MCP tools from the victim's browser without prompt injection or model involvement. With the default demo configuration this can read and write the demo SQLite database; with a real configured database, the same primitive can read, enumerate, and potentially write database contents depending on DBHub's configured tool permissions and database credentials. Version 0.22.5 fixes the issue.

### CVE-2026-61741

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-24T18:17:16.013 |

http4s-scala-xml provides `EntityDecoder[F, scala.xml.Elem]` instances that parse XML message bodies. Prior to versions 0.24.1 and 1.0.0-M39, these decoders used a `javax.xml.parsers.SAXParserFactory` obtained from `SAXParserFactory.newInstance` without any security configuration.  With the JDK's default settings, the parser resolves DOCTYPE declarations, external general and parameter entities, and external DTDs.An application that uses these decoders to parse untrusted XML is vulnerable to XML External Entity (XXE) attacks.  An attacker can craft a request that discloses local files readable by the service process, performs server-side request forgery (SSRF) against internal network resources, and/or causes denial of service through entity expansion. Versions 0.24.1 and 1.0.0-M39 fix the issue.

### CVE-2026-61604

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-862` |
| Published | 2026-09-24T18:17:15.707 |

The ixo Blockchain is a Layer 1 blockchain that runs on both Testnet and Mainnet. Prior to version 8.0.0, the x/bonds module moved funds from an address that was resolved from a DID verification method, without verifying that the resolved address belonged to the transaction signer. Affected handlers included MsgMakeOutcomePayment, MsgBuy, MsgSell, MsgSwap, and MsgWithdrawShare, as well as the batch order processor. Because any account may list an arbitrary blockchainAccountID as a verification method on a DID it controls (without the consent of that address's owner), an attacker could register victims' addresses as verification methods on their own DID and then move the victims' balances into a bond the attacker controlled — later withdrawing and bridging the proceeds off-chain. This was exploited on ixo mainnet (ixo-5) on 2026-06-20. The attack required no victim keys, signatures, or system compromise — any account holding a balance in a token a bond could use was at risk. This was fixed in v8.0.0, delivered via the on-chain v8 software-upgrade. The x/bonds module is disabled: every bonds message is rejected on all routes (top-level, authz, CosmWasm, and ICA), and the bonds batch EndBlocker is a no-op so no further reserve movements can occur. All node operators and validators must upgrade to v8.0.0. The flaw is in chain state-machine logic and can only be remediated by running the patched binary. There is no application-level workaround. The vulnerability is in consensus logic; remediation requires the network to run the patched (v8.0.0) binary. The bonds module remains disabled in v8.0.0 and will only be re-enabled in a future release once the signer-authorization model has been corrected.

### CVE-2026-81630

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-24T21:18:48.737 |

The Botslab G980H dash camera firmware does not adequately verify the authenticity of firmware updates. The update process retrieves firmware through an unprotected connection and relies on an integrity value supplied with the firmware instead of a trusted cryptographic signature. A suitably positioned attacker who intercepts a firmware download, or an authenticated attacker who submits a crafted update, could install modified firmware and execute unauthorized code on the device.

### CVE-2026-97404

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-348` |
| Published | 2026-09-24T15:18:01.537 |

In OpenStack Zaqar before 22.0.2, WSGI transport mishandles the URL-Signature header. By sending a request with an empty URL-Signature header, an unauthenticated remote attacker who knows a target project's UUID may bypass both Keystone authentication and pre-signed URL verification, resulting in the ability to read, enumerate, create, and delete that project's queues, messages, claims, and subscriptions. By additionally claiming an administrative role, the attacker may also perform administrative operations, such as managing pools and flavors in admin_mode deployments. Only deployments using the WSGI transport with an authentication strategy configured are affected; the websocket transport is not affected.

### CVE-2026-90481

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-24T15:17:51.760 |

In PortSwigger Burp Suite DAST (formerly Burp Suite Enterprise Edition) before 2026.8, an authentication bypass can occur via an alternate path or channel.

### CVE-2026-93399

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-25T07:16:56.027 |

The Bookly plugin for WordPress is vulnerable to Insecure Direct Object Reference in versions up to, and including, 28.2 via the 'bookly_get_form_id', 'bookly_render_complete', 'bookly_add_to_calendar' and 'bookly_rollback_order' AJAX actions. This is due to the 'bookly_get_form_id' handler blindly storing the attacker-controlled 'order_id' from the submitted form_data into a new booking session, which the 'bookly_render_complete' handler then trusts to look up and return the corresponding Order's secret token without verifying that the current session created that order. This makes it possible for unauthenticated attackers to enumerate sequential order IDs, disclose other customers' order tokens, retrieve calendar/appointment information via 'bookly_add_to_calendar' and permanently delete arbitrary non-completed bookings via 'bookly_rollback_order', which cascade-deletes the customer_appointment and (when no other customers are attached) the underlying appointment.

### CVE-2026-89055

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-25T07:16:55.140 |

The Customer Reviews for WooCommerce plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 5.120.0. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to permanently delete arbitrary attachments from the Media Library — including administrator-owned product images, logos, and documents — by injecting their IDs into a review that is later trashed and purged. Exploitation requires a public review-form link (a 13-hex formId distributed to customers via e-mail), which exposes the nonce needed to reach the handler without any WordPress account or session.

### CVE-2026-79766

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-24T17:17:06.650 |

Termix is a web-based server management platform with SSH terminal, tunneling, and file editing capabilities. From 2.4.1 until 2.5.1, an authenticated Termix administrator can store attacker-controlled domain and email values through PATCH /users/acme-ssl-settings and trigger their interpolation into a certbot shell command through POST /users/acme-ssl-request. In src/backend/database/routes/acme-ssl-routes.ts, child_process.execSync invokes /bin/sh -c with those values only wrapped in double quotes, so shell metacharacters can execute arbitrary operating-system commands as the Termix backend process. Both HTTP webroot and DNS Cloudflare challenge modes are affected, and compromise exposes Termix databases, process secrets, stored credentials, and network reachability. This issue is fixed in version 2.5.1.

### CVE-2026-93228

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:18.253 |

In the Linux kernel, the following vulnerability has been resolved:

svcrdma: Reject Write/Reply chunks with segcount 0

A peer can send a Write or Reply chunk whose segcount field is zero.
xdr_check_write_chunk() only rejects segcount > rc_maxpages, so zero
passes the range check, and xdr_inline_decode(stream, 0) returns the
current (non-NULL) cursor without advancing. The function returns
true and pcl_alloc_write() then links a struct svc_rdma_chunk with
ch_segcount == 0 onto rc_write_pcl or rc_reply_pcl.

An earlier patch in this series made pcl_for_each_segment() safe for
ch_segcount == 0, so this no longer drives the memory walk it used
to. Rejecting the malformed frame at the decode boundary is still
worthwhile as defense in depth: it keeps degenerate zero-segment
chunks off the parsed chunk lists entirely, so any future consumer
that walks ch_segments directly cannot observe one, and it makes the
zero-floor easy to backport to trees where the macro change is more
intrusive. RFC 8166 has no meaning for a Write/Reply chunk that
describes no remote buffer, so no legitimate client is affected.

xdr_check_reply_chunk() funnels Reply chunks through
xdr_check_write_chunk() and inherits the same rejection.

pcl_alloc_write() also links each chunk onto the parsed chunk list
before filling its segment array. If a future change weakens the
segcount-0 rejection, an incomplete chunk is visible to consumers
during the fill loop. Reorder so that list_add_tail() follows the
segment fill loop, ensuring only fully-populated chunks appear on
the list.

### CVE-2026-93289

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-24T20:17:34.137 |

The affected products are vulnerable to command injection attack that could allow an unauthenticated attacker to execute system commands during the pairing process.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-94606

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-287;CWE-807` |
| Published | 2026-09-24T17:17:17.063 |

authentik is an open-source identity provider. Prior to 2026.2.7, 2026.5.7, and 2026.8.2, authentik email authenticator enrollment during an authentication or enrollment flow accepts a recipient address supplied in the setup request instead of using the address already established by the flow. An actor who knows a target user's password can substitute an attacker-controlled address, receive the one-time code, and finish enrolling the factor as the target. The target must not have enrolled the email factor already. Successful enrollment gives the actor a session as the target and access to single sign-on applications behind the account. Other authenticator types are not affected. This issue is fixed in versions 2026.2.7, 2026.5.7, and 2026.8.2.

### CVE-2026-93834

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-25T14:17:24.063 |

A use-after-free vulnerability was found in QEMU's 9pfs subsystem. A race condition between the main thread and a worker thread when processing concurrent Tlcreate and Twalk requests allows a malicious guest user to craft a fid path containing stale heap data, bypassing directory traversal restrictions and escaping the shared directory boundary. This can lead to arbitrary host file read/write and code execution (VM escape) as the QEMU process user.

### CVE-2026-85542

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-25T14:17:20.193 |

IBM Guardium Data Protection 12.2 is affected by a command injection vulnerability in the GIM bundle import functionality. An authenticated attacker can provide a crafted GIM bundle that causes attacker-controlled arguments to be passed to the tar command, resulting in arbitrary command execution with elevated privileges on the Central Manager.

### CVE-2026-89426

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-25T08:16:40.940 |

The Knit Pay – Cashfree, Instamojo, Razorpay, PayPal and more plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 9.6.1.0. This is due to the `maybe_update_user_role()` function reading the target role directly from an attacker-controlled Gravity Forms entry field — configured via the feed's `user_role_field_id` — and passing it to `WP_User::set_role()` without validating the supplied value against an allowlist of permitted roles. This makes it possible for authenticated attackers, with Subscriber-level access and above, to elevate their privileges to administrator by tampering with the hidden role field value at form submission time. Exploitation is further enabled by the fact that $0 orders are synchronously marked as SUCCESS during form submission without requiring a real payment, and when no GF User Registration user can be resolved, the role assignment target falls back to `$lead['created_by']` — the currently authenticated submitter's own user ID — making any authenticated form submitter an eligible exploitation target.

### CVE-2026-19804

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-25T08:16:40.383 |

The s2Member – Excellent for All Kinds of Memberships, Content Restriction Paywalls & Member Access Subscriptions plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 260814 via the 'first_name' parameter parameter. This is due to insufficient sanitization of the first_name parameter via esc_refs(), which strips only regex backreferences and not PHP tags, before substitution into the eval'd Signup Tracking Codes template, combined with disclosure of the site-global proxy verification key that allows PayPal postback verification to be bypassed. This makes it possible for unauthenticated attackers to execute code on the server. Successful exploitation requires that the site administrator has configured a Signup Tracking Codes template containing the %%first_name%% placeholder (a documented, GUI-supported feature) and that the attacker has obtained the site-global proxy verification key, which is exposed in plaintext in the JSON response of any PayPal Checkout AJAX request on the target site.

### CVE-2026-62062

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-25T07:16:54.010 |

Cross-Site Request Forgery (CSRF) vulnerability in Elementor Website Builder allows Cross Site Request Forgery.

This issue affects Elementor Website Builder: from n/a through 4.3.1.

### CVE-2026-13248

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73;CWE-78;CWE-434` |
| Published | 2026-09-24T19:17:12.917 |

An Authenticated Remote Code Execution via Arbitrary File Write in the Intermec Fingerprint Command Interface vulnerability in the web management interface in Honeywell PD45 Industrial Printer version F10.19.010040, allows an authenticated user with access to the admin or itadmin account to submit commands written in the Intermec Fingerprint programming language directly to the printer ’s internal command interpreter. 


An attacker could potentially exploit this vulnerability, leading to the execution of malicious files and commands. Honeywell also recommends updating to the most recent firmware version, Honeywell PD45 Industrial Printer firmware F10.22.030745, which includes a fix for this vulnerability.

### CVE-2026-97509

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:28.767 |

In the Linux kernel, the following vulnerability has been resolved:

thunderbolt: Keep XDomain reference during the lifetime of a service

This is needed because we release the service ID in tb_service_release()
and the ID array is owned by the parent XDomain.

### CVE-2026-97442

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:22.433 |

In the Linux kernel, the following vulnerability has been resolved:

wifi: ath11k: fix invalid data access in ath11k_dp_rx_h_undecap_nwifi

In certain cases, hardware might provide packets with a
length greater than the maximum native Wi-Fi header length.
This can lead to accessing and modifying fields in the header
within the ath11k_dp_rx_h_undecap_nwifi() function for the
DP_RX_DECAP_TYPE_NATIVE_WIFI decap type and
potentially result in invalid data access and memory corruption.

Kernel stack is corrupted in: ath11k_dp_rx_h_undecap+0x6b0/0x6b0 [ath11k]
Call trace:
 ath11k_dp_rx_h_mpdu+0x0/0x2e8 [ath11k]
 ath11k_dp_rx_h_mpdu+0x1e0/0x2e8 [ath11k]
 ath11k_dp_rx_wbm_err+0x1e0/0x450 [ath11k]
 ath11k_dp_rx_process_wbm_err+0x2fc/0x460 [ath11k]
 ath11k_dp_service_srng+0x2e0/0x348 [ath11k]

Add a sanity check before processing the SKB to prevent invalid
data access in the undecap native Wi-Fi function for the
DP_RX_DECAP_TYPE_NATIVE_WIFI decap type.

This adapted from the discussion/patch of the ath12k driver [1].

Tested-on: WCN6855 hw2.1 PCI WLAN.HSP.1.1-04685-QCAHSPSWPL_V1_V2_SILICONZ_IOE-1

### CVE-2026-97409

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:18.463 |

In the Linux kernel, the following vulnerability has been resolved:

nvme-fc: Do not cancel requests in io target before it is initialized

A new nvme-fc controller in CONNECTING state sees admin request timeout
schedules ctrl->ioerr_work to abort inflight requests. This ends up
calling __nvme_fc_abort_outstanding_ios() which aborts requests in both
admin and io tagsets. In case fc_ctrl->tag_set was not initialized we
see the warning below. This is because ctrl.queue_count is initialized
early in nvme_fc_alloc_ctrl().

nvme nvme0: NVME-FC{0}: starting error recovery Connectivity Loss
INFO: trying to register non-static key.
The code is fine but needs lockdep annotation, or maybe
lpfc 0000:ab:00.0: queue 0 connect admin queue failed (-6).
you didn't initialize this object before use?
turning off the locking correctness validator.
Workqueue: nvme-reset-wq nvme_fc_ctrl_ioerr_work [nvme_fc]
Call Trace:
 <TASK>
 dump_stack_lvl+0x57/0x80
 register_lock_class+0x567/0x580
 __lock_acquire+0x330/0xb90
 lock_acquire.part.0+0xad/0x210
 blk_mq_tagset_busy_iter+0xf9/0xc00
 __nvme_fc_abort_outstanding_ios+0x23f/0x320 [nvme_fc]
 nvme_fc_ctrl_ioerr_work+0x172/0x210 [nvme_fc]
 process_one_work+0x82c/0x1450
 worker_thread+0x5ee/0xfd0
 kthread+0x3a0/0x750
 ret_from_fork+0x439/0x670
 ret_from_fork_asm+0x1a/0x30
 </TASK>

Update the check in __nvme_fc_abort_outstanding_ios() confirm that io
tagset was created before iterating over busy requests. Also make sure
to cancel ctrl->ioerr_work before removing io tagset.

### CVE-2026-94609

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-863` |
| Published | 2026-09-24T17:17:17.230 |

authentik is an open-source identity provider. Prior to 2026.2.7, 2026.5.7, and 2026.8.2, an account with delegated permission to manage a group, group membership, or a user can grant superuser status to an account or assign an existing role to a group without holding the permissions that gate those privileges. Group hierarchy checks do not consistently account for superuser status inherited from ancestor groups, and role assignment to a group lacks the required authorization check. Only deployments that delegate these management capabilities to accounts that are not full administrators are affected. This issue is fixed in versions 2026.2.7, 2026.5.7, and 2026.8.2.

### CVE-2026-93806

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:13.570 |

In the Linux kernel, the following vulnerability has been resolved:

wifi: cfg80211: validate assoc response length before status and IE access

cfg80211_rx_assoc_resp() initialises the status and response-IE fields
of cfg80211_connect_resp_params from the management frame before
proving that the frame is long enough for those offsets. S1G and
regular association responses also have different IE offsets, but the
S1G path only patched resp_ie after the unsafe initialiser had already
run.

Defer resp_ie, resp_ie_len, and status to after the link-iteration
loop. Use a bool to remember whether the frame is S1G, then validate
the appropriate minimum length and set all three fields in a single
if/else block. Funnel short-frame and SME-reject cleanup through a
shared free_bss label for the abandon paths.

### CVE-2026-93799

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:12.720 |

In the Linux kernel, the following vulnerability has been resolved:

wifi: iwlwifi: mvm: validate sta_id in BA window status notif

BA_WINDOW_STATUS_NOTIFICATION_ID extracts a 5-bit sta_id from the
firmware notification and uses it to index fw_id_to_mac_id[] without
bounds checking. Validate sta_id before array access to prevent
out-of-bounds indexing.

### CVE-2026-93793

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:12.050 |

In the Linux kernel, the following vulnerability has been resolved:

wifi: iwlwifi: mvm: validate TX_CMD response layout

TX_CMD parsing uses frame_count to walk status entries and then
read the trailing SCD SSN. Make the minimum-length check follow
that exact runtime layout calculation before parsing the payload.

For new TX API, reject TX_CMD responses with frame_count != 1 and
warn/return in the aggregation handler to document that aggregated
accounting is expected via BA notifications.

### CVE-2026-93790

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:11.710 |

In the Linux kernel, the following vulnerability has been resolved:

wifi: iwlwifi: mvm: fix out-of-bounds tid_data access in BA notif

mvmsta->tid_data was indexed by the TFD loop counter 'i' instead of
the actual TID value 'tid'. This writes lq_color into a random tid_data
slot unrelated to the BA entry.
Since multi-TID blockack is not really in use, 'i' was always 0 and no
harm was done.
Add a out-of-bound check before accessing the array.

### CVE-2026-93284

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:09.587 |

In the Linux kernel, the following vulnerability has been resolved:

drm/pagemap: dma-unmap pages before handling migration errors

drm_pagemap_migrate_unmap_pages() relies on the pages array to determine
which pages require DMA unmapping. However,
drm_pagemap_migration_unlock_put_pages() clears the array as part of its
cleanup, leaving drm_pagemap_migrate_unmap_pages() with no valid page
information if it is called afterward.

Call drm_pagemap_migrate_unmap_pages() before
drm_pagemap_migration_unlock_put_pages() so the pages array remains
valid during DMA unmapping.

### CVE-2026-93280

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:25.290 |

In the Linux kernel, the following vulnerability has been resolved:

greybus: audio: bound the topology section sizes against the fetched size

gb_audio_gb_get_topology() fetches a topology blob of a module-supplied
size, and gbaudio_tplg_parse_data() then walks it by adding the
module-supplied size_dais, size_controls and size_widgets fields to
form the control, widget and route section offsets. Those le32 sizes
are never checked against the fetched blob, so a module reporting a
small topology size but large section sizes makes the offsets point
past the allocation, and parsing reads out of bounds.

Reject a topology whose section sizes do not fit within the fetched
size before it is parsed.

### CVE-2026-82093

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-24T15:17:40.733 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to unsafe deserialization of untrusted data.

### CVE-2026-81552

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-24T15:17:40.020 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of environment variables.

### CVE-2026-81548

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-24T15:17:39.770 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-81547

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-24T15:17:39.650 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary commands due to path traversal.

### CVE-2026-81545

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-24T15:17:39.517 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-81539

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-24T15:17:39.377 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-87722

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-09-24T22:17:02.480 |

Uncontrolled Resource Consumption (CWE-400 / CWE-1333) in regex search query predicates (such as RegexProjectPredicate, RegexRefPredicate, RegexPathPredicate, and sibling predicates) and REST regex filter endpoints (RegexListSearcher /projects/?r= and RefFilter /projects/{project}/branches/?r=) in Gerrit Code Review versions 2.1.6 through 3.12.9, 3.13.0 through 3.13.8, and 3.14.0 through 3.14.2 allows an unauthenticated remote attacker (or an authenticated user if anonymous read access is disabled) to cause a denial of service (CPU starvation and JVM heap exhaustion / OutOfMemoryError) via crafted search queries or REST API requests containing regular expressions with large counted repetitions or exponential DFA determinization patterns. Because the user-supplied regular expression is compiled into an unbounded dk.brics.automaton instance (new RegExp(re).toAutomaton()) on the request thread prior to index evaluation or access control visibility filtering, trivial queries can exhaust JVM heap or pin request threads regardless of heap size. This issue is fixed in Gerrit Code Review versions 3.12.10, 3.13.9, and 3.14.3.

### CVE-2026-87721

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407;CWE-834` |
| Published | 2026-09-24T22:17:02.327 |

Uncontrolled Resource Consumption (CWE-400 / CWE-407) in the ANTLR 3 search query parser (QueryParser / Query.g) in Gerrit Code Review versions 2.0.19 through 3.12.9, 3.13.0 through 3.13.8, and 3.14.0 through 3.14.2 allows an unauthenticated remote attacker (or an authenticated user if anonymous read access is disabled) to cause a persistent denial of service (CPU exhaustion and HTTP worker thread pool starvation requiring a server restart) via crafted search queries containing deeply nested parentheses sent to query evaluation endpoints (/changes/?q=, /accounts/?q=, /groups/?query=, /projects/?query=, /Documentation/?q=, /changes/{id}/query?expression=, or SSH gerrit query). Because syntactic predicates in conditionOr and conditionAnd recurse via conditionBase without memoization prior to capability or visibility checks and worker threads do not abort when the client disconnects, a small number of requests (such as 25 requests matching default httpd.maxThreads) can permanently pin all HTTP worker threads. This issue is fixed in Gerrit Code Review versions 3.12.10, 3.13.9, and 3.14.3.

### CVE-2026-96883

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-24T20:17:35.240 |

pgcollection is an open source extension to PostgreSQL. A type confusion issue in AWS pgcollection 2.0.0 through 2.1.1 might allow an authenticated remote user to execute arbitrary code as the postgres operating system user via crafted SQL statements that rely on mismatched type metadata in collection value retrieval and array conversion functions.



To remediate this issue, users should upgrade to version 2.1.2 or later.

### CVE-2026-84399

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-24T20:17:32.673 |

The Botslab G980H dash camera firmware contains an authorization vulnerability in its session based command functionality. The product does not sufficiently associate an authenticated session with the client connection that established it, and subsequent privileged operations rely on possession of a valid session identifier without adequately validating the requesting client's authenticated context. An unauthenticated attacker with adjacent network access could potentially use valid session state associated with another client to access privileged functionality.

### CVE-2026-82566

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-24T20:17:32.503 |

The Botslab G980H dash camera firmware contains a session management vulnerability in which authentication state can remain valid after the associated client connection has been terminated or replaced. Under certain connection conditions, a newly established connection can displace an existing client while previously established session state remains active until a separate expiration mechanism invalidates it. An unauthenticated attacker with adjacent network access could potentially take advantage of this residual authentication state to access functionality associated with another client's session.

### CVE-2026-86859

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-24T19:17:18.603 |

ServiceNow has remediated an authorization bypass security issue that was identified in the ServiceNow AI Platform. This security issue, if exploited, could enable an unauthenticated user to access data within the ServiceNow AI Platform that the user otherwise would not be entitled to access, potentially enabling further unintended access.





ServiceNow deployed a security update to hosted instances and ServiceNow provided the update to our partners and self-hosted customers. We are not currently aware of malicious exploitation against ServiceNow instances. We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-86858

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-24T19:17:18.483 |

ServiceNow has remediated an improper access control security issue that was identified in the ServiceNow AI Platform. This security issue could enable an unauthenticated user, in certain circumstances, to create, modify, or delete instance data beyond what was intended.





In August 2026, ServiceNow deployed a security update to hosted instances and ServiceNow provided the update to our partners and self-hosted customers. We are not currently aware of malicious exploitation against ServiceNow instances. We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-61825

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-24T19:17:15.500 |

code16 Sharp is a Laravel-based framework for building content-management and administrative interfaces. Versions before 9.22.5 contain a stored cross-site scripting vulnerability in `SharpEditorFormField`: attacker-controlled content bearing the `data-html-content` attribute can bypass HTML sanitization and preserve executable markup, which may execute when another user views the stored content. The vendor identifies version 9.22.5 as patched; applications that intentionally enable `SharpFormEditorField::RAW_HTML` must continue to sanitize editor content themselves. As a workaround, applications should sanitize all editor content before storing or rendering it, for example with Symfony HtmlSanitizer, and disable RAW_HTML functionality where it is not required.

### CVE-2026-85057

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-24T18:19:04.217 |

ZITADEL is an open source identity management platform. From 3.0.0 until 3.4.13 and 4.16.1, ZITADEL Actions V1 enables the goja Node-compatible require() registry without restricting its filesystem source loader. An organization Action author with ORG_OWNER, org.action.write, and org.flow.write permissions can run JavaScript at OIDC, SAML, and login-flow trigger points and load files readable by the ZITADEL server process. This can disclose mounted configuration and secrets, including credentials stored through ZITADEL_FIRSTINSTANCE_LOGINCLIENTPATPATH or ZITADEL_FIRSTINSTANCE_MACHINEKEYPATH, and recovered bootstrap credentials can enable escalation from an organization administrator to an instance administrator. The issue affects Actions V1, and host command execution is not established. This issue is fixed in versions 3.4.13 and 4.16.1.

### CVE-2026-91122

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-24T17:17:08.393 |

Discourse is an open-source discussion platform. Prior to 2026.1.8, 2026.6.3, 2026.7.2, and 2026.8.0, the video placeholder component allowed crafted HTML to cause an attribute breakout and inject an attacker-controlled event handler. An authenticated user with default trust-level posting privileges could store the crafted placeholder in a post. When another user opened the post and clicked the video play overlay, the handler could execute arbitrary JavaScript in the viewer's session. Default Content Security Policy settings block inline event handlers, but instances with CSP disabled or relaxed could allow the script to read page content and make authenticated requests as the viewer. This issue is fixed in versions 2026.1.8, 2026.6.3, 2026.7.2, and 2026.8.0.

### CVE-2026-63498

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-24T17:17:05.513 |

Snipe-IT is an IT asset/license management system. Prior to 8.7.0, the uploaded-files API endpoint GET /api/v1/{object_type}/{id}/files/{file_id} allows an authenticated user with file-management access to upload XML and XSLT attachments and request them with the inline=true parameter. The app/Http/Controllers/Api/UploadedFilesController.php show() path does not apply the safe-inline allowlist used by the equivalent web controller, so the browser can process an attacker-controlled xml-stylesheet reference and execute JavaScript generated by the stylesheet in the Snipe-IT origin. A victim who is authorized to view the object must open the attachment URL, after which the script can read same-origin data and perform authenticated actions with the victim's privileges. This issue is fixed in version 8.7.0.

### CVE-2026-56744

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1288` |
| Published | 2026-09-24T17:17:05.047 |

`@bsv/wallet-toolbox` provides BRC-100 wallet signing and storage components, while `@bsv/wallet-toolbox-client` and `@bsv/wallet-toolbox-mobile` provide client-focused distributions for standard and mobile applications using wallet storage services. A vulnerability in these packages causes transactions created through a remote `StorageClient` to trust output locking scripts returned by the storage provider without verifying that they match the outputs requested by the caller. A malicious or compromised storage provider can substitute a recipient script or inject an additional output, causing the wallet to sign and broadcast a transaction that redirects funds while the application and user interface continue to display the intended recipient. Source and npm publication history indicate that stable versions `@bsv/wallet-toolbox` and `@bsv/wallet-toolbox-client` from 1.1.47 through 2.3.3, and `@bsv/wallet-toolbox-mobile` from its initial 1.3.21 release through 2.3.3, are affected. All three packages are patched in version 2.4.0. Applications unable to upgrade should avoid remote `StorageClient` providers, use local storage, or independently verify every transaction output’s locking script and value against the original request before signing

### CVE-2026-97362

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-09-24T15:18:01.393 |

HFS2 version 2.4.0 and earlier contains a denial of service vulnerability that allows unauthenticated attackers to cause a complete and persistent loss of availability by sending a single crafted request. Attackers can trigger a hung serving thread that enters a busy loop, rendering the entire file server unresponsive to all clients without self-recovery until an operator manually restarts the service.

### CVE-2026-97818

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-25T05:17:08.120 |

phpIPAM through 1.8.3 has incorrect authorization for id=="admins" and id=="all" in api/controllers/User.php.

### CVE-2026-77967

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-24T20:17:30.227 |

The Botslab G980H dash camera firmware accepts a reusable authentication value without adequately verifying its freshness or association with the requesting client. An unauthenticated attacker with adjacent network access who captures a valid authentication value could replay it from another client to establish an authenticated session and access privileged device functionality.

### CVE-2026-81455

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-24T19:17:17.463 |

Dell ThinOS 10, versions prior to SecurityAddon_2605.10.2766_T10, contain a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-95985

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-349;CWE-829` |
| Published | 2026-09-24T18:19:08.357 |

The file write tool in Amazon Kiro IDE versions before 1.0.242 might allow remote unauthenticated actors to inject crafted instructions into the agent's context. When a user runs the agent in a crafted repository as an untrusted workspace, sending any message can cause agent modifications to auto-loaded global configuration paths.



We recommend you upgrade to Kiro IDE version 1.0.242 or later. Users who ran the agent in an untrusted workspace on an earlier version should also review the global Kiro configuration directory (~/.kiro) for entries they did not create.

### CVE-2026-63493

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-24T17:17:05.367 |

Snipe-IT is an IT asset/license management system. Prior to 8.7.0, a password-authenticated session for an account with self.api permission can reach the personal-access-token API flow before completing the account's second-factor challenge because CheckForTwoFactor is enforced in the web middleware group but not the API middleware group. The advisory states that the resulting persistent API token can read and modify resources with the victim's permissions and, for an administrator, can reach the users/two_factor_reset endpoint. Resetting the administrator's enrolled second factor allows the password-holding attacker to enroll an attacker-controlled factor, take over the administrator's web account, and lock out the legitimate user. The token does not create a web session, but it provides broad API access while the same browser session remains blocked at the two-factor page. This vulnerability is fixed in 8.7.0.

### CVE-2026-77581

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-24T16:17:10.943 |

BentoPDF is a client-side PDF toolkit that is self hostable. In 2.8.6 and earlier, the certificate and timestamp CORS proxy in cloudflare/cors-proxy-worker.js uses isPrivateOrReservedHost() to validate a supplied hostname separately from the DNS resolution used by fetch(targetUrl), allowing an attacker-controlled hostname to resolve to an internal or reserved destination after validation. A certificate-like path can satisfy ALLOWED_PATH_PATTERNS, and direct clients can forge the browser-oriented Origin header. Deployments without PROXY_SECRET skip the optional signature check, while the signature is an anti-abuse measure rather than a destination-security boundary. The proxy has a 10 MB response limit and can relay response bodies from reachable destinations. The advisory identifies both the official Worker deployment and self-hosted instances as impacted where the Worker execution environment can reach internal or reserved destinations. This vulnerability is fixed in 2.8.7.

### CVE-2026-77874

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-24T15:17:38.700 |

IBM Enterprise Build of Quarkus 3.27.1 through 3.27.5.SP1, and 3.33.1 through 3.33.3.SP1 is vulnerable to SQL injection. A remote unauthenticated attacker could send specially crafted SQL statements, which could allow the attacker to view, add, modify, or delete information in the back-end database.

### CVE-2026-100176

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T14:17:17.020 |

The AIL Framework's username timeline feature is vulnerable to stored cross-site scripting (XSS). Usernames imported from chats and crawled forums are stored without character restrictions. When an authenticated analyst views the username timeline, the application renders these stored usernames into the DOM using D3's html() method in the tooltip. Because the username value (d.obj) is interpolated directly into an HTML string without sanitization, a crafted username containing HTML event handlers (e.g., <img src=x onerror=alert(1)>) will execute arbitrary JavaScript in the analyst's browser when the analyst hovers over the corresponding timeline entry. The attack requires the victim to be an authenticated analyst with access to the timeline view and to interact with the malicious timeline entry (hover). Successful exploitation can lead to session hijacking, data exfiltration, or unauthorized actions performed within the analyst's authenticated session. The vulnerability resides in the client-side JavaScript file var/www/static/js/d3/timeline_basic.js.

### CVE-2026-100172

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T14:17:15.353 |

The AIL Framework (ail-project/ail-framework) contains a stored cross-site scripting (XSS) vulnerability in two Jinja2 templates that render popovers for matched, tracked, or tagged content: var/www/templates/chats_explorer/block_message.html and var/www/templates/objects/item/show_item.html. In both templates, dynamic values associated with this content, including icon color, icon style, icon glyph, subtype, identifier, name, description, and matched value, are interpolated directly into the data-content HTML attribute of Bootstrap popover elements without appropriate output encoding. Because the popovers are configured with data-html="true", the content is interpreted as HTML in the victim's browser. An authenticated attacker who can influence matched, tracked, or tagged content may inject arbitrary HTML or JavaScript into these values. When a victim displays the affected popover, the injected markup may execute in the victim's session, potentially enabling data exfiltration or actions with the victim's privileges. The vulnerability is classified as stored XSS because the malicious payload can persist in the affected match, tracking, or tag-related data and be delivered to users who view the affected content.

### CVE-2026-97730

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-24` |
| Published | 2026-09-25T03:16:59.533 |

In Netgate pfSense Plus before 26.07 and pfSense CE before 2.9.0, a Local File Inclusion (LFI) vulnerability in the Dashboard (index.php) widget sequence data handling allows an authenticated attacker to execute arbitrary PHP code. To exploit this, an attacker with privileges to modify Dashboard settings and write arbitrary files to the pfSense firewall system (e.g., /tmp/test.widget.php) can submit a crafted widget sequence value containing a path traversal payload (e.g., ../../../../../../../../../../../tmp/test). The Dashboard will subsequently read and execute the arbitrary PHP file as if it were a standard widget.

### CVE-2026-85082

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-25T00:16:57.720 |

Root Browser Classic 3.3.0 passes the path of a selected SQLite database to an operating-system shell without safely separating the filename from the command.

### CVE-2026-93354

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-09-24T20:17:34.613 |

Taskview Community before 1.56.0 contains a missing authentication vulnerability that allows unauthenticated attackers to register arbitrary OAuth clients and take over user accounts by exploiting the OAuth 2.0 Dynamic Client Registration endpoint, which is enabled by default and requires no authentication. Attackers can send a POST request to the registration endpoint to obtain a client_id and client_secret, then craft a malicious authorization link pointing to an attacker-controlled redirect URI to capture authorization codes and exchange them for access tokens granting full API access to victim account data.

### CVE-2026-82372

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-24T20:17:32.353 |

Improper handling of sensitive data during IPsec policy creation and modification in Brocade SANnav versions before 3.0.1a results in pre-shared keys being recorded in application logs. Individuals with read access to system log files or support bundles can view these credentials, leading to the potential exposure of keys used to secure network tunnels.

### CVE-2026-82371

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-24T19:17:18.047 |

Plaintext exposure of sensitive authentication data in Brocade SANnav discovery service log files enables individuals with file read access to retrieve administrative switch credentials and active session tokens. An attacker with access to system logs or support bundles can leverage exposed authentication details to compromise managed network infrastructure and access active application sessions. This vulnerability affects Brocade SANnav versions before 3.0.1a.

### CVE-2026-56738

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-24T17:17:04.890 |

phpMyFAQ is an open source FAQ web application. The `StopWords::add()` method inversions prior to 4.1.6 builds a SQL `INSERT` statement using `sprintf()` and inserts the user-supplied stop word value directly into the query string without calling the application's database escaping function on it. A sibling method, `StopWords::update()`, which modifies an existing stop word, correctly escapes the same kind of input. The omission is isolated to the `add()` (insert) code path. An authenticated administrator who can reach the stop-word management feature can submit a crafted value as the "word" parameter that breaks out of the SQL string literal and injects arbitrary SQL, including statements to drop tables, exfiltrate data, or modify other rows in the database. Version 4.1.6 fixes the issue.

### CVE-2026-56739

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:L/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-24T16:17:07.803 |

Logto is the modern, open-source auth infrastructure for SaaS and AI apps. Prior to 1.43.0, Logto fetches administrator-controlled outbound destinations without validating the address used for the connection. Webhook delivery in packages/core/src/libraries/hook/utils.ts can reach special-use and cloud metadata addresses. Custom OAuth2 connectors can use an attacker-selected userInfoEndpoint and forward the OAuth access token in the Authorization header, while OIDC connectors can fetch an attacker-selected jwksUri. The affected operations require tenant administrative configuration access, but they cross the server's network boundary and can expose internal data or upstream provider credentials. This issue is fixed in version 1.43.0.

### CVE-2026-97898

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-09-25T10:17:08.907 |

Insecure Direct Object Reference / missing object-level authorization in the Akia keyless entry cloud service. The unlock action is relying on a client-supplied room/door identifier that is not properly authorized server-side against the authenticated guest's booking. An authenticated guest could unlock rooms other than their own, resulting in unauthorized physical access to guest rooms at an affected property.




As of 19th September 2026 the service is no more vulnerable to this attack (feedback received by the reporter). 




The attack is remote but the effect is local to an affected property.

### CVE-2026-95699

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-653` |
| Published | 2026-09-24T21:18:58.613 |

Prior to 9/18/2026, the iSteamX mobile application's AWS policy could grant authenticated users access to wildcard MQTT topics, which can expose other users' device data and allow the attacker to start and stop other connected users' devices. This risked exposing user profile information and potential scalding due to unintended device activation.

### CVE-2026-14443

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-24T21:17:12.130 |

Incomplete log sanitization during bulk IPsec policy collection in Brocade SANnav versions before 3.0.1a permit extension switch pre-shared keys to be written to system logs. Individuals with read access to container logs or support archives can obtain these keys, leading to the potential compromise of encrypted network tunnels.

### CVE-2026-86857

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-24T19:17:18.350 |

ServiceNow has remediated an authorization bypass security issue that was identified in the ServiceNow AI Platform. This security issue, if exploited, could enable an authenticated user to access data within the ServiceNow AI Platform that the user otherwise would not be entitled to access, potentially enabling further unintended access.





ServiceNow deployed an update to hosted instances, and ServiceNow provided the update to our partners and self-hosted customers. We are not currently aware of malicious exploitation against ServiceNow instances. We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-97455

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:23.957 |

In the Linux kernel, the following vulnerability has been resolved:

ACPICA: Fix use-after-free in acpi_ds_terminate_control_method()

Fix use-after-free issue in acpi_ds_terminate_control_method() by
clearing references to method locals and arguments.

### CVE-2026-97452

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:23.573 |

In the Linux kernel, the following vulnerability has been resolved:

ACPICA: Prevent adding invalid references

Prevent adding references for local, argument, and debug objects
in acpi_ut_copy_simple_object().

### CVE-2026-97451

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:23.463 |

In the Linux kernel, the following vulnerability has been resolved:

ACPICA: Fix integer overflow in acpi_ex_opcode_3A_1T_1R() (mid_op)

Add overflow check for Index + Length to prevent integer overflow
when calculating the truncation length. This prevents negative
size parameter being passed to memcpy().

### CVE-2026-97450

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:23.350 |

In the Linux kernel, the following vulnerability has been resolved:

ACPICA: validate handler object type in two places

ACPICA: validate handler object type in acpi_ev_has_default_handler()
and acpi_ev_find_region_handler().

### CVE-2026-93827

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:16.410 |

In the Linux kernel, the following vulnerability has been resolved:

virtio-fs: avoid double-free on failed queue setup

virtio_fs_setup_vqs() allocates fs->vqs and fs->mq_map before calling
virtio_find_vqs(). If virtio_find_vqs() fails, the error path frees both
pointers and returns an error to virtio_fs_probe().

virtio_fs_probe() then drops the last kobject reference, and
virtio_fs_ktype_release() frees fs->vqs and fs->mq_map again. This leaves
dangling pointers in struct virtio_fs and can trigger a double-free during
probe failure cleanup.

Set fs->vqs and fs->mq_map to NULL immediately after kfree() in the
virtio_fs_setup_vqs() error path so that the later kobject release sees an
uninitialized state and kfree(NULL) becomes harmless.

This can be reproduced when a broken virtio-fs device advertises more
request queues than the transport actually provides. In that case
virtio_find_vqs() fails while setting up the extra queue, and the probe
path reaches the double-free cleanup sequence.

### CVE-2026-96748

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-177` |
| Published | 2026-09-24T19:17:20.813 |

PyMongo's connection string parsing decodes percent-encoded characters in the host portion before the host list is separated on its delimiters. When an application places a hostname value supplied by an unauthenticated party into a connection string, that party may cause additional servers of their choosing to be added to the application's database client. The application may then send its authentication exchange and database operations to one of those servers, which can observe limited information and return altered results.

### CVE-2026-82157

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-24T19:17:17.917 |

Dell ThinOS 10, versions prior to SecurityAddon_2605.10.2766_T10, contains an Improper Certificate Validation vulnerability. An unauthenticated attacker with adjacent network access could potentially exploit this vulnerability, leading to Protection mechanism bypass and Unauthorized access.

### CVE-2026-96746

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-24T16:17:27.460 |

An out-of-bounds write in the connection-monitoring logic of the MongoDB C Driver may allow an unauthenticated party who controls name resolution and the responses of the hosts named in a client's connection string to write beyond the end of a heap buffer. This may cause the application using the driver to terminate unexpectedly.

### CVE-2026-58008

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-24T15:17:25.163 |

Stack-based buffer overflow vulnerability in Altera Trusted Firmware on HPS allows Exploitation of Improperly Configured or Implemented Memory Protections.

This issue affects Trusted Firmware: through socfpga_v2.14.0.

### CVE-2026-58007

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-24T15:17:25.027 |

Untrusted pointer dereference vulnerability in Altera Trusted Firmware on HPS allows Exploitation of Improperly Configured or Implemented Memory Protections.

This issue affects Trusted Firmware: through socfpga_v2.14.0.

### CVE-2026-58006

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-24T15:17:24.890 |

Untrusted pointer dereference vulnerability in Altera Trusted Firmware on HPS allows Exploitation of Improperly Configured or Implemented Memory Protections.

This issue affects Trusted Firmware: through socfpga_v2.14.0.

### CVE-2026-58005

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-24T15:17:24.750 |

Out-of-bounds read vulnerability in Altera Trusted Firmware on HPS allows Privilege Escalation and Overflow Buffers.

This issue affects Trusted Firmware: through socfpga_v2.14.0.

### CVE-2026-58004

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-24T15:17:24.610 |

Out-of-bounds read vulnerability in Altera Trusted Firmware on HPS allows Privilege Escalation and Overflow Buffers.

This issue affects Trusted Firmware: through socfpga_v2.14.0.

### CVE-2026-13467

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-24T15:17:19.423 |

Out-of-bounds write vulnerability in Altera Trusted Firmware on HPS allows Exploitation of Improperly Configured or Implemented Memory Protections.

This issue affects Trusted Firmware: through socfpga_v2.14.0.

### CVE-2026-13466

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-131` |
| Published | 2026-09-24T15:17:19.280 |

Incorrect calculation of buffer size vulnerability in Altera Trusted Firmware on HPS allows Overflow Buffers.

This issue affects Trusted Firmware: through socfpga_v2.14.0.

### CVE-2026-13465

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-24T15:17:19.117 |

Stack-based buffer overflow vulnerability in Altera Trusted Firmware on HPS allows Exploitation of Improperly Configured or Implemented Memory Protections.

This issue affects Trusted Firmware: through socfpga_v2.14.0.

### CVE-2026-85056

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-24T18:19:04.040 |

ZITADEL is an open source identity management platform. From 4.0.0 until 4.16.1, ZITADEL Login V2 creates a browser session after password verification and can reuse that session for a later authentication request without verifying a user's enrolled TOTP, OTP, or U2F second factor. When the MFA step is abandoned and login starts again, session-validity checks require MFA only when the organization enables Force MFA or Force MFA for local users only, so a voluntarily enrolled factor can be skipped while completing an OIDC or SAML callback for a customer application. Login V1, the ZITADEL Console, Management and Admin APIs, and user self-management are not affected. This issue is fixed in version 4.16.1.

### CVE-2026-97433

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:21.350 |

In the Linux kernel, the following vulnerability has been resolved:

nvme: validate FDP configuration descriptor sizes

Validate descriptor sizes while walking the FDP configurations log so
dsze == 0 or a descriptor past the log end cannot cause unbounded
iteration or reads past the buffer.

### CVE-2026-91160

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-24T17:17:09.257 |

OpenWA is a free, open source, self-hosted WhatsApp API gateway. Prior to 0.23.5, the /events WebSocket gateway delivers the session.qr event to a VIEWER API key that subscribes by event name or through either wildcard subscription form, even though GET /api/sessions/{sessionId}/qr requires the OPERATOR role. When an allowed session is waiting to be paired, the exposed QR lets the key holder link an external device to the WhatsApp account and then read and send messages outside OpenWA and its audit trail. Keys restricted through allowedSessions remain limited to those sessions, and deployments that issue only OPERATOR or ADMIN keys are not affected. This issue is fixed in version 0.23.5.

### CVE-2026-56736

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-24T15:17:24.100 |

phpMyFAQ is an open source FAQ web application. A stored cross-site scripting (XSS) vulnerability in versions prior to 4.2.0-alpha allows any unauthenticated user (or low-privileged registered user) to inject arbitrary JavaScript that executes in an administrator's browser when they review or edit a user-submitted FAQ entry. This leads to admin account takeover via session theft. The vulnerability exists because `html_entity_decode()` converts HTML entities into executable HTML after `strip_tags()` has already passed them through, and the admin template renders the content with Twig's `|raw` filter without any output sanitization. Version 4.2.0-alpha fixes the issue.

### CVE-2026-97875

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-350` |
| Published | 2026-09-25T11:17:16.470 |

Rojo's "rojo serve" HTTP API (default port 34872) has no Host/Origin header validation, making it vulnerable to DNS rebinding. A malicious webpage can read all project source, write malicious code to files on disk, and launch local programs via opener::open() with no user interaction beyond visiting the page.

### CVE-2026-92713

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-25T08:16:41.310 |

The Modula Image Gallery – Photo Grid & Video Gallery plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the upload_image function in all versions up to, and including, 3.0.2. This makes it possible for authenticated attackers, with author-level access and above, to delete arbitrary files on the server. The path restriction to wp-content/uploads is not an effective ownership boundary, as all user attachment files reside within that tree, and Authors trivially satisfy the edit_post check on their own galleries.

### CVE-2026-81473

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-24T19:17:17.607 |

Dell Rugged Control Center (RCC), versions prior to 5.2.206, contain an Improper Authorization vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges.

### CVE-2026-77294

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-24T19:17:16.570 |

TREK is a collaborative travel planner. Prior to 3.3.0, TREK allows an authenticated user to store an attacker-controlled llm_base_url through the settings API when the LLM_PARSING feature is enabled. Write permission to the target trip instance is required to trigger the vulnerable AI-assisted import path. The value is consumed by the clients in server/src/nest/llm-parse/clients/openai-compatible.client.ts, server/src/nest/llm-parse/clients/anthropic.client.ts, and server/src/nest/llm-parse/router/ollama-format.client.ts without applying the server-side request forgery guard. Triggering AI-assisted trip parsing causes the server to request the supplied destination, and upstream error response text can be returned in parsing warnings. This permits internal service discovery and access to link-local cloud metadata, with possible disclosure of infrastructure credentials and subsequent modification of protected cloud resources. This issue is fixed in version 3.3.0.

### CVE-2026-94611

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-09-24T17:17:17.390 |

authentik is an open-source identity provider. Prior to 2026.2.7, 2026.5.7, and 2026.8.2, authentik API serializers return stored credentials when an account has view permission on an affected configuration, even when that account is not authorized to change the configuration or read its secrets. Affected configurations include one-time code delivery by mail or SMS, outbound provisioning targets, device trust integrations, identity sources, the Kubernetes outpost integration, applications using a client or shared secret, and applications using a proxy provider. Deployments are affected when view permission is granted to accounts that are not intended to read these credentials; deployments where every viewer is permitted to read them are not affected. This issue is fixed in versions 2026.2.7, 2026.5.7, and 2026.8.2.

### CVE-2026-93787

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:11.363 |

In the Linux kernel, the following vulnerability has been resolved:

smb: client: bound dirent name against end of SMB response in cifs_filldir

cifs_filldir() copies the entry name out of an SMB1 TRANS2_FIND_FIRST /
FIND_NEXT response using a length (de.namelen) supplied by the server.
The kmalloc'd SMB response buffer is bounded, but nothing checks that
de.name + de.namelen still lies inside that buffer before the eventual
filldir64() -> verify_dirent_name() -> memchr() reads namelen bytes.

A hostile SMB1 server that returns an oversized FileNameLength in a
directory entry therefore causes memchr() to read past the end of the
response slab buffer. Reachable from any user who can list a directory
on a CIFS mount served by an attacker-controlled server (getdents64()
on the mounted directory):

  BUG: KASAN: slab-out-of-bounds in memchr+0x71/0x80
  Read of size 1 at addr ffff88800e0640cc by task poc/115
  Call Trace:
   dump_stack_lvl+0x64/0x80
   print_report+0xce/0x620
   kasan_report+0xec/0x120
   memchr+0x71/0x80
   filldir64+0x4c/0x6a0
   cifs_filldir.constprop.0+0x9bb/0x1e00
   cifs_readdir+0x2101/0x3380
   iterate_dir+0x19c/0x520
   __x64_sys_getdents64+0x126/0x210
   do_syscall_64+0x107/0x5a0
   entry_SYSCALL_64_after_hwframe+0x77/0x7f

Pass the end-of-response pointer down to cifs_filldir() and reject
entries whose name would extend past that boundary.

This bug was discovered by Artiphishell's vTriage pipeline, which
generated a userspace reproducer (an emulated hostile SMB1 server plus
a getdents64() client) that reliably triggers the KASAN report on an
unpatched kernel. The fix below was drafted with the Claude coding
assistant; a userspace reproducer is available on request.

### CVE-2026-93786

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:11.243 |

In the Linux kernel, the following vulnerability has been resolved:

ksmbd: preserve VFS inherited POSIX ACL mask

The VFS initializes a child's POSIX ACL from the parent's default ACL and
the requested creation mode. Do not mutate the parent ACL or overwrite the
child's VFS-computed access and default ACLs afterwards.

This preserves restrictive ACL_MASK entries and prevents SMB object creation
from widening effective permissions.

### CVE-2026-62368

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-24T17:17:05.207 |

Snipe-IT is an IT asset/license management system. Prior to 8.7.0, a user with the customfields.create permission can store markup in CustomField.name, and app/Presenters/AssetPresenter.php assigns that value as an unescaped bootstrap-table header title. When another user opens an asset-list page associated with the fieldset, the stored markup executes on page load in that user's Snipe-IT session. This can expose same-origin data and perform authenticated actions with the victim's privileges, including privilege escalation when a superuser views the affected list. This issue is fixed in version 8.7.0.

### CVE-2026-93282

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:25.570 |

In the Linux kernel, the following vulnerability has been resolved:

ksmbd: fix maximum allowed access checks

The DACL permission check looks for an ACE matching the current user and
falls back to the Everyone ACE. It does not consider an Authenticated
Users ACE, even though an authenticated session is a member of that
well-known group.

As a result, opening a file whose access is granted through S-1-5-11 can
incorrectly fail with STATUS_ACCESS_DENIED. Treat an Authenticated Users
ACE as a fallback entry alongside Everyone.

The maximal access calculation also combines access masks from every ACE,
regardless of whether its SID applies to the current user. This can grant
rights belonging to an unrelated principal. Process only ACEs applying to
the user, Everyone, or Authenticated Users, and accumulate allowed and
denied masks in ACL order. Preserve explicitly requested access bits so
they are validated against the resulting maximal mask.

When ACCESS_SYSTEM_SECURITY is denied, report STATUS_PRIVILEGE_NOT_HELD
instead of the generic STATUS_ACCESS_DENIED. Access to the system ACL
requires a security privilege that ksmbd does not grant.

For regular files, include FILE_EXECUTE in maximal access when the client
requested GENERIC_EXECUTE and the DACL grants the complete file-read set.
Keep a direct FILE_EXECUTE request subject to the explicit DACL bit. This
matches the POSIX file ACL mapping without broadening specific execute
requests.

Do not replace rights from an applicable NT ACE with a POSIX ACL entry.
The POSIX ACL is only a fallback when no user, Everyone, or Authenticated
Users ACE applies; otherwise it can incorrectly broaden the stored DACL.

This fixes smb2.maximum_allowed.maximum_allowed.

### CVE-2026-93224

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:17.720 |

In the Linux kernel, the following vulnerability has been resolved:

svcrdma: Fix unmatched rn_unregister on failed accept

When svc_rdma_accept() takes the errout path before
rpcrdma_rn_register() has succeeded, the existing cleanup block
calls rpcrdma_rn_unregister(dev, &newxprt->sc_rn) unconditionally.
svcxprt_rdma is kzalloc'd, so on that path sc_rn.rn_index is 0 and
sc_rn.rn_done is NULL; the unregister therefore xa_erase()s another
caller's slot 0 and performs an unmatched kref_put() on the
rpcrdma_device's rd_kref.

The same errout also brackets the cleanup with svc_xprt_get()/
svc_xprt_put() around the kref_init() birth reference. The kref
goes 1 -> 2 -> 1 and never reaches 0, so the svcxprt_rdma (and the
net/ns_tracker it pinned) is leaked on every failed accept.

rpcrdma_rn_register() writes rn->rn_done last, only after xa_alloc()
and kref_get() have both succeeded, so rn_done == NULL is a natural
"never registered" sentinel. Guard rpcrdma_rn_unregister() with an
early return when rn_done is NULL, and clear rn_done before the
matching xa_erase() so a repeated unregister is also a no-op.

With that guard in place, the accept errout drops the kref_init()
birth reference via svc_xprt_put(), which dispatches svc_rdma_free().
Teardown of sc_qp, sc_sq_cq, sc_rq_cq, and sc_pd runs under existing
IS_ERR/NULL guards in svc_rdma_free(); sc_rn is covered by the new
rn_done sentinel; sc_cm_id is non-NULL on every errout path because
svc_rdma_accept() dereferences it above the first goto errout.

svc_xprt_free() drops the module reference associated with the freed
transport, and svc_handle_xprt() drops its pre-acquired reference
when ->xpo_accept() returns NULL. Take a replacement module reference
before svc_xprt_put() so the two module_put()s remain balanced.

The rn_done guard also covers svc_rdma_free()'s non-listener call
to rpcrdma_rn_unregister() for transports whose register attempt
failed or never ran.

### CVE-2026-93221

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:17.310 |

In the Linux kernel, the following vulnerability has been resolved:

nfsd: convert nfsd_net boolean flags to unsigned long flags word

nfsd_net contains several boolean fields that are accessed from
concurrent contexts without serialization.  In particular,
nfsd4_end_grace() guards its drain path with a plain bool:

    if (nn->grace_ended)
            return;
    nn->grace_ended = true;

The read and the write are independent, and nothing in struct
nfsd_net serializes them.  At least two contexts can reach this
code with no lock held:

    laundromat path
      laundry_wq kworker
        nfs4_laundromat()
          nfsd4_end_grace()

    RECLAIM_COMPLETE path
      nfsd compound kthread
        nfsd4_reclaim_complete()
          inc_reclaim_complete()
            nfsd4_end_grace()

Both callers can observe grace_ended == false on different CPUs,
both store true, and both proceed into nfsd4_record_grace_done(),
which invokes the active client_tracking_ops->grace_done callback.
For tracking ops that drain reclaim_str_hashtbl (legacy_tracking_ops
via nfsd4_recdir_purge_old, and the cld v1+ ops via
nfsd4_cld_grace_done), grace_done calls nfs4_release_reclaim(),
which walks every bucket of reclaim_str_hashtbl with no lock and
calls nfs4_remove_reclaim_record() (list_del + kfree) on each
entry.  Two concurrent walkers corrupt the list and double-free
every nfs4_client_reclaim.  A concurrent nfsd4_find_reclaim_client()
iterating the same bucket reads through freed memory.

A third call site exists in nfs4_state_start_net() on the
skip_grace startup path, but it runs under nfsd_mutex before any
client has connected and before the laundromat's first delayed
work fires, so it cannot race with the two callers above.

Replace the scattered boolean fields in nfsd_net with a single
unsigned long flags word and an enum nfsd_net_flag for the bit
positions.  The grace_ended race is fixed by using
test_and_set_bit(), which is atomic on all architectures.  The
remaining flags (grace_end_forced, in_grace, somebody_reclaimed,
track_reclaim_completes, nfsd_net_up, lockd_up) are converted to
use test_bit/set_bit/clear_bit for consistency.  This avoids
sub-word cmpxchg issues on architectures like Hexagon that only
support word-sized atomic operations.

### CVE-2026-56737

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-24T16:17:07.637 |

phpMyFAQ is an open source FAQ web application. Versions 3.2.0 through 4.1.5 contain an authentication bypass in its public two-factor authentication verification flow: an unauthenticated attacker can submit an account’s numeric user ID and a valid or brute-forced six-digit TOTP code without first authenticating with the account password, allowing takeover of any 2FA-enabled account, including administrator accounts. Version 4.1.6 is patched by binding TOTP verification to a session established after successful password authentication and limiting failed TOTP attempts. No official workaround is documented; affected installations should upgrade to 4.1.6 or later.

### CVE-2026-90959

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-24T15:17:53.540 |

A path traversal vulnerability was found in pulpcore. The content upload API accepts a 'file_url' parameter that allows users with file repository privileges to specify a local file URL for Pulp to download and store. A URL scheme validation check uses a string prefix comparison that only rejects URLs beginning with 'file://', but Python's URL parser recognizes the 'file:' scheme without double slashes, creating a mismatch between what is validated and what is dispatched to the file downloader. An authenticated user with low-privilege repository permissions can supply a specially crafted URL using relative path traversal sequences to read any file accessible to the Pulp server process. In deployments that include Pulp Container, successful exploitation allows an attacker to read the container registry token signing private key and forge bearer tokens, granting unauthorized access to all private container repositories in the affected registry.

### CVE-2026-97735

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T04:17:50.763 |

ITFlow before 26.08 allows SVG attachments in the ticket email parser (cron/ticket_email_parser.php) for email messages that may arrive over SMTP from arbitrary senders.

### CVE-2026-89325

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-24T19:17:19.580 |

An uncontrolled search path element in InsightVM assessment content in Rapid7 Insight Agent on Windows allows a local, low-privileged user to execute arbitrary code as SYSTEM via a planted executable resolved from the machine PATH.

Assessment content at or below version 0.0.261.0 included a check that invoked the `code` command without a fully qualified path from a process running as SYSTEM. The command was resolved against the machine PATH environment variable at execution time. Where the machine PATH contained a directory writable by non-administrative users and ordered ahead of the legitimate Visual Studio Code installation, a local user could place an executable named `code` in that directory and cause the agent to execute it with SYSTEM privileges.

The version range above refers to InsightVM assessment content versions, not Insight Agent versions. All Insight Agent versions were affected while running assessment content at or below 0.0.261.0. Assessment content is delivered to all Insight Agents via the Rapid7 Insight Platform independently of the Insight Agent version and is not customer-managed.

This issue was resolved in assessment content version 0.0.269.0, which was made generally available on September 15, 2026. Remediation was deployed automatically and no customer action is required.

### CVE-2026-97513

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:29.210 |

In the Linux kernel, the following vulnerability has been resolved:

media: chips-media: wave5: Release m2m_ctx after Instance Removed from List

Possible use after free if IRQ thread manages to obtain spinlock between
m2m_ctx release and wave5_release function removing stream instance from
list of active instances. The IRQ thread looks for the m2m_ctx which is
freed so null pointer dereference occurs.

### CVE-2026-97497

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:27.410 |

In the Linux kernel, the following vulnerability has been resolved:

drm/amdkfd: Check bounds for allocate_sdma_queue restore_sdma_id

allocate_sdma_queue has an option where the sdma queue id can be
specified (used by CRIU). We weren't bounds-checking that
value.

Confirm it's less than the maximum number of queues.

### CVE-2026-97478

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:25.183 |

In the Linux kernel, the following vulnerability has been resolved:

virt: acrn: Fix irqfd use-after-free during eventfd shutdown

acrn_irqfd_deassign() and the eventfd EPOLLHUP wakeup can race and free
the same struct hsm_irqfd:

  CPU0                                 CPU1
  ----                                 ----
  eventfd_release()
    wake_up_poll(EPOLLHUP)
      hsm_irqfd_wakeup()
        queue_work(&irqfd->shutdown)
                                       acrn_irqfd_deassign()
                                         hsm_irqfd_shutdown()
                                           list_del_init()
                                           eventfd_ctx_remove_wait_queue()
                                           eventfd_ctx_put()
                                         kfree(irqfd)
  hsm_irqfd_shutdown_work()
    container_of(work, ..., shutdown)
    irqfd->vm                  <-- use-after-free

The deassign path freed the irqfd while a shutdown work item was
already queued by EPOLLHUP (or vice versa), so the work item could
resurrect a dangling pointer through container_of().

Switch to the lifetime model used by KVM irqfds:

 - Deassign/deinit only deactivate the irqfd: remove it from vm->irqfds
   under irqfds_lock and queue the cleanup work.
 - hsm_irqfd_shutdown_work() becomes the sole owner that unhooks the
   eventfd waitqueue entry, drops the eventfd reference and frees the
   irqfd.
 - A new HSM_IRQFD_FLAG_SHUTDOWN bit guarded by test_and_set_bit()
   ensures the cleanup work is queued at most once, no matter how many
   of {EPOLLHUP, deassign, deinit} fire concurrently.  This is safe to
   call from the waitqueue callback, which runs with wqh->lock held and
   IRQs disabled and therefore cannot take irqfds_lock.
 - acrn_irqfd_deassign() flushes vm->irqfd_wq before returning so the
   eventfd is fully detached on return.  acrn_irqfd_deinit() deactivates
   every irqfd, flushes the workqueue and only then destroys it, so no
   path can queue_work() onto a torn-down workqueue.
 - acrn_irqfd_assign() now installs the eventfd waitqueue entry and
   publishes the irqfd to vm->irqfds under irqfds_lock, so the irqfd is
   never visible to deassign/deinit before its waitqueue entry is in
   place, and any EPOLLHUP that fires in the assign window queues
   cleanup work that blocks on irqfds_lock until publication is done.

### CVE-2026-97429

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:20.907 |

In the Linux kernel, the following vulnerability has been resolved:

drm/amdkfd: fix UAF race in destroy_queue_cpsch

wait_on_destroy_queue() drops locks to wait for queue resume, allowing
a concurrent destroy to free the queue. Use is_being_destroyed flag to
serialize destruction.

### CVE-2026-97421

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:19.993 |

In the Linux kernel, the following vulnerability has been resolved:

RDMA/umem: Be careful about boundary conditions in ib_umem_find_best_pgsz()

Several corner cases, especially important on 32 bits:

- umem->iova is u64, the function argument should pass in u64 or
  iova will be truncated
- Check that the length is not too large for the iova
- Check that lengths > 4G don't overflow the GENMASK

### CVE-2026-97415

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:19.223 |

In the Linux kernel, the following vulnerability has been resolved:

btrfs: tree-checker: validate names in ROOT_REF and ROOT_BACKREF

ROOT_REF and ROOT_BACKREF items contain a struct btrfs_root_ref followed
by the subvolume name. Several readers assume that this layout is already
valid and then use the on-disk name length directly. A corrupted item can
therefore make those readers address bytes outside the item, and
BTRFS_IOC_GET_SUBVOL_INFO can copy too many bytes into its fixed-size UAPI
name buffer.

Validate ROOT_REF and ROOT_BACKREF items in tree-checker before any reader
uses them. Reject records that do not contain a non-empty name, whose
name_len does not exactly describe the remaining item payload, or whose
name exceeds BTRFS_NAME_LEN.

For BTRFS_IOC_GET_SUBVOL_INFO, copy only the validated on-disk name_len
instead of deriving the copy length from the item size. The ioctl result is
zeroed when allocated. That leaves the existing trailing zero byte
untouched.

### CVE-2026-93817

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:15.233 |

In the Linux kernel, the following vulnerability has been resolved:

perf: Fix addr_filter_ranges lifetime

Lee Jia Jie reported that since event::addr_filter_ranges is used
under RCU, it should be RCU freed.

### CVE-2026-93813

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:14.763 |

In the Linux kernel, the following vulnerability has been resolved:

btrfs: tree-checker: validate INODE_REF's namelen

[BUG]
A crafted btrfs image can trigger the following crash:

  BUG: unable to handle page fault for address: ffffd1dc42884000
  #PF: supervisor write access in kernel mode
  #PF: error_code(0x0002) - not-present page
  CPU: 9 UID: 0 PID: 1034 Comm: poc Not tainted 7.1.0-rc4-custom+ #383 PREEMPT(full)  46af0a92938a63be7132e0dfd71e62327c51d5c2
  Hardware name: QEMU Standard PC (Q35 + ICH9, 2009), BIOS unknown 02/02/2022
  RIP: 0010:memcpy+0xc/0x10
  Call Trace:
   <TASK>
   read_extent_buffer+0xe4/0x100 [btrfs 3cf0785dd58fec8c5ff84633b772f17ce1f92a8f]
   btrfs_get_name+0x15e/0x1e0 [btrfs 3cf0785dd58fec8c5ff84633b772f17ce1f92a8f]
   reconnect_path+0x165/0x390
   exportfs_decode_fh_raw+0x337/0x400
   ? drop_caches_sysctl_handler+0xb0/0xb0
   </TASK>
  ---[ end trace 0000000000000000 ]---
  RIP: 0010:memcpy+0xc/0x10
  Kernel panic - not syncing: Fatal exception

[CAUSE]
TThe crafted image has the following corrupted INODE_REF item:

         item 9 key (258 INODE_REF 257) itemoff 11544 itemsize 4106
         	index 2 namelen 4096 name: d\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000

The itemsize matches the namelen, but the namelen is 4096, way larger
than normal name length limit (BTRFS_NAME_LEN, 255).

Meanwhile the memory of the @name is only 255 byte sized, this will cause
out-of-boundary access, and cause the above crash.

[FIX]
Add extra namelen verification for INODE_REF, just like what we have
done in ROOT_REF checks.

Now the crafted image can be rejected gracefully:

 BTRFS critical (device dm-2): corrupt leaf: root=5 block=30572544 slot=14 ino=259, invalid inode ref name length, has 4096 expect [1, 255]
 BTRFS error (device dm-2): read time tree block corruption detected on logical 30572544 mirror 2

[ Rebase, add a Link: tag, add an simple cause analyze ]

### CVE-2026-93798

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:12.607 |

In the Linux kernel, the following vulnerability has been resolved:

btrfs: fix reloc root cleanup in merge_reloc_roots()

If the root we got has zero root refs in its root item, we are resetting
the root's ->reloc_root without using barriers like we do everywhere else.
Sashiko complained about this while reviewing another patch, and it's
correct (see the Link tag below).

Also, we should not clear BTRFS_ROOT_DEAD_RELOC_TREE from the root unless
the root points to the reloc root we have.

Fix this by using clear_reloc_root(), which issues the memory barrier
after setting the root's ->reloc_root to NULL and before clearing the bit
BTRFS_ROOT_DEAD_RELOC_TREE from the root.

### CVE-2026-93782

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:10.793 |

In the Linux kernel, the following vulnerability has been resolved:

vhost-scsi: flush backend after device ioctls

vhost-scsi translates guest response descriptors into userspace iovecs
when commands are submitted.  Target-core completes those commands
asynchronously, so VHOST_SET_MEM_TABLE can replace the memory table while
an in-flight command still retains response iovecs translated through the
old table.

If the old mapping is reused after VHOST_SET_MEM_TABLE returns, command
completion can write the response to an unrelated userspace object.

Flush the vhost-scsi backend after vhost_dev_ioctl() handles a device
ioctl.  This waits for in-flight commands that can still use the old
response iovecs before the ioctl returns.

### CVE-2026-93288

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:10.070 |

In the Linux kernel, the following vulnerability has been resolved:

netfilter: nfnetlink_log: wait for rcu grace period before freeing pernet state

sashiko reports: "nfnl_log_net_exit() calls nf_log_unset(), which
clears the logger pointer without an RCU grace period.  Immediately after,
ops_free_list() frees the per-net state while concurrent packets might
still be executing nf_log_packet() under rcu_read_lock()."

Clear the pointer via .pre_exit to make sure rcu readers have completed
before pernet storage is free'd.  The change in nf_log_syslog.c is only
done for consistency: it doesn't use pernet data.

### CVE-2026-93287

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:09.930 |

In the Linux kernel, the following vulnerability has been resolved:

i2c: smbus: reject oversized block transfers in the common path

The SMBus block transfer length data->block[0] is validated in
i2c_smbus_xfer_emulated() but that check runs too late for tracepoints
and is skipped entirely when the adapter provides a native smbus_xfer
implementation. This allows user-controlled oversized block lengths to
reach tracepoint memcpy calls and driver callbacks unchecked.

Add an early validation in __i2c_smbus_xfer() that rejects block
transfers whose caller-supplied length is zero or exceeds
I2C_SMBUS_BLOCK_MAX before any tracepoint fires or driver callback
runs. data->block[0] is filled in by the device on SMBus block reads,
so the check is scoped to operations where the length is actually
supplied by the caller. This is consistent with the existing -EINVAL
convention in the emulated path and protects all downstream consumers
at once: the smbus_write tracepoint, all native smbus_xfer driver
implementations, and the emulated path.

Two distinct bugs are fixed by this change:

Bug 1: smbus_write tracepoint OOB (include/trace/events/smbus.h)
  trace_smbus_write() fires before any validation and copies
  data->block[0]+1 bytes into a 34-byte event buffer. With
  block[0]=0xfe the tracepoint copies 255 bytes, overflowing by 221.

 BUG: KASAN: stack-out-of-bounds in trace_event_raw_event_smbus_write+0x27c/0x530
 Read of size 255 at addr ffff88800d98fcf8 by task poc_smbus/91
 Call Trace:
  <TASK>
  __asan_memcpy+0x23/0x80
  trace_event_raw_event_smbus_write+0x27c/0x530
  __i2c_smbus_xfer+0x43a/0xa40
  i2c_smbus_xfer+0x19e/0x340
  i2cdev_ioctl_smbus+0x38f/0x7f0
  i2cdev_ioctl+0x35e/0x680
  __x64_sys_ioctl+0x147/0x1e0
  do_syscall_64+0xcf/0x15a0
  entry_SYSCALL_64_after_hwframe+0x76/0x7e
  </TASK>

Bug 2: i2c-stub I2C_SMBUS_I2C_BLOCK_DATA OOB (drivers/i2c/i2c-stub.c)
  stub_xfer() implements .smbus_xfer directly and only clamps
  block[0] against 256-command, not I2C_SMBUS_BLOCK_MAX. With
  block[0]=0xff and command=0 the loop accesses block[1+i] for
  i up to 254, far past the 34-byte union.

 UBSAN: array-index-out-of-bounds in drivers/i2c/i2c-stub.c:223:44
 index 34 is out of range for type '__u8 [34]'
 Call Trace:
  <TASK>
  __ubsan_handle_out_of_bounds+0xd7/0x120
  stub_xfer+0x1971/0x198f [i2c_stub]
  __i2c_smbus_xfer+0x306/0xa40
  i2c_smbus_xfer+0x19e/0x340
  i2cdev_ioctl_smbus+0x38f/0x7f0
  i2cdev_ioctl+0x35e/0x680
  __x64_sys_ioctl+0x147/0x1e0
  do_syscall_64+0xcf/0x15a0
  entry_SYSCALL_64_after_hwframe+0x76/0x7e
  </TASK>

Both traces reproduced on v7.0-rc6+i2c/for-current with KASAN+UBSAN.

### CVE-2026-93277

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:24.907 |

In the Linux kernel, the following vulnerability has been resolved:

RDMA/bnxt_re: Validate udata before executing commands

The destroy callbacks currently zero the udata output after tearing down
driver resources. If the userspace access fails, uverbs preserves the
uobject and allows the destroy callback to run again, even though the
driver resource has already been freed.

Call ib_no_udata_io() before teardown so udata failures are detected
while the resource is still intact, then return success after teardown
completes.

As part of this change, move ib_respond_empty_udata() to the start of
the create and modify flows. While this is not strictly required for
general create flows, as the core layer unwinds uobjects on failure, it
is necessary for create AH. In _rdma_create_ah(), the HW object is
otherwise leaked.

### CVE-2026-93262

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:22.927 |

In the Linux kernel, the following vulnerability has been resolved:

md/raid5-ppl: fix use-after-free in ppl_do_flush()

The loop in ppl_do_flush() continues iterating after calling
ppl_io_unit_finished(), touching io->pending_flushes and leading to a
use-after-free.

Add a break statement to stop the loop once io is freed.

### CVE-2026-93250

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:21.187 |

In the Linux kernel, the following vulnerability has been resolved:

vxlan: mdb: Fix use-after-free in vxlan_mdb_flush()

vxlan_mdb_flush() iterates over the MDB entries using
hlist_for_each_entry_safe(), which only tolerates the removal of the
current entry. Contrary to the comment above the loop, the removal of an
entry can trigger the removal of another entry.

Flushing the remotes of a (*, G) entry also removes the (S, G) entries
that were created for its source list, once they are left without
remotes:

vxlan_mdb_remotes_flush()
-> vxlan_mdb_remote_del()
   -> vxlan_mdb_remote_srcs_del()
      -> vxlan_mdb_remote_src_del()
         -> vxlan_mdb_remote_src_fwd_del()
            -> __vxlan_mdb_del()
               -> vxlan_mdb_entry_put()

Such an entry can be located after the (*, G) entry in the list, as
vxlan_mdb_entry_get() returns an existing entry without moving it to the
head of the list. This order is obtained by adding the (S, G) entry
before the (*, G) entry, the latter with NLM_F_REPLACE, as the addition
of the source otherwise fails with -EEXIST. The (S, G) entry is then the
entry saved by hlist_for_each_entry_safe() and it is freed while the
(*, G) entry is processed. The next iteration calls hlist_del() on it
again, writing LIST_POISON1 to LIST_POISON2 [1].

Besides device deletion, the flush is also reachable from RTM_DELMDB
with NLM_F_BULK.

Fix by re-reading the next entry after the remotes were flushed. The
current entry cannot be removed by this flush, as source lists can only
be configured on (*, G) entries and the removed entries are (S, G)
entries. It is therefore still linked and its next pointer reflects the
removals.

[1]
BUG: KASAN: wild-memory-access in vxlan_mdb_entry_put.part.0+0x328/0x588
Write of size 8 at addr dead000000000122 by task ip/327

CPU: 3 UID: 1000 PID: 327 Comm: ip Not tainted 7.2.0-rc7 #2 PREEMPT
Call trace:
 vxlan_mdb_entry_put.part.0+0x328/0x588
 vxlan_mdb_flush+0x1d8/0x25c
 vxlan_mdb_fini+0x8c/0x100
 vxlan_uninit+0x1c/0x7c
 unregister_netdevice_many_notify+0x954/0xd4c
 rtnl_dellink+0x210/0x530
 rtnetlink_rcv_msg+0x434/0x4d0
 netlink_rcv_skb+0xc4/0x204
 rtnetlink_rcv+0x18/0x24
 netlink_unicast+0x4b8/0x548
 netlink_sendmsg+0x29c/0x560
 ____sys_sendmsg+0x390/0x3ec
 ___sys_sendmsg+0x114/0x188
 __sys_sendmsg+0xf0/0x178
 __arm64_sys_sendmsg+0x48/0x60
 invoke_syscall.constprop.0+0x58/0x180
 el0_svc_common.constprop.0+0x74/0x140
 do_el0_svc+0x30/0x40
 el0_svc+0x38/0x98
 el0t_64_sync_handler+0xa0/0xe4
 el0t_64_sync+0x198/0x19c

### CVE-2026-93237

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:19.447 |

In the Linux kernel, the following vulnerability has been resolved:

LoongArch: Add DIRECT_MAP_PHYSMEM_END definition

get_free_mem_region() and mhp_get_pluggable_range() bound their search
to DIRECT_MAP_PHYSMEM_END. LoongArch does not define it, so the fallback
in include/linux/mm.h applies: under CONFIG_SPARSEMEM_VMEMMAP it is
(1ULL << MAX_PHYSMEM_BITS) - 1, a compile-time constant that does not
adapt to the CPU's physical address space bits (cpu_pabits, probed from
CPUCFG1).

The vmemmap window only covers physical space below 2^(cpu_pabits+1)
(i.e. VMEMMAP_SIZE), so on CPUs with fewer physical address bits than
MAX_PHYSMEM_BITS the fallback allows get_free_mem_region() to return
a ZONE_DEVICE region outside the vmemmap window; vmemmap_populate() then
wraps the memmap range around and maps it into low memory, silently
corrupting the page tables. The same search also picked the top-of-
address-space region that crashed memmap_init_zone_device() with amdkfd
on Loongson-3C6000 in 6.16 [1]; the commit 2969b42c8f99 ("LoongArch/mm:
align vmemmap to maximal folio size") keeps that region in bounds on
current Loongson-3C6000 configs, but CPUs with smaller cpu_pabits (e.g.
the Loongson-2K series) are still affected.

Define DIRECT_MAP_PHYSMEM_END as the vmemmap-covered physical range,
(1ULL << (cpu_pabits + 1)) - 1, capped at (1ULL << MAX_PHYSMEM_BITS) - 1
under CONFIG_SPARSEMEM, similar to the commit f3336b48cf9d ("riscv: mm:
Define DIRECT_MAP_PHYSMEM_END").

[1] https://lore.kernel.org/amd-gfx/20250814032153.227285-1-jeffbai@aosc.io/

### CVE-2026-85496

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-340` |
| Published | 2026-09-24T20:17:32.890 |

The Botslab G980H dash camera firmware generates session identifiers using a small sequential value space rather than a suitably unpredictable source. An unauthenticated attacker with adjacent network access and knowledge that an active session exists could potentially determine a valid session identifier and use it to bypass intended authorization controls.

### CVE-2026-97454

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:23.823 |

In the Linux kernel, the following vulnerability has been resolved:

ACPICA: add boundary checks in acpi_ps_get_next_field()

Add boundary checks in acpi_ps_get_next_field() to prevent out-of-bounds
access.

### CVE-2026-97448

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:23.110 |

In the Linux kernel, the following vulnerability has been resolved:

ACPICA: Add validation for node in acpi_ns_build_normalized_path()

Add validation for node in acpi_ns_build_normalized_path()
to prevent use-after-free vulnerabilities.

### CVE-2026-97445

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:22.773 |

In the Linux kernel, the following vulnerability has been resolved:

ACPICA: Enhance buffer validation in acpi_ut_walk_aml_resources()

Enhance buffer validation in acpi_ut_walk_aml_resources() to prevent
buffer overflows.

### CVE-2026-97444

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:22.663 |

In the Linux kernel, the following vulnerability has been resolved:

ACPICA: add boundary checks in two places

Add boundary checks in acpi_ps_get_next_namestring() and
acpi_ps_peek_opcode() to prevent out-of-bounds access.

### CVE-2026-97428

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:20.797 |

In the Linux kernel, the following vulnerability has been resolved:

drm/amdgpu: harden FRU PIA parsing with bounded helpers

Replace the open-coded TLV walk with fru_pia_advance()
and fru_pia_copy_field() helpers that bound every read
by the actual EEPROM data length, preventing out-of-bounds
reads on truncated or malformed FRU data.

### CVE-2026-88390

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-24T17:17:08.143 |

An out-of-bounds write vulnerability in jslGetTokenValueAsString() in Espruino 2v29 (commit bffc6d0) allows crafted JavaScript input containing an overlong token to trigger a one-byte write beyond the JsLex.token buffer in RELEASE/NO_ASSERT builds. The out-of-bounds write corrupts the adjacent tokenValue pointer, resulting in memory corruption and potentially causing application crashes or denial of service.

### CVE-2026-79764

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-24T17:17:06.510 |

Termix is a web-based server management platform with SSH terminal, tunneling, and file editing capabilities. From 2.5.0 until 2.5.1, the /homepage/proxy endpoint accepts an authenticated user's url query parameter and passes it to http.get or https.get without destination restrictions. In src/backend/database/routes/homepage-proxy-routes.ts, new URL performs only syntactic validation, allowing requests to loopback, RFC1918, link-local, and cloud metadata destinations. The endpoint returns the complete fetched JSON response, so a low-privilege or self-registered account can exfiltrate internal service data and cloud credentials. This issue is fixed in version 2.5.1.

### CVE-2026-93265

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:23.340 |

In the Linux kernel, the following vulnerability has been resolved:

PCI/pwrctrl: tc9563: Fix parsing the integrated Ethernet MAC Endpoint node

DSP3 has an integrated Ethernet MAC Endpoint which has its own set of
config registers for configuring settings such as ASPM. The Endpoint device
has two physical functions and those two functions share the same settings.

Parse the Endpoint node under DSP3 instead of parsing both functions.  The
existing parsing logic also has one OOB issue as parsing both functions
will result in accessing past the tc9563_pwrctrl->cfg array.

### CVE-2026-84893

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-25T14:17:19.913 |

IBM Guardium Data Protection 12.2 is vulnerable to SQL injection in the PESI service. An authenticated attacker could exploit this vulnerability to access sensitive information in the internal database.

### CVE-2026-87720

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613;CWE-706;CWE-863` |
| Published | 2026-09-24T22:17:02.170 |

Incorrect Authorization (CWE-863) in project name normalization (ProjectUtil.stripGitSuffix) and ProjectCache eviction logic (ProjectCacheImpl) in Gerrit Code Review versions 2.16.0 through 3.12.9, 3.13.0 through 3.13.8, and 3.14.0 through 3.14.2 allows an authenticated user (or an unauthenticated user if the repository was previously public) to cause unauthorized disclosure of private repository content and durable restoration of revoked project-owner administrative privileges via crafted requests using repeated .git suffixes (such as project.git.git) across REST APIs, Gitiles, or SSH Git commands. Because Gerrit strips only a single terminal .git suffix when constructing the logical ProjectCache key while JGit (FileKey.lenient) resolves the suffixed alias to the same canonical bare repository on disk, revoking read access or removing owner rules on the canonical project name fails to evict the cached alias ProjectState during the cache validity window, enabling reads of newly created private commits or writes to refs/meta/config. This issue is fixed in Gerrit Code Review versions 3.12.10, 3.13.9, and 3.14.3.

### CVE-2026-63203

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-24T16:17:08.700 |

Logto is the modern, open-source auth infrastructure for SaaS and AI apps. From 1.31.0 until 1.42.0, the Account API handlers in packages/core/src/routes/account/third-party-tokens.ts allow a caller holding a same-user access token with only the openid scope to retrieve stored social or enterprise SSO provider access tokens through GET /api/my-account/identities/{target}/access-token or GET /api/my-account/sso-identities/{connectorId}/access-token. The handlers authenticate the user but do not require the identities scope that protects neighboring identity-detail operations, bypassing the intended Account API consent boundary. Exploitation requires federated token-set storage to be enabled and the affected user to have authenticated through a supported connector. A low-trust application can use the disclosed provider token against upstream APIs within that token's granted scopes. This issue is fixed in version 1.42.0.

### CVE-2026-85029

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-25T14:17:20.050 |

IBM Guardium Data Protection 12.2 could allow a remote attacker to obtain sensitive information, delete arbitrary files, or execute arbitrary code due to improper limitation of a pathname to a restricted directory.

### CVE-2026-84884

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-256` |
| Published | 2026-09-25T14:17:19.770 |

IBM Guardium Data Protection 12.2 stores internal REST service-account passwords in a reversible plaintext-equivalent format. An authenticated attacker who gains access to the stored credential could recover the password and obtain an administrative REST access token.

### CVE-2026-52622

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-25T13:17:14.787 |

An issue in Wellav Technologies Co., Ltd Wellav WES Emergency Broadcast Terminal WES100, WES270, WES280, and WES290 before 08-08-2023 allows a remote attacker to obtain sensitive information via the global API request wrapper function

### CVE-2026-92560

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-25T09:17:06.587 |

A pre-authentication attacker could leverage type size/count handling to cause excessive allocation leading to potential denial of service.

This issue affects Apache Qpid Broker-J: through 10.1.0.

Users are recommended to upgrade to version 10.1.1, which fixes the issue.

### CVE-2026-92550

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-25T09:17:06.447 |

A pre-authentication attacker could leverage type size/count handling to cause excessive allocation leading to potential denial of service.

This issue affects Apache Qpid Broker-J: through 10.1.0.

Users are recommended to upgrade to version 10.1.1, which fixes the issue.

### CVE-2026-89406

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-25T08:16:40.803 |

The Modula Image Gallery – Photo Grid & Video Gallery plugin for WordPress is vulnerable to unauthorized disclosure of private gallery contents in versions up to, and including, 3.0.1. This is due to the Modula_Meta::add_metas() function being hooked to wp_head on every frontend request and looking up any post via get_post( $_GET['modula_gallery_id'] ) without verifying the gallery's post_status or the requester's capability to read it — the gallery-side input guard is bugged (empty('modula_gallery_id') tests a nonempty string literal instead of the GET parameter, so it is always false), the only object validation is a post_type === 'modula-gallery' check, and no is_user_logged_in()/current_user_can('read_post', $gallery_id) check is performed. This makes it possible for unauthenticated attackers to enumerate private modula-gallery posts and their member attachments and recover the image's title, description, dimensions, and original upload URL via Open Graph/Twitter meta tags emitted in the response, which then allows direct unauthenticated download of the original private image bytes.

### CVE-2026-13456

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-25T08:16:39.970 |

The WP Maps – Google Maps,OpenStreetMap,Mapbox,Store Locator,Listing,Directory & Filters plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 4.9.8 via the 'page' parameter parameter. This makes it possible for authenticated attackers, with subscriber-level access and above, to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included.

### CVE-2026-96749

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-24T19:17:20.963 |

An integer overflow in the BSON document encoding component of the MongoDB Python Driver's bundled native extension may occur when a single document is built from an unusually large amount of caller-supplied data. Size arithmetic is performed in a signed 32-bit type, and the guard meant to catch the overflow is written in a form whose behavior is not defined by the C language standard. A party with no privileges who can place a very large value into data that an application encodes may, depending on how the native extension was built, cause a write outside the bounds of an allocated buffer inside the application's own process.

### CVE-2026-57440

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-79;CWE-80` |
| Published | 2026-09-24T19:17:14.630 |

The EmbedVideo Extension is a MediaWiki extension which adds a parser function called #ev and various parser tags for embedding video clips from various video sharing services. Prior to 4.1.0, with $wgEmbedVideoRequireConsent disabled (not the default), the urls for videos are passed into an iframe src attribute without sanitization. When given a malformed url or id, the src attribute can be escaped via double quotes, allowing for html/javascript injection. Version 4.1.0 contains a patch.

### CVE-2026-71540

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-24T18:18:31.340 |

Wazuh is an open-source security platform providing unified XDR and SIEM protection for endpoints and cloud workloads. From 3.9.0 until 4.14.7, wazuh-clusterd in framework/wazuh/core/cluster/common.py allocates a payload buffer using the size declared in a 20-byte cluster protocol header before Fernet decryption validates the peer. An unauthenticated network peer can declare a payload of up to 256 MiB, stop sending after the header, and retain that allocation until the TCP connection closes. The cluster listener has no application-level per-source connection budget in affected versions, allowing concurrent sockets to multiply memory consumption and potentially terminate the cluster process, disrupt synchronization, and interrupt distributed API forwarding. This issue is fixed in version 4.14.7.

### CVE-2026-63645

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-24T18:17:19.053 |

OpenObserve is a cloud-native observability platform. Prior to 0.90.3, OpenObserve registers the /config/runtime endpoint without authentication and serializes the complete server configuration after applying the hide_sensitive_fields keyword filter. The filter does not recognize dsn or creds field names, so meta_postgres_dsn, meta_postgres_ro_dsn, meta_ddl_dsn, and usage_reporting_creds can be returned in plaintext to an unauthenticated network client. PostgreSQL deployments can expose database credentials, and the same response can disclose the root administrator email address, internal NATS address, filesystem layout, and other deployment details. This issue is fixed in version 0.90.3.

### CVE-2026-61816

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-24T18:17:17.303 |

zbateson/mail-mime-parser is a mail mime parser alternative to PHP's imap* functions and Pear libraries for reading messages in Internet Message Format RFC 822. Starting in version 2.0.0 and prior to version 3.0.6 and 4.0.2, an uncontrolled resource consumption / algorithmic complexity vulnerability (CWE-400) affects any application that parses untrusted email with this library. Three independent parsing paths are super-linear in cost, so a byte-size cap on the caller side does **not** bound the work done.  A crafted message under 2 MB can consume seconds of CPU or hundreds of megabytes to multiple gigabytes of memory (leading to an out-of-memory kill), enabling denial of service. The parse is lazy, but the cost is paid on the first `getAllParts()` or content read. This is fxed in 4.0.2 and 3.0.6. The fixes add configurable limits on multipart nesting depth and on header count / total header size (recording a parse error past the threshold rather than throwing), and change sibling append to O(n). Users should upgrade to one of these (or later) versions. Versions 2.x are also affected but are end-of-life and will not receive patches; users on those lines should upgrade to a fixed release. (Versions prior to 2.0 used a different parser and are not affected by all three paths.) These costs are super-linear, so an input byte-size cap alone does not bound them. Until upgrading, restrict exposure of the parser to untrusted input, and run parsing under a constrained memory_limit and execution time limit so a malicious message fails its own request rather than exhausting the host.

### CVE-2026-61782

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-24T18:17:16.333 |

Rsdoctor is a build analyzer tailored for projects built with Rspack. Prior to version 1.5.16, the default Rsdoctor report HTTP server started by `@rsdoctor/rspack-plugin` binds to all network interfaces (`0.0.0.0`) and serves a `POST /api/data/key` endpoint with no authentication and wildcard CORS (`Access-Control-Allow-Origin: *`). Any network-adjacent or remote attacker can send a single unauthenticated request to retrieve the full source code of all compiled JavaScript modules (`moduleCodeMap`), serialized build configuration (`configs`), error details, and other sensitive build metadata. This server is enabled by default in non-CI environments, requiring no special configuration from the victim developer. Version 1.5.16 patches the issue.

### CVE-2026-97508

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:28.650 |

In the Linux kernel, the following vulnerability has been resolved:

thunderbolt: Set tb->root_switch to NULL when domain is stopped

Similarly what we do with the firmware connection manager. This makes
tb_xdp_handle_request() return error to the remote host. However, we
need to make sure we keep the uuid alive so that we can reply until the
whole domain is released.

### CVE-2026-97417

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:19.457 |

In the Linux kernel, the following vulnerability has been resolved:

netfilter: nf_conntrack: use get_unaligned_be32() in tcp_sack()

The timestamp-only fast path dereferences the option stream as
*(__be32 *)ptr, which assumes 4-byte alignment that the TCP option
stream does not guarantee. Use get_unaligned_be32() instead, which
reads the value safely and already returns host byte order, so the
htonl() on the comparison constant can be dropped.

This matches the existing get_unaligned_be32() use later in the same
function.

### CVE-2026-94613

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-24T17:17:17.723 |

authentik is an open-source identity provider. Prior to 2026.2.7, 2026.5.7, and 2026.8.2, an unauthenticated attacker can submit a malformed SAML message to an authentik deployment using SAML in either the identity-provider or SAML source role. The message can stop the worker handling /application/saml/* or /source/saml/*, causing the requests assigned to that worker to fail. Worker process termination and automatic restart do not destroy database-backed sessions, but continued malicious messages can cause a sustained share of legitimate traffic to fail. Other protocol implementations are not affected. This issue is fixed in versions 2026.2.7, 2026.5.7, and 2026.8.2.

### CVE-2026-93830

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:16.740 |

In the Linux kernel, the following vulnerability has been resolved:

net: stmmac: xgmac2: disable RBUE in default RX interrupt mask

Enabling the RX Buffer Unavailable (RBUE) interrupt is counterproductive
and can trigger a MAC interrupt storm under heavy RX pressure. When the
DMA runs out of RX descriptors it fires RBUE continuously until software
refills the ring.

However, RBUE is redundant: the normal RX completion interrupt (RIE)
already triggers NAPI, which processes completed descriptors and refills
the ring, causing the DMA to resume. The RBUE handler itself only sets
handle_rx - the same outcome as RIE.

On Agilex5 under heavy RX pressure, the MAC interrupt (which includes
RBUE) was observed firing 1,821,811,555 times against only 2,618,627
actual RX completions - a ~695x ratio - confirming the severity of the
storm.

RBUE does not provide OOM recovery. If page_pool is exhausted,
stmmac_rx_refill() cannot advance the DMA tail pointer, the DMA stays
suspended, and RBUE fires again on the next NAPI completion - a storm
with no forward progress. This patch trades that storm for a clean
stall with the same RX outcome. Proper OOM recovery is a pre-existing
gap outside the scope of this fix.

Note: as a consequence of disabling RBUE, the rx_buf_unav_irq ethtool
counter will always read 0 on XGMAC2 devices. This behaviour is already
inconsistent across DWMAC core versions.

Remove RBUE from XGMAC_DMA_INT_DEFAULT_EN and XGMAC_DMA_INT_DEFAULT_RX
to prevent the interrupt storm while keeping normal RX handling intact.

### CVE-2026-93826

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:16.297 |

In the Linux kernel, the following vulnerability has been resolved:

HID: hidpp: fix potential UAF in hidpp_connect_event()

If input_register_device() fails, we call input_free_device(), but keep
stale pointer to the old device in hidpp->input, which could potentially
lead to UAF. Fix that by resetting it to NULL before returning from
hidpp_connect_event().

### CVE-2026-88382

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770;CWE-789` |
| Published | 2026-09-24T17:17:07.670 |

hiredis commit 29ea279 (post-v1.5.0) contains an uncontrolled memory allocation vulnerability in its RESP aggregate parser.

### CVE-2026-88376

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-24T17:17:07.313 |

Bento4 1.6.0.0 contains an integer underflow vulnerability in AP4_AvccAtom::Create() and AP4_HvccAtom::Create(). A specially crafted MP4 file containing an avcC or hvcC atom with a declared size smaller than the atom header size can cause the payload-size calculation to wrap to a large unsigned value. The resulting invalid buffer allocation and copy operations can cause application termination, leading to denial of service.

### CVE-2026-88372

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-24T17:17:07.083 |

libsndfile 1.2.2 contains an integer overflow vulnerability in mat4_read_header() when parsing crafted MAT4 (MATLAB v4) files.

### CVE-2026-88368

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-681` |
| Published | 2026-09-24T16:17:13.730 |

NanoSVG commit 239e102ec contains an incorrect numeric conversion vulnerability in the rasterizer's nsvg__addActive() function. A specially crafted SVG document containing sufficiently large geometry coordinates can cause fixed-point-scaled edge coordinates to exceed the range representable by int. The rasterizer subsequently converts these values to int without range validation, resulting in undefined behavior and possible process termination, leading to denial of service.

### CVE-2026-88357

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1335` |
| Published | 2026-09-24T16:17:12.957 |

nDPI 5.1.0 contains a memory access issue in the DNS dissector and serializer deserialization code. Specially crafted network input can cause byte-buffer addresses at odd offsets to be cast to uint16_t or wider integer pointers and directly dereferenced without alignment checks. This results in undefined behavior and can cause process termination in UBSan-instrumented builds or on strict-alignment architectures, leading to denial of service.

### CVE-2026-75907

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287;CWE-294;CWE-613` |
| Published | 2026-09-24T16:17:10.387 |

The door access control on a Norwegian Cruise Line asset grants entry based only on the credential's static 7-byte UID stored on an NTAG212 NFC chip. A UID is a manufacturer serial number sent in the clear on every read and is not intended to be secret or to authenticate the holder. Validating on the UID of the NTAG212 NFC chip alone is identification, not authentication, and the credential has no challenge-response capability that would resist copying.

### CVE-2026-51995

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-24T15:17:23.087 |

An issue in geelen mcp-remote 0.1.32 through 0.1.38 allows a remote attacker to obtain sensitive information via the src/lib/authorization-server-metadata.ts, src/lib/utils.ts components

### CVE-2026-97737

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-25T05:17:07.760 |

In Wakapi before 2.17.6, the user caching service allows a lookup to be resolved in an unintended lookup context, leading to account takeover.

### CVE-2026-61788

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-184;CWE-636;CWE-863` |
| Published | 2026-09-24T18:17:16.837 |

DBHub is a database MCP server for Postgres, MySQL, SQL Server, Oracle, MariaDB, SQLite. Prior to version 0.22.6, setting `readonly = true` on the `execute_sql` tool does not make the connection read-only. The connectors are written to set PostgreSQL `default_transaction_read_only=on` (and open SQLite in `readOnly` mode), but that code is gated on a config value that is never populated, so it never runs. The only thing left enforcing read-only is a classifier that inspects the first keyword of each statement. Any `SELECT` that writes or has side effects through a function call passes it. With an ordinary role this allows sequence tampering; with a privileged role it allows writing arbitrary files on the server (`lo_export`), reading arbitrary host files (`pg_read_file`), and remote code execution (`dblink` + `COPY ... TO PROGRAM`). The HTTP transport is unauthenticated and binds to `0.0.0.0` by default, so this is reachable by any network caller of `/mcp`. Version 0.22.6 patches the issue.

### CVE-2026-57178

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-347` |
| Published | 2026-09-24T18:17:14.970 |

Python Social Auth is a social authentication/registration mechanism. Prior to version 5.0.0, the `vk-app` backend accepted VK application callback data without verifying the callback signature when the `auth_key` parameter was omitted. Applications using this backend could treat unsigned attacker-controlled data as a verified VK identity. An attacker could choose callback fields such as `viewer_id`, `access_token`, `api_id`, and `api_result`, potentially allowing authentication as an arbitrary VK user ID. The issue affects only applications using the `vk-app` backend. The issue has been fixed in version 5.0.0 by requiring `auth_key` to be present and valid before callback data is trusted.

### CVE-2026-97474

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:24.547 |

In the Linux kernel, the following vulnerability has been resolved:

wifi: iwlwifi: mld: purge async notifications upon nic error

This fixes a kernel panic in reconfig failure:

1. we have a BSS connection
2. we have a NAN connection
3. FW error occurs
4. reconfig restores the BSS connection
5. however, restoring the NAN connection fails due to a FW error.
6. erroneously, ieee80211_handle_reconfig_failure is called and marks all
   interfaces as not-in-driver (will be fixed in a different patch).
7. mac80211 frees the links of the BSS connection but doesn't tell the
   driver about that, as it thinks that this vif is not in the driver.
8. in ieee80211_stop_device, *ALL* wiphy works are getting flushed
   (erroneously?)
9. Therefore, async_handlers_wk is being executed, processing the
   statistics notification that was received after we restored the BSS
   connection.
10. the notification handler dereferences fw_id_to_bss_conf[id], which is
    now a dangling pointer, as mac80211 already freed this link in (7).
11. On the first access to one of the links fields, we panic.

While this can and should be fixed by removing the call to
ieee80211_handle_reconfig_failure in (6), it is also not a good idea to
carry and maybe handle notifications from a dead FW.

We do purge the notifications when we stop the FW, but in reconfig
failure we stop the FW too late, after the notifications are processed.
In addition, async_handlers_wk can always be scheduled before the
reconfig work.

Purge the notifications immediately when transport notifies about a nic
error.

### CVE-2026-94612

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-345` |
| Published | 2026-09-24T17:17:17.557 |

authentik is an open-source identity provider. Prior to 2026.2.7, 2026.5.7, and 2026.8.2, an authentik SAML Source verifies an assertion's signature and validity period but does not ensure that the identity provider issued the assertion for that Source or in response to a login request from that Source. The SAML Source also does not record already accepted assertions, allowing replay. An unauthenticated actor who possesses such a valid assertion can use an assertion intended for another service provider or reuse an earlier assertion to authenticate as the user named by the assertion. Only SAML Sources are affected; SAML Providers and other Source types are not affected. This issue is fixed in versions 2026.2.7, 2026.5.7, and 2026.8.2.

### CVE-2026-93543

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-24T17:17:10.307 |

An out-of-bounds read in libXi's XI2 class parser in libXi before 1.8.4 could be used by malicious X servers to crash an attached X client.

### CVE-2026-93260

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:22.670 |

In the Linux kernel, the following vulnerability has been resolved:

powerpc/xive: propagate IPI init errors to prevent use-after-free

When xive_init_ipis() fails (e.g. irq_domain_alloc_irqs() fails),
the error path frees the global xive_ipis array.  However,
xive_smp_probe() previously ignored this failure and proceeded to
call xive_setup_cpu_ipi(), which dereferences the already-freed
xive_ipis pointer -- a use-after-free.

Now that xive_smp_probe() returns int (previous patch), propagate
the error from xive_init_ipis() and xive_setup_cpu_ipi() through
xive_smp_probe().  Check the return value in both pnv_smp_probe()
and pSeries_smp_probe() so that IPI setup is aborted cleanly on
failure, avoiding the use-after-free.

### CVE-2026-93225

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:17.857 |

In the Linux kernel, the following vulnerability has been resolved:

phy: fsl-imx8mq-usb: fix typec switch leak on probe error path

If probe fails after imx95_usb_phy_get_tca() succeeds, the typec
switch leaks because the only cleanup path was in .remove(), which
never runs on probe failure.

Use devm_add_action_or_reset() so the switch is cleaned up on both
probe failure and driver removal. The imx95_usb_phy_put_tca() is no
longer needed, it will be removed in .remove() too.

### CVE-2026-93901

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-25T08:16:41.837 |

The Optima Express IDX plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 8.7.5. This is due to the `provisionBlogCredentials()` function in `iHomefinderAdmin.php` being reachable via the `wp_ajax_nopriv_ihf_clear_cache` AJAX action — through the call chain `iHomefinderAjaxHandler::clearCache()` → `activateAuthenticationToken()` → `getAuthenticationInfo()` → `provisionBlogCredentials()` — with no capability check, nonce verification, or ownership validation, and the function unconditionally calling `$user->set_role('author')` on whichever WordPress account matches the hard-coded login `optima-express` via `get_user_by('login', 'optima-express')`. This makes it possible for unauthenticated attackers to escalate a pre-registered `optima-express` account to the Author role, gaining `publish_posts`, `upload_files`, and `edit_published_posts` capabilities, including access to the plugin's own `/wp-json/optima-express/v1/blog-post` REST endpoint. Exploitation requires open user registration to be enabled on the target site, and the attacker must register the `optima-express` username before the plugin has had the opportunity to provision that login for its own integration account.

### CVE-2026-61823

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-24T19:17:15.350 |

code16 Sharp is a Laravel-based framework for building content-management and administrative interfaces. Versions before 9.22.5 contain a stored cross-site scripting vulnerability in the rich-text editor because the HTML sanitizer permits the `srcdoc` attribute on iframe elements. Although markup inside `srcdoc` is HTML-encoded during sanitization, browsers decode attribute entities before interpreting the iframe document, allowing an authenticated user with permission to edit an Editor field to store executable JavaScript that runs when another user views the content. Successful exploitation can result in session hijacking, unauthorized actions, account takeover, privilege escalation, or disclosure of administrative data. Version 9.22.5 patches the vulnerability by removing `srcdoc` from the permitted iframe attributes. As a workaround, applications that cannot upgrade should manually sanitize all Editor field content and remove every iframe `srcdoc` attribute before storing or rendering it.

### CVE-2026-96750

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-24T16:17:27.610 |

MongoDB Compass can interpolate a database name without escaping into the initial input of its embedded MongoDB shell when a user opens the shell from that database's view. A user with privileges to create databases on a server that a Compass user connects to may, under specific conditions, have content evaluated as shell input within the Compass process, with that process's privileges. This requires the Compass user to open the shell for the affected database.

### CVE-2026-12559

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:U/V:D/RE:M/U:Red` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-24T15:17:18.350 |

A Stored Cross-Site Scripting (XSS) vulnerability has been identified in OpenText Vendor Invoice Management for SAP Solutions Capture Validation application. Under certain conditions, this issue could allow execution of unauthorized script content in a user's browser, potentially impacting confidentiality and integrity of information processed through the application.

### CVE-2026-85750

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-25T14:17:20.330 |

Piwigo before v16.4.0 is vulnerable to arbitrary file read and remote code execution in image upload handling when using the Imagick library due to insufficient validation and unsafe processing of user-supplied image files. By abusing format confusion (e.g., disguising SVG content as PNG), an attacker can trigger unintended interpretation of embedded SVG elements that reference local files. In more advanced scenarios, the Imagick support for Magick Scripting Language (MSL) may be abused to process attacker-controlled instructions, potentially leading to unauthorized server-side file writes and remote code execution, depending on configuration. This has been patched in 16.4.0.

### CVE-2026-96752

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T08:16:42.700 |

The Zero Spam for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Nested POST Array Keys via Contact Form 7 Integration in all versions up to, and including, 5.7.10 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is delivered by submitting a Contact Form 7 request with a nested POST array key containing arbitrary HTML or JavaScript — PHP parses the field name into a nested array key, which is stored verbatim in the zerospam_log.submission_data column when Zero Spam flags the submission as spam due to the absence of the zerospam_david_walsh_key field.

### CVE-2026-96568

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T08:16:42.567 |

The Restaurant Menu and Food Ordering plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'phone_number' parameter in all versions up to, and including, 2.4.14 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-95866

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T08:16:42.307 |

The User Profile Builder – Beautiful User Registration Forms, User Profiles & User Role Editor plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Avatar Field in all versions up to, and including, 4.0.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The zero-length multipart file branch in wppb_save_avatar_value() writes the raw request value directly to user meta, bypassing the wppb_save_attachment_id()/wppb_verify_attachment_id() validation path; the stored payload is later adopted as a WordPress attachment URL and rendered unescaped by wppb_default_fields_make_upload_button() when an administrator views the affected account.

### CVE-2026-95864

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T08:16:42.177 |

The Themify Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'css[fonts]' Parameter in all versions up to, and including, 7.8.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce required to reach the vulnerable endpoint is embedded in plain sight within the front-end page markup for all visitors, reducing the access control to a CSRF token rather than an authentication barrier and making the endpoint fully exploitable by unauthenticated attackers.

### CVE-2026-94573

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T08:16:42.047 |

The Repeater Fields for Elementor Forms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Repeater Field Value in all versions up to, and including, 2.2.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-93654

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T08:16:41.437 |

The Premium Packages – Sell Digital Products Securely plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'cart_items[][product_name]' Parameter in all versions up to, and including, 7.2.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The checkout REST route uses permission_callback set to __return_true and the invoice loader performs no order ownership check, meaning an unauthenticated attacker can both persist the payload and ensure it is renderable to any logged-in user who accesses the invoice.

### CVE-2026-84280

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T08:16:40.550 |

The Fancy Product Designer plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Shortcode Order 'elements[].title' Parameter in all versions up to, and including, 6.5.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload is written to the DOM via innerHTML within the beforeElementAdd JavaScript event handler when processing the elements[].title field from the stored order JSON, meaning execution occurs specifically when an administrator reviews shortcode orders in the WordPress admin panel.

### CVE-2026-96039

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T07:16:56.880 |

The BA Book Everything plugin for WordPress is vulnerable to Stored Cross-Site Scripting via first_name Parameter in all versions up to, and including, 1.8.27 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. An unauthenticated attacker can obtain the valid order_id, order_num, and order_hash credentials required to reach the vulnerable action_to_pay() handler simply by placing a guest booking through the public [babe-booking-form] shortcode, making the full exploit chain reachable without any account.

### CVE-2026-93303

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T07:16:55.890 |

The HT Contact Form – Drag & Drop Form Builder for WordPress plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via 'form_data' Rich Text Field via Draft Save/Resume in all versions up to, and including, 2.10.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires tricking a user into clicking an attacker-supplied draft resume URL, which the attacker constructs using the draft_key and access_token returned directly in the save response.

### CVE-2026-84281

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T07:16:55.013 |

The Fancy Product Designer plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'productTitle' in '_fpd_data' Order Item Meta in all versions up to, and including, 6.5.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The fpd_save_order AJAX action is registered for unauthenticated users via wp_ajax_nopriv_fpd_save_order with no nonce or capability check, and the strip_tags() sanitization applied at save time is bypassed by submitting JSON unicode escape sequences (e.g. \u003c, \u003e), which json_decode() silently converts back to literal angle brackets when the order is rendered in the admin view.

### CVE-2026-84279

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T07:16:54.890 |

The Fancy Product Designer plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'output_format' parameter in all versions up to, and including, 6.5.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the Pro Export/Genius feature to be enabled on the site, as the vulnerable fpd_pr_export AJAX action is only registered when that feature is active.

### CVE-2026-83591

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-25T07:16:54.747 |

The AMP for WP – Accelerated Mobile Pages plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via Regex Transformation in all versions up to, and including, 1.1.16 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The crafted payload uses only WordPress-permitted comment tags and attributes (an anchor with href and title), and the AMP sanitizer pipeline omits javascript: protocol blocking, meaning neither the comment save filter nor the AMP output stage removes the malicious URI introduced by the transformation.

### CVE-2026-61815

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-24T18:17:17.153 |

zbateson/mail-mime-parser is a mail mime parser alternative to PHP's imap* functions and Pear libraries for reading messages in Internet Message Format RFC 822. Prior to version 3.0.6 and 4.0.2, CRLF (carriage-return / line-feed) header injection (CWE-93) affecting any application that uses this library to build or forward MIME messages with an attacker-influenced attachment filename. Attachment filenames are interpolated into the `Content-Type` and `Content-Disposition` header values without stripping CR/LF, so a filename containing `\r\n` serializes as one or more additional, attacker-controlled header lines (for example a forged `Bcc:` that silently exfiltrates a copy of the outgoing message). The untrusted filename can come directly from parsed inbound mail, so no local construction is required — an application that re-attaches or re-sends a parsed filename is exposed. Versions 3.0.6 and 4.0.2 patch the issue. Versions 1.x and 2.x are also affected but are end-of-life and will not receive patches; users on those lines should upgrade to a fixed release. If upgrading is not immediately possible, strip CR and LF from any filename before passing it to attachment APIs, and from the result of getFilename() before reusing it in a constructed message — e.g. preg_replace('/[\r\n]+/', ' ', $filename).

### CVE-2026-91123

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-24T17:17:08.560 |

Discourse is an open-source discussion platform. Prior to 2026.1.8, 2026.6.3, 2026.7.2, and 2026.8.0, the iframe src traversal guard did not treat literal backslashes as path separators after decoded dot segments. A crafted source could therefore pass an allowed_iframes subpath check while browser URL normalization moved the iframe outside the intended allowed path. The resulting iframe could load content from a location that the administrator did not allow. This issue is fixed in versions 2026.1.8, 2026.6.3, 2026.7.2, and 2026.8.0.

### CVE-2026-97731

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-25T03:16:59.697 |

MinIO through 7aac2a2 does not verify that every x-amz-* header present on a request also appears in the client-supplied X-Amz-SignedHeaders list. extractSignedHeaders() in cmd/signature-v4-utils.go iterates only the claimed list and never enumerates the headers that actually arrived, and thus a header that arrives unsigned is neither hashed into the canonical request nor rejected. Because cmd/api-router.go dispatches CopyObject on the presence of x-amz-copy-source alone, the holder of a presigned PUT URL scoped to a single object can add that header to the unmodified URL and cause a server-side copy, executed as the signer, of any object the signing key can read. A grant to write one object becomes a read of every bucket that key can reach. Amazon S3 rejects the equivalent request with HTTP 403 AccessDenied. The minio/minio GitHub repository was archived in April 2026; pgsty/silo before 1233254 is also affected.

### CVE-2026-82708

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-24T21:18:50.330 |

The Botslab G980H dash camera firmware contains a path traversal vulnerability in its HTTP server. An attacker with access to the device's WiFi network could submit a crafted request to access files within the device's removable storage that were not intended to be directly accessible through the web server. Exposed files could include recordings, images, diagnostic logs, or firmware files.

### CVE-2026-82585

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-24T21:18:50.167 |

The Botslab G980H dash camera firmware transmits sensitive information over unencrypted HTTP and RTSP connections. An attacker capable of intercepting communications on the device's WiFi network could obtain stored recordings, live video, location information, images, diagnostic logs, or other sensitive information exchanged between the device and its mobile application.

### CVE-2026-82164

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-24T20:17:32.103 |

Dell Trusted Device Client, versions prior to 8.1.359.0, contain an Incorrect Permission Assignment for Critical Resource vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Information tampering.

### CVE-2026-77293

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-09-24T19:17:16.397 |

TREK is a collaborative travel planner. Prior to 3.3.0, the DELETE /api/trips/:tripId/collab/notes/:noteId/files/:fileId endpoint authorizes an authenticated user against the attacker-controlled tripId but deleteNoteFile in server/src/services/collabService.ts resolves the target only by note and file identifiers without requiring the file to belong to that trip. A user with edit access to any trip can submit identifiers belonging to another user's trip and permanently delete that note-file attachment. Sequential identifiers make broad targeting practical, while attachment read operations remain trip-scoped and are not affected. This issue is fixed in version 3.3.0.

### CVE-2026-48070

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-24T19:17:13.430 |

Docmost is open-source collaborative wiki and documentation software. Prior to 0.80.1, authenticated users can store attacker-controlled avatarUrl values that are later reused by avatar cleanup without confinement to the intended directory on local-storage deployments. A low-privileged user can cause deletion of arbitrary local files or directories reachable by the Docmost service account. This issue is fixed in version 0.80.1.

### CVE-2026-97520

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:30.050 |

In the Linux kernel, the following vulnerability has been resolved:

gfs2: move quota_init qc iterator increment

Move qc++ from the loop body into the for-loop increment
expression in gfs2_quota_init().

This keeps iterator progression explicit and avoids mixing pointer
advance with duplicate-slot handling in the loop body.

### CVE-2026-97496

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:27.290 |

In the Linux kernel, the following vulnerability has been resolved:

drm/amdkfd: Fix OOB memory exposure in get_wave_state()

The get_wave_state() function for v9 trusts cp_hqd_cntl_stack_size and
cp_hqd_cntl_stack_offset values read directly from the MQD, which are
written by GPU microcode and fully attacker-controlled on the
CRIU-restore path (via AMDKFD_IOC_RESTORE_PROCESS with H3).

this leads to an unbounded copy_to_user() that can leak adjacent
GTT/kernel memory. If offset > size, integer underflow produces a ~4 GiB
read length, if size is set to 1 MiB against a 4 KiB allocation, we leak
1 MiB of adjacent kernel memory (other queues' MQDs, ring buffers, KASLR
pointers).

Fix by clamping both cp_hqd_cntl_stack_size to the actual allocated
buffer size (q->ctl_stack_size) and cp_hqd_cntl_stack_offset to the
clamped size before performing arithmetic and copy_to_user().

This ensures we never read beyond the allocated kernel BO regardless of
attacker-supplied MQD field values.

### CVE-2026-97438

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:21.930 |

In the Linux kernel, the following vulnerability has been resolved:

fs/ntfs3: validate index entry key bounds

[BUG]
A malformed NTFS directory index entry can advertise a key_size larger
than the bytes actually present in its NTFS_DE payload. Directory lookup
then passes that malformed key to cmp_fnames(), which can read past the
end of the kmalloc'ed index buffer.

BUG: KASAN: slab-out-of-bounds in fname_full_size fs/ntfs3/ntfs.h:590 [inline]
BUG: KASAN: slab-out-of-bounds in cmp_fnames+0x1ea/0x230 fs/ntfs3/index.c:46
Read of size 1 at addr ffff88801c313018 by task syz.6.3365/9279

Call Trace:
 __dump_stack lib/dump_stack.c:94 [inline]
 dump_stack_lvl+0xbe/0x130 lib/dump_stack.c:120
 print_address_description mm/kasan/report.c:378 [inline]
 print_report+0xd1/0x650 mm/kasan/report.c:482
 kasan_report+0xfb/0x140 mm/kasan/report.c:595
 __asan_report_load1_noabort+0x14/0x30 mm/kasan/report_generic.c:378
 fname_full_size fs/ntfs3/ntfs.h:590 [inline]
 cmp_fnames+0x1ea/0x230 fs/ntfs3/index.c:46
 hdr_find_e.isra.0+0x3ed/0x670 fs/ntfs3/index.c:762
 indx_find+0x4b5/0x900 fs/ntfs3/index.c:1186
 dir_search_u+0x2c0/0x460 fs/ntfs3/dir.c:254
 ntfs_lookup+0x1cc/0x2a0 fs/ntfs3/namei.c:85
 __lookup_slow+0x241/0x450 fs/namei.c:1816
 lookup_slow fs/namei.c:1833 [inline]
 walk_component+0x31c/0x570 fs/namei.c:2151
 link_path_walk+0x592/0xd60 fs/namei.c:2519
 path_lookupat+0x138/0x660 fs/namei.c:2675
 filename_lookup+0x1f3/0x560 fs/namei.c:2705
 filename_setxattr+0xad/0x1c0 fs/xattr.c:660
 path_setxattrat+0x1d8/0x280 fs/xattr.c:713
 __do_sys_lsetxattr fs/xattr.c:754 [inline]
 __se_sys_lsetxattr fs/xattr.c:750 [inline]
 __x64_sys_lsetxattr+0xd0/0x150 fs/xattr.c:750
 ...

Allocated by task 9279:
 kasan_save_stack+0x39/0x70 mm/kasan/common.c:56
 kasan_save_track+0x14/0x40 mm/kasan/common.c:77
 kasan_save_alloc_info+0x37/0x60 mm/kasan/generic.c:573
 poison_kmalloc_redzone mm/kasan/common.c:400 [inline]
 __kasan_kmalloc+0xc3/0xd0 mm/kasan/common.c:417
 kasan_kmalloc include/linux/kasan.h:262 [inline]
 __do_kmalloc_node mm/slub.c:5650 [inline]
 __kmalloc_noprof+0x2bd/0x900 mm/slub.c:5662
 kmalloc_noprof include/linux/slab.h:961 [inline]
 indx_read+0x41d/0xad0 fs/ntfs3/index.c:1059
 indx_find+0x447/0x900 fs/ntfs3/index.c:1179
 dir_search_u+0x2c0/0x460 fs/ntfs3/dir.c:254
 ntfs_lookup+0x1cc/0x2a0 fs/ntfs3/namei.c:85
 __lookup_slow+0x241/0x450 fs/namei.c:1816
 lookup_slow fs/namei.c:1833 [inline]
 walk_component+0x31c/0x570 fs/namei.c:2151
 link_path_walk+0x592/0xd60 fs/namei.c:2519
 path_lookupat+0x138/0x660 fs/namei.c:2675
 filename_lookup+0x1f3/0x560 fs/namei.c:2705
 filename_setxattr+0xad/0x1c0 fs/xattr.c:660
 path_setxattrat+0x1d8/0x280 fs/xattr.c:713
 __do_sys_lsetxattr fs/xattr.c:754 [inline]
 __se_sys_lsetxattr fs/xattr.c:750 [inline]
 __x64_sys_lsetxattr+0xd0/0x150 fs/xattr.c:750
 ...

[CAUSE]
The index-header validators only validated INDEX_HDR-level geometry.
They did not walk each NTFS_DE to verify entry alignment, subnode
layout, or that key_size fit inside the entry payload. They also
allowed a last sentinel entry to carry a non-zero key_size.

[FIX]
Walk every NTFS_DE in ntfs3's index-header validators and reject
entries with invalid layout, mismatched subnode state, oversized
key_size, or non-zero sentinel keys before lookup or log replay can
consume them.

### CVE-2026-97437

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:21.810 |

In the Linux kernel, the following vulnerability has been resolved:

ntfs3: fix out-of-bounds read in ntfs_dir_emit() and hdr_find_e()

The bounds check in ntfs_dir_emit() compares fname->name_len (a
character count) against e->size (a byte count) without accounting
for the 2-byte-per-character UTF-16LE encoding or the ATTR_FILE_NAME
header size:

  if (fname->name_len + sizeof(struct NTFS_DE) > le16_to_cpu(e->size))

This computes: name_len + 16 > e_size

The correct check must account for the ATTR_FILE_NAME header (66 bytes
before the name) and the UTF-16LE character size (2 bytes each):

  sizeof(NTFS_DE) + offsetof(ATTR_FILE_NAME, name) +
  name_len * sizeof(short) > e_size

Which computes: 16 + 66 + name_len * 2 > e_size

The correct calculation already exists as fname_full_size() in ntfs.h
and is used in cmp_fnames(), namei.c, and fslog.c, but was not used
in the readdir path.

A crafted NTFS image with an index entry containing a small e->size
but large fname->name_len bypasses the current check, causing
ntfs_utf16_to_nls() to read past the entry boundary.

Additionally, add a key_size validation in hdr_find_e() to ensure the
declared key_size does not exceed the available entry data, preventing
comparison functions from reading past entry boundaries on the lookup
path.

### CVE-2026-93816

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:15.120 |

In the Linux kernel, the following vulnerability has been resolved:

f2fs: validate inline dentry name lengths before conversion

Inline dentry conversion copies names out of the inline dentry area
before checking that each recorded name length fits in the available
filename slots.

A corrupted image can therefore make the conversion path read past
the inline filename storage while building the regular dentry block.

Validate each inline dentry name length against the inline filename
area before copying it.

### CVE-2026-96744

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-09-24T16:17:27.120 |

Improper neutralization of special elements in data query logic in the cache lock implementation of the MongoDB integration for Laravel can cause a caller-supplied lock owner value to be evaluated as an aggregation expression rather than as a literal value. An authenticated user who can influence the owner value an application uses when acquiring or restoring a lock may take over or prematurely expire a lock held by another process, which can lead to duplicated or conflicting operations.

### CVE-2026-93229

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T16:17:18.387 |

In the Linux kernel, the following vulnerability has been resolved:

nfsd: add missing read barrier to rpc_status_get dumpit seqcount retry

The hand-rolled seqcount-like protocol in nfsd_nl_rpc_status_get_dumpit()
is missing a read memory barrier (smp_rmb) before its second counter
check.  The standard kernel read_seqcount_retry() includes smp_rmb()
to ensure that all data reads complete before the counter is re-checked.

Without this barrier, on weakly-ordered architectures (ARM, POWER),
the CPU may reorder field reads past the second counter check, making
the retry logic ineffective: it could observe a consistent counter pair
while reading fields that have been concurrently modified by the writer.

Add smp_rmb() before the second counter check to order the field reads
ahead of it, matching the barrier semantics of the standard seqcount
read-side.  The begin-side smp_load_acquire() already pairs with the
smp_store_release() in nfsd_dispatch(); with the smp_rmb() now ordering
the field reads, the retry check no longer needs acquire semantics and
reads the counter with a plain READ_ONCE(), as read_seqcount_retry()
does.

[ cel: Use READ_ONCE instead of smp_load_acquire() ]

### CVE-2026-82094

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-24T15:17:40.870 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to traverse directories on the system due to improper limitation of a pathname to a restricted directory.

### CVE-2026-79959

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-24T21:18:44.353 |

The Botslab G980H dash camera firmware contains a hard-coded root account password that cannot be changed by the user. An attacker who obtains the firmware or has physical access to the device could recover the credential and use it to obtain root access through the UART interface.

### CVE-2026-88956

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-24T20:17:33.793 |

The Botslab G980H dash camera firmware contains an authentication vulnerability in the root account exposed through the device's UART interface. The affected account does not require a password before granting access to a privileged system interface, and the interface also displays the device's WiFi password during startup. An unauthenticated attacker with physical access to the device could connect to the UART interface, obtain root privileges, and recover the WiFi password.

### CVE-2026-93810

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:14.433 |

In the Linux kernel, the following vulnerability has been resolved:

cachefiles: Fix double fput

Fix a double fput() in error handling in cachefiles_create_tmpfile().

### CVE-2026-93801

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:13.017 |

In the Linux kernel, the following vulnerability has been resolved:

smb/client: zero-initialize stack-allocated cifs_open_info_data

Stack-allocated cifs_open_info_data may contain random data.
This can make some fields have wrong value if they are not set later.

### CVE-2026-93796

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T17:17:12.383 |

In the Linux kernel, the following vulnerability has been resolved:

wifi: iwlwifi: pcie: null RX pointers after free

When iwl_pcie_tx_init() fails after RX init, nic init unwinds via
iwl_pcie_rx_free().

The freed RX members stayed non-NULL on the live transport object,
so later teardown or retry could touch stale RX state.
Set rx_pool, global_table, rxq, and alloc_page to NULL after free
to make repeated cleanup and retry paths safe.
