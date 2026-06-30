# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-30 15:00 UTC
- **対象期間**: `2026-06-29T15:00:23.000Z` 〜 `2026-06-30T15:00:27.000Z`
- **重要CVE数**: 98 件（Critical 9.0+: 20 件 / High 7.0〜: 78 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE のうち **CVSS 7.0 以上** が 30 件以上報告され、特に **Web アプリケーション（WordPress・Joomla 等）** と **インフラ系コンポーネント（Rancher、NetScaler、Apache Tomcat）** に集中しています。  
- 最高スコア **10.0**（CVE‑2026‑56290）をはじめ、**リモートコード実行 (RCE)**、**特権昇格**、**SQL インジェクション** が多数で、攻撃者が認証なしにシステム全体を制御できるケースが目立ちます。  
- 多くは **プラグインや古いバージョンのデフォルト設定** が原因であり、**即時のパッチ適用** と **設定見直し** が最優先です。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な脆弱性種別 | 影響範囲・被害シナリオ | 推奨される対策（概要） |
|-----|--------|----------------|------------------------|------------------------|
| **CVE‑2026‑56290** | **10.0** | 任意ファイルアップロード → 完全リモートコード実行 | Joomla 拡張 **Page Builder CK** が認証不要で任意の実行ファイルをアップロード可能。攻撃者はサーバ上で任意コードを実行し、Web サイト全体を乗っ取れる。 | 1. **Page Builder CK 5.2.1 以降** にアップデート  <br>2. 不要な拡張は即削除、アップロードディレクトリの実行権限を無効化 |
| **CVE‑2026‑57331** | **9.9** | 任意ファイル削除（特権操作） | **Paid Videochat Turnkey Site** ≤ 7.4.8 で、認証済みユーザーが任意のファイルを削除できる。動画配信サービスのデータ破壊やサービス停止につながる。 | 1. **7.4.9 以上** にアップグレード <br>2. ファイル削除 API のアクセス制御を厳格化 |
| **CVE‑2026‑8402** | **9.8** | Blind SQL Injection | **SYSGUARD 6001** (2.0.2‑6.1.15) の管理画面で盲目的に SQL を注入可能。データベース情報漏洩や改ざんが起こり得る。 | 1. **6.1.16.0 以降** に更新 <br>2. データベース接続にプリペアドステートメントを使用し、入力検証を徹底 |
| **CVE‑2026‑44946** | **9.5** | SAML Assertion Replay（認証再利用） | **Rancher 2.14.0‑2.14.2** の ACS ハンドラが一度きりの使用を強制しないため、MITM 攻撃で認証情報を再利用できる。クラスタ全体の権限が奪取される危険性がある。 | 1. **Rancher 2.14.3 以降** にアップデート <br>2. SAML 設定で **One‑Time Use** を有効化 |
| **CVE‑2026‑58116** | **9.3** | RCE via malicious model path | **LLaMA‑Factory ≤ 0.9.5** の Web UI で、モデルパスに任意の Python スクリプトを指定でき、サーバ上でコードが実行される。機密データ取得やマイニングに悪用可能。 | 1. **0.9.6 以降** に更新 <br>2. Web UI へのアクセスを認証済みユーザーに限定し、モデルパス入力をホワイトリスト化 |

> **注**：上記はスコアが高いだけでなく、**攻撃者が認証不要でシステム全体を制御できる**、あるいは **インフラ基盤全体に波及する** という点で特に危険です。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンの即時更新
| 製品 / プラグイン | 現行脆弱バージョン | 推奨バージョン |
|-------------------|-------------------|----------------|
| Joomla – Page Builder CK | 任意（≤ 5.2.0） | **5.2.1 以降** |
| Paid Videochat Turnkey Site | ≤ 7.4.8 | **7.4.9 以上** |
| SYSGUARD 6001 | 2.0.2‑6.1.15 | **6.1.16.0 以降** |
| Rancher (ACS) | 2.14.0‑2.14.2 | **2.14.3 以降** |
| Rancher (Privilege Escalation) | 2.12.0‑2.12.9, 2.13.0‑2.13.5, 2.14.0‑2.14.1 | **2.12.10, 2.13.6, 2.14.2 以降** |
| LLaMA‑Factory | ≤ 0.9.5 | **0.9.6 以降** |
| Coolify (Auth RCE) | < 4.0.0‑beta.470 | **4.0.0‑beta.470 以降** |
| Apache Tomcat | 9.0.83‑9.0.118, 10.1.0‑10.1.55, 11.0.0‑11.0.22 | **9.0.119 以降、10.1.56 以降、11.0.23 以降** |
| NetScaler ADC / Gateway | すべての 8.8 系脆弱バージョン | **最新安定版（リリースノート参照）** |

### 3.2 設定・運用上のベストプラクティス
1. **最小権限の原則**  
   - Web アプリや API の管理者ロールを必要最小限に絞り、特権ロール（Project Owner 等）は監査ログを必ず取得。  
2. **ファイルアップロード・実行権限の制御**  
   - `upload_tmp_dir` やプラグインが生成するディレクトリに **実行権限 (chmod 0644)** を付与しない。  
   - MIME タイプと拡張子のホワイトリストを徹底。  
3. **入力検証とプリペアドステートメント**  
   - すべての SQL クエリは **パラメータ化クエリ** を使用し、ユーザー入力はサニタイズ／エスケープ。  
   - 特に `search`、`userEmail`、`model path` などフリーテキスト入力は正規表現で制限。  
4. **SAML / OIDC 設定の強化**  
   - Assertion の **One‑Time Use**、**Replay Protection**、**Audience Restriction** を必ず有効化。  
   - IdP と SP の証明書有効期限を自動監視し、期限切れ前にローテーション。  
5. **ネットワーク境界の分離**  
   - PLC（Delta DVP12SE）や Modbus TCP サービスは **内部 VLAN** に配置し、外部からの直接アクセスを防止。  
   - 必要な場合は **IP ホワイトリスト** と **TLS 終

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-56290

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:Red` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-29T15:16:42.360 |

The Joomla extension Page Builder CK is vulnerable to an unauthenticated arbitrary file upload that allows uploading executable files and leads to full RCE.

### CVE-2026-57331

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-29T15:16:43.370 |

Performer Arbitrary File Deletion in Paid Videochat Turnkey Site <= 7.4.8 versions.

### CVE-2026-8402

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-30T12:16:26.613 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Eksagate Electronic Engineering and Computer Industry Trade Inc. SYSGUARD 6001 allows Blind SQL Injection.

This issue affects SYSGUARD 6001: from 2.0.2 before 6.1.16.0. 
NOTE: The vendor was contacted and it was learned that the product is not supported.

### CVE-2026-9711

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-30T10:16:37.350 |

The EventON - WordPress Virtual Event Calendar Plugin plugin for WordPress (full) is vulnerable to SQL Injection via the WordPress 'search' parameter in versions up to, and including, 5.0.11 due to insufficient escaping on the user supplied parameter and lack of preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database, granted the "Enable additional search queries" setting is enabled and at least one published event exists.

### CVE-2026-12073

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-30T06:16:26.560 |

The ProfileGrid – User Profiles, Groups and Communities plugin for WordPress is vulnerable to privilege escalation via account takeover in all versions up to, and including, 5.9.9.5. This is due to the plugin not validating a `user_login` on registration forms that don't contain this parameter, and not properly handling the error messages. This makes it possible for unauthenticated attackers to change email address of user account with ID=1 (usually an administrator), and leverage that to reset the user's password and gain access to their account.

### CVE-2026-57498

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-06-29T20:17:40.013 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.474, Coolify's API controllers consistently validate server ownership with Server::whereTeamId($teamId) before any operation. However, multiple Livewire web UI components accept server_id and destination_uuid from URL query parameters without any team ownership validation, allowing cross-team resource deployment. This vulnerability is fixed in 4.0.0-beta.474.

### CVE-2026-44946

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-06-30T13:18:42.190 |

A SAML authentication replay vulnerability in Rancher's Assertion
 Consumer Service (ACS) handler did not enforce 
one-time use of SAML assertion, potentially allowing person in the middle attacks against Rancher, affecting Rancher 2.14.0 before 2.14.3,

### CVE-2026-41052

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-305` |
| Published | 2026-06-29T16:16:39.870 |

Improper privilege handling could be used by users with Project Owner role to escalate privileges, in Rancher versions 2.14 before 2.14.2, 2.13 before 2.13.6, and 2.12 before 2.12.10.

### CVE-2026-58116

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-829` |
| Published | 2026-06-30T13:19:18.490 |

LLaMA-Factory through 0.9.5 contains a remote code execution vulnerability that allows attackers with WebUI access to execute arbitrary Python code by supplying a malicious model path in the Chat or Training interfaces. The application passes user-supplied model path input unvalidated into AutoTokenizer.from_pretrained() and AutoModel.from_pretrained() with a hardcoded trust_remote_code=True parameter, causing the Hugging Face transformers library to fetch and execute arbitrary code from a remote or local model repository with the privileges of the server process.

### CVE-2026-53690

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-30T12:16:24.403 |

An SQL Injection vulnerability exists in Redeight CMS version 1.0 via the "userEmail" parameter in the POST "/admin/index.php" login endpoint. The application fails to sanitize user input and directly interpolates it into SQL queries without using prepared statements, which allows unauthenticated remote attackers to execute arbitrary SQL commands and extract sensitive database information.

### CVE-2026-14162

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-30T12:16:23.440 |

Hospital Queuing Management developed by Advantech has a Sensitive Data Exposure vulnerability, allowing unauthenticated remote attackers to access a specific URL to obtain API documentation.

### CVE-2026-12076

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-30T10:16:34.260 |

Raytha CMS is vulnerable to SQL Injection within the OData filter parsing pipeline.  The vulnerability allows a remote, unauthenticated attacker to execute 
arbitrary SQL statements against the underlying PostgreSQL database, 
leading to full database compromise, including credential extraction.

Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version 1.5.2 but may also affect other versions.

### CVE-2026-12819

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-30T07:16:32.060 |

Delta Electronics DVP12SE PLC exposes a Modbus TCP service over a specified port without authentication or access control, permitting unauthenticated interaction with security-sensitive PLC functions.

### CVE-2026-12818

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-06-30T07:16:31.933 |

Delta Electronics DVP12SE PLCs are susceptible to a resource allocation vulnerability without limits or throttling (CWE-770) within their Modbus TCP service.

### CVE-2026-56782

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-29T18:16:38.817 |

Gorse before 0.5.10 contains an authentication bypass vulnerability in the /api/dump and /api/restore endpoints that allows unauthenticated attackers to access protected functionality when admin_api_key is empty, which is the default configuration. Remote attackers can exfiltrate the entire database including user records, items, and feedback data containing personally identifiable information, or completely overwrite the dataset without authentication.

### CVE-2026-11720

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-29T18:16:36.173 |

A path traversal vulnerability exists in the HTTP tool URL builder of googleapis/mcp-toolbox.

When constructing downstream API requests, the URL builder substitutes user-controlled pathParams into the configured tool path and parses the resulting string as a relative URL. While it checks that the input does not alter the scheme, host, or user info, it relies on ResolveReference for the final URL resolution. Because dot segments (../) are normalized during this resolution step, an attacker can supply path parameters containing directory traversal sequences to escape the operator-configured path scope. This allows the client to coerce the toolbox into making requests to unintended endpoints on the same target host while forwarding the toolbox's configured credentials (e.g., bypassing a restricted path like /api/v1/users/{{.id}} to reach /admin/secrets).

### CVE-2026-6556

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-06-30T13:19:25.467 |

@fastify/express versions 4.0.6 and earlier only rewrite the plugin prefix for middleware mount paths when the path argument is a string. Non-string mount paths (arrays of paths and regular expressions) are left unprefixed inside prefixed plugin scopes, so middleware registered with those forms does not match the actual prefixed request path. Applications that use path-scoped middleware for authentication, authorization, rate limiting, or auditing on routes inside a prefixed scope can be bypassed by sending a request to the prefixed route, because Fastify still matches the route but the middleware is skipped. Patches: upgrade to @fastify/express 4.0.7. Workarounds: use string mount paths instead of arrays or regular expressions in prefixed plugins, or register one use call per path.

### CVE-2026-53434

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-390` |
| Published | 2026-06-29T21:16:44.937 |

Detection of Error Condition Without Action vulnerability in Apache Tomcat when configuring CRLs for a FFM based connector.

This issue affects Apache Tomcat: from 11.0.0-M1 through 11.0.22, from 10.1.0-M7 through 10.1.55, from 9.0.83 through 9.0.118.

Users are recommended to upgrade to version 11.0.23, 10.1.56 or 9.0.119, which fixes the issue.

### CVE-2026-39868

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-29T20:17:33.930 |

This issue was addressed with improved input validation. This issue is fixed in iOS 26.5.2 and iPadOS 26.5.2, macOS Tahoe 26.5.2. An app may be able to cause unexpected system termination or corrupt kernel memory.

### CVE-2026-37637

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-29T20:17:33.820 |

An issue in Alexantr filemanager v.1.0 allows a remote attacker to execute arbitrary code via the filemanager.php component

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-8655

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-06-30T13:19:34.083 |

Multiple Memory overflow vulnerabilities in NetScaler ADC and NetScaler Gateway leading to unpredictable or erroneous behavior and Denial of Service if NetScaler ADC is configured as an LB of type Oracle OR NetScaler ADC is configured as a DNS Proxy OR NetScaler ADC is configured as a DNS recursive resolver deployment

### CVE-2026-8452

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-06-30T13:19:33.450 |

Memory overflow vulnerability NetScaler ADC and NetScaler Gateway leading to unpredictable or erroneous behavior and Denial of Service if the appliance is configured as a Gateway (SSL VPN, ICA Proxy, CVPN, RDP Proxy) or AAA virtual server

### CVE-2026-8451

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-30T13:19:33.347 |

Insufficient input validation in NetScaler ADC and NetScaler Gateway leading to memory overread if NetScaler ADC or NetScaler Gateway is configured as a SAML IDP

### CVE-2026-41053

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-303` |
| Published | 2026-06-30T12:16:23.580 |

Incorrect authentication caching in the team member ship expansion of the Rancher Github authentication provider caused it granting principal access to any logged in user, in 2.13 before 2.13.6 and 2.14 before 2.14.2.

### CVE-2026-11589

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-30T07:16:31.627 |

The WP Support Plus Responsive Ticket System WordPress plugin through 9.1.2 does not properly validate uploaded files, allowing unauthenticated users to upload files containing malicious JavaScript (such as HTML or SVG) to a publicly accessible location, leading to Stored Cross-Site Scripting attacks against site users and administrators.

### CVE-2026-34597

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-29T21:16:43.993 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.470, a critical Authenticated Host Remote Code Execution (RCE) vulnerability was discovered in Coolify. The flaw resides in the handling of user-defined build parameters for the Nixpacks build pack. Specifically, the install_command provided by a user is directly concatenated into a shell command string that is executed on the deployment host during the building phase. An attacker can leverage this to escape the intended build context and execute arbitrary commands with host-level privileges. This vulnerability is fixed in 4.0.0-beta.470.

### CVE-2026-34594

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-29T21:16:43.840 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, an authenticated command injection vulnerability in the Destination Network Management functionality allows users with destination management permissions to execute arbitrary commands as root on managed servers. The "network" parameter is passed directly to shell commands without proper sanitization, enabling full remote code execution on the host system. This vulnerability is fixed in 4.0.0-beta.471.

### CVE-2026-43731

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-29T20:17:37.220 |

A use-after-free issue was addressed with improved memory management. This issue is fixed in Safari 26.5.2, iOS 26.5.2 and iPadOS 26.5.2, macOS Tahoe 26.5.2. Processing maliciously crafted web content may lead to memory corruption.

### CVE-2026-43715

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-29T20:17:36.173 |

A use-after-free issue was addressed with improved memory management. This issue is fixed in Safari 26.5.2, iOS 26.5.2 and iPadOS 26.5.2, macOS Tahoe 26.5.2. Processing maliciously crafted web content may lead to memory corruption.

### CVE-2026-43705

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-06-29T20:17:35.467 |

A type confusion issue was addressed with improved checks. This issue is fixed in Safari 26.5.2, iOS 26.5.2 and iPadOS 26.5.2, macOS Tahoe 26.5.2. Processing maliciously crafted web content may lead to memory corruption.

### CVE-2026-13749

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-29T16:16:39.640 |

Improper neutralization in the Snowpark annotation processor callback template in Snowflake CLI versions prior to 3.19 allowed arbitrary code execution during application bundling or deployment. An attacker could exploit this by supplying crafted project content that is interpolated into generated Python code, causing Snowflake CLI to execute attacker-controlled code in the local context of the user running the CLI. Successful exploitation requires the victim to run the relevant bundling or deployment workflow against attacker-controlled project content, and any resulting code runs with the privileges of that local execution context. The fix is available in Snowflake CLI version 3.19, and users must manually upgrade.

### CVE-2026-13474

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-06-30T13:17:09.610 |

Denial of service via malformed HTTP/2 requests in NetScaler ADC and NetScaler Gateway if HTTP/2 is enabled in HTTP Profile and associated with the virtual server (of type LB, CS, VPN) or the service configured on NetScaler

### CVE-2026-14161

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-30T12:16:23.293 |

Hospital Quening Management developed by Advantech has a Sensitive Data Exposure vulnerability, allowing unauthenticated remote attackers to access a specific URL to obtain API documentation.

### CVE-2026-58000

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-29T19:16:42.993 |

luci-proto-openvpn through 0.11.1, fixed in commit e4ff45e, contains a command injection vulnerability in the generateKey ubus method where the cl_meta parameter is interpolated into a shell command without proper escaping or quoting. An authenticated LuCI user with OpenVPN protocol configuration access can inject arbitrary shell metacharacters into cl_meta to execute commands as root via the popen function.

### CVE-2026-56124

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-359;CWE-497` |
| Published | 2026-06-29T15:16:42.217 |

phpUploader before 2.0.2 contains an unauthenticated information disclosure vulnerability that allows remote attackers to access the full contents of the uploaded-files database table by visiting any page of the application. The index model executes an unbounded SELECT query and embeds the complete JSON-encoded result set in an inline script block, exposing uploader IP addresses, Argon2ID key hashes, internal filenames, and SHA-256 fingerprints.

### CVE-2026-53691

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-30T12:16:24.530 |

An Unrestricted File Upload vulnerability in Redeight CMS version 1.0 allows authenticated attackers to achieve Remote Code Execution via the POST "/admin/index.php?module=pages&mode=FileAdd" endpoint. The application fails to validate file extensions and MIME types, permitting the upload of arbitrary PHP scripts to the publicly accessible "/uploads/files/" directory where they can be executed directly by the web server.

### CVE-2026-56808

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-30T07:16:32.620 |

DGM3103SCT provided by AVTECH Security Corporation contains an OS command injection vulnerability, which may lead to arbitrary command execution with the root privilege by a user who can log in to the web management console of the affected product.

### CVE-2026-57950

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-29T18:16:40.130 |

ruoyi-vue-pro through 2026.05, fixed in commit 5d1fd70 contains a broken access control vulnerability in ErpSaleOrderController that allows attackers with erp:sale-out permissions to gain unauthorized access to sale order operations by exploiting an incorrect permission namespace enforcement. Attackers holding shipment-level permissions can perform unauthorized create, update, delete, and read operations on financially sensitive sale orders due to the controller enforcing erp:sale-out instead of the intended erp:sale-order namespace.

### CVE-2026-12578

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-30T09:16:24.267 |

The affected product is vulnerable to a deserialization of untrusted data, which may allow an attacker to execute arbitrary code.

### CVE-2026-56137

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-30T07:16:32.400 |

RPG MAKER MV and MZ provided by Gotcha Gotcha Games Inc. contain an OS command injection vulnerability. If a user loads a specially crafted save-file, arbitrary OS command may be executed.

### CVE-2026-58302

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-30T02:16:26.820 |

rtapi_app in linuxcnc-uspace in LinuxCNC before 2.9.9 allows privilege escalation. It is installed SUID root and loads shared library modules via dlopen() by using a user-supplied module name. Insufficient validation of the module name allows path traversal, enabling an unprivileged local user to load an arbitrary shared library. Because the process retains elevated privileges during module loading, this results in local privilege escalation to root.

### CVE-2026-43701

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-29T20:17:35.173 |

The issue was addressed with improved checks. This issue is fixed in Safari 26.5.2, iOS 26.5.2 and iPadOS 26.5.2, macOS Tahoe 26.5.2. A malicious website may be able to process restricted web content outside the sandbox.

### CVE-2026-57960

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-359` |
| Published | 2026-06-29T18:16:42.130 |

Hi.Events through 1.9.0 public check-in list endpoints use short_id as sole access control, allowing unauthenticated access to retrieve full attendee lists including emails and personal information. Attackers with knowledge of the short_id can call GET /api/public/check-in-lists/{short_id}/attendees to read attendee data and create or delete check-in records without authentication.

### CVE-2026-57955

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-29T18:16:40.817 |

SigNoz through 0.130.1 contains a SQL injection vulnerability that allows authenticated attackers to execute arbitrary ClickHouse queries by injecting URL-encoded quotes into the rule ID path parameter of the alert-history endpoints. Attackers can manipulate the unsanitized rule ID interpolated into ClickHouse queries to read all stored traces, logs, and metrics, or abuse the url() function to perform server-side request forgery.

### CVE-2026-13744

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-29T16:16:39.260 |

Improper neutralization of attacker-controlled content in Snowflake CLI versions prior to 3.19 allowed unintended SQL execution. By supplying crafted repository content, project configuration, manifest data, or specification input, an attacker could cause Snowflake CLI to execute unintended SQL in the context of the victim user's Snowflake session. Successful exploitation requires the victim to process attacker-controlled content through a vulnerable command path and is limited by the privileges assigned to that session. The fix is available in Snowflake CLI version 3.19. Users must manually upgrade.

### CVE-2026-53426

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-06-29T20:17:38.473 |

Allocation of Resources Without Limits or Throttling vulnerability in leandrocp MDEx allows Excessive Allocation.

MDEx.parse_document/2 accepts a {:json, json} source. In lib/mdex.ex, the private json_to_node/1 function passes the attacker-controlled node_type value to Module.concat/1, which calls String.to_atom/1 and interns a brand-new atom for every distinct value. Atoms are never garbage collected on the BEAM, so a crafted JSON document carrying a unique node_type at each (deeply nested) node mints one permanent atom per node.

A single document can intern hundreds of thousands of atoms, and a large enough document exhausts the default atom table (around 1,048,576 atoms) and aborts the entire Erlang VM, taking down every process on the node. Any application that passes untrusted input to the {:json, ...} source of MDEx.parse_document is exposed to an unauthenticated denial-of-service.

This issue affects mdex from 0.4.3 before 0.13.2.

### CVE-2026-57959

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-06-29T18:16:41.997 |

Hi.Events through 1.9.0 contains a promo code validation vulnerability where reservation validates usage count before asynchronous UpdateEventStatisticsJob increments it, allowing attackers to redeem limited promo codes unlimited times. Attackers can sequentially reserve multiple orders with the same restricted promo code, each reading order_usage_count=0 and passing validation, then complete them all at discounted prices without concurrent requests.

### CVE-2026-49877

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-06-30T11:16:29.503 |

Improper Authorization vulnerability in Apache ActiveMQ.

An authenticated low-privilege Web Console user by default can access /admin/* paths in the Web Console. The default Jetty settings incorrectly did not limit those paths to only admins.
This issue affects Apache ActiveMQ: before 5.19.8, from 6.0.0 before 6.2.7.

Users are recommended to upgrade to version 6.2.7 or 5.19.8, which fixes the issue.

### CVE-2026-7656

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-290;CWE-670` |
| Published | 2026-06-29T23:16:43.650 |

The IPv6 Neighbor Discovery handlers in subsys/net/ip/ipv6_nbr.c (handle_ra_input, handle_ns_input, handle_na_input) used an incorrect boolean expression that combined the RFC 4861 validity checks with the ICMPv6 code check using the wrong operator precedence: the form was '((length/hop/source/target checks) && (icmp_hdr-code != 0))'. Because every legitimate ND message carries ICMPv6 code 0, an attacker setting code == 0 (the normal value) caused the entire predicate to evaluate false, so the packet was never dropped and all of the other checks were silently skipped. The bypassed checks include the mandatory Hop Limit == 255 verification (which proves an ND packet originated on-link and was not forwarded) and, for Router Advertisements, the requirement that the source be a link-local address, as well as multicast-target sanity checks. As a result, an adjacent on-link attacker — and, because the Hop-Limit-255 guard is bypassed, potentially a remote/off-link attacker whose packets would otherwise be rejected — can have forged Router Advertisement, Neighbor Solicitation, and Neighbor Advertisement messages accepted. A forged RA lets the attacker reconfigure the victim's default router, on-link prefixes (SLAAC), MTU, reachable/retransmit timers, and (with CONFIG_NET_IPV6_RA_RDNSS) DNS servers, while forged NS/NA enable neighbor-cache poisoning, enabling man-in-the-middle, traffic redirection, and denial of service. The flaw is an input-validation/authentication weakness rather than a memory-safety issue: the underlying packet-parsing primitives (net_pkt_get_data, net_pkt_read, net_pkt_skip) are independently bounds-safe and the validated 'length' is the true buffer length, so skipping the length check causes no out-of-bounds access. The defect has existed since the logic was introduced in 2018 and shipped in all releases through v4.4.0; it is fixed by splitting the condition so any failing check drops the packet.

### CVE-2026-12240

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-30T07:16:31.810 |

The Export User Data plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the unserialize function in all versions up to, and including, 2.2.6. This makes it possible for authenticated attackers, with subscriber-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). Successful exploitation requires an administrator to trigger a user data export while a subscriber-level (or higher) user has stored a crafted serialized XLSXWriter object payload as their display name.

### CVE-2026-13763

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-06-29T20:17:33.283 |

Inconsistent interpretation of HTTP/2 requests in AWS Application Load Balancer with AWS WAF enabled might allow remote actors to bypass AWS WAF managed rule body inspection via crafted HTTP/2 requests that fragment the request body across frames so that only a partial body is inspected. This issue only impacts HTTP/2 ALB target groups.



To remediate this issue, customers should enable the "Inspect after sufficient data" target group configuration associated to an ALB load balancer. Refer to: ( https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html#waf-http2-inspection )

### CVE-2026-13762

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-06-29T20:17:33.123 |

Inconsistent interpretation of HTTP/2 requests in Amazon CloudFront with AWS WAF enabled might allow remote actors to bypass AWS WAF managed rule body inspection via crafted HTTP/2 requests that fragment the request body across frames so that only a partial body is inspected.



This issue was remediated server-side. No customer action is required.

### CVE-2025-7406

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-30T10:16:33.720 |

Nokia MantaRay NM is vulnerable to a sudo privilege escalation vulnerability where a local attacker possessing administrative (local admin) privileges can escalate to full root privileges on the host. Successful exploitation results in root-level access to the filesystem and the ability to execute actions as root. The risk can be temporarily mitigated by restricting the set of commands permitted via sudo for the affected accounts.

### CVE-2025-24815

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-30T10:16:32.473 |

Nokia MantaRay NM is subject to an unrestricted file upload vulnerability due to insufficient file type validation. Successful exploitation could allow an authenticated attacker to upload malicious files onto the system.

### CVE-2026-57919

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276;CWE-426` |
| Published | 2026-06-29T20:17:40.160 |

PBackupVSS.exe in Matrix42 Empirum before 25.5 and 26.x before 26.2 creates a named pipe (\\.\pipe\PBackupVSS) with a DACL that grants GENERIC_READ and GENERIC_WRITE permissions to all authenticated users. A low-privileged local attacker can connect to this pipe and send crafted IPC messages to trigger execution of arbitrary commands with SYSTEM privileges via an untrusted search path. This allows privilege escalation by placing a malicious shadow.exe in a controlled working directory.

### CVE-2026-13149

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:U/V:D/RE:M/U:Amber` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-06-30T10:16:34.560 |

brace-expansion through 5.0.6 is vulnerable to denial of service. The expand() function exhibits exponential-time complexity in the number of consecutive non-expanding '{}' brace groups. An attacker who passes a crafted string to expand(), directly or transitively, can cause significant CPU consumption and event-loop blocking. The max option does not mitigate this, as it bounds the output size rather than the recursion work.

### CVE-2026-34592

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-29T22:16:44.120 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.471, Coolify server and project lookups are not scoped to the current team, allowing any authenticated user to access servers and projects belonging to other teams by specifying their IDs directly. This vulnerability is fixed in 4.0.0-beta.471.

### CVE-2026-57999

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-29T19:16:42.857 |

luci-app-tailscale-community contains a command injection vulnerability in the tailscale.do_login RPC method that allows authenticated users to execute arbitrary commands as root. The vulnerability exists because user-controlled loginserver and loginserver_authkey parameters are improperly quoted within a double-quoted shell command, allowing shell substitutions like $() to be evaluated by the outer shell before argument processing.

### CVE-2026-56780

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-29T18:16:38.550 |

Modoboa before 2.9.0 contains an insecure direct object reference vulnerability in the PUT /api/v1/accounts/{pk}/password/ endpoint that allows domain administrators to change any user's password. Attackers with domain admin privileges can bypass object-level access controls to reset superadmin passwords and achieve full account takeover.

### CVE-2026-56285

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918;CWE-1188` |
| Published | 2026-06-29T18:16:38.410 |

Nitter's /video media proxy endpoint fails to validate target URLs against Twitter/X domains and uses a hardcoded default HMAC key, allowing unauthenticated attackers to compute valid HMACs for arbitrary URLs. Attackers can retrieve HTTP responses from any host reachable by the server, including cloud metadata services and internal network resources.

### CVE-2026-55607

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-59;CWE-78` |
| Published | 2026-06-29T15:16:41.597 |

Claude Code is an agentic coding tool.  From 2.1.38 until 2.1.163, Claude Code's worktree handling allowed creation of worktrees named ".git" and navigation to worktrees outside the sandbox context, enabling git directory confusion attacks. By exploiting symlink manipulation and git fsmonitor execution during worktree operations, an attacker could overwrite files in the user's home directory (such as .zshenv), leading to code execution outside of seatbelt sandbox restrictions. Reliably exploiting this required the user to clone a malicious repository containing prompt injection content and run Claude Code against it. This vulnerability is fixed in 2.1.163.

### CVE-2026-57948

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-614;CWE-1004` |
| Published | 2026-06-29T18:16:39.863 |

Pinpoint through version 3.1.0 contains an insecure session management vulnerability that allows attackers to access the pinpointJwt session cookie due to missing HttpOnly and Secure attributes, enabling JavaScript access via document.cookie and cleartext transmission over HTTP. Attackers can exploit stored or reflected cross-site scripting vulnerabilities to exfiltrate the session token or intercept it through network sniffing to perform session hijacking.

### CVE-2026-58016

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-06-30T13:19:17.840 |

A flaw was found in GLib. A state confusion issue exists in g_dbus_node_info_new_for_xml() in the gio/gdbusintrospection.c file when processing malformed D-Bus introspection XML, specifically with a <node> element nested within other elements like <method>, <signal>, <property> or <arg>. This issue can cause an unsigned integer overflow and lead to an out-of-bounds read, resulting in a denial of service.

### CVE-2026-57080

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-06-30T12:16:25.533 |

Net::BitTorrent versions through 2.0.1 for Perl allow remote memory exhaustion via an uncapped peer-wire message-length prefix.

The peer-wire framing in _process_messages trusts the 4-byte length prefix sent by a connected peer with no upper bound, while receive_data appends every inbound byte to the input buffer. A peer announces a length prefix of up to about 4 GiB and then streams bytes; the decoder waits until the buffer holds the full message before processing it, so the buffer grows without limit.

Peer connections are unauthenticated, so any peer in the swarm exhausts the downloading process's memory. The largest legitimate message is a 16 KiB piece block, so any announced length far above that is anomalous.

### CVE-2026-50750

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-30T11:16:29.933 |

Denial of Service via Out of Memory vulnerability in Apache ActiveMQ Broker, Apache ActiveMQ, Apache ActiveMQ All.

Following the fix for  CVE-2026-49270 an unauthenticated attacker can now cause broker OOM by sending an repeated BrokerInfo commands without sending a ConnectionInfo, until the broker will crash with OOM.
This issue affects Apache ActiveMQ Broker: from 5.19.7 before 5.19.8, from 6.2.6 before 6.2.7; Apache ActiveMQ: from 5.19.7 before 5.19.8, from 6.2.6 before 6.2.7; Apache ActiveMQ All: from 5.19.7 before 5.19.8, from 6.2.6 before 6.2.7.

Users are recommended to upgrade to version 6.2.7, which fixes the issue.

### CVE-2026-50734

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-06-30T11:16:29.827 |

Memory Allocation with Excessive Size Value vulnerability in Apache ActiveMQ Client, Apache ActiveMQ, Apache ActiveMQ All.

An unauthenticated network attacker can cause a broker DoS by sending a crafted WireFormatInfo frame with a malicious large size value. The value is not validate and causes the broker to attempt allocation during pre-auth negotiation which can trigger OOM and crash the broker.
This issue affects Apache ActiveMQ Client: before 5.19.8, from 6.0.0 before 6.2.7; Apache ActiveMQ: before 5.19.8, from 6.0.0 before 6.2.7; Apache ActiveMQ All: before 5.19.8, from 6.0.0 before 6.2.7.

Users are recommended to upgrade to version 6.2.7 or 5.19.8, which fixes the issue.

### CVE-2026-49434

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-30T11:16:29.400 |

Improper Input Validation vulnerability in Apache ActiveMQ Broker, Apache ActiveMQ, Apache ActiveMQ All.

An attacker that has access to publish or modify entries in LDAP that match the configured searchBase and searchFilter can instantiate denied transports inside the broker JVM. This can be used to fetch an attacker URL and spawn a second BrokerService inside the same JVM.
This issue affects Apache ActiveMQ Broker: before 5.19.8, from 6.0.0 before 6.2.7; Apache ActiveMQ: before 5.19.8, from 6.0.0 before 6.2.7; Apache ActiveMQ All: before 5.19.8, from 6.0.0 before 6.2.7.


Users are recommended to upgrade to version 6.2.7 or 5.19.8, which fixes the issue.

### CVE-2026-14164

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-06-30T07:16:32.170 |

A double free issue has been identified in libarchive's RAR5 reader. During parsing of a specially crafted RAR5 archive, the filtered_buf pointer may remain stale after being freed during unpacking state reinitialization. Subsequent processing of another archive entry can trigger a second free of the same memory region, resulting in a double-free condition. Successful exploitation may cause applications using the vulnerable libarchive API to terminate unexpectedly, leading to a denial of service.

### CVE-2026-12243

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-30T01:16:29.063 |

NLTK version 3.9.4 is vulnerable to a path traversal attack due to an incomplete fix for GitHub Issue #3504. The `_UNSAFE_NO_PROTOCOL_RE` regex in `nltk/data.py` checks for literal `../` sequences but fails to account for percent-encoded traversal sequences such as `..%2f`. The `url2pathname()` function decodes these sequences after the validation step, allowing an attacker to bypass the protection. This vulnerability enables an attacker to read arbitrary files accessible to the Python process by controlling the resource name parameter passed to `nltk.data.load()` or `nltk.data.find()`. The issue affects applications that rely on NLTK for resource loading, including NLP web applications, Jupyter notebooks, and CLI tools. The default `pathsec.ENFORCE=False` setting exacerbates the impact by not blocking the file read at the `open()` stage.

### CVE-2026-8023

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-23` |
| Published | 2026-06-29T23:16:43.777 |

Zephyr's HTTP server (subsys/net/lib/http) provides a static-filesystem resource type (HTTP_RESOURCE_TYPE_STATIC_FS, available when CONFIG_FILE_SYSTEM is enabled) that serves files from a configured root directory. Before this fix, both the HTTP/1 and HTTP/2 front-ends placed the raw, attacker-controlled request path into client-url_buffer (assembled in on_url() for HTTP/1 and copied verbatim from the :path pseudo-header for HTTP/2) without resolving ./.. segments. The static-FS handler then built the on-disk filename by directly concatenating the configured root with that raw URL (snprintk(fname, ..., "%s%s", static_fs_detail-fs_path, client-url_buffer) at http_server_http1.c:603 and http_server_http2.c:490) and opened it with fs_open(fname, FS_O_READ). Because the handler is reached via wildcard/leading-dir (fnmatch FNM_LEADING_DIR) or fallback resource matching, a request such as GET /<prefix/../../<file is dispatched to the handler and, after the underlying filesystem (e.g. LittleFS/FAT) resolves the .. segments, escapes the configured web root, letting an unauthenticated remote client read arbitrary readable files on the mounted volume (information disclosure). The HTTP server requires no TLS or authentication to reach this path. The fix adds http_server_remove_dot_segments(), which canonicalizes the path portion of the URL before resource lookup in both protocol handlers, neutralizing the traversal. Affects releases v4.0.0 through v4.4.0 for deployments that register a static-filesystem resource.

### CVE-2026-51221

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-29T22:16:49.070 |

A buffer overflow in the Get_Attribute_List function of EIPStackGroup OpENer commit 76b95c allows attackers to cause a Denial of Service (DoS) via supplying a crafted Common Packet Format (CPF) packet.

### CVE-2026-41896

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-29T21:16:44.280 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.474, the HMAC key is the application's manual_webhook_secret_github field, which is used by Coolify's webhook endpoints to validate incoming requests, is nullable with no default — meaning newly created applications have a null webhook secret. PHP's hash_hmac() function silently coerces a null key to an empty string ''. So when the secret is null, the server computes hash_hmac('sha256', $payload, '') — a deterministic value that any attacker can calculate independently. By sending X-Hub-Signature-256: sha256=<hash_hmac('sha256', payload, '')>, an unauthenticated attacker can forge a valid signature and trigger deployments. This vulnerability is fixed in 4.0.0-beta.474.

### CVE-2026-56018

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-401` |
| Published | 2026-06-29T20:17:39.680 |

JavaScript::Minifier::XS versions before 0.16 for Perl leak memory on every call to minify(), allowing unbounded memory growth.

In JsMinify (XS.xs) the cleanup frees only the NodeSet structures and never the per-token contents buffers allocated in JsSetNodeContents; JsDiscardNode unlinks nodes without freeing their contents. Each token's contents buffer is therefore leaked on every call, and the two early returns taken when the node list is empty leak the whole NodeSet.

A long-lived process that minifies repeatedly, such as an asset pipeline or a server-side minifier endpoint, grows in memory without bound until it exhausts available memory and is killed, causing denial of service.

### CVE-2026-56017

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-476` |
| Published | 2026-06-29T20:17:39.570 |

JavaScript::Minifier::XS versions before 0.16 for Perl crash with a NULL pointer dereference when the first meaningful token of the input is a slash.

The regexp versus division disambiguator in JsTokenizeString (XS.xs) inspects the previous token's last byte to choose between a regexp literal and a division operator. When a slash is the first meaningful token, with the start of input or only whitespace and comments before it, there is no valid preceding token: the walk back over whitespace and comment nodes runs off the head of the node list to NULL, and the byte lookup reads through a NULL contents pointer at an underflowed length index. The following identifier check dereferences the same NULL pointer.

The crash is reachable through the public minify() API, so input as small as a single slash byte crashes the calling process. A service that minifies untrusted or third-party JavaScript can be crashed by a remote request, causing denial of service.

### CVE-2026-43721

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-06-29T20:17:36.647 |

This issue was addressed through improved state management. This issue is fixed in Safari 26.5.2, iOS 26.5.2 and iPadOS 26.5.2, macOS Tahoe 26.5.2. A malicious website may be able to silently hijack clipboard data.

### CVE-2026-36848

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-29T18:16:37.583 |

Gigamon GVOS v5.16.1 and below is vulnerable to Directory Traversal in the GVOS H-VUE subsystem.

### CVE-2026-55844

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-06-29T15:16:41.720 |

Home Assistant is open source home automation software that puts local control and privacy first. Prior to 2025.5.0, The iOS companion app ignores the SSID allowlist for internal networks. The app uses SSID to detect when to use the internal URL, but whenever the app cannot find any other URL to be used, it fallbacks to the internal URL as well, which can expose user's token when connected to a not secure network. This vulnerability is fixed in 2025.5.0.

### CVE-2026-49049

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-29T15:16:41.363 |

The Helix3 plugin for Joomla exposes an ajax handler task, that allows unauthenticated attackers to delete arbitrary files, write arbitrary JSON files and update template parameters.

### CVE-2026-13583

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-06-29T16:16:38.767 |

A vulnerability has been found in Edimax EW-7478APC 1.04. Impacted is the function formUSBFolder of the file /goform/formUSBFolder of the component POST Request Handler. Such manipulation of the argument ShareName/SelectName leads to buffer overflow. The attack may be performed from remote. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-13582

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-06-29T16:16:38.610 |

A flaw has been found in Edimax EW-7478APC 1.04. This issue affects the function formUSBAccount of the file /goform/formUSBAccount of the component POST Request Handler. This manipulation of the argument UserName/Password causes buffer overflow. The attack is possible to be carried out remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-13580

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-06-29T16:16:38.280 |

A security vulnerability has been detected in Edimax EW-7478APC 1.04. This affects the function formQoS of the file /goform/formQoS of the component POST Request Handler. The manipulation of the argument selSSID leads to buffer overflow. Remote exploitation of the attack is possible. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-58014

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-193` |
| Published | 2026-06-30T13:19:17.580 |

A flaw was found in GLib. An off-by-one error can occur in the g_key_file_get_locale_string_list function in the gkeyfile.c file when loading a key file with an empty value. This flaw can cause an out-of-bounds access of 1 byte or a denial of service when the out-of-bounds access crosses a page boundary.

### CVE-2026-55957

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-304` |
| Published | 2026-06-29T21:16:45.700 |

Missing Critical Step in Authentication vulnerability in Apache Tomcat when the JNDIRealm was configured to authenticate binds using GSSAPI allowed attackers to authenticate without provided the correct password.

This issue affects Apache Tomcat: from 11.0.0-M1 through 11.0.4, from 10.1.0-M1 through 10.1.36, from 9.0.0.M1 through 9.0.100, from 8.5.0 through 8.5.100, from 7.0.0 through 7.0.109.

Users are recommended to upgrade to version 11.0.5, 10.1.37 or 9.0.101, which fixes the issue.

### CVE-2026-53404

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-670` |
| Published | 2026-06-29T21:16:44.527 |

Always-Incorrect Control Flow Implementation vulnerability in Apache Tomcat's rewrite valve meant that if the first condition in an OR chain matched, subsequent non-OR conditions were skipped.

This issue affects Apache Tomcat: from 11.0.0-M1 through 11.0.22, from 10.1.0-M1 through 10.1.55, from 9.0.0.M1 through 9.0.118, from 8.5.0 through 8.5.100. Other versions that have reached end of support may also be affected.

Users are recommended to upgrade to version 11.0.23, 10.1.56 or 9.0.119, which fix the issue.

### CVE-2026-12912

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-122` |
| Published | 2026-06-29T17:16:28.230 |

A flaw was found in libtiff. A remote attacker could exploit this vulnerability by providing a specially crafted PixarLog-compressed TIFF image. This issue occurs when decoding Pixarlog codec images with the PIXARLOGDATAFMT_8BITABGR output format and a specific stride value, leading to a heap-based buffer overflow. This could potentially result in arbitrary code execution or a denial of service (DoS).

### CVE-2026-8141

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-30T10:16:37.213 |

The Ajax Load More - Filters plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'taxonomy_include_children' parameter in all versions up to, and including, 3.4.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-10816

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-06-30T13:17:04.220 |

Arbitrary File Read (Unauthenticated) in NetScaler ADC and NetScaler Gateway if the access to NSIP, Cluster Management IP or SNIP with management access is enabled

### CVE-2026-43725

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-29T20:17:36.937 |

The issue was addressed with improved input validation. This issue is fixed in Safari 26.5.2, iOS 26.5.2 and iPadOS 26.5.2, macOS Tahoe 26.5.2. A malicious website may be able to process restricted web content outside the sandbox.

### CVE-2026-57951

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-29T18:16:40.253 |

Mythic before 3.4.0.60 contains a broken hasura permission filter on the payload_build_step table with an always-satisfied _or condition that bypasses operation-scoped access controls. Authenticated operators and spectators can query payload_build_step to read step_stdout, step_stderr, step_name, and step_description across all operations on the server.

### CVE-2026-57949

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-29T18:16:39.997 |

ruoyi-vue-pro through 2026.05, fixed in commit c779a47, contains a missing authorization vulnerability in the CRM module's GET /admin-api/crm/follow-up-record/get endpoint that allows authenticated users to read any follow-up record by iterating sequential numeric IDs. Attackers can exploit this by sending requests with arbitrary ID parameters to access other users' follow-up notes, file attachments, scheduling information, and business entity references without proper authorization checks.

### CVE-2026-56783

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-06-29T18:16:38.950 |

Parseable before 2.9.2 contains an information disclosure vulnerability in the notification-target API endpoints that returns webhook tokens and basic-auth credentials in cleartext due to commented-out secret-masking functionality. Any authenticated user with the GetAlert action, including low-privilege reader roles, can recover credentials and internal endpoint URLs for all configured notification targets by querying GET /api/v1/targets or related endpoints.

### CVE-2026-57338

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-29T15:16:44.510 |

Unauthenticated Cross Site Scripting (XSS) in ARForms <= 7.1.2 versions.

### CVE-2026-57337

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-29T15:16:44.390 |

Unauthenticated Cross Site Scripting (XSS) in Landing Page Builder <= 1.5.3.5 versions.

### CVE-2026-57336

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-29T15:16:44.273 |

Unauthenticated Cross Site Scripting (XSS) in Jobify <= 4.3.2 versions.

### CVE-2026-57333

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-29T15:16:43.600 |

Unauthenticated Cross Site Scripting (XSS) in Link Whisper Free <= 0.9.4 versions.

### CVE-2026-57332

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-29T15:16:43.483 |

Subscriber Broken Access Control in Wallet System for WooCommerce <= 2.7.6 versions.

### CVE-2026-57320

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-29T15:16:42.627 |

Unauthenticated Cross Site Scripting (XSS) in BEAR <= 1.1.8 versions.

### CVE-2026-10763

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-06-30T10:16:34.067 |

PROMOD V is using insecure HTTP communication instead of HTTPS. The vulnerability is due to the lack of HTTPS support from 3rd party Digipede server.
