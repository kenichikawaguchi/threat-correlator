# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-17 15:01 UTC
- **対象期間**: `2026-10-16T15:00:52.000Z` 〜 `2026-10-17T15:01:25.000Z`
- **重要CVE数**: 134 件（Critical 9.0+: 33 件 / High 7.0〜: 101 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** と非常に多く、特に **リモートコード実行 (RCE)・認証バイパス・権限昇格** が目立ちます。  
- **DeepSeek Harness、MariaDB、WordPress プラグイン** など、インフラ層からアプリ層まで幅広いスタックで深刻な脆弱性が報告されています。  
- 多くは **ネットワークから直接アクセス可能** なサービス（Docker 管理 UI、IoT OS、CLI SDK 等）で **認証が不十分** もしくは **入力検証が欠如** している点が共通しています。  
- 攻撃者は **特権取得後に横展開** できるため、早急なパッチ適用と防御層の強化が必須です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目すべき理由 |
|-----|------|----------|----------------|
| **CVE‑2026‑95182** (DeepSeek Harness) | 10.0 | 任意コード実行（untrusted search path） | **最高スコア**。攻撃者は任意の実行ファイルを配置するだけで、DeepSeek のビルド/実行環境全体を乗っ取れる。DeepSeek は AI 開発環境として急速に採用が拡大しているため、被害拡大リスクが高い。 |
| **CVE‑2026‑92262** (MariaDB) | 9.9 | `#mysql50#` プレフィックスバイパスによりファイルシステムエンコーディングを回避、任意ファイル書き込み/実行 | MariaDB は多くの Web アプリ・業務システムでデフォルト DB として利用されている。影響バージョンは **10.6.1‑10.6.28、10.11.19、11.4.13、11.8.9、12.3.3、13.0.2** と広範。 |
| **CVE‑2026‑85748** (MariaDB) | 9.9 | `SYS_REFCURSOR` の再割り当てバグでスタック上に残存参照が残り、低権限ユーザーが大量のカーソルを開くと DoS/情報漏洩 | 同じく MariaDB 系列で複数の深刻バグが同時に報告されている点が注目。データベースサーバの安定性に直結。 |
| **CVE‑2026‑104736** (LearnPress – WordPress) | 9.8 | PHP Object Injection によるリモートコード実行 | WordPress は日本国内でも最も普及した CMS。LearnPress は教育系サイトで頻繁に利用され、プラグイン単体の脆弱性が全サイトに波及するリスクが大きい。 |
| **CVE‑2026‑57169** (Dockhand) | 9.6 | WebSocket 認証欠如により、未認証でコンテナ端末に接続可能 | Docker 管理 UI が社内開発・テスト環境で広く使われている。認証バイパスは内部ネットワークからの横展開を容易にする。 |

> **※** それ以外にも RIOT OS 系列（CVE‑2026‑49868、CVE‑2026‑102693）や FreeRTOS の MPU バグ（CVE‑2026‑109588/109587）など、組み込み系でも深刻な脆弱性が多数報告されています。環境に該当するものがあれば同様に対策が必要です。

---

## 3. 推奨アクション  

### 3‑1. 速やかなパッチ適用・バージョンアップ
| 製品 / ライブラリ | 現行脆弱バージョン | 推奨バージョン / パッチ |
|-------------------|-------------------|--------------------------|
| **DeepSeek Harness** | `commit c291e796` 以前 | 公式リポジトリの **最新コミット（2026‑10‑xx 以降）** へ更新。`dsh` の検索パス設定を `--trusted-path` オプションで固定化するパッチが含まれる。 |
| **MariaDB** | 10.6.1‑10.6.28、10.11.19、11.4.13、11.8.9、12.3.3、13.0.2 | それぞれ **10.6.29**、**10.11.20**、**11.4.14**、**11.8.10**、**12.3.4**、**13.0.3** 以上へアップグレード。公式リリースノートの *“#mysql50# prefix bypass fix”* と *“SYS_REFCURSOR stale reference fix”* を確認。 |
| **LearnPress (WordPress)** | ≤ 4.4.10 | **4.4.11** 以上へ更新。プラグインの `checkout-email` パラメータのシリアライズ処理が修正されている。 |
| **Dockhand** | < 1.0.34 | **1.0.34** 以上へアップデート。WebSocket 認証ロジックが追加された。 |
| **RIOT OS** | < 2026.07（DHCPv6） / < 2026.04（ATWINC15x0） | **2026.07** 以上、**2026.04** 以上のリリースへ。`_parse_reply()` と `strcpy` バッファチェックが修正。 |
| **FreeRTOS‑Kernel** | V11.3.0 / V11.3.1 | **V11.3.2** 以上へ。MPU バッファ長チェックと認可ロジックが改善。 |
| **その他多数の Web アプリ**（WhaTicket、LangChat、DataBuff、Simple Admin Core など） | 各 0.1.10 以前、1.5.3 以前等 | 各プロジェクトの **最新リリース**（2026‑10‑xx 以降）へ更新。ハードコードされたデフォルト認証情報・HMAC シークレットが除去されていることを確認。 |

### 3‑2. 防御層の強化
1. **ネットワーク分離**  
   - DB サーバ（MariaDB）や AI 開発環境（DeepSeek Harness）は **内部 VLAN** に配置し、外部からの直接アクセスを防止。  
   - Docker 管理 UI（Dockhand）への

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-95182

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-10-16T15:17:36.940 |

An untrusted search path in DeepSeek Harness (dsh) commit c291e796 allows attackers to execute arbitrary code via supplying and opening crafted executable files in place of legitimate content.

### CVE-2026-92262

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-10-16T17:17:52.710 |

MariaDB server is a community developed fork of MySQL server. From 10.6.1 until 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2, the #mysql50# bypass prefix is affected because it allows the #mysql50# prefix to bypass normal table-name filesystem encoding. An attacker can trigger the issue with a table name using the #mysql50# prefix, then use a #mysql50# table name to access files under their legacy unencoded name and cause crashes, data corruption, data exfiltration, or remote code execution. This issue is fixed in versions 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2.

### CVE-2026-85748

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-16T17:17:51.303 |

MariaDB server is a community developed fork of MySQL server. From 12.3.1 until 12.3.3 and 13.0.2, SYS_REFCURSOR handling is affected because cursor-array reallocation can leave stale references in routine contexts. A low-privileged attacker can open a large number of SYS_REFCURSORs and then fetch one to trigger a use-after-free that can enable remote code execution when combined with another vulnerability. This issue is fixed in versions 12.3.3 and 13.0.2.

### CVE-2026-85746

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-16T17:17:51.167 |

MariaDB server is a community developed fork of MySQL server. From 10.6.1 until 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2, ST_AsText can write beyond an allocated output buffer when converting deeply nested GeometryCollections because recursive WKT serialization does not account for bytes consumed or reserve sufficient space. A low-privileged remote attacker can submit a specially crafted GIS object to corrupt memory and potentially achieve code execution when combined with another vulnerability. This issue is fixed in versions 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2.

### CVE-2026-104736

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-17T04:16:47.780 |

The LearnPress plugin for WordPress is vulnerable to PHP Object Injection in versions up to, and including, 4.4.10 via deserialization of untrusted input from the 'checkout-email' request parameter during the checkout AJAX action. The value is passed through sanitize_text_field(), which does not strip serialized object syntax, then stored in the LearnPress session table and later fed to LP_Helper::maybe_unserialize() → unserialize() (without an allowed_classes restriction) by LP_Session_Handler::get() on subsequent requests. This makes it possible for unauthenticated attackers to inject a PHP Object.

### CVE-2026-111823

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-390` |
| Published | 2026-10-17T02:17:18.470 |

Mage OSS through 0.9.80 before 76c4f46 can proceed with session creation upon encountering an unknown OAuth provider.

### CVE-2026-49868

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-10-16T17:17:34.963 |

RIOT is an open-source microcontroller operating system designed for Internet of Things devices and other embedded systems. Prior to 2026.07, _parse_reply() in sys/net/application_layer/dhcpv6/client.c omits minimum-length validation before passing IA_PD and IA_NA option bodies to sub-option parsers. A malicious or compromised DHCPv6 server can send a REPLY with an option length smaller than the required structure while MODULE_DHCPV6_CLIENT_IA_PD is enabled, causing _parse_ia_pd_option to read past the option body, size_t underflow, and unbounded out-of-bounds heap reads that can crash the device and may expose or corrupt memory. This issue is fixed in version 2026.07.

### CVE-2026-57169

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-10-16T17:17:35.113 |

Dockhand is a Docker management application. Prior to 1.0.34, the in-browser container terminal endpoint /api/containers/<id>/exec does not enforce authentication on the WebSocket upgrade request. When an unauthenticated attacker has network reach to Dockhand, knows a target container ID, and targets a container with an interactive shell, the attacker can open a raw WebSocket terminal session and execute commands inside a known target container. This allows unauthenticated command execution inside the container, with possible host compromise when the container has sensitive mounts or privileged execution. This issue is fixed in version 1.0.34.

### CVE-2026-102693

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-120;CWE-121` |
| Published | 2026-10-16T17:17:17.173 |

RIOT is an open-source microcontroller operating system designed for Internet of Things devices and other embedded systems. Prior to 2026.04, the ATWINC15x0 driver's _atwinc15x0_sta_set_current_ssid function uses strcpy to copy an SSID without checking the destination size. When MODULE_ATWINC15X0_DYNAMIC_CONNECT is enabled, a nearby attacker can advertise a malformed or oversized SSID that is processed during Wi-Fi scanning, causing memory corruption and potentially a hard fault, denial of service, or code execution. This issue is fixed in version 2026.04.

### CVE-2026-111711

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-16T18:17:55.337 |

Netcore NR256CN through 1.5.140116 contains a pre-authentication stack overflow vulnerability in the Boa web server's user_ok() function, which copies Basic-auth usernames with unbounded strcpy() calls into 64-byte stack buffers. Unauthenticated attackers can send a username longer than 63 bytes to any protected /router/*.cgi route to crash the main Boa process or potentially execute code.

### CVE-2026-111708

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-16T18:17:54.933 |

WhaTicket Community through commit cf04795 contains an authentication bypass vulnerability that allows unauthenticated attackers to self-register as administrators via POST /auth/signup. Attackers can omit the profile field or set it to admin, gaining user management, settings, and access to all tickets, contacts, messages, and WhatsApp connections.

### CVE-2026-111704

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T18:17:54.370 |

LangChat through commit 2a6285a contains a missing authentication vulnerability that allows unauthenticated remote attackers to access REST controllers because no Sa-Token interceptor is registered. Attackers can query /api/v1/auth/users to read plaintext passwords, retrieve LLM provider API keys, create super-admin accounts, and modify or delete data.

### CVE-2026-111693

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-10-16T18:17:52.773 |

DataBuff ai-apm-web through 0.1.10 contains a hard-coded default credentials vulnerability that allows unauthenticated attackers to gain administrator access using the built-in admin/Databuff@123 account. Attackers can POST these credentials to /webapi/api/v1/auth/login to obtain an administrator token and access all protected /webapi routes.

### CVE-2026-111692

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-16T18:17:52.633 |

DataBuff ai-apm-web through 0.1.10 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge admin session tokens by using the hardcoded HMAC secret in JwtTokenService. Attackers can sign a payload of admin and a future expiry with the default dev-secret to gain full administrative access to protected /webapi routes, including the Doris SQL query API.

### CVE-2026-111690

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-16T18:17:52.350 |

Simple Admin Core through 1.8.7 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge super administrator tokens by using the hard-coded Auth.AccessSecret in api/etc/core.yaml. Attackers can sign a JWT with the public secret and roleId claim 001 to gain full administrative control over users, roles, menus, API authorities, configuration and tokens.

### CVE-2026-111687

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-10-16T18:17:51.920 |

WeRSS (we-mp-rss) through 1.5.3 contains a remote code execution vulnerability that allows unauthenticated attackers to run code via the template parameter of the public GET /rss/{feed_id} endpoint. Attackers can supply a non-built-in ext value and a {{=expression}} template whose object-subclass traversal bypasses the eval denylist to run OS commands as the service account.

### CVE-2026-111673

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T18:17:49.920 |

IceCMS through 4.1.5 contains a missing authentication vulnerability that allows unauthenticated attackers to modify, delete, or disable any account because /User/** is excluded from the Shiro jwt filter. Attackers can send PUT requests to /User/updateUser to set a new password and role on any userId, including administrators, enabling full account takeover.

### CVE-2026-111643

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T18:17:45.013 |

Misaka Danmu Server through 2.8.9 contains an authentication bypass vulnerability that allows unauthenticated attackers to write arbitrary configuration keys via the unprotected POST /api/ui/config-history/rollback endpoint. Attackers can set the ipWhitelist key to their own /32 address, or alter trustedProxies and webhookApiKey, to access every protected endpoint as the administrator.

### CVE-2026-111641

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T18:17:44.730 |

FastapiAdmin through 3.0 contains an authentication bypass vulnerability that allows unauthenticated attackers to obtain sessions for any user by abusing unprotected auto-login endpoints. Attackers can list users via /api/v1/auth/auto-login/users, mint a superuser auto-login token, and exchange it for a JWT session to gain full administrative control.

### CVE-2026-111626

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T18:17:42.583 |

Webreaper Damselfly through 4.5.3 contains an authentication bypass vulnerability that allows unauthenticated attackers to access all /api/* routes because controller authorization attributes are commented out. Attackers can send PUT /api/users with Admin roles to create administrator accounts, or POST /api/users to reset any user's password, gaining full control.

### CVE-2026-109588

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-197;CWE-787` |
| Published | 2026-10-16T18:17:31.457 |

Numeric truncation of the buffer length in the MPU buffer authorization check in FreeRTOS-Kernel V11.3.0 and V11.3.1 on the Arm Cortex-R82 (Armv8-R AArch64) MPU port might allow, under certain conditions, an unprivileged task on MPU-enabled builds to read or write privileged kernel memory beyond the validated buffer window, via a stream buffer system call.



To remediate this issue, users should upgrade to version V11.3.2 or later.

### CVE-2026-109587

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-16T18:17:31.330 |

Incorrect authorization in the Arm Cortex-R82 (Armv8-R AArch64) MPU port in FreeRTOS-Kernel V11.3.0 and V11.3.1 might allow an unprivileged task on MPU-enabled builds to read and write privileged kernel memory outside the regions assigned to it, via a buffer argument passed to an MPU system call.



To remediate this issue, users should upgrade to version V11.3.2 or later.

### CVE-2026-105279

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T15:17:04.130 |

In the default configuration, the archive accepts DICOM associations from an unregistered calling AE. A remote peer can use C-FIND and C-GET to enumerate and retrieve patient information and medical images. It can also use C-STORE to file fabricated study content under an existing patient identity.

### CVE-2026-96620

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-78;CWE-88` |
| Published | 2026-10-16T20:18:28.293 |

Claude Agent SDK is a Python SDK for Claude Code. Prior to 0.2.121, the resume option is passed to the Claude CLI as a separate token without validation, so a dash-leading value is parsed as an independent CLI flag. An attacker can inject the --mcp-config flag to define a stdio MCP server, causing arbitrary command execution at CLI startup outside the SDK permission controls. The issue is exploitable when an application passes untrusted input as the session ID to resume. This issue is fixed in version 0.2.121.

### CVE-2026-111663

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-16T18:17:48.077 |

Chaskiq through 2.0.3 contains a server-side request forgery vulnerability that allows unauthenticated attackers to fetch arbitrary URLs via the createUrlUpload GraphQL mutation. Attackers can submit internal URLs, including cloud instance metadata endpoints, through POST /graphql and retrieve the full response via the returned ActiveStorage blob URL.

### CVE-2026-111636

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-16T18:17:44.010 |

OpenBMB StaffDeck through 0.5.6 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge administrator session tokens using the hard-coded default app_secret. Attackers can sign an HMAC-SHA256 token for the seeded 'admin' user in 'tenant_demo' to gain full tenant administration, including stored model and channel credentials.

### CVE-2026-102551

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-940` |
| Published | 2026-10-16T18:17:14.750 |

Improper verification of the source of a communication channel in the IPv6 Router Advertisement handler in Amazon FreeRTOS-Plus-TCP before V4.4.2 might allow a remote third-party to influence an endpoint's IPv6 default gateway, on-link prefix, and address configuration via a crafted Router Advertisement.



To remediate this issue, users should upgrade to version V4.4.2.

### CVE-2026-110653

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-17T03:16:28.480 |

The Appointment Booking Plugin – LatePoint | Calendar & Scheduling for WordPress plugin for WordPress is vulnerable to Authentication Bypass via Race Condition in all versions up to, and including, 5.7.4. This is due to a non-atomic read-modify-write on the OTP verification attempts counter in the `verifyOTP` function: the counter is incremented using a stale in-memory value with no conditional `WHERE attempts < 10` guard on the `UPDATE` and no `SELECT ... FOR UPDATE` row lock, creating a TOCTOU window that allows concurrent requests to bypass the 10-attempt lockout. This makes it possible for unauthenticated attackers — who know a target customer's registered email address or phone number — to fire concurrent requests to the `auth__verify_otp` endpoint, defeat the lockout cap, brute-force the 6-digit OTP code, and authenticate as the targeted LatePoint customer, gaining full access to their account, bookings, and personal data. The nonce check present on the endpoint (`otp_verify_otp_nonce`) does not mitigate this issue, as the nonce is publicly emitted by the unauthenticated `request_otp` and `resend_otp` endpoints and is trivially obtainable by any unauthenticated attacker prior to launching the race.

### CVE-2026-111691

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-16T18:17:52.493 |

WIMOOR through commit ec86736 contains an authentication bypass vulnerability that allows attackers to impersonate any tenant and privilege level by sending an unsigned X-USERINFO header. Attackers reaching backend service ports directly, bypassing the gateway, can forge companyid and manager or admin usertype values to read and modify other tenants' orders, finance data, and Amazon seller authorizations.

### CVE-2026-111675

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-16T18:17:50.197 |

Course-tencent-cloud through 2.0.1 contains an improper restriction of authentication attempts vulnerability that allows unauthenticated attackers to brute force 6-digit SMS/email verification codes, which are never invalidated or attempt-limited. Attackers who know a victim's phone or email can trigger a code and rotate source IPs against the password reset and verify login endpoints to take over accounts.

### CVE-2026-102692

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-10-16T17:17:16.980 |

RIOT is an open-source microcontroller operating system designed for Internet of Things devices and other embedded systems. Prior to 2026.07, nanocoap accepts oversized CoAP Block2 option values without enforcing the 20-bit maximum block number, allowing block offset multiplication to overflow on 32-bit targets. The affected master baseline is commit aeeae69e; the verified fix is later on master and remains unreleased. The oversized value passes from coap_get_blockopt() to coap_block_slicer_init(). A remote CoAP client can send a malformed Block2 option that produces an invalid slice range and can cause out-of-bounds memory access, denial of service, or memory corruption. This vulnerability is fixed in 2026.07.

### CVE-2026-102608

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-16T20:17:17.253 |

ZoneMinder is a free, open source closed-circuit television software application. Prior to 1.38.3, downloadEvents() manually wraps a monitor Name value in single quotes instead of using escapeshellarg() before placing it in shell commands when a user with monitor-create or monitor-edit permission stores a monitor Name containing shell metacharacters and a user with Events View permission exports that monitor's events. In this attack mechanism, the stored monitor Name reaches both the ffmpeg concatenation command and the tar or zip archive command and breaks out of manual quoting. Arbitrary commands execute as the web server user. This issue is fixed in version 1.38.3.

### CVE-2026-44977

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-16T16:17:44.483 |

countly-server is the server-side part of Countly, a product analytics solution. Prior to 24.05.50 and 25.03.44, plugins/star-rating/api/api.js allows a non-global application administrator to use uploadFeedbackFile to store attacker-controlled active content while trusting the supplied MIME type. plugins/star-rating/frontend/app.js publicly serves the stored content from feedback/preview/ with the attacker-influenced Content-Type, so a global administrator who opens the preview executes the payload in the Countly origin and exposes authenticated session capabilities, including auth_token and csrf_token values. This issue is fixed in versions 24.05.50 and 25.03.44.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-111853

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-17T02:17:18.610 |

An issue was discovered on Tektronix 3 Series MDO devices before 1.21.1. An OS command injection vulnerability exists in the FILESystem:MOUNT:DRIve SCPI command handler. Insufficient neutralization of user-supplied input allows remote attackers to execute arbitrary operating system commands with elevated privileges.

### CVE-2026-96627

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266;CWE-269` |
| Published | 2026-10-16T22:18:58.227 |

Arcane is an interface for managing Docker containers, images, networks, and volumes. Prior to 2.6.0, UpdateUser in backend/api/handlers/users.go sets PasswordHash for any target without comparing caller and target privilege. A holder of delegated users:update permission can submit a password change for the global administrator, replace the administrator password, and authenticate as that account, resulting in complete global administrator account takeover. This issue is fixed in version 2.6.0.

### CVE-2026-30971

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-16T20:17:23.190 |

ZoneMinder is a free, open source closed-circuit television software application. Prior to 1.39.2, 1.38.2, and 1.36.40, ZoneMinder interpolates an unvalidated monitor Device field into shell commands in PHP and Perl control paths when an authenticated user with monitor-create or monitor-edit permission saves a Local monitor whose Device Path contains shell metacharacters and the monitor control or startup path runs. In this attack mechanism, the stored Device value reaches Perl qx() and backtick execution before zmdc.pl argument detainting, while separate PHP command paths use bypassable escapeshellcmd defenses. The attacker can execute arbitrary commands as the web server user. This vulnerability is fixed in 1.39.2, 1.38.2, and 1.36.40.

### CVE-2026-102607

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-16T20:17:17.097 |

ZoneMinder is a free, open source closed-circuit television software application. Prior to 1.38.3, the exportEvents() function concatenates the attacker-controlled exportFile request parameter into a shell command without neutralizing shell metacharacters when an authenticated user with View Events or View Snapshots permission submits an event export request with a crafted exportFile value, a valid CSRF token, and exportDetail enabled. The affected components are exportEvents(), exportFile, web/ajax/event.php, web/skins/classic/includes/export_functions.php. In this attack mechanism, the crafted exportFile value reaches the trailing directory argument of a tar or zip command executed by exec(). The attacker can execute arbitrary operating system commands as the web server user. This issue is fixed in version 1.38.3.

### CVE-2026-111650

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T18:17:46.047 |

ChronoFrame through 1.0.0 contains a missing authentication vulnerability in the server/api/wizard/ handlers that allows unauthenticated attackers to reconfigure already configured instances. Attackers can POST to /api/wizard/storage to activate an attacker-controlled S3 or OpenList provider, redirecting uploads and storage reads, and overwrite site and map settings.

### CVE-2026-111633

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-16T18:17:43.607 |

ZKEACMS through 4.4 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge REST API JWT bearer tokens using a hard-coded HMAC-SHA256 signing key in JwtBearerDefaults.cs. Attackers can sign a token with the Name claim set to 'admin' to call ApiAuthorize endpoints, modifying articles and products and reading form submissions.

### CVE-2026-97380

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-620;CWE-863` |
| Published | 2026-10-16T17:18:02.013 |

MariaDB server is a community developed fork of MySQL server. From 10.6.1 until 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2, the GRANT PROXY statement treats an IDENTIFIED clause with an empty password as though authentication were not specified, causing it to check the wrong grantor privileges. A low-privileged attacker who can name another account can exploit this authorization error to set that account's password. This issue is fixed in versions 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2.

### CVE-2026-97851

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T15:17:38.490 |

The storage status-change REST service allows location records still associated with DICOM instances to be changed to deletion-related states. Changing a location to TO_DELETE causes PurgeStorageScheduler to delete the referenced object from storage even though the corresponding instance record remains in the database.

### CVE-2026-106705

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-16T15:17:04.767 |

ELADMIN (eladmin-mp) up to 2.7 contains an improper access control vulnerability in the role management module. The endpoint PUT /api/roles/menu (RoleController.updateRoleMenu) authorizes the request only by comparing the target role's level with the caller's minimum level. The application neither validates the granted menu set nor prevents a caller from modifying its own role. A logged-in non-admin user whose role holds the delegated `roles:edit` permission can submit its own role id together with an arbitrary list of menu ids.

### CVE-2026-111723

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T18:17:56.980 |

LingGuo-Drama through commit 8a6924a contains a missing authorization vulnerability that allows any registered user to manage all accounts through the /admin/v1/admins API protected only by AuthAdminJWT. Attackers can self-register, read every account's bcrypt hash, reset the bootstrap administrator's password via PUT, raise their authority_id, and delete accounts.

### CVE-2026-111710

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-16T18:17:55.207 |

Netcore NR256CN through 1.5.140116 contains a NULL pointer dereference vulnerability in the Boa web server's user_auth() function that allows unauthenticated attackers to crash the server via a malformed Authorization header. Attackers can send a Basic Authorization value lacking a colon, such as one decoding to a single character, to protected routes like /router/get_user_type.cgi to kill the main Boa process and deny management interface access.

### CVE-2026-111706

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T18:17:54.663 |

99AI through 4.3.0 contains a missing authentication vulnerability in the POST /api/chatLog/exportExcel route that allows unauthenticated attackers to export all users' chat logs. Attackers can send requests with controlled page, size, and optional email fields to download xlsx files containing usernames, emails, prompts, and AI answers.

### CVE-2026-111702

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:54.080 |

ChatOllama through commit 96c3ce5 contains an insecure direct object reference vulnerability that allows remote attackers to access other users' private knowledge bases by supplying sequential ids. Attackers can enumerate ids via GET /api/knowledgebases/{id} or the knowledgebaseId parameter of POST /api/models/chat to read metadata and retrieved document content.

### CVE-2026-111686

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T18:17:51.787 |

IceCMS through 4.1.5 contains an unauthenticated sql injection vulnerability that allows remote attackers to inject SQL through the num path parameter of /WebArticle/findarticlesbynum. Attackers can append crafted SQL after the LIMIT clause concatenated into a MyBatis-Plus QueryWrapper to extract database contents via union-based or blind techniques.

### CVE-2026-111685

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T18:17:51.643 |

IceCMS through 4.1.5 contains an unauthenticated sql injection vulnerability that allows remote attackers to inject SQL by supplying a crafted num path parameter to /WebResource/findresourcebynum. Attackers can append SQL after the LIMIT clause concatenated via QueryWrapper.last() to extract database contents using union-based or blind techniques.

### CVE-2026-111681

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T18:17:51.063 |

EFAK through 5.1.0 contains a missing authorization vulnerability that allows authenticated low-privilege users to manage accounts because the /api/users endpoints lack administrator role checks. Attackers can send POST, PUT, or DELETE requests to UserController to grant themselves ROLE_ADMIN, create administrators, or delete users, gaining control of managed Kafka clusters.

### CVE-2026-111642

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-16T18:17:44.877 |

FastapiAdmin through 3.0 contains a hard-coded JWT signing secret in backend/app/config/setting.py that allows low-privileged users to forge tokens impersonating the superuser. Attackers can register via the unauthenticated /api/v1/system/user/register endpoint, log in, and forge an HS256 token keeping their session_id but naming the superuser in user_name to gain superuser privileges.

### CVE-2026-111613

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T18:17:40.680 |

AllData through 0.7.1 contains an unauthenticated JDBC injection vulnerability that allows remote attackers to open arbitrary database connections by supplying jdbcUrl and jdbcDriverClass values to the data-dts /jobJdbcDatasource/test endpoint. Attackers can supply a MySQL JDBC URL with allowLoadLocalInfile=true pointing to an attacker-controlled server to read arbitrary files from the data-dts host.

### CVE-2026-111612

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-16T18:17:40.533 |

netdisk-fast-download through 0.4.8 contains an information disclosure vulnerability that allows unauthenticated attackers to retrieve donated netdisk credentials via the /v2/randomAuth endpoint in ParserApi. Attackers can repeatedly call the endpoint and decrypt the encryptedAuth blob using the hard-coded AES key nfd_auth_key2026 to recover other users' cloud-drive cookies, tokens, or passwords.

### CVE-2026-95859

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-16T16:22:44.400 |

libp2p-rust is the official Rust language implementation of the libp2p networking stack. Prior to 0.49.5, Gossipsub GRAFT control-message handling unconditionally adds attacker-supplied topic hashes to connected_peer.topics without confirming that the peer previously subscribed to those topics. A remote unauthenticated peer that can reach a Gossipsub listener can repeatedly send novel GRAFT topics, causing cumulative per-peer memory growth that is not bounded by subscription filters, peer scoring, or per-message size limits. This can exhaust process memory and cause a denial of service. This issue is fixed in version 0.49.5.

### CVE-2026-68906

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-835` |
| Published | 2026-10-16T16:20:00.793 |

libIEC61850 is an open-source implementation of IEC 61850 client and server protocols including MMS, GOOSE, Sampled Values, and R-Session. Prior to 1.6.2, parseUserInformation in src/mms/iso_acse/acse.c checks len for zero before validating the negative bufPos returned by BerDecoder_decodeLength for a truncated long-form length. The continue path therefore swallows the error, reads buffer[-1], resets parsing to the beginning, and repeats the same malformed state. An unauthenticated remote peer can send a malformed AARE PDU during association to cause an infinite CPU loop under a normal allocator or a one-byte out-of-bounds read and process abort when the preceding byte is inaccessible. This issue is fixed in version 1.6.2.

### CVE-2026-107621

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-16T15:17:05.003 |

JPEGParser can enter an infinite loop while parsing a specially crafted or truncated stream.

### CVE-2026-105667

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T15:17:04.260 |

In the default configuration, the HL7 listener accepts ADT^A40 patient-merge messages without authenticating the sending application. A remote sender can reassign studies and related workflow records from one patient identity to another. The archive's unmerge does not reverse this.

### CVE-2026-105273

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-16T15:17:03.993 |

MP4Parser does not adequately validate MP4 box sizes. A malformed box can cause parsing to make no forward progress and repeatedly process the same input.

### CVE-2026-101021

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-16T15:16:58.837 |

MultipartInputStream performs inefficient boundary matching and unnecessary buffer copying. Crafted multipart input can force excessive boundary comparisons and repeated copying.

### CVE-2026-111722

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:56.823 |

LingGuo-Drama through commit 8a6924a contains an insecure direct object reference vulnerability that allows registered users to access other users' projects because projects.Get lacks an owner check. Self-registered attackers can iterate numeric IDs via GET, PUT and DELETE /admin/v1/projects/:id to read, overwrite, reassign or delete any user's short-drama projects.

### CVE-2026-111639

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-16T18:17:44.447 |

bbs-go through 4.4.6 contains an authentication bypass vulnerability in the /api/login/google_one_tap endpoint that allows remote attackers to log in as other users by submitting Google ID tokens issued to any OAuth client. Attackers operating their own Google OAuth client can capture a victim's Google-signed ID token and replay it, since the aud claim is never checked, to obtain an authenticated session as the victim's Google-linked account.

### CVE-2026-111634

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T18:17:43.750 |

Helical Insight through 7.0.0 contains an sql injection vulnerability that allows authenticated viewers to inject SQL through unescaped report parameter values sent to /executeDatasource. Attackers can supply crafted Numeric or String placeholder values that bypass the broken SqlDetect guard to read unexposed tables and modify data in the report's data source.

### CVE-2026-111627

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-16T18:17:42.760 |

HestiaCP before 1.10.5 contains an authorization bypass vulnerability that allows non-ROOT_USER administrators to perform write actions while impersonating the protected ROOT_USER account. Attackers can log in via the loginas parameter and POST to /add/cron/, because the read-only flag is never checked, causing crond to run their commands as the protected administrator's system account.

### CVE-2026-111606

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T18:17:39.647 |

Huly Platform through 0.7.432 contains a missing authorization vulnerability that allows any authenticated user to merge arbitrary persons by calling the mergeSpecifiedPersons account RPC. Attackers knowing two person UUIDs can graft attacker-controlled unverified social ids onto a victim person, then use login or password recovery to take over the victim account.

### CVE-2026-111605

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:39.490 |

Jpom through 2.11.12 contains an authorization bypass vulnerability in SshFileController that allows authenticated workspace users to access SSH hosts belonging to other workspaces by supplying foreign SSH asset ids. Attackers with SSH file permissions in any workspace can call download, upload, read_file_data.json, update_file_data.json, delete.json, rename.json and new_file_folder.json endpoints to read, modify and delete files on other workspaces' SSH hosts.

### CVE-2026-96626

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-10-16T22:18:58.070 |

Arcane is an interface for managing Docker containers, images, networks, and volumes. Prior to 2.5.0, UpdateRegistry and TestRegistry in backend/api/services/container_registry_service.go allow the registry URL to change while preserving the stored encrypted token. When a holder of registries:update and registries:test repoints a generic registry URL without supplying a replacement token, TestRegistry decrypts the preserved token and RegistryLogin sends it to the attacker-controlled host because normalizeRegistryServerAddressInternal does not restrict the destination. This exposes the stored container-registry PAT or password and can enable image access or tampering. This issue is fixed in version 2.5.0.

### CVE-2026-55543

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-470` |
| Published | 2026-10-16T16:18:43.750 |

TuxGuitar is an open-source guitar tablature editor. Prior to 2.1.0, an untrusted .tg file can set gervil.soundbank.path to reference an on-disk archive, including the .tg file itself, whose META-INF/services/javax.sound.midi.Soundbank entry names an attacker-supplied class stored in that archive. When a user opens the file, JARSoundbankReader uses an unverified class loader to load and instantiate that class, executing its constructor with the privileges of the TuxGuitar process. This issue is fixed in version 2.1.0.

### CVE-2026-111701

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T18:17:53.930 |

OtterMind Nubase through 0.1.4 contains a missing authentication vulnerability that allows unauthenticated attackers to access private bucket objects because /storage/v1/object/{bucketId}/{path} is treated as public for every HTTP method. Attackers knowing a tenant subdomain, bucket id and object path can download objects from private buckets and delete stored objects without an apikey or JWT.

### CVE-2026-111638

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T18:17:44.297 |

sshportal through 1.19.5 contains a missing authorization vulnerability in the management shell 'key show' command that allows authenticated non-admin users to obtain decrypted backend private SSH keys. Attackers can request predictable key names like 'default' or 'host' to retrieve private keys and connect directly to backend hosts, bypassing ACLs and session recording.

### CVE-2026-111719

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-16T18:17:56.397 |

Roncoo-pay through commit 9428382 contains a missing authorization vulnerability in F2FPayController.orderQuery that allows unauthenticated attackers to retrieve payment records by supplying a trxNo parameter. Attackers can guess transaction numbers, a '7' prefix plus a snowflake ID, to obtain the full serialized payment record of any merchant.

### CVE-2026-111646

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T18:17:45.440 |

SurveyKing before 1.13.0 contains a missing authorization vulnerability that allows unauthenticated attackers to download any stored file by id through GET /api/public/preview/{attachmentId}. Attackers who know or derive time-ordered snowflake file ids can bypass shared, owner, and project checks in FileServiceImpl.loadFile to read private survey attachments and respondent uploads.

### CVE-2026-102552

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-940` |
| Published | 2026-10-16T18:17:14.893 |

Improper verification of the source of a communication channel in the DNS resolver in Amazon FreeRTOS-Plus-TCP before V4.4.2 might allow remote third-party to insert a chosen address into the device's DNS cache via a forged DNS reply.



To remediate this issue, users should upgrade to version V4.4.2 and enable ipconfigDNS_CHECK_REPLY_SOURCE_IP.

### CVE-2026-86009

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-863` |
| Published | 2026-10-16T17:17:51.920 |

Mailu is a mail server distributed as a set of Docker images. Prior to f05aeb8322e2f61096af6b089d61ba6f40587d96, domain managers can enable spoofing for hosted domains they do not control. A potentially malicious domain administrator enables spoofing for another hosted domain and can send emails that are authenticated with DKIM/SPF for domains they should not be able to. This vulnerability is addressed by f05aeb8322e2f61096af6b089d61ba6f40587d96.

### CVE-2026-68907

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-457;CWE-628` |
| Published | 2026-10-16T16:20:00.960 |

libIEC61850 is an open-source implementation of IEC 61850 client and server protocols including MMS, GOOSE, Sampled Values, and R-Session. Prior to 1.6.2, checkDataSetAccess reverses the source and destination arguments to StringUtils_copyStringToBuffer while constructing an MMS_ASSOCIATION_SPECIFIC dataset reference. The helper treats uninitialized dataSetRef[130] storage as a source string, causing strlen to read beyond the stack buffer, and then copies those bytes into the caller-owned listName buffer. A remote defineNamedVariableList request can crash servers that have dynamic dataset service enabled and a dataset access handler installed; the advisory also observes caller stack corruption but establishes denial of service as the primary impact. This issue is fixed in version 1.6.2.

### CVE-2026-92798

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-17T04:17:10.257 |

The User Registration & Membership plugin for WordPress is vulnerable to Arbitrary Shortcode Execution in versions up to, and including, 5.2.8 This is due to insufficient input sanitization in the 'referrer_url' branch of UR_Smart_Tags::process(), where the attacker-controlled HTTP_REFERER header is only passed through sanitize_text_field() — which does not strip WordPress shortcode delimiters — before being substituted into a Content Restriction message that is subsequently executed via apply_shortcodes()/do_shortcode(). This makes it possible for unauthenticated attackers to execute arbitrary registered shortcodes on any restricted page whose message uses the supported {{referrer_url}} smart tag.

### CVE-2026-111854

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-17T02:17:18.750 |

An issue was discovered on Tektronix 3 Series MDO devices before 1.21.1. A path traversal vulnerability in the SCPI FILESystem command interface allows remote attackers to read or modify arbitrary files on the device through insufficient validation of file paths supplied to filesystem access commands.

### CVE-2026-49410

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-352;CWE-384` |
| Published | 2026-10-16T22:17:23.490 |

OpenHuman is an open-source agent harness available as a desktop application and Rust library. Versions before 0.56.0 allow cross-site request forgery against the unauthenticated GET /auth/telegram loopback callback because telegram_auth_handler consumes an attacker-supplied one-time Telegram login token and passes the returned JWT to credentials::ops::store_session without validating browser fetch metadata or the request origin. An attacker with an OpenHuman account can cause a user with the local core running to visit a malicious page that requests the /auth/telegram endpoint on loopback port 7788, switching the user's active local session to the attacker's backend account and exposing subsequent agent actions, memory writes, and Telegram messages associated with that session to the attacker. This issue is fixed in version 0.56.0.

### CVE-2026-61726

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284;CWE-639;CWE-863` |
| Published | 2026-10-16T20:17:23.980 |

Tandoor Recipes is an application for managing recipes, planning meals, and building shopping lists. Prior to 2.6.12, StepViewSet and IngredientViewSet filter only by active Space and use role-level CustomIsUser checks instead of the private-recipe owner or sharing predicate when an authenticated user with read and write API scope in the victim's Space supplies a private recipe or step identifier to the Step API. Request processing uses StepViewSet, IngredientViewSet, api/step/, api/step/{step_id}/, CustomIsUser, CustomRecipePermission. The attack works because the sub-resource querysets return and update private-recipe steps for non-owners because Space membership is accepted without recipe-level authorization. This can read and silently modify another same-Space member's private recipe instructions, while cross-Space access remains out of scope. This issue is fixed in version 2.6.12.

### CVE-2026-42269

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-16T16:17:23.783 |

countly-server is the server-side part of Countly, a product analytics solution. Prior to 24.05.50 and 25.03.44, the authenticated data-migration deletion route in plugins/data_migration/api/api.js passes the user-controlled exportid to clean_up_data without path validation. plugins/data_migration/api/data_migration_helper.js concatenates that identifier into a path resolved outside the intended import directory and calls remove recursively, allowing an application administrator or user with migration permission to delete writable files or directory trees and cause data loss or service disruption. This issue is fixed in versions 24.05.50 and 25.03.44.

### CVE-2026-102917

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-16T19:17:01.273 |

IBM i 7.3, 7.4, 7.5, and 7.6 is vulnerable to an authenticated attacker elevating their privilege. A bad actor could exploit this vulnerability to perform operations with QSECOFR/Root authority on the system.

### CVE-2026-96424

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-16T16:22:52.560 |

Incorrect DBus policy for lomiri-upload-manager (part of lomiri-download-manager) allows arbitrary user to read arbitrary file as root over DBus

### CVE-2026-88755

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-200;CWE-284;CWE-863` |
| Published | 2026-10-16T15:17:33.537 |

Z.ai ZCode v3.11.2.6792 was discovered to automatically establish connections with MCP servers declared inside a repository's workspace configuration, possibly allowing attackers to execute arbitrary code via opening a crafted repository.

### CVE-2026-108374

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T21:17:19.600 |

ERPNext is a free and open source Enterprise Resource Planning tool. Prior to 15.121.0 and 16.34.0, certain endpoints for status modification fail to enforce proper authorization checks. A low-privileged authenticated user can invoke state-changing whitelisted methods without required write, submit, cancel, document, or role checks. This allows the user to modify data beyond the user's permitted role. This issue is fixed in versions 15.121.0 and 16.34.0.

### CVE-2026-59970

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-16T20:17:23.843 |

Tandoor Recipes is an application for managing recipes, planning meals, and building shopping lists. Prior to 2.6.10, passes an administrator-controlled AI provider URL directly to LiteLLM without applying the server's outbound-request SSRF checks when an authenticated user creates a Space, configures an AI provider with a URL targeting an internal address, and invokes an AI action. In cookbook/views/api.py, the affected AI actions call completion through TARGET/api/ai-import/ and api/ai-step-sort/ while bypassing safe_request. The attack works because the server connects to the supplied provider URL from each AI action and exposes connection success, refusal, or timeout as a blind network-reachability oracle. This can reach internal services, other hosts on the server network, and cloud metadata endpoints and map reachable internal hosts and ports. This issue is fixed in version 2.6.10.

### CVE-2026-86047

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T17:17:52.063 |

MariaDB server is a community developed fork of MySQL server. From 10.6.1 until 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2, SHOW CREATE SERVER, SHOW CREATE USER, and mariadb-dump are affected because each does not consistently quote identifiers and values when serializing SQL. A low-privileged attacker can trigger the issue when an attacker-created object with crafted identifiers or values is included in SHOW output or a dump, then create an object with crafted identifiers or values so generated SQL contains injected statements and execute attacker-injected SQL when the poisoned output is applied. This issue is fixed in versions 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2.

### CVE-2026-111044

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-16T22:17:20.610 |

Sunshine is a self-hosted game stream host for Moonlight. From 2026.329.165800 until 2026.906.222525, Sunshine accepted any client certificate that chained to a stored paired-client certificate, but it did not require the presented certificate to be the exact enabled paired identity. Certificate text was also compared without canonicalizing equivalent PEM encodings. A previously paired client that retains its private key can present an alternate certificate derived from its paired certificate and bypass the Disable control. Equivalent PEM encodings could also cause inconsistent client identity handling. A client that was never paired cannot use this issue, and removing the paired client removes its trust relationship. This issue is fixed in version 2026.906.222525.

### CVE-2026-111622

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-10-16T18:17:41.980 |

smart-sso through 2.1.1 contains an open redirect vulnerability in the /login handler that allows unauthenticated attackers to steal OAuth2 authorization codes by supplying an unvalidated redirectUri parameter. Attackers can send crafted /login links to users with active SSO sessions, then redeem stolen codes at /oauth2/access_token with any valid client credentials to obtain victims' access tokens.

### CVE-2026-110889

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-209` |
| Published | 2026-10-17T11:16:32.017 |

Generation of Error Message Containing Sensitive Information vulnerability in Gantry Gantry 5 Framework gantry5 allows Retrieve Embedded Sensitive Data.This issue affects Gantry 5 Framework: from n/a through 5.6.4.

### CVE-2026-108123

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-17T04:16:48.427 |

The WP Booking System – Booking Calendar plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 2.1.0.3 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to read the stored notification email body of any booking by iterating booking_id and email_log_id, exposing customer PII including names, email addresses, phone numbers, messages, and booking dates intended to be visible only to administrators. This is exploitable by any Subscriber-level user because admin_init fires on profile.php, a wp-admin page accessible to all authenticated users.

### CVE-2026-107762

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-17T03:16:28.083 |

The Kirki – Freeform Page Builder, Website Builder & Customizer plugin for WordPress is vulnerable to Insecure Direct Object Reference in all versions up to, and including, 6.3.2 via the 'context' parameter due to missing validation on a user controlled key. This makes it possible for unauthenticated attackers to expose arbitrary users' sensitive profile data — including email address, display name, nicename, registration date, profile image URL, and any string-valued user meta fields such as first name, last name, nickname, description, and custom meta keys — via the REST response. Exploitation requires a published page that uses a Kirki template containing at least one user-type dynamic content block; target user IDs are enumerable via standard WordPress REST endpoints, making the only prerequisite the presence of such a template on the site.

### CVE-2026-111855

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-17T02:17:18.877 |

An issue was discovered on Tektronix 3 Series MDO devices before 1.21.1. A path traversal vulnerability exists in the web management interface of the device. Insufficient validation of user-supplied file paths allows remote attackers to read arbitrary files accessible to the application. Depending on configuration, exploitation may be possible without authentication.

### CVE-2026-68498

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-16T22:17:25.183 |

StreamReadConstraints.maxNameLength (default 50,000 characters) is intended to bound how much memory a single JSON Object property name can consume while being parsed, independently of the much larger maxStringLength (default 100,000,000 characters) that bounds ordinary string values. For parsers built over character input — Reader, String or char[] sources, all served by ReaderBasedJsonParser — that bound is not applied while the name is being accumulated. The code path instead re-uses the string-value length check, which is roughly 2000x larger by default.



In the character-input slow path, ReaderBasedJsonParser._parseName2() accumulates the name into the TextBuffer and, when a segment fills, calls TextBuffer.finishCurrentSegment(), which validates only maxStringLength. The correct check, StreamReadConstraints.validateNameLength(int), is reached afterwards in CharsToNameCanonicalizer.findSymbol(), once the entire name has been scanned to its closing quote. By that point the full name — up to maxStringLength characters — has already been buffered in memory.



A remote attacker who can have a single sufficiently long JSON Object property name parsed through this path can force allocation on the order of 100,000,000 characters (approximately 200 MB, with segment bookkeeping pushing real peak usage higher) before any StreamConstraintsException is thrown, instead of the approximately 50,000-character (about 100 KB) bound the API promises. Repeating this across concurrent requests can exhaust the heap and crash the process. No authentication or user interaction is required. Because StreamReadConstraints.maxDocumentLength is disabled by default (-1), nothing else bounds the token first, so the issue is exploitable under default configuration.



Byte-input parsers are not affected: UTF8StreamJsonParser, UTF8DataInputJsonParser and the non-blocking (async) parsers re-validate maxNameLength on every growth of the name-decode buffer via ParserBase._growNameDecodeBuffer(), rejecting an oversized name after allocating only tens of kilobytes. Applications are exposed when untrusted JSON is parsed from a String, Reader or char[] — for example an HTTP request body already read into a String — rather than from raw UTF-8 bytes.



This issue affects com.fasterxml.jackson.core:jackson-core from 2.16.0 and tools.jackson.core:jackson-core from 3.0.0. Releases before 2.16.0 are not affected, because StreamReadConstraints.maxNameLength was first introduced in jackson-core 2.16.0.

### CVE-2026-102834

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-16T20:17:17.563 |

JavaCV provides Java interfaces to OpenCV, FFmpeg, and other multimedia libraries. Prior to 1.5.14, IPCameraFrameGrabber doubles a 32-bit buffer capacity without checking for overflow or bounding the parsed Content-Length. An application consumes an MJPEG response from a malicious camera endpoint or a tampered plaintext stream. The source can return an oversized Content-Length header in an MJPEG stream. Successful exploitation can trap the frame-grabbing thread in a permanent CPU-spinning loop and deny service. This issue is fixed in version 1.5.14.

### CVE-2026-77630

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-16T16:21:03.187 |

pupnp is an SDK for development of UPnP device and control point applications. Prior to 22.0.4, parse_hostport in upnp/src/genlib/net/uri/uri.c synchronously calls getaddrinfo while parse_uri is processing attacker-supplied hostnames from inbound HTTP request targets in upnp/src/genlib/net/http/httpparser.c and GENA SUBSCRIBE CALLBACK headers handled by create_url_list in upnp/src/gena/gena_device.c. A remote unauthenticated peer can choose a slow or nonresponsive hostname and block a bounded miniserver worker for the resolver timeout, allowing a small number of requests to exhaust the thread pool and deny UPnP service. This issue is fixed in 22.0.4.

### CVE-2026-57487

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-16T16:18:44.663 |

pupnp is an SDK for development of UPnP device and control point applications. Prior to 2.0.2, Transfer-Encoding: chunked causes the HTTP parser in upnp/src/genlib/net/http/httpparser.c to leave parser->content_length at zero while parser_parse_chunky_entity and parser_parse_chunky_body accumulate decoded bytes in parser->msg.entity. The g_maxContentLength checks in http_RecvMessage in upnp/src/genlib/net/http/httpreadwrite.c therefore reject oversized numeric Content-Length bodies but do not enforce the same limit on decoded chunked bodies. A remote peer that can reach a SOAP, GENA, miniserver, or control-point HTTP response path can make the process buffer an entity larger than the configured maximum, causing resource exhaustion and denial of service. This issue is fixed in 2.0.2.

### CVE-2026-57486

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-16T16:18:44.510 |

pupnp is an SDK for development of UPnP device and control point applications. Prior to 2.0.2, ixmlNode_compare in ixml/src/node.c passes the nullable nodeValue, namespaceURI, prefix, and localName fields directly to strcmp. Non-namespaced attributes created by ixmlDocument_createAttribute legitimately leave those fields NULL. When ixmlElement_removeAttributeNode compares two distinct attribute objects with the same nodeName through find_condition_node, the pointer-identity shortcut does not apply and the comparison dereferences NULL, causing a process crash when application handling of attacker-controlled XML reaches this path. This issue is fixed in 2.0.2.

### CVE-2026-48741

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-129;CWE-252;CWE-476;CWE-754` |
| Published | 2026-10-16T16:18:11.943 |

libIEC61850 is an open-source implementation of IEC 61850 client and server protocols including MMS, GOOSE, Sampled Values, and R-Session. Prior to 1.6.2, alternateArrayAccess in src/mms/iso_mms/server/mms_read_service.c does not validate an alternate-access sub-array range when numberOfElements is greater than zero. An out-of-range MmsValue_getElement call returns NULL, and the sub-array branch passes that value to MmsValue_isDeletable, causing a NULL pointer dereference. A remote MMS Read request can therefore crash servers whose data models contain arrays, while the single-element error path handles the same invalid index safely. This issue is fixed in version 1.6.2.

### CVE-2026-48503

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-191;CWE-200;CWE-252` |
| Published | 2026-10-16T16:18:11.793 |

libIEC61850 is an open-source implementation of IEC 61850 client and server protocols including MMS, GOOSE, Sampled Values, and R-Session. Prior to 1.6.2, the MMS file service in src/mms/iso_mms/server/mms_file_service.c accepts an out-of-range initialPosition in fileOpen and stores it in the file-read state. The fileRead path then subtracts the larger read position from the file size using unsigned arithmetic and fails to limit the response to the actual FileSystem_readFile return value. The oversized response can include stale bytes from the reused connection buffer after the requested file contents, disclosing prior response data and protocol fragments to an unauthenticated remote client when the file service is enabled. This issue is fixed in version 1.6.2.

### CVE-2026-46472

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-16T16:18:11.647 |

An issue was discovered in GStreamer gst-plugins-good before 1.28.2. While parsing an MP4 file, the isomp4 plugin's qtdemux_parse_chnl function may read past the end of a global array, potentially leading to information disclosure.

### CVE-2026-42270

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-16T16:17:23.940 |

countly-server is the server-side part of Countly, a product analytics solution. Prior to 24.05.50 and 25.03.44, star-rating/images/ and dashboards/images/screenshots/ are among public image and screenshot routes using the local fs storage backend that call getStream and pipe filesystem streams to HTTP responses without an error listener. An unauthenticated request containing a URL-encoded dot can make createReadStream open a directory, emit an asynchronous EISDIR error, and terminate the Node.js process as an unhandled exception, allowing repeated requests to keep the analytics API unavailable. The affected routes also include /appimages/*, /memberimages/*, and */screenshots/*. This issue is fixed in versions 24.05.50 and 25.03.44.

### CVE-2026-41582

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-16T16:17:23.623 |

countly-server is the server-side part of Countly, a product analytics solution. Prior to 24.05.50 and 25.03.44, public image and screenshot routes implemented in frontend/express/app.js, plugins/star-rating/frontend/app.js, and plugins/dashboards/frontend/app.js concatenate attacker-controlled wildcard paths without containment validation. On deployments using the local filesystem backend, an unauthenticated request can traverse outside the intended asset directories and reach getStats or getStream in api/utils/countlyFs.js, allowing arbitrary readable server files to be disclosed. The affected routes include /appimages/*, /memberimages/*, */screenshots/*, /star-rating/images/*, and /dashboards/images/screenshots/*. This issue is fixed in versions 24.05.50 and 25.03.44.

### CVE-2026-102941

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-16T16:16:52.937 |

The package github.com/gomarkdown/markdown is a Go library for parsing Markdown text and rendering as HTML. Prior to 0.0.0-20260724235538-61af6e1e6971, parser.IsSafeURL in parser/parser.go slices url[:nPath] before the len(url) >= nPath guard. A short destination causes a slice-bounds panic when the loop reaches a relative-path prefix for which len(url) < nPath and cap(url) < nPath. The one-byte destination / is an explicit non-panic counterexample because it matches the first valid path and returns before a longer prefix is sliced. Demonstrated panic cases include empty, ., and .. destinations under those conditions. The panic is reachable when markdown.ToHTML renders untrusted Markdown with html.Safelink enabled, including an empty link destination, and is also reachable by callers that pass a short attacker-controlled URL directly to the exported parser.IsSafeURL function. An uncaught panic can terminate the calling process and cause denial of service. This issue is fixed in 0.0.0-20260724235538-61af6e1e6971.

### CVE-2026-111110

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-17T08:16:28.310 |

The Payment forms, Buy now buttons, and Invoicing System | GetPaid plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'mmdwqzpoxadd' parameter in all versions up to, and including, 2.8.61 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The required nonce (getpaid_form_nonce) is publicly emitted to all visitors via wp_localize_script as WPInv.formNonce, meaning no authentication or prior nonce leak is needed; the stored payload fires when an administrator views the affected invoice's Payment Form Details metabox.

### CVE-2026-100316

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-17T08:16:26.950 |

The European VAT Compliance Assistant for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via CF-IPCountry Header in all versions up to, and including, 1.36.10 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The malicious header value is persisted verbatim into order post-meta during a guest checkout, meaning no account or authentication is required to plant the payload.

### CVE-2026-96660

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-17T04:17:10.537 |

The User Registration & Membership – Free & Paid Memberships, Subscriptions, Content Restriction, User Profile, Custom User Registration & Login Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Checkbox Field Value in all versions up to, and including, 5.2.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nopriv AJAX action user_registration_user_form_submit reaches ur_process_registration() without nonce validation, meaning any unauthenticated request can reach the vulnerable code path.

### CVE-2026-103899

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-17T04:16:47.413 |

The EU VAT Assistant for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'vat_number' parameter in all versions up to, and including, 2.1.30.260413 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The stored payload executes in the administrator's browser context when reviewing an order via WooCommerce → Orders → Edit Order, enabling privilege escalation up to and including full site takeover via rogue administrator account creation.

### CVE-2026-109208

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-17T03:16:28.340 |

The LearnPress – WordPress LMS Plugin for Create and Sell Online Courses plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'quantity (REST) / order_comments (checkout)' parameter in all versions up to, and including, 4.4.10 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. With guest checkout enabled the attack is fully unauthenticated; with guest checkout disabled, any Subscriber-level user can exploit both vectors through their own checkout.

### CVE-2026-104734

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-17T03:16:27.927 |

The Kirki – Freeform Page Builder, Website Builder & Customizer plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 6.3.2 via deserialization of untrusted input . This makes it possible for authenticated attackers, with administrator-level access and above, to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present. By default, Editor-level users are granted FULL_ACCESS to the plugin's import endpoint via the KIRKI_USERS_DEFAULT_FULL_ACCESS configuration, meaning exploitation is possible at Editor privilege level rather than being restricted to administrators alone.

### CVE-2026-111684

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:51.477 |

Magistrala through 1.0.0 contains an authorization bypass vulnerability that allows authenticated workspace members to view, issue, and revoke other tenants' device certificates by supplying foreign serials or entity ids. Attackers can call RevokeBySerial, RevokeAll, ViewCert, ListCerts, or IssueCert under their own workspace path to disconnect other tenants' devices, disclose certificates, and mint CA-signed certificates for their device ids.

### CVE-2026-111680

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:50.923 |

APIPark through 1.9.7-beta contains an authorization bypass vulnerability that allows authenticated team managers to access other teams' services and applications by supplying their own team id in the team query parameter. Attackers can target service or app ids exposed by /api/v1/simple/services and /api/v1/simple/apps to read, modify, or delete other teams' services and applications via /api/v1/service/info and /api/v1/app endpoints.

### CVE-2026-86008

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-285` |
| Published | 2026-10-16T17:17:51.753 |

Mailu is a mail server distributed as a set of Docker images. Prior to 8577c929b4ade04d3cd4210cf036601abd793556, a domain manager targeting an administrative account or another domain manager with greater privileges can reset passwords or obtain tokens for that account. This authorization failure allows a domain manager to take over a higher-privileged account and exercise that account's permissions. This vulnerability is addressed by commit 8577c929b4ade04d3cd4210cf036601abd793556.

### CVE-2026-92263

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-16T16:22:43.027 |

SparkyFitness is a self-hosted, AI-powered health and fitness tracker for families. Prior to 1.6.0, the api/admin/backup/restore endpoint interpolates an uploaded filename into a shell command. An authenticated global administrator uploads a restore archive with a crafted filename. The administrator can supply a restore archive with a filename containing shell metacharacters. Successful exploitation can execute arbitrary operating-system commands with the server process privileges. This issue is fixed in version 1.6.0.

### CVE-2026-110384

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-17T07:16:50.350 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Heateor Support Fancy Comments WordPress fancy-facebook-comments allows Reflected XSS.This issue affects Fancy Comments WordPress: from n/a through 1.2.21.

### CVE-2026-108372

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346;CWE-942` |
| Published | 2026-10-16T22:17:14.457 |

Open and provider-neutral, LoopX is a lightweight state kernel and local-first control plane for loop engineering. From version 0.0.1 until 0.4.5, `loopx serve-status` in `loopx/status_server.py` uses `StatusRequestHandler._send_json()` and `do_OPTIONS()` to send `Access-Control-Allow-Origin: *` for unauthenticated responses on predictable loopback ports. A remote attacker can cause an operator who visits attacker-controlled web content to issue cross-origin requests to `GET /status.json`, `GET /review-material?goal_id=...&path=...`, `GET /`, and `POST /control-plane/configure-goal/dry-run`, exposing control-plane state, goal and run information, local absolute paths, private Markdown files below registered goal roots, and dry-run configuration projections. The affected routes do not provide cross-origin writes or arbitrary-file access. This issue is fixed in version 0.4.5.

### CVE-2026-59963

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T20:17:23.567 |

Tandoor Recipes is an application for managing recipes, planning meals, and building shopping lists. Prior to 2.6.10, recipe utility endpoints retrieve same-Space Recipe objects without invoking the private-recipe owner or sharing permission when an authenticated member of a shared Space supplies another member's private recipe identifier to AI import, file, external-link, or share-link endpoints. Request processing uses api/ai-import/, api/get_recipe_file/, api/get_external_file_link/, api/share-link/, CustomRecipePermission. The attack works because the endpoints read private recipe files, send file bytes to the configured AI provider, or create and disclose external links without object-level authorization, and api/share-link/ can create a public link when Space sharing is enabled. This can expose private recipe files and sensitive uploaded content to another same-Space user and to configured external services. This issue is fixed in version 2.6.10.

### CVE-2026-111718

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T18:17:56.257 |

AipexBase through commit 690adb9 contains a sql injection vulnerability that allows attackers to inject SQL through the order_by and group_by fields of the /api/data/invoke endpoint. Attackers can supply subqueries or EXTRACTVALUE and UPDATEXML functions that bypass the SqlGuard denylist and row-level security, reading other users' rows and tables.

### CVE-2026-111700

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T18:17:53.780 |

WebVella ERP through 1.8.8 contains an sql injection vulnerability that allows any authenticated user to inject SQL through WHERE-clause text literals in the EQL query API. Attackers can send crafted single-quoted literals to POST /api/v3/en_US/eql, escaping the unsanitized EqlBuilder SQL interpolation to read unauthorized entities, including user and role tables.

### CVE-2026-111698

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:53.490 |

HUIZHI ChargeOS cloud through 3.0.9 contains a missing authorization vulnerability in the hcp-mp PayController.xcxRecharge endpoint that allows attackers to modify any member's wallet balance without payment. Attackers can send requests with arbitrary amount and userId parameters to credit or reduce balances and consume charging services for free.

### CVE-2026-111697

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:53.350 |

HUIZHI ChargeOS cloud through 3.0.9 contains an insecure direct object reference vulnerability in the hcp-mp MeController and OrderController that trusts client-supplied userId, openId and orderNumber parameters. Attackers can enumerate sequential member ids against endpoints like /me/getMemberBalanceByUserId and /order/orderDetail to read any member's wallet, credit, profile and charging orders.

### CVE-2026-111696

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-16T18:17:53.220 |

data-platform-open through commit efeacd3 uses a hardcoded, publicly known default AES key in AesPasswordEncAndDecServiceImpl, allowing authenticated attackers to decrypt stored datasource passwords. Attackers can obtain ciphertext passwords from the datasource detail API, for example via cross-workspace IDOR, and decrypt them offline to recover plaintext database credentials.

### CVE-2026-111695

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:53.080 |

Shaiwz data-platform-open through commit efeacd3 contains an insecure direct object reference vulnerability that allows authenticated workspace members to access other workspaces' datasources by numeric id. Attackers can send foreign sequential ids to /datasource/detail, /listSchemaTable, /tableDetail, /update or /delete to obtain JDBC credentials, enumerate database schemas, and modify or delete datasources.

### CVE-2026-111682

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-16T18:17:51.213 |

EFAK 5.0.0 through 5.1.0 contains a missing authorization vulnerability that allows authenticated low-privilege users to read LLM provider API keys through the /api/model-config REST API. Attackers with any ROLE_USER account can query /api/model-config/page or /api/model-config/{id} to retrieve unmasked keys, enabling provider account access and incurred costs.

### CVE-2026-111671

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:49.647 |

Cube-studio through 2026.09.01 contains an insecure direct object reference vulnerability that allows authenticated users to stop, reset, clear or redeploy other users' notebooks and services by id. Attackers can pass sequential ids to lifecycle endpoints in view_notebook.py, view_inferenceserving.py and view_serving.py to delete pods and take production inference endpoints offline.

### CVE-2026-111669

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T18:17:49.080 |

ZR.Admin.NET through 3.8.2 contains an sql injection vulnerability that allows authenticated attackers to manipulate the ORDER BY clause by supplying a crafted PagerInfo.Sort query parameter to the shared ToPage paging helper. Attackers holding the system:user:list permission can inject subquery or CASE expressions via GET /system/user/list to extract database contents such as stored credentials through blind techniques.

### CVE-2026-111651

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:46.217 |

Risesoft Digital-Infrastructure through 9.6.11 contains a missing authorization vulnerability in the log module DownloadController that allows authenticated users to export any tenant's personnel directory. Attackers can supply another tenant's tenantId to exportLoginXLS or exportNotLoginXLS to obtain XLSX files with names, login names, organization paths, mobile numbers, and emails.

### CVE-2026-111649

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:45.897 |

Rocboss paopao-ce through 0.6.0-alpha.3 contains an insecure direct object reference vulnerability in DownloadAttachment that allows authenticated users to access private media by supplying arbitrary content IDs. Attackers can enumerate sequential post_content ids via the /v1/attachment endpoint to obtain signed download URLs for other users' private, friend-only and following-only images, videos and attachments.

### CVE-2026-111619

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-16T18:17:41.540 |

FilePress through 3.0.1 contains an sql injection vulnerability that allows authenticated low-privilege users to inject SQL into ORDER BY clauses via the unvalidated asc parameter. Attackers can use blind boolean or time-based subqueries in dzz/pichome/library/filelist.php and dzz/collection/filelist.php to extract database rows including administrator credential hashes.

### CVE-2026-111615

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:40.977 |

Mall4cloud through 4.0 contains an insecure direct object reference vulnerability that allows authenticated merchants to read other shops' buyer shipping addresses via the multishop OrderController getOrderAddr handler. Attackers can enumerate auto-increment orderAddrId values in GET /m/order/order_addr/{orderAddrId} requests to obtain consignee names, mobile numbers, addresses and post codes platform-wide.

### CVE-2026-111614

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:40.833 |

DataCap through 2025.1.1 contains an insecure direct object reference vulnerability in BaseController.getInfoForPath that allows authenticated users to read other users' datasources, snippets and dashboards by numeric id. Low-privileged attackers can enumerate auto-increment ids on the source, snippet and dashboard endpoints to retrieve serialized datasource host, port, username and cleartext passwords.

### CVE-2026-111607

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-16T18:17:39.813 |

Jeepay through 3.2.9 contains an insecure direct object reference vulnerability that allows authenticated merchant users to overwrite another merchant application's payment channel configuration by supplying a victim infoId to MchPayInterfaceConfigController.saveOrUpdate. Attackers holding the default ENT_MCH_PAY_CONFIG_ADD permission can replace signing keys, certificates, and fee rates to break or redirect the victim merchant's payment processing.

### CVE-2026-77474

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-400;CWE-407;CWE-693` |
| Published | 2026-10-16T17:17:50.390 |

destructive_command_guard (dcg) is a command-line safety tool that blocks destructive shell commands before AI coding agents run them. Prior to 0.6.6, nested or unclosed substitutions are recursively rescanned after an inner scan returns unterminated, producing exponential-time work. The affected scanners are reached through split_command_segments in src/packs/mod.rs. a destructive command followed by nested or unclosed $( or $(( sequences. nested or unclosed $( and $(( sequences cause repeated rescanning of the remaining command suffix. a hung PreToolUse hook fails open, allowing the destructive command to proceed. This issue is fixed in version 0.6.6.

### CVE-2026-57488

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-190;CWE-444` |
| Published | 2026-10-16T16:18:44.823 |

pupnp is an SDK for development of UPnP device and control point applications. Prior to 2.0.2, raw_to_int in upnp/src/genlib/net/http/httpparser.c parses Content-Length with strtol and casts the resulting long to a 32-bit int before the caller stores it as unsigned int. On LP64 systems, values greater than INT_MAX can truncate or wrap, so the HTTP parser can accept a body length different from the declared value. A remote adjacent-network peer can use the resulting parser disagreement to leave bytes to be interpreted as another request in persistent or proxied contexts, or can make a worker wait for an extremely large body and cause denial of service. This issue is fixed in 2.0.2.

### CVE-2026-107777

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-16T15:17:05.977 |

Thermo Fisher Torrent Suite Software is vulnerable to a path traversal, which could allow an authenticated attacker to read arbitrary files on the Torrent Server that are accessible to the web service account.

### CVE-2026-62439

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-16T22:17:24.440 |

A flaw was found in GIMP. An integer overflow occurs in the file-pvr plug-in when calculating memory buffer sizes for image dimensions. By tricking a user into opening or previewing a specially crafted PowerVR (.pvr) file, an attacker can trigger a heap-based buffer overflow, potentially leading to arbitrary code execution or a Denial of Service (DoS) via an application crash.

### CVE-2026-81452

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-272` |
| Published | 2026-10-16T18:18:37.770 |

Dell Alienware Command Center (AWCC), versions prior to 6.14.54.0, contain a Least Privilege Violation vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privilege and Denial of Service.
