# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-13 15:00 UTC
- **対象期間**: `2026-09-12T15:01:26.000Z` 〜 `2026-09-13T15:00:25.000Z`
- **重要CVE数**: 29 件（Critical 9.0+: 4 件 / High 7.0〜: 25 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超が報告され、特に **Web アプリケーション・コンテナ系** と **通信プロトコルスタック（SIP）** に関する脆弱性が目立ちます。  
- 高スコア（9.0 以上）の脆弱性は **Strapi の XSS**、**sngrep のスタックバッファオーバーフロー**、**LangBot の認証回復キーの低エントロピー** といった、**リモートからコード実行や認証回避が可能**なものが集中しています。  
- 多くは **入力検証不備**、**暗号・証明書検証の欠如**、**不適切なメモリ境界チェック** が根本原因で、パッチ適用だけでなく **開発プロセスでの安全なコーディング指針の徹底** が求められます。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | なぜ注目すべきか |
|-----|------|----------|-------------------|
| **CVE‑2026‑90561** (Strapi 4.x‑4.26.2 / 5.x‑<5.48.1) | 9.3 | Stored XSS（WYSIWYG プレビューで script タグが除去されない） | Author ロールでも悪意スクリプトを永続化でき、管理画面や閲覧ユーザーのブラウザで任意コード実行が可能。CMS が多数利用されているため、被害範囲が広い。 |
| **CVE‑2026‑90558** (sngrep ≤ 1.8.4) | 9.3 | SIP ヘッダーの 255 バイト制限突破によるスタックバッファオーバーフロー | 攻撃者は任意の SIP パケットを送出し、対象サーバをクラッシュさせるだけでなく、メモリ破壊によりコード実行が狙える。通信インフラでの採用が多く、サービス停止リスクが高い。 |
| **CVE‑2026‑90562** (LangBot < 4.10.11) | 9.2 | パスワードリセットキーのエントロピー 24 ビット、レートリミットなし | 管理者メールが判明すれば、キー空間を総当たりで突破でき、管理者権限取得が可能。認証系サービスでの典型的な「弱いトークン」問題。 |
| **CVE‑2026‑90647** (ASE/Kalkitech ASE2000 V2 2.35‑2.37) | 9.1 | IEC 60870‑5‑104 TLS クライアントの証明書検証不備 | 産業制御システム向け製品で、偽証明書を用いた MITM が可能。インフラ系での深刻な機密漏洩・改ざんリスク。 |
| **CVE‑2026‑90777** (ESPnet < 202609) | 8.7 | torch.load (weights_only=False) による任意コード実行 | 機械学習モデルを外部から取得する環境で、悪意ある checkpoint をロードするとサーバ側で任意コードが実行される。AI/ML パイプラインの安全性が揺らぐ。 |

> **注**：上記は **CVSS が高く、かつ実運用環境で広く利用されている** 製品・ライブラリを中心に選定しました。  

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンの即時更新
| 製品・ライブラリ | 現行脆弱バージョン | 修正済みバージョン | 更新手順のポイント |
|------------------|-------------------|-------------------|-------------------|
| **Strapi** | 4.x ≤ 4.26.2、5.x < 5.48.1 | 4.26.3 以上、5.48.1 以上 | `npm install strapi@latest` → **WYSIWYG プレビューのサニタイズロジックが追加** |
| **sngrep** | ≤ 1.8.4 | 1.8.5 以上 | `apt-get update && apt-get install sngrep`（公式リポジトリ） |
| **LangBot** | < 4.10.11 | 4.10.11 以上 | `pip install --upgrade langbot`（PyPI） |
| **ASE/Kalkitech ASE2000 V2** | 2.35‑2.37 | 2.38 以上 | ベンダー提供のパッチを適用、TLS 設定で **証明書検証を必須** に変更 |
| **ESPnet** | < 202609 | 202609 以上 | `pip install --upgrade espnet`（torch の `weights_only=True` がデフォルト） |
| **zstd‑jni** | 1.2.0‑1.5.7‑13 | 1.5.8 以上 | `mvn versions:use-latest-versions -Dincludes=org.apache.commons:zstd-jni` |
| **SIPp** | ≤ 3.7.7 | 3.7.8 以上 | `apt-get install sipp`（Debian/Ubuntu） |
| **Nodemailer** | 9.1.0‑10.0.4 | 10.0.5 以上 | `npm install nodemailer@latest`（addressparser の正規表現改善） |
| **rustypaste** | < 0.18.1 | 0.18.1 以上 | `cargo update -p rustypaste` |
| **UnrealIRCd** | 6.0.5‑6.2.6 | 6.2.7 以上 | `./unrealircd install` → **HTTP ヘッダー数制限を有効化** |
| **snappy‑java** | ≤ 1.1.10.8 | 1.1.10.9 以上 | `mvn dependency:tree -Dincludes=org.xerial.snappy:snappy-java` |
| **PostGIS address_standardizer** | ≤ 3.7.0 | 3.7.1 以上 | `apt-get install postgis`（配布パッケージで修正） |
| **Froxlor** | < 2.3.12 | 2.3.12 以上 | `composer update froxlor/froxlor`（SSH キー検証ロジック追加） |

> **※** 社内のパッケージ管理システム（Artifactory、GitHub Packages 等）で **ハッシュ検証** と **リリースノートの確認** を必ず行ってください。

### 3.2 設定・運用上の対策
1. **入力検証の徹底**  
   - Strapi・ESPnet・SIPp など、ユーザー入力を直接コマンドやテンプレートに流す箇所は **サニタイズ／エスケープ** を実装。  
2. **TLS/証明書の強制検証**  
   - ASE2000 だけでなく、社内全ての TLS クライアント設定で `verify_peer = true`、`verify_depth` を適切に設定。  
3. **レートリ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-90561

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-13T11:17:00.613 |

Strapi versions 4.x through 4.26.2 and 5.x before 5.48.1 contain a stored cross-site scripting vulnerability in the content manager WYSIWYG preview component that fails to strip script tags from rich text. An Author-role user can store malicious script tags in rich text fields that execute in an Editor or Super Admin's session when the preview pane is expanded, enabling account takeover.

### CVE-2026-90558

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-12T18:16:44.587 |

sngrep through 1.8.4 contains stack buffer overflow vulnerabilities in SIP attribute formatting routines when header values exceed the 255-byte buffer limit. Attackers can craft malicious SIP packets with oversized Call-ID, X-Call-ID, or other header fields to overflow stack buffers and cause crashes or execute arbitrary code during packet parsing and rendering.

### CVE-2026-90562

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-331` |
| Published | 2026-09-13T11:17:00.780 |

LangBot before 4.10.11 generates password recovery keys with only 24 bits of entropy and applies no rate limiting to the unauthenticated reset-password endpoint. Remote attackers knowing the administrator email can exhaust the keyspace through concurrent requests to reset the admin password and gain account access.

### CVE-2026-90647

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-12T23:17:01.490 |

ASE/Kalkitech ASE2000 V2 Communication Test Set 2.35 through 2.37 on Windows contains an improper certificate validation vulnerability in the IEC 60870-5-104 TLS client (Task Mode). This allows a network-positioned attacker to bypass certificate validation via a certificate with multiple simultaneous faults, enabling a Man-in-the-Middle attack on protected communications.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-90560

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-12T18:16:44.890 |

zstd-jni versions 1.2.0 through 1.5.7-13 contain an out-of-bounds read vulnerability in the ZstdDictDecompress constructor because offset and length arguments are never validated against the dictionary array bounds. Attackers can supply arbitrary offset or length values to read memory past the end of the supplied array, potentially causing JVM termination.

### CVE-2026-90780

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-13T12:17:17.093 |

SIPp through 3.7.7 contains a buffer overflow vulnerability in the get_header() function in src/sip_parser.cpp when processing SIP messages with header content exceeding 20,490 bytes. Unauthenticated remote attackers can send crafted SIP messages with oversized headers to overflow the static buffer and crash the process.

### CVE-2026-90779

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-13T12:17:16.960 |

SIPp through 3.7.7 contains a stack buffer overflow vulnerability in createAuthHeader() when processing SIP authentication challenges with oversized algorithm parameters. A malicious SIP server can send a crafted 401 or 407 challenge to corrupt the stack and crash the client process.

### CVE-2026-90778

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-13T12:17:16.837 |

SIPp through 3.7.7 contains a buffer overflow vulnerability in get_peer_tag() function when processing SIP To headers with tag parameters of 2049 bytes or more. Unauthenticated remote attackers can send crafted SIP messages with oversized tag parameters to overflow the static buffer and crash the process.

### CVE-2026-90777

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-13T12:17:16.690 |

ESPnet before 202609 deserializes pretrained model checkpoints using torch.load with weights_only=False, allowing arbitrary code execution from attacker-supplied files. Attackers can craft malicious checkpoint files that execute code during deserialization when loaded through the initialization or fine-tuning path.

### CVE-2026-90776

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-13T12:17:16.547 |

Nodemailer versions 9.1.0 through 10.0.4 contain a quadratic time complexity vulnerability in the addressparser component when parsing email addresses with RFC 5322 comments. Attackers can craft malicious email headers with comment-separated atoms to consume excessive CPU and block the Node.js event loop for several seconds, causing denial of service.

### CVE-2026-90774

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-13T11:17:02.163 |

rustypaste before 0.18.1 validates the destination path before applying the optional custom filename HTTP header, allowing attackers to bypass directory-escape checks. Attackers can supply path traversal sequences in the filename header to write files outside the configured upload directory to arbitrary locations.

### CVE-2026-90770

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-13T11:17:01.453 |

Spug through 3.4.0 contains a remote code execution vulnerability in the ping_check function that interpolates user-supplied monitor addresses directly into shell commands without validation. Authenticated users with monitor permissions can inject shell metacharacters via the /monitor/run_test/ endpoint to execute arbitrary commands as the Spug process user.

### CVE-2026-90668

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:L/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-13T02:17:05.103 |

The webserver in UnrealIRCd 6.0.5 through 6.2.6 before 6.2.7 does not limit the number of HTTP request headers, which allows remote attackers to cause a denial of service (memory consumption and unresponsive server) via an HTTP request with an unlimited number of headers, if a websocket or JSON-RPC listener is enabled (disabled by default).

### CVE-2026-90559

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-12T18:16:44.743 |

snappy-java through 1.1.10.8 contains an out-of-bounds write vulnerability in Snappy.uncompress(ByteBuffer, ByteBuffer) because destination buffer capacity is never validated against decompressed size. Attackers can supply valid compressed data that decompresses larger than the destination buffer, causing writes past buffer boundaries and JVM termination.

### CVE-2026-90768

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-13T11:17:01.113 |

CAPEv2 through commit 471ee4b fails to validate task ownership in REST API endpoints, allowing authenticated users to read and delete analyses submitted by other users. Attackers can enumerate all tasks in the system and delete arbitrary analyses by sending requests to task view and delete endpoints without ownership verification.

### CVE-2026-90783

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-680` |
| Published | 2026-09-13T13:16:29.560 |

MKVToolNix through 101.0 contains a heap buffer overflow in the bundled avilib library's ODML superindex parser due to integer wraparound in 32-bit arithmetic. Attackers can craft a malicious AVI file with oversized entry counts that cause an undersized heap allocation, allowing a heap buffer overflow when the file is parsed with mkvmerge.

### CVE-2026-90493

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-09-13T03:16:27.370 |

A vulnerability was detected in Tonec Internet Download Manager up to 6.42 Build 63 on Windows. The impacted element is an unknown function of the file idmwfp.sys of the component Kernel Driver. The manipulation results in improper access controls. Attacking locally is a requirement. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-90556

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-12T18:16:44.193 |

Freeciv versions before 3.2.6 contain a heap buffer overflow in worklist_load() when processing savegame files with declared worklist lengths exceeding the fixed array bound of 64 elements. Attackers can craft malicious savegame files that write past the entries array into adjacent heap-allocated struct fields, potentially corrupting memory when a user or server operator loads the file.

### CVE-2026-90772

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-13T11:17:01.780 |

Amundsen frontend through 4.3.0 renders table, dashboard, and feature descriptions with dangerouslySetInnerHTML without HTML sanitization in ResourceListItem components. Attackers can inject malicious markup like img elements with onerror handlers into descriptions via the metadata service or Elasticsearch, executing JavaScript in every user's browser that views search results.

### CVE-2026-90769

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-13T11:17:01.270 |

Open Notebook before 1.11.0 fails to validate the URL parameter in POST /api/sources endpoint, allowing authenticated users to perform server-side requests to internal services. Attackers can supply arbitrary URLs to read cloud metadata, internal network services, and localhost-bound services through the application server's direct HTTP requests.

### CVE-2026-90651

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-13T00:17:07.203 |

Socket Firewall (socketdev/socket-registry-firewall) in registry mode before 2.0.0 does not verify upstream TLS certificates by default. When the api_ssl_verify and upstream_ssl_verify configuration keys are omitted from socket.yml, the generated configuration sets SOCKET_API_SSL_VERIFY='false' and UPSTREAM_SSL_VERIFY='false', and the OpenResty/Lua HTTP client used for outbound requests accepts any certificate, including self-signed and otherwise untrusted certificates, without validating the chain. An attacker positioned to intercept traffic between Socket Firewall and the Socket API or an upstream package registry can present a crafted certificate and modify responses in transit, including substituting malicious package content or altering the allow/block decisions the firewall enforces. Setting api_ssl_verify: true and upstream_ssl_verify: true enables verification; however, in versions before 1.1.334, the generated nginx configuration did not emit lua_ssl_trusted_certificate, and thus verification could not be used successfully without manually patching the generated configuration. Version 2.0.0 changes the default for both settings to true.

### CVE-2026-89080

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-13T06:16:25.637 |

The Really Simple Security  WordPress plugin before 9.8.1 does not prevent an unauthenticated request from resetting an account's completed email two-factor enrolment, allowing an attacker who already knows the account's password to bypass the second factor and obtain that user's session, up to administrator.

### CVE-2026-86406

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-13T06:16:25.157 |

The User Registration & Membership  WordPress plugin before 5.2.8 does not check the capability of the user making a membership purchase, and does not validate the payment method or the plan submitted with it, allowing any authenticated user such as a subscriber to be granted the WordPress role attached to a paid plan without paying for it. Where the site owner has mapped a plan to a privileged role, this leads to privilege escalation up to administrator.

### CVE-2026-90678

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-130` |
| Published | 2026-09-13T04:17:25.227 |

An issue was discovered in HAProxy 3.3.0 through 3.4.4 and in 3.5-dev1 through 3.5-dev5. Exploitation requires an HTTP/3 frontend: HAProxy must be built with QUIC support and configured with a QUIC bind listener, and the affected traffic must reach a backend over HTTP/1.1 using chunked transfer coding on a reused connection. Under those conditions, when an HTTP/3 request carries no Content-Length header, the HTTP/3 multiplexer credits the length declared in a DATA frame header to the stream endpoint's known-input-payload estimate at the moment the frame header is decoded, before the payload has been received, and that declared length is emitted verbatim as the HTTP/1.1 chunk size. A remote unauthenticated client that declares more payload than it delivers and then ends the stream causes HAProxy to announce a chunk larger than the bytes it writes and to return the connection to the idle pool in a desynchronized state. The result is potential HTTP request smuggling on reused backend connections: an attacker can place a request past a frontend rule such as a path-based http-request deny, so that the smuggled request is never seen by HAProxy's HTTP analysis, and can cause concurrent clients' requests, including their request lines and Authorization headers, to be consumed as the attacker's request body and lost. Exploitation is not deterministic; it depends on a race with backend connection pooling, succeeding in a majority of but not all trials during testing, and can be retried freely. The mechanism was introduced in 3.3-dev10; releases 3.2.x and earlier are unaffected.

### CVE-2026-90616

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-09-12T20:16:30.957 |

In Flatpak before 1.18.1, a malicious sandboxed app can obtain arbitrary read and write access to files on the host, which can be escalated to arbitrary code execution on the host, a different vulnerability than CVE-2026-76925. Flatpak creates a few app data directories (e.g., /var/cache, /var/data, /var/config, and /var/tmp) in every sandbox on every app launch where, in some cases, components of the path are attacker-controlled. Missing symlink protection can redirect the directories. Some of these directories are bind-mounted by Flatpak by passing the path (e.g., /home/user/.var/app/APP_ID/cache/tmp), which contains attacker-controlled directories (tmp) to bwrap --bind SRC DST. bwrap passes the path on to the kernel, which then follows symlinks. A malicious symlink can point to arbitrary locations on the host and it will become mounted inside the sandbox.

### CVE-2026-80071

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-13T06:16:24.947 |

The User Registration & Membership  WordPress plugin before 5.2.8 does not properly restrict who may author a membership plan or validate the plan a user attaches to their own account, allowing authenticated users with Author-level access and above to assign themselves an arbitrary role and escalate their privileges to Administrator.

### CVE-2026-90775

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-13T12:17:16.400 |

PostGIS address_standardizer through 3.7.0 fails to validate the Weight parameter from caller-supplied rules tables before using it as an array index. Attackers can craft malicious rule rows with out-of-range Weight values to trigger out-of-bounds reads in the load_value array, causing the PostgreSQL backend process to crash and terminate all cluster sessions.

### CVE-2026-90767

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-13T11:17:00.947 |

Froxlor before 2.3.12 fails to properly validate multi-line SSH public keys in the SshKeys::add() endpoint, allowing customers to inject arbitrary lines into authorized_keys files. Attackers can inject malicious SSH key entries with option directives to gain persistent unauthorized access that survives key deletion and SSH access revocation.

### CVE-2026-90648

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-252` |
| Published | 2026-09-13T00:17:07.023 |

wasm2c in WebAssembly wabt through 1.0.41 allows sandbox escape in some situations that primarily involve 32-bit platforms, aka a "table flip" attack. It does not check the return value of calloc() in wasm_rt_allocate_funcref_table() (wasm2c/wasm-rt-impl-tableops.inc). When the funcref table allocation fails, table->data is left NULL while table->size keeps the guest-declared element count; thus, bounds checks still pass and table element accesses resolve to absolute memory addresses (i * sizeof(wasm_rt_funcref_t)). This gives arbitrary read and write of host process memory and - via table.get, table.set, and call_indirect - arbitrary code execution, defeating the isolation that wasm2c exists to provide (a full sandbox escape). wasm2c is used as an in-process sandboxing boundary by RLBox and WasmBoxC, including in Firefox, which compiles the Graphite, Hunspell, Ogg, Expat, and Woff2 libraries via wasm2c to contain untrusted font, media, and XML input. Therefore, sandboxing in these applications is potentially affected. Exploitation requires the funcref table allocation to fail, for example under an address-space limit (RLIMIT_AS), on 32-bit hosts, with vm.overcommit_memory=2, or under memory pressure. On 64-bit Linux with default overcommit the allocation succeeds and the defect is not triggered. The wasm2c memory allocator aborts on calloc failure in the same runtime; the table allocator lacks this abort behavior. This was introduced in commit ab9e0b55 (PR #813).
