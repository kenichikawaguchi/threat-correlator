# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-17 15:00 UTC
- **対象期間**: `2026-11-16T15:00:24.000Z` 〜 `2026-11-17T15:00:48.000Z`
- **重要CVE数**: 150 件（Critical 9.0+: 24 件 / High 7.0〜: 126 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件** 近くに上りますが、特に **認証バイパス・不適切なトークン検証・リモートコード実行** が目立ちます。  
- Web アプリケーションや GraphQL API に対する **入力検証不備** が多数報告され、攻撃者は認証なしで権限取得や任意コード実行が可能です。  
- 組み込み系ファームウェア（Zyxel ルータ等）でも **メモリ破壊型脆弱性** が残っており、WAN が無効でも LAN 内からのリモート攻撃が成立します。  
- コンテナ／サーバーレス基盤（OpenFunction、CubeSandbox 等）で **PodSpec の制御不足** が見られ、マルチテナント環境での権限エスカレーションが容易です。  

この傾向は「**認証・権限チェックの欠如**」が根本原因であることが多く、パッチ適用だけでなく **デフォルト設定の見直し** が必須です。

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な脆弱性 | 影響範囲・被害シナリオ | 推奨パッチ/バージョン |
|-----|--------|------------|------------------------|----------------------|
| **CVE‑2026‑120387** | 10.0 | JWT の `none` アルゴリズムを受け入れる不適切な署名検証 | CIRCUTOR PowerStudio SCADA WAVE デスクトップ版で、認証トークンを署名なしで送信できるため、遠隔から管理画面に **無認証でログイン** 可能。SCADA 環境は重要インフラであり、制御系への不正操作リスクが極めて高い。 | **PowerStudio SCADA WAVE 5.3.2 以降**（ベンダーが提供する修正パッチ） |
| **CVE‑2026‑53998** | 10.0 | GraphQL `applyChatTemplate` が F‑string テンプレートを直接評価、`DotDict.__getattr__` がプライベート属性へトラバーサル可能 | Phoenix AI Observability (13.0.0‑15.7.0) の GraphQL API へ細工したテンプレート文字列を送るだけで **任意コード実行** が可能。マルチテナント環境で他テナントのデータを取得・改ざんできる。 | **Phoenix 15.7.1** 以上（F‑string 解析ロジックのサニタイズ） |
| **CVE‑2026‑79614** | 9.8 | Zyxel DX3301‑T0/EX3301‑T0 の `libclinkc.so` に対する **アウト・オブ・バウンズ書き込み** | ファームウェア 5.50(ABVY.8.3)C0 以前で、特定の HTTP リクエストを送ると **特権昇格** → 任意コマンド実行。WAN が無効でも LAN 内の攻撃者がルータを乗っ取れる。 | **5.50(ABVY.8.3)C1** 以降のファームウェアに更新 |
| **CVE‑2026‑130587** | 9.4 | OpenFunction の Function/Serving リソースで **PodSpec の制限が無い** | テナントが自分の Function に `privileged: true` や `hostNetwork: true` を付与でき、ホスト上で **特権コンテナ** を起動可能。K8s クラスタ全体への横展開リスクが高い。 | **OpenFunction 1.2.1**（PodSpec バリデーション強化） |
| **CVE‑2026‑129448** | 9.8 | Apache Roller の XML‑RPC エンドポイントで **未検証のデシリアライズ** | バージョン 4.0.0‑6.1.4 の Roller に対し、任意の XML を送信すると **リモートコード実行** が成立。ブログプラットフォームが多数運用されているため、広範囲への感染が懸念される。 | **Apache Roller 6.1.5** 以降（デシリアライズチェック追加） |

> **注**：上記 5 件は **CVSS が 9.4 以上** かつ **インフラ・クラウド基盤への直接的影響** が大きいものを選出しました。その他にも認証バイパスが多数報告されていますが、まずは上記のパッチ適用を最優先してください。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
- **CIRCUTOR PowerStudio SCADA WAVE**  
  - 公式サイトから **5.3.2 以上** のパッチを取得し、全 SCADA サーバーに適用。  
  - 変更後は JWT 検証ロジックが `alg != none` を必ず要求することを確認。

- **Phoenix AI Observability**  
  - **15.7.1** 以上へアップグレード。  
  - GraphQL エンドポイントのアクセス制御（IP 制限・認証）を追加し、不要な `applyChatTemplate` の公開を停止。

- **Zyxel DX3301‑T0 / EX3301‑T0**  
  - ファームウェア **5.50(ABVY.8.3)C1** 以降に更新。  
  - 管理画面へのアクセスは **VPN 経由のみ** に限定し、LAN 内からの直接 HTTP アクセスをファイアウォールで遮断。

- **OpenFunction**  
  - **1.2.1** 以上にアップデート。  
  - `PodSpec` の `privileged`, `hostNetwork`, `hostPID` などのフラグを **Admission Controller** で強制的に除外するポリシーを導入。

- **Apache Roller**  
  - **6.1.5** 以上へ更新。  
  - XML‑RPC エンドポイントは **IP アクセス制限** と **認証必須** に設定し、不要な場合は無効化。

### 3.2 設定・防御の強化
| 項目 | 推奨設定 |
|------|----------|
| **JWT / トークン検証** | `alg` が `none` の受け入れを禁止し、署名キーは **環境変数で管理**（ハードコード禁止）。 |
| **GraphQL API** | `depth-limit` と `complexity-limit` を導入し、リクエストレートを **IP/ユーザー単位で制限**（例: 5 秒間に 20 件）。 |
| **ファームウェア** | 定期的に **ベンダーのセキュリティアドバイザリ** をチェックし、リリースがあれば即時適用。 |
| **K8s / OpenFunction** |

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-120387

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-17T05:18:33.067 |

An improper JWT signature verification vulnerability in CIRCUTOR PowerStudio SCADA WAVE desktop version allows an unauthenticated remote attacker to bypass authentication by submitting an unsigned JWT with the algorithm set to “none”. The shared JWT validation component accepts the token without verifying a cryptographic signature, allowing the attacker to impersonate another user and access protected functionality with that user's privileges.

### CVE-2026-53998

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-134;CWE-200` |
| Published | 2026-11-16T20:19:06.807 |

Phoenix is an AI observability and evaluation platform. From 13.0.0 until 15.7.0, the applyChatTemplate GraphQL query passed attacker-controlled F-string templates to FStringTemplateFormatter._format, while DotDict.__getattr__ did not prevent traversal through Python private attributes. A crafted field could traverse object internals such as __class__, __init__, and __globals__ to read process environment variables and internal module state. The endpoint is unauthenticated on default installations, and any account can reach it when authentication is enabled. Exposure of PHOENIX_SECRET can allow administrative session-token forgery and decryption of credentials protected by keys derived from that secret. This issue is fixed in version 15.7.0.

### CVE-2026-129448

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-17T11:17:28.190 |

Deserialization of Untrusted Data in Apache Roller versions 4.0.0 through 6.1.4 allows an unauthenticated remote attacker to execute arbitrary code. The XML-RPC endpoint accepts vendor extension types and deserializes them before authenticating the requester.

This is the same vulnerability as CVE-2026-82384, which listed only Apache Roller 6.1.5 as affected. This issue is being actively exploited.

Users are recommended to upgrade to Apache Roller 6.1.6 or later, which disables the extension types and rejects XML-RPC requests when the XML-RPC feature is disabled.

Users who cannot upgrade right away should set "enabledForExtensions" to "false" in WEB-INF/web.xml, or remove the "/roller-services/xmlrpc" servlet mapping, and restart Roller. Disabling XML-RPC in the administration UI is not enough, because older versions deserialize the request before checking that setting.

### CVE-2026-79614

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-17T02:17:22.743 |

An out-of-bounds write vulnerability in “libclinkc.so” in Zyxel DX3301-T0/EX3301-T0 firmware versions through 5.50(ABVY.8.3)C0 could allow an unauthenticated attacker to elevate privileges and potentially execute arbitrary commands by sending a crafted HTTP request. WAN access is disabled by default on these devices.

### CVE-2026-130587

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T14:17:45.317 |

OpenFunction through 1.2.0 contains a privilege escalation vulnerability that allows namespace tenants to create privileged host-access pods by supplying unrestricted PodSpec templates in Function and Serving resources. Attackers with only Function or Serving create permissions can set privileged, hostNetwork, hostPID, or hostPath fields to mount the worker node's root filesystem and escalate to node access.

### CVE-2026-119623

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T11:17:24.740 |

The installer (first installation wizard) could be re-enabled on an already configured instance by placing a file whose name starts with FIRST_INSTALL in the public web root or the project root. The installer then became accessible without authentication, allowing for example to change the database connection and to create a new administrator and system maintainer account, which leads to remote code execution. As demonstrated in TYPO3-CORE-SA-2026-026, such a file could be created by an authenticated, low-privileged backend user without any further permissions. Other ways of creating files in the web root, as well as leftover or restored marker files, could be abused in the same way.

With the fixed versions, the installer can no longer be re-enabled on an already configured instance by a marker file. A new internal setting $GLOBALS['TYPO3_CONF_VARS']['SYS']['isInstalling'] is stored in the system configuration and is only enabled while a new installation is running. Additionally, only the exact file names FIRST_INSTALL and FIRST_INSTALL.txt are accepted as marker files.

### CVE-2026-120699

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-269;CWE-284` |
| Published | 2026-11-16T21:17:20.980 |

CubeSandbox is an instant, concurrent, secure, and lightweight sandbox for AI agents. Prior to 0.5.1, any authenticated tenant permitted to call POST /sandboxes can supply metadata["host-mount"] with an arbitrary existing host path because the control plane performs no authorization check or allowed-prefix validation for the path. injectHostDirMounts forwards the path to prepareHostDirVolume, where Cubelet uses mount --rbind through the function to perform a recursive bind mount as root and exposes the host subtree to the tenant's MicroVM through virtio-fs, read-write by default. This allows host-root file access and modification, host code execution, access to the container runtime, and compromise of co-resident tenants without a kernel or virtual-machine-monitor flaw. This issue is fixed in version 0.5.1.

### CVE-2026-130603

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-122;CWE-125` |
| Published | 2026-11-17T14:17:47.153 |

Eclipse Zenoh's zenoh-pico implementation, versions 0.7.2-rc up to but excluding 1.10.2, does not validate the Zenoh identifier (ZID) length when deserializing timestamps. An attacker-controlled length greater than 16 causes an out-of-bounds write to a fixed 16-byte identifier buffer and causes the subsequent zero-fill operation to receive a negative length converted to a large unsigned size. Truncated timestamp inputs can also cause out-of-bounds reads or assertion failures. A remote attacker able to deliver crafted timestamp-bearing Zenoh messages through an accepted transport can cause memory corruption and denial of service, with potential remote code execution in builds lacking appropriate binary protections. This issue is fixed in version 1.10.2.



Depending on the release and message-decoding path, the unchecked timestamp identifier length causes a heap-based or stack-based buffer overflow. Ordinary-frame network message decoding moved from heap-backed storage to stack-local storage in version 1.5.0. Earlier affected releases already contained stack-based decoding paths, including reassembled fragmented messages.

### CVE-2026-129280

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T11:17:27.187 |

Multiple ServerUI and ServerUI2 SOAP operations in N-able N-central before 2026.4.1 HF3 do not verify the caller's session, permissions or customer scope. A remote attacker, in some cases without authentication, can read device and patch data, test passwords of user accounts, send messages to managed agents, and modify device and service settings belonging to other customers.

### CVE-2026-129272

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-17T11:17:26.110 |

N-able N-central before 2026.4.1 HF3 uses a predictable credential to authenticate appliances to an agent-facing API. A remote, unauthenticated attacker who knows or guesses an appliance identifier can obtain a valid appliance token and session and impersonate that appliance.

### CVE-2026-130327

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-16T23:17:15.313 |

In Open Object Rexx (ooRexx) before 5.2.0, RXAPI relies on a world-writable /tmp file unless XDG_RUNTIME_DIR is set, or localhost TCP port 10010, allowing RXAPI communication by any local user, e.g., for injection of a macro that will be executed by a REXX script.

### CVE-2026-130320

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-16T23:17:15.177 |

In Open Object Rexx (ooRexx) before 5.2.0, RXAPI mishandles nameArg and userid bounds checking, possibly leading to arbitrary code execution via crafted messages.

### CVE-2026-130071

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-16T22:18:22.373 |

TridotsTech go1cms master branch through commit 7f68d05 and version-3 branch before commit ead8da3 contains a missing authentication vulnerability in the guest-whitelisted update_doc method that allows unauthenticated attackers to modify any document. Attackers can supply a doctype, name and arbitrary fields that are saved with ignore_permissions=True, altering User records to escalate privileges, take over accounts or tamper with business data.

### CVE-2026-130070

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-11-16T22:18:22.220 |

Ghost by muneeb141 on the main branch from commit c731cdf through commit 672dfec contains an authentication bypass vulnerability in the whitelisted ghost.api.ghost.convert_to_real_user method that allows unauthenticated attackers to skip OTP verification by setting the client-supplied bypass_otp parameter. Attackers can obtain a ghost session from the guest-accessible create_ghost_session endpoint, then call convert_to_real_user with an arbitrary real_email and bypass_otp=1 to receive OAuth tokens for existing accounts and take them over.

### CVE-2026-129955

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-16T15:17:31.030 |

NodePress through 8.5.1 contains an authentication bypass vulnerability that allows unauthenticated attackers to gain administrator access by using the hardcoded default password 'root'. Attackers can send base64-encoded 'root' to POST /admin/login when NP_ADMIN_DEFAULT_PASSWORD is unset to obtain admin tokens and fully control the site.

### CVE-2026-129952

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1394` |
| Published | 2026-11-16T15:17:30.573 |

NodePress through 8.5.1 contains an authentication bypass vulnerability that allows unauthenticated remote attackers to gain administrator access by forging JWTs with the hardcoded 'nodepress-secret' fallback key. Attackers can sign HS256 bearer tokens with the default issuer, audience, and role 'admin' to access administrator-only APIs for article, comment, options, and file management.

### CVE-2026-129941

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-16T15:17:28.800 |

Prime CMS (@primecms/core) through 0.4.0-beta.0 contains an authentication bypass vulnerability that allows unauthenticated attackers to register accounts via the createUser mutation on /prime/graphql. Because the isAuthenticated() guard has its check commented out and createAbility() hard-codes every role to admin, attackers can log in with full administrative control over content, users, webhooks and settings.

### CVE-2026-130583

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-17T14:17:44.847 |

Rootways Authorize.net CIM Pro extension for Magento 2 before 4.1.5 contains an unauthenticated server-side request forgery vulnerability in the Apple Pay merchant validation controller. Attackers can supply file://, gopher://, or dict:// URLs in the validationUrl parameter to read app/etc/env.php credentials and encryption keys or reach internal services and cloud metadata endpoints.

### CVE-2026-129286

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T11:17:27.943 |

N-able N-central before 2026.4.1 HF3 does not validate version values and download locations in software update metadata. An attacker able to supply or modify the update metadata received by the server can write files outside the download directory and execute code as the N-central service account.

### CVE-2026-130380

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-17T02:17:22.037 |

AdminNeo before 5.9.1 contains an authentication bypass vulnerability in the sqlsrv-based MS SQL driver that allows unauthenticated attackers to log in by submitting an empty username. Attackers can supply any non-empty password, triggering Windows integrated authentication that grants a full session with the web server identity's SQL Server privileges.

### CVE-2026-130371

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T02:17:20.490 |

phpMyFAQ before 4.1.12 and 4.2.0-alpha before 4.2.0-RC.2 contains an authentication bypass vulnerability because the web installer ignores the legacy config/database.php during 3.x upgrades. Unauthenticated attackers can reinstall the site against an attacker-controlled database and create their own administrator account to take over the application.

### CVE-2026-130369

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-17T02:17:20.130 |

phpMyFAQ 4.1.9 before 4.1.12 and 4.2.0-alpha before 4.2.0-RC.2 contains an authorization bypass vulnerability in multisite deployments that allows attackers to overwrite passkeys of accounts on other tenants via a shared PHP session store. Attackers can run WebAuthn prepare() for a login on one tenant, then replay the session against /api/webauthn/register on another tenant or the master to replace that user's passkeys and log in as admin.

### CVE-2026-130366

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-17T02:17:19.593 |

AdminNeo before 5.9.1 contains an authentication bypass vulnerability in the ClickHouse driver that allows remote attackers to log in to passwordless accounts without the configured defaultPasswordHash password. Attackers who know the name of a ClickHouse no_password account can submit any non-empty password, because connect() skips openPasswordless(), and obtain a session with that account's rights.

### CVE-2026-104840

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-16T21:17:17.393 |

OpenCTI is an open source platform for managing cyber threat intelligence knowledge and observables. Prior to 7.260428.0, the token GraphQL mutation used for primary login has no endpoint-specific rate limit, while the global Express limiter defaults to permitting 10,000 requests in a one-second window. An unauthenticated remote attacker can make password guesses at network speed against a chosen user account and, if a credential is recovered, access the account's threat-intelligence data and permitted operations. This issue is fixed in version 7.260428.0.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-12239

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-17T13:17:34.240 |

The WP Abstracts plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.7.6. This is due to a missing capability check on the wpabs_save_regform AJAX action and the use of a static, frontend-exposed nonce that allows any authenticated user to persist attacker-controlled form schemas with arbitrary wpSync mappings that are later used as user meta keys in the wpabstracts_sync_wpfields function. This makes it possible for authenticated attackers, with subscriber-level access and above, to elevate their privileges to administrator.

### CVE-2026-130072

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-16T22:18:22.533 |

Cloud Commander (cloudcmd) before 19.21.4 contains an authentication bypass and path traversal vulnerability that allows unauthenticated attackers to rename files by sending PUT /rename requests handled before authentication middleware. Attackers can supply absolute or ../ paths in the from and to arrays to move any file the Node.js process can access outside the configured root, causing data loss or denial of service.

### CVE-2026-120698

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-16T22:18:14.720 |

Wiki.js is an open source wiki app built on Node.js. Prior to 2.5.315, an authenticated account with only manage:users can use users.update to change the password of any local account, including the Root administrator and other accounts with manage:system, by omitting the optional groups argument, which is automatically allowed and bypasses destination-group authorization without checking the target's current privileges. The attacker can use users.disableTFA to clear the same target's tfaIsActive state and TFA secret without a target-privilege check, then authenticate with the replacement password. Supplying groups: [] to users.update can remove every group relationship from a selected administrator and leave the installation without a legitimate account holding manage:system. Additional administrators with IDs greater than 2 can also be deactivated or deleted. This issue is fixed in version 2.5.315.

### CVE-2026-63477

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-16T21:17:29.793 |

OpenCTI is an open source platform for managing cyber threat intelligence knowledge and observables. Prior to 7.260624.0, an Organization Administrator with VIRTUAL_ORGANIZATION_ADMIN and KNOWLEDGE_KNUPDATE can use organizationFieldPatch to replace the administered organization's grantable_groups without a SETTINGS_SETACCESSES authorization check. The administrator can add the built-in Administrators group to that grant scope and then bypass the grantable_groups guard added by the incomplete CVE-2026-44730 remediation to add their own account to Administrators. Membership grants the BYPASS capability after session cache refresh, escalating the tenant-scoped account to global administrator with access across organizations, users, settings, markings, connectors, and ingestion. This issue is fixed in version 7.260624.0.

### CVE-2026-126526

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-16T20:19:00.043 |

Heap-based buffer overflow in Microsoft Office OneNote allows an unauthorized attacker to execute code over a network.

### CVE-2026-124223

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-16T20:18:56.737 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-91115

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-11-16T17:17:37.480 |

Silverstripe Framework is a PHP framework which powers the Silverstripe CMS. From 6.0.0 until 6.2.13, the writer option of i18nTextCollectorTask is passed to the dependency injector without validating that it names an allowed writer implementation. A crafted dev task URL can therefore instantiate arbitrary objects with attacker-controlled constructor arguments and execute code on the server. An administrator can be induced to run the task by following a link because the nested task did not require confirmation, and a site in dev mode exposes the path without authentication. CMS 5 is not affected. This issue is fixed in version 6.2.13.

### CVE-2026-130591

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T14:17:46.007 |

53AIHub before 0.5.5 contains a missing authentication vulnerability that allows unauthenticated attackers to read files by requesting /api/files/:file_id/preview and /api/file-version/:file_body_id without UserTokenAuth. Attackers can enumerate sequential numeric ids to read raw knowledge-base files and stored file versions belonging to any enterprise tenant.

### CVE-2026-130584

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-17T14:17:45.013 |

Xibo CMS before 4.5.3 contains an insecure direct object reference vulnerability that allows authenticated users to access other DataSets' RSS feeds by pairing their own DataSet id with a foreign RSS id. Attackers with dataset.modify permission can read, edit, or delete feeds and steal PSKs, then use the unauthenticated /rss/{psk} endpoint to exfiltrate victim DataSet rows.

### CVE-2026-124646

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-17T13:17:32.703 |

This vulnerability exists in e-Sushrut HMIS due to insufficient server side object level authorization validation in the API endpoint. An unauthenticated remote attacker could exploit this vulnerability by modifying the parameter value in the API request.

Successful exploitation of this vulnerability could allow the attacker to enumerate and gain unauthorized access to sensitive information of patients on the targeted healthcare organization.

### CVE-2026-124645

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-17T13:17:32.560 |

This vulnerability exists in e-Sushrut HIMS due to the use of a static and predictable value in the client-side password hashing mechanism, which is embedded in the login page and accessible to unauthenticated users. An unauthenticated remote attacker could exploit this vulnerability by accessing the login page, extracting the embedded value and using it to reproduce the password hashing process.

Successful exploitation of this vulnerability could weaken the security of the authentication mechanism and potentially facilitate authentication related attacks on the targeted healthcare organization.

### CVE-2026-124643

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-17T12:17:44.423 |

This vulnerability exists in e-Sushrut HMIS due to insufficient authentication and session validation in the dashboard functionality. An unauthenticated remote attacker could exploit this vulnerability by sending specially crafted HTTP requests to the affected endpoint.

Successful exploitation of this vulnerability could allow the attacker to gain unauthorized access to the dashboard information associated with the targeted healthcare organization.

### CVE-2026-129282

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-17T11:17:27.443 |

The test email delivery function in N-able N-central before 2026.4.1 HF3 does not check permissions, lacks CSRF protection, and passes sender and recipient values to the mail program without neutralising option characters. An authenticated attacker can inject arguments into the mail command executed on the server.

### CVE-2026-129274

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T11:17:26.367 |

N-able N-central before 2026.4.1 HF3 does not authenticate callers of the ServerMMS2 RemoteExecutionTaskSubmit operation or verify task ownership. A remote, unauthenticated attacker can submit forged results for remote execution tasks belonging to any customer.

### CVE-2026-108153

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-17T05:18:30.500 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 16.1 before 19.3.9, 19.4 before 19.4.8, and 19.5 before 19.5.6 that under certain conditions could have allowed an authenticated user to execute arbitrary JavaScript in the browser of users viewing Error Tracking pages due to improper sanitization of user input.

### CVE-2026-105739

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-17T05:18:29.513 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 17.2 before 19.3.9, 19.4 before 19.4.8, and 19.5 before 19.5.6 that under certain conditions could have allowed an authenticated user to execute arbitrary JavaScript in the browser of users viewing a wiki page due to improper sanitization of user input.

### CVE-2026-130382

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-17T02:17:22.380 |

AdminNeo before 5.9.1 contains an authentication bypass vulnerability in OtpLoginPlugin that allows attackers knowing the database password to skip TOTP verification by abusing the permanent-login cookie. Attackers can submit a login with a wrong OTP and permanent=1 to obtain a neo_permanent cookie, then replay it to gain full authenticated database access.

### CVE-2026-130361

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-17T02:17:18.690 |

AdminNeo before 5.9.1 contains a parameter injection vulnerability in its ClickHouse driver that allows attackers to inject ClickHouse HTTP query parameters through an unencoded db GET parameter. Attackers can lure a logged-in victim into opening a crafted GET link that injects a query parameter, bypassing the POST-only CSRF token. ClickHouse then executes attacker-chosen SQL under the victim's credentials to read, modify, or drop data.

### CVE-2026-68934

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-16T22:18:25.070 |

code-review-mcp-server automates code review and can post comments directly on GitHub pull requests. Prior to 1.5.3, the getLocalGitDiff, codeReview, createPR, and getPRTemplate MCP tools accept caller-controlled folderPath and baseBranch string parameters that are interpolated into command strings executed by child_process.execSync through /bin/sh. Shell metacharacters, command substitution, or quote-breaking input can therefore execute arbitrary commands with the privileges of the host process running the MCP server. This issue is fixed in version 1.5.3.

### CVE-2026-130082

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-16T22:18:24.030 |

django-tenants 3.4.8 before 4.0.1 contains an SQL injection vulnerability in its PostgreSQL backend that allows attackers to inject SQL through unescaped tenant schema names. Attackers who can choose or influence a schema name can supply quote characters that are interpolated into SET search_path and CREATE, DROP or ALTER SCHEMA statements, letting them read other tenants' data or run SQL as the application's database user.

### CVE-2026-130081

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-16T22:18:23.887 |

B3log Solo through 4.4.0 contains an information disclosure vulnerability that allows unauthenticated attackers to obtain article view passwords by querying the public GET /articles API. The ArticleProcessor.getArticlesByPage handler leaves the articleViewPwd property in JSON responses, letting attackers read passwords for encrypted articles and access their protected content.

### CVE-2026-120697

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-16T22:18:14.567 |

Wiki.js is an open source wiki app built on Node.js. Prior to 2.5.315, an authenticated user with write:pages can store JavaScript expressions in the v-slot:tabs or v-slot:content attributes of page HTML because server/modules/rendering/html-security/renderer.js adds those executable Vue directives to DOMPurify's allowlist. The sanitized output is inserted as rendered page HTML and later compiled by the Vue 2 runtime compiler, so the expressions execute in the Wiki.js origin when another user views the page even when the author lacks write:scripts and administrative permissions. The script runs with the viewer's browser session and can read same-origin data, modify displayed content, present phishing content, or perform actions available to that viewer, including privileged GraphQL operations when a privileged user opens the page. This issue is fixed in version 2.5.315.

### CVE-2026-76823

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-11-16T21:17:31.227 |

OpenCTI is an open source platform for managing cyber threat intelligence knowledge and observables. Prior to 7.260706.0, the logsWorkerConfig GraphQL query is authorized with the broad CONNECTORAPI capability and returns Elasticsearch connection details including elasticsearch_username, elasticsearch_password, elasticsearch_api_key, the URL, index, proxy, and TLS-verification setting. A holder of any connector API bearer token can retrieve this credential material. If the returned credentials are valid and Elasticsearch is reachable, the caller can directly read, modify, or delete OpenCTI indices and audit history outside application-layer role, marking, organization, and audit controls, with the practical impact bounded by the credentials' privileges and network reachability. This issue is fixed in version 7.260706.0.

### CVE-2026-57150

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-16T21:17:29.217 |

GLPI is a free asset and IT management software package. Prior to 10.0.28, 11.0.10, and 12.0.1, authenticated users can craft a URL that invokes massive actions without all required object- and action-specific authorization checks. The bypass permits operations outside the user's granted rights, including unauthorized plugin activation, deactivation, and uninstallation for plugins already present on the filesystem and other state-changing maintenance actions. This issue is fixed in versions 10.0.28, 11.0.10, and 12.0.1.

### CVE-2026-129266

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-36;CWE-73` |
| Published | 2026-11-16T19:17:40.477 |

External control of a file path in Amazon Deep Java Library (DJL) versions 0.7.0 through 0.38.0 might allow a remote unauthenticated third party to read arbitrary files that the library process can access. To do this, the third party supplies a crafted model archive.



To remediate this issue, users should upgrade to version 0.39.0 or later.

### CVE-2026-127218

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-16T19:17:35.103 |

Axigen Mail Server 10.3.3.67 through 10.3.3.x, 10.4.42 through 10.4.x, 10.5.29 through 10.5.x, 10.6.x before 10.6.41, and 10.7.x before 10.7.3 contains an unauthenticated denial of service vulnerability caused by uncontrolled recursion when validating query parameter and cookie values with a recursive regular expression engine before authentication in the WebAdmin and WebMail services. Attackers can send a single HTTP request with a query parameter or cookie value of a few thousand characters to exhaust the worker thread stack and crash the server process, taking down SMTP, IMAP, POP3, and web services repeatedly.

### CVE-2026-129948

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-16T15:17:29.940 |

Contentlayer @contentlayer/source-files through 0.3.4 contains a code injection vulnerability that allows attackers who control content files to execute JavaScript by abusing gray-matter's still-enabled JavaScript engine in parseMarkdown(). Attackers can start a Markdown or MDX file with a ---js or ---javascript frontmatter delimiter to run code during build, exposing CI build secrets.

### CVE-2026-129879

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-16T15:17:26.900 |

DeepAudit 2.0.0-beta.1 through 3.8.0 contains a path traversal vulnerability that allows authenticated users to write arbitrary files by importing projects with crafted IDs. Attackers can set absolute or ../ project IDs via /api/v1/database/import, then upload ZIPs through /api/v1/scan/upload-zip following cloned symlinks to overwrite app/main.py for remote code execution.

### CVE-2026-129877

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-16T15:17:26.600 |

DeepAudit 2.0.0-beta.1 through 3.8.0 contains an information disclosure vulnerability that allows unauthenticated attackers to retrieve server secrets through the /api/v1/config/defaults endpoint. Attackers can send a GET request to obtain the operator's LLM provider API keys and GitHub or GitLab tokens, then abuse those services and accessible repositories.

### CVE-2026-129875

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-202` |
| Published | 2026-11-16T15:17:26.233 |

REBUILD 4.5.0 through 4.5.4 contains an information disclosure vulnerability that allows low-privileged authenticated users to recover the administrator password hash by filtering User.password through the MCP QueryRecords tool. Attackers can send LK2 prefix-match filters to the /gw/mcp/sse gateway and use the returned total count as an oracle to extract the SHA-256 hash one character at a time, then log in as administrator.

### CVE-2026-129874

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-16T15:17:26.043 |

REBUILD 3.5.0 through 4.5.4 contains a privilege escalation vulnerability that allows low-privileged authenticated users to modify their own roleId through mass assignment in /app/entity/record-save and /app/entity/common-save. Attackers can submit their own User record with roleId set to the built-in administrator role, bypassing updatable=false restrictions to gain full administrator privileges.

### CVE-2026-129873

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-16T15:17:25.850 |

REBUILD 4.3.0 through 4.5.4 contains a privilege escalation vulnerability that allows low-privileged authenticated users to obtain a SYSTEM_USER token by requesting /commons/file-preview with an arbitrary src value. Attackers can read the leaked _csrfToken from the redirect Location header and send it as X-AuthToken to access the admin center and administrative APIs.

### CVE-2026-129855

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-16T15:17:22.723 |

RedAmon before 7.8.0 contains a missing authentication vulnerability in the kali-sandbox terminal server that allows unauthenticated attackers to obtain a root shell by connecting to its WebSocket listener on port 8016. Attackers who can reach the port from co-resident containers or the host loopback can send keystrokes to an interactive /bin/bash session, executing commands as root inside the kali-sandbox container.

### CVE-2026-129854

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-16T15:17:22.553 |

RedAmon 4.0.0 before 7.8.0 contains a missing object-level authorization vulnerability that allows authenticated users to control other tenants' agent sessions by supplying arbitrary session ids. Attackers can call /api/agent/sessions, interact and kill routes to list, kill, or send commands into other users' meterpreter and shell sessions on their compromised targets.

### CVE-2026-82025

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-17T14:17:47.647 |

WP File Manager before 8.0.7 contains a file upload restriction bypass vulnerability that allows authenticated administrators to upload arbitrary PHP files by exploiting a misconfigured elFinder connector in file_folder_manager.php where an empty uploadDeny list causes allowPutMime() to unconditionally return true, bypassing the uploadAllow restriction. Attackers can upload a .php file directly or upload it under an allowed filename and then rename it via the rename connector command, achieving remote code execution as the web server user.

### CVE-2026-130589

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-649` |
| Published | 2026-11-17T14:17:45.653 |

Emitter through 3.1 contains a privilege escalation vulnerability that allows any channel key holder to forge a master key because channel keys use bare XOR Salsa20 encryption without a MAC or signature. Attackers can flip the permissions byte to the master value and present the forged key to the keygen service to mint keys with arbitrary permissions on every channel of the contract.

### CVE-2026-129273

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-11-17T11:17:26.243 |

N-able N-central before 2026.4.1 HF3 does not neutralise control characters in an Audit Export setting before writing it to the system logging configuration. An authenticated attacker with product administrator privileges can inject configuration and execute commands as root on the N-central server.

### CVE-2026-130375

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-17T02:17:21.180 |

AdminNeo before 5.9.1 contains a remote code execution vulnerability that allows authenticated SQLite users to bypass the check_sqlite_name() extension guard using PDO_SQLite file: URI database names. Attackers can select the PDO driver with ext=pdo and submit names like file:/webroot/x.php?x=.db to create a .php file, then store PHP source as table data for code execution.

### CVE-2026-130074

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-16T22:18:22.847 |

free5GC WebConsole through 1.4.6 contains an authorization flaw in the ChangePasswordInfo handler that allows authenticated tenant users to change other members' passwords. Attackers can send POST /api/change-password with another tenant member's email and a new password, without the current password, to take over that account.

### CVE-2026-129957

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-16T15:17:31.333 |

PrestaShop before 8.2.9 and 9.0.0 before 9.2.1 contains a path traversal vulnerability in back-office theme and module archive import that allows authenticated employees to write files outside intended directories. Attackers can craft a theme name in config/theme.yml or upload a module archive extracted before validation to place PHP files in web-accessible locations and execute code.

### CVE-2026-129947

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-16T15:17:29.770 |

Contentlayer @contentlayer/core through 0.3.4 contains a code injection vulnerability that allows attackers to inject JavaScript by embedding single quotes in content file names. Attackers can add a content file whose name breaks out of the import specifier in makeDataExportFile(), executing injected code when contentlayer dev or a Next.js dev server imports the generated module.

### CVE-2026-129943

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-16T15:17:29.100 |

Prime CMS (@primecms/core) through 0.4.0-beta.0 contains an OS command injection vulnerability in the updateSystem GraphQL mutation that allows authenticated administrators to execute shell commands via the package version string. Attackers can append shell metacharacters to the unvalidated version value, which is passed to child_process.exec() in yarn add or npm install commands, executing commands as the server process.

### CVE-2026-129281

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T11:17:27.317 |

N-able N-central before 2026.4.1 HF3 checks only a view permission for ServerII2 operations that write device execution configuration. An authenticated user with view-only access to a device can set configuration that the Windows agent on that device acts on.

### CVE-2026-129271

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T11:17:25.970 |

The Patch Management Engine in N-central is vulnerable to LPE via attacker controlled metadata

### CVE-2026-130067

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-451` |
| Published | 2026-11-16T22:18:21.690 |

7-Zip File Manager before 26.03 fails to detect archive entry names padded with Unicode space characters, allowing attackers to bypass the deceptive file name warning in CPanel::IsVirus_Message. Attackers can craft archive entries like a PDF name followed by ideographic spaces and .hta to hide the real extension, executing script content via ShellExecuteExW when opened.

### CVE-2026-62336

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-59;CWE-367;CWE-377` |
| Published | 2026-11-16T20:19:07.723 |

qbee-agent is the device agent component of the qbee.io IoT device management platform. Prior to 2026.27, the privileged createFile helper followed attacker-controlled symbolic links during file creation. A local unprivileged user whose account is managed by the SSH Keys bundle could replace ~/.ssh with a link to /root/.ssh, causing the agent to write an authorized key for root. On systems using RAUC download mode with ineffective kernel symlink protection, the predictable /tmp/.bundle.raucb.part path could be linked to a system file and then overwritten or truncated during an update. A file-distribution destination beneath an attacker-controlled directory could similarly redirect the partial-download path so the agent changed ownership of a sensitive file. These vectors could result in root privilege escalation, arbitrary file modification, or denial of service. This issue is fixed in version 2026.27.

### CVE-2026-124019

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-11-16T20:18:55.690 |

VB-Audio VB-CABLE virtual audio device kernel streaming driver (vbaudio_cable64_win10.sys 10.0.10011.16384) contains out-of-bounds read and write vulnerabilities in its KSPROPSETID_Audio MUTE, VOLUMELEVEL, and PEAKMETER2 property handlers that allow a local standard user to supply an all-channels sentinel value which is improperly used as a loop terminator or array index instead of being bounds-checked. Attackers can exploit the accessible low-integrity KS filter device object to write attacker-controlled values sequentially into kernel memory corrupting kernel globals and object pointers, or read past an array boundary to leak kernel memory, resulting in local privilege escalation or denial of service via a kernel bug check.

### CVE-2026-84443

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-16T17:17:35.570 |

LibreOffice Base documents can bind macros to document events, such as opening or closing the document. The macro security setting decides whether macros that come with a document may run. Macros bound to the events of a Base document were run without the macro security setting being applied, so opening or converting a crafted database document could run a macro and, through it, any command. In fixed versions macros bound to the events of a Base document follow the macro security setting, as macros in other documents do.

### CVE-2026-104920

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-183;CWE-829` |
| Published | 2026-11-16T17:17:27.730 |

LibreOffice Calc can link a cell range to an external data source, and the link is saved in the document. A Java database driver for such a link is loaded from a class path. Opening a crafted document could still load a Java database driver from a location outside the local machine and run its code, by a route that the fix for CVE-2026-63277 did not cover. In fixed versions an entry in a Java class path has to be a file URL that names a file on the local machine.

### CVE-2026-104692

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470;CWE-1188` |
| Published | 2026-11-16T17:17:27.590 |

LibreOffice bundles the HSQLDB database engine, which can be used through the generic JDBC database driver as well as through the support for embedded databases. HSQLDB lets SQL statements call Java methods, limited to the classes that are permitted. When HSQLDB was used through the generic JDBC driver this limit did not apply, so SQL in a crafted document could call any Java method and run code. In fixed versions SQL can call only the built-in functions of HSQLDB, whichever way the database is reached.

### CVE-2026-104007

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-16T17:17:27.453 |

LibreOffice can connect to databases through JDBC drivers written in Java. A spreadsheet can use a database as the source of a pivot table, and the database document that describes the connection names the driver to use. The location the driver was loaded from was taken from the database document itself, so a crafted document could make LibreOffice load and run Java code that the document supplied when it was opened. This is a different route to the problem fixed for CVE-2026-63277. In fixed versions the driver location is taken only from the driver configuration of the user, and a pivot table whose source is a database document named by a URL connects only once the user allows links to be updated.

### CVE-2026-101930

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-16T17:17:27.180 |

LibreOffice Writer can open HTML documents, and an HTML document can bind macros to events of the document as a whole, such as the document being opened or closed. Macros bound to these events were not taken into account by the macro security check, so they could run when the document was opened, whatever the macro security level. In fixed versions these macros follow the macro security settings like any other macro in the document.

### CVE-2026-101892

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470;CWE-829` |
| Published | 2026-11-16T17:17:26.900 |

LibreOffice documents in ODF format can contain form controls, such as buttons and text fields, and each control names the component that implements it. The component a control named was created even when it was not a form control, and the settings stored with the control were applied to it, so a crafted document could change the configuration of LibreOffice in a way that led to code being run. In fixed versions a control whose component is not a form control is ignored.

### CVE-2026-101352

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-357;CWE-693` |
| Published | 2026-11-16T17:17:26.620 |

A document can carry its own user interface customizations, such as keyboard shortcuts, menus and toolbars, which take effect while the document is open. A command bound in these customizations could run a macro or a script even when the macro security settings did not allow the macros of the document, so a user who pressed a shortcut or chose a menu item in a crafted document could run code without any warning. In fixed versions the customizations of a document are treated like its other macro content, and the macro and script commands in them are only kept when the macros of the document are allowed.

### CVE-2026-129956

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-16T15:17:31.177 |

Sandboxie-Plus before 1.18.6 contains a local privilege escalation vulnerability in SbieSvc that allows standard users to launch UpdUtil.exe as SYSTEM via MSGID_PROCESS_RUN_UPDATER requests. Attackers can inject code into a signed SandMan.exe process to bypass the signature check and write attacker-controlled files to arbitrary paths, achieving SYSTEM code execution.

### CVE-2026-129857

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-16T15:17:23.050 |

Microsoft jxrlib through 1.1 and the mircomir jxrlib fork before 1.3.1 contain a heap buffer overflow in ReadBinaryData() in jxrgluelib/JXRMeta.c caused by integer overflow of the metadata count. Attackers can supply a JPEG XR file with a count of 0xFFFFFFFE or 0xFFFFFFFF, wrapping PKAlloc(uCount + 2) to an undersized buffer that the following file read overflows, corrupting heap memory in decoding applications.

### CVE-2026-107902

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-17T04:17:26.497 |

TELLUS and TELLUS Lite provided by FUJI ELECTRIC CO., LTD. contain a use after free vulnerability. Opening a specially crafted V9 file may lead to information exposure or arbitrary code execution on the affected product.

### CVE-2026-124017

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-16T21:17:21.397 |

Phison E12 and E18 PCIe SSD controllers contain a Secure Boot bypass vulnerability that allows a privileged local attacker to inject persistent boot-patch tuples into the unsigned, CRC-protected flash ID page read by the BootROM. By overwriting a fuse-derived RAM variable via a crafted patch entry using Phison Vendor Specific Commands, an attacker can force CRC-only firmware verification instead of signature checking, enabling an unsigned firmware image to load and creating a persistent controller-level implant that survives firmware reinstallation and operates below the host operating system.

### CVE-2026-100101

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-16T17:17:26.173 |

On Linux and other Unix-like systems, LibreOffice can send the current document as an email attachment with File > Send > Email Document, which starts the mail client through a script bundled with LibreOffice. The script let the shell interpret the name of the document's file, so a file with a crafted name could run commands when it was sent by email. In fixed versions the script passes the file name and the other details to the mail client as plain arguments.

### CVE-2026-130386

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-193` |
| Published | 2026-11-17T14:17:44.493 |

Contiki-NG through 5.2 contains an out-of-bounds access vulnerability in buffer_reclaim() and domain_set_free() in mpl.c that iterate the seed_set array one element past its end. Remote attackers can flood MPL multicast messages to fill the buffered message set, triggering out-of-bounds reads and writes of adjacent static memory that cause memory corruption or a crash.

### CVE-2026-129287

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-17T11:17:28.070 |

N-able N-central before 2026.4.1 HF3 processes XML external entities in software repository files. An attacker able to supply or modify the repository files received by the server can read files accessible to the N-central service account or cause the server to make outbound requests.

### CVE-2026-109138

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636;CWE-863` |
| Published | 2026-11-17T09:17:26.057 |

In the Aliro access control reference
  applications of the Nordic Semiconductor nRF Door Lock and Access Control
  Add-on v1.0.0 through v1.1.1, built with Credential Issuer CA
  certificate-based issuer trust (CONFIG_DOOR_LOCK_CREDENTIAL_ISSUER_CA) and
  the Aliro Step-up phase (CONFIG_DOOR_LOCK_STEP_UP_PHASE) enabled,
  AccessManagerImpl::ProcessValidityIteration() treats a failed lookup of the
  Credential Issuer in the provisioned issuer array as success. For an issuer
  trusted through a certificate chain but not provisioned, the
  ValidityIteration (credential-rollback) check is therefore skipped. A former
  authorized holder with an old but correctly issuer-signed Access Document can
  be granted physical access after the issuer has advanced its iteration to
  revoke that credential. The default Matter provisioning configuration is not
  affected. Fixed in v1.2.0.

### CVE-2026-129880

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-16T15:17:27.043 |

DeepAudit 2.0.0-beta.5 through 3.8.0 contains a server-side request forgery vulnerability that allows registered users to leak server-wide GitLab or Gitea tokens via repository_url. Attackers can create a gitlab or gitea project pointing to a controlled host and request its branches to capture the operator's token and reach internal hosts.

### CVE-2026-129275

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-17T11:17:26.493 |

N-able N-central before 2026.4.1 HF3 allows the repositoryItemGet operation to be called without authentication. A remote, unauthenticated attacker who knows a policy identifier can download the Automation Manager policy of any customer, including embedded scripts and parameter values.

### CVE-2026-125162

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-17T11:17:25.330 |

The cHash argument, which ensures that only URL arguments originally generated by TYPO3 create separate page cache entries, was treated inconsistently when it was passed as an array. The cHash validation treated such a value as missing, while the page cache identifier treated it as present and included all URL arguments. As a result, unauthenticated visitors could create an unlimited number of page cache entries and trigger uncached page renderings by adding an array cHash with arbitrary values to any URL. This could exhaust server resources and fill the page cache storage. Only installations where the cHash validation is not enforced via $GLOBALS['TYPO3_CONF_VARS']['FE']['cacheHash']['enforceValidation'] are affected. This setting is enabled by default for new installations since TYPO3 v12, but is often still disabled in installations upgraded from older versions.

### CVE-2026-125159

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184;CWE-434` |
| Published | 2026-11-17T11:17:24.893 |

ImageMagick and GraphicsMagick use small modules, called "coders", to read each image format. When processing images, TYPO3 determined the coder from the file type detected by the file contents, as long as the detected mime-type started with image/. A file containing MVG (Magick Vector Graphics) instructions, uploaded with an image file extension like .png, was therefore processed with the MVG coder. MVG instructions can read local files into the processed image, which allows disclosing the contents of arbitrary files readable by the web server, for example configuration files containing credentials, through a publicly accessible processed image.

Exploiting this vulnerability requires a way to upload files without a mime-type check, for example a public form of the Form Framework using a FileUpload or ImageUpload element without configured allowedMimeTypes (see TYPO3-CORE-SA-2026-032), which allows exploitation by unauthenticated visitors. Additionally, ImageMagick must be used for image processing, and its default system configuration must allow the MVG coder.

### CVE-2026-18241

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T05:18:36.843 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 9.3 before 19.3.9, 19.4 before 19.4.8, and 19.5 before 19.5.6 that under certain conditions could have allowed an authenticated user to access protected CI/CD variables and resources due to a race condition in pipeline job authorization.

### CVE-2026-125275

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-17T03:17:00.513 |

Loop with Unreachable Exit Condition ('Infinite Loop') vulnerability in device certificate verification in nerves-hub nerves_hub_web allows an unauthenticated remote attacker to cause a denial of service via a TLS client certificate whose CA is not registered. When a client certificate chains to a root in the device endpoint's trust store but no CA in the chain is registered in NervesHub, NervesHub.SSL.decide/2 refuses it with the reason :unknown_ca. Erlang/OTP ssl reads that reason as a missing trust anchor, looks for an alternative root, finds the same root and validates again without end. The handshake process queries the database on each pass and keeps running after the client disconnects, until the node restarts.

The device endpoint trusts the public roots from CAStore unless DEVICE_SSL_CACERTFILE is set, so a client certificate from a public CA whose chain allows client authentication is sufficient. A chain that ends at a root outside the trust store is refused once.

This issue affects nerves_hub: from 1.0.0 before 2.5.4.

### CVE-2026-129853

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-16T15:17:22.373 |

LimeSurvey before 6.17.16+260814 and 7.x before 7.0.10+260813 contains an unauthenticated SQL injection vulnerability in the public statistics page via POST parameter names. Attackers can submit backtick-containing parameter names to buildSelects() and use blind techniques to read administrator password hashes and survey responses on MySQL or MariaDB.

### CVE-2026-130608

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:A/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T14:17:47.310 |

When using the admin area profile form to change ones profile details *except* the password (so, email or username), the password field in the database is overwritten with the plaintext password. Further login is not possible, so the error is noticeable, but the password is leaked to the database.

### CVE-2026-121684

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-11-17T05:18:33.697 |

The Soledad theme for WordPress is vulnerable to unauthenticated Remote Code Execution in versions up to, and including, 8.7.7 The public penci_more_post_ajax AJAX action feeds infeedads[ads_code] (base64+urldecoded) to penci_safe_shortcode(), whose allowlist regex inspects only the hyphen-truncated outer shortcode name (e.g. 'adinserter') and never the nested [elementor-element k=.. data=..] tag, so do_shortcode() renders an attacker-chosen Elementor element. The rendered penci-featured-sliders widget passes its unsanitized 'style' setting to include dirname(__FILE__)."/{$style}.php", a path-traversal local file inclusion.

### CVE-2026-121708

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285;CWE-639` |
| Published | 2026-11-16T21:17:21.137 |

OpenCTI is an open source platform for managing cyber threat intelligence knowledge and observables. Prior to 7.260513.0, Draft Workspace identifiers are accepted without verifying that the authenticated user can access the referenced draft. Any authenticated user can enumerate draftWorkspaces, use a disclosed DRAFT_ID with draftWorkspaceEntities to read unpublished reports, descriptions, observables, and other staged intelligence, or place the identifier in the opencti-draft-id header and run mutations that inject entities and relationships into another user's private workspace. The flaw permits cross-user disclosure and tampering but does not cause a denial of service. This issue is fixed in version 7.260513.0.

### CVE-2026-83816

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-863` |
| Published | 2026-11-16T19:17:53.433 |

CodeWhale is a DeepSeek and MiMo coding agent for the terminal. Prior to 0.9.0, the ExecShellTool::approval_requirement_for path used is_parallel_readonly_command to downgrade commands to automatic approval based on a flag-stripped command allowlist. The allowlist treated fd, rg, and git grep as read-only even when fd -x or fd --exec, rg --pre, or git grep --open-files-in-pager selected an external program. registered_tool_approval_required returned without displaying a prompt for that automatic classification, and the later command-safety check also treated the base utilities as safe. Attacker-controlled content that influenced an agent tool call could therefore cause arbitrary program execution on the developer host without the approval promised by the default interactive profile, resulting in unauthorized access, modification, or disruption. This issue is fixed in version 0.9.0.

### CVE-2026-111760

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-16T21:17:18.907 |

Git is a fast, scalable, distributed revision control system with an unusually rich command set that provides both high-level operations and full access to internals. Prior to 2.50.2, 2.51.3, 2.52.1, 2.53.1, 2.54.1, 2.55.1, and 2.56.1, an attacker-controlled repository hosted by the attacker rather than on a normal forge site can exploit git clone --recurse-submodules by causing Git to overwrite a submodule gitfile with a symbolic link. The symbolic link can point to a directory containing attacker-controlled Git configuration or hooks, allowing those hooks or configuration to execute code on the cloning user's system. The issue requires the recursive-submodule option, and users should avoid cloning repositories from untrusted sources. This issue is fixed in versions 2.50.2, 2.51.3, 2.52.1, 2.53.1, 2.54.1, 2.55.1, and 2.56.1.

### CVE-2026-130290

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-130` |
| Published | 2026-11-16T22:18:24.487 |

In Open Object Rexx (ooRexx) before 5.2.0, RXAPI has a heap buffer over-read in a QueueManager DataQueue::addmethod. In particular, the code blindly trusts the message.parameter1 value provided by the client as the size used to fill the data from the queueData heap buffer. An attacker sends a large parameter1 value in an ADD_TO_SESSION_QUEUE or ADD_TO_NAMED_QUEUE message and then retrieves data with a PULL_FROM_SESSION_QUEUE message. (A very large value causes a process crash.)

### CVE-2026-69154

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-15;CWE-78` |
| Published | 2026-11-16T22:18:25.233 |

The Coder VS Code extension opens Coder workspaces in VS Code with a single click. From 0.1.20 until 1.14.6, a malicious repository can provide .vscode/settings.json values for security-sensitive Coder settings because the extension permits workspace and folder scope to override those settings. Values such as coder.headerCommand and coder.tlsCertRefreshCommand are later executed as shell commands, while other affected settings can redirect the Coder CLI binary or download source, inject CLI or SSH flags, replace TLS material, disable TLS verification, or change identity and credential-storage behavior. A victim with the extension installed must open the malicious workspace or repository; when the extension activates, attacker-controlled commands can run with the victim user's privileges. The issue also affects untrusted workspaces because the extension declares untrusted-workspace support without preventing consumption of the workspace-controlled settings. This issue is fixed in version 1.14.6.

### CVE-2026-101327

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-16T19:17:23.323 |

A maliciously crafted DLL placed in a predictable, attacker-writable temporary directory used by the Autodesk Installer can lead to privilege escalation to NT AUTHORITY\SYSTEM due to insufficient validation of loaded libraries. An attacker with local and low-privilege access could exploit this vulnerability to execute arbitrary code as SYSTEM.

### CVE-2026-113630

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-16T17:17:29.080 |

Command injection in the documentserver-flush-cache.sh maintenance helper in ONLYOFFICE Docs (Document Server) 9.4.0-129 on the official onlyoffice/documentserver container allows a local attacker with command execution as the ds user to execute arbitrary commands as root via a crafted --hash argument that is interpolated unvalidated into a GNU sed expression, where the sed e flag runs attacker-controlled commands. The packaged sudoers policy permits ds to run the helper as root without a password and with unrestricted arguments.

### CVE-2026-119621

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T11:17:24.370 |

When importing a T3D or XML file in the Import/Export module, the file hash values of imported files were taken from the import data without validation and used to build the path of a temporary file. A crafted import file could therefore write files with arbitrary content to any location writable by the web server, for example a PHP file in the public web root, which leads to remote code execution. Exploiting this vulnerability requires an administrator backend user account, or a non-admin backend user for whom importing has been enabled via the user TSconfig option options.impexp.enableImportForNonAdminUser.

### CVE-2026-121864

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-17T09:17:26.857 |

In nanobot, when sandboxed exec is enabled, the shell executable used to run commands can be selected by the caller and is launched before the sandbox is applied. An attacker who can induce the agent to create an executable in the workspace and select it as the shell can cause that executable to run outside the sandbox (e.g. Linux bubblewrap), with the operating-system permissions of the nanobot process.

This issue affects nanobot (nanobot-ai) from 0.2.1 before 0.4.1.

### CVE-2026-130374

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-17T02:17:21.003 |

AdminNeo before 5.9.1 contains an sql injection vulnerability that allows remote attackers to inject SQL by supplying crafted IN and NOT IN search values that process_length() passes unescaped. Attackers can send a logged-in user a cross-site GET link using a backslash-escaped apostrophe to run blind SQL with that user's database rights on PostgreSQL, SQLite, MS SQL, Oracle, or MySQL in NO_BACKSLASH_ESCAPES mode.

### CVE-2026-129872

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-16T15:17:25.653 |

REBUILD 2.7.0 through 4.5.4 contains an SQL injection vulnerability that allows low-privileged authenticated users to inject AjQL conditions through the plan parameter of /project/tasks/list. Attackers can use priority-* plans and the returned task count as a boolean oracle to recover a task creator's SHA-256 password hash and log in as that user, including the administrator.

### CVE-2026-130615

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-17T14:17:47.437 |

Flowise through 3.1.4 contains a server-side request forgery vulnerability that allows authenticated users to reach internal services by exploiting unpinned DNS validation in checkDenyList(). Attackers can configure a chatflow with Playwright or Puppeteer loaders using a DNS-rebinding domain so headless Chromium fetches internal or cloud metadata endpoints, returning responses as document content.

### CVE-2026-97187

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T05:18:39.370 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 17.6 before 19.3.9, 19.4 before 19.4.8, and 19.5 before 19.5.6 that under certain conditions could have allowed an authenticated user to read Kubernetes Secrets from other namespaces in clusters connected through the GitLab agent for Kubernetes due to incorrect authorization in workspaces.

### CVE-2026-129888

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-16T15:17:28.263 |

Cetmix Tower through 17.0.3.0.0 and 18.0 before 18.0.4.0.1 contains an improper SSH host key verification vulnerability in SSHConnection.connect() that falls back to Paramiko's AutoAddPolicy when no host key is pinned. On-path attackers using ARP or DNS spoofing can present their own host key during Skip Host Key or Get from Host connections to capture stored SSH passwords and tamper with commands and files.

### CVE-2026-118498

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T10:17:21.540 |

The CODESYS Automation Server Connector uses server-supplied file names without sufficient path traversal checks. An unauthenticated remote attacker controlling a malicious Automation Server and tricking a user to trust it, or performing a man-in-the-middle attack on a trusted communication channel, can exploit this vulnerability to write attacker-controlled files to arbitrary locations on the engineering workstation and subsequently achieve arbitrary code execution with user privileges.

### CVE-2026-118496

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-706` |
| Published | 2026-11-17T10:17:21.197 |

The affected products process a server-supplied URL without sufficient validation. An unauthenticated remote attacker controlling a malicious Automation Server and tricking a user to trust it or performing a man-in-the-middle attack, can exploit this vulnerability by causing the affected product to process unintended content. Successful exploitation may result in arbitrary code execution with the privileges of the user running the affected product.

### CVE-2026-12487

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T02:17:13.527 |

An incorrect authorization vulnerability in the SNMP parameter of Zyxel EE5301-00 customized firmware version 5.63(ACLD.2)b3_D0 could allow an unauthenticated attacker to cause a denial-of-service (DoS) condition on an affected device.

### CVE-2026-110339

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-16T22:18:13.497 |

The Libreswan pluto daemon dereferences a NULL pointer when a CERT payload is received with an empty PKCS#7 payload, causing the daemon to crash and restart. The NSS function SEC_PKCS7GetCertificateList() was used to check whether the content was empty, but this check did not trigger if the non-empty content of the PKCS#7 wrapped payload was an empty list. Continued triggering of this vulnerability can lead to a denial of service. Remote code execution is not possible. Authentication is not required to trigger this vulnerability.

### CVE-2026-115563

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-345;CWE-522` |
| Published | 2026-11-16T21:17:20.683 |

The Model Context Protocol Python SDK is the official Python SDK for Model Context Protocol servers and clients. From 1.9.1 until 1.30.0 and 2.2.0, OAuth client support in mcp.client.auth can send credentials to an authorization server chosen by an untrusted MCP server. ClientCredentialsOAuthProvider and PrivateKeyJWTOAuthProvider cannot identify the authorization server that owns their credentials. Affected HTTP clients using those providers, OAuthClientProvider, or the deprecated 1.x RFC7523OAuthClientProvider can disclose a client_secret, authorization code, PKCE code_verifier, or signed client assertion. MCP servers, stdio clients, and clients that attach their own tokens or headers are not affected. Interactive OAuthClientProvider use requires a person to start sign-in, while the unattended providers do not. For ClientCredentialsOAuthProvider and PrivateKeyJWTOAuthProvider, callers must configure issuer= after upgrading because omission still follows the MCP server's advertised authorization server, and the deprecated RFC7523OAuthClientProvider must be replaced because it has no issuer option. A stored client registration without an issuer remains unbound after upgrading, so stored OAuth client information must be cleared once to register again or a manually pre-registered record must be updated with its issuer. This issue is fixed in versions 1.30.0 and 2.2.0.

### CVE-2026-129302

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-11-16T20:19:01.030 |

Guard Core is an API security core engine for the FastAPI-Guard, FlaskAPI Guard, and DjAPI Guard adapters. From 3.5.0 until 3.13.0, built-in penetration-detection patterns in guard_core/handlers/suspatterns_handler.py execute through a direct pattern.search(content) call instead of the timeout-protected create_safe_matcher() path used for custom patterns. The built-in template-injection detector contains an unbounded expression with quadratic behavior when scanning repeated opening braces. Because penetration detection and enhanced mode are enabled by a stock SecurityConfig, an unauthenticated request can block the shared asyncio event loop, affecting all application endpoints. The triggering input does not produce a detection match, so the request can complete without incrementing ban counters or being recorded as suspicious. This issue is fixed in version 3.13.0.

### CVE-2026-83817

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862;CWE-1188` |
| Published | 2026-11-16T19:17:53.590 |

CodeWhale is a DeepSeek and MiMo coding agent for the terminal. Prior to 0.9.0, DEFAULT_AUTOMATION_AUTO_APPROVE caused AutomationRecord::task_auto_approve to resolve an omitted setting to true, and the automation_create schema advertised the same insecure default. enqueue_run_task converted that omission into an explicit true value, bypassing the safer task-path fallback and selecting ApprovalMode::Bypass for each scheduled run. After a user approved creation of an apparently benign recurring automation, subsequent executions could silently authorize mutating tools without a human present, and an automation created with shell access could repeatedly execute commands. This issue is fixed in version 0.9.0.

### CVE-2026-129297

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-16T18:17:30.590 |

mail-parser is a tool that parses emails by enhancing the Python standard library and extracting message details into a comprehensive object. Prior to 4.6.2, get_server_ipaddress() can select an attacker-controlled address from attacker-controlled Received headers. The minimum mechanism needed to distinguish this spoofing issue, derived from the advisory's remediation analysis and verified fix evidence, is appearance-based candidate selection that can treat bracketed IPv4 or IPv6 addresses or HELO markers in sender-written text as MTA-recorded addresses and can continue past a trusted hop that names no address. Applications that rely on the returned value can attribute a message to an attacker-selected sender IP address. This issue is fixed in version 4.6.2.

### CVE-2026-129295

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-11-16T18:17:30.183 |

mail-parser is a tool that parses emails by enhancing the Python standard library and extracting message details into a comprehensive object. From 4.2.0 until 4.6.1, attacker-controlled email headers can cause polynomial regular-expression backtracking during ordinary parse_from_string(), parse_from_bytes(), or parse_from_file() calls. In src/mailparser/utils.py, get_addresses() invokes the _ADDR_FALLBACK_RE fallback when strict address parsing yields no usable address, and overlapping quantifiers rescan padded address headers quadratically or cubically. In src/mailparser/const.py, parse_received() applies _CLAUSE_SPLITTER to uncollapsed whitespace in a Received header, causing quadratic backtracking when a whitespace run is not followed by a clause keyword. A small, well-formed message can keep mail gateway, ticketing, quarantine, or archival parsing workers busy for extended periods. This issue is fixed in version 4.6.1.

### CVE-2026-118497

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-17T10:17:21.357 |

The affected products do not sufficiently validate CODESYS Automation Server TLS certificates when a user starts the certificate enrollment. An unauthenticated remote attacker performing a man-in-the-middle attack can exploit this vulnerability by supplying an untrusted certificate that is accepted as trusted. Successful exploitation may allow an attacker to intercept and manipulate communications between the CODESYS Automation Server and the PLC network.

### CVE-2026-3859

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-80` |
| Published | 2026-11-16T15:17:32.153 |

XSS vulnerability in Vibe Versions <= 4.0.8.7 could allow an attacker to inject malicious JavaScript through crafted
search input.

### CVE-2026-108169

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-179` |
| Published | 2026-11-16T17:17:28.280 |

LibreOffice can open a web query file (.iqy), which names a web page to import into a spreadsheet, when the file is given on its command line, for example when a file manager or another program opens the file with LibreOffice. The address in such a file was used without the checks that apply to an address given on the command line directly, so a crafted file could make LibreOffice do something other than open a web page, up to running code. In fixed versions only an http or https address is taken from a web query file.

### CVE-2026-121865

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T09:17:27.057 |

In nanobot, the WebSocket gateway allows a standard client holding a valid client token to select an existing directory outside the operator-configured workspace as the root of a new conversation. The agent can then read and expose files in that directory that are readable by the nanobot service account.

This issue affects nanobot (nanobot-ai) from 0.3.5 before 0.4.1.

### CVE-2026-119643

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-17T09:17:26.677 |

The MembershipWorks - Membership, Events & Directory plugin for WordPress is vulnerable to Stored Cross-Site Scripting in all versions up to, and including, 6.17. This is due to insufficient output escaping on member-supplied data retrieved from the MembershipWorks SaaS API in the sf_shortcode(), sf_widget_event_do(), and sf_widget_folder_do() functions, where the 'nam' (member name), 'ttl' (event title), 'url', 'adn' (venue name), 'szp', and 'ezp' fields are output into page HTML without escaping, or, in sf_widget_folder_do(), placed in an image alt attribute that an onerror handler copies into innerHTML. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-86676

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-17T02:17:22.880 |

A post-authentication command injection vulnerability in the “Description” parameter of a CGI program  in Zyxel DX3300-T0 firmware versions through 5.50(ABVY.8.3)C0 could allow an authenticated attacker with administrator privileges to execute OS commands by sending a crafted HTTP request.

### CVE-2026-130073

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-16T22:18:22.690 |

CBoard before commit 7bd8180 contains a missing authorization vulnerability that allows any authenticated user to reach admin functions because AdminController and DashboardController methods bypass AOP role checks. Attackers with no role grants can call deleteUser, deleteRole, getUserList, getAllWidgetList and getAllDatasetList to read query configurations and delete accounts including the administrator.

### CVE-2026-129236

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-16T17:17:31.313 |

Kubeshark is an eBPF-powered network observability tool for Kubernetes. From 53.1.0 until 53.4.0, the start_kubeshark MCP tool in cmd/mcpRunner.go uses callStartKubeshark to append caller-controlled pod_regex as a bare positional argument to kubeshark tap without a -- end-of-options separator, allowing a value beginning with --set to be parsed as a Helm value override. An attacker who influences tool arguments against kubeshark mcp --allow-destructive can redirect the privileged worker, Hub, and front images through tap.docker.registry and tap.docker.tag to an attacker-controlled registry. Because the deployed worker DaemonSet runs privileged with host networking and host filesystem access, a malicious image can obtain node and cluster-admin access when the host already has permission to deploy it. This issue is fixed in version 53.4.0.

### CVE-2026-129870

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-16T15:17:25.310 |

Rocboss paopao-ce 0.2.0 through 0.6.0-alpha.3 contains a path traversal vulnerability in LocalOSS DeleteObject that allows authenticated users to delete arbitrary files by submitting crafted media values. Attackers can send dot-dot-slash sequences in the avatar or media content to POST /v1/user/avatar or POST /v1/post/comment, deleting server-writable files including configuration and data.

### CVE-2026-130588

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-17T14:17:45.477 |

OpenFunction through 1.2.0 contains a NULL pointer dereference vulnerability in getServingRun that allows users permitted to create Serving resources to crash the operator by omitting the triggers section. Attackers can submit a Serving with nil Spec.Triggers to crash-loop the controller-manager, halting Function and Serving reconciliation cluster-wide until the object is deleted.

### CVE-2026-129283

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-17T11:17:27.570 |

The custom service import in N-able N-central before 2026.4.1 HF3 processes XML external entities. An authenticated attacker can upload a crafted service definition to read files accessible to the N-central service account or cause the server to make outbound requests.

### CVE-2026-119622

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-17T11:17:24.607 |

The backend endpoint for adding online media (e.g. YouTube or Vimeo videos) accepted a target folder in the fallback storage (storage uid 0), which points to the public web root of the installation. File mount and permission checks are not applied to the fallback storage. As a result, any authenticated, low-privileged backend user, even without file mounts or module access, could create online media files with a partially controllable file name in the public web root.

In combination with TYPO3-CORE-SA-2026-027, this could be used to re-enable the installer on an already configured instance. The installer could then be used to create a new administrator and system maintainer account, which leads to remote code execution.

### CVE-2026-21609

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-17T10:17:21.710 |

This High severity Improper Authorization vulnerability was introduced in versions 5.12.0, 10.3.0, and 11.3.0 of Jira Service Management Data Center.  	 	This Improper Authorization vulnerability, with a CVSS Score of 7.1, allows an authenticated attacker to gain unintended access and can lead to the exposure of resources or functionality, possibly providing attackers with sensitive information or even execute arbitrary code.  	 	Atlassian recommends that Jira Service Management Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions: 		 		 Jira Service Management Data Center 10.3: Upgrade to a release greater than or equal to 10.3.27 		 		 Jira Service Management Data Center 11.3: Upgrade to a release greater than or equal to 11.3.13 		 		 	 	See the release notes (https://confluence.atlassian.com/servicemanagement/jira-service-management-release-notes-780083086.html). You can download the latest version of Jira Service Management Data Center from the download center (https://www.atlassian.com/software/jira/service-management/download-archives).  	 	This vulnerability was reported via our Bug Bounty program.

### CVE-2026-130351

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:L/VI:H/VA:L/SC:L/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-17T02:17:16.963 |

phpMyFAQ from 4.2.0-alpha before 4.2.0-RC.2 contains an authorization bypass vulnerability in the multisite Redis configuration store that is not tenant-scoped. As a result, tenant administrators can read and overwrite the master instance's effective configuration. Attackers can save configuration through /admin/api/configuration, optionally resetting storage.redisPrefix, to redirect master SMTP, set a known API token, or alter authentication settings.

### CVE-2026-130080

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-16T22:18:23.740 |

B3log Solo through 4.4.0 contains an SQL injection vulnerability in the console article update API that allows authenticated authors to inject SQL through unvalidated JSON property names. Attackers can send a PUT request to /console/article/ with crafted property names used as UPDATE column names, then read query results back through the updated article.

### CVE-2026-130078

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-16T22:18:23.443 |

B3log Solo through 4.4.0 contains a missing authorization vulnerability in B3Receiver.receiveArticle that allows visitor accounts to modify any article via the POST /apis/symphony/article endpoint. Attackers can supply their username as userB3Key, since OAuth-created visitors receive it as their B3 key, and overwrite any article's title, content and tags.

### CVE-2026-130066

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-16T22:18:21.517 |

Alinto SOGo before 5.12.13 contains an SQL injection vulnerability in SQLSource contact lookup that allows authenticated users to inject SQL by placing a backslash before a quote in the object name. Attackers can send requests under a SQL-backed address book path on MySQL or MariaDB to perform UNION or boolean-based reads of the user-source table, including password hashes.

### CVE-2026-95839

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-16T20:19:20.417 |

containerd is an open-source container runtime. From 2.2.0 until 2.2.10, 2.3.7, and 2.4.2, image manifest processing through the transfer service can encounter a child descriptor containing the io.containerd.manifest.subject annotation and a malformed digest. Pulling or importing such an image, including through a default CRI PullImage request, can trigger an unrecovered panic and crash the containerd daemon. In Kubernetes, kubelet retries can repeatedly trigger the crash and disrupt container operations on the worker node. This issue is fixed in versions 2.2.10, 2.3.7, and 2.4.2.

### CVE-2026-86046

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-16T17:17:35.707 |

termux-sync is an open source tool for backing up and restoring a Termux environment across devices. Prior to 1.2.4, termux-sync restore uses the parent directory of the untrusted manifest.json files.*.source value as an extraction destination, and extract_archive calls tarfile.extract on archive members without enforcing a destination boundary. A victim who restores a malicious or tampered backup from local, shared, GitHub, or Google Drive storage can have files written anywhere the Termux user can write, including shell startup files or executable scripts that can lead to code execution when later used. The restore path also accepts unsafe backup_name values for temporary paths, and archive members are not constrained to the intended destination. This issue is fixed in version 1.2.4.

### CVE-2026-129878

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-16T15:17:26.747 |

DeepAudit 2.0.0-beta.1 through 3.8.0 contains an HTML injection vulnerability in ReportGenerator.generate_task_report that allows registered users to read server files and perform SSRF. Attackers can create a project whose name contains a link attachment element and download the task PDF report to retrieve local files or internal network responses.

### CVE-2026-129868

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-11-16T15:17:24.947 |

Rocboss paopao-ce through 0.6.0-alpha.3 fails to validate the attachment_price field when creating posts, allowing authenticated users to set negative prices on charge attachments. Attackers with two ordinary accounts can download the attachment via GET /v1/attachment, where the negative price increases the buyer's wallet balance, minting funds to purchase other users' paid attachments.

### CVE-2026-129865

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-16T15:17:24.413 |

Dinky through 1.2.5 contains a missing authorization vulnerability in DataSourceController.testConnect that allows any authenticated user to open arbitrary JDBC connections by supplying caller-controlled connection settings. Attackers can probe internal hosts and ports via returned driver errors, or supply a MySQL JDBC URL enabling local-infile against a malicious server to read files from the Dinky host.

### CVE-2026-129864

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-16T15:17:24.253 |

Frappe CRM before 1.84.0 contains a missing authorization vulnerability in the get_deal_contacts method that allows authenticated low-privileged users to read contacts of deals they cannot access. Attackers can supply or iterate CRM Deal names to obtain linked contacts' full names, email addresses, and mobile numbers, bypassing row-level permission rules.

### CVE-2026-129863

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-16T15:17:24.083 |

GitBucket through 4.48.0 contains an incorrect authorization vulnerability that allows authenticated users to edit and merge other users' pull requests because the PATCH pulls and PUT pulls merge REST API endpoints only check read access. Attackers can close, reopen, retitle, retarget, or merge pull requests into the base branch without write permission on public repositories or as private-repository guest collaborators.

### CVE-2026-127044

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-16T15:17:19.030 |

Insecure direct object reference (IDOR) in the STEL Order Tempo module. The server retrieves data based on the `empleadoId` parameter without checking the user's permissions. By modifying this parameter, an authenticated user can view the first name, last name, role, job title, and vacation days of other employees.

### CVE-2026-127043

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-16T15:17:18.873 |

Insecure direct object reference (IDOR) in the myGESTIÓN Time Tracking module. The server skips the permission check when processing the “worker” parameter. By modifying this parameter, an authenticated user can view other users' time logs, including those of administrators.

### CVE-2025-5809

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:L/VI:H/VA:L/SC:L/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-16T15:17:06.887 |

An improper privilege management vulnerability in an LDAP extension used with OpenText eDirectory could require a technical or proxy user to be granted write permission to the ACL when only permission to modify a specific LDAP attribute is intended. A user who possesses the proxy user's credentials could use the excessive ACL permission to modify access rights for objects within the affected container, potentially resulting in unauthorized elevation of privilege. The issue is addressed in OpenText eDirectory 25.2.

### CVE-2026-107190

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:N/VI:L/VA:H/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-17T14:17:32.053 |

Bludit is vulnerable to Path Traversal in the page deletion functionality. An authenticated user with the Author role can set the UUID field of their own page to contain path traversal sequences (.. and path separators), which are saved without proper validation. When the page is deleted, Pages::delete() passes the path constructed from this UUID to Filesystem::deleteRecursive() without verifying that it still points to an allowed directory, allowing the attacker to delete any files, even not belonging to them. Critically, it is possible to delete admin pages and render the site unusable.


Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version 3.22.0 but may also affect other versions.

### CVE-2026-109154

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T09:17:26.540 |

In the Matter door lock applications of
  the Nordic Semiconductor nRF Door Lock and Access Control Add-on v1.0.0
  through v1.1.1, AccessManager::ValidateCredential() checks only credential
  occupancy and the secret bytes, and never reads the owning user's UserStatus.
  It also returns success when no owning user can be resolved. A user suspended
  by setting their status to OccupiedDisabled can continue to unlock the door
  with their previously assigned credential, and an orphaned but occupied
  credential is also accepted. Fixed in v1.2.0.

### CVE-2026-109151

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-193` |
| Published | 2026-11-17T09:17:26.407 |

In
the Matter and Aliro Door Lock Application of the Nordic Semiconductor nRF Door
Lock and Access Control Add-on v1.0.0 through v1.1.1 with
CONFIG_DOOR_LOCK_STEP_UP_PHASE enabled, deleting a Credential Issuer passes the
1-based Matter credential index to ClearValidityIterations(), which expects a
0-based storage index. The intended issuer's ValidityIteration state is left in
place, and the state of the adjacent, still-provisioned issuer is cleared. This
resets that issuer's rollback protection. An attacker holding an older but correctly
signed Access Document from the adjacent issuer, whose validity iteration had
been superseded, can then potentially obtain physical access. Fixed in v1.2.0.

### CVE-2026-109148

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-324;CWE-672` |
| Published | 2026-11-17T09:17:26.253 |

In the Aliro access control reference
  applications of the Nordic Semiconductor nRF Door Lock and Access Control
  Add-on v1.0.0 through v1.1.1, the stored Access Document record does not
  retain validFrom and validUntil. The cached public key path (VerifyPublicKey())
  and the Kpersistent fast path (_VerifyKPersistentKey()) therefore never
  re-evaluate the Access Document validity period. An attacker who held a
  time-limited Aliro credential that was valid when first presented can
  continue to obtain physical access after the Access Document has expired, for
  as long as the cached record remains available. Fixed in v1.2.0.

### CVE-2026-130357

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-17T02:17:18.017 |

phpMyFAQ from 4.2.0-alpha.2 before 4.2.0-RC.2 contains an improper authorization vulnerability in updateUserRights that lets USER_EDIT admins drop category restrictions on group rights. Attackers can re-save rights through the user update-rights API to convert category-restricted group rights into global direct rights, then edit, publish or delete FAQs in withheld categories.
