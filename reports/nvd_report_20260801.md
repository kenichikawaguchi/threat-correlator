# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-31 15:00 UTC
- **対象期間**: `2026-07-30T15:00:43.000Z` 〜 `2026-07-31T15:00:30.000Z`
- **重要CVE数**: 110 件（Critical 9.0+: 29 件 / High 7.0〜: 81 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** と非常に多く、特に **認証不要でリモートコード実行 (RCE) や完全権限取得** が可能になる脆弱性が目立ちます。  
- 製品別に見ると、**クラウドサービス (Azure Cosmos DB、IBM Cloud 製品)、オープンソースフレームワーク (CodeIgniter、Langflow)、IoT/組み込み系 (ESP32、ルータファームウェア)** が集中しており、攻撃対象が多層化しています。  
- 多くの脆弱性が **ハードコーディングされた認証情報、入力検証不備、サンドボックス回避** といった「**基本的なセキュリティ設計ミス**」に起因している点が共通しています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑18452** | 10.0 | DMS+ (Non‑Mobile) の API キーがハードコードされており、認証なしで全デバイスを完全制御可能 | **認証不要で全デバイスを乗っ取れる** ため、産業制御系や医療機器に波及すると深刻。ハードコードされたキーは即座にローテーションが必要。 |
| **CVE‑2026‑66803** | 10.0 | Azure Cosmos DB の不適切なアクセス制御により、ネットワーク経由でコード実行が可能 | **マイクロソフトのマネージド DB サービス** でのリモートコード実行は、クラウド全体の信頼性を揺るがす。Microsoft の緊急パッチ適用が必須。 |
| **CVE‑2026‑12946 / CVE‑2026‑13435** (同一製品) | 9.9 | IBM Langflow OSS 1.0.0‑1.10.1 のコードインジェクション／サンドボックス回避 | **AI/LLM ワークフロー基盤** が外部から任意コード実行できる。Langflow は社内のデータパイプラインで広く利用されているため、即時アップデートと環境変数の見直しが必要。 |
| **CVE‑2026‑17561** | 9.8 | Logsign SIEM (≤ 6.4.108) のコードインジェクション | **SIEM が攻撃者側に乗っ取られる** と、ログ改ざん・検知回避が可能になる。インシデント対応に直結する危険度が高い。 |
| **CVE‑2026‑63223** | 9.8 | CodeIgniter 4.7.3 以前の `is_image` / `mime_in` バリデーション不備で任意ファイル実行 | **PHP アプリケーション全般に波及**。特にファイルアップロード機能を持つ Web サービスでの遠隔コード実行リスクが顕在。 |

> **注:** 上記は **CVSS が 9.8 以上** かつ **認証不要でリモートコード実行** が可能な点で共通しており、被害拡大の可能性が最も高いものを選出しました。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ（必須）

| 製品 / ライブラリ | 現行脆弱バージョン | 推奨バージョン / 対策 |
|-------------------|-------------------|------------------------|
| **DMS+ (Rich Source)** | すべて（ハードコード API キー） | ベンダー提供の **キーリローテーションパッチ** を即適用し、`config.yaml` 等に外部管理されたシークレットを使用。 |
| **Azure Cosmos DB** | すべて（CVE‑2026‑66803 対象） | Microsoft が公開した **2026‑07‑xx 緊急ロールアウト** を適用。アクセス制御ポリシーを最小権限に再設定。 |
| **IBM Langflow OSS** | 1.0.0‑1.10.1 | **1.10.2 以降** にアップデート。`MCP` 起動スクリプトの `DANGEROUS_ENV_VARS` に `SENSITIVE_ENV` 等を追加し、環境変数のホワイトリスト化。 |
| **Logsign SIEM** | < 6.4.108 | **6.4.108 以上** にアップデート。`payload.json` のデフォルト認証情報を削除し、独自の強力パスワードに変更。 |
| **CodeIgniter** | < 4.7.4 | **4.7.4 以降** に更新。`is_image` / `mime_in` での拡張子チェックを有効化し、アップロードファイル名をサーバ側で再生成。 |
| **SQLite** (3.41 系) | 3.41.0‑3.41.2 | **3.41.3 以降** にアップデート。`jsonCacheInsert` と `btreelock` のパッチが含まれる。 |
| **WordPress – Realtyna Organic IDX / WPL Real Estate** | ≤ 5.3.0 | **5.3.1 以降** に更新。ファイルアップロード時の MIME と拡張子検証を強化し、`nonce` による CSRF 防止を実装。 |
| **Activepieces** | < 0.84.0 | **0.84.0 以上** にアップデート。サンドボックスのパス正規化ロジックを有効化し、テナント間のファイルアクセスを分離。 |
| **LazyOwn RedTeam/APT Framework** | < 0.2.154 | **0.2.154 以上** に更新。デフォルト認証情報 (`LazyOwn`) を削除し、`payload.json` の認証情報を暗号化保存。 |

### 3.2 設定・運用面の緊急対策

1. **ハードコーディングされたシークレットの除去**  
   - 環境変数、Vault、AWS Secrets Manager など外部シークレット管理へ移行。  
2. **最小権限の IAM / RBAC 設定**  
   - Azure Cosmos DB、IBM HMC、Logsign SIEM などは **ネットワーク制限 (IP allow‑list)** と **ロールベースアクセス** を再確認。  
3. **ファイルアップロード・入力検証の強化**  
   - `Content‑Type` と拡張子のホワイトリスト化、サーバ側でのファイル名正規化、サイズ上限設定。  
4. **Web アプリケーションファイアウォール (WAF) の導入**  
   - `SQLi`、`RCE`、`Command Injection` パターンをブロックするルールセットを適用。  
5. **監視・インシデント対応体制の整備**  
   - 重大脆弱性に対する **CVE フィード**（NVD、各ベンダーの Security Advisory

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-18452

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-31T07:16:27.400 |

DMS+ (Non-Mobile) developed by Rich Source has a Use of Hard-coded Credentials vulnerability. Unauthenticated remote attackers can exploit a fixed API key to gain control over all installed DMS+ devices.

### CVE-2026-66803

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-30T21:18:12.743 |

Improper access control in Azure Cosmos DB allows an unauthorized attacker to execute code over a network.

### CVE-2026-12946

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-30T20:16:52.293 |

IBM Langflow OSS 1.0.0 through 1.10.0 could allow a remote attacker to inject arbitrary code on the system, due to the improper control of user input code.

### CVE-2026-13435

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-30T19:17:06.840 |

IBM Langflow OSS 1.0.0 through 1.10.1 contains an improper input validation vulnerability in the PythonREPL sandbox implementation.

### CVE-2026-17561

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-31T13:17:19.730 |

Improper Control of Generation of Code ('Code Injection') vulnerability in Innotim Software, Telecommunications and Consulting Trade Ltd. Co. Logsign SIEM allows Code Injection.

This issue affects Logsign SIEM: before 6.4.108.

### CVE-2026-14483

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-31T07:16:24.803 |

The Realtyna Organic IDX plugin + WPL Real Estate plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 5.2.0 via the upload function. This is due to missing file type validation in the upload function, combined with a publicly accessible I/O endpoint authenticated solely by static, plugin-seeded API credentials that are identical across all installations. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. The WPL I/O service endpoint is registered on the public WordPress init hook with no WordPress capability check, and the required api_key and api_secret values are static defaults seeded by the plugin's own SQL migration files, meaning any unauthenticated attacker who knows these publicly documented defaults can reach and exploit the vulnerable upload path.

### CVE-2026-63223

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-31T06:16:32.297 |

CodeIgniter is a PHP full-stack web framework. Prior to 4.7.4, the is_image and mime_in upload validation rules do not independently enforce a safe client filename extension, allowing a remote attacker to upload executable content when an application preserves the client filename and stores uploads in a web-accessible script-enabled directory. Applications are impacted when they validate uploads using is_image or mime_in without an independent safe extension check (such as ext_in on patched versions), save uploaded files using the client-supplied filename, and place uploads in a web-accessible directory where PHP files can execute. This issue is fixed in version 4.7.4.

### CVE-2026-38709

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-30T22:16:54.970 |

TR1200 v2.4.15, TR3000 v2.4.21, WR300 v2.4.25, WR1200 v2.4.23, WR1300 v2.4.22, WR1500 v2.3.10, WR3000 v2.4.19, WR3600 v2.3.16, and WR6500 v2.3.15 were discovered to contain a command injection vulnerability in the net.set_wan interface. This vulnerability allows attackers to execute arbitrary commands as root via a crafted input.

### CVE-2026-68503

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1392` |
| Published | 2026-07-30T21:18:13.460 |

LazyOwn RedTeam/APT Framework is an AI-powered C2 and red-team operations framework. Prior to 0.2.154, LazyOwn ships default C2 credentials LazyOwn and LazyOwn in payload.json and core/payload_schema.py and passes them unchanged to lazyc2.py HTTP Basic authentication, allowing any network-reachable attacker who knows the defaults to authenticate to the C2 dashboard with operator-level access. This issue is fixed in 0.2.154.

### CVE-2026-68502

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-30T21:18:13.317 |

LazyOwn RedTeam/APT Framework is an AI-powered C2 and red-team operations framework. Prior to 0.2.154, LazyOwn's lazyc2.py registers an unauthenticated Socket.IO input event handler that dispatches data.get('value') to LazyOwnShell.one_cmd, reaching LazyOwnShell.do_cmd and subprocess.call(command, shell=True), allowing unauthenticated remote code execution in the C2 process. This issue is fixed in 0.2.154.

### CVE-2026-51272

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-30T19:18:05.820 |

In schreibfaul1 ESP32-audioI2S 3.4.5, a heap-based buffer overflow vulnerability exists in the latinToUTF8() character encoding conversion function. The function calculates required buffer size by simply doubling input length and reallocates ps_ptr heap buffer without strict boundary validation. Malicious oversized input can trigger insufficient buffer allocation and out-of-bounds write during Latin-1 to UTF-8 conversion, leading to code execution, information disclosure, denial of service or privilege escalation.

### CVE-2026-12943

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T19:17:05.453 |

IBM HMC V10.3.1050.0 through 10.3.1064.0 and IBM HMC V11.1.1110.0 through 11.1.1112.0 Management systems in IBM Power environments (HMC and Novalink) could allow an unauthenticated user to execute arbitrary commands with elevated privileges on the system due to improper validation of user supplied input.

### CVE-2026-12118

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-30T19:17:04.483 |

IBM webMethods Integration (on prem) 10.15, 10.11 could allow an unauthenticated remote attacker to execute arbitrary code on the system due to the deserialization of untrusted data.

### CVE-2026-51291

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-30T17:16:32.240 |

sqlite 3.41 is vulnerable to use after free in the json.c jsonCacheInsert function of the JSON cache management module.

### CVE-2026-12940

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T17:16:28.040 |

IBM Langflow OSS 1.0.0 through 1.10.1  are vulnerable to unauthenticated remote code execution via environment variable injection in the MCP (Model Context Protocol) stdio launcher. The vulnerability exists in src/lfx/src/lfx/base/mcp/util.py where the DANGEROUS_ENV_VARS blocklist fails to include SHELLOPTS , BASHOPTS , and PS4 environment variables.

### CVE-2026-4978

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-30T16:17:12.933 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in UMAI Vision Traffic Analysis System allows SQL Injection.

This issue affects Traffic Analysis System: from 30 before 34.

### CVE-2026-28323

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-30T16:17:10.710 |

SolarWinds Web Help Desk is found to be affected by a SAML authentication bypass vulnerability. This requires the SAML 2.0 authentication method to be enabled.

### CVE-2026-15435

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-30T15:16:26.757 |

IBM App Connect Enterprise 13.0.1.0 through 13.0.7.2, and 12.0.1.0 through 12.0.12.27 could allow a remote attacker to traverse directories on the system. An attacker could send a specially crafted URL request containing "dot dot" sequences (/../) to write arbitrary files on the system.

### CVE-2026-66066

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-07-30T19:18:35.843 |

Action Pack is a framework for handling and responding to web requests. In versions prior to 7.2.3.2, 8.0.5.1 and 8.1.3.1, Active Storage does not disable libvips operations marked unsafe for untrusted content, allowing a crafted upload to invoke such an operation. Consuming applications are affected when configured to use libvips and accept image uploads from untrusted users. An unauthenticated attacker may exploit this behavior to read arbitrary files accessible to the Rails process, including environment variables and application secrets. Exposure of credentials such as secret_key_base or external-service tokens may enable remote code execution or lateral movement. This issue has been fixed in versions 7.2.3.2, 8.0.5.1 and 8.1.3.1.

### CVE-2026-63221

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-31T06:16:31.603 |

CodeIgniter is a PHP full-stack web framework. From 4.3.0 through 4.7.3, Query Builder deleteBatch() substitutes bound values from where() conditions into generated SQL while ignoring their escape flags, allowing user-controlled condition values to be interpreted as SQL. This affects only the deleteBatch() code path. Regular delete() operations escape where() binds correctly. This issue is fixed in version 4.7.4.

### CVE-2025-67649

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-31T12:16:48.107 |

A SQL injection vulnerability has been identified in PHP Jabbers - Car Rental Script . Improper neutralization of input provided by user into parameters responsible for sorting functions allows an unauthenticated attacker to perform SQL Injection attacks.

This issue was fixed in version 4.1.

### CVE-2026-66418

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-30T21:18:12.490 |

OpenClaw Dashboard v3.0.0 contains a stored cross-site scripting vulnerability that allows unauthenticated remote attackers to inject arbitrary HTML and script payloads by submitting a crafted username in a failed login POST request, which is recorded verbatim in the audit log. When an administrator opens the notification panel, the unescaped log entry is rendered via innerHTML with a permissive Content-Security-Policy allowing inline event handlers, enabling the attacker-supplied payload to execute in the administrator's session and interact with authenticated endpoints including agent instruction file editing and configuration changes.

### CVE-2026-67594

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-30T20:18:15.173 |

Spikster through commit e1cdf8c contains a missing authentication vulnerability that allows unauthenticated remote attackers to access all API routes by exploiting the unattached CipiAuth middleware, which is registered but never applied to any route in the API routing configuration. Attackers can invoke approximately 50 unprotected API endpoints to enumerate and provision servers, reset root passwords, read and write arbitrary files on the host, and create database users.

### CVE-2026-67208

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-1188` |
| Published | 2026-07-30T20:18:14.323 |

Juggle through 1.6.0 contains a remote code execution vulnerability that allows unauthenticated remote attackers to execute arbitrary OS commands by connecting to the exposed H2 database web console using default shipped credentials. Attackers can access the unprotected /h2-console endpoint, authenticate with default credentials, and leverage the H2 CREATE ALIAS Runtime.exec() technique to execute arbitrary commands, resulting in root-level code execution when running the stock Docker image.

### CVE-2026-48499

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-285;CWE-668;CWE-732` |
| Published | 2026-07-30T19:17:32.747 |

Activepieces is an open source AI workflow automation platform. Prior to 0.84.0, an unsanitized path segment in the Code piece sandbox can let an authenticated flow author reach read-write cached flow and code files belonging to other tenants on the same worker, exposing embedded data and allowing modified code to execute on a victim tenant's next flow run. This issue is fixed in version 0.84.0.

### CVE-2026-11707

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-30T15:16:24.010 |

IBM Tivoli System Automation Application Manager 4.1 and IBM WebSphere Application Server is affected by a cross-site scripting vulnerability in the administrative console login page.

### CVE-2026-52539

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-30T21:17:47.213 |

Outstatic CMS <= 2.1.9 contains a hardcoded JWT signing secret. When the OST_TOKEN_SECRET environment variable is not set, the application falls back to the default value which is publicly visible in the source code repository. An unauthenticated remote attacker can exploit this by forging JWT session tokens with arbitrary user data and full administrative permissions.

### CVE-2026-51290

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-30T17:16:32.133 |

SQLite 3.41 has a use-after-free vulnerability in the shared cache lock management logic of the btree module. The program frees a BtLock structure without removing the node from the linked list. Subsequent linked list traversal accesses the released memory, which can lead to denial of service and sensitive memory information disclosure.

### CVE-2026-53431

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-07-30T15:16:33.567 |

Authentication Bypass by Capture-replay vulnerability in malach-it Boruta allows an attacker who has obtained a previously valid JWT client assertion to authenticate as the issuing OAuth client after the assertion has expired.

Boruta accepts JWT-based client authentication (client_secret_jwt and private_key_jwt token endpoint authentication methods) but never enforces that the assertion's exp claim is in the future. The pre-check helper Boruta.Oauth.Request.Base.check_expiration/1 in lib/boruta/oauth/request/base.ex only verifies that an exp claim is present (it pattern-matches on the existence of the key and returns success), and the Joken token configuration used for signature verification, Boruta.Oauth.Authorization.Client.Token.token_config/0 in lib/boruta/oauth/authorization/client.ex, returns an empty map, so Joken's default exp claim validator is not engaged either. Any attacker who obtains a validly-signed client assertion (for example through logs, reverse proxies, browser tooling, or other observability surfaces) can replay it indefinitely to authenticate as the client and obtain access tokens with that client's privileges.

This issue affects boruta: from 2.3.0 before 2.3.7.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-16236

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-31T07:16:27.257 |

The Realtyna Organic IDX plugin for WordPress is vulnerable to Arbitrary File Upload in versions up to, and including, 5.3.0. This is due to missing file extension and content validation in the saveLiveImages() function combined with an insufficient authorization check on the get_keys() AJAX handler and a missing authentication check on the REST API import endpoint. This makes it possible for authenticated attackers, with subscriber-level access and above, to upload arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-66421

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-30T23:16:53.687 |

OpenClaw Dashboard contains a stored cross-site scripting vulnerability that allows unauthenticated remote attackers to execute arbitrary JavaScript in the administrator's browser session by injecting HTML markup into agent transcript messages processed through the sessions API. Attackers can craft a message containing inline event handler payloads such as an img tag with an onerror attribute within the 60-character rendering budget, which is stored in the session transcript and interpolated unsanitized into innerHTML on the default landing page, allowing theft of session tokens and unauthorized calls to authenticated administrative endpoints including agent instruction file modification.

### CVE-2026-58222

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-90` |
| Published | 2026-07-30T16:17:14.933 |

A security flaw combining LDAP filter injection and improper authorization checks was found in Samba Active Directory Domain Controller (AD DC). When processing LDAP Compare requests, Samba fails to properly validate user-supplied attribute names and executes the resulting internal database search in a trusted context, bypassing normal Access Control List (ACL) enforcement. An authenticated low-privilege domain user can exploit these flaws to disclose confidential Active Directory attributes that would normally be inaccessible. The disclosed information may be leveraged to derive sensitive authentication material, potentially leading to privilege escalation and complete domain compromise. For example: In deployments configured with Group Managed Service Accounts (gMSAs), an attacker can extract the "msKds-RootKeyData" attribute and derive gMSA passwords offline, potentially leading to complete domain compromise if privileged gMSAs are present.

### CVE-2026-28813

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-30T16:17:11.070 |

Apache JSPWiki, up to 2.12.3, is vulnerable to JSON Hijacking, which leads to csrf vulnerabilities.
Users are recommended to upgrade to version 2.12.4, which fixes this issue.

### CVE-2026-14522

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-30T15:16:25.693 |

IBM App Connect Enterprise 13.0.1.0 through 13.0.7.2, and 12.0.1.0 through 12.0.12.27 could allow a remote attacker to execute arbitrary commands due to improper neutralization of CRLF characters.

### CVE-2026-66360

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-30T23:16:53.070 |

The ISO Presentation layer contains a flaw in the handling of specific 
parameters during normal mode negotiation. A missing length check in the
 processing of the encoded presentation data allows an attacker 
controlled field with a zero length value to trigger a bounded heap over
 read. This condition occurs before MMS session establishment, a crafted
 TCP/102 connection attempt can trigger the issue. The resulting over 
read causes the process to terminate, leading to a denial of service 
condition.

### CVE-2026-65423

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-30T23:16:52.743 |

An integer overflow in the UA_Variant arrayDimensions product 
computation in open62541 may allow a remote attacker to trigger an 
out-of-bounds write.

### CVE-2026-63559

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-30T22:16:55.717 |

An integer overflow in the UA_Variant arrayDimensions product 
computation in open62541 may allow a remote attacker to read 
out-of-bounds heap memory, potentially disclosing sensitive information.

### CVE-2026-12562

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-30T22:16:53.343 |

The RCU II+ and Multiload II+ are vulnerable to an unauthenticated 
service that exposes a debug interface granting full root-level access 
to the embedded system. This vulnerability stems from a 
network-accessible port running a Target Communications Framework (TCF) 
service that does not require any authentication, allowing an attacker 
to directly interact with the Linux environment that powers the device. 
Once connected, an attacker can freely view and modify the filesystem, 
manipulate running processes, and control network interfaces, enabling 
deep alteration of system behavior.

### CVE-2026-55768

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-681;CWE-789` |
| Published | 2026-07-30T21:17:57.193 |

GoAccess is a real-time web log analyzer and interactive viewer that runs in a terminal in *nix systems or through the browser. Prior to version 1.11, the built-in WebSocket server narrows a 64-bit extended frame length into the signed 32-bit WSFrame.payloadlen field before enforcing the maximum frame size, allowing an unauthenticated remote client to bypass the guard and force an approximately 18-exabyte allocation request that terminates the process. This issue is fixed in version 1.11.

### CVE-2026-67207

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-697` |
| Published | 2026-07-30T20:18:14.180 |

Wolf CMS through 0.8.3.1 contains an authorization bypass vulnerability in BackupRestoreController that allows authenticated non-administrative users to access restricted backup functionality due to a PHP operator precedence flaw in the permission check expression. Attackers can exploit the incorrect evaluation of the access control expression to create, download, and restore backups without administrative privileges.

### CVE-2026-67206

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-30T20:18:14.030 |

Wolf CMS through 0.8.3.1 contains a remote code execution vulnerability in FileManagerController that allows authenticated attackers to create arbitrary PHP files by exploiting missing file extension validation in the create_file() and save() functions. Attackers with the file_manager_mkfile capability can write malicious PHP content into the web-accessible FILES_DIR directory and trigger execution by requesting the file over HTTP.

### CVE-2026-18140

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-07-30T19:17:26.457 |

Uncontrolled recursion in the unknown-key skip path of the aws-smithy-json runtime crate before 0.62.7, which the smithy-rs code generator invokes from every generated struct deserializer, might allow remote unauthenticated users to cause a denial of service (process abort via stack exhaustion) via a single small HTTP request containing deeply nested JSON to a smithy-rs generated server.



To remediate this issue, users should upgrade to aws-smithy-json 0.62.7 or later and rebuild.

### CVE-2026-54722

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-76` |
| Published | 2026-07-30T17:16:33.180 |

DSSRF is a Node.js library that provides a wide range of utilities and advanced SSRF defense checks. Prior to 1.0.4, is_url_safe in src/helpers.ts strips the @ userinfo delimiter with remove_at_symbol_in_string before new URL parses the URL, allowing an attacker-controlled URL to bypass internal-IP validation and cause a client using the original URL to reach an internal service. This issue is fixed in version 1.0.4.

### CVE-2026-67349

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-30T15:16:36.900 |

OpenCost before 1.121.0 fails to authenticate the GET /helmValues endpoint, exposing base64-decoded HELM_VALUES environment variable containing cloud provider credentials. Additionally, adminAuthMiddleware fails open when ADMIN_TOKEN is unset, allowing unauthenticated attackers to modify GCP service account keys via POST /serviceKey to redirect billing calls.

### CVE-2026-46593

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-31T12:16:50.527 |

A SQL injection vulnerability has been identified in the PHP Jabbers - PHP Poll Script. Improper neutralization of input provided by user to pjAdminPolls.controller.php endpoint allows an authenticated attacker to perform SQL Injection attacks.
This issue was fixed in version 4.1.

### CVE-2025-67650

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-31T12:16:48.250 |

An authenticated SQL injection vulnerability has been identified in multiple PHP Jabbers scripts. Improper neutralization of input provided by an authenticated user into parameters responsible for sorting functions allows an attacker to perform SQL Injection attacks.
This issue was fixed in the versions specified in the affected products list.

### CVE-2026-66420

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-30T23:16:53.527 |

MeshCentral 1.1.21 contains a cross-site WebSocket hijacking protection bypass vulnerability that allows unauthenticated remote attackers to hijack authenticated administrator sessions by exploiting an unconditional early return in the CheckWebServerOriginName() function within webserver.js when self-signed certificates are in use. Attackers can open cross-origin WebSocket connections to any of the twelve WebSocket endpoints, send crafted action commands to exfiltrate the server sessionKey used to sign session cookies, forge session tokens as arbitrary users, and gain full remote control of all managed devices governed by the MeshCentral instance.

### CVE-2026-66416

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-30T19:18:36.340 |

Leantime 3.6.2 contains a cross-site request forgery vulnerability that allows unauthenticated attackers to perform state-changing actions on behalf of authenticated users by excluding the Laravel VerifyCsrfToken middleware from the global middleware stack in app/Http/Kernel.php. Attackers can craft malicious pages delivered via phishing emails or malicious websites to trigger unauthorized POST, PUT, and DELETE requests that create or delete projects, modify settings, and change permissions as any authenticated user.

### CVE-2026-67348

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-30T15:16:36.657 |

Julep contains an insecure direct object reference vulnerability in the get_execution_details endpoint that allows authenticated tenants to read another tenant's execution data. Attackers can supply arbitrary execution_id values to retrieve sensitive execution records including task inputs, outputs, metadata, and temporal task tokens from other tenants.

### CVE-2026-10079

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-07-31T10:16:43.190 |

A flaw was found in Red Hat Advanced Cluster Security for Kubernetes (RHACS). When processing Kubernetes Deployments, ACS replaces deployment identity metadata based on the openshift.io/encoded-deployment-config label. A user with permission to create Deployments can set this label to "null", causing ACS to treat the workload as having empty UID, name and labels and namespace "default". This bypasses deploy-time policy detection and enforcement visibility, prevents correct persistence in Central and breaks violation reporting and compliance correlation for the affected deployment.

### CVE-2026-62246

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-653` |
| Published | 2026-07-30T22:16:55.300 |

Kamaji is the Hosted Control Plane Manager for Kubernetes. Prior to 26.7.4-edge, Kamaji derives a TenantControlPlane datastore schema, database user, and etcd key prefix from a lossy namespace-and-name normalization in GetDefaultDatastoreSchema() and GetDefaultDatastoreUsername(), allowing distinct tenants with colliding normalized identifiers to share control-plane state and read, modify, or destroy another tenant's Kubernetes data. This issue is fixed in version 26.7.4-edge.

### CVE-2026-11536

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-30T20:16:52.140 |

IBM WebSphere Application Server 9.0, and 8.5 is affected by a remote code execution vulnerability in the SOAP/JMX connector.

### CVE-2026-67345

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-183` |
| Published | 2026-07-30T15:16:35.583 |

MaxKey through 4.1.12, fixed in commit ddbb72f, contains an insufficient redirect URI validation vulnerability in DefaultRedirectResolver.hostMatches() that allows remote attackers to hijack OAuth 2.0 authorization codes by supplying a crafted redirect_uri whose hostname suffix matches a registered URI without proper dot-boundary anchoring. Attackers who control a domain ending with the registered redirect URI hostname can social-engineer victims into clicking a crafted authorization URL, causing the authorization code to be issued to the attacker-controlled URI and exchanged for an access token granting access to the victim's identity.

### CVE-2026-66415

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-30T19:18:36.190 |

Leantime 3.6.2 contains a server-side request forgery and local file inclusion vulnerability that allows authenticated attackers to read internal resources by passing unsanitized user-supplied filenames to file_get_contents() in the Blueprints::import() method without path validation. Attackers can submit crafted filenames containing URL wrappers or path traversal sequences through the JSON-RPC API endpoint to access cloud metadata services or read arbitrary files from the server filesystem.

### CVE-2026-10535

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-30T19:17:01.167 |

IBM Db2 11.5.0 through 11.5.9, and 12.1.0 through 12.1.4 is vulnerable to buffer overflow in setgid helper db2flacc.

### CVE-2026-11885

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-07-30T17:16:27.760 |

IBM PowerVM Hypervisor FW1110.00 through FW1110.20, FW1060.00 through FW1060.71, and FW950.00 through FW950.H1 A carefully crafted OS hypervisor call can cause the PowerVM hypervisor to crash or compromise OS memory integrity.

### CVE-2026-57862

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-30T16:17:14.607 |

Kanboard 1.2.52 and prior contains a server-side request forgery vulnerability that allows authenticated users to bypass SSRF protections by supplying hexadecimal IP address notation in user-controlled URLs. Attackers can submit hexadecimal-encoded internal IP addresses through the web link creation feature, causing cURL to resolve and connect to internal network resources such as cloud instance metadata services, localhost services, and RFC1918 addresses while the isPrivateURL() filter in app/Core/Http/Client.php incorrectly treats the input as safe due to FILTER_VALIDATE_IP rejecting non-dotted-decimal notation.

### CVE-2026-65635

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:L/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-653` |
| Published | 2026-07-30T15:16:35.017 |

Improper Isolation or Compartmentalization vulnerability in malach-it boruta (Elixir.Boruta.Openid module) allows attackers to register OpenID Connect clients with administrative privileges through the dynamic client registration entry point. Boruta.Openid.register_client/3 forwards caller-supplied registration parameters to the administrative client creation path without a public/admin field-level allowlist, so an unauthenticated registrant can set security-sensitive attributes including supported grant types, authorized scopes, PKCE enforcement, public refresh and revocation behavior, token lifetimes, and signing settings. The library does not distinguish between metadata a public registrant is allowed to set and administrative controls that should require operator approval.

This vulnerability is associated with program files lib/boruta/openid.ex and program routines 'Elixir.Boruta.Openid':register_client/3, 'Elixir.Boruta.Openid':parse_registration_params/2.

This issue affects boruta from 2.3.0 before 2.3.7.

### CVE-2026-14980

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-30T15:16:26.120 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.8 is vulnerable to cross-site request forgery which could allow an attacker to perform SSRF attacks with elevated privileges when the collectiveController-1.0 feature is enabled.

### CVE-2026-56672

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-31T06:16:30.170 |

ComfyUI is a node-based diffusion model GUI, API, and backend. Prior to 0.28.0, GET /userdata/{file} served user-controlled HTML and SVG files with extension-derived content types, allowing stored cross-site scripting in the ComfyUI origin and access to browser-stored API tokens, settings, workflows, and authenticated-equivalent API calls. The handler used web.FileResponse(path), so an uploaded .html/.svg was served as text/html/image/svg+xml. POST /userdata stores arbitrary request bodies (confined to the user's userdata directory). When a victim navigated to the file URL, the embedded script executed same-origin. The /view endpoint already forced dangerous MIME types to download; that protection had never been applied to /userdata. This issue is fixed in version 0.28.0.

### CVE-2026-56670

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-31T06:16:27.560 |

ComfyUI is a modular diffusion model GUI, api and backend with a graph/nodes interface. Prior to 0.28.0, the /view endpoint served uploaded SVG files inline because image/svg+xml and related XML content types were absent from the dangerous-content-type handling, allowing stored cross-site scripting in the ComfyUI origin. This issue is fixed in version 0.28.0.

### CVE-2026-63362

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-07-30T23:16:52.263 |

An unsigned integer underflow in the PubSub signature verification path 
in open62541 may allow a remote attacker to cause a denial of service 
via a crafted UDP packet.

### CVE-2026-18064

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-30T22:16:54.790 |

An incomplete fix for CVE-2026-15352 in the NASA core Flight System 
(cFS) Health and Safety (HS) application leaves a separate NULL pointer 
dereference reachable in versions through 7.0.1. An attacker who can 
trigger the affected command under specific conditions could cause the 
HS application to crash, resulting in a denial-of-service condition and 
processor reset.

### CVE-2026-65313

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-798;CWE-1392` |
| Published | 2026-07-31T09:16:59.090 |

A provisioning script used when installing HIPASE-250 (formerly 250
SCALA) engineering workstations sets a fixed, hard-coded x11vnc
password. Because the same credential is applied to every workstation
provisioned this way, an attacker with adjacent-network access who
knows the password can gain VNC access to affected workstations.

### CVE-2026-14537

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-31T02:16:27.687 |

Incorrect Authorization in the direct HTTP API tool invocation endpoint in Google mcp-toolbox versions v1.3.0 and v1.4.0 allows an unauthenticated attacker to invoke tools protected by the scopeRequired feature via sending tool invocation requests through legacy HTTP endpoints when the --enable-api flag is active.

### CVE-2026-13444

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-520` |
| Published | 2026-07-30T19:17:06.997 |

IBM Langflow OSS 1.0.0 through 1.10.1 can allow an attacker to access another user's private vector documents by creating their own flow with matching Chroma persist_directory and collection_name values. The attacker receives exact victim content in their workflow output despite having no authorization to read the victim's flow. Additionally, the attacker can pollute the victim's collection by inserting their own documents into the shared namespace.

### CVE-2026-14541

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-31T03:16:24.170 |

An authentication bypass and audience confusion vulnerability exists in the Google OAuth provider component of Google mcp-toolbox version 1.4.0. When a Google authService is initialized with mcpEnabled: true but lacks an explicitly defined audience or clientId, the ValidateMCPAuth pipeline for opaque tokens skips audience validation entirely. As a result, the toolbox will accept any valid Google OAuth access token—even those minted for unrelated ecosystem applications—granting unauthorized clients access to protected tools and data backends.

### CVE-2026-14540

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-31T02:16:29.060 |

A Server-Side Request Forgery (SSRF) vulnerability exists in the generic HTTP source and tool components of Google mcp-toolbox versions 0.3.0 through 1.4.0. While the toolbox implements baseline input sanitization for user-controlled parameters, the underlying HTTP client (internal/sources/http/http.go) fails to safely regulate request redirection boundaries. Specifically, the client is initialized without a restrictive CheckRedirect policy hook and lacks target IP validation. An attacker or a malicious data-driven prompt can supply a crafted path parameter that triggers an open redirect or a direct destination swap on the target backend, coercing the mcp-toolbox into blindly following the redirection and making unauthorized requests to internal or arbitrary external endpoints.

### CVE-2026-6540

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-23` |
| Published | 2026-07-30T15:16:37.533 |

Calico's Application Layer Policy (disabled by default), which enforces HTTP rules through Dikastes, fails to perform URL path normalization. As a result, HTTP requests using path-traversal segments, encoded slashes, or repeated slashes are not correctly evaluated by Prefix path rules. Dikastes authorizes the request under the permitted prefix while the downstream workload or a fronting proxy normalizes the path and serves the restricted endpoint. An attacker with network access and no special RBAC can potentially reach HTTP endpoints the policy was intended to restrict.

### CVE-2026-18157

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-31T03:16:25.223 |

A flaw was found in yggdrasil-worker-package-manager. A local attacker with existing access to the system could exploit an argument injection vulnerability in the APT backend. This allows specially crafted package names, which begin with a hyphen, to be misinterpreted as command options by apt-get. Successful exploitation could lead to remote code execution (RCE) with root privileges, enabling the attacker to fully compromise the system's integrity, confidentiality, and availability.

### CVE-2026-67346

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-30T15:16:35.953 |

Swarms through 6.8.1, fixed in commit 8b0fc9e, contains a server-side request forgery vulnerability in the _is_safe_url function that fails to validate hostnames through DNS resolution, allowing attackers to bypass the blocklist. Attackers can supply user-controlled image or audio URLs that resolve to private, loopback, or metadata addresses to reach internal services and exfiltrate credentials.

### CVE-2026-5846

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-07-30T22:16:55.107 |

The affected Watchfire Controller Software contains self-signed hard-coded RSA private keys and corresponding X.509 certificates used for authenticating and encrypting HTTPS/TLS connections to the controller's built-in web management interface. These keys are embedded in plaintext within the application patch binaries in the firmware directly from Watchfire's Remote Support filestore.

### CVE-2026-67527

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-30T20:18:14.473 |

OpenProject is open-source, web-based project management software. Prior to 17.6.0, PATCH /api/v3/work_packages/{id} accepted _links.fileLinks and allowed authenticated users with edit_work_packages but without manage_file_links to resolve Storages::FileLink records by raw id, detach or hard-delete existing FileLinks, and re-parent FileLinks from other projects to an attacker-controlled work package, exposing origin filename, origin id, and MIME type metadata. This issue is fixed in 17.6.0.

### CVE-2026-18358

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-31T13:17:19.933 |

A flaw was found in gnome-remote-desktop as shipped in Red Hat Enterprise Linux. When the daemon is running in system mode with RDP enabled, the incoming connection handler bypasses the connection throttler, allowing an unauthenticated remote attacker to open many parallel pre-authentication connections to the RDP listener. This can accumulate accepted sockets and pending routing-token operations until timeout, exhausting resources and preventing legitimate users from establishing RDP sessions. This issue does not affect the upstream version.

### CVE-2026-15722

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-31T10:16:44.863 |

A stack buffer overflow flaw was found in 389 Directory Server (389-ds-base). The get_ruvelement_from_berval() function in repl5_ruv.c copies digit characters from a network-supplied RUV berval into a fixed 16-byte stack buffer without bounds checking. A remote unauthenticated attacker can crash the LDAP server by sending a crafted StartNSDS50ReplicationRequest extended operation containing a replica ID field with more than 16 digit characters. The overflow occurs during payload decoding, before any authorization check. Stack protectors limit impact to denial of service.

### CVE-2026-11770

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-90` |
| Published | 2026-07-31T10:16:44.720 |

A flaw was found in 389 Directory Server. An unauthenticated remote attacker can inject LDAP search filters into the CleanAllRUV replication status-check extended operation. Because the handler performs the search against cn=config with elevated replication plugin privileges and returns a boolean match result, the attacker can extract sensitive server configuration metadata, including replication bind DNs and password storage scheme information.

### CVE-2026-65310

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306;CWE-942` |
| Published | 2026-07-31T09:16:58.447 |

ANDRITZ HIPASE-250 (formerly 250 SCALA), in the default configuration
of affected versions, exposes its data and configuration endpoint
without any authentication and permissive CORS on every response. An
unauthenticated attacker with network access can read live process
values and server configuration.

### CVE-2026-65309

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-257;CWE-327` |
| Published | 2026-07-31T08:16:28.330 |

ANDRITZ HIPASE-250 (formerly 250 SCALA) in affected versions stores
and transmits user passwords using a reversible format instead of a
one-way password hash. This allows an attacker able to read the
credential store or capture network traffic to recover all stored
passwords.

### CVE-2026-14830

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-31T07:16:25.097 |

The FlxWoo WordPress plugin before 3.1.1 does not verify with the payment processor that a checkout session was actually paid before marking the associated order as paid, allowing unauthenticated attackers to complete WooCommerce orders without paying.

### CVE-2026-14333

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-31T07:16:24.703 |

The Demi  WordPress plugin before 0.0.7 stores its full-site backup archives in a publicly accessible location under a predictable filename and without access protection, allowing unauthenticated attackers to download complete backups including the site database and its user password hashes.

### CVE-2026-63222

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-31T06:16:31.953 |

CodeIgniter is a PHP full-stack web framework. Prior to 4.7.4, calling UploadedFile::move() without a second argument uses the client-provided filename without sanitization, allowing a remote attacker to use path traversal sequences to write uploaded content outside the intended directory when the application exposes an upload path. This issue is fixed in version 4.7.4.

### CVE-2026-56673

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-31T06:16:30.520 |

ComfyUI is a modular diffusion model GUI, API, and backend with a graph-and-node interface. Prior to 0.28.0, folder_paths.get_annotated_filepath and exists_annotated_filepath join workflow-controlled annotated filenames to a base directory without a containment check, allowing an unauthenticated crafted POST /prompt workflow using LoadImage or sibling nodes to probe arbitrary host paths and exfiltrate image-format files through /view. LoadImage defines a VALIDATE_INPUTS method, which causes the execution engine to skip COMBO (input-directory) validation. Affected nodes include LoadImage, LoadImageMask, LoadImageOutput, LoadAudio, LoadLatent, LoadVideo, and Load3D. This issue is fixed in version 0.28.0.

### CVE-2026-56671

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-31T06:16:29.860 |

ComfyUI is a modular diffusion model GUI, api and backend with a graph/nodes interface. Prior to 0.28.0, get_model_preview in app/model_manager.py joins an unrestricted filename route capture to a selected model directory without a containment check, allowing an unauthenticated remote attacker to use traversal, encoded traversal, absolute paths, or an unbounded path_index to read image-decodable files and enumerate host paths. get_model_preview (app/model_manager.py) built the path with os.path.join(folder, filename) where filename is an unrestricted {filename:.*} route capture. Literal ../, percent-encoded %2e%2e%2f, and absolute paths all escaped the model directory; path_index was also unbounded. The target file is piped through Pillow and re-encoded as WEBP, so disclosure is limited to image-decodable files plus a file-existence/enumeration oracle (and internal-path leakage via path_index errors). This issue is fixed in version 0.28.0.

### CVE-2026-68500

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-30T21:18:13.007 |

Sylius Mollie Plugin provides Mollie payment integration for Sylius applications. Prior to 2.2.8, 3.2.4, and 3.3.1, Sylius Mollie Plugin's POST /{_locale}/update-payment payment webhook accepts attacker-controlled id and orderId parameters but does not verify that the Mollie payment belongs to the referenced Sylius order, allowing an unauthenticated attacker with any valid paid Mollie payment ID to mark a victim order as paid without transferring funds for that order. This issue is fixed in 2.2.8, 3.2.4, and 3.3.1.

### CVE-2026-61536

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-470` |
| Published | 2026-07-30T19:18:34.553 |

Banks generates meaningful LLM prompts using a simple template language. In versions prior to 2.4.3, banks parses Tool JSON objects from the rendered body of {% completion %} blocks and later resolves their import_path field through importlib.import_module(...) + getattr(...) to obtain the callable that handles a tool call. There is no allowlist or sanitization on import_path, so any importable Python attribute (e.g. os.system, subprocess.getoutput) can be selected. When the LLM emits a tool_calls entry whose function.name matches the attacker-supplied tool name, the resolved callable is invoked with kwargs decoded from tool_call.function.arguments, yielding arbitrary code execution in the banks-hosting process. This is distinct from GHSA-gphh-9q3h-jgpp / CVE-2026-44209. That advisory was fixed in 2.4.2 by switching src/banks/env.py from Environment to SandboxedEnvironment. The fix does not touch src/banks/extensions/completion.py, and the unsafe import + getattr chain still executes on 2.4.2. The malicious Tool JSON is plain text in the rendered template body — it requires no Jinja attribute access, so the sandbox is irrelevant. This issue has been fixed in version 2.4.3.

### CVE-2026-12942

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-30T19:17:05.297 |

IBM Langflow OSS 1.0.0 through 1.10.1 could allow a remote attacker to traverse directories on the system. An attacker could send a specially crafted URL request containing "dot dot " sequences ( /.. /) to view arbitrary files on the system.

### CVE-2026-12733

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-30T19:17:04.867 |

IBM DataPower Gateway could allow a remote attacker to cause a denial of service due to improper resource limitations.

### CVE-2026-10545

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-601` |
| Published | 2026-07-30T19:17:01.597 |

IBM Planning Analytics Local 2.1.0 through 2.1.21 is vulnerable to an open redirect that allows an attacker to redirect users to arbitrary external websites via a crafted URL. If used in SSO authentication flows, this could result in exposure of session tokens and allow attackers to hijack user sessions.

### CVE-2024-25039

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-30T19:16:56.507 |

IBM Engineering Requirements Management DOORS and DOORS Web Access 9.7.2.1 through 9.7.2.11, and 9.6.1.1 through 9.6.1.13 do not limit the length of a connection which could allow for a Slowloris HTTP denial of service attack to take place. This can cause the web server to become unresponsive.

### CVE-2026-9322

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-30T17:16:34.580 |

IBM WebSphere Application Server 9.0, and 8.5 and IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.7 are vulnerable to a denial of service via a crafted HTTP request.

### CVE-2026-62663

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-30T17:16:33.900 |

Banks generates meaningful LLM prompts using a simple template language. In versions prior to 2.4.4, all four media filters (image, audio, video, document) in banks accept untrusted user input as file paths via Path(value) and pass them directly to open(file_path, "rb") without any path sanitization, canonicalization, or directory restriction. An attacker who controls template variables passed to a banks Prompt can use path traversal (../) to read arbitrary files accessible to the Python process—including .env files, SSH keys, cloud credentials, source code, /etc/passwd, and /etc/shadow—with the content returned base64-encoded in the rendered prompt output, making exfiltration trivial. This is particularly dangerous for applications that use banks to process user-provided template variables before sending prompts to an LLM. This issue has been fixed in version 2.4.4.

### CVE-2026-10842

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-289` |
| Published | 2026-07-30T16:16:53.980 |

IBM WebSphere Application Server 8.5, and 9.0 and IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.7 Traditional and Liberty could allow a remote attacker to bypass security constraints.

### CVE-2026-16308

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-30T15:16:26.910 |

IBM Enterprise Build of Quarkus 3.27.1 through 3.27.4.SP2, and 3.33.1 through 3.33.2.SP2 Quarkus REST could allow a remote attacker to cause a denial of service due to unbounded accumulation of multipart MIME part-header bytes.

### CVE-2026-14519

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-30T15:16:25.547 |

IBM App Connect Enterprise 13.0.1.0 through 13.0.7.2, and 12.0.1.0 through 12.0.12.27 could allow a remote attacker to read arbitrary files due to a path traversal vulnerability.

### CVE-2026-12947

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-07-30T15:16:24.427 |

IBM App Connect Enterprise 13.0.1.0 through 13.0.7.2, and 12.0.1.0 through 12.0.12.27 stores potentially sensitive information in log files that could be read by a local user.

### CVE-2026-11897

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-30T15:16:24.143 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.7 is vulnerable to a denial of service, caused by sending a specially crafted request. A remote attacker could exploit this vulnerability to cause the server to consume memory resources.

### CVE-2026-11980

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-242` |
| Published | 2026-07-30T15:16:24.277 |

IBM Aspera Desktop App 1.0.5 through 1.0.19 can allow arbitrary code execution by loading DLL files at start-up.

### CVE-2026-16843

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-31T11:17:05.567 |

Some Hikvision Wireless Access Points are vulnerable to authenticated command execution due to insufficient input validation. Attackers with valid credentials can exploit this flaw by sending crafted packets containing malicious commands to affected devices, leading to arbitrary command execution.

### CVE-2026-63035

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-30T23:16:52.070 |

A heap use-after-free vulnerability in the TransferSubscriptions service
 in open62541 may allow an authenticated attacker to cause a denial of 
service or potentially execute arbitrary code.

### CVE-2026-55502

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-31T04:17:23.563 |

Cloudreve is a self-hosted file management and sharing system. Prior to 4.17.0, POST /api/v4/admin/policy/oauth/signin requires only Admin.Read even though GetOauthRedirectService persists caller-supplied OneDrive secret and app_id values, allowing an OAuth token without Admin.Write to modify storage policy credentials. The route is inside the admin group that requires Admin.Read, but it does not add the local Admin.Write guard used by sibling policy mutation routes. Its handler persists attacker-supplied secret and app_id values into the selected OneDrive storage policy before returning an OAuth URL. This issue is fixed in version 4.17.0.

### CVE-2026-66720

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-30T23:16:53.830 |

The GOOSE subscriber component improperly validates the UTC timestamp 
field in unauthenticated IEC 61850 GOOSE (EtherType 0x88B8) Layer-2 
multicast messages. A specially crafted GOOSE frame containing an 
undersized timestamp field can trigger a heap out-of-bounds read during 
message processing, causing the process to crash and resulting in a 
denial-of-service condition.

### CVE-2026-66369

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-30T23:16:53.377 |

The GOOSE parser contains an off-by-one boundary-handling flaw that can 
be triggered by a single unauthenticated Layer-2 multicast frame on the 
process bus. When specific GOOSE message fields are processed, the 
parser advances its internal buffer position incorrectly, resulting in a
 heap out-of-bounds read. On affected platforms, this condition reliably
 terminates the subscriber process and causes a denial-of-service.

### CVE-2026-66364

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-30T23:16:53.223 |

The GOOSE payload parser contains a boundary handling flaw that can be 
triggered by a single unauthenticated Layer 2 multicast frame on the 
process bus. When processing specific payload fields, an attacker 
controlled inner element length may exceed its enclosing length, causing
 the parser to over read by one byte. This out-of-bounds read reliably 
terminates the subscriber process, resulting in a denial-of-service 
condition.

### CVE-2026-65421

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-30T23:16:52.597 |

The MMS BER decoder contains a flaw in decoding fixed-width BER fields 
(boolean/integer): an attacker-supplied length value is not validated, 
causing a read past the end of a heap buffer. This leads to termination 
of the MMS service process and a denial-of-service condition.

### CVE-2026-63550

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-30T23:16:52.443 |

The MMS BER decoder contains a boundary-handling flaw in the processing 
of certain fields within confirmed-request messages. When a crafted 
BER-encoded element is received over an established MMS session (TCP 
port 102), the decoder may advance its internal read position 
incorrectly, leading to a heap out-of-bounds read. This condition causes
 the MMS handling process to terminate unexpectedly, resulting in a 
denial-of-service.

### CVE-2026-64816

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-30T22:16:55.920 |

RapidRAW before 1.6.0 does not validate the lutPath field in preset files before passing it to File::open() in lut_processing.rs. On Windows, a UNC path in lutPath causes an outbound SMB connection to an attacker-controlled host, leaking the victim's NTLMv2 credentials. The vulnerable code path is reachable through two vectors: community presets fetched automatically from the remote preset repository when the victim opens the Community tab, and individual preset files imported directly by the victim via the preset import feature (handle_import_presets_from_file in file_management.rs). The second vector does not require control of the community preset repository and is triggered when a user imports a preset file shared through Discord, forums, or similar channels.

### CVE-2026-54715

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-07-30T21:17:49.323 |

GoAccess is a real-time web log analyzer and interactive viewer that runs in a terminal in *nix systems or through the browser. In version 1.10.2, parse_browser assumes the matched browser token begins with Opera and moves a trailing version substring to match plus five, allowing a crafted User-Agent in a processed access log to write one to four attacker-influenced bytes beyond the heap allocation and corrupt or crash GoAccess. This issue is fixed in version 1.11.

### CVE-2026-12945

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-30T17:16:28.173 |

IBM Langflow OSS 1.0.0 through 1.10.1 allows authenticated users to access and manipulate other users' build jobs through improper access control on log retrieval and unauthenticated build endpoints.

### CVE-2026-12932

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-07-30T17:16:27.920 |

A memory leak in the tls-crypt-v2 client key extraction in OpenVPN 2.5.0 through 2.6.20 and 2.7_alpha1 through 2.7.4 allows remote attackers to cause a denial of service (memory exhaustion) via a flood of crafted packets

### CVE-2026-11771

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-193;CWE-787` |
| Published | 2026-07-30T17:16:27.610 |

OpenVPN version 2.1.0 through 2.6.20 and 2.7_alpha1 through 2.7.4 allows attackers via an off-by-one buffer write in the NTLM proxy authentication to potentially cause a crash via a crafted NTLM response from a malicious proxy server
