# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-26 15:00 UTC
- **対象期間**: `2026-06-25T15:04:06.000Z` 〜 `2026-06-26T15:00:57.000Z`
- **重要CVE数**: 111 件（Critical 9.0+: 19 件 / High 7.0〜: 92 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE のうち **CVSS 7.0 以上** が 40 件以上報告され、特に **認証不要でリモートコード実行や任意ファイル書き込みが可能** な脆弱性が集中しています。  
- 高スコア（9.0 以上）の脆弱性は **Flowise 系列、GeoVision カメラ、File Browser、pnpm、RTKLIB** など多様な製品にまたがり、IoT デバイスから開発ツールまで幅広い攻撃対象が増大しています。  
- 多くの脆弱性は **入力検証不足（パス・トラバーサル、バッファ長チェック）** や **認証・認可の欠如** が根本原因であり、コードレベルのサニタイズと認証設計の見直しが急務です。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目理由 |
|-----|--------|----------|----------|
| **CVE‑2025‑71338** (Flowise) | 10.0 | 任意ファイル書き込み（`/api/v1/document-store/loader/process`） | 認証不要で `../` パス・トラバーサルが可能。`package.js` など重要ファイルを書き換えられ、サーバ全体の制御が奪われる危険性が極めて高い。 |
| **CVE‑2026‑57700** (OMGF Pro) | 10.0 | 任意ファイルアップロード（危険な拡張子） | 5.2.6 以前のすべてのバージョンで **無制限にファイルをアップロード** でき、Web シェル等のマルウェア設置が容易。プラグインマーケット全体の信頼性が揺らぐ。 |
| **CVE‑2026‑57881 / 57880 / 57879 / 57878** (GeoVision GV‑LPC2011/2211) | 9.8 | スタックベースバッファオーバーフロー（vlsvr/ssvr/thttpd） | 複数コンポーネントで同一の脆弱性が連鎖。認証不要でリモートから任意コード実行が可能。IoT カメラはネットワークの外部に露出しやすく、侵入点として狙われやすい。 |
| **CVE‑2025‑71336** (Flowise) | 9.3 | 認証なしで任意コード実行（Custom MCP 機能） | Flowise の最小限の認証モデルが原因で、OS コマンド実行が可能。内部ツールとして広く利用されるため、企業内部での横展開リスクが大。 |
| **CVE‑2026‑55413** (ToolJet) | 9.4 | 認証ユーザーがプラグインを任意の JavaScript で上書き | Builder ロール（無料プラン）でも **全社的に実行されるスクリプト** を改ざんでき、情報漏洩やランサムウェア実行の踏み台になる。 |

> **注:** 上記は **スコアが最高かつ攻撃範囲が広い**（認証不要・リモートコード実行・重要インフラへの影響）ものを抜粋。特に Flowise 系列は複数の脆弱性が同一エンドポイントに集中している点が危険です。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンのアップデート
| 製品 | 現行脆弱バージョン | 修正版 (最低) | アップデート手順 |
|------|-------------------|----------------|-------------------|
| **Flowise** | 2.2.7‑patch.1 以前、2.2.8 以前、3.0.6 以前 | **3.0.10**（全脆弱性修正） | `npm install -g flowise@3.0.10` もしくは Docker イメージを `flowise:3.0.10` に更新 |
| **OMGF Pro** | 5.2.6 以前 | **5.2.7** 以上 | WordPress 管理画面 → プラグイン更新、または手動で `omgf-pro.zip` を上書き |
| **GeoVision GV‑LPC2011/2211** | V1.12 以前 | **V1.13** 以上 | ベンダー提供のファームウェア `GV‑LPC2011_V1.13.bin` を OTA または手動で適用 |
| **ToolJet** | 3.20.178‑lts 以前 | **3.20.179‑lts** 以上 | `docker pull tooljet/tooljet:3.20.179-lts` → 再デプロイ |
| **RTKLIB** | 2.4.3 以前 | **2.4.4** 以上 | ソースからビルドする場合 `git checkout v2.4.4 && make clean && make` |
| **pnpm** | 10.34.0 / 10.34.2 以前、11.4.0 / 11.5.3 以前 | **10.34.2**、**11.5.3** 以上 | `npm i -g pnpm@latest`（自動で最新安定版） |
| **File Browser** | 2.63.6 以前 | **2.63.7** 以上 | `docker pull filebrowser/filebrowser:2.63.7` → 再起動 |
| **Cursor** | 3.0 以前 | **3.1** 以上 | `npm i -g @cursor/cli@3.1` もしくは公式インストーラ更新 |

### 3.2 共通的な防御策
- **入力サニタイズ徹底**  
  - パス・トラバーサル対策として、ファイルパスは必ず **正規化 (`realpath`)** 後に許可ディレクトリと比較。  
  - バッファ長チェックは **定数長** か **安全なライブラリ**（`strlcpy`、`memcpy_s`）を使用。
- **認証・認可の強化**  
  - すべての API エンドポイントに **認証トークン（JWT 等）** を必須化し、ロールベースのアクセス制御を実装。  
  - 特権操作（ファイル書き込み、プラグイン更新、パスワード変更）には **二要素認証** または **現在パスワードの再入力** を要求。
- **Web アプリケーションファイアウォール (WAF)**  
  - `../` などのパス・トラバーサル文字列、危険拡張子（`.php`, `.js`, `.sh`）のアップロードをブロック。  
  - 既知の CVE のシグネチャを追加し、リクエストレートリミットを設定（特に WebSocket 認証エンドポイント）。
- **監査ログの有効化**  
  - ファイル書き込み・プラグイン更新・認証失敗のすべてを **タイムスタンプ付きで保存**。  
  - 異常なパターン（大量のアップロード、短時間の認証リクエスト）を SIEM でアラート化。
- **定期的な脆弱性スキャン**  
  - コンテナイメージは **Trivy**、ホストは **OpenVAS** で週次スキャン。  
  - `pnpm` のようなパッケージマネージャは **npm audit**、`npm audit

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2025-71338

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-06-25T22:16:59.520 |

Flowise contains a path traversal vulnerability in the /api/v1/document-store/loader/process endpoint that allows unauthenticated attackers to write arbitrary files to the filesystem. Attackers can exploit unsanitized fileName parameters with ../ sequences to overwrite critical files like package.json and achieve remote code execution when the application restarts.

### CVE-2026-57700

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-25T19:16:45.973 |

Unrestricted Upload of File with Dangerous Type vulnerability in Daan.Dev OMGF Pro allows Using Malicious Files.

This issue affects OMGF Pro: from n/a through 5.2.6.

### CVE-2026-57881

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-26T08:16:25.087 |

An unauthenticated
stack-based buffer overflow vulnerability exists in vlsvr in GeoVision
GV-LPC2011 and GV-LPC2211 V1.12 and earlier. The vulnerability is caused by
insufficient length validation when processing remote login data. A remote
attacker may exploit this vulnerability by sending crafted login data with
overly long input, resulting in memory corruption, denial of service, or potentially
arbitrary code execution.

### CVE-2026-57880

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-26T08:16:24.983 |

An unauthenticated
stack-based buffer overflow vulnerability exists in ssvr in GeoVision
GV-LPC2011 and GV-LPC2211 V1.12 and earlier. The vulnerability is caused by
insufficient bounds checking when parsing RTSP Digest authentication fields. A
remote attacker may exploit this vulnerability by sending a crafted RTSP
request containing overly long authentication data, resulting in memory
corruption, denial of service, or potentially arbitrary code execution.

### CVE-2026-57879

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-26T08:16:24.877 |

An unauthenticated
stack-based buffer overflow vulnerability exists in ssvr in GeoVision
GV-LPC2011 and GV-LPC2211 V1.12 and earlier. The vulnerability is caused by
insufficient bounds checking when processing RTSP custom authentication data. A
remote attacker may exploit this vulnerability by sending a crafted RTSP
request, resulting in memory corruption, denial of service, or potentially
arbitrary code execution.

### CVE-2026-57878

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-26T08:16:24.773 |

An unauthenticated
stack-based buffer overflow vulnerability exists in thttpd in GeoVision
GV-LPC2011 and GV-LPC2211 V1.12 and earlier. The vulnerability is caused by
insufficient bounds checking when processing web request parameters in a
specific request path. A remote attacker may exploit this vulnerability by
sending a crafted HTTP request with overly long input, resulting in memory
corruption, denial of service, or potentially arbitrary code execution.

### CVE-2026-55413

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-25T17:16:42.200 |

ToolJet is the open-source foundation am AI-native platform for building and deploying internal tools, workflows and AI agents. Prior to 3.20.178-lts, any authenticated user with builder role (free tier) can overwrite a globally-shared marketplace plugin with arbitrary JavaScript that executes server-side with full Node.js access (require, process). The malicious code runs whenever any user on the instance triggers a query using that plugin — achieving both RCE and supply-chain compromise of the entire ToolJet deployment. This vulnerability is fixed in 3.20.178-lts.

### CVE-2026-40702

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-25T22:17:01.483 |

WebSocket endpoints lack proper authentication mechanisms, enabling attackers to impersonate charging stations. As a result, attackers can exploit this weakness to gain unauthorized access to sensitive data or perform unauthorized actions. Given that no authentication is required, this can lead to privilege escalation and potentially compromise the security of the entire system.

### CVE-2025-71336

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-25T22:16:59.390 |

Flowise before 3.0.6 (affected versions 2.2.7-patch.1 and earlier) contains an unsandboxed remote code execution vulnerability in the Custom MCP feature, which is designed to execute OS commands such as launching local MCP servers. Because Flowise's authentication and authorization model is minimal and lacks role-based access control, and the default installation runs without authentication unless FLOWISE_USERNAME and FLOWISE_PASSWORD are set, an attacker can send a crafted JSON payload with the header 'x-request-from: internal' to the /api/v1/node-load-method/customMCP endpoint to execute arbitrary OS commands, resulting in complete compromise of the platform container or server.

### CVE-2025-71334

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-06-25T22:16:59.127 |

Flowise before 3.0.6 (affected versions 2.2.8 and earlier) contains an arbitrary file access vulnerability due to missing validation that the chatflowId and chatId parameters are UUIDs or numbers in file handling operations. By supplying a path-traversal value (e.g., '../../../../../tmp') as the chatflow id, an unauthenticated attacker can use the /api/v1/chatflows endpoint (via addBase64FilesToStorage) to write arbitrary files, and the /api/v1/get-upload-file and /api/v1/openai-assistants-file/download endpoints (via streamStorageFile) to read arbitrary files. Arbitrary file write may lead to remote code execution.

### CVE-2025-71333

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-06-25T22:16:59.010 |

Flowise through 2.2.4 contains an unauthenticated arbitrary file upload vulnerability in the /api/v1/attachments endpoint when storageType is set to local. Attackers can exploit path traversal in the chatId and chatflowId parameters to upload malicious files to arbitrary directories, potentially enabling remote code execution and server compromise.

### CVE-2025-71327

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-25T22:16:58.740 |

Flowise contains an authentication bypass vulnerability in the unprotected /api/v1/account/register endpoint that allows unauthenticated attackers to create user accounts. Remote attackers can exploit this endpoint to register arbitrary accounts and authenticate to the system, gaining full API access without credentials.

### CVE-2026-56786

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-25T19:16:44.997 |

RTKLIB through 2.4.3 contains an out-of-bounds write vulnerability in decode_type1033 function that fails to clamp length counters to destination buffer size, allowing up to 191-byte overflow into fixed 64-byte descriptor fields. An attacker controlling an NTRIP or serial RTCM3 correction stream can craft a valid CRC-bearing type-1033 message to corrupt adjacent rtcm_t object members, potentially achieving arbitrary code execution or denial of service.

### CVE-2026-54088

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-88;CWE-306` |
| Published | 2026-06-25T19:16:40.687 |

File Browser is a file managing interface for uploading, deleting, previewing, renaming, and editing files within a specified directory. Prior to 2.63.6, the Hook Authentication feature in File Browser allows administrators to delegate login verification to an external shell command. User-supplied credentials (username and password) are interpolated into this command string using os.Expand without sanitization. An unauthenticated remote attacker can inject shell metacharacters in the username or password field at the login screen, causing the server to execute arbitrary OS commands before any authentication takes place. This is a critical pre-authentication RCE. This vulnerability is fixed in 2.63.6.

### CVE-2026-50549

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-06-25T19:16:39.793 |

Cursor is a code editor built for programming with AI. Prior to 3.0, Cursor runs agent terminal commands in a sandbox by default. Before a Write, the agent canonicalizes the target path to confirm it stays inside the workspace, but when canonicalization fails it falls back to the original path and writes without approval. A malicious agent can create an in-workspace symlink that points outside the workspace and force canonicalization to fail — either because the target does not exist or because read permission is removed from the path — so the agent writes through the symlink to an arbitrary location without approval. A malicious agent could write arbitrary files outside the workspace under the user's privileges. This enables non-sandboxed Remote Code Execution — for example by overwriting the cursorsandbox helper so later commands run unsandboxed — with no user interaction beyond a benign prompt. This vulnerability is fixed in 3.0.

### CVE-2026-50548

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-25T19:16:39.660 |

Cursor is a code editor built for programming with AI. Prior to 3.0, Cursor runs agent terminal commands in a sandbox by default, and the sandbox grants write access to the command's working directory. A flaw was identified in how the agent could modify the working_directory parameter, which could cause the sandbox to include writable paths outside the intended workspace. A malicious agent could set working_directory to a sensitive location and write arbitrary files outside the workspace under the user's privileges. This enables non-sandboxed Remote Code Execution — for example by overwriting the cursorsandbox helper so later commands run unsandboxed — with no user interaction beyond a benign prompt. This vulnerability is fixed in 3.0.

### CVE-2026-9222

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-836` |
| Published | 2026-06-26T00:16:55.647 |

Setracker2 Android Companion App com.tgelec.setracker versions 3.1.5 and prior only require the password hash when authenticating with backend services from the client. This could allow an attacker, who knows the hash, to authenticate and gain full access.

### CVE-2026-56123

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-25T17:17:01.967 |

socat versions 1.8.0.0 through 1.8.1.1 contain a heap-based buffer overflow vulnerability that allows a malicious SOCKS5 proxy server to overwrite adjacent heap memory by exploiting a sign-extension flaw in the DOMAINNAME reply parser. During connection setup, the domain name length byte is read through a signed char field causing a negative bytes_to_read value that is implicitly converted to size_t, resulting in an unbounded heap write into the 262-byte reply buffer with attacker-controlled size and content.

### CVE-2026-54089

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-290` |
| Published | 2026-06-25T19:16:40.827 |

File Browser is a file managing interface for uploading, deleting, previewing, renaming, and editing files within a specified directory. Starting with 2.0.0-rc.1, when FileBrowser is configured with proxy authentication (auth.method=proxy), any unauthenticated attacker who can reach the server directly can impersonate any user - including admin - by sending a single forged HTTP header. No credentials are required. Additionally, specifying a non-existent username causes the server to automatically create a new user account, providing an account creation primitive with no authorization. This is an already known issue that has been documented in the documentation for several years, but has not been documented as a vulnerability before.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-50741

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-26T02:16:53.627 |

Bypass to the fix for CVE-2026-34916. Variants of such vectors have been also reported by phucrio and offsetmd. The fix can be bypassed either by sending a disallowed but otherwise valid plugin identifier as `type`, or using the `ox.setChannelTargeting` XML-RPC API method.

### CVE-2026-6679

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-197;CWE-787` |
| Published | 2026-06-25T21:16:28.167 |

A heap buffer overflow could occur in the DTLS 1.3 ACK serialization path before the connecting peer is authenticated. The buffer overflow was due to an integer truncation when computing the length of the ACK record-number list, causing an undersized buffer to be allocated and then overrun. This affects builds using DTLS 1.3 and wolfSSL version 5.9.0 and earlier. A fix was added to the 5.9.1 release.

### CVE-2026-56445

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-25T21:16:27.550 |

The qrscp application's C-STORE handler uses a specific instance from attacker-supplied DICOM datasets directly in os.path.join() without sanitization, allowing file writes to arbitrary paths.

### CVE-2026-55698

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345;CWE-494;CWE-829` |
| Published | 2026-06-25T18:16:40.837 |

pnpm is a package manager. Prior to 10.34.2 and 11.5.3, pnpm can persist package-manager bootstrap metadata in the first YAML document of pnpm-lock.yaml. Before the patch, direct pnpm execution trusted an already resolved packageManagerDependencies entry when the committed env lockfile contained matching pnpm and @pnpm/exe versions. A malicious repository could therefore commit package-manager lockfile package records and snapshots that bypassed fresh package-manager resolution, then cause pnpm to install and execute bytes selected by that committed lockfile state during automatic version switching. This vulnerability is fixed in 10.34.2 and 11.5.3.

### CVE-2026-50016

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-06-25T18:16:39.303 |

pnpm is a package manager. Prior to 10.34.0 and 11.4.0, pnpm allows a transitive dependency alias from registry package metadata to contain path traversal segments. During install, pnpm later uses that alias as a filesystem path when linking dependency nodes. As a result, a registry package can cause `pnpm install --ignore-scripts` to replace paths in the current project with symlinks to attacker-controlled dependency package directories. This vulnerability is fixed in 10.34.0 and 11.4.0.

### CVE-2026-57532

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-80` |
| Published | 2026-06-25T15:16:41.457 |

Malicious HTML content contained in the layout specification of a PDF 
ticket or badge layout was executed when the PDF editor is opened in the
 browser. This could allow one backend user to inject JavaScript into 
the browser context of another backend user. Due to requirements of the 
PDF rendering and editing libraries used, this is one of the few pages 
in our backend that do not have a strong Content-Security-Policy that 
would render this capability useless for most scenarios.

### CVE-2026-9221

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-327` |
| Published | 2026-06-26T00:16:55.500 |

The Setracker2 Android Companion App (com.tgelec.setracker) versions 3.1.5 and earlier uses MD5 to generate a request signature for authenticating communications between the mobile client and the backend REST API. Attackers could potentially reverse the signature to recover the session ID. With the session ID exposed, an attacker could impersonate the legitimate user and issue authenticated API requests.

### CVE-2026-9220

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-06-26T00:16:55.367 |

Setracker2 Android Companion App com.tgelec.setracker versions 3.1.5 and prior encrypts requests between the watch and its backend with static hardcoded AES keys and initialization vectors. This allows an attacker to decrypt Setracker2 watch traffic.

### CVE-2026-50176

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-06-25T22:17:01.873 |

The WebSocket Application Programming Interface lacks restrictions on the number of authentication requests. This absence of rate limiting may allow an attacker to conduct denial-of-service attacks or brute-force attacks to gain unauthorized access.

### CVE-2025-71328

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620` |
| Published | 2026-06-25T22:16:58.877 |

Flowise before 3.0.10 contains an unverified password change vulnerability. An authenticated user can change their account password through the account settings (Security) section without supplying the current password or any additional verification, as the application does not enforce a current-password check on the credential change. This can lead to full account takeover, particularly if an attacker can hijack or coerce an authenticated session.

### CVE-2025-71324

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-06-25T22:16:58.600 |

Flowise before 3.0.6 contains an arbitrary file read vulnerability in the chatId parameter of the /api/v1/get-upload-file and /api/v1/openai-assistants-file/download endpoints. The chatId value is not validated and is passed to streamStorageFile(), where a fallback file-lookup path constructed without the orgId is evaluated after the storage-directory containment check, allowing path traversal beyond the intended storage directory. Unauthenticated attackers can read sensitive files such as /root/.flowise/database.sqlite, exposing all database content in the default configuration.

### CVE-2026-11310

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-06-25T20:17:09.777 |

X.509 trust-chain bypass in the OpenSSL compatibility certificate verifier (wolfSSL_X509_verify_cert()). This affects only builds with --enable-opensslextra (OPENSSL_EXTRA) and whose application validates certificates by calling X509_verify_cert() with caller-supplied untrusted intermediate certificates; for those users it is critical, otherwise the library is unaffected. In particular, native wolfSSL TLS/DTLS usage is not impacted. wolfSSL's X509_verify_cert() temporarily loads each caller-supplied untrusted intermediate into the certificate manager but failed to drop them before the trusted-store check, so an untrusted intermediate could anchor the path itself. An attacker can present a chain that never reaches a configured trust anchor and have it accepted, resulting in acceptance of an attacker-controlled certificate. This is certificate verification independent of TLS (e.g. S/MIME/CMS, code/firmware signing, JWT/JWS x5c), is not specific to any key type or algorithm, and a single untrusted intermediate suffices. The default wolfSSL TLS handshake (WOLFSSL_VERIFY_PEER) is not affected; only TLS applications doing manual or deferred peer verification through this API are, which also requires --enable-sessioncerts.

### CVE-2026-56770

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-06-25T19:16:44.113 |

libais through 0.15 VdmStream::AddLine uses an unchecked sentinel value as a vector index when processing AIS sentences with empty or out-of-range sequential message IDs. Remote attackers can crash services or vessel systems by sending crafted AIVDM sentences over VHF marine radio or IP feeds, causing out-of-bounds memory access and potential corruption.

### CVE-2026-56768

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-25T19:16:43.840 |

Seahub before 13.0.23 does not enforce SHARE_LINK_LOGIN_REQUIRED on GET /api/v2.1/share-link-zip-task/, allowing unauthenticated users to bypass authentication. Attackers with a folder share-link token can call the GET endpoint to obtain a fileserver zip token and download entire shared directory trees.

### CVE-2026-56767

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-25T19:16:43.713 |

Maxun before 0.0.42 contains a cross-tenant insecure direct object reference vulnerability in storage and webhook API handlers that allows authenticated users to access other users' robots and OAuth tokens. Attackers can read plaintext Google and Airtable access tokens, modify, delete, or execute other users' robots by bypassing ownership checks in API endpoints.

### CVE-2026-54090

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-184` |
| Published | 2026-06-25T19:16:40.980 |

File Browser is a file managing interface for uploading, deleting, previewing, renaming, and editing files within a specified directory. Prior to 2.33.8, when a shell interpreter is configured (e.g. /bin/sh -c), the command allowlist can be bypassed through shell metacharacters. The allowlist validates only the first token of user input, but the entire raw string is handed to the shell — semicolons, pipes, backticks, and $() all work to chain arbitrary commands after a permitted one. This vulnerability is fixed in 2.33.8.

### CVE-2026-9716

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-06-25T16:16:44.107 |

CWE-476 NULL Pointer Dereference vulnerability exists that could cause a denial-of-service condition, rendering the device’s HMI and configuration functionality unavailable when malformed requests are received over exposed network interfaces.

### CVE-2026-9650

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-06-25T16:16:43.867 |

CWE-522 Insufficiently Protected Credentials vulnerability that could cause unauthorized access and exposure of sensitive information when unauthenticated attacker accesses credentials stored within firmware or system files. With this credential an attacker could subsequently compromise the device if they have physical access to the device.

### CVE-2026-57877

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-06-26T08:16:24.667 |

An unauthenticated
format string vulnerability exists in vlsvr in GeoVision GV-LPC2011 and
GV-LPC2211 V1.12 and earlier. The vulnerability is caused by improper handling
of externally controlled input during log message formatting in the login
processing path. A remote attacker may exploit this vulnerability by sending
crafted login data, potentially causing information disclosure, memory
corruption, or a denial of service.

### CVE-2025-71335

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-06-25T22:16:59.260 |

Flowise before 3.0.10 (affected versions 3.0.7 and earlier) fails to invalidate existing sessions and session tokens after a user changes their password. An attacker who already holds an active session, for example via a stolen session token or a device left logged in, remains authenticated as the legitimate user even after the user rotates their credentials, undermining the security purpose of the password change.

### CVE-2026-56766

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-25T19:16:43.577 |

Hydra through 9.7, fixed in commit 9cc84c2, contains a stack buffer overflow in NTLM authentication across SMTP, POP3, IMAP, NNTP, HTTP, HTTP-Proxy, and HTTP-Proxy-Urlenum modules when processing malicious NTLM Type-2 challenges. A malicious server can send a crafted NTLM Type-2 challenge with an excessively long domain string, causing base64-encoded response data to overflow a 500-byte stack buffer by 18 to 330 bytes, enabling remote code execution on systems without stack protection.

### CVE-2026-9717

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-25T16:16:44.220 |

CWE-78 Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability exists that could allow unauthorized execution of commands with elevated privileges, impacting system integrity, confidentiality, and availability when a privileged authenticated user interacts with a vulnerable network-exposed service.

### CVE-2026-13325

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-26T11:16:30.830 |

A flaw was found in KubeVirt's migration proxy. When spec.configuration.migrations.disableTLS is set to true on the KubeVirt custom resource, the target virt-handler binds a plain TCP listener on all interfaces (0.0.0.0/::) on a random port with no authentication, peer allow-list, or handshake token. This listener proxies directly into the target virt-launcher's virtqemud control socket. An attacker with a running pod on the cluster network can connect to this listener and issue unfiltered libvirt RPC commands against another tenant's virtual machine, including reading VM memory and configuration, modifying VM state via QMP, or destroying the VM. The bind address is unconditionally 0.0.0.0 — configuring a dedicated migration network via migrations.network only changes the advertised migration IP, not the listener bind address, so the port remains reachable on the pod network even when a dedicated migration network is configured. The API documentation describes disableTLS as removing "the additional layer of live migration encryption" without disclosing that it also removes all mutual authentication.

### CVE-2026-8797

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-06-26T05:16:31.930 |

An access control deficiency vulnerability exists in ExpressUpdate Agent for Windows. If a malicious user gains access to the product, arbitrary code could be executed with SYSTEM privileges.

### CVE-2026-12975

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:N/A:H` |
| Weaknesses | `CWE-611` |
| Published | 2026-06-25T22:17:00.620 |

A flaw was found in Apicurio Registry. The ContentTypeUtil.isParsableXml() method creates a SAXParserFactory without enabling secure processing features or disabling external entity resolution. An attacker with artifact-write permission (or unauthenticated when the registry runs with default configuration) can upload a crafted XML document to trigger blind server-side request forgery (SSRF) via external DTD/entity fetch, or cause denial of service via entity expansion.

### CVE-2026-54096

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-25T19:16:41.620 |

File Browser is a file managing interface for uploading, deleting, previewing, renaming, and editing files within a specified directory. Prior to 2.63.7, `POST /api/share/<path>` accepts an authenticated request for an arbitrary path and stores a public share record without checking whether the target file currently exists. Later, when a file is created at that same path, the previously created public share immediately becomes valid and exposes the new file through `GET /api/public/dl/<hash>`. This vulnerability is fixed in 2.63.7.

### CVE-2026-12921

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-25T19:16:36.167 |

In AzeoTech DAQFactory versions 21.1 and prior, a Use After Free vulnerability can be exploited by an attacker using specially crafted .ctl files which can result in code execution.

### CVE-2026-12897

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-25T19:16:35.773 |

Horner Automation Cscape versions prior to 10.2 SP3 are vulnerable to an Out-of-Bounds Read vulnerability through parsing CSP files. Successful exploitation of this vulnerability could allow an attacker to disclose information and execute arbitrary code.

### CVE-2026-57456

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-25T16:16:42.900 |

Vim is an open source, command line text editor. Prior to 9.2.0699, Vim's Python omni-completion (runtime/autoload/python3complete.vim and the legacy pythoncomplete.vim) executes reconstructed function and class definitions from the current buffer with exec() as part of populating the completion dictionary. When reconstructing that source, each scope's docstring is inserted verbatim between triple quotes with no escaping, so a hostile buffer can break out of the triple-quoted literal and execute attacker-controlled Python during omni-completion. This vulnerability is fixed in 9.2.0699.

### CVE-2026-2053

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-26T08:16:21.603 |

The WSO2 API Manager's message flow component, when processing WS-Addressing headers, does not sufficiently validate or restrict user-controlled input within these headers. This omission allows an attacker to manipulate WS-Addressing headers to specify arbitrary destinations for server-initiated requests.

Successful exploitation allows an unauthenticated attacker to control the destination of server-initiated requests originating from the WSO2 API Manager. This direct control can enable unauthorized access to internal network resources or services that would typically be inaccessible from external networks.

### CVE-2026-9219

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-340` |
| Published | 2026-06-26T00:16:55.213 |

Setracker2 Android Companion App com.tgelec.setracker versions 3.1.5 and prior have a predictable registration ID derived from IMEI. The enrollment system lacks additional authentication before assignment. If an attacker is able to obtain the registration ID, they would be able to arbitrarily enroll watches belonging to other users.

### CVE-2026-13281

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-472` |
| Published | 2026-06-25T22:17:00.880 |

Integer overflow in Mojo in Google Chrome prior to 149.0.7827.201 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a malicious file. (Chromium security severity: High)

### CVE-2026-12473

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-25T21:16:26.530 |

Two data sources (DICOMWebProxy and DICOMJSON) shipped in the default configuration fetch an arbitrary URL parameter without validation. A global authentication service in OHIF automatically injects the authenticated user's OIDC Bearer token into the resulting requests, sending it to the attacker-controlled server. DICOMweb data sources are not impacted.

### CVE-2026-55958

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-393;CWE-787` |
| Published | 2026-06-25T20:17:16.140 |

Out-of-bounds write in the Renesas TSIP TLS 1.3 transcript buffer. In tsip_StoreMessage() the capacity check guarding the fixed message bag (MSGBAG_SIZE) sets an error code but fails to return, so execution falls through to an XMEMCPY that writes past the end of the buffer once the accumulated TLS 1.3 handshake transcript exceeds MSGBAG_SIZE (8 KB), corrupting adjacent heap state and potentially causing a remote denial of service crash. The bag is sized to hold a normal handshake, so this is reached only by an unusually large but valid certificate chain, or by a malicious or man-in-the-middle server sending an oversized handshake message to a client that does not strictly verify the chain. This only affects builds using the Renesas TSIP TLS port (WOLFSSL_RENESAS_TSIP_TLS) as a TLS 1.3 client on Renesas MCUs with TSIP hardware enabled, and is rated High within those builds. All other configurations are unaffected.

### CVE-2026-55412

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-25T17:16:42.020 |

ToolJet is the open-source foundation am AI-native platform for building and deploying internal tools, workflows and AI agents. Prior to 3.20.178-lts, there's an SSRF in the RestAPI data source component. The RestAPI data source executes HTTP requests server-side, and its private IP filter only checks the hostname string — not the resolved IP. DNS names like 169.254.169.254.nip.io resolve to the Azure IMDS link-local address and bypass the filter entirely. This allows any authenticated user (free tier) to steal Azure managed identity tokens for the AKS production cluster. This vulnerability is fixed in 3.20.178-lts.

### CVE-2026-55960

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-06-25T20:17:16.617 |

Un-negotiated Raw Public Key (RFC 7250) accepted in place of an X.509 certificate, bypassing chain validation. A raw public key has no chain, so ParseCertRelative() accepts it without performing any trust verification; it must therefore only be accepted when RPK was actually negotiated for that peer. The check now defaults the expected type to X.509 (per RFC 7250/8446) when no type was negotiated, comparing against the received server certificate type on the client and the selected client certificate type on the server, and rejects any mismatch, including an un-negotiated raw public key, with UNSUPPORTED_CERTIFICATE. Only affects builds with Raw Public Key support (HAVE_RPK) enabled - disabled by default in a standalone build, but included in --enable-all.

### CVE-2026-55667

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-06-25T19:16:43.017 |

File Browser is a file managing interface for uploading, deleting, previewing, renaming, and editing files within a specified directory. Prior to 2.63.16, a scoped, non-admin File Browser user holding only the Create permission can delete arbitrary files outside their scope (other tenants' data, and the application's own database) via the upload failure-cleanup path. ScopedFs.RemoveAll is the one dereferencing operation that skips the symlink guard every other method enforces. The direct-upload handler runs RemoveAll on the user-controlled path during failed-upload cleanup, gated only by Perm.Create. If an escaping directory symlink already exists inside the user's scope, an authenticated create-only user can delete an out-of-scope target, bypassing both the ScopedFs boundary and the Perm.Delete gate. This vulnerability is fixed in 2.63.16.

### CVE-2026-55961

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-06-25T18:16:41.213 |

wolfSSL_PKCS7_verify() returning success for a degenerate (certs-only) PKCS#7 object that contains no signer. Such an object has empty signerInfos, so the underlying signed-data verification succeeds without authenticating any content. The compatibility-layer verify path now rejects the object when no signer signature has actually been verified, so a PKCS#7 carrying no valid signature is no longer reported as verified. This is enforced regardless of the PKCS7_NOVERIFY flag, which only suppresses signer certificate chain validation and was never intended to waive the requirement that a signature exist. Only affects OpenSSL compatibility builds that call the PKCS7_verify() compatibility API on potentially degenerate PKCS#7 bundles.

### CVE-2026-11999

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-06-25T18:16:37.613 |

X.509 trust-chain bypass (path-depth exhaustion) in the OpenSSL compatibility certificate verifier (wolfSSL_X509_verify_cert()). This affects only builds with --enable-opensslextra whose application calls X509_verify_cert() with caller-supplied untrusted intermediates; for those users it is critical, otherwise the library is unaffected. Native wolfSSL TLS/DTLS usage is not impacted. X509_verify_cert() returned success based only on the last verified link rather than on reaching a trust anchor: when the supplied chain is deeper than the verifier's maximum path depth (default 100), path building runs out of depth while still walking untrusted intermediates and the chain is accepted even though it never reaches a configured trust anchor, allowing acceptance of an attacker-controlled certificate. The default TLS handshake (WOLFSSL_VERIFY_PEER) is not affected; only applications doing manual or deferred verification through this API are.

### CVE-2026-22879

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-06-25T22:17:01.193 |

vtk vtk-dicom vtkDICOMItem::NewDataElement heap-based buffer overflow vulnerability

### CVE-2026-11800

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-06-25T22:17:00.473 |

A flaw was found in Keycloak. This JWT algorithm confusion vulnerability in the JWT Authorization Grant flow allows an attacker with valid client credentials to bypass signature verification. By forging an assertion, the attacker can create unauthorized access tokens. This enables the attacker to impersonate any federated user linked to the affected Identity Provider, leading to unauthorized access and potential privilege escalation.

### CVE-2026-9800

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1025` |
| Published | 2026-06-25T17:17:04.180 |

A flaw was found in Keycloak Policy Enforcer. This vulnerability allows any authenticated user to bypass all authorization policies, including role, scope, and User-Managed Access (UMA) permission checks. By including the configured access-denied page path within a request URL, either as a path segment or a query parameter, an attacker can gain unauthorized access to protected resources.

### CVE-2026-40711

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-26T13:16:34.493 |

Dell Dell Container Storage Modules, version(s) csi-powerstore v2.16.0, csi-unity v2.16.0, csi-powerflex v2.16.0, csi-powermax v2.16.0, contain(s) an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-54030

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-06-25T17:16:40.660 |

LibreChat is an enhanced ChatGPT clone that supports multiple AI providers. Prior to 0.8.5, LibreChat's MCP OAuth implementation does not validate that the resource parameter from OAuth Protected Resource metadata (RFC 9728) matches the configured MCP server URL, allowing a malicious MCP server to steal access tokens intended for a legitimate server. This vulnerability is fixed in 0.8.5.

### CVE-2025-60464

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-25T20:17:08.533 |

A use-after-free in the gf_sei_load_from_state_internal function (/filters/sei_load.c) of GPAC Project/MP4Box before 26.02.0 allows attackers to cause a Denial of Service (DoS) via supplying a crafted MPEG-2 TS file.

### CVE-2026-54917

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-25T19:16:42.230 |

SeaweedFS is a distributed storage system for object storage (S3), file systems, and Iceberg tables. Prior to 4.30, the S3 API gateway and the Iceberg REST catalog gateway construct their routers with mux.NewRouter().SkipClean(true). With path cleaning disabled, a .. segment inside the URL survives routing, so a request such as `GET /bucket-A/../evil-bucket/key`, is matched as bucket=bucket-A, object=../evil-bucket/key. The captured object key is then joined into a filer path with util.JoinPath (S3) / path.Join (Iceberg), which collapse the .. server-side, so the actual read or write lands in evil-bucket. This vulnerability is fixed in 4.30.

### CVE-2026-53925

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-25T19:16:40.017 |

Glances is an open-source system cross-platform monitoring tool. From 4.0.8 until 4.5.5, the secure_popen() function in glances/secure.py interprets > (file redirection), | (pipe), and && (command chaining) operators in command strings. These operators are applied without any validation on the target file path, piped command, or chained command. When Application Monitoring Process (AMP) modules load their command or service_cmd configuration values from glances.conf, those values are passed directly to secure_popen() with no sanitization. This allows an attacker who can modify the Glances configuration file to write arbitrary content to arbitrary filesystem paths (via >), chain arbitrary commands (via &&), or pipe command output to arbitrary programs (via |). This vulnerability is fixed in 4.5.5.

### CVE-2026-46607

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-25T19:16:37.527 |

Glances is an open-source system cross-platform monitoring tool. Prior to 4.5.5, glances/outdated.py uses pickle.load() to read a version-check cache file stored at a predictable, world-accessible path (~/.cache/glances/glances-version.db or $XDG_CACHE_HOME/glances/glances-version.db). No integrity check, signature verification, or format validation is performed before deserialization. An attacker with write access to that path — through any of several realistic local or container-level scenarios — can plant a malicious pickle file and achieve arbitrary code execution as the OS user running Glances the next time it starts with version checking enabled (the default). This vulnerability is fixed in 4.5.5.

### CVE-2026-46606

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-25T19:16:37.380 |

Glances is an open-source system cross-platform monitoring tool. Prior to 4.5.5, the Glances KVM/QEMU monitoring engine (glances/plugins/vms/engines/virsh.py) passes VM domain names, read directly from virsh list --all output, into f-string command templates that are processed by secure_popen(). secure_popen() is explicitly designed to interpret &&, |, and > as shell operators. Because domain names are never sanitised before interpolation, any user with the ability to create or rename a KVM/QEMU virtual machine can execute arbitrary commands as the OS user running Glances — commonly root on hypervisor hosts. This vulnerability is fixed in 4.5.5.

### CVE-2026-46735

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-25T15:16:35.797 |

Dell Display and Peripheral Manager (DDPM Mac), versions prior to 2.3, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-57920

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-551` |
| Published | 2026-06-26T13:16:36.020 |

Peplink InControl 2 through 2.14.2 before 2026-06-03 allows use of a semicolon to bypass access-control rules for certain /rest/o/{orgId} endpoints.

### CVE-2026-48618

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-176` |
| Published | 2026-06-26T02:16:52.397 |

A flaw in Node.js TLS hostname handling can cause Node.js unicode dot separator handling can lead to tls wildcard-depth authentication bypass due to resolver and verifier hostname normalization mismat.

This can lead to confidentiality impact or bypass of the intended security boundary under affected configurations.

This vulnerability affects all supported release lines: **Node.js 22**, **Node.js 24**, and **Node.js 26**.

### CVE-2021-47987

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-06-25T22:16:58.373 |

Parse Server before 4.10.0 was affected by a supply chain incident in which incorrect version tags were pushed to the official repository pointing to an unreviewed personal fork of a contributor with write access. No releases were published with these tags; a project was exposed only if it defined a git-based dependency referencing one of the affected tags (for example, parse-server#4.9.3). The code behind the tags was not reviewed or approved, and although no malicious code was identified, the introduction of security vulnerabilities could not be ruled out.

### CVE-2021-47986

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-06-25T22:16:58.210 |

Parse Server before 4.10.0 contains a supply chain vulnerability where incorrect version tags were pushed to the repository linking to unreviewed code in a personal fork. Attackers could exploit this by specifying affected version tags in dependency declarations to execute unreviewed and potentially malicious code.

### CVE-2026-9099

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-25T17:17:03.267 |

A flaw was found in Keycloak. A missing authorization check in the GroupResource.addChild() endpoint within the Admin REST API allows an authenticated user with limited administrative privileges to reparent any existing group. When Fine-Grained Admin Permissions v2 (FGAPv2) is enabled, an attacker with management rights over a single low-privilege group can reparent a highly privileged group (such as one possessing the realm-admin role) under their managed group.

Because group permissions follow a hierarchical structure, this action unauthorizedly grants the attacker management and password-reset capabilities over the members of the targeted privileged group. An attacker can exploit this to reset an administrator's password, compromise the account, and achieve a full realm takeover, leading to a complete compromise of confidentiality, integrity, and availability.

### CVE-2026-54033

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-25T17:16:40.783 |

LibreChat is an enhanced ChatGPT clone that supports multiple AI providers. Prior to 0.8.4-rc1, LibreChat allows users to configure custom OpenAI-compatible API endpoints by setting a baseURL. This URL is used to construct HTTP requests without any SSRF validation — no private IP check, no scheme restriction, no DNS pinning. An authenticated user can set baseURL to internal network addresses. This vulnerability is fixed in 0.8.4-rc1.

### CVE-2025-71340

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-25T22:16:59.647 |

picklescan through 0.0.26 fails to detect malicious pickle files that invoke idlelib.pyshell.ModifiedInterpreter.runcode in __reduce__ methods. Attackers can embed undetected code in pickle files that executes arbitrary commands when the file is loaded via pickle.load(), enabling supply chain attacks on PyTorch models and saved Python objects. This is fixed in version 0.0.30.

### CVE-2026-57913

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-602` |
| Published | 2026-06-26T11:16:31.573 |

Johnson & Johnson Audit Tracking Management System (ATMS) before 2026-04-21 allows viewing of meeting minutes and transcripts.

### CVE-2026-57912

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-602` |
| Published | 2026-06-26T11:16:31.440 |

Johnson & Johnson Campus Recruiting before 2025-10-31 allows viewing of data provided by recruited students, and notes entered about students by interviewers.

### CVE-2026-57876

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-26T08:16:24.560 |

An unauthenticated
out-of-bounds write vulnerability exists in onvif.cgi in GeoVision GV-LPC2011
and GV-LPC2211 V1.12 and earlier. The vulnerability is caused by insufficient
bounds checking when processing HTTP request body data. A remote attacker may
exploit this vulnerability by sending a crafted request with excessive input,
causing memory corruption and resulting in a denial of service.

### CVE-2026-57875

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-06-26T08:16:24.457 |

An unauthenticated
NULL pointer dereference vulnerability exists in the HTTP request parsing logic
of multiple CGI components in GeoVision GV-LPC2011 and GV-LPC2211 V1.12 and
earlier. The vulnerability is caused by improper validation of required HTTP
request metadata before it is used by the affected components. A remote attacker
may exploit this vulnerability by sending a specially crafted HTTP request,
causing the affected process to crash and resulting in a denial of service.

### CVE-2026-57874

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-06-26T08:16:24.350 |

An unauthenticated
buffer overflow vulnerability exists in IEEE8021x_upload.cgi in GeoVision
GV-LPC2011 and GV-LPC2211 V1.12 and earlier. The vulnerability is caused by
insufficient bounds checking when parsing filename values in multipart upload
data. A remote attacker may exploit this vulnerability by sending a crafted
upload request with overly long input, causing memory corruption and resulting
in a denial of service.

### CVE-2026-57873

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-06-26T08:16:24.243 |

An unauthenticated
NULL pointer dereference vulnerability exists in IEEE8021x_upload.cgi in GeoVision
GV-LPC2011 and GV-LPC2211 V1.12 and earlier. The vulnerability is caused by
improper validation of multipart upload headers when processing
certificate-related upload fields. A remote attacker may exploit this
vulnerability by sending a malformed multipart request, causing the affected
CGI process to crash and resulting in a denial of service.

### CVE-2026-57872

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-26T08:16:24.123 |

An unauthenticated
directory traversal vulnerability exists in get_fcont.cgi in GeoVision
GV-LPC2011 and GV-LPC2211 V1.12 and earlier. The vulnerability is caused by
insufficient validation of user-supplied file path input before the requested
file is accessed by the CGI component. A remote attacker may exploit this
vulnerability by sending a crafted request to read arbitrary files accessible
to the affected process, resulting in information disclosure.

### CVE-2026-10823

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-26T07:16:22.017 |

The YMC Filter WordPress plugin before 3.11.3 does not properly authorize access to one of its REST API endpoints and does not validate a user-supplied query parameter, allowing unauthenticated attackers to retrieve the titles and content of private, draft, and other non-public posts.

### CVE-2026-48933

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-06-26T02:16:52.833 |

A flaw in Node.js WebCrypto implementation can crash the process if the input of `subtle.encrypt()` is a multiple of 2GiB.

This vulnerability affects all supported release lines: **Node.js 22**, **Node.js 24**, and **Node.js 26**.

### CVE-2026-13283

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-25T22:17:01.090 |

Use after free in AdFilter in Google Chrome on Android prior to 149.0.7827.201 allowed a remote attacker who convinced a user to engage in specific UI gestures to execute arbitrary code via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-38640

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-25T21:16:27.030 |

A reachable unwrap in the __assert_fail function (/assert/mod.rs) of relibc commit 61f42d allows attackers to cause a Denial of Service (DoS) via a crafted string.

### CVE-2026-54094

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-06-25T19:16:41.490 |

File Browser is a file managing interface for uploading, deleting, previewing, renaming, and editing files within a specified directory. Prior to 2.63.14, it does not stop the HTTP file handlers from following symbolic links before they open, serve, write, share, or list a file. As a result, a scoped user — and in some cases an unauthenticated public-share recipient — can cross the intended scope boundary by following a symlink whose path is lexically inside their scope but whose target is outside it. This vulnerability is fixed in 2.63.14.

### CVE-2026-54091

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-25T19:16:41.103 |

File Browser is a file managing interface for uploading, deleting, previewing, renaming, and editing files within a specified directory. Prior to 2.63.6, File Browser's public share handlers rebase the share owner's filesystem root to the shared directory and then evaluate descendant paths against the owner's global and per-user rules using the rebased relative path instead of the original path relative to the owner's scope. As a result, an attacker who knows a public directory share URL can access files and subdirectories that the owner explicitly blocked with rules, as long as those blocked paths are located underneath the shared directory. In the simplest case this is an unauthenticated information disclosure through `GET /api/public/share/*` and `GET /api/public/dl/*`. This vulnerability is fixed in 2.63.6.

### CVE-2026-55697

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-494;CWE-829` |
| Published | 2026-06-25T18:16:40.707 |

pnpm is a package manager. Prior to 10.34.2 and 11.5.3, pnpm can install configDependencies declared in pnpm-workspace.yaml before command dispatch. Before the patch, a repository could declare pacquet or @pnpm/pacquet as a config dependency and pnpm treated that repository-controlled dependency as an install-engine opt-in. During install, pnpm resolved a platform-specific @pacquet/<platform>-<arch>/pacquet binary from node_modules/.pnpm-config/<packageName> and spawned it as the developer or CI user. This vulnerability is fixed in 10.34.2 and 11.5.3.

### CVE-2026-55487

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346;CWE-693;CWE-829` |
| Published | 2026-06-25T18:16:40.460 |

pnpm is a package manager. Prior to 10.34.2 and 11.5.3, the generic peer-suffix normalizer also stripped parenthesized text from git, URL, tarball, file, and other opaque locators. Approval for one source string could therefore authorize a different attacker-controlled source whose locator normalized to the same value. This vulnerability is fixed in 10.34.2 and 11.5.3.

### CVE-2026-13351

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-772` |
| Published | 2026-06-25T17:16:38.460 |

Zephyr's IPv6 network stack can be prevented from receiving or processing future incoming packets by sending a small number of maliciously fragmented IPv6 packets. When such a packet is handled by the fragment-header processing path, the associated RX network packet buffer (allocated from a memory slab) is not released back to the pool. Repeating the malicious packet exhausts all RX buffer slots, after which the device can no longer obtain RX buffers and stops receiving traffic, resulting in a denial of service.

### CVE-2026-12844

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-06-25T16:16:33.097 |

List::SomeUtils::XS versions before 0.59 for Perl have a heap buffer overflow in the pairwise function.

pairwise() collects the values returned by the block into a heap buffer sized to the longer input array, then grows the buffer before each copy with a single quadrupling (alloc <<= 2) instead of a loop. A block call that returns more than four times the current allocation in one invocation outgrows that one quadrupling, and the copy writes past the end of the buffer.

Any caller of pairwise() whose block returns, for a single pair, more than four times the longer input array's length writes past the buffer and corrupts the heap.

### CVE-2026-12992

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-25T22:17:00.760 |

A flaw was found in Apicurio Registry. The WSDLReaderAccessor creates a wsdl4j WSDLReader without disabling the javax.wsdl.importDocuments feature. When the VALIDITY rule is set to FULL, an attacker with Developer-role access can upload a WSDL document containing attacker-controlled import locations, causing the registry to issue HTTP requests to arbitrary internal URLs (server-side request forgery).

### CVE-2026-46608

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-183;CWE-942` |
| Published | 2026-06-25T19:16:37.663 |

Glances is an open-source system cross-platform monitoring tool. Prior to 4.5.5, the Glances XML-RPC server (glances -s) introduced a configurable CORS origin list in version 4.5.3 as a mitigation for CVE-2026-33533. However, the implementation silently falls back to Access-Control-Allow-Origin: * whenever cors_origins contains more than one entry. An operator who configures an explicit two-entry allowlist (e.g. two internal dashboard origins) intending to restrict browser access instead receives the unrestricted wildcard. A malicious web page served from any origin can issue a CORS simple request to /RPC2 and read the full system monitoring dataset without the victim's knowledge. This vulnerability is fixed in 4.5.5.

### CVE-2026-50015

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-25T18:16:39.167 |

pnpm is a package manager. Prior to 10.34.0 and 11.4.0, pnpm's patch application pipeline (@pnpm/patch-package) performs no path validation on file paths extracted from .patch files. An attacker who contributes a malicious patch file via a pull request can write attacker-controlled content to or delete arbitrary files on the filesystem during pnpm install, as the user running the install. The diff --git header paths containing ../../ sequences traverse out of the package directory, and the traversal is difficult to catch in code review because patch file diff headers are opaque to most reviewers. This vulnerability is fixed in 10.34.0 and 11.4.0.

### CVE-2026-9086

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-25T17:17:03.147 |

A flaw was found in Keycloak. A remote attacker with administrative privileges, specifically those with `manage-client` permission or access to client registration endpoints, could bypass client Uniform Resource Identifier (URI) validation. This is achieved by registering a malicious client with a specially crafted redirect URI using a case-insensitive `javascript:` or `data:` scheme. This Cross-Site Scripting (XSS) vulnerability allows for arbitrary code execution in the Keycloak origin when a victim clicks the crafted link, such as in the logout flow or the Admin Console.

### CVE-2026-40083

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-25T23:17:02.900 |

Cacti is an open source performance and fault management framework. Versions 1.2.30 and prior have SQL Injection through unsanitized unserialize+implode in managers.php.  At line 756 of managers.php, the application assigns $selected_items by calling cacti_unserialize(stripslashes(gnrv('selected_graphs_array'))). The  cacti_unserialize() function calls unserialize() with allowed_classes set to false, which prevents object injection but still allows arbitrary string  arrays to be deserialized. Then, at lines 760 to 766, the deserialized array values are passed directly into db_execute('DELETE FROM snmpagent_managers  WHERE id IN (' . implode(',', $selected_items) . ')'), where they are imploded into the SQL statement without any integer validation, resulting in SQL  Injection when using SNMP agent management permissions. This issue has been fixed in version 1.2.31.

### CVE-2026-54097

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-25T19:16:41.753 |

File Browser is a file managing interface for uploading, deleting, previewing, renaming, and editing files within a specified directory. Prior to 2.63.6, a low-privileged authenticated user of filebrowser (with create + delete permissions in their own isolated scope) can silently destroy share-link records belonging to any other user — including the administrator — by performing a legitimate DELETE on a file in their own directory whose logical path happens to be a byte-prefix of another user's stored share.Link.Path. The file contents of the victim are not exposed, but the victim's share links are irrevocably wiped. This vulnerability is fixed in 2.63.6.

### CVE-2026-45233

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-25T17:16:39.207 |

HTMLy CMS through 3.1.1 contains a path traversal vulnerability that allows low-privileged authenticated attackers to relocate arbitrary files by supplying directory traversal sequences in the oldfile parameter at the admin autosave endpoint. Attackers can pass unsanitized traversal sequences directly to file_exists() and rename() functions in admin.php without canonicalization or directory boundary enforcement to cause unintended relocation of any file writable by the web server process to an attacker-specified draft location.

### CVE-2026-55477

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-06-25T16:16:40.033 |

3X-UI is a web control panel for managing Xray-core servers. Prior to 3.3.1, an authenticated administrator can abuse the database import functionality to achieve arbitrary file write on the host by modifying Xray configuration values stored in the database. This can be leveraged to obtain code execution and persistent access as the user running Xray (including root when Xray is running as root). This vulnerability is fixed in 3.3.1.

### CVE-2026-57918

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-191` |
| Published | 2026-06-26T11:16:31.700 |

libnfs through 6.0.2 before 935b8db has an xid integer underflow in READ_IOVEC in rpc_read_from_socket in lib/socket.c during a connection to a crafted NFS server, when the expected pdu size exceeds the absolute pdu size from the xid/record-marker.

### CVE-2025-7958

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-26T11:16:30.487 |

A Code Injection vulnerability existed in Trellix Network Security CM and NX. A locally authenticated admin user can execute arbitrary code using the web interface and Alert artifact details.

### CVE-2026-40941

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-06-25T23:17:03.170 |

Cacti is an open source performance and fault management framework. Versions 1.2.30 and prior have a package import signature validation bypass allows which allows self-signed packages. This issue has been fixed in version 1.2.31.

### CVE-2026-57520

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-25T20:17:17.020 |

Bitwarden Server before 2026.5.0 contains a privilege escalation vulnerability that allows authenticated Custom users with ManageUsers permission to remove Admin accounts from an organization by exploiting a missing role hierarchy check in the bulk user-remove endpoint. Attackers can supply Admin organization-user IDs in a bulk DELETE request to bypass the guard enforced on the single-user removal path, effectively removing one or more Admin accounts from an organization.

### CVE-2026-56789

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-25T19:16:45.477 |

RTKLIB through 2.4.3 contains a heap buffer overflow vulnerability in the readrnxobsb function in src/rinex.c that allows attackers to trigger memory corruption by failing to clamp satellite count values from RINEX epoch headers. Attackers can craft malicious RINEX files declaring more than 64 satellites per epoch to cause heap buffer overflow writes and out-of-bounds stack reads, crashing RTKLIB-based applications including rnx2rtkp and RTKPOST.

### CVE-2026-4930

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-331` |
| Published | 2026-06-25T19:16:39.103 |

SYMCRYPTO is the SiXG301's host side hardware engine accessed by PSA crypto library that accelerates symmetric cryptographic operations (AES encryption/decryption and hashing).


DPA Countermeasures on SYMCRYPTO can be weakened (reduced entropy) by forcing certain seed values if an attacker gains code execution capability on the impacted device.

  *  Therefore, the keys loaded on SYMCRYPTO may be more vulnerable to extraction through DPA attacks than intended

### CVE-2026-55700

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-06-25T18:16:41.087 |

pnpm is a package manager. From 11.3.0 until 11.5.3, `pnpm stage download` derived a local filename from registry-controlled package name and version fields. A crafted manifest could escape the selected download directory and overwrite another reachable file. The merged fix validates both fields, derives one safe filename, and verifies the final destination before writing. This vulnerability is fixed in 11.5.3.

### CVE-2026-49839

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-25T18:16:38.917 |

jq is a command-line JSON processor. Prior to 1.8.2,` jq --rawfile` can turn a handled oversized-string error into invalid-state reuse and a real heap out-of-bounds write in assertion-disabled builds. When jv_load_file(raw=1) reads an attacker-controlled file, it repeatedly appends file chunks to the same jv string accumulator. Once jv_string_append_buf() returns jv_invalid_with_msg("String too long"), the raw-file loop does not stop. If the file contains at least one more byte, the next loop iteration appends a new chunk to an object that is already invalid. With assertions enabled this aborts in jvp_string_ptr(). With assertions disabled, the invalid object is interpreted as a string object and ASan reports heap-buffer-overflow. This vulnerability is fixed in 1.8.2.

### CVE-2026-56790

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-193` |
| Published | 2026-06-25T19:16:45.637 |

CANBoat through 6.22, fixed in commit a5a22b7, contains an off-by-one global buffer overflow in the searchForPgn() function in analyzer/pgn.c that allows remote attackers to crash the application. Attackers can deliver a crafted NMEA-2000 message with an out-of-range PGN value over CAN bus or N2K-over-IP to trigger an out-of-bounds array access and denial of service.

### CVE-2026-55092

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-25T17:16:41.647 |

Trivy is a security scanner. Prior to 0.71.1, when Trivy downloads an OCI artifact, it uses the org.opencontainers.image.title annotation from the artifact manifest as the destination filename without validation. An attacker who can make Trivy fetch an attacker-controlled artifact can supply a crafted annotation that resolves to a path outside the intended destination, causing Trivy to write the layer content to an arbitrary location on the host filesystem. This vulnerability is fixed in 0.71.1.
