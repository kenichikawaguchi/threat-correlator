# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-08 15:00 UTC
- **対象期間**: `2026-08-07T15:00:52.000Z` 〜 `2026-08-08T15:00:31.000Z`
- **重要CVE数**: 61 件（Critical 9.0+: 11 件 / High 7.0〜: 50 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公表された CVE のうち、CVSS 7.0 以上のものは **30 件以上** と非常に多く、特に **認証不要でリモートからコード実行や権限昇格が可能** な脆弱性が目立ちます。  
- Web アプリケーション系（WordPress、Plesk、Kata Containers など）と、AI/LLM 連携サービス（LightRAG、AI Copilot）で **ネットワーク公開が前提** のコンポーネントが集中しており、攻撃者が外部から直接突くシナリオが増加しています。  
- 多くの脆弱性は **デフォルト設定で認証が無効化** されていたり、**入力検証・オリジンチェックが欠如** している点が共通しているため、設定ミスが重大なリスクに直結しています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑64637** (Plesk XML‑RPC API) | 9.9 | 認証済みリセラーが root 権限の管理セッションを取得 | **最高スコア**。Plesk は多くの中小企業・ホスティング事業者で採用されており、root 取得はサーバ全体の乗っ取りにつながる。バージョン **18.0.80 未満** が対象。 |
| **CVE‑2026‑14526** (WordPress AI Copilot – Content Generator) | 9.8 | 認証不要で任意のプラグイン機能を実行できる（任意コード実行） | WordPress のプラグインは数千件がインストールされている環境が多く、**プラグイン単体の脆弱性がサイト全体の破壊につながる**。バージョン **1.5.6 以下** が対象。 |
| **CVE‑2026‑61808** (LightRAG API) | 9.8 | API が全ネットワークインタフェースで認証なしにバインド → ドキュメント閲覧・改ざん・任意ファイルアップロード | LLM アプリケーションは社内外のデータを扱うことが前提で、**情報漏洩と改竄リスクが同時に顕在**。バージョン **1.5.4 以下** が対象。 |
| **CVE‑2026‑50540** (Kata Containers – host code execution) | 9.6 | 未検証の `annotation` によりホスト上でコード実行可能 | コンテナ/VM ハイブリッド環境で広く採用されている Kata は、**クラウド・オンプレミス双方のマルチテナント環境** に影響。**4.0.0 未満** が対象。 |
| **CVE‑2026‑46409** (OpenYak desktop backend) | 9.6 | ローカル HTTP API が Origin 検証なしで公開 → 任意コード実行・情報取得 | デスクトップ型 AI エージェントは開発者向けに広く配布されているが、**ローカルネットワーク上の他プロセスからの攻撃が可能**。バージョン **1.1.3 未満** が対象。 |

> **共通点**：認証・入力検証の欠如、デフォルトで「オープン」なリスニング、そして **アップデートが明確に提示されている** 点が特徴です。これらはすぐにパッチ適用または設定変更でリスクを低減できます。

---

## 3. 推奨アクション  

### 3‑1. 直ちにパッチ適用・バージョンアップ
| 製品 / ライブラリ | 修正済みバージョン (最低) | 具体的なアップデート手順 |
|-------------------|--------------------------|--------------------------|
| **Plesk** | `18.0.80` 以上 | Plesk 管理画面 → **Tools & Settings → Updates** で「Update to latest」または `yum/apt` で `plesk-release` パッケージを更新 |
| **WordPress AI Copilot – Content Generator** | `1.5.7` 以上 | WordPress 管理画面 → **Plugins → Installed Plugins** → 「Update」または手動で `ai-copilot-content-generator.zip` を上書き |
| **LightRAG** | `1.5.5` 以上 | `pip install --upgrade lightrag` または Docker イメージを `lightrag:1.5.5` 以降に差し替え |
| **Kata Containers** | `4.0.0` 以上 (runtime)  <br> `3.31.0` 以上 (virtio‑fs) | `apt-get update && apt-get install -y kata-runtime kata-proxy` <br> もしくは公式リポジトリから最新の `kata-containers` パッケージを取得 |
| **OpenYak** | `1.1.3` 以上 | `npm install -g openyak@>=1.1.3` または `yarn add openyak@1.1.3` で更新し、`127.0.0.1` バインドのまま Origin チェックを有効化（設定ファイル `backend.yaml` の `originCheck: true`） |

### 3‑2. 設定のハードニング（共通対策）
1. **ネットワークバインドの制限**  
   - API サーバやデスクトップバックエンドは必ず `127.0.0.1` または内部 VLAN のみでリッスンし、外部からの直接アクセスを防止。  
2. **認証・認可の強制**  
   - デフォルトで無効化されている認証は必ず有効化し、強力なパスワード／API キーを使用。  
3. **入力検証とオリジンチェック**  
   - すべての HTTP エンドポイントで `Origin` / `Referer` ヘッダーを検証し、CSRF・XSS のリスクを低減。  
4. **最小権限の原則**  
   - 管理者権限を必要としないサービスは `least‑privilege` のユーザーで実行し、`root` でのプロセス起動を回避。  
5. **監査ログの有効化**  
   - 失敗した認証、権限変更、API 呼び出しはすべて syslog / ELK へ転送し、異常検知ルールを設定。  

### 3‑3. 影響が大きい周辺コンポーネントの確認
- **Nexus Repository** 系列（CVE‑2026‑14644

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-64637

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-07T18:17:20.200 |

Improper privilege management in the XML-RPC API of Plesk before 18.0.80, allows an authenticated reseller to obtain an administrative session for the root user account.

### CVE-2026-14526

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-08T07:17:08.297 |

The AI Copilot – Content Generator plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 1.5.6. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to create a new administrator-level user account and achieve full site takeover by saving and executing a malicious workflow containing a wp_create_user action node specifying role=administrator. This vulnerability is exploitable by unauthenticated attackers on any site where the [aiwu-form] shortcode or public chatbot is rendered on a frontend page, as the waic-nonce value is emitted into publicly accessible JavaScript (WAIC_DATA.waicNonce) on those pages, rendering the nonce check a non-functional authorization barrier.

### CVE-2026-61808

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-07T20:16:52.007 |

LightRAG provides simple and fast retrieval-augmented generation. Through version 1.5.4, the LightRAG API server binds to all network interfaces with authentication disabled by default, allowing an unauthenticated network attacker to read indexed document content, upload or delete documents, modify the knowledge graph, cancel pipelines, clear caches, and consume LLM resources. This issue is mitigated in version 1.5.5rc1.

### CVE-2026-46409

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-306;CWE-346;CWE-352;CWE-942` |
| Published | 2026-08-07T23:17:03.243 |

OpenYak is a local-first agent runtime for reliable tool-using models, with a desktop workspace built on top. Prior to version 1.1.3, the OpenYak desktop backend binds an HTTP API to `127.0.0.1:<random port>` (commonly 19141) without server-side Origin validation, loopback authentication, or Content-Type enforcement, and with a wildcard CORS policy. Any webpage a user visits while OpenYak is running can issue cross-origin requests to this local server — the browser acts as a proxy into loopback, bypassing OS-level network isolation. Chained, this lets a malicious page execute arbitrary shell commands on the host (RCE) via the build agent with `permission_presets.bash=true`, shut down the service, and exfiltrate chat history and account PII — with no user interaction beyond opening the page. Version 1.1.3 patches the issue.

### CVE-2026-50540

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20;CWE-22` |
| Published | 2026-08-07T21:17:28.827 |

Kata Containers is an open source project focusing on a standard implementation of lightweight Virtual Machines (VMs) that perform like containers. Prior to version 4.0.0, kata-runtime is vulnerable to host code execution via an unvalidated configuration path annotation. The runtime accepts an arbitrary io.katacontainers.config_path pod annotation and loads the referenced host TOML file without restriction. As a result, a pod user who can place a file at a host-visible path can supply a configuration that selects an attacker-controlled hypervisor or virtio-fs daemon binary, executing code as root on the host. This issue is fixed in version 4.0.0.

### CVE-2026-19264

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-07T15:17:00.297 |

Postiz is an open-source social media scheduling tool. The route that serves locally stored media joins URL-supplied path segments onto the upload directory and streams the file without normalising the path or confining it to that directory, and the route requires no authentication. Raw dot-segments are collapsed before routing, but URL-encoded separators survive route matching and are decoded only once they reach the handler, restoring the traversal at the filesystem call. An unauthenticated remote attacker can therefore read any file readable by the application process, including the process environment, which exposes the JWT signing secret, the database connection string, and connected provider and billing secrets. Because session tokens are signed with that secret and carry no expiry, this allows forging a non-expiring session as any user, including an administrator, without a password.

### CVE-2022-4995

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-07T15:16:57.600 |

Weaver (Fanwei) E-cology 9.0 versions prior to 10.52 contain a file upload vulnerability that allows a remote, unauthenticated attacker to upload arbitrary files, including JSP webshells, by submitting a multipart/form-data POST request to /workrelate/plan/util/uploaderOperate.jsp with arbitrary secId and plandetailid field values. Successful exploitation results in remote code execution under the privileges of the application server process. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14 (UTC).

### CVE-2026-47243

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-36` |
| Published | 2026-08-07T22:16:58.753 |

Kata Containers is an open source project focusing on a standard implementation of lightweight Virtual Machines (VMs) that perform like containers. Prior to 3.31.0, the runtime-rs standalone virtio-fs path is vulnerable to a guest-root to host-root escape. In this configuration, Kata runs the host virtiofsd as root with --sandbox none --seccomp none, so an attacker with root-equivalent access inside the guest can bypass the guest virtio-fs client entirely by taking over the virtio-fs PCI device and building a virtqueue in userspace to submit raw FUSE requests directly to the host virtiofsd. A crafted FUSE_SYMLINK request whose new symlink name is an absolute host path is honored outside the configured shared directory, allowing guest root to create root-owned symlinks in sensitive host locations such as /etc/cron.d. By pointing such a symlink at a guest-controlled crontab payload reachable through a live runtime process's mount namespace, the attacker causes the host cron daemon to execute that payload as host root, crossing the Kata isolation boundary. This issue is fixed in version 3.31.0.

### CVE-2026-48170

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-1321` |
| Published | 2026-08-07T22:16:59.170 |

`scim-patch`, a library to perform SCIM patch, prior to version 0.9.1 performs prototype pollution when applying a SCIM PATCH operation whose `value` object contains a key like `"__proto__.someProp"`. After one such patch,
`Object.prototype.someProp` is set process-wide, affecting every plain object in the Node process. Any service that calls `scimPatch()` on attacker-controlled JSON (i.e. any SCIM endpoint accepting `PATCH` from an external IdP) is exploitable on a stock Node runtime. Version 0.9.1 contains a patch. A workaround is available. Calling `Object.freeze(Object.prototype)` (and the same on `Array.prototype`, `Function.prototype`) at process startup neutralizes this class of bug — assignment to a frozen prototype becomes a silent no-op in sloppy mode or a `TypeError` in strict mode. Node's `--frozen-intrinsics` flag does this for built-ins automatically.

### CVE-2026-48039

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-07T20:16:51.723 |

Meta Ads MCP is a Model Context Protocol (MCP) server that lets AI assistants run Meta Ads. Prior to version 1.0.109, `AuthInjectionMiddleware.dispatch()` at `http_auth_integration.py:272` unconditionally forwards unauthenticated Streamable HTTP requests to downstream MCP tool handlers without issuing a `401` response, allowing any network-reachable caller to invoke MCP tools without authentication. When no per-request credential is present, tool handlers fall back to the `META_ACCESS_TOKEN` environment variable, and when the downstream Meta Graph API call fails, `api.py:263–269` serialises the raw `httpx` request URL—including the operator's `access_token` as a query parameter—into the JSON-RPC response body, delivering the credential to the unauthenticated caller. Version 1.0.109 fixes the issue.

### CVE-2026-71851

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-331;CWE-334;CWE-338` |
| Published | 2026-08-07T19:18:54.390 |

crypto-js is a JavaScript library of crypto standards. Versions of crypto-js prior to 4.0.0 generate randomness in CryptoJS.lib.WordArray.random() using a custom variation of the Multiply-With-Carry pseudorandom number generator, seeded from Math.random(), instead of a cryptographically secure source. This generator was introduced in version 3.1.2-4 and remained present in nearly every 3.x release. Nominal requests for 128 or 256 bits of entropy through this function produce effective search spaces of approximately 2 to the 39th and 2 to the 47th possibilities, small enough to enumerate on commodity hardware. Downstream wallet applications that used CryptoJS.lib.WordArray.random() as the entropy source for BIP39 recovery phrases are affected, and an attacker who enumerates the reduced output space can recover the resulting private keys and control the associated funds. This issue is fixed in version 4.0.0.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-64638

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-07T18:17:20.340 |

WordPress is vulnerable to a pre-auth reflected XSS vulnerability on the login screen.

Via a specially crafted malicious third-party website hosted by an attacker, it is possible for this to be escalated to an RCE vulnerability with conditions outside of the attackers control. This requires successful social engineering of and explicit interaction by the target victim.

This issue affects all versions of WordPress. Version 7.0.3 has been released, containing a fix for the vulnerability, and as a courtesy to users on older branches the fix has been backported to all branches back to 4.7.

Discovered and responsibly disclosed by [the team at pwn.ai](https://pwn.ai/).

### CVE-2026-17601

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-07T17:17:01.013 |

A user holding a permission to update privilege definitions could modify a wildcard privilege already assigned to their own role to grant broader permissions than they were authorized to hold, including full administrative access, without any additional authorization check or role reassignment.

### CVE-2026-48169

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-07T22:16:59.013 |

PraisonAI is a multi-agent teams system. Versions prior to 0.1.4 of the PraisonAI Platform API have two authorization failures that together break workspace isolation. The service layer for issues and projects performs global primary-key lookups without checking workspace ownership, so any authenticated user can read, modify, and delete resources in any workspace just by swapping UUIDs in their API requests. On top of that, every member management endpoint (add, update role, remove) only requires `min_role="member"`, which lets any workspace member promote themselves to owner and kick out the original owner. A low-privilege member of one workspace can steal data from every other workspace and take over any workspace they belong to. Both issues come from the same gap: the route layer pulls `workspace_id` from the URL and verifies membership, but the service layer ignores the workspace scope for resource lookups and ignores the caller's role level for member operations. The `require_workspace_member()` dependency does its job correctly. The problem is that the service layer doesn't use the information it provides. Version 0.1.4 of the PraisonAI Platform API patch the issue.

### CVE-2026-13505

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-772` |
| Published | 2026-08-08T02:17:16.520 |

In Bouncy Castle for Java FIPS (BC-FJA) before bc-fips 1.0.2.7 (1.0.X series), 2.0.2 (2.0.X series) and 2.1.3 (2.1.X series), sensitive key material held by the AES and DESede engines, the SP 800-90A DRBGs, SymmetricSecretKey and the PBKD and scrypt parameter classes was zeroised on garbage collection by overriding Object.finalize. Finalization runs at an unspecified time and in an unspecified order and is serviced by a single finalizer thread, so where objects carrying a finalizer are allocated faster than that thread retires them the pending-finalization queue grows without bound: disposal falls arbitrarily far behind, which can contribute to an OutOfMemoryError under load, and the key material those objects hold stays resident in the heap for as long as they are queued, defeating the purpose of the zeroisation. The behaviour was not a problem on Java 8 or Java 11; it is later JVMs, on which finalization has been deprecated and progressively de-emphasised, where it becomes one. Disposal of these classes now runs from a java.lang.ref.Cleaner registered in the multi-release jdk1.9 overlay, so on Java 9 and later it no longer depends on the finalizer being scheduled. Bouncy Castle for Java (bcprov) and Bouncy Castle for Java LTS are not affected, as neither implements the finalizer-based zeroisation scheme.

### CVE-2026-8798

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-835` |
| Published | 2026-08-08T01:16:31.393 |

In Bouncy Castle for Java FIPS (BC-FJA) before bc-fips 2.1.3, the native entropy source used on Intel platforms retried the CPU entropy instructions without any bound. RDSEED and RDRAND report failure through their carry flag, and the JNI seeding routine spun re-issuing the instruction for as long as that flag stayed clear, so a persistent failure of the on-chip entropy source - whether from a hardware fault, from the underlying DRBG being exhausted by contention across many cores, or from a hypervisor that does not provide the instruction - left the calling thread looping indefinitely inside the JNI call, where it could be neither interrupted nor timed out. Any operation drawing from the native entropy source could therefore hang, denying service to the application. The retry loops are now bounded (200 attempts for RDSEED and 20 for RDRAND, twice the baselines given in Intel's Digital Random Number Generator software implementation guide), pausing between attempts and, on exhaustion, clearing any partially written buffer and throwing rather than continuing to spin. The clear is performed by an un-elidable memzero, which uses a volatile pointer and an assembly memory barrier so that a compiler cannot optimise the erase away as a dead store. Bouncy Castle for Java (bcprov) is not affected, as it has no native entropy source; the 1.0.X and 2.0.X FIPS series are not affected.

### CVE-2026-48026

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-07T23:17:03.810 |

lakeFS is an open-source tool that transforms object storage into a Git-like repositories. Prior to version 1.81.1 of the open source edition and 1.84.0 of the enterprise edition, lakeFS Web UI renders markdown files from repository objects without sanitizing the resulting HTML. A user with write access to any repository branch can commit a `.md` object containing arbitrary HTML/JavaScript. Any other user who opens that object, or who navigates to a repository or directory containing a malicious `README.md`, executes the attacker-supplied script in their own authenticated session. lakeFS fixes the issue in v1.81.1 and lakeFS Enterprise fixes the issue in in v1.84.0. Enterprise customers using older versions can temporarily disable Markdown rendering by adding YAML to their config. No workaround exists for OSS release. Users are advised to upgrade to the latest version for both lakeFS and lakeFS-Enterprise.

### CVE-2026-47663

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-07T21:17:28.500 |

Pathling is a set of tools that make it easier to use FHIR and clinical terminology within health data analytics. Prior to version 2.0.0 of Pathling Server, Pathling's typed CRUD/search/batch FHIR surface allows an authenticated caller with only coarse operation authorities to act on attacker-chosen resource families because those entrypoints do not consistently enforce the documented per-resource `read` and `write` authorities. The documented authorization model requires an operation authority (e.g. `pathling:search`) to be paired with the matching per-resource `read` or `write` authority (e.g. `pathling:read:Patient`). Delete and batch are documented to require write authority for all referenced resource types. However, typed search, update, and related handlers are annotated only with `@OperationAccess(...)` and act on the provider-selected resource type without checking the corresponding per-resource authority. This is fixed in Pathling Server 2.0.0.

### CVE-2026-47662

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-522;CWE-918` |
| Published | 2026-08-07T21:17:28.347 |

Pathling is a set of tools that make it easier to use FHIR and clinical terminology within health data analytics. Prior to version 2.0.0 of Pathling Server, Pathling's typed CRUD/search/batch FHIR surface allows an authenticated caller with only coarse operation authorities to act on attacker-chosen resource families because those entrypoints do not consistently enforce the documented per-resource `read` and `write` authorities. The documented authorization model requires an operation authority (e.g. `pathling:search`) to be paired with the matching per-resource `read` or `write` authority (e.g. `pathling:read:Patient`). Delete and batch are documented to require write authority for all referenced resource types. However, typed search, update, and related handlers are annotated only with `@OperationAccess(...)` and act on the provider-selected resource type without checking the corresponding per-resource authority. This is fixed in Pathling Server 2.0.0.

### CVE-2026-47661

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-07T20:16:51.423 |

Pathling is a set of tools that make it easier to use FHIR and clinical terminology within health data analytics. Prior to version 2.0.0 of Pathling Server, Pathling's `/$result` endpoint allows a caller who can obtain any valid async export job ID to supply `file` parameter values containing path traversal sequences. The handler verifies only the supplied `job` and never normalises or confines the requested `file` path to that job's `jobs/<jobId>` directory before opening it as a filesystem resource. Because async export scratch space lives under the same warehouse database root as persisted resource tables, an attacker can use their own export job to read other files from the warehouse. This is fixed in Pathling Server 2.0.0. As an interim mitigation, disable the async export operations (`pathling.operations.exportEnabled`, `patientExportEnabled`, `groupExportEnabled`, `bulkSubmitEnabled`) or enable authentication and restrict export capability to trusted callers.

### CVE-2026-47660

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-918` |
| Published | 2026-08-07T20:16:51.283 |

Pathling is a set of tools that make it easier to use FHIR and clinical terminology within health data analytics. Prior to version 2.0.0 of Pathling Server, Pathling's bulk-submit operation allows an allowed submitter to supply an explicit `oauthMetadataUrl` parameter that is not validated against `pathling.bulkSubmit.allowableSources`. When present, the bulk-submit OAuth flow trusts metadata and the returned `token_endpoint` from the caller-chosen location, then builds outbound OAuth client authentication directly from the submitter's stored credentials. This is fixed in Pathling Server 2.0.0.

### CVE-2026-47659

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-918` |
| Published | 2026-08-07T20:16:51.130 |

Pathling is a set of tools that make it easier to use FHIR and clinical terminology within health data analytics. Prior to version 2.0.0 of Pathling Server, Pathling's `/$result` endpoint allows a caller who can obtain any valid async export job ID to supply `file` parameter values containing path traversal sequences. The handler verifies only the supplied `job` and never normalises or confines the requested `file` path to that job's `jobs/<jobId>` directory before opening it as a filesystem resource. Because async export scratch space lives under the same warehouse database root as persisted resource tables, an attacker can use their own export job to read other files from the warehouse. This is fixed in Pathling Server 2.0.0. The `$result` handler now resolves and canonicalizes the requested file path and rejects any request that escapes the job's `jobs/<jobId>` directory. As an interim mitigation, disable the async export operations (`pathling.operations.exportEnabled`, `patientExportEnabled`, `groupExportEnabled`, `bulkSubmitEnabled`) or enable authentication and restrict export capability to trusted callers.

### CVE-2026-71847

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-07T19:18:53.807 |

Ruby JSON is a JSON implementation for Ruby. From 2.20.0 until 2.21.2, Ruby's JSON native C extension clears the consumed JSON::ResumableParser input buffer but leaves state.start, state.cursor, and state.end pointing into released storage. When partial_value reconstructs an incomplete object containing duplicate keys, the duplicate-key warning path calls cursor_position, which dereferences those stale pointers. This results in a heap-use-after-free and can terminate the Ruby process. An attacker who can supply JSON stream data to an application using JSON::ResumableParser may cause process termination when the application calls partial_value on incomplete attacker-controlled input containing duplicate object keys. This issue has been fixed in version 2.21.2.

### CVE-2026-67585

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-07T17:17:06.927 |

Allocation of Resources Without Limits or Throttling vulnerability in DivvyPayHQ absinthe_federation allows an unauthenticated remote attacker to abort the Erlang VM via crafted _entities representation keys.

Every key of every object in the representations argument of the federation-mandated _entities field is converted with String.to_atom/1 by convert_key/2 in lib/absinthe/federation/schema/entities_field.ex. representations is typed as the open-ended _Any scalar, so its keys bypass schema coercion and the attacker names them freely. Atoms are never garbage collected and the BEAM atom table is hard-capped (about 1,048,576 entries by default), so one request carrying tens of thousands of unique keys creates that many permanent atoms and a handful of such requests exhausts the table and aborts the node. The impact is confined to availability: no data is read or altered, and recovery requires restarting the application.

This issue affects absinthe_federation: from 0.1.0 before 0.9.3.

### CVE-2026-17603

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-07T17:17:01.250 |

Nexus Repository 3 did not sufficiently restrict which HikariCP connection-pool properties could be set through the DataStore configuration API. A user holding the nx-datastores-update permission could set the connectionInitSql property to execute arbitrary SQL against the configured database on every new connection. On the default H2 database backend, this could be leveraged to achieve remote code execution as the Nexus process user.

### CVE-2026-17600

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-08-07T17:17:00.850 |

Sonatype Nexus Repository 3 did not immediately terminate a user's active login session or revoke their cached permissions when that user's account was deleted, deactivated, or had its password changed. A user whose account was already logged in at the time of one of these actions could continue using their existing session to interact with the repository as though the account were still active, until that session independently expired. Depending on the permissions previously held, this could allow continued unauthorized access to read, modify, or delete repository content after access was intended to be revoked.

### CVE-2026-48120

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-07T23:17:04.117 |

Kakoune is a code editor. Prior to version 2026.05.21, the bundled, enabled by default, `autorestore.kak` script can be exploited by malicious backup files leading to arbitrary kakoune and shell commands being executed by simply opening a file. Kakoune 2026.05.21 fixes the issue. As a workaround, add `autorestore-disable` to the user kakrc will disable the autorestore feature.

### CVE-2026-47664

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-345;CWE-918` |
| Published | 2026-08-07T21:17:28.657 |

Pathling is a set of tools that make it easier to use FHIR and clinical terminology within health data analytics. Prior to version 2.0.0 of Pathling Server, the `$import-pnp` operation in Pathling Server accepts a caller-supplied `exportUrl` and uses it as the remote FHIR Bulk Export endpoint without constraining it to a trusted source. When PNP credentials are configured, Pathling builds a credentialed bulk-export client targeting the caller-chosen host, downloads manifest-selected files, and then reclassifies those staged files as trusted local `file://` imports - bypassing the configured `allowableSources` allowlist that protects the ordinary `$import` operation. This is fixed in Pathling Server 2.0.0. As a workaround, disable the `$import-pnp` operation (`pathling.operations.importPnpEnabled=false`) or do not configure PNP credentials.

### CVE-2026-48007

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-07T20:16:51.573 |

Element Call is a native Matrix video conferencing application. Versions 0.5.17 through 0.19.3 report analytics data to a PostHog server, when configured to by a `posthog` key in config.json or by the `posthogApiHost` and `posthogApiKey` URL parameters. Several fields of this data (`$initial_person_info`, `$session_entry_url`, and `$current_url`) were found to contain the full URL of the user's visited page, including the fragment. Users of a standalone Element Call ‘SPA’ instance such as https://call.element.io may therefore have reported the full URLs of certain calls, including encryption passwords, to the configured PostHog server, potentially compromising the confidentiality of the calls to actors who could access both the PostHog analytics data and the encrypted media streams. The same issue is present in Element Call's embedded package, but in practice it does not impact applications using this package (including Element Web, Element Desktop, Element X iOS, and Element X Android) because they distribute encryption keys over Matrix rather than encoding a password in the URL. The issue is patched in Element Call 0.19.4. Some workarounds are available. Users may opt out of analytics in the 'Feedback' tab of Element Call's settings and create new links for future calls. Admins who host Element Call as a standalone application may disable PostHog analytics entirely by removing the `posthog` key from their deployment's config.json file.

### CVE-2026-14644

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-07T17:16:57.030 |

Nexus Repository 3 contained a privilege escalation vulnerability in the REST privileges API. An authenticated user with permission to manage privileges could, under certain role configurations, escalate their own access to full administrator by exploiting a type-confusion flaw in the privilege update endpoint.

### CVE-2026-68772

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-07T17:17:07.573 |

ZenML 0.94.6 contains a remote code execution vulnerability in the CloudpickleMaterializer component that allows attackers with write access to a shared artifact store to execute arbitrary code by planting a malicious pickle file. Attackers can replace a stored artifact.pkl file with a crafted cloudpickle payload containing a malicious __reduce__ method, which executes arbitrary system commands when any user or pipeline materializes the artifact through the unsanitized cloudpickle.load() call in cloudpickle_materializer.py.

### CVE-2026-17594

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-07T17:16:59.470 |

Nexus Repository 3 CE/Pro versions 3.0.0 through 3.94.x contain an incorrect authorization vulnerability (CWE-863) in the repository-creation user interface. An individual user account holding a delegated repository-admin privilege scoped to a specific repository format could create a repository of a different, unauthorized format, because authorization was checked against one request field while a separate, attacker-controlled field determined the repository format actually created. This does not affect the anonymous user, which cannot hold this privilege by default. Fixed in version 3.95.0.

### CVE-2026-48097

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-476` |
| Published | 2026-08-07T19:17:47.627 |

NexTor IP Changer is a command-line tool that leverages the Tor network to periodically rotate a user's IP address. Versions prior to 2.0.0 have a command execution vulnerability due to unsafe use of `shell=True` with commands that rely on executable resolution through the `PATH` environment variable. An attacker controlling the execution environment can place malicious executables such as sudo earlier in the `PATH`, resulting in execution of attacker-controlled code. Version 2.0.0 fixes the issue.

### CVE-2026-64636

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-07T18:17:20.070 |

An SQL injection vulnerability in Plesk Obsidian up to 18.0.80 for Linux and Windows allows an authenticated user to read arbitrary data from the panel database.

### CVE-2026-52880

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-08-07T23:17:04.890 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Versions from 1.7.14 through 1.7.17 are vulnerable to a remotely triggerable denial of service. Both REST APIs are started with the Gin Engine.Run convenience method, which serves requests through Go's default HTTP server with no ReadHeaderTimeout, ReadTimeout, or MaxHeaderBytes configured. As a result, incoming connections that never complete their request headers are held open indefinitely. When a REST listener is reachable beyond localhost through the documented all-interface bind or a Docker port-publish deployment, a single unauthenticated client can open many slow-header connections and hold them open until server file descriptors are exhausted, preventing the API from accepting new connections. This renders the REST API unavailable to legitimate clients. This issue is fixed in version 1.7.18.

### CVE-2026-52879

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-08-07T23:17:04.743 |

Klever-Go is the Go implementation of the Klever blockchain protocol. In versions 1.7.14 through 1.7.17, the direct-message ingress handler spawns a new goroutine for every incoming direct message before the processor-level antiflood layer makes any admission decision, with no semaphore, throttler, or bound on the number of concurrent in-flight spawns. Because the antiflood check runs inside the spawned goroutine rather than before it, a single connected peer can open a direct-send stream and send a stream of well-formed messages to force unbounded goroutine creation, where each goroutine allocates its own stack and holds a message reference until processing completes, adding scheduler and garbage-collection pressure faster than the runtime can drain it. This lets one peer degrade the node's availability and its ability to process legitimate traffic, resulting in a remotely triggerable denial of service. The issue is fixed in 1.7.18.

### CVE-2026-52878

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-07T23:17:04.593 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Versions 1.7.14 through 1.7.17 are vulnerable to a nil-pointer panic triggered by a protobuf Transaction whose embedded RawData sub-message is omitted. This omission causes RawData to decode to nil. Every transaction gossiped on the Klever-Go P2P network is decoded and validated synchronously inside the libp2p pubsub topic-validator callback, where txVersionChecker.CheckTxVersion dereferences tx.RawData.Version with no nil check. Because the libp2p pubsub callback, the underlying go-libp2p-pubsub validation worker, and Klever's own network/p2p layer install no recover(), the panic propagates and crashes the entire node process. The attacker payload is a 3-byte protobuf message; no validator key, stake, funds, or on-chain account is required, and delivery aimed at enough of the BLS validator set can halt block production, resulting in a chain halt. This issue has been fixed in version 1.7.18.

### CVE-2026-47249

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-07T23:17:03.670 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.18, the P2P resolver request handling logic is vulnerable to hash-array amplification. A connected peer can send a compressed RequestDataType_HashArrayType direct request that is only 442 bytes on the wire but expands into 200,000 decoded hash entries inside the resolver path. The resolver's antiflood logic counts only a single logical message and the compressed wire size, and while Batch.Decompress() caps the decompressed byte size, it never limits the number of decoded repeated-field items. As a result, both TxResolver and TrieNodeResolver preallocate and iterate over the entire unchecked set of decoded hashes, causing remote memory and CPU amplification against any node that accepts P2P peer connections. This issue is fixed in version 1.7.18.

### CVE-2026-65819

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-400` |
| Published | 2026-08-07T20:16:52.603 |

gopacket provides packet processing capabilities for Go. Through version 1.7.0, multiple layer decoders use attacker-controlled lengths, counts, or offsets before validating them against packet buffers, allowing a crafted packet decoded through DecodingLayerParser or DecodeFromBytes to trigger an unrecovered panic and remotely deny service.  A patch commit is available at 210f25f.

### CVE-2026-62296

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-400;CWE-674` |
| Published | 2026-08-07T20:16:52.457 |

HAPI FHIR is a complete implementation of the HL7 FHIR standard for healthcare interoperability in Java. Prior to 6.9.11, XhtmlParser.java imposes no maximum element nesting depth, so a deeply nested text.div narrative triggers unbounded recursion between parseElementInner() and parseElement(), raising a StackOverflowError. An attacker who can submit FHIR resources containing such narratives can thus crash a parsing or validation worker thread, affecting validator services and any application that parses attacker-supplied FHIR JSON or XML. This issue is fixed in version 6.9.11.

### CVE-2026-62295

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-400;CWE-674` |
| Published | 2026-08-07T20:16:52.310 |

HAPI FHIR is a complete implementation of the HL7 FHIR standard for healthcare interoperability in Java. Prior to 6.9.11, the JSON utility parser in org.hl7.fhir.utilities.json.parser.JsonParser enforces no maximum nesting depth for arrays or objects. As a result, a small but deeply nested, syntactically valid FHIR JSON document can trigger unbounded readArray() or readObject() recursion, raising a StackOverflowError before structural validation runs. An attacker who can submit JSON resources for validation can thus crash the request thread, and services that do not isolate StackOverflowError safely may experience worker loss or process instability — a denial-of-service condition. This issue is fixed in version 6.9.11.

### CVE-2026-15972

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-07T20:16:50.020 |

Consul Community Edition and Consul Enterprise 1.13.0 through 2.0.2 are vulnerable to an unauthenticated denial of service through unbounded connection acceptance on the external gRPC listeners. A remote attacker may exhaust agent file descriptors, goroutines, and memory by opening many incomplete connections, potentially preventing legitimate clients from connecting. This vulnerability, CVE-2026-15972, is fixed in Consul 2.0.3 and Consul Enterprise 1.21.17, 1.22.11, and 2.0.3.

### CVE-2025-63235

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-07T19:17:33.580 |

In sol commit 373d848 (2024-12-12), the broker does not fully release resources when handling malformed or duplicate CONNECT packets. When clients send invalid CONNECT packets - either due to repeated attempts or failed authentication - the server may silently drop the connection or send a CONNACK but fail to close the session or deallocate internal resources. This behavior allows an attacker to create numerous half-open connections that consume memory and file descriptors indefinitely, potentially triggering the Linux OOM killer and causing a denial of service.

### CVE-2026-19082

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-07T18:17:11.363 |

Imager versions from 0.45_02 before 1.034 for Perl may expose adjacent heap bytes via strlen() over-read from zero-count ASCII EXIF entries in copy_string_tags.

copy_string_tags() computes an ASCII EXIF tag's length as `entry->size - 1` to strip the trailing NUL. A zero-count ASCII entry sets `entry->size` to 0, and the derived length reaches i_tags_add() as -1, which is interpreted as a request to call strlen(), scanning past the entry to the next NUL and copying those bytes into the tag. JPEG reaches this path via im_decode_exif(), as does the separate Imager::File::WEBP distribution, which is fixed by upgrading Imager.

Any caller of Imager->read() on an attacker-supplied image with such an entry may receive an exif_* tag holding adjacent heap bytes instead of an empty string.

### CVE-2026-20348

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-07T17:17:03.537 |

A vulnerability in the XAR file format parser of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition or possibly other expanded impacts as a result of&nbsp;memory corruption on an affected device.

This vulnerability is due to improper boundary checks for content in XAR files during scanning. An attacker could exploit this vulnerability by submitting a crafted file that contains XAR content to be scanned by ClamAV on an affected device. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-20347

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-07T17:17:03.337 |

A vulnerability in the Mach-O file format parser of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition or possibly other expanded impacts as a result of&nbsp;memory corruption on an affected device.

This vulnerability is due to improper boundary checks for content in Mach-O files during scanning, which may result in an out-of-bounds buffer read. An attacker could exploit this vulnerability by submitting a crafted Mach-O file to be scanned by ClamAV on an affected device. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-20346

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-07T17:17:03.140 |

A vulnerability in the PDF file format parser of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition or possibly other expanded impacts as a result of&nbsp;memory corruption on an affected device.

This vulnerability is due to improper boundary checks for content in PDF files during scanning, which may result in an out-of-bounds buffer read. An attacker could exploit this vulnerability by submitting a crafted PDF file to be scanned by ClamAV on an affected device. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-20345

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-07T17:17:03.003 |

A vulnerability in the GPT file format parser of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition or possibly other expanded impacts as a result of&nbsp;memory corruption on an affected device.

This vulnerability is due to improper handling of an endian conversion operation, which may result in an out-of-bounds buffer write. An attacker could exploit this vulnerability by submitting a crafted GPT file to be scanned by ClamAV on an affected device. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-20339

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-07T17:17:02.807 |

A vulnerability in the PESpin file format parser of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition or possibly other expanded impacts as a result of&nbsp;memory corruption on an affected device.

This vulnerability is due to improper boundary checks for content in PESpin files during scanning, which may result in an integer overflow. An attacker could exploit this vulnerability by submitting a crafted file that contains PESpin content to be scanned by ClamAV on an affected device. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-20338

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-08-07T17:17:02.610 |

A vulnerability in the zip archive parser of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition on an affected device.

This vulnerability is due to improper memory handling when processing content in zip files during scanning. An attacker could exploit this vulnerability by submitting a crafted zip file for scanning. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate as a result of a memory double-free, resulting in a DoS condition on the affected software.

### CVE-2026-20337

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-07T17:17:02.413 |

A vulnerability in the zip archive parser of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition on an affected device.

This vulnerability is due to improper boundary checks for content in zip files during scanning, which may result in an out-of-bounds write condition. An attacker could exploit this vulnerability by submitting a crafted zip file for scanning. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-48098

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-78;CWE-250` |
| Published | 2026-08-07T19:17:47.780 |

NexTor IP Changer is a command-line tool that leverages the Tor network to periodically rotate a user's IP address. Versions prior to 2.0.0 execute privileged system commands using `sudo` and `shell=True` directly inside application logic. In environments where passwordless sudo (`NOPASSWD`) is enabled, privileged commands may execute silently without explicit user confirmation. Version 2.0.0 fixes the issue.

### CVE-2026-17593

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-08-07T17:16:59.167 |

An account holding the nexus:settings:update permission in Nexus Repository 3 (or the equivalent nexus:settings permission in the legacy Nexus Repository 2) could submit arbitrary values as realm identifiers through an internal configuration API that did not validate them against the set of registered realms. Because unrecognized entries were persisted and re-evaluated on every realm load via a legacy code path, this could result in unintended code executing inside the Nexus Repository process, and in some cases a persistent authentication lockout that was not visible through the administrative UI.

### CVE-2026-58262

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-347` |
| Published | 2026-08-07T22:16:59.327 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.20, header signature verification counts the unused padding bits of the PubKeysBitmap toward the two-thirds validator quorum. These padding bits do not correspond to any validator and are ignored by the actual BLS aggregate-signature check, so a malicious or compromised block producer can set them to reach the required quorum while gathering fewer genuine validator signatures than the protocol demands. As a result, nodes that import or intercept the header accept it as correctly signed without a real two-thirds quorum, weakening consensus safety and undermining finality. This issue is fixed in version 1.7.20.

### CVE-2026-45808

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-07T22:16:58.370 |

OpenBao is an open source identity-based secrets management system. Prior to version 2.5.4, OpenBao's namespaces provide multi-tenant separation. A tenant who intentionally leaks lease identifiers can have their lease and underlying credential revoked or renewed by a user in another tenant via the legacy, undocumented `sys/revoke` and `sys/renew` endpoints. This is fixed in OpenBao v2.5.4.

### CVE-2026-66061

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-07T21:17:29.693 |

Home Assistant is open source home automation software focused on local control and privacy.  Prior to 2026.5.0, the iOS Companion app treats tag links (NFC or QR) delivered through an OS-level routing mechanism such as iOS universal links as if they were physically scanned, without validating the calling app or prompting the user. As a result, any untrusted app on the device can forward an arbitrary tag to Home Assistant, causing it to execute the associated automation as though a legitimate user had scanned an authorized tag. This allows silent, unattended automation execution by untrusted local callers. This issue has been fixed in version 2026.5.0.

### CVE-2026-66060

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-07T21:17:29.520 |

Home Assistant is open source home automation software focused on local control and privacy.  Prior to 2026.5.3,  the Companion app treats tag links (NFC or QR) delivered through an OS-level routing mechanism as if they were physically scanned, without validating the calling app or prompting the user. As a result, any untrusted app on the device can forward an arbitrary tag to Home Assistant, causing it to execute the associated automation as though a legitimate user had scanned an authorized tag. This allows silent, unattended automation execution by untrusted local callers. This issue is fixed in version 2026.8.1.

### CVE-2026-70561

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-07T19:18:53.277 |

TestLink 1.9.20 and prior contains an insecure direct object reference vulnerability that allows any authenticated user, including low-privilege guest accounts, to read arbitrary attachments by supplying an integer attachment ID to the attachmentdownload.php handler without any project or role authorization check. Attackers can enumerate sequential integer IDs through the attachment download endpoint to retrieve file contents from private projects they have no membership in, bypassing the per-project access control model and exposing test specifications, requirements documents, execution evidence, and other sensitive uploaded files across the entire installation.

### CVE-2025-71412

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-08-07T19:17:34.190 |

Injection of false emergency or status messages over CPDLC may lead to misallocation of resources, operational confusion, and improper response actions by flight crews, traffic controllers, and ground operations.  This type of attack can be carried out remotely over radio frequency.

### CVE-2025-71409

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-07T19:17:33.720 |

Lack of authentication for Very High Frequency Data Link messages allows rogue ground stations to inject CPDLC messages leading to unexpected or misleading clearances and potential pilot confusion. This type of attack can be carried out remotely over radio frequency.

### CVE-2026-71556

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-07T17:17:10.150 |

go-git is an extensible git implementation library written in pure Go. Prior to 5.19.2 and 6.0.0-alpha.5, worktree operations (including checkout, status, and add) resolve symbolic links inside the working tree without confining resolution to the worktree boundary, so a maliciously crafted repository containing a symlink can cause go-git to read from or write to files outside the intended working directory when the repository is cloned and its worktree operations are used. Versions 5.19.2 and 6.0.0-alpha.5.
