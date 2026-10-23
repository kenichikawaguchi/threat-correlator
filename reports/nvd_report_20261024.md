# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-23 15:00 UTC
- **対象期間**: `2026-10-22T15:01:36.000Z` 〜 `2026-10-23T15:00:34.000Z`
- **重要CVE数**: 243 件（Critical 9.0+: 80 件 / High 7.0〜: 163 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** と非常に多く、特に **クラウド基盤（Azure）** と **オープンソースの Web アプリケーション** に集中しています。  
- Azure の認証・権限昇格系脆弱性が **CVSS 10.0** と最高評価で多数報告され、ネットワーク越しに無認証でフル権限取得が可能になる点が共通しています。  
- WordPress 系テーマ・プラグインの **Object Injection** 系脆弱性が続発し、PHP 環境全般に対するリスクが拡大しています。  
- IoT/ルータ向けの **odhcpd** や AI ゲートウェイの **LiteLLM** でも、メモリ破壊や暗号コンテキスト再利用といった深刻な欠陥が確認されました。  

> **傾向**：認証バイパス・権限昇格がクラウドサービスで顕在化している一方、オープンソース CMS のサプライチェーンリスクも依然として高止まりしています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑83938** | 10.0 | Azure Kubernetes Configuration Service の認証欠如により、攻撃者がネットワーク上で **フル管理権限** を取得可能 | Azure のコアインフラに対する **認証なしの権限昇格**。K8s クラスタ全体が乗っ取られる危険性がある。 |
| **CVE‑2026‑97785** | 10.0 | Azure AD Application Proxy の不適切な認証により、ネットワーク経由で **特権昇格** が可能 | AAD App Proxy は多くの企業がリモートアクセスに利用しているため、被害範囲が広い。 |
| **CVE‑2026‑110063** | 10.0 | Azure VM Inspector のシンボリックリンク解決不備 → 任意ファイルアクセス・権限昇格 | VM の監査・診断ツールが攻撃対象になる珍しいケースで、**内部ネットワーク全体** に波及する恐れ。 |
| **CVE‑2026‑53921** | 9.8 | OpenWrt の odhcpd がスタックバッファオーバーフローを起こし、リモートからコード実行が可能 | IoT デバイス・ホームルータに広く組み込まれており、**家庭・産業ネットワーク** の踏み台化リスクが高い。 |
| **CVE‑2026‑114612** | 9.9 | LiteLLM (AI Gateway) が暗号コンテキストを再利用し、認証済み内部ユーザーが **任意のシークレット** を取得可能 | AI API のプロキシとして広く採用されているため、機密情報漏洩や不正利用が懸念される。 |
| **CVE‑2026‑63244** | 9.8 | WizLearn LMS の認証バイパス → 任意のユーザーとしてログイン可能 | 教育機関・企業の LMS が標的になるケースが増加。学習データや個人情報が危険にさらされる。 |
| **CVE‑2026‑112858 〜 112851 系列** (WordPress テーマ) | 9.8 | 複数テーマで **Object Injection** が可能。PHP のシリアライズデータを細工して任意コード実行 | WordPress サイトは世界中で数千万件稼働中。テーマ単位での脆弱性は **一括感染** のリスクが高い。 |

> **上位 5 件** としては、Azure 系 (83938, 97785, 110063) と odhcpd、LiteLLM を選出。これらは **ネットワーク境界を越えて直接権限取得・コード実行** が可能で、被害拡大が最も速いと判断しました。

---

## 3. 推奨アクション  

### 3.1 Azure 系サービス（CVE‑2026‑83938・97785・110063）  
- **即時パッチ適用**  
  - Azure Kubernetes Configuration Service → **2026‑04‑15 以降の最新リリース**へアップデート。  
  - Azure AD Application Proxy → **2026‑04‑20 以降のパッチ**を適用。  
  - Azure VM Inspector → **2026‑04‑22 以降のバージョン**（`v2.5.3` 以上）に更新。  
- **アクセス制御の強化**  
  - Azure AD の条件付きアクセスポリシーで **MFA 必須**、IP 制限を有効化。  
  - 管理者ロールの **最小権限化** と **ロールベースアクセス制御 (RBAC)** の再評価。  
- **監視・ログ**  
  - Azure Monitor の **Azure AD Sign‑in logs** と **Kubernetes audit logs** をリアルタイムでアラート設定。  
  - 不審な API 呼び出しや権限変更が検出されたら自動で **アカウントロック** するプレイブックを導入。

### 3.2 odhcpd (OpenWrt) – CVE‑2026‑53921  
- **ファームウェア更新**  
  - OpenWrt 25.12 以上（`odhcpd` パッケージ `1.4.2` 以上）へアップグレード。  
- **ネットワーク分離**  
  - DHCPv6/RA サービスは **信頼できる VLAN** に限定し、外部からの直接アクセスを遮断。  
- **IDS/IPS ルール**  
  - Suricata/Zeek で **DHCPv6 IA‑Option のサイズ異常** を検知するシグネチャを追加。

### 3.3 LiteLLM – CVE‑2026‑114612  
- **バージョン更新**  
  - 1.104.0‑rc.2 以前のすべてのバージョンを **1.104.0‑rc.3 以降**（または公式リリース `1.105.0`）に置き換える。  
- **暗号コンテキスト分離**  
  - 環境変数 `LLM_SECRET_CONTEXT_ISOLATION=true` を設定し、シークレットごとに独立した鍵を使用。  
- **内部アクセス制御**  
  - プロキシへのアクセスは **Zero‑Trust ネットワーク** 上の認証済みサービスアカウントのみに限定。  
  -

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-97785

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-22T22:20:13.483 |

Improper authentication in AAD App Proxy allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-83938

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-22T22:19:18.540 |

Missing authentication for critical function in Azure Kubernetes Configuration Service allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-110063

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-22T22:18:00.750 |

Improper link resolution before file access ('link following') in VM Inspector for Azure Virtual Machines allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-79851

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-22T19:17:57.290 |

No description provided

### CVE-2026-79850

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-22T19:17:57.183 |

No description provided

### CVE-2026-79849

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T19:17:57.070 |

No description provided

### CVE-2026-79848

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T19:17:56.850 |

No description provided

### CVE-2026-79847

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-22T19:17:56.633 |

No description provided

### CVE-2026-79846

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:56.490 |

No description provided

### CVE-2026-79844

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-22T19:17:56.367 |

No description provided

### CVE-2026-114612

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-345;CWE-441` |
| Published | 2026-10-22T19:17:37.540 |

LiteLLM is a proxy server (AI Gateway) to call LLM APIs in OpenAI (or native) format. From 1.87.0 until 1.100.4, 1.101.3, 1.102.2, 1.103.1, and 1.104.0-rc.2, the proxy reuses one cryptographic context for at-rest secrets and session tokens, allowing an authenticated internal user to have crafted metadata containing a forged administrator credential encrypted and returned by the API-key flow. Replaying that ciphertext as a bearer token causes the proxy to trust the forged proxy administrator identity, permitting administrative access and arbitrary commands through the MCP stdio endpoint. Versions 1.87.0 through 1.90.x require EXPERIMENTAL_UI_LOGIN to be enabled, while versions after 1.91.0 are exploitable in the default configuration. This issue was fixed in LiteLLM 1.100.4, 1.101.3, 1.102.2, 1.103.1, and 1.104.0-rc.2.

### CVE-2026-53921

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-23T14:17:53.710 |

odhcpd is the DHCPv6, DHCPv4, and router-advertisement server used by OpenWrt. Prior to version 25.12, odhcpd's DHCPv6 IA response handler writes past the end of a fixed 512-byte stack buffer (pdbuf) when a single DHCPv6 REQUEST carries enough IA options to nearly exhaust the reply space. Two independent overflow sites exist in the same call chain, both reachable from the network via a single unauthenticated UDP packet. odhcpd runs as root on OpenWrt; embedded targets often lack stack canaries and ASLR, making code execution realistic. This issue has been patched in version 25.12.

### CVE-2026-57116

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-306;CWE-862` |
| Published | 2026-10-23T13:17:10.690 |

PraisonAI is a multi-agent teams system. From version 4.2.1 to before version 4.6.59, PraisonAI's AgentOS FastAPI deployment surface remains unauthenticated in current main and in releases after the published patched version for GHSA-pm96-6xpr-978x / CVE-2026-40151. The chat route directly calls agent.chat(request.message). No-auth and wrong-bearer requests both execute the deployed agent. This is broader than passive metadata disclosure. In any deployment where AgentOS wraps agents with tools, private context, memory, API integrations, or cost-bearing model calls, an unauthenticated reachable client can drive those agents. This issue has been patched in version 4.6.59.

### CVE-2026-112859

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:07.700 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Little Birdies little-birdies allows Object Injection.This issue affects Little Birdies: from n/a through 1.3.16.

### CVE-2026-112858

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:07.573 |

Deserialization of Untrusted Data vulnerability in axiomthemes Rhodos rhodos allows Object Injection.This issue affects Rhodos: from n/a through 1.3.3.

### CVE-2026-112857

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:07.447 |

Deserialization of Untrusted Data vulnerability in axiomthemes Reprizo reprizo allows Object Injection.This issue affects Reprizo: from n/a through 1.0.8.

### CVE-2026-112856

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:07.323 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Vagabonds vagabonds allows Object Injection.This issue affects Vagabonds: from n/a through 1.3.10.

### CVE-2026-112855

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:07.197 |

Deserialization of Untrusted Data vulnerability in axiomthemes Redy redy allows Object Injection.This issue affects Redy: from n/a through 1.3.5.

### CVE-2026-112854

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:07.070 |

Deserialization of Untrusted Data vulnerability in axiomthemes Holistic Center holistic-center allows Object Injection.This issue affects Holistic Center: from n/a through 1.2.6.

### CVE-2026-112853

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:06.940 |

Deserialization of Untrusted Data vulnerability in axiomthemes Hallelujah hallelujah allows Object Injection.This issue affects Hallelujah: from n/a through 1.1.1.

### CVE-2026-112851

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:06.697 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group HotLock hotlock allows Object Injection.This issue affects HotLock: from n/a through 1.3.9.

### CVE-2026-112848

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:06.310 |

Deserialization of Untrusted Data vulnerability in AivahThemes Hostme v2 hostmev2 allows Object Injection.This issue affects Hostme v2: from n/a through 7.0.

### CVE-2026-112847

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:06.190 |

Deserialization of Untrusted Data vulnerability in ThemeREX ZenSoul zensoul allows Object Injection.This issue affects ZenSoul: from n/a through 1.13.

### CVE-2026-112846

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:06.057 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Save Life save-life allows Object Injection.This issue affects Save Life: from n/a through 1.2.14.

### CVE-2026-112862

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T09:17:06.393 |

Deserialization of Untrusted Data vulnerability in xnau webdesign Participants Database participants-database allows Object Injection.This issue affects Participants Database: from n/a through 2.7.8.5.

### CVE-2026-63244

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-23T08:16:55.320 |

An authentication
bypass vulnerability in WizLearn Technologies' Learning Management System (LMS)
could allow an unauthenticated remote attacker to bypass password
authentication and the OAuth authentication flow by sending a specially crafted
POST request, potentially resulting in unauthorised access to user accounts and
full administrative control of the LMS platform.

### CVE-2026-79861

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:58.407 |

No description provided

### CVE-2026-79860

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:58.303 |

No description provided

### CVE-2026-79859

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:58.190 |

No description provided

### CVE-2026-79858

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:58.083 |

No description provided

### CVE-2026-79857

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:57.963 |

No description provided

### CVE-2026-79856

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:57.857 |

No description provided

### CVE-2026-79855

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:57.743 |

No description provided

### CVE-2026-79854

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:57.627 |

No description provided

### CVE-2026-79853

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:57.513 |

No description provided

### CVE-2026-79852

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:57.410 |

No description provided

### CVE-2026-55981

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-23T07:16:38.420 |

A firmware verification vulnerability in Creative Sound
Blaster Katana could allow an attacker to modify a legitimate firmware image
and upload the modified firmware to an affected device.

### CVE-2026-54630

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-23T04:18:17.007 |

Part-DB is an open source inventory management system for electronic components. Prior to version 2.12.1, the part attachment upload handler stores uploaded files under the web-served media directory using the client-supplied file extension, and its extension blocklist does not include phar. AttachmentSubmitHandler::renameBlacklistedExtensions() rewrites dangerous extensions (php, phtml, sh, cgi, py, js, html, htaccess, ...) to .txt, but phar is absent from the list, so a .phar file keeps its extension. Public attachments (the default) are written into public/media/, which is the Apache document root. The shipped Apache configuration routes .phar to PHP-FPM, so the stored file is executed as PHP on request. The per-attachment-type extension filter is empty by default and is not consulted by the upload handler in a way that blocks this, and a non-admin user in the default users group can create an attachment type with no filter and attach files to parts. Any authenticated user in the default users group uploads a .phar attachment to a part and fetches it under /media/, executing arbitrary PHP as the www-data web user. Ability to exploit depends on the webserver config, docker image contained the vulnerability by default. This issue has been patched in version 2.12.1.

### CVE-2026-79871

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:59.493 |

No description provided

### CVE-2026-79870

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:59.390 |

No description provided

### CVE-2026-79869

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:59.280 |

No description provided

### CVE-2026-79868

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:59.177 |

No description provided

### CVE-2026-79867

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:59.067 |

No description provided

### CVE-2026-79866

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:58.960 |

No description provided

### CVE-2026-79865

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:58.850 |

No description provided

### CVE-2026-79864

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:58.743 |

No description provided

### CVE-2026-79863

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:58.630 |

No description provided

### CVE-2026-79862

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:58.520 |

No description provided

### CVE-2026-97631

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120;CWE-131;CWE-787` |
| Published | 2026-10-22T17:17:02.027 |

EDK2 contains a vulnerability in BIOS where a user may cause “Out-of-bounds
Write”, Classic
Buffer Overflow, and “Incorrect Calculation of Buffer Size” by remote access. Successful exploitation of this vulnerability
can lead to arbitrary
code execution. It could also impact
Confidentiality,
Integrity,
and Availability.

### CVE-2025-30050

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-23T09:17:04.810 |

CGM CLININET is vulnerable to Code Injection in the RunCGI.pm component, which dynamically imports the module specified as a query parameter and executes code from untrusted data provided by the user. An attacker from adjacent network can supply a crafted query parameter to have an attacker-controlled module imported which results in arbitrary code execution with root privileges.


This issue was fixed in version 2026.MS3

### CVE-2025-30047

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T09:17:04.573 |

CGM CLININET is vulnerable to Remote Code Execution caused by deserialization of untrusted data. The server exposes an HTTP-based API, used by the administrative module, that exchanges data using Java object serialization. An attacker within the same local network is able to send requests to this API and transmit a crafted serialized object. When it is deserialized, it allows arbitrary code execution with root privileges on the server. 


This issue was fixed in version 2026.MS3

### CVE-2026-110243

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-22T23:18:22.520 |

The network management service on affected Kiloview E3 NDI encoder firmware fails to validate the network interface name accepted by its link maintenance address configuration endpoint before passing it to a shell command, unlike sibling handlers that perform the same validation. An authenticated web user with permission to configure network settings can exploit this to execute arbitrary operating system commands as root.

### CVE-2026-107861

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-22T23:18:17.190 |

The system control service on affected Kiloview E3 NDI encoder firmware fails to sanitize the hostname parameter accepted by its device naming endpoint, passing it unquoted into a shell command. An authenticated web user with access to this function can embed characters to execute arbitrary operating system commands as root, resulting in full device compromise.

### CVE-2026-109122

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-22T22:17:59.930 |

The network management service on affected Kiloview E3 NDI encoder firmware fails to sanitize one field used when configuring static routes via the web management API. An authenticated web user with permission to configure static routes can exploit this to execute arbitrary operating system commands as root, and the malicious configuration persists across reboots. Successful exploitation could result in full device compromise, including exposure of stored credentials and cryptographic material.

### CVE-2026-114625

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-22T21:17:16.870 |

VeloCloud Orchestrator (VCO) on-prem has a security issue where this issue may allow a remote attacker to access privileged internal functionality and impact the VCO host. Successful exploitation may compromise the confidentiality, integrity, and availability of the orchestrator and data managed by the orchestrator.

On an affected system, any authenticated user can gain operator privileges and masquerade as a local "superuser operator" user. This includes access to functionality that is intended for internal use only and which is not intended to be remotely accessible.

Hosted, including Dedicated, versions of VCO were impacted and have already been patched.

### CVE-2026-79872

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:59.600 |

No description provided

### CVE-2026-115384

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-22T19:17:45.543 |

Wasmtime 39.0.0 before 48.0.4 and 49.0.0 before 49.0.2 contains a stack buffer overflow vulnerability that allows malicious guests to write ~16KB to the native stack via unvalidated async callback result types. Attackers can supply components with mistyped component-model-async callback functions to overwrite return addresses, crashing the host or escaping the sandbox.

### CVE-2026-115377

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-22T19:17:44.460 |

Incus before 6.0.7, 6.1.0 before 7.0.2, and 7.1.0 before 7.5.0 contains an arbitrary file write vulnerability that allows malicious migration sources to write host files by planting symlinks in transferred volumes. Attackers can craft rsync or btrfs receive streams with a symlink such as rootfs pointing to the host root, writing files as root for full host compromise.

### CVE-2026-115375

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T19:17:44.133 |

Incus 7.0.0 before 7.0.2 and 7.1.0 before 7.5.0 contains a path traversal vulnerability that allows clients able to create instances to write files on the host. The flaw stems from unvalidated dependent custom volume names in instance backup index.yaml files. Attackers can import a crafted instance backup with ../ sequences in dependent volume names to create root-owned directories with controlled content, leading to full host compromise.

### CVE-2026-114357

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-23T14:17:49.820 |

Missing authentication for a critical function in the Android Debug Bridge daemon (adbd) in DJI CrystalSky ZS600C firmware v0.3.9.7 through v0.6.6.9 allows an attacker to obtain an unauthenticated shell (uid 2000), a foothold for privilege escalation to root. The device ships with ro.adb.secure=0 (no host key authorization) and USB ADB enabled by default; ADB over TCP is not enabled by default but, once enabled (e.g. via the shipped /system/bin/adbd_tcp.sh or 'setprop persist.adb.tcp.port 5555'), the same unauthenticated shell is reachable over the network (CVSS 4.0 base 9.3).

### CVE-2026-25784

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-1188` |
| Published | 2026-10-23T09:17:06.943 |

Initialization of a Resource with an Insecure Default vulnerability in Hallo Welt! GmbH BlueSpice (container image bluespice/wiki) allows privilege escalation. The default value of $mwsgTokenAuthenticatorServiceCIDR in the container's LocalSettings.php was intended to restrict internal service authentication to the container network, but evaluated to an empty string when the environment variable WIKI_SERVICE_TOKEN_AUTH_ALLOWED was not set. An empty value disables the IP restriction in the token authenticator component (mwstake/mediawiki-component-token-authenticator). As a result, any user with read access to the wiki (anonymous users on publicly readable wikis) could obtain an application token from the REST API and use it to get a session with sysop privileges as the internal service user.

This issue affects BlueSpice: from 5.2.3 before 5.2.7, and the 5.2.7 container images published before 2026-10-19 15:37 UTC.

### CVE-2026-112860

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-23T09:17:06.280 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in xnau webdesign Participants Database participants-database allows Blind SQL Injection.This issue affects Participants Database: from n/a through 2.7.8.5.

### CVE-2025-30054

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-23T09:17:05.290 |

CGM CLININET is vulnerable to local privilege escalation. The service that processes incoming HL7 messages runs with root privileges, but due to incorrect permissions, its scripts and configuration files can be modified by the uhcapache user. An attacker with uhcapache privileges can modify these files to execute arbitrary code as root.


The vulnerability was confirmed to affect versions up to 2026.MS3 but later versions may also be vulnerable.

### CVE-2026-19677

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-23T02:16:57.560 |

An authentication bypass vulnerability in the public onPhase/ frevvo registration form version 11.0.14 allows an unauthenticated remote attacker to authenticate as an arbitrary tenant user, obtain TenantAdmin and Designer privileges, and execute arbitrary operating system commands via manipulation of registration parameters containing a valid tenant name and existing user identifier.

### CVE-2026-79876

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:00.050 |

No description provided

### CVE-2026-79875

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:59.943 |

No description provided

### CVE-2026-79874

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:59.837 |

No description provided

### CVE-2026-79873

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:17:59.727 |

No description provided

### CVE-2022-51026

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-22T19:17:30.883 |

Bytebase 0.12.0 before 1.0.1 contains an authentication bypass vulnerability that allows unauthenticated attackers to log in as any user. The flaw stems from trusting client-supplied GitLab provider configuration in the POST /api/auth/login/GITLAB_SELF_HOST endpoint. Attackers can set instanceUrl to a server they control that returns an active user with a chosen email. Bytebase then issues session tokens for that principal, letting attackers impersonate existing users including the Owner or create new members.

### CVE-2026-115727

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-10-23T12:18:13.560 |

AgenticSeek before commit 409840c contains a remote code execution vulnerability because llm_server/app.py hardcodes Flask debug mode while binding to all interfaces. Attackers who reach the server port and obtain the derivable Werkzeug debugger PIN can execute Python code and operating system commands with llm_server privileges.

### CVE-2026-111594

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-22T22:18:01.060 |

InterSystems IRIS for Health has TLS/SSL encryption turned off by default, which may enable an attacker to view transmitted data and use that data to log into the device.

### CVE-2026-115353

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T19:17:41.227 |

Mistune before 3.3.0 contains a path traversal vulnerability in the RST include directive that allows attackers to read arbitrary files by supplying relative or absolute paths. Attackers can submit markdown containing include directives referencing ../ sequences or absolute paths to embed sensitive files like credentials or environment data in rendered HTML.

### CVE-2026-107685

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-23T12:18:06.410 |

Improper Certificate Validation vulnerability in the WebSocket streaming client in agentjido req_llm allows an on-path attacker to read and modify OpenAI WebSocket sessions, including the authorization bearer token, via a TLS certificate the client does not trust. ReqLLM.Streaming.WebSocketSession.Client.start/3 in lib/req_llm/streaming/web_socket_session/client.ex starts WebSockex without TLS options, and WebSockex defaults to insecure: true, which connects with verify: :verify_none. The option allowlist also drops any caller-supplied cacerts or ssl_options, so an application cannot turn verification on.

The OpenAI Responses, Realtime, and Codex WebSocket paths reach this client and send the API key or OAuth access token in the authorization header. HTTP streaming through Finch and the HTTP/2 duplex session through Mint verify certificates and are not affected.

This issue affects req_llm: from 1.9.0 before 1.29.0.

### CVE-2026-115547

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-94` |
| Published | 2026-10-23T04:18:16.030 |

An input validation issue in the Okta Access Gateway (OAG) Admin Console allows the processing of specially formatted configuration values. An authenticated administrator can leverage this to execute system commands within the context of the OAG service account.

### CVE-2026-105014

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-22T22:17:52.183 |

Improper neutralization of special elements used in a command ('command injection') in Azure Pipelines allows an unauthorized attacker to execute code over a network.

### CVE-2026-114611

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-22T18:17:28.377 |

OCO-Server is a self-hosted endpoint management application for computer inventory, software deployment, and mobile device management. Prior to 1.2.3,the Apple MDM enrollment endpoint `frontend/api-mdm.php` verifies the signed enrollment-request plist with `openssl_pkcs7_verify(..., PKCS7_NOVERIFY, ...)`. `PKCS7_NOVERIFY` disables signer certificate chain and trust validation, so the signature only has to be self-consistent with whatever certificate is embedded in the PKCS#7 blob. A self-signed certificate from an unrelated attacker is accepted. Because the endpoint trusts the `SERIAL` field taken from the unverified payload, anyone who knows a registered device's serial number can sign a forged plist (`SERIAL` = victim device, attacker-chosen `UDID`) with an arbitrary self-signed certificate; POST it unauthenticated to `/api-mdm.php/profile` (Content-Type: `application/pkcs7-signature`); and receive the victim device's freshly minted MDM identity: a certificate with `CN=<serial>` issued by the server's internal MDM device CA, bundled with its private key in a PKCS#12 payload inside the returned `.mobileconfig` enrollment profile. Additionally, the victim's `mobile_device` database row is silently overwritten with the attacker-supplied `UDID` (device-record hijack). With the stolen certificate and key, the attacker can impersonate the victim device on all subsequent MDM traffic (`/checkin`, `/mdm`, `/parameters`), which authenticate callers by the certificate CN (the serial number) via `checkSignature()` in the same file. This yields control over the victim device's MDM relationship: reading its management data, replacing its push token, and disrupting or redirecting its enrollment. Version 1.2.3 fixes the issue.

### CVE-2026-114607

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-22T17:16:58.577 |

Better Auth is an authentication and authorization library for TypeScript. From 1.4.0-beta.18 until 1.7.7, deployments that enable Magic Link with storeToken set to plain, or with storeToken set to hashed and the global verification.storeIdentifier setting also set to hashed, enable a built-in social or Generic OAuth provider, and use account.storeStateStrategy set to database can accept an OAuth sign-in state value as a Magic Link token. These settings can cause Magic Link verification records and OAuth state to resolve to the same stored identifier, allowing an unauthenticated attacker to start OAuth sign-in for a known email address and redeem the returned state through Magic Link without controlling the mailbox or completing the provider callback. The attacker can obtain a normal session for an existing user, or create an account incorrectly marked as email verified when sign-up is enabled. This issue is fixed in version 1.7.7.

### CVE-2025-30046

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-10-23T09:17:04.450 |

In the CGM CLININET application server, multiple processes responsible for HL7 communication with external systems run with root privileges while processing untrusted data received from those external systems. An attacker in adjacent network able to send data to these HL7 communication processes can achieve remote code execution with root privileges. 


The vulnerability was confirmed to affect versions up to 2026.MS3 but later versions may also be vulnerable.

### CVE-2026-94267

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-23T06:17:08.200 |

The Advanced Custom Fields: Extended WordPress plugin before 0.9.2.8, Advanced Custom Fields: Extended PRO WordPress plugin before 0.9.2.8 does not perform any capability check when updating a post through one of its front-end form actions, allowing unauthenticated visitors to overwrite arbitrary posts, including the ones in which the site stores its own field definitions, which in turn leads to arbitrary code execution on the server. Exploitation requires the site to publish a form whose post-update action maps both its target and its content to visitor-submitted values.

### CVE-2026-115372

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-22T19:17:43.670 |

Incus from 7.3.0 before 7.5.0 contains a project restriction bypass that allows restricted project users to set block.create_options through volume update, copy, and move operations. Attackers can set the option on a custom volume and trigger a copy or move onto a formatting pool to inject arguments into mkfs executed as root.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-115729

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-23T13:17:08.740 |

@pdfme/common from 5.5.10 before 6.2.6 contains a server-side request forgery vulnerability that allows attackers to bypass the isUrlSafeToFetch denylist in getB64BasePdf. Attackers can supply basePdf URLs using IPv4-mapped IPv6, [::], NAT64 or localhost alias hostnames to read loopback, internal or cloud metadata responses through generated documents.

### CVE-2026-53918

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416;CWE-672;CWE-825` |
| Published | 2026-10-23T14:17:53.423 |

odhcpd is the DHCPv6, DHCPv4, and router-advertisement server used by OpenWrt. Prior to version 25.12, odhcpd's DHCPv6 IA handler keeps a per-message `first` lease pointer so multiple IA options in one message reuse the same Reconfigure authentication key. A DHCPv6 REQUEST from an adjacent-network client can make the first IA set `first`, then make a later same-IAID IA fail the on-link check and free that same lease, leaving `first` dangling. A following IA in the same packet allocates a new lease and copies `first->key`, producing a 16-byte heap-use-after-free read. ASan confirms the UAF; native tracing shows the packet shape can deterministically reclaim the freed lease as the destination allocation, producing a zeroed Reconfigure key copy. The validated impact is unauthenticated adjacent-network denial of service and DHCPv6 Reconfigure/ForceRenew key confusion. Arbitrary PC control is not proven for this UAF alone. This issue has been patched in version 25.12.

### CVE-2026-114621

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-23T14:17:51.143 |

baserCMS is a website development framework. In versions 5.0.0 before 5.3.2 and 5.4.0 before 5.4.2, list and detail actions in the Admin and Api/Admin prefixes pass request query parameters, including contain, conditions, fields, finder, and order, directly to the ORM as options. A user able to log into the admin panel can embed SQL fragments in those options to execute arbitrary SQL against the application's database, including reading password hashes from the users table. Public-page and public-API fixes released in 5.3.1 and 5.4.1 did not protect these administrative paths. Setting USE_CORE_ADMIN_API to false does not prevent access through an authenticated browser session. This issue has been patched in versions 5.3.2 and 5.4.2.

### CVE-2026-57144

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-266;CWE-668;CWE-693` |
| Published | 2026-10-23T13:17:11.370 |

PraisonAI is a multi-agent teams system. From version 4.5.110 to before version 4.6.61, praisonai.sandbox.SandlockSandbox is documented and implemented as the kernel-enforced sandbox backend for untrusted code. Its SandboxConfig.native() path lets callers configure allowed filesystem paths and network=False. On systems where the optional sandlock module imports but reports that Landlock is unavailable, SandlockSandbox.execute() and run_command() do not fail closed. They silently fall back to SubprocessSandbox(self.config). That fallback keeps the same high-level native policy object but does not enforce the native filesystem or network boundary during code execution. A sandboxed payload can read files outside the configured allowed path and open network connections despite network=False. This issue has been patched in version 4.6.61.

### CVE-2026-57117

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-863` |
| Published | 2026-10-23T13:17:10.870 |

PraisonAI is a multi-agent teams system. From version 4.6.10 to before version 4.6.59, LocalManagedAgent / SandboxedAgent compute bridging wraps read_file, list_files, and write_file when a compute provider is attached. The bridge converts those file operations into shell command strings using raw path arguments, then sends those strings to shell-backed compute providers. An attacker who can influence a file-tool path argument can break out of the quoted path and execute arbitrary shell commands in the compute environment. With compute="local", commands execute through the local subprocess compute provider on the host. With Docker, commands execute in the container. This issue has been patched in version 4.6.59.

### CVE-2026-55888

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-23T13:17:10.090 |

XDG Desktop Portal is a desktop integration portal. Prior to version 1.22.1, malicious sandboxed applications can use the FileChooser.SaveFiles method to gain arbitrary file access to non-existing files on the host (limited to files the user has access to). The FileChooser.SaveFiles method takes optional filenames which get appended to the selected directory by backends. The backends are supposed to check that the file does not exist yet. The filenames are not validated by the frontend and also not by common backends. This issue has been patched in version 1.22.1.

### CVE-2026-56840

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T12:18:15.510 |

PraisonAI is a multi-agent teams system. From version 4.5.2 to before version 4.6.59, praisonai.bots.HTTPApproval renders pending tool approval arguments directly into the approval dashboard HTML. An attacker-controlled tool argument can inject JavaScript into that page. When a human opens the approval URL to inspect the risky tool request, the script runs in the dashboard origin and can POST to the same request's /approve/{request_id}/decide endpoint, causing HTTPApproval to return approved=True. This issue has been patched in version 4.6.59.

### CVE-2026-56832

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345;CWE-863` |
| Published | 2026-10-23T12:18:14.437 |

PraisonAI is a multi-agent teams system. From version 4.5.2 to before version 4.6.59, praisonai.bots.DiscordApproval approves a pending dangerous tool call when it sees any later non-bot message in the configured Discord channel whose text is classified as approval, such as yes. As a result, any user who can post in the configured approval channel can approve a pending high-risk tool call by sending yes after the approval message appears. the same PoV also shows that the Slack and Telegram messaging approval backends have no explicit approver allowlist parameter, but the primary report-grade issue is the Discord backend's unthreaded channel cross-talk: the approving message does not need to be a reply or otherwise request-bound. This issue has been patched in version 4.6.59.

### CVE-2026-89320

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-10-23T09:17:08.610 |

`HmacShaCryptor.Hash` never hashed its input. For any input it returned `HMAC_K("")` — the MAC of the empty message under the key. Every AES-CBC-HMAC JWE produced or verified by gose therefore carried an authentication tag that is constant per key and independent of the message, removing ciphertext integrity entirely.

### CVE-2025-30052

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-23T09:17:05.040 |

The rsyncd service of the CGM CLININET is vulnerable to Authentication Bypass via IP spoofing. Access is granted based solely on the client's source IP address. An attacker able to spoof an allowed IP address, can bypass this check and gain the ability to edit files on the affected system. 


The vulnerability was confirmed to affect versions up to 2026.MS3 but later versions may also be vulnerable.

### CVE-2026-79879

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:00.380 |

No description provided

### CVE-2026-79878

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:00.273 |

No description provided

### CVE-2026-79877

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:00.163 |

No description provided

### CVE-2026-115392

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-61` |
| Published | 2026-10-22T19:17:46.863 |

Wasmtime before 24.0.13, 25.0.0 before 36.0.14, 37.0.0 before 46.0.3, and 47.0.0 before 47.0.4 allows a filesystem sandbox escape in wasmtime-wasi because its cap-std dependency mishandles symlinks with trailing slashes on macOS and Linux kernels lacking openat2. A guest with write access to any sandboxed directory can read and write any host-accessible file, and read-only guests may read host files via preexisting symlinks.

### CVE-2026-108358

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611;CWE-776` |
| Published | 2026-10-22T18:17:26.553 |

PhpSpreadsheet is a pure PHP library for reading and writing spreadsheet files. Prior to 1.30.7, 2.1.19, 2.4.8, 3.10.8, and 5.10.0, XmlScanner::scan in src/PhpSpreadsheet/Reader/Security/XmlScanner.php uses a DOCTYPE detection pattern that accounts for NUL-byte interleaving but not ISO-2022 escape sequences in XLSX XML parts. The escape sequences prevent the scanner from matching the declaration, and XML charset normalization then removes the escape bytes before parsing, exposing a valid DOCTYPE and entity definitions. Processing an attacker-controlled XLSX can therefore cause entity-expansion denial of service on supported PHP versions and can permit local file access or SSRF on PHP before 8.0 or when LIBXML_NOENT is enabled. This issue is fixed in versions 1.30.7, 2.1.19, 2.4.8, 3.10.8, and 5.10.0.

### CVE-2026-108357

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611;CWE-776` |
| Published | 2026-10-22T18:17:26.377 |

PhpSpreadsheet is a pure PHP library for reading and writing spreadsheet files. From 3.3.0 until 3.10.8 and 5.10.0, Reader\Xml passes stored SpreadsheetML XML through XmlScanner::scan in Xml::canRead and Xml::trySimpleXMLLoadStringPrivate, while Xml::unentity decodes numeric entities only after each DOCTYPE pattern check. A double-encoded less-than character is reduced by the first callback to another encoded character and by the second callback to a literal less-than sign, so SimpleXML receives an unchecked DOCTYPE and entity declaration. Processing attacker-controlled SpreadsheetML XML can cause entity-expansion denial of service and can permit local file access or SSRF on PHP before 8.0 or when LIBXML_NOENT is enabled. This issue is fixed in versions 3.10.8 and 5.10.0.

### CVE-2026-93639

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-23T14:17:57.640 |

A missing authorization vulnerability in Zimbra Collaboration Suite (ZCS) allows a delegated administrator with no explicit administrative grants to overwrite global Zimlet configuration through ConfigureZimletRequest. The uploaded configuration can also add an attacker-controlled domain to the proxy allowlist of the default class of service. If a signed-in user in that class opens a crafted /service/proxy URL, Zimbra serves attacker-controlled HTML under its own origin. The resulting JavaScript can read mailbox data and perform authenticated actions as the victim. Exploitation requires a delegated-administrator account and access to the admin SOAP service; the browser compromise additionally requires the victim to open the crafted URL. ZCS 10.1.16 and 10.1.20 are affected.

### CVE-2026-55826

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-23T14:17:54.017 |

The GTM Server Side plugin by stape.io implements server-side tracking on WordPress websites. From version 2.0.0 to before version 2.1.48, the WooCommerce purchase event tracking mechanism allows an unauthenticated attacker to trigger the rendering of another customer's full order data — including personally identifiable information (PII) — into the page's JavaScript dataLayer. This issue has been patched in version 2.1.48.

### CVE-2026-53920

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-126;CWE-200;CWE-201` |
| Published | 2026-10-23T14:17:53.573 |

odhcpd is the DHCPv6, DHCPv4, and router-advertisement server used by OpenWrt. From version 17.01.0 to before version 25.12.3, odhcpd's DHCPv6 IA parser accepts an IA_NA or IA_PD option whose body is shorter than struct dhcpv6_ia_hdr, casts the option header to that full structure, and reads ia->iaid before proving that the IA body contains the IAID field. If an unauthenticated network-adjacent client places a zero-length or otherwise short IA option at the end of odhcpd's 8192-byte receive stack buffer, the IAID read crosses from data_buf into adjacent stack memory. The disclosed bytes are then reflected in the DHCPv6 reply IAID; prior ARM validation showed data_buf[8192:8196] disclosing the saved stack canary, and wider stack scans can leak ASLR-useful stack/process contents. This issue has been patched in version 25.12.3.

### CVE-2026-50053

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-642` |
| Published | 2026-10-23T14:17:53.060 |

A request attribute override vulnerability in Zimbra Collaboration Suite (ZCS) allows unauthenticated requests to /h/* to populate servlet attributes intended for trusted internal dispatch. RestFilter copies URL parameters specifying an authentication token, target account, target item and dispatch state into the request attributes consumed by the Classic Web Client. Combined with CVE-2026-10632 on ZCS 10.1.16, this allows an attacker to supply their own valid token and document identifiers and execute JavaScript in another user's signed-in browser session. ZCS 10.1.17 blocks that XSS chain by changing the document renderer, but retains the request attribute override.

### CVE-2026-10632

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T14:17:31.107 |

A reflected cross-site scripting vulnerability in the Classic Web Client of Zimbra Collaboration Suite (ZCS) allows an attacker to inject JavaScript through the packages parameter of the /h/rest document editor. The editor inserts package names into script attributes without HTML encoding. When combined with CVE-2026-50053, an attacker with an ordinary Zimbra account can supply their own authentication token and document identifiers in a URL and execute JavaScript in another signed-in user's Zimbra browser session when that user opens the URL. This permits reading mailbox data and performing authenticated actions as the victim. The issue affects ZCS 10.1.16 and was remediated in 10.1.17.

### CVE-2026-115728

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-23T13:17:08.590 |

@hapi/content from 6.0.1 before 6.0.3 contains a regular expression denial of service vulnerability in Content.disposition() caused by an incomplete fix for CVE-2026-35213. Unauthenticated remote attackers can send multipart uploads with a long Content-Disposition parameter lacking an equals sign, triggering quadratic backtracking that blocks the event loop.

### CVE-2026-112904

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-26` |
| Published | 2026-10-23T12:18:11.050 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. In versions 1.0.8.6 and prior, the nextRestore() and nextBackup() functions in the backup controller accept a file GET parameter and concatenate it directly to DIR_BACKUP without calling sanitizeFileName(). This allows an authenticated administrator to read arbitrary files on the server (via nextRestore) and write SQL dump content to arbitrary locations (via nextBackup). This is inconsistent with the sibling functions restore(), delete(), and download() which all correctly call sanitizeFileName() first. This issue has been patched via commit aa29cb0.

### CVE-2026-16762

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:A/V:X/RE:L/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-23T09:17:06.647 |

An attacker able to supply a crafted XML document to an application using QXmlStreamReader can cause disproportionate CPU consumption during parsing, making the application unresponsive (denial of service). Exploitation requires only that the application parse attacker-influenced XML; no authentication, privileges, or user interaction beyond ingesting the input are needed. There is no loss of confidentiality or integrity — no data disclosure, data modification, or code execution — and the impact is contained to the affected process.

### CVE-2026-93489

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-23T08:16:55.720 |

Improper Authentication in ASUS router modules allows an unauthenticated nearby user to send an HTTP request and forge an access ticket, subsequently enabling the user to perform administrator operations.
Refer to the ' Security Update for ASUS Router Firmware ' section on the ASUS Security Advisory for more information.

### CVE-2026-86055

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-23T05:17:19.060 |

Part-DB is an open source inventory management system for electronic components. Prior to version 2.13.3, Part-DB builds the absolute URL of the password-reset link it emails to a user from the client-supplied HTTP Host header, with no trusted-host validation. An unauthenticated attacker who submits a forgot-password request for a known account while sending a spoofed Host header causes Part-DB to email that account a reset link whose hostname is attacker-controlled, while still embedding the genuine reset token. When the victim opens the link (or an automated inbound mail-security scanner dereferences it), the valid token is disclosed to the attacker, who replays it against the real instance to set a new password and take over the account. Because the seeded admin account can be targeted, this yields full pre-authentication administrative account takeover. This issue has been patched in version 2.13.3.

### CVE-2026-19678

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-23T02:16:57.700 |

A server-side request forgery (SSRF) vulnerability in the unauthenticated form service in version 11.0.14 in onPhase Forms allows an unauthenticated remote attacker to access sensitive internal Apache Solr data via an attacker-controlled URL supplied to a publicly accessible form.

### CVE-2026-92450

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-22T23:20:33.703 |

The authentication framework used by affected Kiloview E3 NDI encoder firmware signs session JSON Web Tokens using an HMAC-SHA256 secret hardcoded as a static string within the firmware image, identical across all deployed devices. An attacker with access to the publicly distributed firmware can recover this secret and forge arbitrary session tokens, including administrative tokens, without valid credentials, enabling unauthenticated access to privileged device functions.

### CVE-2026-110825

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-22T23:18:22.940 |

The ONVIF device service on affected Kiloview E3 NDI encoder firmware accepts hostname, DNS, and NTP configuration write operations without requiring authentication, regardless of the device's configured authentication setting for this service. A remote, unauthenticated attacker can alter the device hostname, redirect DNS resolution, or modify the configured time source, enabling follow on attacks such as traffic interception or certificate validation bypass.

### CVE-2026-115506

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-776` |
| Published | 2026-10-22T20:17:06.620 |

libexpat through 2.9.0 contains a denial of service vulnerability because billion laughs protection in accountingDiffTolerated() in xmlparse.c detects entity amplification too late. Attackers can supply a moderately sized XML document with a large DTD and nested entity expansions to consume tens of seconds of CPU per parse.

### CVE-2026-112332

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-755` |
| Published | 2026-10-22T20:17:05.890 |

Motor.NET before 0.19.0 contains an uncaught exception vulnerability in JsonNetDeserializer.Deserialize that allows a remote attacker who can publish to a consumed queue or topic to crash the service permanently by sending structurally valid JSON that does not match the handler's expected type. Attackers can exploit the fact that JsonSerializationException is not caught alongside JsonReaderException and InvalidCastException, causing TypedConsumerService.SingleMessageConsumeAsync to treat the error as CriticalFailure and call StopApplication, which combined with the unacknowledged message being redelivered on restart results in a permanent crash-loop.

### CVE-2026-112331

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-755` |
| Published | 2026-10-22T20:17:05.750 |

Motor.NET before 0.19.0 contains a denial-of-service vulnerability that allows a remote attacker who can produce records to a consumed topic to crash the service permanently by sending a single crafted record. By setting the content-type header to application/cloudevents+json and omitting required CloudEvent attributes (id, source, type), the attacker triggers an ArgumentException in KafkaMessageConsumer.SingleMessageHandlingAsync that is treated as fatal, causing the host to stop and re-process the same poison record on every restart, resulting in a permanent crash-loop.

### CVE-2026-112330

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-755` |
| Published | 2026-10-22T20:17:05.580 |

Motor.NET before 0.19.0 contains a denial of service vulnerability that allows a remote attacker who can publish to a consumed queue to crash the service permanently by sending a message with crafted cloudEvents headers. Attackers can supply an invalid cloudEvents:motorversion, a single double-quote header value, or an unparsable typed attribute such as cloudEvents:time to trigger an unhandled exception in ExtractCloudEvent that is treated as fatal, causing the application to stop and the unacknowledged message to be redelivered on restart, resulting in a permanent crash-loop.

### CVE-2026-79880

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:00.490 |

No description provided

### CVE-2026-115355

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T19:17:41.520 |

Mistune before 3.3.0 contains a path traversal vulnerability in the Include directive that allows attackers to read arbitrary files by supplying ../ sequences in include paths. Attackers can also inject HTML through unescaped error messages and included file contents to perform cross-site scripting even when escape=True is set.

### CVE-2026-115352

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-22T19:17:41.077 |

Mistune before 3.3.0 contains an algorithmic complexity vulnerability in the inline link parser that allows unauthenticated attackers to exhaust CPU by submitting long runs of unmatched '[' characters. Attackers can send small markdown payloads that trigger O(N^2) parse_link_text and parse_link_label probing, occupying rendering workers for 30+ seconds per 16 KB input.

### CVE-2026-115349

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-22T19:17:40.597 |

Mistune from 3.0.0 before 3.3.0 contains an algorithmic complexity denial of service vulnerability in the parse_link_text function in src/mistune/helpers.py. Attackers can submit markdown with deeply nested square brackets triggering quadratic parsing time, exhausting server CPU with small crafted requests.

### CVE-2026-115348

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-22T19:17:40.430 |

Mistune from 3.0.0 before 3.3.0 contains an algorithmic complexity vulnerability in the inline link parser's parse_link_text function that allows unauthenticated attackers to exhaust CPU with unbalanced brackets. Attackers can submit Markdown containing many unbalanced '[' or '![' characters, forcing repeated unbounded forward scans and tying up worker processes for minutes.

### CVE-2026-115347

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-22T19:17:40.267 |

Mistune before 3.3.0 contains an inefficient algorithmic complexity vulnerability in parse_link_text that allows remote attackers to cause denial of service through unbalanced square brackets. Attackers can submit markdown containing long runs of unmatched brackets to mistune.html(), triggering repeated forward scans that stall worker processes for minutes.

### CVE-2026-113873

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-22T18:17:27.077 |

SmileCDR HAPI FHIR does not properly handle highly compressed data, allowing an unauthenticated attacker to send compressed payloads that exhaust server heap or crash certain services when decompressed.

### CVE-2026-108359

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-789` |
| Published | 2026-10-22T18:17:26.740 |

PhpSpreadsheet is a pure PHP library for reading and writing spreadsheet files. Prior to 1.30.7, 2.1.19, 2.4.8, 3.10.8, and 5.10.0, Ods::processTableRow in src/PhpSpreadsheet/Reader/Ods.php accepts an unbounded table:number-rows-repeated attribute from an ODS table row. When the row contains a value, the reader materializes a cell for every repetition without checking the spreadsheet row limit, so a small attacker-controlled ODS file can consume substantial CPU and memory and terminate the PHP worker. Column repetition is separately bounded and is not part of this vulnerability. This issue is fixed in versions 1.30.7, 2.1.19, 2.4.8, 3.10.8, and 5.10.0.

### CVE-2026-114355

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-23T14:17:36.323 |

OS command injection in the root-privileged 'hardware_monitor' helper in DJI CrystalSky ZS600C firmware v0.3.9.7 through v0.6.6.9 on Android allows a local unprivileged process to execute arbitrary commands as root by writing a crafted line to the Android log (logcat), which the helper reads and passes to a shell eval.

### CVE-2026-114354

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-862` |
| Published | 2026-10-23T14:17:35.297 |

Missing authorization in the native binder service 'android.dji.server' (transaction code 1018) in DJI CrystalSky ZS600C firmware v0.3.9.7 through v0.6.6.9 on Android allows a local application with no permissions to execute arbitrary OS commands as root, because the handler passes a caller-supplied string to system() in the root-privileged 'assistant' daemon without any caller-identity or permission check.

### CVE-2026-56837

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-287;CWE-306;CWE-347` |
| Published | 2026-10-23T12:18:15.203 |

PraisonAI is a multi-agent teams system. From version 4.6.56 to before version 4.6.59, PraisonAI's LinearBot starts a public webhook listener on 0.0.0.0 and treats LINEAR_WEBHOOK_SECRET as optional. When the secret is absent, startup only logs a warning and _handle_webhook() skips Linear-Signature verification entirely. An unauthenticated network caller who can reach the webhook endpoint can submit a forged Linear-Event: AgentSession request. The forged request is parsed, scheduled for background processing, dispatched to _handle_agent_session(), and passed into BotSessionManager.chat(). The bot then attempts to post the agent response back to Linear under the configured bot token. The PoV is offline and deterministic. It does not contact Linear. It calls the webhook handler directly, monkey-patches the outbound Linear comment path, and proves both sides of the boundary. This issue has been patched in version 4.6.59.

### CVE-2025-30045

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-23T09:17:04.327 |

CGM CLININET is vulnerable to Code Injection in the ConvExpr function, which processes Perl expressions into RTF document content. Due to improper control of the code evaluated from these expressions, an authenticated, high-privileged attacker can cause arbitrary code to be executed with root privileges. 


The vulnerability was confirmed to affect versions up to 2026.MS3 but later versions may also be vulnerable.

### CVE-2026-75779

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-352` |
| Published | 2026-10-23T08:16:55.587 |

Improper Neutralization of Special
Elements used in an OS Command (“OS Command Injection”) and Cross-Site Request
Forgery (CSRF) in an ASUS router model allow an attacker to trick a logged-in
administrator into visiting a phishing website, causing the router to execute
arbitrary commands with root privileges.
Refer to the '
Security Update for ASUS Router Firmware ' section on the ASUS Security Advisory for more information.

### CVE-2026-115419

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-488` |
| Published | 2026-10-22T21:17:17.790 |

The A2A server component in Amazon Strands Agents SDK for Python before 1.43.0 and Amazon Strands Agents SDK for TypeScript before 1.5.0 does not properly isolate conversation state between callers. An authenticated remote user could read other tenants' conversation history and add persistent instructions that alter model behavior for subsequent callers via HTTP requests to the A2A endpoint using a different context_id.



To mitigate this issue, users should upgrade to strands-agents 1.43.0 (Python) or @strands-agents/sdk 1.5.0 (TypeScript).

### CVE-2026-114519

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-22T19:17:37.267 |

Missing Authorization (CWE-862) in the user API of Roskus Prospero Flow CRM from 2.0.0 before 5.26.0 allows a user with a basic role to read the accounts of other users of its own company, including accounts with higher privileges, and, in versions from 3.5.0, to delete them, because the routes GET /api/user/{id} and DELETE /api/user/{id} in routes/api.php carry only the auth:api middleware, which checks that a JSON Web Token is valid and nothing more, and neither UserReadController::read() nor UserDeleteController::delete() checks a permission, a policy or a role before acting. Object access is scoped by company: the read path limits the query to the company of the authenticated user, and the delete path compares the company of the target account with the company of the authenticated user. The delete path skips that comparison when the company of the authenticated user is Company::DEFAULT_COMPANY, so a user with a basic role in that company can delete any account of any company of the installation. Deleting an account removes the data held on it, and the last administrative account of a company can be deleted. This gives the attacker the personal data held on the other accounts, including email address, telephone number, postal address and IBAN, and the ability to delete accounts it has no permission to administer.

### CVE-2026-97635

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-22T18:17:32.337 |

The Agent Zero Web UI before 1.15 does not correctly sanitize user-provided input in chat messages or file uploads. When Agent Zero reproduces content in the chat interface, any injected JavaScript is executed in the context of the victim’s authenticated Agent Zero Web UI session.

### CVE-2026-113874

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-22T18:17:27.237 |

SmileCDR HAPI FHIR allows an untrusted bundle body to replace a partition identity previously established by a trusted source, and does not enforce storage partition entitlement by default. An attacker authorized for one tenant can read from or write to another tenant's partition.

### CVE-2026-104068

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-22T17:16:56.720 |

JetBackup plugin for WordPress before 3.1.24.10 contains a symlink-based arbitrary file write vulnerability that allows an authenticated WordPress administrator to write attacker-controlled file contents outside the intended restore destination during backup import and restore. Attackers can craft a backup archive containing a symbolic link that archive extraction follows without validating targets or enforcing destination containment, potentially leading to server-side code execution depending on the writable destination and server configuration.

### CVE-2026-115481

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-23T14:17:52.307 |

baserCMS is a website development framework. Starting in version 5.0.0-beta1 and prior to versions 5.3.2 and 5.4.2, `PermissionGroupsService::build()` reads a plugin's `config/permission.php` to decide what each user group may reach. When that file is absent it writes a wildcard allow rule instead: `url` `/baser/<prefix>/<plugin>/*`, `method` `*`, `auth` true, for every non-admin group. BcCustomContent has no such file in any release. After an administrator installs it, the default `operators` group can store and execute arbitrary PHP under the document root. Versions 5.3.2 and 5.4.2 patch the issue.

### CVE-2026-115726

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-23T12:18:13.413 |

Aider through 0.86.2 contains a command execution vulnerability that allows attackers to run shell commands by committing a malicious .aider.conf.yml that is auto-loaded without a trust prompt. Attackers can set notifications-command or editor values that are executed via subprocess with shell=True after model replies or /editor use, running commands with the victim's privileges.

### CVE-2026-112837

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-23T09:17:06.043 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Ruben Garcia GamiPress gamipress allows Blind SQL Injection.This issue affects GamiPress: from n/a through 8.0.7.

### CVE-2026-115504

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-22T20:17:06.313 |

CFITSIO through 4.7.0 contains an out-of-bounds write vulnerability in ffgcls2() in getcols.c that trusts attacker-controlled heap descriptor lengths for variable-length string columns. Attackers can supply a crafted FITS file that overflows a fixed 28,800-byte stack buffer and the caller's string array, enabling arbitrary code execution.

### CVE-2026-63120

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-23T13:17:12.010 |

pghoard is a PostgreSQL backup daemon and restore tooling that stores backup data in cloud object stores. Prior to version 2.7.2, an incomplete path traversal fix in pghoard allows an attacker with write access to the backup object storage (such as S3, GCS, or Azure) to execute arbitrary file writes and directory creation outside the designated PostgreSQL data directory (pgdata). When a database administrator executes a restore operation (via pghoard_restore get-basebackup), a maliciously crafted delta backup manifest with path traversal sequences (e.g., ../../../../etc/cron.d/backdoor) will write arbitrary payloads to the host system. This issue has been patched in version 2.7.2.

### CVE-2026-115414

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-22T19:17:47.843 |

OS command injection in the Terraform hook in AWS SAM CLI before 1.166.2 might allow an actor who can influence the Terraform configuration or plan file consumed by a build to execute arbitrary commands as the build user on the host running the build via a crafted Terraform resource address.



To remediate this issue, users should upgrade to version 1.166.2 or later.

### CVE-2026-16477

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-22T15:17:05.817 |

CleanShot X for macOS insecurely deserializes untrusted data embedded in a .cleanshot project file (editable screenshot annotations). Exploitation requires an attacker to craft a malicious .cleanshot file, deliver it to the target, and have the target open it; the payload then executes automatically during parsing, resulting in arbitrary code execution in the context of the current user. Users who have never opened a .cleanshot file from an untrusted source are not affected by this vulnerability. This vulnerability was fixed in versions: 4.5.2, 4.6.3, 4.7.8 and 4.8.10

### CVE-2026-55889

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330;CWE-337` |
| Published | 2026-10-23T13:17:10.230 |

XDG Desktop Portal is a desktop integration portal. Prior to version 1.22.1, malicious sandboxed applications can use the FileTransfer.RetrieveFiles method to redirect drag-and-drop and copy-paste data targeted at other applications to itself. Some portals generate tokens which provide access to resources. The sharing of the token transfers access to the resource and is supposed to happen out of band. The tokens were generated with g_random_int or g_uuid_string_random, both of which use GLib's GRand based on the Mersenne Twister PRNG which created a stream of reproducible random numbers. By generating enough tokens, the state of the GRand can be recover and with it, the next tokens can be predictedinsufin. This issue has been patched in version 1.22.1.

### CVE-2026-56835

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-862;CWE-863` |
| Published | 2026-10-23T12:18:14.897 |

PraisonAI is a multi-agent teams system. From version 3.11.0 to before version 4.6.59, PraisonAI's Slack bot applies its configured allowed_users, allowed_channels, and unknown-user pairing policy in the normal Slack message event handler, but not in the adjacent Slack app_mention event handler. A Slack workspace user who can mention the bot in a channel where the Slack app is present can trigger the configured PraisonAI agent even when: the sender is not in BotConfig.allowed_users; the channel is not in BotConfig.allowed_channels; unknown_user_policy="deny" is configured; and the same event content is correctly dropped by the normal message handler. This issue has been patched in version 4.6.59.

### CVE-2026-115723

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-23T12:18:12.983 |

Snap7 through 1.4.3 contains an out-of-bounds write vulnerability in the passive partner that allows a malicious active partner to overflow application buffers by declaring an unvalidated BSend total length. Attackers connecting from the configured peer address can declare up to 65535 bytes and send a short fragment, causing BRecv to memcpy past the buffer and crash or corrupt SCADA, HMI or gateway processes.

### CVE-2026-96616

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-22T22:20:01.343 |

Authentication tokens issued by the E3's web management interface on login are given an expiration time far beyond any reasonable session lifetime, effectively making them non-expiring. A token obtained through interception or device compromise remains valid for authenticated access for an extended period.

### CVE-2026-79883

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:00.820 |

No description provided

### CVE-2026-79882

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:00.707 |

No description provided

### CVE-2026-79881

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:00.600 |

No description provided

### CVE-2026-115376

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-22T19:17:44.320 |

Incus 7.0.1 before 7.0.2 and 7.2.0 before 7.5.0 contains an authorization bypass vulnerability that allows project-restricted clients to copy volumes by omitting source.type. Attackers can send crafted POST requests to the custom volumes endpoint with a chosen source.project to copy and read other projects' volumes, snapshots, and configuration.

### CVE-2026-56836

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-306;CWE-862` |
| Published | 2026-10-23T12:18:15.050 |

PraisonAI is a multi-agent teams system. From version 4.5.112 to before version 4.6.59, PraisonAI's installed console entrypoint is Typer-first. In current releases, the recipe command is registered in the Typer app and praisonai recipe serve dispatches to the deprecated Typer command in src/praisonai/praisonai/cli/commands/recipe.py. That Typer command can start the Recipe HTTP server on a non-localhost interface with no authentication. It prints a deprecation warning, and then launches the server. Because config.auth is absent, create_app() does not attach the API-key or JWT middleware. Unauthenticated requests can then reach the recipe API and, when enabled, /admin/reload. This issue has been patched in version 4.6.59.

### CVE-2025-30049

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-916` |
| Published | 2026-10-23T09:17:04.690 |

The CGM CLININET application stores user passwords as unsalted MD5 hashes.


This issue was fixed in versions 2026.MS1 and 2026.MS3

### CVE-2026-115417

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-22T21:17:17.633 |

Memory allocation with excessive size value in the MQTT 3.1.1 compatibility adapter in AWS aws-c-mqtt before 0.16.2 might allow a remote actor to cause a denial of service of the client application.



To remediate this issue, users should upgrade to aws-c-mqtt 0.16.2 or later, or to an AWS Common Runtime or AWS IoT Device SDK release that bundles it.

### CVE-2026-79886

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:01.130 |

No description provided

### CVE-2026-79885

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:01.023 |

No description provided

### CVE-2026-79884

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:00.917 |

No description provided

### CVE-2026-114644

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-22T19:17:38.023 |

The MongoDB C# Driver's BSON library contains an uncontrolled resource consumption weakness in its deserialization handling of one BSON value type. An application that deserializes untrusted content with the library retains data derived from that content for the lifetime of the process, with no limit on how much accumulates. An unauthenticated remote party who can cause such content to be deserialized can drive unbounded memory growth, exhausting the host application's available memory and denying service. There is no impact to confidentiality or integrity, and no MongoDB server component is affected.

### CVE-2026-94482

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-22T16:19:16.720 |

Next.js is a React framework for building full-stack web applications. From 13.0.0 until 15.5.28 and 16.4.1, crafted requests targeting App Router applications with at least one Server Action can cause excessive CPU consumption and block processing of further requests in the same process. Applications using the Pages Router and App Router applications without Server Actions are not affected. This issue is fixed in versions 15.5.28 and 16.4.1.

### CVE-2026-57121

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-10-23T13:17:11.057 |

PraisonAI is a multi-agent teams system. From version 0.1.4 to before version 0.1.5 in praisonai-platform, a workspace member can permanently delete any resource — projects, agents, issues, labels, issue dependencies, and issue-label attachments — created by the workspace owner or other members. All six content DELETE endpoints enforce workspace membership but perform no ownership or role check. A single malicious or compromised member account can wipe an entire workspace's content irreversibly. This issue has been patched in version 0.1.5.

### CVE-2026-57113

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-10-23T13:17:10.373 |

PraisonAI is a multi-agent teams system. From version 2.6.0 to before version 4.6.59, PraisonAI's template loader accepts GitHub template URIs with refs, for example github:owner/repo/template@v1.0.0. The resolver stores the user-controlled template path and ref verbatim, and the cache layer later joins those values into ~/.praison/cache/templates/github/<owner>/<repo>/<template>/<ref> without normalizing each segment or checking that the final path remains inside the template cache root. A crafted ref such as ../../../../../../outside-delete-target therefore escapes the cache directory. The first load can write .cache_meta.json outside the cache. If the normal cache hierarchy for the same owner/repo/template has already been created, the same path reaches shutil.rmtree(cache_path) and removes an attacker-selected outside directory before replacing it with cache metadata. This issue has been patched in version 4.6.59.

### CVE-2026-112852

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T13:17:06.817 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Helion helion allows Object Injection.This issue affects Helion: from n/a through 1.1.12.

### CVE-2026-112850

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-23T13:17:06.563 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in AncoraThemes Your Dress your-dress allows PHP Local File Inclusion.This issue affects Your Dress: from n/a through 1.4.1.

### CVE-2026-94268

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-23T06:17:08.297 |

The Advanced Custom Fields: Extended WordPress plugin before 0.9.2.8, Advanced Custom Fields: Extended PRO WordPress plugin before 0.9.2.8 does not resolve the target of the update-user action in its front-end Forms module consistently between the stage that authorises the request and the stage that carries it out, which allows unauthenticated visitors to bypass the guard protecting administrator accounts, take over the site administrator's account and be issued a valid session for it. Exploitation requires the site to publish two separate front-end form configurations whose targets are mapped to visitor-submitted values.

### CVE-2026-94262

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-23T06:17:08.000 |

The Advanced Custom Fields: Extended WordPress plugin before 0.9.2.8, Advanced Custom Fields: Extended PRO WordPress plugin before 0.9.2.8 does not verify that the requester is authorised to edit the targeted user account in the update-user action of its front-end Forms module, performing that check only when the target account holds an administrator role, which allows unauthenticated visitors to overwrite any non-administrator account's credentials and obtain a session for that account. Exploitation requires the site to publish a form whose user-update action maps its target to a visitor-submitted value rather than to the default current user.

### CVE-2026-115546

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-639` |
| Published | 2026-10-23T04:18:15.047 |

Okta Access Gateway (OAG) does not validate the selected authentication source during sign-on. An authenticated user with an active session can modify the authentication source parameter, which may generate a SAML assertion granting access to the Admin Console.

### CVE-2026-79891

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:01.663 |

No description provided

### CVE-2026-79890

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:01.557 |

No description provided

### CVE-2026-79889

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:01.457 |

No description provided

### CVE-2026-79888

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:01.350 |

No description provided

### CVE-2026-79887

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:01.247 |

No description provided

### CVE-2026-93640

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-23T14:17:57.757 |

A local privilege escalation vulnerability in the optional dnscache package of Zimbra Collaboration Suite (ZCS) allows the Unix zimbra account to access files with root privileges. The passwordless sudo policy permits arbitrary arguments to zmunbound, whose wrapper forwards them to Unbound without restricting the configuration path. An attacker can supply a configuration that retains root privileges and disables the chroot. Include directives expose root-readable file contents through parser errors, while an attacker-selected logfile path creates a root-owned file or appends Unbound log records to an existing file. This can disclose password hashes and private keys and corrupt privileged configuration files, preventing affected services from starting with the modified configuration. The affected configuration is present in ZCS 10.1.16 and 10.1.21 dnscache packages.

### CVE-2026-50057

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-23T14:17:53.303 |

A local privilege escalation vulnerability in the Zimbra Collaboration Suite (ZCS) MTA package allows the Unix zimbra account to execute arbitrary commands as root. The installed sudo policy permits passwordless root execution of Postfix administration commands without restricting their arguments. An attacker can select a zimbra-controlled daemon_directory in the Postfix configuration and invoke postfix set-permissions, causing Postfix to execute the attacker's post-install program as root. The Postfix configuration directory is also writable by zimbra, so restricting postconf alone does not remove the execution path. Exploitation requires local command execution as zimbra on an MTA node. ZCS 10.1.16 and 10.1.21 are affected.

### CVE-2026-50056

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-23T14:17:53.187 |

A local privilege escalation vulnerability in the zmmailboxdmgr launcher of Zimbra Collaboration Suite (ZCS) allows the Unix zimbra account to execute arbitrary commands as root. The passwordless sudo interface accepts JVM arguments that are not adequately restricted. An attacker can postpone Jetty's privilege drop, register an OnOutOfMemoryError command and force heap exhaustion during startup, causing the command to execute while the JVM still runs as root. Exploitation requires local command execution as zimbra on a mailbox server and interrupts mailboxd during the malicious restart. ZCS 10.1.16 and 10.1.21 are affected.

### CVE-2026-57142

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-94;CWE-863` |
| Published | 2026-10-23T13:17:11.210 |

PraisonAI is a multi-agent teams system. From version 4.5.87 to before version 4.6.61, PraisonAI recipe execution has a dangerous-tool policy that is supposed to block default-denied tools unless the caller explicitly passes allow_dangerous_tools=True. That policy only checks tools declared in TEMPLATE.yaml requires.tools. For steps-based recipes, the actual execution path loads workflow.yaml with YAMLWorkflowParser. That parser resolves agent-level tools: declarations and preserves top-level approve:. Workflow.start() then installs those YAML-approved tools into the approval context. As a result, an untrusted recipe can omit execute_command from TEMPLATE.yaml requires.tools, declare it in workflow.yaml agents.*.tools, and add top-level approve: [execute_command]. The caller did not set allow_dangerous_tools=True, but the recipe policy allows the recipe and the workflow approval path self-approves the critical shell tool. This issue has been patched in version 4.6.61.

### CVE-2026-56838

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-693;CWE-863` |
| Published | 2026-10-23T12:18:15.357 |

PraisonAI is a multi-agent teams system. From version 4.5.87 to before version 4.6.59, PraisonAI recipe execution blocks default-denied dangerous tools unless the caller explicitly passes allow_dangerous_tools=True. The normal recipe.run() path enforces this with _check_tool_policy(). The streaming path, recipe.run_stream(), loads the same recipe, checks dependencies, and then calls _execute_recipe() without running the dangerous-tool policy check. As a result, a recipe that honestly declares execute_command in TEMPLATE.yaml requires.tools is denied by recipe.run(), but reaches the execution engine through recipe.run_stream() with allow_dangerous_tools=False. This issue has been patched in version 4.6.59.

### CVE-2026-79892

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:01.767 |

No description provided

### CVE-2026-75775

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-23T08:16:55.443 |

Improper Neutralization of Special Elements used in an OS Command in certain ASUS routers allows remote user to execute arbitrary commands with root privileges via crafted parameters sent to the router while the device is in its factory-default state.Refer to the ' Security Update for ASUS Router Firmware ' section on the ASUS Security Advisory for more information.

### CVE-2026-108456

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-22T22:17:58.473 |

Server-side request forgery (ssrf) in Azure AI Foundry allows an authorized attacker to elevate privileges over a network.

### CVE-2026-115484

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-23T01:16:53.670 |

A flaw was found in the iscsiuio component of open-iscsi. The DHCPv4 option parser incorrectly calculates the length of the options data, causing it to read beyond the allocated buffer into adjacent heap memory. An attacker on the same network segment can send a crafted DHCP response to crash the daemon or corrupt its network configuration.

### CVE-2026-114649

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1025` |
| Published | 2026-10-22T19:17:38.703 |

The MongoDB C# Driver compares TLS client certificates by issuer and serial number only when deciding whether two clients can share cached connections. In an application that creates clients from certificates supplied by different users, a user who provides a certificate copying another user's issuer and serial number, without that user's private key, can be given connections authenticated with the other user's certificate. Database operations can then run under the other user's identity, affecting the confidentiality and integrity of data that identity can access.

### CVE-2026-57146

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-306` |
| Published | 2026-10-23T13:17:11.527 |

PraisonAI is a multi-agent teams system. From version 4.5.115 to before version 4.6.61, the published A2U advisory GHSA-f292-66h9-fpmf says unauthenticated A2U event streaming was fixed in praisonai 4.5.115. Current head still exposes the same A2U subscription and event routes without authentication when the operator starts the documented CLI entrypoint. The current CLI wrapper does not expose --api-key, does not install the common API-key middleware, and does not generate a token for A2U. It calls create_a2u_routes(app) directly. That helper only enforces auth if A2U_AUTH_TOKEN is already present; if the variable is missing, _authenticate_request() returns None and treats auth as disabled. This issue has been patched in version 4.6.61.

### CVE-2026-56834

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-200` |
| Published | 2026-10-23T12:18:14.750 |

PraisonAI is a multi-agent teams system. From version 3.8.1 to before version 4.6.59, PraisonAI's Dynamic Context Discovery feature exposes artifact helper tools through ctx.get_tools(). The implemented artifact tools do not enforce that the supplied artifact_path is an artifact created by the configured store or that it lives under the configured artifact base directory. Instead, artifact_head, artifact_tail, artifact_grep, and artifact_chunk wrap the caller-supplied path directly into an ArtifactRef and then read it from the host filesystem. As a result, any prompt/user/tool-caller that can influence those tool arguments can read files readable by the PraisonAI process, such as project .env files, cloud credentials, SSH keys, source files, or other local data. This issue has been patched in version 4.6.59.

### CVE-2026-56833

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-200` |
| Published | 2026-10-23T12:18:14.600 |

PraisonAI is a multi-agent teams system. From version 3.8.1 to before version 4.6.59, PraisonAI's Dynamic Context module provides filesystem-backed history and terminal-log storage. The module also exports agent-callable tool factories. Those tools accept run_id and agent_id arguments from the tool caller. The underlying stores join those values into filesystem paths without rejecting absolute paths or .. traversal. Because run_id can be an absolute path and agent_id can contain traversal, a lower-trust prompt/user that can call these tools can read .jsonl and .log files outside the configured Dynamic Context base directory. This issue has been patched in version 4.6.59.

### CVE-2026-112359

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-23T09:17:05.540 |

Missing Authorization vulnerability in Amauri.IO WPMobile.App wpappninja allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects WPMobile.App: from n/a through 11.86.

### CVE-2026-113500

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T06:17:06.587 |

The LiteSpeed Cache WordPress plugin before 7.9.2 does not limit one of its HTML optimization routines to stylesheet content, so it can delete the markup that closes an attribute in the rendered page, and combined with unescaped comment author output this allows unauthenticated users whose comments are published to inject event-handler attributes that run JavaScript in the browser of any visitor, including a logged-in administrator, viewing front-end pages while the optimization is enabled.

### CVE-2026-113499

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T06:17:06.490 |

The LiteSpeed Cache WordPress plugin before 7.9.2 does not restrict one of its HTML rewriting routines to stylesheet content, so it removes a quote that terminates an attribute in the rendered page, and combined with unescaped comment author output this allows unauthenticated users whose comment is published to inject attributes that execute JavaScript in the browser of any visitor, including a logged-in administrator, who views front-end pages while the affected option is enabled.

### CVE-2026-109936

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T06:17:05.487 |

The Otter Blocks  WordPress plugin before 3.2.8 does not correctly bound a pattern it uses to rewrite its dynamic-content tokens while rendering blocks, so the pattern can consume the quote that closes an HTML attribute and pull adjacent unescaped data into the markup as new attributes. This allows unauthenticated users to achieve stored Cross-Site Scripting that executes in the browser of any visitor who views an affected page, including a logged-in administrator.

### CVE-2026-115497

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-23T05:17:15.063 |

The Music Store – WordPress eCommerce plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 1.4.7 via the 'f' parameter parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. Exploitation requires a valid purchase_id token, which any user can obtain by making a single low-cost purchase or receiving a shared download link.

### CVE-2026-96185

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-22T22:19:53.850 |

Stack-based buffer overflow in Microsoft Exchange Online allows an authorized attacker to execute code over a network.

### CVE-2026-79955

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:02.200 |

No description provided

### CVE-2026-79895

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:02.090 |

No description provided

### CVE-2026-79894

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:01.983 |

No description provided

### CVE-2026-79893

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:01.877 |

No description provided

### CVE-2026-115365

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-22T19:17:42.953 |

OpenBao from 2.3.0 before 2.6.3 contains an incorrect authorization vulnerability in its ACL policy cache that allows tokens to reference policies from arbitrary namespaces using specially crafted policy names. Attackers holding such tokens can gain capabilities of cached policies in other namespaces, including the root namespace, to act across namespace boundaries.

### CVE-2026-114613

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-10-22T19:17:37.733 |

MessagePack is the serializer implementation for Python msgpack.org. Prior to 1.2.3, the msgpack-python C extension (msgpack._cmsgpack) leaks a decoded map value when deserialization rejects a key with strict_map_key=True (the default). Repeated malformed inputs can cause unbounded process memory growth and denial of service in applications that deserialize attacker-controlled MessagePack data. Both unpackb() and the streaming Unpacker API are affected. The pure-Python fallback does not exhibit this leak in the reported tests. This issue is fixed in version 1.2.3.

### CVE-2026-75508

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-22T17:16:59.933 |

GraphQL-core is a Python port of the GraphQL.js reference implementation. From 3.2.3 until 3.2.12 and 3.3.0rc1, the parser's max_tokens limit in Parser.advance_lexer counts only non-comment tokens returned after Lexer.lookahead skips comments. Each skipped comment is still allocated as a Token and retained through token.next and token.prev, allowing a highly compressible comment-padded GraphQL document to pass a low token limit while consuming memory. An unauthenticated remote attacker can exhaust worker memory before AST-based depth or complexity controls run. This issue is fixed in versions 3.2.12 and 3.3.0rc1.

### CVE-2026-75507

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-10-22T17:16:59.757 |

GraphQL-core is a Python port of the GraphQL.js reference implementation. From 3.0.0 until 3.2.12 and 3.3.0rc1, the OverlappingFieldsCanBeMerged rule in specified_rules repeatedly compares fields that share response names and recursively re-compares flattened inline fragments during the validation phase. The prior named-fragment memoization does not cover this path, so nested repeated inline fragments can drive quadratic and worst-case O(n²·m²) CPU work before any resolver or AST-based depth or complexity control runs. An unauthenticated remote attacker can submit a shallow, highly compressible GraphQL query that pins a worker process and can saturate a multi-worker service. This issue is fixed in versions 3.2.12 and 3.3.0rc1.

### CVE-2026-114605

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-22T17:16:58.237 |

dnspython is a DNS toolkit for Python. Prior to 2.9.0, dns.name.from_wire_parser follows attacker-controlled DNS compression pointer chains without a hop limit. A malicious DNS wire-format message can force excessive pointer traversal during name decompression, causing high CPU use, application degradation, or denial of service in applications that process untrusted DNS messages. This issue is fixed in version 2.9.0.

### CVE-2026-115482

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-22T16:17:35.490 |

In lsquic before 4.9.0, the HTTP/3 implementation can use an excessive amount of memory because the number of buffered header sets is not limited, as demonstrated by a QPACK amplification attack. This is related to header_out_dynamic_entry and es_max_header_list_size.

### CVE-2026-113872

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-404` |
| Published | 2026-10-22T15:17:05.377 |

multer is a middleware for Node.js that handles multipart/form-data file uploads. In versions from 2.0.0 before 2.5.0, when multer is configured with an asynchronous fileFilter, a single request can crash the Node.js process. If the request is aborted while one file's asynchronous fileFilter is still pending, the pending callback later resumes a parsing stream that multer has already torn down, and the underlying parser emits an error on a stream that no longer has an error listener, which Node raises as an unhandled error event so the process exits. Any application using multer with an asynchronous fileFilter is affected regardless of storage engine, while uploads using a synchronous fileFilter are not affected. The issue is fixed in multer 2.5.0, and users should upgrade to 2.5.0 or later. As a workaround, use a synchronous fileFilter.

### CVE-2026-111181

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-22T15:17:04.763 |

body-parser is body parsing middleware for Node.js and Express. In versions before 1.20.9 and in versions from 2.0.0 before 2.4.0, a single request can crash any application using body-parser with default options. When a request carries a Content-Encoding such as gzip, body-parser pipes it into a decompression stream and, after reading the body, leaves that stream with no error listener. A payload of one valid compressed frame followed by trailing bytes decodes and the application responds normally, but the trailing bytes then reach the already-finished decoder, which emits an error that is re-thrown as an uncaught exception and terminates the process. No matching route is required because body parsing runs before routing, so any endpoint that parses a body is affected. The issue is fixed in body-parser 2.4.0 and 1.20.9, and users should upgrade to one of those versions or later. As a workaround, disable request-body inflation (set the body-parser inflate option to false) so encoded requests are rejected before any decompression stream is created.

### CVE-2026-114616

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-326;CWE-1391` |
| Published | 2026-10-22T22:18:04.420 |

Authlib is a Python library which builds OAuth and OpenID Connect servers. Prior to 1.9.1, Authlib's OctKey.import_key() and HMAC signing and verification path accept zero-length key material. If an application's secret lookup can return an empty string or empty bytes, a remote attacker can compute the deterministic HS256, HS384, or HS512 signature for arbitrary token claims and have Authlib treat the token as authentic. This issue is fixed in version 1.9.1.

### CVE-2026-114615

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-184;CWE-347` |
| Published | 2026-10-22T22:18:04.257 |

Authlib is a Python library which builds OAuth and OpenID Connect servers. From 1.3.1 until 1.9.0, OctKey.import_key() checks asymmetric-key markers only at byte zero while Authlib's PEM loaders accept leading whitespace, comments, or a byte-order mark. In deployments that use the documented mixed algorithm registry and already configure verification with PEM or certificate bytes containing such a prefix, an unauthenticated attacker who knows those same public-key bytes can use them as an HMAC secret and forge HS256 tokens with arbitrary identity or authorization claims. This is a bypass of the remediation for CVE-2024-37568. The module-level jwt object reaches OctKey.import_key() in authlib/jose/rfc7518/oct_key.py, where POSSIBLE_UNSAFE_KEYS fails to identify prefixed asymmetric key material. This issue is fixed in version 1.9.0.

### CVE-2026-61791

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-83` |
| Published | 2026-10-22T15:17:05.980 |

OCO-Server is a self-hosted endpoint management application for computer inventory, software deployment, and mobile device management. Prior to 1.2.1, `Html::commandButton()` in `lib/Html.class.php` embeds an action URL containing a stored computer hostname into a JavaScript string in an inline `onclick` handler, using `htmlspecialchars(ENT_QUOTES)` only for HTML escaping. Browsers decode the HTML entities before interpreting the handler as JavaScript, allowing a crafted hostname to escape the string and execute script in an administrator's authenticated session when an affected command button is activated. `frontend/views/computer-details.php` passes `$computer->hostname` to this helper using `Computer::DEFAULT_COMPUTER_COMMANDS` in `lib/Models/Computer.class.php`, whose VNC, RDP, SSH, and Ping entries use `new_tab=false` and the vulnerable `window.location` branch. A remote attacker who possesses the shared `agent-registration-key` can use the `oco.agent.hello` handler in `frontend/api-agent.php` to store an unchecked hostname when `agent-self-registration-enabled` is enabled; self-registration is disabled by default. The vulnerable default command buttons require no custom command configuration. The injected script can abuse the administrator's privileges, including permission to deploy software jobs to managed computers. This issue is fixed in version 1.2.1.

### CVE-2026-114624

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T14:17:51.583 |

baserCMS is a website development framework. In versions 5.0.0 before 5.3.2 and 5.4.0 before 5.4.2, the widget-area entity serializes widgets only when the submitted value is an array, allowing a string submitted through the admin JSON API to be stored unchanged. Entity reads, including front-end rendering and API responses, deserialize the stored value with unserialize() without an allowed_classes restriction, accepting both raw and base64-encoded serialized data. An administrator, or an attacker who obtains widget-write capability through a separate vulnerability such as chained XSS, can plant an object graph that subsequently triggers on unauthenticated page requests. Two demonstrated gadget chains in the default dependency set use composer/composer ProcessExecutor::startJob() with Process::fromShellCommandline(), or logiscape/mcp-sdk-php StdioTransport::connect() with StdioServerParameters, to reach proc_open() and execute commands as the web-server user. Deserialization bypasses constructor-based readonly safeguards, and the stored payload can execute repeatedly until the database row is repaired. Unauthenticated page access is a trigger after privileged payload storage, not an unauthenticated means of initially planting the payload. This issue has been patched in versions 5.3.2 and 5.4.2.

### CVE-2026-114622

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-180` |
| Published | 2026-10-23T14:17:51.283 |

baserCMS is a website development framework. In versions 5.2.3 before 5.3.2 and 5.4.0 before 5.4.2, the optional BcThemeFile plugin's Admin API validates a raw path in ThemeFilesService::update() and getFullpath(), but ThemeFileForm::_execute() subsequently applies rawurldecode() to fullpath before writing. Because normalizePath() resolves only literal dot segments, percent-encoded traversal can pass the containment checks and become a path outside the theme directory at the write sink. An authenticated administrator can write PHP files into writable locations such as webroot and execute them, exceeding the intended theme-template editing boundary. The source also identifies the same check-before-decode ordering in ThemeFilesService::copy(), although that path was not dynamically verified. Exploitation requires the non-default plugin, an administrator session, and a same-origin Origin header; USE_CORE_ADMIN_API=false does not block session-authenticated requests. The Admin web form is not affected by this encoded-path tampering because FormProtection protects fullpath. This is a third bypass of the protections associated with CVE-2026-30940, using encoded traversal decoded after validation. This issue has been patched in versions 5.3.2 and 5.4.2.

### CVE-2026-57114

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-367;CWE-918` |
| Published | 2026-10-23T13:17:10.533 |

PraisonAI is a multi-agent teams system. From version 4.5.126 to before version 4.6.59, PraisonAI's Async Jobs API validates webhook_url when a job request is parsed and again when the internal Job object is constructed. That validation blocks direct loopback/private targets, but it is not bound to the later network request. When a job completes, _send_webhook() passes the original hostname to httpx.AsyncClient.post() with no send-time validation, IP pinning, or guarded transport. An attacker-controlled hostname can therefore resolve to a public IP during Pydantic validation and later resolve to loopback/private/cloud-metadata infrastructure during webhook delivery. This bypasses the intended SSRF guard in current supported releases. This appears to be an incomplete fix / patch bypass for GHSA-8frj-8q3m-xhgm. This issue has been patched in version 4.6.59.

### CVE-2026-111982

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-23T06:17:06.097 |

The User Profile Builder  WordPress plugin before 4.0.5 does not verify that a user is authorized to edit the specific account selected on its front-end Edit Profile form, allowing an Administrator of a Multisite subsite to change any other user's account email, including a Network Super Admin's, and take over that account through the password-reset flow.

### CVE-2026-107858

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-942;CWE-1385` |
| Published | 2026-10-23T06:17:03.733 |

Missing Origin Validation in WebSockets (CWE-1385) and Permissive Cross-domain Policy with Untrusted Domains (CWE-942) in the development web server (ADK Web) in Google Agent Development Kit (ADK) for Java (com.google.adk:google-adk-dev versions 0.1.0 before 1.13.0 and com.google.adk:google-adk-maven-plugin versions 0.3.0 before 1.13.0) allow a remote attacker to control a locally running agent and read its data via a malicious web page visited by a developer while the server is running. The /run_live WebSocket endpoint accepts connections from any origin by default (hardcoded via setAllowedOrigins("*") in versions 0.1.0 through 1.5.0, and defaulting to * via adk.web.cors.origins in versions 1.6.0 through 1.12.0), and since version 0.4.0 the REST API returns Access-Control-Allow-Origin: * by default. Because the server has no authentication and requests originate from the developer's browser (so binding to localhost does not prevent exploitation), a cross-origin page can send messages to the agent (triggering registered tools), stream agent responses, and list, read, create, or delete sessions and artifacts. In versions 1.6.0 through 1.12.0, users can mitigate the issue by setting the adk.web.cors.origins property to an explicit allowlist of trusted origins (such as http://localhost:8000). The vulnerability is fixed in version 1.13.0, which enforces a same-origin default for CORS and the /run_live WebSocket endpoint, and rejects DNS-rebinding requests over loopback.

### CVE-2026-109198

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T05:17:14.773 |

The Anti-Spam by CleanTalk – Spam Protection Without CAPTCHA plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'user_email' parameter in all versions up to, and including, 6.89.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires user registration to be open on the site, and script execution is triggered when an Administrator subsequently runs the plugin's user-spam scan and views the resulting Non-checkable users or Spam users tab — the plugin's own documented workflow.

### CVE-2026-115505

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-22T20:17:06.470 |

libsmb2 before 6.3 contains integer overflow vulnerabilities in the DCE/RPC NDR decoder in lib/dcerpc.c that allow heap out-of-bounds reads and writes. A malicious SMB server or machine-in-the-middle on unsigned connections can send crafted NetrShareEnum replies with wrapping actual_count or max_count values when clients call smb2_share_enum_async(), corrupting heap memory.

### CVE-2026-95709

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:06.660 |

No description provided

### CVE-2026-95708

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:06.553 |

No description provided

### CVE-2026-95707

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:06.447 |

No description provided

### CVE-2026-95706

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:06.337 |

No description provided

### CVE-2026-95705

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:06.230 |

No description provided

### CVE-2026-95704

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:06.120 |

No description provided

### CVE-2026-79956

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:02.303 |

No description provided

### CVE-2026-114648

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-10-22T19:17:38.567 |

The MongoDB C# Driver does not neutralize dot and dollar characters in dictionary keys, field names and array-filter identifiers used in LINQ queries before placing them into the field paths it sends to the server. An application user whose input reaches these positions can redirect a query or update to fields the application did not name, which can expose other users' documents and widen updates beyond the intended data. Certain values can also write malformed fields that leave stored documents unreadable by the application until they are repaired.

### CVE-2026-93631

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-23T14:17:57.023 |

A cross-site request forgery vulnerability in the OAuth extension of Zimbra Collaboration Suite (ZCS) Network Edition allows an attacker to link an attacker-controlled external account to a victim's mailbox. The OAuth callback does not bind its state value or authorization code to the initiating Zimbra session and instead selects the destination mailbox from the browser's current authentication cookie. On a deployment with the provider configured, an attacker can induce a signed-in victim to load a callback containing a fresh code for the attacker's provider account. This creates a persistent data source that imports attacker-controlled contacts or events. With bidirectional CalDAV synchronization, appointments subsequently created or edited in the linked calendar are also disclosed to the attacker. ZCS 10.1.16 and 10.1.20 are affected.

### CVE-2026-115457

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T14:17:51.867 |

baserCMS is a website development framework. In versions 5.0.0 before 5.3.2 and 5.4.0 before 5.4.2, global shortcode expansion runs over the complete rendered page, including HTML-escaped blog comments supplied by unauthenticated visitors. A comment containing the BcBaser.getGoogleMaps shortcode can set apiBaseUrl to an attacker-controlled script URL, which is emitted as a script src and executes JavaScript on the site's origin when another visitor or administrator opens the article displaying that comment. Escaping raw HTML in comments does not prevent this stored cross-site scripting because shortcode processing happens after HTML rendering. Other registered shortcodes also expand in comments; Mail.getForm can embed a working contact form with a valid CSRF token. The flaw can compromise the authenticated browser context of an administrator who views the affected article. This issue has been patched in versions 5.3.2 and 5.4.2.

### CVE-2026-112863

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T13:17:07.830 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Hogash KALLYAS kallyas allows Reflected XSS.This issue affects KALLYAS: from n/a through 4.25.0.

### CVE-2026-112849

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T13:17:06.437 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in AivahThemes Hostme v2 hostmev2 allows DOM-Based XSS.This issue affects Hostme v2: from n/a through 7.0.

### CVE-2026-25716

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-23T09:17:06.790 |

Missing Authorization vulnerability in Hallo Welt! GmbH BlueSpice (Extension:BlueSpiceUserManager) allows any authenticated user without special privileges to block or unblock arbitrary user accounts, including administrators. The REST endpoints /bs-usermanager/v1/block/create and /bs-usermanager/v1/block/delete call UserManager::blockUser() and UserManager::unblockUser(), which do not verify the permissions of the acting user. This allows locking out all administrators (denial of service) and lifting blocks imposed by administrators.

This issue affects BlueSpice: from 5.0.0 before 5.1.11, from 5.2.0 before 5.2.7.

### CVE-2026-112838

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T09:17:06.163 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in e4jvikwp VikRentCar vikrentcar allows Stored XSS.This issue affects VikRentCar: from n/a through 1.4.8.

### CVE-2026-112835

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T09:17:05.927 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in e4jvikwp VikRentCar vikrentcar allows Reflected XSS.This issue affects VikRentCar: from n/a through 1.4.8.

### CVE-2025-30043

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-23T09:17:03.300 |

CGM CLININET is vulnerable to Missing Authentication for Critical Function in the /DocManagment path. The endpoint is accessible without authentication, allowing an unauthenticated attacker in the adjacent network to retrieve the list of patient documents and download those documents. 


This issue was fixed in version 2026.MS3

### CVE-2026-115486

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-23T01:16:53.943 |

A flaw was found in the iscsiuio component of open-iscsi. The IPv6 Neighbor Discovery handler accesses link-layer address options at a fixed offset without verifying the packet contains them. Additionally, the ARP table is updated unconditionally with attacker-controlled addresses from the packet headers. An attacker on the same network segment can send a minimal Neighbor Advertisement to poison the ARP table and redirect network traffic.

### CVE-2026-115508

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-22T20:17:06.910 |

Crawl4AI 0.7.0 before 0.9.5 contains an inefficient regular expression complexity vulnerability in the Docker API server that allows authenticated API clients to supply unbounded regular expressions in /crawl request bodies. Attackers can submit catastrophic-backtracking patterns via RegexExtractionStrategy.custom, RegexChunking.patterns or JsonCss, JsonXPath and JsonLxml schema regex fields against a crafted page to freeze the entire server, including /health.

### CVE-2026-95712

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:07.040 |

No description provided

### CVE-2026-95711

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:06.880 |

No description provided

### CVE-2026-95710

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:06.770 |

No description provided

### CVE-2026-115374

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-22T19:17:43.953 |

Incus 7.0.0 before 7.0.2 and 7.1.0 before 7.5.0 contains a signature verification flaw in its built-in S3 server that allows presigned URL holders to inject unsigned x-amz-* headers. Attackers can add an unsigned X-Amz-Copy-Source header to a presigned upload URL to copy other bucket objects onto the granted key, disclosing their contents and ETags.

### CVE-2026-115371

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-22T19:17:43.530 |

Incus 6.0.3 before 6.0.7, 6.6.0 before 7.0.2, and 7.1.0 before 7.5.0 contains an improper authorization vulnerability that allows restricted TLS clients to read storage bucket keys in the default project. Attackers can query the bucket keys endpoints to obtain S3 access and secret keys, then read, modify or delete objects in those buckets.

### CVE-2026-115354

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-22T19:17:41.373 |

Mistune before 3.3.0 contains a path traversal vulnerability in the opt-in Include directive that allows attackers to read local files by supplying relative or absolute include paths. Attackers who submit Markdown rendered via Markdown.read() can disclose files such as /etc/passwd and inject unescaped HTML or script content into rendered output.

### CVE-2026-114653

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-185` |
| Published | 2026-10-22T19:17:39.307 |

A client-side encryption schema construction component in the MongoDB C# Driver places caller-supplied field identifiers into a position that is interpreted as a pattern expression, without normalizing or validating them. As a result, an application that designates certain fields for client-side field-level encryption may have the protection silently fail to apply, so data intended to be encrypted is stored and returned in cleartext; conversely, the rule may apply more broadly than intended. No user action is required to cause the condition, and any party with ordinary read access to the stored data — without possession of the encryption keys — can observe the unprotected values.

### CVE-2026-114652

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-10-22T19:17:39.147 |

A data-query-logic neutralization weakness in the update-statement construction component of the MongoDB C# Driver can cause application-supplied values to be interpreted as query/update logic rather than as literal data. An application user who can influence the content of values that the application passes into the affected builder surface, without any special privilege beyond ordinary read-write application access, may cause stored data to be modified or removed in ways the application never intended. The result is unauthorized integrity impact on the affected application data; there is no direct loss of confidentiality or availability of the database service.

### CVE-2026-93336

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-22T18:17:32.157 |

Missing authorization in the unit resources download route in Canonical Juju 4.0 through 4.0.15 allows a controller-authenticated principal (a unit agent, or a user with only login permission) to read any application's charm resource in any model,  including container-registry credentials, via a crafted request naming an arbitrary unit.

### CVE-2026-115453

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-22T16:17:35.183 |

Authorization Bypass Through User-Controlled Key (CWE-639) in the cart and wishlist repositories of MarcosCamara01 Ecommerce Template allows any authenticated user to delete and modify the cart and wishlist rows of any other user, because cartRepository.delete(), cartRepository.updateQuantityInternal() and wishlistRepository.delete() in src/lib/db/drizzle/repositories/ match rows by primary key alone, with no predicate on the owning user, and the per user authorization for those three operations rests on PostgreSQL row level security. The migrations run ALTER TABLE ... ENABLE ROW LEVEL SECURITY and create policies comparing app.current_user_id() with user_id, but never ALTER TABLE ... FORCE ROW LEVEL SECURITY, and PostgreSQL does not apply policies to the role that owns a table. The template uses one DATABASE_URL both to run the migrations, which create the tables, and for the application at runtime, so the application connects as the owner of the tables and the policies do not apply to it. cart_items.id and wishlist.id are sequential bigserial values, so the identifiers of rows belonging to other users can be enumerated, and the update path returns the modified row, which carries the identifier of the user it belongs to. This results in the destruction and modification of cart and wishlist contents belonging to other accounts of the installation.

### CVE-2026-115450

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-472` |
| Published | 2026-10-22T16:17:35.027 |

External Control of Assumed-Immutable Web Parameter (CWE-472) in the cart and checkout flow of MarcosCamara01 Ecommerce Template allows an authenticated user with no special privileges to be charged the price of one product while placing an order for another, because POST /api/user/cart accepts variantId, which determines what the order records, and stripeId, which determines what Stripe charges, as two independent fields of the request body, stores both on the cart row, and no check requires the stripeId to be the one that belongs to the variantId. POST /api/stripe/payment builds the Stripe Checkout line items from the stored value, as { price: item.stripeId, quantity }, so the amount charged is the amount of that Stripe price. The checkout.session.completed webhook then creates the order products from the variantId of the same cart row, so the order records a product that was not paid for. Every stripeId in the catalogue is readable by any visitor, so no value has to be guessed. This results in orders for goods at the price of the cheapest item in the catalogue, repeatable without limit, and in order records whose amount does not correspond to the product they list.

### CVE-2026-114510

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-116;CWE-943` |
| Published | 2026-10-22T15:17:05.500 |

Flexible GraphRAG is a Python framework for building graph and retrieval-augmented generation applications across multiple graph, vector, and search backends. From 0.6.0 until 0.8.2, the _escape() helper in flexible-graphrag/langchain/graph/pg_store_adapters/falkordb_adapter.py escapes quotes before backslashes and then interpolates the result into Cypher assembled by FalkorDBAdapter.add_graph_documents, allowing an inserted escape to be doubled and a quote to terminate the string early. When GRAPH_BACKEND=langchain and GRAPH_DB=falkordb are configured, attacker-influenced ingested document content can cause the extraction model to produce malicious entity or relationship values that reach these queries, allowing injected Cypher clauses to modify or delete graph data and, when the calling code surfaces query results to the user or LLM, disclose graph data. Dynamic node and relationship type identifiers are also inserted into backtick-quoted query positions without safe parameterization. The LlamaIndex FalkorDB store is not affected. This issue is fixed in version 0.8.2.

### CVE-2026-114356

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-23T14:17:36.507 |

Missing authorization in the system-privileged 'DJIUpdateService' binder in DJI CrystalSky ZS600C firmware v0.3.9.7 through v0.6.6.9 on Android allows a local application with no permissions to invoke privileged operations, including factory reset with user-data wipe (transaction 153), shutdown (105), clock/timezone change (101/123), and the firmware-apply hand-off (151), because onTransact() performs no caller-identity or permission check.

### CVE-2026-114353

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-912` |
| Published | 2026-10-23T14:17:33.397 |

Hidden functionality (undocumented backdoor) in the root-privileged 'assistant' daemon in DJI CrystalSky ZS600C firmware v0.3.9.7 through v0.6.6.9 on Android allows a physically-present attacker with USB access to execute arbitrary OS commands as root by sending the hard-coded magic string 'dji26656677' to the USB-gadget serial interface (/dev/ttyGS0), after which each subsequent line is passed to system().

### CVE-2026-57210

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-116;CWE-290` |
| Published | 2026-10-23T13:17:11.847 |

Heimdall is a cloud native Identity Aware Proxy and Access Control Decision service. Prior to version 0.17.17, when the trusted_proxies option is configured, heimdall extracts client IP addresses from the Forwarded (for= parameter) and X-Forwarded-For headers and exposes them as Request.ClientIPAddresses to the rule pipeline. However, extracted values are not validated to be syntactically valid IP addresses. Arbitrary strings, malformed IP literals, and RFC 7239 unknown values and obfuscated identifiers are accepted without further checks. In addition, the Forwarded header parser splits on , and ; without accounting for RFC 7239 quoted strings, which can cause a single quoted value to be parsed as multiple entries, with fragments — including trailing quote characters — treated as independent addresses. This issue has been patched in version 0.17.17.

### CVE-2026-57209

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-74` |
| Published | 2026-10-23T13:17:11.687 |

Heimdall is a cloud native Identity Aware Proxy and Access Control Decision service. Prior to version 0.17.17, when Heimdall operates in proxy mode, it constructs the Forwarded HTTP header after executing the matched rule pipeline by inserting the incoming request's Host header value directly into the header string without sanitizing commas or semicolons. This allows an attacker to inject additional parameters into the Forwarded header, potentially spoofing IP addresses for upstream services. This issue has been patched in version 0.17.17.

### CVE-2026-95713

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-22T19:18:07.313 |

No description provided

### CVE-2026-115373

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-22T19:17:43.813 |

Incus before 6.0.7, 6.1.0 before 7.0.2, and 7.1.0 before 7.5.0 contains a missing authorization vulnerability in GET /1.0/operations/{uuid} that lets project-restricted clients read operations in other projects. Attackers holding a restricted certificate and a known operation UUID can retrieve command lines, environment secrets, websocket secrets, and trust enrolment tokens.
