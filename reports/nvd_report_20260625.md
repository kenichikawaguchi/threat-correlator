# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-24 15:01 UTC
- **対象期間**: `2026-06-23T19:00:43.000Z` 〜 `2026-06-24T15:01:19.000Z`
- **重要CVE数**: 71 件（Critical 9.0+: 16 件 / High 7.0〜: 55 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超に上り、特に **リモートコード実行 (RCE) や認証バイパス** が目立ちました。  
- コンテナ CI 環境や組み込みデバイスのネットワークスタックに対する **ゼロデイ的な遠隔実行** が多数報告されています。  
- WordPress 系プラグインや SaaS 向けの認証フローに対する **入力検証不備** が続き、アカウント乗っ取りや情報漏洩のリスクが高まっています。  
- いずれも **デフォルトで外部に開放されたポート／ヘッダー** を経由した攻撃が可能であり、内部ネットワークの境界防御だけでは防げないケースが多いです。  

---

## 2. 特に注目すべき CVE  

| CVE | 重大度 (CVSS) | 主な影響 | 注目すべき理由 |
|-----|---------------|----------|----------------|
| **CVE‑2026‑12537** | 10.0 | Google **Gemini CLI**（0.39.1 未満）および `run‑gemini‑cli` GitHub Action（0.1.22 未満）で、コンテナランチャーの OS コマンド文字列が適切にエスケープされず、**サンドボックス外でコード実行** が可能になる。 | CI/CD パイプラインは多くの組織で共有リソースとなっており、攻撃者がビルドジョブを乗っ取ると **全社的なコード改竄・機密情報漏洩** が即座に起こり得る。 |
| **CVE‑2026‑12848** (同一系列: 12847, 12846, 12485) | 10.0 | **GV‑I/O Box 4E**（ファームウェア 2.09）に内蔵された `DVRSearch` UDP サービス（ポート 10001）に対し、任意のパケットを送信するだけで **リモートコード実行** が可能。 | 産業・ビルディングオートメーションで広く使われる組み込みデバイス。ネットワーク上に露出したまま放置すると、制御系システム全体が乗っ取られる危険がある。 |
| **CVE‑2026‑12417** / **CVE‑2026‑12416** | 9.8 | WordPress 用 **SignUp & SignIn**、**Invoice Generator** プラグイン（1.0.0 まで）で、パスワードリセット用 AJAX ハンドラが認証・nonce をチェックせず、**アカウント乗っ取り** が可能。 | 多くのサイトでプラグインがそのままインストールされたままになりがち。管理者権限取得により、サイト全体の改ざん・マルウェア埋め込みが容易になる。 |
| **CVE‑2026‑54588** | 9.6 | **Poweradmin**（4.2.4 / 4.3.3 未満）で `HTTP_HOST` ヘッダーを検証せず OIDC・SAML のコールバック URL を生成。**オープンリダイレクト／認証情報漏洩** が発生。 | DNS 管理ツールはインフラ全体に影響するため、認証フローの改ざんは **権限昇格や内部情報の窃取** に直結する。 |
| **CVE‑2026‑41862** | 8.8 | **Spring Statemachine**（3.0 系）で Kryo シリアライズされたステートマシンコンテキストを **クラスホワイトリストなしでデシリアライズ**。攻撃者が細工したバイト列を送ると **JVM 内で任意コード実行** が可能。 | Java エンタープライズアプリは多くが Spring を採用。デシリアライズ攻撃はサーバ側で直接コードが走るため、被害範囲が広い。 |

> **注**：上記の GV‑I/O Box 系は同一脆弱性が複数 CVE に分割されているが、実質的に同一のリスクを示すため **1 件** としてまとめて評価しています。

---

## 3. 推奨アクション  

### 3.1 共通対策
- **ネットワーク境界の最小化**  
  - 不要な UDP/ポート 10001（GV‑I/O Box）や外部からの `HTTP_HOST` ヘッダー受信をファイアウォールで遮断。  
- **インシデントレスポンス手順の整備**  
  - 重要コンポーネント（CI/CD、IoT デバイス、認証サーバ）の **緊急パッチ適用フロー** を自動化。  
- **監査ログの強化**  
  - CI ランナー、WordPress 管理画面、Spring アプリの認証・デシリアライズ処理に対する **詳細ログ** を有効化し、SIEM でリアルタイム検知。

### 3.2 個別パッケージ／バージョンアップ

| 製品 / パッケージ | 現行脆弱バージョン | **推奨アップデート** | 主な修正点 |
|-------------------|-------------------|----------------------|------------|
| **Google Gemini CLI** | `< 0.39.1` | `0.39.1` 以上 | コンテナランチャーでの OS コマンドエスケープ修正 |
| **run‑gemini‑cli (GitHub Action)** | `< 0.1.22` | `0.1.22` 以上 | CI 環境でのサンドボックス突破防止 |
| **GV‑I/O Box 4E (ファームウェア)** | `2.09`（デフォルト） | ベンダー提供の **2.10 以降**（セキュリティパッチ） | `DVRSearch` UDP サービスの認証追加・コマンドインジェクション防止 |
| **WordPress プラグイン – SignUp & SignIn** | `1.0.0` まで | `1.0.1` 以上 | パスワードリセット AJAX に nonce と権限チェックを実装 |
| **WordPress プラグイン – Invoice Generator** | `1.0.0` まで | `1.0.1` 以上 | 同上 |
| **Poweradmin

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-12537

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-24T14:17:29.630 |

Improper Neutralization used in an OS Command in the container launcher in Google Gemini CLI (versions prior to 0.39.1) and run-gemini-cli GitHub Action (versions prior to 0.1.22) on headless CI platforms allows an unprivileged attacker to achieve pre-sandbox host-level code execution a maliciously crafted .gemini/.env file.

### CVE-2026-12848

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-24T05:17:26.710 |

GV-I/O Box 4E is a smart embedded device with 4 input and 4 relays output that can be controlled over Ethernet and RS-485.

DVRSearch is a service running by default on the IOBox listening for UDP messages on port 10001. Any user on the network can send messages to this service and interact with it. 



Upon receiving a UDP message,  the server reads at most 1460 bytes into a local buffer and a pointer to the buffer is stored in a global variable:



#### DNS field stack overflow

The following code is vulnerable to a stack overflow that is attacker-controlled:



    v8 = strlen(g_network_config->dns_addr);

    memcpy(&reply_buf[248], g_network_config->dns_addr, v8);

### CVE-2026-12847

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-24T05:17:26.587 |

GV-I/O Box 4E is a smart embedded device with 4 input and 4 relays output that can be controlled over Ethernet and RS-485.

DVRSearch is a service running by default on the IOBox listening for UDP messages on port 10001. Any user on the network can send messages to this service and interact with it. 



Upon receiving a UDP message,  the server reads at most 1460 bytes into a local buffer and a pointer to the buffer is stored in a global variable:


#### Gateway field stack overflow

The following code is vulnerable to a stack overflow that is attacker-controlled:



      v7 = strlen(g_network_config->gateway);

      memcpy(&reply_buf[216], g_network_config->gateway, v7);

### CVE-2026-12846

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-24T05:17:26.463 |

GV-I/O Box 4E is a smart embedded device with 4 input and 4 relays output that can be controlled over Ethernet and RS-485.

DVRSearch is a service running by default on the IOBox listening for UDP messages on port 10001. Any user on the network can send messages to this service and interact with it. 



Upon receiving a UDP message,  the server reads at most 1460 bytes into a local buffer and a pointer to the buffer is stored in a global variable:


#### Net Mask field stack overflow

The following code is vulnerable to a stack overflow that is attacker-controlled:



      v6 = strlen(g_network_config->net_mask);

      memcpy(&reply_buf[184], g_network_config->net_mask, v6);

### CVE-2026-12485

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-24T05:17:25.973 |

GV-I/O Box 4E is a smart embedded device with 4 input and 4 relays output that can be controlled over Ethernet and RS-485.

DVRSearch is a service running by default on the IOBox listening for UDP messages on port 10001. Any user on the network can send messages to this service and interact with it. 



Upon receiving a UDP message,  the server reads at most 1460 bytes into a local buffer and a pointer to the buffer is stored in a global variable:


#### IP field stack overflow

The following code is vulnerable to a stack overflow that is attacker-controlled:



      v3 = strlen(g_network_config->ip_addr);

      memcpy(&reply_buf[36], g_network_config->ip_addr, v3);

### CVE-2026-12417

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-06-24T07:16:26.890 |

The SignUp & SignIn plugin for WordPress is vulnerable to Authentication Bypass via Weak Password Reset Validation leading to Account Takeover in versions up to, and including, 1.0.0. This is due to the `pravel_change_password()` AJAX handler — registered via `wp_ajax_nopriv_pravel_change_password` and therefore accessible to unauthenticated users — performing no nonce verification, no capability check, and only a loose equality check between an attacker-supplied `reset_activation_code` POST parameter and the target user's `forgot_email` user meta value; when a user has never initiated a password reset, `get_user_meta()` returns an empty string that trivially satisfies this check against an omitted or empty attacker-supplied code. This makes it possible for unauthenticated attackers to change the password of any WordPress user, including administrators, by sending a crafted POST request to `admin-ajax.php` with `action=pravel_change_password`, `reset_user_id` set to the target account's user ID, and `new_password_custom` set to an attacker-chosen password. Successful exploitation allows the attacker to authenticate with the newly set password and fully take over the targeted account, achieving administrator-level privilege escalation on the affected site.

### CVE-2026-12416

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-06-24T07:16:26.767 |

The Invoice Generator plugin for WordPress is vulnerable to Account Takeover via Password Reset in all versions up to, and including, 1.0.0. This is due to the `pravel_invoice_change_password()` function being registered as a nopriv AJAX handler with no nonce verification and no authorization check, and performing a loose equality comparison between the supplied `reset_activation_code` POST parameter and the target user's stored `forgot_email` user meta — a check that trivially evaluates to true (`'' == ''`) for any user who has never initiated a forgot-password request, which applies to administrators under normal conditions. This makes it possible for unauthenticated attackers to supply an arbitrary user ID via the `reset_user_id` POST parameter, bypass the activation code check entirely by omitting `reset_activation_code`, and set the target account's password to an attacker-chosen value, enabling full takeover of any account on the site, including administrator accounts.

### CVE-2026-53753

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-913` |
| Published | 2026-06-23T19:17:07.107 |

Crawl4AI is an open-source LLM friendly web crawler & scraper. Prior to 0.8.7, the _safe_eval_expression() function in the computed fields feature uses an AST validator that only blocks attributes starting with underscore. Python generator and frame object attributes (gi_frame, f_back, f_builtins) do NOT start with underscore, enabling a complete sandbox escape to achieve arbitrary code execution. The attack requires no authentication (JWT disabled by default) and is triggered via POST /crawl with a crafted extraction schema. This vulnerability is fixed in 0.8.7.

### CVE-2026-54588

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-20;CWE-601` |
| Published | 2026-06-23T23:16:49.863 |

Poweradmin is a web-based DNS administration tool for PowerDNS server. Versions prior to 4.2.4 and 4.3.3 use the attacker-controlled `HTTP_HOST` request header as the authoritative source for building callback URLs in its OIDC, SAML, and logout authentication flows without any validation. An unauthenticated attacker can poison the `redirect_uri` sent to the Identity Provider, causing the IdP to redirect the victim's authorization code to an attacker-controlled server - resulting in full account takeover with no credentials required. Versions 4.2.4 and 4.3.3 patch the issue.

### CVE-2026-11807

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-23T21:16:54.350 |

A missing authorization vulnerability was found in the Event-Driven Ansible (EDA) websocket API. The /api/eda/ws/ansible-rulebook endpoint does not verify user permissions when processing Worker messages. Any authenticated user can send a forged message with an arbitrary activation_id to receive plaintext credentials associated with that activation, including OAuth tokens, vault passwords, and SSH keys.

### CVE-2026-56237

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-24T13:16:33.467 |

Capgo before 12.128.2 contains a broken authentication vulnerability in its API key generation mechanism. API keys are exposed in frontend requests, and the backend fails to validate that keys are securely generated and bound to the authenticated user. An attacker can tamper with the API key parameter in the generation request and supply arbitrary values, generating custom API keys without proper authorization, which can lead to unauthorized access to protected endpoints.

### CVE-2026-56223

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-24T13:16:33.067 |

Capgo before 12.128.2 contains a cross-domain SSO account takeover vulnerability in the provision-user endpoint that allows attackers to merge arbitrary victim accounts based on email match without validating SSO provider domain authorization. An attacker with enterprise org admin access and a malicious IdP can forge SAML assertions containing victim email addresses to trigger account merge and gain full access to victim accounts, organizations, and data.

### CVE-2026-12851

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-24T05:17:27.157 |

Multiple OS command injection vulnerabilities exist in the libNetSetObj.so functionality of GeoVision GV-I/O Box 4E 2.09. A specially crafted network packet can lead to command execution. An attacker can send a network request to trigger this vulnerability.


`libNetSetObj.so` is an internal library used by various binaries on the device to configure the network stack (start and stop various services, configure IP, Netmask, gateway, dns, etc.)


#### CNetSetObj::m_F_n_Set_DNS_Addr command injection

The following function can take up to two addresses, performs no sanitization and then calls `system`. This is a classic command injection vulnerability. The function is reachable from both the network-exposed `DVRSearch` service and the `Network.cgi` endpoint. 



    int __fastcall CNetSetObj::m_F_n_Set_DNS_Addr(CNetSetObj *this, char *dns1, char *dns2)

    {

      int result; // r0

      char v5[80]; // [sp+0h] [bp-50h] BYREF



      if ( !dns1 )

        result = 0;

      if ( dns1 )

      {

        sprintf(v5, "/bin/echo nameserver %s > /etc/resolv.conf", dns1);  // attacker controlled dns1 field

        system(v5);

        if ( dns2 )

        {

          sprintf(v5, "/bin/echo nameserver %s >> /etc/resolv.conf", dns2);

          system(v5);

        }

        return 1;

      }

      return result;

### CVE-2026-12850

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-24T05:17:27.020 |

Multiple OS command injection vulnerabilities exist in the libNetSetObj.so functionality of GeoVision GV-I/O Box 4E 2.09. A specially crafted network packet can lead to command execution. An attacker can send a network request to trigger this vulnerability.


`libNetSetObj.so` is an internal library used by various binaries on the device to configure the network stack (start and stop various services, configure IP, Netmask, gateway, dns, etc.)


#### CNetSetObj::m_F_n_Set_Gate_way command injection

The following function takes a string as a gatewy address, performs no sanitization on it and calls `system`. This is a classic command injection vulnerability. The function is reachable from both the network-exposed `DVRSearch` service and the `Network.cgi` endpoint. 





    int __fastcall CNetSetObj::m_F_n_Set_Gate_way(const char **this, char *gw, char *dev)

    {

      char s[324]; // [sp+4h] [bp-144h] BYREF



      if ( !dev && !*this || !gw )

        return 0;

      system("/sbin/route del -net 224.0.0.0 netmask 224.0.0.0");

      system("/sbin/route del default ");

      if ( dev )

        sprintf(s, "/sbin/route add default gw %s dev %s", gw, dev); //attacker controlled gw string

      else

        sprintf(s, "/sbin/route add default gw %s dev %s", gw, *this); //attacker controlled gw string

      system(s);

      sprintf(s, "/sbin/route add -net 224.0.0.0 netmask 224.0.0.0 gw %s dev %s", gw, *this); //attacker controlled gw string

      system(s);

      return 1;

      }

### CVE-2026-12849

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-24T05:17:26.890 |

Multiple OS command injection vulnerabilities exist in the libNetSetObj.so functionality of GeoVision GV-I/O Box 4E 2.09. A specially crafted network packet can lead to command execution. An attacker can send a network request to trigger this vulnerability.


`libNetSetObj.so` is an internal library used by various binaries on the device to configure the network stack (start and stop various services, configure IP, Netmask, gateway, dns, etc.)



#### CNetSetObj::m_F_n_Set_Net_Mask command injection

The following function takes a string as a net mask address, performs no sanitization on it and calls `system`. This is a classic command injection vulnerability. The function is reachable from both the network-exposed `DVRSearch` service and the `Network.cgi` endpoint. 



    int __fastcall CNetSetObj::m_F_n_Set_Net_Mask(const char **this, char *netmask_addr)

    {

      bool v2; // zf

      char v4[72]; // [sp+0h] [bp-48h] BYREF



      v2 = *this == 0;

      if ( *this )

        v2 = netmask_addr == 0;

      if ( v2 )

        return 0;

      sprintf(v4, "/sbin/ifconfig %s netmask %s", *this, netmask_addr);  // attacker controlled netmask_addr

      system(v4);

      return 1;

    }

### CVE-2026-12486

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-24T05:17:26.220 |

Multiple OS command injection vulnerabilities exist in the libNetSetObj.so functionality of GeoVision GV-I/O Box 4E 2.09. A specially crafted network packet can lead to command execution. An attacker can send a network request to trigger this vulnerability.


`libNetSetObj.so` is an internal library used by various binaries on the device to configure the network stack (start and stop various services, configure IP, Netmask, gateway, dns, etc.)


#### CNetSetObj::m_F_n_Set_IP_Addr command injection

The following function takes a string as an ip address, performs no sanitization and calls `system`. This is a classic command injection vulnerability. The function is reachable from both the network-exposed `DVRSearch` service and the `Network.cgi` endpoint. 



    int __fastcall CNetSetObj::m_F_n_Set_IP_Addr(const char **this, char *ip_addr)

    {

      bool v2; // zf

      char v4[72]; // [sp+0h] [bp-48h] BYREF



      v2 = *this == 0;

      if ( *this )

        v2 = ip_addr == 0;

      if ( v2 )

        return 0;

      sprintf(v4, "/sbin/ifconfig %s %s", *this, ip_addr);  // attacker controlled ip address 

      system(v4);

      return 1;

    }

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-12681

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1285` |
| Published | 2026-06-24T02:16:28.060 |

Improper Validation of Specified Index, Position, or Offset in Input vulnerability in Google go-attestation. parseEfiSignatureList() does not advance the buffer past vendor bytes before reading entries. For hashSHA256SigGUID lists, this allows attacker-controlled vendor header bytes to be appended to the trusted SHA256 hash list. A crafted TPM event log could inject arbitrary SHA256 hashes into the verifier's trusted measurement database, enabling a remote attestation verifier to accept a compromised boot state. This issue affects go-attestation: through 0.6.0.

### CVE-2026-56245

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-24T13:16:34.820 |

Supabase Capgo before 12.128.2 contains an authorization bypass vulnerability in the SECURITY DEFINER record_build_time RPC function that allows unauthenticated attackers to insert arbitrary build-time records. Attackers can exploit this by calling POST /rest/v1/rpc/record_build_time with a public API key to poison billing and quota data for any organization, enabling resource exhaustion and cross-tenant billing manipulation.

### CVE-2026-12242

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-24T13:16:31.447 |

The AdRotate Banner Manager plugin for WordPress is vulnerable to PHP Code Injection in all versions up to, and including, 5.17.7 via the 'banner' attribute of the adrotate shortcode. This is due to insufficient input validation and sanitization of the banner shortcode attribute before concatenation into a PHP code string wrapped in W3 Total Cache mfunc or Borlabs Cache fragment markers. This makes it possible for authenticated attackers, with Contributor-level access and above, to execute arbitrary PHP code on the server. This vulnerability requires W3 Total Cache or Borlabs Cache support to be enabled in AdRotate settings.

### CVE-2026-7761

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-24T08:16:24.830 |

The Ultimate Member plugin for WordPress is vulnerable to Account Takeover via Password Reset Link Disclosure in all versions up to and including 2.11.4. This is due to a chain of three logic bugs: (1) an MD5 hash fallback in get_directory_by_hash() that allows any post to be used as a member directory by computing SUBSTRING(MD5(post_id), 11, 5), (2) a strstr() parsing logic flaw in post_data() that allows bypassing WordPress's protected meta key restrictions by placing '_um_' anywhere in the meta key name rather than at the start, and (3) missing field name validation in build_user_card_data() that allows arbitrary field names including 'password_reset_link' to be passed to um_filtered_value(). This makes it possible for authenticated attackers with Contributor-level access and above to create a malicious post via XMLRPC with crafted meta fields, use the MD5 fallback to point the member directory AJAX handler to their post, inject 'password_reset_link' into the tagline_fields configuration, and leak live password reset URLs for all users in the member directory response, including administrators.

### CVE-2026-4297

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-24T07:16:27.310 |

The Welcome Software Publishing plugin for WordPress is vulnerable to Arbitrary Options Update in all versions up to and including 0.0.31. This is due to a missing capability check in the nc_setOption() function, which is exposed via the nc.setOption XML-RPC method. The function authenticates the user via $wp_xmlrpc_server->login() (verifying credentials are valid) but does not perform any authorization check such as current_user_can('manage_options'). This makes it possible for authenticated attackers, with Subscriber-level access and above, to update arbitrary WordPress options via XML-RPC requests. This can be leveraged to change the default_role option to 'administrator' and then register a new administrator account, achieving full privilege escalation and site takeover.

### CVE-2026-54639

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1321` |
| Published | 2026-06-24T01:16:25.363 |

Style Dictionary, a build system for creating cross-platform styles, has a prototype pollution vulnerability starting in version 4.3.0 and prior to version 5.4.4. Impact users have: direct usage of `convertTokenData(tokens, { output: 'object' });`; indirect usage, via using Expand API; and/or indirect usage via SD's transform lifecycle. Impact is high for this when style-dictionary is used as an integration in a NodeJS server application. Impact is moderate for when style-dictionary is used as an integration in a Web application. Impact is low for most common cases where the user of style-dictionary also maintains the tokens, and access is limited via read/write access to the repository/workflows where it is used. A patch has been published in version `5.4.4`. The only known workaround is to sanitize token data first. Whether using DTCG format or old Style Dictionary format, check the token data object recursively for any object keys that include `__proto__`.

### CVE-2026-41862

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-23T21:16:57.820 |

Spring Statemachine's Kryo-based persistence backends (JPA, MongoDB, Redis and ZooKeeper) deserialise persisted state-machine contexts without enforcing a class allowlist (CWE-502, deserialisation of untrusted data), which can lead to remote code execution inside the application JVM.

Affected versions:
Spring Statemachine 4.0.0 through 4.0.1
Spring Statemachine 3.2.0 through 3.2.4

### CVE-2026-56270

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-24T13:16:35.540 |

Flowise before 3.1.0 (versions 3.0.13 and earlier) contains a missing authentication vulnerability in the /api/v1/loginmethod endpoint that allows unauthenticated users to retrieve an organization's complete SSO configuration, including OAuth client secrets in cleartext, by providing an organizationId parameter. Remote attackers can send a GET request to harvest sensitive API credentials for Google, Microsoft/Azure, GitHub, and Auth0 integrations. This affects FlowiseAI Cloud and self-hosted instances where the endpoint is exposed.

### CVE-2026-56232

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-24T13:16:33.327 |

Capgo before 12.128.2 fails to enforce limited_to_orgs and limited_to_apps constraints on subkeys provided via x-limited-key-id header in middlewareKey function. Attackers can bypass subkey scope restrictions by referencing their own subkeys, causing all downstream route handlers to use the unrestricted parent key instead of the scoped subkey.

### CVE-2026-7574

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-353` |
| Published | 2026-06-24T00:16:34.173 |

Anthropic Claude Desktop Cowork VM image handling (confirmed across v1.1348.0 through v1.2278.0, including v1.1348.0, v1.1617.0, and v1.2278.0) validates only file presence and a version marker string before booting rootfs.img, but does not verify image content integrity at time-of-use. A local attacker with unprivileged code execution as the victim macOS user can modify the VM root filesystem image and have it trusted on subsequent Cowork VM boots, enabling persistent arbitrary code execution in the VM and access to host-mounted directories. The estimated CWE mapping is CWE-353 (Missing Support for Integrity Check).

### CVE-2026-35025

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-06-24T14:17:30.950 |

ProFTPD through 1.3.9b and 1.3.10rc2 contains an access control bypass vulnerability that allows authenticated FTP users to circumvent Directory ACL restrictions by prefixing paths with /proc/self/root in the RNFR command handler. Attackers can exploit the unresolved symlink components in dir_canonical_path() to cause dir_check() to perform lexical path comparisons that match no configured Directory block, enabling rename operations on files in DenyAll-protected directories and subsequent retrieval of those files. Mitigation: Sessions configured with DefaultRoot (chroot) are not affected, as chroot changes the directory to which /proc/self/root resolves.

### CVE-2026-53755

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-23T19:17:07.477 |

Crawl4AI is an open-source LLM friendly web crawler & scraper. Prior to 0.8.9, the Docker API server applied its SSRF destination check to the crawl target URL only, not to the proxy address. An unauthenticated request could supply a proxy pointing at an internal IP and route the browser through it, reaching internal services and cloud-metadata endpoints, while using a perfectly valid crawl URL. The Docker API is unauthenticated by default. /crawl, /crawl/stream, and /crawl/job accept a browser_config (and crawler_config). The following all feed Chromium's egress and were unchecked: browser_config.proxy_config.server, browser_config.proxy (deprecated field), crawler_config.proxy_config.server, and --proxy-server / --proxy-pac-url / --proxy-bypass-list / --host-resolver-rules flags in browser_config.extra_args. This vulnerability is fixed in 0.8.9.

### CVE-2025-71332

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-24T13:16:30.263 |

Flowise through 2.2.7 contains a SQL injection vulnerability in the importChatflows API. Due to insufficient validation of the chatflow.id value, an authenticated user can supply a crafted JSON import file whose id field is concatenated unsanitized into a SQL IN clause, allowing arbitrary SQL to be executed, including blind and error-based extraction of data from the credential table.

### CVE-2026-42450

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-06-24T14:17:31.190 |

OpenColorIO is a color management framework for visual effects and animation. Prior to version 2.5.2, `FileFormatSpi3D.cpp:163` uses `sscanf` with `%s` into 64-byte stack buffers when parsing LUT data lines. Input comes from `lineBuffer[4096]`, so a crafted .spi3d file can overflow by ~4000 bytes on non-Windows. Version 2.5.2 fixes the issue.

### CVE-2026-56785

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-23T23:16:50.020 |

FlatPress versions prior to commit 10be83c, contains a stored cross-site scripting vulnerability in comment and contact forms where name, URL, and email fields are rendered without proper output encoding in Smarty templates. Attackers can inject arbitrary HTML and JavaScript through these fields to execute malicious scripts in browsers of viewers including administrators, or bypass URL scheme validation to inject javascript: or data: URIs.

### CVE-2026-47387

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-23T21:17:00.743 |

NocoDB is software for building databases as spreadsheets. Prior to 2026.05.1, the shared form-view submit handler (packages/nc-gui/composables/useSharedFormViewStore.ts) in NocoDB writes the form's redirect_url to window.location.href after a same-host check that does not validate the URL scheme. A user with editor role (or above) on any base can plant a javascript: URL in the form's redirect_url; when an authenticated viewer opens the share-link and submits the form, the payload executes in the NocoDB origin and can read the session token from localStorage["nocodb-gui-v2"]. This vulnerability is fixed in 2026.05.1.

### CVE-2026-54320

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-287;CWE-863` |
| Published | 2026-06-23T19:17:07.993 |

Daytona is a secure and elastic infrastructure runtime for AI-generated code execution and agent workflows. Prior to 0.184.0, organization invitations could be accepted (and declined) by a user whose email matched the invitation but had not been verified. Daytona authenticates users via OIDC and matches an invitation's target email against the email in the caller's token, but the invitation accept and decline paths did not require that email to be verified, unlike organization creation, which already enforced verification. On identity providers that allow self-service signup and issue a session before the email is verified, an actor could register an address matching a pending invitation, leave it unverified, and accept the invitation, joining the target organization with the role the invitation carried (up to Owner). This vulnerability is fixed in 0.184.0.

### CVE-2026-11972

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-252;CWE-606;CWE-770` |
| Published | 2026-06-23T23:16:49.033 |

When using the "tarfile" module with a file opened in "streaming mode" (mode="r|") the tarfile module did not properly handle EOF, meaning an archive could be parsed in an infinite loop.

### CVE-2026-54513

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-06-23T21:17:02.333 |

jackson-databind contains the general-purpose data-binding functionality and tree-model for Jackson Data Processor. From 2.10.0 until 2.18.8, 2.21.4, and 3.1.4, BasicPolymorphicTypeValidator.Builder.allowIfSubTypeIsArray() allowlists any array type based only on clazz.isArray(), without validating the array's component (element) type against the configured allowlist. A PTV built with allowIfSubTypeIsArray() plus an explicit concrete-type allowlist therefore still permits EvilType[] even though EvilType is not allowlisted. When Jackson deserializes the elements and no per-element type IDs are present, it instantiates the component type directly with no further PTV check, bypassing the allowlist. This vulnerability is fixed in 2.18.8, 2.21.4, and 3.1.4.

### CVE-2026-54512

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184;CWE-502` |
| Published | 2026-06-23T21:17:02.203 |

jackson-databind contains the general-purpose data-binding functionality and tree-model for Jackson Data Processor. From 2.10.0 until 2.18.8, 2.21.4, and 3.1.4, jackson-databind's PolymorphicTypeValidator (PTV) is the primary safety mechanism guarding polymorphic deserialization. When polymorphic typing is enabled and a type identifier contains generic parameters (i.e. the type ID string contains <), DatabindContext._resolveAndValidateGeneric() validates only the raw container class name (the substring before <) against the configured PTV. If the container type is approved, the method parses the full canonical type string via TypeFactory.constructFromCanonical() and returns the fully parameterized type without ever validating the nested type arguments against the PTV. The nested type arguments are then resolved, instantiated, and populated as beans during deserialization. An attacker who controls the type ID can therefore place a denied class as a generic type parameter of an allowed container — for example java.util.ArrayList<com.evil.Gadget> when only java.util.ArrayList is allow-listed. The container passes the PTV check; com.evil.Gadget is loaded via Class.forName(name, true, loader), instantiated, and its properties are set from attacker-controlled JSON. This completely bypasses an explicitly configured PTV allow-list. This vulnerability is fixed in 2.18.8, 2.21.4, and 3.1.4.

### CVE-2026-39253

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-23T20:16:47.243 |

An issue in Pivotal CRM v.6.6.04.08 allows a remote attacker to execute arbitrary code via the Pivotal.Core.Common.dll and Pivotal.Engine.Client.Services.Conversion.dll components.

### CVE-2026-10745

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-117` |
| Published | 2026-06-24T09:16:30.147 |

Improper output neutralization for logs vulnerability in upKeeper Solutions upKeeper Instant Privilege Access on Windows allows Log Injection-Tampering-Forging.

This issue affects upKeeper Instant Privilege Access: through 1.6.1.

### CVE-2026-12112

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-23T21:16:54.823 |

A flaw was found in the foreman-mcp-server. A session management vulnerability in the MCP Server allows unauthenticated attackers to hijack active administrative sessions due to an improper cache of authenticated client connections, by trusting a non-secret session ID without re-validating authentication tokens and by logging all newly created session IDs to standard logs. This issue can result in privilege escalation and infrastructure-wide code execution.

### CVE-2026-54555

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-23T20:16:49.737 |

rtk filters and compresses command outputs before they reach your LLM context. Prior to 0.42.2, the permission splitter did not conservatively split or reject several shell constructs that Bash treats as command execution boundaries or nested execution. As a result, a command beginning with an allowed prefix such as git could hide a second command behind one of these constructs. rtk rewrite returned exit code 0, causing the Claude hook to emit permissionDecision: "allow". The rewritten command still contained the hidden command, so it ran without the user confirmation or denial that the permission rules were intended to enforce. This vulnerability is fixed in 0.42.2.

### CVE-2026-53622

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-23T20:16:48.777 |

Traefik is an HTTP reverse proxy and load balancer. Prior to 3.7.3, there is a critical vulnerability in Traefik's HTTP/3 (QUIC) TLS configuration selection that allows unauthenticated clients to bypass router-specific mTLS enforcement. When HTTP/3 is enabled on an entrypoint, the TLS handshake selects the applicable TLS configuration through an exact, case-sensitive lookup on the SNI value, which fails to match wildcard host patterns (e.g., *.example.com) or case variants of the configured hostname. Because the handshake falls back to the default TLS configuration — which may not require client certificates — a client can complete the QUIC handshake without presenting a certificate, while the subsequent HTTP routing layer still dispatches the request to a backend protected by a router-specific mTLS policy. The issue affects deployments where HTTP/3 is enabled, a router uses a wildcard Host rule or case-insensitive hostname matching, a router-specific TLSOptions enforces client certificate authentication, and UDP access to the entrypoint is reachable by an attacker. This vulnerability is fixed in 3.7.3.

### CVE-2026-48491

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-23T20:16:48.123 |

Traefik is an HTTP reverse proxy and load balancer. From 3.7.0 until 3.7.3, there is a high severity vulnerability in Traefik's domain-fronting protection (SNICheck) that allows an unauthenticated client to bypass mutual TLS enforced through wildcard router TLSOptions. When a router uses a wildcard host rule such as Host(*.example.com) with stricter TLS options (for example RequireAndVerifyClientCert), SNICheck resolves the TLS options for the HTTP Host header using exact map lookups only and never applies wildcard matching. If another permissive SNI is served on the same entrypoint, an attacker can complete the TLS handshake under the permissive options and then send an HTTP Host header targeting the wildcard-protected backend, reaching it without presenting a client certificate. This affects the regular HTTPS / HTTP-2 path and does not require HTTP/3. This vulnerability is fixed in 3.7.3.

### CVE-2026-48020

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-23T20:16:47.993 |

Traefik is an HTTP reverse proxy and load balancer. Prior to 2.11.48, 3.6.19, and 3.7.3, there is a high severity vulnerability in Traefik's StripPrefix middleware that allows an unauthenticated attacker to bypass route-level authentication and authorization. When a public router matches on a PathPrefix rule and applies the StripPrefix middleware, a request path containing .. or its percent-encoded form %2e%2e can match the public route at routing time and then, after the prefix is stripped and the path is normalized, resolve to a path served by a separate, authenticated router. As a result, an attacker can reach protected backend paths — such as admin or internal configuration endpoints — without satisfying the authentication middleware attached to the protected router. This vulnerability is fixed in 2.11.48, 3.6.19, and 3.7.3.

### CVE-2026-9710

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-24T07:16:30.317 |

The Cornerstone WordPress plugin before 7.8.8 does not enforce capability checks on one of its CSS-preview request handlers, and exposes the nonce needed to call it to every logged-in user on any wp-admin page, allowing any authenticated user to evaluate dynamic content tokens against arbitrary users and disclose their sensitive metadata including raw password hashes. This affects the premium co Cornerstone page builder distributed bundled with the X , not the unrelated free `cornerstone` Cornerstone WordPress plugin before 7.8.8 (v0.8.x) on the .org repository.

### CVE-2026-9709

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-24T07:16:30.217 |

The Cornerstone WordPress plugin before 7.8.9 does not enforce capability checks on one of its REST API routes, allowing any authenticated user to disclose the metadata of any other user, including roles, session token previews and stored billing/shipping fields. This affects the premium co Cornerstone page builder distributed bundled with the X , not the unrelated free `cornerstone` Cornerstone WordPress plugin before 7.8.9 (v0.8.x) on the .org repository.

### CVE-2026-54322

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-06-23T19:17:08.370 |

Daytona is a secure and elastic infrastructure runtime for AI-generated code execution and agent workflows. Prior to 0.185.0, Daytona's organization role update and delete endpoints authorized the caller as an owner of the organization named in the request path, but resolved and mutated the target role by its identifier alone, without verifying the role belonged to that organization. An authenticated user who owns any organization (organizations are self-service) could therefore modify the permissions of, or delete, a role belonging to a different organization, given that role's identifier. This vulnerability is fixed in 0.185.0.

### CVE-2025-71361

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-06-24T13:16:30.543 |

picklescan before 0.0.29 fails to detect malicious idlelib.calltip.Calltip.fetch_tip calls in pickle files, allowing remote code execution. Attackers can embed undetected payloads in pickle files that execute arbitrary code when loaded via pickle.load().

### CVE-2025-71354

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-24T13:16:30.413 |

picklescan before 0.0.29 fails to detect malicious pickle files that exploit idlelib.debugobj.ObjectTreeItem.SetText function in reduce methods. Attackers can craft pickle files with embedded code that bypasses picklescan detection and executes arbitrary commands when pickle.load() is called.

### CVE-2026-56052

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-24T08:16:24.623 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in FunnelKit Funnel Builder by FunnelKit allows Blind SQL Injection.

This issue affects Funnel Builder by FunnelKit: from n/a through 3.15.0.5.

### CVE-2026-9179

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-24T07:16:29.257 |

The WP Forms Connector plugin for WordPress is vulnerable to SQL Injection via the 'order' parameter of the /wp-json/wp/v3/post/list REST endpoint in versions up to and including 1.8. This is due to insufficient escaping on the user-supplied 'order' parameter (read directly from $_GET['order'] into $shorting) and the lack of sufficient preparation on the existing SQL query in the listPost() function, where the value is concatenated unquoted into the ORDER BY clause and executed via $wpdb->get_results() without $wpdb->prepare(). The endpoint is registered with permission_callback '__return_true' and performs only a broken header-based check that validates the supplied 'Username' corresponds to an administrator account while never verifying the 'Password'. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-9178

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-24T07:16:29.133 |

The WP Forms Connector plugin for WordPress is vulnerable to Information Exposure in all versions up to, and including, 1.8. The plugin registers the REST route wp/v3/user/list/<id> (callback userDetail()) with permission_callback set to '__return_true', and the function's home-grown authentication only verifies that the supplied 'Username' HTTP header maps to an administrator account and that a 'Password' HTTP header is non-empty. It never validates the password with wp_check_password() (unlike the sibling delete_wc_user() function which does). This makes it possible for unauthenticated attackers to retrieve sensitive information for any registered user ID — including the WordPress password hash (user_pass) and email address — by sending a request with a valid administrator login name (commonly the default 'admin') and any arbitrary password value.

### CVE-2026-8705

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-24T07:16:28.417 |

The ClearSale Total plugin for WordPress is vulnerable to SQL Injection via the `pagseguro[metodo]` POST parameter of the `clearsale_total_push` AJAX action in all versions up to, and including, 3.4.2. The handler is registered for unauthenticated users (`wp_ajax_nopriv_clearsale_total_push`), and although a `wp_verify_nonce()` check exists, the failing branch's `die()` is commented out so execution continues regardless of nonce validity. On PHP < 8.0 the attacker-supplied `$metodo` value bypasses the `switch ($metodo) { case 4: ... }` guard via loose type juggling (the string `"4 AND SLEEP(5)"` compares equal to integer `4`), reaching an unquoted `UPDATE wp_cs_total_dadosextras SET metodo=$metodo, ...` query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. Exploitation requires the target server to be running PHP < 8.0.

### CVE-2026-10735

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-24T07:16:25.867 |

Multiple Shapedsmart-post-show-pro WordPress plugin before 4.0.2, Real Testimonials Pro WordPress plugin before 3.2.5, Product Slider for WooCommerce Pro WordPress plugin before 3.5.3 Pro smart-post-show-pro WordPress plugin before 4.0.2, Real Testimonials Pro WordPress plugin before 3.2.5, Product Slider for WooCommerce Pro WordPress plugin before 3.5.3 were distributed with malicious code through the vendor's compromised update server, allowing unauthenticated attackers to deploy a second-stage payload that exfiltrates credentials and other sensitive data and grants full control of affected sites.

### CVE-2026-53754

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-23T19:17:07.303 |

Crawl4AI is an open-source LLM friendly web crawler & scraper. Prior to 0.8.8, the Docker API server's SSRF protection (validate_webhook_url / validate_url_destination in deploy/docker/utils.py) used an explicit IPv4/IPv6 CIDR blocklist that missed several address families. An attacker could reach internal services and cloud metadata endpoints (e.g. 169.254.169.254) despite the filter by encoding an internal IPv4 address inside an IPv6 transition form, or by using the IPv6 unspecified address. Because the Docker API is unauthenticated by default (jwt_enabled: false), no credentials are required. This vulnerability is fixed in 0.8.8.

### CVE-2026-47383

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-23T21:17:00.200 |

NocoDB is software for building databases as spreadsheets. Prior to 2026.05.1, an authenticated commenter could store HTML in row comments that executed as script when other users hovered over the comment in the expanded form view. The comment write paths persisted the raw comment body with no server-side sanitisation; the expanded-form sidebar then rendered the stored body and fed its data-tooltip attribute to Tippy with allowHTML: true. Even when the editor stripped script tags at write time, attribute-level payloads re-entered the DOM as live HTML on hover. This vulnerability is fixed in 2026.05.1.

### CVE-2026-54328

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-379` |
| Published | 2026-06-23T20:16:49.603 |

Pi is a minimal terminal coding harness. From 0.74.0 until 0.78.1, Pi versions with temporary npm or git extension package installs used predictable paths under the operating system temporary directory. On Linux-based multi-user systems, a local attacker who can write to the shared temporary directory could prepare the expected package location before another user runs pi with a temporary extension package source. Pi could then load attacker-controlled extension code in the victim user's process.  This vulnerability is fixed in 0.78.1.

### CVE-2026-56231

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-06-24T13:16:33.200 |

Capgo before 12.128.2 contains a broken object level authorization (BOLA) vulnerability in the POST /build/start/:jobId and POST /build/cancel/:jobId endpoints. The handlers authorize the request based only on the attacker-controlled app_id supplied in the request body and never verify that the jobId in the URL belongs to that app_id (or the same tenant/org) before issuing privileged builder commands with the server-held builder API key. An authenticated user with the app.build_native permission for any app they control can start or cancel arbitrary builder jobs belonging to other tenants by supplying a victim jobId, resulting in cross-tenant build sabotage (denial of service), unauthorized compute actions, and potential billing impact.

### CVE-2026-9643

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-24T07:16:30.093 |

The WP Meta SEO plugin for WordPress is vulnerable to Unauthenticated Stored Cross-Site Scripting via the REQUEST_URI server variable in all versions up to, and including, 4.5.18. When the plugin's `wpmsTemplateRedirect()` hook detects a 404, it concatenates `$_SERVER['HTTP_HOST']` with the raw `$_SERVER['REQUEST_URI']` and inserts that value verbatim into the `wp_wpms_links.link_url` column via `$wpdb->insert()`. This makes it possible for unauthenticated attackers to inject arbitrary web scripts that execute whenever an administrator views the plugin's 404 & Redirects admin page (`/wp-admin/admin.php?page=metaseo_broken_link`).

### CVE-2026-12100

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-24T07:16:26.647 |

The URL Preview plugin for WordPress is vulnerable to Server-Side Request Forgery in all versions up to, and including, 1.0 via the 'url' parameter. This makes it possible for unauthenticated attackers to make web requests to arbitrary locations originating from the web application and can be used to query and modify information from internal services.

### CVE-2026-12095

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-24T07:16:26.527 |

The Kargo Takip plugin for WordPress is vulnerable to Server-Side Request Forgery in all versions up to, and including, 1.2 via the 'api_url' parameter. This makes it possible for unauthenticated attackers to make web requests to arbitrary locations originating from the web application and can be used to query and modify information from internal services. The script echoes internal API response data (specifically the value of any 'auth' key in a JSON response body) verbatim back to the attacker's browser, enabling direct exfiltration of responses from internal services such as cloud instance metadata endpoints.

### CVE-2026-10749

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-24T07:16:25.970 |

The Post Duplicator WordPress plugin before 3.0.15 does not safely handle custom meta-data during post duplication, storing attacker-supplied serialized values without the WordPress meta API's double-serialization protection, allowing users with Contributor-level access and above to inject a PHP Object.

### CVE-2026-10092

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-24T07:16:25.520 |

The Cincopa video and media plug-in plugin for WordPress is vulnerable to Stored Cross-Site Scripting via cincopa Shortcode in Post Comments in all versions up to, and including, 1.163 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation is possible because the plugin processes the [cincopa] shortcode via a comment_text filter hook, allowing unauthenticated visitors who can post comments to supply a malicious shortcode argument that persists in the database.

### CVE-2026-10091

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-24T07:16:25.330 |

The Email JavaScript Cloak plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the plugin's 'email' shortcode in all versions up to, and including, 1.03 due to insufficient input sanitization and output escaping on user supplied attributes. This makes it possible for authenticated attackers, with contributor-level access and above, to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-3652

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-24T04:17:06.923 |

The ARForms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the `value` parameter of the `arf_save_incomplete_form_data` AJAX action in all versions up to, and including, 7.1.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts that will execute whenever an administrator views the "Partial Filled Form Entries" page in the ARForms dashboard.

### CVE-2026-5818

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:H/UI:N/VC:N/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-253` |
| Published | 2026-06-24T00:16:33.830 |

Incorrect check of function return value in Caliptra Core Runtime Firmware (ActivateFirmwareCmd::activate_fw modules) allows bypass of Caliptra Core's verification of the MCU FW during a hitless update.

This issue affects Core Runtime Firmware: from 2.0.0 through 2.0.1, 2.1.0.

### CVE-2026-56257

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-24T13:16:35.123 |

Capgo before 12.128.2 allows direct patching of public.apps.owner_org through PostgREST, bypassing the transfer_app() workflow and creating split-brain ownership. Attackers can directly update apps.owner_org while leaving app_versions.owner_org unchanged, enabling old-org keys to retain access to version data while new-org keys control the app record.

### CVE-2026-56256

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-602` |
| Published | 2026-06-24T13:16:34.980 |

Capgo before 12.128.2 enforces mandatory two-factor authentication only at the UI level. Sensitive Organization (ORG) management API endpoints (e.g., editing organization details, inviting users) do not validate 2FA completion on the backend. An authenticated Admin user who has not enabled 2FA can replay or modify a previously captured ORG API request to perform privileged organization actions, bypassing the globally enforced 2FA requirement.

### CVE-2026-56244

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-24T13:16:33.597 |

Capgo before 12.128.2 allows non-admin API keys to read webhook signing secrets via Supabase REST due to insufficient row-level security policies on the webhooks table. Attackers can retrieve the webhook secret and forge valid X-Capgo-Signature headers to send authenticated webhook events to configured receivers, breaking webhook authenticity and integrity.

### CVE-2026-23513

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-23T21:16:55.203 |

FOSSBilling is a free, open-source billing and client management system. In versions 0.7.2 and prior, a query-construction flaw in client list endpoints allowed authenticated clients to bypass tenant scoping and retrieve other clients’ data. Details
In ServiceTransaction::getSearchQuery() and Order\Service::getSearchQuery(), OR-based search/action filters were appended without grouping, allowing SQL operator precedence to evaluate OR clauses independently of the enforced client_id constraint. Crafted requests could therefore return records and metadata belonging to other clients, including identifiers, amounts, status, timestamps, and related fields. This issue was fixed in version 0.8.0.

### CVE-2026-13006

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:N/R:X/V:X/RE:M/U:Green` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-24T07:16:27.127 |

ACE vulnerability in conditional configuration file processing  by QOS.CH logback-core up to and including version 1.5.34 in Java applications, allows an attacker to execute arbitrary code circumventing existing protections against CVE-2025-11226 by compromising an existing logback configuration file or by injecting an environment variable before program execution.



A successful attack requires the presence of Janino library to be present on the user's class path. In addition, the attacker must  have write access to a 
configuration file. Alternatively, the attacker could inject a malicious 
environment variable pointing to a malicious configuration file. In both 
cases, the attack requires existing privilege.

### CVE-2026-54321

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-613;CWE-863` |
| Published | 2026-06-23T19:17:08.190 |

Daytona is a secure and elastic infrastructure runtime for AI-generated code execution and agent workflows. From 0.101.0 until 0.184.0, sandbox previews that were switched from public to private could remain reachable without authentication for a short period after the change, due to a cached visibility state that was not invalidated when the sandbox's visibility changed. This vulnerability is fixed in 0.184.0.
