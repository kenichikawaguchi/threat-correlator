# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-28 15:00 UTC
- **対象期間**: `2026-09-27T15:00:14.000Z` 〜 `2026-09-28T15:00:31.000Z`
- **重要CVE数**: 79 件（Critical 9.0+: 22 件 / High 7.0〜: 57 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超にのぼり、**コンテナ基盤、ネットワーク・アプライアンス、Web アプリケーション** が集中して攻撃対象となっています。特に **LXD のストレージドライバ** と **Citrix NetScaler ADC/Gateway** に関する脆弱性は、認証済みユーザーでもリモートから **root 権限取得** や **コード実行** が可能になる点で深刻です。  
また、Apache Roller の XML‑RPC デシリアライズや Logsign SIEM のデフォルト認証情報漏洩といった **認証・権限チェック不備** が続いており、**内部ネットワークへの横展開** が容易になる傾向が見られます。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目すべき理由 |
|-----|------|----------|----------------|
| **CVE‑2026‑87799** | 9.9 (CVSS:3.1) | LXD 4.0 以降の *migration receive* パスで不適切なリンク解決が可能。認証済みクライアントが任意のファイルを書き換え、ホスト上で **root 権限でコード実行** できる。 | LXD は多くの CI/CD パイプラインや開発環境で標準採用されているため、被害拡大リスクが高い。 |
| **CVE‑2026‑85526** | 9.9 (CVSS:3.1) | LXD の Btrfs ストレージドライバ `unpackVolume` にパス・トラバーサル。バックアップ YAML に細工した `subvolumes[].path` を送るだけで **任意ファイル削除/上書き** が可能。 | 同上に加えて、**バックアップ機能** がデフォルトで有効化されている環境が多く、攻撃者が容易にトリガーできる点が危険。 |
| **CVE‑2026‑88772** | 9.5 (CVSS:4.0) | Citrix NetScaler ADC / Gateway の複数バージョンで **リモートコード実行 (RCE) / DoS** が可能。特に FIPS 版も対象。 | 金融・医療・官公庁で広く採用されている ADC/ゲートウェイは、外部から直接アクセスされやすく、**一度侵入すれば内部ネットワーク全体への横展開** が可能。 |
| **CVE‑2026‑82384** | 9.8 (CVSS:3.1) | Apache Roller 6.1.5 の XML‑RPC エンドポイントで **未認証デシリアライズ** が可能。攻撃者は任意のオブジェクトを送信し、サーバ上でコード実行ができる。 | 多くの企業が内部ブログやナレッジベースに Roller を利用しているが、XML‑RPC はデフォルトで有効化されているケースが多く、**認証不要**で攻撃が成立する点が重大。 |
| **CVE‑2026‑90924** | 9.8 (CVSS:3.1) | Logsign SIEM のデフォルト認証情報がそのまま使用可能。`admin/admin` などの組み合わせで **管理コンソールに不正ログイン** ができる。 | SIEM はセキュリティ監視の要であり、**管理権限が奪われると全社のインシデント情報が漏洩・改ざん** される危険性がある。 |

> **共通点**  
> - いずれも **認証・権限チェックの欠如**、または **入力検証の不備** が根本原因。  
> - 影響範囲は **ホスト OS の root 権限取得**、もしくは **ネットワーク境界装置の完全制御** と、組織全体のセキュリティ姿勢を揺るがすレベル。

---

## 3. 推奨アクション  

### 3.1 LXD 系 (CVE‑2026‑87799 / CVE‑2026‑85526 / CVE‑2026‑85185)  
- **パッケージ**: `lxd` (Ubuntu/Debian 系)、`lxd` (Snap)  
- **アップデート**:  
  - 4.0 系 → **4.0.14** 以上  
  - 5.0 系 → **5.0.10** 以上  
  - 5.21 系 → **5.21.8** 以上  
  - 6.x 系 → **6.10** 以上  
- **設定上の対策**:  
  - **XML‑RPC / migration API** を使用しない環境では、`/etc/lxd/lxd.conf` の `migration.allow` を `false` に設定。  
  - Btrfs バックエンドを使用している場合は、**バックアップ機能の利用を最小限に抑える**か、`lxc storage set <pool> source` で `btrfs` 以外のストレージへ移行。  
  - すべての **LXD クライアント** に対し、最小権限 (project‑level) のロールを付与し、不要な `instance create` 権限を削除。

### 3.2 Citrix NetScaler ADC / Gateway (CVE‑2026‑88772・88771・88773)  
- **製品**: `Citrix ADC` (旧 NetScaler) / `Citrix Gateway`  
- **アップデート**:  
  - **ADC**: 14.1‑73.37 以降、または 13.1‑64.23 以降（FIPS 版含む）へ更新。  
  - **Gateway**: 同上 (14.1‑73.37 以降、13.1‑64.23 以降)。  
- **緊急対策**:  
  - 管理インタフェースへの **IP アクセス制限**（ACL、VPN 経由のみ）を徹底。  
  - **未使用の XML‑RPC / SOAP API** を無効化 (`nsconfig -set -feature xmlrpc off`)。  


---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-87799

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-28T14:17:21.427 |

Improper link resolution in the migration receive path in Canonical LXD versions 4.0 and later (fixed in 4.0.14, 5.0.10, 5.21.8 and 6.10) on Linux allows an authenticated client that can create instances or custom storage volumes in a project, or a malicious migration source server, to write attacker-controlled files to arbitrary paths on the target host as root, leading to full host compromise. The attacker does this with a crafted rsync or btrfs send stream that plants a symlink in the transferred volume, such as rootfs or root.img, and then writes through it.

### CVE-2026-85526

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-28T14:17:20.423 |

Path traversal in the Btrfs storage driver (unpackVolume) in Canonical LXD on Linux allows an authenticated user with instance creation privileges to delete or replace arbitrary files and directories on the host filesystem as root via a crafted subvolumes[].path entry in backup/optimized_header.yaml during a btrfs optimized backup import.

### CVE-2026-82377

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-28T08:16:41.417 |

Missing Authorization in Apache Roller 6.1.5 allows an authenticated user to read, modify, or delete weblog content belonging to other weblogs through the legacy XML-RPC Blogger and MetaWeblog APIs, because the handlers authenticate the caller but do not verify the caller's permission on the weblog or entry actually affected. Only installations that enable the non-default global XML-RPC setting are affected; the per-weblog API flag defaults to enabled for UI-created weblogs. Users are recommended to upgrade to Apache Roller 6.1.6 or later, which applies an explicit per-method permission check, or to keep the XML-RPC feature disabled.

### CVE-2026-90924

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1392` |
| Published | 2026-09-28T14:17:21.720 |

Use of default credentials vulnerability in Innotim Software, Telecommunications and Consultancy Trade Ltd. Co. Logsign SIEM allows Try Common or Default Usernames and Passwords.

This issue affects Logsign SIEM: from 6.4.101 before 6.4.117.

### CVE-2026-82384

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-28T08:16:42.273 |

Deserialization of Untrusted Data in Apache Roller 6.1.5 allows an unauthenticated remote attacker to cause deserialization of attacker-controlled bytes, because the XML-RPC endpoint accepts vendor extension types that are deserialized during request parsing, before authentication. The servlet is mapped unconditionally, so parsing occurs even when the global XML-RPC feature is set to disabled; no non-default configuration is required for this path. This can lead to remote code execution. Users are recommended to upgrade to Apache Roller 6.1.6 or later, which disables the extension types and rejects requests when the XML-RPC feature is disabled.

### CVE-2026-85185

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-28T14:17:20.130 |

Path traversal in the btrfs storage driver in Canonical LXD versions 4.0.2 and later (fixed in 4.0.14, 5.0.10, 5.21.8 and 6.10) on Linux allows an authenticated client with permission to create instances in a project to delete arbitrary files on the host as root. On hosts whose root filesystem is btrfs, the client can also place attacker-controlled content at arbitrary host paths, leading to full host compromise. The client does this with a crafted subvolume path containing ../ sequences, sent in either of two ways: in the optimized_header.yaml of an optimized btrfs backup, or in the btrfs migration header sent by a malicious migration source.

### CVE-2026-88772

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-27T17:16:56.390 |

Vulnerability in Citrix NetScaler ADC and Citrix NetScaler Gateway.

This issue affects ADC: before 14.1-73.37, before 13.1-64.23, before 14.1-73.37 FIPS, and before 13.1.37.279 FIPS and NDcPP; Gateway: before 14.1-73.37 and before 13.1-64.23 leading to Remote Code Execution or Denial of Service

### CVE-2026-88771

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-27T17:16:56.260 |

Improper input validation vulnerability in Citrix NetScaler ADC and Citrix NetScaler Gateway.

This issue affects ADC: before 14.1-73.37, before 13.1-64.23, before 14.1-73.37 FIPS, and before 13.1.37.279 FIPS and NDcPP; Gateway: before 14.1-73.37 and before 13.1-64.23 leading to an unauthenticated attacker to execute arbitrary commands.

### CVE-2026-81867

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-28T11:16:48.070 |

A Deserialization of Untrusted Data vulnerability in the JavaScript Task in Google Cloud Application Integration versions prior to 2026-06-28 on Google Cloud Platform allows an authenticated user with standard permissions to run arbitrary code on the shared production servers using a specially crafted script bypassing param guards.


This vulnerability was patched on 28 June 2026, and no customer action is needed.

### CVE-2026-19759

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-28T11:16:45.337 |

An Incorrect Authorization vulnerability in the task configuration in Google Cloud Application Integration versions prior to 2026-06-17 on Google Cloud Platform allows an authenticated Google Cloud user to execute arbitrary internal RPCs from inside Google's production network under a privileged identity using an internal-only task type.


This vulnerability was patched on 17 June 2026, and no customer action is needed.

### CVE-2026-73640

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-28T14:17:16.843 |

Dayforce Payroll is vulnerable to Time Based-Blind SQL Injection in password recovery functionality. The unauthenticated attacker can prepare GET request with one of the parameters filled in with an arbitrary SQL query. The parameter is interpreted as part of SQL predicate resulting in Time-Based Blind SQL Injection.
Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version R2026.2.0 but may also affect other versions.

### CVE-2026-101072

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-28T14:17:13.973 |

A vulnerability was identified in Netcore NR289-GE 1.4.5102. This issue affects the function system of the file /ap_ip.cgi of the component CGI Handler. Such manipulation of the argument ip leads to os command injection. The attack can be launched remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101039

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-28T11:16:43.600 |

A vulnerability was identified in FAST FAC1900R 20190827_2.0.2. Affected by this issue is the function copy_msg_element of the component devdiscover Service. Such manipulation leads to stack-based buffer overflow. The attack can be executed remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101001

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-28T05:16:30.570 |

A vulnerability was identified in Netcore NBR200V2 1.3.241127.071246. This impacts the function eval of the file /www/cgi-bin/network_tools of the component Web Management Interface. Such manipulation of the argument QUERY_STRING leads to os command injection. It is possible to launch the attack remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101000

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862;CWE-863` |
| Published | 2026-09-28T05:16:30.270 |

A vulnerability was determined in Netcore NBR100V2 1.3.240614.030928. This affects the function uci.apply of the file /usr/share/rpcd/acl.d/unauthenticated.json of the component ACL Handler. This manipulation of the argument section causes missing authorization. It is possible to initiate the attack remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-100886

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-27T23:16:59.020 |

A vulnerability was identified in Seetong T8108, T8108P, T8116 and T8232 4.6.1.4-build202604241011. The affected element is an unknown function of the component Debug Service. Such manipulation leads to improper authentication. The attack may be launched remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101090

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-09-27T21:17:03.003 |

Nezha 2.2.3 contains a Host header injection regression in the OAuth2 redirect endpoint. When the new optional dashboard_host setting is empty, /api/v1/oauth2/{provider} (cmd/dashboard/controller/oauth2.go) reflects the attacker-supplied HTTP Host header into the redirect_uri sent to the identity provider instead of falling back to the configured install_host. An attacker who induces a victim to begin OAuth2 login via a request that reaches Nezha with a forged Host header can cause an attacker-controlled callback URL to be used as the redirect_uri; if the OAuth2 provider accepts it, the victim's authorization code is delivered to the attacker origin, allowing the attacker to complete the OAuth2 login/binding flow and take over the account. This regresses the fix for GHSA-9rc6-8cjv-rcvx and is configuration-dependent (dashboard_host empty). At the time of the advisory no patched version was available.

### CVE-2026-101084

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-27T21:17:02.163 |

obot versions before v0.21.1 fail to enforce Access Control Rules on the /mcp-connect endpoint, allowing any authenticated user to connect to restricted MCP servers if they possess the server ID. Attackers can bypass authorization checks to access and manipulate sensitive backend systems through MCP tool calls using stored OAuth credentials.

### CVE-2026-101065

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-27T21:17:02.027 |

Obot is an open-source AI agent/MCP platform. In all versions up to and including commit d7e6970, the Docker quickstart command documented in the README starts the container listening on 0.0.0.0:8080 with authentication disabled by default. When authentication is disabled, every request is mapped to a synthetic "nobody" user that holds the Owner and Admin roles, so any unauthenticated party who can reach the exposed port obtains full administrative access to the Obot API and UI, including the ability to register and launch attacker-controlled MCP servers. Because the quickstart also mounts /var/run/docker.sock into the container, the MCP runtime backend reachable this way has access to the host's Docker control surface. The fix is documentation-only: the quickstart now enables authentication, and operators who followed the previous instructions should set OBOT_SERVER_ENABLE_AUTHENTICATION=true before exposing the host to any untrusted network.

### CVE-2026-88773

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-27T17:16:56.507 |

Inconsistent interpretation of HTTP requests ('HTTP Request/Response smuggling') vulnerability in Citrix NetScaler ADC and Citrix NetScaler Gateway.

This issue affects ADC: before 14.1-73.37, before 13.1-64.23, before 14.1-73.37 FIPS, and before 13.1-37.279 and NDcPP; Gateway: before 14.1-73.37 FIPS and before 13.1-64.23.

### CVE-2026-73642

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-28T14:17:17.160 |

Dayforce Payroll is vulnerable to Path Traversal  in file download functionality. An unauthenticated attacker can sent GET request with file path parameter set to any path including an absolute
local file path.


Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version R2026.2.0 but may also affect other versions.

### CVE-2026-82378

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-28T08:16:41.540 |

Incorrect Authorization in the OAuth 1.0a authorization endpoint of Apache Roller 6.1.5 allows an unauthenticated remote attacker who learns an outstanding request token for a configured site-wide consumer to bind that token to an arbitrary user account, including an administrator, by submitting an unsigned authorization request. The endpoint derives the authorizing identity from a request-supplied value rather than the authenticated session. Only installations that configure an OAuth 1.0a site-wide consumer are affected, and exploitation requires knowledge of one of its outstanding request tokens. Users are recommended to upgrade to Apache Roller 6.1.6 or later, which binds authorization to the logged-in session.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-101045

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-27T18:16:30.897 |

Fleet-maintained app install and uninstall scripts for macOS are generated from Homebrew cask metadata. In manifests generated before 2026-08-19, the script generator escaped this metadata at some interpolation sites but not all of them, so cask metadata containing shell metacharacters (for example $(...) command substitution) could be carried into scripts that execute as root on managed macOS hosts. An attacker who could land crafted metadata in an upstream Homebrew cask — without needing any Fleet credentials — could achieve arbitrary command execution as root on managed macOS hosts that install or uninstall the affected Fleet-maintained app; exploitation required the crafted metadata to pass both upstream Homebrew cask review and Fleet's review of the automated ingestion pull request. The fix (fleetdm/fleet#51324) landed in Fleet's ingestion pipeline on 2026-08-19 so that all manifests generated on or after that date escape cask metadata at every interpolation site; because manifests are generated centrally and distributed as pre-built content, remediation applied to all deployments with no customer action, and the code fix is included in Fleet v4.92.0.

### CVE-2026-90926

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-28T14:17:21.993 |

Improper Control of Generation of Code ('Code Injection') vulnerability in Innotim Software, Telecommunications and Consultancy Trade Ltd. Co. Logsign SIEM allows Code Injection.

This issue affects Logsign SIEM: from 6.4.101 before 6.4.117.

### CVE-2026-12265

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-28T13:17:21.550 |

Zohocorp ManageEngine DDI Central versions before 6201 are vulnerable to Insufficient access control in HA failover endpoint leading to destructive PostgreSQL database operations.

### CVE-2026-78424

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-28T12:17:40.897 |

Improper parameter handling in NeuVector allows any authenticated user who holds the namespaced Runtime Policies (write) permission or anyone with access to NeuVector’s internal gRPC certificate key pair the ability to inject OS commands in the privileged enforcer container, which can lead to the complete compromise of the worker node. This affects NeuVector 5.4 before 5.4.11, NeuVector 5.5 before 5.5.4, NeuVector 5.6 before 5.6.2 and potentially older versions.

### CVE-2026-12264

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-28T12:17:36.597 |

Zohocorp ManageEngine DDI Central versions before 6201 are vulnerable to Arbitrary file write via HA Failover Config sync upload leading to remote code execution.

### CVE-2026-12269

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-434` |
| Published | 2026-09-28T11:16:44.177 |

Zohocorp ManageEngine DDI Central 6.2.0 build below 6201 had a Keepalived configuration injection vulnerability in the HA configuration workflow. This issue could allow an authenticated operator-level user to modify the Keepalived configuration and potentially execute commands as root on the DDI Central host.

### CVE-2026-12268

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-28T11:16:44.063 |

ManageEngine DDI Central versions below 6201 are vulnerable to PowerShell command injection in Windows DNS SPF/TXT record push leading to remote code execution.

### CVE-2026-85134

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-28T09:17:07.380 |

Unrestricted upload of file with dangerous type vulnerability in Bimser Solution Software Trade Inc. EBA Plus Document and Workflow Management System allows Upload a Web Shell to a Web Server.

This issue affects eBA Plus Document and Workflow Management System: from 6.7.141 before 10.0.11.

### CVE-2026-88778

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-342` |
| Published | 2026-09-27T17:16:57.110 |

Predictable exact value from previous values vulnerability in Citrix NetScaler ADC and Citrix NetScaler Gateway.

This issue affects ADC: before 14.1-73.37, before 13.1-64.23, before 14.1-73.37 FIPS, and before 13.1.37.279 FIPS and NDcPP; Gateway: before 14.1-73.37 and before 13.1-64.23.

### CVE-2026-88777

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-27T17:16:56.990 |

Memory overflow vulnerability vulnerability in Citrix NetScaler ADC and Citrix NetScaler Gateway.

This issue affects ADC: before 14.1-73.37, before 13.1-64.23, before 14.1-73.37 FIPS, and before 13.1.37.279 FIPS and NDcPP; Gateway: before 14.1-73.37 and before 13.1-64.23  leading to unpredictable or erroneous behavior or Denial of Service

### CVE-2026-88776

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-27T17:16:56.870 |

Memory overflow vulnerability vulnerability in Citrix NetScaler ADC and Citrix NetScaler Gateway.
This issue affects ADC: before 14.1-73.37, before 13.1-64.23, before 14.1-73.37 FIPS, and before 13.1.37.279 FIPS and NDcPP; Gateway: before 14.1-73.37 and before 13.1-64.23  leading to unpredictable or erroneous behavior or Denial of Service

### CVE-2026-88775

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-27T17:16:56.750 |

Memory overflow vulnerability in Citrix NetScaler ADC and Citrix NetScaler Gateway.

This issue affects ADC: before 14.1-73.37, before 13.1-64.23, before 14.1-73.37 FIPS, and before 13.1.37.279 FIPS and NDcPP; Gateway: before 14.1-73.37 and before 13.1-64.23 leading Memory overflow vulnerability leading to unpredictable or erroneous behavior or Denial of Service

### CVE-2026-95104

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-28T09:17:08.697 |

Stack-based buffer overflow vulnerability exists in BUFFALO Wi-Fi products. A non-authenticated crafted HTTP request may cause a denial-of-service (DoS) condition.

### CVE-2026-101062

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-27T21:17:01.617 |

Obot before v0.23.0 (affected versions <= v0.22.1) running with OBOT_SERVER_ENABLE_AUTHENTICATION=true exposes OAuth dynamic client registration without authentication and without any restriction on the redirect URIs a client may register. Because the authorization flow auto-completes for an already logged-in user with no consent screen, an attacker who registers a client pointing at their own domain and induces a logged-in victim to visit a single crafted authorization URL receives an authorization code at the attacker-controlled redirect URI and can exchange it for an access token and refresh token. The token minted by the MCP OAuth flow carries the victim's full group set in the JWT, and Obot validated only the issuer and not the audience, so the token is accepted as a bearer token against any Obot API endpoint the victim can access rather than being scoped to the requested MCP server, allowing the attacker to read or modify the victim's resources until the token is revoked. v0.23.0 adds a consent screen, restricts MCP OAuth tokens to the MCP involved in the request, and enforces audience validation.

### CVE-2026-101038

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-28T11:16:43.423 |

A vulnerability was determined in FAST FAC1200R 5.0_20201119_1.0.2. Affected by this vulnerability is the function MmtAtePrase of the component MmtAtePrase Parser. This manipulation causes stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101037

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-28T10:16:42.793 |

A vulnerability was found in FAST FAC1200R 5.0_20201119_1.0.2. Affected is the function parse_advertisement_frame of the component devdiscover Service. The manipulation results in stack-based buffer overflow. The attack may be launched remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-86530

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-28T09:17:07.653 |

BUFFALO Wi-Fi products handle some web form input improperly to assemble command line strings internally. An administrative user may send a crafted HTTP request and execute an arbitrary OS command.

### CVE-2026-101002

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-28T06:16:29.783 |

A security flaw has been discovered in Netcore NBR200V2 1.3.241127.071246. Affected is the function system of the file /usr/bin/network_tools of the component Tools Ping Handler. Performing a manipulation of the argument url results in os command injection. The attack can be initiated remotely. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-100896

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-28T02:17:19.617 |

A weakness has been identified in TOTOLINK N150RT 3.4.0-B20201030. The affected element is the function system of the file /boafrm/formWlSiteSurvey of the component Web Management Interface. This manipulation of the argument wlanif causes os command injection. Remote exploitation of the attack is possible. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-101009

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-28T07:17:20.573 |

A vulnerability was determined in aaPanel BaoTa up to 11.8.0. The affected element is the function panelTask.bt_task._unzip of the file /www/server/panel/class/panelTask.py of the component Unzip Handler. Executing a manipulation of the argument Password can lead to os command injection. The attack may be performed from remote. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101008

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-28T07:17:20.403 |

A vulnerability was found in aaPanel BaoTa up to 11.8.0. Impacted is the function merge_split_file of the file /www/server/panel/class/files.py of the component File Merge Handler. Performing a manipulation of the argument split_file_path results in command injection. The attack is possible to be carried out remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-101007

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-28T07:17:20.197 |

A vulnerability has been found in aaPanel BaoTa up to 11.8.0. This issue affects the function InputSql of the file class/database.py of the component Database Backup Handler. Such manipulation of the argument Password leads to os command injection. The attack can be executed remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-100750

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-28T07:17:18.620 |

Joomla Extension - regularlabs.com - LFI / SSRF in Modules Anywhere 1.5.0 - 9.0.5 for Joomla - Modules Anywhere Pro lets additional attributes on a module tag replace arbitrary parameters of the selected module. This feature is enabled by default in affected versions. The overrides are applied without checking who authored the content containing the tag. The security effect depends on how the selected module consumes the replaced parameter. Joomla's core Feed module provides a concrete affected path: its rssurl parameter is opened by the server and accepts local file: URLs as well as network URLs.

### CVE-2026-101060

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-27T18:16:32.273 |

python-utcp versions before 1.1.4 contain a server-side request forgery vulnerability in HttpCommunicationProtocol.call_tool that validates the initial tool URL but follows HTTP redirects without re-validating the target. Attackers controlling a tool endpoint can return a 302 redirect to internal services, allowing the UTCP client to reach cloud metadata endpoints or internal HTTP services and return their response bodies to the caller.

### CVE-2026-81375

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-610` |
| Published | 2026-09-28T11:16:47.860 |

A Confused Deputy vulnerability in the EmailTask component in Google Cloud Application Integration versions prior to 2026-06-30 on Google Cloud Platform allows an authenticated attacker to read and exfiltrate arbitrary Google-internal files via a crafted attachment file path.


This vulnerability was patched on 30 June 2026, and no customer action is needed.

### CVE-2026-101064

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-27T21:17:01.893 |

Obot before v0.23.0 contains a server-side request forgery vulnerability in remote MCP server registration that allows privileged users to specify arbitrary URLs without destination validation. Attackers with Power User or higher roles can coerce Obot to make requests to internal services and cloud metadata endpoints, reading responses in error messages to disclose sensitive credentials.

### CVE-2026-101043

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-09-27T18:16:29.700 |

pnpm versions 11.0.0 before 11.11.0 and 10.7.0 before 10.34.5 expand ${VAR} environment-variable placeholders in the httpProxy, httpsProxy, and noProxy settings read from a project's pnpm-workspace.yaml. Because the manifest is repository-controlled and the proxy keys were omitted from the request-destination key set that otherwise suppresses placeholder expansion for untrusted manifests (as already done for registry, pnprServer, registries and namedRegistries), an attacker who controls a repository's pnpm-workspace.yaml can cause a victim who clones the repository and runs a pnpm command (e.g. pnpm install) to expand environment secrets such as NPM_TOKEN or GITHUB_TOKEN into a proxy hostname or userinfo and route install traffic — and the corresponding DNS lookups — through an attacker-controlled host. The exfiltration occurs during configuration loading, before any lifecycle script executes. Fixed in pnpm 11.11.0 and 10.34.5.

### CVE-2026-101050

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-27T17:16:56.100 |

Heym before 0.0.53 fails to verify the X-Telegram-Bot-Api-Secret-Token header on Telegram webhook endpoints when credential_id is absent or secret_token is empty. Remote unauthenticated attackers can post forged Telegram updates to trigger workflows with the owner's configured credentials and execute actions on attacker-supplied input.

### CVE-2026-101049

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-27T17:16:55.967 |

Heym before 0.0.53 fails to verify Slack request signatures when trigger nodes lack credential IDs or have empty signing secrets. Remote unauthenticated attackers can send forged Slack events to known webhook URLs to trigger workflows with the owner's credentials.

### CVE-2026-101292

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-09-28T13:17:21.267 |

Apache ActiveMQ Artemis before 2.34.0 contains an unsafe reflection vulnerability in FederationStreamConnectMessage.getFederationPolicy(). The method calls Class.forName(clazz).getConstructor().newInstance() where clazz is read directly from the CORE protocol wire buffer without type validation. An authenticated federation peer can send a FEDERATION_DOWNSTREAM_CONNECT packet with a crafted class name, causing the broker to load and instantiate arbitrary classes visible to the Artemis module classloader. Static initializers (<clinit>) and no-argument constructors (<init>()) execute as side effects before the type cast, enabling denial of service via system-property poisoning, out-of-memory conditions via classloading, or broker state manipulation.

### CVE-2026-91043

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-28T12:17:41.693 |

Allocation of Resources Without Limits or Throttling vulnerability in elixir-mint mint allows a malicious HTTP/2 server to exhaust memory on the client host and cause a denial of service.

Mint.HTTP2 enforces the client's max_header_list_size setting only on the compressed size of an inbound header block, while RFC 9113 section 6.5.2 defines the limit on the decoded header list. An HPACK indexed field costs one byte on the wire and decodes to a dynamic table entry of up to 4 KB, and join_cookie_headers/1 in lib/mint/http2.ex copies every cookie value of a response into one new binary. A header block under the default 256 KB wire limit therefore makes the client allocate about 1 GB for a single response, and several such responses in one delivery exhaust the memory of the process that owns the connection or of the whole VM.

This issue affects mint: from 1.1.0 before 1.11.0.

### CVE-2026-82383

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-28T08:16:42.153 |

Missing Authentication for Critical Function in Apache Roller 6.1.5 allows an unauthenticated remote attacker to persistently change a site-global configuration value (the frontpage weblog selection) on any installed instance, because the setup action remains anonymously reachable after installation and persists configuration without an authorization check. No optional feature or non-default configuration is required; the result can redirect or break the site's public frontpage, with administrative recovery available. Users are recommended to upgrade to Apache Roller 6.1.6 or later, which restricts the write to global administrators.

### CVE-2026-82323

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-28T13:17:22.973 |

Authorization bypass through User-Controlled key vulnerability in Enocta Educational Technologies Inc. Enocta Platform allows Exploitation of Trusted Identifiers.

This issue affects Enocta Platform: through 2026-09-28.

### CVE-2026-82380

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-28T08:16:41.787 |

Cross-Site Request Forgery (CSRF) in Apache Roller 6.1.5 allows a remote attacker to cause a logged-in user to perform state-changing actions under the victim's authority, because the CSRF validation filters accept a request that does not submit the required salt token, validating instead against a value the server itself generated for the request. No optional feature or non-default configuration is required; any logged-in author or administrator is affected when induced to visit a crafted page. Users are recommended to upgrade to Apache Roller 6.1.6 or later, which validates only the submitted salt and applies the same check to multipart forms.

### CVE-2026-97335

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-28T14:17:24.103 |

Incorrect authorization in the custom storage volume creation endpoint in Canonical LXD versions 5.0.0 and later (fixed in 5.0.10, 5.21.8 and 6.10) on Linux allows an authenticated client with permission to create custom volumes in a project to copy, and so read, any custom storage volume from any other project on the server, including its snapshots and configuration. The client does this with a crafted request that sets a source volume and source.project but omits source.type.

### CVE-2026-82928

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1242` |
| Published | 2026-09-28T13:17:23.253 |

mH-DEVELOPER smart home module contains a hardcoded SSH public key in /root/.ssh/authorized_keys, serving as a potential backdoor. The SSH daemon allows root login via key authentication and starts automatically. An attacker with the matching private key can gain a root shell on any affected device, resulting in full system compromise. The key cannot be removed without remounting the file system and survives a factory reset. Vendor notes that this functionality was used only for service purposes.


This issue was fixed in version 3.0.30

### CVE-2026-82386

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-28T08:16:42.527 |

Improper Restriction of XML External Entity Reference in Apache Roller 6.1.5 allows a weblog administrator to read files readable by the Roller process and reach internal network addresses by importing a crafted OPML document, because the bookmark import parser does not disable external entity resolution. No non-default configuration is required; the import is reached through the administrator bookmark-import action. Users are recommended to upgrade to Apache Roller 6.1.6 or later, which uses a hardened parser that disables external entities and document type declarations.

### CVE-2026-82379

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-28T08:16:41.663 |

Authentication Bypass by Capture-replay in Apache Roller 6.1.5 allows an attacker who captures a valid WSSE digest authentication header to replay it and gain the victim's AtomPub authority, because the authentication does not enforce nonce uniqueness or timestamp freshness. Only installations that enable the non-default AtomPub API with WSSE authentication and plaintext-compatible password storage are affected. Users are recommended to upgrade to Apache Roller 6.1.6 or later, which removes WSSE as an AtomPub authentication method; existing installations configured for WSSE fail closed until an administrator explicitly selects a supported authentication method.

### CVE-2026-82376

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-28T08:16:41.293 |

Improper Restriction of XML External Entity Reference in Apache Roller 6.1.5 allows a user with entry-editing rights on a weblog to cause the server to parse an attacker-influenced trackback response with an XML parser that does not disable external entity resolution, leading to disclosure of files readable by the Roller process. The Trackback control is hidden in the standard UI, but its action remains directly reachable, and no non-default server configuration is required. Users are recommended to upgrade to Apache Roller 6.1.6 or later, which removes the outbound trackback response parser.

### CVE-2026-82348

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-28T08:16:40.990 |

Authorization Bypass Through User-Controlled Key in Apache Roller 6.1.5 allows an authenticated user with authoring rights on one weblog to read, modify, or delete resources belonging to another weblog through unscoped identifier-based lookups. This affects multi-user installations where users are intended to be isolated between weblogs; no optional feature or non-default configuration is required. A user with administrator rights on their weblog can also overwrite another weblog's Velocity template, whose content is evaluated when the victim weblog renders. Users are recommended to upgrade to Apache Roller 6.1.6 or later, which scopes authoring resource lookups to the acting weblog.

### CVE-2026-100908

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-28T05:16:29.877 |

A vulnerability has been found in Eyeplus 57.0.0.0308. This affects an unknown function of the component p2pcam HTTP Parser. Such manipulation leads to stack-based buffer overflow. The attack may be performed from remote. The exploit has been disclosed to the public and may be used.

### CVE-2026-100751

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-28T07:17:19.703 |

Joomla Extension - regularlabs.com - Privileged stored XSS via data-rlta-url attributes in Tabs & Accordions (Pro) 2.3.0 - 3.1.0 - Tabs & Accordions Pro accepts a url option for an item and writes it to a generated data-rlta-url attribute. The browser code passes that value to window.open() when the item is activated. Affected versions do not reject browser URL schemes which execute JavaScript. Joomla sees ordinary plugin syntax while filtering the authored article; Tabs & Accordions creates the executable browser behavior later while rendering the article.

### CVE-2026-96280

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-09-27T21:17:04.200 |

The OCI delta stream parser read sizes as guint64 but passed them to GLib I/O and allocation functions expecting gsize (32 bits on 32-bit systems), causing undersized allocations while subsequent operations use the original 64-bit size, leading to heap buffer overflows. An attacker controlling an OCI registry can craft a delta stream that triggers this during flatpak install/update, potentially achieving code execution on 32-bit systems.

### CVE-2026-82375

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-28T08:16:41.170 |

Server-Side Request Forgery (SSRF) in Apache Roller 6.1.5 allows an authenticated user with entry-editing rights on a weblog to cause outbound HTTP requests to attacker-chosen destinations through legacy outbound Trackback and entry enclosure handling. The Trackback control is hidden in the standard UI, but its action remains directly reachable; the enclosure path is relevant only when an author supplies an enclosure URL. No non-default server configuration is required, and the default empty Trackback allow-list permits all destinations. Requests can reach loopback and private-network addresses, while enclosure handling exposes response status, content type, and length. Users are recommended to upgrade to Apache Roller 6.1.6 or later, which removes the outbound trackback action and stops dereferencing enclosure URLs.

### CVE-2026-101042

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-27T17:16:55.820 |

Parse Server is an open-source backend server. In versions >= 9.0.0 < 9.10.1-alpha.10 and >= 8.0.2 < 8.6.91, the code-based authentication adapters (GitHub, Google Play Games, Instagram, LINE, LinkedIn, Microsoft, QQ, Spotify, WeChat, Weibo) verify the client's authorization code with the external provider on signup and on provider linking, but not when authentication data is supplied together with a username and password on the login endpoint. As a result, a low-privileged authenticated user can attach an arbitrary, unverified provider identity to their own account without the provider ever being contacted, spoofing an external identity toward application logic that trusts the linked provider ID. An attacker can also pre-hijack accounts: by claiming the provider ID of a victim who has not yet linked that provider, the victim's later legitimate sign-in with that provider resolves to the attacker's account. Only deployments configuring one of the affected code-based auth adapters are impacted. Versions 9.10.1-alpha.10 and 8.6.91 fix the issue by running the adapter's credential verification on the login and challenge endpoints and rejecting a provider identity already linked to another user. As a workaround, disable the affected code-based auth adapters.

### CVE-2026-86330

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-28T13:17:24.787 |

An OS command injection flaw was found in the set_hostname_internal function of NooBaa's cluster_internal_api. This component is responsible for managing the Multi-Cloud Object Gateway in OpenShift Data Foundation. The vulnerability occurs because the hostname parameter is passed directly to a shell command without proper sanitization. An authenticated attacker with administrative privileges can provide a specially crafted hostname containing shell metacharacters to execute arbitrary commands on the host system with the privileges of the NooBaa process.

### CVE-2026-12267

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-28T11:16:43.943 |

ManageEngine DDI Central versions below 6201 are vulnerable to Command injection in Windows DNS Query Resolution Policy name field leading to remote code execution.

### CVE-2026-90925

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-28T14:17:21.863 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Innotim Software, Telecommunications and Consultancy Trade Ltd. Co. Logsign SIEM allows Path Traversal.

This issue affects Logsign SIEM: from 6.4.101 before 6.4.117.

### CVE-2026-15952

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-28T14:17:15.110 |

Incorrect Permission Assignment for Critical Resource vulnerability in ABB Protection and control IED manager (PCM600).

This issue affects Protection and control IED manager (PCM600): through 2.14.

### CVE-2026-52748

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-28T13:17:21.847 |

The Kaon AR2140X router contains a vulnerability where the backup functionality is accessible without authentication. This allows an unauthenticated remote attacker to trigger a configuration backup and retrieve it in a form encrypted by a device-specific key. Triggering this function renders the router inoperable for a substantial period of time. 



This issue was identified in firmware versions up to 4.2.17. Status of newer versions remains unknown.

### CVE-2026-94286

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-09-28T09:17:08.463 |

An out-of-bounds read in libXtst's RECORD reply parser in libXtst before 1.2.6 could be used by malicious X servers to crash attached X clients.

### CVE-2026-101086

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-27T21:17:02.450 |

Nezha Dashboard versions before 2.3.5 fail to restrict service monitor task types to supported probe types, allowing authenticated users with nezha:service:write scope to submit privileged task types through the service API. Attackers can deliver command execution or Agent configuration tasks to Agents within their authorization scope by exploiting the shared protobuf Task.Type namespace between service monitors and privileged operations.

### CVE-2026-101085

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-197` |
| Published | 2026-09-27T21:17:02.307 |

Nezha before 2.3.8 fails to validate alert rule type and duration bounds, allowing authenticated non-administrator users to create malformed rules that trigger unrecovered panics in the alert evaluator goroutine. Attackers can submit a crafted alert rule via the POST /api/v1/alert-rule endpoint to crash the dashboard process, which persists the rule and causes repeated crashes on restart, disabling all monitoring and control plane functionality.

### CVE-2026-101059

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-27T18:16:32.130 |

utcp-http before 1.1.4 fails to validate the OAuth2 tokenUrl field from remote OpenAPI specifications, allowing attackers to redirect credential submission to arbitrary endpoints. When a victim registers an attacker-controlled OpenAPI spec and invokes a generated OAuth2-protected tool, the library POSTs the victim's client_id and client_secret to the attacker-supplied token endpoint without URL validation.

### CVE-2026-101058

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-27T18:16:31.973 |

python-utcp (pip package utcp-http) before 1.1.12 does not verify whether tool URLs declared in a hand-written UTCP manual point at the agent's own loopback interface when that manual is discovered from a remote, non-loopback origin. Because ensure_secure_url intentionally permits loopback HTTP for local development and native manuals bypassed the loopback check performed by the OpenAPI converter, an attacker who can serve a UTCP manual that a victim registers can cause the client to issue requests to services bound only to 127.0.0.1 on the victim host and have the response bodies returned to the caller (server-side request forgery). The http, sse and streamable_http protocols are all affected. Reach is limited to loopback, and exploitation further requires a loopback service that answers unauthenticated requests with useful data. Fixed in utcp-http 1.1.12, which rejects manuals fetched from a non-loopback origin that declare loopback tool URLs, keyed off the final post-redirect discovery URL.

### CVE-2026-101044

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-27T18:16:30.753 |

pacquet, the Rust package-manager component shipped in the pnpm npm package versions >=12.0.0-alpha.0 and <12.0.0-alpha.5, does not validate dependency alias/name paths taken from a lockfile before using them in install-time filesystem joins. When a user installs a project with an attacker-supplied lockfile using --trust-lockfile or a frozen lockfile, alias entries containing path traversal segments (for example '../../escaped-link') are used when creating dependency and package links, bin destinations, hoisted entries, and virtual-store slots, allowing symlinks and directories to be created outside the intended project and node_modules boundary. Version 12.0.0-alpha.5 validates dependency names and every virtual-store slot path with a shared safe-join containment helper before any filesystem materialization, rejecting traversal, absolute, platform-specific, and reserved names with ERR_PNPM_INVALID_DEPENDENCY_NAME.

### CVE-2026-88774

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `NVD-CWE-noinfo` |
| Published | 2026-09-27T17:16:56.633 |

Vulnerability in Citrix NetScaler ADC and Citrix NetScaler Gateway.

This issue affects ADC: before 14.1-73.37, before 13.1-64.23, before 14.1-73.37 FIPS, and before 13.1.37.279 FIPS and NDcPP; Gateway: before 14.1-73.37 and before 13.1-64.23 leading to a feature policy bypass due to improper HTTP URL based expression usage.
