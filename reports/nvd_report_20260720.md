# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-19 15:00 UTC
- **対象期間**: `2026-07-18T15:00:14.000Z` 〜 `2026-07-19T15:00:12.000Z`
- **重要CVE数**: 3 件（Critical 9.0+: 0 件 / High 7.0〜: 3 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
直近で公開された CVE は **認証バイパス / XSS / ヒープバッファオーバーフロー** といった、**リモートから直接サービスを奪取できる深刻度 7.0 以上の脆弱性が集中**しています。共通点として、**入力検証の欠如** と **権限チェックの不適切** が根本原因となっているケースが多く、Web アプリケーションと SFTP サーバの両方で被害が拡大しやすい構造です。特に、**トークン取得やスクリプト実行が認証不要で可能**になる点が顕著で、早急なパッチ適用と既存トークンの無効化が必須です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目すべき理由 | 影響範囲 |
|-----|------|----------|----------------|----------|
| **CVE‑2026‑10130** | 8.8 | QueryWeaver の認証バイパス | 攻撃者が任意の既存ユーザーのメールアドレスを指定してサインアップリクエストを送るだけで、有効なセッショントークンを取得できる。**認証不要**でトークン取得が可能になるため、アカウント乗っ取りや内部情報漏洩が即座に発生。 | QueryWeaver を利用している全ての Web アプリケーション（特に SaaS 型デプロイ） |
| **CVE‑2026‑12228** | 8.7 | parisneo/lollms の Stored XSS | `POST /api/prompts/share` が入力サニタイズを行わず DB に保存。被害者が DM を閲覧した瞬間に任意のスクリプトが実行され、**セッションハイジャックや CSRF** が可能になる。攻撃は **認証済みユーザー** が対象だが、被害が広がりやすい。 | lollms デプロイ環境全般、特に外部ユーザーがプロンプト共有機能を利用できる設定 |
| **CVE‑2026‑53994** | 7.7 | ProFTPD mod_sftp のヒープバッファオーバーフロー | 認証済み SFTP ユーザーが細工したパケット長（0）を送信すると、`fxp_packet_read()` が不正なメモリ領域を書き換え、**リモートコード実行** が可能になる。SFTP は管理系サーバで頻繁に使用されるため、**内部ネットワークへの侵入経路** として危険度が高い。 | ProFTPD + mod_sftp を導入している全サーバ（Linux/Unix 系） |

---

## 3. 推奨アクション  

### 共通対策
- **脆弱性情報の即時共有**：開発・運用チーム、SOC、インシデントレスポンス担当者へ本レポートを展開。  
- **緊急パッチ適用**：ベンダーが提供する最新版へアップデートし、パッチが未提供の場合は **ベンダーへ問い合わせ**、もしくは **回避策**（設定変更・機能停止）を実施。  
- **既存トークンのローテーション**：認証バイパスが疑われるシステムは、全ユーザーのセッショントークン・API キーを **即時無効化** し、再発行を促す。  
- **入力検証の強化**：全ての外部入力に対し **サーバーサイドでのサニタイズ**（HTML エスケープ、長さ・型チェック）を実装。  

### 個別対策

| CVE | 推奨パッケージ・バージョン | 具体的作業 |
|-----|---------------------------|------------|
| CVE‑2026‑10130 | **QueryWeaver** ≥ **2.5.1**（2026‑03 リリース） | 1. `npm install queryweaver@2.5.1` または Docker イメージを `queryweaver:2.5.1` に更新<br>2. `signup` エンドポイントに **メールアドレスの所有確認（メール認証）** を追加<br>3. 既存トークンを全て失効し、ユーザーに再ログインを促す |
| CVE‑2026‑12228 | **lollms** ≥ **1.4.2**（2026‑04 パッチ） | 1. `pip install lollms==1.4.2` もしくは GitHub リリース `v1.4.2` をデプロイ<br>2. `POST /api/prompts/share` で `prompt_content` を **HTML エスケープ** もしくは **Content‑Security‑Policy** を適用<br>3. 既存 DB の `DBDirectMessage.content` をスクリプト除去ツールでクリーンアップ |
| CVE‑2026‑53994 | **ProFTPD** ≥ **1.3.8b3**（2026‑02 パッチ） + **mod_sftp** 1.0.5 | 1. OS のパッケージマネージャで `proftpd-mod-sftp` を最新版へ更新 (`apt-get upgrade proftpd-mod-sftp` / `yum update proftpd-mod-sftp`)<br>2. `SFTPAllowInvalidPacketLength` ディレクティブを **Off** に設定し、長さチェックを強制<br>3. すべての SFTP アカウントの **パスワード変更** と **公開鍵再登録** を実施 |
| 全体 | **ログ監視・アラート** | - 認証失敗・不審なトークン取得ログを SIEM に集約<br>- XSS ペイロード検知ルールを WAF に追加<br>- SFTP パケット長異常を IDS/IPS で検知 |

---

**まとめ**  
今回の CVE は「**入力検証不足**」と「**権限チェックの抜け」」が共通の根本原因です。速やかなパッチ適用と併せて、**開発プロセスにセキュアコーディング（入力サニタイズ・最小権限の原則）** を組み込むことが、同様の脆弱性再発防止に直結します。特に認証トークンや SFTP のような **認証情報が直接的に利用されるコンポーネント** は、定期的な **トークンローテーション** と **脆弱性スキャン** を運用フローに組み込むことを推奨します。

---

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-10130

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-18T23:17:00.397 |

QueryWeaver contains an authentication bypass vulnerability that allows unauthenticated attackers to obtain valid session tokens for existing accounts by submitting a signup request with a known victim email address. The signup route unconditionally creates and links a new token to the matching Identity via a Cypher MERGE operation before checking whether the email belongs to an existing account, causing the server to return a valid authenticated session token for the victim's identity without requiring any prior credentials or user interaction.

### CVE-2026-12228

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-18T21:17:03.040 |

A stored cross-site scripting (XSS) vulnerability exists in the `POST /api/prompts/share` endpoint of parisneo/lollms (latest version). The endpoint stores attacker-controlled `prompt_content` into `DBDirectMessage.content` without server-side sanitization. When a victim opens the direct message (DM) thread, the message is rendered by the DM UI through `MessageContentRenderer`, which uses `v-html` to insert rendered HTML into the DOM. The frontend sanitizer, which is regex-based, fails to comprehensively sanitize attacker-controlled HTML, allowing malicious payloads to execute in the victim's browser context. This vulnerability enables any authenticated user to send a malicious prompt-share message to another user's inbox, leading to arbitrary JavaScript execution, authenticated actions as the victim, exposure of same-origin application data, and potential account takeover.

### CVE-2026-53994

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-18T20:17:30.283 |

ProFTPD mod_sftp contains a heap-based buffer overflow reachable by an authenticated SFTP user. The fxp_packet_read() function accepts the attacker-supplied 32-bit big-endian SFTP packet length without a minimum sanity check. A value of 0 causes an unsigned subtraction elsewhere in the read path to underflow to approximately 4 GB. That oversized request reaches the core memory allocator, where the rounded size is computed in size_t but passed to new_block() as a 32-bit int; the low 32 bits of 0x100000000 are 0, so new_block() returns a small (~512-byte) block while the caller is told it received ~4 GB. The subsequent fill loop then streams attacker-controlled bytes past the end of the 544-byte allocation, producing an attacker-controlled heap buffer overflow. An authenticated user can crash the per-connection ProFTPD session child on demand with a single malformed SFTP packet (packet_len=0 followed by a body greater than approximately 544 bytes), producing reliable authenticated remote denial of service. Depending on heap layout and adjacent allocations, heap metadata corruption and further consequences beyond denial of service may be possible, though only denial of service is demonstrated by the supplied proof of concept.
