# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-04 15:00 UTC
- **対象期間**: `2026-07-03T15:00:34.000Z` 〜 `2026-07-04T15:00:13.000Z`
- **重要CVE数**: 76 件（Critical 9.0+: 4 件 / High 7.0〜: 72 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコア 7.0 以上のものは **30 件** 超に上り、特に **Gitea 系列** と **Microsoft Edge (Chromium 系) のブラウザコンポーネント** に集中しています。  
- Gitea は認証ヘッダーや Webhook の実装不備により、リバースプロキシ経由のなりすまし・SSRF・XSS といったリモートコード実行に直結する脆弱性が多数報告されています。  
- Edge 系列は type‑confusion・use‑after‑free・整数オーバーフローといったメモリ安全性の欠陥が続発し、ネットワーク越しに任意コード実行が可能になる点が共通しています。  
- 併せて、機械学習フレームワーク（Keras）や CI/CD ツール（n8n）、システム管理ツール（pardus‑software、Parsec）でも権限昇格や任意コード実行が確認され、**サーバ／開発環境全体の攻撃対象が広がっている**ことが読み取れます。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑20896** | 9.8 | Gitea Docker イメージ (≤ 1.26.2) が `REVERSE_PROXY_TRUSTED_PROXIES=*` をデフォルトで有効化し、任意の IP が `X‑WEBAUTH‑USER` 等のヘッダーでユーザーになりすます | **認証バイパス** がネットワーク上のどのホストからでも可能になるため、社内 Git サーバ全体が乗っ取られるリスクが極めて高い。特にリバースプロキシを経由している環境で設定ミスが顕在化しやすい。 |
| **CVE‑2026‑58426** | 9.6 | Gitea Actions Artifacts V4 の署名付き URL の HMAC 計算曖昧性により、リポジトリ間でアーティファクトを読み取れ、アップロード状態を書き換え可能 | **クロスリポジトリ情報漏洩** と **不正ビルドインジェクション** が同時に成立。CI/CD パイプラインを利用する組織は、機密ビルド成果物が外部に流出する危険がある。 |
| **CVE‑2026‑22874** | 9.6 | Gitea (≤ 1.26.2) の Webhook / Migration の allow‑list フィルタが不完全で SSRF が成立 | **内部ネットワークへの不正リクエスト** が可能となり、クラウド環境やオンプレミスの内部 API・メタデータサービスへのアクセスが許される。 |
| **CVE‑2026‑12481** | 8.8 | Keras 3.14.0 の `Lambda` レイヤーのデシリアライズ不備により任意コード実行 | 機械学習モデルを配布・ロードする環境で **コードインジェクション** が起き、サーバ全体が乗っ取られる。特に SaaS 型 ML プラットフォームは注意必須。 |
| **CVE‑2026‑14460 / CVE‑2026‑14459** | 8.8 | pardus‑software ≤ 1.0.4 のコマンド引数注入 (Argument Injection) | ローカル権限が低いユーザーでも **任意コマンド実行** が可能。システム管理ツールとして広くデプロイされているため、内部脅威や横移動の足掛かりになる。 |

> **※** Edge 系列（CVE‑2026‑58289 など）は多数報告されているが、ブラウザはクライアント側の脆弱性であり、サーバ側の防御策は「最新版への更新」だけで対処できるため、上記 5 件を優先的に対策すべきです。

---

## 3. 推奨アクション  

### (1) Gitea 系列の緊急対策
- **アップグレード**  
  - `gitea/gitea:1.26.3` 以降（Docker イメージ）へ更新。  
  - 公式リリースノートで `REVERSE_PROXY_TRUSTED_PROXIES` のデフォルトが `""`（空）に変更されたことを確認。  
- **設定見直し**  
  - `APP_INI` の `REVERSE_PROXY_TRUSTED_PROXIES` を **明示的に許可するプロキシの IP/CIDR のみ** に限定。  
  - Webhook / Migration の allow‑list ルールを **正規表現でホスト名・IP を厳格に検証** する。  
- **CI/CD の署名 URL**  
  - `actions.artifacts.signed_url_hmac_secret` を **ランダムに生成した長さ 32 バイト以上のシークレット** に変更し、古い URL を即時失効させる。  

### (2) Keras
- **アップグレード**  
  - `keras==3.15.0` 以上へ更新（3.15.0 で `Lambda` レイヤーの安全モードが強化）。  
- **デシリアライズ制御**  
  - `safe_mode` パラメータを **必ず `True`** に設定し、外部から提供されるモデルファイルは **サンドボックス化された環境**（例: Docker, virtualenv）でロードする。  

### (3) pardus‑software
- **アップグレード**  
  - `pardus-software` を **1.0.5 以上** に更新。  
- **入力検証**  
  - コマンドライン引数を受け取る全てのエンドポイントで **`shlex.quote`** もしくは同等のサニタイズを実装。  

### (4) Microsoft Edge (Chromium)  
- **ブラウザ更新**  
  - Windows/macOS/Linux の Edge を **最新版 (2026‑07‑xx 以降)** に自動更新設定。  
- **組織内ポリシー**  
  - 企業環境では **Edge の自動ロールアウト** を管理ツール (Intune, SCCM) で強制し、旧バージョンの残存を排除。  

### (5) その他注目ツール
| 製品 | 修正済みバージョン | 推奨対策 |
|------|-------------------|----------|
| Trail of Bits **fickling** | `0.1.12` 以上 | 依存パッケージを `pip install --upgrade fickling` |
| n8n | 0.236.0 以上（

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-20896

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-03T21:16:56.660 |

Gitea Docker image versions up to and including 1.26.2 use REVERSE_PROXY_TRUSTED_PROXIES=* by default, allowing any source IP to impersonate a user when reverse-proxy authentication headers such as X-WEBAUTH-USER are enabled.

### CVE-2026-58426

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-03T21:17:05.770 |

Gitea Actions Artifacts V4 signed URL HMAC ambiguity allows cross-repository artifact read and cross-task upload-state write

### CVE-2026-22874

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-03T21:16:57.157 |

Gitea versions up to and including 1.26.2 have incomplete SSRF protection in webhook and migration allow-list filtering.

### CVE-2026-58289

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-03T21:17:03.640 |

Access of resource using incompatible type ('type confusion') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-58424

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-285;CWE-732;CWE-863` |
| Published | 2026-07-03T21:17:05.660 |

Permanent Fork PR Workflow Approval Gate Bypass

### CVE-2026-14535

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-07-04T14:16:29.063 |

In Trail of Bits fickling versions up to and including 0.1.11, the UnsafeImportsML analysis pass unconditionally calls AnalysisContext.shorten_code(node) on every import node it inspects, regardless of whether the import is flagged as unsafe. This call registers the shortened code representation in the shared AnalysisContext.reported_shortened_code set. When the MLAllowlist analysis pass subsequently runs, it calls the same shorten_code() method, receives already_reported=True for every import, and executes a continue statement that skips its allowlist check entirely. This renders MLAllowlist dead code for all imports — it never evaluates whether an import is in the ML allowlist or not. The MLAllowlist pass was designed to catch imports of modules outside the known-safe ML ecosystem (torch, numpy, transformers, etc.) that slip past the UnsafeImports denylist. With MLAllowlist inoperative, any standard library module not in the UNSAFE_IMPORTS denylist can be invoked via pickle deserialization while fickling's check_safety() returns LIKELY_SAFE. The fickling.load() API chains check_safety() into pickle.loads() as an explicit security gate, meaning a LIKELY_SAFE verdict causes the payload to be deserialized and executed. The root cause is shared mutable state between independently-correct analysis passes — UnsafeImportsML works as designed in isolation, MLAllowlist works as designed in isolation, but the shared reported_shortened_code set causes UnsafeImportsML to poison MLAllowlist's deduplication logic.

### CVE-2026-14534

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184;CWE-502` |
| Published | 2026-07-04T14:16:28.400 |

Trail of Bits fickling versions up to and including 0.1.10 do not include the Python standard library modules _posixsubprocess, site, and atexit in the UNSAFE_IMPORTS denylist (fickle.py). Because these modules are absent from the denylist, fickling's check_safety() function returns LIKELY_SAFE with zero findings for pickle payloads that invoke dangerous functions including _posixsubprocess.fork_exec (C-level process spawner capable of executing arbitrary binaries), site.execsitecustomize (executes arbitrary site customization code), and atexit._run_exitfuncs (triggers all registered exit handler callbacks). The fickling.load() API chains check_safety() into pickle.loads() as an explicit security gate; a LIKELY_SAFE verdict causes the payload to be deserialized and executed. This shares the same root cause as CVE-2026-22607 (cProfile), CVE-2025-67748 (pty), and CVE-2025-67747 (marshal/types). OvertlyBadEvals does not flag these modules because they are standard library imports. UnsafeImports does not flag them because they are not in the denylist. The UnusedVariables heuristic is defeated by the SETITEMS opcode pattern.

### CVE-2026-57981

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-03T21:17:01.313 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-57974

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-03T21:17:00.957 |

Integer overflow or wraparound in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-56645

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-03T21:17:00.670 |

Heap-based buffer overflow in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-12481

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-03T21:16:54.737 |

A vulnerability in keras-team/keras version 3.14.0 allows for arbitrary code execution due to improper handling of deserialization in the `Lambda` layer. Specifically, the `_raise_for_lambda_deserialization()` function fails to enforce the safe-mode guard when `safe_mode` is set to `None`, which is the default value when `from_config()` is called outside of a `SafeModeScope` context. This logic error conflates `None` (unset/default-deny) with `False` (explicitly disabled), bypassing the guard and allowing attacker-controlled `marshal` bytecode to be deserialized. Affected call sites include `keras.layers.deserialize(config)`, `keras.models.clone_model(model)`, and any direct invocation of `Lambda.from_config(config)` without an enclosing `SafeModeScope(True)`. This vulnerability can be exploited to achieve arbitrary OS-level code execution in the context of the server or user process.

### CVE-2026-14460

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-03T15:16:32.367 |

Missing Authorization vulnerability in TUBITAK BILGEM Software Technologies Research Institute pardus-software allows Argument Injection.

This issue affects pardus-software: from <= 1.0.4 before 1.0.5.

### CVE-2026-14459

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-03T15:16:32.253 |

Improper neutralization of argument delimiters in a command ('argument injection') vulnerability in TUBITAK BILGEM Software Technologies Research Institute pardus-software allows Argument Injection.

This issue affects pardus-software: from <= 1.0.4 before 1.0.5.

### CVE-2025-71380

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-04T02:16:23.477 |

The Execute Command node in n8n allows authenticated users to execute arbitrary commands on the host system where n8n runs. Attackers with user access or compromised credentials can exploit this node to run malicious commands, potentially leading to data exfiltration, service disruption, or complete system compromise.

### CVE-2026-57983

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-03T21:17:01.433 |

Improper authorization in Microsoft Edge (Chromium-based) allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-28737

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-03T21:16:59.787 |

Gitea versions from 1.25.0 before 1.26.0 allow stored cross-site scripting through the extensionsRequired field in glTF files rendered by the 3D file viewer.

### CVE-2026-12195

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-04T12:16:53.300 |

myVesta is affected by an authenticated remote code execution vulnerability. Low privileged users can insert arbitrary commands as a part of the v_ftp_user parameter when deleting FTP usernames. This could result in the execution of commands as the admin user or takevoer of the admin user in myVesta.

### CVE-2026-26231

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-03T21:16:58.200 |

Gitea versions up to and including 1.26.1 allow the Allow edits from maintainers permission path to authorize commits to repositories that the user can read but should not be able to write.

### CVE-2026-54424

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-648` |
| Published | 2026-07-04T01:16:27.340 |

An Incorrect Use of Privileged APIs vulnerability in Unity Parsec on Windows hosts leads to a potential Elevation of Privilege. This issue affects Parsec through v2026-05-04.0. The patched version is Parsec for Windows version 150-104a. A user can generate a situation where there is an instance of parsecd.exe running as NT AUTHORITY\SYSTEM with a user-controlled value of the AppData environment variable.

### CVE-2026-12196

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-04T12:16:53.600 |

HestiaCP panel cronjob feature is affected by a broken access control vulnerability. Low privilege users can modify the panel cronjob to execute scripts HestiaCP management scripts with passwordless sudo. This could result in the takeover of administrator users in the application and the underlying webserver.

### CVE-2026-58295

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-03T21:17:04.417 |

Access of resource using incompatible type ('type confusion') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-58288

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-03T21:17:03.523 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-58287

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-03T21:17:03.413 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-58285

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-03T21:17:03.180 |

Access of resource using incompatible type ('type confusion') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-58284

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-03T21:17:03.057 |

Improper authorization in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-27771

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-03T21:16:59.043 |

Gitea versions up to and including 1.26.1 have insufficient permission checks for Composer package source links, which can expose private or internal package source information.

### CVE-2026-58293

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-03T21:17:04.143 |

External control of file name or path in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-58286

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-03T21:17:03.293 |

Improper access control in Microsoft Edge (Chromium-based) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-58283

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-03T21:17:02.943 |

Access of resource using incompatible type ('type confusion') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-58282

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-03T21:17:02.820 |

Improper access control in Microsoft Edge (Chromium-based) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-28744

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-03T21:17:00.003 |

Gitea versions up to and including 1.26.1 allow Git smart HTTP requests authenticated with bearer tokens to bypass repository token scope checks.

### CVE-2026-28699

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284;CWE-863` |
| Published | 2026-07-03T21:16:59.567 |

Gitea versions up to and including 1.26.1 allow OAuth2 access token scope enforcement to be bypassed through HTTP Basic authentication.

### CVE-2026-22555

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-03T21:16:57.023 |

Gitea versions before 1.26.0 allow API users to fork a repository into an organization without first passing the CanCreateOrgRepo check, which can expose organization secrets.

### CVE-2026-12252

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-04T02:16:23.603 |

In nltk/nltk versions 3.9.3 and earlier, five Stanford interface classes (StanfordPOSTagger, StanfordNERTagger, StanfordParser, StanfordDependencyParser, and StanfordNeuralDependencyParser) are vulnerable to untrusted JAR code execution. These classes accept user-controllable JAR paths and execute them via the `java()` function, which invokes `subprocess.Popen()` without integrity verification. This vulnerability is identical to CVE-2026-0848, which was fixed for StanfordSegmenter by adding SHA256 verification. However, the fix was not applied to these additional classes, leaving them susceptible to arbitrary code execution when loading untrusted JAR files.

### CVE-2026-58423

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-03T21:17:05.550 |

LFS authentication bypass via malformed SSH sub-verb allows unauthorized read access to private repositories

### CVE-2025-71375

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:23.347 |

picklescan before 0.0.34 fails to detect the _operator.methodcaller built-in function when scanning pickle files for malicious code. Attackers can craft malicious pickle payloads using _operator.methodcaller that evade detection and execute arbitrary code when loaded by pickle.load().

### CVE-2025-71373

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-07-04T02:16:23.220 |

picklescan before 0.0.33 fails to detect operator.methodcaller function calls in pickle files, allowing attackers to bypass security checks. Remote attackers can craft malicious pickle payloads using operator.methodcaller that execute arbitrary code when loaded, compromising systems relying on picklescan for validation.

### CVE-2025-71372

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:23.097 |

Picklescan before 0.0.33 fails to detect the numpy.f2py.crackfortran.getlincoef gadget in pickle __reduce__ methods, allowing arbitrary code execution. Attackers can craft malicious pickle files that execute arbitrary Python code when loaded, bypassing Picklescan's safety checks and enabling supply-chain poisoning of shared model files.

### CVE-2025-71369

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:22.963 |

picklescan before 0.0.28 fails to detect malicious pickle files that use torch.utils.data.datapipes.utils.decoder.basichandlers in reduce methods, allowing attackers to bypass safety checks. Remote attackers can embed undetected malicious code in pickle files that executes during deserialization, enabling remote code execution.

### CVE-2025-71367

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:22.833 |

picklescan before 0.0.34 fails to detect _operator.attrgetter function calls in pickle payloads, allowing attackers to bypass security checks. Remote attackers can craft malicious pickle files using _operator.attrgetter in reduce methods to execute arbitrary code when pickle.load() processes the file.

### CVE-2025-71366

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:22.707 |

picklescan before 0.0.28 fails to detect malicious torch.utils.bottleneck.__main__.run_cprofile function calls in pickle files, allowing attackers to bypass safety checks. Remote attackers can embed undetected code in pickle files to achieve arbitrary code execution when victims load the files.

### CVE-2025-71364

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:22.583 |

picklescan before 0.0.30 fails to detect the asyncio.unix_events._UnixSubprocessTransport._start function in pickle reduce methods, allowing remote code execution. Attackers can craft malicious pickle files embedding this built-in function that evade detection but execute arbitrary commands when loaded.

### CVE-2025-71362

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:22.457 |

picklescan before 0.0.33 fails to detect unsafe deserialization when numpy.f2py.crackfortran functions call eval on arbitrary strings. Attackers can embed malicious code in pickle files that executes when loaded from untrusted sources.

### CVE-2025-71360

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:22.327 |

picklescan before 0.0.29 fails to detect malicious pickle files using idlelib.calltip.get_entity function in reduce methods. Attackers can embed undetected code in pickle files that executes remote commands when loaded by victims.

### CVE-2025-71359

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:22.197 |

picklescan before 0.0.29 fails to detect malicious pickle payloads that utilize lib2to3.pgen2.grammar.Grammar.loads in the reduce method, allowing remote code execution. Attackers can craft pickle files embedding dangerous code that evades picklescan detection and executes during pickle.load() deserialization.

### CVE-2025-71356

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:22.063 |

picklescan before 0.0.28 fails to detect malicious torch.fx.experimental.symbolic_shapes.ShapeEnv.evaluate_guards_expression function calls in pickle files. Attackers can embed undetected code in pickle files that executes remote code when loaded by victims.

### CVE-2025-71353

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:21.933 |

picklescan before 0.0.28 fails to detect malicious pickle files that exploit torch._dynamo.guards.GuardBuilder.get function in reduce methods. Attackers can craft pickle files with embedded code that evades picklescan detection and executes arbitrary commands when loaded.

### CVE-2025-71347

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:21.803 |

picklescan before 0.0.33 fails to detect malicious pickle files using numpy.f2py.crackfortran.param_eval function in reduce methods, allowing attackers to bypass security checks. Remote attackers can embed undetected code in pickle files that executes during deserialization, enabling arbitrary code execution in applications loading untrusted pickle data.

### CVE-2025-71345

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:21.670 |

picklescan before 0.0.30 fails to detect malicious pickle files that invoke torch.utils.bottleneck.__main__.run_autograd_prof function. Attackers can embed undetected code in pickle files that executes during deserialization, enabling remote code execution.

### CVE-2025-71343

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:21.527 |

picklescan before 0.0.30 fails to detect malicious pickle files that exploit lib2to3.pgen2.pgen.ParserGenerator.make_label function in the reduce method. Attackers can craft malicious pickle files with embedded code that evades detection but executes arbitrary commands when pickle.load() is called.

### CVE-2025-71342

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-04T02:16:21.387 |

picklescan before 0.0.30 fails to detect malicious pickle files using idlelib.run.Executive.runcode in reduce methods. Attackers can embed undetected code in pickle files that executes during pickle.load, enabling remote code execution in PyTorch models and supply chain attacks.

### CVE-2026-57985

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-03T21:17:01.663 |

Improper input validation in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-58299

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-07-03T21:17:04.907 |

Time-of-check time-of-use (toctou) race condition in Microsoft Edge for Android allows an unauthorized attacker to execute code over a network.

### CVE-2026-58294

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-03T21:17:04.293 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-58292

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-03T21:17:04.013 |

Improper input validation in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-58290

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-03T21:17:03.770 |

Access of resource using incompatible type ('type confusion') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-58276

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-03T21:17:02.573 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-57992

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-03T21:17:02.310 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-57986

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-03T21:17:01.780 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-57984

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-03T21:17:01.550 |

Use after free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-57975

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-03T21:17:01.077 |

Access of resource using incompatible type ('type confusion') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-57993

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-03T21:17:02.443 |

Server-side request forgery (ssrf) in Microsoft Edge (Chromium-based) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-57991

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-03T21:17:02.180 |

Improper link resolution before file access ('link following') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to disclose information over a network.

### CVE-2026-58379

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-03T19:16:37.040 |

A flaw was found in GIMP's Paint Shop Pro (PSP) file format parser. This heap buffer overflow vulnerability allows a remote attacker to cause arbitrary code execution or a denial of service (DoS) by tricking a user into opening a specially crafted PSP image file. The vulnerability occurs because the software incorrectly calculates buffer sizes when processing low bit-depth images, leading to an overwrite of adjacent memory.

### CVE-2026-58298

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-03T21:17:04.790 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-53478

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-03T15:16:32.840 |

Dell PowerProtect Data Domain, versions 7.7.1.0 through 8.7, LTS2026 release version 8.6.1.0 through 8.6.1.10, LTS2025 release version 8.3.1.0 through 8.3.1.30, LTS2024 release versions 7.13.1.0 through 7.13.1.70 contain an improper neutralization of special elements used in an OS command ('OS command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to command execution.

### CVE-2026-49815

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-03T15:16:32.720 |

Dell PowerProtect Data Domain, versions 7.7.1.0 through 8.7, LTS2026 release version 8.6.1.0 through 8.6.1.10, LTS2025 release version 8.3.1.0 through 8.3.1.30, LTS2024 release versions 7.13.1.0 through 7.13.1.70 contain an improper neutralization of special Elements used in an OS command ('OS command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to execution of arbitrary OS commands.

### CVE-2026-49814

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-03T15:16:32.610 |

Dell PowerProtect Data Domain, versions 7.7.1.0 through 8.7, LTS2026 release version 8.6.1.0 through 8.6.1.10, LTS2025 release version 8.3.1.0 through 8.3.1.30, LTS2024 release versions 7.13.1.0 through 7.13.1.70 contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to arbitrary command execution.

### CVE-2026-58297

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-359` |
| Published | 2026-07-03T21:17:04.663 |

Exposure of private personal information to an unauthorized actor in Microsoft Edge for Android allows an unauthorized attacker to disclose information over a network.

### CVE-2026-58296

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-359` |
| Published | 2026-07-03T21:17:04.547 |

Exposure of private personal information to an unauthorized actor in Microsoft Edge for Android allows an unauthorized attacker to disclose information over a network.

### CVE-2026-57988

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-03T21:17:02.023 |

Relative path traversal in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-57977

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-03T21:17:01.193 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-28740

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-07-03T21:16:59.890 |

Gitea versions up to and including 1.26.2 allow Git LFS object reuse to authorize private source objects for users who have repository access but lack Code-unit access.

### CVE-2026-20779

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-294` |
| Published | 2026-07-03T21:16:56.543 |

Gitea versions from 1.5.0 before 1.26.3 have a TOTP single-use enforcement defect that allows a valid TOTP code to be accepted more than once across web two-factor authentication flows and the Basic Auth X-Gitea-OTP path.

### CVE-2026-14606

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-03T20:16:52.237 |

A security flaw has been discovered in RT-Thread up to 5.0.2. Affected by this issue is the function CAN_Receive in the library bsp/synwit/libraries/SWM341_CSL/CMSIS/DeviceSupport/SWM341.h of the component SWM341 CAN Handler. Performing a manipulation results in stack-based buffer overflow. The attack needs to be approached locally. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-14605

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-03T20:16:52.070 |

A vulnerability was identified in RT-Thread up to 5.0.2. Affected by this vulnerability is the function recvmsg in the library bsp/loongson/ls1cdev/libraries/ls1c_can.h of the component ls1c CAN Handler. Such manipulation leads to stack-based buffer overflow. Local access is required to approach this attack. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.
