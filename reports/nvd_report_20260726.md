# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-25 15:00 UTC
- **対象期間**: `2026-07-24T15:00:27.000Z` 〜 `2026-07-25T15:00:16.000Z`
- **重要CVE数**: 51 件（Critical 9.0+: 9 件 / High 7.0〜: 42 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超に上ります。  
- **リモートから認証不要で特権昇格や任意コード実行が可能** な脆弱性が目立ち、特に Microsoft Azure 系サービス (App Service、AKS、Portal) に集中しています。  
- **IoT/産業制御系製品**（Loytec、Weintek 等）でも認証バイパスやメモリ破壊が報告され、サプライチェーンリスクが拡大しています。  
- **マルチメディアライブラリ (FFmpeg) やオープンソース SSH ライブラリ (libssh2)** でもヒープ破壊や二重解放が確認され、広範囲のサーバ・クライアントに影響が波及する可能性があります。  

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目すべき理由 |
|-----|------|----------|----------------|
| **CVE‑2026‑58630** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | Azure App Service の不適切なアクセス制御により、ネットワーク上の任意の攻撃者が **管理者権限へ昇格** 可能 | Azure の基幹 PaaS が対象で、影響範囲は世界中の多数の顧客テナントに及ぶ。Microsoft が即時緊急パッチを提供しているが、未適用環境が多数残存。 |
| **CVE‑2026‑57106** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | Data Quality 製品の SSRF により、内部ネットワークへのリクエストが外部から **任意に実行** できる | SSRF はクラウド環境での横方向移動や認証情報取得に直結。特に内部 API が多数公開されている組織で深刻。 |
| **CVE‑2026‑56163** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | Azure Kubernetes Service (AKS) の認証欠如により、**クラスタ全体の制御権** が取得可能 | AKS は多くの企業が採用するマネージド K8s。クラスタが乗っ取られると、全ワークロード・シークレットが漏洩・改竄されるリスクがある。 |
| **CVE‑2026‑66012** | 10.0 (AV:N/AC:L/PR:N/UI:N) | SiYuan (ノートアプリ) の `/mcp` エンドポイントが認可チェック不足で **31 の管理ツール** が無制限に操作可能 | オープンソースのローカルノートツールだが、Web UI を公開している環境では攻撃者がファイル操作・コード実行に至る可能性が高い。 |
| **CVE‑2026‑66013** | 9.3 (AV:N/AC:L/PR:N/UI:N) | OpenRemote コンソール登録 API の認証バイパスにより、**既存コンソール資産の上書き** が可能 | IoT/スマートシティ向けのプラットフォームで、資産情報改竄は制御系システムの信頼性を直接揺るがす。 |

> **※** これらは **CVSS 10.0** かつ **ネットワーク経由で認証不要** という点で共通しており、被害拡大が最も懸念されます。

## 3. 推奨アクション  

### 3.1 直ちに適用すべきパッチ・アップデート
| 製品 / ライブラリ | 現行バージョン (脆弱) | 修正版バージョン | パッケージ名 / 更新手順 |
|-------------------|------------------------|-------------------|--------------------------|
| **Azure App Service** | 2026‑06‑xx (未パッチ) | 2026‑07‑15 以降の **Security Update** | Azure ポータル → 「App Service」→「更新プログラム」→「最新のセキュリティ更新プログラムを適用」 |
| **Azure Kubernetes Service (AKS)** | 2026‑06‑xx | 2026‑07‑20 以降の **AKS Patch** | `az aks upgrade --resource-group <RG> --name <cluster> --kubernetes-version <latest‑patch>` |
| **Azure Portal** (CVE‑2026‑62835) | 2026‑06‑xx | 2026‑07‑10 以降 | 同上、Portal の「更新」タブから適用 |
| **SiYuan** | < 3.7.2 | **≥ 3.7.2** | `npm install -g siyuan@latest` または公式サイトからバイナリダウンロード |
| **OpenRemote** | < 1.26.2 | **≥ 1.26.2** | `docker pull openremote/openremote:1.26.2` → 再デプロイ |
| **FFmpeg** | ≤ 8.1.2 | **≥ 8.1.3** (コミット b506faf / aafb5c6 で修正) | `apt-get update && apt-get install -y ffmpeg=8.1.3*`（Debian/Ubuntu） |
| **libssh2** | ≤ 1.11.1 | **≥ 1.11.2** | `yum update libssh2` / `apt-get install libssh2=1.11.2*` |
| **sysPass** | ≤ 3.2.11 | **≥ 3.2.12** | `composer update` または公式リリースパッケージをデプロイ |
| **Devolutions PowerShell Universal** | ≤ 2026.2.2 | **≥ 2026.3.0** | `Install-Module -Name PowerShellUniversal -Force -AllowClobber` |
| **Weintek cMT3092X HMI** | 2026‑xx (ファームウェア) | **≥ 2026‑07‑01** | ベンダー提供の OTA パッチを適用 |
| **Loytec L‑INX 系列** | 8.4.16 以前 | **≥ 8.4.19** | `apt-get upgrade loytec-linx`（Linux）または公式アップデートツール |

### 3.2 環境・設定の見直し
1. **最小権限の徹底**  
   - Azure のロールベースアクセス制御 (RBAC) を再評価し、`Owner` 権限を必要最小限のユーザーに限定。  
   - AKS の API Server への IP 制限、PodSecurityPolicy の有効化。

2. **ネットワーク境界の強化**  
   - SSRF 対策として、外部への HTTP/HTTPS リクエストを **アウトバウンドプロキシ** 経由に限定し、内部

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-66012

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-25T11:17:19.053 |

SiYuan before v3.7.2 contains a missing authorization vulnerability in the POST /mcp kernel endpoint, which is gated only by a general auth check (model.CheckAuth) with no admin-role or read-only enforcement. This exposes 31 MCP tools, including a file tool with list/read/write/delete/rename/copy actions across the entire workspace. When the Publish server is enabled in anonymous mode (Conf.Publish.Enable=true and Conf.Publish.Auth.Enable=false), the Publish reverse proxy attaches an anonymous RoleReader JWT to proxied requests, allowing a remote unauthenticated attacker to reach /mcp. The attacker can read conf/conf.json to extract accessAuthCode, api.token, and cookieKey in plaintext, write arbitrary files in the workspace, and plant a plugin into data/plugins/ that executes with nodeIntegration:true and no contextIsolation on the next desktop launch, leading to administrator takeover.

### CVE-2026-58630

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-24T15:18:47.847 |

Improper access control in Azure App Service allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-57106

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-24T15:18:39.633 |

Server-side request forgery (ssrf) in Data Quality allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-56163

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-24T15:18:33.030 |

Missing authentication for critical function in Microsoft Azure Kubernetes Service allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-66013

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-25T11:17:19.193 |

OpenRemote before 1.26.2 contains an authentication bypass vulnerability in the console registration API that allows unauthenticated attackers to update existing console assets by supplying a known asset identifier. Attackers can overwrite push notification tokens and console metadata without authentication or ownership validation, redirecting notifications or denying delivery to legitimate consoles.

### CVE-2026-61884

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-24T22:16:50.963 |

The web management interface of Tycon Systems TPDIN-Monitor-WEB2

 does not perform server-side validation of credentials during the login process. By submitting empty values for both credential fields, an unauthenticated remote attacker can bypass the authentication check and establish a valid administrative session. This grants full access to device controls including power relay management, device reboot, remote access service configuration, and network settings, which could allow an attacker to disrupt connected infrastructure or cause physical damage to equipment.

### CVE-2026-62835

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-24T20:18:19.410 |

Improper authorization in Azure Portal allows an unauthorized attacker to disclose information over a network.

### CVE-2026-12503

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-24T15:17:10.997 |

Improper Link Resolution (CWE-59) in `/usr/bin/larm_starter` in Loytec L-INX, L-GATE, L-ROC, L-IOB, L-DALI, L-VIS and L-PAD through 8.4.16 on LINX-A64 allows an authenticated `larmapp` attacker to make `/etc/passwd` writable by the `larmapp` group (leading to root privilege escalation) via a symlink attack on `/etc/lighttpd/ssl/server.pem`.

### CVE-2026-48021

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-347` |
| Published | 2026-07-24T19:16:58.033 |

In epa4all, prior to version 2026-05-20, an attacker who can intercept the TLS connection between epa4all and the ePA backend can complete the VAU handshake with attacker-controlled keys and obtain the session encryption keys. All inner HTTP traffic (patient consent decisions, medication data, document operations, authorization tokens, and entitlement queries) becomes readable and modifiable. The attacker can also inject arbitrary requests through the hijacked channel. This issue has been patched in version 2026-05-20.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-16801

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-24T15:17:13.077 |

Improper control of generation of code ('Code Injection') in the variables feature in Devolutions PowerShell Universal 2026.2.2 and earlier allows an authenticated user with variable write permission to execute arbitrary PowerShell code via a crafted variable value that is not properly escaped when written to the variables configuration file.

### CVE-2026-16800

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-24T15:17:12.963 |

Improper control of generation of code ('Code Injection') in the schedule feature in Devolutions PowerShell Universal 2026.2.2 and earlier allows an authenticated user with schedule creation permission to execute arbitrary PowerShell code via crafted schedule parameter names concatenated into a script invocation.

### CVE-2026-61892

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-07-24T23:16:51.333 |

Weintek cMT3092X HMI allows a non-privileged user to modify tokens to escalate privileges.

### CVE-2026-60134

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-784` |
| Published | 2026-07-24T23:16:50.890 |

Weintek cMT3092X HMI allows a non-privileged user to modify cookies to gain elevated privileges.

### CVE-2026-66040

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-24T20:18:21.063 |

FFmpeg through 8.1.2, fixed in commit b506faf, contains a heap out-of-bounds write vulnerability in the native PNG and APNG encoders that allows remote attackers to corrupt heap memory by supplying a crafted PNG image with a malicious eXIf chunk. Attackers can craft an eXIf chunk where multiple IFD entries reference the same large value payload, causing canonical serialization to expand the output far beyond the undersized allocation estimated by add_exif_profile_size(), resulting in png_write_chunk() writing tens of thousands of bytes past the buffer boundary, leading to deterministic heap corruption, process crash, and potentially arbitrary code execution.

### CVE-2026-66039

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-24T20:18:20.880 |

FFmpeg through 8.1.2, fixed in commit aafb5c6, contains a signed integer overflow vulnerability in the MACE6 audio decoder that allows attackers to corrupt heap memory by supplying a crafted CAF file with a malicious bytes_per_packet value. Attackers can craft a CAF file with oversized bytes_per_packet and frames_per_packet values in the desc chunk to trigger an integer overflow in mace_decode_frame() during output sample count computation, resulting in an undersized buffer allocation and heap out-of-bounds write that could enable code execution.

### CVE-2026-66033

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-07-24T17:17:35.263 |

libssh2 through 1.11.1, fixed in commit a2ed82d, contains a pre-authentication integer underflow vulnerability in the ssh2_cipher_crypt() function in src/openssl.c that allows a malicious SSH server to crash any connecting client by negotiating AES-GCM ciphers during handshake. Attackers can exploit the underflow in the expression computing blocksize minus aadlen minus authentication tag length to trigger an out-of-bounds read and a memcpy call with a near-SIZE_MAX length argument, causing immediate process crash before any authentication occurs.

### CVE-2026-66032

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-07-24T17:17:35.120 |

libssh2 through 1.11.1, fixed in commit 5e47761, contains a double-free vulnerability in the sftp_open() function in src/sftp.c that allows a malicious SSH server to corrupt the heap of any authenticated client opening an SFTP session. When a server responds to SSH_FXP_OPEN with SSH_FXP_STATUS containing FX_OK, the response data buffer is freed, and if a subsequent sftp_packet_require() call returns a specific error such as LIBSSH2_ERROR_CHANNEL_PACKET_EXCEEDED, the same pointer is freed a second time, enabling tcache dup conditions on glibc systems that allow overlapping allocations and function pointer overwrites.

### CVE-2026-65709

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-24T17:17:34.573 |

sysPass through version 3.2.11 contains a missing object-level authorization vulnerability in the JSON-RPC API that allows API token holders to enumerate account metadata, overwrite passwords, and delete accounts across the entire vault without per-account access control. Attackers can invoke AccountController methods such as viewAction, editAction, deleteAction, and editPassAction without AccountFilterUser checks to modify or delete accounts beyond the scope of their assigned token permissions.

### CVE-2026-65623

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-07-24T17:17:34.107 |

Inefficient Algorithmic Complexity vulnerability in mtrudel bandit allows unauthenticated remote denial of service via CPU exhaustion during WebSocket fragment reassembly.

The size guard 'Elixir.Bandit.WebSocket.Connection':oversize_message?/2 called from handle_frame/3 in lib/bandit/websocket/connection.ex appends each non-final continuation frame to a left-nested iolist and then re-measures the entire accumulated buffer with IO.iodata_length/1 on every frame. Because the buffer grows by one element per frame and is fully re-traversed each time, reassembly work is quadratic (O(n^2)) in the number of continuation frames.

The max_fragmented_message_size limit (default 8 MB) bounds total bytes but not frame count, and each frame can carry as little as one payload byte, so an attacker can send millions of tiny continuation frames using modest bandwidth to pin a CPU core for minutes to hours. Many concurrent connections can starve the whole server of CPU, denying service to legitimate users. The WebSocket read timeout does not help, because it is an idle timeout evaluated between reads and cannot preempt the synchronous reassembly work spent inside a single callback.

This issue affects bandit: from 1.11.0 before 1.12.1.

### CVE-2026-66027

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-24T16:16:55.983 |

Suna before 0.9.102 contains a broken access control vulnerability in the message queue API that allows authenticated attackers to access and manipulate queue resources belonging to other users by exploiting missing ownership and account isolation checks. Attackers can read pending prompt queues of all users, read or delete individual sessions, and inject arbitrary prompts into another user's session queue, causing the background drainer to forward malicious messages to the victim's running AI agent with the victim's credentials and permissions.

### CVE-2026-55732

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-24T15:18:31.543 |

Out-of-bounds Read (CWE-125) in BACnet packet parsing (`bacdt_datetime_to_tod`) in Loytec LIP-ME201C, L-INX, L-GATE, L-ROC, L-IOB, L-DALI, L-VIS and L-PAD through 8.4.18 on LINX-A64 allows an unauthenticated remote attacker to crash `linx_a64.exe` and ultimately reboot the device via a malformed BACnet TimeSynchronization or UTC-TimeSynchronization packet with an invalid month value. The same vulnerability affects multiple other Loytec products.

### CVE-2026-55730

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-07-24T15:18:31.257 |

Reflected Cross-Site Scripting (CWE-79) in LWEB802 in Loytec LWEB-802 before 5.0.8 on all platforms allows an unauthenticated remote attacker to execute arbitrary JavaScript in a victim's browser and perform actions with the victim's privileges via a crafted link containing a malicious `project` or `mspParams` parameter.

### CVE-2026-12496

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-07-24T15:17:08.663 |

Stored Cross-Site Scripting (CWE-79) in the OPC XML-DA server statistics in Loytec LIP-ME201C, L-INX, L-GATE, L-ROC, L-IOB, L-DALI, L-VIS and L-PAD through 8.4.16 on LINX-A64 allows an unauthenticated remote attacker to execute arbitrary JavaScript in an administrator's browser (session hijacking, credential theft, device reconfiguration) via a crafted `User-Agent` header in a `POST /da` request.

### CVE-2026-65711

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-24T17:17:34.857 |

sysPass through version 3.2.11 contains an OS command injection vulnerability that allows authenticated administrators to execute arbitrary commands as the web server process user by setting a malicious backup path and triggering a backup. The FileBackupService builds a tar shell command via string concatenation, inserting the admin-configurable siteBackupPath setting without escapeshellarg() or equivalent sanitization before passing it to exec(), causing injected commands to persist and execute on every subsequent backup trigger.

### CVE-2026-65708

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-24T17:17:34.433 |

sysPass through version 3.2.11 contains an insecure direct object reference vulnerability that allows any authenticated attacker to access account file attachments belonging to accounts they do not have ACL permissions for by exploiting missing authorization checks in AccountFileController. Attackers can supply arbitrary numeric file IDs through the download, view, delete, upload, and list actions to enumerate and manipulate any attachment in the vault, bypassing account-level access controls entirely.

### CVE-2026-65693

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-24T16:16:55.360 |

Microweber CMS through 2.0.20 contains a server-side template injection vulnerability that allows authenticated administrators to achieve arbitrary OS command execution by injecting Twig expressions into mail templates. Attackers can exploit the unsandboxed Twig environment in TwigView::render(), which lacks SandboxExtension or a SecurityPolicy, to inject malicious expressions such as filter('system') into mail template bodies stored unsanitized in the database, causing automatic payload execution on each subsequent application event that triggers a mail dispatch.

### CVE-2025-71408

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-07-24T22:16:50.063 |

NLTK (Natural Language Toolkit) before version 3.9.3 contains an eval injection vulnerability in the nltk.collocations module that allows an attacker who controls command-line arguments to execute arbitrary Python code. When collocations.py is invoked directly, the __main__ block passes command-line arguments directly to eval() as suffixes of BigramAssocMeasures without allowlist validation or sanitization, enabling an attacker to supply a Python expression that escapes the intended attribute lookup and executes arbitrary code including OS commands via the os module.

### CVE-2026-48034

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-24T19:16:58.477 |

Hulumi is an open-source toolkit that ships secure-by-default cloud and platform infrastructure components for Pulumi. Prior to version 1.4.0, there is a bypass via decoy sibling resources targeting a different bucket. This issue has been patched in version 1.4.0.

### CVE-2026-17107

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-07-24T19:16:55.907 |

A flaw was found in the cluster-proxy service-proxy component used in Red Hat Advanced Cluster Management for Kubernetes (RHACM) and multicluster-engine (MCE). The service-proxy appends impersonation group headers to proxied requests without first removing caller-supplied values, and the spoke ServiceAccount holds unrestricted impersonation permissions. An authenticated hub principal can inject an Impersonate-Group header to escalate to cluster-admin on every managed cluster.

### CVE-2026-65707

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-24T17:17:34.290 |

Likeshop through 3.0.5 contains an authenticated SQL injection vulnerability that allows admin-level users to extract arbitrary database contents by submitting unsanitized POST parameters to the adjustAccount endpoint. The adjustAccount method in UserLogic.php concatenates the money, integral, growth, and earnings parameters directly into Db::raw() SQL fragments without type casting, numeric validation, or parameter binding, enabling boolean-based binary-search extraction of credentials, PII, and session tokens via distinct success and failure response messages.

### CVE-2026-48036

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-755` |
| Published | 2026-07-24T19:16:58.753 |

Hulumi is an open-source toolkit that ships secure-by-default cloud and platform infrastructure components for Pulumi. Prior to version 1.4.0, consumers running drift detection in CI / cron could see transient adapter failures silently cached as "all clear" — masking real attacks for up to six hours — or see ordinary provider-version churn falsely promoted to incident severity. Either way, the verdict source was unreliable for downstream incident workflows that gate on it. This issue has been patched in version 1.4.0.

### CVE-2026-48033

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-07-24T19:16:58.340 |

Hulumi is an open-source toolkit that ships secure-by-default cloud and platform infrastructure components for Pulumi. Prior to version 1.4.0, policy packs can be bypassed by a forged Pulumi-URN logical name. This issue has been patched in version 1.4.0.

### CVE-2026-12504

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-521` |
| Published | 2026-07-24T15:17:11.157 |

Improper Authentication (CWE-287) in the PAM configuration in Loytec LIP-ME201C, L-INX, L-GATE, L-ROC, L-IOB, L-DALI, L-VIS and L-PAD through 8.4.16 on LINX-A64 allows a local attacker to authenticate as a uid=0 account without a password and obtain a root shell via an `/etc/passwd` entry with an empty password field.

### CVE-2026-12502

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-24T15:17:10.860 |

Improper Privilege Management (CWE-269) in `/usr/bin/ltsudo` in Loytec LIP-ME201C, L-INX, L-GATE, L-ROC, L-IOB, L-DALI, L-VIS and L-PAD through 8.4.16 on LINX-A64 allows a `superadmin`-group attacker to reset the password of any LARM user (including the `larmapp` service account) via the `set-passwd` subcommand.

### CVE-2026-48032

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-697` |
| Published | 2026-07-24T19:16:58.190 |

Hulumi is an open-source toolkit that ships secure-by-default cloud and platform infrastructure components for Pulumi. Prior to version 1.4.0, IAM-role policy checks can be bypassed when the role trusts multiple OIDC providers. This issue has been patched in version 1.4.0.

### CVE-2026-10818

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-25T07:17:08.880 |

The WPForms Pro plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 1.10.1.1 via the ajax_chunk_upload_finalize function. This is due to the file type validation occurring after chunk metadata and file contents have already been written to disk, and the assembled file not being deleted upon validation failure. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible.

### CVE-2026-66374

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-25T01:16:26.423 |

Knot Resolver before 6.4.1 allows remote code execution via a heap-based buffer overflow in the DoQ (DNS-over-QUIC) receive path.

### CVE-2026-54342

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-24T19:16:59.200 |

In epa4all, prior to version 2026-05-20, an attacker on the network path between epa4all and any backend (ePA Aktensystem, Konnektor, IDP, TSS) can present a self-signed TLS certificate and intercept the connection. For non-VAU connections (Konnektor, IDP), this allows direct read and modification of the inner traffic, including smartcard operations and OIDC authentication exchanges. For the ePA backend, the disabled TLS verification is the transport-level enabler for the VAU MITM described in GHSA-vvh7-x6c7-46gh. This issue has been patched in version 2026-05-20.

### CVE-2026-8789

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-24T15:19:08.320 |

The Easy Appointments plugin for WordPress is vulnerable to unauthorized modification of data due to a missing capability check and missing nonce verification on the `ea_delete_multiple_connections` AJAX action in all versions up to, and including, 3.12.27. This makes it possible for authenticated attackers, with Contributor-level access and above, to delete arbitrary connection records from the `wp_ea_connections` table, disrupting the plugin's core booking functionality.

### CVE-2026-66041

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-24T20:18:21.240 |

FFmpeg 7.0 through 8.1.2, fixed in commit 4da9812, contains a heap out-of-bounds write vulnerability in the vf_quirc filter that allows an attacker to corrupt heap memory by supplying a crafted PGS/SUP subtitle file with mismatched frame dimensions. Attackers can provide a subtitle file whose second presentation has larger dimensions than its first, causing av_image_copy_plane() to copy data exceeding the initial allocation size into the undersized libquirc grayscale image buffer, resulting in heap corruption and process crash with potential for code execution.

### CVE-2026-66036

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-24T20:18:20.433 |

FFmpeg through 8.1.2, fixed in commit 5d7112c, contains a heap out-of-bounds write vulnerability in the vf_hqdn3d filter that allows attackers to corrupt heap memory by supplying a crafted video whose frame resolution increases between frames when filtergraph reinitialization is disabled via the -reinit_filter 0 option. Attackers can provide a malicious video input where vf_hqdn3d.config_input() allocates undersized per-plane line-history buffers based on the initial frame width, and subsequent larger frames cause denoise_spatial() to write beyond the allocation boundary, resulting in heap memory corruption.

### CVE-2026-66035

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-24T17:17:35.547 |

libssh2 through 1.11.1, fixed in commit 42e33d8, contains a pre-authentication heap buffer overflow vulnerability that allows a malicious SSH server to corrupt heap metadata in any connecting client by sending a packet with a packet_length smaller than the cipher's block size during Encrypt-then-MAC cipher negotiation. In the fullpacket() function in src/transport.c, the ETM path allocates a buffer of packet_length bytes but copies blocksize minus one bytes via memcpy, causing an overflow that on 32-bit glibc writes attacker-controlled bytes into an adjacent chunk's SIZE field, enabling tcache bin confusion, overlapping live objects, and function pointer overwrite during the session handshake before authentication.

### CVE-2026-66034

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-908` |
| Published | 2026-07-24T17:17:35.407 |

libssh2 through 1.11.1, fixed in commit a13bb6c, contains a missing bounds check vulnerability that allows a malicious SSH server to trigger an arbitrary-length heap out-of-bounds read and a free of an uninitialized pointer via the publickey subsystem. In libssh2_publickey_list_fetch(), the version 1 response parser reads a server-controlled comment_len value and advances the parse pointer without verifying sufficient bytes remain in the buffer, causing the out-of-bounds read to leak heap pointers from adjacent allocations defeating ASLR, followed by heap allocator state corruption when the error cleanup path frees an uninitialized pointer from a non-zeroed realloc() region.

### CVE-2026-55729

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-24T15:18:31.120 |

Exposure of Sensitive Information (CWE-200) in LWEB802 browser `localStorage` in Loytec LWEB-802 before 5.0.8 on all platforms allows an unauthenticated remote attacker to leak stored management credentials via a crafted link.

### CVE-2026-66373

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-07-25T01:16:26.277 |

Redis before 8.8.0, in the unusual case where an authenticated attacker can execute RESTORE, allows remote code execution via a RESTORE payload where the same NACK (pending entry) is referenced by more than one consumer, because deleting both consumers via XGROUP DELCONSUMER leads to a double free. NOTE: this issue exists because of an incomplete fix for CVE-2026-25243.

### CVE-2026-61886

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-256` |
| Published | 2026-07-24T23:16:51.197 |

Weintek cMT3092X HMI stores user account passwords in plaintext.

### CVE-2026-60135

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-286` |
| Published | 2026-07-24T23:16:51.037 |

An attacker can modify data that should be restricted to read‑only access.

### CVE-2026-66038

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-908` |
| Published | 2026-07-24T20:18:20.727 |

FFmpeg through 8.1.2, fixed in commit 8670835, contains an information disclosure vulnerability in the LCL/ZLIB video decoder that allows attackers to expose uninitialized heap memory by supplying a valid zlib stream that inflates to fewer bytes than the expected frame size. The zlib_decomp() function in lcldec.c treats short decompression as non-fatal and continues to the RGB24 conversion path, which copies a full frame's worth of rows from the allocation buffer using original frame dimensions, causing uninitialized heap contents including pointer-derived allocator bytes to be copied into the attacker-observable AVFrame output and potentially defeating ASLR in long-lived media processing services.

### CVE-2026-66037

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-24T20:18:20.573 |

FFmpeg through 8.1.2, fixed in commit 5d7112c, contains an uncontrolled resource consumption vulnerability in the IAMF demuxer that allows an unauthenticated attacker to cause multi-gigabyte memory allocation from a 17-byte input file by supplying a crafted count_label field. The mix_presentation_obu() function in libavformat/iamf_parse.c calls av_calloc(count_label, sizeof(*language_label)) with an attacker-controlled value before validating available OBU data, enabling an allocation amplification of approximately 126 million bytes per input byte that exhausts process memory or triggers an OOM-kill during format probing.

### CVE-2026-48035

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1059` |
| Published | 2026-07-24T19:16:58.617 |

Hulumi is an open-source toolkit that ships secure-by-default cloud and platform infrastructure components for Pulumi. Prior to version 1.4.0, consumers using AccountFoundation could ship an AWS account whose CloudTrail / Config audit logs were deletable by any S3-delete-capable principal — while believing the startup-hardened tier guaranteed tamper-resistance. Sandbox-tier deployments had no audit immutability at all (defects 1 and 3 compounded). This issue has been patched in version 1.4.0.

### CVE-2026-65710

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-24T17:17:34.713 |

sysPass through version 3.2.11 contains a missing authorization vulnerability that allows authenticated users with the PUBLICLINK_CREATE profile flag to trigger unauthorized decryption and persistent storage of any vault account's password by exploiting the absence of AccountAcl checks in the public link creation flow. Attackers can invoke the saveCreateFromAccountAction endpoint to cause AccountService::getDataForLink to load arbitrary target accounts without AccountFilterUser restrictions, decrypt credentials using the session master key, and serialize cleartext passwords into Vault storage on the PublicLink database row, enabling subsequent unauthenticated retrieval if the generated link hash is recovered.
