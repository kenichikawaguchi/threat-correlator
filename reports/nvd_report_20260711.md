# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-10 15:00 UTC
- **対象期間**: `2026-07-09T15:00:33.000Z` 〜 `2026-07-10T15:00:37.000Z`
- **重要CVE数**: 122 件（Critical 9.0+: 27 件 / High 7.0〜: 95 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** 把握されています。特に **リモートコード実行 (RCE)・サンドボックス脱出・任意ファイルアップロード** といった「認証不要」かつ「ネットワーク越しに完全権限取得」できる脆弱性が目立ちます。  
- AI/LLM フレームワーク（Langroid）やコンテナオーケストレーション（Ruflo）で **CVSS 10.0** のクリティカルな RCE が複数報告されました。  
- オープンソース BI ツール **Metabase** の H2 データベース連携におけるデシリアライズ脆弱性は **CVSS 9.9** と極めて高リスクです。  
- WordPress プラグイン系では **任意ファイルアップロード** が連続して報告され、管理者権限取得が容易になる点が共通しています。  

この傾向は、**「外部入力を直接実行・デシリアライズに渡す」実装ミス** が依然として多く、開発・デプロイ時の入力検証・権限分離が不十分であることを示唆しています。

---

## 2. 特に注目すべき CVE  

| CVE ID | 製品・コンポーネント | 主な脆弱性 | 影響範囲・攻撃シナリオ | 修正バージョン |
|--------|-------------------|------------|------------------------|----------------|
| **CVE‑2026‑54769** | Langroid (0.65.2 未満) | Sandbox Escape → Remote Code Execution | `TableChatAgent` と `VectorStore` が LLM 生成メッセージを評価する際、サンドボックスを迂回し任意コードを実行できる。攻撃者は外部から LLM プロンプトを操作できれば即座にサーバ上でシェル権限取得が可能。 | **0.65.2** 以降 |
| **CVE‑2026‑59726** | Ruflo (3.16.3 未満) | 認証なし Docker‑Compose エンドポイント公開 | デフォルト `docker‑compose.yml` が `POST /mcp` / `POST /mcp/:group` を無認証で受け付け、`terminal_execute` ツール呼び出しが可能になる。攻撃者は任意コマンドをコンテナ内で実行でき、ホスト側への横展開も想定。 | **3.16.3** 以降 |
| **CVE‑2026‑59827** | Metabase (1.58.15, 1.59.12, 1.60.6.3, 1.61.1.4 未満) | H2 データベースのデシリアライズ | H2 の `native query` 結果列に任意の Java オブジェクトを埋め込み、Metabase がそれをデシリアライズして RCE。デフォルトのサンプル DB を使用している環境は即座に攻撃対象になる。 | **1.58.15**, **1.59.12**, **1.60.6.3**, **1.61.1.4** 以降 |
| **CVE‑2026‑15282** | WordPress – Instant Appointment plugin (≤ 1.2) | 任意ファイルアップロード | `insapp_upload_image_as_attachment` がファイルタイプ検証を行わず、任意の PHP ファイルを `wp-content/uploads` に配置できる。認証不要で Web シェルを設置し、サイト全体の権限取得が可能。 | **1.2.1** 以降 (開発元が提供するパッチ) |
| **CVE‑2026‑14894** | WordPress – Super Forms (≤ 6.3.313) | 任意ファイルアップロード | `submit_form` の AJAX ハンドラが `nopriv` でも実行され、ファイル拡張子チェックが欠如。攻撃者は任意のスクリプトをアップロードし、管理者権限で実行できる。 | **6.3.314** 以降 |

> **注**：上記 5 件は **CVSS ≥ 9.8** かつ「認証不要」か「管理者権限が不要」な点で共通しており、被害拡大リスクが最も高いと判断しました。

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
1. **直ちに該当パッケージを最新版へアップデート**（下表参照）。  
2. アップデートが不可能な場合は、**該当機能・エンドポイントをファイアウォールで外部から遮断**、または **Web アプリケーションファイアウォール (WAF)** でリクエストパラメータを制限。  
3. **デフォルトのサンプルデータベースやテスト用コンテナは本番環境で無効化**し、不要なポート・エンドポイントは閉じる。  
4. **ファイルアップロード系プラグインは MIME タイプと拡張子のホワイトリスト化**、さらにアップロード先ディレクトリに実行権限を付与しない。  
5. **CI/CD パイプラインで依存ライブラリの脆弱性スキャン**（例: `Trivy`, `Dependabot`, `GitHub Advanced Security`）を必須化し、CVSS 9.0 以上の脆弱性は自動的にブロック。

### 3.2 製品別具体的アップデート指示

| 製品 / パッケージ | 現行バージョン (例) | 推奨バージョン | アップデート手順 |
|-------------------|-------------------|----------------|----------------|
| **Langroid** | `< 0.65.2` | `0.65.2` 以上 | `pip install --upgrade langroid==0.65.2` |
| **Ruflo** | `< 3.16.3` | `3.16.3` 以上 | Docker イメージを `docker pull ruflo/ruflo:3.16.3`、`docker-compose.yml` のイメージタグを書き換えて再デプロイ |
| **Metabase** | `1.58.15` 未満、`1.59.12` 未満、`1.60.6.3` 未満、`1.61.1.4` 未満 | `1.58.15`, `1.59.12`, `1.60.6.3`, `1.61.1.4` いずれかの **最新安定版**（2026‑07 時点で `1.62.0`） | `docker pull metabase/metabase:1.62.0` → コンテナ再起動 |
| **Instant Appointment (WordPress)** | `≤ 1.2` | `1.2.1` 以上（公式パッチ） | WordPress 管理画面 → 「プラグイン」→「更新」

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-54769

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-10T00:16:33.603 |

Langroid is a framework for building large-language-model-powered applications. Versions prior to 0.65.2 are vulnerable to a critical Sandbox Escape leading to Remote Code Execution (RCE) in its `TableChatAgent` and `VectorStore` capabilities. When these agents evaluate LLM-generated tool messages with `full_eval=True`, they attempt to sandbox the execution by explicitly setting `locals` to an empty dictionary `{}` inside Python's `eval()` function. However, this relies on an incomplete understanding of Python's execution model. Because `__builtins__` is not explicitly scrubbed from the `globals` dictionary mapping, Python implicitly injects all built-ins during execution, granting full access to functions like `__import__('os').system()`. Since `TableChatAgent.pandas_eval()` executes external LLM outputs natively, this bypass permits any attacker providing prompt payload to achieve unauthenticated RCE on the host system. Version 0.65.2 patches the issue.

### CVE-2026-59726

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-306;CWE-942` |
| Published | 2026-07-09T18:16:57.337 |

Ruflo is an agent meta-harness for Claude Code and Codex. Prior to 3.16.3, ruflo's default docker-compose deployment exposed the MCP bridge POST /mcp and POST /mcp/:group endpoints without authentication, allowing an unauthenticated network attacker to invoke tools/call to terminal_execute, obtain a shell in the bridge container, read provider API keys, and poison AgentDB learning-store patterns. This issue is fixed in version 3.16.3.

### CVE-2026-59827

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-09T18:16:57.893 |

Metabase is an open-source business intelligence and embedded analytics tool. Prior to 1.58.15, 1.59.12, 1.60.6.3, and 1.61.1.4, Metabase instances with an H2 database connection, including the default sample database, deserialize arbitrary Java objects returned in H2 native query result columns of type OTHER without validation, allowing an authenticated user who can run native H2 queries to execute code on the Metabase server. This issue is fixed in versions 1.58.15, 1.59.12, 1.60.6.3, and 1.61.1.4.

### CVE-2026-15282

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-10T05:16:30.820 |

The Instant Appointment plugin for WordPress is vulnerable to arbitrary file uploads due to missing file type validation in the 'insapp_upload_image_as_attachment' function in all versions up to, and including, 1.2. This makes it possible for unauthenticated attackers to upload arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-14894

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-10T04:17:47.587 |

The Super Forms – Drag & Drop Form Builder plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 6.3.313 via the submit_form function. This is due to missing file type validation and the absence of any capability check on the submit_form nopriv AJAX handler, whose only barrier is a session nonce freely obtainable by unauthenticated visitors via a separate nopriv endpoint. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. The nonce requirement is trivially bypassed because the super_create_nonce nopriv AJAX action allows any unauthenticated visitor to mint a valid sf_nonce and session cookie in a single prior request, reducing exploitation to two unauthenticated HTTP requests.

### CVE-2026-42486

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-07-09T16:16:41.443 |

[This CNA information record relates to multiple CVEs; the text explains which aspects/vulnerabilities correspond to which CVE.]
XAPI can configure different users with different roles, using Role
Based Access Control.  For more details, see:

  https://docs.xenserver.com/en-us/xencenter/current-release/rbac-overview.html#rbac-roles

The pool-admin role is fully privileged.  Notably, users with this role
can also SSH into the host as root.

The other administrator roles are pool-operator, vm-power-admin and
vm-admin, each of which are authorised to configure and manage various
aspects of the system.

Some settings are inadequately restricted, and can be set by a lower
privilege of administrator than expected.

 * CVE-2026-23559: A vm-admin can set VBD.other_config:backend-local and
   turn arbitrary files in dom0 into VDIs (virtual disks) and give said
   disks to a VM they control.  This is an arbitrary read and/or modify
   of files in dom0.

 * CVE-2026-23560: A vm-admin can set VM.other-config:is_system_domain
   and mark a VM as a system domain.  System domains are ignored and
   left running during certain other host/pool operations, and may be
   hidden from view in tooling.

 * CVE-2026-23561: A vm-admin can set VM.other_config:storage_driver_domain
   and mark a VM as the storage domain for a particular host storage
   connection (PBD). Shutting down the VM can cause the PBD to be
   erroneously marked as unplugged when it is not.

 * CVE-2026-23562: Configuration of PCI passthrough is normally
   restricted to the pool-admin role.  However one API was missing this
   check, allowing a vm-admin access to unintended host hardware.

 * CVE-2026-42486: A vm-admin can set the VM.platform:hvm_serial
   parameter, which should be restricted to the pool-admin role, as it
   can allow arbitrary dom0 file write.

### CVE-2026-23562

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-07-09T16:16:39.233 |

[This CNA information record relates to multiple CVEs; the text explains which aspects/vulnerabilities correspond to which CVE.]
XAPI can configure different users with different roles, using Role
Based Access Control.  For more details, see:

  https://docs.xenserver.com/en-us/xencenter/current-release/rbac-overview.html#rbac-roles

The pool-admin role is fully privileged.  Notably, users with this role
can also SSH into the host as root.

The other administrator roles are pool-operator, vm-power-admin and
vm-admin, each of which are authorised to configure and manage various
aspects of the system.

Some settings are inadequately restricted, and can be set by a lower
privilege of administrator than expected.

 * CVE-2026-23559: A vm-admin can set VBD.other_config:backend-local and
   turn arbitrary files in dom0 into VDIs (virtual disks) and give said
   disks to a VM they control.  This is an arbitrary read and/or modify
   of files in dom0.

 * CVE-2026-23560: A vm-admin can set VM.other-config:is_system_domain
   and mark a VM as a system domain.  System domains are ignored and
   left running during certain other host/pool operations, and may be
   hidden from view in tooling.

 * CVE-2026-23561: A vm-admin can set VM.other_config:storage_driver_domain
   and mark a VM as the storage domain for a particular host storage
   connection (PBD). Shutting down the VM can cause the PBD to be
   erroneously marked as unplugged when it is not.

 * CVE-2026-23562: Configuration of PCI passthrough is normally
   restricted to the pool-admin role.  However one API was missing this
   check, allowing a vm-admin access to unintended host hardware.

 * CVE-2026-42486: A vm-admin can set the VM.platform:hvm_serial
   parameter, which should be restricted to the pool-admin role, as it
   can allow arbitrary dom0 file write.

### CVE-2026-23561

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-07-09T16:16:39.100 |

[This CNA information record relates to multiple CVEs; the text explains which aspects/vulnerabilities correspond to which CVE.]
XAPI can configure different users with different roles, using Role
Based Access Control.  For more details, see:

  https://docs.xenserver.com/en-us/xencenter/current-release/rbac-overview.html#rbac-roles

The pool-admin role is fully privileged.  Notably, users with this role
can also SSH into the host as root.

The other administrator roles are pool-operator, vm-power-admin and
vm-admin, each of which are authorised to configure and manage various
aspects of the system.

Some settings are inadequately restricted, and can be set by a lower
privilege of administrator than expected.

 * CVE-2026-23559: A vm-admin can set VBD.other_config:backend-local and
   turn arbitrary files in dom0 into VDIs (virtual disks) and give said
   disks to a VM they control.  This is an arbitrary read and/or modify
   of files in dom0.

 * CVE-2026-23560: A vm-admin can set VM.other-config:is_system_domain
   and mark a VM as a system domain.  System domains are ignored and
   left running during certain other host/pool operations, and may be
   hidden from view in tooling.

 * CVE-2026-23561: A vm-admin can set VM.other_config:storage_driver_domain
   and mark a VM as the storage domain for a particular host storage
   connection (PBD). Shutting down the VM can cause the PBD to be
   erroneously marked as unplugged when it is not.

 * CVE-2026-23562: Configuration of PCI passthrough is normally
   restricted to the pool-admin role.  However one API was missing this
   check, allowing a vm-admin access to unintended host hardware.

 * CVE-2026-42486: A vm-admin can set the VM.platform:hvm_serial
   parameter, which should be restricted to the pool-admin role, as it
   can allow arbitrary dom0 file write.

### CVE-2026-23560

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-07-09T16:16:38.943 |

[This CNA information record relates to multiple CVEs; the text explains which aspects/vulnerabilities correspond to which CVE.]
XAPI can configure different users with different roles, using Role
Based Access Control.  For more details, see:

  https://docs.xenserver.com/en-us/xencenter/current-release/rbac-overview.html#rbac-roles

The pool-admin role is fully privileged.  Notably, users with this role
can also SSH into the host as root.

The other administrator roles are pool-operator, vm-power-admin and
vm-admin, each of which are authorised to configure and manage various
aspects of the system.

Some settings are inadequately restricted, and can be set by a lower
privilege of administrator than expected.

 * CVE-2026-23559: A vm-admin can set VBD.other_config:backend-local and
   turn arbitrary files in dom0 into VDIs (virtual disks) and give said
   disks to a VM they control.  This is an arbitrary read and/or modify
   of files in dom0.

 * CVE-2026-23560: A vm-admin can set VM.other-config:is_system_domain
   and mark a VM as a system domain.  System domains are ignored and
   left running during certain other host/pool operations, and may be
   hidden from view in tooling.

 * CVE-2026-23561: A vm-admin can set VM.other_config:storage_driver_domain
   and mark a VM as the storage domain for a particular host storage
   connection (PBD). Shutting down the VM can cause the PBD to be
   erroneously marked as unplugged when it is not.

 * CVE-2026-23562: Configuration of PCI passthrough is normally
   restricted to the pool-admin role.  However one API was missing this
   check, allowing a vm-admin access to unintended host hardware.

 * CVE-2026-42486: A vm-admin can set the VM.platform:hvm_serial
   parameter, which should be restricted to the pool-admin role, as it
   can allow arbitrary dom0 file write.

### CVE-2026-23559

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-07-09T16:16:38.807 |

[This CNA information record relates to multiple CVEs; the text explains which aspects/vulnerabilities correspond to which CVE.]


XAPI can configure different users with different roles, using Role
Based Access Control.  For more details, see:

   https://docs.xenserver.com/en-us/xencenter/current-release/rbac-overview.html#rbac-roles 

The pool-admin role is fully privileged.  Notably, users with this role
can also SSH into the host as root.

The other administrator roles are pool-operator, vm-power-admin and
vm-admin, each of which are authorised to configure and manage various
aspects of the system.

Some settings are inadequately restricted, and can be set by a lower
privilege of administrator than expected.

 * CVE-2026-23559: A vm-admin can set VBD.other_config:backend-local and
   turn arbitrary files in dom0 into VDIs (virtual disks) and give said
   disks to a VM they control.  This is an arbitrary read and/or modify
   of files in dom0.

 * CVE-2026-23560: A vm-admin can set VM.other-config:is_system_domain
   and mark a VM as a system domain.  System domains are ignored and
   left running during certain other host/pool operations, and may be
   hidden from view in tooling.

 * CVE-2026-23561: A vm-admin can set VM.other_config:storage_driver_domain
   and mark a VM as the storage domain for a particular host storage
   connection (PBD). Shutting down the VM can cause the PBD to be
   erroneously marked as unplugged when it is not.

 * CVE-2026-23562: Configuration of PCI passthrough is normally
   restricted to the pool-admin role.  However one API was missing this
   check, allowing a vm-admin access to unintended host hardware.

 * CVE-2026-42486: A vm-admin can set the VM.platform:hvm_serial
   parameter, which should be restricted to the pool-admin role, as it
   can allow arbitrary dom0 file write.

### CVE-2026-23556

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-281` |
| Published | 2026-07-09T16:16:38.690 |

When oxenstored is tearing a domain down, the node data is cleaned up
but the usage counts are leaked.

When the domain ID is eventually reused, the new domain can create fewer
nodes before beeing deemed to be over quota.

### CVE-2025-58151

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-07-09T16:16:33.817 |

varstored is a component of the Xapi toolstack handling UEFI Variables
for a VM.  It has a communication path with OVMF inside the VM involving
mapping a buffer prepared by OVMF.

Within varstored, there were insufficient compiler barriers, creating
TOCTOU issues with data in the shared buffer.

The exact vulnerable behaviour depends on the code generated by the
compiler.  In a build of varstored using default settings, the attacker
can control an index used in a jump table.

### CVE-2025-58146

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-09T16:16:33.687 |

There are multiple issues.

 1. Updates to the XAPI database sanitise input strings, but try
    generating the notification using the unsanitised input.  This
    causes the database's event thread to terminate and cease further
    processing.

 2. XAPI's UTF-8 encoder implements v3.0 of the Unicode spec, but XAPI
    uses libraries which conform to the stricter v3.1 of the Unicode
    spec.  This causes some strings to be accepted as valid UTF-8 by
    XAPI, but rejected by other libraries in use.  Notably, such strings
    can be entered into the database, after which the database can no
    longer be loaded.

 3. There is no input sanitisation for Map/Set updates on objects in the
    XAPI database.

### CVE-2025-27464

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-07-09T16:16:33.313 |

[This CNA information record relates to multiple CVEs; the text explains which aspects/vulnerabilities correspond to which CVE.] The Windows PV drivers expose various facilities to userspace. Several of these have no security descriptor, and are therefore fully accessible to unprivileged users. These are: 1. XenCons, CVE-2025-27462 2. XenIface, CVE-2025-27463 3. XenBus, CVE-2025-27464

### CVE-2025-27463

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-07-09T16:16:33.203 |

[This CNA information record relates to multiple CVEs; the text explains which aspects/vulnerabilities correspond to which CVE.] The Windows PV drivers expose various facilities to userspace. Several of these have no security descriptor, and are therefore fully accessible to unprivileged users. These are: 1. XenCons, CVE-2025-27462 2. XenIface, CVE-2025-27463 3. XenBus, CVE-2025-27464

### CVE-2025-27462

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-07-09T16:16:33.070 |

[This CNA information record relates to multiple CVEs; the text explains which aspects/vulnerabilities correspond to which CVE.]


The Windows PV drivers expose various facilities to userspace.  Several
of these have no security descriptor, and are therefore fully accessible
to unprivileged users.  These are:

  1. XenCons,  CVE-2025-27462
  2. XenIface, CVE-2025-27463
  3. XenBus,   CVE-2025-27464

### CVE-2026-15378

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-10T10:16:23.553 |

A flaw was found in the `guardrails-detectors` component. This vulnerability allows a remote attacker to perform a blind Server-Side Request Forgery (SSRF) by submitting a specially crafted XML Schema Definition (XSD) string. This can lead to unauthorized access to sensitive information, including credentials from cloud metadata services, Kubernetes API, internal MinIO, and other internal network endpoints. Additionally, it enables local file reads of critical data such as service account tokens and pod secrets.

### CVE-2026-54760

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-89` |
| Published | 2026-07-10T00:16:33.477 |

Langroid is a framework for building large-language-model-powered applications. Prior to version 0.65.1, the `SQLChatAgent` SQL-injection mitigation, with default `allow_dangerous_operations=False`, combines a raw-text regex blocklist (`_DANGEROUS_SQL_PATTERNS`) with a `sqlglot` SELECT-only statement allowlist. The blocklist entries that target callable functions require the function name to be immediately followed by `\s*\(`. PostgreSQL accepts the same call with the name separated from `(` by a quoted identifier, an inline comment, or schema qualification. These forms evade the regex, still parse as `SELECT`, and execute the same PostgreSQL function. This restores the `pg_read_file` server-side file-read primitive that the prior CVE-2026-25879 / GHSA-pmch-g965-grmr fix was meant to block: the parent advisory fixed a missing `pg_read_file` blocklist entry, while this report shows that the added regex is bypassable. Version 0.65.1 fixes the issue.

### CVE-2026-58123

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-09T22:17:09.517 |

Hermes WebUI before 0.51.788 contains an unauthenticated remote code execution vulnerability that allows remote attackers to execute arbitrary shell commands by accessing the embedded terminal API endpoints without credentials. Attackers can create a session, attach a PTY shell, and write arbitrary commands through the terminal input endpoint to achieve full command execution as the server process user via four sequential unauthenticated HTTP requests.

### CVE-2026-58122

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-348` |
| Published | 2026-07-09T22:17:09.363 |

Hermes WebUI before 0.51.307 contains an authentication bypass vulnerability that allows unauthenticated remote attackers to circumvent local-origin IP restrictions on onboarding endpoints by supplying a spoofed X-Forwarded-For header with a loopback address. Attackers can exploit this bypass to perform server-side request forgery against internal services including cloud metadata endpoints, overwrite LLM provider configuration and API keys with attacker-controlled values, or initiate OAuth device-code flows to obtain persistent access tokens stored in auth.json.

### CVE-2026-55615

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-07-10T00:16:33.867 |

Langroid is a framework for building large-language-model-powered applications. Prior to version 0.65.5, Neo4jChatAgent passes LLM-generated Cypher queries straight to the Neo4j driver with no validation, no statement-type allowlist, and no opt-out gate. The query text is influenceable by prompt injection (direct user input or indirect content the agent reads back via RAG), so an attacker who can influence the prompt can read or destroy all graph data and, when APOC or dbms.security procedures are enabled on the server, achieve OS-command and filesystem access. This is the same defect class and threat model as the SQLChatAgent prompt-to-SQL-to-RCE issue fixed in version 0.63.0 (CVE-2026-25879); that fix did not extend to the neo4j module. Version 0.65.5 contains a fix for the neo4j module.

### CVE-2026-56292

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:L/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-09T15:16:37.937 |

A SQLi vulnerability in AcyMailing component < 10.11.1 for Joomla was discovered. Exploiting this flaw can lead to unauthorized database access and data leakage.

### CVE-2026-56688

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-10T12:17:23.453 |

Dell PowerFlex Manager, Version prior to 5.1.0.1, contain(s) an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability during OS Repository processing to achieve arbitrary command execution as root, potentially leading to full appliance compromise and lateral movement into managed infrastructure.

### CVE-2026-15300

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-10T05:16:33.393 |

The GEO my WP plugin for WordPress was vulnerable to SQL Injection via the 'distance', 'lat', and 'lng' parameters in versions up to, and including, 4.5.4. The values were read from $_SERVER['QUERY_STRING'] via parse_str() (bypassing wp_magic_quotes, which does not cover $_SERVER), then passed through bare esc_sql() before being interpolated into unquoted numeric positions in the proximity-search query (HAVING/SELECT clause distance math, BETWEEN bounding-box pre-filter) built by gmw_locations_query() in plugins/posts-locator/includes/class-gmw-wp-query.php. Because esc_sql() only escapes string delimiters and these positions are numeric, payloads such as `1 OR SLEEP(3)` survived sanitization. Fixed in 4.5.5 by adding an upstream is_numeric() guard that short-circuits the WHERE clause to `AND 1 = 0` when either coordinate is non-numeric, and by replacing the three esc_sql() calls with (float) casts.

### CVE-2026-54003

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-454` |
| Published | 2026-07-09T19:17:06.120 |

Kirby is an open-source content management system. Prior to 4.9.4 and from 5.4.4, Kirby sites with no configured user accounts that run on publicly accessible servers behind a reverse proxy setting the Forwarded, X-Client-IP, or X-Real-IP request header could allow remote attackers to install the Panel and create the first admin user because local-IP checks trusted those headers incorrectly. This issue is fixed in versions 4.9.4 and 5.4.4.

### CVE-2026-59826

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-09T18:16:57.757 |

Metabase is an open-source business intelligence and embedded analytics tool. From 1.55.0 until 1.58.15.1, 1.59.12, 1.60.6.3, and 1.61.2, Metabase did not validate unsafe H2 connection properties on one database-creation code path, allowing an authenticated administrator to register a crafted H2 database connection and execute arbitrary Java code on the Metabase server. This issue is fixed in versions 1.58.15.1, 1.59.12, 1.60.6.3, and 1.61.2.

### CVE-2026-41880

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-10T10:16:24.193 |

R-SOFT DMS is vulnerable to OS Command Injection in the Optical Character Recognition (OCR) module. Multiple command execution functions accept user-controllable file paths without proper sanitization before passing them to the system shell via SSH. In current infrastructure the URL encoding neutralizes the injection during the standard web upload flow. An authenticated attacker who is able to trigger the OCR functionality for the uploaded file can execute OS commands within the context of a root user.

This issue was fixed in version v3.19-2862 and v3.17-2580.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-54469

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-10T13:16:20.427 |

Dell Unisphere for PowerMax, version(s) 10.3.0.5 and prior, contain(s) a Deserialization of Untrusted Data vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to arbitrary command execution with root privileges.

### CVE-2026-15070

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-10T04:17:47.727 |

The Salon Booking System – Free Version plugin for WordPress is vulnerable to Cross-Site Request Forgery in all versions up to, and including, 10.30.32. This is due to missing or incorrect nonce validation on the setCustomText function. This makes it possible for unauthenticated attackers to inject arbitrary PHP code into the web-accessible translate-constants.php file within the plugin directory, enabling remote code execution on the server via a forged request granted they can trick a site administrator into performing an action such as clicking on a link. sanitize_text_field() is applied to the POST 'value' parameter but does not neutralize the characters — single quotes, parentheses, semicolons, $, and [] — required to break out of the PHP string literal into which the value is interpolated before being written to disk via file_put_contents().

### CVE-2026-55207

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-07-09T21:16:55.890 |

Pimcore is an Open Source Data & Experience Management Platform. Prior to 2025.4.6 and 2026.1.6, an unauthenticated attacker who knows a valid admin username can take over any Pimcore admin account by sending a password reset request with an attacker-controlled resetPasswordUrl. The server generates a real cryptographic recovery token, appends it to the supplied URL, and emails the link to the victim; when the victim clicks the link, the token is sent to the attacker and can be used with POST /pimcore-studio/api/login/token to authenticate with full admin privileges while bypassing two-factor authentication. This issue is fixed in versions 2025.4.6 and 2026.1.6.

### CVE-2026-59148

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-352;CWE-732;CWE-942` |
| Published | 2026-07-09T19:17:07.067 |

Mockoon provides way to design and run mock APIs. Prior to 9.7.0, Mockoon's admin API in commons-server/src/libs/server/admin-api.ts is mounted on the same Express listener as user-defined mock routes, enabled by default in shipped runtimes, serves Access-Control-Allow-Origin: * with write methods allowed, and has no authentication. Any unauthenticated caller who can reach the mock server port can read MOCKOON_* environment variables, write arbitrary process environment variables through /mockoon-admin/env-vars, rewrite mock route bodies, statuses, and headers through PUT /mockoon-admin/environment, read transaction logs and SSE streams, and purge state. This issue is fixed in version 9.7.0.

### CVE-2026-13492

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-09T19:17:03.883 |

The UsersWP plugin for WordPress is vulnerable to Arbitrary File Deletion in versions up to, and including, 1.2.65. This is due to insufficient validation of file-field values in the UsersWP_Validation::validate_fields() function (which falls through to sanitize_text_field() for fields of type 'file', leaving directory-traversal sequences intact) combined with the UsersWP_Forms::upload_file_remove() AJAX handler building the deletion target from the uploads basedir concatenated with the attacker-controlled metadata value without any realpath canonicalization or uploads-directory boundary check before calling unlink(). This makes it possible for authenticated attackers, with Subscriber-level access and above, to delete arbitrary files on the affected site's server, including wp-config.

### CVE-2026-59734

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-09T18:16:57.473 |

Coolify is an open-source and self-hostable tool for managing servers, applications, and databases. Prior to 4.0.0-beta.469, Coolify's app/Jobs/ApplicationDeploymentJob.php generate_healthcheck_commands() function directly interpolated the health_check_host, health_check_method, and health_check_path parameters into shell commands without proper sanitization, allowing authenticated users to execute arbitrary commands inside deployment containers. This issue is fixed in version 4.0.0-beta.469.

### CVE-2026-41876

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-10T10:16:23.687 |

R-SOFT DMS is vulnerable to OS Command Injection in konwertujAction() function. The document converter executes shell commands using unsanitized file paths and format parameters. This allows an authenticated attacker to execute arbitrary system commands with the privileges of the web server user.

This issue was fixed in version v3.19-2752 and v3.17-2580.

### CVE-2026-50180

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-89` |
| Published | 2026-07-10T00:16:33.197 |

Langroid is a framework for building large-language-model-powered applications. Prior to version 0.64.0, `SQLChatAgent` in `langroid` ships a `_validate_query` defense-in-depth layer whose `_DANGEROUS_SQL_PATTERNS` regex blocklist enumerates dangerous SQL primitives by specific function name. The list misses the canonical PostgreSQL filesystem-disclosure family `pg_read_file()`, `pg_stat_file()`, `pg_ls_logdir()`, `pg_ls_waldir()`, `pg_current_logfile()` (and similar `SELECT`-shaped functions in the same family). It also leaves SQL Server `OPENDATASOURCE` and SQLite `ATTACH '<file>' AS x` (DATABASE keyword omitted) unblocked. An attacker able to shape the LLM's generated SQL (directly via prompt input or transitively via prompt-injection in data the LLM ingests) can read arbitrary files from the PostgreSQL host through ordinary `SELECT` queries, even with the agent's strict default configuration (`allow_dangerous_operations=False`, `allowed_statement_types=['SELECT']`). The payloads survive the statement-type allowlist (each is a `SELECT`) and pass through the regex blocklist (none of the function names match), then reach the live SQLAlchemy engine via `SQLChatAgent.run_query`. Version 0.64.0 contains a patch for the issue.

### CVE-2026-58143

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-09T22:17:09.663 |

Cotonti Siena 0.9.26 and earlier contains a cross-site request forgery vulnerability that allows unauthenticated attackers to modify administrator configuration by tricking a logged-in administrator into submitting a forged POST request to the admin.php config update handler, which never invokes the application's CSRF validation function. Attackers can disable the PFS module's file extension whitelist by setting pfsfilecheck to 0, enabling any user with PFS access to upload and execute arbitrary PHP files on the server.

### CVE-2026-57026

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-1286` |
| Published | 2026-07-09T22:17:07.923 |

An Improper Validation of Syntactic Correctness of Input vulnerability in the SIP plugin of Juniper Networks Junos OS on MX Series with SPC3 and SRX Series allows an unauthenticated, network-based attacker to cause a Denial-of-Service (DoS).If the SIP ALG is enabled on an affected device, the processing of a malformed SIP invite packet will cause a flow processing daemon (flowd) crash and restart. This leads to a complete service outage until the system has automatically recovered.



This issue affects Junos OS on MX Series with SPC3 and SRX Series:


  *  all versions before 23.2R2-S7,
  *  23.4 versions before 23.4R2-S8,
  *  24.2 versions before 24.2R2-S5,
  *  24.4 versions before 24.4R2-S4,
  *  25.2 versions before 25.2R2,
  *  25.4 versions before 25.4R1-S2.

### CVE-2026-57023

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-09T22:17:07.397 |

An Improper Validation of Specified Quantity in Input vulnerability in the TCP proxy plugin of Juniper Networks Junos OS on MX Series with SPC3, and SRX Series allows an unauthenticated, network-based attacker to cause a complete Denial of Service (DoS).

When TCP proxy is engaged in a flow session, to support ALGs, Advanced Anti-Malware, ICAP or UTM, a TCP packet with specifically malformed TCP header will cause flow processing daemon (flowd) to crash and restart. This causes a complete service outage until the system has automatically recovered.



This issue affects Junos OS on MX with SPC3, and SRX Series: 



  *  23.4 versions before 23.4R2-S7, 
  *  24.2 versions before 24.2R2-S4, 
  *  24.4 versions before 24.4R2-S3,
  *  25.2 versions before 25.2R2.




This issue does not affect releases before 23.4R1.

### CVE-2026-15308

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-09T17:16:58.260 |

The incremental HTML parser (html.parser.HTMLParser) allows for CPU
denial-of-service through repeated unterminated markup declarations when
processing uncontrolled data.

### CVE-2026-11404

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-09T16:16:34.640 |

Cesanta Mongoose before 7.22 contains an out-of-bounds read in the built-in TLS server function mg_tls_server_recv_hello(), which uses an attacker-controlled session_id_len byte from a TLS ClientHello as a buffer index without validating it against the length of received data. A remote, unauthenticated attacker can send a single crafted ClientHello with an oversized session id length to read past the receive buffer, crashing any HTTPS, MQTTS, or WSS service built on MG_TLS_BUILTIN.

### CVE-2026-60109

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-09T15:16:41.757 |

Zeek before 8.0.9 contains a null pointer dereference vulnerability in its Kerberos protocol analyzer that allows unauthenticated remote attackers to crash the sensor by sending a crafted KRB_ERROR message with error-code 25 (KDC_ERR_PREAUTH_REQUIRED) containing a PA-DATA element with padata-type 2, 3, 11, or 19. Attackers can exploit a parser and analyzer state mismatch where proc_padata() dereferences an uninitialized pa_data_element field selected by the wrong parsing arm, triggering a crash via a single UDP or TCP packet to port 88 without any credentials or prior authentication.

### CVE-2026-60108

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-09T15:16:41.627 |

Zeek before 8.0.9 contains an uncontrolled memory consumption vulnerability in the FTP analyzer that allows unauthenticated remote attackers to cause process termination by sending a crafted FTP control session negotiating AUTH GSSAPI followed by a large ADAT control line. Attackers can exploit the NVT_Analyzer component's lack of a maximum line length check, causing it to continuously double its internal buffer without bounds during base64 decoding of an attacker-controlled ADAT token, resulting in denial of service of the Zeek sensor.

### CVE-2026-22660

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-697` |
| Published | 2026-07-10T14:16:52.687 |

FlaskBB through 2.2.0, fixed in commit a5da9a5, contains a logic flaw vulnerability that allows authenticated administrators to delete all built-in authorization groups by exploiting a type mismatch in the bulk delete protection check. The bulk AJAX endpoint in the management views compares received JSON integer group IDs against string literals, causing the protection check to always pass, which allows deletion of all six built-in groups and destroys the forum's permission model, potentially rendering the site unusable.

### CVE-2026-59855

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-80` |
| Published | 2026-07-09T23:17:06.293 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.1, Asset.render in app/src/asset/index.ts interpolates the unsanitized this.path value into HTML assigned to innerHTML, allowing a crafted asset link containing a double quote to break out of the src attribute, inject an event handler, and execute JavaScript that can run OS commands in the Electron renderer. This issue is fixed in versions 3.7.1-alpha.2 and 3.7.1.

### CVE-2026-59833

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-94;CWE-116` |
| Published | 2026-07-09T23:17:05.773 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.1, SiYuan renders note and package content to HTML through the Lute engine with sanitization enabled, but Lute's dangerous javascript scheme block does not check form action or SVG xlink:href attributes, allowing stored cross-site scripting in document export-preview and Bazaar package README render paths that can execute OS commands in the Electron desktop renderer. This issue is fixed in versions 3.7.1.

### CVE-2026-55604

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-09T22:17:06.247 |

DeepSeek MCP Server is an MCP server for DeepSeek V4. Starting in version 1.4.2 and prior to version 1.7.0, the process-global `SessionStore` accepts caller-supplied `session_id` values without binding them to any authenticated principal or transport session. An attacker can enumerate active session IDs via `deepseek_sessions`, then reuse a victim-controlled `session_id` in `deepseek_chat` to retrieve and continue the victim's conversation context. Version 1.7.0 contains a patch.

### CVE-2026-61343

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-09T18:16:58.030 |

LibreBooking's email template editor save action passes the submitted template name directly into the destination file path, allowing a remote attacker with administrator credentials to write an arbitrary file outside the template directory and execute code. Fixed in 5.1.0.

### CVE-2026-58378

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-07-09T18:16:54.847 |

Allwinner H616 TV Box TV98 has ADB enabled and exposed to the network on production. An attacker could request for ADB authorization and gain root level privileges if the victim allows access.

### CVE-2026-54801

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620` |
| Published | 2026-07-09T15:16:36.830 |

A vulnerability has been identified in CPCI85 Central Processing/Communication (All versions < V26.20), SICORE Base system (All versions < V26.20.0). The affected application contains insufficient validation of authentication credentials when processing administrative account modifications through the web API. This could allow an authenticated attacker to bypass security controls and gain unauthorized elevated privileges.

### CVE-2026-56690

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-10T12:17:23.700 |

Dell PowerFlex Manager, Version prior to 5.1.0.1, contain(s) an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Information disclosure, Information exposure, and Unauthorized access.

### CVE-2026-21055

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-10T05:16:36.217 |

Improper export of android application components in Bixby prior to version 4.0.70.8 allows local attackers to execute arbitrary commands with Bixby privilege.

### CVE-2026-54002

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-87` |
| Published | 2026-07-09T19:17:05.977 |

Kirby is an open-source content management system. Prior to 4.9.4 and 5.4.4, Kirby sites and plugins that use the writer or list fields or call Dom::sanitize(), Sane::sanitize(), Sane::Html::sanitize(), Sane::Svg::sanitize(), Sane::Xml::sanitize(), Sane::sanitizeFile(), or file sanitizeContents() with untrusted input allow malicious markup injected as children of an unknown HTML or XML tag to pass through Dom::sanitize() without being correctly sanitized, causing stored cross-site scripting. This issue is fixed in versions 4.9.4 and 5.4.4.

### CVE-2026-21049

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-10T05:16:35.533 |

Out-of-bounds write in libpadm.so library prior to SMR Jul-2026 Release 1 allows local attackers to execute arbitrary code.

### CVE-2026-21046

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-10T05:16:35.290 |

Time-of-check time-of-use race condition in fabricKeymaster trustlet prior to SMR Jul-2026 Release 1 allows local privileged attackers to execute arbitrary code.

### CVE-2026-21042

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-10T05:16:34.797 |

Out-of-bounds write in libsavsac.so prior to SMR Jul-2026 Release 1 allows local attackers to execute arbitrary code.

### CVE-2026-59858

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-09T23:17:06.740 |

Vim is an open source, command line text editor. Prior to 9.2.0735, the C omni-completion script in runtime/autoload/ccomplete.vim interpolates the typeref: or typename: extension field of a tags entry, without escaping, into a :vimgrep pattern that is run through :execute. Because :vimgrep honors the bar as a command separator, a crafted tag field can close the search pattern and append an arbitrary Ex command; opening a hostile .c file whose project tags file contains such an entry and invoking C omni-completion runs that command as the editing user. This issue is fixed in version 9.2.0735.

### CVE-2026-59856

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-09T23:17:06.420 |

Vim is an open source, command line text editor. Prior to 9.2.0736, the PHP omni-completion script in runtime/autoload/phpcomplete.vim interpolates a class or trait name, taken from the contents of the edited buffer, into a search() pattern that is run via win_execute() without escaping. A name containing a single quote can terminate the search() string argument early, and because the bar is honored as an Ex command separator, the remainder of the name is run as Ex commands; via the :! command this allows arbitrary operating-system command execution when a victim opens a crafted PHP file and invokes omni-completion. This issue is fixed in version 9.2.0736.

### CVE-2026-58459

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-09T17:17:01.493 |

gpsd through release-3.27.5, fixed at commit 4c06658, contains a command injection vulnerability in gpsprof that allows attackers who control the GPS device subtype value to execute arbitrary shell commands by embedding backtick payloads in the gnuplot plot title without proper escaping. The subtype field sourced from a DEVICES JSON log entry or NMEA PGRMT sentence is written into a generated gnuplot program via a set title statement with only double-quote characters escaped, enabling arbitrary shell command execution as the user running gnuplot when the victim renders the generated plot through the gpsprof and gnuplot workflow.

### CVE-2026-54799

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-07-09T15:16:36.580 |

A vulnerability has been identified in CPCI85 Central Processing/Communication (All versions < V26.20), SICORE Base system (All versions < V26.20.0). The affected application contains a vulnerability in its firmware update mechanism's signature validation process. This could allow an attacker to install malicious firmware, leading to persistent code execution and system compromise.

### CVE-2026-21048

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-10T05:16:35.410 |

Out-of-bounds write in parsing DNG format in libimagecodec.media.quram.so prior to SMR Jul-2026 Release 1 allows remote attackers to write out-of-bounds memory.

### CVE-2026-21045

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-10T05:16:35.177 |

Out-of-bounds write in parsing TIFF format in libimagecodec.media.quram.so prior to SMR Jul-2026 Release 1 allows remote attackers to write out-of-bounds memory.

### CVE-2026-41879

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-328` |
| Published | 2026-07-10T10:16:24.077 |

R-SOFT DMS stores superadmin credentials using a non-salted nested MD5 hash. This allows an attacker who obtain password hash to decode superadmin credentials. Critically, this password cannot be changed except by modifying the configuration file.

This issue was fixed in version v3.17-2000.

### CVE-2026-54423

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-424` |
| Published | 2026-07-10T04:17:52.230 |

In OpenStack Ironic before 37.0.1, an Ironic user with the ability to deploy nodes using the IPMI management interface can maliciously use the send_raw step to send arbitrary IPMI commands to a node, bypassing Ironic's access control.

### CVE-2026-57030

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:X/RE:M/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-09T22:17:08.643 |

A Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') vulnerability in the packet forwarding engine (PFE) of Juniper Networks Junos OS on SRX Series allows an unauthenticated, network-based attacker to cause a Denial-of-Service (DoS).

As part of the stateful traffic processing on SRX Series devices flows are being established, and removed when not needed anymore. During the removal process the timeout of a flow should be set to 3 seconds and consequentially the flow should be removed shortly after. Due to a race condition occurring when setting the timeout there is a chance (the exact conditions are outside the attackers control) that the timeout is instead set to a very high value of larger than 10,000 seconds:



user@host> show security flow session | match timeout
Session ID: 98784248524, Policy name: PROD-FLOW/4, HA State: Active, Timeout: 85250, Session State: Valid

This will lead to an accumulation of flows which can be observed by an ever-increasing value of invalidated sessions in the output of 'show security flow session summary':

user@host> show security flow session summary | match invalid
Invalidated sessions: 216931These sessions can't be cleared manually with the 'clear security flow session' command, which will either lead to forwarding to stop (and the system needs to be manually recovered with a reboot) or to a flowd core and automatic reboot.


This issue affects Junos OS on SRX Series:


  *  24.2 versions before 24.2R2-S3,
  *  24.4 versions before 24.4R2-S1, 24.4R2-S2,
  *  25.2 versions before 25.2R1-S2, 25.2R2.




This issue does not affect releases earlier than 24.2R1;

### CVE-2026-57022

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-07-09T22:17:07.233 |

An Improper Check for Unusual or Exceptional Conditions vulnerability in the Packet Forwarding Engine (PFE) of Juniper Networks Junos OS on MX with SPC3 and SRX Series allows an unauthenticated, network-based attacker to cause a Denial-of-Service (DoS).

When an affected device initiates a TCP connection to an attacker-controlled system that responds with a specific packet, this causes a PFE crash and restart, which affects all services until the system has automatically recovered.
This issue can happen among others in the following scenarios: ALG, SSL proxy, UTM, RTLOG, AppQoE probing, AAMW, ICAP, URL filtering.

This issue affects Junos OS on MX Series with SPC3, SRX5k Series with SPC3, SRX1600 Series, SRX2300 Series, SRX4000 Series, and vSRX Series:

  *  all versions before 23.2R2-S4,
  *  23.4 versions before 23.4R2-S5,
  *  24.2 versions before 24.2R2.

### CVE-2026-44787

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-09T22:17:04.607 |

Discourse is an open-source discussion platform. Prior to 2026.6.0, 2026.5.1, 2026.4.2, and 2026.1.5, the signup flow could allow newly registered users to set primary_group_id and gain whisper-group privileges without legitimate group membership on sites with whispers_allowed_groups configured. This issue is fixed in versions 2026.6.0, 2026.5.1, 2026.4.2, and 2026.1.5.

### CVE-2026-33794

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:C/RE:M/U:Green` |
| Weaknesses | `CWE-754` |
| Published | 2026-07-09T21:16:54.790 |

An Improper Check for Unusual or Exceptional Conditions vulnerability in the 

advanced forwarding toolkit (evo-aftmand)

 of Juniper Networks Junos OS Evolved on PTX Series allows an unauthenticated network-based attacker generating continuous routing updates, resulting in unilist ECMP routes, to crash the 

evo-aftmand process on the PFE, leading to a Denial-of-Service (DoS). The conditions required for successful exploitation are based on a sequence of events that are outside an attacker's direct control.

Unified list (unilist) ECMP routes are a specific ECMP behavior where multiple equal-cost routes share a single logical next-hop list entry. The router treats them as one route with multiple next hops and load balances traffic across that unified list. Due to an issue processing unilist ECMP routing updates, internal state corruption may occur, especially in large-scale ECMP unilist deployments, leading to the evo-aftmand process crashing, resulting in an evo-aftmand-bx core. Manual intervention is required to recover by rebooting the system or restarting the FPC.

This issue affects Junos OS Evolved on PTX :


  *  from 24.4R2-EVO before 24.4R2-S3-EVO;
  *  from 25.2 before 25.2R2-EVO.

### CVE-2026-54771

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-75` |
| Published | 2026-07-10T00:16:33.737 |

Langroid is a framework for building large-language-model-powered applications. Prior to version 0.65.3, a Langroid application exposing a chat interface to untrusted users may allow direct tool invocation via raw JSON payloads, even when tools are registered with `use=False, handle=True`. Version 0.65.3 fixes the issue.

### CVE-2026-12598

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-10T00:16:32.727 |

The LoginPress Pro plugin for WordPress is vulnerable to authentication bypass in versions up to and including 6.2.3 via the Spotify Social Login addon. This is due to the loginpress_on_spotify_login() function trusting the unverified 'email' field returned by Spotify's /v1/me endpoint and using it directly with get_user_by('email', $profile['email']) to identify and log in an existing WordPress account, without confirming that the Spotify user actually owns the email address (Spotify documents that the profile email is unverified) and without requiring the user to prove ownership of the matching WordPress account. This makes it possible for unauthenticated attackers to log in as any existing WordPress user, including Administrators, by registering a Spotify account using the targeted user's email address and authenticating via the Spotify provider.

### CVE-2026-12597

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-10T00:16:32.603 |

The LoginPress Pro plugin for WordPress is vulnerable to Authentication Bypass via the GitHub OAuth callback in versions up to, and including, 6.2.3. The vulnerability exists in the loginpress_on_github_login() function, which blindly trusts the first element (profile[0]['email']) of the array returned by GitHub's /user/emails endpoint as an account-binding identifier without verifying that the email carries a verified === true status. This makes it possible for unauthenticated attackers to log in as any existing WordPress user, including administrators, by adding an unverified email address matching a local account to their GitHub profile and triggering the OAuth callback via a crafted code parameter — causing the plugin to call get_user_by('email', ...) and establish an authenticated session for the matched account. Practical exploitation is conditional on GitHub returning the attacker-added unverified email at index 0 of the /user/emails response, as GitHub typically prioritizes the primary verified address first; nonetheless, the absence of any email verification check in the plugin constitutes a fundamental authentication bypass flaw.

### CVE-2026-12595

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-10T00:16:32.120 |

The LoginPress Pro plugin for WordPress is vulnerable to Authentication Bypass via Unverified OAuth Email in all versions up to and including 6.2.3. The vulnerability exists in the loginpress_on_discord_login() Discord OAuth callback handler, which accepts the email field returned by Discord's /users/@me endpoint without ever checking that the profile's verified flag is true, then directly maps that email to a local WordPress account via get_user_by('email', $profile['email']) and issues an authenticated session cookie via wp_set_auth_cookie(). This makes it possible for unauthenticated attackers to take over any existing WordPress account — including administrator accounts — by registering a Discord account configured with an unverified email address that matches the target user's registered WordPress email and completing the standard Discord OAuth flow.

### CVE-2026-15293

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-10T05:16:32.700 |

The WP Business Intelligence Lite plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 3.2.0. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with Subscriber-level access and above, to modify stored SQL queries, which can lead to privilege escalation via arbitrary SQL execution when the modified query is viewed by an administrator.

### CVE-2026-59224

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-290` |
| Published | 2026-07-09T17:17:03.770 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. Prior to 0.10.0, backend/open_webui/routers/terminals.py built the ws_terminal upstream URL from an unencoded session_id and appended user_id as a query parameter, allowing query injection to make the terminal backend resolve another user identity; the HTTP proxy path also forwarded X-User-Id as an integrity-unbound identity claim. This issue is fixed in version 0.10.0.

### CVE-2026-56689

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-10T12:17:23.577 |

Dell PowerFlex Manager, Version prior to 5.1.0.1, contain(s) an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Information exposure.

### CVE-2026-59832

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-23` |
| Published | 2026-07-09T23:17:05.627 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.1, the /snippets/*filepath route handler serveSnippets in kernel/server/serve.go joins a single-decoded request path with the snippets directory without subpath containment or sensitive-path checks, allowing an authenticated request such as /snippets/%2e%2e/%2e%2e/conf/conf.json to read workspace secrets and the document database. This issue is fixed in versions 3.7.1.

### CVE-2026-33655

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-09T23:17:04.763 |

New API is a large language mode (LLM) gateway and artificial intelligence (AI) asset management system. Prior to 0.12.0-alpha.1, the default SSRF protection configuration did not apply IP filtering to hostnames; with ApplyIPFilterForDomain disabled by default, URL validation checked domain allow/block rules but did not resolve a hostname and validate the resolved IP address, allowing authenticated users to configure Webhook, Bark, or Gotify notification URLs that point at an internal or metadata IP address. This issue is fixed in version 0.12.0-alpha.1.

### CVE-2026-15271

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-272` |
| Published | 2026-07-09T22:17:02.210 |

A security vulnerability has been detected in TOTOLINK A3000RU, A3100R, A950RG, AC1200T10, CP450, CS185R_T10 and EX200 up to 20260906. Affected by this issue is some unknown functionality of the file /etc/boa/boa.conf of the component Web Interface. The manipulation leads to least privilege violation. The attack may be initiated remotely. The attack's complexity is rated as high. The exploitation is known to be difficult.

### CVE-2026-55208

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-09T21:16:56.020 |

Pimcore Studio Backend Bundle is the backend bundle for Pimcore Studio. Prior to 2025.4.6 and 2026.1.6, an authenticated user can extract the admin password hash and other database content through time-based blind SQL injection in the DateFilter column key parameter. The POST /pimcore-studio/api/website-settings endpoint and other listing endpoints accept a columnFilters array where the key field is interpolated directly into SQL with manual backtick wrapping, allowing a backtick character to break out of quoting and append arbitrary SQL such as SLEEP() and IF() subqueries. This issue is fixed in versions 2025.4.6 and 2026.1.6.

### CVE-2026-59221

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-918` |
| Published | 2026-07-09T18:16:55.613 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.9.6 before 0.10.0, _sanitize_proxy_path in backend/open_webui/routers/terminals.py decoded proxy paths only eight times, allowing a nine-times percent-encoded ../ traversal value to pass normalization checks and be decoded by the upstream terminal server. This issue is fixed in version 0.10.0.

### CVE-2026-59216

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-94;CWE-200;CWE-639;CWE-862` |
| Published | 2026-07-09T17:17:02.467 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. Prior to 0.10.0, get_event_call delivered execute:python and execute:tool Socket.IO events to a client-supplied session_id after checking only that the session was connected, allowing authenticated users who learned another socket ID through ydoc:document:join to run code interpreter Python or tools in that user session. This issue is fixed in version 0.10.0.

### CVE-2026-59208

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-346;CWE-346` |
| Published | 2026-07-09T16:16:46.610 |

n8n is an open source workflow automation platform. Prior to 2.27.4 and from 2.28.0 prior to 2.28.1, n8n instances configured with more than one trusted token-exchange issuer resolved external identities to local accounts using only the JWT sub claim and ignored the iss claim, allowing an attacker with a valid token from one trusted issuer and a sub matching a victim under another issuer to authenticate as that victim. This issue is fixed in versions 2.27.4 and 2.28.1.

### CVE-2026-13347

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-10T08:16:20.857 |

The Hide My WP Lite plugin for WordPress is vulnerable to Arbitrary File Read in versions up to and including 1.3 via the he_wrapper_js and he_wrapper_css query parameters processed by the elementor_assets_filter() function. This is due to the function concatenating user-supplied input directly onto ABSPATH and passing the result to file_get_contents() without any path traversal validation, allow-list, realpath containment, or extension check; the result is then echoed in the HTTP response. Although the output is passed through wp_kses_post(), that function only filters HTML tags and does not prevent disclosure of arbitrary file contents. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the affected site's server (such as wp-config). Note: The exploit requires the Elementor plugin and the 'Hide Elementor' feature to be enabled.

### CVE-2026-15291

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-10T05:16:32.430 |

The Chat Help – Click to Chat Button & Form plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 3.1.3 via the REST API endpoints /wp-json/chat-help/v1/leads and /wp-json/chat-help/v1/leads/{id}. This is due to the plugin not performing any authentication and authorization checks. This makes it possible for unauthenticated attackers to extract sensitive data including customer names, email addresses, phone numbers, WhatsApp messages, complete geolocation data (IP addresses, city, country, ISP, coordinates), device fingerprinting information (browser, OS, screen resolution), and WordPress account credentials (user IDs, usernames, emails, names) for logged-in users who submit forms.

### CVE-2026-15290

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-10T05:16:32.287 |

The Ultimate Member – User Profile, Registration, Login, Member Directory, Content Restriction & Membership Plugin plugin for WordPress is vulnerable to blind SQL Injection via the search parameter in all versions up to, and including, 2.10.1 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query.  This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. This vulnerability was partially patched in version 2.9.2 when initially addressing CVE-2025-0308.

### CVE-2026-15288

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-10T05:16:31.923 |

The SureForms – Drag and Drop Form Builder for WordPress plugin for WordPress is vulnerable to Improper Input Validation in all versions up to, and including, 2.2.1. This is due to the plugin accepting the payment amount directly from user-controlled POST data in the 'create_payment_intent' and 'create_subscription_intent' functions without validating it against the form's configured price. This makes it possible for unauthenticated attackers to modify the payment amount to any arbitrary value when submitting a Stripe payment form, potentially purchasing products or services at significantly reduced prices.

### CVE-2026-59834

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-09T23:17:05.900 |

SiYuan is an open-source personal knowledge management system. Prior to 3.7.1, the block search endpoint POST /api/search/fullTextSearchBlock concatenates attacker-controlled paths values into SQL predicates used by non-SQL search modes, allowing an unauthenticated publish visitor to inject a UNION SELECT and return rows from hidden documents by projecting an allowed visible box and path. This issue is fixed in versions 3.7.1.

### CVE-2026-54695

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-09T19:17:06.540 |

Pipecat is an open-source Python framework for building real-time voice and multimodal conversational agents. Prior to 1.4.0, the pipecat development runner registers a /ws WebSocket endpoint for telephony testing that accepts connections without authentication, reads an attacker-supplied callSid from a Twilio stream-start handshake in src/pipecat/runner/utils.py, and passes it to TwilioFrameSerializer so the server can issue an authenticated Twilio REST API hang-up request with the server operator's credentials; equivalent unauthenticated call-control sinks exist for Telnyx and Plivo. This issue is fixed in version 1.4.0.

### CVE-2025-63579

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-284;CWE-311;CWE-326` |
| Published | 2026-07-09T19:16:57.757 |

Unauthorized use of Kyocera printers, allows all information stored in the Kyocera address book to be exported. The security measure that encrypts incoming data ian be bypassed with this vulnerability, allowing encrypted data to be decrypted. Passwords and other sensitive information can be obtained. This affects Kyocera Command Center RX TASKalfa 2552ci, TASKalfa 3252ci, TASKalfa 2553ci, TASKalfa 3253ci, TASKalfa 3554ci, TASKalfa 4052ci, TASKalfa 5052ci, TASKalfa 6052ci, TASKalfa 7052ci, TASKalfa 8052ci, TASKalfa 7353ci, TASKalfa 8353ci, TASKalfa 2554ci, TASKalfa 3254ci, TASKalfa 505.

### CVE-2026-59720

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-284` |
| Published | 2026-07-09T18:16:57.063 |

Hoppscotch is an open source API development ecosystem. Prior to 2026.6.0, mock server creation in mock-server.service.ts does not persist the isPublic input field while schema.prisma defaults isPublic to true, causing mock servers linked to private collections to be publicly accessible without authentication and potentially expose sensitive API data. This issue is fixed in version 2026.6.0.

### CVE-2026-55420

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-09T18:16:54.440 |

Discourse is an open-source discussion platform. Prior to 2026.6.0, 2026.5.1, 2026.4.2, and 2026.1.5, under certain non-default configurations, processing of PDF uploads could be exploited to obtain RCE on the server. This issue is patched in 2026.6.0, 2026.5.1, 2026.4.2, and 2026.1.5.

### CVE-2026-51606

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-09T17:17:01.173 |

An improper input handling vulnerability in the RTSP service of Tenda CP3 V3.0 (firmware V31.1.9.91) causes the device to abruptly terminate the TCP connection with a RST packet when a request containing an oversized field value is received, without returning any RFC 2326-compliant error response. This behavior affects the request-line URL field and header field values across multiple RTSP request types.

### CVE-2026-51605

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-09T17:17:01.070 |

A stack-based buffer overflow vulnerability in the RTSP service of Tenda CP3 V3.0 (firmware V31.1.9.991) allows an unauthenticated remote attacker to cause a denial of service via a crafted TEARDOWN request.

### CVE-2026-51604

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-09T17:17:00.970 |

A stack-based buffer overflow vulnerability in the RTSP service of Tenda CP3 V3.0 (firmware V31.1.9.91) allows an unauthenticated remote attacker to cause a denial of service via a crafted PLAY request.

### CVE-2026-51603

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-09T17:17:00.867 |

A stack-based buffer overflow vulnerability in the RTSP service of Tenda CP3 V3.0 (firmware V31.1.9.91) allows an unauthenticated remote attacker to cause a denial of service via a crafted second SETUP request. After completing the OPTIONS, DESCRIBE, and a legitimate first SETUP request to obtain a valid session ID, the RTSP service's second-stage URL routing parser fails to validate the length of the URL field in the subsequent SETUP request. By supplying a URL consisting of exactly four consecutive repetitions of a valid RTSP URL, an attacker can bypass first-stage format validation and trigger a stack buffer overflow, causing an immediate crash of the RTSP service process and rendering the device inaccessible to all clients on the local network.

### CVE-2026-51602

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-09T17:16:59.930 |

A stack-based buffer overflow vulnerability in the RTSP service of Tenda CP3 V3.0 (firmware V31.1.9.91) allows an unauthenticated remote attacker to cause a denial of service via a crafted SETUP request. The RTSP service's second-stage URL routing parser fails to validate the length of the URL field in the first SETUP request. By supplying a URL consisting of exactly four consecutive repetitions of a valid RTSP URL, an attacker can bypass first-stage format validation and trigger a stack buffer overflow, causing an immediate crash of the RTSP service process and rendering the device inaccessible to all clients on the local network.

### CVE-2026-51600

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-703` |
| Published | 2026-07-09T17:16:59.693 |

Tenda CP3 V3.0 firmware V31.1.9.91 does not validate the Content-Length header field in RTSP requests (including DESCRIBE, SETUP, and PLAY methods). When a request carrying a Content-Length header is received without a corresponding message body, the RTSP parser enters a persistent body-awaiting state, causing the affected TCP connection to become permanently non-functional. The device does not actively close the connection, resulting in a TCP resource leak. This issue can be exploited by an unauthenticated remote attacker to cause a denial-of-service condition.

### CVE-2026-13462

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-09T17:16:57.090 |

PayRange Android app, version 7.0.7 and below, contains an SSL bypass vulnerability that allows invalid certificates to be accepted in application webviews. A remote and unauthenticated attacker can steal information that the user sends.

### CVE-2026-55424

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-09T22:17:06.097 |

Discourse is an open-source discussion platform. Prior to 2026.6.0, 2026.5.1, 2026.4.2, and 2026.1.5, a topic "featured link" was not sufficiently normalized and escaped before being rendered in the topic list, allowing a user who can set a featured link to inject JavaScript when default Content Security Policy protections were modified or disabled. This issue is fixed in versions 2026.6.0, 2026.5.1, 2026.4.2, and 2026.1.5.

### CVE-2026-49276

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-83` |
| Published | 2026-07-09T19:17:05.670 |

Kirby is an open-source content management system. Prior to 4.9.4 and 5.4.4, Kirby sites using the writer field in any blueprint allowed a scripting link to be included as the target of a link or email link in writer mark components, making the target clickable by the user who entered it and enabling self cross-site scripting in the Panel. This issue is fixed in versions 4.9.4 and 5.4.4.

### CVE-2026-53963

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-09T22:17:05.763 |

Discourse is an open-source discussion platform. Prior to 2026.6.0, 2026.5.1, 2026.4.2, and 2026.1.5, a malicious second factor name on an attacker-controlled account was not escaped in the delete confirmation dialog, allowing stored cross-site scripting when an administrator impersonated that account. This issue is fixed in versions 2026.6.0, 2026.5.1, 2026.4.2, and 2026.1.5.

### CVE-2026-59214

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-09T17:17:02.177 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. Prior to 0.10.0, Open WebUI runs client-side Python with Pyodide in a same-origin web worker, allowing stored chat payloads that use pyodide.http.pyfetch or the js module fetch and XMLHttpRequest APIs to issue authenticated same-origin requests when a victim clicks Run, which can reach admin-only endpoints and execute server-side code through configured tools. This issue is fixed in version 0.10.0.

### CVE-2026-53987

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-09T17:17:01.277 |

The Tag plugin for GLPI 11 before 2.14.4 stores the tag name without HTML sanitization and renders it into the Kanban badge markup via PluginTagTag::preKanbanContent() without output escaping, resulting in stored cross-site scripting. An authenticated user with TAG MANAGEMENT create or update rights can set a tag name containing HTML, which then executes in the browser of any user who opens the Kanban view of a ticket, problem, change, or project the tag is attached to.

### CVE-2026-22659

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-10T14:16:52.547 |

FlaskBB through 2.2.0, fixed in commit acc88cf, contains an authorization bypass vulnerability that allows authenticated moderators to perform unauthorized actions on topics in forums they do not control by submitting crafted topic ID lists. Attackers can include a low-ID topic from a permitted forum as an anchor in a batch request, causing the permission check applied only to the first result to pass, and then execute lock, unlock, delete, or hide actions against topics in unmoderated forums.

### CVE-2026-15298

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-10T05:16:33.117 |

The TelSender plugin for WordPress is vulnerable to DOM-Based Cross-Site Scripting in all versions up to, and including, 1.14.14. This is due to insufficient input sanitization when processing Telegram API responses containing attacker-controlled chat titles. This makes it possible for unauthenticated attackers to inject malicious scripts via Telegram chat titles that execute when an administrator opens the TelSender settings page and clicks the "Tested" button.

### CVE-2026-13430

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-10T04:17:47.430 |

The Post Export Import with Media plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 1.13.1 via the import_media_file_secure function. This is due to insufficient file extension validation caused by a trailing-dot filename bypass, where the extension allow-list check in ajax_import_media_start() uses pathinfo() on the raw ZIP entry name (e.g., 'shell.php.'), which returns an empty string for the extension, causing the allow-list guard to be skipped and the file to be extracted to a temporary location, after which import_media_file_secure() copies it into the WordPress uploads directory without re-validating the extension. This makes it possible for authenticated attackers, with administrator-level access and above, to upload files that may be executable, which makes remote code execution possible.

### CVE-2026-59721

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-78;CWE-915` |
| Published | 2026-07-09T18:16:57.200 |

Hoppscotch is an open source API development ecosystem. Prior to 2026.6.0, the updateInfraConfigs GraphQL mutation in admin/infra.resolver.ts accepts an attacker-controlled MAILER_SMTP_URL value, and validateSMTPUrl in utils.ts permits path, query, or fragment content that nodemailer parses into sendmail transport options, allowing an admin to execute arbitrary commands as root in the backend container after restart and mail sending. This issue is fixed in version 2026.6.0.

### CVE-2026-41878

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-10T10:16:23.957 |

R-SOFT DMS is vulnerable to Insecure Direct Object Reference (IDOR) attack in multiple file download endpoints. The application fetches files from the database by ID and serves them to whoever requests them, relying only on session authentication, meaning any valid user can access any file.

This issue was fixed in version v3.19-2862 and v3.17-2580.

### CVE-2026-50181

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-23` |
| Published | 2026-07-10T00:16:33.340 |

Langroid is a framework for building large-language-model-powered applications. Prior to version 0.64.0, Langroid's `ReadFileTool` and `WriteFileTool` appear to treat `curr_dir` as the intended working-directory boundary for file operations. However, the tools only change the process working directory to `curr_dir` and then operate on the user-supplied `file_path` without resolving and enforcing that the final path remains inside `curr_dir`. As a result, a tool caller can supply path traversal sequences such as `../secret.txt` to read files outside the configured current directory, or `../written_by_tool.txt` to write files outside that directory. This can impact applications that expose Langroid file tools to an LLM agent, user-controlled tool call, or delegated coding/documentation agent while relying on `curr_dir` to restrict file access to a project/workspace directory. Version 0.64.0 patches the issue.

### CVE-2026-57032

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-236` |
| Published | 2026-07-09T22:17:09.007 |

An Improper Handling of Undefined Parameters vulnerability in the packet forwarding engine (pfe) of Juniper Networks Junos OS on EX Series devices allows an authenticated attacker with low privileges to cause a Denial-of-Service (DoS).

If an attempt is made to subscribe to an unsupported telemetry sensor path on EX2300, EX3400, EX4000, EX4100 and EX4400 via gRPC, this causes the FPC to crash. This leads to a complete service outage until the module has automatically restarted. 

The following log message can be seen when this issue happens:

agentd[<PID>]: AGENTD_RESOURCE_NOT_FOUND: No resource name found for <sensor>


This issue affects Junos OS on 

EX2300, EX3400, EX4000, EX4100 and EX4400

devices:


  *  all versions before 23.2R2-S7,
  *  23.4 versions before 23.4R2-S8,
  *  24.2 versions before  24.2R2-S5,
  *  24.4 versions before 24.4R2.

### CVE-2026-57027

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-07-09T22:17:08.093 |

A Missing Release of Memory after Effective Lifetime vulnerability in the packet forwarding engine (pfe) of Juniper Networks Junos OS on specific EX Series devices allows an unauthenticated adjacent attacker to cause a Denial-of-Service (DoS).When sFlow is configured in a Virtual Chassis (VC) scenario with EX4100 Series or EX4400 Series devices, multicast traffic which is received on one VC member and sent out on another member leads to a memory leak and ultimately an FPC crash and restart.

The leak can be monitored by watching the continuous increase of the buffer values in the output of:

user@host> show chassis fpc 
This issue affects Junos OS on EX4100 Series and EX4400:


  *  all versions before 23.2R2-S7,
  *  23.4 versions before 23.4R2-S7,
  *  24.2 versions before 24.2R2-S4,
  *  24.4 versions before 24.4R2.

### CVE-2026-57020

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:X/RE:M/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-07-09T22:17:06.887 |

An Improper Check for Unusual or Exceptional Conditions vulnerability in the packet forwarding engine (pfe) of Juniper Networks Junos OS on QFX10000 Series allows an unauthenticated, adjacent attacker to cause a Denial-of-Service (DoS).

On all QFX10000 platforms in an EVPN-VxLAN scenario, if an attacker sends IPv6 multicast traffic and these packets reach the non-IRB interface of a spine switch it floods the packet to other spines and all Ethernet Segment Identifier (ESI) leaf switches. This flooding causes the packet to be forwarded in a endless loop, which can lead to saturation of the involved links and in turn impact to legitimate traffic.



This issue affects Junos OS on QFX10000 Series:


  *  all versions before 23.2R2-S7,
  *  23.4 versions before 23.4R2-S8,
  *  24.2 versions before 24.2R2-S4,
  *  24.4 versions before 24.4R2-S4.



This issue does not affect Junos version after 24.4 as the QFX10000 Series devices are not supported on newer versions anymore.

### CVE-2026-57019

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-09T22:17:06.707 |

An Improper Validation of Specified Quantity in Input vulnerability in the Packet Forwarding Engine (pfe) of Juniper Networks Junos OS on MX Series allows an unauthenticated, adjacent attacker to cause a Denial-of-Service (DoS).


When a specific packet is received from device in the same broadcast domain, an affected system calculates the packet size incorrectly. This causes further packet processing to fail, which triggers an FPC major error, resulting in a FPC reset impacting traffic until the FPC has automatically recovered.

Affected scenarios are: MAP-T, or non-IP traffic encapsulated in IP (e.g. MPLS over GRE).

When this issue happens the following logs can be observed:

fpc<#> CMError: /fpc/0/pfe/0/cm/0/MQSS(0)/0/MQSS_CMERROR_LI_INT_REG_UNROLL_TAIL_LENGTH_OVF (0x2205eb), scope: pfe, category: functional, severity: major, module: MQSS(0), type: LI: Unroll TAIL length overflow, oc_category: default
fpc<#> Performing action reset-fru for error /fpc/0/pfe/0/cm/0/MQSS(0)/0/MQSS_CMERROR_LI_INT_REG_UNROLL_TAIL_LENGTH_OVF (0x2205eb) in module: MQSS(0) with scope: pfe category: functional level: major, oc_category: default




This issue affects Junos OS on MX Series:


  *  all versions before 23.2R2-S6,
  *  23.4 versions before 23.4R2-S7,
  *  24.2 versions before 24.2R2-S4,
  *  24.4 versions before 24.4R2-S4,
  *  25.2 versions before 25.2R2.

### CVE-2026-55865

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-09T21:16:56.277 |

Python Liquid is a Python engine for the Liquid template language. Prior to 2.2.1, given a malformed {% case %} tag without an associated {% when %} or {% else %} block and no terminating {% endcase %} tag, Python Liquid hangs in an infinite loop at parse time because liquid.TokenStream.eof did not give the EOF token matching kind and value fields, allowing malicious template authors to craft templates for a denial of service attack. This issue is fixed in version 2.2.1.

### CVE-2026-55212

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-09T21:16:56.150 |

Pimcore is an Open Source Data & Experience Management Platform. Prior to 2025.4.6 and 2026.1.6, the Studio API class definition creation endpoint POST /pimcore-studio/api/class/definition/configuration-view/detail/create is guarded by the objects permission instead of the classes permission, allowing a standard editor-level user to create class definitions without admin privileges. Class definition creation generates new database tables and PHP class files on the server, and missing API-layer UID format validation allows malformed UIDs to reach model-layer validation and return internal exceptions. This issue is fixed in versions 2025.4.6 and 2026.1.6.

### CVE-2026-33801

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-07-09T21:16:55.330 |

An Improper Check for Unusual or Exceptional Conditions vulnerability in the routing protocol daemon (RPD) of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent, unauthenticated attacker sending a specific BGP update over an established BGP session to cause a Denial-of-Service (DoS).

Upon receipt of a specifically malformed non-inet/inet6 unicast BGP update, an RPD crash and restart is triggered, which will cause a complete service outage until routing has reconverged. The rpd crash occurs before the update can be readvertised, so there is no downstream propagation.


This issue affects:



  *  Junos OS versions 25.2 before 25.2R2;


  *  Junos OS Evolved versions 25.2 before 25.2R2-EVO.




This issue doesn't affect Junos OS versions before 25.2R1 nor Junos OS Evolved versions before 25.2R1-EVO.

### CVE-2026-33800

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-606` |
| Published | 2026-07-09T21:16:55.163 |

An Unchecked Input for Loop Condition vulnerability in the Packet Forwarding Engine (pfe) of Juniper Networks Junos OS on MX Series allows an unauthenticated, adjacent attacker to cause a Denial-of-Service (DoS).Micro-BFD session flaps generate respective up/down events which are queued by PFEMAN for processing. Especially in a Virtual-Chassis (VC) scenario with locality‑bias configured, processing takes a significant amount of time for each event. If these sessions keep flapping, new events are constantly added, and in turn PFEMAN never completes processing these events. This results in the PFEMAN watchdog timer expiring, which causes the FPC to crash and restart, representing a complete service outage.


This issue only affects MX series FPCs up to and including MPC9. It does not affect MPC10/11, LC4800/9600 and MX304.

This issue affects Junos OS on MX Series:


  *  all versions before 23.2R2-S7,
  *  23.4 versions before 23.4R2-S8,
  *  24.2 versions before 24.2R2-S4,
  *  24.4 versions before 24.4R2-S3,
  *  25.2 versions before 25.2R2.

### CVE-2026-54005

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-09T19:17:06.400 |

Kirby is an open-source content management system. Prior to 4.9.4 and 5.4.4, Kirby sites where a role has the pages.access permission disabled allowed authenticated users who know or guess page IDs or UUIDs to retrieve page information, including full content and metadata, for arbitrary published pages through the /api/site/find route without authorization to access those pages. This issue is fixed in versions 4.9.4 and 5.4.4.

### CVE-2026-59219

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-613` |
| Published | 2026-07-09T17:17:02.877 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.9.0 before 0.10.0 with Redis configured, Socket.IO connect, user-join, join-channels, join-note, and the terminal websocket first-message authentication used decode_token without the Redis-backed is_valid_token revocation check, allowing revoked JWTs to continue authenticating realtime connections. This issue is fixed in version 0.10.0.

### CVE-2026-59209

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-07-09T17:17:01.780 |

n8n is an open source workflow automation platform. Prior to 1.123.61, 2.27.4, and, 2.28.1, an authenticated member with use-only editor access to a shared workflow could read credential-populated headers exposed via the $request object inside an HTTP Request node's pagination expression and exfiltrate the secret through item data. This issue is fixed in versions 1.123.61, 2.27.4, and 2.28.1.

### CVE-2026-59207

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693;NVD-CWE-noinfo` |
| Published | 2026-07-09T16:16:46.470 |

n8n is an open source workflow automation platform. Prior to 2.27.4 and 2.28.1, the AI Agents feature did not enforce the Allowed HTTP Request Domains restriction configured on credentials when an MCP tool was pointed at an arbitrary URL, allowing a member-level user with use-only access to a shared credential to send its secret to an external server they control. This issue is fixed in versions 2.27.4 and 2.28.1.

### CVE-2026-59206

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-07-09T16:16:46.323 |

n8n is an open source workflow automation platform. Prior to 1.123.61, 2.27.4, and, 2.28.1, an authenticated user with the default workflow:create permission could pollute Object.prototype through a crafted workflow saved, updated, or imported via the workflow API, allowing unauthenticated requests to be treated as a privileged user and exposing user and project listing endpoints. This issue is fixed in versions 1.123.61, 2.27.4, and 2.28.1.

### CVE-2026-54798

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-07-09T15:16:36.443 |

A vulnerability has been identified in CPCI85 Central Processing/Communication (All versions < V26.20), SICORE Base system (All versions < V26.20.0). The affected application includes a debugging interface that is accessible through HTTP endpoints. This could allow an authenticated attacker to disrupt the system by crashing the web process causing denial of service conditions.
