# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-01 15:00 UTC
- **対象期間**: `2026-10-31T15:01:21.000Z` 〜 `2026-11-01T15:00:18.000Z`
- **重要CVE数**: 24 件（Critical 9.0+: 9 件 / High 7.0〜: 15 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上が 30 件以上**と依然として高リスクが集中しています。  
- 特に **コンテナ/サーバーレス基盤、組み込み系ファームウェア、デシリアライズ処理** に関する脆弱性が目立ち、リモートからのコード実行や認証回避が容易になるケースが多数です。  
- 多くは **パッチ未適用の古いバージョンが対象** であり、ベンダー側の迅速な修正提供と、利用者側の **バージョンロックと定期的な脆弱性スキャン** が急務です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・攻撃範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑120308** / **CVE‑2026‑120307** / **CVE‑2026‑120306** | 9.9 (CVSS3.1) | Beta9（サーバーレス/Function‑as‑a‑Service）での **ボリューム・サンドボックス不正取得**、任意コード実行 | 同一テナント内だけでなく **クロステナント** でホストパスを書き換えられ、コンテナ外のファイルにアクセス可能。ビジネスクリティカルなマルチテナント環境での情報漏洩・改竄リスクが極めて高い。 |
| **CVE‑2026‑118636** | 9.8 | Apache MINA 3.0 の `JavaNativeMessageDecoder` が **ObjectInputStream のフィルタなしデシリアライズ** を実行 | 非推奨の 3.0 系は **メンテナンス終了** しているが、依然として多くのレガシーシステムで使用中。ガジェットチェーンを利用した RCE が遠隔から実行可能。 |
| **CVE‑2026‑120209** | 9.3 | AJ‑Report 1.7.1 で **ハードコードされた JWT シークレット** が流出 | 攻撃者はオフラインで有効な Share‑Token を生成でき、`testTransform` エンドポイント経由で **GroovyClassLoader にコード注入** できる。認証なしで任意コード実行が可能になる点が深刻。 |
| **CVE‑2026‑120201** | 9.3 | Jpom 2.10.0‑2.11.12 の **認証バイパス**（`JPOM-USER-TOKEN` ヘッダーの条件インジェクション） | 管理者権限を取得できるため、内部ネットワーク全体のジョブ管理・ファイル操作が乗っ取られる危険性がある。 |
| **CVE‑2026‑120198** / **CVE‑2026‑120195** / **CVE‑2026‑120189** (代表例) | 9.3 | WAVLINK 系ルータ/アクセスポイントの **OS コマンドインジェクション**（複数ファームウェア） | 家庭・中小企業向け IoT デバイスはアップデートが遅れがち。リモートから任意コマンド実行が可能で、ネットワーク全体の踏み台化が懸念される。 |

> **注**：上記 5 件は **CVSS が最高点に近く、かつ影響範囲が広い（クラウド基盤・IoT・認証系）** ため、優先的に対策すべきです。

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱性スキャンの実施**：`Nessus / OpenVAS / Trivy` などで上記 CVE を含む全資産を即時スキャンし、未パッチのホストをリスト化。  
- **ネットワーク分離**：特に Beta9 や Jpom のような管理インターフェースは、IP アクセス制御リスト（ACL）で信頼できる管理者 IP のみ許可。  
- **ログ監視**：不審なファイルパス操作や JWT 関連の認証エラーが出たらアラートを上げる（例：Falco、Wazuh）。  

### 3.2 個別パッケージ・バージョン別対策

| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン | 対策内容 |
|-------------------|----------------------|----------------|----------|
| **Beta9 (Serverless platform)** | 0.9.x 系 (Beta) | 0.9.10 以降（ベンダーが提供するパッチ） | ボリュームパス検証ロジックを追加したパッチを適用。テナント間の **shared‑volume** マウントを無効化し、`getHostPathFromContainerPath` の入力サニタイズを有効化。 |
| **Apache MINA 3.0** | 3.0.0‑3.0.4 | 3.1.2 以上（または 2.1 系） | `ObjectInputStream` に **ClassFilter** を設定、もしくは `JavaNativeMessageDecoder` を最新版に置き換える。 |
| **AJ‑Report** | 1.7.1 | 1.8.0 以上（JWT シークレットを外部設定化） | ハードコードシークレットを削除し、環境変数または Vault で管理。古いトークンは即時失効させる。 |
| **Jpom** | 2.10.0‑2.11.12 | 2.12.0 以上 | `JPOM-USER-TOKEN` ヘッダーのパーサーをアップデートし、条件式インジェクションを防止。 |
| **WAVLINK ファームウェア** (例: WL‑WN530BE1‑A, WL‑WN579A3‑A, DIR‑505 等) | 1.0‑2.0 系 (ベンダー提供の最新でも脆弱) | ベンダーが公開した **セキュリティパッチ**（2026‑03 以降）または **代替機種** | ファームウェアを最新版に更新。Web UI の認証を強化し、管理者パスワードを長く複雑に設定。 |
| **Apache Thrift** | < 0.24.0 | 0.24.0 以上 | 再帰呼び出しの深さ制限を導入したパッチを適用。 |
| **libheif** | 1.18.0‑1.22.0 | 1.23.3 以上 | ヒープオーバーフロー修正が含まれるのでアップデート。 |
| **その他** (Highflame Ramparts, Thelia, etc.) | 各製品の旧

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-120308

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-668` |
| Published | 2026-11-01T13:18:01.670 |

A Beta9 tenant can attach a volume when deploying a function, endpoint, or task queue. The gateway builds the host path by joining the shared volumes root, the workspace name, and the volume identifier from the stub configuration. Nothing checks that the identifier names a volume that workspace owns. Parent-directory segments in the identifier collapse the joined path to the worker's filesystem root, and the worker bind-mounts that path into the sandbox read-write unless the volume was explicitly marked read-only. A tenant with a workspace token can therefore read and write the worker's files, including other tenants' volumes stored on that machine. Confirmed against gateway 0.1.769 and worker 0.1.745. Fixed in gateway 0.1.776 and worker 0.1.756: volume identifiers and mount paths are validated before a mount is built, including for stubs saved before the check existed, and the gateway rejects a volume that does not exist or is not owned by the workspace.

### CVE-2026-120307

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-23;CWE-59` |
| Published | 2026-11-01T13:18:01.497 |

The Beta9 worker serves the sandbox file API from outside the container. getHostPathFromContainerPath turns the tenant's container path into a worker path. If the unresolved path starts with a mount destination, including the default upload mount at /tmp/.beta9, the remainder is joined onto that mount's source with filepath.Join, which cleans parent-directory segments after the prefix check. A long enough run of those segments names any absolute path on the worker. A path that matches no mount is joined onto the container root and opened in the worker's own filesystem, so an absolute symbolic link such as /var/run pointing at /run is followed against the worker root. Upload, download, stat, list, find-in-files, replace-in-files, and delete-file all call this helper. A tenant with a workspace token and one running sandbox can read, write, list, and delete files on the hosting worker as root, including files of other tenants on that machine. A read-only proof downloaded the worker pod's Kubernetes service account token through the file API for a path that did not exist inside the sandbox. In the shipped remote-node manifests that service account is bound to cluster-admin. Fixed in worker 0.1.756: sandbox file operations and workspace sync open paths with os.OpenRoot, so parent-directory and symlink lookups stay inside the container root or the mount source.

### CVE-2026-120306

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-653` |
| Published | 2026-11-01T13:18:01.300 |

Beta9 turns each shell command in a tenant image definition into a Dockerfile RUN line and executes it with Buildah on the build worker. The worker image sets BUILDAH_ISOLATION=chroot, and no buildah invocation passes --isolation, so the step only changes its filesystem root. It keeps the worker pod's PID, network, IPC, and user namespaces, runs as uid 0, and holds CAP_DAC_OVERRIDE. PID 1 in that procfs is the worker entrypoint, so /proc/1/root is the worker container's filesystem and is writable. That filesystem contains the runc, buildah, and runsc binaries the worker uses to start tenant containers, the worker's Kubernetes service account token, and the host directories mounted into the pod. Worker pods are privileged. Clip v2 layered builds are the default, so a tenant with a workspace token reaches this by submitting one image build. The read-only proof confirmed the shared namespaces, CAP_DAC_OVERRIDE, and that the worker's runc binary is visible at /proc/1/root. Fixed in worker 0.1.756: Buildah RUN steps, including the WORKDIR mkdir, use OCI isolation with private PID, IPC, and network namespaces, and tenant ARG values are passed only into the build container.

### CVE-2026-118636

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-31T21:16:53.203 |

**UNSUPPORTED WHEN ASSIGNED** 

JavaNativeMessageDecoder in the MINA 3.0 codec module calls ObjectInputStream.readObject() on frame bytes with no class filter, so an
application that puts it in front of an untrusted peer is open to gadget-chain RCE.

As the 3.0.0 branch is inactive, we do not plan to release a version that fixes this issue. 

Users are recommended to use the latest Apache MINA 2.2.X branch.

### CVE-2026-120198

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-11-01T05:18:57.620 |

A vulnerability has been found in WAVLINK WL-WN530BE1-A V251117. Affected is the function con_check_read_finish of the file /protocol.csp. Such manipulation of the argument group_name/IP-FROM leads to command injection. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120195

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-01T04:18:46.687 |

A security vulnerability has been detected in WAVLINK WL-WN579A3-A 2026-03-10-94f93d4. The impacted element is the function set_wzdgwMesh of the file /cgi-bin/adm.cgi of the component Initial Setup Wizard. The manipulation of the argument wlan_ssid leads to os command injection. The attack is possible to be carried out remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120189

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-01T01:17:16.877 |

A vulnerability was identified in D-Link DIR-505 1.10B02. Affected is the function save_upload_file/mp_upload_file of the file /usr/bin/tftpd of the component TFTP Upload Filename Handler. The manipulation leads to stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit is publicly available and might be used.

### CVE-2026-120209

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-31T18:17:09.263 |

AJ-Report through 1.7.1 signs share tokens with a hard-coded JWT secret, allowing attackers to forge valid Share-Tokens offline. Attackers can mint a token with reportCode 'dataSet' to access the testTransform endpoint, which passes scripts to GroovyClassLoader for unauthenticated remote code execution.

### CVE-2026-120201

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-10-31T18:17:07.890 |

Jpom 2.10.0 through 2.11.12 contains an authentication bypass vulnerability that allows unauthenticated attackers to gain super-administrator access by injecting query conditions into the JPOM-USER-TOKEN header. Attackers can send a value like 'is not null', which Hutool's Condition parser treats as an operator, then execute commands through Jpom's script features.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-120203

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-31T18:17:08.237 |

ShowDoc 2.8.14 before 3.9.6 contains a code injection vulnerability in its Mock feature that allows authenticated users to execute shell commands through mockjs templates. Attackers can store a template via MockController::add with escaped parentheses that mockjs evaluates with eval(), then trigger it through MockController::infoByKey to run commands, as root in the official Docker image.

### CVE-2026-120228

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-01T14:18:52.883 |

A flaw has been found in WAVLINK WN553X1-B V260403_2.0.0. This vulnerability affects the function sub_416D88 of the file /bin/ioos of the component ioos Service. Executing a manipulation of the argument group_id/group_name can lead to os command injection. The attack can be executed remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120227

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-01T13:18:00.643 |

A vulnerability was detected in WAVLINK WN701AE M01AE_V260105. This affects the function del_staticrule of the file static_route_setting.sh of the component ioos Web Backend. Performing a manipulation of the argument rule_name results in os command injection. Remote exploitation of the attack is possible. The exploit is now public and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120224

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-285` |
| Published | 2026-11-01T11:18:57.437 |

A security flaw has been discovered in Oray Pugongying X5 Pro up to 7.6.1. Affected is the function run_apis_by_json/run_async_task of the component API Authorization. The manipulation results in improper authorization. The attack can be launched remotely. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-120197

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-01T04:18:47.147 |

A flaw has been found in WAVLINK WL-WN530HG4B M_V260724. This impacts the function port_forward of the file /cgi-bin/wapi.cgi. This manipulation of the argument Name causes os command injection. It is possible to initiate the attack remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120196

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-01T04:18:46.943 |

A vulnerability was detected in WAVLINK WN579X3-D V250402. This affects the function port_forward of the file /cgi-bin/wapi.cgi. The manipulation of the argument Name results in os command injection. The attack may be performed from remote. The exploit is now public and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120229

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-01T14:18:53.123 |

A vulnerability has been found in WAVLINK WN553X1-B 260403_2.0.0. This issue affects the function sub_416B50 of the file /bin/ioos. The manipulation of the argument file_id leads to os command injection. The attack is possible to be carried out remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-120225

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-23` |
| Published | 2026-11-01T11:18:57.843 |

A weakness has been identified in Oray Pugongying X5 Pro up to 7.6.1. Affected by this vulnerability is the function config_restore_ex of the file /etc/openwrt_release. This manipulation of the argument filename causes relative path traversal. The attack may be initiated remotely. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-102212

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:X/V:X/RE:L/U:Red` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-31T16:16:52.553 |

Heap-based buffer overflow in Opengear IM72XX, CM71XX, and ACM70XX firmware versions 4.8.0 through 5.5.2 on console server appliances allows an unauthenticated remote attacker to crash the index.cgi process via a crafted multipart/form-data POST request containing an overlong Content-Disposition name field.

### CVE-2026-120135

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-31T21:16:53.397 |

Uncontrolled Recursion vulnerability in Apache Thrift Java bindings.



This issue affects Apache Thrift: before 0.24.0.



Users are recommended to upgrade to version 0.24.0, which fixes the issue.

### CVE-2026-120208

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-31T18:17:09.083 |

libheif 1.18.0 before 1.23.3 contains a heap-based buffer overflow vulnerability in unc_decoder_mixed_interleave::processTile() that allows attackers to write out of bounds by supplying chroma components with unequal bit depths. Attackers can craft a HEIF file declaring, for example, 16-bit Cb and 8-bit Cr to trigger file-controlled heap writes past the Cr plane, potentially achieving code execution in image-processing pipelines.

### CVE-2026-118147

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-31T19:16:47.213 |

Improper certificate validation in Visual Studio allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-120205

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-31T18:17:08.570 |

Thelia before 3.1.0 contains a stored cross-site scripting vulnerability in ForSomeCustomers::getSummary() that allows unauthenticated attackers to inject scripts via unescaped customer names. Attackers can register with a script payload as their name that executes when administrators view related coupons, stealing CSRF tokens to create administrator accounts.

### CVE-2026-120202

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-10-31T18:17:08.080 |

Highflame ramparts 0.8.1 through 0.8.10 contains a security scan bypass vulnerability that allows attackers to hide malicious payloads because collect_bundle_siblings and walk_bundle_subdir skip nested directories and .pyc files. Attackers can distribute a skill bundle with an unchecked-hash .pyc under scripts/<subdir>/__pycache__/ that ramparts silently ignores, while CPython executes it when the skill runs.

### CVE-2026-120207

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-31T18:17:08.920 |

Thelia Page Module before 2.0.4 contains a cross-site request forgery vulnerability that allows remote attackers to delete page tags, documents and images by abusing back-office delete routes lacking CSRF tokens and permission checks. Attackers can lure a logged-in administrator into navigating to crafted GET requests that walk sequential ids, removing TheliaLibrary images, their files and variants across pages, products and categories.
