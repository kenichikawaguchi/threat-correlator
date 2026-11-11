# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-11 15:01 UTC
- **対象期間**: `2026-11-10T15:00:25.000Z` 〜 `2026-11-11T15:01:20.000Z`
- **重要CVE数**: 1156 件（Critical 9.0+: 92 件 / High 7.0〜: 1064 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公表された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** に上り、特に **Adobe 製品、WordPress プラグイン、そしてネットワーク機器（FortiManager）** に集中しています。  
- **コードインジェクション / RCE** が目立ち、リモートから認証不要で任意コード実行が可能になるケースが多数。  
- **スコープが変更 (Scope = C)** の脆弱性が多く、攻撃者が横方向に権限を拡大できる点が共通しています。  
- 多くは **既知のパッケージバージョン**（例: STAGGS ≤ 3.3.0、Adobe Connect ≤ 最新リリース、WordPress プラグイン ≤ 1.0.16 など）で **修正がリリース済み** であるため、速やかなパッチ適用が最重要課題です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲・理由 |
|-----|------|----------------|----------------|
| **CVE‑2026‑78287** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | Code Injection (Remote Code Inclusion) | STAGGS 3.3.0 以前の全バージョンで、任意のコードがサーバ上で実行可能。スコープが **Changed** で、攻撃者は他サービスへも権限昇格が可能。 |
| **CVE‑2026‑121352** (Adobe Connect) | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | Incorrect Authorization (Privilege Escalation) | 認証不要で管理権限へ昇格でき、全社内会議・録画データへの不正取得が可能。Adobe Connect は多くの企業でコア業務ツールとして使用されているためインパクト大。 |
| **CVE‑2026‑121353** (Adobe Connect) | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | CRLF Injection → 任意コード実行 | ユーザーコンテキストでコード実行が可能で、XSS 併用により内部ネットワークへの踏み台化が容易。 |
| **CVE‑2026‑126261** | 9.8 (AV:N/AC:L/PR:N/UI:N/S:U) | Improper Authorization (FGFM ポート経由 RCE) | FortiManager 7.2‑7.6 系列で、FGFM ポートに到達できるだけでコード実行が可能。ネットワーク管理者権限取得につながり、全社インフラが危険に晒される。 |
| **CVE‑2026‑123695** | 9.8 (AV:N/AC:L/PR:N/UI:N/S:U) | 認証なしで REST API からトークン取得 → 任意ユーザーでログイン | WooCommerce 用プラグイン「Security For WooCommerce」1.0.16 以前で、管理者アカウントへの不正ログインが可能。EC サイトの顧客情報・決済情報が直接流出リスク。 |

> **注記**  
> - Adobe Connect 系列は **6 件**（SSRF、SQLi、Path Traversal など）すべてが CVSS 10.0 で、同一製品に集中している点が特に危険です。  
> - WordPress 系プラグインは **3 件**（WooCommerce、AskAny、Basel Post Types）が認証バイパスや任意コード実行を許すため、プラグイン管理が甘い環境での被害が顕在化しやすいです。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン / 対策 |
|-------------------|-------------------|------------------------|
| **STAGGS** | ≤ 3.3.0 | 公式が提供する **3.3.1 以降** のリリースへ即時アップデート。 |
| **Adobe Connect** | すべての 2026 年リリース（脆弱性が報告された全バージョン） | Adobe が公開した **2026‑Q3 パッチ**（例: 2026.3.5 以上）を適用。Web アプリケーションファイアウォール (WAF) で **RCE/SSRF/CRLF** 攻撃パターンをブロック。 |
| **Adobe Experience Manager** | すべての 2026 年リリース | **2026.2.2 以降** のアップデートを適用。特に Code Injection 系の修正が含まれるリリースを確認。 |
| **Fortinet FortiManager** | 7.2.0‑7.6.7, 7.4.0‑7.4.5, 8.0.0 | **7.6.8 以上**、もしくは **7.2.9 以上** のファームウェアへ更新。FGFM ポート (TCP 5555) を外部から遮断し、必要な場合は IP アクセスリストで限定。 |
| **WooCommerce – Security For WooCommerce** | ≤ 1.0.16 | **1.0.17 以降**（またはベンダーが提供するパッチ）へ更新。REST API の認証設定を必ず有効化。 |
| **AskAny** | < 2.2.0 | **2.2.0 以上** に更新し、ファイルアップロードの MIME タイプ検証を有効化。 |
| **Basel Post Types** | ≤ 1.18 | **1.19 以降** に更新。`SECURE_AUTH_SALT` の定義ミスが修正されたバージョンを使用。 |
| **AstroBlocks** | < 3.4.0 | **3.4.0 以上** にアップグレードし、JWT シークレットを環境変数 `ASTROBLOCKS_JWT_SECRET` に正しく設定。 |
| **Nitrite (NO2)** | < 4.4.1 | **4.4.1 以上** に更新。データベースオープン時の互換性チェックロジックが修正。 |
| **Active Storage (Rails)** | < 8.1.4.1 / < 8.0.5.2 | **8.1.4.1 以上**、または **8.0.5.2 以上** にアップデートし、ImageMagick の `policy.xml` で外部コマンド実行を禁止。 |
| **Microsoft Windows Media Foundation / Color Management** | 該当 OS の最新パッチ未適用 | Windows Update で **2026‑09‑Cumulative Update** 以降を適用し、ヒープオーバーフロー対策を取得。 |

### 3.2 環境・ネットワークレベルの防御
1. **外部からの直接アクセス遮断**  
   - FortiManager の FGFM ポート、Adobe Connect の管理ポート、STAGGS の管理インターフェースは **ファイアウォールで内部 IP のみ許可**。  
2. **WAF / IDS ルール追加**  
   - `code injection`, `

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-78287

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-11T11:17:21.293 |

Improper Control of Generation of Code ('Code Injection') vulnerability in Staggs STAGGS staggs allows Remote Code Inclusion.This issue affects STAGGS: from n/a through 3.3.0.

### CVE-2026-121889

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-10T22:18:26.180 |

Adobe Connect is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121356

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-10T22:18:25.637 |

Adobe Connect is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121353

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-10T22:18:25.217 |

Adobe Connect is affected by an Improper Neutralization of CRLF Sequences ('CRLF Injection') vulnerability that could result in arbitrary code execution in the context of the current user, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121352

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T22:18:25.060 |

Adobe Connect is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. An attacker could exploit this vulnerability to gain unauthorized access to sensitive resources. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121351

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T22:18:24.910 |

Adobe Connect is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121908

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T22:18:27.533 |

Adobe Connect is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121906

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T22:18:27.400 |

Adobe Connect is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121898

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T22:18:26.897 |

Adobe Connect is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121896

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T22:18:26.773 |

Adobe Connect is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121894

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T22:18:26.650 |

Adobe Connect is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary SQL commands, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121892

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T22:18:26.520 |

Adobe Connect is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121887

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-10T22:18:26.060 |

Adobe Connect is affected by an Improper Restriction of XML External Entity Reference ('XXE') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121354

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T22:18:25.373 |

Adobe Connect is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-119017

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T22:18:24.520 |

Adobe Experience Manager is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-114371

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T22:18:22.617 |

Adobe Experience Manager is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-113580

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T22:18:22.493 |

Adobe Experience Manager is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-113579

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T22:18:22.360 |

Adobe Experience Manager is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-120002

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:20:26.080 |

Incorrect authorization in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-109467

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-10T19:18:15.890 |

Improper authentication in Azure DevOps allows an authorized attacker to execute code over a network.

### CVE-2026-123695

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-11T06:17:18.470 |

The Security For WooCommerce WordPress plugin through 1.0.16 does not restrict access to several of its REST API routes, allowing unauthenticated users to generate login tokens for every user and then retrieve them, and so log in as any user, including administrators.

### CVE-2026-121497

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-11T06:17:16.570 |

The AskAny  WordPress plugin before 2.2.0 does not validate the extension or content of files attached to chat messages, trusting the browser-supplied file type instead, which allows unauthenticated users to upload PHP files and execute arbitrary code when visitor attachments are enabled.

### CVE-2026-64682

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321;CWE-798` |
| Published | 2026-11-11T05:19:52.120 |

AstroBlocks is a block-first CMS for Astro projects. Prior to version 3.4.0, admin session tokens can be forged due to a hard-coded fallback JWT secret and a mismatched environment variable name. An attacker who knows the public fallback value (readable in the published package) can forge a valid session token with role: "owner" and obtain full administrative control of the CMS — creating/deleting content, users, media, redirects, and configuration. This issue has been patched in version 3.4.0.

### CVE-2026-64678

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-11T05:19:51.937 |

NOsql Object (NO2 a.k.a Nitrite) database is an open source nosql embedded document store. Prior to version 4.4.1, when Nitrite opens a database file, MVStoreUtils.openOrCreate() automatically checks for a legacy v1-format store and, on detecting one (or hitting a compatibility error while opening), triggers an automatic migration path. This path deserializes stored values using NitriteDataType.deserialize(byte[]), which passes the raw bytes directly to java.io.ObjectInputStream.readObject() via a custom NitriteObjectInputStream subclass. That subclass overrides only readClassDescriptor() — solely to remap a handful of known legacy class names to their current equivalents — and implements no class allowlist, blocklist, or ObjectInputFilter (JEP 290). Any Serializable class reachable on the embedding application's classpath can therefore be instantiated via readObject(), with readObject()/readExternal()/readResolve() callbacks invoked unconditionally. If a suitable gadget class (e.g. from commons-collections or similar) happens to be present on the classpath, this is a precondition for remote code execution. This issue has been patched in version 4.4.1.

### CVE-2026-126261

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-10T23:17:20.897 |

A improper authorization vulnerability in Fortinet FortiManager 8.0.0, FortiManager 7.6.0 through 7.6.7, FortiManager 7.4.0 through 7.4.5, FortiManager 7.2.0 through 7.2.8 may allow an unauthenticated attacker that can reach the FGFM port to execute code or commands via crafted FGFM packets.

### CVE-2026-89324

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-10T22:21:14.003 |

The Basel Post Types plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 1.18. The vulnerability exists because a missing-quotes coding error in the defined() call for SECURE_AUTH_SALT inside BASEL_Auth::get_config() causes PHP to evaluate the constant's value rather than its name, making the check always fail and permanently falling back to the static hardcoded salt 2NlBUibcszrVtNmDnxqDbwCOpLWq91eatIz6O1O that is publicly visible in the theme source code; because this salt is static and known, an attacker can compute a valid Opauth signature entirely offline and submit a forged ?opauth callback to the unauthenticated init hook endpoint processed by register_or_login. This makes it possible for unauthenticated attackers to authenticate as any existing WordPress user, including administrators, by forging a callback tied to a known target account email address — bypassing all password verification, multi-factor authentication, and ownership checks, and receiving a fully authenticated session cookie via wc_set_customer_auth_cookie(). Exploitation requires WooCommerce to be active and at least one Basel social-login provider (Facebook, Google, or VKontakte) to be configured with a valid app_id and app_secret in the theme settings.

### CVE-2026-126082

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1188` |
| Published | 2026-11-10T21:19:26.980 |

Active Storage makes it simple to upload and reference files in cloud services and attach those files to Active Record objects. Prior to 8.1.4.1 and 8.0.5.2, a Rails application that processes attachments with ImageMagick may allow an unauthenticated attacker to write arbitrary files on the server and, when attachments are stored with the Disk service, to read arbitrary files readable by the application process. Those files typically include secret_key_base and credentials for external systems, which may in turn allow escalation to remote code execution or lateral movement to those systems. ImageMagick selects a coder from the content of the file it is given, and some coders act on files named inside the image rather than on the image itself. Active Storage constrained none of ImageMagick's coders, and the ImageMagick analyzer runs when a file is attached, so an attacker who can upload a crafted file may be able to invoke one. Attaching the upload is sufficient; no variant, preview, or analyze call is required. One specific attack chain has been reported, but other attack chains may exist. An application is affected when it uses ImageMagick for Active Storage image processing through config.active_storage.variant_processor = :mini_magick, runs ImageMagick under a security policy that does not already deny the involved coders, and allows uploads from untrusted users. This issue is fixed in versions 8.1.4.1 and 8.0.5.2.

### CVE-2026-126065

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-10T21:19:24.310 |

OpenObserve is a cloud-native observability platform. Prior to 1.1.0, the shared authentication validator in src/api/common/src/auth/validator.rs accepts an empty or whitespace-only HTTP Basic password for an account whose password_ext value is missing or empty. SSO-provisioned and migration-created users can have this state, allowing an unauthenticated attacker who knows an affected user's email address and organization to authenticate on protected non-ingestion API routes with the victim's role and permissions. A compromised privileged account can expose or modify telemetry, alerts, streams, users, and security configuration. An account with search permission can submit a DataFusion COPY ... TO statement through the search API to create or overwrite attacker-controlled files at service-process-writable locations, creating a conditional escalation to pre-authentication remote code execution. This issue is fixed in version 1.1.0.

### CVE-2026-96157

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:13.027 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-96078

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-11-10T19:22:06.210 |

Heap-based buffer overflow in Microsoft Color Management allows an unauthorized attacker to execute code over a network.

### CVE-2026-96067

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T19:22:04.777 |

Integer overflow or wraparound in Microsoft Color Management allows an unauthorized attacker to execute code over a network.

### CVE-2026-95901

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:21:43.510 |

Double free in Windows Microsoft DirectMusic allows an unauthorized attacker to execute code over a network.

### CVE-2026-95882

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:21:41.527 |

Stack-based buffer overflow in Windows Microsoft DirectMusic allows an unauthorized attacker to execute code over a network.

### CVE-2026-88243

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:21:33.783 |

Out-of-bounds read in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-88234

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-11-10T19:21:32.247 |

Release of invalid pointer or reference in Windows iSCSI allows an unauthorized attacker to execute code over a network.

### CVE-2026-88218

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:21:28.907 |

Double free in Windows DNS allows an unauthorized attacker to execute code over a network.

### CVE-2026-85844

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-10T19:21:25.653 |

Authentication bypass using an alternate path or channel in Windows Kerberos allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-66801

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:17.250 |

Heap-based buffer overflow in Xbox allows an unauthorized attacker to execute code over a network.

### CVE-2026-119990

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T19:20:24.280 |

Missing authentication for critical function in Azure OpenAI allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-119958

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T19:20:19.857 |

Out-of-bounds write in Windows LDAP - Lightweight Directory Access Protocol allows an unauthorized attacker to execute code over a network.

### CVE-2026-116945

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:27.737 |

Heap-based buffer overflow in SQL Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-116928

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T19:19:21.287 |

Out-of-bounds write in Microsoft Windows Search Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-114160

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-10T19:19:09.527 |

Server-side request forgery (ssrf) in Azure Managed Grafana allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-112967

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:46.937 |

Heap-based buffer overflow in Windows Xbox Live Networking Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-61547

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T17:17:45.650 |

rabbitmq-c is a C-language AMQP client library for RabbitMQ. Prior to version 0.17.0, a heap buffer overflow exists in rabbitmq-c when the public amqp_send_frame() API is used to serialize an oversized AMQP_FRAME_BODY. The issue occurs because amqp_frame_to_bytes() copies frame.payload.body_fragment.len bytes into the connection outbound buffer without validating that the body fragment fits within the allocated frame buffer. An application that passes an oversized body frame to amqp_send_frame() can trigger a heap out-of-bounds write, resulting in process crash and memory corruption. This issue has been patched in version 0.17.0.

### CVE-2026-121653

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T16:17:17.580 |

SQL injection in the Core of Ivanti Endpoint Manager before version 2024 SU8 allows a remote unauthenticated attacker to achieve remote code execution.

### CVE-2026-115735

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-11T06:17:13.893 |

The Somatic Framework WordPress plugin through 1.8.14 does not perform an authorization check or validate a user-supplied file path before deleting it, allowing any authenticated user, such as a subscriber, to delete arbitrary files on the server, which can lead to a full site takeover.

### CVE-2026-115734

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-11T06:17:13.753 |

The Pay with a tweet WordPress plugin through 1.0.5 does not validate a file path before deleting it, nor does it restrict access to the relevant administration screens, allowing users with a role as low as Subscriber to delete arbitrary files on the server, which can lead to a full site compromise.

### CVE-2026-121904

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T22:18:27.280 |

Adobe Connect is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a low-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-121349

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T22:18:24.643 |

Adobe Connect is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to gain elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121529

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-10T20:18:56.790 |

A origin validation error vulnerability in Fortinet FortiClientMac 7.4.0 through 7.4.7, FortiClientWindows 7.4.0 through 7.4.7, FortiClientWindows 7.2.0 through 7.2.14, FortiClientWindowsPAM 7.4.7, FortiClientWindowsPAM 7.2.14 may allow an unauthorized remote attacker to execute unauthorized code or commands. Successful exploitation requires interaction with the victim.

### CVE-2026-120779

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T19:20:27.040 |

Improper control of generation of code ('code injection') in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-125347

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T18:17:34.843 |

Incorrect authorization in FileSystem in Google Chrome prior to 157.0.8103.50 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-108186

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-10T16:17:14.183 |

Improper Input Validation in Zoom Workplace for Windows may allow an unauthenticated user to conduct an escalation of privilege via network access.

### CVE-2026-126187

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-10T23:17:20.687 |

React is a JavaScript library for building user interfaces. From 19.0.0 until 19.0.9, 19.1.10, 19.2.9, and 19.3.1, the react-server-dom-webpack, react-server-dom-parcel, and react-server-dom-turbopack packages are vulnerable to unauthenticated remote code execution through crafted payloads targeting frameworks that support React Server Components. The vulnerability only affects extremely rare cases where responses transport multiple typed arrays and an attacker-controlled value. Applications whose React code does not use a server are not affected. Applications that do not use a framework, bundler, or bundler plugin that supports React Server Components are not affected. This issue is fixed in versions 19.0.9, 19.1.10, 19.2.9, and 19.3.1.

### CVE-2026-118383

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T21:18:58.980 |

A use-after-free in the replication component of MongoDB Server can occur when a newly elected replica set primary completes catch-up. The condition can be caused by requests that do not require authentication, and may result in the server terminating unexpectedly or, under certain conditions, arbitrary code execution in the context of the server process. Replica set members are affected, including the shard and config server replica set members of sharded clusters; standalone mongod instances are not.

### CVE-2026-121374

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-11T11:17:14.377 |

Argument injection in the Kubernetes special agent in Checkmk <2.5.0p19, <2.4.0p40, and 2.3.0 (EOL) allows a user with permission to edit rules in at least one folder to write files to arbitrary locations writable by the site user via crafted node roles in the "Exclude nodes based on their role" rule option, leading to code execution as the site user.

### CVE-2026-120495

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-11T11:17:13.433 |

Path traversal in the Synthetic Monitoring "Robotmk" test service of Checkmk <2.5.0p19, <2.4.0p40, and 2.3.0 (EOL) allows an attacker who controls the agent output of a monitored host's check output for a host to inject a crafted robot output to define the contents and location for the generated HTML log, leading to code execution as the site user.

### CVE-2026-118965

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-11T11:17:13.080 |

Path traversal in the discovered host label synchronization in Checkmk <2.5.0p19, <2.4.0p40 and 2.3.0 (EOL) allows an attacker in control of a remote site in a distributed monitoring setup to write arbitrary files on the central site and thereby execute code as the central site user.

### CVE-2026-121902

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T22:18:27.143 |

Adobe Connect is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution. An attacker could exploit this vulnerability to execute arbitrary SQL commands, potentially compromising the confidentiality, integrity, and availability of the application. Exploitation of this issue does not require user interaction.

### CVE-2026-102166

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-10T20:17:21.237 |

Arista C-260 and C-250 access points ship with fleet-wide static cryptographic keys used for firmware image verification and SSLP authentication. An attacker who is able to access these keys would be able to create modified firmware that will pass verification checks. This vulnerability is specific to the C-260 and C-250 models; other access point models enforce digitally signed upgrade images with secure boot and are not affected by this issue.

### CVE-2026-126087

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-10T19:21:13.740 |

Untrusted search path in the cross-user process launcher in Open Job Description (OpenJD) Sessions for Python before 0.11.0, as used in the AWS Deadline Cloud worker agent before 0.33.0, on Linux might allow an authenticated remote user with permission to submit jobs to a queue to execute arbitrary code as the worker agent OS user and obtain the AWS credentials held by the worker agent via a crafted job that modifies the PATH environment variable.



To remediate this issue, users of customer-managed fleets should upgrade the Deadline Cloud worker agent to version 0.33.0 or later, which includes OpenJD Sessions 0.11.0. Service-managed fleets were remediated service-side.

### CVE-2026-61887

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-304` |
| Published | 2026-11-10T18:17:44.703 |

Missing critical step in authentication in the MigTD SPDM rebind implementation for the Intel(R) TDX Migration Trust Domain (MigTD) within Ring 0: Hypervisor may allow an escalation of privilege and information disclosure. Network adversary with an unauthenticated user combined with a low complexity attack may enable remote code execution. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (high) impacts.

### CVE-2026-63011

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-95;CWE-184` |
| Published | 2026-11-10T17:17:45.980 |

Group-Office is an enterprise customer relationship management and groupware tool. Prior to versions 6.8.167, 25.0.102, and 26.0.27, the Contact/labels JMAP endpoint in GroupOffice accepts a fully attacker-controlled template string (tpl parameter) that is passed without restriction to TemplateParser::parse(). When the template contains an [assign] block whose expression includes a {{...}} variable reference, the engine calls eval() on the expanded expression after running it through a validateExpression() guard. The guard double-quotes unrecognized tokens, but PHP 7+ allows a string enclosed in parentheses to be invoked as a function ("system")("id") is valid PHP and calls system("id"). A single authenticated HTTP request is sufficient to execute arbitrary OS commands as the web server user (www-data). This issue has been patched in versions 6.8.167, 25.0.102, and 26.0.27.

### CVE-2026-125757

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-10T16:17:23.107 |

mailcow: dockerized before 2026-11 contains a server-side template injection vulnerability that allows domain administrators to execute commands in the shared rspamd container by storing a malicious domain-wide footer. Attackers can embed a Jinja macro with an os.execute default value, rendered by the rspamd MOO_FOOTER prefilter, to read or inject mail for every tenant and disable filtering.

### CVE-2026-121683

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T16:17:17.900 |

Missing authentication in Ivanti Cloud Services Application version 5.0.8 allows a remote unauthenticated attacker to add and delete arbitrary trusted EPM Core certificate entries.

### CVE-2026-112174

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-11T10:16:42.960 |

Local privilege escalation vulnerability in Iperius Backup 8.8.3, due to insufficient separation between the graphical user interface running with elevated privileges and local users with low privileges. When the backup service is configured to run persistently with Administrator privileges, a local attacker with low privileges can use the native Windows dialogues exposed by the application to run programmes that inherit its elevated context. This allows commands to be executed with SYSTEM or Administrator privileges, depending on the application’s context, and compromises the affected Windows system.

### CVE-2026-64670

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-11-11T05:19:51.527 |

Waline is a comment system with backend support. In versions 3.15.2 and prior, @waline/client renders the comment editor's live preview with marked and no sanitizer (utils/markdown.ts), and the preview is injected with v-html. When a comment is edited, the editor is seeded with the comment's raw, un-sanitized body (orig). Only administrators and the comment owner can edit. So an administrator who clicks Edit on an attacker's comment renders that attacker's raw HTML in their own session: an unauthenticated commenter achieves privilege-escalation stored XSS against a moderator with a single Edit click. At time of publication, there are no publicly available patches.

### CVE-2026-126542

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-11T01:17:15.547 |

WWBN AVideo 6.5 through 29.7.1 contains an authentication bypass vulnerability that allows unauthenticated attackers to log in as any user via Hybridauth social login display names. Attackers can set their X, Facebook, Yahoo or LinkedIn display name to a victim's username and withhold email, causing login.json.php or oauth2.php to log them in as that account, including administrators, without a password.

### CVE-2026-125883

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-10T22:18:31.143 |

Improper restriction of XML external entity reference vulnerability in N-able N-central allows XML Schema Poisoning.

This issue affects N-central: before 26.4.1.

### CVE-2026-125881

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-10T22:18:30.860 |

Server-Side request forgery (SSRF) vulnerability in N-able N-central allows Server Side Request Forgery.

This issue affects N-central: before 26.4.1.

### CVE-2026-125298

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-10T22:18:30.240 |

AsiaInfo Business Support System (BSS) 9.2.0 through 9.2.40 does not correctly verify cryptographic signatures for JSON Web Tokens (JWT). A remote, unauthenticated attacker could forge a well-formed JWT without a valid signature and use it to execute privileged actions. Fixed in 9.2.41.

### CVE-2026-125297

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-11-10T22:18:30.080 |

AsiaInfo Business Support System (BSS) 9.2.0 through 9.2.40 accepts unauthenticated requests via the management API '/bss/sysmgnt/api/'. A remote, unauthenticated attacker could provision a new account with administrative privileges or take over existing accounts, and perform other administrative actions. Fixed in 9.2.41.

### CVE-2026-121289

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T20:18:54.283 |

On affected platforms running Arista EOS with BGP configured, a specially crafted packet can cause the BGP agent to crash.

Successful exploitation causes the BGP agent process to terminate, resulting in the loss of all BGP sessions on the affected device and possible disruption to network routing until the process recovers. Due to the nature of the vulnerability, it may also be possible for a sophisticated attacker to achieve arbitrary code execution, which could compromise the confidentiality and integrity of the affected system.

### CVE-2026-44685

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-10T18:17:40.273 |

Authentication bypass by spoofing in the MigTD rebinding protocol for the Intel(R) TDX Migration Trust Domain (MigTD) within Ring 0: Hypervisor may allow an escalation of privilege. System software adversary with a privileged user combined with a low complexity attack may enable local code execution. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (high) impacts.

### CVE-2026-126539

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636` |
| Published | 2026-11-11T01:17:15.173 |

Directus before 12.1.0 contains an authorization bypass vulnerability that allows unauthenticated attackers to skip permission checks by sending a failed auth message on public-mode WebSocket connections. Attackers can send an invalid token so handleAuthRequest sets accountability to null, then read, create, update or delete records in any user-defined collection.

### CVE-2026-121370

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-10T20:18:56.507 |

On affected platforms running Arista EOS with Precision Time Protocol (PTP) configured, an unauthenticated attacker with network access to a PTP-enabled port can create a denial of service (DoS) condition by sending traffic to the system.

### CVE-2026-121295

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-11-10T20:18:55.750 |

On affected platforms running Arista EOS configured as S-BFD peers, an unauthenticated attacker could send a crafted S-BFD PDU to an initiator device. This crafted PDU could cause the kernel on the initiator device to crash, resulting in an unexpected device reboot.

### CVE-2026-61473

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-11-10T18:17:44.563 |

Authentication bypass by capture-replay in the MigTD for the Intel(R) TDX Migration Trust Domain (MigTD) within Ring 0: Hypervisor may allow an escalation of privilege. System software adversary with a privileged user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (none) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (none) impacts.

### CVE-2026-126537

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-11T13:17:23.810 |

The Ninja Forms - File Uploads add-on for WordPress is vulnerable to Arbitrary File Deletion (and arbitrary file read via S3/Dropbox/Google Drive exfiltration) in versions up to, and including, 3.3.36. The flaw spans NF_FU_Fields_Upload::process() in includes/fields/upload.php — which returns early (leaving the client-supplied files[] intact) whenever a public submission carries a nonempty extra.saveProgress — and NF_FU_External_Abstracts_Service::process_upload() in includes/external/abstracts/service.php, whose authoritative-path reload only fires when the client sends upload_id. By omitting upload_id, an attacker's data[file_path] survives into the Background Upload queue and is used by both upload_file_to_s3() (as SourceFile) and the maybe_delete_server_file() unlink() call in includes/external/abstracts/backgroundupload.php, with no canonicalization or upload-directory containment check (the plugin's own is_path_within_upload_dir() helper is only applied on admin paths). This makes it possible for unauthenticated attackers to delete arbitrary files on the affected site's server which may make remote code execution possible — specifically, deleting wp-config.php forces WordPress into its setup screen, enabling full site takeover.

### CVE-2026-115733

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-11T06:17:13.607 |

The Printaura-Woocommerce WordPress plugin through 4.0.2 does not properly restrict access to the WooCommerce REST API, causing every WooCommerce REST route to accept unauthenticated requests, which allows unauthenticated attackers to read and modify store data including customer orders and personal information, store and payment settings, and webhooks.

### CVE-2026-82391

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T22:21:05.710 |

The HTTP/2 front-end of the Zephyr HTTP server aliased connection receive state as a scratch output. In subsys/net/lib/http/http_server_http2.c, handle_http2_static_fs_resource() passed &client->data_len as the file_size out-parameter of http_server_find_file(). client->data_len is the count of unprocessed bytes remaining in the fixed-size per-connection receive buffer client->buffer[CONFIG_HTTP_SERVER_CLIENT_BUFFER_SIZE] (256 bytes by default), an invariant every frame handler and the socket receive path rely on. Serving any static file therefore replaced that bounded value with the file's on-disk size, and nothing resets it afterwards.

The defect is reached by an unauthenticated HTTP/2 GET for any file under the web root, in applications that register a static-filesystem resource (HTTP_RESOURCE_TYPE_STATIC_FS) with CONFIG_FILE_SYSTEM=y; CONFIG_HTTP_SERVER_VERSION_2 is enabled by default and no TLS or credentials are required on this path. Once client->data_len exceeds the buffer size, the frame dispatch loop in subsys/net/lib/http/http_server_core.c keeps parsing past the end of the received data, and the peer controls the bytes at client->cursor, so it can choose which fabricated frame the state machine consumes next by appending bytes after its request.

The inflated length defeats the only guards on the buffer. parse_http_frame_header() and the per-frame handlers read and skip up to a 24-bit frame length beyond the buffer (out-of-bounds read); the compaction memmove(client->buffer, client->cursor, client->data_len) at the end of request handling copies the file-size number of bytes into the 256-byte buffer, overflowing the rest of struct http_client_ctx — including the current_detail/current_stream pointers, the parser_settings function-pointer table and the inactivity_timer work handler — and the adjacent client contexts in static memory; and the subsequent zsock_recv(client->fd, client->buffer + client->data_len, sizeof(client->buffer) - client->data_len, 0) underflows its size argument, writing attacker-supplied data of attacker-chosen length out of bounds.

The impact is remote memory corruption in the server's single address space: at minimum a crash or hang of the device, and plausibly control-data overwrite leading to code execution. The HTTP/1 and HTTP/3 static-filesystem handlers already used a local variable and are unaffected; the fix makes the HTTP/2 handler use a local size_t file_size as well.

### CVE-2026-121355

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T22:18:25.510 |

Adobe Connect is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. An attacker could exploit this vulnerability to gain elevated access to sensitive information or functionality. Exploitation of this issue does not require user interaction.

### CVE-2026-120808

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-10T20:18:51.180 |

An issue exists in MongoDB's macOS TLS client implementation where certificate chain-of-trust validation is bypassed for outbound connections to IPv6-addressed peers. When a MongoDB process using the Apple SecureTransport TLS backend connects to an IPv6 target, the trust evaluation result from SecTrustEvaluate is silently discarded, regardless of whether the peer's certificate is trusted. An on-path party could exploit this by presenting a self-signed certificate containing the target's IPv6 address in the Subject Alternative Name to intercept and modify encrypted inter-node or external service traffic. This issue only affects MongoDB processes running on macOS with the Apple SecureTransport TLS provider.

### CVE-2026-125331

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862;CWE-863` |
| Published | 2026-11-10T19:21:10.630 |

HarnessRouter is a self-hosted unified API for running agent harnesses with sessions, streaming, files, cancellation, and failure handling. Prior to 0.31.8, a console that is not in self-hosted mode attaches the server's internal key to requests carrying an Authorization header before validating the bearer, while the service-only PUT and GET /v1/orgs/{org}/connections/{name}, PUT /v1/orgs/{org}/policy/{backend}, and /internal/* routes trust that key and take the organization from the URL. In a multi-organization deployment, a remote caller can use a made-up bearer to rewrite another organization's provider connection to an attacker-controlled endpoint, causing later prompts to be disclosed and attacker-controlled responses to influence tasks. This issue is fixed in version 0.31.8.

### CVE-2026-118740

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T19:19:50.740 |

Missing authorization in Aspire allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-114162

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:19:09.807 |

Incorrect authorization in Microsoft Graph allows an authorized attacker to elevate privileges over a network.

### CVE-2026-125758

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-11-10T16:17:23.267 |

Aptabase before commit 61d4c01 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge sign-in links by using the publicly known example AUTH_SECRET. Attackers can enumerate registered e-mails via /api/_auth/signin, forge HS256 JWTs redeemed by /api/_auth/continue, impersonate users, export analytics data, and transfer app ownership.

### CVE-2026-95962

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:51.060 |

Use after free in Windows Virtual Filtering Platform (VFP) allows an unauthorized attacker to execute code over a network.

### CVE-2026-80095

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:21:22.760 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-114146

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:19:07.683 |

Incorrect authorization in ASP.NET Core allows an authorized attacker to elevate privileges over a network.

### CVE-2026-109454

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:18:14.347 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-121368

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T20:18:56.123 |

On affected platforms running Arista EOS with Bidirectional Forwarding Detection (BFD) configured to use keyed MD5 or keyed SHA1 authentication, an unauthenticated attacker with network adjacency (direct or multi-hop) to a BFD-enabled interface can send a specially crafted BFD packet resulting in a system reboot.

### CVE-2026-125850

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:37.853 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti Appointment Dark appointment-dark allows Cross Site Request Forgery.This issue affects Appointment Dark: from n/a through 1.3.4.

### CVE-2026-125849

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:37.557 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti Shk Corporate shk-corporate allows Cross Site Request Forgery.This issue affects Shk Corporate: from n/a through 2.4.3.

### CVE-2026-125848

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:37.267 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti Leo leo allows Cross Site Request Forgery.This issue affects Leo: from n/a through 1.7.4.

### CVE-2026-125847

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:37.083 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti vdperanto vdperanto allows Cross Site Request Forgery.This issue affects vdperanto: from n/a through 2.2.

### CVE-2026-125846

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:36.920 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti Mazino mazino allows Cross Site Request Forgery.This issue affects Mazino: from n/a through 1.1.

### CVE-2026-125845

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:36.757 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti vdequator vdequator allows Cross Site Request Forgery.This issue affects vdequator: from n/a through 1.2.7.

### CVE-2026-125844

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:36.593 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti vice vice allows Cross Site Request Forgery.This issue affects vice: from n/a through 1.4.

### CVE-2026-125843

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:36.417 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti Spasalon spasalon allows Cross Site Request Forgery.This issue affects Spasalon: from n/a through 3.0.

### CVE-2026-125842

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:36.257 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti Wallstreet Agency wallstreet-agency allows Cross Site Request Forgery.This issue affects Wallstreet Agency: from n/a through 1.3.4.

### CVE-2026-125841

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:36.083 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti Heroic heroic allows Cross Site Request Forgery.This issue affects Heroic: from n/a through 1.4.2.

### CVE-2026-125840

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:35.923 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti Rambo rambo allows Cross Site Request Forgery.This issue affects Rambo: from n/a through 3.0.

### CVE-2026-125839

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:35.750 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti ElitePress elitepress allows Cross Site Request Forgery.This issue affects ElitePress: from n/a through 3.2.1.

### CVE-2026-125838

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T14:17:35.563 |

Cross-Site Request Forgery (CSRF) vulnerability in webriti Quality quality allows Cross Site Request Forgery.This issue affects Quality: from n/a through 3.3.

### CVE-2026-125446

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T13:17:21.387 |

Cross-Site Request Forgery (CSRF) vulnerability in WisdmLabs Edwiser Bridge edwiser-bridge allows Cross Site Request Forgery.This issue affects Edwiser Bridge: from n/a through 4.3.4.

### CVE-2026-118411

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T13:17:16.313 |

Cross-Site Request Forgery (CSRF) in Apache Roller 5.0.1 through 6.1.6 allows an unauthenticated attacker to create an administrator account if a logged-in Roller administrator opens a link that the attacker controls. The request-token check applied only to POST requests, and administrative actions also accepted GET requests. Users are recommended to upgrade to Apache Roller 6.1.7 or later, which requires POST and a valid token for actions that change data.

### CVE-2026-125784

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-11T12:19:50.867 |

Cross-Site Request Forgery (CSRF) vulnerability in Magnigenie RestroPress restropress allows Cross Site Request Forgery.This issue affects RestroPress: from n/a through 3.4.11.

### CVE-2026-119615

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-11T12:19:15.223 |

The Reset Database plugin for WordPress is vulnerable to privilege escalation in versions up to, and including, 1.1.3. This is due to the process_reset() function being registered on admin_init with no capability check, a computed-but-unused nonce, a gating condition that passes whenever no WordPress administrator literally named 'admin' exists (the default on modern installs), and an identity test that verifies the ATTACKER'S OWN password rather than an administrator's. This makes it possible for authenticated attackers, with subscriber-level access and above, to drop every prefixed database table, re-run wp_install() with their own credentials — making the attacker the sole site administrator — authenticate as that administrator via wp_set_auth_cookie(), and delete the uploads directory.

### CVE-2026-103883

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-11T12:18:14.700 |

The 6Storage Rentals plugin for WordPress is vulnerable to Authentication Bypass leading to Administrator Account Takeover in all versions up to, and including, 2.31.0. The vulnerability exists because the `six_storage_portal_registration()` AJAX handler — registered on `wp_ajax_six_storage_portal_plugin_registration` — performs no capability check and no nonce verification before writing the caller-supplied `six_storage_online_api_url` POST parameter to the site-wide option of the same name; the unauthenticated `six_storage_create_wp_user()` handler then redeems a transient seeded from that attacker-controlled URL's response and unconditionally calls `wp_set_current_user()` and `wp_set_auth_cookie()` with no ownership or credential verification. This makes it possible for authenticated attackers, with Subscriber-level access and above, to authenticate as any existing WordPress user — including any administrator whose email address is known or guessable — resulting in full site compromise. This issue represents an incomplete fix for a prior vulnerability: the 2.29.0 remediation moved the target email out of POST data into a server-side transient, but because any Subscriber can still overwrite the outbound API URL that populates that transient, the full authentication bypass chain remains exploitable in three AJAX requests.

### CVE-2026-126617

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T09:17:13.860 |

SQL injection in the database layer of Progressive Robot hMailServer 6.0.0-B1 through 6.2.18, when the server uses MySQL/MariaDB or PostgreSQL, allows a remote attacker to alter SQL statements the server runs. On those two engines parameters are not bound: SQLStatement::GenerateFromCommand wrote each value into the statement's text as a quoted literal with a separate string replacement over the whole text per parameter, so a value holding the name of a parameter substituted after it had that name replaced, inside the value, by the later value with its own quotes, which ended the literal early and placed the later value in the statement as SQL. The row the server writes for each recipient of a queued message carries the recipient's address twice, so in the default configuration an authenticated user who may send mail reaches it by sending to an address of their choosing. A remote unauthenticated sender reaches the same statement through a message the server sends to the envelope sender, such as a delivery failure notice or an automatic reply, and, when greylisting or message indexing is enabled (both are off by default), through the greylisting record's envelope addresses or through the message metadata the server stores for IMAP SORT, which carries four header fields of a received message. An altered statement runs with the privileges of the server's database account; on PostgreSQL, whose client call runs every statement in the text it is given, further statements can follow it, while on MySQL/MariaDB, where one statement is run per call, the change is confined to the statement it is in. SQL Server and SQL Server Compact, where parameters are bound, are not affected.

### CVE-2026-76981

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T08:17:18.760 |

Zoho Corporation ManageEngine ADAudit Plus versions below 8711 are vulnerable to an authenticated second order SQL injection vulnerability affecting ADAudit Plus custom reports module.

### CVE-2026-12062

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T08:17:17.960 |

Zoho Corporation ManageEngine ADAudit Plus versions below 8703 are vulnerable to an authenticated SQL injection vulnerability in ADAudit Plus Reports API.

### CVE-2026-123134

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T06:17:17.693 |

The Smoove abandoned cart trigger for WooCommerce WordPress plugin before 4.3.6 does not sanitise and escape abandoned-cart data submitted by visitors before outputting it in the admin dashboard, allowing unauthenticated users to perform Stored Cross-Site Scripting attacks against administrators.

### CVE-2026-121998

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-11T06:17:17.270 |

The iChart  WordPress plugin before 2.2.4 does not perform capability or ownership checks in several of its AJAX actions, relying only on a nonce that any logged-in user can obtain, allowing users with a role as low as Subscriber to read, modify and permanently delete arbitrary posts and to overwrite a site-wide option.

### CVE-2026-121862

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T06:17:16.710 |

The Knowledge Building WordPress plugin before 0.7.3 does not sanitise and escape comments submitted through its reply feature, and publishes them without moderation, allowing unauthenticated users to perform Stored Cross-Site Scripting attacks against any visitor of the affected posts, including administrators.

### CVE-2026-118041

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-11T06:17:14.767 |

The Contest Gallery  WordPress plugin before 34.0.3 does not sanitise the name of files uploaded through its e-commerce sale file-replacement feature, allowing authenticated users with Author-level access and above to write files with an arbitrary name and extension to a web-accessible directory and, by overwriting the directory's protection file through the same flow, achieve Remote Code Execution.

### CVE-2026-126186

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-646` |
| Published | 2026-11-10T22:18:31.843 |

Active Storage makes it simple to upload and reference files in cloud services and attach those files to Active Record objects. Prior to 8.1.4.1 and 8.0.5.2, ActiveStorage::Blob#open writes a blob to a tempfile whose name carries the extension of the uploaded filename, and hands that path to ffprobe (VideoAnalyzer, AudioAnalyzer), ffmpeg (VideoPreviewer) and ImageMagick (ImageAnalyzer, the :mini_magick variant processor). These tools select a decoder from the file extension when the content does not identify its own format, so an attacker who chooses the filename and declares the content type of an upload chooses which decoder processes it. An FFmpeg built with AviSynth support treats a file with the .avs extension as an AviSynth script and evaluates it, which could disclose files readable by the application process through the preview image, or load a native library the attacker has also uploaded, possibly leading to remote code execution in the FFmpeg process. ImageMagick selects its coders and delegates from the extension in the same way. An application is affected if it accepts uploads from untrusted users and analyzes video or audio attachments, generates video previews, or processes images with ImageMagick. The AviSynth attack additionally requires an FFmpeg built with --enable-avisynth and the AviSynthPlus runtime on the host. Upstream FFmpeg and the common Linux distribution and Homebrew packages do not enable it; the GPL builds distributed for Windows and Linux from ffmpeg.org do. Other decoders that FFmpeg or ImageMagick select from the extension may be reachable without AviSynth. This issue is fixed in versions 8.1.4.1 and 8.0.5.2.

### CVE-2026-121913

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T22:18:27.920 |

Adobe Connect is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain elevated access to sensitive information or functionality. Exploitation of this issue does not require user interaction.

### CVE-2026-26248

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T20:19:11.280 |

A improper neutralization of input during web page generation ('cross-site scripting') vulnerability in Fortinet FortiSandbox 5.0.0 through 5.0.5, FortiSandbox 4.4.0 through 4.4.8, FortiSandbox 4.2 all versions, FortiSandbox Cloud 5.0.4 through 5.0.5, FortiSandbox PaaS 5.0.4 through 5.0.5 may allow an unauthenticated attacker to perform an XSS attack via social engineering and crafted HTTP requests.

### CVE-2026-96164

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:13.770 |

Heap-based buffer overflow in Windows Imaging Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-96064

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:04.450 |

Heap-based buffer overflow in DNS Server allows an authorized attacker to execute code over a network.

### CVE-2026-96020

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T19:21:58.657 |

Out-of-bounds write in DNS Server allows an authorized attacker to execute code over a network.

### CVE-2026-96010

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-10T19:21:57.800 |

Integer underflow (wrap or wraparound) in HID Parser Library allows an authorized attacker to elevate privileges over a network.

### CVE-2026-96002

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:56.850 |

Heap-based buffer overflow in DNS Server allows an authorized attacker to execute code over a network.

### CVE-2026-95996

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-10T19:21:55.927 |

Integer underflow (wrap or wraparound) in Windows Bluetooth Port Driver allows an authorized attacker to elevate privileges over a network.

### CVE-2026-95975

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:54.163 |

Heap-based buffer overflow in Windows Performance Counters allows an unauthorized attacker to execute code over a network.

### CVE-2026-95960

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-10T19:21:50.187 |

Access of resource using incompatible type ('type confusion') in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-94511

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:36.760 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-88249

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:34.447 |

Use after free in Windows Client for NFS allows an unauthorized attacker to execute code over a network.

### CVE-2026-88229

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:31.343 |

Heap-based buffer overflow in Windows Media Player allows an unauthorized attacker to execute code over a network.

### CVE-2026-88222

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:30.117 |

Heap-based buffer overflow in Microsoft WDAC OLE DB provider for SQL allows an unauthorized attacker to execute code over a network.

### CVE-2026-88176

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T19:21:26.847 |

Missing authorization in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-85923

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-10T19:21:26.240 |

Authorization bypass through user-controlled key in Azure DevOps Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-85839

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:25.460 |

Heap-based buffer overflow in Microsoft WDAC OLE DB provider for SQL allows an unauthorized attacker to execute code over a network.

### CVE-2026-85838

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:25.250 |

Heap-based buffer overflow in Microsoft WDAC OLE DB provider for SQL allows an unauthorized attacker to execute code over a network.

### CVE-2026-70094

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-10T19:21:20.410 |

Untrusted search path in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-67646

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:19.327 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67637

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:19.173 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67632

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:19.013 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67391

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:18.843 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67387

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:21:18.687 |

Untrusted pointer dereference in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-67375

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:21:17.960 |

Stack-based buffer overflow in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-67374

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:17.813 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-67372

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:17.663 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-125136

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:07.360 |

Heap-based buffer overflow in Windows Network Connected Devices Auto-Setup Service allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-124228

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T19:20:50.050 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Microsoft Office Outlook allows an authorized attacker to execute code over a network.

### CVE-2026-124226

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-10T19:20:49.467 |

Execution with unnecessary privileges in Windows PowerShell allows an authorized attacker to bypass a security feature locally.

### CVE-2026-124187

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:47.997 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-124176

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:45.303 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-124174

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:44.780 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-123394

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-11-10T19:20:43.187 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-123391

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:20:43.010 |

Incorrect authorization in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-123390

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-10T19:20:42.837 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-123385

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:20:42.053 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-123384

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:41.907 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-123383

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:41.763 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-123382

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:20:41.617 |

Untrusted pointer dereference in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-123381

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-681` |
| Published | 2026-11-10T19:20:41.470 |

Stack-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-123380

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:41.317 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-123377

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:20:40.893 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-123376

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:40.737 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-123375

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-191` |
| Published | 2026-11-10T19:20:40.590 |

Stack-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-122475

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:20:37.417 |

Untrusted pointer dereference in Windows Storage Spaces Controller allows an unauthorized attacker to execute code over a network.

### CVE-2026-122198

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:36.843 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-122194

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-10T19:20:36.467 |

Null pointer dereference in Microsoft Defender allows an unauthorized attacker to execute code over a network.

### CVE-2026-122176

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:35.520 |

Heap-based buffer overflow in Windows SMB allows an authorized attacker to execute code over a network.

### CVE-2026-122171

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:34.540 |

Heap-based buffer overflow in Microsoft XPS Document Converter allows an unauthorized attacker to execute code over a network.

### CVE-2026-121665

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-501` |
| Published | 2026-11-10T19:20:30.100 |

Trust boundary violation in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-121663

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-10T19:20:29.777 |

Incomplete list of disallowed inputs in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-120791

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:28.490 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-120790

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:28.220 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-120789

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:28.080 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-120788

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:27.933 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-120786

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:27.793 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-120785

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:27.650 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-120005

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:26.403 |

Heap-based buffer overflow in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-120003

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:26.240 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-120001

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:25.920 |

Heap-based buffer overflow in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-119986

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:23.610 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-119983

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-10T19:20:23.310 |

Server-side request forgery (ssrf) in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-119975

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:20:22.667 |

Improper neutralization of input during web page generation ('cross-site scripting') in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-119969

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:21.770 |

Heap-based buffer overflow in Graphic Fonts allows an unauthorized attacker to execute code over a network.

### CVE-2026-119950

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:18.490 |

Heap-based buffer overflow in Windows Print Spooler Components allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-119934

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:20:15.487 |

Double free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-119925

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:20:14.303 |

Out-of-bounds read in Windows Text Services Framework allows an authorized attacker to elevate privileges locally.

### CVE-2026-119916

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:13.213 |

Heap-based buffer overflow in Windows Input System allows an authorized attacker to elevate privileges locally.

### CVE-2026-119908

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-10T19:20:11.630 |

Integer underflow (wrap or wraparound) in Windows Storage Spaces Controller allows an unauthorized attacker to execute code over a network.

### CVE-2026-119881

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:20:07.430 |

Heap-based buffer overflow in Microsoft XPS Document Converter allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-119862

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:20:04.997 |

Out-of-bounds read in Windows Input System allows an authorized attacker to elevate privileges locally.

### CVE-2026-119839

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-10T19:20:00.970 |

Untrusted search path in Remote Desktop Client allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-119824

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T19:19:57.290 |

Missing authentication for critical function in Remote Desktop Client allows an unauthorized attacker to perform tampering over a network.

### CVE-2026-119392

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:53.700 |

Heap-based buffer overflow in Windows Storage Spaces Controller allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-118745

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:51.200 |

Heap-based buffer overflow in Visual Studio allows an unauthorized attacker to execute code over a network.

### CVE-2026-118732

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:49.843 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118731

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:49.687 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118730

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:49.533 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118729

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:49.377 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118726

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-193` |
| Published | 2026-11-10T19:19:48.853 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118725

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:19:48.720 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-118724

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:19:48.570 |

Untrusted pointer dereference in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118722

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:48.230 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118721

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:48.090 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118720

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:47.947 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118719

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:19:47.800 |

Double free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118718

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:47.650 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118717

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:47.507 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118716

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:47.337 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118715

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:47.117 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-118714

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:46.960 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118713

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:46.820 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118712

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-10T19:19:46.667 |

Integer underflow (wrap or wraparound) in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118711

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:46.510 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118710

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:46.360 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118709

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:46.203 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118708

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-11-10T19:19:46.053 |

Release of invalid pointer or reference in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118707

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:45.890 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118706

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:45.740 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118705

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:45.573 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118704

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:45.403 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118703

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:44.553 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118702

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:19:44.377 |

Double free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118701

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:44.233 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118700

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:44.090 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118302

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:43.947 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118299

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:43.507 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118298

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:43.370 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118297

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:43.217 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118296

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:19:43.037 |

Double free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118295

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-190` |
| Published | 2026-11-10T19:19:42.883 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118294

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:42.743 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118293

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-11-10T19:19:42.600 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118292

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:42.447 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118283

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:42.113 |

Stack-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118279

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:19:41.757 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118278

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:19:41.577 |

Out-of-bounds read in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118277

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:41.393 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118232

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:19:41.227 |

Out-of-bounds read in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118229

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:41.050 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118228

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:40.873 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118227

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:40.690 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118226

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:40.503 |

Stack-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118225

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-10T19:19:40.337 |

Inclusion of functionality from untrusted control sphere in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118221

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:39.593 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118219

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:39.160 |

Use after free in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118218

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:38.970 |

Use after free in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118217

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:38.780 |

Use after free in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118216

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:38.590 |

Use after free in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118207

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-11-10T19:19:37.653 |

Improper input validation in Microsoft Exchange Server allows an authorized attacker to execute code over a network.

### CVE-2026-118154

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-807` |
| Published | 2026-11-10T19:19:37.340 |

Reliance on untrusted inputs in a security decision in Microsoft Exchange Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118150

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-10T19:19:36.603 |

Authorization bypass through user-controlled key in Microsoft Exchange Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118149

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T19:19:36.440 |

Improper control of generation of code ('code injection') in Microsoft Exchange Server allows an authorized attacker to execute code over a network.

### CVE-2026-118146

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:19:34.907 |

Incorrect authorization in Active Directory Domain Services allows an authorized attacker to execute code over a network.

### CVE-2026-118141

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:33.897 |

Stack-based buffer overflow in Windows Client for NFS allows an unauthorized attacker to execute code over a network.

### CVE-2026-118120

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T19:19:30.893 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118110

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T19:19:29.267 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118109

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T19:19:29.107 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118105

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T19:19:28.663 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-116946

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:27.920 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-116942

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:27.250 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-116941

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:27.090 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-116934

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:19:24.750 |

Untrusted pointer dereference in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-116930

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-10T19:19:22.843 |

Improper neutralization of special elements used in a command ('command injection') in SQL Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-116927

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:20.650 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-116925

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:19.600 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-116923

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:18.813 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-116722

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:18.003 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-116720

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:16.517 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-116719

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:15.903 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-116717

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:14.773 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-114171

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-451` |
| Published | 2026-11-10T19:19:10.887 |

User interface (ui) misrepresentation of critical information in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-114169

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:10.537 |

Heap-based buffer overflow in Windows Raw Image Extension allows an unauthorized attacker to execute code over a network.

### CVE-2026-114164

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-10T19:19:09.963 |

Integer underflow (wrap or wraparound) in Microsoft Windows Codecs Library allows an unauthorized attacker to execute code over a network.

### CVE-2026-114159

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:09.380 |

Heap-based buffer overflow in Visual Studio allows an unauthorized attacker to execute code over a network.

### CVE-2026-114158

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:09.240 |

Heap-based buffer overflow in Visual Studio allows an unauthorized attacker to execute code over a network.

### CVE-2026-114152

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-822` |
| Published | 2026-11-10T19:19:08.497 |

Stack-based buffer overflow in Visual Studio allows an unauthorized attacker to execute code over a network.

### CVE-2026-114151

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-502` |
| Published | 2026-11-10T19:19:08.357 |

Deserialization of untrusted data in Visual Studio allows an unauthorized attacker to execute code over a network.

### CVE-2026-113863

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:07.193 |

Heap-based buffer overflow in Windows DHCP Client allows an unauthorized attacker to elevate privileges over an adjacent network.

### CVE-2026-113814

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:18:59.373 |

Untrusted pointer dereference in Windows Storage Spaces Controller allows an unauthorized attacker to execute code over a network.

### CVE-2026-113760

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:54.827 |

Heap-based buffer overflow in Windows XWizard Framework allows an authorized attacker to elevate privileges locally.

### CVE-2026-112805

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:18:43.213 |

Untrusted pointer dereference in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-112762

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-10T19:18:39.323 |

Relative path traversal in Windows Print Spooler Components allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-112741

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:33.923 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112739

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:33.497 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112737

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:33.130 |

Use after free in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-112735

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:32.780 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112734

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:32.603 |

Use after free in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-112733

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:32.390 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112730

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:32.070 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112729

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:31.920 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112728

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:31.770 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112727

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:18:31.577 |

Untrusted pointer dereference in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-112726

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-11-10T19:18:31.397 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112724

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:31.210 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112723

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:30.947 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112722

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-11-10T19:18:30.790 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112721

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-11-10T19:18:30.580 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112719

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:30.160 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112718

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:30.000 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112717

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:29.857 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112716

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:29.710 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112715

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:29.560 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-112714

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:29.403 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111310

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:18:29.253 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111309

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-11-10T19:18:29.113 |

Release of invalid pointer or reference in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-111308

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-11-10T19:18:28.953 |

Numeric truncation error in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111307

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:28.800 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111306

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:28.647 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111305

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:28.500 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-111304

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:28.347 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111301

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:27.890 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-111299

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:27.600 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111298

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:18:27.450 |

Out-of-bounds read in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111295

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:27.023 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111294

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:26.883 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111290

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:26.183 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111289

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:26.003 |

Use after free in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-111285

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:25.267 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-110068

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:25.080 |

Use after free in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-110067

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:24.863 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-110064

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-11-10T19:18:24.287 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-110062

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:24.120 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-110061

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:23.910 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-110060

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:23.767 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-110059

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:23.610 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-110058

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:23.447 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-110055

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:23.003 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-110054

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:22.853 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-110050

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:22.177 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-110048

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:21.810 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-110047

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:21.620 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-110044

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-10T19:18:20.810 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-110043

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:20.547 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-109505

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:18:20.327 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-109503

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:18:19.943 |

Double free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-109502

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-10T19:18:19.773 |

Server-side request forgery (ssrf) in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-109501

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:18:19.610 |

Out-of-bounds read in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-109499

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-10T19:18:18.987 |

Access of resource using incompatible type ('type confusion') in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-109496

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:18.557 |

Heap-based buffer overflow in Microsoft Office Visio allows an unauthorized attacker to execute code over a network.

### CVE-2026-109494

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:18.227 |

Heap-based buffer overflow in Microsoft Office Visio allows an unauthorized attacker to execute code over a network.

### CVE-2026-109493

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:18.060 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-109492

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-10T19:18:17.917 |

Authorization bypass through user-controlled key in Microsoft MCP Gateway allows an authorized attacker to elevate privileges over a network.

### CVE-2026-109472

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-10T19:18:16.043 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-109464

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-10T19:18:15.607 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-109463

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-10T19:18:15.410 |

Deserialization of untrusted data in Windows DNS allows an unauthorized attacker to execute code over a network.

### CVE-2026-108411

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:11.593 |

Heap-based buffer overflow in Windows ODBC Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-108401

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:02.807 |

Heap-based buffer overflow in Windows Remote Desktop Services allows an authorized attacker to execute code over a network.

### CVE-2026-105581

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:18:00.837 |

Stack-based buffer overflow in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-105542

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:17:55.947 |

Untrusted pointer dereference in Windows NTFS allows an unauthorized attacker to execute code over a network.

### CVE-2026-105534

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:54.677 |

Heap-based buffer overflow in Windows Storage allows an unauthorized attacker to execute code over a network.

### CVE-2026-105518

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:17:50.957 |

Use after free in Windows iSCSI allows an unauthorized attacker to execute code over a network.

### CVE-2026-105499

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-11-10T19:17:48.043 |

Out-of-bounds read in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105498

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-11-10T19:17:47.830 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105497

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:47.623 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105496

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:17:47.393 |

Double free in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105495

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:47.213 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105493

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:17:46.910 |

Stack-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105491

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:46.540 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105490

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:17:46.357 |

Stack-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105026

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:43.697 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105023

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:43.077 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105021

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:42.303 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105020

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:42.113 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-57892

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1220` |
| Published | 2026-11-10T18:17:42.210 |

Insufficient granularity of access control in the MigTD v2 policy evaluation engine for the Intel(R) TDX Migration Trust Domain (MigTD) within Ring 0: Hypervisor may allow an escalation of privilege. Network adversary with an unauthenticated user combined with a high complexity attack may enable escalation of privilege. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (none) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (none) impacts.

### CVE-2026-125350

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T18:17:35.237 |

Use after free in XML in Google Chrome prior to 157.0.8103.50 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-125348

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T18:17:34.980 |

Out of bounds write in GPU in Google Chrome prior to 157.0.8103.50 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-125346

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T18:17:34.707 |

Use after free in XML in Google Chrome prior to 157.0.8103.50 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-125344

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-10T18:17:34.443 |

Type confusion in V8 in Google Chrome prior to 157.0.8103.50 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-97891

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-11-10T17:17:57.597 |

In Eclipse Kura version 5.0.0 to 5.6.2, the Web Console allocates a new HTTP session for every request to its built-in authentication endpoints (/admin/auth, /admin/login/password, /admin/login/cert) before checking the HTTP method, parsing the request, or validating any submitted credentials, and does not limit how many such sessions can be allocated. An unauthenticated client that sends requests to these endpoints without honoring the returned session cookie can cause the server to allocate an unbounded number of sessions, exhausting the JVM heap and crashing the Kura process.

### CVE-2026-124251

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-10T17:17:25.060 |

Cross-Site Request Forgery (CSRF) vulnerability in XplodedThemes WPIDE – File Manager & Code Editor wpide allows Cross Site Request Forgery.This issue affects WPIDE – File Manager & Code Editor: from n/a through 3.6.4.

### CVE-2026-11316

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T16:17:17.453 |

A out-of-bounds write vulnerability exists in the dr_wav drwav__read_cue_to_metadata_obj functionality of dr_libs (version(s): 0.14.5). A specially crafted .wav file can lead to an out-of-bounds write. An attacker can provide a malicious file to trigger this vulnerability.

### CVE-2026-126659

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-11T13:17:24.167 |

BlueprintUE Self-Hosted Edition 1.0.0 before 4.3.5 contains a resource exhaustion vulnerability that allows unauthenticated attackers to fill server storage by repeatedly creating anonymous blueprints. Attackers can send large requests to HomeController::doProcessCreateBlueprint() with a 'never' expiration, bypassing purges to fill the disk and deny service.

### CVE-2026-96414

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-649` |
| Published | 2026-11-11T07:17:36.980 |

In affected versions of Octopus Server, insufficient integrity protection of authentication cookies, combined with incorrect validation of permissions assigned to a user that allowed them to view users or audit events, could result in the user escalating their privileges to those of an Administrator.

### CVE-2026-63194

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-11T03:16:52.200 |

OpenMRS module bahmnicore contains Core OpenMRS modules for Bahmni (including ERP & ELIS Atom Feed Clients). In version 0.93, there is insufficient validation of input paths during the admin CSV import process, allowing for potential arbitrary file write. This issue has been patched in version 0.93.1.

### CVE-2026-126543

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-11T01:17:15.727 |

WWBN AVideo through 29.7.1 contains an improper payment verification vulnerability in plugin/PayPalYPT/ipnV2.php that credits wallets from PayPal IPNs not bound to the site's merchant account. Unauthenticated attackers can forward genuine VERIFIED recurring-payment IPNs from their own PayPal account with a chosen users_id to add wallet balance each billing cycle.

### CVE-2026-92545

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-524` |
| Published | 2026-11-10T22:21:15.290 |

The proxy-cache and proxy-cache-advanced plugins in Kong Gateway Enterprise and Kong AI Gateway omit the request hostname from the cache key which may allow a response cached for a hostname to be served for another.

### CVE-2026-125878

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T22:18:30.380 |

Improper neutralization of input during web page generation ('cross-site scripting') vulnerability in N-able N-central allows Resource Injection.

This issue affects N-central: before 26.4.1.

### CVE-2026-122102

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T22:18:28.730 |

Adobe Connect is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a low-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-107356

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-10T22:18:14.577 |

U.S. Geological Survey Area Species Management Research Program (ARMI) accepts any uploaded file and stores the file under '/uploads/{upload-file}'. A remote, authenticated attacker could upload a crafted PHP file that executes and returns command output from the server when accessed. Fixed on 2026-07-20.

### CVE-2026-92544

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T21:21:40.433 |

SQL injection in the LLM usage counters of Kong Gateway Enterprise and Kong AI Gateway may allow a client to execute arbitrary SQL against the Kong database via a crafted model name.

### CVE-2026-120828

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-10T21:19:02.700 |

A replica-set database server node does not limit or reclaim internal wait records created while handling a client-supplied read option that names a point in time the node will never reach. A party with network access and no credentials can cause these records to accumulate without bound and persist after the requests end, which may make the server run out of memory and become unavailable.

### CVE-2026-120824

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T21:19:02.143 |

A use-after-free in the time-series collection component of MongoDB Server can occur when the server validates a time-series bucket document during a write. The condition can be caused by an authenticated user with privileges to write bucket documents directly, and may result in the server terminating unexpectedly or, under certain conditions, arbitrary code execution in the context of the server process.

### CVE-2026-113551

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-657` |
| Published | 2026-11-10T21:18:48.963 |

Audition is affected by a Violation of Secure Design Principles vulnerability that could result in privilege escalation. A low-privileged attacker could leverage this vulnerability to gain elevated access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-105986

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T21:17:52.560 |

Incorrect authorization in the Admin API RBAC of Kong Gateway Enterprise allows a delegated administrator to elevate  privileges via a percent-encoded role name or a self-assigned role.

### CVE-2026-121371

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T20:18:56.640 |

On affected EOS versions with the eAPI service enabled, a specially crafted HTTP request can allow an unauthenticated, remote attacker to read arbitrary files, including sensitive credentials from the switch filesystem.

### CVE-2026-120982

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-440` |
| Published | 2026-11-10T20:18:53.507 |

On affected platforms running Arista EOS with Border Gateway Protocol (BGP) configured, An unauthenticated attacker who can establish a BGP peering session with an affected device and can send specially crafted BGP messages to cause repeated BGP session resets, enabling sustained disruption to network routing and traffic forwarding.

### CVE-2026-70003

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-10T19:21:20.263 |

Improper verification of cryptographic signature in JDBC Driver for SQL Server allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-57891

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T18:17:42.073 |

Out-of-bounds write in the XmlCliCommonDxe for the Intel(R) Server Board D50DNP and Intel(R) Server Board M50FCP within Ring 0 UEFI may allow an escalation of privilege. System software adversary with a privileged user combined with a high complexity attack may enable local code execution. This result may potentially occur via local access when attack requirements are present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (high) impacts.

### CVE-2026-57890

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-460` |
| Published | 2026-11-10T18:17:41.947 |

Improper cleanup on thrown exception in the MigTD's SPDM responder for the Intel(R) TDX Migration Trust Domain (MigTD) within Ring 0: Hypervisor may allow an information disclosure. Network adversary with an unauthenticated user combined with a low complexity attack may enable data exposure. This result may potentially occur via network access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (none) and availability (none) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-57882

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T18:17:41.813 |

Out-of-bounds write in the XmlCliCommonDxe for the Intel(R) Server Board D50DNP and Intel(R) Server Board M50FCP within Ring 0 UEFI may allow an escalation of privilege. Startup code and smm adversary with a privileged user combined with a high complexity attack may enable local code execution. This result may potentially occur via local access when attack requirements are present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (high) impacts.

### CVE-2026-56435

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T18:17:41.370 |

Out-of-bounds write in the XmlCliCommonDxe for the Intel(R) Server Board D50DNP and Intel(R) Server Board M50FCP within Ring 0 UEFI may allow an escalation of privilege. Startup code and smm adversary with a privileged user combined with a high complexity attack may enable local code execution. This result may potentially occur via local access when attack requirements are present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (high) impacts.

### CVE-2026-92684

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T17:17:50.150 |

Missing Authentication for Critical Function in aggregation queries in Neo4j @neo4j/graphql 5.0.0 before 5.12.17 and 7.0.0 before 7.6.8 allows remote attackers to read protected data via GraphQL aggregation queries. Field-level @authentication is not enforced on string aggregates, which can return stored values verbatim, and connection-root aggregates bypass an entity's AGGREGATE authentication requirement, allowing unauthenticated callers to obtain aggregate results.

### CVE-2026-63651

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-10T17:17:46.143 |

LiveDocs is a primary-source-first documentation for AI agents. Prior to version 0.7.0, fetch_docs and introspect (kinds openapi/graphql, and resolve_source's docs_url) pass a client-supplied URL straight to URLSession with no scheme or host allowlist, and redirects are followed unconditionally. A prompt-injection payload embedded in fetched documentation can steer the model to call fetch_docs against internal or metadata endpoints and stream the response back into the conversation. This issue has been patched in version 0.7.0.

### CVE-2026-63010

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-80` |
| Published | 2026-11-10T17:17:45.800 |

Group-Office is an enterprise customer relationship management and groupware tool. Prior to versions 6.8.172, 25.0.108, and 26.0.33, a low-privileged user can create manual reminders containing arbitrary HTML/JavaScript and assign them to any other user (including administrators). When the victim's browser polls for pending notifications, the payload renders unsanitized as innerHTML in the ExtJS notification panel, achieving Stored Cross-Site Scripting (XSS) leading to full Account Takeover (ATO) of the victim's session. This issue has been patched in versions 6.8.172, 25.0.108, and 26.0.33.

### CVE-2026-112186

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674;CWE-696;CWE-770` |
| Published | 2026-11-10T17:17:20.850 |

In Eclipse Kura versions 5.4.0 through 5.6.2, the Service Listing V1 REST API read the JSON body of every request into memory, with no limit on its size. The endpoints parse the body before they check whether the caller is authenticated. A remote attacker without valid credentials can therefore send a few dozen large JSON requests at the same time, exhaust the Java heap with an `OutOfMemoryError`, and cause a denial of service. Likewise, a remote attacker, can send a deeply nested JSON request and trigger a `StackOverflowError` because of an unbound recursion in Service Listing V1.

### CVE-2026-126541

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-11T01:17:15.357 |

WWBN AVideo through 29.7.1 contains a missing authorization vulnerability in Live plugin restream endpoints that allows authenticated streamers to obtain other users' stream keys by supplying arbitrary live_transmitions_history_id values. Attackers can redeem the issued action tokens at verifyTokenForAction.json.php to retrieve victims' HLS URLs and stream keys, then publish as the victim or restream private or pay-per-view lives.

### CVE-2026-125882

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-10T22:18:31.000 |

Relative path traversal vulnerability in N-able N-central allows Path Traversal.

This issue affects N-central: before 26.4.1.

### CVE-2026-125879

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-10T22:18:30.553 |

Incorrect privilege assignment vulnerability in N-able N-central allows Privilege Escalation.

This issue affects N-central: before 26.4.1.

### CVE-2026-120822

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T21:19:01.573 |

MongoDB Server may omit an authorization check on the resource that a replication-related administrative command actually targets, because that check is conditioned on a value taken from the client's own request. A user holding backup and restore privileges may therefore read and relocate collections outside the set that user is permitted to access. This may result in unintended access to data and unintended changes to the collection catalog.

### CVE-2026-113563

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-657` |
| Published | 2026-11-10T21:18:50.270 |

Audition is affected by a Violation of Secure Design Principles vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-113558

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-10T21:18:49.657 |

Audition is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-113557

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-10T21:18:49.487 |

Audition is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-113534

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-10T21:18:45.617 |

After Effects is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-113532

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T21:18:45.177 |

After Effects is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-113526

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-657` |
| Published | 2026-11-10T21:18:44.127 |

After Effects is affected by a Violation of Secure Design Principles vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-120815

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T20:18:52.193 |

An incorrect authorization check in the MongoDB Server authorization subsystem may allow an unauthenticated party with local host access to obtain administrative privileges on a database server that has authorization enabled. This may result in unintended access to stored data and credentials, unintended modification of data, and loss of availability of the server.

### CVE-2026-121662

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-10T19:20:29.580 |

Improper neutralization of special elements used in a command ('command injection') in Visual Studio Code allows an unauthorized attacker to execute code locally.

### CVE-2026-118742

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-10T19:19:51.050 |

Incorrect permission assignment for critical resource in Azure Front Door (AFD) allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-102236

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1021` |
| Published | 2026-11-10T19:17:40.657 |

Improper restriction of rendered ui layers or frames in Visual Studio Code allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-41224

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T18:17:39.080 |

Out-of-bounds write in the UEFI firmware for the Intel(R) Slim Bootloader within Ring 0: Bare Metal OS may allow an escalation of privilege. Startup code and smm adversary with an unauthenticated user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via physical access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (high) impacts.

### CVE-2026-41221

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T18:17:38.937 |

Integer overflow in the UEFI firmware for the Intel(R) Slim Bootloader within Ring 0: Bare Metal OS may allow an escalation of privilege. Startup code and smm adversary with an unauthenticated user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via physical access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (high) impacts.

### CVE-2026-35500

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T18:17:37.693 |

Stack-based buffer overflow in the UEFI firmware for the Intel(R) Slim Bootloader within Ring 0: Bare Metal OS may allow an escalation of privilege. Startup code and smm adversary with an unauthenticated user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via physical access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (high) impacts.

### CVE-2026-112185

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-668;CWE-863` |
| Published | 2026-11-10T17:17:20.693 |

In Eclipse Kura versions 5.1.0 through 5.6.2, the Configuration REST API v2 (org.eclipse.kura.rest.configuration.provider) does not restrict access to the configuration of the UserAdmin persistence component to identities holding the kura.admin permission. An authenticated identity holding only the rest.configuration permission can read the password hashes of all identities, including administrators, which are stored as unsalted SHA-256 digests. The same identity can also modify identities and permission assignments, and restore previous configuration snapshots, which allows escalation to full administrative privileges. The issue is fixed in Eclipse Kura 5.6.3.

### CVE-2026-112191

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-863` |
| Published | 2026-11-10T16:17:16.947 |

In Eclipse Kura versions 5.4.0 through 5.6.2, the Identity REST APIs (identity/v1, and identity/v2 since 5.5.0, provided by org.eclipse.kura.rest.identity.provider) do not check identity and permission management requests against the permissions of the requesting identity. An authenticated identity holding the rest.identity permission, but not kura.admin, can assign any permission to any identity, including kura.admin to itself. It can also change the password of, or delete, identities holding more privileges than its own, including administrators, and create or delete permissions. This allows escalation to full administrative privileges and can lock legitimate administrators out of the device. The issue is fixed in Eclipse Kura 5.6.3.

### CVE-2026-123040

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-11T14:17:32.280 |

An attacker who gains the ability to execute arbitrary code on a system with TrueConf Server (Linux) versions from 4.7.2 up to, but not including, 5.5.6 installed, running as the user trueconf (by exploiting some other vulnerability), can elevate their privileges to root.

### CVE-2026-18769

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-11-11T09:17:15.503 |

A local low privileged attacker can move arbitrary physical memory content via TcRouter.sys because of exposed IOCTL function calls resulting in a full compromise of the affected devices.

### CVE-2026-18768

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-11-11T09:17:15.313 |

A local low privileged attacker can access arbitrary physical memory or define its mapping via TcRouter.sys because of exposed IOCTL function calls resulting in a full compromise of the affected devices.

### CVE-2026-18767

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-11-11T09:17:15.133 |

A local low privileged attacker or process can access I/O ports via TcRouter.sys because of exposed IOCTL function calls resulting in a full compromise of the affected devices.

### CVE-2026-126497

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-11T01:17:14.597 |

LibreCAD through 2.2.1.6 contains a heap-based out-of-bounds write vulnerability in the bundled libdxfrw dwgReader18::parseDataPage() function due to unchecked buffer size and page offsets. Attackers can craft an AC1018 (R2004) DWG file with malicious startOffset values that cause decompress18 to write past the heap buffer when opened, causing crashes and potential code execution.

### CVE-2026-40433

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T18:17:38.240 |

Heap-based buffer overflow for some Intel(R) PROSet Wireless Wi-Fi Software for Windows within Ring 0: Kernel may allow a denial of service. Network adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent network access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (high) and availability (high) impacts.

### CVE-2026-57907

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-10T17:17:44.877 |

A privilege escalation vulnerability in WatchGuard Endpoint Protection's inter-process communication between the console and the protection service allows a local, low-privileged authenticated user to execute arbitrary code with SYSTEM privileges by injecting code into the trusted console process and issuing privileged commands to the service.

### CVE-2026-34016

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-10T17:17:41.880 |

Time-of-check time-of-use race condition for the Intel(R) VTune(TM) Profiler software before version 2026.0.0 within Ring 1: Device Drivers may allow an escalation of privilege. Unprivileged software adversary with an authenticated user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-32670

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-10T17:17:40.830 |

Time-of-check time-of-use race condition for the Intel(R) VTune(TM) Profiler software within Ring 1: Device Drivers may allow an escalation of privilege. Unprivileged software adversary with an authenticated user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-32667

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T17:17:40.700 |

Out-of-bounds write for the Intel(R) VTune(TM) Profiler software within Ring 1: Device Drivers may allow an escalation of privilege. Unprivileged software adversary with an authenticated user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-126050

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T17:17:32.107 |

apitrace 2.0 through 14.0 contains a heap-based buffer overflow in SnappyFile::flushReadCache() that allows attackers to write past m_compressedCache via an oversized compressed chunk length. Attackers can supply a crafted .trace file whose 4-byte chunk length exceeds the fixed buffer size, corrupting heap memory when users dump, inspect, or replay it.

### CVE-2026-125271

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863;CWE-1025` |
| Published | 2026-11-10T17:17:28.497 |

Incorrect normalization of operation names in the custom security policy enforcement in awslabs aws-api-mcp-server before 1.5.1 might allow an actor to execute AWS API operations across AWS services that the operator's security policy was configured to deny or require elicitation for, via calls to operations whose names contain consecutive capital letters.



To remediate this issue, users should upgrade to version 1.5.1.

### CVE-2025-0008

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-10T23:17:18.703 |

Insufficient verification of data authenticity may allow a local attacker to bypass Secure Debug Unlock (SDU), potentially resulting in unauthorized debug access.

### CVE-2026-91000

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T22:21:14.613 |

Missing authentication for critical function vulnerability in N-able N-central allows Privilege Escalation.

This issue affects N-central: before 2026.4.1.

### CVE-2026-40275

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:16.190 |

Heap-based Buffer Overflow in the DCMD_PROC_EVENT handler of the procnto could allow an attacker with local access to cause an information disclosure, data tampering or a crash of the QNX Neutrino kernel.

### CVE-2026-125329

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-11-10T19:21:10.290 |

Kaneo is a project management application with boards, Gantt charts, and GitHub integration that can be self-hosted or used as a cloud service. Prior to 2.13.0, GET /api/external-link/task/:taskId returns integration.config to any workspace member, including the viewer role, when a task has a linked Gitea issue or pull request. The plaintext integration.config contains the Gitea accessToken and webhookSecret, allowing the token's granted Gitea actions and forged webhook deliveries that pass HMAC verification. GitHub integrations and installations without a configured Gitea integration are not affected. This issue is fixed in version 2.13.0.

### CVE-2026-102224

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T19:17:40.010 |

Improper neutralization of special elements used in an os command ('os command injection') in Azure CycleCloud allows an authorized attacker to elevate privileges over a network.

### CVE-2026-62929

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-825` |
| Published | 2026-11-10T18:17:45.130 |

Expired pointer dereference in the MigTD's virtio-vsock implementation for the Intel(R) TDX Migration Trust Domain (MigTD) within Ring 0: Hypervisor may allow an escalation of privilege and information disclosure. System software adversary with a privileged user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-60142

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-123` |
| Published | 2026-11-10T18:17:43.610 |

Write-what-where condition in the MigTD for the Intel(R) TDX Migration Trust Domain (MigTD) within Ring 0: Hypervisor may allow an information disclosure and escalation of privilege. System software adversary with a privileged user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-60138

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-823` |
| Published | 2026-11-10T18:17:43.193 |

Use of out-of-range pointer offset in the MigTD's virtio-vsock implementation for the Intel(R) TDX Migration Trust Domain (MigTD) within Ring 0: Hypervisor may allow an escalation of privilege. System software adversary with a privileged user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-50175

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T18:17:40.550 |

Untrusted pointer dereference in the FirmwareWakingVector for the Intel(R) Slim Bootloader within Ring 0: Bare Metal OS may allow an escalation of privilege. System software adversary with a privileged user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-126499

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-11T01:17:14.963 |

Jellyfin before 12.0 contains a path traversal vulnerability in the DELETE /Library/VirtualFolders and POST /Library/VirtualFolders/Name endpoints that allows attackers to delete or move directories via unvalidated library names. Unauthenticated attackers can supply names like .. or absolute paths before setup completes to recursively delete the data directory and jellyfin.db.

### CVE-2026-92442

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-524` |
| Published | 2026-11-10T22:21:14.987 |

The graphql-proxy-cache-advanced plugin in Kong Gateway Enterprise omits the caller's identity from the cache key, allowing a response cached for one caller to be served to another.

### CVE-2026-77685

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:H` |
| Weaknesses | `CWE-125;CWE-191;CWE-787` |
| Published | 2026-11-10T22:20:53.717 |

The RFCOMM multiplexer control-channel handler in subsys/bluetooth/host/classic/rfcomm.c computed the echo length for a BT_RFCOMM_TEST command as buf->len - 1 and passed it to rfcomm_send_test(), whose length parameter is a uint8_t. A malformed but FCS-valid UIH frame on DLCI 0 can leave buf->len == 0 after rfcomm_handle_msg() pulls the two-byte MCC header, so buf->len - 1 underflows and narrows to 255.

rfcomm_send_test() then copies 255 bytes out of a receive buffer that holds no remaining valid data, and appends them to an outgoing L2CAP PDU allocated with only CONFIG_BT_L2CAP_TX_MTU (253 by default for CONFIG_BT_CLASSIC) bytes of tailroom. The source read runs past the end of the ACL receive buffer into adjacent buffers of the same net_buf pool, and the destination copy overruns the transmit buffer by about eight bytes; net_buf_add_mem() performs no runtime bounds check in ordinary builds, where the underlying __ASSERT_NO_MSG() is compiled out.

The trigger is a single five-byte RFCOMM frame on the multiplexer control channel, which is processed as soon as the L2CAP channel for PSM 3 is established — before any DLC exists and independent of RFCOMM session state. bt_rfcomm_init() registers that L2CAP server with .sec_level = BT_SECURITY_L1, which l2cap_br_conn_security() accepts without any link key from a peer that does not claim host Secure Simple Pairing support, so an unpaired BR/EDR device in radio range of a connectable target with CONFIG_BT_RFCOMM enabled (SPP, HFP, HSP, GOEP and similar profiles all enable it) can reach the defect.

The resulting 255-byte TEST response is transmitted back to the attacker, disclosing roughly 255 bytes of adjacent stack/pool memory — including the contents of neighbouring receive buffers, which an attacker can prime with earlier packets — and the accompanying out-of-bounds write corrupts memory following the transmit buffer, which can crash the Bluetooth host. The request is trivially repeatable, so both the disclosure and the corruption can be driven at will.

Two fixes are needed, and the first on its own does not close the out-of-bounds write. Fix 1 (0040ef781e1d, #115768) strips the FCS byte in rfcomm_recv() and echoes buf->len, rejecting anything over UINT8_MAX, which removes the underflow and the over-read. But rfcomm_make_uih_msg() still allocates the response with bt_l2cap_create_pdu() and never compares the requested length with the buffer's tailroom, so a well-formed TEST command carrying a pattern of about 248 bytes or more still builds a response (3-byte frame header, 2-byte message header, pattern, FCS) larger than the 253 bytes available. A pattern that long can only be received when the RFCOMM L2CAP receive MTU (CONFIG_BT_RFCOMM_L2CAP_MTU, which defaults to CONFIG_BT_BUF_ACL_RX_SIZE) exceeds CONFIG_BT_L2CAP_TX_MTU. The plain BR/EDR defaults (200 against 253) cannot reach it, but from v4.3.0 enabling CONFIG_BT_GOEP raises CONFIG_BT_BUF_ACL_RX_SIZE to 264 (265 from v4.4.0), so GOEP builds with only fix 1 applied still overrun the transmit buffer by up to eight bytes. This includes v4.3.2, the last v4.3 release, which carries fix 1 but will not receive fix 2. Fix 2 (214530895dd3, #118293) checks the tailroom on every RFCOMM PDU allocation and closes this residual write.

### CVE-2026-125880

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-644` |
| Published | 2026-11-10T22:18:30.710 |

Improper neutralization of HTTP headers for scripting syntax vulnerability in N-able N-central allows Cross-Site Scripting (XSS).

This issue affects N-central: before 26.4.1.

### CVE-2026-121900

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T22:18:27.020 |

Adobe Connect is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary SQL commands. Exploitation of this issue does not require user interaction.

### CVE-2026-125337

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-862;CWE-863` |
| Published | 2026-11-10T20:19:08.097 |

Winter CMS is a content management system built on the Laravel PHP framework. Prior to 1.2.14, the ImportExportController behavior applies userHasAccess() only to the import() and export() page actions, while Backend\Classes\Controller::execAjaxHandlers() dispatches onImport(), onImportLoadForm(), onImportLoadColumnSampleForm(), onExport(), and onExportLoadForm() before those gated actions run, and the separately reachable download() action also lacks the granular export check. An authenticated backend user with a valid session and coarse access through $requiredPermissions, but without the configured import[permissions] or export[permissions], can use the import handlers to write or overwrite records and can use onExport() followed by download() to retrieve the complete dataset exposed by the export model. Controllers without granular permission keys are unaffected because userHasAccess() is intentionally default-permissive. This issue is fixed in version 1.2.14.

### CVE-2026-121292

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T20:18:54.743 |

A malformed Error Report can cause EOS to read beyond packet boundaries, potentially terminating the RPKI agent or exposing unintended memory contents through logging.

### CVE-2026-121291

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-696` |
| Published | 2026-11-10T20:18:54.597 |

A crafted Error Report can leave EOS stuck believing that a cache reset is in progress, preventing ROA publication, withdrawal reconciliation, and BGP origin-validation updates.

### CVE-2026-121290

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-420` |
| Published | 2026-11-10T20:18:54.447 |

On affected platforms running Arista EOS with Border Gateway Protocol (BGP) changing the BGP listen port from its default value disables default protective Access Control List (ACL) rules against unexpected BGP peering attempts.

### CVE-2026-121664

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:20:29.957 |

Improper neutralization of input during web page generation ('cross-site scripting') in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-120780

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-10T19:20:27.200 |

Improper access control in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-119985

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:20:23.453 |

Incorrect authorization in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-125343

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T18:17:34.303 |

Buffer overflow in Compositing in Google Chrome prior to 157.0.8103.50 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-50109

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T17:17:44.267 |

Out-of-bounds write for some Intel(R) Performance Counter Monitor (Intel(R) PCM) within Ring 3: User Applications may allow a denial of service. Unprivileged software adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via network access when attack requirements are present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (low) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-125755

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-11-10T16:17:22.767 |

Nodemailer 3.0.0 before 10.4.1 contains an address parsing flaw in addressparser that truncates domains at folding whitespace or comments before a dot, allowing attackers to bypass recipient domain restrictions. Attackers can submit crafted to, cc, bcc or replyTo addresses that pass RFC 5322 domain checks but deliver mail to an attacker-chosen address under the application's sender identity.

### CVE-2026-96437

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636` |
| Published | 2026-11-10T22:21:17.753 |

The ai-azure-content-safety plugin in Kong Gateway Enterprise skips inspection of request bodies larger than the in-memory body buffer, allowing prompts to bypass input content-safety checks.

### CVE-2026-92443

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-524` |
| Published | 2026-11-10T22:21:15.133 |

The caching plugins in Kong Gateway Enterprise and Kong AI Gateway may serve a response cached for a request carrying an Authorization or Proxy-Authorization to different callers.

### CVE-2026-123041

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-524` |
| Published | 2026-11-10T22:18:28.870 |

The request-callout plugin in Kong Gateway Enterprise and Kong AI Gateway omits callout headers not sent by the client from its cache key, allowing a cached callout response for a caller to be served to another.

### CVE-2026-118483

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-10T22:18:24.213 |

Dimension is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-120813

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-11-10T20:18:51.900 |

An issue in MongoDB Server's client-side field-level encryption (CSFLE) schema processing component allows encryption metadata to be silently dropped during schema parsing under certain conditions. A party who can deliver a specially crafted schema to a user's CSFLE client may cause sensitive data intended for encryption to be stored in plaintext, bypassing confidentiality protections. Exploitation requires the ability to deliver the malicious schema to the user's client, such as through a man-in-the-middle position or an untrusted server.

### CVE-2026-120804

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-772` |
| Published | 2026-11-10T20:18:50.593 |

A flaw exists in the server-side SSPI Kerberos authentication handler on Windows Enterprise builds of MongoDB. When processing certain authentication requests, the server fails to properly release an underlying system resource due to an internal tracking error. An unauthenticated user can trigger this by repeatedly sending authentication requests using the Kerberos mechanism, eventually exhausting available resources and causing all subsequent Kerberos authentication attempts to fail. Server restart is required to recover.

### CVE-2026-119989

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-10T19:20:24.137 |

Improper neutralization of special elements used in a command ('command injection') in Azure Pipelines allows an authorized attacker to execute code over a network.

### CVE-2026-113753

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:18:53.547 |

Untrusted pointer dereference in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-56432

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-10T18:17:41.230 |

Unintended proxy or intermediary ('confused deputy') in the MigTD signing for the Intel(R) TDX Migration Trust Domain (MigTD) within Ring 0: Hypervisor may allow an escalation of privilege. System software adversary with a privileged user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (high) and availability (none) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (none) impacts.

### CVE-2026-125756

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-11-10T16:17:22.937 |

postal-mime before 4.2.1 contains a parser differential vulnerability in its address parser that truncates the domain at folding whitespace or comments preceding a dot. Remote attackers can craft From headers that pass SPF/DKIM/DMARC alignment for their own subdomain while PostalMime.parse() reports a spoofed victim sender address.

### CVE-2026-125753

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T16:17:22.307 |

ABP Framework 2.9.0 before 10.6.2 and 10.7.0 pre-releases before 10.7.0 contain a path traversal vulnerability in DefaultBlobFilePathCalculator that allows unauthenticated attackers to access files outside the blob container. Attackers can send %5C-encoded backslashes through the Blogging api/blogging/files/{name} endpoint on Windows hosts to read files like appsettings.json containing signing keys and connection strings.

### CVE-2026-124037

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-359` |
| Published | 2026-11-10T16:17:18.800 |

An information exposure flaw in the public access-list sign-up feature of the Flock Safety Platform, present from 2026-06-23 to 2026-10-22, allowed a remote, unauthenticated attacker who had a community's public sign-up link and a registered vehicle's license plate to retrieve that registrant's name, email address, home address and approval status. Each lookup required solving a CAPTCHA. No license plate reader detections, images or video were exposed. Flock remediated the issue in the hosted service on 2026-10-22; no customer action is required.

### CVE-2026-111190

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-11T08:17:16.887 |

The ARForms plugin for WordPress is vulnerable to arbitrary file upload in all versions up to, and including, 7.2.4 via its form file-upload handler. The name of the stored file is taken from an attacker-controlled request header and is not adequately restricted to safe file types, and the plugin's file-type and content-safety checks can be evaded, allowing files that contain executable PHP code to be written to a publicly accessible directory. This makes it possible for unauthenticated attackers to upload malicious files to the affected site's server, which may make remote code execution possible. Exploitation requires a published form containing a File field to be publicly accessible on the site.

### CVE-2026-111579

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-11T06:17:11.617 |

The Forminator Forms  WordPress plugin before 1.58.4 does not enforce payment on the server side when a form's configured payment gateway is unavailable, allowing unauthenticated visitors to complete a payment-gated User Registration form without paying and be assigned the form's configured role, up to administrator, after the gateway has been connected and later disconnected.

### CVE-2026-109870

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-11T06:17:10.727 |

The User Registration & Membership  WordPress plugin before 5.3.2 does not verify that a discount coupon applied to a paid membership plan is actually valid for that plan before treating a fully discounted order as paid, allowing unauthenticated users to be granted the role mapped to a paid plan without paying for it, which can lead to privilege escalation up to administrator where a plan is mapped to a privileged role.

### CVE-2026-63660

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-11-11T03:16:52.367 |

node-fontnik is a library that delivers a range of glyphs rendered as SDFs (signed distance fields) in a protocol buffer. Prior to version 0.7.7, a crafted font could trigger a heap out-of-bounds write in RenderSDF (include/mapbox/glyph_foundry_impl.hpp). RenderSDF computed the SDF bitmap allocation size as buffered_width * buffered_height in 32-bit unsigned int. Glyph dimensions are derived from the uploaded font's outline bounding box with no upper bound, so a glyph large enough to make that product exceed 2³² wrapped to a small value. The buffer was then under-allocated while the render loop still wrote one byte per pixel, corrupting the heap (CWE-190 → CWE-787) and crashing the process. A 680-byte font is enough to drive FreeType to a 65536×65536 buffered glyph, wrapping the size to 0. This issue has been patched in version 0.7.7.

### CVE-2026-95780

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-10T20:19:48.770 |

A vulnerability exists in the authentication and session-management mechanisms that may result in access not being fully terminated following certain account or session state changes. Under specific conditions, a remote user with prior legitimate access could retain access to protected system resources beyond the intended authorization period. Successful exploitation could result in continued unauthorized access.

### CVE-2025-61625

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T20:17:20.203 |

An improper limitation of a pathname to a restricted directory ('path traversal') vulnerability in Fortinet FortiAnalyzer 7.6.0 through 7.6.4, FortiAnalyzer 7.4.0 through 7.4.7, FortiAnalyzer 7.2.0 through 7.2.11, FortiManager 7.6.0 through 7.6.4, FortiManager 7.4.0 through 7.4.7, FortiManager 7.2.0 through 7.2.11, FortiManager Cloud 7.6.0 through 7.6.4, FortiManager Cloud 7.4.1 through 7.4.7, FortiManager Cloud 7.2.1 through 7.2.10 may allow an authenticated attacker whose profile only has read permission to write and delete files from the underlying filesystem via crafted HTTP or HTTPs requests.

### CVE-2026-96177

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:22:17.970 |

Use after free in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-96092

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:22:07.853 |

Use after free in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-95956

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:49.703 |

Use after free in Windows eSCL Scanner allows an unauthorized attacker to execute code over a network.

### CVE-2026-95885

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:41.857 |

Use after free in Windows Client for NFS allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-81384

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:23.460 |

Heap-based buffer overflow in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-72998

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:21.277 |

Use after free in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-66813

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:21:17.403 |

Out-of-bounds read in SQL Server allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-122979

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T19:20:37.740 |

Improper control of generation of code ('code injection') in Microsoft Teams for Android allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-119967

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:21.573 |

Use after free in Windows Message Queuing Queue Manager allows an unauthorized attacker to execute code over a network.

### CVE-2026-119964

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:20:21.067 |

Double free in Windows Message Queuing allows an unauthorized attacker to execute code over a network.

### CVE-2026-119963

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:20:20.860 |

Double free in Windows Message Queuing allows an unauthorized attacker to execute code over a network.

### CVE-2026-119962

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:20:20.650 |

Double free in Windows Cred SSProvider Protocol allows an unauthorized attacker to execute code over a network.

### CVE-2026-119961

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:20:20.437 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Internet Information Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-119952

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-208` |
| Published | 2026-11-10T19:20:18.867 |

Observable timing discrepancy in Windows Schannel allows an unauthorized attacker to execute code over a network.

### CVE-2026-119951

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:18.687 |

Use after free in Windows Deployment Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-119945

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:20:17.600 |

Use after free in Windows Modern Device Management (MDM) allows an unauthorized attacker to execute code over a network.

### CVE-2026-118741

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-10T19:19:50.893 |

Improper authentication in ASP.NET Core allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-118737

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-10T19:19:50.377 |

Improper verification of cryptographic signature in Windows Remote Procedure Call Runtime allows an unauthorized attacker to execute code over a network.

### CVE-2026-118106

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:28.820 |

Heap-based buffer overflow in SQL Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-116710

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:13.230 |

Heap-based buffer overflow in Windows Message Queuing allows an unauthorized attacker to execute code over a network.

### CVE-2026-113862

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:06.993 |

Use after free in Windows Network Address Translation (NAT) allows an unauthorized attacker to execute code over a network.

### CVE-2026-109459

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:14.953 |

Heap-based buffer overflow in Windows Message Queuing Queue Manager allows an unauthorized attacker to execute code over a network.

### CVE-2026-102219

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-326` |
| Published | 2026-11-10T19:17:39.797 |

Inadequate encryption strength in Windows Modern Device Management (MDM) allows an unauthorized attacker to execute code over a network.

### CVE-2026-108187

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-10T16:17:14.330 |

Origin Validation Error in Zoom Workplace for Windows may allow an unauthenticated user to conduct an escalation of privilege via network access.

### CVE-2026-96115

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-415` |
| Published | 2026-11-10T19:22:09.303 |

Double free in Windows DHCP Client allows an authorized attacker to elevate privileges over an adjacent network.

### CVE-2026-94513

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:36.950 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-88240

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:33.217 |

Heap-based buffer overflow in Windows DHCP Client allows an authorized attacker to elevate privileges over an adjacent network.

### CVE-2026-88187

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:27.017 |

Heap-based buffer overflow in Windows Bluetooth A2DP driver allows an authorized attacker to elevate privileges over an adjacent network.

### CVE-2026-123387

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-10T19:20:42.213 |

Improper neutralization of special elements used in a command ('command injection') in Windows Active Directory allows an authorized attacker to elevate privileges over a network.

### CVE-2026-122988

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T19:20:38.523 |

Improper authorization in Windows Admin Center allows an authorized attacker to elevate privileges over a network.

### CVE-2026-122164

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-10T19:20:33.153 |

Weak authentication in Windows Kerberos allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118119

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T19:19:30.737 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118118

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T19:19:30.587 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118117

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T19:19:30.430 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118113

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T19:19:29.730 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118112

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T19:19:29.577 |

Improper control of generation of code ('code injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118111

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-10T19:19:29.427 |

Origin validation error in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-111297

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:18:27.297 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-111296

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-10T19:18:27.160 |

Server-side request forgery (ssrf) in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-109466

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T19:18:15.750 |

Missing authorization in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over an adjacent network.

### CVE-2026-109457

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T19:18:14.803 |

Improper neutralization of special elements used in an os command ('os command injection') in Azure CLI allows an authorized attacker to execute code over a network.

### CVE-2026-126612

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-11T09:17:13.110 |

Improper link resolution in the Windows installer of Progressive Robot hMailServer 6.0.0 through 6.3.7 allows a local authenticated user to run code as the mail server's service account or as an administrator when the path to the program folder passes through a junction, a symbolic link or a mount point that the user controls or that every user may change, such as a junction made at the root of a drive, which takes the root's permissions, or through a folder that every user may rename. Setup installed the programs through any such link without first checking who controls it, or whether a folder above the program folder may be renamed, and the service is registered to run the programs by that path, so the programs are installed where a link another account controls leads, or that account can later make the path lead to a folder it controls; the service, which runs as LocalSystem or as its virtual account, and the programs administrators run from Bin are then started from there. 6.3.7's fix for CVE-2026-107571 does not cover this: its hardening of the program folder, Bin and ControlPanel does not change a folder reached through a link that the administrators do not alone control, and setup does not refuse such a path: it installs through the link and at most reports afterwards that the folders could not be hardened. The default installation under Program Files is not affected.

### CVE-2026-126607

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-11T09:17:11.410 |

Progressive Robot hMailServer 6.2.3 through 6.3.7 on Windows, with a MySQL or MariaDB database, hands the bundled MariaDB Connector/C the folder of its authentication plugins (the plugin folder in the installation's Bin folder) as Latin-1 bytes, which the client reads in the system's ANSI code page when it builds a plugin's path and loads the plugin with LoadLibraryExA, which allows a local authenticated user to execute code as the hMailServer service's account (LocalSystem, or the service's virtual account for a new installation from 6.3.4) by creating the folder those bytes name in the code page and placing in it a DLL with a plugin's name, when the installation folder's path holds a character between U+0080 and U+00FF whose byte the code page reads as another character, and none above U+00FF, and the user can create that other folder (by default any authenticated user may create a folder directly under the root of the system drive). The server converted the path with the C runtime's wcstombs_s in the C locale, which writes each character up to U+00FF as the byte of the same value: on code page 1252 those bytes are the same letters, while on another code page, such as 1251, or on a UTF-8 code page, they name another folder. The client loads the plugin the database server names in its greeting, unless it is built in, and any plugin the server names in an authentication switch, and tries again at each connection while a load fails, so with a MySQL 8.0 or later server, whose greeting names caching_sha2_password by default, the DLL is loaded at the next connection the service makes, whatever plugin the database account uses; a DLL's entry point runs when it is loaded. A path holding any character above U+00FF was handed over as an empty string, whatever the code page, from which the client makes a plugin's name at the root of the current drive: for the service, whose current folder is System32, that is the root of the system drive, where by default only administrators can create a file, but the server's own database commands (hMailServer.exe --check-database, --upgrade-database and the others from 6.3.4, and the /Debug and /Test console modes from 6.2.3) run in the folder they are started from - the product tells administrators to run them from an elevated prompt in the Bin folder, and the setup of 6.3.4 and 6.3.5 ran two or three of them itself with the Bin folder as their working folder for a new installation with an external database - so a DLL that a local authenticated user placed under a plugin's name at the root of a drive other users may write, such as a FAT or exFAT volume, was loaded into the administrator's process at the command's first connection to a MySQL 8.0 or later server. 6.3.8 fixes both cases: it hands the folder in the code page's bytes or by its short (8.3) name, and where neither can be written, a folder under the Windows system folder that holds no plugin and that only administrators can create, or else refuses the connection before attempting it; it never hands the empty value or a folder the current drive completes. The configuration is not the default: the default installation folder, under Program Files, is ASCII. Linux builds set no plugin folder and are not affected.

### CVE-2026-92441

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-10T22:21:14.867 |

Kong Gateway Enterprise and Kong AI Gateway include decoded CR/LF characters from the request path in the X-Forwarded-Prefix header on regex Routes, allowing HTTP header injection and request smuggling to the upstream.

### CVE-2026-92439

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-10T22:21:14.740 |

The SAML plugin in Kong Gateway Enterprise does not enforce AudienceRestriction, allowing a valid assertion issued for another Service Provider to be replayed to authenticate to Kong.

### CVE-2026-90833

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T22:21:14.320 |

The simulated EEPROM driver validated access ranges in eeprom_range_is_valid() (drivers/eeprom/eeprom_simulator.c) with a single test, (offset + len) <= config->size. Because offset is a signed off_t and len an unsigned size_t of the same rank, the addition is evaluated in unsigned arithmetic: a negative offset combined with a compensating len wraps the sum back into the accepted range. eeprom_sim_read() and eeprom_sim_write() then memcpy() through the EEPROM(addr) macro, which is plain pointer arithmetic on the driver's static mock_eeprom array, so the copy addresses memory located before that array.

eeprom_read() and eeprom_write() are __syscall entry points, and their verification handlers in drivers/eeprom/eeprom_handlers.c check only the device object and the caller's own data buffer (K_SYSCALL_MEMORY_READ/K_SYSCALL_MEMORY_WRITE) — the offset argument is passed to the driver unvalidated. With CONFIG_USERSPACE=y, a CONFIG_EEPROM_SIMULATOR device instance, and the device object granted to a user thread (the usage the in-tree tests/drivers/eeprom/api suite exercises from ZTEST_USER threads), an unprivileged thread could supply a negative offset and have the kernel perform the copy on its behalf.

The result is an out-of-bounds read of kernel .bss returned into the caller's buffer and, via the write path, an out-of-bounds write of caller-supplied bytes over kernel memory preceding mock_eeprom. Both the start address and the length of the affected span are attacker-selected, so the primitive is sufficient to corrupt adjacent kernel state and escape the user-mode sandbox. Exposure is limited to builds that instantiate the simulated EEPROM (status = "okay" by default on qemu_x86 and native_sim, otherwise added by a devicetree overlay) together with userspace isolation.

The fix rejects negative offsets and performs the remaining bound check without overflow.

### CVE-2026-82012

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:20:12.097 |

Premiere Pro is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48402

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-10T21:19:30.600 |

Premiere Pro is affected by an Untrusted Search Path vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-123263

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T21:19:04.617 |

After Effects is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-117547

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:57.570 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-117546

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T21:18:57.393 |

Photoshop Desktop is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-116480

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T21:18:57.117 |

Photoshop Desktop is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-116003

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:56.917 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113575

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T21:18:51.073 |

Photoshop Desktop is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113567

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:50.580 |

Audition is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113565

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:50.423 |

Audition is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113555

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:49.320 |

Audition is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113553

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:49.157 |

Audition is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113547

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:48.630 |

Media Encoder is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113545

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:48.353 |

Media Encoder is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113543

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:47.923 |

Media Encoder is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113541

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:47.463 |

Media Encoder is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113538

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:46.520 |

After Effects is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113536

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:46.027 |

After Effects is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113530

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:44.900 |

After Effects is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113528

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:44.537 |

After Effects is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113525

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:43.993 |

After Effects is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113523

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:43.840 |

After Effects is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113517

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:43.350 |

After Effects is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113516

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:43.033 |

After Effects is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113512

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T21:18:42.757 |

After Effects is affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-110089

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-124` |
| Published | 2026-11-10T21:18:20.067 |

Premiere Pro is affected by a Buffer Underwrite ('Buffer Underflow') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-110088

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-10T21:18:19.900 |

Premiere Pro is affected by a Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-110086

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:19.637 |

Premiere Pro is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-110085

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:18:19.507 |

Premiere Pro is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-104352

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T21:17:39.163 |

Premiere Pro is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-97013

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-10T19:22:23.497 |

Access of resource using incompatible type ('type confusion') in Windows Shell allows an authorized attacker to elevate privileges locally.

### CVE-2026-96845

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T19:22:18.590 |

Improper authorization in Windows Task Scheduler allows an authorized attacker to elevate privileges locally.

### CVE-2026-96184

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:18.273 |

Heap-based buffer overflow in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-96175

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-11-10T19:22:17.627 |

Release of invalid pointer or reference in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-96174

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-11-10T19:22:17.467 |

Release of invalid pointer or reference in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-96172

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-11-10T19:22:17.283 |

No cwe for this issue in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-96162

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:22:13.590 |

Incorrect authorization in Windows Clipboard Virtual Channel Extension allows an authorized attacker to elevate privileges locally.

### CVE-2026-96160

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:22:13.407 |

Out-of-bounds read in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96152

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-681` |
| Published | 2026-11-10T19:22:12.257 |

Stack-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96129

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-10T19:22:10.363 |

Inclusion of functionality from untrusted control sphere in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96127

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:10.190 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96126

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:10.000 |

Heap-based buffer overflow in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96122

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:22:09.627 |

Untrusted pointer dereference in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96117

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:09.447 |

Heap-based buffer overflow in Windows LUAFV allows an authorized attacker to elevate privileges locally.

### CVE-2026-96103

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:08.670 |

Heap-based buffer overflow in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-96102

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:08.480 |

Heap-based buffer overflow in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-96085

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:07.320 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96084

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:06.890 |

Heap-based buffer overflow in Graphic Fonts allows an authorized attacker to elevate privileges locally.

### CVE-2026-96076

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:22:05.783 |

Use after free in Windows DIAL Client allows an authorized attacker to elevate privileges locally.

### CVE-2026-96074

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:05.363 |

Heap-based buffer overflow in Windows AppX Package Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-96066

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:22:04.590 |

Stack-based buffer overflow in Windows Local Security Authority Subsystem Service (LSASS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-96062

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-822` |
| Published | 2026-11-10T19:22:04.277 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96060

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:22:03.910 |

Out-of-bounds read in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96057

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:03.343 |

Heap-based buffer overflow in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96056

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:03.153 |

Heap-based buffer overflow in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96055

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:02.953 |

Heap-based buffer overflow in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96053

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-10T19:22:02.527 |

Improper neutralization of special elements used in a command ('command injection') in Windows Task Scheduler allows an authorized attacker to elevate privileges locally.

### CVE-2026-96052

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-10T19:22:02.370 |

Integer underflow (wrap or wraparound) in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96038

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822;CWE-829` |
| Published | 2026-11-10T19:22:00.697 |

Inclusion of functionality from untrusted control sphere in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96037

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:00.500 |

Heap-based buffer overflow in Windows User Manager Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96036

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:22:00.290 |

Integer overflow or wraparound in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96031

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T19:21:59.913 |

Out-of-bounds write in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96029

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T19:21:59.730 |

Improper access control in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96028

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822;CWE-843` |
| Published | 2026-11-10T19:21:59.533 |

Access of resource using incompatible type ('type confusion') in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96023

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:58.973 |

Use after free in Windows Push Notification Core allows an authorized attacker to elevate privileges locally.

### CVE-2026-96016

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:57.993 |

Heap-based buffer overflow in Windows Local Security Authority Subsystem Service (LSASS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-96005

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:57.197 |

Heap-based buffer overflow in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-95999

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:21:56.483 |

Out-of-bounds read in Windows USB Hub Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-95997

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:56.143 |

Use after free in Windows Event Logging Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-95991

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:55.717 |

Use after free in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95988

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:21:55.347 |

Incorrect authorization in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95983

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:21:54.890 |

Untrusted pointer dereference in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95965

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:53.053 |

Heap-based buffer overflow in Windows USB Video Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-95963

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-10T19:21:52.677 |

Improper link resolution before file access ('link following') in Data Sharing Service Client allows an authorized attacker to elevate privileges locally.

### CVE-2026-95953

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:21:49.290 |

Out-of-bounds read in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95951

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:47.790 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-95948

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:21:47.290 |

Stack-based buffer overflow in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95947

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T19:21:47.107 |

An elevation of privilege vulnerability exists in Windows Error Reporting (WER) when WER handles and executes files. The vulnerability could allow elevation of privilege if an attacker can successfully exploit it.
An attacker who successfully exploited the vulnerability could gain greater access to sensitive information and system functionality. To exploit the vulnerability, an attacker could run a specially crafted application.
The security update addresses the vulnerability by correcting the way that WER handles and executes files.

### CVE-2026-95942

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:21:46.600 |

Out-of-bounds read in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95935

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T19:21:46.217 |

Integer overflow or wraparound in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95934

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:21:46.043 |

Double free in Windows Diagnostic Policy Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-95933

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:45.863 |

Heap-based buffer overflow in Windows OLE allows an authorized attacker to elevate privileges locally.

### CVE-2026-95932

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-10T19:21:45.663 |

Inclusion of functionality from untrusted control sphere in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95920

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:45.080 |

Heap-based buffer overflow in Windows Management Instrumentation allows an authorized attacker to elevate privileges locally.

### CVE-2026-95909

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:21:44.427 |

Out-of-bounds read in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95902

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:43.700 |

Heap-based buffer overflow in Windows USB Hub Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-95898

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:43.327 |

Heap-based buffer overflow in Windows iSCSI allows an authorized attacker to elevate privileges locally.

### CVE-2026-95896

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:43.140 |

Heap-based buffer overflow in Windows Microsoft DirectMusic allows an authorized attacker to execute code locally.

### CVE-2026-95895

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:42.973 |

Use after free in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95894

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:42.790 |

Heap-based buffer overflow in Windows Task Scheduler allows an authorized attacker to elevate privileges locally.

### CVE-2026-95891

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:21:42.427 |

Heap-based buffer overflow in Windows Microsoft DirectMusic allows an authorized attacker to execute code locally.

### CVE-2026-95881

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:41.347 |

Heap-based buffer overflow in Windows Push Notifications allows an authorized attacker to elevate privileges locally.

### CVE-2026-95879

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:21:40.997 |

Out-of-bounds read in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95877

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:40.793 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-95874

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:40.380 |

Heap-based buffer overflow in Xbox allows an authorized attacker to elevate privileges locally.

### CVE-2026-95872

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:40.190 |

Heap-based buffer overflow in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-94531

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:21:38.960 |

Stack-based buffer overflow in Windows COM allows an authorized attacker to elevate privileges locally.

### CVE-2026-94527

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:21:38.440 |

Heap-based buffer overflow in Windows GDI allows an authorized attacker to elevate privileges locally.

### CVE-2026-94515

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:37.420 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-94507

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:36.543 |

Heap-based buffer overflow in Windows DirectX allows an authorized attacker to elevate privileges locally.

### CVE-2026-88245

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T19:21:34.123 |

Missing authentication for critical function in Windows Brokering File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-88241

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:33.410 |

Heap-based buffer overflow in Windows Sensor Data Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-88239

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:33.043 |

Heap-based buffer overflow in Windows Biometric Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-88238

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:32.883 |

Heap-based buffer overflow in Windows Camera Frame Server Monitor allows an authorized attacker to elevate privileges locally.

### CVE-2026-88235

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-10T19:21:32.397 |

Unintended proxy or intermediary ('confused deputy') in Servicing Stack Updates allows an authorized attacker to elevate privileges locally.

### CVE-2026-88233

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-283` |
| Published | 2026-11-10T19:21:32.063 |

Improper authorization in Windows Task Scheduler allows an authorized attacker to elevate privileges locally.

### CVE-2026-88232

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:31.910 |

Use after free in Windows Camera Frame Server Monitor allows an authorized attacker to elevate privileges locally.

### CVE-2026-88230

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:31.540 |

Heap-based buffer overflow in Windows LUAFV allows an authorized attacker to elevate privileges locally.

### CVE-2026-88227

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:21:30.957 |

Heap-based buffer overflow in Windows Local Security Authority Subsystem Service (LSASS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-88213

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-11-10T19:21:27.813 |

Numeric truncation error in Windows Bluetooth Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85942

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:26.520 |

Heap-based buffer overflow in Windows Camera Frame Server Monitor allows an authorized attacker to elevate privileges locally.

### CVE-2026-85929

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-10T19:21:26.380 |

Incorrect permission assignment for critical resource in Windows Brokering File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-85801

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:25.060 |

Use after free in Windows Local Security Authority Subsystem Service (LSASS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-83563

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:23.613 |

Heap-based buffer overflow in Winlogon allows an authorized attacker to elevate privileges locally.

### CVE-2026-70182

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-10T19:21:20.750 |

Weak authentication in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-125137

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:07.527 |

Heap-based buffer overflow in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-124225

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T19:20:48.837 |

Improper control of generation of code ('code injection') in Windows PowerShell allows an unauthorized attacker to execute code locally.

### CVE-2026-123388

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-170` |
| Published | 2026-11-10T19:20:42.420 |

Heap-based buffer overflow in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-122986

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-10T19:20:38.233 |

Improper privilege management in Microsoft Azure Kubernetes Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-122984

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:37.880 |

Heap-based buffer overflow in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-122183

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:20:36.253 |

Out-of-bounds read in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-122172

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:20:34.753 |

Use after free in Microsoft Trace Data Helper allows an authorized attacker to elevate privileges locally.

### CVE-2026-122168

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:33.967 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an authorized attacker to elevate privileges locally.

### CVE-2026-122166

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:20:33.533 |

Stack-based buffer overflow in Windows Remote Desktop Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-122165

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:33.340 |

Heap-based buffer overflow in Windows Client for NFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-121681

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:32.040 |

Heap-based buffer overflow in Microsoft Trace Data Helper allows an authorized attacker to elevate privileges locally.

### CVE-2026-121673

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:30.993 |

Use after free in Windows Filter Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-121661

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-10T19:20:29.430 |

Incomplete list of disallowed inputs in Visual Studio Code allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-120782

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-863` |
| Published | 2026-11-10T19:20:27.370 |

Improper control of generation of code ('code injection') in Visual Studio Code allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-119997

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:25.307 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code locally.

### CVE-2026-119987

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-10T19:20:23.767 |

Untrusted search path in Microsoft Windows App Store allows an authorized attacker to elevate privileges locally.

### CVE-2026-119957

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:20:19.687 |

Double free in Windows Remote Desktop Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-119954

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-36;CWE-306` |
| Published | 2026-11-10T19:20:19.257 |

Absolute path traversal in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-119953

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:19.057 |

Use after free in Windows DNS allows an authorized attacker to elevate privileges locally.

### CVE-2026-119943

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-11-10T19:20:17.247 |

Buffer over-read in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-119941

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:20:16.850 |

Untrusted pointer dereference in Windows Volume Shadow Copy allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-119939

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-10T19:20:16.447 |

Improper privilege management in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-119933

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-11-10T19:20:15.283 |

Use of uninitialized resource in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-119929

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:14.683 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-119917

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:13.403 |

Heap-based buffer overflow in Windows Distributed Transaction Coordinator allows an authorized attacker to elevate privileges locally.

### CVE-2026-119907

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:20:11.420 |

Untrusted pointer dereference in Windows Function Discovery Resource Publication allows an authorized attacker to elevate privileges locally.

### CVE-2026-119906

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T19:20:11.280 |

Improper neutralization of special elements used in an os command ('os command injection') in Windows Sandbox allows an authorized attacker to elevate privileges locally.

### CVE-2026-119904

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-10T19:20:10.923 |

Improper control of generation of code ('code injection') in Microsoft Windows Speech allows an authorized attacker to elevate privileges locally.

### CVE-2026-119903

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T19:20:10.713 |

Improper access control in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-119899

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T19:20:10.163 |

Improper access control in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-119892

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:20:09.377 |

Incorrect authorization in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-119886

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T19:20:08.410 |

Missing authentication for critical function in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119853

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-10T19:20:02.987 |

Untrusted search path in Windows Remote Access API allows an authorized attacker to elevate privileges locally.

### CVE-2026-119847

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:01.867 |

Heap-based buffer overflow in Windows Kerberos allows an authorized attacker to elevate privileges locally.

### CVE-2026-119846

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:20:01.687 |

Out-of-bounds read in Windows Subsystem for Linux allows an authorized attacker to elevate privileges locally.

### CVE-2026-119834

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:59.043 |

Heap-based buffer overflow in Windows Subsystem for Linux allows an authorized attacker to elevate privileges locally.

### CVE-2026-119826

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:57.743 |

Use after free in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-119821

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-10T19:19:56.707 |

Improper authorization in Windows Network Connection Broker allows an authorized attacker to elevate privileges locally.

### CVE-2026-119818

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:19:56.523 |

Incorrect authorization in Windows Text Services Framework allows an authorized attacker to elevate privileges locally.

### CVE-2026-119817

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:19:56.330 |

Double free in Windows Shell allows an authorized attacker to elevate privileges locally.

### CVE-2026-119816

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:56.137 |

Heap-based buffer overflow in Windows Microsoft Account Sign-in Assistant allows an authorized attacker to elevate privileges locally.

### CVE-2026-119393

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:53.880 |

Stack-based buffer overflow in Windows Credential Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-119391

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:53.537 |

Use after free in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-119390

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:53.330 |

Heap-based buffer overflow in Remote Desktop Client allows an authorized attacker to execute code locally.

### CVE-2026-119382

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:52.070 |

Heap-based buffer overflow in Windows TPM allows an authorized attacker to elevate privileges locally.

### CVE-2026-118723

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:19:48.420 |

Untrusted pointer dereference in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-118280

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:19:41.923 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118224

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:40.160 |

Use after free in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118223

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:39.963 |

Use after free in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118222

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:39.780 |

Heap-based buffer overflow in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118220

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-415` |
| Published | 2026-11-10T19:19:39.373 |

Double free in Windows Multiple Provider Router allows an authorized attacker to elevate privileges locally.

### CVE-2026-118215

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:38.400 |

Use after free in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-118142

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:19:34.110 |

Out-of-bounds read in Windows Distributed File System (DFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-118138

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-822` |
| Published | 2026-11-10T19:19:32.317 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Client for NFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-118137

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T19:19:32.120 |

Improper authorization in Windows FTP Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-118126

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:31.647 |

Use after free in Windows Message Queuing allows an authorized attacker to elevate privileges locally.

### CVE-2026-116714

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:19:13.820 |

Incorrect authorization in Windows AppX Deployment Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-114170

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:10.690 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-114167

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:10.397 |

Heap-based buffer overflow in Microsoft Windows Codecs Library allows an unauthorized attacker to execute code locally.

### CVE-2026-114165

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:10.107 |

Heap-based buffer overflow in Microsoft Windows Codecs Library allows an unauthorized attacker to execute code locally.

### CVE-2026-114161

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T19:19:09.667 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Azure CycleCloud allows an authorized attacker to elevate privileges locally.

### CVE-2026-113865

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-10T19:19:07.527 |

Time-of-check time-of-use (toctou) race condition in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-113856

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:06.327 |

Heap-based buffer overflow in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-113848

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-10T19:19:05.977 |

Null pointer dereference in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-113847

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:19:05.793 |

Integer overflow or wraparound in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-113843

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-10T19:19:05.373 |

Improper authentication in Windows Remote Access Connection Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-113767

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822;CWE-829` |
| Published | 2026-11-10T19:18:56.090 |

Inclusion of functionality from untrusted control sphere in Windows COM+ Event System Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-113765

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:18:55.783 |

Heap-based buffer overflow in Windows File Server Resource Management Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-113759

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:54.663 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-113758

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:18:54.460 |

Out-of-bounds read in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-113748

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:18:52.587 |

Stack-based buffer overflow in Software Protection Platform (SPP) allows an authorized attacker to elevate privileges locally.

### CVE-2026-112981

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-11-10T19:18:50.220 |

Heap-based buffer overflow in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-112978

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:49.633 |

Use after free in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-112811

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-822` |
| Published | 2026-11-10T19:18:45.770 |

Stack-based buffer overflow in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-112802

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T19:18:42.667 |

Missing authorization in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-112801

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-10T19:18:42.500 |

Insufficiently protected credentials in Windows eSCL Scanner allows an authorized attacker to elevate privileges locally.

### CVE-2026-112799

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:18:42.170 |

Stack-based buffer overflow in Windows Projected File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-112794

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:41.210 |

Heap-based buffer overflow in Windows Smart Card allows an authorized attacker to elevate privileges locally.

### CVE-2026-112760

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T19:18:38.790 |

Integer overflow or wraparound in Windows Overlay Filter allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-112758

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:18:37.400 |

Double free in Windows Defender Firewall Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-112752

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-10T19:18:35.690 |

Improper access control in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-112751

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:35.440 |

Use after free in Windows Remote Assistance allows an authorized attacker to elevate privileges locally.

### CVE-2026-112743

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:18:34.150 |

Untrusted pointer dereference in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-111302

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:28.037 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-110056

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:23.153 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-110049

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:21.993 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-109473

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:16.423 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-108412

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:11.797 |

Heap-based buffer overflow in Windows Redirected Drive Buffering allows an authorized attacker to elevate privileges locally.

### CVE-2026-108407

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:18:09.897 |

Out-of-bounds read in Windows GDI allows an authorized attacker to elevate privileges locally.

### CVE-2026-108405

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T19:18:09.120 |

Integer overflow or wraparound in Windows CD-ROM Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-108403

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:07.460 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-105580

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:00.650 |

Heap-based buffer overflow in Windows Management Instrumentation allows an unauthorized attacker to execute code locally.

### CVE-2026-105575

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-10T19:18:00.113 |

Access of resource using incompatible type ('type confusion') in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-105569

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:17:59.780 |

Out-of-bounds read in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-105543

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-10T19:17:56.130 |

Null pointer dereference in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-105541

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-823` |
| Published | 2026-11-10T19:17:55.770 |

Use of out-of-range pointer offset in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-105532

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-10T19:17:53.513 |

Improper link resolution before file access ('link following') in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-105528

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:52.357 |

Heap-based buffer overflow in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-105524

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-10T19:17:51.487 |

Weak authentication in Windows Management Instrumentation allows an authorized attacker to elevate privileges locally.

### CVE-2026-105507

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:49.410 |

An elevation of privilege vulnerability exists in the Windows Installer when the Windows Installer fails to properly sanitize input leading to an insecure library loading behavior.
A locally authenticated attacker could run arbitrary code with elevated system privileges. An attacker could then install programs; view, change, or delete data; or create new accounts with full user rights.
The security update addresses the vulnerability by correcting the input sanitization error to preclude unintended elevation.

### CVE-2026-105505

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-10T19:17:48.913 |

Relative path traversal in Microsoft Input Method Editor (IME) allows an authorized attacker to elevate privileges locally.

### CVE-2026-105503

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:48.453 |

Heap-based buffer overflow in Windows Management Instrumentation allows an authorized attacker to elevate privileges locally.

### CVE-2026-105501

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:17:48.250 |

Incorrect authorization in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-105494

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-10T19:17:47.080 |

Untrusted search path in Azure NFS mount helper (aznfs) allows an authorized attacker to elevate privileges locally.

### CVE-2026-105028

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:17:44.527 |

Out-of-bounds read in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-105025

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:17:43.493 |

Double free in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-105022

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:17:42.640 |

Use after free in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-100223

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:17:39.327 |

An elevation of privilege vulnerability exists when reparse points are created by sandboxed processes allowing sandbox escape. An attacker who successfully exploited the vulnerability could use the sandbox escape to elevate privileges on an affected system.
To exploit the vulnerability, an attacker would first have to log on to the system, and then run a specially crafted application to take control over the affected system.
The security update addresses the vulnerability by preventing sandboxed processes from creating reparse points targeting inaccessible files.

### CVE-2026-125323

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-1188` |
| Published | 2026-11-10T18:17:33.703 |

pgEdge Control Plane is a distributed application for managing and orchestrating Postgres databases across multiple hosts. From 0.1.0 to 0.10.1, generated pg_hba.conf files began with hard-coded trust entries for Unix-socket and loopback connections. Because PostgreSQL evaluates the file from top to bottom, those entries also preempted operator-supplied rules in the pg_hba_conf field. Under the systemd orchestrator, any unprivileged operating-system account on a database host could authenticate as any PostgreSQL role, including the superuser, without credentials and obtain full control of the host's databases. Under Docker Swarm, reaching the container-local socket or loopback interface required code execution inside the database container. Publishing the PostgreSQL port to the host did not expose these trust rules because host connections did not appear to originate from 127.0.0.1 or ::1. This issue is fixed in version 0.11.0.

### CVE-2026-105153

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-11T13:17:12.957 |

Improper Restriction of XML External Entity Reference in Apache Roller 4.0 through 6.1.6 allows an authenticated user with no weblog permissions to read files readable by the Roller process and cause the server to issue outbound HTTP requests to attacker-chosen destinations, by submitting a crafted Atom entry to the AtomPub endpoint. The entry body is parsed with a parser configuration that permits external parameter entities and external DTD subsets, and the parse happens before any per-weblog authorization check and before any check of whether the AtomPub feature is enabled, so the endpoint is reachable by any authenticated account on a default installation. Users are recommended to upgrade to Apache Roller 6.1.7 or later, which parses AtomPub entries with a hardened XML configuration and rejects AtomPub requests while the feature is disabled.

### CVE-2026-105948

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T08:17:16.740 |

In affected versions of Octopus Server, incorrect validation of permissions assigned to a user that would allow them to edit their own login identities could result in that user being granted elevated permissions, up to and including system administrator access. This issue affects instances using LDAP authentication with self-service login editing enabled.

### CVE-2026-121890

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-10T22:18:26.350 |

Adobe Connect is affected by an Improper Restriction of XML External Entity Reference ('XXE') vulnerability that could lead to arbitrary file system read. A low-privileged attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121350

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T22:18:24.777 |

Adobe Connect is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could lead to disclosure of sensitive memory. A low-privileged attacker could leverage this vulnerability to disclose sensitive information. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-82002

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T21:20:11.960 |

Media Encoder is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-113562

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-10T21:18:49.980 |

Audition is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-113560

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T21:18:49.823 |

Audition is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-50077

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T20:19:12.123 |

Invalid Memory Access via the MSI-X table in QVM could allow an attacker in the guest to execute arbitrary code in the QVM to cause memory corruption, information disclosure or a crash of the QVM.

### CVE-2026-121287

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-124` |
| Published | 2026-11-10T20:18:53.950 |

An unauthenticated attacker on an adjacent network segment can send crafted RIPv2 packets to a RIP-enabled interface on the device to trigger the Rip agent crash without providing valid credentials. Repeated exploitation reliably interrupts routing service on the affected device, which may also disrupt routing for other devices that depend on it. In a worst-case scenario, the vulnerability may allow an attacker to execute arbitrary code on the affected device.

### CVE-2026-115539

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-10T20:18:03.897 |

SwarmKit's Cluster-API proxy can overwrite a forwarded client's TLS identity with an intermediary manager's identity. WithMetadataForwardTLSInfo replaces outgoing metadata with a copy of the incoming metadata, discarding the redirect guard's changes when built with grpc-go 1.39 or later. During a short window after a leader change, two proxy hops through managers with inconsistent views of the leader can allow an attacker possessing a valid worker node TLS certificate and private key to obtain a manager node certificate for the attacker's own key, escalating privileges from worker to manager. Applications built with an affected SwarmKit version and grpc-go 1.39 or later are impacted.

### CVE-2026-121668

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T19:20:30.263 |

Missing authorization in Azure Confidential Clean Rooms allows an authorized attacker to perform tampering over a network.

### CVE-2026-125759

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T16:17:23.430 |

Nango before 0.71.3 contains an sql injection vulnerability that allows unauthenticated attackers to execute arbitrary SQL by supplying a crafted task group key to the orchestrator API. Attackers can send a malicious group.key to POST /v1/immediate, which TaskEventsHandler.notify() interpolates into a Postgres NOTIFY statement, running stacked queries against the scheduler database.

### CVE-2026-113422

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807;CWE-863` |
| Published | 2026-11-10T15:17:12.510 |

In Eclipse Kura versions 5.0.0 through 5.6.2, the Wire Graph update functionality of the Kura Web UI, and the Wire Service REST API v1 (available since 5.1.0, org.eclipse.kura.rest.wire.provider), determine whether a configuration update targets a Wire Component, Driver or Asset from the factory identifier supplied in the request, instead of the actual factory of the existing component. An authenticated identity holding only the Wires management permission (kura.wires.admin for the Web UI, rest.wires.admin for the REST API) can therefore modify the configuration of existing components that are not part of the Wire Graph, including security-relevant ones, or replace existing components. This allows escalation to full administrative privileges and can disrupt the device. Modifying arbitrary components requires at least one Driver to be installed on the device. The issue is fixed in Eclipse Kura 5.6.3.

### CVE-2026-124741

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-11T11:17:17.233 |

A flaw was found in BusyBox. The udhcpc6 DHCPv6 client does not properly validate the size of network options sent by a server before copying them into memory. A malicious DHCPv6 server on the local network can exploit this flaw by sending a crafted reply, triggering a stack-based buffer overflow. This vulnerability could allow an attacker to achieve arbitrary code execution with root privileges or cause a denial of service (DoS) crash.

### CVE-2026-124036

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-10T16:17:18.630 |

Missing authorization checks in the visual alert feature of FlockOS, Flock's hosted public safety platform, prior to 2026-09-28, allowed an authenticated user with permission to manage saved searches in their own organization to read, modify or delete another organization's saved-search alerts and change their recipients, given the alert's identifier, and to create alerts attributed to another organization. Flock remediated the issue in the hosted service on 2026-09-28; no customer action is required.

### CVE-2026-124739

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-11T11:17:16.983 |

A flaw was found in BusyBox. When the httpd web server processes subdirectory configuration files, an overly long index page name can trigger a stack-based buffer overflow. An attacker with permissions to write to a subdirectory configuration file could exploit this vulnerability to execute arbitrary code with elevated privileges or cause a denial of service (DoS) by crashing the server process.

### CVE-2026-124737

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-11T10:16:43.620 |

A flaw was found in BusyBox. When the TFTP (Trivial File Transfer Protocol) client requests a custom small block size and receives a standard response, it falls back to the default block size without resizing the allocated memory buffer. A malicious TFTP server can exploit this issue by sending standard-sized network packets during a transfer, causing a heap buffer overflow. This flaw allows an attacker to achieve arbitrary code execution or cause a Denial of Service (DoS) by crashing the application.

### CVE-2026-126623

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-11T09:17:14.550 |

Inefficient algorithmic complexity in the JSON reader of Progressive Robot hMailServer 6.3.6 and 6.3.7 allows a remote attacker to hold the server's mail delivery threads or its REST API's worker threads, making mail delivery, the REST API and the webmail unavailable. 6.3.6 fixed CVE-2026-107574, in which reading a JSON object searched the member names already read for each new name, by keeping the names in a hash set; the set uses the standard library's hash, which takes no secret, so member names chosen to fall in one bucket of it still cost time growing with the square of their number. Against the released reader, one such object of 16 MB took about 5 seconds to read in the Linux build, and one of under 6 MB about 23 seconds in the Windows build, where objects of the same sizes with other names took under a tenth of a second. A remote unauthenticated attacker reaches the reader by mailing such an object as a TLS-RPT report, up to 16 MB once decompressed, to a hosted domain's report mailbox, where an administrator has set one; it is read on a mail delivery thread (ten by default), and those threads deliver all mail, local and outbound, so a stream of such reports stops all delivery for as long as it continues. It is also reached without an account through the reply to a password-protected message, with the message's link alone, where the REST API is on (it is off by default) and a public base URL for such links is set; and by any account through the webmail's routes granted 16 MB, and by an application's API key through the send API. Each such request holds one of the REST API's four worker threads, in the process that also serves SMTP, IMAP and POP3.

### CVE-2026-126621

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T09:17:14.277 |

Progressive Robot hMailServer 6.0.0-B1 through 6.3.7 on Windows hands OpenSSL the names of its own TLS files - the listeners' certificates, chains, private keys and Diffie-Hellman parameters, a port's client-certificate CA file (from 6.2.19), the object store's CA file (from 6.3.4) and the ACME client's keys and certificates - as Latin-1 bytes, which on code page 1252 are the code page's own for U+00A0 to U+00FF, and OpenSSL's file opening on Windows reads a name as UTF-8 first and opens the file at that reading when it is there, or creates it there when its folder is. When every byte of a configured name outside ASCII also reads as UTF-8 - for example U+00C3 U+00A9, the bytes C3 A9, which are U+00E9 in UTF-8 - the server used the file at that other name whenever one was there, which allows a local attacker who can create that file or its folder but cannot change the configured one, as any user can by default beside a file an administrator keeps under ProgramData, to have a port that logs on by client certificate (from 6.2.25) accept certificates from a certificate authority of the attacker's own and so sign in over the network as any mailbox without its password; to have the server trust such an authority for its object store and, intercepting that connection, read and modify the messages it stores; to receive the private keys the ACME client writes, the key of a certificate issued for the server's names among them; or to keep TLS ports from starting. The configuration is not the default: by default these files have names in ASCII, client certificates are off on every port, and the object store and ACME are off. The Linux builds are not affected.

### CVE-2026-126613

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-11T09:17:13.267 |

Allocation of resources without limits in the JSON reader of Progressive Robot hMailServer 6.3.2 through 6.3.7 allows a remote attacker to exhaust the server's memory and hold its threads, making mail delivery, the REST API and the webmail unavailable. The reader built a tree of values far larger than the text it read, copying each value into every level above it, and set no bound on the number of values, so a single JSON document of many small values, within the 16 MB the server reads, raised the service's memory by about 2 GB and held one thread for seconds to minutes. From 6.3.4 a remote unauthenticated attacker reaches the reader by mailing such a document as a TLS-RPT report, up to 16 MB once decompressed, to a hosted domain's report mailbox, where an administrator has set one; it is read on a mail delivery thread (ten by default), and those threads deliver all mail, local and outbound. From 6.3.4 it is also reached without an account through the reply to a password-protected message, with the message's link alone, where the REST API is on (it is off by default) and a public base URL for such links is set; and by any account, from 6.3.2 through the webmail's send and draft routes and from 6.3.4 through its other routes granted 16 MB and the send API; the webmail's send, draft and settings routes parsed the body again for each member read. The REST API serves every request on four worker threads, in the process that also serves SMTP, IMAP and POP3, so a few such documents at once make it unavailable and can exhaust the machine's memory and end the whole service. This is a separate defect from CVE-2026-107574, the reader's handling of duplicate member names, fixed in 6.3.6.

### CVE-2026-126609

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T09:17:12.687 |

Progressive Robot hMailServer 6.2.25 through 6.3.7 on Windows, with a PostgreSQL database, the connection's sslmode require, verify-ca or verify-full, and a root certificate file named by PostgreSQLSslRootCert (from 6.2.25) or, with TlsMode=verify-full and neither PostgreSQL key set, by TlsCaFile (from 6.3.4), hands the file's name to libpq as bytes in the system's ANSI code page (up to 6.3.5 as Latin-1 bytes, which on code page 1252 are the code page's own for U+00A0 to U+00FF), and libpq looks for the file by those bytes and then hands the same bytes to OpenSSL, whose file opening on Windows reads a name as UTF-8 first and opens the file at that reading when one is there. When every byte of the name outside ASCII also reads as UTF-8 - for example U+00C3 U+00A9, the bytes C3 A9 on code page 1252, which are U+00E9 in UTF-8 - the database server's certificate was checked against the file at that other name whenever one was there, which allows a local attacker who can create that file but cannot change the configured one, as any user can by default beside a file an administrator keeps under ProgramData, or beside a folder directly under the system drive's root whose permissions the administrator restricted, and who can intercept the connection to the database server or stand in for it, to have hMailServer trust a certificate authority of the attacker's own and read and modify the traffic between hMailServer and its database, the database password included; the file alone, holding no authority that issued the database server's certificate, stops hMailServer from connecting to its database. The same applies in 6.3.4 through 6.3.7 to TlsCaFile when an Oracle MySQL client library has been put in place of the bundled MariaDB Connector/C, since that client opens the file through OpenSSL in the same way; the bundled MariaDB Connector/C opens the file in the code page and is not affected, and neither are the Linux builds. The configuration is not the default: by default no root certificate file is named.

### CVE-2026-123700

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-11T06:17:19.163 |

The Security For WooCommerce WordPress plugin through 1.0.16 does not check that the requester is authorised before running several of its comment cleanup actions, allowing unauthenticated users to permanently delete all comments on the site, including approved ones and WooCommerce order notes.

### CVE-2026-123697

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-11T06:17:18.730 |

The Security For WooCommerce WordPress plugin through 1.0.16 does not restrict who can request a user's current two-factor code or two-factor secret, allowing unauthenticated users to obtain them for any account and bypass the second factor on sites where its one-time password library is available.

### CVE-2026-123696

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-11T06:17:18.607 |

The Security For WooCommerce WordPress plugin through 1.0.16 does not check that the requester is authorised before resetting two-factor authentication enrolment, allowing unauthenticated users to remove the second factor from any account, or from every account at once.

### CVE-2026-121870

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-11T06:17:17.020 |

The Simpler Checkout WordPress plugin before 1.5.4 does not properly restrict who can create orders and checks its automatic login link with a key that stays empty until the store owner configures the Simpler Checkout WordPress plugin before 1.5.4, allowing subscribers on stores that have not completed setup to log in as an administrator.

### CVE-2026-125958

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-10T22:18:31.287 |

Download of code without integrity check vulnerability in N-able N-central allows Remote Code Inclusion.

This issue affects N-central: through 24.6.1.

### CVE-2026-126081

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-10T21:19:26.817 |

Action Pack is a framework for handling and responding to web requests. Prior to 8.1.4.1 and 8.0.5.2, ActionController::Parameters#each_key delegates to the internal ActiveSupport::HashWithIndifferentAccess that holds the request parameters, so when called with a block it returns that hash instead of the Parameters instance. The hash does not respond to permitted?, so Active Model mass assignment (new, assign_attributes, update) accepts it without raising ActiveModel::ForbiddenAttributesError. An application that passes the return value of each_key to mass assignment could allow a remote, unauthenticated attacker to set attributes that the application does not permit, such as an authorization flag. This is an incomplete fix of CVE-2020-8164, which made each, each_pair and each_value return the Parameters instance but left each_key delegated. An application is affected if it passes the return value of ActionController::Parameters#each_key, called with a block, to mass assignment. Rails itself makes no such call. This issue is fixed in versions 8.1.4.1 and 8.0.5.2.

### CVE-2026-126080

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-11-10T21:19:26.663 |

Active Support is a collection of utility classes and standard library extensions used by Rails and other Ruby projects. Prior to 8.1.4.1 and 8.0.5.2, when constant lookup raises LoadError, ActiveSupport::Inflector#safe_constantize (and String#safe_constantize) builds a regular expression from the requested constant name without escaping it, so a caller that passes untrusted input lets the attacker choose the source of a pattern that the application compiles. Crafted patterns can trigger defects in Ruby's regular expression compiler, possibly leading to a crash of the server process, and repeated requests could keep the application unavailable. Action Cable passes the channel value of each subscribe command to safe_constantize before any channel lookup, so an unauthenticated client can reach this code when the application mounts Action Cable and accepts connections from untrusted clients without an added authentication check. This issue is fixed in versions 8.1.4.1 and 8.0.5.2.

### CVE-2026-95784

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-10T20:19:49.350 |

A vulnerability exists in a system component that may, under certain conditions, disrupt the availability of affected services. Successful exploitation could result in temporary service interruption or loss of functionality.

### CVE-2026-95783

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-10T20:19:49.210 |

A vulnerability exists in a network-facing component that may, under certain conditions, result in service disruption. Successful exploitation could cause temporary unavailability of affected functionality.

### CVE-2026-95782

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-10T20:19:49.063 |

A vulnerability exists in a monitoring component that may, under certain conditions, allow security controls to be circumvented. Successful exploitation could result in unauthorized access to information intended for authorized users only.

### CVE-2026-95781

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-10T20:19:48.920 |

A security vulnerability exists in AthonetOS that may allow an unauthorized party to affect service operation or gain access to certain protected system functions. Successful exploitation could result in a compromise of service integrity or unauthorized system access.

### CVE-2026-59632

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-10T20:19:32.860 |

In RespondReceivedMessage of MtsMessageController.cpp, there is a possible way to trigger memory exhaustion via an undrained message queue due to a type confusion. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-59623

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-11-10T20:19:32.140 |

In CompareTelUris of SipAddress.cpp, there is a possible way to trigger an unhandled out of range exception and process crash due to an incorrect bounds check. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-59613

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-10T20:19:31.600 |

In multiple locations, there is a possible way to trigger an out of bounds read and temporary denial of service due to improper input validation. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-59611

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-10T20:19:31.393 |

In multiple locations, there is a possible way to trigger a temporary denial of service via an integer overflow trap due to improper input validation. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-59603

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T20:19:30.757 |

In RespondReceivedMessage of MtsMessageController.cpp, there is a possible way to trigger a double free and process abort during message retry handling due to a use after free. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-59595

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-10T20:19:30.123 |

In DecodeHeaderComponent of SipStack.cpp, there is a possible way to trigger stack exhaustion via unbounded mutual recursion due to a resource exhaustion. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-59585

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-10T20:19:29.473 |

In SetDisplayName of RegInfoContact.cpp, there is a possible denial of service due to a missing null check. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-59582

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T20:19:29.267 |

In StartTimer of UcePublishManager.cpp, there is a possible way to trigger a process abort during timer calculation due to an integer overflow. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58807

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-10T20:19:27.717 |

In Retry_MtsMessageInPending of MtsMessageController.cpp, there is a possible way to trigger memory exhaustion via leaked message objects due to a logic error. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58789

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T20:19:26.303 |

In s_gen_tile_param of multiple files, there is a possible way to trigger an out of bounds write in tile parameter arrays due to an incorrect bounds check. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-120814

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-10T20:18:52.047 |

An improper privilege management issue in the sharding subsystem of MongoDB Server may allow a user holding certain shard-level administrative privileges to cause persisted internal coordination state to be reprocessed with elevated internal authority. Because that state is trusted rather than re-validated, operations may be carried out beyond the user's authorized scope, including changes to cluster-wide security configuration. Successful triggering this issue requires an authenticated session directly against a cluster member and can result in unauthorized access to and modification of data across the cluster.

### CVE-2026-120807

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-11-10T20:18:51.033 |

A flaw in MongoDB’s X.509 cluster-membership authentication guard could allow a holder of a cluster-member certificate to gain elevated internal privileges when a specific deployment configuration is in use. An internal check, which prevents a certificate recognized as a cluster member from also being treated as a regular user, does not correctly distinguish between certain error conditions encountered during user lookup. Under certain timing conditions, this can cause the check to be bypassed, granting the connection full internal system privileges. Triggering this issue requires possession of a valid cluster-member TLS certificate, non-default X.509 cluster authentication configuration, and specific conditions during the user cache lookup process.

### CVE-2026-115483

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T20:18:03.537 |

The Everest Forms plugin for WordPress is vulnerable to Arbitrary File Read in all versions up to, and including, 3.6.3 via the attach_entry_files() function. This is due to the function attaching any entry field value whose meta key matches /signature_/ to the notification email after only a file_exists() check, without validating or restricting the path. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, such as wp-config.php, which can contain sensitive information. Successful exploitation requires a form whose email notification has the “Attach Files” setting enabled and that contains a field with a meta key matching /signature_/ (for example, a text field labelled “Signature”), with the notification routed to an attacker-supplied email address so the exfiltrated file is delivered to the attacker. Note: The Everest Forms Pro add-on is required to exploit this vulnerability, as it provides the signature field and the email file-attachment functionality (file-email-attachments) that the attack relies on.

### CVE-2026-97002

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:22:23.170 |

Out-of-bounds read in Windows VMSwitch allows an authorized attacker to elevate privileges locally.

### CVE-2026-96993

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-763` |
| Published | 2026-11-10T19:22:22.623 |

Release of invalid pointer or reference in Windows Performance Monitor allows an unauthorized attacker to execute code over a network.

### CVE-2026-96972

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:22:19.457 |

Out-of-bounds read in Windows DNS allows an unauthorized attacker to disclose information over a network.

### CVE-2026-96176

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-11-10T19:22:17.803 |

Missing release of memory after effective lifetime in Windows DNS allows an unauthorized attacker to deny service over a network.

### CVE-2026-96134

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T19:22:10.690 |

Uncontrolled resource consumption in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-96081

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:06.413 |

Heap-based buffer overflow in Windows Rich Text Edit Control allows an unauthorized attacker to execute code over a network.

### CVE-2026-96077

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-10T19:22:06.010 |

Null pointer dereference in Windows TCP/IP allows an unauthorized attacker to deny service over a network.

### CVE-2026-95964

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:21:52.863 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-88244

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:33.937 |

Use after free in Windows Link Layer Topology Discovery Protocol allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-88236

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-10T19:21:32.550 |

Null pointer dereference in Microsoft QUIC allows an unauthorized attacker to deny service over a network.

### CVE-2026-88216

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-367` |
| Published | 2026-11-10T19:21:28.500 |

Time-of-check time-of-use (toctou) race condition in Windows DHCP Server allows an authorized attacker to execute code over a network.

### CVE-2026-88212

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:27.470 |

Use after free in Windows Network Address Translation (NAT) allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-88111

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:26.700 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-84010

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-11-10T19:21:24.573 |

Exposed dangerous method or function in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-83684

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-126` |
| Published | 2026-11-10T19:21:23.750 |

Buffer over-read in Windows iSCSI Target Service allows an unauthorized attacker to disclose information over a network.

### CVE-2026-80094

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:22.593 |

Use after free in Remote Desktop Gateway Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-70240

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-11-10T19:21:21.077 |

Missing release of memory after effective lifetime in Windows Kerberos allows an unauthorized attacker to deny service over a network.

### CVE-2026-69901

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-10T19:21:19.900 |

Origin validation error in Microsoft Teams for Android allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-125330

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-10T19:21:10.463 |

HarnessRouter is a self-hosted unified API for agent harnesses. From version 0.4.2 until 0.31.7, routes that accept a session ID or response ID validate only the caller's organization and do not enforce the workspace scope of a non-default workspace API key. A key holder who learns a non-guessable identifier from another workspace in the same organization can read sessions, conversation turns, files, traces, and responses, overwrite files, cancel or delete sessions, and publish share links. The issue does not cross organization boundaries, and console users, organization keys, and Default Workspace keys intentionally retain organization-wide access. This issue is fixed in version 0.31.7.

### CVE-2026-125327

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-405;CWE-770` |
| Published | 2026-11-10T19:21:09.977 |

pgEdge RAG Server is an API server for retrieval-augmented generation over PostgreSQL content using pgvector. Prior to 2.0.0, the unauthenticated query endpoint uses FetchDocuments in internal/database/search.go to read the entire filtered corpus without a LIMIT and rebuild an in-memory BM25 index on every request. Because HybridEnabled is set by default in internal/config/loader.go and the endpoint has no rate limit, inexpensive remote queries can impose database and CPU work proportional to corpus size and exhaust service resources. This issue is fixed in version 2.0.0.

### CVE-2026-125134

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:06.983 |

Use after free in Windows Function Discovery Resource Publication allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-124227

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-11-10T19:20:49.863 |

Use of uninitialized resource in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-124185

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-11-10T19:20:47.787 |

Use of uninitialized resource in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-124170

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:44.530 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-123379

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:41.180 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-123378

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:20:41.043 |

Integer overflow or wraparound in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-122177

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-10T19:20:35.697 |

Improper link resolution before file access ('link following') in Windows iSCSI allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-122169

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-1220` |
| Published | 2026-11-10T19:20:34.170 |

Insufficient granularity of access control in Windows IKE Extension allows an authorized attacker to perform spoofing locally.

### CVE-2026-122163

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:20:32.970 |

Double free in Windows Image Acquisition allows an unauthorized attacker to execute code over a network.

### CVE-2026-121680

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-10T19:20:31.833 |

Exposure of sensitive information to an unauthorized actor in Windows NTLM allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-121660

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-10T19:20:29.287 |

Incomplete list of disallowed inputs in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-120006

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-10T19:20:26.560 |

Insertion of sensitive information into sent data in .NET Aspire allows an authorized attacker to elevate privileges locally.

### CVE-2026-120000

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-10T19:20:25.773 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-119996

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:25.130 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-119995

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:20:24.960 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-119966

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T19:20:21.417 |

Integer overflow or wraparound in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-119960

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-11-10T19:20:20.277 |

Use of uninitialized resource in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-119948

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:20:18.283 |

Stack-based buffer overflow in Windows Active Directory allows an authorized attacker to execute code over a network.

### CVE-2026-119947

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:18.020 |

Use after free in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-119944

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:17.393 |

Heap-based buffer overflow in Windows Mobile Device Management allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-119938

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:16.253 |

Heap-based buffer overflow in Windows Shell allows an unauthorized attacker to execute code over a network.

### CVE-2026-119932

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-10T19:20:15.080 |

Null pointer dereference in Windows Remote Desktop allows an unauthorized attacker to deny service over a network.

### CVE-2026-119880

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:07.250 |

Heap-based buffer overflow in Microsoft XPS Document Converter allows an unauthorized attacker to execute code over a network.

### CVE-2026-119858

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:20:03.843 |

Heap-based buffer overflow in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-119837

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:59.990 |

Heap-based buffer overflow in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-118750

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-10T19:19:51.923 |

Allocation of resources without limits or throttling in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-118749

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-10T19:19:51.787 |

Inefficient algorithmic complexity in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-118748

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-10T19:19:51.643 |

Allocation of resources without limits or throttling in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-118747

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-10T19:19:51.497 |

Inefficient algorithmic complexity in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-118735

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-10T19:19:50.003 |

Weak authentication in Active Directory Domain Services allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118301

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-11-10T19:19:43.787 |

Use of uninitialized resource in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-118153

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-10T19:19:37.173 |

Inefficient algorithmic complexity in Microsoft Exchange Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-118148

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:19:35.093 |

Improper authentication in Active Directory Domain Services allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118145

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:34.687 |

Use after free in Windows Function Discovery SSDP Provider allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-118115

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T19:19:30.097 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118114

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T19:19:29.903 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118108

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-283` |
| Published | 2026-11-10T19:19:28.967 |

Improper authorization in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-116947

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:28.070 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-116943

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-126` |
| Published | 2026-11-10T19:19:27.410 |

Buffer over-read in SQL Server allows an unauthorized attacker to disclose information over a network.

### CVE-2026-116938

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:26.270 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-116937

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:26.047 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-116931

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:23.410 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-116929

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-10T19:19:22.090 |

Execution with unnecessary privileges in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-116926

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:19:20.023 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Teams allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-116718

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:15.340 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-116706

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:12.017 |

Use after free in Windows Link Layer Topology Discovery Protocol allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-116698

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:11.390 |

Use after free in Microsoft WDAC OLE DB provider for SQL allows an unauthorized attacker to execute code over a network.

### CVE-2026-114157

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:19:09.087 |

Concurrent execution using shared resource with improper synchronization ('race condition') in ASP.NET Core allows an authorized attacker to elevate privileges locally.

### CVE-2026-114155

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-10T19:19:08.783 |

Time-of-check time-of-use (toctou) race condition in .NET allows an authorized attacker to elevate privileges locally.

### CVE-2026-114154

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-11-10T19:19:08.633 |

Uncontrolled resource consumption in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-114149

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-10T19:19:08.040 |

Uncontrolled resource consumption in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-114147

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-11-10T19:19:07.853 |

Missing release of memory after effective lifetime in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-113861

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:06.800 |

Use after free in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-113859

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:06.487 |

Use after free in Windows TCP/IP allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-113855

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-11-10T19:19:06.177 |

Use of uninitialized resource in Windows DNS allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-113825

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:19:04.827 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows SMB Server Network Transport Driver (srvnet.sys) allows an authorized attacker to execute code over a network.

### CVE-2026-113823

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T19:19:04.327 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Azure CycleCloud allows an unauthorized attacker to disclose information over a network.

### CVE-2026-113768

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:56.273 |

Heap-based buffer overflow in Windows Performance Counters allows an unauthorized attacker to execute code over a network.

### CVE-2026-113752

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:53.363 |

Use after free in Windows Print Spooler Components allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-113749

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:18:52.763 |

Heap-based buffer overflow in Microsoft Windows Codecs Library allows an unauthorized attacker to execute code over a network.

### CVE-2026-112985

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:18:50.937 |

Integer overflow or wraparound in Microsoft JScript allows an unauthorized attacker to execute code over a network.

### CVE-2026-112972

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-10T19:18:47.860 |

Integer overflow or wraparound in Windows SMB Server allows an authorized attacker to execute code over a network.

### CVE-2026-112966

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-10T19:18:46.743 |

Uncontrolled resource consumption in Windows Security Account Manager allows an unauthorized attacker to deny service over a network.

### CVE-2026-112793

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:18:41.010 |

Use after free in Windows Event Collector Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-111287

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:18:25.627 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-111286

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:25.443 |

Use after free in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-110053

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:22.717 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-110052

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:22.550 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-109500

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:19.167 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-109498

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:18.847 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-109491

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:17.767 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-109487

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:17.593 |

Use after free in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-109481

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-10T19:18:17.267 |

Cross-site request forgery (csrf) in ASP.NET Core allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-109478

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-10T19:18:17.113 |

Inefficient algorithmic complexity in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-109475

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:18:16.770 |

Stack-based buffer overflow in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-108421

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:18:13.213 |

Out-of-bounds read in Windows File Server Resource Management Service allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-105579

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125;CWE-190` |
| Published | 2026-11-10T19:18:00.503 |

Integer overflow or wraparound in Windows DNS allows an unauthorized attacker to disclose information over a network.

### CVE-2026-105578

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-822` |
| Published | 2026-11-10T19:18:00.303 |

Integer overflow or wraparound in Microsoft JScript allows an unauthorized attacker to execute code over a network.

### CVE-2026-105561

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-11-10T19:17:58.740 |

Uncontrolled resource consumption in Windows Secure Socket Tunneling Protocol (SSTP) allows an unauthorized attacker to deny service over a network.

### CVE-2026-105558

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:58.203 |

Heap-based buffer overflow in Windows Deployment Services allows an authorized attacker to execute code over a network.

### CVE-2026-105551

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:57.300 |

Heap-based buffer overflow in Windows NetBIOS allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-105544

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-10T19:17:56.330 |

Improper access control in .NET allows an authorized attacker to elevate privileges locally.

### CVE-2026-105515

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-11-10T19:17:50.740 |

Buffer over-read in Windows Message Queuing allows an unauthorized attacker to deny service over a network.

### CVE-2026-105512

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-10T19:17:50.283 |

Integer underflow (wrap or wraparound) in Microsoft QUIC allows an unauthorized attacker to deny service over a network.

### CVE-2026-105437

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:46.200 |

Affected versions of Git have a heap buffer overflow in the three-way merge
code (xdiff), which an attacker can trigger through a repository they
control.

When Git merges a file, it first adds up the size of the merged
output, allocates a buffer of that size, and then writes the output into
it. That total was kept in a 32-bit signed integer. The
conflict-marker-size attribute, which can be set from a committed
.gitattributes file, accepts any positive integer, and the markers are
written several times for every conflict. A small file with a huge marker
size and many separate conflicts can therefore push the total past 4 GiB,
so the integer wraps to a small value and Git writes attacker-controlled
merge output past the end of a buffer that is too small. At minimum this
crashes Git, and because the overflow is large and its contents are largely
attacker-controlled, worse heap corruption is possible.

Any command that does a textual three-way merge can trigger it, such
as git-merge(1), git-rebase(1), git-cherry-pick(1), and
git-merge-tree(1). The latter is most likely a target for Git forges,
which might use git-merge-tree(1) on the server-side to check
mergeability. When the server reads attributes from trees in the
repository (for example through attr.tree or --attr-source), any
user who can push branches and request that they be merged (for
example by opening a pull or merge request) can trigger the overflow
without anyone else doing anything, and the data they push is small
because the oversized output only appears during the merge.

The problem has been patched by computing the size as size_t and
checking every addition for overflow, so Git stops with an error
instead of overflowing.

Servers that cannot upgrade right away can add

* conflict-marker-size=7

to each repository's info/attributes as a workaround, which overrides
any in-tree .gitattributes, or turn off server-side mergeability checks for
untrusted repositories.

### CVE-2026-126610

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T09:17:12.830 |

Progressive Robot hMailServer 6.3.4 through 6.3.7, with a MySQL or MariaDB database and TlsMode=verify-full, does not hand the database client the CA file that TlsCaFile names when the file's name contains a character outside ASCII on Linux, or above U+00FF on Windows, which allows an attacker who can intercept the connection to the database server to read and modify the traffic between hMailServer and its database, by presenting, with MariaDB Connector/C 3.4.2 to 3.4.10 as the client, a certificate from any authority, its own included, for any name, and otherwise a certificate for the database server's name issued by any certificate authority in the system's trust store. The server converted the name for the client with the C runtime's conversion in the C locale, which gives an empty string for such a name, and then set no CA file at all, without an error, while certificate verification stayed on, so the client - MariaDB Connector/C, bundled on Windows and the distribution's on Linux - verified the certificate of a database server over the network against the system's trust store instead of the configured CA; Connector/C 3.4.2 to 3.4.10 (bundled on Windows in 6.3.4 to 6.3.6) went further and, with no CA file, took a certificate within its dates whose issuer it could not find, for any name, with neither its chain nor its name checked and no password proof, when the server offered first a sign-in method that hashes the password, which an attacker in the middle chooses (MariaDB's CONC-853, fixed in Connector/C 3.4.11), and Connector/C 3.4 accepted from a MariaDB 11.4 or later server a certificate the store did not vouch for when that server proved it held the account's password; on a connection it treats as local (127.0.0.1, ::1, a Unix socket, a named pipe, and localhost on Windows), Connector/C 3.4.1 and later checked neither the certificate's issuer nor its name, so that a local attacker able to stand in for the database server could present any certificate within its dates of its own making. The settings line of hmailserver --check-database still named the configured file, and the application log said the certificate had been checked. With MariaDB Connector/C 3.4.1 to 3.4.9 as the client - bundled on Windows in 6.3.4 to 6.3.6, and the client of Linux distributions that have not patched it - the missing CA file also met the precondition of CVE-2026-107819, so that a certificate issued for any other name by a trusted authority was enough to obtain the database password. On Linux the file was found only when the server ran on glibc under a locale whose character set holds the name's characters (a UTF-8 locale, or a legacy 8-bit one the system has, in whose bytes the file is then named); with no locale, LC_ALL=C or a locale the system lacks, and on Alpine (musl), the connection failed instead. The configuration is not the default: TlsMode defaults to prefer, which checks no certificate.

### CVE-2026-64669

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285;CWE-693` |
| Published | 2026-11-11T05:19:51.327 |

pam_usb provides hardware authentication for Linux using removable media. From version 0.8.0 to before version 0.9.3, the deny_remote feature in pam_usb uses /usr/bin/w -i to detect whether the authenticating user has an active remote tmux session. In pusb_tmux_has_remote_clients() (src/tmux.c), the IPv6 detection regex required exactly four explicit colon-separated groups of 1-4 hex digits (e.g. 2001:0db8:85a3:0000). Any IPv6 address in compressed notation — including loopback (::1), link-local (fe80::1), and global unicast addresses (2001:db8::1) — did not match this pattern. As a result the remote-client check silently returned "no remote clients" even when a remote tmux client was connected from such an address. This issue has been patched in version 0.9.3.

### CVE-2026-64668

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285;CWE-693` |
| Published | 2026-11-11T05:19:51.113 |

pam_usb provides hardware authentication for Linux using removable media. From version 0.8.0 to before version 0.9.3, the deny_remote feature in pam_usb uses /usr/bin/w -i to detect whether the authenticating user has an active remote tmux session. In pusb_tmux_has_remote_clients() (src/tmux.c), the IPv6 detection pattern matched the address group and then immediately expected whitespace. On Linux systems with multi-homed network interfaces, w -i appends a zone index (scope identifier) to link-local IPv6 addresses — e.g. fe80::1%eth0. The %eth0 suffix appeared between the address and the next whitespace field, causing the regex match to fail even for an otherwise-matching remote session. The function returned "no remote clients" and granted access. This issue has been patched in version 0.9.3.

### CVE-2026-126083

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-348` |
| Published | 2026-11-10T21:19:27.133 |

Action Pack is a framework for handling and responding to web requests. From 8.1 until 8.1.4.1, Since Rails 8.1.0, ActionDispatch::RemoteIp derives request.remote_ip from Rack::Request#forwarded_for, which under Rack 3 reads the RFC 7239 Forwarded header in preference to X-Forwarded-For. When a reverse proxy appends the client address to X-Forwarded-For but passes a client-supplied Forwarded header through unchanged, request.remote_ip returns an address chosen by the client, and the IP spoofing check does not raise, because it compares only Client-Ip with the forwarded addresses. An unauthenticated attacker could therefore spoof request.remote_ip, possibly bypassing IP-based access controls and rate limits keyed on the client address (including the default by: of rate_limit), and falsifying the client address in logs. An application is affected if it meets all of these requirements: Runs Rails 8.1.0 through 8.1.4 with Rack 3. Under Rack 2.2, forwarded_for reads only X-Forwarded-For. Is served behind a proxy that does not remove or overwrite a client-supplied Forwarded header. Relies on request.remote_ip for access control, rate limiting, or auditing. The fix detects a spoofed Forwarded header only when the proxy also sets X-Forwarded-For. An application whose proxy passes a client-supplied Forwarded header through and sets no X-Forwarded-For remains exposed after upgrading, and should configure the proxy to remove or overwrite Forwarded, or apply the workaround below. This issue is fixed in version 8.1.4.1.

### CVE-2026-69327

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:19.600 |

Use after free in Remote Desktop Gateway Service allows an unauthorized attacker to execute code locally.

### CVE-2026-62903

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294` |
| Published | 2026-11-10T19:21:17.087 |

Authentication bypass by capture-replay in SQL Server allows an unauthorized attacker to disclose information over a network.

### CVE-2026-54436

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:16.513 |

Heap-based Buffer
Overflow in the io-char library's DCMD_CHR_WAITINFO devctl() handler could
allow an attacker with local access to cause data tampering, arbitrary code
execution, or a crash in the Character I/O device driver.

### CVE-2026-125336

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-10T19:21:11.393 |

Forge (also called node-forge) is a native implementation of Transport Layer Security in JavaScript. Prior to 1.4.3, pki.verifyCertificateChain() in lib/x509.js does not decode or enforce the X.509 nameConstraints extension while validating certificate paths. A name-constrained certificate authority with a non-critical extension can therefore issue a leaf certificate with a subjectAltName dNSName or subject commonName outside a permitted subtree or inside an excluded subtree, and node-forge accepts the chain. Exploitation requires a name-constrained CA that chains to a trusted root and either its private key or the ability to obtain an out-of-scope certificate, allowing impersonation of names outside the delegated namespace, including against forge.tls clients. Chains without nameConstraints are not affected, and affected versions safely reject critical nameConstraints as unsupported rather than accepting them. This issue is fixed in version 1.4.3.

### CVE-2026-102230

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T19:17:40.163 |

Missing authorization in Visual Studio Code allows an unauthorized attacker to disclose information over a network.

### CVE-2026-97401

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:L/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73;CWE-269` |
| Published | 2026-11-10T17:17:55.450 |

In Kura versions <= 5.6.2, `CommandCloudApp.execute()` extracts a caller-supplied ZIP archive into a caller-supplied directory inside the Kura JVM process before dispatching the command to the executor service. On a packaged Kura installation the JVM runs as `kurad` with `CAP_DAC_OVERRIDE`, while the configurable "Unprivileged" executor drops to the `kura` user via `su`.



A caller with permissions `rest.command` who is intentionally restricted to unprivileged command execution (`privileged.command.service.enable=false`, the default) can therefore set `workingDirectory` to `/` and use the ZIP body to write or overwrite arbitrary files on the device as `kurad`, completely bypassing the unprivileged sandbox the operator selected.



The command service is disabled by default since Kura 4.0.0 [1]. The issue does not apply when the command service is disabled.



[1] https://github.com/eclipse-kura/kura/blob/f9f969231892769a269876b23f19fa0e8173e3df/kura/distrib/RELEASE_NOTES.txt#L94

### CVE-2026-59986

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-190` |
| Published | 2026-11-10T17:17:45.043 |

rabbitmq-c is a C-language AMQP client library for RabbitMQ. Prior to version 0.17.0, the bounds check (*offset = o + len) <= encoded.len overflows when o + len > SIZE_MAX on 32-bit systems. len is a uint32_t read from the AMQP wire as a BYTES/UTF8 field length. The overflow wraps the check to a small value that passes, producing a decoded amqp_bytes_t with a multi-GB .len pointing into a small frame buffer. This results in an out-of-bounds read of up to ~4GB of process memory on 32-bit systems (ARM, MIPS, x86 ILP32, embedded IoT AMQP clients). Enabling information disclosure or denial of service. Not exploitable on 64-bit systems where size_t is 64-bit. This issue has been patched in version 0.17.0.

### CVE-2026-126624

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-283` |
| Published | 2026-11-11T09:17:14.690 |

Unverified ownership in the Windows installer of Progressive Robot hMailServer 6.3.7 allows a local authenticated user to run code as the mail server's service account or as an administrator when setup installs into, or upgrades, a program folder that accounts other than the administrators could write before, such as one made beforehand at the root of a drive. 6.3.7 fixed CVE-2026-107571 by giving the program folder, Bin and ControlPanel permissions that only administrators may change, but setup refused nothing that was already in them, or in the folders that hold the event script, the add-ons and the database scripts: a program, a library, a script or a settings file that another account owns, or whose own permissions let another account change it, is kept with that owner and those permissions, which the hardening of the folders does not take away. Setup then runs programs from Bin with the administrator's elevated rights, and the service, which runs as LocalSystem or as its virtual account, runs them and the event script, so that a library such an account placed in Bin is loaded in place of the system's; the account can still change the file after the installation. The default installation under Program Files is not affected.

### CVE-2026-126622

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-11T09:17:14.413 |

Incorrect default permissions in the Windows installer of Progressive Robot hMailServer 6.3.7 allow a local authenticated user to run code as the administrator who runs setup, when the server is installed into a program folder that is already there and that accounts other than the administrators could write, such as a folder made beforehand at the root of a drive, or when such an installation is upgraded or repaired. 6.3.7 fixed CVE-2026-107571 by giving the program folder, Bin and ControlPanel permissions that only administrators may change, but for a folder that is already there it does so only at the end of setup: setup first copies the programs into Bin, which every user may still write, and runs programs from Bin with the administrator's elevated rights, registering the service among them, before that hardening, so that a library another account places in Bin meanwhile is loaded in place of the system's. A handle an account opened on such a folder while it could write it keeps that access after the hardening. The default installation under Program Files, whose folders give ordinary users read and execute only, is not affected.

### CVE-2026-120792

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-10T19:20:28.720 |

Insertion of sensitive information into log file in Aspire allows an authorized attacker to disclose information locally.

### CVE-2026-120778

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-379` |
| Published | 2026-11-10T19:20:26.887 |

Creation of temporary file in directory with insecure permissions in .NET Aspire allows an authorized attacker to elevate privileges locally.

### CVE-2026-119900

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:20:10.363 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-111303

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:18:28.180 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-111300

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:18:27.743 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-110065

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:18:24.447 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-110045

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:18:21.043 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-109504

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:18:20.113 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-109497

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-10T19:18:18.697 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-126042

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T17:17:31.303 |

VNote 3.11.0 before 4.12.0 contains an OS command injection vulnerability in its Tasks feature: magic variables such as ${bufferName} and ${selectedText} are substituted into a shell command string without escaping. Attackers can share a notebook containing a note whose filename or text includes shell metacharacters such as $(...), backticks, ; or |, executing commands as the victim when they run a task referencing these variables.

### CVE-2026-12427

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T08:17:18.250 |

The ARforms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'description' parameter in all versions up to, and including, 7.2.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload is deserialized via maybe_unserialize() when an administrator views the affected entry; if the attacker's array contains a 'referrer' key, the attacker-controlled page_url and http_referrer values are used as-is and rendered unescaped into the admin entry detail view.

### CVE-2026-12424

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T08:17:18.097 |

The ARforms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Referer Header in all versions up to, and including, 7.2.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The arf_save_incomplete_form_data() AJAX handler is registered with wp_ajax_nopriv_, meaning unauthenticated attackers can store a malicious payload by submitting a partial form entry with a forged Referer header, with no authentication required at any step.

### CVE-2026-64671

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-11-11T05:19:51.733 |

Waline is a comment system with backend support. In versions 3.15.2 and prior, the @waline/client UserList widget builds its DOM by concatenating server-returned commenter fields directly into root.innerHTML with no HTML escaping. The commenter nick and link are stored and returned verbatim by the server (only the comment body is sanitized), and the link field is never sent to the spam filter. So an unauthenticated visitor who posts a comment with link = x"><img src=x onerror=...> achieves stored cross-site scripting that executes, with no interaction, in the browser of every visitor to a page that embeds the UserList widget. At time of publication, there are no publicly available patches.

### CVE-2026-95785

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-10T20:19:49.483 |

A vulnerability exists in a system component that may, under certain conditions, allow an authorized user to make unauthorized changes to system-managed content. Successful exploitation could affect system confidentiality, integrity, and availability, and may disrupt trusted interactions among system functions.

### CVE-2026-118157

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-10T19:19:37.493 |

Weak authentication in Microsoft Exchange Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-118151

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-10T19:19:36.763 |

External control of file name or path in Microsoft Exchange Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-116944

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:27.570 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-116936

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:19:25.723 |

Stack-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-116933

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:19:24.067 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-105560

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-763` |
| Published | 2026-11-10T19:17:58.580 |

Release of invalid pointer or reference in Windows DHCP Server allows an authorized attacker to execute code over a network.

### CVE-2026-105520

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-10T19:17:51.160 |

Improper link resolution before file access ('link following') in Windows DNS allows an authorized attacker to elevate privileges over a network.

### CVE-2026-105425

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-10T16:17:13.410 |

OS command injection in Ivanti Sentry before versions 11.0.0, 10.8.3, and 10.7.4 as well as in Ivanti EPMM before versions 12.11.0.0, 12.10.0.1, and 12.9.0.3 allows a remote authenticated attacker with admin privileges to achieve remote code execution.

### CVE-2026-126662

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-11T13:17:24.337 |

Contao 4.0.0 before 5.3.54, 5.4.0 before 5.7.17, and 6.0.0 before 6.0.6 contains an access control bypass vulnerability that allows filemount-restricted backend users to modify folders outside their filemount via the file manager Edit-Multiple operation. Attackers holding the protected or syncExclude field permission can submit outside folder paths in the IDS parameter to publish protected folders or exclude them from DBAFS synchronization, exposing files for public download.

### CVE-2026-124253

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T11:17:16.803 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in codepeople Calculated Fields Form calculated-fields-form allows DOM-Based XSS.This issue affects Calculated Fields Form: from n/a through 5.5.2.8.

### CVE-2026-123478

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T11:17:16.603 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Meow Apps AI Engine ai-engine allows Stored XSS.This issue affects AI Engine: from n/a through 3.9.1.

### CVE-2026-124250

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T10:16:43.140 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in AyeCode Ltd GeoDirectory geodirectory allows Reflected XSS.This issue affects GeoDirectory: from n/a through 2.8.202.

### CVE-2026-93487

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T08:17:19.213 |

In affected versions of Octopus Server, incorrect validation of the permissions assigned to a user that would allow them to create project triggers could result in the user being able to run runbooks or create deployments they were not authorised to perform.

### CVE-2026-121863

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T06:17:16.877 |

The Knowledge Building WordPress plugin before 0.7.3 does not escape several user-supplied values before echoing them back in the response of an AJAX action available to unauthenticated users, and serves that response as HTML, leading to a Reflected Cross-Site Scripting.

### CVE-2026-64666

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-807` |
| Published | 2026-11-11T05:19:50.700 |

pam_usb provides hardware authentication for Linux using removable media. Prior to version 0.9.3, src/local.c reads XRDP_SESSION with plain getenv(3) at the head of pusb_local_login while every other env consumer in the same function uses secure_getenv(3). When pam_usb.so loads into a setuid PAM host, the calling user controls the environment passed in. Clearing XRDP_SESSION before invoking the host bypasses the explicit XRDP-deny rule. Other remote-detection signals (rmsvc, evdev, loginctl, utmp) may still catch the session, but the env-based detection alone is defeated. This issue has been patched in version 0.9.3.

### CVE-2026-63192

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T03:16:52.017 |

OpenMRS module bahmnicore contains Core OpenMRS modules for Bahmni (including ERP & ELIS Atom Feed Clients). In version 0.93, an attacker with authenticated access could potentially exfiltrate sensitive data from the database. This issue has been patched in version 0.93.1.

### CVE-2026-126566

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-11T03:16:51.057 |

Semantic MediaWiki 7.3.1 before 7.4.1 contains an incorrect authorization vulnerability in EditProtectionUpdater::userMayChangeProtection() that checks protection changes against the page's latest revision author. Editors can add {{#set:Is edit protected=false}} to a transcluded template, removing administrator edit and move protection logged under the administrator's name.

### CVE-2026-126561

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-11T03:16:50.217 |

Semantic MediaWiki 2.5.0 before 7.4.1 contains a missing authorization vulnerability that allows editors without the edit-protection right to lock pages by adding an Is edit protected annotation. Attackers can add [[Is edit protected::true]] to pages or #set it in widely transcluded templates, so the TitleQuickPermissions hook blocks other editors and administrators from editing, moving or deleting them indefinitely.

### CVE-2026-116645

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-11T03:16:48.630 |

LimeSurvey Community Edition 7.8.0 contains an SQL injection vulnerability in the survey-archive participant import and SPSS-response export workflow. An authenticated user with global surveys.create permission can import a crafted .lsa archive whose participant XML creates an attacker-named attribute column. When the user exports responses from the imported non-anonymous survey, LimeSurvey passes the persisted name to Yii's select builder. Names containing parentheses are treated as SQL expressions instead of quoted identifiers, causing attacker-controlled SQL to execute with the application's database privileges.

### CVE-2026-126123

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-11-10T22:18:31.577 |

BeeS Software Solutions ERP before 04 September 2026 allows any low-privileged user to navigate directly to the administrative dashboard endpoint and gain access to the administrative console, including unrestricted access to institutional, employee, and student data.

### CVE-2026-120826

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T21:19:02.517 |

An authorization flaw in the aggregation and view-definition handling of sharded deployments may allow a user holding only basic read-write privileges on a single database to define a view whose underlying processing is not fully subjected to privilege checking. Reading that view may result in unintended access to data belonging to other databases held on the same shard.

### CVE-2026-120825

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T21:19:02.333 |

An authorization weakness in the aggregation framework of MongoDB Server may allow an authenticated user holding only basic database privileges to read the contents of collections in a database for which they have not been granted read access. The privilege evaluation performed while a view definition is validated does not cover a nested portion of the supplied pipeline, so the resulting view returns data the user is otherwise refused. This may result in unintended access to data, including stored authentication material.

### CVE-2026-120821

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T21:19:01.090 |

A use-after-free in the aggregation framework of MongoDB Server can occur when certain expressions are evaluated in an aggregation sub-pipeline. The condition can be caused by an authenticated user with read privileges, and may result in the server terminating unexpectedly.

### CVE-2026-120818

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T21:19:00.283 |

A use-after-free weakness in MongoDB Server's server-side JavaScript support for aggregation may allow a stale reference to previously freed process memory to be read and returned. An authenticated user with minimal or no assigned roles can trigger this condition over the normal network protocol by submitting a single crafted aggregation request, with no additional privileges or non-default configuration. Successful triggering this issue may result in adjacent process memory contents being returned, including data that undermines memory-layout randomization, and may in some cases affect server availability.

### CVE-2026-120817

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T21:19:00.130 |

A race condition in the schema validation component of MongoDB Server can occur when concurrent writes are checked against a collection validator that uses geospatial query operators. The condition can be caused by an authenticated user with write privileges, and may result in the server terminating unexpectedly.

### CVE-2026-110091

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T21:18:20.427 |

Premiere Pro is affected by a Missing Authentication for Critical Function vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-110090

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T21:18:20.270 |

Premiere Pro is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-120977

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-11-10T20:18:52.800 |

On affected platforms running Arista EOS with 802.1X with Dynamic Host Configuration Protocol (DHCP) device profiling enabled, a network-adjacent attacker can send a crafted DHCP packet to force the device to record a spoofed device profile. This may potentially allow the authenticated supplicant to acquire unauthorized access to a network segment with elevated privileges.

### CVE-2026-120810

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-10T20:18:51.473 |

An issue in MongoDB server’s aggregation framework allows an authenticated user with read privileges to cause a denial of service by sending specially crafted aggregate commands using an internal expression. Despite its internal naming, this expression is registered as accessible to any authenticated client. By supplying crafted input parameters across multiple concurrent connections, each evaluation triggers unbounded memory allocations with no per-expression memory limits enforced. This can exhaust available server memory and cause the mongod process to be terminated by the operating system’s out-of-memory killer.

### CVE-2026-120803

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T20:18:50.420 |

A use-after-free issue exists in MongoDB’s SBE (Slot-Based Execution) implementation of a window function accumulator used by certain $setWindowFields aggregation pipelines. Under specific conditions, the accumulator can retain a dangling pointer to memory that has since been freed. When this stale pointer is later dereferenced during serialization of the carried-forward value, it can result in a heap out-of-bounds read that may expose adjacent heap contents and crash the mongod server. An authenticated user with readWrite privileges on a database can trigger this issue by crafting a specific aggregation pipeline.

### CVE-2026-104060

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T20:17:23.897 |

Worklenz before 3.3.0 contains an SQL injection vulnerability in the reporting members endpoints that allows authenticated attackers to read arbitrary database contents by injecting SQL through the projects and status parameters. Attackers can send crafted values to POST /api/v1/reporting/members/all or GET /api/v1/reporting/members/export, which are interpolated unparameterized into IN clauses in getTeamMemberInsightData, and use time-based blind techniques to extract data across tenants, including user password hashes.

### CVE-2026-119988

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-11-10T19:20:23.937 |

Numeric truncation error in Windows SMB allows an authorized attacker to execute code over a network.

### CVE-2026-118208

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-10T19:19:37.800 |

Improper access control in Microsoft Exchange Server allows an authorized attacker to perform spoofing over a network.

### CVE-2026-112973

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-10T19:18:48.100 |

Improper access control in Windows Kernel allows an authorized attacker to bypass a security feature locally.

### CVE-2026-44382

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T18:17:39.720 |

Out-of-bounds read for some Intel(R) Wireless Bluetooth(R) within Ring 0: Kernel may allow a denial of service. Network adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-42956

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T18:17:39.493 |

Out-of-bounds write for some Intel(R) Wireless Bluetooth(R) within Ring 0: Kernel may allow a denial of service. Network adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-82518

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T17:17:48.770 |

Akamai CLI before 2.0.6 contains a path traversal vulnerability that allows malicious packages to write files outside the install directory via unvalidated commands[].name values in cli.json. Attackers who convince victims to install or update a package can use '..' segments to overwrite executables on the user's PATH, persisting after uninstall.

### CVE-2026-125754

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-10T16:17:22.493 |

Dolibarr 20.0.0 through 23.0.4 and 24.x before 24.0.2 contains an insecure direct object reference vulnerability in api_expensereports.class.php payment endpoints that lets authenticated users access other users' expense report payments. Attackers with only expense report read and create rights can call getAllPayments, getPayments, addPayment, or updatePayment to read, create, or modify payments, falsifying reimbursement state.

### CVE-2026-125750

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T16:17:21.070 |

Firekylin through 2.18.1 contains an improper authorization vulnerability that allows editor-role users to read administrator-only secrets because the admin API base guard permits all GET actions. Editors can query options.js for TOTP secrets, push credentials, and cloud storage keys, or user.js for other users' app_key/app_secret to publish posts as administrators via admin/post_push.

### CVE-2026-126611

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-11T09:17:12.973 |

Progressive Robot hMailServer 6.3.4 through 6.3.7, with a MySQL or MariaDB database, TlsMode=verify-full and no TlsCaFile, does not verify the database server's certificate's issuer or name when the connection is one that MariaDB Connector/C treats as local - Server= set to 127.0.0.1, ::1 or localhost (on Linux a Unix socket), to . on Windows (a named pipe), or to a comma-separated list of servers that holds such an element - which allows a local attacker who can stand in for the database server, for example by listening on its port while it is stopped or restarting, to receive the database sign-in, the password included, and to read and modify the traffic between hMailServer and its database. hMailServer applied verify-full by turning the client's certificate verification on without a CA file, but MariaDB Connector/C 3.4.1 and later, on a connection they treat as local and with no CA file, accept any certificate within its validity period that is self-signed or sent with its own root, for any name (Connector/C 3.4.2 to 3.4.10 also one whose issuer they cannot find), so the client accepted the certificate an impostor made, asked no proof of the password and allowed a switch to an authentication method that sends the password unhashed, while hmailserver --check-database said the certificate had been checked against the system's trust store and the application log that it had been checked. The Windows builds bundle Connector/C 3.4.9 (6.3.4 to 6.3.6) and 3.4.11 (6.3.7); on Linux the distribution's client is used, and Connector/C 3.3 and 3.4.0 and Oracle's MySQL client are not affected. The configuration is not the default: TlsMode defaults to prefer, which checks no certificate.

### CVE-2026-118368

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-11T05:19:27.373 |

Akaunting 3.3.0 contains a stored cross-site scripting vulnerability in the XLSX item-import workflow. An authenticated Manager can import an item whose name contains HTML. When another authenticated user selects that item while creating a document, Akaunting places the stored name in an invoice or bill line item through Vue v-html, causing attacker-controlled markup to execute in the victim's Akaunting origin.

### CVE-2026-126570

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:N/VI:L/VA:H/SC:N/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-11-11T03:16:51.627 |

Padloc 4.0.0 before 4.3.1 contains a prototype pollution vulnerability that allows SCIM token holders to modify Object.prototype by sending crafted SCIM PATCH paths to ScimServer._handleScimUsersPatch(). Attackers can supply paths like __proto__.x or constructor.prototype.x passed to setPath() to pollute the shared server process, disrupting requests for all other organizations.

### CVE-2026-120976

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-10T20:18:52.660 |

On affected platforms running Arista EOS with IEEE 802.1X authentication and MACsec using dynamically derived keys, sensitive authentication information may be recorded in diagnostic data during a Smart Switch Upgrade (SSU).

An attacker with administrative access on the device who obtains the affected diagnostic data could recover sensitive authentication information. This could potentially compromise the confidentiality and integrity of traffic protected by MACsec on the affected link.

The vulnerability is only exposed during and after an SSU reload where an active 802.1X session used for MACsec is present.

### CVE-2026-120806

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-459` |
| Published | 2026-11-10T20:18:50.880 |

A flaw in MongoDB Server's user management commands may lead to incomplete cleanup of role authorization data when roles are dropped from a database. Due to incorrect internal query predicates, the drop operation removes role definitions but fails to remove stale references in user and role documents. If a role with the same name is subsequently recreated with different privileges, previously associated users may silently inherit the new role's privileges without an explicit grant or corresponding audit event. Exploitation requires authenticated access with database administrative privileges on the target database.

### CVE-2026-115538

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-10T20:18:03.747 |

Moby's overlay network driver does not restore the iptables rules for encrypted overlay networks after firewalld deletes them. Unlike other Docker Engine networking components, the overlay driver does not handle firewalld reload or start signals over D-Bus. The missing rules cause outgoing VXLAN datagrams to bypass IPsec encryption and remove the protection against incoming cleartext VXLAN traffic. The condition is not logged by dockerd and persists until the encrypted network's last local endpoint is removed and another is added, or dockerd is restarted. Each further firewalld event repeats the condition.

### CVE-2026-97000

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-10T19:22:22.993 |

Null pointer dereference in Windows USM Communication Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-96994

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:22:22.810 |

Use after free in Winsock allows an authorized attacker to elevate privileges locally.

### CVE-2026-96978

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:22:20.370 |

Use after free in Windows Credential User Interface allows an authorized attacker to elevate privileges locally.

### CVE-2026-96973

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:22:19.620 |

Use after free in Windows Encrypting File System (EFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-96971

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:22:19.267 |

Use after free in Windows NetBIOS allows an authorized attacker to elevate privileges locally.

### CVE-2026-96969

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:22:18.973 |

Double free in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-96171

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:22:16.997 |

Use after free in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96168

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:22:13.980 |

Untrusted pointer dereference in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96158

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-908` |
| Published | 2026-11-10T19:22:13.210 |

Use of uninitialized resource in Microsoft ActiveX Installer Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96155

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:22:12.637 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96153

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:22:12.447 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-96139

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:22:11.440 |

Untrusted pointer dereference in Windows Kernel-Mode Drivers allows an authorized attacker to elevate privileges locally.

### CVE-2026-96124

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:22:09.813 |

Use after free in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96107

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-10T19:22:08.830 |

Null pointer dereference in Windows Phone Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96097

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-11-10T19:22:08.170 |

Release of invalid pointer or reference in Windows Brokering File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-96088

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:22:07.670 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Connected User Experiences and Telemetry allows an authorized attacker to elevate privileges locally.

### CVE-2026-96075

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:22:05.563 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Feedback Hub allows an authorized attacker to elevate privileges locally.

### CVE-2026-96073

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:22:05.163 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96072

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:22:04.973 |

Use after free in Windows Connected User Experiences and Telemetry allows an authorized attacker to elevate privileges locally.

### CVE-2026-96061

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:22:04.093 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96054

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:22:02.743 |

Heap-based buffer overflow in Microsoft Color Management allows an unauthorized attacker to execute code locally.

### CVE-2026-96051

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:22:02.177 |

Out-of-bounds read in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96047

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:22:01.740 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96046

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:22:01.517 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96043

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:22:01.267 |

Use after free in Windows Connection Manager Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96042

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:22:01.070 |

Use after free in Windows Connection Manager Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96035

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:22:00.113 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96027

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:21:59.353 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96026

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:21:59.160 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96019

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-822` |
| Published | 2026-11-10T19:21:58.467 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96008

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:21:57.573 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96007

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:21:57.390 |

Use after free in Connected Devices Platform Service (Cdpsvc) allows an authorized attacker to elevate privileges locally.

### CVE-2026-96004

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:21:57.007 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-95989

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:21:55.507 |

Use after free in vhdmp.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-95987

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:55.117 |

Use after free in Windows User Manager Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-95979

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:54.697 |

Use after free in Windows Brokering File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-95976

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:21:54.347 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Diagnostic Policy Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-95974

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:53.980 |

Heap-based buffer overflow in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95973

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:21:53.800 |

Untrusted pointer dereference in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95971

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:21:53.610 |

Untrusted pointer dereference in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95968

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:21:53.417 |

Use after free in Windows Smart Card allows an authorized attacker to elevate privileges locally.

### CVE-2026-95966

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:21:53.240 |

Use after free in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95961

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:21:50.587 |

Double free in Windows USB Video Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-95950

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:21:47.520 |

Out-of-bounds read in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95938

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:46.417 |

Heap-based buffer overflow in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95923

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:45.463 |

Heap-based buffer overflow in Windows HTTP.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-95922

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:45.267 |

Heap-based buffer overflow in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95906

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-362` |
| Published | 2026-11-10T19:21:44.073 |

Out-of-bounds read in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95888

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:21:42.040 |

Heap-based buffer overflow in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-95876

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:40.560 |

Use after free in Windows Local Session Manager (LSM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-95871

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-362` |
| Published | 2026-11-10T19:21:39.963 |

Heap-based buffer overflow in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-94529

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-362` |
| Published | 2026-11-10T19:21:38.680 |

Heap-based buffer overflow in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-94525

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-10T19:21:38.227 |

An elevation of privilege vulnerability exists in Windows Error Reporting (WER) when WER handles and executes files. The vulnerability could allow elevation of privilege if an attacker can successfully exploit it.
An attacker who successfully exploited the vulnerability could gain greater access to sensitive information and system functionality. To exploit the vulnerability, an attacker could run a specially crafted application.
The security update addresses the vulnerability by correcting the way that WER handles and executes files.

### CVE-2026-94522

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:37.963 |

Use after free in Kernel Transaction Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-94519

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:21:37.803 |

Use after free in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-94514

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:21:37.170 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-88242

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:33.590 |

Use after free in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-88237

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:21:32.703 |

Use after free in Windows Subsystem for Linux allows an authorized attacker to elevate privileges locally.

### CVE-2026-88228

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-362` |
| Published | 2026-11-10T19:21:31.143 |

Heap-based buffer overflow in Windows Local Security Authority Subsystem Service (LSASS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-88224

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-10T19:21:30.747 |

Improper link resolution before file access ('link following') in Windows AppX Deployment Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-88221

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:29.693 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85862

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-415;CWE-416` |
| Published | 2026-11-10T19:21:25.853 |

Double free in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-83894

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:23.903 |

Use after free in RPC Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-70231

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:20.887 |

Use after free in Windows Local Security Authority Subsystem Service (LSASS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-70120

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:20.560 |

Use after free in Microsoft Bluetooth Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-69565

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:21:19.750 |

Use after free in Remote Desktop Gateway Service allows an authorized attacker to execute code locally.

### CVE-2026-14968

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-10T19:21:14.630 |

EDK2 contains vulnerabilities in
BIOS where skilled and privileged users or attackers may cause “Out-of-bounds Write” by local access. Successful exploitation of this vulnerability could compromise
SMM handler integrity, cause system instability, and lead to denial of service. It could also impact Integrity and Availability.

### CVE-2026-124224

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-10T19:20:48.560 |

Improper link resolution before file access ('link following') in Windows PowerShell allows an authorized attacker to elevate privileges locally.

### CVE-2026-123389

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:42.630 |

Use after free in Quality Windows Audio/Video Experience (QWAVE) service allows an authorized attacker to elevate privileges locally.

### CVE-2026-122182

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-10T19:20:36.073 |

Improper link resolution before file access ('link following') in Windows Maps allows an authorized attacker to elevate privileges locally.

### CVE-2026-122179

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:35.890 |

Heap-based buffer overflow in Windows Internet Connection Sharing (ICS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-122175

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:35.367 |

Use after free in Windows Autopilot allows an authorized attacker to elevate privileges locally.

### CVE-2026-122174

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-10T19:20:35.160 |

Improper link resolution before file access ('link following') in Windows Task Scheduler allows an authorized attacker to elevate privileges locally.

### CVE-2026-122170

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:20:34.350 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-121671

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:30.817 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-121670

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:20:30.593 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-119992

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:20:24.600 |

Double free in Windows HTTP.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-119981

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-10T19:20:23.003 |

Missing authentication for critical function in Visual Studio Code allows an authorized attacker to elevate privileges locally.

### CVE-2026-119974

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-10T19:20:22.480 |

Time-of-check time-of-use (toctou) race condition in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-119931

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-10T19:20:14.880 |

Time-of-check time-of-use (toctou) race condition in Windows Text Services Framework allows an authorized attacker to elevate privileges locally.

### CVE-2026-119928

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:14.497 |

Use after free in Windows PrintWorkflowUserSvc allows an authorized attacker to elevate privileges locally.

### CVE-2026-119921

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:20:14.067 |

Heap-based buffer overflow in Windows Microsoft Account Sign-in Assistant allows an authorized attacker to elevate privileges locally.

### CVE-2026-119919

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:13.847 |

Heap-based buffer overflow in Windows Distributed Transaction Coordinator allows an authorized attacker to elevate privileges locally.

### CVE-2026-119913

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-10T19:20:12.430 |

Improper link resolution before file access ('link following') in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-119898

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-10T19:20:10.010 |

Null pointer dereference in Windows PrintWorkflowUserSvc allows an authorized attacker to elevate privileges locally.

### CVE-2026-119895

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:09.850 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119894

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:09.703 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119893

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:20:09.560 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119888

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:08.803 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119876

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:20:07.073 |

Heap-based buffer overflow in Windows USB Scanner Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-119874

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:06.740 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119873

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:06.560 |

Use after free in Windows NetBIOS allows an authorized attacker to elevate privileges locally.

### CVE-2026-119870

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:20:06.043 |

Untrusted pointer dereference in Windows SMB Client allows an authorized attacker to elevate privileges locally.

### CVE-2026-119868

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:20:05.743 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-119866

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:20:05.380 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119865

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:20:05.180 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-119861

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:04.803 |

Heap-based buffer overflow in Windows Internet Connection Sharing (ICS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-119860

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:04.617 |

Use after free in Windows Internet Connection Sharing (ICS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-119859

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:04.473 |

Use after free in Windows Internet Connection Sharing (ICS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-119851

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-10T19:20:02.457 |

Time-of-check time-of-use (toctou) race condition in Windows Storage Spaces Controller allows an authorized attacker to elevate privileges locally.

### CVE-2026-119849

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:20:02.250 |

Stack-based buffer overflow in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to execute code locally.

### CVE-2026-119844

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:20:01.513 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119835

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:59.210 |

Use after free in Windows Smart Card allows an authorized attacker to elevate privileges locally.

### CVE-2026-119833

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:19:58.860 |

Untrusted pointer dereference in Windows Message Queuing allows an authorized attacker to elevate privileges locally.

### CVE-2026-119831

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:19:58.460 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-119827

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-10T19:19:57.903 |

Missing authorization in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-119822

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-497` |
| Published | 2026-11-10T19:19:56.907 |

Exposure of sensitive system information to an unauthorized control sphere in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-119405

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:55.833 |

Use after free in Windows Backup Engine allows an authorized attacker to elevate privileges locally.

### CVE-2026-119403

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:55.490 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119402

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:55.330 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119401

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:55.180 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119399

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367;CWE-415` |
| Published | 2026-11-10T19:19:54.987 |

Double free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-119398

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-10T19:19:54.800 |

Improper access control in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-119397

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:54.607 |

Use after free in Kernel Transaction Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-119389

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:53.163 |

Use after free in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-119388

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:52.977 |

Use after free in Quality Windows Audio/Video Experience (QWAVE) service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119387

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:52.797 |

Use after free in Quality Windows Audio/Video Experience (QWAVE) service allows an authorized attacker to elevate privileges locally.

### CVE-2026-119386

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:52.630 |

Use after free in Windows Resilient File System (ReFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-118288

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-10T19:19:42.287 |

Incorrect permission assignment for critical resource in Azure File Sync allows an authorized attacker to elevate privileges locally.

### CVE-2026-118125

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:19:31.423 |

Use after free in Windows Message Queuing allows an authorized attacker to elevate privileges locally.

### CVE-2026-118124

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-10T19:19:31.233 |

Out-of-bounds read in Windows Internet Connection Sharing (ICS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-118123

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:19:31.043 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Point-to-Point Protocol over Ethernet (PPPoE) allows an authorized attacker to elevate privileges locally.

### CVE-2026-118116

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-10T19:19:30.263 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-116707

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:12.660 |

Use after free in Windows Link Layer Topology Discovery Protocol allows an authorized attacker to elevate privileges locally.

### CVE-2026-113860

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:06.637 |

Use after free in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-113842

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:05.040 |

Use after free in Windows Security Center allows an authorized attacker to elevate privileges locally.

### CVE-2026-113820

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:02.173 |

Use after free in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-113819

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:19:01.930 |

Use after free in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-113770

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:18:56.690 |

Untrusted pointer dereference in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-113769

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:18:56.470 |

Use after free in Windows COM+ Event System Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-113762

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:55.153 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-113761

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-822` |
| Published | 2026-11-10T19:18:55.013 |

Untrusted pointer dereference in Windows Container Isolation FS Filter Driver (unionfs.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-113755

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:53.853 |

Use after free in Windows Filter Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-113751

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-362` |
| Published | 2026-11-10T19:18:53.170 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Fast FAT Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-113750

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:52.980 |

Heap-based buffer overflow in Windows Device Inventory allows an authorized attacker to elevate privileges locally.

### CVE-2026-112989

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-10T19:18:51.710 |

Untrusted pointer dereference in Servicing Stack Updates allows an authorized attacker to elevate privileges locally.

### CVE-2026-112987

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-10T19:18:51.293 |

Integer overflow or wraparound in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-112986

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:18:51.127 |

No cwe for this issue in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-112976

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:18:49.247 |

Use after free in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-112971

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:47.667 |

Heap-based buffer overflow in Windows SMB Client allows an authorized attacker to elevate privileges locally.

### CVE-2026-112970

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:47.487 |

Use after free in Windows SMB Client allows an authorized attacker to elevate privileges locally.

### CVE-2026-112968

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:47.090 |

Use after free in Windows COM allows an authorized attacker to elevate privileges locally.

### CVE-2026-112812

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:45.967 |

Use after free in Windows SMB Client allows an authorized attacker to elevate privileges locally.

### CVE-2026-112810

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-10T19:18:45.593 |

Time-of-check time-of-use (toctou) race condition in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-112804

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-11-10T19:18:43.017 |

Heap-based buffer overflow in Windows exFAT File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-112800

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:42.343 |

Heap-based buffer overflow in Windows Diagnostic Policy Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-112798

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:41.987 |

Use after free in Windows NetBIOS allows an authorized attacker to elevate privileges locally.

### CVE-2026-112797

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:18:41.807 |

Use after free in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-112796

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:18:41.623 |

Double free in Windows Event Collector Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-112792

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:40.820 |

Use after free in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-112791

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367;CWE-416` |
| Published | 2026-11-10T19:18:40.633 |

Time-of-check time-of-use (toctou) race condition in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-112790

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:40.447 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-112766

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:40.060 |

Use after free in Windows exFAT File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-112765

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-11-10T19:18:39.860 |

Heap-based buffer overflow in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-112764

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:39.680 |

Use after free in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-112763

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:39.517 |

Use after free in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-112761

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:39.163 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-112759

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:38.190 |

Heap-based buffer overflow in Windows Task Scheduler allows an authorized attacker to elevate privileges locally.

### CVE-2026-112756

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:36.680 |

Use after free in Windows Filtering Platform (WFP) allows an authorized attacker to elevate privileges locally.

### CVE-2026-112753

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-10T19:18:35.947 |

Access of resource using incompatible type ('type confusion') in Windows Container Isolation FS Filter Driver (unionfs.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-108414

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:12.180 |

Use after free in Windows Projected File System Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-108413

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:11.990 |

Use after free in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-108406

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:09.523 |

Use after free in Windows Network Connection Broker allows an authorized attacker to elevate privileges locally.

### CVE-2026-105734

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-10T19:18:02.433 |

Incorrect permission assignment for critical resource in Azure Local allows an authorized attacker to elevate privileges locally.

### CVE-2026-105589

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:18:02.070 |

Use after free in Windows Wireless Networking allows an authorized attacker to elevate privileges locally.

### CVE-2026-105587

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:18:01.710 |

Heap-based buffer overflow in Windows OLE DB allows an authorized attacker to elevate privileges locally.

### CVE-2026-105586

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-10T19:18:01.517 |

Null pointer dereference in Microsoft Windows SCSI Class System File allows an authorized attacker to elevate privileges locally.

### CVE-2026-105583

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-11-10T19:18:01.180 |

Release of invalid pointer or reference in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-105582

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-11-10T19:18:01.000 |

Release of invalid pointer or reference in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-105574

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:17:59.970 |

Use after free in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-105567

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:17:59.430 |

Use after free in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-105566

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-415` |
| Published | 2026-11-10T19:17:59.237 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-105565

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-11-10T19:17:59.087 |

Use after free in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-105554

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-10T19:17:57.863 |

Heap-based buffer overflow in Windows Background Intelligent Transfer Service (BITS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-105553

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-10T19:17:57.670 |

Stack-based buffer overflow in Windows Filtering Platform (WFP) allows an authorized attacker to elevate privileges locally.

### CVE-2026-105547

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-415` |
| Published | 2026-11-10T19:17:56.900 |

Double free in Windows Setup and Deployment allows an authorized attacker to elevate privileges locally.

### CVE-2026-105546

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:17:56.710 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Management Instrumentation allows an authorized attacker to elevate privileges locally.

### CVE-2026-105545

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-415` |
| Published | 2026-11-10T19:17:56.503 |

An elevation of privilege vulnerability exists in the Windows Installer when the Windows Installer fails to properly sanitize input leading to an insecure library loading behavior.
A locally authenticated attacker could run arbitrary code with elevated system privileges. An attacker could then install programs; view, change, or delete data; or create new accounts with full user rights.
The security update addresses the vulnerability by correcting the input sanitization error to preclude unintended elevation.

### CVE-2026-105540

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-669` |
| Published | 2026-11-10T19:17:55.580 |

Incorrect resource transfer between spheres in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-105533

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-763` |
| Published | 2026-11-10T19:17:53.923 |

Release of invalid pointer or reference in Windows COM allows an authorized attacker to elevate privileges locally.

### CVE-2026-105529

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-10T19:17:52.573 |

Weak authentication in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-105526

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:17:51.890 |

Double free in Winsock allows an authorized attacker to elevate privileges locally.

### CVE-2026-105525

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-416` |
| Published | 2026-11-10T19:17:51.693 |

Integer overflow or wraparound in Windows Network Connection Broker allows an authorized attacker to elevate privileges locally.

### CVE-2026-105522

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:17:51.310 |

Use after free in Winlogon allows an authorized attacker to elevate privileges locally.

### CVE-2026-105513

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-11-10T19:17:50.523 |

An elevation of privilege vulnerability exists in the way that the Windows Kernel handles objects in memory. An attacker who successfully exploited the vulnerability could execute code with elevated permissions.
To exploit the vulnerability, a locally authenticated attacker could run a specially crafted application.
The security update addresses the vulnerability by ensuring the Windows Kernel properly handles objects in memory.

### CVE-2026-105511

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:17:50.053 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Point-to-Point Protocol over Ethernet (PPPoE) allows an authorized attacker to elevate privileges locally.

### CVE-2026-105510

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:17:49.850 |

Use after free in Windows Secure Socket Tunneling Protocol (SSTP) allows an authorized attacker to elevate privileges locally.

### CVE-2026-105509

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-11-10T19:17:49.687 |

Use after free in Windows Resilient File System (ReFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-105504

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:17:48.673 |

An elevation of privilege vulnerability exists in the way that the Windows Kernel handles objects in memory. An attacker who successfully exploited the vulnerability could execute code with elevated permissions.
To exploit the vulnerability, a locally authenticated attacker could run a specially crafted application.
The security update addresses the vulnerability by ensuring the Windows Kernel properly handles objects in memory.

### CVE-2026-105024

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:17:43.283 |

Use after free in Windows Storage Spaces Controller allows an authorized attacker to elevate privileges locally.

### CVE-2026-105017

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-10T19:17:41.733 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Volume Shadow Copy allows an authorized attacker to elevate privileges locally.

### CVE-2026-103571

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-10T19:17:41.037 |

An elevation of privilege vulnerability exists when the Windows Cryptography Next Generation (CNG) Key Isolation service improperly handles memory. An attacker who successfully exploited this vulnerability could run processes in an elevated context.
To exploit this vulnerability, an attacker would first have to gain execution on the victim system. An attacker could then run a specially crafted application to elevate privileges.
The security update addresses the vulnerability by correcting how the Windows CNG Key Isolation Service handles memory.

### CVE-2026-100204

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-10T19:17:39.033 |

Use after free in HEIF Image Extensions allows an unauthorized attacker to execute code locally.

### CVE-2026-111729

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-10T17:17:20.353 |

In Kura versions <= 5.6.2, the "Command" file-upload handler at `POST /admin/denali/file/command` extracts a client-supplied ZIP archive into the configured `command.working.directory`. The path-containment check `validateFileName()` compares canonical paths with `String.startsWith()` without appending a trailing path separator, so an entry that canonicalises to a sibling directory sharing the same string prefix (e.g. `/tmpevil/x` when the intended directory is `/tmp`) is accepted. The handler then calls `parent.mkdirs()` and `new FileOutputStream(newFile)`, creating directories and writing attacker-controlled bytes outside the intended extraction root.



The command service is disabled by default since Kura 4.0.0 [1]. The issue does not apply when the command service is disabled. The caller must be authenticated with `rest.command` permission.

### CVE-2026-114359

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-10T15:17:12.933 |

Eclipse Kura downloads deployment packages (DPs) from a remote URL without any limit on the size of the data it receives. A malicious or compromised HTTP(S) server, or an attacker able to tamper with a plain-HTTP download, can stream an arbitrarily large (or endless) response. Kura writes the response to local storage until the filesystem is full. On gateways the temporary directory is often a RAM-backed tmpfs, so this can also exhaust memory. The result is denial of service of the device: failed configuration persistence, failed logging and possible crashes of the framework or other services.



The same missing size limit is present in the REST upload endpoint `POST /deploy/v2/_upload`, which copies the request body to the temporary directory with no limit.



Workarounds: only install DPs from trusted HTTPS sources, restrict who can install packages (Web UI `kura.packages.admin` permission, REST `kura.permission.rest.deploy`, cloud DEPLOY-V2 access).
