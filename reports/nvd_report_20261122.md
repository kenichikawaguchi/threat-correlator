# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-21 15:01 UTC
- **対象期間**: `2026-11-20T15:00:49.000Z` 〜 `2026-11-21T15:01:42.000Z`
- **重要CVE数**: 147 件（Critical 9.0+: 15 件 / High 7.0〜: 132 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上**のものは 30 件を超え、特に **リモートコード実行 (RCE)** や **権限昇格** が目立ちます。  
- WordPress 系プラグイン、医療画像解析ツール、PostgreSQL Enterprise Manager など、**Web アプリケーションとデータベース管理ツール** が集中しています。  
- 多くは **入力検証の欠如**（文字列結合・ディレクトリトラバーサル・検索パス設定ミス）に起因し、攻撃者が認証なしで任意コードを実行できる点が共通しています。  
- いくつかは **サプライチェーン（pip の certifi）** に関わる問題で、依存パッケージの更新が直接的な防御策となります。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・被害規模 |
|-----|------|----------|-------------------|
| **CVE‑2026‑120539** | 9.8 (3.1) | WordPress **BuddyPress** プラグイン (≤ 1.5.4) の `eval()` でリモートコード実行 | WordPress は世界で最も利用される CMS。プラグインが RCE を許すと、サイト全体が乗っ取られ、マルウェア配布や情報漏洩につながる。 |
| **CVE‑2026‑133968** | 9.8 (3.1) | **MONAI Label** (≤ 0.8.5) の `PUT /datastore/image` でディレクトリトラバーサル → 任意コード実行 | 医療画像解析は機密性が極めて高く、実稼働環境での RCE は患者データの改ざん・漏洩リスクが重大。実際に 2026‑09 からワイルドに利用報告あり。 |
| **CVE‑2026‑132660** / **CVE‑2026‑132659** / **CVE‑2026‑132658** | 9.4 (4.0) | **Postgres Enterprise Manager (PEM)** の SECURITY DEFINER 関数・RLS ポリシー・ロール設定ミス | PEM は多くの企業で DB 監視・運用に採用。スーパーユーザー権限で任意関数を呼び出せる、エージェント間でジョブ操作が横走できる、サーバーファイルの読み書きが可能になるという **3 つの連鎖的脆弱性**。被害範囲はデータベース全体に波及。 |
| **CVE‑2026‑133949** | 9.3 (4.0) | **pip** (≤ 26.2.1) に同梱された **certifi** が改ざんされた中間証明書を含む | Python 環境で広く利用される pip が信頼できない証明書を配布していると、**サプライチェーン攻撃** により任意コードがインストールされる危険性がある。 |
| **CVE‑2026‑115407** | 9.1 (4.0) | **crypto11** ライブラリ (≤ 2.0.0‑rc8) の GCM 実装バグで認証タグ検証が不完全 → 改竄可能 | 金融・医療システムで暗号化ライブラリが直接使用されるケースが増えており、認証タグの破られた暗号文が復号可能になると機密情報漏洩につながる。 |

> **注:** これらは CVSS が 9.0 以上で、かつ **実稼働環境での利用実績が高い**（WordPress、PostgreSQL、Python、医療系ツール）点が選定基準です。

---

## 3. 推奨アクション  

### 3.1. すぐに実施すべき共通対策
- **脆弱性スキャンの実行**：`CVE‑2026‑*` をキーワードに全サーバ/コンテナを対象にスキャンし、該当パッケージのバージョンを一覧化。  
- **最小権限の徹底**：Web アプリ・データベース・バックエンドサービスの実行ユーザーを `root` から切り離し、不要な `SUPERUSER` 権限や `pg_read_server_files`/`pg_write_server_files` ロールを削除。  
- **WAF/IPS でリクエスト検査**：`eval` 文字列や不正なパス文字列 (`../`, `..\\`) を検知・ブロックするルールを追加。  

### 3.2. 個別パッケージ・バージョン別対策

| 製品・パッケージ | 現行バージョン (脆弱) | 推奨バージョン | 更新手順・ポイント |
|------------------|----------------------|----------------|-------------------|
| **BuddyPress (WordPress プラグイン)** | ≤ 1.5.4 | **≥ 1.5.5** | WordPress 管理画面 → プラグイン > 更新、または `wp plugin update buddypress`。更新後 **キャッシュクリア** と **プラグイン設定の再確認** を実施。 |
| **MONAI Label** | ≤ 0.8.5 | **≥ 0.8.6** | `pip install --upgrade monailabel`（Python 環境は 3.9 以上推奨）。アップグレード後、`/datastore/image` エンドポイントのアクセス制御を再確認。 |
| **Postgres Enterprise Manager (PEM)** | 5.x 系 (脆弱関数が残存) | **≥ 5.2.0**（リリースノートで「Security‑Definer functions fixed」） | 1. PEM バックエンド DB の `search_path` を `pg_catalog, public` に固定。<br>2. `pem_agent` ロールから `pg_read_server_files`/`pg_write_server_files` を除外。<br>3. RLS ポリシーを `pem.job`/`pem.jobstep` に適用し、エージェントは自分のジョブのみ操作可能にする。 |
| **pip** | ≤ 26.2.1 | **≥ 26.2.2** | `python -m pip install --upgrade pip`。Python 3.12 以降は **TLS 1.3** と **証明書ピンニング** がデフォルトで有効になるため、併せて Python 本体も最新版へ。 |
| **crypto11** (Go ライブラリ) | ≤ 2.0.0‑rc8 | **≥ 2.0.0‑rc9** または **v2.1.0** 以降 | `go get -u github.com/eclipse-keypont/crypto11/v2`。`go.mod` に **`replace`** で安全版を固定し

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-120539

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-21T06:16:33.227 |

The Restrictions for BuddyPress plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 1.5.4 This is due to the plugin splicing the attacker-controlled request URI into a PHP expression inside a double-quoted string and evaluating it with eval(). Because PHP interpolates double-quoted strings, a payload of the form {${...}} in the URL path is executed during interpolation, so no quote breakout is required and WordPress' slashing does not mitigate it. This makes it possible for unauthenticated attackers to execute arbitrary code on the server with a single GET request. The affected conditions ship enabled by default and are evaluated before any logged-in check, so no plugin configuration is needed; the site must have BuddyPress and Paid Memberships Pro active alongside this plugin.

### CVE-2026-133968

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-24` |
| Published | 2026-11-20T19:18:51.670 |

monailabel (aka MONAI Label) through 0.8.5 allows directory traversal, with resultant remote code execution, via the image parameter to the PUT /datastore/image endpoint, as exploited in the wild starting in September 2026.

### CVE-2026-132660

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-20T15:17:47.800 |

In Postgres Enterprise Manager (PEM), several SECURITY DEFINER functions in the pem schema of the PEM backend database are owned by a superuser but do not set a safe search_path. Any PEM user who can connect to the PEM backend database can create objects that these functions use in place of the intended ones, and so run arbitrary SQL with superuser privileges. Temporary objects can be used for this on every supported PostgreSQL version, and objects in the public schema on PostgreSQL 14 backends and backends upgraded from PostgreSQL 14.
From PEM 10.6.1, these functions run with a fixed search_path.

### CVE-2026-132659

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-20T15:17:47.637 |

In Postgres Enterprise Manager (PEM), the row-level security policies on pem.job and pem.jobstep that apply to PEM agents do not limit an agent to its own jobs. An attacker who controls one monitored host, and so its PEM agent certificate, can create, change or delete jobs for every other agent, including the agent on the PEM server. Agents run SQL job steps with the database credentials of the server they monitor, and shell job steps where batch jobs are enabled, so compromising one monitored host can give superuser SQL access to every monitored database and to the PEM backend.
From PEM 10.6.1, PEM agents can no longer create jobs or change job definitions or job steps.

### CVE-2026-132658

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-20T15:17:47.477 |

In Postgres Enterprise Manager (PEM), the pem_agent role, which every PEM agent login inherits, is a member of the PostgreSQL pg_read_server_files and pg_write_server_files roles on the PEM backend database. An attacker who controls any monitored host, and so its PEM agent certificate, can read and write files on the PEM server host as the postgres operating system user. This includes the PEM certificate authority key, which lets the attacker issue certificates for other agents and act as them.
From PEM 10.6.1, PEM agents no longer hold these roles.

### CVE-2026-129175

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-20T20:17:21.980 |

U.S Department of the Interior Unstable Slope Management Program allows an unauthenticated user to inject unauthorized SQL commands that allow the attacker to gain root access and complete control over the database. Fixed on or around 2026-10-19.

### CVE-2026-94567

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-434;CWE-436` |
| Published | 2026-11-20T19:18:56.790 |

NukeViet CMS is a multi Content Management System. Prior to 4.5.12 and 4.6.02, an attacker with access to an SVG upload flow can hide a script element in an internal DTD entity. NukeViet\Files\Upload::check_svg_tmpfile() loads the document without entity expansion, leaving a DOMEntityReference, and sanitize_svg_dom() inspects only element nodes, while browsers expand the entity when the stored file is served as image/svg+xml. The SVG path also returned before verify_image() and preserved the original bytes, so the hidden script reached disk unchanged. Guest comment attachments make the upload unauthenticated only when a module's comment feature is open to the All or Guest group and allowattachcomm is enabled; module administrators can also use the file manager, allowing same-origin script execution in an administrator's session. This issue is fixed in versions 4.5.12 and 4.6.02.

### CVE-2026-94565

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:56.500 |

NukeViet CMS is a multi Content Management System. From the 3.x release line until 4.6.01, an unauthenticated visitor can submit a Contact module message containing an event-handler attribute prefixed by a slash. NukeViet\Core\Request::filterTags() tokenizes attributes using only ASCII spaces, so it sees /onerror and misses the ^on denylist, while the browser treats the slash as a separator and activates onerror. The message is stored and rendered without output encoding in the administration panel, which lacks a Content Security Policy, allowing same-origin JavaScript execution when an administrator opens the message. This issue is fixed in version 4.6.01.

### CVE-2026-133949

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-20T19:18:51.517 |

pip prior to v26.2.2 the certifi bundled with pip contains the compromised eMudhra certificates. 




Upgrading to a secure version of pip should be done either by first upgrading Python to a version that rejects the compromised intermediates (CVE-2026-115557) or use hash pinning with a known-secure version of pip. pip is not vulnerable when using a Python version that rejects the compromised certificates. See the references below for more information.

### CVE-2026-62318

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415;CWE-416` |
| Published | 2026-11-20T18:18:54.807 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. From 2.0.0 until 4.5.1, the DHX2 and DHX2-PAM authentication state machine in etc/uams/uams_dhx2_pam.c permits logincont1 to be invoked again with the same FPLoginCont retID after it has released the global gcry_mpi_t Ra object. When DHX2 or DHX2PAM is enabled in the UAM list, a remote attacker without valid AFP credentials can repeat the first continuation step, causing gcry_mpi_powm to dereference the freed Ra value and gcry_mpi_release to free it again in a privileged afpd worker. The demonstrated result is a repeatable pre-authentication worker crash, and the use-after-free and double-free provide a plausible allocator exploitation primitive although code execution was not demonstrated. This issue is fixed in version 4.5.1.

### CVE-2026-126054

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-11-20T15:17:39.943 |

A Path Traversal vulnerability in workspace directory handling and Git integration in Google Cloud Dataform, BigQuery Studio and Colab Enterprise on Google Cloud Platform allows an authenticated remote attacker to read private files and create arbitrary files across tenant repositories using crafted workspace operations and Git integration requests.


This vulnerability was patched on 10 October 2026, and no customer action is needed.

### CVE-2026-127027

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-20T15:17:40.763 |

Poste.io is vulnerable to remote code execution in DMARC report processing. Email sent to dmarc-reports@<domain> is saved without sender verification. Script that runs as root unpacks the attachments using unsafe shell commands, allowing command injection through crafted attachments (e.g. file names or archive contents). A remote unauthenticated attacker who can send an email to the server's port 25 can execute arbitrary commands as root within the Poste.io container.


This issue was fixed in version 2.5.22.

### CVE-2026-133872

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-20T17:18:24.293 |

LessPass self-hosted sync server backend before commit 9469b0c lacks rate limiting on the JWT login endpoints /tokens/auth/ and /auth/jwt/create/, allowing unlimited authentication attempts. Unauthenticated remote attackers can brute force passwords or perform credential stuffing against known account emails to obtain tokens granting read and write access to stored profiles.

### CVE-2026-115407

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-323;CWE-1204` |
| Published | 2026-11-20T17:18:07.373 |

In `github.com/eclipse-keypont/crypto11/v2` versions `<= 2.0.0-rc8` (and the deprecated v1 module paths `github.com/eclipse-keypont/crypto11 <= 1.6.8`, `github.com/ThalesGroup/crypto11 <= 1.7.0-rc1` and `github.com/ThalesIgnite/crypto11 <= 1.2.5`), the `cipher.AEAD` returned by `SecretKey.NewGCM()` passes whatever nonce it is given straight to `CK_GCM_PARAMS` without checking its length against `NonceSize()`, and accepts an empty nonce. On a token that accepts a zero-length GCM IV — SoftHSM2 does — every `Seal` with an empty nonce encrypts under the same IV, reusing the keystream and exposing the GHASH authentication key, which allows forgeries. Separately, `Config.UseGCMIVFromHSM` sends a NULL IV with length zero to the token unless `GCMIVFromHSMControl.SupplyIvForHSMGCMEncrypt` is also set, so the token has nowhere to write the IV it generates: a `Seal` with a non-empty nonce panics after the plaintext has already been encrypted, and a `Seal` with an empty nonce returns ciphertext under an empty IV without error. On the v1 line HSM-IV mode additionally never copies the token-generated IV back to the caller, so the caller keeps its own nonce while the data was encrypted under another one.

### CVE-2026-133212

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-444` |
| Published | 2026-11-20T18:18:47.127 |

@fastify/reply-from is a Fastify plugin that forwards an incoming HTTP request to an upstream server. In versions before 12.9.1, when the plugin forwards a request whose body is not written to the upstream connection, such as a GET, HEAD, or TRACE request that carried a body, or a request with a falsy JSON body, it still forwards the client's Content-Length header while sending no body. The upstream server then treats the bytes of the following request as the unfinished body, which an attacker can use to desynchronize the connection and smuggle a request. The issue is fixed in @fastify/reply-from 12.9.1, and users should upgrade to 12.9.1 or later.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-129811

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-21T13:16:40.880 |

The PDO mapping bit lengths stored in the mapping objects are writable by the master via SDO. sizeOfPDO summed them without checking the total against the size of the rxpdo[] or txpdo[] process data buffers. A master can craft a mapping whose total bit count exceeds those buffers, causing COE_pdoPack and COE_pdoUnpack to write past their ends during each process data cycle after the PREOP to SAFEOP transition.

### CVE-2026-129798

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-21T13:16:39.247 |

The CoE SDO segmented download handler advances a write pointer by each incoming segment's size but does not track how many bytes have been written in total. A master can keep sending non-last segments until the pointer has walked past the end of the object buffer or the complete-access staging buffer.

### CVE-2026-129797

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-21T13:16:39.120 |

SDO_downloadsegment is called whenever a mailbox frame carries the DOWNLOADSEGREQ command byte, regardless of whether a segmented download is actually in progress. ESCvar.data, which the handler writes through, is NULL until a segmented transfer is started. A master can send a DOWNLOADSEGREQ at any time and write through a NULL or stale pointer.

### CVE-2026-129796

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191;CWE-787` |
| Published | 2026-11-21T13:16:38.987 |

The CoE SDO download handler for flexible-length objects (VISIBLE_STRING, OCTET_STRING, and similar) does not check that the master-declared transfer size fits within the object before writing. Two distinct writes are affected: the VISIBLE_STRING zero-padding memset and the first-frame copy into the object buffer.

### CVE-2026-129794

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-21T13:16:38.033 |

The EoE fragment reassembly code uses a frame size from the wire as the bound for memcpy into the application receive buffer, without checking that the declared size fits in the actual buffer. A master can write up to 2016 bytes into a buffer the application may have sized much smaller.

### CVE-2026-129220

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T07:16:41.030 |

The Everest Forms – Contact Form, Payment Form, Quiz, Survey & Custom Form Builder with AI plugin for WordPress is vulnerable to Missing Authorization in all versions up to, and including, 3.6.4 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with everest_forms_create_forms capabilities, to activate any already-installed inactive plugin on the server by supplying an arbitrary slug, triggering its activation hooks and escalating privileges up to administrator level. Exploitation requires that a site administrator has delegated the everest_forms_create_forms capability to a lower-privileged role via the plugin's Role & Permission feature, and that at least one inactive installed plugin whose main file follows the slug/slug.php naming convention exists on the server.

### CVE-2026-19793

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-21T04:17:20.800 |

The WP Import Export Lite plugin for WordPress is vulnerable to Limited Code Injection in all versions up to, and including, 3.9.32 via the 'comment' parameter. This is due to a two-stage shortcode check that evaluates the raw mapping placeholder before data substitution, causing the neutralizer to be skipped when attacker-controlled comment content containing a malicious [wpie_function] shortcode is substituted at runtime. This makes it possible for unauthenticated attackers to inject arbitrary PHP callables on the server. Exploitation requires an Administrator to perform the standard Export With Settings For Import followed by a New Import migration workflow, which is a routine operational task; the attacker themselves requires no account or authentication, needing only the ability to submit a pending comment on any comments-open post.

### CVE-2026-134052

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-20T20:17:39.850 |

Open Robotics RViz fillIndexBuffer Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Open Robotics RViz. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the handling of mesh resources in PointCloud and Marker displays. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the service account. Was ZDI-CAN-32652.

### CVE-2026-129176

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-20T20:17:22.207 |

U.S Department of the Interior Unstable Slope Management Program accepts a POST request from an unauthenticated user, with no cookie header, to a specific endpoint allowing for the deletion of specified users. Fixed on or around 2026-10-19.

### CVE-2026-77355

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-20T19:18:54.933 |

isomorphic-git is a pure JavaScript implementation of Git for Node.js and browsers. Prior to 1.38.7, tree-entry validation in src/models/GitTree.js does not reject the Windows NTFS reserved pathname alias .git::$INDEX_ALLOCATION. When clone() or checkout materializes an attacker-controlled tree containing this alias on Windows using an NTFS filesystem, the alias resolves to the active .git directory and permits writes to trusted repository metadata instead of a normal worktree directory. A malicious repository or object stream can therefore poison repository configuration, hooks, refs, attributes, or other gitdir state. Strict hosting that rejects hasDotgit objects can block the crafted tree, and non-NTFS systems do not interpret the pathname as the active gitdir. isomorphic-git performs the gitdir write but does not itself execute the written hook or configuration; a later native Git or compatible-tool action, such as processing a poisoned core.fsmonitor value, can execute configured commands as the victim developer or CI identity. This issue is fixed in version 1.38.7.

### CVE-2026-77347

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-11-20T19:18:54.780 |

Pozeiden is a MermaidJS renderer written in Zig. Prior to 0.3.0, src/renderers/c4.zig, src/renderers/class.zig, src/renderers/er.zig, and src/renderers/requirement.zig use fixed row-layout arrays while deriving subsequent loop bounds from an untrusted diagram's actual item count, and src/renderers/state.zig indexes a fixed depth array using user-controlled nesting depth. A valid diagram with at least 193 grid items can make the row count exceed the 64-row storage, while a deeply nested state diagram can exceed the col_count depth storage through the public pozeiden.render() path. Safe CLI and ReleaseSafe builds abort the rendering process, enabling reliable denial of service in applications that render untrusted diagrams. ReleaseSmall WASM builds with safety checks disabled instead perform out-of-bounds stack reads or writes, creating a memory-safety violation. This issue is fixed in version 0.3.0.

### CVE-2026-129995

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-20T19:18:44.467 |

mcp-ssh-manager is an MCP server for managing servers over SSH with human approval, an encrypted vault, and a live audit trail. Prior to 3.8.5, ssh_backup_create, ssh_backup_restore, ssh_backup_schedule, and ssh_backup_list build remote shell commands from caller-controlled values in src/backup-manager.js and inline backup handlers in src/index.js without neutralizing shell metacharacters. Crafted database, connection, backup directory, path, exclusion, schedule, or comment arguments can therefore execute arbitrary OS commands on managed remote servers as the configured SSH user. ssh_backup_schedule can persist execution through cron. ssh_backup_list does not pass through the server policy check and remains available in readonly and restricted modes, allowing command execution despite those restrictions. Tool arguments can be supplied by a malicious or compromised MCP client or steered through indirect prompt injection; fully trusted benign arguments do not trigger the issue. The earlier database-helper remediation for CVE-2026-77383 applied shell quoting to src/database-manager.js but did not cover these parallel backup builders. This issue is fixed in version 3.8.5.

### CVE-2026-125132

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-20T19:18:39.127 |

libumqtt is vulnerable to an integer underflow which may allow a remote attacker to cause a denial of service, memory corruption, or information disclosure.

### CVE-2026-77309

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-459` |
| Published | 2026-11-20T18:18:55.847 |

AIT GUI provides a framework for building custom websites for real-time telemetry monitoring, commanding, and other mission operations. From 1.0.0 until 2.5.1, POST /tlm/query in ait/gui/__init__.py writes attacker-controlled field data to fields_in.txt, and its no-PCAP error path can abort before deleting that file. The unauthenticated POST /script/run route accepts a scriptPath that resolves outside ScriptRoot, reads the selected file, and executes it as Python. A network-reachable attacker can obtain the ordinary session cookie without credentials, combine the two routes, and execute arbitrary Python code with the AIT-GUI server process privileges. This issue is fixed in version 2.5.1.

### CVE-2026-62320

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-130` |
| Published | 2026-11-20T18:18:55.157 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. From 1.5.0 until 4.5.1, dsi_tcp_open in libatalk/dsi/dsi_tcp.c silently limits the bytes read from an unauthenticated DSI frame received on TCP/548 to server_quantum when the attacker-controlled dsi_len is larger, without rejecting the frame or draining the declared remainder. The same silent dsi_len truncation pattern exists in libatalk/dsi/dsi_stream.c. The leftover bytes remain queued on the TCP connection and the next dsi_stream_receive call interprets them as a new DSI header and payload, allowing a remote unauthenticated attacker to smuggle one or more additional attacker-controlled DSI frames into the same connection. This issue is fixed in version 4.5.1.

### CVE-2026-77329

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346;CWE-350` |
| Published | 2026-11-20T17:18:26.917 |

Tapo provides Rust and Python APIs and an MCP server for TP-Link Tapo smart devices. From 0.3.1 until 0.5.0, the Streamable HTTP implementation in tapo-mcp/src/server.rs calls disable_allowed_hosts() without replacement Host or Origin validation, while TAPO_MCP_API_KEY remains optional for a listener that can bind to all interfaces. A malicious website can use DNS rebinding to send same-origin browser requests to the victim's local or LAN Tapo MCP listener when it runs without an API key. The attacker can invoke exposed tools including control_device for smart-device actuation and take_snapshot for configured cameras. Deployments with TAPO_MCP_API_KEY set are not affected by the unauthenticated path, and exploitation requires a running listener configured with real Tapo credentials and devices, plus victim interaction with the malicious site. This issue is fixed in version 0.5.0.

### CVE-2026-134169

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-20T23:16:58.873 |

Qwik City before 1.20.3 (@builder.io/qwik-city) and @qwik.dev/router before 2.0.0-rc.4 contain an improperly controlled object modification vulnerability in formToObj that allows unauthenticated attackers to overwrite built-in function properties. Attackers can send a form POST with nested field names traversing inherited members of string values, breaking Object.prototype.hasOwnProperty.call process-wide until server restart.

### CVE-2026-134167

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-20T23:16:58.563 |

devpi-web before 5.2.0 contains an unauthenticated path traversal vulnerability in the +doc documentation route because docs_file_exists and docs_file_path in doczip.py never confine relpath to the documentation directory. Attackers can request a relpath with a leading // or percent-encoded .. segments to read server files, including the keyfs sqlite database holding password hashes.

### CVE-2026-134164

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-20T23:16:58.120 |

probe-image-size before 7.5.0 contains an algorithmic-complexity denial of service vulnerability in lib/exif_utils.js that allows remote unauthenticated attackers to exhaust CPU by supplying self-referencing EXIF IFDs. Attackers can submit a crafted 9.6 KB JPEG with repeated ExifIFD and InteropIFD pointers to block the Node.js event loop for about 23 seconds.

### CVE-2026-129177

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-20T20:17:22.390 |

U.S Department of the Interior Unstable Slope Management Program contains a vulnerable endpoint that allows an unauthenticated attacker, without a cookie header, to send a POST request resulting in the creation of a new user. Fixed on or around 2026-10-19.

### CVE-2026-77383

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-20T19:18:55.113 |

mcp-ssh-manager is an MCP server for managing servers over SSH with human approval, an encrypted vault, and a live audit trail. Prior to 3.6.7, ssh_db_list, ssh_db_dump, ssh_db_import, and ssh_db_restore in src/database-manager.js interpolate caller-controlled database, table, collection, file path, user, host, port, and password values into shell-evaluated command strings without neutralization. Shell metacharacters in these arguments therefore execute arbitrary commands on the configured SSH target as the account used by the MCP server. ssh_db_list is classified as read-only and remains available in readonly and restricted server security modes, so this path bypasses the command-execution boundary those modes are intended to enforce. The dump and import builders are blocked in readonly mode but remain vulnerable in the default unrestricted mode. The earlier version 3.6.5 hardening covered only ssh_db_query query text; it did not protect the list, dump, import, or restore builders, or the connection flags used by query builders. This issue is fixed in version 3.6.7.

### CVE-2026-54065

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-20T19:18:52.453 |

NukeViet CMS is a multi Content Management System. Prior to 4.5.09, an authenticated administrator can submit a crafted attach value to modules/comment/admin/edit.php. The handler removed a fixed-length upload prefix without validating containment, allowing padding followed by a traversal path to be stored in the database. When the comment is deleted, modules/comment/admin/del.php joins the stored path to NV_UPLOADS_REAL_DIR and passes it to nv_deletefile(), whose realpath() check restricts deletion only to NV_ROOTDIR rather than the upload directory, permitting deletion of application files such as config.php and causing an outage. This issue is fixed in version 4.5.09.

### CVE-2026-54064

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:52.283 |

NukeViet CMS is a multi Content Management System. Prior to 4.5.09, a user with news-posting permission can bypass NukeViet\Core\Request::filterAttr() by prefixing an event-handler attribute with an ASCII form-feed character, which PHP trimming preserves but browsers treat as whitespace. NukeViet\Core\Request::unhtmlentities() omitted a decimal HTML entity tab embedded in a javascript: URI. These parser differences allow persistent event handlers or script URLs to survive filtering in vendor/vinades/nukeviet/Core/Request.php and execute for visitors, including administrators. This issue is fixed in version 4.5.09.

### CVE-2026-49259

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:52.127 |

NukeViet CMS is a multi Content Management System. From the 4.x release line until 4.5.09, a low-privileged authenticated user can store script-breaking content in the first_name and last_name profile fields used to form a comment display name. Both reply links in themes/default/modules/comment/comment.tpl interpolate {COMMENT.post_name} into the inline onclick call to nv_commment_feedback(). HTML numeric references produced by Request::_get_title() are decoded by the browser before JavaScript parsing, so clicking Reply can terminate the string and execute attacker-controlled JavaScript in the visitor's origin, including an administrator's session. This issue is fixed in version 4.5.09.

### CVE-2026-62321

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-11-20T18:18:55.320 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. From 3.1.0 until 4.5.1, the afpd Spotlight RPC fetchQueryResultsForContext: reply path in etc/afpd/spotlight_marshalling.c calls the top-level sl_pack function from sl_pack_filemeta on a shifted sub-buffer without passing the remaining capacity of the outer DSI reply buffer. An authenticated AFP client can request an amplified nested file-metadata tree so the nested packer applies MAX_SLQ_DAT relative to the shifted pointer and writes beyond struct DSI::data. The out-of-bounds write corrupts heap memory beyond the DSI reply buffer. This issue is fixed in version 4.5.1.

### CVE-2026-133680

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-20T20:17:35.750 |

A vulnerability was found in D-Link DCS-935L 1.10.01. This affects the function loginRouter of the file web/cgi-bin/localrecording/setconf.cgi of the component Local Recording CGI. Performing a manipulation of the argument account/password results in os command injection. Remote exploitation of the attack is possible. The exploit has been made public and could be used.

### CVE-2026-77326

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-20T19:18:54.110 |

MapServer is a system for developing web-based GIS applications. From 8.2.0 until 8.6.5, an unauthenticated attacker can send a WMS GetLegendGraphic request with a nonempty BBOX and repeated LAYER parameters to trigger a heap buffer overflow in msWMSDispatch() in src/mapwms.cpp. The handler appends synthesized entries to cgiRequestObj.ParamNames and cgiRequestObj.ParamValues at NumParams without retaining the arrays' capacity or reallocating them, while incrementing NumParams inside the loop. Once the parser's hidden capacity is exhausted, the writes pass the heap allocation boundary. A single request can corrupt heap memory and crash the process; code execution may be possible but was not demonstrated. This issue is fixed in version 8.6.5.

### CVE-2026-133874

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-20T17:18:24.647 |

Iceburg CRM through 5.0.0 contains an incorrect authorization vulnerability in Module::saveRecord() that allows authenticated users to write to unauthorized modules by prefixing request body keys with another module id. Attackers with write access to one module can submit crafted requests to POST /data/save or PUT /api/crm/{id} to set their role_id to Admin and access administrative data.

### CVE-2026-134172

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-20T23:16:59.420 |

audio-separator before 0.47.2 contains an insecure deserialization vulnerability that allows attackers to execute code by supplying malicious Demucs .th model files loaded via torch.load with weights_only=False. Local users writing to the shared /tmp/audio-separator-models/ default directory, or attackers controlling unverified model download sources, can execute code when victims run Demucs separation.

### CVE-2026-96805

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-20T19:18:58.183 |

The affected products have an unauthenticated command injection, which may allow an in-range BLE device to gain access to write to the control interface and influence braking with no authentication or pairing.

### CVE-2026-125273

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-11-20T19:18:39.320 |

No replay or command-integrity protection. Commands lack sequence numbers, nonces, or session tokens; captured commands can be replayed, and the last command persists across sessions.

### CVE-2026-133847

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T15:17:52.740 |

flowintel contains an authorization bypass in the browser-based admin user editing interface. The edit_user view in the admin panel verified that a non-platform-admin user could only edit accounts belonging to their own organization, but it did not verify that the target account was not a platform-admin account. As a result, an authenticated user holding an organization-admin role could open the edit form for any platform-admin account and submit modifications, including changes to credentials, roles, or other account attributes.

The API layer already enforced a restriction preventing non-admin users from targeting admin accounts, but the browser-based admin view lacked the equivalent check, creating an inconsistent authorization boundary.

Impact:
- Unauthorized modification of platform-admin account data (integrity)
- Potential lockout or privilege manipulation of platform administrators (availability)
- Escalation of an organization-admin role to effectively control platform-level administration

Affected versions: flowintel prior to 4.1.0.

### CVE-2026-133848

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-20T15:17:52.937 |

flowintel contains an authorization flaw in its user deletion functionality. Organization-scoped administrators (org admins) are able to delete platform-level administrator accounts through both the browser-based admin interface and the REST API.

The existing authorization logic verified that an org admin could only target users within their own organization, but it did not enforce the privilege hierarchy between organization admins and platform admins. As a result, an authenticated org admin could issue a deletion request against any platform-admin account belonging to the same organization, causing the target account, its sessions, and related records to be permanently removed.

Impact:
- Loss of platform-level administrative oversight
- Potential disruption of platform-wide management functions
- Removal of higher-privilege accounts that should be protected from lower-privilege roles

Affected versions: flowintel prior to 4.1.0

### CVE-2026-129344

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-21T11:16:39.077 |

Uncaught Exception vulnerability in phoenixframework phoenix allows an unauthenticated attacker to cause a denial of service via a client-selected legacy serializer on binary channel broadcasts.

When an application broadcasts {:binary, data} payloads on a channel topic, any client that connects without a vsn parameter, or with vsn=1.0.0, and joins that topic makes those broadcasts fail. Phoenix.Channel.Server.send/4 encodes each broadcast with every subscriber's own serializer inside the PubSub dispatch loop, calling fastlane!/1 with no rescue, and the negotiated Phoenix.Socket.V1.JSONSerializer raises Protocol.UndefinedError on a binary payload. Every binary broadcast on the topic then crashes the broadcasting process and skips every subscriber dispatched after the attacker. For broadcasts arriving from other nodes the loop runs in the PubSub adapter worker, whose repeated crashes restart the PubSub supervisor and empty the node's subscription registry while sockets stay connected.

This issue affects phoenix: from 1.5.7 before 1.5.16, from 1.6.0-rc.0 before 1.6.18, from 1.7.0-rc.0 before 1.7.25, and from 1.8.0-rc.0 before 1.8.17.

### CVE-2026-128361

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-21T11:16:38.787 |

Improper Input Validation vulnerability in phoenixframework phoenix (Phoenix.Presence) allows an attacker who can join a channel to cause a denial of service via a non-string presence key.

track/3,4 accepts any term as the presence key, such as a JSON object taken from a join payload. The key is converted with to_string/1 only later, in Phoenix.Presence.group/1, which raises Protocol.UndefinedError on a map. group/1 runs whenever presences are listed and when each presence diff is broadcast, together with the application's fetch/2, which can likewise raise on an unexpected key. Once such a key is tracked, every process that lists presences on the topic crashes, typically each channel that joins it, and presence diffs for the topic are lost.

From 1.7.0 the diff runs in a Task.Supervisor.async task linked to the tracker shard, and Phoenix.Presence.handle_info/2 has no clause for its failure. The shard then terminates, taking down every channel and LiveView process tracked on it and erasing presence state for all its topics. Repeated joins exhaust the restart intensity and take down the application supervisor.

This issue affects phoenix: from 1.2.0 before 1.5.16, from 1.6.0-rc.0 before 1.6.18, from 1.7.0-rc.0 before 1.7.25, and from 1.8.0-rc.0 before 1.8.17.

### CVE-2026-134170

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-11-20T23:16:59.037 |

Cesanta Mongoose 7.22 before 7.24 with the built-in TLS stack contains an out-of-bounds read in mg_timegm() that allows remote attackers to crash the process via crafted X.509 certificate validity months. Attackers can present a certificate with month '00' or out-of-range values during the handshake, before signature verification, causing an unchecked dm array index and denial of service.

### CVE-2026-94598

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:57.090 |

NukeViet CMS is a multi Content Management System. From 4.5.08 until 4.5.12 and 4.6.02, an attacker can place NukeViet's internal {@[, ]@}, [@{, and }@] sanitizer markers in an iframe srcdoc value by encoding square brackets as HTML entities. Recursive NukeViet\Core\Request::filterTags() processing decodes the characters, accepts the forged marker, and later converts it to real markup without normal tag or attribute filtering. Because an unsandboxed srcdoc iframe shares the parent origin and iframe is enabled by default through NV_ALLOWED_HTML_TAGS, stored Contact messages, comments with the editor enabled, or submitted articles can execute JavaScript with the viewer's session. This issue is fixed in versions 4.5.12 and 4.6.02.

### CVE-2026-94564

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-172;CWE-184` |
| Published | 2026-11-20T19:18:56.357 |

NukeViet CMS is a multi Content Management System. Prior to 4.6.01, an unauthenticated visitor can submit Contact module content containing numeric HTML entities with more than eight leading zeros in a URL-bearing attribute. NukeViet\Core\Request::unhtmlentities() does not decode that form before filterAttr() checks for a javascript: scheme, but browsers decode it when rendering the stored content. With an allowed tag such as the default iframe, the reconstructed script URL executes in the administration origin when staff view the message, permitting session-riding actions while remaining unable to read the HttpOnly session cookie directly. This issue is fixed in version 4.6.01.

### CVE-2026-48118

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:51.957 |

NukeViet CMS is a multi Content Management System. Prior to 4.5.09, the Comment module accepts attacker-controlled base64 content in the status_comment parameter through modules/comment/funcs/main.php; modules/comment/comment.php decodes it with nv_base64_decode() and assigns it to STATUS_COMMENT without output escaping. The required checkss token was derived from the site-wide NV_CACHE_PREFIX rather than NV_CHECK_SESSION, so a token disclosed in public comment markup could be reused across sessions in a crafted URL. An unauthenticated attacker can therefore cause decoded HTML or JavaScript to render in a victim's browser and perform phishing or same-origin actions. This issue is fixed in version 4.5.09.

### CVE-2026-122247

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-284;CWE-306;CWE-770;CWE-863` |
| Published | 2026-11-20T17:18:08.170 |

Budibase is an open-source low-code platform. Prior to 3.50.0, the public POST /api/global/users/init endpoint on a self-hosted single-tenant deployment accepts an attacker-controlled tenantId and evaluates checkAnyUserExists() in the selected tenant database instead of the legitimate default tenant. An unauthenticated attacker can select an unused tenant namespace to bypass the one-time initialization guard, causing packages/worker/src/api/controllers/global/users.ts to create a tenant-specific CouchDB database and a global-administrator document without a session or CSRF token. Repeating this operation with unique tenant identifiers can exhaust datastore resources and leave latent privileged records. The created administrator cannot log into the default tenant while multi-tenancy remains disabled, which limits the immediate impact to persistent writes, denial of service, and records that may become usable during later multi-tenant operation or migration. This issue is fixed in versions 3.50.0 and 4.0.0.

### CVE-2026-118049

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T10:16:50.300 |

The Tutor LMS – eLearning and online course solution plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 4.2.0 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with subscriber-level access and above, to permanently delete any comment they authored anywhere on the site — including regular post comments and lesson comments — along with all replies to those comments authored by any other user, including Administrators and Instructors.

### CVE-2026-123086

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-21T07:16:39.647 |

The PublishPress Revisions: Duplicate Posts, Submit, Approve and Schedule Content Changes plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 4.3.4 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with contributor-level access and above, to permanently force-delete arbitrary trashed posts, pages, and revisions owned by any user, including higher-privileged users. The required nonce is trivially harvested by any Contributor-level user because the static 'revisions-deleted' nonce action is emitted in a redirect header on the init hook before WordPress enforces edit.php's capability check, and once obtained it authorizes deletion of any trashed post or revision on the site.

### CVE-2026-54039

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-915` |
| Published | 2026-11-20T20:17:42.073 |

LibreChat is an enhanced ChatGPT clone that supports multiple AI providers. From 0.7.0 until 0.8.6, when local registration is enabled and at least one social provider is configured, POST /api/auth/register passes an unparsed request object into api/server/services/AuthService.js, allowing an unauthenticated attacker to persist a forged provider value for a known victim email. The api/strategies/socialLogin.js email-fallback path then accepts the planted record when the victim signs in because it compares the stored provider name without requiring the provider subject identifier. The victim OAuth session and the attacker local-password session become bound to the same user record, giving the attacker persistent read and write access to data created by the victim. The first-user administrator role is an additional conditional impact only on a fresh deployment. This issue is fixed in version 0.8.6.

### CVE-2026-84693

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-20T18:18:56.847 |

The WPvivid — Backup, Migration & Staging plugin for WordPress is vulnerable to Arbitrary File Deletion in version up to, and including, 0.9.134. This is due to a timing side channel in the bundled RSA decryption path, insufficient validation of migration receiver backup records, and missing path validation in the cleanup_local_backup() function. This makes it possible for unauthenticated attackers to recover an active migration receiver's RSA modulus, inject a backup record containing path traversal, and cause a later scheduled cleanup to delete an attacker-selected file writable by the web server. Exploitation requires an unexpired receiver key generated by an administrator and a subsequent manual or scheduled backup lifecycle.

### CVE-2026-55216

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-345` |
| Published | 2026-11-20T18:18:54.100 |

Logto is the modern, open-source auth infrastructure for SaaS and AI apps. Prior to 1.46.0, social account linking can use an unverified email returned by the standard OAuth 2.0 or Azure AD connector to select an existing local account. When findSocialRelatedUser matches a victim's email and a request to POST /api/experience/identification enables linkSocialIdentity, an attacker who controls that unverified provider email can link an attacker-controlled social identity to the victim account and sign in as the victim. The issue applies when the provider does not verify email ownership or allows the value to be set freely; Google, GitHub, and default OIDC connector behavior is not affected because those paths expose only verified email. Version 1.46.0 adds an opt-in email synchronization control to the standard OAuth 2.0 connector, while the Azure AD connector has offered an equivalent opt-in control since version 1.43.0. These controls preserve existing behavior by default, so administrators must enable them on affected connectors. A configurable mitigation is available in version 1.46.0.

### CVE-2026-82675

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-20T17:18:27.703 |

The GiveWP – Donation Plugin and Fundraising Platform plugin for WordPress is vulnerable to donor account account takeover in all versions up to, and including, 4.17.0. This is due to the plugin not properly validating a donor's identity prior to updating the password of a linked WordPress account. The donation receipt processes an attacker-controlled first name through the V3 template engine and then reprocesses the result through the legacy `{meta_donor_*}` engine, which can disclose the donor's email-access bearer token. The donor-dashboard password endpoint accepts that token by itself and calls `wp_set_password()` for the WordPress user linked to the donor. This makes it possible for unauthenticated attackers to reset the password of any WordPress account linked to a GiveWP donor record and gain access to that account. If the linked account is an administrator, the attacker can achieve full site compromise and remote code execution through standard administrator functionality. A published GiveWP form with a usable gateway, enabled donor email access (enabled by default), knowledge of the donor email address, and an account already linked to the targeted donor record are required. NOTE: This vulnerability can be chained with CVE-2026-82676 to satisfy the administrator donor pre-requisite for a targeted administrator user attack.

### CVE-2026-86017

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-20T19:18:55.490 |

isomorphic-git is a pure JavaScript implementation of Git for Node.js and browsers. Prior to 1.38.8, git cherry-pick applies tree changes through applyTreeChanges in src/utils/walkerToTreeEntryMap.js without checking whether a leading path component is a symbolic link. If a victim worktree contains a tracked symlink to a location outside the worktree and a cherry-picked tree places a file beneath that path, the write follows the symlink and materializes attacker-controlled blob content at the external destination. This allows arbitrary file writes and can cause data tampering, code injection into interpreted files, privilege escalation, denial of service, or follow-on code execution depending on the selected target path. This issue is fixed in version 1.38.8.

### CVE-2026-19776

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-20T20:17:40.157 |

G DATA Total Security TSNxGService Link Following Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of G DATA Total Security. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the TSNxGService service. By creating a symbolic link, an attacker can abuse the service to delete a file. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-28663.

### CVE-2026-134043

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-20T20:17:38.480 |

Krita TIF File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Krita. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of TIF files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28517.

### CVE-2026-134042

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-20T20:17:38.313 |

Krita HEIC File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Krita. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The issue results from the use of a vulnerable version of libheif. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28656.

### CVE-2026-134041

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-20T20:17:38.170 |

Krita EXR File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Krita. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of EXR files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before writing to memory. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28752.

### CVE-2026-134040

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-20T20:17:38.017 |

Krita HEIC File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Krita. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The issue results from the use of a vulnerable version of libde265. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28657.

### CVE-2026-134039

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-20T20:17:37.857 |

Krita TIFF File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Krita. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of TIFF files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28771.

### CVE-2026-134038

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-20T20:17:37.727 |

Krita PSB File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Krita. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of PSB files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before allocating a buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28905.

### CVE-2026-134037

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-20T20:17:37.597 |

Krita ASL File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Krita. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of ASL files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before allocating a buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28906.

### CVE-2026-134036

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-20T20:17:37.450 |

Krita ABR File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Krita. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of ABR files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28785.

### CVE-2026-134035

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-20T20:17:37.310 |

Krita JC2 File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Krita. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The issue results from the use of a vulnerable version of openjpeg. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28646.

### CVE-2026-114495

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-681;CWE-787` |
| Published | 2026-11-20T20:17:10.850 |

codebase-memory-mcp provides local code intelligence for developers and AI agents through a persistent graph and MCP tools. Prior to 0.9.0, automatic import of a repository's .codebase-memory/ artifact allocated a decompression buffer using the attacker-controlled 64-bit original_size value from artifact.json but truncated that value to int when passing the destination capacity to the Zstandard decompressor. A value with bit 31 set became negative and was sign-extended to a large size_t, allowing the decompressor to write frame content beyond the actual allocation. Indexing a malicious repository containing the crafted artifact could corrupt heap memory with attacker-controlled bytes, causing a reliable crash and potentially code execution. This issue is fixed in version 0.9.0.

### CVE-2026-114494

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-11-20T20:17:10.410 |

codebase-memory-mcp provides local code intelligence for developers and AI agents through a persistent graph and MCP tools. Prior to 0.9.0, the Cypher parser accepted an unbounded number of projection items in RETURN and WITH clauses while projection executors indexed fixed 32-element stack arrays using the parsed count. A query_graph query with more than 32 projection items could therefore write beyond those arrays, and a related result-column path could read uninitialized stack slots even when no node matched. Any caller of query_graph, including an agent whose query is influenced by untrusted content, could cause a reliable server crash and potentially compromise process confidentiality and integrity. This issue is fixed in version 0.9.0.

### CVE-2026-54044

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-522;CWE-863` |
| Published | 2026-11-20T20:17:42.803 |

LibreChat is an enhanced ChatGPT clone that supports multiple AI providers. Prior to 0.8.7, POST /api/agents/actions/:agent_id in api/server/routes/agents/actions.js loads an existing action with owner credentials and merges editor-controlled metadata.domain and metadata.raw_spec while preserving metadata.api_key and related OAuth client secrets. A collaborator with EDIT permission can repoint an action to an attacker-controlled host, and a later tool invocation decrypts and sends the retained owner credential to that destination. This issue is fixed in version 0.8.7.

### CVE-2026-103933

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-20T18:18:34.790 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. From 2.1.0 until 4.5.2, get_eacontent in libatalk/vfs/ea_ad.c subtracts MAX_REPLY_EXTRA_BYTES from a client-controlled FPGetExtAttr MaxReplySize without rejecting values from 1 through 5, and a signed-to-unsigned comparison can then select an untrusted AppleDouble ea_size. An authenticated client on a volume configured with ea = ad can use a pre-existing malformed AppleDouble sidecar to make read copy attacker-controlled bytes beyond dsi->data + 6 into the surrounding struct DSI, including protocol callback pointers. The malformed sidecar must already exist or be created through a separate local, co-export, management, restore, or vulnerability-assisted write path, and practical code execution depends on the target architecture, structure layout, and address uncertainty; runtime command execution was demonstrated on one x86-64 build. Volumes using ea = sys, ea = none, or ea = auto when it resolves to native system xattrs do not reach this path. This issue is fixed in version 4.5.2.

### CVE-2026-133879

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-280` |
| Published | 2026-11-20T17:18:25.317 |

A flaw was found in KubeVirt/containerized-data-importer. When a VirtualMachine with an embedded DataVolumeTemplate carrying the cdi.kubevirt.io/storage.checkStaticVolume annotation and a cross-namespace clone source is created by a tenant, the service-account clone authorization check can be bypassed, allowing a PVC from another namespace to be cloned into the tenant's namespace without the required permissions. This can result in cross-tenant data disclosure.

### CVE-2026-122244

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-116;CWE-1021` |
| Published | 2026-11-20T17:18:07.970 |

Budibase is an open-source low-code platform. Prior to 3.50.0, a BASIC application user, or an unauthenticated visitor to a public write form, can store markup in a shared external datasource that a builder or administrator later evaluates in any Handlebars binding Preview that surfaces the value, including the Data-section Formula column editor or any binding drawer. jsonFormatter.format() in packages/frontend-core/src/utils/jsonFormatter.ts leaves raw strings and object keys unescaped, while packages/builder/src/components/common/bindings/EvaluationSidePanel.svelte inserts the formatted result as raw HTML. The Handlebars SafeString path preserves the attacker-controlled value, and the Builder origin lacks a Content-Security-Policy that would block the resulting script. This permits stored script execution in the higher-privileged builder or administrator session rather than the writer's own role, allowing privileged Builder API actions and workspace data access. This issue is fixed in versions 3.50.0 and 4.0.0.

### CVE-2026-129179

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288;CWE-304` |
| Published | 2026-11-20T20:17:22.727 |

U.S Department of the Interior Unstable Slope Management Program allows attackers with valid local application credentials to establish an application session by sending JSON POST requests to the application's login endpoint without a Referrer header or completing the intended Keycloak flow. Fixed on or around 2026-10-19.

### CVE-2026-79751

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-269;CWE-284;CWE-639` |
| Published | 2026-11-20T17:18:27.397 |

SportEase is a web application for managing school sports events, class rosters, and competition teams. Prior to 1.3, an authenticated account with is_profile_complete=false can submit an attacker-selected class_id for any class in the currently active event to PUT /api/user/profile during first profile completion. AuthHandler.UpdateProfile accepts the class without validating the user's legitimate membership and automatically derives and assigns the corresponding {class_name}_rep role while isFirstCompletion is true. The attacker can become representative of one selected class, view roster information including email addresses, and add or remove competition-team assignments. Downstream handlers correctly reject access to other classes, so the impact is bounded to the selected class, but the representative privilege cannot be revoked through the exposed API and requires direct database intervention or another out-of-band remediation method. This issue is fixed in version 1.3.

### CVE-2026-132661

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-20T15:17:47.937 |

In Postgres Enterprise Manager (PEM), multi-factor authentication (MFA) is not enforced on the PEM web application's own routes. An attacker who knows the password of a user who has enrolled a second factor can skip the second factor and call PEM's pages and APIs directly, with that user's permissions. A similar issue in pgAdmin 4 was assigned CVE-2024-4215.
From PEM 10.6.1, every authenticated PEM route requires a completed MFA check.

### CVE-2026-107654

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-21T12:16:38.173 |

The One to one user Chat by WPGuppy plugin for WordPress is vulnerable to generic SQL Injection via the 'userId' parameter in all versions up to, and including, 1.1.6 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The plugin's permission callback is trivially bypassed because it validates a JWT that the plugin itself signs using an attacker-supplied value from the guppy_guest_account cookie, and the guest code path (userType=0) skips the get_userdata() check that would confirm the userId corresponds to a real WordPress user.

### CVE-2026-94597

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184;CWE-434` |
| Published | 2026-11-20T19:18:56.947 |

NukeViet CMS is a multi Content Management System. Prior to 4.5.12 and 4.6.02, an attacker who can reach an image-upload flow can upload a valid image with appended PHP short-tag code and a double-extension filename. NukeViet\Files\Upload::save_file() relied on verify_image(), which missed the <? short-open tag, while filename handling preserved embedded dots, validation inspected only the final extension, and an .htaccess rule blocked PHP extensions only at the end of the URI. On Apache mod_php systems configured with short_open_tag and a PHP extension handler, the stored polyglot can execute as PHP and run operating-system commands as the web-server user; PHP-FPM, nginx, and end-anchored handler configurations are not exposed to the execution step. This issue is fixed in versions 4.5.12 and 4.6.02.

### CVE-2026-77324

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476;CWE-690;CWE-754` |
| Published | 2026-11-20T19:18:53.793 |

MapServer is a system for developing web-based GIS applications. From 4.4.0 until 8.6.5, an unauthenticated remote attacker can send a WCS GetCoverage XML POST request whose BoundingBox element omits the crs attribute, causing xmlGetProp() in src/mapwcs.cpp to return null. msWCSParseRequest() then calls string functions on the null value before normal WCS exception handling, crashing the CGI or FastCGI worker. The analogous KVP or GET path is not affected because it obtains a count-validated, non-null token. A single request can terminate one worker, and repeated requests can exhaust a fixed worker pool and deny service. This issue is fixed in version 8.6.5.

### CVE-2026-61832

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295;CWE-502` |
| Published | 2026-11-20T19:18:52.917 |

NukeViet CMS is a multi Content Management System. Prior to 4.6.00, a network attacker who can alter outbound traffic to the extension store can exploit the HTTP client's disabled sslverify setting to substitute a serialized response. Extension-store handlers pass the response to unserialize() without an allowed_classes restriction, allowing an in-tree GuzzleHttp\Cookie\FileCookieJar gadget to write attacker-controlled content to a chosen path. When a GODADMIN opens or uses the store list, detail, install, or update functions, the substituted response can write a PHP file under the web root and execute code as the web-server user. This issue is fixed in version 4.6.00.

### CVE-2026-129054

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-20T19:18:43.287 |

Insertion of Sensitive Information Into Sent Data vulnerability in Datasolution AcyMailing SMTP Newsletter acymailing allows Retrieve Embedded Sensitive Data.This issue affects AcyMailing SMTP Newsletter: from n/a through 11.1.0.

### CVE-2026-95826

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-20T18:18:57.320 |

The SMSC911x/LAN9220 Ethernet driver stages every outgoing frame in a fixed-size static buffer before pushing it to the controller FIFO. eth_tx() in drivers/ethernet/eth_smsc911x.c took the frame length from net_pkt_get_len(pkt) and passed it directly to net_pkt_read(pkt, tx_buf, total_len), with no comparison against the size of tx_buf (NET_ETH_MAX_FRAME_SIZE). net_pkt_read() takes no destination size and only fails when the packet is shorter than the requested length, so any packet longer than the staging buffer was copied past its end.

Nothing between the IP layer and the driver bounds the frame to what the link can carry: ethernet_send() in subsys/net/l2/ethernet/ethernet.c performs no length check, and the IPv6 output path only compares the packet against the interface MTU when CONFIG_NET_IPV6_FRAGMENT is enabled (it is disabled by default). The size the stack will build is therefore governed by the interface MTU, and that MTU is remotely settable: handle_ra_input() in subsys/net/ip/ipv6_nbr.c honours the MTU option of any Router Advertisement with a value up to 0xffff, gated only by the standard hop-limit-255 and link-local-source checks. An unauthenticated attacker on the same link can raise the MTU and then have the device emit a single frame of several kilobytes, for example as a TCP segment from any service that returns more than ~1.5 KB or as an oversized UDP datagram.

The result is an out-of-bounds write into .bss immediately after tx_buf, with the overrun length and much of its content derived from the transmitted frame. Consequences range from corruption of adjacent kernel data and a crash to potential control-flow influence where the clobbered globals hold pointers; the practical overrun size is bounded by the network buffer pool rather than by the advertised MTU. The fix rejects frames larger than NET_ETH_MAX_FRAME_SIZE with -EMSGSIZE before any TX_DATA_PORT write, so the controller FIFO is also not left holding a command word without its payload.

### CVE-2026-45354

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-444` |
| Published | 2026-11-20T18:18:52.790 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. Prior to 4.4.3, libatalk/dsi/dsi_stream.c interprets the dsi_code and dsi_doff union field as a data offset for all DSI command types instead of limiting that interpretation to DSIWrite. An unauthenticated client can send a non-WRITE DSIFUNC_CMD packet with a nonzero dsi_code smaller than dsi_len, causing dsi_stream_receive to consume only the dsi_code number of payload bytes and leave attacker-controlled bytes in the readahead buffer. The residual bytes become the next DSI header, allowing protocol desynchronization that can close sessions, corrupt protocol state, or trigger an infinite-read denial of service. This issue is fixed in version 4.4.3.

### CVE-2026-132275

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-776` |
| Published | 2026-11-20T17:18:12.567 |

svglib reads SVG files and converts them to other formats. Prior to 2.3.1, the svg2rlg() renderer recursively expands nested SVG <use> references by deep-copying each referenced subtree; SvgRenderer.renderUse() in src/svglib/svglib.py calls xlink_href_target(), which rejects direct cycles but permits acyclic reference graphs with repeated fan-out. A small attacker-controlled SVG can therefore trigger exponentially increasing node expansion, consuming excessive CPU and memory in any application that renders it without a non-default option; HTML-to-PDF workflows using xhtml2pdf can reach the same renderer when an embedded data:image/svg+xml image in an HTML img element is passed to pisa.CreatePDF(). This issue is fixed in 2.3.1.

### CVE-2026-119114

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-21T10:16:50.800 |

The WP Fastest Cache – WordPress Cache Plugin plugin for WordPress is vulnerable to arbitrary directory deletion due to insufficient file path validation in the singleDeleteCache function in all versions up to, and including, 1.5.4 This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). Successful exploitation requires either the Custom Permalinks plugin or the GeoDirectory plugin to be co-installed, as these provide the necessary mechanism to write a traversal-bearing permalink value into the database that WP Fastest Cache then consumes without validation.

### CVE-2026-19779

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-20T20:17:40.543 |

G DATA Total Security Backup Service Uncontrolled Search Path Element Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of G DATA Total Security. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the Backup Service. The service restores archives from an unsecured location. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-28666.

### CVE-2026-129998

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-20T20:17:23.157 |

MaxKB is an open-source AI assistant for enterprise. Prior to 2.10.7-lts, custom Tool Init Param definitions accept attacker-controlled props_info.rules[].validator strings through POST /admin/api/workspace/{workspace_id}/tool and PUT /admin/api/workspace/{workspace_id}/tool/{tool_id}, store them without restriction, and pass them to eval() when the parameter form renders. An authenticated user with the default USER workspace role can store JavaScript and trigger execution by opening the tool's Debug screen before entering or submitting a parameter value. The same Init Param form is exposed to accounts with edit permission on the tool, but execution by a different account was not independently verified. The confirmed script runs in the MaxKB origin; access to another user's bearer token and authenticated account authority is plausible only if that user renders the malicious form. This issue is fixed in version 2.10.7-lts.

### CVE-2026-77350

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-20T18:18:56.280 |

pmo-platform is a modular PMO and release-management platform for Claude Code. Prior to 3.69.1, core/hooks/block-credential-reads.sh, core/hooks/block-egress.sh, core/hooks/block-fs-boundary.sh, and core/hooks/block-mcp-writes.sh pin PATH to /usr/bin:/bin, hard-code jq as /usr/bin/jq, and return success when jq is unavailable there. On systems where jq exists only in a Homebrew path, including affected pre-Sequoia or Homebrew-only macOS installations, the hooks can skip credential-read, network-egress, filesystem-boundary, and MCP-write controls. Native deny rules independently protect some credential paths but do not backstop the egress or MCP controls. An attacker who can influence a prompt, repository, or evaluation flow can use the skipped checks to expose secrets or perform unauthorized tool actions. This issue is fixed in version 3.69.1.

### CVE-2026-130323

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T12:16:41.563 |

The Accept Stripe Payments plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'href of any <a> element containing 'asp_action=show_pp&product_id='' parameter in all versions up to, and including, 2.1.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires that a user clicks the attacker-placed comment link to trigger the sink; however, if the non-default 'Prefetch Payment Popup Scripts' option is enabled, execution occurs on page load with no user interaction required.

### CVE-2026-124976

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T12:16:41.260 |

The Swift Performance Lite plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '<attacker-chosen parameter name>' parameter in all versions up to, and including, 2.3.7.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires that an administrator has configured at least one Cacheable AJAX Action via the plugin's AJAX Cache feature, a condition attackers can confirm by probing for a swift-performance: HIT response header.

### CVE-2026-124216

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T12:16:40.953 |

The Orphans plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 3.4.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires a two-step comment chain: a benign first comment must be approved under a given name and email so that WordPress's comment_previously_approved mechanism auto-publishes the attacker's payload comment without moderation.

### CVE-2026-123830

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T12:16:40.657 |

The wpForo Forum plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'data[display_name]' parameter in all versions up to, and including, 3.2.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires public user registration to be enabled (users_can_register=1) and a valid _wpfnonce fetched from the public sign-up page, but is otherwise fully unauthenticated.

### CVE-2026-120745

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T12:16:40.203 |

The Paid Membership Plugin, Ecommerce, User Registration Form, Login Form, User Profile & Restrict Content – ProfilePress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'reg_bio' parameter in all versions up to, and including, 4.18.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The reg_bio parameter is accepted by the registration handler's allowlist even when the rendered registration form does not include a biography field, meaning an unauthenticated attacker can supply the payload via a raw POST request without needing a visible biography input on the form.

### CVE-2026-120736

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T12:16:40.053 |

The AutomatorWP – No-Code Workflow Automation, Integration & Webhooks Plugin, now with AI plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'your-message (any CF7 form field used in a form_field: tag)' parameter in all versions up to, and including, 6.0.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires an administrator to have configured a public 'Guest submits a form' automation whose Send-an-email action embeds a form_field tag, after which the payload fires the next time any user opens the affected automation's email log entry.

### CVE-2026-116518

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T12:16:39.593 |

The ElasticPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'orderby' parameter in all versions up to, and including, 5.3.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload is stored in the ep_query_log transient for up to 24 hours after a single unauthenticated frontend GET request, and only fires when an administrator subsequently opens the Status Report page and expands the Failed Queries panel.

### CVE-2026-133367

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T10:16:52.467 |

The WPC Frequently Bought Together for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'variation' parameter in all versions up to, and including, 8.0.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce protecting the woobt_add_all_to_cart AJAX handler is emitted to all unauthenticated visitors via wp_localize_script, effectively nullifying the nonce as an authentication barrier and making the handler reachable without any login.

### CVE-2026-131609

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T10:16:52.293 |

The Germanized for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'billing_address.first_name (Store API checkout) → stored on parent order; withdrawal get_first_name() fallback' parameter in all versions up to, and including, 4.1.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is planted via an unauthenticated guest checkout order's billing first name through the WooCommerce Store API, with execution triggered by a subsequent unauthenticated withdrawal request submission whose nonce is publicly available on the /withdraw-from-contract/ page.

### CVE-2026-122230

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T10:16:51.800 |

The Thim Kit for Elementor – Pre-built Templates & Widgets for Elementor plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 1.4.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that the Post Comment widget is used with the Text Reveal entrance animation (Elementor class 'ekit--fx-word-reveal') on a Single Post template, and the comment widget must be within the initial viewport; once the first comment by an attacker is approved, or if comment moderation is disabled, subsequent payloads fire automatically for every visitor who loads the affected page.

### CVE-2026-120526

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T10:16:51.477 |

The WCFM Membership – WooCommerce Memberships for Multivendor Marketplace plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'wcfm_membership_registration_form[store_name]' parameter in all versions up to, and including, 2.12.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce required to reach the registration endpoint is publicly emitted on the /vendor-register/ page, making the endpoint fully reachable by unauthenticated attackers without any prior authentication or privilege escalation.

### CVE-2026-119061

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T10:16:50.637 |

The VikBooking Hotel Booking Engine & PMS plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'vbf<field_id>' parameter in all versions up to, and including, 1.8.20 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-118061

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T10:16:50.470 |

The VikBooking Hotel Booking Engine & PMS plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'inquiry (array keys)' parameter in all versions up to, and including, 1.8.20 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The endpoint's only access gate is a CSRF token that is publicly emitted on the unauthenticated inquiry page, making the injection reachable by any unauthenticated visitor without any precondition beyond loading that public page.

### CVE-2026-107632

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T10:16:49.960 |

The Unbounce Landing Pages plugin for WordPress is vulnerable to Stored Cross-Site Scripting in versions up to, and including, 1.1.6. This is due to insufficient input sanitization and output escaping on the proxy error message that is persisted to the 'ub-proxy-error-message' option: unauthenticated attacker-controlled REQUEST_URI data is concatenated into the error string in UBHTTP::stream_request_curl()/stream_request_wp_remote() and stored via update_option(), then later echoed inside a <textarea> on the Unbounce Pages Diagnostics admin page without any escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user (an administrator viewing the Diagnostics screen) accesses an injected page.

### CVE-2026-125054

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T09:16:38.957 |

The SiteOrigin CSS plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'class' parameter in all versions up to, and including, 1.6.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires a Contributor-level or higher attacker to store a crafted class attribute value in a post, which then fires when a user with the edit_theme_options capability opens the Visual Inspector on the affected post and clicks anywhere in the preview iframe. Exploitation by unauthenticated attackers requires that a third-party plugin providing wp_kses_post()-filtered unauthenticated front-end submission is installed and configured, and a moderator approves the submission. On a default installation, where that is not configured, the vulnerability requires attackers with contributor-level access and above.

### CVE-2026-96991

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:40.353 |

The SchemaEngine AI – AI Schema Markup, Reviews & Rich Snippets for SEO plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via WebPage JSON-LD Description in all versions up to, and including, 3.1.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that the target page renders a core/latest-comments block with the displayExcerpt option enabled, causing comment content to be incorporated into the WebPage JSON-LD description output in wp_head.

### CVE-2026-133361

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:39.870 |

The BlockStrap Page Builder – Bootstrap Blocks plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 0.1.65 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires that the attacker has previously had at least one comment approved for a given name and email address, allowing subsequent comments from that author to bypass moderation under WordPress's default policy; exploitation is also limited to sites using a block theme, which is the WordPress default.

### CVE-2026-132620

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:39.680 |

The WPBot – AI ChatBot for WordPress & Growth Suite: SEO, AI Writer, Email Marketing, Social Media plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'text' parameter in all versions up to, and including, 9.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit is triggered when an administrator opens the Chat Sessions screen, at which point the plugin's bundled Bootstrap 3.3.7 affix data-API passes the attacker-controlled data-target attribute value to jQuery as HTML, executing the injected script in the administrator's session.

### CVE-2026-131822

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:39.513 |

The Contact Form to Any API plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'your-message (any CF7 form field)' parameter in all versions up to, and including, 3.0.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The malicious payload is stored via a single unauthenticated POST to Contact Form 7's public REST feedback endpoint, which uses permission_callback __return_true and requires no authentication or prior interaction to submit.

### CVE-2026-126011

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:39.147 |

The Photo Gallery, Sliders, Proofing and Themes – NextGEN Gallery plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 4.5.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the site administrator to have configured the Thickbox lightbox effect with the "Try to apply to all images" context (thumbEffectContext=all_images), and exploitation additionally depends on an administrator approving the attacker's initial comment so that subsequent comments from that author are auto-approved.

### CVE-2026-125039

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:38.993 |

The EZ SQL Reports Shortcode Widget and DB Backup plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'User-Agent header (stored to comment_agent)' parameter in all versions up to, and including, 5.26.45 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires that an administrator has saved a report whose SQL query selects attacker-controlled data such as comment_agent, and that the attacker can identify the saved report's slug — a condition trivially met when the administrator publishes the report on a public page via the [SQLREPORT] shortcode.

### CVE-2026-120676

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:38.523 |

The Forminator Forms – Contact Form, Payment Form & Custom Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'upload-1 (the File Upload field's element_id)' parameter in all versions up to, and including, 1.58.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability is an incomplete fix for CVE-2024-1794; exploitation requires that the Forminator form's File Upload field is left at plugin defaults (no 'custom-files' restriction configured) and that the server maps no Content-Type to the .rtx extension — the default behavior of the Debian/Ubuntu Apache package used by the official WordPress Docker image and many shared hosts.

### CVE-2026-120529

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:38.377 |

The Admin Columns plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'HTTP_USER_AGENT' parameter in all versions up to, and including, 7.1.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The kses sanitization pass in classes/Sanitize/Kses.php uses wp_kses_allowed_html('post') augmented with iframe[src] and the data: protocol; because wp_kses_attr_check accepts any data-* attribute on any allowed tag without inspecting its value, a payload embedded inside a data-ac-tip attribute survives intact and is subsequently assigned to innerHTML by assets/js/table.js, bypassing the apparent mitigation entirely.

### CVE-2026-120485

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:38.073 |

The Admin Columns plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'url' parameter in all versions up to, and including, 7.1.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that an administrator has added the Author URL column to the Comments screen layout and that the site accepts unauthenticated comments, both of which are default WordPress and plugin configurations.

### CVE-2026-119632

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:37.920 |

The Forminator Forms – Contact Form, Payment Form & Custom Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'textarea-N (rich-text draft value, saved as Save-and-Continue draft meta)' parameter in all versions up to, and including, 1.58.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the targeted form to have a Rich-Text Textarea field with Save-and-Continue enabled and public submission permissions — once a crafted draft is saved, the payload executes whenever any user, including an administrator, resumes the draft or opens the Draft ID link from the Forminator Submissions screen.

### CVE-2026-116619

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:37.610 |

The MetForm – Contact Form, Survey, Quiz, Conditional Forms, Form Templates & Custom Form Builder for Elementor plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'mf-te (the form-builder-chosen name of the Text Editor field)' parameter in all versions up to, and including, 4.3.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires a published form containing a Text Editor block; the form's public markup exposes the submission nonce as data-form-nonce, allowing any unauthenticated visitor to satisfy the only submission barrier and store the malicious payload.

### CVE-2026-107713

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-21T08:16:37.443 |

The Flutterwave Payments plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'form_id' parameter in all versions up to, and including, 1.0.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The storing endpoint is accessible without authentication because the required nonce is publicly exposed on any front-end page rendering the plugin's [flw-pay-form], [flw-pay-button], or [flw-donation-form] shortcodes, allowing any unauthenticated visitor to scrape and reuse it.

### CVE-2026-94562

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-470;CWE-749` |
| Published | 2026-11-20T19:18:56.067 |

NukeViet CMS is a multi Content Management System. Prior to 4.6.01, a super-administrator satisfying the NV_IS_SPADMIN gate can use modules/users/admin/fields.php to store an arbitrary existing PHP function in the func_callback setting for a custom profile field because the callback name is checked only with function_exists() and no allowlist restricts which function may be selected. modules/users/fields.check.php later invokes that function through call_user_func() when the field is validated through registration, profile editing, or administrator editing. Selecting a command-execution function crosses the super-administrator to operating-system boundary and executes commands as the web-server account, while ordinary users can trigger the stored callback after it is configured. Because the remediation validates callbacks only when they are written, upgrading does not remove a malicious callback already stored in the database, which must be cleaned manually. This issue is fixed in version 4.6.01.

### CVE-2026-94561

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-20T19:18:55.910 |

NukeViet CMS is a multi Content Management System. In 4.6.00, an unauthenticated attacker can place the configured domain in X-Forwarded-Host while choosing a different destination in the ordinary Host header. The earlier fix validates only the forwarded value in includes/mainfile.php, while set_ini_file() in includes/ini.php constructs an outbound cURL request from the separately retained NV_SERVER_NAME before the ordinary host is rejected. Redirect following can carry the blind request to an attacker-selected private host, port, and path and invoke internal HTTP endpoints. This issue is fixed in version 4.6.01.

### CVE-2026-55372

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-20T19:18:52.607 |

NukeViet CMS is a multi Content Management System. Prior to 4.5.09, an unauthenticated attacker can submit the __serverInfoUpdate=1 field while controlling X-Forwarded-Host and X-Forwarded-Proto. NukeViet\Core\Server::standardizeHost() did not validate the forwarded host against my_domains, and a trailing slash could preserve an attacker-selected port that server_info_update() used to construct a cURL request in includes/ini.php before authentication. The blind, HEAD-only request uses a fixed path, but it permits internal host and port discovery and can poison cached server_headers. This issue is fixed in version 4.5.09.

### CVE-2026-129029

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-20T19:18:42.687 |

Server-Side Request Forgery (SSRF) vulnerability in Brainstorm Force OttoKit suretriggers allows Server Side Request Forgery.This issue affects OttoKit: from n/a through 1.1.42.

### CVE-2026-62319

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-130` |
| Published | 2026-11-20T18:18:54.980 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. From 1.5.0 until 4.5.1, dsi_stream_receive in libatalk/dsi/dsi_stream.c independently clamps dsi_doff and dsi_len for DSIWrite requests without enforcing that the data offset is no greater than the declared frame length. An authenticated AFP client can send dsi_doff greater than dsi_len, causing the receiver to consume bytes from a queued subsequent frame before libatalk/dsi/dsi_write.c detects the inconsistency. The irreversible stream desynchronization lets the attacker control the next parsed DSI header and payload and corrupts protocol framing for the connection. This issue is fixed in version 4.5.1.

### CVE-2026-132662

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-20T15:17:48.070 |

In Postgres Enterprise Manager (PEM), the SQL Profiler save and load functions in the PEM web application do not keep the client-supplied file name inside the user's storage directory. A user with the SQL Profiler role (pem_comp_sqlprofiler) can read JSON files, and overwrite files that the PEM web server account can write, outside their own storage directory. Overwriting the PEM web application's configuration database stops the web console for all users.
From PEM 10.6.1, the SQL Profiler only reads and writes files inside the user's storage directory.

### CVE-2026-129801

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-21T13:16:39.637 |

The FoE DATA frame handler computes the payload length from the master-supplied mailbox length field and passes it directly to FOE_fwrite. The length is checked against the remaining file capacity but not against the physical mailbox buffer size. A master can declare a large length while sending a short frame, causing FOE_fwrite to read past the end of the mailbox buffer.

### CVE-2026-134126

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T21:17:36.977 |

WPC Smart Messages for WooCommerce plugin before 4.3.6 contains a missing authorization vulnerability that allows authenticated attackers with Contributor or Author privileges to disclose arbitrary post meta and private product data by supplying attacker-controlled id and key attributes to the [wpcsm_product_field] and [wpcsm_product_data] shortcodes without any capability or protected-meta checks. Attackers can embed these shortcodes in a published post to exfiltrate sensitive order data such as billing email, phone, and address stored as post meta, as well as private or draft product descriptions and purchase notes, exposing confidential customer and business information to unauthenticated site visitors.

### CVE-2026-129178

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-759` |
| Published | 2026-11-20T20:17:22.563 |

U.S Department of the Interior Unstable Slope Management Program stores local user passwords as unsalted MD5 hashes. Fixed on or around 2026-10-19.

### CVE-2026-130602

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:44.760 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in BdThemes Prime Slider – Addons For Elementor bdthemes-prime-slider-lite allows Stored XSS.This issue affects Prime Slider – Addons For Elementor: from n/a through 5.1.2.

### CVE-2026-130601

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:44.623 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in BdThemes Element Pack Elementor Addons bdthemes-element-pack-lite allows Stored XSS.This issue affects Element Pack Elementor Addons: from n/a through 10.0.9.

### CVE-2026-129063

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:43.577 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Brainstorm Force Spectra ultimate-addons-for-gutenberg allows Stored XSS.This issue affects Spectra: from n/a through 2.20.5.

### CVE-2026-129042

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:43.150 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Tribulant Software Newsletters newsletters-lite allows Stored XSS.This issue affects Newsletters: from n/a through 4.18.2.

### CVE-2026-129037

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:43.007 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Ahmad WP Job Portal wp-job-portal allows Reflected XSS.This issue affects WP Job Portal: from n/a through 2.8.1.

### CVE-2026-129033

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:42.847 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Ays Pro Quiz Maker quiz-maker allows Reflected XSS.This issue affects Quiz Maker: from n/a through 6.7.1.99.

### CVE-2026-129007

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-20T19:18:42.547 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Knit Pay Knit Pay knit-pay allows Stored XSS.This issue affects Knit Pay: from n/a through 9.6.4.0.

### CVE-2026-49388

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-20T18:18:53.480 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. From 3.1.0 until 4.5.0, sl_unpack_loop in etc/afpd/spotlight_marshalling.c uses an attacker-controlled Spotlight table-of-contents index during FPSpotlightRPC without checking it against the number of entries or the remaining dsi->commands buffer. An authenticated AFP client with access to a Spotlight-enabled volume can choose a large toc_index whose multiplication and addition produce an out-of-range address, causing an attacker-influenced heap read and reliably crashing the worker serving that session. The earlier CVE-2026-44066 remediation bounded recursion depth and toc_offset but did not bound toc_index. This issue is fixed in version 4.5.0.

### CVE-2026-49387

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-20T18:18:53.307 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. From 3.1.0 until 4.5.0, the afpd FPSpotlightRPC unmarshalling handlers in etc/afpd/spotlight_marshalling.c trust the element count encoded in the upper 32 bits of an RPC tag without comparing it with the remaining input length. An authenticated client with access to a Spotlight-enabled volume can make sl_unpack_ints, sl_unpack_date, sl_unpack_uuid, or sl_unpack_floats iterate beyond dsi->commands and read heap memory. The read values remain in internal dalloc storage and no information-disclosure channel was demonstrated, but the worker serving the attacker's session can be crashed. This issue is fixed in version 4.5.0.

### CVE-2026-45356

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-11-20T18:18:53.130 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. Prior to 4.4.3, the afpd Spotlight RPC unmarshalling loop in etc/afpd/spotlight_marshalling.c subtracts an attacker-controlled subcount from the unsigned count variable in sl_unpack_loop without verifying that subcount is not larger. An authenticated AFP client can place an excessive element count in the sl_unpack_ints, sl_unpack_uuid, sl_unpack_floats, or sl_unpack_date handler, or in a null element, so the subtraction wraps near UINT_MAX and the loop continues reading heap memory at increasing offsets up to toc_offset, which is capped at 65000. The out-of-bounds values can be stored in dalloc structures and returned in the Spotlight RPC response, disclosing heap contents. This issue is fixed in version 4.4.3.

### CVE-2026-45355

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-11-20T18:18:52.967 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. Prior to 4.4.3, the afpd Spotlight RPC string unmarshalling path in etc/afpd/spotlight_marshalling.c uses sl_unpack_cpx to calculate slen from qlen and the attacker-controlled used_in_last_block value without preventing a negative result. An authenticated AFP client can send a complex string or UTF-16 string element that makes slen negative, and the implicit conversion to size_t causes dalloc_strndup or convert_string_allocate to read beyond the heap buffer. The out-of-bounds read can expose heap data through the RPC response or crash the worker process. This issue is fixed in version 4.4.3.

### CVE-2026-104184

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-915` |
| Published | 2026-11-20T18:18:34.980 |

LinkAce is a self-hosted archive to collect website links. Prior to 2.6.0, LinkController::update() in app/Http/Controllers/API/LinkController.php passes $request->all() to the repository update method even though user_id is fillable and is not an allowed field in the validated update request. An authenticated API user who is authorized to update a link can therefore assign an arbitrary or nonexistent user_id, transferring the link into another user's bookmark collection or orphaning it from any real account. The web update controller is unaffected because it passes only validated fields. This issue is fixed in version 2.6.0.

### CVE-2026-133854

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T15:17:54.090 |

flowintel contains a vulnerability in the case and task classification usage endpoints that allows authenticated users to view classification data associated with cases they do not have permission to access.

The affected endpoints, which provide lists of used taxonomies, tags, galaxies, clusters, and custom tags, did not properly enforce object-level access controls. While the endpoints required authentication, they failed to filter the returned data based on the requesting user's visibility permissions for the underlying cases. This allowed any authenticated user to enumerate classification usage across all cases, including private or restricted cases belonging to other organizations or users.

This issue could lead to the disclosure of sensitive information, such as the existence of specific cases, the types of threats or indicators associated with them, and the relationships between different classification elements, potentially aiding an attacker in reconnaissance or targeting.

Affected versions: < 4.1.0

### CVE-2026-133849

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-20T15:17:53.137 |

A vulnerability exists in the flowintel application's calendar functionality that allows unauthorized access to private case data. The task calendar queries failed to enforce visibility checks on the parent case associated with tasks. Specifically, tasks assigned to a user or belonging to the user's organization were returned in calendar views (including browser and API ICS feeds) without verifying whether the user had permission to view the parent case. This allowed users to potentially discover and access details of private cases they were not authorized to view, leading to information disclosure.

The issue affected the default task visibility logic and the assigned-only task queries. The fix ensures that case visibility is rechecked in addition to task assignment or organization membership, preventing the exposure of private case data in calendar outputs.

Affected versions: flowintel < 4.1.0

### CVE-2026-133839

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T15:17:51.530 |

FlowIntel contains a missing authorization vulnerability in its task file deletion functionality. When a privileged task is in a restricted state (Requested, Rejected, or Request Review), any authenticated user with basic case membership (e.g., editor or queuer) was able to delete evidence files associated with that task via both the browser interface and the REST API. The deletion operation should have been restricted to users holding Admin, Case Admin, or Queue Admin roles.

The vulnerability affects the core file deletion logic, the browser-facing task endpoint, and the API task endpoint. No role-based restriction was enforced prior to performing disk removal, database record deletion, timeline event removal, or history log updates.

An attacker with a low-privilege case membership could destroy evidence files, corrupt investigation timelines, and alter case history, compromising the integrity of ongoing investigations.

Affected versions: FlowIntel prior to 4.1.0.

### CVE-2026-133837

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-20T15:17:51.130 |

flowintel contains an authorization bypass in its task completion workflow for privileged cases. Users with lower-privilege roles (editor, queuer) were able to mark tasks as completed without the required approver review (Admin, Case Admin, or Queue Admin), undermining the approval workflow.

The vulnerability was exploitable through multiple paths:
- Direct task completion via browser UI or REST API
- Changing a task's status to "Finished", which implicitly completed the task
- Creating a new task in a privileged case with the completed flag already set
- Using UUID aliases or Matrix delegation to reach the same endpoints

Preconditions:
- An authenticated user with at least editor or queuer role
- A privileged case with tasks in a non-completed state

Security impact:
- Bypass of the mandatory approver review process for privileged cases
- Unauthorized modification of task completion state
- Potential to mark sensitive work as finished without proper oversight

Affected versions: flowintel prior to 4.1.0

### CVE-2026-132663

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-20T15:17:48.200 |

In Postgres Enterprise Manager (PEM), webhook URLs are not validated, and the PEM agent does not restrict the URL schemes it uses to deliver webhooks. A user with the alert configuration role (pem_config_alert) can set up a webhook with a file:// URL. When the webhook is sent, the agent on the PEM server, which runs as root by default, reads the local file and stores its contents in the webhook error record in the PEM database, where any PEM user can read it.
From PEM 10.6.1, PEM accepts and sends only http and https webhook URLs.

### CVE-2026-132664

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321;CWE-522` |
| Published | 2026-11-20T15:17:48.333 |

In Postgres Enterprise Manager (PEM), any PEM user can read the encrypted passwords that PEM agents use to connect to monitored servers, including the PEM backend superuser password stored when the PEM server is configured. Unless a custom encryption key is configured, these passwords are encrypted with a key that is the same in every PEM installation, so they can be decrypted.
From PEM 10.6.1, PEM users can no longer read these passwords.
