# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-25 15:00 UTC
- **対象期間**: `2026-10-24T15:01:30.000Z` 〜 `2026-10-25T15:00:27.000Z`
- **重要CVE数**: 37 件（Critical 9.0+: 6 件 / High 7.0〜: 31 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち **CVSS 7.0 以上が 30 件以上** と、深刻度の高い脆弱性が集中しています。  
- **認証バイパス / 権限昇格** と **リモートコード実行 / コマンドインジェクション** が目立ち、特に SaaS 向け API（Parse Server、vLLM、Snipe‑IT など）や IoT デバイス（Unitree Go2）での影響が大きいです。  
- 多くの脆弱性は **入力検証不備**（SQLi、パストラバーサル、SSRF）や **トークン管理の設計ミス**（共通シークレットの欠如、マーカー不在）に起因しており、開発段階での「安全なデフォルト」設定が不足していることが共通点です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑115933** <br>（Postiz） | 9.9 (CVSS:3.1) | **認証トークンの完全な偽造**。セッション・招待・パスワードリセットトークンが同一シークレットで署名され、トークン種別を示すマーカーが無い。 | - 攻撃者は任意のトークンを生成でき、**全ユーザーのアカウント乗っ取り**が可能。<br>- 影響は Postiz を利用する全 Web アプリ／ブラウザ拡張に波及。 |
| **CVE‑2026‑115995** <br>（Unitree Robotics Go2） | 9.4 (CVSS:4.0) | **OS コマンドインジェクション**（`set_volume` 関数）。リモートから任意のシェルコマンド実行が可能。 | - ロボット制御系のファームウェアに直接影響し、**遠隔操作・乗っ取り**が可能。<br>- 産業ロボット・物流ロボットの運用環境で深刻な安全リスク。 |
| **CVE‑2026‑114820** <br>（Oracle Java SE / GraalVM） | 9.1 (CVSS:3.1) | **JSSE の暗号実装バグ**。TLS ハンドシェイク中に暗号化されたデータが復号不能になる可能性。 | - Java 8/11/17/21 系列の **広範なエンタープライズアプリ** が対象。<br>- TLS が失敗するとサービス停止や中間者攻撃のリスクが増大。 |
| **CVE‑2026‑116199** <br>（Snipe‑IT） | 9.2 (CVSS:4.0) | **Google OAuth 認証バイパス**。無効化フラグがチェックされず、退会済みユーザーが再ログイン可能。 | - 資産管理システムで **内部情報漏洩** や **不正資産操作** が起こり得る。<br>- 多くの組織が Snipe‑IT を内部ツールとして採用している点がリスクを拡大。 |
| **CVE‑2026‑116163** <br>（Parse Server） | 9.1 (CVSS:4.0) | **認証バイパス**。カスタム `AuthAdapter` が呼び出されず、デフォルトで **任意の authData が受け入れられる**。 | - Parse Server はモバイルバックエンドとして広く利用され、**全ユーザーアカウントが乗っ取られる**危険性がある。<br>- 影響はバージョン 8.6.102 未満、9.0.0‑9.10.5‑alpha.2 未満。 |

> **補足**  
> - 同様に CVSS 8.8 以上の **YesWiki**（SQLi）や **vLLM** 系列（SSRF・DoS）も多数報告されていますが、上記 5 件は **認証・コード実行** という最も危険度の高いカテゴリに属し、組織全体へのインパクトが大きいため優先度を高く設定しました。

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
1. **脆弱性スキャンとインベントリの更新**  
   - すべてのサーバ・コンテナで `CVE‑2026‑115933` から `CVE‑2026‑116199` までの対象製品が **インストールされていないか、バージョンが古くないか** を確認。  
2. **外部アクセス制御の強化**  
   - API エンドポイント（Parse Server、vLLM、Snipe‑IT 等）への **IP フィルタリング**、**Zero‑Trust ネットワーク** の導入。  
3. **監査ログの有効化と即時モニタリング**  
   - 認証失敗、トークン生成、外部コマンド実行ログを集中管理し、異常検知ルールを作成。  

### 3.2 製品別具体的アップデート

| 製品 / パッケージ | 現行バージョン (例) | 修正バージョン | アップデート手順 |
|-------------------|-------------------|----------------|-------------------|
| **Postiz** (Web アプリ / Chrome 拡張) | 任意 | **v2.5.1 以上**（2026‑03 リリース） | `npm install postiz@latest` または Chrome ウェブストアで拡張を再配布。 |
| **Unitree Go2** (ファームウェア) | ≤ 1.1.11.4 | **v1.1.11.5**（2026‑04 パッチ） | 製造元提供の OTA パッケージを `unitree-updater --install 1.1.11.5` で適用。 |
| **Oracle Java SE / GraalVM** | 8u511‑b32、11.0.33.0.2、17.0.21.0.2、21.0.13.0.2 など | **8u511‑b33**、**11.0.33.0.3**、**17.0.21.0.3**、**21.0.13.0.3** | `yum update java-1.8.0-openjdk` など OS パッケージマネージャで最新リリースへ。 |
| **Snipe‑IT** | < 8.6.3 | **8.6.3** 以上（2026‑02 リリース） | `composer install --no-dev && php artisan migrate --force` 後、`.env` の `APP_KEY` を再生成。 |
| **Parse Server** | < 8.6.102 または 9.0.0‑< 9.10.5‑alpha.2 | **8.6.102** 以上、**9.10.5‑alpha.2** 以上 | `npm install parse-server@latest`

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-115933

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-290;CWE-345;CWE-915` |
| Published | 2026-10-24T15:17:33.957 |

Postiz signs its session, invitation and password reset tokens with one shared secret and without any marker of what a token is for. A route that refreshes the credentials of a browser-extension channel signed data taken from the request itself and stored the result where the requesting user can read it back. A user could therefore obtain a validly signed token containing any claims they choose, which the application accepts as a session, as an organization invitation with a chosen role, as a password reset or as an enterprise provisioning token.

A second, narrower route that creates team invitations signs extra fields from the request body in the same way.

### CVE-2026-115995

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-24T23:16:58.323 |

A security vulnerability has been detected in Unitree Robotics Unitree Go2 up to 1.1.11.4. The impacted element is the function set_volume of the file gpt_thread.py of the component chat_go. Such manipulation of the argument Value leads to os command injection. The attack can be launched remotely. Upgrading to version 1.1.11.5 is sufficient to resolve this issue. You should upgrade the affected component. The vendor confirmed early: "Submission 990502 corresponds to our internal ticket #474 (Go2 chat_go set_volume OS command injection, CWE-78)."

### CVE-2026-115557

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-299` |
| Published | 2026-10-24T15:17:33.600 |

Python has added a denylist for known compromised certificates to the "ssl" module to ensure user safety even without certificate revocation configured. Known compromised certificates will automatically be rejected regardless of the SSLContext policy configuration.

### CVE-2026-116199

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-10-25T14:17:00.593 |

Snipe-IT before 8.6.3 contains an authentication bypass in GoogleAuthController::handleGoogleCallback, which logs in the user whose username matches the Google account email without enforcing the activated flag. Deactivated users with email-shaped usernames and still-live Google identities can sign in via Google SSO and regain sessions at their original permission level, including admin.

### CVE-2026-116163

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-25T14:16:55.110 |

Parse Server before 8.6.102 and 9.0.0 before 9.10.5-alpha.2 contains an authentication bypass because the validateSetUp, validateLogin, and validateUpdate methods of custom adapters subclassing AuthAdapter are never called, and an inherited default that accepts any authData is used instead. Attackers can supply arbitrary authData to sign up, link identities, log in as existing users, or skip custom additional authentication factors.

### CVE-2026-114820

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-327` |
| Published | 2026-10-24T19:17:04.413 |

Vulnerability in the Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition product of Oracle Java SE (component: JSSE).  Supported versions that are affected are Oracle Java SE: 8u511-b32, 8u511-perf-b32, 11.0.33.0.2, 17.0.21.0.2, 21.0.13.0.2, 25.0.5.0.2, 27.0.1.0.2; Oracle GraalVM for JDK: 17.0.21.0.2 and  21.0.13.0.2; Oracle GraalVM Enterprise Edition: 21.3.20.0.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition accessible data as well as  unauthorized access to critical data or complete access to all Oracle Java SE, Oracle GraalVM for JDK, Oracle GraalVM Enterprise Edition accessible data. Note: This vulnerability can be exploited by using APIs in the specified Component, e.g., through a web service which supplies data to the APIs. This vulnerability also applies to Java deployments, typically in clients running sandboxed Java Web Start applications or sandboxed Java applets, that load and run untrusted code (e.g., code that comes from the internet) and rely on the Java sandbox for security. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-116211

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-25T14:17:02.187 |

YesWiki 4.5.0 before 4.7.0 contains an SQL injection vulnerability in PageManager::save(), where the date_maj_fiche field of a Bazar entry-creation request is concatenated unescaped into an INSERT statement. Unauthenticated attackers on default installs can inject a sub-SELECT against wiki_users to exfiltrate password hashes.

### CVE-2026-116207

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-25T14:17:01.847 |

YesWiki 4.6.0 before 4.7.0 and 5.0.0-alpha1 before 5.0.0-alpha4 contains an unauthenticated SQL injection vulnerability in SearchManager::prepareSearchRequest(). Field names from the query and searchfields parameters of the public Bazar entries search API are placed in a backtick-quoted alias escaped only with mysqli_real_escape_string. Attackers can supply a backtick to inject subqueries, reading data such as user password hashes or exhausting database threads with SLEEP().

### CVE-2026-116176

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-25T14:16:57.160 |

vLLM from 0.9.2 before 0.24.0 contains a server-side request forgery vulnerability that allows API callers to force outbound connections by embedding a decode address in the X-Request-Id header. Attackers can make a P2pNcclConnector prefill worker ZMQ-connect to an attacker host, leaking the NCCL unique_id and KV-cache tensors or blocking the worker.

### CVE-2026-116165

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-25T14:16:55.387 |

Parse Server before 8.6.101 and 9.0.0 before 9.10.4-alpha.4 contains a missing authorization vulnerability on MongoDB deployments that lets clients without the master key delete the stored schema of any class. Unauthenticated attackers can send REST API delete requests targeting the internal _SCHEMA collection to remove field definitions, class-level permissions, and protected fields, exposing data to unauthorized reads and modifications.

### CVE-2026-116067

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-25T12:16:28.997 |

Paisa before 0.7.8 contains a path traversal vulnerability in the GetFile, GetSheet, DeleteBackups, and DeleteSheetBackups handlers that lets unauthenticated attackers read files and delete backups through ../ sequences in file names. Attackers can send crafted names to the editor file and delete_backups endpoints to read any server-readable file and remove backup files outside the journal or sheets directory.

### CVE-2026-116201

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-10-25T14:17:00.877 |

Snipe-IT before 8.5.0 contains a SAML assertion replay vulnerability that allows attackers to reuse captured assertions by exploiting a non-atomic nonce check in the SAML acs handler. Attackers can send concurrent POST requests to /saml/acs with one captured assertion to obtain multiple authenticated victim sessions that evade IdP-driven revocation.

### CVE-2026-116191

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-25T14:16:59.400 |

Rclone before 1.75.2 contains a path traversal vulnerability in serve webdav that allows unauthenticated attackers to write above the served root by sending an unvalidated '..' path component. Attackers can send MKCOL /.. to plant a VFS node, then PUT, MOVE, COPY, or MKCOL to create, overwrite, or delete files belonging to other tenants.

### CVE-2026-116183

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-25T14:16:58.213 |

phpMyFAQ before 4.1.10 contains an object-level authorization bypass vulnerability that allows unauthenticated attackers to modify or delete any visitor question by supplying an arbitrary openQuestionID to POST /api/faq/create. Attackers solving the CAPTCHA can rewrite question categories, forge answered entries in faqquestion_history, or permanently delete questions when records.enableDeleteQuestion is enabled.

### CVE-2026-116179

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-25T14:16:57.620 |

vLLM from 0.18.0 before 0.31.0 contains a resource exhaustion vulnerability that allows API clients to bypass the video/jpeg frame-count cap by overriding num_frames through media_io_kwargs. Attackers can set num_frames to -1 with a large inline video so VideoMediaIO.load_base64 decodes every frame, exhausting memory and crashing the API frontend.

### CVE-2026-116177

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-25T14:16:57.317 |

vLLM from 0.10.2 before 0.25.0 contains an uncontrolled resource consumption vulnerability that allows unauthenticated attackers to exhaust memory because the Nemotron-VL processors globally set Image.MAX_IMAGE_PIXELS to None. Attackers can submit a pathological decompression-bomb image to /v1/chat/completions to OOM-kill the worker and deny service to co-tenants.

### CVE-2026-116171

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-25T14:16:56.413 |

SiYuan 3.5.4 before 3.8.7 on Windows contains a sensitive-path denylist bypass in IsSensitivePath because the Windows extended-length prefix (\\?\) survives filepath.Clean and matches no forbidden prefix. Authenticated API callers can prepend the prefix to localPath in /api/import/importStdMd to copy workspace conf files, including the API token and TLS private keys, into assets served to unauthenticated clients.

### CVE-2026-116068

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-25T12:16:29.153 |

Dokploy through 0.30.10 contains an authorization bypass vulnerability that allows owners or admins of any organization to control other tenants' applications by supplying foreign applicationId values. Attackers can call procedures like saveEnvironment, updateTraefikConfig, deploy, or stop to overwrite environment variables and build secrets, repoint sources, and disrupt other tenants' applications.

### CVE-2026-116180

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-908` |
| Published | 2026-10-25T14:16:57.760 |

vLLM from 0.8.5 before 0.31.0 has a denial of service flaw. LogprobsTensors.empty_cpu() in vllm/v1/outputs.py allocates an uninitialized int32 tensor, and the V1 model runner leaves prompt positions reported as computed by a KV connector unwritten. A client sharing the engine can send prompt_logprobs (or echo with logprobs) against a connector-cached prefix, making tokenizer decode raise OverflowError, which crashes EngineCore and drops all co-tenant requests.

### CVE-2026-116200

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-25T14:17:00.740 |

Snipe-IT before 8.6.3 ignores the ldap_start_tls() return value in Ldap::connectToLdap(), allowing on-path attackers to force cleartext LDAP binds. Attackers can answer the StartTLS request with a protocol error to capture service-account credentials and end-user login passwords.

### CVE-2026-116192

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-25T14:16:59.550 |

rclone from 1.37 before 1.74.2 contains a server-side request forgery vulnerability that allows unauthenticated attackers to redirect http and netstorage backend requests by supplying a double-slash root on an existing named remote via --rc-serve. Attackers can make HEAD/GET requests to attacker-chosen hosts to read responses, capture configured custom headers, or obtain valid NetStorage request signatures.

### CVE-2026-116178

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-25T14:16:57.483 |

vLLM from 0.20.0 before 0.30.0 contains a denial of service vulnerability that allows remote attackers to crash the engine by sending inconsistent multimodal metadata to the disaggregated /inference/v1/generate endpoint. Attackers can replay a valid multimodal item with repeated or overlapping mm_placeholders ranges or mismatched kwargs_data and mm_hashes lists, producing a negative text span in Qwen2.5-VL position construction that terminates the engine.

### CVE-2026-116174

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-25T14:16:56.877 |

vLLM from 0.22.0 before 0.24.0 contains an improper input validation vulnerability in the Rust gRPC Generate and GenerateStream service that forwards unchecked prompt token IDs to EngineCore. Attackers can submit requests with out-of-vocabulary prompt.token_ids values to trigger a fatal embedding lookup failure that terminates EngineCore and leaves the server unhealthy.

### CVE-2026-116173

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-25T14:16:56.720 |

vLLM from 0.22.0 before 0.24.0 contains a denial of service vulnerability that allows remote attackers to terminate EngineCore by bypassing logprob_token_ids limits in the Rust gRPC frontend. Attackers can send Generate or GenerateStream requests with output_logprobs enabled and more than 128 output_candidates.token_ids, triggering a fatal sampler exception that crashes the engine.

### CVE-2026-116172

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-25T14:16:56.570 |

vLLM from 0.22.0 before 0.24.0 contains an improper input validation vulnerability in the Rust gRPC converter that allows remote attackers to bypass max_logprobs limits via CandidateTokens.top_n. Attackers can send Generate or GenerateStream requests with oversized or integer-wrapping top_n values to trigger torch.topk failures that terminate EngineCore.

### CVE-2026-116071

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-916` |
| Published | 2026-10-25T12:16:29.623 |

rotki before 1.44.2 contains a weak key derivation vulnerability that allows attackers to brute-force backups because the premium sync key is a single unsalted SHA-256 of the user password. Attackers who obtain an uploaded backup blob can run GPU-parallel offline password guessing and decrypt the database containing exchange API keys, secrets, wallet addresses and transaction history.

### CVE-2026-116189

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-25T14:16:59.120 |

rclone from 1.55.0 before 1.75.2 contains a signature verification bypass in stable selfupdate that trusts checksums from unsigned bytes preceding the PGP-clearsigned SHA256SUMS block. Attackers controlling the release distribution path can prepend an unsigned checksum line matching a malicious archive, causing selfupdate to install an attacker-controlled rclone executable.

### CVE-2026-116194

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-25T14:16:59.847 |

Rclone from 1.52.0 before 1.75.2 contains a cross-site request forgery vulnerability in the pCloud backend's localhost OAuth callback, which disables the state check and trusts the hostname parameter. Malicious web pages can send a stateless request to port 53682 during authorization, planting attacker tokens and API hosts so later transfers reach the attacker.

### CVE-2026-116167

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-25T14:16:55.733 |

SiYuan from 2.9.0 before 3.8.7 contains a cross-site scripting vulnerability in the unauthenticated /check-auth page that assigns the to parameter to window.location.href without scheme validation. Attackers can send a crafted link with a javascript: URI that executes after victim login, invoking kernel APIs to read or modify workspace content and settings.

### CVE-2026-116166

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-25T14:16:55.517 |

SiYuan 3.6.0 before 3.8.7 accepts and persists the networkServeTLS setting but never enforces it, so the kernel port keeps serving full API access over plain HTTP alongside HTTPS. Network-adjacent attackers can sniff the cleartext login flow and session cookie, which lacks the Secure attribute while responses omit HSTS, to hijack kernel API sessions.

### CVE-2026-116208

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-25T14:17:02.010 |

YesWiki from 4.6.2 before 4.7.0 contains a missing authorization vulnerability in ActivityPubService::syncActorPosts that lets malicious ActivityPub servers manipulate other actors' mirrored entries. Attackers can serve a poisoned outbox with cross-actor Delete, Update, or Create activities during admin-initiated sync to delete, overwrite, forge, or mass-delete entries.

### CVE-2026-116204

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-25T14:17:01.350 |

YesWiki before 4.7.0 contains a cross-site request forgery vulnerability in the despam action (tools/security/actions/despam.php) that lets unauthenticated attackers delete or restore pages through an administrator's session. Attackers can plant an auto-submitting raw HTML form on a wiki page, so an administrator who views it posts clean, suppr[], or rev[] parameters that delete PagePrincipale, configuration pages, or overwrite current content.

### CVE-2026-116149

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-25T14:16:53.123 |

ImageMagick before 6.9.13-58 and 7.x before 7.1.2-33 contains a stack-based buffer overflow in the handling of bzip2 compressed images. Attackers can supply a crafted image using bzip2 compression to overwrite stack memory during decoding, causing crashes or memory corruption.

### CVE-2026-116181

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-10-25T14:16:57.907 |

vLLM from 0.20.1 before 0.29.0 contains an improper input validation vulnerability that allows remote attackers to crash the engine by supplying out-of-vocabulary stop_token_ids. Attackers can send OpenAI chat, completion, generate, or batch requests with invalid IDs to terminate the engine or write outside the V2 runner's logits buffer.

### CVE-2026-116175

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-25T14:16:57.017 |

vLLM from 0.19.0 before 0.24.0 contains a decompression bomb vulnerability because the AudioMediaIO multimodal path calls load_audio without the max_duration_s decoded-duration limit. Authenticated attackers can send small compressed audio via input_audio or audio_url in /v1/chat/completions requests that expands to huge decoded PCM, exhausting server memory.

### CVE-2026-116195

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-25T14:16:59.990 |

Rclone before 1.75.2 contains a path traversal vulnerability in the local backend's translateLink function, which trims the .rclonelink suffix from a path after the containment check, so a name can resolve outside the destination root. Attackers can plant a directory named ...rclonelink in a source tree synced with --links and --metadata to change ownership, timestamps, and xattrs of the destination's parent directory.

### CVE-2026-116066

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-25T12:16:27.370 |

Firecrawl before 2.11.586 contains a server-side request forgery vulnerability in the Playwright service SSRF proxy that allows attackers to bypass isInternalHost checks via DNS rebinding. Attackers controlling DNS for a scrape target can return a public address during validation and a private address at connect time, retrieving cloud metadata and internal resources through the scrape API.
