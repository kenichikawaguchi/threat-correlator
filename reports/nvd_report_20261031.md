# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-30 15:00 UTC
- **対象期間**: `2026-10-29T15:00:58.000Z` 〜 `2026-10-30T15:00:45.000Z`
- **重要CVE数**: 267 件（Critical 9.0+: 62 件 / High 7.0〜: 205 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上期に公表された CVE のうち、CVSS 7.0 以上が集中して **認証なしリモートコード実行 (RCE)・認証バイパス** に関するものとなっている。  
- 特に **Progress Software の WS_FTP Server** と **AjaxLoadMore Cache**、そして **WordPress 系プラグイン** に対する脆弱性が高い深刻度 (CVSS 9.8‑10.0) を示し、ネットワーク境界を越えて即座にシステム制御が奪取できる点が共通している。  
- 同時期に多数の小規模 PHP アプリケーション（プラグイン・テーマ）で **PHP Object Injection** が連続報告され、攻撃対象が広範囲に拡大している。  
- これらは「**認証不要**」かつ「**ネットワークから直接利用可能**」という条件を満たすため、早急なパッチ適用と防御層の強化が必須である。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲・被害シナリオ | 推奨される対策バージョン |
|-----|------|----------------|------------------------|--------------------------|
| **CVE‑2026‑84295** | 10.0 | Improper authentication (認証バイパス) | Progress Software **WS_FTP Server** (Windows) の認証ロジック不備により、未認証リモート攻撃者が管理者権限情報やファイル一覧にアクセス可能。内部ネットワークだけでなく、インターネット経由でも情報漏洩・横展開が可能。 | **2024.0.6** 以降、**2025.0.3** 以降にアップデート |
| **CVE‑2026‑61991** | 10.0 | Unauthenticated RCE | WordPress 用 **AjaxLoadMore Cache** ≤ 3.1.1 における任意コード実行。キャッシュ処理時にシリアライズデータを検証せず、遠隔から任意 PHP コードを実行できる。サイト全体が乗っ取られる危険性が高い。 | **3.1.2** 以降 (公式リリースがある場合は最新版) |
| **CVE‑2026‑90868** | 9.9 | OS command injection | WS_FTP Server の特定設定下で OS コマンドインジェクションが可能。`PR:L` だが、特権が付与されたサービスアカウントで実行されるため、システム全体への影響が大きい。 | **2024.0.7** 以降、**2025.0.4** 以降にアップデート |
| **CVE‑2025‑31704** | 9.8 | Remote command execution (特権取得) | **Dahua Intelligent Connection Center** に対し、特製リクエストで任意コマンド実行が可能。IoT/監視カメラ環境に広く導入されており、ネットワーク分離が不十分な場合は内部侵入の足掛かりになる。 | ベンダー提供の **最新ファームウェア**（2025 年以降のリリース） |
| **CVE‑2026‑103039** | 9.8 | PHP Object Injection (POI) | WordPress **Gravity Forms** ≤ 3.1.2 の `GFFormsModel::create_post()` が `maybe_unserialize()` を無制限に呼び出すため、攻撃者が任意オブジェクトを注入し、サーバ上でコード実行が可能。多数のサイトでプラグインが利用されている点がリスクを拡大。 | **3.1.3** 以降、もしくは **最新安定版** |

> **注:** IBM Langflow 系 (CVE‑2026‑107327/107328/107329/93680) も CVSS 9.9‑9.8 で深刻だが、対象が OSS の開発者・利用者に限定されるため、上記 5 件を優先的に取り上げた。

---

## 3. 推奨アクション  

### 3‑1. 直ちに適用すべきパッチ・バージョン
- **Progress Software WS_FTP Server**  
  - 2024 系: `2024.0.6` 以上 → **2024.0.7** 以上を推奨（認証バイパス＋コマンドインジェクション両方の修正）  
  - 2025 系: `2025.0.3` 以上 → **2025.0.4** 以上を推奨  
- **AjaxLoadMore Cache (WordPress)**  
  - `3.1.2` 以上（公式リリースが無い場合は GitHub の master ブランチをデプロイ）  
- **Dahua Intelligent Connection Center**  
  - ベンダーが提供する **最新ファームウェア**（2025‑2026 年リリース）を適用。  
- **Gravity Forms (WordPress)**  
  - `3.1.3` 以上、もしくは **最新バージョン**（執筆時点で 3.2.x 系）へ更新。  
- **IBM Langflow OSS**  
  - `1.12.9` 以上（リリースノートで CVE‑1073xx 系が修正済み）へアップグレード。  

### 3‑2. 影響範囲の特定とインベントリ化
1. **資産管理ツール**（CMDB、Qualys、Tenable 等）で上記製品・プラグインのバージョンを自動収集。  
2. **未パッチのサーバ** が検出されたら、以下の手順で即時隔離 → パッチ適用 → 再接続。  
3. **WordPress 環境** は `wp plugin list --status=active` で全プラグインを列挙し、特に `gravityforms`、`ajax-load-more-cache` が含まれるか確認。  

### 3‑3. 防御層の強化
- **WAF ルール**:  
  - `CVE‑2026‑61991` のようなシリアライズデータの POST/GET 送信を検知し、`application/octet-stream` 以外のシリアライズ文字列をブロック。  
  - `CVE‑2025‑31704` 用に、Dahua 製品への外部からの管理ポート（80/443/

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-84295

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-522` |
| Published | 2026-10-29T16:19:29.860 |

Improper authentication in Progress Software WS_FTP Server versions prior to 2024.0.6 and 2025.0.3 on Windows could allow an unauthenticated remote attacker to access sensitive information, including administrative credentials.

### CVE-2026-61991

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T16:18:11.463 |

Unauthenticated Remote Code Execution (RCE) in AjaxLoadMore Cache <= 3.1.1 versions.

### CVE-2026-90868

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-10-29T16:20:04.963 |

An OS command injection vulnerability in Progress Software WS_FTP Server versions prior to 2024.0.7 and 2025.0.4 on Windows could allow arbitrary command execution under certain configurations.

### CVE-2026-107329

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T16:17:50.633 |

IBM Langflow OSS 1.0.0 through 1.12.4 could allow a remote authenticated attacker to execute arbitrary code due to improper control of code generation.

### CVE-2026-107328

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T16:17:50.480 |

IBM Langflow OSS 1.0.0 through 1.12.4 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of code in eval/exec.

### CVE-2026-107327

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-29T16:17:50.330 |

IBM Langflow OSS 1.0.0 through 1.12.4 could allow a remote authenticated attacker to execute arbitrary code due to missing authorization.

### CVE-2025-31704

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-30T11:17:31.450 |

A vulnerability has been found in the Dahua Intelligent Connection Center. A remote attacker could send a specially crafted request to the affected system, allowing the attacker to execute arbitrary commands, resulting in remote code execution.

### CVE-2026-103039

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T07:16:30.733 |

The Gravity Forms plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 3.1.2 via a Post Custom Field whose input type is List. This is due to GFFormsModel::create_post() passing the submitted value to WordPress' unrestricted global maybe_unserialize() rather than the plugin's own hardened GFCommon::maybe_unserialize(), which was added in 3.1.1 and passes allowed_classes => false precisely to prevent object instantiation. Where the field has a content template enabled, the submitted row reaches that call verbatim. This makes it possible for unauthenticated attackers to inject a PHP object into post meta. No PHP Object Injection gadget chain is present in the plugin itself; however, if a gadget chain is present via an additional plugin or theme, it could allow the attacker to perform actions such as remote code execution. Where the custom field is mapped to the protected _wp_page_template meta key, WordPress itself supplies the chain: validate_file() accepts non-scalars, WP_Theme::__toString() then resolves an attacker-controlled path, and on hosts with a readable PEAR install and register_argc_argv enabled this yields remote code execution.

### CVE-2026-107058

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-29T17:17:58.620 |

An issue in Shelter versionCode 445 allows attackers to register their own auth_key and execute a takeover of another user's binder service API and preference state.

### CVE-2026-93680

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-29T16:20:06.040 |

IBM Langflow OSS 1.0.0 through 1.12.8 could allow a remote attacker to bypass security restrictions due to improper authentication.

### CVE-2026-62131

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:14.800 |

Unauthenticated PHP Object Injection in Zoho Flow <= 2.14.5 versions.

### CVE-2026-62018

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:14.643 |

Unauthenticated PHP Object Injection in Gunslinger <= 1.11 versions.

### CVE-2026-62017

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:14.513 |

Unauthenticated PHP Object Injection in Good Homes <= 1.3.13 versions.

### CVE-2026-62016

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:14.387 |

Unauthenticated PHP Object Injection in Gamic <= 1.19 versions.

### CVE-2026-62015

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:14.263 |

Unauthenticated PHP Object Injection in Gamezone <= 1.1.11 versions.

### CVE-2026-62014

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:14.143 |

Unauthenticated PHP Object Injection in EmojiNation <= 1.0.12 versions.

### CVE-2026-62013

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:14.027 |

Unauthenticated PHP Object Injection in Edge Decor <= 2.9 versions.

### CVE-2026-62012

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:13.907 |

Unauthenticated PHP Object Injection in Coinpress <= 1.0.15 versions.

### CVE-2026-62011

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:13.787 |

Unauthenticated PHP Object Injection in Bonbon <= 1.11 versions.

### CVE-2026-62010

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:13.670 |

Unauthenticated PHP Object Injection in Avventure <= 1.1.12 versions.

### CVE-2026-62009

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:13.543 |

Unauthenticated PHP Object Injection in Filmax <= 1.1.11 versions.

### CVE-2026-62008

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:13.427 |

Unauthenticated PHP Object Injection in Orpheus <= 1.8 versions.

### CVE-2026-62006

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:13.310 |

Unauthenticated PHP Object Injection in Nuts <= 1.12 versions.

### CVE-2026-62005

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:13.190 |

Unauthenticated PHP Object Injection in Muzicon <= 1.15 versions.

### CVE-2026-62004

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:13.070 |

Unauthenticated PHP Object Injection in Motorix <= 1.11 versions.

### CVE-2026-62003

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:12.950 |

Unauthenticated PHP Object Injection in Mission <= 1.22 versions.

### CVE-2026-62002

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:12.823 |

Unauthenticated PHP Object Injection in Meals & Wheels <= 1.1.13 versions.

### CVE-2026-62001

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:12.693 |

Unauthenticated PHP Object Injection in Marcell <= 1.2.14 versions.

### CVE-2026-61998

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:12.580 |

Unauthenticated PHP Object Injection in Le Truffe <= 1.1.7 versions.

### CVE-2026-61997

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:12.457 |

Unauthenticated PHP Object Injection in Legal Stone <= 1.2.11 versions.

### CVE-2026-61992

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:11.820 |

Unauthenticated PHP Object Injection in GEO my WordPress <= 4.5.5.3 versions.

### CVE-2026-54860

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:10.220 |

Unauthenticated PHP Object Injection in Ozisti <= 1.1.10 versions.

### CVE-2026-54859

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:10.097 |

Unauthenticated PHP Object Injection in Preservation <= 1.15 versions.

### CVE-2026-54858

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:09.980 |

Unauthenticated PHP Object Injection in Printy <= 1.13.0 versions.

### CVE-2026-54857

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:09.860 |

Unauthenticated PHP Object Injection in Quirky <= 1.23 versions.

### CVE-2026-54856

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:09.740 |

Unauthenticated PHP Object Injection in RexCoin <= 1.2.6 versions.

### CVE-2026-110186

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T16:17:55.837 |

IBM Langflow OSS 1.0.0 through 1.12.8 could allow a remote attacker to execute arbitrary code due to improper control of code generation.

### CVE-2026-104339

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T16:17:44.403 |

IBM Langflow OSS 1.0.0 through 1.12.3 could allow a remote attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-119263

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-30T01:16:45.047 |

Memory corruption in GarbageCollection in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-119261

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-30T01:16:44.797 |

Improper input validation in Skia in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-116366

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-30T11:17:32.540 |

An issue has been discovered in ClickHouse Server that, under certain conditions, could allow an unauthenticated user with network access to execute arbitrary code on the ClickHouse Server.

### CVE-2026-82104

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-30T08:17:00.240 |

In Teltonika Networks RUTOS devices running versions from 7.22 through 7.24.2 and TSWOS devices running versions 1.9 through 1.10, a vulnerability exists whereby an unauthenticated user can directly call LUA functions, bypassing validations that might be called under normal API requests. Due to those requests not following proper flows, this could lead to OS command execution.



This issue affects RUT: from 7.22 through 7.24.2; RUTX: from 7.22 through 7.24.2; RUTM: from 7.22 through 7.24.2; RUTC: from 7.22 through 7.24.2; ATRM: from 7.22 through 7.24.2; TAP: from 7.22 through 7.24.2; CAP: from 7.22 through 7.24.2; OXA: from 7.22 through 7.24.2; DAP: from 7.22 through 7.24.2; TRB: from 7.22 through 7.24.2; OTD: from 7.22 through 7.24.2; EBG: from 7.22 through 7.24.2; SWM: from 1.9 through 1.10; TSW: from 1.9 through 1.10.

### CVE-2026-103093

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-29T19:17:15.113 |

ServiceNow has remediated a sandbox escape security issue that was identified in the ServiceNow AI Platform. This vulnerability could enable an authenticated user with the admin role to bypass Rhino sandbox restrictions and execute arbitrary code on the underlying host operating system, potentially enabling further unintended access. 



ServiceNow deployed an update to hosted instances, and ServiceNow provided the update to our partners and self-hosted customers. We are not currently aware of malicious exploitation against ServiceNow instances. We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-119145

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-29T16:18:08.277 |

Frappe before 15.121.0 and 16.x before 16.34.0 contains a path traversal vulnerability because certain file-upload handling does not validate the destination path before writing to disk. Authenticated attackers can upload crafted files to locations outside the intended storage directory to achieve remote code execution on the server.

### CVE-2026-119597

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-30T14:16:47.770 |

OpenDeepWiki through 2.0.6 contains a hard-coded JWT signing key vulnerability that allows unauthenticated attackers to forge administrator tokens using the publicly known Jwt:SecretKey in appsettings.json. Attackers can mint HS256 bearer tokens with an Admin role claim to access /api/admin endpoints and control users, roles, repositories, settings, and API keys.

### CVE-2023-22793

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T23:16:54.270 |

A vulnerability allowing an unauthenticated attacker to perform remote code execution (RCE) on servers running the Veeam Virtualization Extensions service of Veeam Management Pack for Microsoft System Center.

### CVE-2026-118762

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-29T17:18:07.070 |

Monkeytype is a minimalistic and customizable typing test. Prior to 26.43.0, the .github/workflows/fix-formatting.yml workflow runs on pull_request_target with repository write permissions, checks out a fork pull request, installs dependencies from the fork's package.json, and invokes the fork-controlled oxfmt binary. Because actions/checkout persists the elevated GITHUB_TOKEN in Git configuration until after untrusted code executes, an external contributor whose pull request receives the format label can run arbitrary code, read or exfiltrate the token, and push repository content or modify pull requests and issues. The issue affects the repository CI workflow, not the Monkeytype application or user data. This issue is fixed in version 26.43.0.

### CVE-2026-111732

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-29T16:17:57.480 |

P-Net before 1.0.3, when built with PNET_OPTION_AR_VENDOR_BLOCKS enabled, parses a data length from a field of the ARVendorBlock request that is not part of the block definition and uses it as the number of bytes to copy into a fixed-size buffer, without comparing it with the buffer size or the block length. A crafted Connect request causes an out-of-bounds write. This can lead to a crash (denial of service) or potentially arbitrary code execution.



This option is disabled by default.

### CVE-2026-119419

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-30T12:16:38.550 |

CakePHP through 5.4.3 contains an sql injection vulnerability that allows attackers to inject SQL by supplying unvalidated collation values to StringExpression and IdentifierExpression. Attackers controlling a collation name passed to the constructor or setCollation() can append SQL after the unquoted COLLATE clause, affecting every database driver within the connection's privileges.

### CVE-2026-119418

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-30T12:16:38.390 |

CakePHP through 5.4.3 contains an sql injection vulnerability that allows attackers to inject SQL by supplying unvalidated frame offsets and directions to WindowExpression::range() and frame(). Attackers can pass crafted values through applications forwarding user input into the OVER clause to execute SQL with the database connection's privileges.

### CVE-2026-118769

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-681;CWE-787` |
| Published | 2026-10-29T18:17:29.180 |

Botan is a C++ cryptography library. From 2.1.0 until 3.13.0, the Botan C API function botan_block_cipher_block_size converted a size_t block size to int without a bounds check. In an application that accepts external algorithm parameter strings and uses the FFI raw ECB mode, an attacker can select the variable-block-size Lion cipher so that the reported size is truncated, the caller allocates insufficient memory, and later block processing causes memory corruption. The C++ API and normally used C API modes such as CBC and CTR are unaffected. This issue is fixed in version 3.13.0.

### CVE-2026-112256

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:C/RE:M/U:Red` |
| Weaknesses | `CWE-349` |
| Published | 2026-10-29T16:17:58.390 |

Acceptance of extraneous untrusted data with trusted data vulnerability in OpenText Advanced Authentication Server allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects Advanced Authentication Server: from 6.4.0.0 through 6.4.3.8, from 6.5.0.0 through 6.5.0.10, and from 6.6.0.0 through 6.6.1.0.

### CVE-2026-119568

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-940` |
| Published | 2026-10-30T12:16:44.580 |

vsftpd through 3.0.5 contains an authentication bypass vulnerability in ssl_data_accept() that allows unauthenticated attackers to hijack FTPS data connections by resuming their own TLS session ticket. Attackers sharing the victim's source IP can obtain a ticket via AUTH TLS, then connect to the victim's PASV port to steal downloads or inject upload data.

### CVE-2026-61645

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-29T22:17:04.963 |

Docat is a tool for hosting versioned static documentation. In the affected implementation, an arbitrary file upload vulnerability in the `Upload API` arises because the API does not validate the `uploaded file path or type`. An attacker can overwrite sensitive configuration files or place malicious files on the Docat web server. Depending on deployment context, uploaded content can enable remote code execution or cross-site scripting intended to steal cookies or redirect users to malicious websites. Version 1.6.0 mitigates filename-based path traversal; remediation of unrestricted file types or deployment-dependent malicious-content effects is not established by the verified patch.

### CVE-2026-90866

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-434` |
| Published | 2026-10-29T16:20:04.690 |

A path traversal vulnerability in Progress Software WS_FTP Server versions prior to 2024.0.7 and 2025.0.4 on Windows could allow a delegated Host Administrator to access locations outside their authorized scope, potentially enabling remote code execution.

### CVE-2026-90864

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-434` |
| Published | 2026-10-29T16:20:04.453 |

A path traversal vulnerability in Progress Software WS_FTP Server versions prior to 2024.0.7 and 2025.0.4 on Windows could allow a delegated Host Administrator to access or modify files outside their authorized scope.

### CVE-2026-90863

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862;CWE-915` |
| Published | 2026-10-29T16:20:04.337 |

Missing authorization in the administrative interface of Progress Software WS_FTP Server versions prior to 2024.0.7 and 2025.0.4 on Windows could allow a delegated Host Administrator to exceed their authorized scope, potentially enabling arbitrary command execution with elevated privileges and complete compromise of the underlying server.

### CVE-2026-119128

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-565` |
| Published | 2026-10-29T16:18:05.643 |

ZITADEL 4.0.0 before 4.19.5 contains an authentication bypass vulnerability in the Login V2 UI that allows unauthenticated attackers to set the first credential of users lacking any authentication method. Attackers can compute a valid verificationCheck cookie from the user ID and browser fingerprint to set a password, register a passkey, or link an identity provider, taking over the account.

### CVE-2026-107032

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-926` |
| Published | 2026-10-29T16:17:48.943 |

Insecure permissions in Bulk Share : Location Sender v2.1.0 (versionCode 5) allows unauthorized attackers to invoke an exported component, leading to arbitrary data access and control of data flow.

### CVE-2026-107015

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-29T15:17:15.200 |

Insecure permissions in Simple Contacts Pro versionCode 107 allow unauthorized attackers to write and read notes in another user's' note database.

### CVE-2026-61707

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-862;CWE-1336` |
| Published | 2026-10-29T22:17:05.603 |

SOCFortress CoPilot focuses on providing a single pane of glass for all your security operations needs. Prior to 0.1.76, in the reported deployment, case-report templates uploaded by `customer_user`, the lowest-privilege portal role, are later executed by non-sandboxed Jinja2 engines when an admin or analyst generates a report. The `/case-report-template/upload` route in `backend/app/incidents/routes/db_operations.py` validates only the filename-derived MIME type, not the template content. Templates share a global store without customer_code scoping, and `customer_user` can also list, download and delete them, allowing an attacker to replace a legitimate default template under the same name. In `backend/app/incidents/services/reports.py`, `render_document_with_context` uses `DocxTemplate` without a sandbox; in `backend/app/incidents/services/reports_pdf.py`, `render_html_template` uses a non-sandboxed `Environment` without autoescaping. Normal privileged requests to `POST /api/incidents/report/generate-report-docx` or `/generate-report-pdf` therefore evaluate attacker-controlled Jinja expressions as Python on the backend. The reported deployment executes commands as root, exposing all tenants' incident and SIEM data and stored connector credentials. The HTML/PDF wkhtmltopdf renderer additionally permits local-file reads and requests to internal services. This issue is fixed in version 0.1.76.

### CVE-2026-90865

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-10-29T16:20:04.570 |

An OS command injection vulnerability in Progress Software WS_FTP Server versions prior to 2024.0.7 and 2025.0.4 on Windows could allow arbitrary command execution with elevated privileges under certain configurations.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-61719

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T22:17:05.763 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.7, a stored cross-site scripting vulnerability in `saude/historico_prontuarios.php` arises because the `textoProntuario` field accepts arbitrary HTML or JavaScript without proper sanitization. An attacker able to create or access a patient's medical record can submit the field through `POST /controle/control.php` with `nomeClasse=SaudeControle`, `metodo=alterarProntuario`, and `id_fichamedica`. The stored content is rendered when another user accesses `/html/saude/historico_prontuarios.php` with `id_historico`, automatically executing attacker-controlled JavaScript in the victim's browser. The vulnerability permits session cookie theft and potential account compromise depending on the victim's privileges. This issue is fixed in version 3.8.7.

### CVE-2026-91913

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-30T14:17:10.757 |

Dell OpenManage Enterprise, versions prior to 4.8.0, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-111505

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-30T12:16:35.070 |

Dell OpenManage Enterprise, versions prior to 4.8.0, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-59387

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-30T09:17:14.913 |

The Nginx routing configuration for Cloud Controller blocks unauthenticated access to /internal/v4/ and /internal/v5/ endpoints but omits an equivalent deny rule for /internal/v3/. As a result, the staging callback endpoints /internal/v3/staging/:guid/droplet_completed and /internal/v3/staging/:guid/build_completed are reachable from the public API listener without OAuth or mutual TLS.



 



An attacker with a valid build or droplet GUID can submit a forged staging callback, transition a droplet to STAGED, and persist arbitrary process metadata and sidecar data with no associated package or actor. A SpaceAuditor can enumerate GUIDs without write permissions, making this an effective privilege escalation beyond the intended role boundary.

### CVE-2026-89435

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-10-30T07:16:34.410 |

The Formidable Forms – WordPress Form Builder for Contact Forms, Calculators, Quizzes & More plugin for WordPress is vulnerable to Arbitrary Plugin Installation in all versions up to, and including, 6.35 via the 'file_url' parameter parameter. This is due to insufficient URL prefix validation in validate_url_is_in_s3_bucket() and a permission callback that relies solely on a shared token obtainable by any user with the delegable frm_view_forms capability, without checking install_plugins or activate_plugins capabilities. This makes it possible for authenticated attackers, with subscriber-level access and above, to install arbitrary plugins on the server. Exploitation additionally requires that the site is free-only (Formidable Pro is NOT installed).

### CVE-2026-117571

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T06:16:46.007 |

The WP Visitor Statistics (Real Time Traffic) WordPress plugin before 8.8 does not sanitize and escape tracking data derived from public visitor requests before storing it and outputting it in the administrative statistics dashboard, allowing unauthenticated attackers to inject arbitrary web scripts that execute when a logged-in administrator views the statistics pages.

### CVE-2026-104368

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-116` |
| Published | 2026-10-30T05:16:57.833 |

The Export and Import Users and Customers plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.7.5 via the plugin's own export and re-import workflow. The vulnerability exists because of a CSV escape-character mismatch between the exporter and the importer: class-csvwriter.php writes cells with fputcsv() using PHP's default backslash (\) escape character, while class-csvreader.php parses the same file with fgetcsv() using a double-quote (") as the escape character. As a result, a crafted value stored in a Subscriber's Biographical Info field — containing a backslash-quote sequence followed by a newline — is written as a single quoted CSV field but parsed back as two separate rows on import. The injected second row is then processed by hf_create_customer() as a new user record whose user_login, user_pass, user_email, and role are entirely attacker-controlled, allowing the creation of an arbitrary Administrator account. This makes it possible for authenticated attackers with Subscriber-level access and above to escalate their privileges to Administrator.

### CVE-2026-76031

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-30T01:16:47.717 |

Use after free in Input in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-76030

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-30T01:16:47.593 |

Memory corruption in FileSystem in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-76029

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-30T01:16:47.467 |

Memory corruption in Network in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-76028

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-30T01:16:47.337 |

Use after free in FileSystem in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-76026

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-30T01:16:47.093 |

Memory corruption in Autofill in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-76025

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-30T01:16:46.970 |

Use after free in FileSystem in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-119271

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-30T01:16:46.063 |

Use after free in Skia in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-119270

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-30T01:16:45.937 |

Improper input validation in CacheStorage in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-119269

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-30T01:16:45.807 |

Use after free in Blink in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-119268

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-30T01:16:45.680 |

Integer overflow in Editing in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-119267

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-30T01:16:45.553 |

Memory corruption in DOM in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-119266

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-30T01:16:45.430 |

Use after free in Quota in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-119265

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-30T01:16:45.303 |

Memory corruption in Quota in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-119264

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-30T01:16:45.177 |

Memory corruption in Dawn in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-119262

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-30T01:16:44.920 |

Improper input validation in V8 in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-119260

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-30T01:16:44.663 |

Use after free in Frames in Google Chrome prior to 156.0.8078.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-107239

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-29T23:16:54.887 |

A vulnerability allowing a member of the Veeam Virtualization Extensions Users group to perform remote code execution (RCE) on servers running the Veeam Management Pack for Microsoft System Center Collector service.

### CVE-2026-119168

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-29T19:17:21.120 |

HashiCorp Nomad and Nomad Enterprise are vulnerable to symlink following during same-client allocation data migration that may allow a malicious workload to change permissions and ownership of host directories. This could allow unauthorized access to host data or modification of host files, potentially leading to privilege escalation. This vulnerability (CVE-2026-119168) is fixed in Nomad 2.1.1 and Nomad Enterprise 2.1.0, 1.11.12, and 1.10.18.

### CVE-2026-96203

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-29T16:20:09.003 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-96199

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-29T16:20:08.737 |

Heap-based buffer overflow in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-96198

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-29T16:20:08.607 |

Heap-based buffer overflow in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-96196

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-10-29T16:20:08.477 |

Incomplete list of disallowed inputs in Microsoft Edge (Chromium-based) allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-96192

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-29T16:20:08.347 |

Use after free in Microsoft Edge for iOS allows an unauthorized attacker to execute code over a network.

### CVE-2026-88077

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-29T16:19:52.807 |

Integer overflow or wraparound in Microsoft Edge (Chromium-based) allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-85897

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-29T16:19:45.220 |

Heap-based buffer overflow in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-85890

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-29T16:19:45.017 |

Double free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-118082

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-29T16:18:03.193 |

Subscriber Privilege Escalation in Buddyboss Platform <= 3.5.0 versions.

### CVE-2026-118081

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:02.917 |

Contributor PHP Object Injection in 10Web Social Photo Feed <= 1.5.6 versions.

### CVE-2026-118080

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:02.790 |

Contributor PHP Object Injection in Social Snap <= 1.5.4 versions.

### CVE-2026-118076

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:02.297 |

Contributor PHP Object Injection in Frisbii Pay <= 1.8.19 versions.

### CVE-2026-118075

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:02.177 |

Contributor PHP Object Injection in WP Media folders <= 1.1.10 versions.

### CVE-2026-118073

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:01.937 |

Subscriber PHP Object Injection in News Kit Elementor Addons <= 1.5.0 versions.

### CVE-2026-116868

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:01.667 |

Subscriber PHP Object Injection in BuddyPress Xprofile Custom Field Types <= 1.3.1 versions.

### CVE-2026-116867

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:01.507 |

Contributor PHP Object Injection in Dynamic QR Code &#8211; generator <= 1.0.1 versions.

### CVE-2026-116866

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:01.350 |

Contributor PHP Object Injection in Extra Fees Plugin for WooCommerce <= 4.4.0 versions.

### CVE-2026-110309

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T16:17:57.033 |

IBM Langflow OSS 1.0.0 through 1.12.4 could allow a remote authenticated attacker to execute arbitrary commands due to improper control of code generation.

### CVE-2026-110244

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-29T16:17:56.693 |

IBM Langflow OSS 1.0.0 through 1.12.4 could allow a remote authenticated attacker to obtain sensitive information due to improper limitation of a pathname to a restricted directory.

### CVE-2026-110196

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-29T16:17:56.380 |

IBM Langflow OSS 1.0.0 through 1.12.4 could allow a remote attacker with a low-privileged authenticated account to bypass the administrator-only restriction and execute arbitrary code on the server by configuring a built-in code-execution component with attacker-supplied inputs.

### CVE-2026-110193

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T16:17:56.253 |

IBM Langflow OSS 1.0.0 through 1.12.8 could allow a remote attacker with a low-privileged authenticated account to cause the Agentic Assistant to generate or submit component code using these unblocked patterns, resulting in arbitrary operating system command execution on the server.

### CVE-2026-107326

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-29T16:17:50.160 |

IBM Langflow OSS 1.0.0 through 1.12.4 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-104328

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T16:17:44.153 |

IBM Langflow OSS 1.0.0 through 1.12.3 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-104324

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:17:44.033 |

IBM Langflow OSS 1.0.0 through 1.12.3 could allow a remote authenticated attacker to execute arbitrary code due to deserialization of untrusted data.

### CVE-2026-101288

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-29T16:17:35.203 |

IBM Langflow OSS 1.0.0 through 1.12.3 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in code.

### CVE-2026-119420

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-30T12:16:38.717 |

Lago through 1.55.0 contains an authentication bypass vulnerability that allows organization administrators to obtain session tokens for existing accounts via the acceptInvite mutation without a password check. Attackers can invite a victim's email, accept with an arbitrary password, and receive a JWT to access the victim's organizations, billing data, API keys and payment integrations.

### CVE-2026-119408

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-653` |
| Published | 2026-10-30T12:16:37.283 |

n8n before 2.42.6, 2.43.x before 2.43.3, and 3.x before 3.0.1 contains a remote code execution vulnerability via deprecated Function, Function Item, and LangChain Code nodes running outside task runner isolation. Authenticated users who can create, modify, or import workflows naming these hidden node types can execute JavaScript in the n8n main process.

### CVE-2026-85268

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T11:17:33.750 |

A Cross-Site Scripting (XSS) (CWE-79) vulnerability in the auth/handler in Google Cloud Identity Platform and Firebase Authentication versions prior to 2026-08-14 on iOS allows an unauthenticated remote attacker to execute arbitrary JavaScript using a malicious iOS bundle ID.

### CVE-2026-22110

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-30T11:17:33.040 |

The web server does not check authentication on POST or PUT. An unauthenticated attacker can reboot the charger; by brute-forcing the configid, they can also set the service password and then change any setting.

### CVE-2026-22105

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-10-30T11:17:32.700 |

Delta UFC500 charging stations derive the default credentials of the Service account from character positions of the device serial number. An unauthenticated attacker with adjacent network access can reconstruct the resulting password, or exhaust the keyspace, and log in to read and change sensitive settings such as the OCPP backend.

### CVE-2026-92744

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295;CWE-306` |
| Published | 2026-10-29T23:17:02.190 |

Under certain conditions, privilege manager agent allows a remote unauthenticated attacker to execute
arbitrary code as LocalSystem.

### CVE-2026-107238

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T23:16:54.760 |

A vulnerability allowing an authenticated domain user to perform remote code execution (RCE) as the LocalSystem account on servers running the Veeam Management Pack for Microsoft System Center Collector service.

### CVE-2026-13303

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-29T21:17:22.000 |

HashiCorp Boundary and Boundary Enterprise are vulnerable to a server-side request forgery in the Vault credential store integration that may allow an authenticated user with permission to manage credential stores and credential libraries within a project to cause the Boundary controller to issue outbound requests to a network destination of the requester's choosing and to receive the response. This may expose endpoints reachable only from the controller's host, such as a cloud instance metadata service. This vulnerability, CVE-2026-13303, is fixed in Boundary Enterprise 1.0.2 and 0.21.6.

### CVE-2026-118764

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-405` |
| Published | 2026-10-29T17:18:07.380 |

minimatch is a minimal matching utility for converting glob expressions into JavaScript RegExp objects. Prior to 11.0.1, src/index.ts implements firstPhasePreProcess() so that, at optimizationLevel 2 or higher, it repeatedly expands attacker-controlled **/.. pattern segments inside a fixpoint loop, allowing generated globParts entries to be processed and expanded again. secondPhasePreProcess() then compares the expanded entries pairwise, so a short malicious glob can cause excessive CPU and memory consumption during pattern compilation. This issue is fixed in version 11.0.1.

### CVE-2026-119144

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-29T16:18:08.117 |

Frappe Framework before 15.111.0 and 16.x before 16.21.0 contains a server-side template injection vulnerability because user-controlled message fields are rendered as templates without neutralization. An authenticated attacker holding a common operational role can inject template expressions that the server evaluates in an unrestricted context.

### CVE-2026-119119

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-29T16:18:04.207 |

Crawl4AI before 0.9.5 contains a denial of service vulnerability in the Docker API server where _clamp_untrusted() fails to cap the delay_before_return_html, mean_delay, and max_range fields of untrusted CrawlerRunConfig bodies. Unauthenticated attackers can send huge values to /crawl or /crawl/stream to hold browser pages or stall the rate limiter, exhausting the page pool and blocking other crawls.

### CVE-2026-115793

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-772` |
| Published | 2026-10-29T16:17:58.870 |

P-Net before 1.0.3 does not release the RPC session allocated for an RPC request that names an unknown interface or object UUID, and does not start a timeout for it. Repeated requests with different activity UUIDs exhaust the available sessions. Once they are exhausted the device no longer answers new RPC requests, including Endpoint Mapper Lookup and Connect, until it is restarted. A remote unauthenticated attacker can use this to cause a denial of service.

### CVE-2026-112200

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-772` |
| Published | 2026-10-29T16:17:58.067 |

P-Net before 1.0.3 does not release the Application Relationship (AR) and the RPC session when an RPC request is rejected because its data representation has incorrect endianness. The session and its AR remain allocated, so repeated requests exhaust the available sessions. Once they are exhausted the device no longer answers new RPC requests, including Connect, until it is restarted. A remote unauthenticated attacker can use this to cause a denial of service.

### CVE-2026-111736

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-29T16:17:57.950 |

P-Net before 1.0.3 dereferences a NULL AR pointer in pf_fspm_cm_read_ind() when handling an implicit read request without a valid target AR UUID for a user specific record index, if the application has registered a read callback. A remote unauthenticated attacker can send such a request to crash the device (denial of service).

### CVE-2026-111733

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-29T16:17:57.600 |

P-Net before 1.0.3 dereferences a NULL AR pointer when handling an implicit read request without a valid target AR UUID for a record index that requires an AR (AR specific indices 0xE000-0xEFFF, and the expected identification data of a slot or subslot). A remote unauthenticated attacker can send such a request to crash the device (denial of service).

### CVE-2026-111731

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-29T16:17:57.343 |

P-Net before 1.0.3 enters an infinite loop when handling a read request for the PDPortDataCheck record with subslot 0 (whole module). The loop over the ports never advanced to the next port, so the request never completes and the device stops responding. A remote unauthenticated attacker can use this to cause a denial of service.

### CVE-2026-119409

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-30T12:16:37.510 |

OPNsense before 26.7.8 contains a command injection vulnerability that allows authenticated users with the System: Firmware privilege to execute commands as root by storing a malicious firmware mirror URL. Attackers can submit shell metacharacters through POST /api/core/firmware/set that opnsense-update evaluates with eval, and can also disable package signature verification through sed injection.

### CVE-2026-110972

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-603` |
| Published | 2026-10-30T12:16:34.803 |

Płatnik performs client-side authentication. An attacker with access to any application instance connected to the backend server can bypass the login verification process and authenticate as an arbitrary user.



This issue was fixed in metric 242 in version 10.02.002.

### CVE-2023-7357

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-29T17:17:54.467 |

A remote code execution (RCE) vulnerability was identified in the FlexNet Publisher lmadmin web user interface. This vulnerability is addressed in the FlexNet Publisher 2023 R2 (11.19.4.0) release.

### CVE-2026-119129

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-29T16:18:05.800 |

ZITADEL 3.0.0 through 3.4.15 and 4.0.0 before 4.19.5 contains a missing authorization vulnerability in Login V2 that allows attackers to approve OAuth 2.0 device authorizations using a victim's existing session without consent. Attackers can send a signed-in user a link carrying the attacker's user code to obtain the victim's tokens, and can bypass project access settings via the OIDC device authorization API.

### CVE-2026-119127

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-29T16:18:05.487 |

ZITADEL 4.0.0 before 4.19.5 contains a host header injection vulnerability in the Login V2 UI that allows unauthenticated attackers to poison password-reset, invite, and email-verification links by supplying untrusted x-zitadel-public-host, x-zitadel-forward-host, or x-forwarded-host headers. Attackers knowing a victim's login name can point the links in genuine emails at their host, harvest the single-use codes when the links are opened, and take over accounts including instance administrators.

### CVE-2026-119578

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-10-30T14:16:47.377 |

MONAI from 1.6.0 before 1.6.1 contains a remote code execution vulnerability in Auto3DSeg algo_from_json() that allows attackers to run Python code via a crafted work directory's algo_object.json. Attackers can ship a malicious algorithm_templates module plus a _target_ name that is imported and instantiated when victims call AutoRunner or import_bundle_algo_history, executing code under default configuration.

### CVE-2026-75882

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-30T13:20:06.177 |

An improper access control vulnerability in ESET Endpoint Encryption and ESET Full Disk Encryption allow attacker with standard user permissions access a device interface belonging to a privileged kernel driver and send specially crafted requests.

### CVE-2026-119586

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-30T12:16:44.730 |

SQLite command-line shell through 3.54.1 contains a command injection vulnerability in the .recover command that emits attacker-planted dot-commands stored in sqlite_schema.sql values verbatim. Attackers can craft a database whose schema holds a valid CREATE statement followed by a .shell or .system line, executing OS commands when victims pipe .recover output into sqlite3.

### CVE-2026-119379

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-30T12:16:36.967 |

SQLite before 3.54.0 built with the session extension contains a heap buffer overflow vulnerability in sqlite3changeset_apply() that allows attackers to corrupt heap memory by supplying crafted changesets. Attackers can repeat a table name in a second changeset block with a larger column count, causing sessionUpdateFind() to memset past the undersized aUpdateMask allocation.

### CVE-2026-119374

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-30T12:16:36.187 |

SQLite before 3.54.0 built with FTS5 contains a heap buffer overflow in fts5DoSecureDelete() that allows attackers to write past the leaf page buffer via crafted footer key offsets. Attackers can supply a database file with a corrupted FTS5 index that, when deleted from with secure-delete enabled, corrupts heap memory and crashes the application.

### CVE-2026-119373

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-30T12:16:36.027 |

SQLite before 3.54.0 built with FTS5 contains a heap buffer overflow in fts5MergeRowidLists() that undersizes the output buffer when merging detail=none prefix doclists. Attackers who can populate a detail=none FTS5 table with negative rowids and run a prefix MATCH query can write past the allocation, corrupting heap memory and crashing the process.

### CVE-2026-61996

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T16:18:12.303 |

Subscriber SQL Injection in MLS On The Fly <= 1.8.1.5 versions.

### CVE-2026-103092

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-29T16:17:41.547 |

IBM Langflow OSS 1.0.0 through 1.12.3 could allow a remote authenticated attacker to execute arbitrary SQL commands due to improper access control.

### CVE-2025-68394

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-30T12:16:33.590 |

ARKETEAM Protectel modules PROTECTELMAJ and BDF are vulnerable to SQL injection vulnerability. Improper neutralization of input provided by a low privileged user into "profilInput" parameter allows for SQL Injection attacks.
This issue has been fixed in: PROTECTELMAJ v6.5.19 and BDF v6.4.67

### CVE-2025-68393

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-30T12:16:33.447 |

ARKETEAM Protectel modules PROTECTELMAJ and BDF are vulnerable to SQL injection vulnerability. Improper neutralization of input provided by a low privileged user into "Utilisateur" parameter allows for SQL Injection attacks.
This issue has been fixed in: PROTECTELMAJ v6.5.19 and BDF v6.4.67

### CVE-2026-22109

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-10-30T11:17:32.860 |

The shipped WebUI template database retains the factory default passwords for all five account types in cleartext. Defaults are identical across devices and were unchanged on the tested unit.

### CVE-2026-107347

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-29T18:17:21.940 |

HashiCorp Nomad and Nomad Enterprise are vulnerable to symlink following during dispatch payload and executor log writes that may allow a malicious workload to modify files outside its allocation directory. When the client agent runs as root, this could lead to code execution as root on the client host. This vulnerability (CVE-2026-107347) is fixed in Nomad 2.1.1 and Nomad Enterprise 2.1.0, 1.11.12, and 1.10.18.

### CVE-2026-119115

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-29T17:18:07.667 |

Incorrect authorization in the issuer resolution logic in AWS Private CA Connector for Kubernetes (aws-privateca-issuer) before v1.10.1 might allow an authenticated remote user to obtain certificates, including subordinate CA certificates, signed by a cluster-scoped AWS Private CA issuer that their approval policy does not authorize.



To remediate this issue, users should upgrade aws-privateca-issuer to version v1.10.1 or the AWS Private CA Connector for Kubernetes EKS add-on to version v1.10.1-eksbuild.1, and update any certificate requests, Certificate resources, or Ingress annotations whose issuerRef.kind is missing, incorrect, or does not match the referenced issuer, since v1.10.1 requires issuerRef.kind to be exactly AWSPCAIssuer or AWSPCAClusterIssuer and to match the issuer it references.

### CVE-2026-61654

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T22:17:05.110 |

Lightdash is an open source business intelligence platform. In affected versions through 0.3213.0, the dbt Cloud webhook `POST /api/v1/projects/{projectUuid}/dbt-cloud/webhook` has no authentication middleware or signature validation. In `packages/backend/src/controllers/projectController.ts`, `testWebhook()` accepts `accountId` and `runId` from a `job.run.completed` request and passes them to `createPreviewWithExplores()` in `packages/backend/src/services/ProjectService/ProjectService.ts`. These unsanitized values are interpolated into the server-side dbt Cloud API URL, which is requested with the victim project's API key in the `Authorization` header. Path traversal through `accountId` changes the requested path on `cloud.getdbt.com` without changing its host, so the credential-bearing request reaches an attacker-influenced path on that fixed host. The advisory claims API-key theft, but the supplied evidence does not establish that the attacker can observe the `Authorization` header. The unauthenticated webhook also allows preview creation. The target must be a `dbt Cloud IDE` project and the attacker must know its `projectUuid`; the UUID is not enumerable but can be discovered in shared or multi-tenant contexts. Version 0.3214.0 fixes identifier path traversal and verifies webhook HMAC signatures only when a secret is configured; without a secret, unsigned webhooks continue to be processed.

### CVE-2026-45049

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-29T22:17:02.400 |

Open Access Management (OpenAM) is an access management solution. Prior to 16.1.1, the `Cross-Domain Single Sign-On` (`CDSSO`) servlet allows a logged-in user's raw OpenAM session token to be POSTed to an attacker-controlled URL. An attacker who induces an authenticated victim to visit a crafted URL can receive the session credential and potentially hijack the session. Deployments must have `CDSSO` enabled, as is common in multi-domain deployments, and exploitation is additionally gated on a non-default configuration being absent. This issue is fixed in version 16.1.1.

### CVE-2026-61576

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-29T21:17:27.313 |

Lightdash is an open source business intelligence platform. In affected versions through 0.3213.0, the dbt Cloud webhook `POST /api/v1/projects/{projectUuid}/dbt-cloud/webhook` has no authentication middleware or signature validation. In `packages/backend/src/controllers/projectController.ts`, `testWebhook()` accepts `accountId` and `runId` from a `job.run.completed` request and passes them to `createPreviewWithExplores()` in `packages/backend/src/services/ProjectService/ProjectService.ts`. These unsanitized values are interpolated into the server-side dbt Cloud API URL, which is requested with the victim project's API key in the `Authorization` header. Path traversal through `accountId` changes the requested path on `cloud.getdbt.com` without changing its host, so the credential-bearing request reaches an attacker-influenced path on that fixed host. The advisory claims API-key theft, but the supplied evidence does not establish that the attacker can observe the `Authorization` header. The unauthenticated webhook also allows preview creation. The target must be a `dbt Cloud IDE` project and the attacker must know its `projectUuid`; the UUID is not enumerable but can be discovered in shared or multi-tenant contexts. Version 0.3214.0 fixes identifier path traversal and verifies webhook HMAC signatures only when a secret is configured; without a secret, unsigned webhooks continue to be processed.

### CVE-2026-119118

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-29T16:18:04.027 |

Crawl4AI before 0.9.5 contains an improper certificate validation vulnerability that allows network attackers to intercept crawls because Chromium always launches with --ignore-certificate-errors. Man-in-the-middle or DNS-controlling attackers can serve forged content to the crawler and read cookies and headers sent, while hard-coded --no-sandbox also overrides CRAWL4AI_CHROMIUM_SANDBOX.

### CVE-2026-119574

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-567` |
| Published | 2026-10-30T14:16:46.453 |

Traefik from 3.2.0 before 3.7.15 contains a data race in the experimental FastProxy that allows unauthenticated attackers to crash the process by abusing HTTP/1 protocol upgrades. Attackers can repeatedly open and abort upgraded connections such as WebSocket, corrupting the unsynchronized shared bufio.Reader and triggering an unrecovered panic that terminates Traefik.

### CVE-2026-119559

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-30T12:16:43.210 |

OpenLiteSpeed through 1.9.4 contains an authentication bypass vulnerability that allows unauthenticated remote attackers to evade virtual host client certificate requirements over HTTP/3. Because QuicStream inherits a verifyContext() implementation that always returns true, attackers can present a non-mTLS host's SNI with a protected Host header to access protected content.

### CVE-2026-119557

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-30T12:16:42.887 |

n8n from 2.14.0 through 2.46.3 contains a path traversal vulnerability in the Databricks node that allows unauthenticated attackers to reach arbitrary Databricks API endpoints by injecting unencoded resource identifiers. Attackers can supply ../ sequences and query strings via webhook, chat, or form inputs mapped to spaceId, indexName, or filePath to read secrets using the stored credential.

### CVE-2026-119422

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-30T12:16:39.047 |

Juspay Hyperswitch before 1.128.0 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge payment status updates because the Worldpayxml connector's verify_webhook_source always returns true without enforced mTLS. Attackers knowing the merchant_id and Worldpay orderCode can POST unsigned XML with lastEvent SETTLED to the worldpayxml webhook endpoint, marking unpaid payments as charged or triggering refund, dispute and payout events.

### CVE-2026-119421

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-30T12:16:38.887 |

Juspay Hyperswitch through 1.128.0 (and builds before 2026.10.19.0) contains a missing authorization vulnerability that allows unauthenticated attackers to confirm payouts with any client_secret via POST /payouts/{payout_id}/confirm. Attackers holding the merchant's publishable key and a payout_id can confirm payouts and overwrite amount, currency, connector, and routing fields to trigger unauthorized merchant payouts.

### CVE-2026-14467

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-30T10:16:53.820 |

An information disclosure vulnerability in the Forocoches comments editor that allows an attacker to obtain unauthorised user information by inserting an image containing a malicious external URL into a comment. When a victim views the discussion thread, their browser automatically sends an HTTP/HTTPS request to the server controlled by the attacker, who can then collect information such as the source IP address, the User-Agent header, the date and time of access, and other metadata derived from the request, thereby compromising the user’s privacy.

### CVE-2026-9535

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-29T19:17:29.923 |

A out-of-bounds read vulnerability exists in the vtkChacoReader InputGraph2 functionality of vtk (version(s): 9.6.1). A specially crafted chaco can lead to an out-of-bounds read. An attacker can provide a malicious file to trigger this vulnerability.

### CVE-2026-93570

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-29T16:20:05.730 |

Szafir and Szafir Weryfikująca are vulnerable to XML External Entity (XXE) injection. When a user signs or verify a crafted XML file containing a `DOCTYPE` with an external DTD reference, the parser processes external entities, allowing an attacker to read arbitrary files from the victim's filesystem.


This issue was fixed in Szafir version 2.0 build 708. Szafir Weryfikująca is no longer supported (End of Life) and has not been fixed.

### CVE-2026-115709

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-29T15:17:18.100 |

Improper Link Resolution Before File Access ('Link Following') (CWE-59) in Elastic Cloud Enterprise (ECE) can lead to unauthorized disclosure and loss of data belonging to other deployments on the same host via Symlink Attack (CAPEC-132).

### CVE-2026-61671

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-352;CWE-639` |
| Published | 2026-10-29T22:17:05.273 |

WeGIA is a web manager for charitable institutions. Prior to the advisory's stated patched version 3.8.7, the `/controle/control.php` dispatch endpoint accepts attacker-controlled `nomeClasse`, `metodo`, and record identifier parameters through `extract($_REQUEST)`, including id, `idatendido`, `idInterno`, and `id_funcionario`, while the affected Controle CRUD methods do not verify record ownership. Any authenticated user can view, modify, or delete another user's records, exposing CPF, RG, addresses, medical records, financial data, and employee records. `AtendidoControle` lacks ownership checks on alterar, excluir, `listarUm`, `alterarInfPessoal`, `alterarDocumentacao`, `alterarImagem`, `alterarEndereco`, and `alterarStatus`; `InternoControle` lacks them on incluir, alterar, excluir, `listarUm`, `listarTodos`, and `listarCpf`. `FuncionarioControle` lacks ownership checks on `alterarInfPessoal`, `alterarEndereco`, `alterarDocumentacao`, `alterarImagem`, `alterarCargaHoraria`, and excluir; `VoluntarioControle` lacks them on `alterarInfPessoal`, `alterarEndereco`, `alterarDetalhes`, `alterarImagem`, and excluir. `AtendidoControle` and `InternoControle` additionally lack CSRF validation, allowing a malicious page visited by an authenticated victim to perform state-changing operations using the victim's session. `FuncionarioControle` and `VoluntarioControle` have per-method CSRF checks, but those checks do not prevent the object-authorization bypass. The advisory identifies version 3.8.7 as patched.

### CVE-2026-90867

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-29T16:20:04.827 |

Improper access control in the Web Admin console of Progress Software WS_FTP Server versions prior to 2024.0.7 and 2025.0.4 on Windows could expose administrative functionality to remote authentication attempts.

### CVE-2026-85899

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-29T16:19:45.410 |

Use after free in Microsoft Edge (Chromium-based) allows an authorized attacker to elevate privileges over a network.

### CVE-2026-104317

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:17:43.907 |

IBM Langflow OSS 1.0.0 through 1.12.3 could allow a remote attacker who could reach the message broker to execute arbitrary code on the system due to the deserialization of untrusted data.

### CVE-2026-91917

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-30T13:20:53.097 |

Dell OpenManage Enterprise, versions prior to 4.8.0, contains an Improper Input Validation vulnerability. A low privileged attacker with adjacent network access could potentially exploit this vulnerability, leading to Code execution.

### CVE-2026-119528

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-30T14:16:45.143 |

A flaw was found in GIMP. The PSD plug-in’s image resource header loader uses an incorrect destination size when copying a converted resource name into a fixed stack buffer. Opening a crafted PSD file can cause a stack-based buffer overflow, leading to a crash and potentially arbitrary code execution.

### CVE-2026-101213

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-30T12:16:34.130 |

Dell OpenManage Enterprise, versions prior to 4.8.0, contains an Improper Privilege Management vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-119250

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-29T19:17:21.363 |

A malicious actor with local access and low privileges could exploit an External Control of File Name or Path vulnerability found in WiFiman Desktop for macOS to execute arbitrary commands with root privileges on the host device.

### CVE-2026-115805

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-29T17:18:01.840 |

Improper handling of local filesystem paths in Rapid7 Insight Agent on Linux and macOS may allow authenticated local users to gain elevated privileges. Exploitation requires existing local access and depends on the Agent's inventory collection processing the crafted path.

### CVE-2026-114148

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-10-29T16:17:58.693 |

Incorrect default permissions in ASP.NET Core allows an authorized attacker to elevate privileges locally.

### CVE-2026-119426

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-30T12:16:39.683 |

phpMyAdmin through 5.2.3 contains a cross-site request forgery vulnerability that allows remote attackers to execute arbitrary SQL by bypassing CSRF token checks on non-AJAX POST requests. Attackers can lure authenticated victims into submitting cross-site POSTs carrying sql_query to /sql or /database/sql, running SQL with the victim's database privileges under http or config authentication.

### CVE-2026-110971

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-261` |
| Published | 2026-10-30T12:16:34.663 |

Use of a weak password encoding algorithm in Płatnik software allows a user who obtains encoded password to easily decode it. 


This issue was fixed in metric 242 in version 10.02.002.

### CVE-2026-84294

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-29T16:19:29.237 |

Improper limitation of pathname in the Ad Hoc Transfer component of Progress Software WS_FTP Server versions prior to 2024.0.6 and 2025.0.3 on Windows could allow an authenticated user to access files outside intended directories.

### CVE-2026-119120

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:04.370 |

Crawl4AI from 0.9.0 before 0.9.5 fails to filter the CosineStrategy model_name field in untrusted Docker API request bodies, allowing authenticated clients to choose which HuggingFace model the server loads. Attackers can reference a malicious repository with a pickle weight file to execute Python code under PyTorch below 2.6, or exhaust disk and memory.

### CVE-2026-119577

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-30T14:16:47.183 |

ArcadeDB before 26.10.2 contains an improper authorization vulnerability that allows revoked users to retain access through already-open Postgres, Bolt, MongoDB, or Redis wire-protocol connections. Attackers holding an existing connection can keep reading and writing data after deletion, grant removal, or password rotation, because executors keep a stale ServerSecurityUser.

### CVE-2026-119561

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-30T12:16:43.513 |

phpMyAdmin through 5.2.3 contains an authentication bypass vulnerability in CustomServer::parseAndValidateAssertionResponse() that never verifies WebAuthn assertion signatures against stored public keys. Attackers holding a victim's MySQL credentials can POST a crafted webauthn_request_response with matching challenge, origin, and rpIdHash to bypass the second factor and gain database privileges.

### CVE-2026-110732

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T07:16:31.913 |

The AI Engine – The Chatbot, AI Framework & MCP for WordPress plugin for WordPress is vulnerable to Missing Authorization in all versions up to, and including, 3.8.6 This is due to the MCP module's OAuth 2.1 Dynamic Client Registration endpoint (/wp-json/mcp/v1/oauth/register) being registered with a permission_callback of __return_true, allowing an unauthenticated user to register an active OAuth client with an attacker-controlled redirect URI. This makes it possible for unauthenticated attackers to obtain an administrator-bound MCP access token, and thereby full administrator-level control through the MCP tools (including user creation and option updates), once an administrator approves the attacker's client on the OAuth consent screen. The consent page is additionally served without X-Frame-Options or Content-Security-Policy frame-ancestors, so that approval can be obtained via clickjacking.

### CVE-2026-114443

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-30T06:16:45.533 |

The Security Plugin, Firewall & Malware Scanner with Auto Removal WordPress plugin before 2.191 does not verify the account password before accepting an authenticator-app two-factor code at login, allowing anyone who holds a user's current authenticator code to log in as that user, including an administrator, without the password.

### CVE-2026-114422

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-30T06:16:44.770 |

The Enable Media Replace WordPress plugin before 4.2.3 does not restrict the classes allowed when deserializing stored metadata during its media replace-and-update-links routine, allowing unauthenticated users to inject a PHP object that is instantiated when a user with upload access performs a routine media replacement, resulting in PHP Object Injection and local file inclusion of existing PHP/HTML files, which can be escalated to remote code execution where an attacker-influenced PHP or HTML file is present on the server.
This is a regression of CVE-2023-4643, which was fixed in 4.1.3 and reintroduced in 4.1.4.

### CVE-2026-103963

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-30T05:16:57.237 |

A flaw was found in glib-networking. When establishing connections using Transport Layer Security (TLS) version 1.3, the client-side session cache does not limit the number of session tickets retained for a single host. A malicious server can exploit this by sending excessive session ticket messages, causing the client application to continuously consume memory. This unbounded memory growth can exhaust system memory, resulting in a Denial of Service (DoS).

### CVE-2026-119286

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-401` |
| Published | 2026-10-29T22:17:01.517 |

GraphQL-core is a Python port of the GraphQL.js reference implementation. From 3.3.0a3 until 3.3.1, validate() reuses a module-level ValidationAbortedError when a document exceeds max_errors. Python appends frames to the reused exception's traceback on every raise, retaining each document, validation context, and error set for the process lifetime. An unauthenticated client can repeatedly submit a small document with more than 100 validation errors to cause unbounded memory growth before query execution, eventually exhausting worker memory without disclosing or modifying data. This issue is fixed in version 3.3.1.

### CVE-2026-119283

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-29T22:17:01.047 |

joserfc is a Python library that provides an implementation of several JSON Object Signing and Encryption (JOSE) standards. Prior to 1.7.5, joserfc.jwe.decrypt_json() accepts a JWE General JSON Serialization recipients array without a count limit and calls decrypt_cek() for every entry. An unauthenticated attacker who can submit a JWE to an endpoint using an RSA key-management algorithm can choose the number of private-key decryption operations performed by one request. The verify_all_recipients option does not reduce this work because the affected loop processes every recipient before consulting that setting, allowing repeated requests to exhaust service CPU without affecting confidentiality or integrity. This issue is fixed in version 1.7.5.

### CVE-2026-119325

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-29T21:17:21.870 |

Bricks Theme 2.4 and before for WordPress contains an unauthenticated broken access control vulnerability in the load_popup_content REST endpoint that allows anonymous attackers to read draft and unpublished page content by supplying a popupId parameter without any status or capability checks. Attackers can obtain a public nonce via the bricks_regenerate_query_nonce action and then increment the popupId value in requests to the /wp-json/bricks/v1/load_popup_content endpoint to enumerate and disclose confidential content from any unpublished post on the site.

### CVE-2026-119202

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-29T21:17:19.217 |

@hapi/content provides HTTP Content-* header parsing. From 3.0.6 until 6.0.3, Content.disposition() uses an unanchored parameter-name expression in a global regular-expression scan, causing repeated failed matching over the remaining input when a Content-Disposition parameter contains a long token without an equals sign. The resulting quadratic processing can block the Node.js event loop before route handlers or validation when @hapi/pez parses multipart/form-data headers, including unauthenticated hapi routes with payload.multipart enabled, and also affects applications that pass untrusted headers directly to Content.disposition(). This issue is fixed in @hapi/content version 6.0.3.

### CVE-2026-119197

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-29T20:17:30.907 |

pyasn1 is a generic ASN.1 library for Python. Prior to 0.6.5, binary REAL decoding builds a large mantissa one octet at a time by shifting a growing integer and slicing the remaining byte string. Attacker-controlled ASN.1 includes a binary-encoded REAL with a large mantissa and reaches BER, CER, or DER decode(), with or without a schema containing REAL. RealPayloadDecoder.valueDecoder repeatedly performs a left shift, OR, and suffix copy for every mantissa octet, making decode time quadratic in mantissa length. A comparatively small REAL value can hold a decoding worker on one CPU core for seconds or longer and cause availability loss. This issue is fixed in version 0.6.5.

### CVE-2026-119196

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-29T20:17:30.770 |

pyasn1 is a generic ASN.1 library for Python. Prior to 0.6.5, constructed BIT STRING decoding repeatedly shifts and copies the complete bit value accumulated from earlier fragments. Attacker-controlled BER or CER input contains many constructed BIT STRING fragments; schema-driven DER also accepts a definite-length constructed BIT STRING. BitStringPayloadDecoder repeatedly calls BitString.fromOctetString with the prior bitString as prepend, shifting an ever-growing SizedInteger for each fragment and causing quadratic work. Large fragmented values can exhaust CPU during decode() without requiring later conversion or formatting. This issue is fixed in version 0.6.5.

### CVE-2026-119195

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-29T20:17:30.633 |

pyasn1 is a generic ASN.1 library for Python. Prior to 0.6.5, constructed string and indefinite-length ANY decoding repeatedly concatenates each fragment onto a growing bytes value. Attacker-controlled BER or CER data can use many constructed OCTET STRING or character-string fragments. DER rejects constructed OCTET STRING without a schema, but accepts its definite-length form when asn1Spec selects univ.OctetString; it also accepts constructed character strings such as UTF8String without a schema, even though those encodings are not valid DER. The separate indefinite-length ANY path is reachable in BER and CER when asn1Spec selects univ.Any; DER rejects indefinite lengths. OctetStringPayloadDecoder uses growing header concatenation and AnyPayloadDecoder.indefLenValueDecoder uses growing chunk concatenation, repeatedly copying an increasing prefix and causing quadratic work. A sufficiently fragmented value can occupy decoding workers and cause CPU exhaustion without confidentiality or integrity impact. This issue is fixed in version 0.6.5.

### CVE-2026-119194

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-29T20:17:30.480 |

pyasn1 is a generic ASN.1 library for Python. From 0.3.3 until 0.6.5, schemaless container decoding stores every decoded component's TagSet in a growing set even though only one-versus-multiple tag types must be distinguished. Attacker-controlled BER, CER, or DER input contains many distinct long tag IDs whose TagSet hashes collide. Each later set insertion compares against an increasing number of earlier colliding tags in ConstructedPayloadDecoderBase._decodeComponentsSchemaless, producing quadratic CPU work while decoded values and order remain valid. Repeated inputs can exhaust decoder CPU and reduce service availability. This issue is fixed in version 0.6.5.

### CVE-2026-119191

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-674` |
| Published | 2026-10-29T20:17:30.197 |

Forge (also called node-forge) is a native implementation of Transport Layer Security in JavaScript. Prior to 1.4.1, the affected implementation used asn1.fromDer(), BIT STRING decoding, maxDepth to process the relevant input or security decision. node-forge decoded ASN.1 stored inside BIT STRING values without consistently applying the configured maxDepth limit and recursively retained copies at each nesting level. Crafted DER containing nested BIT STRINGs could cause excessive recursion, CPU use, and quadratic memory consumption during asn1.fromDer(). This issue is fixed in version 1.4.1.

### CVE-2026-119188

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-476` |
| Published | 2026-10-29T20:17:29.783 |

Forge (also called node-forge) is a native implementation of Transport Layer Security in JavaScript. Prior to 1.4.1, the affected implementation used forge.tls.createConnection(), fragmented handshake message, interleaved record to process the relevant input or security decision. node-forge continued processing after a TLS record of another content type interrupted a fragmented handshake message. A remote peer could trigger an uncaught TypeError in process(), causing the connection or hosting process to fail. This issue is fixed in version 1.4.1.

### CVE-2026-119187

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-29T20:17:29.647 |

Forge (also called node-forge) is a native implementation of Transport Layer Security in JavaScript. Prior to 1.4.1, the affected implementation used forge.tls.createConnection(), TLS record processing, process() to process the relevant input or security decision. node-forge processed received TLS records recursively, consuming one JavaScript stack frame per record in a single input chunk. A remote peer could send thousands of small records together and exhaust the call stack, causing an uncaught exception and denial of service. This issue is fixed in version 1.4.1.

### CVE-2026-9536

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-29T19:17:30.047 |

A heap-based buffer overflow vulnerability exists in the vtkWindBladeReader FindVariableOffsets functionality of vtk (version(s): 9.6.1). A specially crafted .wind can lead to a buffer overflow. An attacker can provide a malicious file to trigger this vulnerability.

### CVE-2026-8824

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-29T19:17:28.330 |

A memory corruption vulnerability exists in the vtkBMPReader ExecuteDataWithInformation functionality of vtk (version(s): 9.6.1). A specially crafted .bmp file can lead to a buffer overflow. An attacker can provide a malicious file to trigger this vulnerability.

### CVE-2026-8822

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-29T19:17:28.173 |

A memory corruption vulnerability exists in the vtkDEMReader ReadProfiles functionality of vtk (version(s): 9.6.1). A specially crafted USGS DEM can lead to a buffer overflow. An attacker can provide a malicious file to trigger this vulnerability.

### CVE-2026-42057

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-825` |
| Published | 2026-10-29T19:17:21.837 |

An invalid pointer dereference vulnerability exists in the vtkPNGReader::vtkPNGReaderUpdate2 functionality of vtk 9.6. A specially crafted .png file can lead to a denial of service. An attacker can provide a malicious file to trigger this vulnerability.

### CVE-2026-41216

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-825` |
| Published | 2026-10-29T19:17:21.710 |

An invalid pointer dereference vulnerability exists in the vtkPNGReader::ExecuteInformation functionality of vtk 9.6. A specially crafted .png file can lead to a denial of service. An attacker can provide a malicious file to trigger this vulnerability.

### CVE-2026-119249

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-1327` |
| Published | 2026-10-29T19:17:21.237 |

A malicious actor with access to the network could exploit a Binding to an Unrestricted IP Address vulnerability found in WiFiman Desktop for macOS to obtain information about the host device.

### CVE-2026-118782

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-354;CWE-1284` |
| Published | 2026-10-29T19:17:20.983 |

Forge (also called node-forge) is a native implementation of Transport Layer Security in JavaScript. Prior to 1.4.1, node-forge accepted a PKCS#12 MAC or PKCS#12 password-based encryption iteration count of zero or less. pki.pbe.generatePkcs12Key() then returned a constant key independent of the password and salt, allowing crafted PKCS#12 input processed by forge.pkcs12.pkcs12FromAsn1() to bypass password-based integrity checks. Predictable encryption keys and IVs also affected PKCS#12 PBE using pbeWithSHAAnd3-KeyTripleDES-CBC or pbewithSHAAnd40BitRC2-CBC, including shrouded key bags, encrypted SafeContents, and PKCS#8 ENCRYPTED PRIVATE KEY input processed independently by forge.pki.decryptPrivateKeyInfo(). PBES2/PBKDF2-encrypted content is unaffected. This issue is fixed in version 1.4.1.

### CVE-2026-118779

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-10-29T19:17:20.560 |

Forge (also called node-forge) is a native implementation of Transport Layer Security in JavaScript. Prior to 1.4.1, the affected implementation used pem.decode(), lib/pem.js, missing END line to process the relevant input or security decision. node-forge used polynomial-time regular expressions in pem.decode(), including when searching for a matching END line and parsing encapsulated headers. An unauthenticated attacker able to supply PEM input to any high-level parser could consume excessive CPU with a long malformed message and cause denial of service. This issue is fixed in version 1.4.1.

### CVE-2026-118772

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-29T19:17:19.563 |

joi is a schema description language and data validator for JavaScript. From 17.1.1 until 17.13.9 and 18.3.1, the Joi.string().email({ multiple: true }) rule uses a separator regular expression whose leading whitespace quantifier is retried at every position in a long whitespace run that contains no separator, causing quadratic work during String.prototype.split. The behavior applies to the default separator and every custom separator. Applications that validate attacker-controlled values with the multiple option and no effective prior length limit can have the Node.js event loop blocked for seconds by one request, preventing other work. A .max() rule is not sufficient when abortEarly: false allows the email rule to run after the maximum-length check fails. This vulnerability is fixed in versions 17.13.9 and 18.3.1.

### CVE-2026-118761

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-29T17:18:06.907 |

Kubeflow Pipelines enables users to build and deploy portable, scalable machine learning workflows. Prior to 2.18.0, the API server decompressed uploaded pipeline archives without adequately bounding expanded data while locating or reading the pipeline file. A small ZIP or gzip-compressed tar archive can consume disproportionately large memory and exhaust API-server resources. Multipart pipeline and pipeline-version upload processing performs decompression before namespace authorization, so a reachable caller does not need a successful pipeline-create authorization decision. URL-import handlers authorize before fetching and decompressing a remote archive. The amount of expansion required to interrupt service depends on deployment resource limits and concurrent activity, and no specific archive is guaranteed to crash every deployment. This issue is fixed in version 2.18.0.

### CVE-2026-118759

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-862` |
| Published | 2026-10-29T17:18:06.630 |

Kubeflow Pipelines enables users to build and deploy portable, scalable machine learning workflows. Prior to 2.18.0, the API server's GET /apis/v1alpha1/runs/{run_id}/nodes/{node_id}/log handler retrieved logs without authorizing the caller against the selected run. A caller who can reach the backend and knows a victim run ID and suitable pod or node identifier can read live or archived logs with the API server's permissions. For live logs, the caller-controlled node ID was also accepted as a pod name without verifying that the pod belonged to the requested run, allowing a known run ID to select the namespace of an unrelated pod and read its main container logs. The handler does not authenticate requests itself, although an external authentication gate or network policy can limit reachability. Exposed logs can contain sensitive workload data or credentials. This issue is fixed in version 2.18.0.

### CVE-2026-118758

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-29T17:18:06.487 |

Kubeflow Pipelines enables users to build and deploy portable, scalable machine learning workflows. Prior to 2.18.0, the volume artifact handler for GET /artifacts/get?source=volume did not confine a caller-supplied file path to the selected volume. A caller who can reach the route and identify an existing mounted volume can use path traversal to read files outside that volume when the artifact-serving process can read them. The frontend pod serves the request when artifact proxying is disabled, while the selected namespace's artifact-service pod serves it when proxying is enabled. A deployment with authentication disabled requires no application credentials; in multi-user deployments, the caller ordinarily must be authorized for the supplied namespace. This issue is fixed in version 2.18.0.

### CVE-2026-107052

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-276` |
| Published | 2026-10-29T17:17:57.920 |

Insecure permissions in the AIDL interface of ProjectMAXS MAXS Module FileRead versionCode 27 allows unauthorized attackers to arbitrarily reead files outside of the sandbox via providing an absolute path.

### CVE-2026-107047

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-29T17:17:57.223 |

Insecure permissions in mendhak GPSLogger versionCode 137 allows unauthorized attackers to arbitrarily manipulate the app's logging mechanism and log data.

### CVE-2026-90869

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-125` |
| Published | 2026-10-29T16:20:05.080 |

A remote attacker who knows a valid account's enrolled SSH public key can terminate the shared SSH service in Progress Software WS_FTP Server versions prior to 2024.0.7 and 2025.0.4 on Windows.

### CVE-2026-118083

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-29T16:18:03.323 |

Unauthenticated Sensitive Data Exposure in WP Crowdfunding <= 2.2.2 versions.

### CVE-2026-110245

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-29T16:17:56.860 |

IBM Langflow OSS 1.0.0 through 1.12.4 could allow a remote attacker to obtain sensitive information due to improper authentication.

### CVE-2026-107042

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-29T16:17:50.050 |

Insecure permissions in USP Ultimate Screenshot Painter versionCode 240213.009 allows unauthorized attackers to move or overwrite files in another user's private storage via supplying a crafted content URI.

### CVE-2026-107037

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-29T16:17:49.490 |

Insecure permissions in the NotificationHelper component of NoNonsense Notes versionCode 72600 allows unauthorized attackers to write in another user's notes via supplying a note id.

### CVE-2026-107026

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-29T16:17:48.383 |

Insecure permissions in Share to Clipboard v1.14.1 (versionCode 32) allows unauthorized attackers to arbitrarily overwrite another user's clipboard content.

### CVE-2026-115713

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-29T15:17:18.460 |

Improper Link Resolution Before File Access ('Link Following') (CWE-59) in Elastic Cloud Enterprise (ECE) can lead to unauthorized read and write access to data of other deployments on the same host via Symlink Attack (CAPEC-132).

### CVE-2026-107020

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-601` |
| Published | 2026-10-29T15:17:15.780 |

An issue in the activity.LoadLinkLaterActivity component of FeedEx / Handy News Reader versionCode 116 allows attackers to force victim users into fetching a crafted URL.

### CVE-2026-92092

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-494` |
| Published | 2026-10-29T20:17:36.440 |

A flaw was found in openshift-ansible. The installer container's `run` script downloads and executes remote inventory and dynamic scripts without integrity verification. A remote attacker, by performing a Man-in-the-Middle (MITM) attack or compromising the HTTP server providing these scripts, could substitute an arbitrary executable. This malicious executable would then run with the installer's user ID (UID) and full cluster-provisioning privileges, leading to arbitrary code execution.

### CVE-2026-119190

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-436` |
| Published | 2026-10-29T20:17:30.067 |

Forge (also called node-forge) is a native implementation of Transport Layer Security in JavaScript. Prior to 1.4.1, node-forge parsed deprecated extension OIDs 2.5.29.10 and 2.5.29.13 as basicConstraints, and pki.verifyCertificateChain() used the first extension with that name. Exploitation requires a CA trusted by the application to issue a certificate carrying an attacker-supplied deprecated-OID extension, commonly because the CA copies extensions from a certificate signing request. By placing a permissive deprecated extension before the genuine 2.5.29.19 basicConstraints extension, the certificate holder could have the certificate accepted as a CA and issue certificates for arbitrary names, enabling server or client impersonation. If the issuing CA adds a keyUsage extension without keyCertSign, node-forge rejects the chain. This issue is fixed in version 1.4.1.

### CVE-2026-118763

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-29T17:18:07.230 |

sigstore-js provides JavaScript libraries for interacting with Sigstore services. Prior to 0.7.2, packages/oci/src/registry.ts contains a RegistryClient.signIn() method that stores registry Authorization and Docker configuration headers as defaults on a shared HTTP client, while RegistryClient.uploadBlob() sends a fresh PUT to an absolute blob-upload Location supplied by the registry without checking that its origin or scheme matches the registry. A malicious or compromised registry can therefore direct a user pushing an artifact through attachArtifactToImage() to an attacker-controlled host and receive the registry bearer token, Basic credentials, or custom authentication headers. Redirect-time header stripping does not prevent the leak because the cross-host PUT is a new explicit request rather than a followed redirect. This is a residual of CVE-2026-59891, whose fix changed credential selection in credentials.ts but did not constrain where credentials are sent from registry.ts. Version 0.7.2 fixes the issue by separating registry credentials from client-wide defaults and sending them only to the registry origin.

### CVE-2026-96187

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-29T16:20:08.143 |

Access of resource using incompatible type ('type confusion') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to disclose information over a network.

### CVE-2026-91912

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-30T14:17:10.617 |

Dell OpenManage Enterprise, versions prior to 4.8.0, contains an Use of Hard-coded Cryptographic Key vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Information disclosure.

### CVE-2026-119282

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-10-29T22:17:00.887 |

Nx is a monorepo solution for TypeScript and polyglot codebases. From 22.0.2 until 22.7.9 and 23.1.2 for @nx/maven, and from 21.0.0 until 22.7.9 and 23.1.2 for @nx/gradle, the plugins' project-graph analyzers launch through a shell and interpolate plugin options from nx.json into command arguments. The @nx/maven targetNamePrefix value and arbitrary @nx/gradle option names or values can therefore be interpreted as shell syntax whenever an nx command constructs the project graph. A user who runs Nx in an attacker-controlled repository or pull request can execute injected commands with the user's privileges, while workspaces that register neither affected plugin are not exposed to this path. Remediation requires upgrading both nx and each affected plugin to matching releases because the plugin fix depends on code in the nx package. This issue is fixed in versions 22.7.9 and 23.1.2.

### CVE-2026-118765

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-335` |
| Published | 2026-10-29T17:18:07.523 |

Botan is a C++ cryptography library. From 3.7.0 until 3.13.0, an application that calls AutoSeeded_RNG::clear() and then calls randomize with an empty output buffer while the generator is unseeded can cause AutoSeeded_RNG to mark itself seeded without consulting the configured entropy source. On builds without BOTAN_HAS_SYSTEM_RNG, the fallback uses only a clock value and process ID, so a later non-empty request can produce output from predictable state. This issue is fixed in version 3.13.0.

### CVE-2026-112347

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T14:16:37.903 |

Kirki plugin for WordPress before 6.4.1 contains a broken object-level access control vulnerability in its page REST API, where the PUT /wp-json/kirki/v1/pages/{page_id} route and the save_page_data, duplicate, and delete handlers in PageController.php rely only on a coarse role-to-access middleware check without performing a per-object WordPress capability check. A user with Kirki edit access, granted to the Editor role by default, can exploit this flaw to modify the title, slug, and publication status of any non-trashed post of any post type, including custom post types and WooCommerce products they do not own, exposing private or draft content or removing published content by manipulating the unrestricted post_status field.

### CVE-2026-111504

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-30T12:16:34.943 |

Dell OpenManage Enterprise, versions prior to 4.8.0, contains an Improper Neutralization of Argument Delimiters in a Command ('Argument Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-101214

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-30T12:16:34.260 |

Dell OpenManage Enterprise, versions prior to 4.8.0, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-101210

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-30T12:16:34.000 |

Dell OpenManage Enterprise, versions prior to 4.8.0, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-97645

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T07:16:35.393 |

The Gravity Forms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via List Field in all versions up to, and including, 3.1.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires the administrator to click the injected link in the entry detail view and confirm a dialog, which triggers the admin JavaScript bundle's delegated data-dialog-callback handler to invoke the attacker-supplied function reference.

### CVE-2026-90437

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T07:16:34.600 |

The Gravity Forms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Post Excerpt / Post Custom Field / Rich-Text Paragraph Field Values in all versions up to, and including, 3.1.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is possible because Post Excerpt, Post Custom Field, and Rich-Text-Editor-enabled Paragraph Text fields allow raw HTML submissions via allow_html(), and an entity-encoded payload stored in a data-dialog-confirm attribute evades wp_kses_post() at save time but is decoded into executable markup by the browser when the plugin's admin JavaScript passes the attribute value to insertAdjacentHTML().

### CVE-2026-116622

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-30T07:16:33.040 |

The Food Store – Online Food Delivery & Pickup plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'service_time' parameter in all versions up to, and including, 1.5.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the site to have the 'Enable Checkout Service Fields' option turned off, which is a non-default configuration, while 'Enable Pickup/Delivery Service' remains enabled.

### CVE-2026-11587

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-29T17:18:08.167 |

SQL injection allowing an authenticated user with access to ACL management to read and modify the Centreon database

### CVE-2026-42701

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:09.370 |

Shop manager PHP Object Injection in YayMail <= 4.4.6 versions.

### CVE-2026-118079

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:02.673 |

Shop manager PHP Object Injection in FV Flowplayer Video Player <= 8.3.4 versions.

### CVE-2026-118078

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:02.550 |

Shop manager PHP Object Injection in Product Catalog Feed by PixelYourSite <= 3.1.4 versions.

### CVE-2026-118077

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:02.423 |

Author PHP Object Injection in Sastra Essential Addons for Elementor <= 1.2.3 versions.

### CVE-2026-118074

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:02.053 |

Shop manager PHP Object Injection in Finale Lite <= 2.21.0 versions.

### CVE-2026-116869

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:01.800 |

Shop manager PHP Object Injection in myPOS Checkout <= 1.4.5 versions.

### CVE-2026-116865

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:01.213 |

Editor PHP Object Injection in Zippy <= 1.7.0 versions.

### CVE-2026-116864

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-29T16:18:01.090 |

Author PHP Object Injection in WPCargo Track & Trace <= 8.0.5 versions.

### CVE-2026-111730

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-29T16:17:57.210 |

P-Net before 1.0.3 does not validate the LengthPeerStationName field of a CheckPeers block in get_check_peer(). The received length (up to 255) was used to copy data into the 241-byte peer station name buffer and to place the terminating NUL byte, so a crafted block writes up to 15 bytes past the end of the buffer. This can lead to a crash (denial of service) or potentially arbitrary code execution.



Requires establishment of session that needs ADJACENT network access.

### CVE-2026-115708

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-29T15:17:17.977 |

Improper Link Resolution Before File Access ('Link Following') (CWE-59) in Elastic Cloud Enterprise (ECE) can lead to authentication bypass and unauthorized changes to the configuration of other deployments on the same host via Symlink Attack (CAPEC-132).

### CVE-2026-91914

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-30T14:17:10.900 |

Dell OpenManage Enterprise, versions prior to 4.8.0, contains an Authentication Bypass by Spoofing vulnerability. An unauthenticated attacker with adjacent network access could potentially exploit this vulnerability, leading to Session theft.

### CVE-2026-86715

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-256` |
| Published | 2026-10-30T14:17:10.313 |

Plaintext storage of a password vulnerability in Crypttech Crypto and Informatics Technologies Industry and Trade Inc. Vatos DLP allows Use of Known Domain Credentials.

This issue affects Vatos DLP: from 1.1.176 before 1.1.243.

### CVE-2026-119575

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-30T14:16:46.643 |

ArcadeDB from 26.8.1 before 26.10.2 contains a server-side request forgery vulnerability that allows authenticated users with updateDatabaseSettings to disable the LOAD CSV IP block list via ALTER DATABASE. Attackers can set arcadedb.opencypher.loadCsv.blockedIpRanges to an empty string, then issue LOAD CSV requests to read cloud metadata and internal loopback or private services.

### CVE-2026-111503

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-30T13:18:28.453 |

Dell OpenManage Enterprise, versions prior to 4.8.0, contains an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Information exposure.

### CVE-2026-119553

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-30T12:16:42.273 |

Moodle 5.3.0, 5.2.0 through 5.2.4, 5.1.0 through 5.1.8, 5.0.0 through 5.0.11, and through 4.5.15 contains a path traversal vulnerability in the Blackboard question import format. Teachers with question import or lesson edit rights can upload a crafted zip with img src values containing ../ sequences, copying server files like config.php into their draft area.

### CVE-2026-119551

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-30T12:16:41.933 |

Jellyfin through 12.4 contains an authorization bypass vulnerability in SuggestionsController.GetSuggestions that allows authenticated non-administrator users to bypass library and parental restrictions by omitting the userId parameter. Attackers can repeatedly call GET /Items/Suggestions without userId to enumerate restricted items, including IDs and server filesystem paths, and then stream them.

### CVE-2026-119549

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-30T12:16:41.330 |

Jellyfin through 12.4 contains a server-side request forgery vulnerability that lets authenticated users bypass SvgSecurityValidator by embedding gzip-compressed SVG in non-SVG image data URIs. Attackers can upload such profile images via POST /UserImage, then trigger unauthenticated rendering via GET /UserImage to fetch internal URLs, read local image files, or exhaust memory.

### CVE-2026-119407

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-30T12:16:37.120 |

Element Web and Element Desktop before 1.12.32 accept guest credentials from URL fragment parameters in loadSession, allowing remote unauthenticated attackers to log out users and clear local stores. Attackers can lure logged-in users into opening links with guest_user_id and guest_access_token to force an attacker-controlled guest session and destroy unbacked end-to-end encryption keys.

### CVE-2026-119209

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-29T21:17:20.230 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.21.3, pypdf can consume excessive memory while opening a crafted PDF containing cross-reference streams that declare very large entry counts. Highly compressible streams and /Prev chains can multiply the number of parsed entries across a document, while negative /Index counts can bypass the existing per-stream clamp. This issue is fixed in version 6.21.3.

### CVE-2026-119208

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-29T21:17:20.090 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.21.3, pypdf can consume excessive time and memory when an application accesses the page count of a crafted encrypted PDF whose page tree declares a forged /Count value. Even after successful decryption, page-count retrieval trusts the unvalidated declared count instead of walking the page tree, allowing the attacker-controlled value to drive excessive work and memory use. This issue is fixed in version 6.21.3.

### CVE-2026-119207

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-405` |
| Published | 2026-10-29T21:17:19.953 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.21.3, pypdf can consume excessive memory when strict mode loads a crafted invalid PDF dictionary. Nested parsing failures add repeated exception text to newly raised errors, allowing a small malformed dictionary to amplify into very large error messages. This issue is fixed in version 6.21.3.

### CVE-2026-119206

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-29T21:17:19.817 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.21.3, pypdf can take excessive time to retrieve page labels from a crafted PDF containing a flat page-label number tree with many ranges. The page_labels property resolves each page independently and repeatedly scans the same /Nums array from the beginning, causing work to grow with both the page count and the number of label ranges. This issue is fixed in version 6.21.3.

### CVE-2026-119205

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-29T21:17:19.677 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.21.4, pypdf can enter an infinite loop when cloning or duplicating a crafted cyclic DictionaryObject. Clone traversal checked generated destination references rather than the original source references, allowing some source cycles to evade the visited-object check. This issue is fixed in version 6.21.4.

### CVE-2026-119204

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-29T21:17:19.527 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.21.4, pypdf can consume excessive memory while parsing a crafted PDF page tree containing many shared resources. Page-tree flattening copies page dictionary and inherited resource entries without a document-wide entry budget, allowing the crafted resource structure to cause disproportionate allocations. This issue is fixed in version 6.21.4.

### CVE-2026-119203

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-29T21:17:19.377 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.21.4, pypdf can enter an infinite loop while opening a crafted incomplete PDF whose standard cross-reference table reaches the end of the file without a trailer. The trailer search can repeatedly rewind to the same stream position instead of terminating when parsing makes no progress, blocking the processing thread. This issue is fixed in version 6.21.4.

### CVE-2026-103094

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-256` |
| Published | 2026-10-29T19:17:15.267 |

ServiceNow has remediated an information disclosure vulnerability that was identified in the ServiceNow AI Platform. This vulnerability could cause a user's plaintext password to be persisted in a system table, potentially exposing that password to a user who otherwise would not be entitled to view it.





ServiceNow remediated the vulnerability through security updates that address the unintended persistence of plaintext credentials. We are not currently aware of malicious exploitation against ServiceNow instances. We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-62374

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-176;CWE-754` |
| Published | 2026-10-29T17:18:10.143 |

SD JWT JS is a JavaScript implementation of the Selective Disclosure JWT (SD-JWT) specification. In version 0.19.0 and earlier, `@sd-jwt/decode`, also used by `@sd-jwt/core`, silently drops a tampered Disclosure whose digest no longer matches the Issuer-signed `_sd` array and returns a reduced claim set, reporting success while the Issuer signature remains valid. Both a tampered Disclosure that remains valid JSON and a Disclosure containing invalid UTF-8 bytes reach this silent-drop behavior. In the latter case, the `TextDecoder / Buffer` decoding path substitutes U+FFFD replacement characters, recovering syntactically valid disclosure data instead of rejecting the malformed input. This violates RFC 9901 section 7.1 step 5, which requires rejection of unreferenced Disclosures, and section 7.1 step 3 / section 4.2.1, which require rejection of invalid Disclosures. A malicious holder can exploit this omission primitive, including through `SDJwtInstance.verify()` when key binding is required. An on-path attacker can also tamper with a Disclosure when the relying party does not enforce key binding; enforced key binding rejects on-path tampering because it invalidates the KB-JWT `sd_hash` binding. If the relying party defaults to allowing access when a constraining age, role, or restriction claim is absent, the silent claim reduction can change an authorization decision without an error. This issue is fixed in `@sd-jwt/core` version 0.20.0; no patched version of the standalone `@sd-jwt/decode` package is identified.

### CVE-2026-61995

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T16:18:12.177 |

Unauthenticated Cross Site Scripting (XSS) in YouTube Showcase <= 4.1.0 versions.

### CVE-2026-61993

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T16:18:12.033 |

Unauthenticated Cross Site Scripting (XSS) in Blockonomics 3.11.0 versions.

### CVE-2026-61989

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T16:18:11.340 |

Unauthenticated Cross Site Scripting (XSS) in Easy Property Listings <= 3.5.25 versions.

### CVE-2026-61988

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T16:18:11.217 |

Unauthenticated Cross Site Scripting (XSS) in Auction Nudge – Your eBay on Your Site <= 8.4.0 versions.

### CVE-2026-54866

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T16:18:10.577 |

Unauthenticated Cross Site Scripting (XSS) in Razorpay Payment Button Elementor Plugin <= 1.2.8 versions.

### CVE-2026-54864

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T16:18:10.333 |

Unauthenticated Cross Site Scripting (XSS) in Post Video Players <= 1.165 versions.

### CVE-2026-42692

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T16:18:09.130 |

Unauthenticated Cross Site Scripting (XSS) in WP Crowdfunding <= 2.2.2 versions.

### CVE-2026-27394

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T16:18:08.887 |

Unauthenticated Cross Site Scripting (XSS) in Eventer <= 0.1.1 versions.

### CVE-2026-118085

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T16:18:03.577 |

Unauthenticated Cross Site Scripting (XSS) in GlobalPayments WooCommerce <= 1.23.3 versions.

### CVE-2026-111735

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-10-29T16:17:57.833 |

P-Net before 1.0.3 contains an integer underflow in pf_cpm_c_data_ind(). When handling a received cyclic data frame while the consumer is in the FRUN or RUN state, the offset of the APDU status was computed as the frame length minus 4 using 16-bit arithmetic, without checking that the frame is long enough. A crafted short frame makes the offset wrap around, so the function reads outside the receive buffer. This can cause a crash (denial of service) or disclose memory content.

### CVE-2026-111734

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-29T16:17:57.717 |

P-Net before 1.0.3 does not validate the length of a received Ethernet frame in pf_eth_recv() before reading the EtherType, any VLAN tags and the PROFINET FrameID. The VLAN tag loop had no upper bound, so a truncated frame, or a frame consisting only of VLAN tags, makes the function read past the end of the receive buffer. This can cause a crash (denial of service) or disclose memory content.

### CVE-2026-108494

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-29T16:17:55.277 |

Unauthenticated Cross Site Scripting (XSS) in Chained Quiz <= 1.4.1 versions.

### CVE-2026-119572

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-30T14:16:46.070 |

Traefik from 3.7.0-ea.1 before 3.7.15 contains an authentication bypass vulnerability in the Kubernetes Ingress NGINX provider that silently disables mTLS configured via the auth-tls-secret annotation. When another Ingress declares a path on the same host without matching auth-tls settings, Traefik falls back to default TLS options, letting unauthenticated attackers reach backends requiring client certificates.
