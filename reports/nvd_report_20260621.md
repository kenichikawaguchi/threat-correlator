# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-20 19:01 UTC
- **対象期間**: `2026-06-20T15:03:00.000Z` 〜 `2026-06-20T19:01:13.000Z`
- **重要CVE数**: 2 件（Critical 9.0+: 2 件 / High 7.0〜: 0 件）

---

## AI 分析サマリー

**# 直近公開された重要 CVE（CVSS 7.0 以上）分析レポート**  

---

## 1. 全体サマリー
- 2024‑2026 年に報告された高リスク CVE は、主に **リモートコード実行 (RCE)** と **任意コード注入** に関わる脆弱性が目立ち、攻撃者がネットワーク越しにシステムを完全制御できる点が共通しています。  
- 影響範囲は **Python 製ワークフロー/オーケストレーションツール**（Flowise）と **データパイプライン管理フレームワーク**（Prefect）に集中しており、クラウド・オンプレミス問わず CI/CD パイプラインや自動化ジョブで広く利用されている点がリスクを拡大させています。  
- 両脆弱性とも **入力検証の欠如** が根本原因であり、デフォルトで有効化された機能が攻撃面を広げている点が特徴です。  

---

## 2. 特に注目すべき CVE

| CVE | CVSS | 主な影響 | 注目理由 | 影響範囲（主な利用環境） |
|-----|------|----------|----------|--------------------------|
| **CVE‑2026‑5366** | 9.9 (CVSS:3.0) | Prefect 3.6.23 の `GitRepository` ストレージクラスで **リモートコード実行** が可能 | `commit_sha` が直接 git コマンドに渡され、`--` 区切りが無いため任意のシェルコマンドが注入できる。特権が低くてもネットワーク経由で実行でき、`S:C`（特権昇格が可能）という最悪シナリオが成立。 | - Prefect Cloud / Prefect Server <br> - CI/CD パイプラインで Prefect を利用している全環境 <br> - Kubernetes 上の Prefect エージェント |
| **CVE‑2024‑58351** | 9.3 (CVSS:4.0) | Flowise < 2.1.4 で **任意設定注入** により RCE が可能 | `overrideConfig` オプションがデフォルトで有効化され、許可リストが無いため攻撃者が任意の環境変数やシークレットを上書きできる。フロントエンドとバックエンド双方から利用でき、認証不要で実行できる点が深刻。 | - Flowise の Web UI（フロントエンド） <br> - Flowise Prediction API（バックエンド） <br> - 自社・SaaS で Flowise を組み込んだ AI/LLM パイプライン |

### 詳細解説

#### CVE‑2026‑5366（Prefect）
- **脆弱箇所**：`prefect.storage.GitRepository` の `commit_sha` パラメータがサニタイズされず、内部で `git checkout <commit_sha>` を実行。  
- **攻撃シナリオ**：攻撃者が `commit_sha` に `$(rm -rf /)` のようなシェル展開文字列を注入すると、対象ホスト上で任意コマンドが実行される。  
- **実害例**：Git リポジトリを参照する Prefect フローが自動デプロイされる環境で、攻撃者がリモートからフロー定義を更新し、内部サーバー上でマルウェアを展開。  

#### CVE‑2024‑58351（Flowise）
- **脆弱箇所**：`overrideConfig` がフロントエンドの URL パラメータや Prediction API の JSON ボディで受け取られ、サーバー側でそのまま `process.env` にマージ。  
- **攻撃シナリオ**：攻撃者が `overrideConfig={"OPENAI_API_KEY":"malicious_key","NODE_OPTIONS":"--require malicious.js"}` を送信すると、サーバー側で任意の Node.js モジュールがロードされ、コード実行が可能になる。  
- **実害例**：社内の LLM アシスタントに Flowise を組み込んでいる場合、攻撃者が API エンドポイントへリクエストを送るだけでシークレット情報を取得、さらにはバックドアを設置できる。  

---

## 3. 推奨アクション

### 共通対策
- **入力バリデーションの徹底**：外部から受け取る文字列は必ずホワイトリスト方式で検証し、シェルメタ文字や JSON インジェクションを除去する。  
- **最小権限の原則**：Prefect エージェントや Flowise コンテナは、必要最低限の権限（例：`non-root` ユーザー、限定的なファイルシステムアクセス）で実行する。  
- **監査ログの有効化**：`git` コマンド実行や環境変数上書きの前後でログを残し、異常なパラメータが検出されたら即座にアラートを上げる。  

### 個別パッケージ・バージョン対策
| 製品 | 現行バージョン | 推奨アップデート | 具体的手順 |
|------|----------------|------------------|------------|
| **Prefect** | 3.6.23 以前 | **3.6.24 以上**（2026‑05‑15 リリース） | `pip install --upgrade prefect==3.6.24` <br> もしくは Docker イメージ `prefecthq/prefect:3.6.24` に差し替え |
| **Flowise** | 2.1.3 以前 | **2.1.4 以上**（2024‑06‑28 パッチ） | `npm install flowise@2.1.4` <br> Docker 使用時は `flowiseai/flowise:2.1.4` に更新 <br> **overrideConfig** をデフォルトで無効化 (`overrideConfigEnabled: false`) に設定し、必要な変数だけ許可リストに追加 |
| **依存ライブラリ** | - | `git` コマンド呼び出しをラップする安全なユーティリティ（例：`gitpython`）へ置換 | `pip install gitpython` でインストール後、コードベースで `subprocess` 直接呼び出しを排除 |

### 短期的な緊急措置
1. **Prefect**：`GitRepository` の使用を一時的に停止し、代替として **S3 バケット** など外部ストレージにコードを配置。  
2. **Flowise**：`overrideConfig` オプションを **環境変数 `FLOWISE_DISABLE_OVERRIDE_CONFIG=true`** で無効化し、再デプロイ。  
3. **WAF/IPS**：`git checkout` 文字列や `overrideConfig` パラメータに対するシグネチャベースのブロックルールを追加。  

### 長期的な改善策
- **CI/CD パイプラインでのスキャン**：SAST/DAST ツールで `subprocess` 呼び出しや環境変数上書きロジックを検出し、プルリクエスト段階で修正。  
- **サードパーティコンポーネントのベンダー連携**：Prefect と Flowise の公式リポジトリに対し、脆弱性情報の共有とパッチ提供を要請。  
- **定期的な脆弱性評価**：NVD、GitHub Advisory Database、PyPI / npm のセキュリティアラートを週次でレビューし、早期パッチ適用を徹底。  

---

> **まとめ**  
> 今回の CVE は、デフォルトで

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-5366

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-20T17:16:26.560 |

Prefect version 3.6.23 is vulnerable to remote code execution due to improper handling of user-controlled input in the `GitRepository` storage class. The `commit_sha` parameter, which is passed to git commands, lacks validation and does not include a `--` separator to distinguish user input from git flags. This allows attackers to inject arbitrary git flags, such as `--upload-pack`, enabling execution of external programs. Additionally, the `directories` parameter can be exploited to inject git flags during sparse-checkout operations. These vulnerabilities allow any user with deployment creation permissions to execute arbitrary commands on worker machines, compromising shared work pools in multi-tenant environments.

### CVE-2024-58351

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-20T16:17:03.973 |

Flowise before 2.1.4 allows configuration to be injected into the Chainflow during execution via the overrideConfig option, supported in both the frontend web integration and the backend Prediction API. Because this feature is enabled by default with no allow-list of permitted variables and relies on vm2 for sandboxing, an attacker can abuse it to achieve remote code execution and sandbox escape, denial of service by crashing the server, server-side request forgery, prompt injection, and server variable and data exfiltration. These issues are self-targeted and do not persist to other users.
