# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-06 15:00 UTC
- **対象期間**: `2026-09-05T15:01:22.000Z` 〜 `2026-09-06T15:00:13.000Z`
- **重要CVE数**: 30 件（Critical 9.0+: 11 件 / High 7.0〜: 19 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE のうち **CVSS 7.0 以上が 30 件以上** と、深刻度の高い脆弱性が集中しています。  
- **リモートコード実行 (RCE)・認証バイパス** が目立ち、特に **ネットワーク機器（Tenda ルータ、RouterOS、N‑central）** と **WordPress プラグイン** が攻撃対象になりやすい構成です。  
- 多くは **認証不要 (PR:N)・ネットワーク経路から直接利用可能 (AV:N)** で、攻撃者が遠隔から即座に権限取得や情報漏洩を行える点が共通しています。  
- 同一ベンダー（Tenda）で **OS コマンドインジェクションが複数箇所** に報告されているなど、ファームウェアの品質管理に課題が残っていることが伺えます。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 種類 | 主な影響範囲 | 注目理由 |
|-----|------|------|--------------|----------|
| **CVE‑2026‑86218** | 10.0 | Pre‑auth RCE | **N‑central** (全バージョン < 2026.3.1.14) | 認証不要で任意コード実行が可能。管理コンソールが社内ネットワークに露出しているケースが多く、被害拡大リスクが極めて高い。 |
| **CVE‑2026‑86152** | 10.0 | OS コマンドインジェクション (リモート) | **Tenda CP3** 27.5.57.101 の `CAutoAddWifi::ThreadProc` | ルータの Wi‑Fi 自動追加機能を悪用し、任意シェルコマンドが実行できる。家庭・小規模オフィスのインターネットエッジで広く使用されている。 |
| **CVE‑2026‑75816** | 9.8 | 認証バイパス → アカウント乗っ取り | **WordPress DynamiApps “Frontend Admin”** プラグイン ≤ 3.29.12 | `pre_update_value` の権限チェック欠如により、管理者権限を取得できる。プラグインは多数のサイトで導入されているため、広範囲な影響が予想される。 |
| **CVE‑2026‑16310** | 9.8 | IDOR → 任意ユーザーパスワード変更 | **WordPress MemberDash** プラグイン ≤ 1.8.5 | `id` パラメータの検証不備により、認証なしで任意ユーザーのパスワードを書き換え可能。会員制サイトの運営者は即時対策が必要。 |
| **CVE‑2026‑86060** | 9.2 | SSH ログインパラメータ操作による特権昇格 | **RouterOS** (全バージョン) | SSH ログイン時に特定文字列でポリシーマスクが変更され、管理者権限取得が可能。RouterOS は ISP・企業のバックボーンで広く使用されるため、インフラ全体への波及リスクが大きい。 |

> **※** 上記は **CVSS が 9.0 以上** かつ **リモートから直接利用可能** なものを優先的に選出しています。  

---

## 3. 推奨アクション  

### 3‑1. 直ちに実施すべき緊急対策
- **N‑central**  
  - 2026.3.1.14 以降のバージョンへ **アップデート**（公式パッチ適用）。  
  - 管理コンソールへの外部アクセスを **ファイアウォールで遮断**、IP 制限を徹底。  

- **Tenda CP3 (27.5.57.101)**  
  - ベンダーが提供する **最新ファームウェア (≥ 27.5.57.102)** に更新。  
  - 不要な **Auto‑Add‑WiFi** 機能を無効化し、管理 UI の **HTTPS 化** と **IP アクセス制御** を実施。  

- **WordPress プラグイン**  
  - `Frontend Admin (DynamiApps)` → **3.29.13 以降**に更新。  
  - `MemberDash` → **1.8.6 以降**に更新。  
  - `SureCart` → **4.6.3 以降**に更新（サブスクユーザーの権限昇格対策）。  
  - `Kirki` → **6.3.0 以降**に更新（XSS 防止）。  
  - `HivePress Authentication` → **1.1.5 以降**に更新（認証バイパス修正）。  

- **RouterOS**  
  - **公式リリースの最新安定版**（例: 7.15.0 以降）へアップグレード。  
  - SSH の **PermitRootLogin** を `no`、`AllowUsers` で必要最小限に絞る。  
  - 不要な **SSH ポート** を閉じ、代替の管理手段 (API token) を利用。  

### 3‑2. 中長期的に実施すべき対策
| 項目 | 内容 |
|------|------|
| **資産インベントリの整備** | ルータ・サーバ・WordPress 環境の **バージョン管理表** を作成し、脆弱性情報と照合できるよう自動化 (例: `nmap`, `wpscan`, `routeros‑scanner`)。 |
| **パッチ適用プロセスの自動化** | CI/CD パイプラインに **脆弱性スキャン** (Trivy, Snyk) と **自動アップデート** を組み込み、特に `npm` パッケージ (`h3` など) のバージョンを常に最新に保つ。 |
| **最小権限の徹底** | ルータ・サーバの管理アカウントは **最小権限** に設定し、不要な `root`/`admin` アカウントは無効化。 |
| **ネットワーク分離** | 管理系 (N‑central, RouterOS) とユーザ系 (Wi‑Fi AP) を **別 VLAN** に分離し、管理 VLAN へのアクセスは VPN 経由に限定。 |
| **監視・インシデント対応** | ① **ログ集約** (Syslog, ELK) ② **不審なコマンド実行・SSH ログイン失敗** のアラート設定 ③ **CVE 公開後 48 時間以内** にパッチ適用できる **SLA** を策定。 |

### 3‑3. 具体的なパッケ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-86218

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-96` |
| Published | 2026-09-06T03:17:17.373 |

N-central is vulnerable to a pre-auth remote code execution This issue affects N-central: before 2026.3.1.14.

### CVE-2026-86152

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-06T02:17:19.370 |

A flaw has been found in Tenda CP3 27.5.57.101. The impacted element is the function CAutoAddWifi::ThreadProc of the file Functions/AutoAddWifi.cpp of the component Kylin. Executing a manipulation can lead to os command injection. The attack may be launched remotely.

### CVE-2026-75816

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-06T03:17:16.607 |

The Frontend Admin by DynamiApps plugin for WordPress is vulnerable to Authentication Bypass to Account Takeover in all versions up to, and including, 3.29.12. This is due to the pre_update_value function lacking any capability or ownership check, and ActionPost::conditions_logic() short-circuiting its current_user_can('edit_post') authorization gate whenever the post ID is non-numeric — such as the string user_1 — allowing unauthenticated form submissions to be routed to arbitrary user records without restriction. This makes it possible for unauthenticated attackers to overwrite any user's registered email address, including an administrator's, and then leverage WordPress's native password-reset flow to fully take over the targeted account.

### CVE-2026-16310

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-06T03:17:15.540 |

The MemberDash plugin for WordPress is vulnerable to Insecure Direct Object Reference in all versions up to, and including, 1.8.5 via the 'id' parameter due to missing validation on a user controlled key. This makes it possible for unauthenticated attackers to change the password of any WordPress user, including administrators, by supplying an arbitrary user ID during registration, and take over their account without any notification sent to the victim.

### CVE-2026-86153

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-269` |
| Published | 2026-09-06T02:17:19.770 |

A vulnerability has been found in Tenda CP3 27.5.57.101. This affects the function CRedirServer::SetRedirectEnable of the file Functions/Redirect.cpp. The manipulation leads to improper privilege management. Remote exploitation of the attack is possible.

### CVE-2026-86151

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-06T00:16:55.773 |

A vulnerability was detected in Tenda CP3 27.5.57.101. The affected element is the function sub_2F77E8 of the file Apis/system.c of the component Network Configuration Management. Performing a manipulation results in os command injection. The attack may be initiated remotely.

### CVE-2026-86149

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-05T22:17:18.943 |

A weakness has been identified in Tenda CP3 27.5.57.101. This issue affects some unknown processing of the file Net/NetCheckPing.cpp. This manipulation of the argument interface_name/host causes os command injection. The attack can be initiated remotely.

### CVE-2026-86148

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-05T22:17:18.743 |

A security flaw has been discovered in Tenda CP3 27.5.57.101. This vulnerability affects the function SystemAsh of the file Apis/system.c of the component Kylin. The manipulation of the argument AlarmVoiceURL results in os command injection. It is possible to launch the attack remotely.

### CVE-2026-86060

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-05T20:17:18.703 |

RouterOS contains an argument-handling flaw in the SSH login
path involving usernames that begin with a prohibited character, allowing for the trusted RouterOS policy mask to be changed, leading to privilege escalation. Exploitation requires an unauthenticated SSH session to reach the RouterOS login helper.This issue was fixed in versions: 6.49.21 (Long-term), 7.23.4 (Long-term) and 7.24.2 (Stable)

### CVE-2026-67276

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-05T20:17:17.977 |

RouterOS does not compare the complete RSA public key when matching an SSH authentication request to an authorized user key, checking the key type and modulus but omitting the exponent. Because signature verification uses the client-supplied key, an attacker knowing an authorized RSA modulus can supply a key with exponent one, forge a valid signature, and open an SSH command channel as the target user without the private key.This issue was fixed in versions: 6.49.21 (Long-term), 7.23.4 (Long-term) and 7.24.2 (Stable)

### CVE-2026-86259

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-918` |
| Published | 2026-09-06T13:17:10.963 |

OpenMAIC before 1.0.1 skips server-side request forgery validation in non-production builds, allowing unauthenticated attackers to reach cloud instance metadata services. Attackers can supply arbitrary provider URLs via the x-base-url header or baseUrl parameter to access sensitive cloud credentials and metadata.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-86165

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-06T04:18:32.523 |

A vulnerability was found in Tenda HG10 300001138. This vulnerability affects the function formURL of the file /boaform/admin/formURL. Performing a manipulation of the argument Keywd/urlFQDN results in buffer overflow. The attack may be initiated remotely. The exploit has been made public and could be used.

### CVE-2026-18480

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-06T07:16:43.097 |

The SureCart  WordPress plugin before 4.6.3 does not ensure that the account affected by a customer update is the same account its permission check authorised, allowing users with a subscriber-level account to change another user's email address, including an administrator's, and take over that account via a password reset. It further allows an attacker-controlled customer record to be associated with an arbitrary user, and discloses customer identifiers and email addresses to any authenticated user, which together make the takeover reachable from a subscriber-level account alone.

### CVE-2026-67277

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-05T20:17:18.120 |

RouterOS accepts a "related" btest connection before the corresponding primary session has completed authentication. An unauthenticated client can use this state to start an IPv4 UDP test. With "random-data=false", the sender transmits an uninitialized tail from a kernel packet buffer. A separate unchecked, inverted packet-size interval causes unsigned integer underflow, anomalously large fragmented output, and can restart the RouterOS kernel.



This issue was fixed in versions: 6.49.21 (Long-term), 7.23.4 (Long-term) and 7.24.2 (Stable)

### CVE-2026-86250

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-06T12:17:15.767 |

h3 versions before 2.0.1-rc.18 fail to validate the chunk count parsed from user-controlled cookie values in setChunkedCookie() and deleteChunkedCookie() functions. Attackers can send a crafted cookie header with an extremely large chunk count to trigger an O(n²) cleanup loop that hangs the server process.

### CVE-2022-51009

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-06T12:17:15.073 |

PocketMine-MP before 4.7.2 fails to properly handle exceptions from the adhocore/json-comment library when parsing skin geometry data. Attackers can send login or skin packets with invalid geometry JSON to trigger an unhandled RuntimeException, causing server crash.

### CVE-2026-67281

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-824` |
| Published | 2026-09-05T20:17:18.547 |

RouterOS WebFig contains an unauthenticated file-read vulnerability in the /jsproxy path where a newly allocated session retains a stale uninitialized principal pointer used for file authorization. An unauthenticated attacker can prepare the allocator so that the file-serving path dereferences this pointer with sufficient rights, then supply parent-directory components in an encrypted URI to escape the WebFig file namespace and disclose root-owned files, including configuration stores containing credentials.This issue was fixed in versions: 6.49.21 (Long-term), 7.23.4 (Long-term) and 7.24.2 (Stable)

### CVE-2026-0799

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-129;CWE-787` |
| Published | 2026-09-05T19:16:55.320 |

In BPF instructions that load/store a value from/to a scratch memory register the register index is an unsigned 32-bit integer and must not exceed 15, but libpcap BPF interpreter does not validate the value.  In particular uncommon use cases a crafted filter program can cause the interpreter to try reading and writing the OS process memory in the 16GiB starting at the current stack frame on 64-bit architectures and in the entire address space on 32-bit architectures.

### CVE-2026-86167

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-06T05:16:50.477 |

A vulnerability was identified in Tenda HG10 300001138. Impacted is the function formgponConf of the file /boaform/admin/formgponConf of the component Boa. The manipulation of the argument fmgpon_loid leads to os command injection. Remote exploitation of the attack is possible. The exploit is publicly available and might be used.

### CVE-2026-86258

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-06T13:17:10.830 |

nbviewer through 1.0.1 contains a path traversal vulnerability in LocalFileHandler.can_show() that uses string-prefix comparison instead of proper path validation. Attackers can read files from sibling directories outside the configured root by requesting paths that share the root as a textual prefix, disclosing unintended notebooks and credentials.

### CVE-2026-86253

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-06T12:17:16.163 |

h3 (npm package) versions <= 2.0.1-rc.14 contain a path traversal vulnerability in serveStatic(). On Node.js deployments, event.url.pathname is not normalized, so percent-encoded dot segments (%2e%2e) are passed to decodeURI() and decoded to ../ sequences without sanitization. An unauthenticated remote attacker can send crafted requests to endpoints served by serveStatic() to read arbitrary files outside the intended static directory. Fixed in 1.15.6 and 2.0.1-rc.15.

### CVE-2026-86251

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-06T12:17:15.900 |

h3 versions before 1.15.9 contain a path traversal vulnerability in the serveStatic utility. A double-decoding flaw allows a request path containing double-encoded dot sequences (e.g. %252e%252e) to be decoded to %2e%2e, which survives resolveDotSegments() because that function only checks for literal '.' characters. When the resulting asset ID is resolved by URL-based backends (CDN, S3, object storage), %2e%2e is interpreted as '..' per RFC 3986, enabling path traversal to read arbitrary files from the backend.

### CVE-2026-86242

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-284;CWE-306` |
| Published | 2026-09-06T12:17:15.583 |

Bifrost HTTP transport before 2.0.0 accepts an enabled custom plugin whose path is an HTTP URL through unauthenticated POST /api/plugins when management authentication is disabled (the default, governance.auth_config.is_enabled=false). The shared-object loader treats an http-prefixed path as a download URL, writes the body to a temporary .so, and passes it to Go's plugin.Open. After a successful open, optional Init runs immediately with the supplied config as the Bifrost process user. On documented dynamically linked builds (DYNAMIC=1 / no static-link flags), which the vendor requires for custom Go plugins, plugin.Open is expected to succeed and this is unauthenticated remote code execution. On the published statically linked Docker image, plugin.Open fails with Dynamic loading not supported, so that build class is only server-side request forgery. Attack complexity is High because the attacker cannot force RCE on the default static image and a loadable plugin must match the host Go version, OS, architecture, and linkage. The 1.6.x HTTP transport line through 1.6.11 does not contain the fix.

### CVE-2026-86207

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-305` |
| Published | 2026-09-05T19:16:56.190 |

An authentication bypass in N-central < 2026.3 HF 3 leads to authentication bypass in internal only APIs

### CVE-2026-84219

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-06T07:16:43.427 |

The Kirki  WordPress plugin before 6.3.0 does not hold back every spelling of the HTML entities it decodes when rendering, allowing unauthenticated users to store JavaScript in a comment which then runs in the session of anyone viewing a page that displays it, including an administrator, and on every page of the site when its header or footer is built to show comments.

### CVE-2026-18056

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-06T03:17:16.467 |

The HivePress Authentication plugin for WordPress is vulnerable to Authentication Bypass via the access_token parameter in all versions up to, and including, 1.1.4. This is due to the authenticate_user function's Facebook authenticator resolving third-party identity by forwarding the attacker-supplied access_token to the Facebook Graph API and trusting the returned email and ID verbatim, without performing any application ID or audience validation — specifically, no /debug_token verification and no comparison of the token's app_id against the configured hp_facebook_app_id. This makes it possible for unauthenticated attackers to authenticate as any existing WordPress user, including administrators, whose email address is associated with a Facebook account for which the attacker can obtain any valid access token. Important Note: To exploit the vulnerability, the attacker must obtain the victim's access token.

### CVE-2026-86166

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-06T04:18:32.783 |

A vulnerability was determined in Tenda HG10 300001138. This issue affects the function formWanRedirect of the file /boaform/formWanRedirect of the component Boa Web Server. Executing a manipulation of the argument if can lead to buffer overflow. The attack may be launched remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-86255

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-06T12:17:16.433 |

wger before 2.5 fails to validate the maximum duration of routine date ranges, allowing authenticated users to create routines spanning arbitrarily long periods. Attackers can trigger the date_sequence computation via routine detail endpoints, forcing the server to iterate thousands of times per request and exhaust worker threads, denying service to legitimate users.

### CVE-2021-48007

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-06T12:17:14.783 |

PocketMine-MP versions before 3.18.1 fail to validate NaN or INF values in MovePlayerPacket position and rotation fields. Malicious clients can send crafted movement packets with invalid floating-point values to crash servers through unhandled mathematical operations or prevent clients from rendering other players.

### CVE-2020-37277

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-06T12:17:13.547 |

PocketMine-MP versions before 3.15.4 contain a denial of service vulnerability in the InventoryTransaction component's findResultItem() method. Malicious clients can send specially crafted InventoryTransactionPackets with multiple conflicting pathways to cause exponential processing complexity, freezing the server.
