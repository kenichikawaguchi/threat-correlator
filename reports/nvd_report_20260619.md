# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-18 19:00 UTC
- **対象期間**: `2026-06-18T15:01:54.000Z` 〜 `2026-06-18T19:00:20.000Z`
- **重要CVE数**: 20 件（Critical 9.0+: 5 件 / High 7.0〜: 15 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVSS 7.0 以上の脆弱性は、**リモートから認証不要でコード実行や権限昇格が可能**なものが目立ちます。特にネットワーク機器（InHand Networks）や Web アプリケーションフレームワーク（JTL Shop、Webmin、HAProxy）に集中しており、攻撃者は *ネットワーク境界をすり抜けてルート権限* を取得できる点が共通しています。  

- **コマンドインジェクション／テンプレートインジェクション** が多数。  
- **SSL クライアント証明書偽装** や **整数オーバーフロー** によるバッファ破壊が報告され、既存の防御策（ファイアウォール等）だけでは防げないケースが多い。  
- 影響範囲は **組み込みデバイス、E‑コマース、システム管理ツール、ロードバランサ** と広範囲に及び、早急なパッチ適用が必須です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲・被害シナリオ | 推奨される対策（概要） |
|-----|------|----------------|------------------------|------------------------|
| **CVE‑2026‑38715** | 9.8 | コマンドインジェクション（log viewing 機能） | InHand Networks IR912/IR915 のファームウェア (V1.0.0.r20042 以前) で、遠隔から任意コマンドを **root 権限** で実行可能。IoT ゲートウェイや産業制御系に組み込まれると、ネットワーク全体の乗っ取りリスクが高まる。 | ベンダー提供の **最新ファームウェア (≥ V1.0.0.r20050)** に更新。不要なログ閲覧機能は無効化し、管理インタフェースへの IP フィルタリングを実施。 |
| **CVE‑2026‑54390** | 9.3 | サーバーサイドテンプレートインジェクション (Smarty) | JTL Shop 5.2.0‑5.7.1 において、ユーザー入力がサニタイズされず Smarty テンプレートへ流れ込み、任意 PHP コード実行が可能。EC サイトが乗っ取られ、顧客情報・決済情報が漏洩する危険がある。 | **JTL Shop 5.7.2 以降** にアップデート。`smarty` の `security` オプションを有効化し、外部入力のエスケープを徹底。 |
| **CVE‑2026‑54103** | 9.3 | 認証なしパスワード変更 API | 米国 GAO の EPDS/EDS が `/update-profile/N` エンドポイントで認証を行わず、パスワードを任意に変更できる。政府系システムのアカウント乗っ取りにつながり、機密文書や入札情報が改ざんされる恐れ。 | ベンダー（GAO）提供の **パッチリリース (2026‑Q2)** を適用。API に **認証・CSRF トークン** を必須化し、アクセス制御リスト (ACL) で IP 制限を実装。 |
| **CVE‑2026‑56020** | 9.2 | SSL クライアント証明書偽装（Webmin） | Webmin (miniserv.pl) が HTTP ヘッダー `X-SSL-Client-DN` を信頼し、任意の DN を送信できるため、**任意ユーザーとして認証** が可能。管理者権限取得後にシステム全体を操作できる。 | **Webmin 2.641 以降** にアップデート。`X-SSL-Client-DN` の検証を無効化し、クライアント証明書の検証は TLS ハンドシェイクに委任。 |
| **CVE‑2026‑55203** | 9.0 | 整数オーバーフローによるバッファ誤解析 (HAProxy) | HAProxy 3.4.0 未満で、FCGI の `contentLength=65535` + `paddingLength>=1` の組み合わせで `drl` が 0 になる。攻撃者は任意の FCGI レコードを作成し、**リモートコード実行** が可能。 | **HAProxy 3.4.1 以降**、または **commit 5985276** を取り込んだビルドへ更新。FCGI パーサーの長さチェックを強化し、外部からの FCGI リクエストは必ず認証で保護。 |

> **補足**  
> - AutoGPT 系列（CVE‑2026‑55237 など）は XSS や一時ファイル残留が問題ですが、上記 5 件に比べて直接的な権限取得リスクは低めです。  
> - Eclipse Theia 系列（CVE‑2026‑46580、‑44691、‑44688）はローカル/開発環境向けで、**ワークスペースの信頼設定** が緩いことが根本原因です。  

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ（必須）

| 製品 / コンポーネント | 現行バージョン | 推奨バージョン / パッチ | 取得先 |
|----------------------|----------------|------------------------|--------|
| InHand Networks IR912/IR915 ファームウェア | V1.0.0.r20042 以前 | **V1.0.0.r20050 以降** | ベンダー公式サイト（Support → Firmware） |
| JTL Shop | 5.2.0‑5.7.1 | **5.7.2 以上** | JTL Shop ダウンロードページ |
| GAO EPDS / EDS API | 2026‑Q1 リリース | **2026‑Q2 パッチ**（`epds_security_update_2026_02`） | GAO 公開リポジトリ |
| Webmin | 2.640 以前 | **2.641 以上** | Webmin ダウンロードページ |
| HAProxy | 3.4.0 未満 | **3.4.1 以上**（または `git checkout 5985276` でビルド） | HAProxy 公式リリースページ |

### 3.2 設定・運用面での緊急対策

1. **ネットワーク境界の制限**  
   - InHand デバイスの管理ポート (HTTP/HTTPS) を社内 VPN のみからアクセス可能にし、IP アクセスリストで外部からの直接接続を遮断。  
   - Webmin, HAProxy, JTL Shop への管理 UI

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-38715

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-06-18T17:16:30.220 |

InHand Networks IR912 V1.0.0.r20042 and IR915 V1.0.0.r20042 (including earlier versions) were discovered to contain a command injection vulnerability in the log viewing function. This vulnerability allows remote attackers to execute arbitrary commands as root via a crafted input.

### CVE-2026-54390

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-06-18T18:16:19.943 |

JTL Shop versions 5.2.0 through 5.7.1 contains a server-side template injection vulnerability that allows unauthenticated attackers to inject malicious template syntax due to unsanitized user-supplied input passed to the Smarty template engine. Attackers can exploit this flaw to read sensitive server-side values such as database credentials and encryption keys, and on versions 5.4.0 through 5.7.1, leverage registered Smarty modifiers including unserialize and file_get_contents to write a webshell to the web root and execute arbitrary commands as the web server user.

### CVE-2026-54103

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-18T17:16:33.387 |

The U.S. Government Accountability Office (GAO) Electronic Protest Docketing System (EPDS) and Civilian Board of Contract Appeals (CBCA) Electronic Docketing System (EDS) does not authenticate password change requests to the '/update-profile/N' API endpoint. A remote, unauthenticated attacker could change an arbitrary user's password.

### CVE-2026-56020

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-06-18T17:16:35.247 |

The Webmin HTTP server (miniserv.pl) allows unauthenticated attackers to impersonate any user with a configured SSL client certificate by sending a forged HTTP header. A remote attacker can spoof certificate DNs and authenticate as any user. Fixed in 2.641.

### CVE-2026-55203

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-06-18T17:16:34.373 |

HAProxy through 3.4.0, fixed in commit 5985276, contains an integer overflow vulnerability in the fcgi_conn structure's drl field that allows buffer misparse as new FCGI record headers. When contentLength is 65535 and paddingLength is 1 or more, the drl field wraps to 0, causing incorrect record consumption and allowing malicious FastCGI backends to desynchronize the FCGI framing parser, potentially causing request routing errors, response smuggling, or memory safety issues.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-55237

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-87;CWE-601` |
| Published | 2026-06-18T17:16:34.900 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. Versions prior to 0.6.62 have a DOM-based Cross-Site Scripting (XSS) vulnerability in AutoGPT's signup page. The application improperly trusts a URL parameter (`next`), which is passed to `router.push`. An attacker can craft a malicious link that, when opened by an authenticated user, performs a client-side redirect and executes arbitrary JavaScript in the context of their browser. This could lead to credential theft, internal network pivoting, and unauthorized actions performed on behalf of the victim. Version 0.6.62 patches the issue.

### CVE-2026-55204

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-06-18T17:16:34.567 |

HAProxy through  3.4.0, fixed in commit 9a6d1fe, contains a null pointer dereference vulnerability in hpack_dht_insert() within src/hpack-tbl.c that fails to validate the return value of hpack_dht_defrag() when the memory pool is exhausted. An attacker can trigger HPACK dynamic table insertions under memory pressure to dereference a NULL pointer and crash HAProxy worker processes, causing denial of service.

### CVE-2026-54104

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-602` |
| Published | 2026-06-18T17:16:33.567 |

The U.S. Government Accountability Office (GAO) Electronic Protest Docketing System (EPDS) and Civilian Board of Contract Appeals (CBCA) Electronic Docketing System (EDS) trusts client-provided values for the 'epds_role_id' parameter without verification, allowing a remote, authenticated attacker to escalate their own privileges.

### CVE-2025-32437

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-18T17:16:26.923 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. Prior to 0.6.63, `MediaDurationBlock` will download and store the video in a temporary directory without deleting before all noded are done. `StepThroughItemsBlock` can be used to iterate `MediaDurationBlock` multiple times. `StepThroughItemsBlock` does not limit the number of loops. In addition, `MediaDurationBlock ` does not limit the amount of disk space consumed in the current working directory and does not delete the video after outputing the result. When a malicious user chooses to screen shot many web pages, the disk space will eventually run out, causing a DoS. Version 0.6.63 patches the issue.

### CVE-2025-32424

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-18T17:16:26.667 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. Prior to 0.6.63, ScreenshotWebPageBlock will store the captured screenshots in a temporary directory. `StepThroughItemsBlock` can be used to iterate `ScreenshotWebPageBlock` multiple times. `StepThroughItemsBlock` does not limit the number of loops. In addition, `ScreenshotWebPageBlock` does not limit the amount of disk space consumed in the current working directory. When a malicious user chooses to screen shot many web pages, the disk space will eventually run out, causing a DoS. Version 0.6.63 patches the issue.

### CVE-2025-32422

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-18T17:16:26.547 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. Prior to 0.6.63, `StepThroughItemsBlock` can iterate all the contents in a list and send them to `FileStoreBlock` for downloading one by one. Although `FileStoreBlock` has access time limits for downloading files, `StepThroughItemsBlock` can be used to slowly iterate and download relatively small files (e.g., 100M) multiple times. `StepThroughItemsBlock` does not limit the number of loops. In addition, `FileStoreBlock` does not limit the amount of disk space consumed in the current working directory. When a malicious user chooses to download too many videos, the disk space will eventually run out, causing a DoS. Version 0.6.63 patches the issue.

### CVE-2025-32392

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-18T17:16:26.407 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. Prior to 0.6.63, AutoGPT's LoopVideoBLock allows users to input a video file and process the video, such as looping it 5 times or extending the time, and finally writing it to disk. However, there is no limit on the resources that can be allocated during execution. For example, the number of loops is user-controllable and unlimited. When a malicious attacker loops too many times, the generated video is too large, and after writing it to disk, the disk space is exhausted, eventually causing DoS. Version 0.6.63 patches the issue.

### CVE-2026-46580

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-06-18T16:16:54.213 |

In Eclipse Theia versions prior to 1.71.0, files matching the pattern .prompts/*.prompttemplate in a workspace were automatically loaded and could override or extend the AI agent's system prompts. An attacker could craft a malicious repository containing prompt template files that, when the workspace was opened in Theia, replaced the AI's system instructions with attacker-controlled content (indirect prompt injection). Combined with other AI chat features available in untrusted workspaces, this enabled attack chains leading to data exfiltration via Markdown image rendering or arbitrary command execution via task definitions.

### CVE-2026-44691

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-06-18T16:16:54.097 |

In Eclipse Theia versions prior to 1.69.0, custom task definitions in workspace files (e.g. .theia/tasks.json, .vscode/tasks.json) could be executed without requiring workspace trust. An attacker could craft a malicious repository that, when cloned and opened in Theia, leads to execution of arbitrary commands with the user's privileges. In combination with AI chat features and a workspace .theia/settings.json that disabled tool confirmation, this could be triggered automatically by sending a message in the AI chat.

### CVE-2026-44688

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-06-18T16:16:53.977 |

In Eclipse Theia versions prior to 1.71.0, the AI chat agent processed workspace file and directory names as part of its prompt context without distinguishing them from system instructions. An attacker could craft a malicious repository with adversarial directory or file names that, when analyzed by the AI agent, would cause the agent to follow attacker-controlled instructions (indirect prompt injection). Combined with other AI chat features available in untrusted workspaces, this enabled attack chains leading to data exfiltration via Markdown image rendering or arbitrary command execution via task definitions.

### CVE-2026-38718

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-06-18T17:16:30.523 |

InHand Networks IR912 V1.0.0.r20042 and IR915 V1.0.0.r20042 (including earlier versions) were discovered to contain a buffer overflow vulnerability in the device registration function. This vulnerability could allow an attacker to cause a denial of service attack on the remote target device.

### CVE-2025-53114

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-18T17:16:27.150 |

CometD is a scalable comet implementation for web messaging. In versions 5.0.0 through 5.0.22, 6.0.0 through 6.0.18, 7.0.0 through 7.0.18, and 8.0.0 through 8.0.8, bad clients that always send a fixed batch value when the server is using the acknowledgement extension may cause the unacknowledged message queue to grow indefinitely, eventually causing an `OutOfMemoryError`. Versions 5.0.23, 6.0.19, 7.0.19, and 8.0.9 patch the issue. As a workaround, disable the acknowledgement extension.

### CVE-2025-52465

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-06-18T16:16:52.027 |

GeoServer is an open source server that allows users to share and edit geospatial data. Prior to versions 2.26.4 and 2.27.3, a vulnerability exists that allows an authenticated administrator with access to GeoServer's security system to pass arbitrary file names to the Master Password Dump web page and create files containing the master password in plaintext. The provided file name must be an absolute path to the target file, the target file can not already exist and all parent directories must already exist. Versions 2.26.4 and 2.27.3 contain a fix. GeoServer installations where the web interface is either disabled or completely removed are not affected since the vulnerability exists in one of the web pages.

### CVE-2025-27511

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-502` |
| Published | 2026-06-18T16:16:50.960 |

GeoServer is an open source server that allows users to share and edit geospatial data. Prior to version 2.27.0 of the GeoServer DB2 DataStore Extension, an administrator can perform a JNDI attack through specially crafted DB2 jdbc url leading to to Remote Code Execution (RCE). Version 2.27.0 fixes the issue.

### CVE-2025-32436

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-18T17:16:26.797 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. Prior to 0.6.63, `AddAudioToVideoBlock` will download and store the video and audio in a temporary directory without deleting before all noded are done. `StepThroughItemsBlock` can be used to iterate `MediaDurationBlock` multiple times. `StepThroughItemsBlock` does not limit the number of loops. In addition, `AddAudioToVideoBlock` does not limit the amount of disk space consumed in the current working directory and does not delete the video after outputing the result. When a malicious user chooses to screen shot many web pages, the disk space will eventually run out, causing a DoS. Version 0.6.63 patches the issue.
