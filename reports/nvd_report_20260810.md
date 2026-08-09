# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-09 15:00 UTC
- **対象期間**: `2026-08-08T15:00:31.000Z` 〜 `2026-08-09T15:00:17.000Z`
- **重要CVE数**: 31 件（Critical 9.0+: 26 件 / High 7.0〜: 5 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上の深刻度が集中**しているのは **組み込み系ネットワーク機器（ルータ・Wi‑Fi リピータ）** と **Web アプリ／デスクトップアプリ** の 2 カテゴリです。  
- ルータ／リピータ系は **コマンドインジェクション** が多数報告され、攻撃者は認証なしでルート権限取得が可能です。  
- ソフトウェア側は **ヒープバッファオーバーフロー**（GIMP DDS パーサ）や **パストラバーサル**（lollms）といった、リモートコード実行や情報漏洩につながる欠陥が目立ちます。  
- 多くの脆弱性は同一ファームウェアバージョンに集中しているため、**一括アップデートで多数のリスクを除去**できる点が特徴です。

---

## 2. 特に注目すべき CVE  

| CVE | 製品・バージョン | 主な脆弱性種別 | 影響範囲・リスク | 注目理由 |
|-----|------------------|----------------|-------------------|----------|
| **CVE‑2026‑71993** | MSI Radix AXE6600  fw v781521 | コマンドインジェクション（openvpn 関数） | リモートから任意コマンド実行 → ルート権限取得。管理画面へのアクセス不要。 | 同ファームウェアに **10 以上の類似脆弱性** が埋め込まれている代表例。1 件の修正で多数のリスクを緩和できる。 |
| **CVE‑2026‑71958** | D‑Link DWR‑M961  fw 1.1.2_C1_202602110044 | バッファオーバーフロー（quicksetup.cgi） | 任意コード実行（root）。Web UI から直接攻撃可能。 | D‑Link 製品は **多数の CGI に同様のコマンドインジェクション** が報告されており、最も古いバージョンが対象。 |
| **CVE‑2026‑19348** | Shenzhen Aitemi M300 Repeater r0‑ea7890a | コマンドインジェクション（sprintf での format string） | 任意コマンド実行 → LAN 内全デバイスへの踏み台化。 | 小規模オフィス・家庭向けデバイスで、ファームウェア更新が滞りがち。 |
| **CVE‑2026‑42170** | GIMP 2.10.x（DDS プラグイン） | ヒープベースバッファオーバーフロー | 悪意ある DDS 画像を開くと任意コード実行。デスクトップ環境全体が危険に晒される。 | デスクトップユーザーだけでなく、サーバー側で画像処理を行う自動化パイプラインでも影響。 |
| **CVE‑2026‑10595** | lollms 2.1.0（Python） | パストラバーサル（`backend/routers/ui.py`） | 任意ファイル読み取り・書き換えが可能。機密情報漏洩やバックドア設置に利用できる。 | オープンソース AI チャットボットは多くの組織で内部ツールとして導入されており、**即時パッチ適用が必須**。 |

> **共通点**：すべて「リモートから認証不要でコード実行」または「任意ファイル操作」が可能で、**攻撃成功時の影響は機密情報漏洩から完全なシステム乗っ取りまで**広がります。  

---

## 3. 推奨アクション  

### 3‑1. ファームウェア・ソフトウェアの緊急アップデート
| 製品 | 現行脆弱バージョン | 推奨バージョン / パッケージ | アップデート手順のポイント |
|------|-------------------|----------------------------|----------------------------|
| **MSI Radix AXE6600** | v781521 | **v781522 以降**（MSI 公開のセキュリティパッチ） | - 管理画面 → 「ファームウェアアップデート」から手動適用<br>- アップデート後、`openvpn`, `macfilter`, `telnetssh` など全機能の動作確認 |
| **D‑Link DWR‑M961** | 1.1.2_C1_202602110044 | **1.1.5_C1_202607071108** 以上 | - D‑Link の公式サイトから「Firmware Upgrade」パッケージを取得<br>- Web UI → 「System → Firmware Upgrade」へアップロード<br>- アップデート完了後、`quicksetup.cgi` など全 CGI のレスポンスをテスト |
| **Aitemi M300 Repeater** | r0‑ea7890a | **r0‑ea7890b 以降**（2026‑07‑xx リリース） | - デバイスの管理画面で「Upgrade Firmware」ボタンを使用<br>- アップデート前に設定バックアップを取得 |
| **GIMP** | 2.10.0 〜 2.10.38 | **2.10.38 以降**（公式リポジトリ） | - Linux: `sudo apt-get update && sudo apt-get install gimp`（リポジトリが新しい場合）<br>- Windows/macOS: GIMP 公式サイトから最新版インストーラをダウンロード |
| **lollms** | 2.1.0 | **2.1.1 以降**（PyPI） | - `pip install --upgrade lollms` <br>- 依存パッケージ (`fastapi`, `uvicorn`) も同時に最新化 |
| **Tenda CH22** | 1.0.0.1 | **1.0.0.2 以降**（Tenda 公開） | - Web UI → 「Upgrade」からファームウェアを適用<br>- `formCertListInfo` のパラメータ送信テストでエラーが出ないことを確認 |

### 3‑2. 追加的な防御策
- **ネットワーク分離**：ルータ・リピータは管理 VLAN とユーザ VLAN を分離し、管理インタフェースへの外部アクセスを遮断。  
- **Web アプリケーションファイアウォール (WAF)**：`/boafrm/*` や `*.cgi` へのリクエストで **入力長チェック**・**正規表現フィルタ** を有効化。  
- **最小権限

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-71993

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-09T00:16:48.550 |

MSI Radix AXE6600 router firmware version v781521 contains a command injection vulnerability in the openvpn function that allows remote attackers to execute arbitrary commands on the affected device. Attackers can exploit the macfilter function to inject malicious commands and obtain root privileges on the underlying system.

### CVE-2026-71992

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-09T00:16:48.410 |

MSI Radix AXE6600 router firmware version v781521 contains a command injection vulnerability in the macfilter function that allows remote attackers to execute arbitrary commands on the affected device. Attackers can exploit the macfilter function to inject malicious commands and obtain root privileges on the underlying system.

### CVE-2026-71991

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-09T00:16:48.270 |

MSI Radix AXE6600 router firmware version v781521 contains a command injection vulnerability in the TelnetSSH function used for Telnet configuration that allows remote attackers to execute arbitrary commands on the affected device. Attackers can exploit this vulnerability through the Telnet configuration interface to inject malicious commands and obtain root privileges on the underlying system.

### CVE-2026-71990

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-09T00:16:48.130 |

MSI Radix AXE6600 router firmware version v781521 contains a command injection vulnerability in the TelnetSSH function used for SSH configuration that allows remote attackers to execute arbitrary commands on the affected device. Attackers can exploit this vulnerability through the SSH configuration interface to inject malicious commands and obtain root privileges on the underlying system.

### CVE-2026-71989

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-09T00:16:47.953 |

MSI Radix AXE6600 router firmware version v781521 contains a command injection vulnerability in the porTrigger function that allows remote attackers to execute arbitrary commands on the affected device. Attackers can exploit this vulnerability through the alg function to execute malicious commands and obtain root privileges on the underlying system.

### CVE-2026-71988

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-09T00:16:47.780 |

MSI Radix AXE6600 router firmware version v781521 contains a command injection vulnerability in the portFw function that allows remote attackers to execute arbitrary commands on the affected device. Attackers can exploit this vulnerability through the alg function to execute malicious commands and obtain root privileges on the underlying system.

### CVE-2026-71987

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-09T00:16:47.637 |

MSI Radix AXE6600 router firmware version v781521 contains a command injection vulnerability in the alg function that allows remote attackers to execute arbitrary commands on the affected device. Attackers can exploit this vulnerability through the alg function to execute malicious commands and obtain root privileges on the underlying system.

### CVE-2026-71986

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-09T00:16:47.500 |

MSI Radix AXE6600 router firmware version v781521 contains a command injection vulnerability in the dmz function that allows remote attackers to execute arbitrary commands on the affected device. Attackers can exploit this vulnerability through the dmz function to execute malicious commands and obtain root privileges on the underlying system.

### CVE-2026-71985

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-09T00:16:47.360 |

MSI Radix AXE6600 router firmware version v781521 contains a command injection vulnerability in the accesscontrol function that allows remote attackers to execute arbitrary commands on the affected device. Attackers can exploit this vulnerability through the accesscontrol function to execute malicious commands and obtain root privileges on the underlying system.

### CVE-2026-71984

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-09T00:16:47.207 |

MSI Radix AXE6600 router firmware version v781521 contains a command injection vulnerability in the urlfilter function that allows remote attackers to execute arbitrary commands on the affected device. Attackers can exploit the urlfilter function to inject malicious commands and obtain root privileges on the underlying system.

### CVE-2026-71983

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T23:16:56.967 |

MSI Radix AXE6600 router firmware version v781521 contains a command injection vulnerability in the wps.cgi interface that allows remote attackers to execute arbitrary commands by injecting malicious input through the pin2g, pin5g, or pin6g parameters. Attackers can exploit these unsanitized parameters to execute arbitrary commands on the affected device and obtain root privileges.

### CVE-2026-71958

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-08T18:16:56.783 |

D-Link DWR-M961 devices with hardware version C1 and software version 1.1.2_C1_202602110044 contain a buffer overflow vulnerability in the quicksetup.cgi interface. A remote attacker can write overly long strings to the test4, ssid2, and username fields and execute arbitrary commands by crafting a specific payload, or cause the device to crash.

### CVE-2026-71957

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-08T18:16:56.647 |

D-Link DWR-M961 devices with hardware version C1 and software version 1.1.2_C1_202602110044 contain a buffer overflow vulnerability in the app.cgi interface. A remote attacker can write an overly long string to the netAcc.addlist[].name field and execute arbitrary commands by crafting a specific payload, or cause the device to crash.

### CVE-2026-71956

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T18:16:56.503 |

D-Link DWR-M961 devices with hardware version C1 and software version 1.1.2_C1_202602110044 contain a command injection vulnerability in the app.cgi interface. A remote attacker can inject arbitrary malicious commands into the netDig.ping.dst field, resulting in command execution with root privileges.

### CVE-2026-71955

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:49.250 |

D-Link DWR-M961 devices with hardware version C1 and software version 1.1.2_C1_202602110044 contain a command injection vulnerability in the /boafrm/formWsc interface. A remote attacker can inject arbitrary malicious commands into the localPin, targetAPSsid, peerPin, and peerRptPin fields, resulting in command execution with root privileges.

### CVE-2026-71954

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:49.097 |

D-Link DWR-M961 devices with hardware version C1 and firmware version before 1.1.5_C1_202607071108 contain a command injection vulnerability in the /boafrm/formL2tpv3ConfigSetup interface. A remote attacker can inject arbitrary malicious commands into the tunnelid and sessionid fields, resulting in command execution with root privileges.

### CVE-2026-71953

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:48.890 |

D-Link DWR-M961 devices with hardware version C1 and firmware version before 1.1.5_C1_202607071108 contain a command injection vulnerability in the /boafrm/formNtp interface. A remote attacker can inject arbitrary malicious commands into the ntpServerIp1 field, resulting in command execution with root privileges.

### CVE-2026-71952

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:48.733 |

D-Link DWR-M961 devices with hardware version C1 and firmware version before 1.1.5_C1_202607071108 contain a command injection vulnerability in the /boafrm/formPinManageSetup interface. A remote attacker can inject arbitrary malicious commands into the oldPIn field, resulting in command execution with root privileges.

### CVE-2026-71951

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:48.570 |

D-Link DWR-M961 devices with hardware version C1 and firmware version before 1.1.5_C1_202607071108 contain a command injection vulnerability in the /boafrm/formIMEISetup interface. A remote attacker can inject arbitrary malicious commands into the IMEI_value field, resulting in command execution with root privileges.

### CVE-2026-71950

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:48.413 |

D-Link DWR-M961 devices with hardware version C1 and firmware version before 1.1.5_C1_202607071108 contain a command injection vulnerability in the /boafrm/formSmsManage interface. A remote attacker can inject arbitrary malicious commands into the action_value field, resulting in command execution with root privileges.

### CVE-2026-71949

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:48.267 |

D-Link DWR-M961 devices with hardware version C1 and firmware version before 1.1.5_C1_202607071108 contain a command injection vulnerability in the /boafrm/formUSSDSetup interface. A remote attacker can inject arbitrary malicious commands into the ussdValue and selectMenuValue fields, resulting in command execution with root privileges.

### CVE-2026-71948

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:48.127 |

D-Link DWR-M961 devices with hardware version C1 and firmware version before 1.1.5_C1_202607071108 contain a command injection vulnerability in the /boafrm/formDebugDiagnosticRun interface. A remote attacker can inject arbitrary malicious commands into the host field, resulting in command execution with root privileges.

### CVE-2026-71947

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:47.983 |

D-Link DWR-M961 devices with hardware version C1 and firmware version before 1.1.5_C1_202607071108 contain a command injection vulnerability in the /boafrm/formTracerouteDiagnosticRun interface. A remote attacker can inject arbitrary malicious commands into the host and ipVer fields, resulting in command execution with root privileges.

### CVE-2026-71946

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:47.847 |

D-Link DWR-M961 devices with hardware version C1 and firmware version before 1.1.5_C1_202607071108 contain a command injection vulnerability in the /boafrm/formPingDiagnosticRun interface. A remote attacker can inject arbitrary malicious commands into the host field, resulting in command execution with root privileges.

### CVE-2026-71945

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:47.710 |

D-Link DWR-M961 devices with hardware version C1 and firmware version before 1.1.5_C1_202607071108 contain a command injection vulnerability in the /boafrm/formLtefotaUpgradeFibocom interface. A remote attacker can inject arbitrary malicious commands into the fota_url field, resulting in command execution with root privileges.

### CVE-2026-71944

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-08T17:16:47.550 |

D-Link DWR-M961 devices with hardware version C1 and firmware version before 1.1.5_C1_202607071108 contain a command injection vulnerability in the /boafrm/formLtefotaUpgradeQuectel interface. A remote attacker can inject arbitrary malicious commands into the fota_url field, resulting in command execution with root privileges.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-19348

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-09T11:16:52.743 |

A security flaw has been discovered in Shenzhen Aitemi M300 Wi-Fi Repeater r0-ea7890a. Impacted is the function sprintf of the file /protocol.csp?fname=net&opt=smacfilter_conf&function=set&act=add&name=test&enable=1. Performing a manipulation of the argument enable/name/mac results in command injection. The attack may be initiated remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-42170

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-131` |
| Published | 2026-08-08T16:16:49.093 |

A heap-based buffer overflow vulnerability exists in the GIMP DDS (DirectDraw Surface) file parser. When a crafted DDS file declares a D3D9 pixel format but sets a lower bits-per-pixel (bpp) value in the header, the loader allocates an undersized heap buffer. Subsequent pixel data consumption at the real format's stride causes a write past the heap buffer boundary, leading to heap metadata corruption and potential code execution.

### CVE-2026-10595

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-09T04:17:29.400 |

A path traversal vulnerability exists in parisneo/lollms version 2.1.0, specifically in the SPA catch-all route implemented in `backend/routers/ui.py`. The vulnerability arises from the improper handling of user-controlled path input, which is directly joined into a filesystem path without sanitization or containment checks. URL-encoded dot-dot sequences (`%2e%2e`) bypass Starlette's built-in path normalization and are resolved by Python's `pathlib`, allowing an unauthenticated attacker to read arbitrary files on the server. This issue has been resolved in version 3.

### CVE-2026-19346

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-09T10:17:10.567 |

A vulnerability was determined in Tenda CH22 1.0.0.1. This vulnerability affects the function formCertListInfo of the file /goform/CertListInfo. This manipulation of the argument Name causes command injection. The attack can be initiated remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-19341

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-09T07:17:04.373 |

A security vulnerability has been detected in UTT HiPER 1200GW up to 2.5.3-170306. This impacts the function strcpy of the file /goform/pptpSrvGlobalConfig. Such manipulation of the argument EncryptionMode leads to stack-based buffer overflow. The attack can be executed remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.
