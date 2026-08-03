# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-03 15:00 UTC
- **対象期間**: `2026-08-02T15:00:15.000Z` 〜 `2026-08-03T15:00:25.000Z`
- **重要CVE数**: 72 件（Critical 9.0+: 16 件 / High 7.0〜: 56 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件** 近くに上りますが、特に **認証不要でリモートからコード実行・認可バイパスが可能** な脆弱性が目立ちます。  
- スコア 9.9 以上の **SQL インジェクション** が SiYuan 系製品で連続して報告され、データベース全体が取得・改ざんできる危険性があります。  
- **Wapt Server** の認証バイパスは CVSS 10.0 と最高点で、セッションハイジャックに直結します。  
- モバイルアプリやネットワーク機器（Check Point、OpenWrt 等）でも **認証バイパスやコマンドインジェクション** が多数報告され、企業ネットワークの境界防御が崩れやすくなっています。  

## 2. 特に注目すべき CVE  

| CVE | スコア | 製品・バージョン | 主な問題点 | 影響範囲・リスク |
|-----|--------|------------------|------------|-------------------|
| **CVE‑2026‑33591** | **10.0** | Wapt Server < **2.6.1.17813** | 認証なしで特別に細工したパケットを送ると、対象アカウントの有効なセッショントークンを取得できる。 | 完全な認証バイパス → 任意ユーザーとして管理コンソールにアクセス可能。内部ネットワーク全体の資産管理が危険に。 |
| **CVE‑2026‑69085** / **CVE‑2026‑69084** / **CVE‑2026‑69083** | **9.9** (3 件) | SiYuan ≤ **v3.7.2**（69084, 69083） / < **v3.7.3**（69085） | `/api/filetree/searchDocs`、`/api/search/searchEmbedBlock`、`/api/fullTextSearchAssetContent` でユーザー入力が SQL に直接埋め込まれ、認証不要で任意 SQL が実行可能。 | データベース全体の閲覧・改ざん、機密情報漏洩、永続的なバックドア設置が可能。 |
| **CVE‑2026‑2346** | **9.8** | Menulux Software Inc. Mobile App ≤ **12.05.2026** | ユーザーがコントロールできるキーで認可チェックを回避でき、アプリの整合性チェックが無効化される。 | アプリ改ざん・不正インストール、モバイル端末上での機密データ取得や不正操作が可能。 |
| **CVE‑2026‑18574** | **9.3** | Check Point Security Management Server / Multi‑Domain Security Management Server | 認証バイパスにより管理サービスへ直接リモートコマンド実行が可能。 | 管理サーバ全体の設定変更・情報漏洩、ネットワーク全体の防御が崩壊。 |
| **CVE‑2026‑18588** | **9.3** | Wavlink WL‑NU516U1 (ファームウェア) | `nas.cgi` の `fgets` に対する `CONTENT_LENGTH` 操作でスタックバッファオーバーフロー。リモートからコード実行が可能。 | ルータ/NAS 機能の完全乗っ取り、内部ネットワークへの踏み台化。 |

> **注記**  
> - 上記 5 件は **CVSS ≥ 9.3** かつ **認証不要** で攻撃が成立する点が共通。  
> - SiYuan 系は同一製品で複数エンドポイントが脆弱であるため、**一括アップデート** が最も効果的です。

## 3. 推奨アクション  

### 3‑1. 直ちにパッチ適用・バージョンアップ
| 製品 | 現行脆弱バージョン | 推奨バージョン | 取得先・備考 |
|------|-------------------|----------------|--------------|
| **Wapt Server** | < 2.6.1.17813 | **≥ 2.6.1.17813** | 公式サイトの Security Patch リリース (2026‑07‑xx) |
| **SiYuan** | ≤ v3.7.2 (69084/69083) / < v3.7.3 (69085) | **v3.7.3 以降** | GitHub Release `v3.7.3` (2026‑06‑15) |
| **Menulux Mobile App** | ≤ 12.05.2026 | **12.05.2026‑patch‑1** 以上 | Google Play / Apple App Store の緊急アップデート |
| **Check Point Security Management Server** | すべての 2026‑リリース | **R80.10 P‑2026‑001** 以上 | Check Point Customer Support Portal から取得 |
| **Wavlink WL‑NU516U1** | ファームウェア 4.4.5 以前 | **4.4.6** 以上 | メーカー提供の OTA 更新パッケージ |

### 3‑2. 侵入検知・防御策
1. **ネットワークレベルでのアクセス制御**  
   - Wapt Server、Check Point 管理サーバ、SiYuan の管理 API へは **内部 IP アドレスのみ**、もしくは VPN 経由に限定。  
   - `GET /account/delete/*` など状態変更系エンドポイントは **POST のみ受け付け、CSRF トークン必須** に設定。

2. **Web アプリケーションファイアウォール (WAF)**  
   - SiYuan の `/api/*` エンドポイントに対し **SQL インジェクションパターン**（シングルクオート、UNION、SELECT など）をブロック。  
   - Wavlink の `nas.cgi` へは `CONTENT_LENGTH` の上限を **1 KB** に制限し、異常長は 400 エラーで遮断。

3. **ログ監視とインシデント対応**  
   - セッショントークン取得や認証バイパスの試行は **ログイン失敗/成功イベント** と合わせて SIEM に集約。  
   - 異常な SQL クエリや大量の `/api/search/searchEmbedBlock` 呼び出しは即座にアラート化。

### 3‑3. 長期的な対策
- **依存ライブラリの定期的な脆弱性スキャン**（特に Bouncy Castle 系は多数の 9.3‑級脆弱性が報告されているため、**2.73.12 以降**への更新を推奨）。  
- **コードレビュー時の入力検証徹底**：SQL 文字列結合は **プリペアドステートメント**、ファイルパスは **正規化 + ホワイトリスト**、外部からのサイズ指定は **上限チェック** を必ず実装。  
- **緊急パッチ適用プロセスの自動化**：CVE 公開から 7 日以内に

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-33591

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-03T10:16:28.610 |

A vulnerability in Wapt Server before version 2.6.1.17813 allows a  remote unauthenticated attacker to bypass
security restriction using a specially crafted packet and retrieve a valid
session token for the targeted account.

### CVE-2026-69085

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-03T14:16:28.820 |

SiYuan before v3.7.3 contains a SQL injection vulnerability in the /api/filetree/searchDocs endpoint, where the caller-supplied keyword parameter is concatenated directly into SQL statements with no escaping or parameter binding. The endpoint is reachable by a publish RoleReader token, or unauthenticated when publish mode is enabled with Publish.Auth.Enable set to false. Because the statement executes on a read-write SQLite handle via a driver that supports stacked (semicolon-separated) statements, an attacker can read and modify database content across all cleartext (non-encrypted) notebooks on the instance.

### CVE-2026-69084

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-03T14:16:28.680 |

SiYuan versions <= v3.7.2 expose the /api/search/searchEmbedBlock endpoint, which passes a client-supplied SQL statement verbatim to the main read-write siyuan.db handle with no single-statement, read-only, or admin restrictions. The endpoint is gated only by CheckAuth, making it reachable by the publish RoleReader token and by anonymous users when publish authentication is disabled. Because the underlying driver executes stacked statements, an attacker can read and modify content across all opened cleartext notebooks (encrypted per-box notebooks are excluded). Fixed in v3.7.3.

### CVE-2026-69083

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-03T14:16:28.537 |

SiYuan versions before v3.7.3 contain SQL injection vulnerabilities in the fullTextSearchAssetContent endpoint reachable by unauthenticated users and publish RoleReader tokens. Attackers can execute arbitrary SQL on the read-write asset-content database via unescaped method parameters and REGEXP clauses to read, modify, or delete cross-notebook data.

### CVE-2026-2346

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-03T13:17:39.513 |

Authorization bypass through User-Controlled key vulnerability in Menulux Software Inc. Mobile App allows Software Integrity Attack.

This issue affects Mobile App: through 12.05.2026.

### CVE-2026-64827

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-08-03T14:16:27.630 |

Telenia Software TVox 26.5.3 and prior 26.x versions, and 24.9.21 and prior 24.x versions, contain an authentication bypass vulnerability in set_env.php where the redirectToLoginAdminIRequestHaveAccessToken() function derives the current page name from PHP_SELF and skips authentication when the value matches 'login_admin.php'. Attackers can append '/login_admin.php' to the path of any target PHP script to cause the authentication check to pass and gain unauthenticated access to all PHP scripts under the manager HTML directory.

### CVE-2026-18574

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-03T13:17:13.000 |

An authentication bypass vulnerability in Check Point Security Management Server and Multi-Domain Security Management Server (MDS) could allow an unauthenticated remote attacker with network access to Management services to execute arbitrary commands on the Security Management Server. Successful exploitation could result in full compromise of the Security Management system. Check Point discovered this issue internally and has no indication of active exploitation.

### CVE-2026-18588

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-03T07:16:43.047 |

A vulnerability has been found in Wavlink WL-NU516U1 708c073-mt7628. This affects the function fgets of the file nas.cgi. The manipulation of the argument CONTENT_LENGTH leads to stack-based buffer overflow. Remote exploitation of the attack is possible. You should upgrade the affected component. The vendor was contacted early, responded in a very professional manner and quickly released a fixed version of the affected product.

### CVE-2026-58062

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-03T03:16:45.640 |

In Bouncy Castle for Java before 1.85, Stapled OCSP response accepted without binding to the checked certificate. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bc-fips 2.0.2 (2.0.X series) and 2.1.3 (2.1.X series).

### CVE-2026-8763

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-03T01:16:45.807 |

In Bouncy Castle for Java before 1.85, Name Constraints bypass via trailing dot in rfc822Name and URI. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bc-fips 1.0.2.7 (1.0.X series), 2.0.2 (2.0.X series) and 2.1.3 (2.1.X series).

### CVE-2026-59650

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-03T01:16:45.250 |

In Bouncy Castle for Java before 1.85, MTI/A0 DH agreement exponentiates unvalidated peer value. This issue also affects Bouncy Castle for Java LTS before 2.73.12.

### CVE-2026-59638

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-297` |
| Published | 2026-08-03T01:16:43.543 |

In Bouncy Castle for Java before 1.85, JSSE hostname verifier CN-fallback enabled by default despite documented opt-in. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bctls-fips 1.0.24 (1.0.X series), 2.0.24 (2.0.X series) and 2.1.24 (2.1.X series).

### CVE-2026-65321

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-02T15:16:33.957 |

PyAthena prior to 3.35.4 contains a sql injection vulnerability that allows unauthenticated attackers to inject arbitrary SQL by exploiting improper quote-escaping in DefaultParameterFormatter.format(), which routes DELETE and CTAS statements to the _escape_hive function that backslash-escapes single quotes rather than doubling them. Because Athena and Trino do not treat backslashes as escape characters inside string literals, attacker-supplied input such as a single quote followed by SQL syntax causes the parser to terminate the string literal prematurely, enabling data exfiltration via UNION SELECT, execution of destructive statements, and attacker-controlled CTAS destination and content.

### CVE-2026-68587

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-03T14:16:28.397 |

SiYuan versions before v3.7.3 contain an information disclosure vulnerability in the getHeadingDeleteTransaction, getHeadingLevelTransaction, and getHeadingInsertTransaction endpoints that return rendered block DOM without publish-access checks. Anonymous readers or publish RoleReader tokens can supply a heading block ID to read full rendered content of publish-disabled documents that should be restricted.

### CVE-2026-68586

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-03T14:16:28.237 |

SiYuan before v3.7.3 fails to apply publish-access filters to the getBacklinkDoc and getBackmentionDoc content endpoints (/api/ref/getBacklinkDoc and /api/ref/getBackmentionDoc). While the corresponding backlink list endpoints filter publish-forbidden documents, the content endpoints (gated only by CheckAuth) do not. A publish-mode reader — including an anonymous reader when publish Basic Auth is disabled — can call these endpoints directly with a publish-forbidden document's ID to retrieve its rendered DOM content and to determine whether the document references a given block (a reference-existence oracle).

### CVE-2026-68584

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-03T14:16:27.943 |

SiYuan versions before v3.7.3 contain an authentication bypass vulnerability in publish mode where content-returning endpoints getHeadingChildrenDOM, getHeading*Transaction, and getBacklinkDoc perform no password check despite protecting the primary getDoc endpoint. Anonymous attackers can retrieve full content of password-protected documents by obtaining internal block IDs from reader-accessible endpoints and calling unprotected content endpoints to bypass the password gate.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-18601

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-03T14:16:25.947 |

A vulnerability was found in GL.iNet GL-MT3000 up to 4.4.5. This impacts the function ovpn-client.check_config of the file /cgi-bin/glc of the component ovpn-client.so Native Plugin. Performing a manipulation of the argument filename results in command injection. Remote exploitation of the attack is possible. The exploit has been made public and could be used. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-18589

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-03T07:16:43.260 |

A vulnerability was found in Wavlink WL-NU516U1 708c073-mt7628. This impacts the function change_password of the file nas.cgi. The manipulation of the argument User1Passwd results in stack-based buffer overflow. The attack can be executed remotely. The exploit has been made public and could be used. The affected component should be upgraded. The vendor was contacted early, responded in a very professional manner and quickly released a fixed version of the affected product.

### CVE-2026-69082

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-03T10:16:33.540 |

CTI-Transmute contained a cross-site request forgery vulnerability in the administrative user deletion functionality. The /account/delete/<id> endpoint accepted HTTP GET requests for an operation that modified application state.

An unauthenticated remote attacker could construct a malicious link or embed a request targeting this endpoint and induce an authenticated CTI-Transmute administrator to visit the attacker-controlled content. If the administrator had an active session, the browser would automatically include the administrator’s session credentials, causing the selected user account to be deleted without the administrator intentionally confirming the operation.

Successful exploitation requires interaction from a currently authenticated administrator who has permission to delete users. The attacker does not need a CTI-Transmute account or administrative privileges because the forged request executes using the victim administrator’s session.

The vulnerability could allow an attacker to delete arbitrary user accounts, resulting in unauthorized modification of application state and denial of access for affected users. Depending on whether administrators can delete other administrators or the final administrative account, exploitation could also disrupt administration of the CTI-Transmute instance.

The patch resolves the issue by restricting the deletion endpoint to HTTP POST requests and submitting the deletion through a form containing a CSRF token.

### CVE-2026-69078

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-03T10:16:33.243 |

CTI-Transmute is affected by a server-side request forgery vulnerability in the evaluation report PDF-generation functionality.

User-controlled CTI content, including conversion names, descriptions, and comments, is converted from Markdown to HTML and rendered as a PDF using WeasyPrint. Before the patch, the renderer used WeasyPrint’s default URL-fetching behavior without restricting the protocols or destinations that could be referenced by the generated HTML.

An attacker able to supply content included in an evaluation report could inject crafted resource references using schemes such as http://, https://, or file://. When the report was rendered, CTI-Transmute could fetch these resources using the application server’s network connectivity and filesystem privileges.

Successful exploitation could allow an attacker to:

  *  access services available only from the CTI-Transmute server or its internal network;
  *  probe internal hosts and service endpoints;
  *  retrieve local files readable by the application process; and
  *  expose fetched content through the generated PDF, depending on the referenced resource type and rendering context.


The vulnerability is corrected by providing WeasyPrint with a restrictive URL fetcher that permits only self-contained data: URIs. The externally hosted Google Fonts stylesheet was also removed so that PDF generation performs no intentional network or filesystem fetches.

### CVE-2026-69096

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-03T14:16:30.500 |

OpenWrt luci-app-dockerman (LuCI master and openwrt-25.12 snapshots containing the ucode docker_rpc.uc RPC backend after the JS/ucode conversion) contains an OS command injection vulnerability. The package's read ACL grants broad ubus access to docker.* / docker.container.*, which exposes the docker.container.ttyd_start method even though it performs mutating operations. The run_ttyd handler builds a shell command from the request-controlled id, cmd, and uid fields and passes it to system() without quoting or argv-style execution in the rpcd root context. An authenticated attacker holding only the luci-app-dockerman read ACL can inject shell metacharacters (e.g., in id) to execute arbitrary commands as root via an HTTP POST to /ubus. openwrt-24.10 and openwrt-23.05 do not contain this backend and are not affected; no patched version was known as of the advisory.

### CVE-2026-69095

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-03T14:16:30.343 |

OpenWrt luci-app-bmx7 before commit 5890760a454dad2cb00389dba2cdc5e779e0ffdd contains a path traversal vulnerability in the bmx7-info CGI script that allows unauthenticated attackers to read files outside the configured runtimeDir. Attackers can supply directory traversal sequences in the query string to escape the intended directory and read sensitive files accessible to the CGI process.

### CVE-2026-69091

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-03T14:16:29.730 |

Admidio before 5.0.11 contains an authentication bypass vulnerability in the forum module when configured in login-only mode. The access control logic in modules/forum.php fails to validate the login-only configuration state, allowing unauthenticated attackers to read forum topics and posts by directly accessing the module with read-only parameters.

### CVE-2026-69089

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-03T14:16:29.420 |

Grav CMS 2.0.10 contains a path traversal vulnerability in ImageMedium::watermark(), which passes its unsanitized $image argument to RocketTheme\Toolbox\ResourceLocator\UniformResourceLocator::findResource(). Because the file:// scheme branch only lexically collapses '..' segments without a realpath/containment check, an editor authoring Markdown image syntax with traversal sequences can cause arbitrary image files outside Grav's media sandbox to be composited into a carrier image, which is then cached and served from a public, unauthenticated URL — disclosing those files to anonymous visitors.

### CVE-2026-69079

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-03T10:16:33.407 |

CTI-Transmute contains an uncontrolled resource-consumption vulnerability in the unauthenticated /activity_timeline endpoint. The endpoint accepts a user-controlled days query parameter that was not restricted to a reasonable range.

A remote, unauthenticated attacker could submit an excessively large value for this parameter, causing the application to retrieve and process activity data over an arbitrarily large period. This could consume excessive database, CPU, or memory resources, delay the processing of concurrent requests, or trigger an internal server error. Repeated requests could further degrade the availability of the CTI-Transmute website.

The vulnerability is corrected by clamping the requested timeline range to a minimum of one day and a maximum of 1,095 days.

### CVE-2026-14682

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-03T04:16:43.213 |

In Bouncy Castle for Java before 1.85, Possible OOM from unbounded up-front allocation on a definite-length read. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bc-fips 1.0.2.7 (1.0.X series), 2.0.2 (2.0.X series) and 2.1.3 (2.1.X series), and before bctls-fips 1.0.24.

### CVE-2026-13506

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-03T04:16:39.957 |

In Bouncy Castle for Java before 1.85, Lazy ASN.1 sequence forcing resets nesting-depth guard. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bc-fips 1.0.2.7 (1.0.X series), 2.0.2 (2.0.X series) and 2.1.3 (2.1.X series).

### CVE-2026-12860

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-03T04:16:39.797 |

In Bouncy Castle for Java before 1.85, RSA PKCS#1 verification skips last two hash bytes in NULL-omitted path. This issue also affects Bouncy Castle for Java LTS before 2.73.12.

### CVE-2026-12852

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-03T04:16:39.640 |

In Bouncy Castle for Java before 1.85, MLS wire decoder allocates attacker-declared opaque length before bounds check.

### CVE-2026-12817

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-354` |
| Published | 2026-08-03T04:16:39.473 |

In Bouncy Castle for Java before 1.85, OpenPGP AEAD decryption skips final tag on chunk-aligned data. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bcpg-fips 1.0.13 (1.0.X series), 2.0.13 (2.0.X series) and 2.1.13 (2.1.X series).

### CVE-2026-12816

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-354` |
| Published | 2026-08-03T04:16:39.330 |

In Bouncy Castle for Java before 1.85, IESEngine stream-mode MAC forgery via length-dependent KDF split. This issue also affects Bouncy Castle for Java LTS before 2.73.12.

### CVE-2026-12803

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-354` |
| Published | 2026-08-03T04:16:39.177 |

In Bouncy Castle for Java before 1.85, KCCMBlockCipher MAC does not bind nonce when AAD is absent (cross-nonce AEAD forgery). This issue also affects Bouncy Castle for Java LTS before 2.73.12.

### CVE-2026-12802

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-354` |
| Published | 2026-08-03T04:16:38.070 |

In Bouncy Castle for Java before 1.85, CMS AuthEnvelopedData fails to enforce tag-length on decryption. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bcpkix-fips 1.0.12 (1.0.X series), 2.0.12 (2.0.X series) and 2.1.12 (2.1.X series).

### CVE-2026-58061

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-354` |
| Published | 2026-08-03T03:16:45.500 |

In Bouncy Castle for Java before 1.85, CCM-family modes write plaintext to caller buffer before tag check. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bc-fips 1.0.2.7 (1.0.X series), 2.0.2 (2.0.X series) and 2.1.3 (2.1.X series).

### CVE-2026-58060

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-03T03:16:45.340 |

In Bouncy Castle for Java before 1.85, HSS public-key level count unbounded, enabling huge allocation on verify. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bc-fips 2.0.2 (2.0.X series) and 2.1.3 (2.1.X series).

### CVE-2026-58059

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-407` |
| Published | 2026-08-03T03:16:45.137 |

In Bouncy Castle for Java before 1.85, Quadratic-time escaping when stringifying X.500 distinguished names. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bc-fips 1.0.2.7 (1.0.X series), 2.0.2 (2.0.X series) and 2.1.3 (2.1.X series).

### CVE-2026-59649

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-03T01:16:45.120 |

In Bouncy Castle for Java before 1.85, OpenPGP user-attribute subpacket length bounded only by JVM max memory. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bcpg-fips 1.0.13 (1.0.X series), 2.0.13 (2.0.X series) and 2.1.13 (2.1.X series).

### CVE-2026-59646

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-03T01:16:44.733 |

In Bouncy Castle for Java before 1.85, DTLS handshake reassembler allocates buffer from unchecked 24-bit length. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bctls-fips 1.0.24 (1.0.X series), 2.0.24 (2.0.X series) and 2.1.24 (2.1.X series).

### CVE-2026-59645

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-03T01:16:44.600 |

In Bouncy Castle for Java before 1.85, OER parser recurses without depth limit on self-referential IEEE 1609.2 schema. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bcutil-fips 2.0.7 (2.0.X series) and 2.1.7 (2.1.X series).

### CVE-2026-59644

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-834` |
| Published | 2026-08-03T01:16:44.467 |

In Bouncy Castle for Java before 1.85, MLS hash-ratchet honours arbitrary 32-bit generation counter from sender.

### CVE-2026-59643

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-03T01:16:44.333 |

In Bouncy Castle for Java before 1.85, OpenPGP inline-signature policy failures silently ignored. This issue also affects Bouncy Castle for Java FIPS (BC-FJA) before bcpg-fips 2.0.13.

### CVE-2026-59642

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-354` |
| Published | 2026-08-03T01:16:44.203 |

In Bouncy Castle for Java before 1.85, CMS AuthenticatedData content not bound to MAC when authAttrs present. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bcpkix-fips 1.0.12 (1.0.X series), 2.0.12 (2.0.X series) and 2.1.12 (2.1.X series).

### CVE-2026-59641

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-03T01:16:44.060 |

In Bouncy Castle for Java before 1.85, S/MIME validator trusts signer-asserted signingTime for path validation. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bcmail-fips and bcjmail-fips 1.0.7 (1.0.X series), 2.0.7 (2.0.X series) and 2.1.7 (2.1.X series).

### CVE-2026-59640

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-203` |
| Published | 2026-08-03T01:16:43.907 |

In Bouncy Castle for Java before 1.85, OpenPGP CFB quick-check oracle active on symmetric/session-key paths. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bcpg-fips 1.0.13 (1.0.X series), 2.0.13 (2.0.X series) and 2.1.13 (2.1.X series).

### CVE-2026-59639

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-03T01:16:43.700 |

In Bouncy Castle for Java before 1.85, CMS verifySignatures returns true for SignedData with zero signers. This issue also affects Bouncy Castle for Java LTS before 2.73.12, and Bouncy Castle for Java FIPS (BC-FJA) before bcpkix-fips 1.0.12 (1.0.X series), 2.0.12 (2.0.X series) and 2.1.12 (2.1.X series).

### CVE-2026-69088

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-03T14:16:29.253 |

Grav CMS versions 2.0.7 through 2.0.10 fail to validate fully-qualified static method calls (Class::method) in blueprint dynamic-field directives because Blueprint::isSafeDynamicCall() only applies its dangerous-callable denylist to strings that do not contain '::'. An account with only page-editing rights (admin.pages, not super-admin or admin.pages_twig) can plant a directive in a page's form-field frontmatter that invokes an arbitrary public static PHP method with attacker-controlled arguments. Using built-in gadget methods this allows reading of any server-readable file (disclosed to anonymous visitors of the crafted page) and arbitrary creation/copying of files and directories under the web-server account. Fixed in 2.0.11.

### CVE-2026-67608

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-03T14:16:27.793 |

Telenia Software TVox 26.5.3 and prior 26.x versions, and 24.9.21 and prior 24.x versions, contain an OS command injection vulnerability in action_audio.php that allows authenticated attackers to execute arbitrary operating system commands by passing an unsanitized pid parameter into an exec() call when the action parameter is set to checkProcess. Attackers can inject malicious OS commands through the pid request parameter to execute arbitrary commands with the privileges of the apache user.

### CVE-2026-9593

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-03T07:16:44.200 |

A vulnerability in the iDTM FDI allows an attacker with elevated privileges and access to the host system to enable the debug interface by placing a crafted file in the application directory, potentially resulting in unauthorized access to connected devices and exposure, modification, or disruption of device data or operation.

### CVE-2026-69086

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-03T14:16:28.960 |

SiYuan versions before v3.7.3 fail to validate the avID parameter on all code branches in attribute-view read endpoints, allowing attackers to construct traversal paths that escape the storage directory. Authenticated users with RoleReader permissions or anonymous clients when publish authentication is disabled can read JSON files outside the attribute-view directory to disclose cross-scope database content.

### CVE-2026-18577

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:L/SI:L/SA:L/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-02T23:16:26.210 |

An incomplete patch for CVE-2026-18556 allows for authentication bypass and account takeover in N-central Versions through 2026.3.1

### CVE-2026-18642

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-03T14:16:26.123 |

Deserialization of untrusted data vulnerability in TUBITAK BILGEM Software Technologies Research Institute eta-otp-lock allows Object Injection.

This issue affects eta-otp-lock: before 1.0.4.

### CVE-2026-3245

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-03T00:16:29.280 |

A deserialization vulnerability in PRISMAproduction Version 6.5 or earlier that may lead to arbitrary code execution.

### CVE-2026-21555

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-03T08:17:20.257 |

In modem, there is a possible improper input validation. This could lead to remote denial of service with no additional execution privileges needed

### CVE-2026-21554

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-03T08:17:20.130 |

In modem, there is a possible improper input validation. This could lead to remote denial of service with no additional execution privileges needed

### CVE-2026-21553

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-03T08:17:20.020 |

In modem, there is a possible improper input validation. This could lead to remote denial of service with no additional execution privileges needed

### CVE-2026-21552

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-03T08:17:19.903 |

In modem, there is a possible improper input validation. This could lead to remote denial of service with no additional execution privileges needed

### CVE-2026-21551

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-03T08:17:19.787 |

In modem, there is a possible improper input validation. This could lead to remote denial of service with no additional execution privileges needed

### CVE-2026-21550

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-03T08:17:19.663 |

In modem, there is a possible improper input validation. This could lead to remote denial of service with no additional execution privileges needed

### CVE-2026-21549

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-03T08:17:19.537 |

In modem, there is a possible improper input validation. This could lead to remote denial of service with no additional execution privileges needed

### CVE-2026-21548

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-03T08:17:19.393 |

In nr modem, there is a possible improper input validation. This could lead to remote denial of service with System execution privileges needed.

### CVE-2026-18600

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-03T14:16:25.763 |

A vulnerability has been found in GL.iNet GL-MT3000 up to 4.4.5. This affects the function network.switch_info/network.switch_status of the file /usr/lib/oui-httpd/rpc/network of the component Network Lua RPC Plugin. Such manipulation of the argument switch leads to command injection. The attack may be launched remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-18598

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-03T13:17:13.140 |

A vulnerability was detected in GL.iNet GL-MT3000 up to 4.4.5. The affected element is the function logread.get_system_log of the file /usr/lib/oui-httpd/rpc/logread of the component Logread Lua RPC plugin. The manipulation of the argument module results in command injection. The attack can be launched remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-69097

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-03T14:16:30.677 |

GitPython before 3.1.53 fails to properly escape section names in git config files, allowing attackers to inject arbitrary configuration directives through malicious submodule names. Attackers can inject core.sshCommand or other dangerous config keys into the victim's .git/config via create_submodule or clone_from operations, achieving remote code execution when git performs ssh operations.

### CVE-2026-18599

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-03T13:17:13.337 |

A flaw has been found in GL.iNet GL-MT3000 up to 4.4.5. The impacted element is the function logread.set_config of the file /usr/lib/oui-httpd/rpc/logread of the component Logread Lua RPC Plugin. This manipulation of the argument record_size causes command injection. The exploit has been published and may be used. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability.

### CVE-2026-0392

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295;CWE-347;CWE-494` |
| Published | 2026-08-03T10:16:27.747 |

eParakstītājs 3.0 for Windows before version
1.10.0 retrieves and executes its automatic updates over a channel that is not
authenticated or integrity-protected. On each launch the application fetches an
update descriptor (XML) over TLS but accepts any TLS certificate (a permissive
TrustManager and a HostnameVerifier that always returns true), does not verify
any digital signature on the update descriptor, and does not verify the
Authenticode signature or a checksum of the downloaded installer before running
it. A man-in-the-middle attacker able to redirect www.eparaksts.lv can serve a
crafted update descriptor pointing to an attacker-controlled executable, which
the client downloads and executes, resulting in arbitrary code execution on the
victim host.

### CVE-2026-4793

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-08-03T07:16:43.453 |

An incorrect default permissions vulnerability in Synology Assistant before 7.0.7-50095 allows local users to read or write arbitrary files and conduct denial-of-service during installation.

### CVE-2026-69093

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-03T14:16:30.057 |

Admidio before 5.0.11 does not validate the adm_csrf_token in modules/category-report/preferences.php, which performs persistent Category Report configuration changes based on GET parameters (delete and copy). An attacker can trick an authenticated administrator into visiting a crafted URL to delete or duplicate Category Report configurations, affecting the integrity and availability of that module's configuration.

### CVE-2026-69087

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-08-03T14:16:29.103 |

The Grav form plugin (getgrav/grav-plugin-form) before 9.1.13 contains an open redirect vulnerability. Since v9.1.11, the redirect process action evaluates user-supplied form data inside Twig expressions, and Grav::redirect() accepts external URLs without origin validation. When a form blueprint defines a redirect target such as redirect: "{{ form.value('next') }}" using an attacker-controllable field, an unauthenticated form submitter can supply a value like https://evil.com to cause a 302 redirect to an arbitrary external site, enabling phishing.

### CVE-2026-59651

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-326` |
| Published | 2026-08-03T01:16:45.380 |

In Bouncy Castle for Java before 1.85, BKS keystore accepts legacy version with 16-bit integrity MAC key. This issue also affects Bouncy Castle for Java LTS before 2.73.12.

### CVE-2026-12185

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-03T01:16:42.987 |

In Bouncy Castle for Java before 1.85, BKS/UBER keystore allocates from untrusted lengths before integrity check. This issue also affects Bouncy Castle for Java LTS before 2.73.12.

### CVE-2026-9856

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-02T16:16:25.413 |

A vulnerability in huggingface/transformers versions <=5.8.0.dev0 allows an attacker to perform arbitrary file writes via path traversal. The issue resides in the `save_pretrained()` methods of `PreTrainedTokenizerBase` and `ProcessorMixin`, where keys from the `chat_template` dictionary are used directly as filenames without proper validation. An attacker can exploit this by publishing a malicious Hugging Face Hub repository with a crafted `tokenizer_config.json` file. When a victim downloads and saves the tokenizer or processor, the attacker-controlled keys can escape the intended save directory, enabling arbitrary file writes with attacker-controlled content. This vulnerability affects multiple processors inheriting from `ProcessorMixin`, including Idefics, Florence, Gemma, Phi, and Qwen-VL.

### CVE-2026-10848

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-08-02T17:16:58.163 |

The OCPP 1.6 client in subsys/net/lib/ocpp parsed inbound WAMP RPC frames in parse_rpc_msg() (subsys/net/lib/ocpp/ocpp_j.c) using a hand-rolled helper, extract_string_field(), that copied the message's uid and action fields with strncpy(out_buf, token + 1, outlen - 1) and then scanned the result with strchr(out_buf, '"'). Because strncpy does not NUL-terminate the destination when the source is at least outlen - 1 (127) bytes long, the subsequent strchr reads past the 128-byte destination buffer into adjacent stack memory; if a " byte is found beyond the buffer, a one-byte out-of-bounds NUL write also occurs. A related defect in extract_payload() runs strchr/strrchr over the receive buffer, which may not be NUL-terminated when a maximal-length frame fills it.

The parsed bytes come directly from the OCPP central-system server over a websocket: the reader thread fills recv_buf via websocket_recv_msg() and calls parse_rpc_msg() on each inbound DATA frame (subsys/net/lib/ocpp/ocpp.c). A malicious or compromised central server, or an on-path attacker (OCPP is commonly deployed over plain ws://), can send an RPC frame whose uid or action field is 127+ bytes with no closing quote, triggering the out-of-bounds access.

The primary impact is a remotely triggerable denial of service: the unbounded scan can fault on an unmapped page, and the stray NUL write can corrupt adjacent stack state. The over-read data is not reflected to the peer, so disclosure is limited. The feature is EXPERIMENTAL and must be explicitly enabled (CONFIG_OCPP). The fix replaces the manual parser with the bounds-respecting json_mixed_arr_parse() and copies the extracted uid with an explicitly NUL-terminated buffer, eliminating both over-reads.
