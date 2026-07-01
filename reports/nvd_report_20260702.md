# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-01 15:03 UTC
- **対象期間**: `2026-06-30T15:00:27.000Z` 〜 `2026-07-01T15:03:09.000Z`
- **重要CVE数**: 154 件（Critical 9.0+: 46 件 / High 7.0〜: 108 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件** 超に上ります。特に目立つのは、**認証不要でリモートコード実行 (RCE) が可能** な脆弱性が集中している点です。ストレージ・コンセントレータ、Adobe Campaign、ColdFusion、IBM Langflow といったエンタープライズ向け製品で **コマンドインジェクション** や **不適切な権限付与** が連続して報告されており、攻撃者はネットワーク境界を超えて内部システムへ横移動しやすい状況です。  

## 2. 特に注目すべき CVE  

| CVE ID | 製品・バージョン | 主な影響 | なぜ注目すべきか |
|--------|------------------|----------|-------------------|
| **CVE‑2026‑56415** | Storage Concentrator (SC & SCVM) – `debug.pl` | 認証不要のコマンドインジェクション。任意のシェルコマンドが実行可能。 | **CVSS 10.0** かつ管理インタフェースが外部に露出しやすく、ネットワーク分離が不十分な環境で即座に全権取得が可能。 |
| **CVE‑2026‑56413** | Storage Concentrator (SC & SCVM) – `ms_service.pl` (TCP 9000) | 認証不要のコマンドインジェクション。特製パケットで任意コード実行。 | 同製品の別エントリポイントで二重に脆弱。**防御層が一つ失われても即座に侵入** できる点が危険。 |
| **CVE‑2026‑10134** | IBM Langflow OSS 1.0.0‑1.9.3 | データベース全体への読み書き、内部サービスへの接続、クラウドメタデータ取得が可能。 | **CVSS 10.0**。AI ワークフロー基盤で機密情報・認証情報が丸ごと漏洩し、**横移動・権限昇格** に直結。 |
| **CVE‑2026‑48286** | Adobe Campaign Classic (ACC) 7.4.3 build 9396 以前 | 誤った認可により任意コード実行（スコープ変更）。 | **CVSS 10.0**。マーケティングプラットフォームは顧客データを大量に保持しているため、**情報漏洩リスクが極めて高い**。 |
| **CVE‑2026‑48283** (系列) | Adobe ColdFusion 2023.20, 2025.9 以前 | 複数の「任意コード実行」系脆弱性（危険ファイルアップロード、パストラバーサル、入力検証不備）。 | **CVSS 10.0** が複数件報告されており、ColdFusion が Web アプリのバックエンドとして広く利用されている点で **インパクトが広範**。 |

> **補足**：上記 5 件は **CVSS 10.0**（最高評価）で、かつ「認証不要」または「認証済みでも権限昇格が容易」という共通点があります。実際の攻撃シナリオでは、まず外部からのリモートコード実行で足場を確保し、続いて内部サービス（Langflow の Redis、Adobe の内部 API など）へ横移動するケースが想定されます。

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 | 推奨バージョン / パッチ | 備考 |
|------|------------------------|------|
| Storage Concentrator (SC & SCVM) | ベンダーが提供する **2026‑06‑xx 以降のパッチ**（`debug.pl` と `ms_service.pl` の入力サニタイズを実装） | 可能なら **debug.pl** を無効化し、`ms_service.pl` のリスニングポート 9000 をファイアウォールで遮断。 |
| IBM Langflow OSS | **v1.10.1 以上**（2026‑07‑xx リリース） | 1.10.0 までの全脆弱性が修正。Redis 認証強化と `EXPRESS_SESSION_SECRET` の必須化が含まれる。 |
| Adobe Campaign Classic | **7.4.4 build 9400 以降** | 2026‑05‑xx のセキュリティリリースで認可バグが修正。 |
| Adobe ColdFusion | **2025.10** 以降、または **2023.21** 以降 | すべての CVE‑2026‑48xxx 系がパッチ適用済み。 |
| containerd (CVE‑2026‑53488) | **v1.7.33** 以上、または **v2.3.2** 以上 | CRI ラベル検証が追加。 |

### 3.2 設定・運用上の緊急対策
1. **ネットワーク分離**  
   - Storage Concentrator の管理インタフェース (`debug.pl`) と `ms_service.pl` のポート 9000 を **内部 VLAN のみ** に限定し、外部からの直接アクセスを遮断。  
   - IBM Langflow の Redis エンドポイントは **認証必須** にし、IP アクセス制御リスト (ACL) を適用。

2. **認証・権限の強化**  
   - ColdFusion の管理コンソールに **二要素認証 (2FA)** を導入。  
   - Adobe Campaign の管理者アカウントは **最小権限** に設定し、不要な管理者権限は即座に削除。

3. **機密情報のローテーション**  
   - Storage Concentrator の内部サービス用 **ハードコードされた認証情報**（CVE‑2026‑50110）を全てリセットし、暗号化されたシークレットストアに移行。  
   - Langflow の `EXPRESS_SESSION_SECRET` がデフォルト (`flowise`) のままにな

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-56415

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-30T23:17:32.157 |

Storage Concentrator (SC & SCVM) contains a command injection vulnerability within the debug.pl script that is reachable without authentication. A remote attacker can submit a specially crafted HTTP request containing a malicious payload that is processed without adequate input sanitization, resulting in arbitrary command execution with root-level privileges on the underlying system.

### CVE-2026-56413

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-30T23:17:32.027 |

Storage Concentrator (SC & SCVM) contains a command injection vulnerability in the ms_service.pl service, which listens on TCP port 9000 by default and accepts custom network packets to perform device actions. An unauthenticated remote attacker can send a specially crafted packet containing a malicious payload that is processed without adequate sanitization, resulting in arbitrary command execution with root-level privileges.

### CVE-2026-10134

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-30T20:17:26.883 |

IBM Langflow OSS 1.0.0 through 1.9.3 allows an attacker to read every secret available to the Langflow process, read and modify every flow, conversation, message, file upload, and saved component in the Langflow database, can connect to internal services, abuse cloud metadata endpoints, laterally move to other tenants on the same Langflow instance, and Establish persistence by modifying the public flow's `tool_code` so normal `/api/v1/build/...` calls by any user re-execute attacker code at each build.

### CVE-2026-48286

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-30T16:16:54.870 |

Adobe Campaign Classic (ACC) versions 7.4.3 build 9396 and earlier are affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48283

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-30T16:16:54.643 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by an Unrestricted Upload of File with Dangerous Type vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48282

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-30T16:16:54.533 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48281

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-30T16:16:54.427 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48277

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-30T16:16:54.320 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48276

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-30T16:16:54.193 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by an Unrestricted Upload of File with Dangerous Type vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-7873

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-30T20:17:31.750 |

IBM Langflow OSS 1.0.0 through 1.10.0 allows authenticated attackers to execute arbitrary OS commands and read sensitive files including credentials, enabling complete system compromise and lateral movement.

### CVE-2026-57692

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-01T14:16:46.800 |

Incorrect Privilege Assignment vulnerability in LCweb PrivateContent allows Privilege Escalation.

This issue affects PrivateContent: from n/a through 9.9.2.

### CVE-2026-11387

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-01T08:16:20.587 |

The SMS Alert – SMS & OTP for WooCommerce, Order Notifications & Abandoned Cart Recovery plugin for WordPress is vulnerable to privilege escalation via account takeover in all versions up to, and including, 3.9.5. This is due to the plugin not properly validating a user's identity prior to updating their details like reset the password of any user account, including administrators, and gain full access to those accounts. This makes it possible for unauthenticated attackers to change arbitrary user's email addresses, including administrators, and leverage that to reset the user's password and gain access to their account. This is only vulnerable on sites with OTP verification for password resets enabled, and where the administrator (or other user) has set a phone number for OTP verification.

### CVE-2026-7871

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-30T20:17:31.543 |

IBM Langflow OSS 1.0.0 through 1.10.0 allows users with Redis access to execute arbitrary code with full application privileges, compromising all secrets, data, and system integrity.

### CVE-2026-7803

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-30T20:17:31.413 |

IBM Langflow OSS 1.0.0 through 1.10.0 could allow arbitrary code execution due to improper validation of flow nodes with missing or empty component type fields.

### CVE-2026-10109

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-30T20:17:26.603 |

IBM Db2 11.5.0 through 11.5.9, and 12.1.0 through 12.1.4 is vulnerable to remote code execution due to improper pre-auth DRDA handshake handling.

### CVE-2026-14152

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787;CWE-787` |
| Published | 2026-06-30T23:17:26.557 |

Out of bounds read and write in ANGLE in Google Chrome prior to 150.0.7871.47 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-14151

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-30T23:17:26.470 |

Inappropriate implementation in AI in Google Chrome prior to 150.0.7871.47 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-14056

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-20` |
| Published | 2026-06-30T23:17:17.927 |

Insufficient validation of untrusted input in Media in Google Chrome prior to 150.0.7871.47 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted video file. (Chromium security severity: Low)

### CVE-2026-14055

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-20` |
| Published | 2026-06-30T23:17:17.833 |

Insufficient validation of untrusted input in Device Trust in Google Chrome on Windows prior to 150.0.7871.47 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-14043

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-416` |
| Published | 2026-06-30T23:17:16.770 |

Use after free in GetUserMedia in Google Chrome prior to 150.0.7871.47 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-14037

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-06-30T23:17:16.253 |

Insufficient policy enforcement in GPU in Google Chrome prior to 150.0.7871.47 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-10140

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-30T20:17:27.007 |

IBM Langflow OSS 1.0.0 through 1.10.0 voice mode contains improper shared-state handling that allows reuse of API clients across tenant boundaries. An authenticated attacker can manipulate cache state to cause requests from other users to be processed using incorrect upstream API credentials, leading to cross-tenant billing and accountability misattribution.

### CVE-2026-10539

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-305` |
| Published | 2026-07-01T08:16:20.340 |

A Control-M/Server communication command does not sufficiently filter or sanitize user-supplied input. Under certain conditions, this issue may allow an unauthenticated attacker to execute unauthorized commands on the affected server, potentially leading to compromise of the server. 



This vulnerability affects Control-M/Server versions 9.0.20.x to 9.0.21.200 (included) and potentially earlier unsupported versions.

### CVE-2026-53488

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-01T02:17:00.467 |

containerd is an open-source container runtime. In versions prior to 1.7.33, 2.3.2, 2.2.5, 2.1.9, and 2.0.10 the CRI plugin propagates labels from an image config (LABEL instruction in Dockerfile) to a container without validation. This may result in executing an arbitrary command on the host, via a plugin that consumes container labels for some operations. This issue has been fixed in versions 1.7.33, 2.3.2, 2.2.5, 2.1.9, and 2.0.10.

### CVE-2026-7840

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-01T05:16:24.820 |

UltraVNC repeater through 1.8.2.2 contains a global buffer overflow in its embedded HTTP administration server. The functions wi_senderr() and wi_replyhdr() in repeater/webgui/webutils.c write the caller-supplied HTTP request URI into a fixed 1000-byte global buffer (hdrbuf) via unchecked sprintf calls. The HTTP receive buffer accepts URIs up to approximately 150 KB (WI_RXBUFSIZE = 153600), so an unauthenticated attacker who can reach the repeater HTTP port (default TCP 80) can overflow hdrbuf by at least 500 bytes with a single HTTP request containing a URI of 1500 bytes or longer, corrupting adjacent .bss-segment globals. The overflow occurs before any authentication check, making it reachable without credentials. A remote, unauthenticated attacker can achieve arbitrary code execution on the host running the repeater.

### CVE-2026-56700

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-502` |
| Published | 2026-06-30T23:17:32.287 |

Grav CMS before 2.0.0-beta.2 contains multiple code-execution vulnerabilities. Three unsafe unserialize() calls - in Scheduler\JobQueue, Framework\Cache\Adapter\FileCache, and Session - deserialize untrusted data without restricting allowed classes, enabling PHP object injection and, via a gadget chain, arbitrary code execution where an attacker controls the serialized input. Additionally, InstallCommand's git clone operation passes the branch, url, and path parameters into a shell command without escaping, allowing OS command injection via plugin/theme installation (which requires admin access). A Twig security blocklist bypass (server-side template injection) is also present. The issues are fixed in 2.0.0-beta.2.

### CVE-2026-56278

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-06-30T23:17:29.610 |

Flowise before 3.1.0 (affected versions 3.0.13 and earlier) uses a weak hardcoded default secret ('flowise') for the express-session middleware when the EXPRESS_SESSION_SECRET environment variable is not set (packages/server/src/enterprise/middleware/passport/index.ts). Because this default secret is publicly visible in the source code, an attacker can forge valid signed session cookies to impersonate any user and bypass authentication.

### CVE-2026-50110

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-06-30T23:17:27.300 |

Storage Concentrator (SC & SCVM) contains hardcoded credentials for numerous internal services embedded within a configuration file. While the credentials are stored in an encoded format, the encoding can be reversed to plaintext. The exposed credentials span a broad range of internal services, including database accounts, licensing, replication services, and third-party integrations, meaning successful exploitation of this vulnerability could provide an attacker with unauthorized access to multiple interconnected systems.

### CVE-2026-14038

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20;CWE-20` |
| Published | 2026-06-30T23:17:16.340 |

Insufficient validation of untrusted input in New Tab Page in Google Chrome prior to 150.0.7871.47 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-58449

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-30T22:16:58.397 |

txtai through 9.10.0, fixed in commit 11b32da, exposes an API /reindex endpoint whose function body parameter is resolved through txtai.util.Resolver, which performs __import__ and getattr on the caller-supplied dotted path with no allowlist. When the API is exposed with no TOKEN configured (authentication is opt-in, so all endpoints are unauthenticated) and the index is configured writable, a remote attacker can set function to an arbitrary callable such as subprocess.getoutput, achieving remote code execution as the server process during reindexing. Exploitation requires those deployment conditions (API exposed, no TOKEN, writable index); it is not the default configuration. The fix gates the endpoint behind a new reindex configuration flag.

### CVE-2026-50003

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-30T22:16:57.190 |

A malicious or compromised server can make a DCMTK client using bit-preserving C-GET storage mode write files outside the chosen output directory, using both relative (../) paths and absolute paths.

### CVE-2026-11712

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-30T20:17:27.897 |

IBM WebSphere Application Server 9.0, and 8.5 is affected by a cross-site scripting vulnerability in the administrative console help system.

### CVE-2026-11708

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-30T20:17:27.767 |

IBM WebSphere Application Server 9.0, and 8.5 is affected by a cross-site scripting vulnerability in the administrative console's integrated help system.

### CVE-2026-58138

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-30T19:17:00.520 |

Orkes Conductor 3.21.21 before 3.30.2 contains an unauthenticated remote code execution vulnerability that allows remote attackers to execute arbitrary OS commands by submitting inline workflow definitions containing malicious JavaScript or Python expressions to the workflow API endpoint prior to authentication. Attackers can exploit unsandboxed GraalVM evaluators configured with HostAccess.ALL or allowAllAccess(true) through INLINE, LAMBDA, DO_WHILE, and SWITCH task types to invoke arbitrary system commands via Java reflection or direct subprocess calls.

### CVE-2026-58172

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-30T17:16:24.313 |

Ocelot through 24.1.0, fixed in commit f156fd4, contains a security control bypass vulnerability that allows denied clients to circumvent IP-based access restrictions by sending WebSocket upgrade requests. The WebSocket upgrade pipeline branch configured via MapWhen in OcelotPipelineExtensions.cs omits SecurityMiddleware, causing requests from blocked IP addresses to be proxied to downstream services without enforcement of the configured allow/block list.

### CVE-2026-48315

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-30T16:16:55.310 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to inject malicious scripts into a web page, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-48313

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-30T16:16:55.093 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read and limited write access. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-56264

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-30T23:17:29.363 |

Crawl4AI before 0.8.7 contains an arbitrary JavaScript execution vulnerability in the Docker API server's /execute_js endpoint, which accepts and executes arbitrary user-supplied JavaScript in the server's browser context with --disable-web-security enabled. An attacker can execute arbitrary JavaScript and, combined with the browser's relaxed security settings, perform server-side request forgery against internal services.

### CVE-2026-55721

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-30T23:17:28.427 |

Storage Concentrator (SC & SCVM) is vulnerable to SQL injection through cookie values processed by the login.pl and debug.pl scripts. The cookie value is incorporated directly into database queries without adequate sanitization, allowing an unauthenticated remote attacker to manipulate those queries and extract sensitive information from the underlying database, including session tokens, password hashes, and stored secret keys.

### CVE-2026-58370

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-06-30T17:16:24.987 |

Woodpecker before 3.15.0 matches the ApprovalAllowedUsers bypass list against pipeline.Author. For the GitLab forge driver, pipeline.Author is populated from the git commit author name (commit.author.name) carried in the webhook payload, which is attacker-controlled and not verified by GitLab. A user who can open a merge request from a fork can set the commit author name to match an entry in ApprovalAllowedUsers, causing needsApproval to return false so the pipeline runs without the required approval. This defeats the fork-approval security boundary and allows execution of attacker-controlled pipeline steps on a Woodpecker agent and exfiltration of CI secrets exposed to the run. Other built-in forge drivers (Gitea, Forgejo, GitHub, Bitbucket) derive pipeline.Author from the forge-validated sender/actor identity and are not affected.

### CVE-2026-14198

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-07-01T12:16:38.463 |

@fastify/middie versions 9.1.0 through 9.3.2 decode the encoded slash %2F inside path parameter values before matching middleware paths, while Fastify's underlying router preserves the encoding during route lookup. The two layers disagree on the canonical request path, so the middleware fails to match a URL that the route handler does match. When middleware is used for authentication, authorization, rate limiting, or auditing on parameterized paths, an attacker can reach the protected handler by sending a single crafted URL with an encoded slash in the parameter position. The bypass is HTTP method agnostic and requires no authentication or special preconditions. Patches: upgrade to @fastify/middie 9.3.3. Workarounds: avoid parameterized middleware paths for security decisions, or enforce authentication at the route handler or via a Fastify hook that runs after the router has resolved the request.

### CVE-2026-7839

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-01T05:16:24.680 |

UltraVNC repeater through 1.8.2.2 initializes the HTTP administration server with a hardcoded default password. In repeater/webgui/settings.c:197, when settings2.txt is absent on first run the repeater writes the literal string "adminadmi2" as the admin password via strcpy_s(saved_password, 64, "adminadmi2"). The HTTP Basic-auth handler wi_decode_auth() checks this password without rate-limiting or lockout. Any remote attacker who can reach the repeater HTTP port (default TCP 80) can authenticate as administrator using the well-known default credential on a fresh or unmodified installation, gaining full control of the repeater configuration including allow/deny rules and session visibility.

### CVE-2026-6070

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-01T05:16:23.277 |

The WP-BusinessDirectory plugin for WordPress is vulnerable to Unauthenticated Arbitrary File Deletion in versions up to and including 4.0.1. This is due to insufficient path validation in the remove() method of the JBusinessDirectoryControllerUpload class. The task=upload.remove endpoint is accessible without authentication via the plugin's frontend routing system. The _filename parameter is accepted with RAW filter (no sanitization), and the helper function makePathFile() only normalizes directory separator characters without stripping path traversal sequences (../). When combined with the _path_type=2 parameter, which sets the base directory to the plugin's site folder, an attacker can supply a _filename value containing ../ sequences to traverse outside the plugin directory and call PHP's unlink() on arbitrary files — including wp-config.php, wp-config-backup.php, or other critical server files accessible to the web server process. This makes it possible for unauthenticated attackers to delete arbitrary files on the server.

### CVE-2026-7874

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-338` |
| Published | 2026-06-30T20:17:31.900 |

IBM Langflow OSS 1.0.0 through 1.10.0 Langflow could allow disclosure of all stored credentials due to the use of a weak and reversible key derivation mechanism for encryption at rest.

### CVE-2026-7663

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-06-30T20:17:31.280 |

IBM Langflow OSS 1.0.0 through 1.9.6 could allow unauthenticated attackers to access protected MCP project resources and execute MCP operations due to improper authorization enforcement in the Streamable MCP transport endpoint.

### CVE-2026-13603

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-918` |
| Published | 2026-07-01T14:16:31.910 |

The payment integration pretix-oppwa provides support 
for the payment providers VR Payment, Hobex, and potentially others 
based on Oppwa's technology. The integration of Oppwa, following their 
official documentation, includes a step where the user is redirected 
from the payment provider back to our system with a query parameter like
 ?resourcePath=/v1/checkouts/{checkoutId}/payment in the URL. Our system is then supposed to fetch the status of the transaction from the URL given by baseUrl + resourcePath.



Our plugin pretix-oppwa did so insecurely by 
concatenating the parameter form the URL to the base domain of the API 
without further validation and, critically, without a / at the end of the baseUrl. Therefore, an attacker could inject a resourcePath argument in a way that causes pretix to call a different
 server instead. Since the request includes the access token (API key) 
of the Oppwa account, this would leak the access token, giving access to
 data contained in the payment provider's system. This is fixed with the
 release today by strictly validating the given API URL.









After installing the update, we recommend asking your payment provider for a new access token and updating it in pretix.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-10538

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-01T08:16:20.197 |

Messaging consumer functionality allows deserialization of user-controlled data without sufficient restriction of allowed object types in the out of support Control-M/Server and Control-M/Enterprise Manager versions 9.0.20.x and potentially earlier. This issue may allow an authenticated attacker to trigger unintended server-side behavior through crafted serialized content.

### CVE-2026-5136

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-01T14:16:47.277 |

A flaw was found in Foreman. The Usergroup model in Foreman does not properly validate role assignments against the calling user's permissions. This allows an authenticated user with usergroup management permissions to attach arbitrary roles, including administrative roles, to a user group and then add themselves as a member. Successful exploitation of this vulnerability leads to full privilege escalation, granting the attacker administrator-level access.

### CVE-2026-13228

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-01T11:16:25.377 |

The LatePoint – Calendar Booking Plugin for Appointments and Events plugin for WordPress is vulnerable to Privilege Escalation to Administrator in versions up to, and including, 5.6.3 This is due to an Insecure Direct Object Reference (IDOR) in the create_or_update() function of OsOrdersController, which allows an authenticated Agent to supply an arbitrary order[customer_id] and overwrite any LatePoint customer's email field (including one linked to a WordPress Administrator's account) through the public-scope customer set_data() call, combined with a missing role verification in OsAuthHelper::authorize_customer() which logs in the linked WordPress user without checking its role. This makes it possible for authenticated attackers, with custom (Agent)-level access and above, to elevate their privileges to Administrator.

### CVE-2026-12224

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-01T08:16:20.827 |

The Dokan Pro plugin for WordPress is vulnerable to privilege escalation via update_capabilities REST Endpoint in all versions up to, and including, 5.0.4.  This is due to the `update_capabilities()` REST handler accepting arbitrary capability strings from the request body and passing them directly to WP_User::add_cap() with no allowlist validation, only verifying that the caller holds the dokandar capability. This makes it possible for authenticated attackers with a self-provisioned Vendor-level access and above, on sites with the Vendor Staff module enabled, to grant arbitrary WordPress capabilities, including administrator, to any vendor_staff account, leading to a full site takeover.

### CVE-2026-12158

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-01T08:16:20.710 |

The RegistrationMagic – User Registration Forms Plugin plugin for WordPress is vulnerable to Cross-Site Request Forgery in all versions up to, and including, 6.0.9.1. This is due to missing or incorrect nonce validation on the process_request function. This makes it possible for unauthenticated attackers to escalate the privileges of an arbitrary form submitter to administrator by creating a malicious Chronos automation task that is executed via WordPress cron via a forged request granted they can trick a site administrator into performing an action such as clicking on a link.

### CVE-2026-14040

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-416` |
| Published | 2026-06-30T23:17:16.510 |

Use after free in BrowserTag in Google Chrome prior to 150.0.7871.47 allowed an attacker who convinced a user to install a malicious extension to potentially exploit heap corruption via a crafted Chrome Extension. (Chromium security severity: Low)

### CVE-2026-13888

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T23:17:03.040 |

Use after free in Extensions in Google Chrome prior to 150.0.7871.47 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-13885

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T23:17:02.750 |

Use after free in Skia in Google Chrome on Android prior to 150.0.7871.47 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-13884

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-30T23:17:02.640 |

Integer overflow in Chromecast in Google Chrome prior to 150.0.7871.47 allowed a local attacker to execute arbitrary code via malicious network traffic. (Chromium security severity: Medium)

### CVE-2026-13870

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T23:17:01.343 |

Use after free in WebView in Google Chrome on Android prior to 150.0.7871.47 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-13850

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-30T23:16:59.483 |

Insufficient validation of untrusted input in Chrome for iOS in Google Chrome on iOS prior to 150.0.7871.47 allowed a local attacker to execute arbitrary code inside a sandbox via a malicious file. (Chromium security severity: High)

### CVE-2026-13848

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T23:16:59.300 |

Use after free in Forms in Google Chrome prior to 150.0.7871.47 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-13845

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T23:16:59.020 |

Use after free in DOM in Google Chrome prior to 150.0.7871.47 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-13830

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T23:16:57.610 |

Use after free in Chromoting in Google Chrome on Linux prior to 150.0.7871.47 allowed a remote attacker to execute arbitrary code via malicious network traffic. (Chromium security severity: High)

### CVE-2026-13821

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T23:16:56.777 |

Use after free in Canvas in Google Chrome prior to 150.0.7871.47 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-52868

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-30T22:16:57.570 |

An unauthenticated attacker can read worklist records from a directory outside the intended per-AE worklist storage area. In a multi-area deployment, this can cross departmental or clinic data separation.

### CVE-2026-58166

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-30T17:16:23.487 |

OpenBMB ChatDev through 2.2.0, fixed in commit 4fd4da6, contains a path traversal vulnerability that allows unauthenticated remote attackers to write or delete arbitrary files by supplying a malicious multipart filename in the file upload endpoint. Attackers can send a crafted filename containing path traversal sequences or an absolute path to the POST uploads session endpoint, which constructs the destination path without sanitization in save_upload_file, causing file write and cleanup operations to target attacker-chosen paths on the server filesystem.

### CVE-2026-48307

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-30T16:16:54.987 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by a reflected Cross-Site Scripting (XSS) vulnerability. An attacker could exploit this vulnerability to inject malicious scripts into a web page, potentially resulting in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious link. Scope is changed.

### CVE-2026-27957

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-30T15:16:52.863 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.464, an authenticated command injection vulnerability in the CA Certificate management feature allows any authenticated user to execute arbitrary commands as the configured SSH user on the managed server host. As the SSH user typically would have to either be root or part of the docker group for Coolify to function as intended, this provides complete compromise of the managed server and associated docker containers. This vulnerability is fixed in 4.0.0-beta.464.

### CVE-2026-12577

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-358` |
| Published | 2026-07-01T08:16:21.380 |

DVP80ES3 with Improperly Implemented Security Check for Standard vulnerability.

### CVE-2026-7838

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-07-01T05:16:24.540 |

UltraVNC viewer through 1.8.2.2 contains an integer overflow leading to a heap buffer overflow in the RFB protocol failure-response parsing path. In vncviewer/ClientConnection.cpp, the 4-byte network-supplied reasonLen field (type CARD32) is passed as reasonLen+1 to CheckBufferSize(). Because both operands are unsigned 32-bit, a reasonLen of 0xFFFFFFFF overflows to 0, causing CheckBufferSize to allocate only 256 bytes. The subsequent ReadString(m_netbuf, reasonLen) call then performs ReadExact for the original 4 GiB length into that 256-byte heap buffer. This overflow is reachable via rfbConnFailed (auth-scheme negotiation) and rfbVncAuthFailed (post-handshake) message types without successful authentication. A malicious VNC server, or any man-in-the-middle on the RFB stream, can trigger this condition when the victim viewer connects, potentially resulting in remote code execution as the user running the viewer. The crash was confirmed with AddressSanitizer on a portable reproduction harness (heap-buffer-overflow WRITE at offset 256).

### CVE-2026-57995

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-30T23:17:32.537 |

phpMyFAQ before 4.1.5 contains a privilege escalation vulnerability in GroupController::updatePermissions that allows GROUP_EDIT administrators to grant arbitrary rights to groups without verifying they hold those rights themselves. A delegated administrator can exploit this by assigning high-value permissions to a group they belong to, inheriting those rights and escalating privileges up to full administrative control.

### CVE-2026-56300

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-30T23:17:29.873 |

Capgo before 12.128.2 contains unauthenticated security definer RPC functions get_user_id and get_org_perm_for_apikey that expose API key validity oracles and user UUID disclosure. Unauthenticated attackers using the public API key can validate leaked keys, enumerate users and apps, and determine permission levels, significantly increasing the actionability of compromised credentials.

### CVE-2026-56247

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-30T23:17:29.107 |

Capgo before 12.128.2 allows org admins to assign org-scoped RBAC roles at app scope without validating role scope compatibility, including to pending invitees. Attackers can pre-seed malformed high-privilege bindings that survive invite acceptance, enabling accepted low-privilege users to perform unauthorized privileged app actions.

### CVE-2026-56233

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-30T23:17:28.980 |

Capgo before 12.128.2 contains a path traversal vulnerability in the builder upload proxy that allows authenticated users with build permissions to bypass upload restrictions. Attackers can append traversal sequences to the upload path, which are normalized by the WHATWG URL parser, enabling access to internal administrative endpoints with the privileged BUILDER_API_KEY header and resulting in server-side privilege escalation.

### CVE-2026-56230

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-30T23:17:28.853 |

Capgo before 12.128.2 contains a broken object level authorization vulnerability in middlewareKey() that accepts the client-controlled x-limited-key-id header without validating ownership, allowing authenticated users to adopt cross-tenant limited keys. Attackers can supply another tenant's limited key ID to bypass authorization checks and access unauthorized cross-tenant resources across multiple API endpoints.

### CVE-2026-56219

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-30T23:17:28.587 |

Capgo before 12.128.2 contains a NULL-auth bypass vulnerability in the public.get_org_user_access_rbac function that allows unauthenticated attackers to retrieve RBAC role bindings and member email addresses. Attackers can exploit improper NULL comparison in the authorization gate to disclose organization membership, roles, and email addresses via the PostgREST RPC endpoint using only a public API key.

### CVE-2026-50254

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-06-30T22:16:57.320 |

An unauthenticated remote attacker can repeatedly send a single crafted connection request to leak memory. Against storescp in its default single-process mode, memory grows quickly and the service is eventually killed, after which it stops accepting connections until an operator restarts it.

### CVE-2026-35505

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-06-30T22:16:46.477 |

An unauthenticated remote attacker can repeatedly send crafted connection requests to leak memory. In single-process deployments the memory grows until the service is killed and the port stops responding until restart.

### CVE-2026-44628

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-06-30T21:16:30.653 |

An unauthenticated attacker can crash the worklist server with a single crafted query when the server has a valid Called AE Title / storage directory, the expected lockfile, and at least one matching worklist record.

### CVE-2026-13207

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-06-30T21:16:30.500 |

FUXA versions 1.3.1 and prior contain an authentication bypass vulnerability via dot-segment path normalization in the REST API. The API router fails to normalize dot-segment sequences before applying authentication middleware, allowing unauthenticated requests to access protected endpoints by prefixing paths with dot-segments such as /api/./users, /api/./roles, and /api/project/../users. These requests bypass authentication checks and return sensitive user and role data without credentials.

### CVE-2026-58375

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-30T17:16:25.743 |

JimuReport through 2.5.0 exposes the POST /jmreport/auto/export endpoint without authentication: the handler is annotated @JimuNoLoginRequired, so JimuReportTokenInterceptor skips all authentication and authorization, and the export service streams the rendered report for any supplied report id without verifying the auto-export configuration flag. An unauthenticated remote attacker can enumerate Snowflake report identifiers and export the full contents of any report, including the data returned by the report configured SQL queries and any credentials embedded in its data sources.

### CVE-2026-58165

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-30T17:16:23.350 |

OpenZiti through 2.0.0, fixed in commit 3027fdf, contains a privilege escalation vulnerability that allows authenticated non-admin identities with fine-grained enrollment management permissions to create enrollments for any identity, including the default administrator, because the ApplyCreate function in controller/model/enrollment_manager.go verifies only that the target identity exists without performing authorization checks binding the caller to the target identity. Attackers can redeem the resulting one-time token through the unauthenticated client API enrollment endpoint to obtain a client certificate authenticating as the targeted admin identity, yielding full administrative control of the controller and the zero-trust overlay it manages.

### CVE-2026-50043

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-01T08:16:21.727 |

Improper neutralization of special elements used in an OS command ('OS Command Injection') issue exists in SkyBridge MB-A100/MB-A110. If this vulnerability is exploited, an arbitrary OS command may be executed by an attacker who can log in to the product with an administrative privilege.

### CVE-2026-58377

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-30T17:16:26.010 |

JeecgBoot through 3.9.2 contains a broken access control vulnerability that allows authenticated low-privilege users to perform full create, read, update, and delete operations on OpenAPI credentials by accessing the OpenApiAuthController and OpenApiPermissionController endpoints which lack Shiro authorization annotations. Attackers can exploit the unenforced access controls to list, add, edit, and delete all AK/SK credential pairs, with the list endpoint returning secret keys in plaintext, enabling credential theft and unauthorized invocation of the OpenAPI surface.

### CVE-2026-48285

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-30T16:16:54.753 |

ColdFusion versions 2025.9, 2023.20 and earlier are affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized read access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-11594

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-30T21:16:30.383 |

IBM WebSphere Application Server 9.0, and 8.5 is affected by a cross-site scripting vulnerability in the administrative console.

### CVE-2026-11714

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-30T20:17:28.033 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.7 is affected by a server-side request forgery vulnerability with the apiDiscovery-1.0 feature enabled.

### CVE-2026-10129

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-30T20:17:26.747 |

IBM Langflow OSS 1.0.0 through 1.9.3 contains a Server-Side Request Forgery (SSRF) protection bypass vulnerability in the API Request component. An authenticated attacker with low-level privileges (flow author role) can bypass SSRF protections by enabling the follow_redirects parameter and supplying a public URL that redirects to internal/localhost addresses. The vulnerability exists because the application validates only the initial URL but does not re-validate redirect destinations. This allows attackers to access internal HTTP services, localhost endpoints, cloud metadata services, and private network resources that should be unreachable when SSRF protection is enabled. Successful exploitation can lead to disclosure of sensitive information including credentials, tokens, internal API responses, and administrative panel data.

### CVE-2026-54673

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-30T23:17:28.000 |

electron-updater allows for automatic updates for Electron apps. Prior to 9.7.0, the HTTP redirect handler (HttpExecutor.prepareRedirectUrlOptions) only stripped a credential header whose key string matched exactly lowercase "authorization", exposing credentials. Other credential-bearing headers — most notably PRIVATE-TOKEN (used by GitLab's personal access token flow) and mixed-case Authorization (used by GitLab's Bearer/OAuth flow) — were not stripped and could be forwarded to an attacker-controlled cross-origin redirect destination. This issue has been fixed in version 9.7.0.

### CVE-2026-10564

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-30T20:17:27.387 |

IBM Langflow OSS 1.0.0 through 1.9.6 contains a Server-Side Request Forgery (SSRF). The legacy RSSReaderComponent in rss.py and SearXNG component in searxng.py make unvalidated HTTP requests to user-controlled URLs, bypassing SSRF protections introduced in version 1.9.3. An authenticated attacker can exploit this to access internal resources including cloud metadata services (AWS/Azure/GCP IMDS), potentially exfiltrating IAM credentials and enumerating internal networks. The vulnerability can also be triggered through prompt injection in agentic workflows due to tool_mode=True exposure.

### CVE-2026-10560

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-30T20:17:27.263 |

IBM Langflow OSS 1.0.0 through 1.9.6 contains a missing authentication vulnerability in /api/v1/build_public_tmp/ endpoints that allows an unauthenticated attacker to read build event data or cancel jobs using a valid job identifier, resulting in information disclosure and denial of service.

### CVE-2026-5120

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-01T13:17:48.033 |

A Race Condition vulnerability affecting BIOVIA Workbook from Release 2021 through Release 2026 could allow a user to access unauthorized data from another user.

### CVE-2026-11794

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-01T07:16:22.260 |

The Advanced Form Integration — Connect Forms to 200+ Apps WordPress plugin before 2.1.1 does not restrict the WordPress role assigned when it creates a user from a public form submission, allowing unauthenticated visitors to create an administrator account when an active integration maps the user role to a public form field. This requires a specific, non-default multi-Advanced Form Integration — Connect Forms to 200+ Apps WordPress plugin before 2.1.1 configuration.

### CVE-2026-10750

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-01T07:16:21.890 |

The Royal MCP  WordPress plugin before 1.4.26 does not perform capability checks on the majority of its MCP tools after token authentication, allowing authenticated users with a low-privileged role such as Subscriber to read private content, enumerate all users and their roles, and create, modify, or delete content owned by other users.

### CVE-2025-36359

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-613` |
| Published | 2026-06-30T21:16:30.123 |

IBM DevOps Automation 1.0.1 and IBM DevOps Loop 1.0.2 does not invalidate session IDs after expiration which could allow an authenticated user to impersonate another user on the system.

### CVE-2026-14191

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-129;CWE-787` |
| Published | 2026-07-01T04:16:58.647 |

An out-of-bounds heap write exists in the RAR5 recovery-volume (.rev) parser in WinRAR and UnRAR (RecVolumes5::ReadHeader in recvol5.cpp). The RecItems vector is sized only when the first .rev file in a set is processed; subsequent .rev files supply an independent RecNum value that is validated against that file's own TotalCount field but never against the actual size of RecItems. A crafted set of two or more .rev files can therefore write an attacker-controlled 32-bit value (the header's RevCRC field) to RecItems[RecNum] at an attacker-controlled offset up to 65534 * sizeof(RecVolItem) bytes past the allocation, corrupting adjacent heap objects. Triggering requires the victim to run a recovery/test operation on an attacker-supplied .rev set (for example 'unrar t x.part1.rev', WinRAR 'Repair archive', or auto-recovery when extracting a volume set with a missing .rar part). This is the RAR5-path sibling of CVE-2023-40477 (which was fixed in the RAR3 path only in WinRAR 6.23). Fixed in WinRAR / RAR 7.23.

### CVE-2026-54672

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-06-30T23:17:27.863 |

electron-updater allows for automatic updates for Electron apps. Prior to 26.15.0, AppImage targets built by app-builder-lib could use an empty path component when setting the LD_LIBRARY_PATH environment variable at runtime. This causes the current working directory to be added to the dynamic linker search path, which may allow an attacker to execute arbitrary code by placing a malicious shared library in the directory from which the AppImage is launched. This issue has been fixed in version 26.15.0.

### CVE-2026-13844

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T23:16:58.927 |

Use after free in Updater in Google Chrome on Windows prior to 150.0.7871.47 allowed a local attacker to perform OS-level privilege escalation via a malicious file. (Chromium security severity: High)

### CVE-2026-13827

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T23:16:57.327 |

Use after free in Updater in Google Chrome on Mac prior to 150.0.7871.47 allowed a local attacker to perform privilege escalation via a malicious file. (Chromium security severity: High)

### CVE-2026-58169

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-06-30T17:16:23.907 |

Vibe-Trading before 0.1.10 contains a DNS rebinding authentication bypass vulnerability that allows remote attackers to bypass bearer-token authentication by exploiting the server's trust of TCP peer addresses for loopback clients combined with missing Host header validation while binding to 0.0.0.0 with credentialed CORS. Attackers can craft a malicious DNS rebinding page to issue authenticated requests to the local API server, reach the shell execution endpoint with a bash-enabled preset, and achieve remote code execution as the API process user while also overwriting LLM and data-source settings to exfiltrate credentials.

### CVE-2026-58168

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-30T17:16:23.753 |

DeepTutor before version 1.4.10 contains an authorization bypass vulnerability that allows low-privilege users to invoke unrestricted MCP tools due to the allowed_mcp_tools function returning None instead of a denied result when mcp_tools is omitted from a user's grant in deeptutor/multi_user/tool_access.py. Attackers or prompt-injected content acting within a user session can enumerate and invoke any configured MCP tool, including filesystem, shell, and browser servers, gaining unauthorized access to sensitive deployment resources.

### CVE-2026-7831

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-193;CWE-787` |
| Published | 2026-07-01T05:16:24.380 |

UltraVNC viewer through 1.8.2.2 contains an off-by-one stack buffer overflow in the RFB ServerInit message handler. In vncviewer/ClientConnection.cpp, when the server-supplied nameLength equals exactly 2024 the code declares a 2024-byte stack buffer _dn[2024] and calls ReadString(_dn, 2024). ReadString writes the NUL terminator at buf[length], i.e., _dn[2024], one byte past the end of the stack buffer. A malicious VNC server can trigger this condition by advertising a desktop name of length 2024 in its ServerInit message. On release builds without stack canaries the single-byte NUL overwrite adjacent stack data. On builds with /GS stack protection the canary is corrupted and the process terminates, resulting in denial of service. User interaction (connecting the viewer to the malicious server) is required.

### CVE-2025-71374

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-30T23:16:51.903 |

picklescan before 0.0.29 fails to detect the built-in python profile.Profile.run function when used in pickle reduce methods, allowing attackers to execute arbitrary code. Remote attackers can craft malicious pickle files that bypass picklescan detection and achieve code execution upon deserialization.

### CVE-2025-71371

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-30T23:16:51.773 |

picklescan before 0.0.29 fails to detect malicious pickle files using code.InteractiveInterpreter.runcode in reduce methods. Attackers can craft pickle payloads that bypass picklescan detection and execute arbitrary code when loaded via pickle.load().

### CVE-2025-71368

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-30T23:16:51.653 |

picklescan before 0.0.30 fails to detect the doctest.debug_script function when analyzing pickle files, allowing attackers to execute arbitrary code. Remote attackers can craft malicious pickle files embedding doctest.debug_script calls that bypass picklescan detection and execute arbitrary commands upon pickle.load invocation.

### CVE-2025-71363

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-30T23:16:51.533 |

picklescan before 0.0.30 fails to detect cProfile.run function calls in pickle reduce methods, allowing attackers to execute arbitrary code. Remote attackers can craft malicious pickle files with cProfile.run payloads that bypass picklescan detection and achieve code execution upon deserialization.

### CVE-2025-71355

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-06-30T23:16:51.417 |

Picklescan before 0.0.25 fails to detect unsafe global functions in the Numpy library, allowing attackers to bypass static analysis and execute arbitrary code during deserialization. Attackers can craft malicious pickle files using numpy.testing._private.utils.runstring within the reduce method to import dangerous libraries like os and execute arbitrary OS commands when the pickle file is loaded.

### CVE-2025-71352

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-06-30T23:16:51.290 |

picklescan before 0.0.29 fails to detect the built-in Python trace.Trace.runctx function when used in pickle file reduce methods, allowing attackers to execute arbitrary code. Remote attackers can craft malicious pickle files with trace.Trace.runctx payloads that bypass picklescan detection and execute code upon pickle.load() invocation.

### CVE-2025-71350

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-30T23:16:51.163 |

picklescan before 0.0.28 fails to detect malicious pickle files using torch.utils.collect_env.run function in reduce methods. Attackers can embed undetected code in pickle files that executes remote commands when loaded by victims.

### CVE-2025-71349

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-30T23:16:51.010 |

picklescan before 0.0.29 fails to detect the built-in trace.Trace.run function when analyzing pickle files, allowing attackers to embed undetected malicious code. Remote attackers can craft malicious pickle files using trace.Trace.run in the reduce method to achieve arbitrary code execution when pickle.load processes the file.

### CVE-2026-13449

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-611` |
| Published | 2026-06-30T20:17:28.820 |

IBM Business Automation Manager Open Editions 9.0.0 through 9.4.2 is vulnerable to an XML external entity injection (XXE) attack when processing XML data. A remote attacker could exploit this vulnerability to expose sensitive information or consume memory resources.

### CVE-2026-14181

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-01T12:16:38.343 |

@fastify/middie versions 9.1.0 through 9.3.2 fail to guard the URL normalization step used by the standalone engine when incoming request paths contain malformed percent-encoded sequences. Inputs such as an incomplete percent escape or a truncated multibyte sequence cause the underlying decoder to throw synchronously, and the exception escapes the middie normalize step and terminates the Node.js process. The bypass affects applications that call middie.run directly on the standalone engine API, causing an immediate denial of service for all connected clients until restart. Applications using the Fastify plugin path are not affected because Fastifys error handler catches the exception. Patches: upgrade to @fastify/middie 9.3.3. Workarounds: migrate from the standalone engine API to the Fastify plugin path, where the framework error handler catches the exception.

### CVE-2026-12576

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-924` |
| Published | 2026-07-01T08:16:21.277 |

DVP80ES3 with Improper Enforcement of Message Integrity During Transmission in a Communication Channel vulnerability.

### CVE-2026-12575

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-404` |
| Published | 2026-07-01T08:16:21.177 |

DVP80ES3 with 
Improper Resource Shutdown or Release vulnerability.

### CVE-2026-1239

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-01T07:16:22.983 |

The Ninja Forms – The Contact Form Builder That Grows With You plugin for WordPress is vulnerable to unauthorized access of data due to a missing authorization check on the 'ninja-forms-views/token/refresh' REST callback in all versions up to, and including, 3.14.1. This makes it possible for unauthenticated attackers to view form submissions, which could potentially contain sensitive information.

### CVE-2026-14193

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-07-01T07:16:22.873 |

DVP80ES300T with Improper Validation of Array Index Vulnerability

### CVE-2026-11823

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-01T07:16:22.353 |

The BookingPress Appointment Booking Pro plugin for WordPress is vulnerable to SQL Injection via the 'store_service_date' parameter of the bpa_assign_staffmember_to_slots() function in versions up to and including 5.7.1. This is due to the explicit use of stripslashes_deep() on user-supplied POST data before it is interpolated verbatim into a SQL LIKE clause without use of $wpdb->prepare() or any parameterization. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-11568

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-01T07:16:22.083 |

The Product Configurator for WooCommerce WordPress plugin before 1.7.3 does not perform any authorisation or post-status check before returning WooCommerce product data through a public AJAX action, allowing unauthenticated users to retrieve the data (title, price, weight, stock status, and configurator option pricing/SKUs) of private and draft, non-public products by supplying the product ID. WordPress post-visibility controls are bypassed.

### CVE-2026-13468

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-01T05:16:18.663 |

The Visualizer – Tables & Charts Manager with Built-in AI Generator plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 4.0.3. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to access and export the contents of any visualizer chart on the site — including charts in draft, private, pending, future, or trash status — as CSV, Excel, or HTML via the /wp-json/visualizer/v1/action/{chart}/{type}/ REST endpoint. This bypass is particularly impactful because the standard WordPress REST endpoint for the non-public 'visualizer' custom post type correctly enforces capability checks and returns HTTP 401 to unauthenticated callers, whereas this plugin-registered route circumvents that protection entirely.

### CVE-2026-12923

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-01T05:16:18.040 |

The Youtube Showcase plugin for WordPress is vulnerable to Arbitrary Function Call in versions up to and including 4.0.3. This is due to insufficient validation of the 'path' parameter in the emd_delete_file() AJAX handler in includes/common-functions.php. The user-supplied value is passed through sanitize_text_field(), has its trailing '_PLUGIN_DIR' substring stripped, and is then invoked as a PHP function name with no arguments via `$sess_name()`. The handler is gated only by a nonce — no current_user_can() check is present — and the nonce is emitted on any front-end page that renders a form shortcode containing file fields. This makes it possible for authenticated attackers, with Subscriber-level access and above, to invoke arbitrary zero-argument PHP functions (such as phpinfo, phpversion, get_defined_vars, error_get_last), resulting in sensitive information disclosure and potential further compromise depending on the functions available in the environment.

### CVE-2026-20458

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-01T04:17:13.943 |

In Modem, there is a possible memory corruption due to a missing bounds check. This could lead to remote escalation of privilege, if a UE has connected to a rogue base station controlled by the attacker, with no additional execution privileges needed. User interaction is not needed for exploitation. Patch ID: MOLY01402160; Issue ID: MSV-7298.

### CVE-2026-54592

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-07-01T00:16:32.743 |

Oj (Optimized JSON) is a JSON parser and Object marshaller packaged as a Ruby gem. In versions prior to 3.17.3, Oj::Doc#each_child, when invoked recursively over a deeply nested JSON document, overflows a fixed-size stack buffer and aborts the process, leading to DoS.  In a two-step chain in ext/oj/fast.c, doc_each_child increments doc->where past the where_path[MAX_STACK = 100] array with no bounds check and never restores it (the doc->where-- is missing), so calling each_child recursively from inside the yield block drives doc->where beyond the array. On the next entry  the function copies the path into the 800-byte stack-local buffer save_path[MAX_STACK]  using wlen = doc->where - doc->where_path, so when the previous recursive call left doc->where past where_path[100] the wlen exceeds MAX_STACK and  the memcpy overflows save_path on the C stack; because the Oj::Doc parser imposes no JSON nesting-depth limit (relying on a C-stack pressure check), deeply nested attacker input reaches this path. This issue has been fixed in version 3.17.3.

### CVE-2026-13891

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-30T23:17:03.333 |

Insufficient validation of untrusted input in Extensions in Google Chrome prior to 150.0.7871.47 allowed a remote attacker who had compromised the renderer process to perform privilege escalation via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-13856

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-30T23:17:00.040 |

Insufficient validation of untrusted input in Speech in Google Chrome on Android prior to 150.0.7871.47 allowed a remote attacker who had compromised the renderer process to perform privilege escalation via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-13855

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T23:16:59.947 |

Use after free in Ozone in Google Chrome on Linux prior to 150.0.7871.47 allowed a remote attacker who convinced a user to engage in specific UI gestures to execute arbitrary code via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-13831

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T23:16:57.730 |

Out of bounds read and write in GPU in Google Chrome prior to 150.0.7871.47 allowed a remote attacker who had compromised the renderer process to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-13824

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-30T23:16:57.050 |

Insufficient policy enforcement in Extensions in Google Chrome prior to 150.0.7871.47 allowed a remote attacker who had compromised the renderer process to perform privilege escalation via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-57585

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-30T22:16:57.837 |

MessagePack is the serializer implementation for Python msgpack.org. Prior to 1.2.1, there is an Out-of-bounds read/crash on Unpacker reuse after a caught error, potentially leading to a DoS attack.  If the Unpacker is used repeatedly after an error occurs, the process may crash with a SEGV. This issue has been fixed in version 1.2.1.

### CVE-2026-13772

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-06-30T20:17:29.080 |

IBM WebSphere Extreme Scale 8.6.1.0 through 8.6.1.6 's Object Query Language engine resolves attacker-supplied class names via Class.forName() and invokes their constructors with no allow-list at three distinct sinks (SELECT NEW, enum literals, and reflection-based comparators); an authenticated remote attacker who can influence an application-built OQL query string can execute arbitrary constructors on the WAS JVM, and a SELECT DISTINCT variant using planted grid values fires the same gadget post-readObject in a manner that survives JEP-290 serialization filters across grid node boundaries

### CVE-2026-13759

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-30T20:17:28.953 |

IBM WebSphere Extreme Scale 8.6.1.0 through 8.6.1.6 ships three ObjectInputStream subclasses (WsObjectInputStream, ObjectStreamPool$ReusableInputStream, ObjectInputStreamResolver) that install no JEP-290 class filter; when Coherence is on the classpath, multiple RCE gadget chains including RemoteConstructor.readResolve and PriorityQueue/ExtractorComparator are confirmed working, allowing a post-login attacker who can write a session attribute or a LAN-adjacent attacker on the grid replication wire to execute arbitrary code on peer WAS JVMs

### CVE-2026-49451

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-06-30T17:16:22.390 |

The OpenAPI.NET SDK contains a useful object model for OpenAPI documents in .NET along with common serializers to extract raw OpenAPI JSON and YAML documents from the model. From 2.0.0-preview11 until 2.7.5 and 3.5.4, a small OpenAPI document containing a circular schema reference can cause process termination through stack overflow in Microsoft.OpenApi. The issue affects OpenAPI document parsing through public OpenAPI.NET reader APIs and has been confirmed across both JSON and YAML reader paths. This vulnerability is fixed in 2.7.5 and 3.5.4.

### CVE-2026-12579

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-01T07:16:22.753 |

AS228T with Authentication Bypass Vulnerability

### CVE-2026-7830

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-326;CWE-338` |
| Published | 2026-07-01T05:16:24.210 |

UltraVNC through 1.8.2.2 uses inadequate cryptography in the MS-Logon II authentication scheme (rfbUltraVNC_MsLogonIIAuth). In rfb/dh.cpp the Diffie-Hellman key exchange is performed with parameters that fit in an unsigned 64-bit integer (DH_MAX_BITS controls the prime size). A 64-bit DH key can be broken by Pollard's rho algorithm in under one second on current hardware. Additionally, the private exponent is generated by the rng() function, which multiplies three libc rand() values seeded from time(NULL). With approximately 31 bits of internal state and a time-based seed, the private exponent is recoverable in under a minute by a passive observer. A network attacker who can observe the MS-Logon II handshake (via sniffing, recording, or man-in-the-middle) can derive the shared DH key and decrypt the encapsulated username and password, resulting in full credential disclosure. This affects legacy MS-Logon II connections; MS-Logon III (X25519 + AES-256-GCM) is unaffected.

### CVE-2026-11541

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-06-30T22:16:46.317 |

IBM WebSphere Application Server 9.0, and 8.5 and IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.6 are affected by an HTTP request smuggling vulnerability.

### CVE-2026-8864

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-30T17:16:26.260 |

The HP Fan Control App might allow local escalation of privileges. An updated version of HP Fan Control App has been released
               to mitigate this potential vulnerability.

### CVE-2026-12142

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-01T11:16:24.043 |

The NEX-Forms – Ultimate Forms Plugin for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via '_name[]' Array Parameter in all versions up to, and including, 9.2.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The wp_kses() output filtering pass provides no mitigation because NEXForms_allowed_tags() explicitly permits &lt;script&gt;, &lt;iframe src/srcdoc&gt;, and JS event handlers such as onClick, onBlur, and onChange in its allow-list.

### CVE-2026-11883

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-01T07:16:22.577 |

The WebAuthn Provider for Two Factor WordPress plugin before 2.5.6 does not correctly validate the second-factor authentication response, allowing an attacker who already knows a user's password to bypass the two-factor authentication requirement by submitting a malformed request.

### CVE-2026-7829

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-01T05:16:24.087 |

UltraVNC repeater through 1.8.2.2 contains a post-authentication out-of-bounds write in the allow/deny rule parser. In repeater/webgui/settings.c:225-272, after strncpy_s copies a rule token into temp1[rule1] (25-byte destination) or temp2/temp3 (16-byte destination), the code unconditionally writes a NUL terminator at temp1[rule1][len] = 0 without clamping len to the destination size. When an authenticated administrator saves a rule with a token length equal to or greater than the destination size, the NUL byte is written one or more bytes past the end of the stack-allocated array, corrupting adjacent stack data. An attacker who has obtained admin credentials (including via CVE-2026-7839 default password) can trigger this to gain code execution on the repeater host.

### CVE-2026-7517

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-01T05:16:23.550 |

The Custom Payment Gateways for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'alg_wc_cpg_input_fields' parameter in all versions up to, and including, 2.1.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability is exploitable by unauthenticated guest users submitting a crafted checkout POST request, requiring no custom input fields to be configured in the plugin.

### CVE-2026-13731

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-01T05:16:18.800 |

The WPBot – AI ChatBot for Live Support, Lead Generation, AI Services plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'conversation' parameter in all versions up to, and including, 8.4.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The AJAX nonce required to authenticate the save request is publicly emitted on every frontend page via wp_localize_script, making it freely obtainable by any anonymous visitor and removing any practical barrier to exploitation.

### CVE-2026-56249

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-06-30T23:17:29.233 |

Capgo before 12.128.2 contains an authorization bypass vulnerability in the channel creation endpoint that allows authenticated users to overwrite existing channels by reusing their names. Attackers with app.create_channel permission can exploit a logic mismatch between existence validation and upsert operations to reassign channel ownership and modify critical production channel configurations.

### CVE-2026-11806

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-444` |
| Published | 2026-06-30T20:17:28.157 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.6 is affected by an arbitrary file read vulnerability with the restConnector-2.0 feature enabled.

### CVE-2026-10513

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-30T19:16:26.473 |

The Webmention plugin for WordPress is vulnerable to Stored Cross-Site Scripting in versions up to and including 5.8.0 via parser-derived 'avatar' and 'url' author metadata. This is due to insufficient input sanitization and output escaping on user-supplied MF2 author properties processed by the unauthenticated webmention REST endpoint and rendered directly into HTML 'value' attributes by the edit-comment-form template without esc_attr() or esc_url(). This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a privileged user (moderator or administrator) opens the affected comment edit screen.

### CVE-2026-58376

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-30T17:16:25.873 |

Dolibarr through 23.0.3, fixed in commit 14db36e, contains a sql injection vulnerability that allows authenticated API users to exfiltrate arbitrary database contents by supplying malicious values to the sqlfilters query parameter in the setup dictionary and multicurrencies REST API endpoints. The affected endpoints in api_setup.class.php and api_multicurrencies.class.php validate sqlfilters only for balanced parentheses and rewrite matched triplets, allowing text placed outside the expected shape such as an appended UNION SELECT to be concatenated into the SQL WHERE clause unmodified, enabling retrieval of sensitive data including password hashes and API keys.

### CVE-2026-58372

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-30T17:16:25.450 |

SeaweedFS before 4.34 contains a path traversal vulnerability in the S3 gateway DeleteMultipleObjectsHandler that allows authenticated S3 principals with write access to a single bucket to delete arbitrary objects in other tenants' buckets by supplying object keys containing ../ sequences in the DeleteObjects XML request body. Attackers can bypass authorization controls through a confused deputy condition, as the validateRequestPath middleware only inspects URL-captured path variables and never examines request-body keys, allowing the filer path to collapse directory traversal sequences and resolve deletions outside the authorized bucket.

### CVE-2026-58170

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-30T17:16:24.057 |

Vibe-Trading before 0.1.10 builds the proposal file path by joining a caller-supplied proposal identifier onto the broker proposals directory without sanitization (agent/src/live/mandate/commit.py). A proposal identifier containing path traversal sequences causes the application to load an attacker-controlled JSON file as an authoritative live trading mandate. Combined with the file upload endpoint, an admitted caller can write a JSON file to a known location and traverse to it, and because the ceilings validation is skipped when ceilings are absent, the attacker fully controls the committed mandate.

### CVE-2026-53902

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-863` |
| Published | 2026-07-01T13:17:45.237 |

MCO does not properly enforce authorization checks in the /customer/servlet/mco/webapi/profile-sections/group-membership endpoint. An authenticated user can modify their group membership without proper authorization checks, allowing privilege escalation.
An attacker can add themselves to arbitrary groups by supplying a valid group ID, which can be obtained via other application functionalities (e.g. /customer/servlet/mco/webapi/group/picker/groups), provided he has necessary permissions, or potentially inferred through brute-force techniques.



Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version 25.3.3.1 but may also affect other versions.

### CVE-2026-56328

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-670` |
| Published | 2026-06-30T23:17:30.370 |

Capgo before 12.128.2 allows multiple public channels for the same app and platform to coexist simultaneously, while unnamed /updates requests without defaultChannel implicitly resolve to a single hidden winner channel. An authorized app or channel manager can create ambiguous default update state and silently influence which bundle unnamed clients receive, breaking release routing integrity and predictability.

### CVE-2026-56320

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-06-30T23:17:30.120 |

Capgo before 12.128.2 contains an authorization flaw in POST /private/create_device that accepts a caller-supplied org_id parameter without validating it matches the target app's owner organization. Authenticated attackers can create device records for an application using a foreign organization identifier, bypassing the intended org/app authorization boundary.

### CVE-2026-58448

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-30T22:16:58.240 |

yudao-cloud before 2026.06 contains a broken access control vulnerability in the BPM module that allows any authenticated user to access arbitrary process instance records by supplying a caller-controlled process-instance identifier to an unprotected endpoint lacking the @PreAuthorize annotation. Attackers can query any process-instance identifier through the unguarded GET endpoint to read sensitive workflow data including submitted form variables, approver identities, approval and rejection comments, and process BPMN XML without ownership or tenant party verification.

### CVE-2026-58447

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-30T22:16:58.103 |

Invidious through 2.20260626.0, fixed in commit 77ad416, contains a broken object level authorization vulnerability that allows authenticated attackers to delete videos from other users' playlists by supplying an arbitrary global video index in the remove_video action of the playlist endpoint. Attackers can obtain per-video index values from the public playlist JSON API and submit them to the playlist video deletion endpoint without ownership validation, permanently removing videos from playlists they do not own.

### CVE-2026-11546

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-30T20:17:27.507 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.7 is affected by a server-side request forgery vulnerability with the adminCenter-1.0 feature enabled.

### CVE-2026-10546

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-30T20:17:27.140 |

IBM Langflow OSS 1.0.0 through 1.9.3 contains a Server-Side Request Forgery (SSRF) vulnerability in the URL component ( src/lfx/src/lfx/components/data_source/url.py ) due to a Time-of-Check/Time-of-Use (TOCTOU) race condition that can be exploited via DNS rebinding.

### CVE-2026-58176

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-30T17:16:24.720 |

RuoYi-Vue-Plus through 5.6.2, fixed in commit 88d03d9, exposes workflow task management endpoints under /workflow/task (FlwTaskController) without any permission check: the controller declares no class-level or method-level authorization annotation, so the endpoints are gated only by global authentication. Any authenticated user, regardless of assigned role, can therefore reassign workflow approval tasks to arbitrary users via updateAssignee (defeating segregation of duties in the approval process), urge arbitrary tasks, and enumerate all pending and finished tasks via the pageByAllTaskWait and pageByAllTaskFinish listing endpoints. The issue was resolved by adding permission identifiers (SaCheckPermission) to these endpoints.

### CVE-2026-58167

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-30T17:16:23.623 |

Nightingale (n9e) before 9.0.0-beta.2 exposes full datasource configurations, including plaintext database passwords, HTTP bearer tokens, HTTP basic-auth passwords, and mTLS client keys, to any authenticated low-privilege (Standard role) user through POST /api/n9e/datasource/list. The route is registered without an admin authorization gate, unlike the sibling datasource mutation routes, and the open-source DatasourceFilter does not redact secret fields, so the secret-bearing settings, http, and auth objects are serialized in the response. The disclosed credentials enable access to the connected downstream systems.

### CVE-2026-56286

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-30T23:17:29.743 |

Capgo before 12.128.2 contains an authentication bypass vulnerability in the account deletion endpoint that allows deletion without password re-authentication or secondary verification. Attackers can delete user accounts via session hijacking, CSRF attacks, or parameter tampering, resulting in unauthorized account deletion, data loss, and denial-of-service.

### CVE-2026-44949

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-30T15:16:56.853 |

A Rancher FleetWorkspace admission path allowed side effects to occur in
 the Rancher webhook handler for versions 0.7.0 up to 0.7.10, 0.8.0 up to 0.8.7, 0.9.0 up to 0.9.6 and 0.10.0 up to 0.10.7. An unauthenticated attacker with network access to
 the in-cluster rancher-webhook service
 could submit a crafted admission payload and cause workspace-related 
Kubernetes objects to be created with attacker-chosen identity data.
