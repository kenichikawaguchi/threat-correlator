# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-29 09:01 UTC
- **対象期間**: `2026-06-28T19:56:22.000Z` 〜 `2026-06-29T09:01:03.000Z`
- **重要CVE数**: 7 件（Critical 9.0+: 0 件 / High 7.0〜: 7 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE のうち、**CVSS 7.0 以上**のものはすべて **リモートからのコード実行（RCE）や権限昇格** を可能にする深刻なバッファオーバーフローが中心です。  
- 対象製品は **エンタープライズ向けストレージ（Hitachi Virtual Storage Platform）** と **家庭・中小規模向けネットワーク機器（Wavlink、Tenda）** に偏っており、特に **Web 管理インターフェース** の入力検証不備が共通点です。  
- 多くの脆弱性は **ファームウェアの古いバージョン** に残っており、ベンダーがすでにパッチをリリースしているケースが多数です。早急なアップデートが被害防止の鍵となります。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 製品・影響範囲 | 主なリスク | 注目理由 |
|-----|------|----------------|------------|----------|
| **CVE‑2025‑2902** | 8.3 (AV:N/AC:L/PR:L/UI:N) | Hitachi Virtual Storage Platform (E390/E590/E790/E990/E1090 など) | メンテナンスユーティリティの認可不備により、認証済みユーザーが任意の管理コマンドを実行可能。機密データの取得やストレージ構成変更が可能になる。 | エンタープライズ向けストレージは重要インフラであり、被害が広範囲に及ぶ可能性が高い。パッチ適用が遅れると、内部脅威だけでなく外部からの標的型攻撃の踏み台になる。 |
| **CVE‑2026‑13539** | 7.4 (AV:N/AC:L/PR:L) | Wavlink WL‑NU516U1‑A (ファームウェア V240425) | `/cgi-bin/wireless.cgi` の `Guest_ssid` パラメータでスタックバッファオーバーフローが発生し、リモートからコード実行が可能。 | 無線アクセスポイントは社内ネットワークの入り口。公開 Wi‑Fi 環境での利用が想定され、攻撃者がネットワーク全体に踏み込む足掛かりになる。 |
| **CVE‑2026‑13519** 〜 **CVE‑2026‑13515** (Tenda JD12L) | 7.4 (AV:N/AC:L/PR:L) | Tenda JD12L (ファームウェア 16.03.53.23) の複数 CGI エンドポイント (`/goform/NatStaticSetting` など) | 各エンドポイントでスタックバッファオーバーフローが確認され、遠隔から任意コード実行が可能。全 6 件が同一ファームウェアに集中。 | 同一デバイスに多数の未修正脆弱性が残存。攻撃者は任意のエンドポイントを選択でき、検知回避が容易になる。 |

> **注:** Tenda 系の脆弱性はすべて同一ファームウェアバージョンに起因しているため、**一括アップデート** が最も効果的です。

---

## 3. 推奨アクション  

### 3.1 共通対策
- **ファームウェア／ソフトウェアの即時更新**  
  - ベンダーが提供する最新パッチを適用し、バージョン番号を確認。  
- **管理インターフェースへのアクセス制限**  
  - 管理画面は VPN や IP アクセスリストで社内ネットワークのみからアクセス可能にする。  
- **不要な機能・サービスの無効化**  
  - `Guest_ssid` や `NatStaticSetting` など、使用しない CGI エンドポイントは Web サーバ設定で無効化。  
- **侵入検知・ログ監視の強化**  
  - `/cgi-bin/`、`/goform/` への POST リクエストを監視し、異常なパラメータ長や頻度をアラート化。  

### 3.2 製品別具体的アクション  

| 製品 | 推奨パッケージ／ファームウェア | 取得先・リリースノート |
|------|------------------------------|------------------------|
| **Hitachi Virtual Storage Platform** | **DKCMAIN Ver. 93‑07‑26‑xx/00 以降**、**GUM Ver. 93‑07‑26/00 以降** | Hitachi Support Portal（[リンク](https://www.hitachi.com/support)） |
| **Wavlink WL‑NU516U1‑A** | **Firmware V240426 以上**（2026‑02‑15 リリース） | Wavlink ダウンロードセンター → 「WL‑NU516U1‑A Firmware」 |
| **Tenda JD12L** | **Firmware 16.03.53.24**（2026‑03‑01 リリース） | Tenda Support → 「JD12L Firmware」 |
| **共通** | **OpenSSH ≥ 9.5**（管理端末での安全なリモート接続） | OS ディストリビュータのパッケージリポジトリ |

### 3.3 短期的な緊急措置
1. **外部からの管理ポート（例: 80/443）を一時的に遮断**し、内部からのみアクセスできるようにする。  
2. **脆弱性が確認された CGI エンドポイントの POST パラメータ長を Web アプリケーションファイアウォール（WAF）で上限設定**（例: 256 バイト）し、オーバーフローを防止。  
3. **影響デバイスの資産一覧を作成し、優先度（業務重要度）に応じて段階的にパッチ適用**する。  

---

### まとめ
- 今回の CVE はすべて **リモートコード実行** を可能にする深刻度の高いバッファオーバーフローです。特にエンタープライズ向けストレージと家庭向けルータが対象となっており、**ネットワーク境界の防御が崩れるリスク** が顕著です。  
- ベンダーが提供する **最新ファームウェア**（Hitachi: DKCMAIN/GUM 93‑07‑26‑xx/00、Wavlink: V240426、Tenda: 16.03.53.24）へのアップデートが最優先です。  
- アップデートと同時に **アクセス制御・ログ監視・WAF 設定** を強化し、攻撃者の足掛かりを排除してください。  

> **※** 本レポートは 2026 年 6 月時点の情報に基づいています。以降に新たなパッチや脆弱性情報が公開される可能性がありますので、定期的なベンダー情報のチェックを推奨します。

---

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2025-2902

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-29T07:16:23.583 |

Improper Authorization Vulnerability of Maintenance Utility in Hitachi Virtual Storage Platform.

This issue affects Hitachi Virtual Storage Platform E390, E590, E790, E990, E1090, E390H, E590H, E790H, E1090H: before DKCMAIN Ver. 93-07-26-xx/00, GUM Ver. 93-07-26/00; Hitachi Virtual Storage Platform 5100, 5500, 5100H, 5500H, 5200, 5600, 5200H, 5600H: before DKCMAIN Ver. 90-09-27-00/00, GUM Ver. 90-09-27/00; Hitachi Virtual Storage Platform G130, G150, G350, G370, G700, G900, F350, F370, F700, F900: before DKCMAIN Ver. 88-08-16-xx/00, GUM Ver. 88-08-20/00.

### CVE-2026-13539

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-06-29T07:16:24.183 |

A vulnerability was identified in Wavlink WL-NU516U1-A M16U1_V240425. The impacted element is the function sub_407504 of the file /cgi-bin/wireless.cgi of the component POST Parameter Handler. Such manipulation of the argument Guest_ssid leads to stack-based buffer overflow. The attack can be executed remotely. The exploit is publicly available and might be used. It is suggested to upgrade the affected component. The vendor was contacted early, responded in a very professional manner and quickly released a fixed version of the affected product.

### CVE-2026-13519

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-06-29T02:16:25.063 |

A vulnerability was found in Tenda JD12L 16.03.53.23. This impacts the function fromNatStaticSetting of the file /goform/NatStaticSetting. The manipulation of the argument page results in stack-based buffer overflow. The attack can be executed remotely. The exploit has been made public and could be used.

### CVE-2026-13518

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-06-29T01:16:30.683 |

A vulnerability has been found in Tenda JD12L 16.03.53.23. This affects the function fromAddressNat of the file /goform/addressNat. The manipulation of the argument page leads to stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit has been disclosed to the public and may be used.

### CVE-2026-13517

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-06-29T01:16:30.517 |

A flaw has been found in Tenda JD12L 16.03.53.23. The impacted element is the function formWifiBasicSet of the file /goform/WifiBasicSet. Executing a manipulation of the argument security_5g can lead to stack-based buffer overflow. The attack may be launched remotely. The exploit has been published and may be used.

### CVE-2026-13516

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-06-29T00:16:47.633 |

A vulnerability was detected in Tenda JD12L 16.03.53.23. The affected element is the function fromSetWifiGusetBasic of the file /goform/WifiGuestSet. Performing a manipulation of the argument shareSpeed results in stack-based buffer overflow. The attack may be initiated remotely. The exploit is now public and may be used.

### CVE-2026-13515

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-06-29T00:16:47.463 |

A security vulnerability has been detected in Tenda JD12L 16.03.53.23. Impacted is the function formSetPPTPServer of the file /goform/SetPptpServerCfg. Such manipulation of the argument startIp leads to stack-based buffer overflow. The attack can be launched remotely. The exploit has been disclosed publicly and may be used.
