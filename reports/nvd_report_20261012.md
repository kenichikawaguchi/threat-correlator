# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-11 15:00 UTC
- **対象期間**: `2026-10-10T15:01:21.000Z` 〜 `2026-10-11T15:00:30.000Z`
- **重要CVE数**: 215 件（Critical 9.0+: 63 件 / High 7.0〜: 152 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で報告された CVE のうち **CVSS 7.0 以上** が 40 件以上に上り、特に **リモートから認証不要でコード実行が可能** な脆弱性が集中しています。  
- WordPress エコシステム（プラグイン・テーマ）に対する **PHP Object Injection** 系の脆弱性が大量に報告され、同一手法で多数のサイトが一括で侵害され得る状況です。  
- ネットワーク機器や SaaS バックアップ製品にも **OS コマンドインジェクション**・**任意ファイルアップロード** が確認され、インフラ層とアプリ層の両方で「外部から直接コード実行」できるリスクが顕在化しています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑108576** | 10.0 | TOZED X300 (≤ 6.01.3) の `process_ping` で **OS コマンドインジェクション** が可能 | ネットワーク機器は外部から直接攻撃されると、内部ネットワーク全体への踏み台化が容易になる。ファームウェア更新が必須。 |
| **CVE‑2026‑42696** | 10.0 | SiteVault – Backup, Restore, Migration & Cloning (≤ 1.5.19) の **認証なし RCE** | バックアップ・復元サービスは管理者権限で実行されることが前提。未認証でコード実行できるため、全顧客データが即座に漏洩・改ざんされる危険がある。 |
| **CVE‑2026‑62129** | 9.9 | Creator LMS (≤ 1.2.21) の **任意ファイルアップロード**（Contributor 権限） | LMS は教育機関・企業で広く利用。権限が低いユーザーでも PHP ファイルを配置でき、管理者権限取得に直結。 |
| **CVE‑2026‑85118** | 9.8 | AI Content Generator Marketing WordPress プラグイン (≤ 1.0.0) の **AJAX でオプション操作** が無認証 | WordPress のオプションテーブルを書き換えるだけで **管理者権限取得** が可能。プラグインがインストールされている全サイトが対象。 |
| **CVE‑2026‑78535** (代表例) | 9.8 | 複数 WordPress テーマ/プラグイン (例: Buzz Stone, Photolia, Qwery など) の **PHP Object Injection** | 同一手法で 20 以上のテーマ・プラグインが影響。攻撃コードが共通化しやすく、スキャンツールで一括検出・悪用が可能。 |

> **共通点**：すべて **ネットワークから直接アクセス可能**（`AV:N`）で、**認証不要**、かつ **完全なコード実行**（`C:H/I:H/A:H`）が可能です。特に WordPress 系はインストールベースが大きく、被害拡大リスクが高い点に注意が必要です。

---

## 3. 推奨アクション  

### 3.1 直ちに実施すべき緊急対策
- **脆弱製品・プラグインのバージョン確認**  
  - `TOZED X300` → 6.01.4 以降にアップデート（ベンダー提供のパッチがリリース済みか確認）  
  - `SiteVault` → 1.5.20 以降へ更新、もしくは一時的にバックアップ機能を無効化  
  - `Creator LMS` → 1.2.22 以降にアップデート、ファイルアップロード先のディレクトリ権限を **0750** へ制限  
  - `AI Content Generator Marketing` (WordPress) → 1.0.1 以降に更新、またはプラグインを無効化  
  - すべての **PHP Object Injection 系プラグイン/テーマ**（Buzz Stone, Photolia, Qwery, Jacqueline, Alliance, Kicker, Original, Anesta, FC United, ShiftCV, Windsor, Education Center, Drone Media, Asia Garden, N7 Golf, Invetex, Law Office, WineShop など） → 公式が提供する **修正版** が出ているか確認し、未提供の場合は **即時無効化**  

- **WAF/IPS でのブロック**  
  - `process_ping` の `Host` パラメータに対する **OS コマンド文字列**（`;`, `&&`, `|` など）を検知しブロック  
  - WordPress の `wp-admin/admin-ajax.php` への **POST** で `action` がプラグイン固有のもの（例: `ai_content_generator_update_option`）の場合は **CSRF トークン必須** とするルールを追加  
  - PHP Object Injection に利用されやすい `unserialize()` 呼び出しパラメータ（例: `?action=...&data=`）を **長さ・文字種** で制限  

- **権限・ファイルシステムの最小化**  
  - `Creator LMS`・`CodeBard Help Desk` のアップロードディレクトリは **web サーバーから実行不可**（`php_flag engine off`）に設定  
  - WordPress の `wp-content/uploads` 以外の書き込み可能ディレクトリは **所有者を www-data に限定**、実行権限は付与しない  

### 3.2 中長期的な防御策
- **定期的な脆弱性スキャン**  
  - NVD・JVN の API を利用し、**CVSS ≥ 7.0** の新規 CVE を週次で取得し、対象製品・プラグインのバージョンと照合  
- **サードパーティプラグインの使用ポリシー策定**  
  - 「公式リポジトリに掲載されていないプラグインは原則使用禁止」  
  - 使用許可を出す際は **開発元のセキュリティレビュー** と **過去の CVE 実績** を必ずチェック  
- **コードレビュー・サニタイズ徹底**  
  - `unserialize()` の使用は **JSON** へ置き換える、または **`allowed_classes`** オプションで制限  
  - 外部入力（GET/POST/COOKIE）に対しては **ホワイトリスト方式** のバリデーションと **エスケープ** を必ず実装  
- **インシデントレスポンス体制の整備**  
  - 重大脆弱性が公開された際の **緊急パッチ適用フロー**（担当者・承認手順・

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-108576

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-11T13:17:13.067 |

A vulnerability was found in TOZED X300 up to 6.01.3. This vulnerability affects the function process_ping of the component IPPingDiagnostics Handler. The manipulation of the argument Host results in os command injection. The attack can be launched remotely. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-42696

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-10T20:16:35.313 |

Unauthenticated Remote Code Execution (RCE) in SiteVault – Backup, Restore, Migration &amp; Cloning <= 1.5.19 versions.

### CVE-2026-62129

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-10T20:16:44.780 |

Contributor Arbitrary File Upload in Creator LMS <= 1.2.21 versions.

### CVE-2026-62024

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-10T20:16:38.750 |

Subscriber Arbitrary File Upload in CodeBard Help Desk <= 1.1.2 versions.

### CVE-2026-85118

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-11T07:17:25.900 |

The AI Content Generator Marketing WordPress plugin through 1.0.0 does not enforce a nonce or capability check on some of its AJAX actions, allowing unauthenticated users to update and delete arbitrary WordPress options, which can be used to gain administrator access to the site.

### CVE-2026-84737

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-11T07:17:25.797 |

The Freeton WP WordPress plugin through 1.0.0 does not correctly validate the activation code when authenticating a user, allowing unauthenticated attackers to log in as any user whose email address they know, including administrators.

### CVE-2026-84734

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-11T07:17:25.687 |

The Mindstien Quick Login WordPress plugin through 1.0 does not correctly validate a value supplied in the request against the visitor's own session before authenticating them, allowing unauthenticated attackers to obtain a session as the administrator account the Mindstien Quick Login WordPress plugin through 1.0 is configured with.

### CVE-2026-84254

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T07:17:25.180 |

The click5 CRM add-on to Contact Form 7 WordPress plugin through 1.0.4 does not have authorisation and CSRF checks when updating options via a REST endpoint, and does not ensure that the option to be updated belongs to the click5 CRM add-on to Contact Form 7 WordPress plugin through 1.0.4. As a result, unauthenticated attackers could change arbitrary blog options, allowing them to create a new administrator account and take over the site.

### CVE-2026-84253

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T07:17:25.057 |

The click5 CRM add-on to Gravity Forms WordPress plugin through 1.0.3 does not have authorisation and CSRF checks when updating options via a REST endpoint, and does not ensure that the option to be updated belongs to the click5 CRM add-on to Gravity Forms WordPress plugin through 1.0.3. As a result, unauthenticated attackers could change arbitrary blog options, allowing them to create a new administrator account and take over the site.

### CVE-2026-84252

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T07:17:24.943 |

The click5 CRM add-on to WPForms WordPress plugin through 1.0.3 does not have authorisation and CSRF checks when updating options via a REST endpoint, and does not ensure that the option to be updated belongs to the click5 CRM add-on to WPForms WordPress plugin through 1.0.3. As a result, unauthenticated attackers could change arbitrary blog options, allowing them to create a new administrator account and take over the site.

### CVE-2026-84251

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T07:17:24.820 |

The click5 CRM add-on to Ninja Forms WordPress plugin through 1.0.1 does not have authorisation and CSRF checks when updating options via a REST endpoint, and does not ensure that the option to be updated belongs to the click5 CRM add-on to Ninja Forms WordPress plugin through 1.0.1. As a result, unauthenticated attackers could change arbitrary blog options, allowing them to create a new administrator account and take over the site.

### CVE-2026-104028

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-11T07:17:22.440 |

The Anton Extensions WordPress plugin through 1.2.2 does not perform any capability check, nonce verification, or file-type validation before writing attacker-supplied content to an attacker-chosen path, allowing unauthenticated attackers to upload arbitrary PHP files and achieve remote code execution.

### CVE-2026-81797

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:47.507 |

Unauthenticated PHP Object Injection in Buzz Stone | Magazine & Viral Blog WordPress Theme <= 1.0.2 versions.

### CVE-2026-78535

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:47.380 |

Unauthenticated PHP Object Injection in Photolia <= 1.0.3 versions.

### CVE-2026-78533

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:47.133 |

Unauthenticated PHP Object Injection in Qwery <= 3.6.1 versions.

### CVE-2026-78531

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:46.830 |

Unauthenticated PHP Object Injection in Jacqueline <= 2.22 versions.

### CVE-2026-78529

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:46.590 |

Unauthenticated PHP Object Injection in Alliance <= 3.11 versions.

### CVE-2026-66569

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:46.467 |

Unauthenticated PHP Object Injection in Kicker <= 2.2.1 versions.

### CVE-2026-66568

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:46.347 |

Unauthenticated PHP Object Injection in Original <= 1.9.0 versions.

### CVE-2026-66567

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:46.223 |

Unauthenticated PHP Object Injection in Anesta <= 1.5.3 versions.

### CVE-2026-66565

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:45.980 |

Unauthenticated PHP Object Injection in FC United <= 1.1.1 versions.

### CVE-2026-66564

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:45.857 |

Unauthenticated PHP Object Injection in ShiftCV <= 3.0.14 versions.

### CVE-2026-66563

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:45.737 |

Unauthenticated PHP Object Injection in Windsor <= 2.10 versions.

### CVE-2026-66483

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:45.613 |

Unauthenticated PHP Object Injection in Education Center <= 3.6.12 versions.

### CVE-2026-66482

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:45.493 |

Unauthenticated PHP Object Injection in Drone Media <= 2.2.0 versions.

### CVE-2026-62125

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:44.660 |

Unauthenticated PHP Object Injection in Asia Garden <= 1.3.1 versions.

### CVE-2026-62124

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:44.540 |

Unauthenticated PHP Object Injection in N7 | Golf Club Sports & Events <= 2.21 versions.

### CVE-2026-62123

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:44.420 |

Unauthenticated PHP Object Injection in Invetex <= 2.18 versions.

### CVE-2026-62120

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:44.300 |

Unauthenticated PHP Object Injection in Law Office <= 3.20 versions.

### CVE-2026-62090

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:42.617 |

Unauthenticated PHP Object Injection in WineShop <= 3.20 versions.

### CVE-2026-62087

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:42.497 |

Unauthenticated PHP Object Injection in Equadio <= 1.1.4 versions.

### CVE-2026-62086

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:42.377 |

Unauthenticated PHP Object Injection in Juno <= 2.25 versions.

### CVE-2026-62077

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:42.143 |

Unauthenticated PHP Object Injection in Avala <= 1.1.4 versions.

### CVE-2026-62076

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:42.023 |

Unauthenticated PHP Object Injection in Kalles <= 1.1.7.1 versions.

### CVE-2026-62054

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:40.760 |

Unauthenticated PHP Object Injection in Yacht Rental <= 2.6 versions.

### CVE-2026-62053

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:40.633 |

Unauthenticated PHP Object Injection in Wine House <= 3.20 versions.

### CVE-2026-62052

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:40.510 |

Unauthenticated PHP Object Injection in Tipsy <= 1.6 versions.

### CVE-2026-62051

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:40.387 |

Unauthenticated PHP Object Injection in Stargaze <= 1.10 versions.

### CVE-2026-62050

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:40.260 |

Unauthenticated PHP Object Injection in Splendour <= 1.23 versions.

### CVE-2026-62032

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:39.357 |

Unauthenticated Local File Inclusion in DirectoryPress <= 3.6.27 versions.

### CVE-2026-62022

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-10T20:16:38.630 |

Unauthenticated Privilege Escalation in Tonda Membership <= 1.0.1 versions.

### CVE-2026-42723

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:37.270 |

Unauthenticated PHP Object Injection in CleanSkin <= 1.5.0 versions.

### CVE-2026-42719

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:37.030 |

Subscriber PHP Object Injection in Dynamic User Directory <= 2.4 versions.

### CVE-2026-42718

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:36.907 |

Unauthenticated PHP Object Injection in Booster for WooCommerce <= 8.4.0 versions.

### CVE-2026-42716

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:36.630 |

Unauthenticated PHP Object Injection in Payever - WooCommerce Gateway <= 4.8.2 versions.

### CVE-2026-39801

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-10T20:16:33.483 |

Subscriber Privilege Escalation in AIWU <= 1.5.9 versions.

### CVE-2026-106610

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-10T19:16:57.187 |

Incorrect Privilege Assignment vulnerability in miniOrange miniorange otp verification miniorange-otp-verification allows Privilege Escalation.This issue affects miniorange otp verification: from n/a through 5.5.7.

### CVE-2026-105892

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-10T19:16:56.990 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in rtCamp Inc. rtMedia for WordPress, BuddyPress and bbPress buddypress-media allows Path Traversal.This issue affects rtMedia for WordPress, BuddyPress and bbPress: from n/a through 4.7.13.

### CVE-2026-104398

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T17:16:59.937 |

Deserialization of Untrusted Data vulnerability in VillaTheme AFFI – Affiliate Marketing for WooCommerce affi-affiliate-marketing-for-woo allows Object Injection.This issue affects AFFI – Affiliate Marketing for WooCommerce: from n/a through 1.0.10.

### CVE-2026-108860

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-11T14:17:05.933 |

BotSharp through 5.2.0 contains an authentication bypass vulnerability that allows unauthenticated remote attackers to forge bearer tokens using the hard-coded Jwt:Key in WebStarter appsettings.json. Attackers can sign tokens with the committed HMAC secret and fixed botsharp issuer and audience to impersonate any known user, including administrators, on Authorize-protected API routes.

### CVE-2026-108753

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-11T13:17:20.237 |

Agnaistic agnai through 1.0.555 contains a hard-coded credentials vulnerability in self-host.docker-compose.yml, which sets a fixed admin password and public JWT secret. Unauthenticated attackers can log in as admin or sign their own JWT with admin: true to impersonate users, reset passwords, and change server configuration.

### CVE-2026-108707

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-11T02:16:39.477 |

Wukong_HRM through commit 186115e contains an authentication bypass vulnerability in ParamAspect that allows unauthenticated attackers to call every HRM API endpoint by omitting the AUTH-TOKEN header. Attackers gain HR administrator access to read payslips, salary history and employee personal data, download attachments, and modify or delete company-wide HR records.

### CVE-2026-62031

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T20:16:39.237 |

Unauthenticated SQL Injection in uListing <= 2.2.0 versions.

### CVE-2026-40800

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T20:16:33.863 |

Subscriber SQL Injection in ELEX WooCommerce Advanced Bulk Edit Products, Prices & Attributes <= 1.5.3 versions.

### CVE-2026-108598

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-10T19:16:58.347 |

Floci 1.1.0 before 2.2.0 contains a code injection vulnerability in VtlTemplateEngine that allows unauthenticated attackers to execute commands via unrestricted Velocity mapping templates. Attackers can create a REST API with a MOCK integration whose template uses $util reflection to reach Runtime or ProcessBuilder, executing OS commands in the Floci JVM.

### CVE-2026-105889

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T17:17:00.063 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Tickera Tickera tickera-event-ticketing-system allows Blind SQL Injection.This issue affects Tickera: from n/a through 3.6.0.6.

### CVE-2026-108551

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-10T15:16:58.273 |

openapi-typescript-codegen through 0.31.0 contains a code injection vulnerability that allows attackers controlling an OpenAPI document to inject JavaScript by supplying unescaped values interpolated into single-quoted string literals. Attackers can embed a single quote in path keys, parameter names, servers[0].url, or info.version to execute arbitrary JavaScript when generated clients are imported or service methods called.

### CVE-2026-108549

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-10T15:16:57.973 |

cc-connect through 1.5.0 contains a missing authentication vulnerability in the MAX platform adapter webhook mode in platform/max/max.go that accepts unauthenticated updates when no webhook_secret is configured. Remote attackers reaching the webhook listener on port 8080 can forge updates with an allowed or admin user_id to run privileged commands like /shell on the host.

### CVE-2026-86717

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T07:17:26.337 |

The Insurify  WordPress plugin through 1.0 does not have authorisation and nonce checks on one of its AJAX actions, allowing unauthenticated users to delete arbitrary WordPress options, which can take the site offline and strip every user of their role.

### CVE-2026-86706

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T07:17:26.220 |

The Quick quotes  WordPress plugin through 1.0.0 does not perform any capability or nonce check on one of its AJAX actions and lets the caller choose which option is written, allowing unauthenticated users to alter arbitrary site settings and to make the site unavailable.

### CVE-2026-85121

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T07:17:26.007 |

The Insurify  WordPress plugin through 1.0 does not have authorisation and nonce checks on one of its AJAX actions, allowing unauthenticated users to create and overwrite arbitrary WordPress options with request data, which can take the site offline and deactivate all of its Insurify  WordPress plugin through 1.0.

### CVE-2026-81649

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-11T07:17:24.703 |

The Fundiin cho WooCommerce WordPress plugin through 3.4.0 does not have proper authorisation on several of its REST API routes, relying instead on a credential that is identical on every installation, allowing unauthenticated attackers to disclose the store's payment credentials and customer order data, overwrite the payment gateway configuration so that payments are credited elsewhere, and mark unpaid orders as paid. The same missing authorisation also allows arbitrary script to be stored in a field which is output unescaped on the classic checkout, leading to unauthenticated stored XSS on stores that do not use the block-based checkout.

### CVE-2026-62025

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-10T20:16:38.870 |

Unauthenticated Arbitrary File Upload in Tailored Tools <= 3.0.3 versions.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-108865

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-11T14:17:06.640 |

AmoyLab Unla through 0.10.0 contains an authentication bypass vulnerability that allows unauthenticated attackers to obtain valid access tokens because the OAuth2 server never authenticates a resource owner. Attackers can register a client, request a code from /authorize, and exchange it at /token to access OAuth2-protected MCP prefixes, proxied upstream APIs and injected credentials.

### CVE-2026-108758

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-11T13:17:21.020 |

Easy!Appointments through 1.6.0 contains an authorization bypass vulnerability in Booking::register() that allows unauthenticated attackers to modify any appointment by supplying an appointment id without its hash. Attackers can enumerate sequential appointment ids with a self-asserted manage_mode flag to rewrite appointment details, rebind them to attacker-controlled customers, and obtain management hashes for rescheduling or cancellation.

### CVE-2026-96227

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:29.543 |

The Piotnet Forms WordPress plugin through 1.0.30 does not authenticate or validate a form-submission file-upload request and permits browser-renderable file types to be stored, allowing unauthenticated attackers to store a file that executes arbitrary JavaScript in the site's origin when it is opened (Stored XSS).

### CVE-2026-88905

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:27.493 |

The KeyWord Collector WordPress plugin through 1.4 does not have any authorisation or nonce check when saving its settings, and does not escape them before output, allowing unauthenticated attackers to store malicious JavaScript that executes when an administrator opens the KeyWord Collector WordPress plugin through 1.4's settings page or when a visitor loads a page displaying its output.

### CVE-2026-88903

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:27.377 |

The Topcontent WordPress plugin through 1.2.1 does not properly authorise one of its request handlers and disables HTML sanitisation before storing the submitted content, allowing unauthenticated attackers to publish arbitrary posts containing malicious JavaScript on any site where its API key has never been configured.

### CVE-2026-88827

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-11T07:17:27.267 |

The Disable Users WordPress plugin through 1.0.5 does not enforce its account-disabling control on all authentication paths, allowing the holder of an account an administrator has disabled to continue authenticating with the account's full privileges.

### CVE-2026-88826

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:27.153 |

The SmugMug Embed WordPress plugin through 3.13 does not have authorisation or CSRF checks on an AJAX action that stores gallery data, and does not sanitise or escape that data before outputting it, allowing unauthenticated users to store arbitrary web scripts that execute when an administrator views the SmugMug Embed WordPress plugin through 3.13's settings screen.

### CVE-2026-87764

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:26.913 |

The BuddyPress Instant Chat WordPress plugin through 1.6 does not check that the sender of a chat message belongs to the conversation it is being added to, nor does it escape message content before outputting it back, allowing unauthenticated users to store arbitrary web scripts that will execute in the session of any member who later views that conversation.

### CVE-2026-87762

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:26.803 |

The Adwised Web Push Notification WordPress plugin through 2.5.7 does not have authorisation checks on several state-changing operations, and the secret comparison it uses instead can be bypassed on installations where the secret key has never been set, allowing unauthenticated users to store arbitrary JavaScript that is executed in the browser of every site visitor.

### CVE-2026-87760

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:26.573 |

The Web Vitals Tracking WordPress plugin through 5.4.2 does not validate or escape performance measurements submitted by unauthenticated visitors before storing them and outputting them in a script context on an administrative page, allowing unauthenticated attackers to perform Stored Cross-Site Scripting attacks against administrators.

### CVE-2026-86798

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:26.450 |

The HootBoard  WordPress plugin through 3.1.4 does not perform any authorisation check on some of its REST endpoints, and does not escape the values stored through them before outputting them in a public page, allowing unauthenticated users to inject arbitrary web scripts that will execute in the browser of anyone visiting that page, including administrators.

### CVE-2026-84261

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:25.590 |

The click5 CRM add-on to Contact Form 7 WordPress plugin through 1.0.4 does not sanitise and escape content submitted through an unauthenticated endpoint before outputting it back in an admin page, leading to Stored XSS which could be used against high privilege users such as admin.

### CVE-2026-84260

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:25.483 |

The click5 CRM add-on to Gravity Forms WordPress plugin through 1.0.3 does not sanitise and escape content submitted through an unauthenticated endpoint before outputting it back in an admin page, leading to Stored XSS which could be used against high privilege users such as admin.

### CVE-2026-84259

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:25.390 |

The click5 CRM add-on to WPForms WordPress plugin through 1.0.3 does not sanitise and escape content submitted through an unauthenticated endpoint before outputting it back in an admin page, leading to Stored XSS which could be used against high privilege users such as admin.

### CVE-2026-84258

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:25.287 |

The click5 CRM add-on to Ninja Forms WordPress plugin through 1.0.1 does not sanitise and escape content submitted through an unauthenticated endpoint before outputting it back in an admin page, leading to Stored XSS which could be used against high privilege users such as admin.

### CVE-2026-103694

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-11T07:17:22.230 |

The Mobile builder WordPress plugin through 1.4.2 does not properly restrict which user meta keys a logged-in user can update through one of its REST routes, allowing any user with a self-registered account, such as a customer, to grant themselves the administrator role.

### CVE-2026-103305

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:21.007 |

The Prenotazioni WordPress plugin through 1.7.5 does not have authorisation and CSRF checks when saving its settings, and does not escape some of them when outputting them, allowing unauthenticated users to perform Stored Cross-Site Scripting attacks against administrators and site visitors.

### CVE-2026-62021

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:38.503 |

Subscriber PHP Object Injection in Angio <= 1.1.1 versions.

### CVE-2026-108863

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-11T14:17:06.360 |

Katanemo Plano through 0.4.37 contains a missing authentication vulnerability that allows unauthenticated network attackers to access the Envoy admin interface, which is bound to all host interfaces on port 9901. Attackers can request the /config_dump endpoint to read configured LLM provider API keys in plaintext from the WASM filter configuration.

### CVE-2026-108859

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-11T14:17:05.780 |

mcp-go through 1.2.1 contains a denial of service vulnerability in StreamableHTTPServer.ServeHTTP that allows remote unauthenticated attackers to exhaust memory by sending oversized POST bodies. Attackers can send arbitrarily large or many concurrent POST requests, read fully via io.ReadAll before validation, to degrade or OOM-kill the server process.

### CVE-2026-108746

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-11T13:17:19.230 |

Vearch 3.5.2 through 3.5.9 contains an incorrect authorization vulnerability in Role.HasPermissionForResources that ignores stored ReadOnly or None privilege levels for resources listed in a role. Authenticated non-root users can upsert and delete documents with read-only access, or call PUT /roles to grant their role WriteRead privileges, escalating toward cluster administrator access.

### CVE-2026-108739

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-11T13:17:18.383 |

OpenAgents Workspace backend through launcher-v1.0.17 contains an information disclosure vulnerability that allows unauthenticated attackers to list all workspaces via GET /v1/workspaces. Attackers can read the unmasked browserfabric_api_key in each workspace's settings map, along with workspace ids, slugs, creator emails and member lists.

### CVE-2026-108714

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-11T13:17:14.430 |

MCP Kotlin SDK through 0.15.0 contains an uncontrolled memory allocation vulnerability that allows remote clients to exhaust server memory because Application.mcpWebSocket installs Ktor WebSockets without a maxFrameSize limit. Attackers can send small frame headers declaring payloads near 2 GiB over one or a few connections, forcing huge heap allocations and causing denial of service.

### CVE-2026-108708

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T02:16:39.650 |

Wukong_HRM through commit 186115e contains a missing authorization vulnerability because EmployeeAspect assigns every caller the HR administrator role and EmployeeUtil data-scope checks return all employees. Any authenticated low-privileged employee can read payslips, salary records, bank cards and personal data, edit bank cards, and delete employees, departments and contracts company-wide.

### CVE-2026-108550

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-10T15:16:58.133 |

SkillHub before 0.2.22 contains an incorrect authorization vulnerability in AccountMergeService and AccountMergeController that allows authenticated attackers to take over other accounts by abusing the merge flow. Attackers can call the merge initiate endpoint with a target username or OAuth identity, receive the verification token directly, and confirm the merge to inherit the victim's API tokens, roles and namespace ownership.

### CVE-2026-108718

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T13:17:15.020 |

Rill 0.77.0 through 0.90.5 contains a missing authorization vulnerability in the admin OAuth server that issues authorization codes to dynamically registered clients without user consent. Attackers can register a client with the long_lived_access_token scope and lure a user to an authorization link, obtaining a non-expiring API token with the user's full permissions.

### CVE-2026-89302

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:28.873 |

The Post Voting System WordPress plugin through 1.0 does not properly sanitize and escape a parameter before using it in a SQL query, allowing unauthenticated users to perform SQL injection attacks.

### CVE-2026-89299

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:28.770 |

The WP Verify API WordPress plugin through 1.0.0 does not properly sanitize and escape a parameter before using it in a SQL query, allowing unauthenticated users to perform SQL injection attacks.

### CVE-2026-89297

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:28.670 |

The Loja Automática WordPress plugin through 1.0.0 does not properly sanitize and escape a parameter before using it in a SQL query, allowing unauthenticated users to perform SQL injection attacks.

### CVE-2026-89287

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:28.560 |

The ASPL Product Quotation WordPress plugin through 1.1.0 does not sanitize and escape a parameter before using it in SQL statements, allowing unauthenticated attackers to perform SQL injection and read arbitrary data from the database.

### CVE-2026-89285

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:28.440 |

The Datalist it WordPress plugin through 0.0.3 does not sanitize and escape several request parameters before using them to build a SQL query, allowing unauthenticated attackers to perform SQL injection and read arbitrary data from the database.

### CVE-2026-89283

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T07:17:28.330 |

The WP Posts Password Batch Manager WordPress plugin through 1.1 does not perform any capability or nonce check on a bulk post-password action that runs on an always-loaded admin handler, allowing unauthenticated attackers to reset or overwrite the password of every published post, disclosing password-protected content or locking all posts behind an attacker-chosen password.

### CVE-2026-89234

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:28.217 |

The WP-Partner WordPress plugin through 1.2.1 does not sanitise and escape a parameter before using it in a SQL query, allowing unauthenticated attackers to append additional SQL queries and extract sensitive information from the database.

### CVE-2026-89232

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:28.070 |

The Recordbrowser WordPress plugin through 1.1.7 does not sanitise and escape a parameter before using it in a SQL query, allowing unauthenticated attackers to append additional SQL queries and extract sensitive information from the database.

### CVE-2026-89214

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:27.957 |

The WpCues Basic Quiz WordPress plugin through 1.6.5 does not properly sanitise and escape values before using them in a SQL statement, which allows unauthenticated attackers to perform SQL injection attacks and read data from the database.

### CVE-2026-89213

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:27.840 |

The Llavero.io WordPress plugin through 0.1.4 does not properly sanitise and escape a parameter before using it in a SQL statement, which allows unauthenticated attackers to perform SQL injection attacks and read data from the database.

### CVE-2026-89195

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:27.720 |

The Site Setup Wizard WordPress plugin through 1.5.8 does not properly sanitise and escape a parameter before using it in a SQL statement, which allows unauthenticated attackers to perform SQL injection attacks and read data from the database.

### CVE-2026-88930

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:27.603 |

The Social Web Suite  WordPress plugin through 4.1.12 does not require its shared secret to be set before accepting requests authorised by it, and does not sanitise and escape a parameter before using it in an SQL statement, allowing unauthenticated users to perform SQL injection attacks.

### CVE-2026-81420

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:24.593 |

The Tcard WP WordPress plugin through 1.8.0 does not sanitise and escape a parameter before using it in a SQL statement in one of its unauthenticated AJAX actions, allowing unauthenticated users to perform SQL injection attacks.

### CVE-2026-108540

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-11T07:17:23.303 |

A flaw has been found in OpenSpug Spug up to 3.4.0/4.0.1. This impacts an unknown function of the file /exec/transfer of the component File Transfer. Executing a manipulation can lead to os command injection. The attack may be launched remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-103695

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-11T07:17:22.340 |

The Mobile builder WordPress plugin through 1.4.2 does not sanitise and escape a parameter before using it in a SQL statement, allowing unauthenticated users to perform SQL injection attacks.

### CVE-2026-108657

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T22:16:41.923 |

JeecgBoot through 3.9.5 contains a missing authorization vulnerability in the SysTenantController passApply handler that allows any authenticated user to approve tenant administrator applications. Attackers can file a pending application via doApplyTenantPackUser and approve it through PUT /sys/tenant/passApply to gain tenant administrator pack permissions in any tenant.

### CVE-2026-108628

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T22:16:37.590 |

JeecgBoot through 3.9.5 contains a missing authorization vulnerability in the saveDeptRolePermission endpoint of SysDepartPermissionController that allows any authenticated user to modify department role permissions. Low-privileged attackers can submit roleId and permissionIds values to grant arbitrary menu or button permissions, escalating privileges or revoking other users' permissions.

### CVE-2026-62117

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T20:16:44.060 |

Subscriber SQL Injection in Barcode Scanner with Inventory & Order Manager <= 1.13.1 versions.

### CVE-2026-42712

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T20:16:36.397 |

Subscriber SQL Injection in Qode Tours <= 3.1.3.2 versions.

### CVE-2026-42633

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T20:16:35.080 |

Subscriber SQL Injection in Events Manager <= 7.4.6 versions.

### CVE-2026-108699

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-11T14:17:04.257 |

hyper-mcp through 0.8.3 contains an improper signature verification vulnerability that allows attackers to load malicious WebAssembly plugins because cosign_verify_args() accepts any signer identity and OIDC issuer by default. Attackers controlling a plugin image reference can sign a malicious image with a free Sigstore keyless certificate to execute plugins with configured host, filesystem, and environment capabilities.

### CVE-2026-108698

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-11T14:17:04.113 |

hyper-mcp through 0.8.3 contains a signature verification bypass vulnerability in load_wasm in src/wasm/oci.rs that verifies the Cosign signature of a separately resolved tag rather than the loaded manifest. Attackers controlling registry responses for the tag can serve an unsigned malicious manifest to the loader and a signed one to Cosign, executing unsigned WebAssembly plugins with configured host capabilities.

### CVE-2026-108729

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-11T13:17:16.750 |

Corteza through 2024.9.10 contains an incorrect authorization vulnerability in compose attachment endpoints that allows unauthenticated attackers to download private attachments by setting the URL kind segment to page, icon, or namespace. Attackers who know a private record or module attachment id can request the original or preview route without a token or signature to retrieve files across namespace and record permission boundaries.

### CVE-2026-96341

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-10T19:16:59.037 |

Incorrect Privilege Assignment vulnerability in WPMU DEV Forminator forminator allows Privilege Escalation.This issue affects Forminator: from n/a through 1.57.3.

### CVE-2026-108545

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-10T15:16:57.413 |

SillyTavern 1.12.13 through 1.19.0 contains a denial of service vulnerability that allows unauthenticated remote attackers to exhaust resources because body-parser middleware runs before authentication and whitelist checks. Attackers can send large or compressed JSON or urlencoded bodies up to 500 MB, optionally in parallel, to exhaust memory and CPU and deny service.

### CVE-2026-66566

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:46.103 |

Unauthenticated Local File Inclusion in Ambient <= 1.7 versions.

### CVE-2026-62115

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:43.813 |

Unauthenticated Local File Inclusion in KuteShop <= 4.2.9 versions.

### CVE-2026-62099

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:43.580 |

Unauthenticated Local File Inclusion in Boutique <= 2.3.3 versions.

### CVE-2026-62096

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:43.333 |

Unauthenticated Local File Inclusion in Biolife <= 3.2.3 versions.

### CVE-2026-62094

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:43.090 |

Unauthenticated Local File Inclusion in TechOne <= 3.0.3 versions.

### CVE-2026-62092

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:42.853 |

Unauthenticated Local File Inclusion in Armania <= 1.4.8 versions.

### CVE-2026-62075

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:41.880 |

Unauthenticated Local File Inclusion in Backhoe <= 2.0 versions.

### CVE-2026-62074

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:41.737 |

Unauthenticated Local File Inclusion in Ozeum <= 1.3.0 versions.

### CVE-2026-62070

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:41.613 |

Unauthenticated Local File Inclusion in Flipmart <= 2.8 versions.

### CVE-2026-62069

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:41.490 |

Unauthenticated Local File Inclusion in Fabius <= 1.0 versions.

### CVE-2026-62068

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:41.373 |

Unauthenticated Local File Inclusion in Teoro <= 1.1 versions.

### CVE-2026-62067

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:41.250 |

Unauthenticated Local File Inclusion in Kaven <= 1.2 versions.

### CVE-2026-62066

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:41.130 |

Unauthenticated Local File Inclusion in Volos <= 1.2 versions.

### CVE-2026-62065

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:41.010 |

Unauthenticated Local File Inclusion in Cardea <= 2.3 versions.

### CVE-2026-62020

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:38.380 |

Unauthenticated Local File Inclusion in TouchUp < 1.4 versions.

### CVE-2026-48194

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:38.030 |

Unauthenticated Local File Inclusion in DukaMarket <= 1.3.0 versions.

### CVE-2026-48193

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:37.903 |

Unauthenticated Local File Inclusion in Uminex <= 1.0.9 versions.

### CVE-2026-42777

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:37.533 |

Unauthenticated Local File Inclusion in Aalto <= 1.8 versions.

### CVE-2026-42724

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:37.390 |

Unauthenticated Local File Inclusion in CleanSkin <= 1.5.0 versions.

### CVE-2026-42704

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T20:16:35.797 |

Unauthenticated Local File Inclusion in Kids Care <= 3.2.4 versions.

### CVE-2026-40801

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T20:16:33.990 |

Subscriber Broken Access Control in Wordable <= 8.2.10 versions.

### CVE-2026-40777

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T20:16:33.737 |

Subscriber Broken Access Control in WPSection <= 1.5.1 versions.

### CVE-2026-39802

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-10T20:16:33.613 |

Unauthenticated Remote Code Execution (RCE) in Everest Backup <= 2.3.13 versions.

### CVE-2026-87761

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:26.690 |

The Adwised Web Push Notification WordPress plugin through 2.5.7 does not perform any capability or nonce check before allowing an authenticated user to overwrite its site-wide configuration, and does not escape those configuration values before printing them inside an inline script block on every front-end page, allowing any authenticated user, such as a subscriber, to perform Stored Cross-Site Scripting attacks against every visitor, including administrators.

### CVE-2026-78530

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-10T20:16:46.710 |

Subscriber Arbitrary File Deletion in FoodBakery <= 4.6 versions.

### CVE-2026-40805

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-10T20:16:34.353 |

Subscriber Arbitrary File Deletion in PeepSo <= 9.0.5.4 versions.

### CVE-2026-108553

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-10T15:16:58.410 |

OpenRefine through 3.10.1 contains a cross-site request forgery vulnerability in the get-rows command that allows remote attackers to execute Jython facet expressions. Attackers can lure a user to a malicious page issuing a cross-origin GET with a crafted engine parameter, executing operating system commands as the OpenRefine user.

### CVE-2026-108546

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-10T15:16:57.573 |

Spotweb through 1.5.8 contains an OS command injection vulnerability in the runcommand NZB handler that allows remote attackers to execute commands by publishing spots with malicious titles. Attackers can post self-signed spots over Usenet with shell metacharacters in the title, which are substituted unescaped for $SPOTTITLE and passed to exec() when a user downloads the spot, running commands as the Spotweb PHP process.

### CVE-2026-108759

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-11T13:17:21.167 |

mistral.rs 0.9.0 through 0.9.4 contains a link following vulnerability in mistralrs-code-exec that allows sandboxed shell code to read and overwrite files outside the sandbox via symlinks. Attackers or prompt-injected agents can name symlinks as outputs or reuse sessions with symlinked input paths to access files with the server process's permissions.

### CVE-2026-108737

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-11T13:17:18.053 |

Traccar through 6.16.0 contains a weak password recovery vulnerability that allows attackers to reuse password reset tokens as session credentials because TokenManager does not bind tokens to a purpose. Attackers holding a leaked reset link can obtain a full session via /api/session or change passwords via /api/password/update, retaining access for seven days even after the victim resets their password.

### CVE-2026-62033

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T20:16:39.480 |

Subscriber Settings Change in uListing <= 2.2.0 versions.

### CVE-2026-45440

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T20:16:37.740 |

Administrator SQL Injection in WP Ultimate CSV Importer <= 9.2 versions.

### CVE-2026-42722

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T20:16:37.150 |

Administrator SQL Injection in Frontend Admin by DynamiApps <= 3.29.13 versions.

### CVE-2026-42717

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T20:16:36.780 |

Administrator SQL Injection in Leyka <= 3.32.3 versions.

### CVE-2026-40802

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T20:16:34.110 |

Subscriber Settings Change in Pubjet | پاب‌جت <= 5.4.8 versions.

### CVE-2026-14854

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-11T07:17:24.003 |

The WooCommerce Bookings WordPress plugin before 3.11.0 does not limit a user-supplied value before using it to allocate memory in one of its unauthenticated AJAX actions, allowing unauthenticated attackers to exhaust server memory and cause a Denial of Service with a single request.

### CVE-2026-106029

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T07:17:22.963 |

The WeddingCity Lite  WordPress plugin through 1.0.4 does not perform any authorisation or validity checks before deleting posts, pages and media attachments, allowing unauthenticated attackers to permanently delete arbitrary content site-wide.

### CVE-2026-65459

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T20:16:45.117 |

Unauthenticated Arbitrary Content Deletion in Forminator <= 1.57.3 versions.

### CVE-2026-62043

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-10T20:16:40.137 |

Unauthenticated Sensitive Data Exposure in Contact Form 7 – Dynamic Text Extension <= 5.0.7 versions.

### CVE-2026-42706

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T20:16:36.040 |

Unauthenticated Broken Access Control in DK <= 3.2.1 versions.

### CVE-2026-42705

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T20:16:35.917 |

Unauthenticated Broken Access Control in Grand News <= 3.4 versions.

### CVE-2026-42630

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-10T20:16:34.717 |

Unauthenticated Sensitive Data Exposure in Web Plura Backup &amp; Restore Manager <= 0.2.25 versions.

### CVE-2026-106609

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T17:17:00.310 |

Missing Authorization vulnerability in Web Impian Bayarcash WooCommerce bayarcash-wc allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Bayarcash WooCommerce: from n/a through 4.4.2.

### CVE-2026-103071

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-10T17:16:59.673 |

Improper Control of Generation of Code ('Code Injection') vulnerability in VillaTheme Thank You Page Customizer for WooCommerce woo-thank-you-page-customizer allows Code Injection.This issue affects Thank You Page Customizer for WooCommerce: from n/a through 1.2.3.

### CVE-2026-108744

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-11T13:17:18.957 |

pbi-cli 3.10.1 through 3.12.0 contains an OS command injection vulnerability in desktop_sync.py that passes unquoted .pbip paths to cmd /c start when reopening projects. Attackers can lure victims into opening a Power BI project from a space-free path containing & to run commands with victim privileges during report write or reload.

### CVE-2026-108693

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-11T02:16:37.607 |

ImageMagick on Windows through 7.1.2-33 and 6.9.13-58 contains an uncontrolled search path vulnerability in NTGhostscriptEXE() that launches gswin64c.exe by bare name when Ghostscript is unregistered. Attackers can plant a malicious gswin64c.exe in the working directory to execute code with ImageMagick privileges when PDF, PostScript, or EPS files are converted.

### CVE-2026-62118

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T20:16:44.180 |

Unauthenticated Broken Access Control in Barcode Scanner with Inventory & Order Manager <= 1.13.1 versions.

### CVE-2026-62038

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-10T20:16:40.010 |

Unauthenticated Broken Authentication in eRoom <= 1.7.1 versions.

### CVE-2026-108593

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-10T19:16:57.607 |

9router 0.4.1 through 0.5.99 contains a configuration injection vulnerability in the POST /api/cli-tools/hermes-settings endpoint that allows authenticated dashboard users to inject arbitrary keys into the Hermes Agent config.yaml file. Attackers can submit a baseUrl containing double quotes and newlines to add hooks_auto_accept and a hooks.post_llm_call shell command, which Hermes Agent executes without approval after an LLM call.

### CVE-2026-108853

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-11T14:17:04.960 |

UnicomAI Wanwu before 0.6.3 contains an insecure direct object reference vulnerability that allows authenticated low-privileged users to delete other tenants' agent or RAG applications by supplying their appId. Attackers can send requests to DELETE /v1/appspace/app with guessed sequential assistant IDs to permanently delete victims' applications, workflows, conversations, and associated data.

### CVE-2026-108760

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1327` |
| Published | 2026-10-11T13:17:21.310 |

LlamaFarm through 0.0.34 contains an insecure default configuration that binds its unauthenticated FastAPI server to 0.0.0.0 on port 14345, while the lf CLI silently discards HOST overrides. Network-adjacent attackers can call the project and dataset management API to read stored provider API keys, modify projects, trigger ingestion, and irreversibly delete projects.

### CVE-2026-108740

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-10-11T13:17:18.527 |

GoatCounter through 2.7.0 contains a mass assignment privilege escalation vulnerability in the userPrefSave handler that allows logged-in users to modify protected account fields via form-encoded requests. Attackers with read-only access can POST user.access[all]=* and user.email_verified=true to /user/pref, bypassing readonly tags to gain superuser or admin access.

### CVE-2026-85126

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-11T07:17:26.113 |

The Crowdfundly WordPress plugin through 2.2.2 does not have capability checks on some of its AJAX actions, allowing users holding one of its own low privileged roles to grant themselves the administrator role or arbitrary capabilities, leading to a full site takeover.

### CVE-2026-104680

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-11T07:17:22.550 |

The Envira Gallery  WordPress plugin before 1.16.2 does not verify that a user holds the capability WordPress reserves for installing Envira Gallery  WordPress plugin before 1.16.2 code before processing its setup-wizard Envira Gallery  WordPress plugin before 1.16.2-installation request, and does not restrict the installation to its own curated list, allowing a Multisite subsite Administrator to install an arbitrary WordPress.org-published Envira Gallery  WordPress plugin before 1.16.2 into the network-shared Envira Gallery  WordPress plugin before 1.16.2 directory, a privilege Multisite reserves for the network Super Admin.

### CVE-2026-62130

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T20:16:44.913 |

Shop manager PHP Object Injection in WooCommerce Multilingual & Multicurrency <= 5.5.8 versions.

### CVE-2026-62030

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-10T20:16:39.110 |

Unauthenticated Server Side Request Forgery (SSRF) in StreamCast <= 2.4.5 versions.

### CVE-2026-27350

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-10T20:16:33.100 |

Server-Side Request Forgery (SSRF) vulnerability in Builderius.io Builderius allows Server Side Request Forgery.

This issue affects Builderius: from 1.4 through 1.4-beta.

### CVE-2026-62044

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T17:17:00.803 |

Deserialization of Untrusted Data vulnerability in bPlugins Super Video Player super-video-player allows Object Injection.This issue affects Super Video Player: from n/a through 1.8.13.

### CVE-2026-106608

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-10T17:17:00.190 |

Incorrect Privilege Assignment vulnerability in Automattic WooCommerce woocommerce allows Privilege Escalation.This issue affects WooCommerce: from 9.8.0 through 11.1.2.

### CVE-2026-108757

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-11T13:17:20.840 |

Nexting pinclaw OpenClaw channel plugin through 0.3.0 contains a missing authentication vulnerability in src/core/http-router.ts that skips the authToken check on POST /pinclaw/send. Unauthenticated attackers reaching port 18790, which binds all interfaces by default, can inject blind prompts into the user's main OpenClaw agent session as user instructions.

### CVE-2026-108728

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-10-11T13:17:16.590 |

Flyte 2.0.1 through 2.0.51 contains a cleartext secret storage vulnerability that allows users with Pod read access to obtain secrets by reading init container environment variables. The embedded secret manager webhook writes base64-encoded FILE-mounted secret values into the SECRETS environment variable, letting principals without Secret store access decode them from the Pod spec.

### CVE-2026-108710

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T13:17:13.720 |

NornicDB through 1.4.1 contains a missing authorization vulnerability that allows authenticated users to bypass per-database read restrictions on the /nornicdb/search and /nornicdb/similar endpoints. Viewer-role users allowlisted for a database but denied read can submit search queries or node IDs to retrieve node IDs, labels and full property maps.

### CVE-2026-91829

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-11T07:17:29.193 |

The Subscribe to Comments WordPress plugin before 2.3.3 does not properly validate a parameter before reflecting it into a link target, allowing unauthenticated attackers to perform Reflected Cross-Site Scripting via a crafted URL against anyone who clicks it, including administrators.

### CVE-2026-108700

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T02:16:38.277 |

1Panel-dev CordysCRM before 1.9.2 contains a missing authorization vulnerability that allows authenticated users to list business titles by calling POST /field/source/business-title without permission checks. Users lacking CONTRACT_BUSINESS_TITLE_READ can retrieve organization invoicing entities, exposing tax identification numbers, bank account numbers, opening banks, registration addresses, and phone numbers.

### CVE-2026-108695

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-11T02:16:37.957 |

MultiVendorX WordPress plugin through 5.0.19 contains an incorrect authorization vulnerability that allows vendor accounts to modify marketplace-wide settings via the settings REST endpoint. Attackers with the store_owner role can send POST requests to /wp-json/multivendorx/v1/settings, gated only by edit_stores, to overwrite commission, payout, and onboarding settings.

### CVE-2026-108694

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-11T02:16:37.777 |

ConvertX through 0.19.0 contains an arbitrary file read vulnerability that allows authenticated users to read server files because src/converters/pandoc.ts invokes Pandoc without the --sandbox flag. Attackers can upload a reStructuredText document with an include directive naming an absolute path, convert it, and download output containing the referenced file's contents.

### CVE-2026-108692

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T02:16:37.360 |

1Panel-dev CordysCRM from 1.9.0 before 1.9.2 contains a missing authorization vulnerability in eight ModuleFieldController /field/source data-source endpoints lacking permission checks. Authenticated users denied module permission can page through organization-wide leads, contacts, quotations, contracts, payment plans, payment records, orders and invoices owned by other users.

### CVE-2026-108677

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T22:16:44.800 |

JeecgBoot through 3.9.5 contains a missing authorization vulnerability in GET /sys/api/getUserByName that allows low-privileged authenticated users to retrieve any user's stored password value. Attackers can decrypt the AES-CBC protected response using the hard-coded key exposed by /sys/getEncryptedString to obtain administrators' password ciphertexts for offline guessing.

### CVE-2026-108671

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T22:16:43.920 |

JeecgBoot through 3.9.5 contains a missing authorization vulnerability that allows any authenticated user to read MCP server configurations because the queryById permission check is commented out. Attackers can obtain record ids from the unguarded /airag/app/queryById endpoint and retrieve MCP endpoint URLs, headers, and outbound authentication tokens.

### CVE-2026-108661

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T22:16:42.493 |

JeecgBoot through 3.9.5 contains a missing authorization vulnerability that allows any authenticated user to transfer tenant ownership via POST /sys/tenant/changeOwenUserTenant. Low-privileged attackers can supply userId and tenantId parameters to reassign any tenant's owner to a member, including themselves, and strip the legitimate owner.

### CVE-2026-108648

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T22:16:40.600 |

JeecgBoot through 3.9.5 contains a missing authorization vulnerability in the GET /sys/api/getDynamicDbSourceByCode endpoint of SystemApiController, which lacks Shiro permission or role annotations. Any authenticated low-privileged user can supply datasource codes in the dbSourceCode parameter to retrieve JDBC URLs, usernames and decrypted cleartext database passwords.

### CVE-2026-108623

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T22:16:36.870 |

JeecgBoot through 3.9.5 contains a missing authorization vulnerability in the SysLogController deleteBatch handler that allows any authenticated user to delete system audit log entries. Low-privileged attackers can send a DELETE request with ids set to allclear to wipe the entire sys_log table, erasing all users' audit trails.

### CVE-2026-78534

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:47.260 |

Unauthenticated Cross Site Scripting (XSS) in Educavo <= 3.4.2 versions.

### CVE-2026-78532

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:46.950 |

Unauthenticated Cross Site Scripting (XSS) in LMS <= 8.3 versions.

### CVE-2026-62116

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:43.937 |

Unauthenticated Cross Site Scripting (XSS) in Barcode Scanner with Inventory & Order Manager <= 1.13.1 versions.

### CVE-2026-62100

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:43.693 |

Unauthenticated Cross Site Scripting (XSS) in KuteShop <= 4.2.9 versions.

### CVE-2026-62095

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:43.210 |

Unauthenticated Cross Site Scripting (XSS) in Biolife <= 3.2.3 versions.

### CVE-2026-62093

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:42.973 |

Unauthenticated Cross Site Scripting (XSS) in TechOne <= 3.0.3 versions.

### CVE-2026-62091

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:42.730 |

Unauthenticated Cross Site Scripting (XSS) in Armania <= 1.4.8 versions.

### CVE-2026-62082

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:42.257 |

Unauthenticated Cross Site Scripting (XSS) in Pin WP <= 7.0 versions.

### CVE-2026-62064

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:40.883 |

Unauthenticated Cross Site Scripting (XSS) in Ambed <= 1.0.0 versions.

### CVE-2026-62037

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:39.873 |

Unauthenticated Cross Site Scripting (XSS) in Document Embedder <= 2.4.0 versions.

### CVE-2026-62034

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:39.610 |

Unauthenticated Cross Site Scripting (XSS) in Before After Image Comparison – Image comparison for WP <= 1.1.21 versions.

### CVE-2026-62027

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:38.990 |

Unauthenticated Cross Site Scripting (XSS) in Team Section Block <= 2.0.4 versions.

### CVE-2026-57742

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:38.160 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in ThemeREX Group Kids Planet allows Reflected XSS.

This issue affects Kids Planet: from n/a through 2.2.14.2.

### CVE-2026-42715

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:36.513 |

Unauthenticated Cross Site Scripting (XSS) in Photo Gallery by 10Web <= 1.8.47 versions.

### CVE-2026-42711

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:36.273 |

Unauthenticated Cross Site Scripting (XSS) in Slider by 10Web <= 1.2.63 versions.

### CVE-2026-42709

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:36.157 |

Unauthenticated Cross Site Scripting (XSS) in Food Menu – Restaurant Menu & Online Ordering for WooCommerce <= 6.0.5 versions.

### CVE-2026-42702

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:35.680 |

Unauthenticated Cross Site Scripting (XSS) in Tutor LMS <= 4.1.0 versions.

### CVE-2026-42699

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:35.560 |

Unauthenticated Cross Site Scripting (XSS) in FV Player 8 <= 8.1.8 versions.

### CVE-2026-42697

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:35.433 |

Unauthenticated Cross Site Scripting (XSS) in Social Share Icons & Social Share Buttons <= 3.7.5 versions.

### CVE-2026-42693

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:35.193 |

Unauthenticated Cross Site Scripting (XSS) in Jannah <= 7.6.5 versions.

### CVE-2026-42632

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:34.960 |

Unauthenticated Cross Site Scripting (XSS) in Qode Real Estate <= 1.1.7.3 versions.

### CVE-2026-42631

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:34.837 |

Unauthenticated Cross Site Scripting (XSS) in Qode Music <= 2.1.8.2 versions.

### CVE-2026-40803

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:34.233 |

Unauthenticated Cross Site Scripting (XSS) in Jotform &#8211; AI Chatbot <= 3.8.2 versions.

### CVE-2026-39800

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:33.357 |

Unauthenticated Cross Site Scripting (XSS) in Additional Order Filters for WooCommerce <= 1.24 versions.

### CVE-2026-39799

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T20:16:33.233 |

Unauthenticated Cross Site Scripting (XSS) in WP File Download <= 6.3.6 versions.

### CVE-2026-57806

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T19:16:58.787 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in drfuri Martfury - WooCommerce Marketplace WordPress Theme martfury allows Reflected XSS.This issue affects Martfury - WooCommerce Marketplace WordPress Theme: from n/a through 3.3.9.

### CVE-2026-94160

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T17:17:01.090 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in themeStek ThemeStek Extras for LabtechCO Theme themestek-labtechco-extras allows Reflected XSS.This issue affects ThemeStek Extras for LabtechCO Theme: from n/a through 8.4.

### CVE-2026-108581

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T16:16:31.380 |

TencentCloud Octop through 1.0.2b6 contains a missing authorization vulnerability that allows authenticated low-privileged users to read stored provider API keys via GET /api/providers and GET /api/voice/providers. Attackers can query these endpoints, which only validate the JWT, to obtain plaintext LLM and voice provider API keys and abuse the upstream provider accounts.

### CVE-2026-108547

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-10T15:16:57.707 |

AstronRPA through 1.1.6 contains a missing tenant authorization check in robot-service that allows authenticated users to read other tenants' shared variables via the get-batch-shared-var endpoint. Attackers can enumerate sequential shared variable IDs and decrypt all-users variables re-encrypted with their own tenant key to recover other tenants' credentials in plaintext.
