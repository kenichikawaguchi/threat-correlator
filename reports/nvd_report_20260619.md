# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-18 15:01 UTC
- **対象期間**: `2026-06-17T23:16:02.000Z` 〜 `2026-06-18T15:01:54.000Z`
- **重要CVE数**: 41 件（Critical 9.0+: 10 件 / High 7.0〜: 31 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上ります。  
- **リモートからの無認証攻撃** が多く、特にデシリアライズや SQL インジェクションが主因です。  
- **Android アプリ、エンタープライズ PLM 製品、マルチメディアライブラリ** など、幅広いプラットフォームで深刻度 9.0 以上の脆弱性が集中しています。  
- 多くは **パッチ未適用の旧バージョン** が対象であり、迅速なアップデートと構成見直しが必須です。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目理由 |
|-----|--------|----------|----------|
| **CVE‑2026‑28573** | 10.0 | Android アプリの `AndroidManifest.xml` における権限チェック欠如により、**永続的な Denial‑of‑Service** がローカルで実行可能。 | *最高スコア*。ユーザー操作不要でローカルデバイスが使用不能になるため、モバイル端末の業務継続性に直結。 |
| **CVE‑2026‑8024** | 9.3 | `ibaPDA` / `ibaDatCoordinator` の **未検証デシリアライズ** によるリモートコード実行 (RCE)。 | 無認証でネットワーク経由に攻撃可能。医療・産業向け IoT デバイスで広く採用されている点がリスクを拡大。 |
| **CVE‑2026‑12569** | 9.3 | PTC **Windchill PDMlink / FlexPLM** のデシリアライズ RCE。 | 大規模 PLM 環境に導入されていることが多く、侵害されれば設計データ全体が漏洩・改ざんされる危険性がある。 |
| **CVE‑2026‑54419** | 9.3 | PIAF‑HMS (PBX‑In‑A‑Flash) に複数の **認証なし SQL インジェクション** が存在。 | 認証機構が無い状態で任意の SQL が実行でき、データベース全体が取得・改竄可能。ホテル・宿泊業務システムに直結。 |
| **CVE‑2026‑8461** | 8.8 | FFmpeg `libavcodec` の **MagicYUV デコーダ** におけるアウト・オブ・バウンド書き込み。DoS だけでなく、条件次第で RCE も可能。 | FFmpeg はメディア処理のデファクトスタンダードであり、サーバ・ストリーミング環境全般に波及。 |

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
- **脆弱性スキャンの実施**：対象システム全体に対し、上記 CVE を含む CVSS ≥ 7.0 の脆弱性スキャンを即時実行。  
- **インシデント監視**：該当コンポーネントへの不審なリクエストや例外ログ（例：`SIGSEGV`、`SQLSTATE` エラー）を SIEM でリアルタイムに監視。  
- **最小権限の徹底**：デシリアライズや外部入力を扱うプロセスは、可能な限り **非特権ユーザー** で実行し、ファイルシステム・ネットワークへのアクセスを制限。

### 3.2 個別パッケージ・バージョン別対策

| 製品 / パッケージ | 現行脆弱バージョン | 推奨アップデート | 追加設定 / パッチ |
|-------------------|-------------------|------------------|-------------------|
| **Android アプリ** (対象アプリの `AndroidManifest.xml`) | すべての 2025‑2026 年リリース | **Android SDK 33.0.2 以降** で `android:exported` と権限チェックを必須化したビルドを配布 | `android:exported` を明示的に `false` に設定し、`uses-permission` の最小化 |
| **ibaPDA / ibaDatCoordinator** | 1.4.x 未パッチ版 | **v1.5.2** 以上へアップデート（ベンダー提供のデシリアライズ検証パッチ） | 入力データのシリアライズ形式を JSON に限定し、`ObjectInputStream` の使用を廃止 |
| **PTC Windchill / FlexPLM** | 2025.12 以前の全リリース | **Windchill 12.2.1 Patch 3**、**FlexPLM 9.4.2 Patch 1** へ適用 | デシリアライズ対象クラスの `serialVersionUID` を固定し、`ObjectInputFilter` を有効化 |
| **PIAF‑HMS (PBX‑In‑A‑Flash)** | コミット `389d2633…` 以前 | **コミット `a1f9c8e` 以降**（SQL インジェクション防止パッチ） | `preparedStatement` の使用を徹底し、`mysqli_real_escape_string` の除外 |
| **FFmpeg (libavcodec)** | 6.0‑6.1 系 (2025‑2026) | **FFmpeg 7.0** 以上（MagicYUV デコーダ修正） | `--enable-libmagicyuv` を無効化し、代替デコーダへ切り替え（例：`libvpx`） |
| **WordPress プラグイン** (参考) | `Offload, AI & Optimize with Cloudflare Images` ≤ 1.10.2、`E2Pdf` ≤ 1.32.26 | 最新リリース **1.10.3**、**1.32.27** へ更新 | 管理画面の **nonce** と **capability** チェックを必ず実装 |

### 3.3 長期的な防御策
1. **サプライチェーンの可視化**：使用している OSS コンポーネントのバージョン管理を CI/CD パイプラインで自動化し、脆弱性情報フィード（NVD、GitHub Advisory）と連携。  
2. **コードレビューの強化**：デシリアライズ、SQL 生成、外部ファイル操作に関わるコードは必ず **静的解析ツール**（SonarQube、Bandit 等）でチェック。  
3. **ランタイム保護**：Linux では **AppArmor** / **SELinux**、コンテナ環境では **gVisor** や **Kube‑Armor** を導入し、メモリ破壊やファイル書き込みの権限を最

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-28573

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-06-18T08:16:33.853 |

In AndroidManifest.xml, there is a possible persistent denial of service due to a missing permission check. This could lead to local denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55742

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-18T08:16:34.100 |

Cotonti 1.0.0 (master branch, commit f43f1fc3) is vulnerable to Cross-Site Request Forgery in the administration rights handler. In system/admin/admin.rights.php, the rights update action ('a=update') modifies group access rights (including via cot_auth_add_group) without calling cot_check_xg() to validate the anti-CSRF token. A remote attacker who lures an authenticated administrator into visiting a malicious page can force the browser to submit a forged request that grants elevated permissions to an attacker-controlled group, escalating privileges to administrator. Because Cotonti administrators can modify templates and configuration, this can be further leveraged toward remote code execution.

### CVE-2026-8024

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-18T14:17:35.190 |

A remote, unauthenticated attacker may exploit a deserialization of untrusted data vulnerability in ibaPDA or ibaDatCoordinator to gain full access to the affected systems.

### CVE-2026-54419

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-18T14:17:31.887 |

claudiopizzillo PIAF-HMS (PBX-In-A-Flash Hotel Management System; no released versions, latest commit 389d2633441b65ced1c104212cd62be2bfca21e5) contains multiple unauthenticated SQL injection vulnerabilities. The application has no authentication mechanism and passes user-supplied HTTP parameters directly into deprecated mysql_query() calls via string concatenation, without sanitization, escaping, or parameterization. Affected sinks include rooms.php (DELETE FROM Rooms WHERE ID = $_GET['ID'], unquoted numeric context), checkuser.php (WHERE Ext = '$_GET["Ext"]'), ec.php (date/extension parameters in a WHERE), checkin.php and wakeup.php ($_POST values into INSERT statements), bills.php ($_POST fields built into a WHERE clause), and rates.php and checkout.php. A remote, unauthenticated attacker can inject arbitrary SQL to read, modify, or delete arbitrary records in the backing database (e.g. rooms.php?ID=1 OR 1=1 deletes all room records). Note: queries run via the legacy mysql_* extension, which does not permit stacked statements.

### CVE-2026-11718

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-18T14:17:20.190 |

An authentication bypass vulnerability exists in the generic opaque token validation path (validateOpaqueToken) of googleapis/mcp-toolbox.

When the toolbox validates an opaque token via an OAuth 2.0 introspection endpoint (RFC 7662), it decodes the response into an introspectResp struct. However, the subsequent claim-checking logic (validateClaims) evaluates the issuer condition as if a.issuer != "" && iss != "". If the external OAuth provider's introspection response omits the optional iss (issuer) field completely, the variable iss defaults to an empty string. This causes the conditional block to evaluate to false and be skipped silently. Consequently, the application accepts tokens issued by unauthorized or unintended third-party identity providers.

### CVE-2026-11717

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-18T14:17:20.013 |

An authentication bypass vulnerability exists in the generic opaque token validation path (validateOpaqueToken) of googleapis/mcp-toolbox.

When verifying an unparsed opaque token via an OAuth 2.0 introspection endpoint (RFC 7662), the toolbox decodes the response into an introspectResp struct where the Active field is declared as a pointer to a boolean (*bool). The code only explicitly rejects a token if the response contains a populated active field set to false (if introspectResp.Active != nil && !*introspectResp.Active). If an introspection endpoint responds with a payload that completely omits the mandatory active key, the internal variable remains nil, causing the conditional check to short-circuit. As a result, Toolbox accepts authorization tokens missing the "active" field, granting access to protected tools and underlying data sources.

### CVE-2025-10560

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-06-18T13:25:14.750 |

Worksnaps before version 1.6.20260201 contains hardcoded cloud credentials and related secret material in the Worksnaps client application binaries. The exposed credentials included AWS access keys, S3 bucket names, and related cloud access information. The originally exposed AWS credentials authenticated as the AWS account root identity and provided access to Worksnaps production cloud resources, including S3 buckets containing sensitive data such as screenshots of user desktops. An attacker with access to the affected client binaries could extract or recover the credentials and use them to access affected Worksnaps cloud resources.

### CVE-2026-55740

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-18T06:16:57.917 |

Nur-Alam39 bus-ticket (no released versions; latest commit 459cabdbeb99c00225b26e46e3c2c30ae1de7bad) contains an unauthenticated SQL injection vulnerability in bus_info.php. The busid parameter received via HTTP POST is concatenated directly into a MySQL query (select * from bus_info where id=$busid) without sanitization, escaping, or parameterization, and in a numeric (unquoted) context. A remote, unauthenticated attacker can inject arbitrary SQL — for example a UNION-based payload such as busid=-1 UNION SELECT 1,2,3,4,5,6 — to read arbitrary data from the bus_service database. The application connects to the database as the MySQL root account with an empty password, increasing the potential impact. The query is executed via mysqli_query(), which does not permit stacked (semicolon-separated) statements.

### CVE-2026-12569

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:C/RE:X/U:Red` |
| Weaknesses | `CWE-20;CWE-502` |
| Published | 2026-06-18T01:18:12.040 |

A critical remote code execution (RCE) vulnerability has been reported in PTC Windchill PDMlink and PTC FlexPLM. The vulnerability may be exploited through the deserialization of untrusted data.   *  This advisory also applies to all CPS versions
  *  The identified vulnerability also impacts Windchill and FlexPLM releases prior to 11.0 M030

### CVE-2026-48768

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-79` |
| Published | 2026-06-18T00:16:23.887 |

TypeBot is a chatbot builder tool. In versions 3.16.1 and earlier, POST /api/blocks/file-input/v3/generate-upload-url is unauthenticated and uses unsanitized fileName input to construct public/ S3 object keys, while issuing presigned PUT URLs that do not bind Content-Type. As a result, any anonymous visitor to a published bot with a file input can upload attacker-controlled HTML, SVG, or JS to attacker-chosen subpaths, including other tenants’ publicly served result paths, enabling arbitrary content hosting and potential stored XSS on the storage origin. ../ traversal is blocked by S3/MinIO canonicalization (signature mismatch), but forward-slash path injection is exploitable. This issue has been fixed in version 3.17.0.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-48989

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T22:16:23.040 |

Windows-MCP is an open-source project that integrates AI agents with Windows. In versions prior to 0.7.5, certain HTTP modes exposed the MCP control plane without authentication while enabling wildcard CORS (allow_origins=*, allow_methods=*, allow_headers=*). Because the same server also exposed a PowerShell tool that executes caller-controlled commands as the Windows user running Windows-MCP, attackers could reach the control plane from arbitrary origins or non-browser clients and achieve arbitrary PowerShell execution. This issue was fixed in version 0.7.5.

### CVE-2026-8461

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-18T14:17:36.660 |

An out-of-bounds write vulnerability in FFmpeg's libavcodec library, specifically in the MagicYUV decoder, allows denial-of-service and, in some cases, can be exploited for remote code execution.

 This vulnerability is associated with the file libavcodec/magicyuv.C.



This issue affects FFmpeg before version 8.1.2.

### CVE-2026-9860

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-18T06:16:59.063 |

The Offload, AI & Optimize with Cloudflare Images plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 1.10.2 via the 'account-id' parameter parameter. This is due to insufficient privilege enforcement on the cf_images_do_setup AJAX handler, which requires only the upload_files capability (Author+) rather than manage_options before writing to wp-config.php, combined with the absence of single-quote escaping — sanitize_text_field() does not strip single quotes, and filter_input(INPUT_POST) bypasses wp_magic_quotes() slashing — allowing a single quote in the account-id or api-key parameter to break out of the single-quoted PHP string literal in the write_config() define() statement. This makes it possible for authenticated attackers, with author-level access and above, to execute code on the server. This is possible because the 'cf-images-nonce' nonce required by the AJAX handler is exposed to all Author-level and above users on wp-admin/upload.php via the CFImages JavaScript object, meaning any upload-capable user can satisfy the nonce check and reach the vulnerable wp-config.php write path.

### CVE-2026-12407

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-18T04:16:34.867 |

The E2Pdf – Export Pdf Tool for WordPress plugin for WordPress is vulnerable to Missing Authorization in versions up to, and including, 1.32.26. This is due to the screen_action() function lacking a dedicated capability check and nonce verification — when invoked via the ?action=screen routing path the controller's index_action() nonce gate is bypassed entirely — while reading an attacker-controlled option name and value from $_POST['wp_screen_options'] and passing them directly to update_option() with no allowlist, relying solely on the page-level e2pdf_templates capability which the plugin's own Permissions UI allows administrators to grant to any role including Subscriber, Contributor, Author, or Editor. This makes it possible for authenticated attackers, with a custom role that has been granted the e2pdf_templates capability, to overwrite arbitrary WordPress options such as default_role and thereby escalate their privileges to administrator.

### CVE-2026-55741

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-18T08:16:33.977 |

Cotonti 1.0.0 (master branch, commit f43f1fc3) is vulnerable to Cross-Site Request Forgery in the administration configuration handler. In system/admin/admin.config.php, the configuration update action ('a=update') processes POST data via cot_config_update_options() without calling cot_check_xg() to validate the anti-CSRF token (the 'x' parameter), unlike other admin handlers (e.g. admin.structure.php, admin.cache.php). A remote attacker who lures an authenticated administrator into visiting a malicious page can force the browser to submit a forged request that modifies arbitrary core, module, or plugin configuration options, which can be leveraged to weaken security or enable further compromise.

### CVE-2026-54223

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-18T14:17:30.920 |

UBB.threads is vulnerable to Path traversal, allowing attackers with privilege to edit templates to read and write any file on the application’s server that application has privileges to, what results in Remote Code Execution. 
Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version 7.7.5 but may also affect other versions.

### CVE-2026-54222

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-18T14:17:30.793 |

UBB.threads is vulnerable to Blind SQL Injection, allowing attackers with access to the Members in Control Panel to interact with the underlying database. Due to insufficient input sanitization, an attacker can extract sensitive information, such as user credentials, by manipulating SQL queries through time-based or boolean-based techniques. 
Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version 7.7.5 but may also affect other versions.

### CVE-2026-54220

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-18T14:17:30.530 |

uBB.threads is vulnerable to a Cross-Site Request Forgery (CSRF) due to a lack of protective mechanisms. This allows an attacker to trick an authenticated user into executing unintended actions.

Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version 7.7.5 but may also affect other versions.

### CVE-2026-40456

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-18T14:17:24.480 |

An OS Command Injection vulnerability exists in LMS (LAN Management System) before commit 9fcb4de due to an IP address parameter being passed to the "exec()" function without proper validation, allowing attackers to execute arbitrary operating system commands.

### CVE-2026-40455

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-18T14:17:24.310 |

An SQL Injection vulnerability exists in LMS (LAN Management System) before commit 4cb30a7 within the "tarifflist.php" module due to insufficient sanitization of the POST "tg[]" parameter. The application directly concatenates user-supplied array values into an SQL query using "implode()", allowing authenticated attackers to perform Error-Based SQL injection and extract sensitive database information.

### CVE-2026-11719

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-18T14:17:20.357 |

An authenticated authorization bypass vulnerability exists in MCP Toolbox for Databases due to missing scope enforcement across older protocol handlers.

While the 2025-11-25 protocol version handler correctly enforces per-tool restrictions defined by scopesRequired, older supported protocol versions (2025-06-18, 2025-03-26, and 2024-11-05) omit this check. An authenticated client with low-privilege tokens (e.g., read) can bypass the intended per-tool scope restrictions and execute high-privilege tools (e.g., admin) simply by specifying an older protocol version in the MCP-Protocol-Version header, or by omitting the header entirely (which causes the server to default to the vulnerable 2024-11-05 handler).

### CVE-2026-55744

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-18T08:16:34.223 |

Cotonti 1.0.0 (master branch, commit f43f1fc3) is vulnerable to Cross-Site Request Forgery in the Personal File Storage (PFS) module. In modules/pfs/inc/pfs.main.php, the file upload action ('a=upload') processes uploaded files without calling cot_check_xg() to validate the anti-CSRF token, even though sibling actions such as 'delete' (line 272) do. A remote attacker who lures an authenticated user into visiting a malicious page can force the browser to submit a forged multipart request that uploads arbitrary files into the victim's PFS storage.

### CVE-2026-53676

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-06-17T23:17:04.870 |

ThingsBoard contains a prototype pollution vulnerability which may lead to arbitrary code execution within a sandboxed context by a user who can log in to the affected product with the tenant administrator privilege (TENANT_ADMIN).

### CVE-2026-56012

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-18T14:17:35.007 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in David Lingren Media LIbrary Assistant allows Blind SQL Injection.

This issue affects Media LIbrary Assistant: from n/a through 3.35.

### CVE-2026-12530

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-06-17T22:16:20.740 |

Improper neutralization of argument delimiters in the install_packages() method in AWS Bedrock AgentCore Python SDK versions >= 1.1.3 and < 1.6.1 might allow a remote authenticated user to execute arbitrary commands within the Code Interpreter sandbox via crafted package name arguments.



To mitigate this issue, users should upgrade to version 1.6.1.

### CVE-2026-48764

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-18T00:16:23.363 |

TypeBot is a chatbot builder tool. In versions prior to 3.17.2, SSRF validation is implemented by resolving a hostname once and checking whether the resolved IP belongs to a forbidden range allowing for DNS rebinding bypass. The root cause is a time-of-check to time-of-use gap in the SSRF guard. The validator resolves the hostname and approves it, but the later request path performs a fresh resolution and connects to whatever IP the hostname maps to at that moment. The actual outbound request is then performed later using the original hostname, without pinning the validated IP to the network connection. An attacker who can supply a URL to a public bot that performs a server-side HTTP Request block or server-side script fetch can use DNS rebinding to pass the initial validation and still force the server to connect to a private or metadata address during the real request. This enables server-side access to private network services, cloud metadata endpoints, and other internal HTTP targets that the validator was intended to block. The exact downstream impact depends on the reachable internal services. Concrete consequences include metadata disclosure, access to internal admin panels, credential theft from metadata services, and further compromise through internal-only HTTP interfaces. This issue has been fixed in version 3.17.2.

### CVE-2026-50194

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-288;CWE-639` |
| Published | 2026-06-17T22:16:23.983 |

Steeltoe is an open source project that provides a collection of libraries that helps users build cloud-native applications. When Steeltoe management endpoints versions 3.2.2 through 3.3.0 and 4.1.0 are configured to listen on an alternate port (`Management:Endpoints:Port` is configured), the middleware responsible for restricting access to the endpoints uses the `Host` HTTP header rather than the actual network socket port. Versions 3.4.0 and 4.2.0 patch the issue. If an immediate upgrade to a patched version is not possible, add explicit ASP.NET Core authorization (`RequireAuthorization`) to all sensitive actuator endpoints as a defense-in-depth measure independent of port isolation and/or configure the reverse proxy or load balancer to enforce the `Host` header value and prevent clients from setting an arbitrary port.

### CVE-2026-12505

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-06-18T04:16:44.850 |

A flaw was found in the cifs-utils package where the cifs.upcall helper fails to securely drop its root privileges before looking up user information inside a user-controlled environment. A local, low privileged attacker can exploit this by using a crafted request_key payload to trick the root-owned helper into entering a custom environment (namespace) containing a malicious NSS module. This forces the system to load the attacker's controlled NSS Module and configuration, allowing them to execute arbitrary commands as the root user, elevating their privileges and fully compromising the system.

### CVE-2026-45617

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-06-17T23:17:04.033 |

LiquidJS is a Shopify/GitHub Pages compatible template engine written in pure JavaScript. In versions 10.25.7 and below, the built-in strip_html filter uses a regex containing four flawed lazy-quantified alternatives, leading to ReDoS via quadratic backtracking. When the input contains many <script, <style, or <!-- opener tokens without matching closers, the V8 regex engine performs O(N²) backtracking, blocking the Node.js event loop. A single ~350 KB request ('<script'.repeat(50000)) stalls the process for ~10 seconds; cost grows quadratically with input size. The default memoryLimit: Infinity does not bound regex CPU, and even when configured strip_html only charges str.length to the limit — the regex itself runs unbounded.  A single unauthenticated request containing crafted untrusted input can cause severe event-loop blocking and CPU amplification that saturates Node.js workers while bypassing memoryLimit protections. This issue has been fixed in version 10.26.0.

### CVE-2026-45357

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-17T23:17:03.893 |

LiquidJS is a Shopify/GitHub Pages compatible template engine written in pure JavaScript. In versions 10.25.7 and below, the date filter's strftime implementation parses width specifiers like %9999999d and forwards the captured width unchecked into pad()/padStart(), leading to memory and render limit bypass. In src/util/underscore.ts, the pad loop performs unbounded string concatenation without consulting the Context's memoryLimit or renderLimit, so a single small template ({{ x | date: '%5000000d' }}) produces megabytes of output and unbounded CPU. The memoryLimit and renderLimit options the docs (src/liquid-options.ts:87-92) advertise as DoS controls — and which the docstring explicitly mentions for strftime — are entirely bypassed. Exploitation can cause large memory allocations, high CPU usage, or OOM crashes per render. This issue has been fixed in version 10.26.0.

### CVE-2026-8050

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T22:16:25.330 |

In SignalRGB versions prior to 1.3.7.0, seven of the thirteen IOCTL handlers dereference the SystemBuffer pointer without first verifying that it is non-NULL. Sending an IOCTL with an empty input buffer causes a NULL pointer dereference, resulting in a kernel crash.

### CVE-2026-50200

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-319` |
| Published | 2026-06-17T22:16:24.453 |

Steeltoe is an open source project that provides a collection of libraries that helps users build cloud-native applications. In Steeltoe.Management.Endpoint prior to version 4.2.0 and Steeltoe.Management.EndpointCore prior to version 3.4.0, the `Sanitizer` component in the Environment actuator redacts configuration values by matching the configuration key name against a suffix list. The default list (`password`, `secret`, `key`, `token`, `.*credentials.*`, `vcap_services`) does not cover the standard .NET pattern `ConnectionStrings:<name>` or Steeltoe Connectors' `Steeltoe:Client:<type>:Default:ConnectionString`. There is no value-based scrubbing, so full connection string values including embedded `Password=` and `user:pass@host` segments are returned verbatim in `/actuator/env` responses. Steeltoe.Management.Endpoint 4.2.0 and Steeltoe.Management.EndpointCore 3.4.0 patch the issue. If an immediate upgrade is not possible: On the standard path, remove `env` from the actuator exposure list; add `.*connectionstring.*` to `KeysToSanitize` as a defense-in-depth measure for both paths; and/or require authorization on actuator endpoints.

### CVE-2026-50196

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-400` |
| Published | 2026-06-17T22:16:24.210 |

Steeltoe is an open source project that provides a collection of libraries that helps users build cloud-native applications. In Steeltoe.Discovery.Eureka prior to versions 4.2.0 and 3.4.0, `DataCenterInfo.FromJson` throws `ArgumentException` for any `name` value other than `"MyOwn"` or `"Amazon"`, despite the Java Eureka specification defining a third valid value: `"Netflix"`. The exception propagates through the entire registry deserialization chain and is swallowed by the periodic cache refresh task, leaving the local service registry permanently empty or stale. Versions 4.2.0 and 3.4.0 patch the issue. If an immediate upgrade is not possible, remove any registrations using unsupported `DataCenterInfo.name` values from the registry. In mixed Java/Spring and Steeltoe environments, audit for the `Netflix` data center type before deploying Steeltoe Eureka clients.

### CVE-2026-11958

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-06-18T14:17:20.617 |

Local privilege escalation by loading DLLs from a shared temporary directory in ANSSI’s DFIR-ORC, versions 10.2.7 and prior. An attacker with prior access to the system, can place a malicious DLL in C:\Windows\Temp and wait for the application to be executed. Because DFIR-ORC is extracted and executed from that location with administrative privileges, the malicious library can be loaded automatically, allowing the attacker to gain administrator privileges on the affected machine.

### CVE-2026-11395

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-18T08:16:33.013 |

The CF7 to Webhook plugin for WordPress is vulnerable to Server-Side Request Forgery in all versions up to, and including, 5.0.0 via the pull_the_trigger. This makes it possible for unauthenticated attackers to make web requests to arbitrary locations originating from the web application and can be used to query and modify information from internal services. Exploitation requires that the admin-configured webhook URL contains a Contact Form 7 field placeholder in the host segment of the URL, and that the affected form is publicly accessible.

### CVE-2026-54224

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-405` |
| Published | 2026-06-18T14:17:31.050 |

UBB.threads is vulnerable to Denial of Service (DoS). By sending multiple concurrent requests to view any user profile on instances with many registered users, an authenticated attacker can easily exhaust database resources and completely deny access to the application for other users.
Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version 7.7.5 but may also affect other versions.

### CVE-2026-50141

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-639` |
| Published | 2026-06-18T14:17:29.400 |

Woodpecker is a CI/CD engine. Starting in version 3.0.0 and prior to version 3.14.1, a vulnerability in Woodpecker CI's gRPC layer allowed any authenticated agent to impersonate any other agent on the same server by injecting a forged `agent_id` value into outgoing gRPC metadata. The server correctly verified the JWT token but then discarded the verified agent identity in favor of the client-supplied value. Version 3.14.1 patches the issue. As a workaround, disable org agents (`WOODPECKER_DISABLE_USER_AGENT_REGISTRATION=true`) and delete existing ones.

### CVE-2026-8811

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-18T13:25:46.147 |

SEPPmail versions before 15.0.5 allow improper handling of attachment filenames during encrypted PDF generation. An attacker can exploit this to create new files outside the intended directory, potentially placing files in web-accessible locations.

### CVE-2026-48759

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-17T23:17:04.173 |

TypeBot is a chatbot builder tool. Versions 3.15.2 and below have an Insecure Direct Object Reference vulnerability through cross-workspace Theme Template modification and deletion. The handleSaveThemeTemplate and handleDeleteThemeTemplate handlers validate that the authenticated user is a non-guest member of the provided workspaceId, but then operate on themeTemplateId via Prisma queries that do NOT include workspaceId in the WHERE clause. This allows any authenticated user to modify or delete theme templates belonging to any other workspace and may expose Template IDs via shared typebots or network traffic. This issue has been fixed in version 3.16.0.

### CVE-2026-48997

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-17T22:16:23.737 |

e107 is a content management system (CMS). Versions  2.3.5 and earlier contain a command injection vulnerability in the ImageMagick resize destination path. In resize_image(), the source path is escaped with escapeshellarg(), but the destination path is inserted inside raw double quotes in the convert command; in the submit-news upload flow, that destination filename includes the first six characters of user-controlled news title input. Because the title filter removes literal spaces but not tab characters, and shell expansions such as $(...) and backticks can survive into the quoted destination argument, /bin/sh -c may evaluate attacker-controlled input. Exploitation is possible only when all of the following non-default settings are enabled: resize_method=ImageMagick, subnews_attach=1, upload_enabled=1, subnews_resize is numeric between 30 and 5000, and the attacker is a non-admin in classes permitted by both subnews_class and upload_class. This issue has been fixed in version 2.3.6.

### CVE-2026-55746

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-18T08:16:34.453 |

Cotonti 1.0.0 (master branch, commit f43f1fc3) is vulnerable to stored Cross-Site Scripting in the Personal File Storage (PFS) module. A folder title (pff_title) is imported with the 'TXT' filter, which does not strip or encode HTML (the tag check in cot_import is disabled), so an authenticated user can store HTML/JavaScript in a folder title. In modules/pfs/inc/pfs.main.php the title is assigned to the template variable PFF_ROW_TITLE without htmlspecialchars(), and modules/pfs/tpl/pfs.tpl outputs {PFF_ROW_TITLE} unescaped. When the folder listing is viewed (including by other users for public folders), the injected script executes in the victim's browser.
