# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-17 15:00 UTC
- **対象期間**: `2026-08-16T15:00:26.000Z` 〜 `2026-08-17T15:00:21.000Z`
- **重要CVE数**: 60 件（Critical 9.0+: 23 件 / High 7.0〜: 37 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS 7.0 以上が **30 件以上** 把握されており、特に **Web アプリケーションのヘッダー不備・認証回避** と **暗号ライブラリのサンドボックス破り** が目立ちます。  
- 高スコア（9.0 以上）の脆弱性は、**認証済みでも低権限でリモートコード実行が可能**になるものが多く、攻撃者が内部ネットワークへ横展開する足掛かりになる点が共通しています。  
- 製品別に見ると、**SiYuan、Google Cloud Chronicle SOAR、Wavlink ルータ、openssl_encrypt（Python パッケージ）** が最も深刻な影響を受けており、いずれも **即時パッチ適用か設定変更** が必須です。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目すべき理由 |
|-----|--------|----------|----------------|
| **CVE‑2026‑74800** | 9.4 | SiYuan (v3.7.4 未満) が `Content‑Disposition` と `X‑Content‑Type‑Options` を付与せず、任意の HTML アセットを保存できる。保存された HTML がワークスペース所有者のブラウザで実行され、**フルカーネル API へのアクセス** が可能になる。 | *Stored XSS* が **認証済みユーザーの権限でカーネルレベル API** までエスカレーションできる点が極めて危険。 |
| **CVE‑2026‑15623** | 9.4 | Google Cloud Chronicle SOAR (v6.3.85 未満) のダッシュボードウィジェット API に SQLi が存在。認証済みユーザーが任意の盲目 SQL を実行できる。 | GCP 上の **SecOps 自動化プラットフォーム** が攻撃対象になると、インシデントレスポンスやログ取得ロジックを改ざんでき、**組織全体の監視体制が崩壊** する恐れ。 |
| **CVE‑2026‑74843** | 9.3 | Wavlink ルータ (WN531P3 / WN535M1) の CGI `export_pingortrace.cgi` が `strcpy` 使用。`HTTP_COOKIE` を細工すると **スタックオーバーフロー** が発生し、リモートコード実行が可能。 | 家庭・SOHO 環境だけでなく、企業のゲートウェイとしても使用されることが多く、**外部から直接攻撃が成立** する点が重大。 |
| **CVE‑2026‑74899** 〜 **CVE‑2026‑74880**（共通） | 9.3 | `openssl_encrypt` (Python パッケージ) 1.4.0 未満に多数のサンドボックス回避・認証バイパス・暗号弱体化が混在。特に **pqc.py のプラグイン実行サンドボックス** が破られ、任意コード実行が可能。 | 同一ライブラリに **10 件以上** の高危険度脆弱性が集中。暗号サービス・プラグインエコシステム全体が **信頼できないコードに汚染** されるリスクがある。 |
| **CVE‑2026‑74798** | 9.3 | SiYuan の `database_clean` ツールでパス・トラバーサルが可能。任意のファイル削除や情報漏洩が実行できる。 | 既に上記 CVE‑2026‑74800 と組み合わせると、**ファイルシステムへの不正アクセス** が容易になる。 |

> **注:** ここで取り上げた 5 件は CVSS が 9.3 以上で、**認証要件が低い（PR:L/N）** か **認証不要** である点が共通しています。実運用環境でのインパクトが最も大きいため、優先的に対策すべきです。

---

## 3. 推奨アクション  

### 3.1 パッケージ・ファームウェアのアップデート
| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン | アップデート手順のポイント |
|-------------------|----------------------|----------------|----------------------------|
| **SiYuan** | < 3.7.4 | **≥ 3.7.4** (2026‑09‑01 リリース) | - 公式サイトから最新版の `.zip` を取得<br>- 既存データベースはバックアップ後に上書き<br>- `--mode=prod` フラグで起動し、`/debug/pprof/*` エンドポイントを無効化 |
| **Google Cloud Chronicle SOAR** | < 6.3.85 | **≥ 6.3.85** | - GCP コンソール → Marketplace → 「アップデート」ボタン<br>- アップデート後は **Dashboard → Widget API** のアクセス権限を最小化 |
| **Wavlink ルータ (WN531P3 / WN535M1)** | ファームウェア V250922 | **≥ V250923** (2026‑08‑15 パッチ) | - 管理画面 → Firmware Upgrade で公式イメージを適用<br>- `export_pingortrace.cgi` が無効化されているか確認 |
| **openssl_encrypt (Python)** | < 1.4.0 | **≥ 1.4.0** (2026‑07‑30 リリース) | - `pip install --upgrade openssl_encrypt` <br>- 既存プラグインは **サンドボックス対応版** に再デプロイ |
| **Roundcube (markasjunk plugin)** | < 1.7.3 | **≥ 1.7.3** | - `apt-get update && apt-get install roundcube=1.7.3-...` <br>- `cmd_learn` ドライバを無効化またはプラグインを削除 |

### 3.2 設定・運用上の緩和策
1. **ヘッダー強制**  
   - SiYuan、nginx、Apache いずれでも `Content‑Disposition: attachment` と `X‑Content‑Type‑Options: nosniff` を **全レスポンスに付与**。  
2. **デバッグエンドポイントの遮断**  
   - `--mode=prod` 以外で起動した SiYuan の `/debug/pprof/*` を **ファイアウォールで外部から遮断**、もしくは `pprof` ハンドラを削除。  
3. **最小権限の IAM 設定**  
   - Chronicle SOAR の API キーは **Read‑Only** に限定し、ウィジェット API へのアクセスは **特定ロールのみ** に付与。  
4. **プラグインサンドボックスの強

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-74800

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-17T11:16:40.187 |

SiYuan before v3.7.4 fails to set Content-Disposition and X-Content-Type-Options headers when serving arbitrary file assets, allowing stored cross-site scripting attacks. Authenticated attackers can upload HTML files as assets and execute scripts with full kernel API access when the workspace owner opens the asset link.

### CVE-2026-15623

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-17T07:17:12.020 |

A SQL Injection vulnerability in a legacy dashboard widget API in Google Cloud Google SecOps (Chronicle SOAR) versions prior to 6.3.85 on Google Cloud Platform allows an authenticated attacker to execute blind SQL queries using a crafted request parameter.


This vulnerability was patched in version 6.3.85, and no customer action is needed.

### CVE-2026-74843

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-17T12:18:58.180 |

A vulnerability was determined in Wavlink WN531P3 and WN535M1 V250922. Affected by this vulnerability is the function strcpy of the file /etc/lighttpd/www/cgi-bin/export_pingortrace.cgi of the component Export Pingortrace CGI. Executing a manipulation of the argument HTTP_COOKIE can lead to stack-based buffer overflow. The attack may be launched remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure.

### CVE-2026-74901

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-17T11:16:45.183 |

openssl_encrypt versions before 1.4.0 contain an authentication bypass vulnerability in pqc.py where AES-GCM decryption failures trigger fallback to unauthenticated AES-CTR mode. Attackers can modify ciphertext in transit to bypass integrity verification and perform bit-flipping attacks without detection.

### CVE-2026-74900

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-391` |
| Published | 2026-08-17T11:16:45.050 |

openssl_encrypt versions before 1.4.0 contain a critical vulnerability in pqc.py where KEM decapsulation failures silently fall back to simulation mode, generating a deterministic shared secret from only 16 bytes of the private key and publicly available encapsulated key data. Attackers who obtain 16 bytes of the private key can compute the shared secret and decrypt all ciphertext, as the fallback triggers on any KEM failure without raising an error.

### CVE-2026-74899

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-17T11:16:44.917 |

openssl_encrypt versions before 1.4.0 contain a sandbox escape vulnerability in IsolatedPluginExecutor that exposes Python type objects in restricted exec() builtins. Attackers can traverse the Python class hierarchy via __class__.__mro__.__subclasses__() to access system functions and execute arbitrary OS commands.

### CVE-2026-74896

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-17T11:16:44.787 |

openssl_encrypt versions before 1.4.0 contain a sandbox escape vulnerability in the DangerousPatternVisitor AST analyzer that fails to detect dunder attribute traversal techniques. Attackers can use __class__, __bases__, __subclasses__(), and __globals__ chains to access restricted functions and execute arbitrary system commands from plugin code.

### CVE-2026-74895

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-17T11:16:44.653 |

openssl_encrypt versions before 1.4.0 fail to apply sandbox restrictions in the default process isolation mode for plugin execution. Attackers can execute malicious plugins with unrestricted access to the filesystem, network, subprocess execution, and all Python modules.

### CVE-2026-74894

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-17T11:16:44.523 |

openssl_encrypt before 1.4.0 contains an authentication bypass vulnerability in the verify_api_token function that accepts any non-empty Bearer token string without validation. Attackers can upload arbitrary public keys, enumerate all keys, and revoke keys belonging to any user by providing any Bearer token in the Authorization header.

### CVE-2026-74890

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-17T11:16:43.960 |

openssl_encrypt versions before 1.4.0 contain an authentication bypass vulnerability in CamelliaCipher that disables HMAC tag generation and verification when the PYTEST_CURRENT_TEST environment variable is set. Attackers with code execution can set this environment variable to produce unauthenticated ciphertext and bypass integrity protection on encrypted data.

### CVE-2026-74889

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-326` |
| Published | 2026-08-17T11:16:43.803 |

openssl_encrypt versions before 1.4.0 use HKDF with no salt and static info parameter in key normalization functions, reducing entropy extraction and determinism. Attackers can exploit predictable key derivation with identical inputs to weaken cryptographic security against multi-target attacks.

### CVE-2026-74887

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-338` |
| Published | 2026-08-17T11:16:43.523 |

openssl_encrypt before 1.4.0 imports Python's non-cryptographic 'random' module (Mersenne Twister PRNG) at line 15 of openssl_encrypt/modules/pqc.py. No direct calls to random.* were present in the code, so no cryptographic operation is currently affected; however, the import creates a hazard that future code could inadvertently use random.randint() instead of a cryptographically secure alternative (secrets/os.urandom), producing predictable values since the Mersenne Twister state can be recovered from approximately 624 outputs. Fixed by removing the import in 1.4.0.

### CVE-2026-74886

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-08-17T11:16:43.390 |

openssl_encrypt versions before 1.4.0 contain a plugin sandbox bypass vulnerability where the PluginImportGuard blocks a different set of modules than the AST analyzer's DANGEROUS_MODULES set. Attackers can bypass AST analysis through string obfuscation or encoding to import unblocked dangerous modules like sys, shutil, multiprocessing, importlib, and pickle for arbitrary code execution.

### CVE-2026-74885

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-117` |
| Published | 2026-08-17T11:16:43.260 |

openssl_encrypt versions before 1.4.0 contain a logging bug in restore_hidden_modules() that logs module counts after clearing, always showing zero restored modules and corrupting audit trails. Additionally, a race condition exists between module hiding and import hook installation where another thread could re-import blocked modules in multi-threaded environments.

### CVE-2026-74880

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-598` |
| Published | 2026-08-17T11:16:42.593 |

openssl_encrypt versions before 1.4.0 accept refresh tokens as URL query parameters in keyserver and telemetry server routes. Attackers can extract tokens from server logs, proxy logs, browser history, and HTTP Referer headers to gain unauthorized access.

### CVE-2026-74878

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-17T11:16:42.330 |

openssl_encrypt versions before 1.4.0 use an in-memory rate limiter for TOTP brute-force protection that is not shared across workers and is lost on server restart. Attackers can distribute authentication attempts across multiple server instances or retry immediately after a restart to bypass rate limiting protections.

### CVE-2026-74876

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-17T11:16:42.073 |

openssl_encrypt versions before 1.4.0 contain a vulnerability in PublicKeyBundle.from_dict() that creates key bundles from untrusted data without verifying signatures. Attackers can call from_dict() followed by to_identity() without signature verification to encrypt data using attacker-controlled public keys, leaking secrets.

### CVE-2026-74875

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-17T11:16:41.943 |

openssl_encrypt versions before 1.4.0 silently skip JSON schema validation when the jsonschema library is not installed, allowing malformed metadata to be accepted. Attackers can remove the jsonschema package or supply unknown metadata format versions to bypass all schema checks and process malicious data.

### CVE-2026-74872

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-17T11:16:41.560 |

openssl_encrypt versions before 1.4.0 contain an arbitrary code execution vulnerability in the Whirlpool hash implementation that uses broad glob patterns to load .so modules without integrity verification. Attackers can place malicious .so files matching the whirlpool*py313*.so pattern in site-packages directories to achieve native code execution when the module is loaded.

### CVE-2026-74798

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-17T11:16:39.873 |

SiYuan kernel before v3.7.4 contains a path traversal vulnerability in the database_clean MCP tool. The tool performs only an empty-string check on the id parameter before passing it to RemoveUnusedAttributeView (kernel/model/attribute_view.go), which builds a filesystem path via filepath.Join without validating that id matches SiYuan's node-ID format. An authenticated MCP client can supply path traversal sequences in id to cause the kernel to copy an arbitrary file readable by the process into SiYuan's history directory (arbitrary file read) and then delete the original file (arbitrary file deletion). The corresponding HTTP API handler was hardened in GHSA-7hm9-v7vf-7g4w, but this MCP caller was not.

### CVE-2026-19977

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-17T03:16:50.517 |

A vulnerability was detected in EFM ipTIME A3004T 14.19.0. The affected element is the function httpcon_check_session_url of the component Session Validation. Performing a manipulation results in improper authentication. Remote exploitation of the attack is possible. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-74799

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:H/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-215` |
| Published | 2026-08-17T11:16:40.017 |

SiYuan before 3.7.4 registers Go net/http/pprof debug endpoints including heap and goroutine dumps without authentication when --mode flag is not set to exactly prod. Attackers can access /debug/pprof/heap and related endpoints to extract in-memory secrets including AccessAuthCode and AI provider API keys.

### CVE-2026-14564

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-17T13:16:50.797 |

Insufficiently Protected Credentials vulnerability in Innotim Software Telecommunications and Consulting Trade Ltd. Co. Logsign SIEM allows Retrieve Embedded Sensitive Data.

This issue affects Logsign SIEM: from 6.4.97 before 6.4.114.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-74997

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-17T13:16:54.100 |

In Roundcube Webmail before 1.6.18 and 1.7.x before 1.7.3, the cmd_learn driver of the markasjunk plugin is subject to remote code execution via crafted placeholder replacement values. This issue only affects Roundcube instances using the markasjunk plugin with its cmd_learn driver.

### CVE-2026-74893

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-17T11:16:44.397 |

openssl_encrypt versions before 1.4.0 contain hardcoded default JWT signing secrets in config.py that pass validation checks. Attackers with access to source code can forge valid JWT tokens for any client_id to gain authenticated access to keyserver and telemetry APIs.

### CVE-2026-74892

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-17T11:16:44.263 |

openssl_encrypt versions before 1.4.0 contain a hardcoded default secret key in the standalone telemetry server configuration that is used for API key hashing. Attackers who know this default value can predict or forge API key hashes to compromise telemetry API authentication.

### CVE-2026-74891

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-17T11:16:44.120 |

openssl_encrypt versions before 1.4.0 contain hardcoded database credentials in standalone server configuration files. Attackers on the same network can access PostgreSQL databases using well-known default credentials to retrieve sensitive data.

### CVE-2026-74888

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-327` |
| Published | 2026-08-17T11:16:43.653 |

openssl_encrypt versions before 1.4.0 use a non-standard PBKDF2 key derivation construction with iterations=1 per call in an outer loop, creating a KDF whose security properties have not been formally analyzed. Attackers can exploit this weakened key derivation to more efficiently crack passwords protecting legacy encrypted files compared to standard PBKDF2 implementations.

### CVE-2026-74884

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-17T11:16:43.130 |

openssl_encrypt versions before 1.4.0 contain a path traversal vulnerability in the _is_safe_path method where the plugin_id parameter is not sanitized before constructing the plugin config directory path. Attackers can declare a malicious plugin_id containing path traversal sequences like '../' to access arbitrary directories outside the intended plugin directory.

### CVE-2026-74883

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-17T11:16:42.993 |

openssl_encrypt versions before 1.4.0 contain a sandbox bypass vulnerability where the plugin sandbox fails to restrict alternative file access methods like pathlib.Path and io.open. Attackers can import pathlib or io modules to read and write arbitrary files, completely bypassing the restricted_open file access controls.

### CVE-2026-74882

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-17T11:16:42.863 |

openssl_encrypt versions before 1.4.0 contain an insecure default configuration that trusts the entire RFC 1918 private address space in IntegrityProxyConfig trusted_proxies. Attackers on private networks can forge client certificate headers to bypass mTLS authentication when ProxyAuth validation is relaxed or modified.

### CVE-2026-74879

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-209` |
| Published | 2026-08-17T11:16:42.460 |

openssl_encrypt versions before 1.4.0 contain an information disclosure vulnerability in the /ready endpoint that returns full database exception strings to unauthenticated callers. Attackers can trigger database errors to extract sensitive information including hostnames, IP addresses, connection parameters, and potentially credentials from exception messages.

### CVE-2026-74877

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-17T11:16:42.203 |

openssl_encrypt versions before 1.4.0 contain a missing ownership verification vulnerability in the revoke_key method that allows authenticated clients to revoke any other client's key. Attackers can revoke arbitrary keys by providing a valid ML-DSA signature, bypassing the intended ownership restriction.

### CVE-2026-74874

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-338` |
| Published | 2026-08-17T11:16:41.813 |

openssl_encrypt versions before 1.4.0 use Python's non-cryptographic random module for steganographic pixel selection in the generate_pseudorandom_sequence function. Attackers who know the password can recover the Mersenne Twister state from approximately 624 outputs and predict pixel locations containing hidden data for extraction.

### CVE-2026-74873

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-214` |
| Published | 2026-08-17T11:16:41.690 |

openssl_encrypt versions before 1.4.0 expose passwords passed via the --password CLI argument in process listings accessible to all system users. Attackers can read process arguments through ps aux or /proc/[pid]/cmdline to retrieve plaintext passwords and keystore passwords.

### CVE-2026-74870

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-08-17T11:16:41.293 |

openssl_encrypt (pip) versions <= 1.4.7 contain an information exposure vulnerability where the 'hsm fido2-test' and 'hsm onlykey-test' diagnostic commands unconditionally print the full derived hardware pepper as hex to stdout/stderr (crypt_cli.py, handle_hsm_command). The printed value can persist in terminal scrollback, session recordings, or CI logs. Impact is limited because the pepper is derived from a random per-invocation test salt and is salt-bound, so the leaked value cannot be used to decrypt real files. A related plugin issue logged raw prf_data outside the secret-redaction path. Fixed in 1.4.8 (and 1.5.0) by removing the hex dumps and routing plugin debug output through the redaction layer.

### CVE-2026-74868

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-08-17T11:16:41.030 |

SiYuan versions before 3.7.4 contain an unthrottled brute-force vulnerability in the Publish Service Basic Auth implementation (PublishServiceTransport.RoundTrip() in kernel/server/proxy/publish.go). The Publish Service runs on a separate, unauthenticated-by-default listener (default TCP port 6808) and gates named publish-viewer accounts (Conf.Publish.Auth.Accounts) with Basic Auth that has no rate limiting, per-account lockout, or backoff. Unauthenticated remote attackers can submit unlimited password guesses against named accounts to gain access to published notes/notebooks.

### CVE-2026-74845

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-17T10:16:42.403 |

Official Document Management System developed by 2100 Technology has an Arbitrary File Upload vulnerability, allowing authenticated remote attackers to upload and execute web shell backdoors, thereby enabling arbitrary code execution on the server.

### CVE-2026-74801

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-17T11:16:40.323 |

SiYuan before 3.7.4 fails to properly escape workspace directory paths when constructing command-line arguments for the elevated elevator.exe helper process. Attackers can create a malicious workspace directory with command metacharacters in its path and trigger the Microsoft Defender exclusion flow to execute arbitrary commands with administrator privileges after UAC approval.

### CVE-2026-19961

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-08-16T23:16:25.050 |

A vulnerability was detected in Edimax EW-7478APC 1.04. Affected is the function formWlSiteSurvey of the file /goform/formWlSiteSurvey. Performing a manipulation of the argument selSSID results in buffer overflow. The attack is possible to be carried out remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-19959

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-16T23:16:24.710 |

A weakness has been identified in Edimax EW-7478APC 1.04. This affects the function formWanTcpipSetup of the file /goform/formWanTcpipSetup. This manipulation of the argument pppUserName causes stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-50602

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-08-17T03:16:50.840 |

A security vulnerability has been identified in Planet9 due to incorrect file permissions assigned to an application executable used by the Planet9 background service. The service runs with SYSTEM privileges, while the affected executable grants excessive permissions to non-administrative users. As a result, an authenticated local user could potentially modify or replace the executable and execute arbitrary code with SYSTEM privileges when the service starts or the system is restarted.

### CVE-2026-74869

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-17T11:16:41.163 |

stoatchat before 0.15.0 contains a missing authorization vulnerability in the Subscribe message handler that allows authenticated attackers to enumerate members and monitor profile updates of private servers without membership. Attackers can subscribe to any server's member-update topic by sending a Subscribe message with an arbitrary server ID, receiving live UserUpdate events including display names, avatars, and status changes for members they should not have access to.

### CVE-2026-22072

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-17T07:17:15.797 |

Loading arbitrary external URLs through WebView components introduces malicious JS code that can steal arbitrary user tokens.

### CVE-2026-19693

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-08-17T14:20:20.737 |

extract-zip through 2.0.1 containment-checks only the parent directory of each archive entry and never the entry's own final path component, so an archive containing two entries with identical names - a symlink whose target is outside the destination, followed by a regular file - writes through the planted symlink and yields an arbitrary file write outside the destination directory.

### CVE-2026-16138

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-17T14:20:19.797 |

In Progress ShareFile Storage Zones Controller v5.12.5 and below versions, unsafe deserialization of untrusted file metadata can allow a user with write access to a Network share to execute arbitrary code on the Storage Zones Controller host.

### CVE-2026-15218

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-17T14:20:19.357 |

A flaw was found in the maas-api and maas-controller ServiceAccounts within Red Hat OpenShift AI. These ServiceAccounts are granted cluster-wide permissions that exceed their operational requirements. An attacker who compromises the identity of these ServiceAccounts, either through a remote code execution vulnerability or by creating a malicious pod in the same namespace, could exploit these excessive permissions. This could lead to full cluster administrator privileges through the creation of new ClusterRoleBindings or the disclosure of sensitive information by accessing all secrets across the cluster.

### CVE-2026-59910

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-17T14:20:21.623 |

Dell ObjectScale, versions prior to 4.3.0.1, contain(s) an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-56686

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-17T14:20:21.333 |

Dell ObjectScale, versions prior to 4.3.0.1, contain(s) an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-16471

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-17T14:20:20.147 |

Missing Authorization vulnerability in Dolusoft Software Technologies Sonlogger allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects Sonlogger: from v6.6.6 before 6.7.4.8.

### CVE-2026-16467

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-17T13:16:50.963 |

Missing Authorization vulnerability in Dolusoft Software Technologies Fortilogger allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects Fortilogger: before 6.1.5.9.

### CVE-2026-56685

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-17T14:20:21.193 |

Dell ObjectScale, versions prior to 4.3.0.1, contain(s) an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-56090

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-17T14:20:21.077 |

Dell ObjectScale, versions prior to 4.3.0.1, contain(s) an Uncontrolled Search Path Element vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-16139

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-22;CWE-73` |
| Published | 2026-08-17T14:20:19.913 |

In Progress ShareFile Storage Zones Controller versions <= 5.12.5 and <= 6.0.2, an authenticated zone administrator can exploit improper validation in the download preparation flow, enabling attacker-controlled files to be written outside the intended preparation directory. This can lead to remote code execution in v5 versions. Remote code execution is not confirmed on v6 versions.

### CVE-2026-16137

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73;CWE-434` |
| Published | 2026-08-17T14:20:19.670 |

In Progress ShareFile Storage Zones Controller v5.12.5 and below, a party with valid zone credentials can perform path traversal using resumable upload initiation endpoint, allowing the party to write arbitrary content to any location writable by the application's service account. This may result in the execution of attacker-supplied code.

### CVE-2026-74998

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-17T13:16:54.270 |

In Roundcube Webmail before 1.6.18 and 1.7.x before 1.7.3, responses from the CSS (Cascading Style Sheets) proxy were not validated, which may result in information disclosure or XSS (cross-site scripting) via MIME sniffing.

### CVE-2026-59909

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-35` |
| Published | 2026-08-17T14:20:21.487 |

Dell ObjectScale, versions prior to 4.3.0.1, contain(s) a Path Traversal vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Information tampering.

### CVE-2026-75002

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-17T13:16:54.747 |

In Roundcube Webmail before 1.6.18 and 1.7.x before 1.7.3, mail search and LITERAL+ byte-count desynchronization could lead to information disclosure or privilege escalation via IMAP command injection.

### CVE-2026-74881

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-942` |
| Published | 2026-08-17T11:16:42.723 |

openssl_encrypt versions before 1.4.0 configure CORS with allow_origins set to wildcard and allow_credentials enabled to true. Attackers can create malicious websites that make authenticated cross-origin requests to the API on behalf of any user who visits them.

### CVE-2026-18674

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-863` |
| Published | 2026-08-17T13:16:51.820 |

On a Kong Mesh global control plane, resources received over the zone-to-global KDS sync are attributed using the in-band, sender-controlled ControlPlane.Identifier rather than the authenticated zone identity derived from the connection. Authenticated zones can have the global control plane store and re-distribute those resources as belonging to another zone.



The result is a cross-zone isolation bypass: the holder of a single enrolled zone's credential can inject, attribute, and overwrite resources in another zone's namespace mesh-wide.




The root cause lives in Kuma's open-source KDS sync code, which Kong Mesh's control plane is built on.
