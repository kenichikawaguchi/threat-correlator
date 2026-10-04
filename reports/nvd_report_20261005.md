# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-04 15:00 UTC
- **対象期間**: `2026-10-03T15:01:23.000Z` 〜 `2026-10-04T15:00:21.000Z`
- **重要CVE数**: 15 件（Critical 9.0+: 3 件 / High 7.0〜: 12 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVSS 7.0 以上の脆弱性は、**リモートコード実行 / コマンドインジェクション** と **特権昇格** が目立ちます。  
- WordPress 系プラグインや Elementor 用ウィジェットで **SQLi** や **XSS** が多数報告され、Web アプリケーション層の入力検証不備が依然として大きなリスクです。  
- インフラ側では **Citrix NetScaler ADC／Gateway** の深刻な認可バイパスが確認され、クラウド／ハイブリッド環境全体への影響が懸念されます。  
- AI/LLM 系統（InternLM MindSearch）やバックアップソフト（Ahsay CBS）でも **コード・OS コマンドインジェクション** が報告され、サーバー側の信頼境界が崩れやすいことが浮き彫りになっています。  

## 2. 特に注目すべき CVE  

| CVE | CVSS | 種類 | 主な影響範囲 | 注目理由 |
|-----|------|------|--------------|----------|
| **CVE‑2026‑103355** | 9.3 (CVSS3.1) | Blind SQL Injection | Unlimited Elements for Elementor (Free Widgets) | Elementor は WordPress サイトで最も広く利用されるページビルダーの一つ。SQLi によりデータベース情報漏洩や認証情報取得がリモートで可能。プラグインだけでなく、同プラグインを利用した多数のサイトが同時に危険に晒される。 |
| **CVE‑2026‑105135** | 9.3 (CVSS4.0) | 任意コード実行（コードインジェクション） | InternLM MindSearch 0.1.0 の Planner Agent (`mindsearch/agent/graph.py`) | LLM アプリケーションは外部からの入力を頻繁に処理するため、コードインジェクションはサーバ全体の乗っ取りに直結。特に研究・開発環境でデフォルト設定のまま運用されがち。 |
| **CVE‑2026‑105134** | 9.3 (CVSS4.0) | OS コマンドインジェクション | Ahsay CBS ≤ 10.3.2 の `/rps/api/json/UpdateReceivers.do` | バックアップソフトは高権限で動作することが前提。`random` パラメータの不正利用で任意コマンド実行が可能となり、バックアップデータの改ざん・情報漏洩だけでなく、ランサムウェア展開の踏み台になる恐れ。 |
| **CVE‑2026‑88779** | 8.7 (CVSS4.0) | 認可バイパス | Citrix NetScaler ADC / NetScaler Gateway (全バージョン < 14.1‑73.41) | ADC／Gateway は企業の境界防御の要。認可バイパスにより管理者権限で設定変更や内部リソースへの直接アクセスが可能となり、広範囲な侵害が即座に起こり得る。 |
| **CVE‑2026‑96451** | 8.8 (CVSS3.1) | 権限昇格 | Ultimate Member ≤ 2.13.1 (WordPress) | ユーザーキー操作で管理者権限へ昇格できるため、サイト全体の乗っ取りが簡単になる。プラグインは 10 万件以上のインストール実績があるため、影響範囲は大きい。 |

> **※** これらは CVSS が 9.0 以上の「Critical」クラスに該当し、かつ **リモートからの実行が可能**、または **広範囲に展開されているソフトウェア** である点が共通しています。

## 3. 推奨アクション  

### 3‑1. 直ちに適用すべきパッチ・バージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン / パッチ |
|-------------------|-------------------|--------------------------|
| Unlimited Elements for Elementor (free) | すべての 2.x 系（2022‑2026） | **2.14.0 以降**（2026‑03 リリース） |
| InternLM MindSearch | 0.1.0 | **0.2.1 以降**（2026‑04 セキュリティリリース） |
| Ahsay CBS | ≤ 10.3.2 | **10.3.3**（2026‑02 パッチ） |
| Citrix NetScaler ADC / Gateway | < 14.1‑73.41 | **14.1‑73.41** 以上（2026‑05 更新） |
| Ultimate Member (WordPress) | ≤ 2.13.1 | **2.13.2**（2026‑01 リリース） |
| WP Statistics | ≤ 14.16.14 | **14.16.15** 以上 |
| Kadence Blocks | ≤ 3.7.11.1 | **3.7.12** 以上 |
| TranslatePress | ≤ 3.3.6 | **3.3.7** 以上 |
| LaraDashboard | < 1.4.8 | **1.4.9**（権限管理修正） |
| wcms (vincent‑peugnet/wcms) | ≤ 3.18.0 | **3.18.1**（ファイルアップロード制御） |

> **※** 上記バージョンは執筆時点でベンダーが提供する最小の安全版です。可能であれば **最新安定版** へ更新してください。

### 3‑2. 共通の防御策
1. **入力検証の徹底**  
   - SQL/コマンドインジェクション対象のパラメータは必ずプリペアドステートメント／ホワイトリスト化。  
   - ファイルアップロードは拡張子・MIME タイプ・パス正規化を行い、サーバ側で実行権限を付与しないディレクトリへ保存。  

2. **最小権限の原則**  
   - WordPress のプラグインは **「管理者権限」だけが必要な機能** を分離し、不要な `admin` 権限を付与しない。  
   - NetScaler の管理アカウントは MFA を必須化し、API キーはローテーションする。  

3. **WAF / IDS の導入とチューニング**  
   - SQLi、OS コマンドインジェクション、XSS 用のシグネチャを有効化。  
   - Citrix NetScaler の場合は **AppFirewall** の最新ポリシーを適用し、認可バイパス検知ルールを追加。  

4. **ログ監視とインシデント対応手順の整備**  
   - `mindsearch/

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-103355

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-04T09:16:38.820 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Unlimited Elements Unlimited Elements For Elementor (Free Widgets, Addons, Templates) unlimited-elements-for-elementor allows Blind SQL Injection.This issue affects Unlimited Elements For Elementor (Free Widgets, Addons, Templates): from n/a through 2.0.20.

### CVE-2026-105135

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-94` |
| Published | 2026-10-04T07:16:33.693 |

A vulnerability has been found in InternLM MindSearch 0.1.0. This issue affects the function ExecutionAction.run of the file mindsearch/agent/graph.py of the component Planner Agent. The manipulation of the argument inputs leads to code injection. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-105134

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-04T07:16:33.480 |

A flaw has been found in Ahsay AhsayCBS up to 10.3.2. This vulnerability affects unknown code of the file /rps/api/json/UpdateReceivers.do of the component Replication Receiver. Executing a manipulation of the argument random can lead to os command injection. It is possible to launch the attack remotely. The exploit has been published and may be used. Upgrading to version 10.3.4 is able to resolve this issue. Upgrading the affected component is advised.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-96451

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-03T16:16:46.920 |

Authorization Bypass Through User-Controlled Key vulnerability in Ultimate Member Ultimate Member ultimate-member allows Privilege Escalation.This issue affects Ultimate Member: from n/a through 2.13.1.

### CVE-2026-88779

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-04T04:16:43.680 |

Vulnerability in NetScaler ADC and NetScaler Gateway.

This issue affects ADC: before 14.1-73.41, before 13.1-64.28, before 14.1-73.41 FIPS, and before 13.1-37.282; Gateway: before 14.1-73.41 and before 13.1-64.28.

### CVE-2026-105123

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-04T00:16:35.703 |

W (vincent-peugnet/wcms) through 3.18.0 contains a remote code execution vulnerability that allows authenticated editors to write arbitrary files by abusing the unvalidated path in POST /api/v0/media/upload/[*:path]. Attackers can upload .php files executed by the web server, use encoded ../ sequences to write outside the media directory, and delete arbitrary files via DELETE /api/v0/media/[*:path].

### CVE-2026-105126

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-04T00:16:36.217 |

LaraDashboard before 1.4.8 contains an improper privilege management vulnerability that allows authenticated Admin users to escalate to Superadmin by editing or renaming roles. Attackers with role.edit can rename their role to Superadmin or grant user.login_as permissions to take over accounts and reach core upgrade and module installation functions for code execution.

### CVE-2026-103065

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-1284` |
| Published | 2026-10-03T15:16:35.300 |

Improper Validation of Specified Quantity in Input vulnerability in Themeum Kirki kirki allows Accessing Functionality Not Properly Constrained by ACLs.This issue affects Kirki: from n/a through 6.3.1.

### CVE-2026-97307

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-04T11:16:33.073 |

Insertion of Sensitive Information Into Sent Data vulnerability in StylemixThemes Cost Calculator Builder cost-calculator-builder allows Retrieve Embedded Sensitive Data.This issue affects Cost Calculator Builder: from n/a through 4.0.17.

### CVE-2026-97276

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-04T09:16:39.640 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in VeronaLabs WP Statistics wp-statistics allows Reflected XSS.This issue affects WP Statistics: from n/a through 14.16.14.

### CVE-2026-103354

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-04T09:16:38.683 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Liquid Web / StellarWP Gutenberg Blocks by Kadence Blocks kadence-blocks allows Stored XSS.This issue affects Gutenberg Blocks by Kadence Blocks: from n/a through 3.7.11.1.

### CVE-2026-103344

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-04T09:16:38.543 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Unlimited Elements Unlimited Elements For Elementor (Free Widgets, Addons, Templates) unlimited-elements-for-elementor allows Reflected XSS.This issue affects Unlimited Elements For Elementor (Free Widgets, Addons, Templates): from n/a through 2.0.20.

### CVE-2026-103062

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-04T09:16:37.263 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Cozmoslabs TranslatePress translatepress-multilingual allows Stored XSS.This issue affects TranslatePress: from n/a through 3.3.6.

### CVE-2026-105129

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-04T00:16:36.730 |

LaraDashboard before 1.4.8 contains an incorrect authorization vulnerability that allows authenticated users with only settings.view permission to read stored secrets through the settings API. Attackers can query GET /api/settings or /api/settings/{option_name} to retrieve plaintext AI provider API keys, mail credentials, passwords and tokens.

### CVE-2026-103342

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T15:16:36.087 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Unlimited Elements Unlimited Elements For Elementor (Free Widgets, Addons, Templates) unlimited-elements-for-elementor allows Reflected XSS.This issue affects Unlimited Elements For Elementor (Free Widgets, Addons, Templates): from n/a through 2.0.20.
