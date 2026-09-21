# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-21 15:00 UTC
- **対象期間**: `2026-09-20T15:00:25.000Z` 〜 `2026-09-21T15:00:25.000Z`
- **重要CVE数**: 44 件（Critical 9.0+: 6 件 / High 7.0〜: 38 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上が 30 件以上** と依然として高リスクが集中しています。  
- **Web アプリケーション（Joomla、D‑Link ルータ、Netcore NBR200V2）** と **サーバー側ライブラリ（libXrender、Tuleap）** に対するリモートコード実行／コマンドインジェクションが目立ち、特権昇格や完全なシステム乗っ取りが可能です。  
- 多くは **認証不要**、または **認証済みでも特権ユーザーでなくても実行可能** な脆弱性であり、攻撃者がネットワークに到達できれば即座に悪用できる点が共通しています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 種類 | 主な影響範囲 | 注目理由 |
|-----|------|------|--------------|----------|
| **CVE‑2026‑88857** / **CVE‑2026‑88856** | 9.4 | Joomla Extension – OrdaSoft Gallery (認証済み特権 RCE) | Joomla 6.2.7 未満で OrdaSoft Gallery を使用している全サイト | 同一コードベースで **ファイル名を検証せずに保存**、および **JSON の `method` フィールドを直接 PHP 関数として実行** するため、認証済み管理者権限があれば任意コード実行が可能。プラグインは多数の中小企業サイトで採用されているため、被害拡大リスクが高い。 |
| **CVE‑2026‑94097** | 9.3 | Netcore NBR200V2 (CGI Diagnostic Endpoint) – コマンドインジェクション | NBR200V2 1.3.241127.071246 以前の全デバイス | `/www/cgi-bin/network_tools` の `param/key/val` パラメータがサニタイズされず、リモートからシェルコマンドを実行できる。管理画面への認証が不要で、IoT/産業用ネットワークに広く展開されている点が危険。 |
| **CVE‑2026‑94089** | 9.3 | D‑Link DIR‑868L – 認証ハンドラのスタックバッファオーバーフロー | DIR‑868L 2.01b05 以前の全モデル | `strcpy` で `id/password` パラメータを直接コピーし、スタック破壊により任意コード実行が可能。家庭用・小規模オフィスの Wi‑Fi ルータに多く搭載されている。 |
| **CVE‑2026‑84285** | 8.8 | Tuleap Enterprise Edition – OS コマンドインジェクション | Tuleap 17.3〜17.5 | 管理者権限が不要な **POST** パラメータでシェルコマンドを注入でき、サーバ全体の制御が奪取できる。Tuleap は開発・プロジェクト管理ツールとして大手企業でも採用されている。 |
| **CVE‑2026‑88807** | 8.9 | libXrender – ヒープオーバーフロー (RenderQueryPictFormats) | X11 クライアント/サーバー環境全般 (Linux, BSD) | 悪意ある X サーバからクライアントへヒープオーバーフローを仕掛け、任意コード実行が可能。X11 のデフォルト設定が多くのデスクトップ環境で有効なため、広範囲に影響。 |

> **注:** 上記 5 件は **CVSS が 8.8 以上**、かつ **リモートからのコード実行が可能** で、実装ベースが広く採用されている点で優先度が高いです。

---

## 3. 推奨アクション  

### 3‑1. Joomla / OrdaSoft Gallery 系統  
- **アップデート**: OrdaSoft Gallery 6.2.7 以上へ更新。  
- **パッケージ名**: `ordasoft-gallery` (Joomla Extension)  
- **緊急対策**:  
  - 直ちに **`/plugins/ordasoft/gallery/`** 配下の `saveWatermark.php` と `updateOSGallery.php` を無効化（プラグイン管理画面で「無効化」またはファイルリネーム）。  
  - アップロードされたファイル名を **ホワイトリスト化**（拡張子チェック）し、`move_uploaded_file()` で安全なディレクトリに保存するパッチを適用。  

### 3‑2. Netcore NBR200V2 系列（CGI Diagnostic, Upgrade, Backup 等）  
- **ファームウェア更新**: Netcore 公式サイトから **最新ファームウェア 1.3.241127.071246‑patch** 以上を適用。  
- **パッケージ名**: `netcore-nbr200v2-firmware`  
- **緊急対策**:  
  - `/www/cgi-bin/` 配下の **`network_tools`、`upgrade`、`restore.cgi`** への外部アクセスを **IP アクセス制御**（ファイアウォールで内部ネットワークのみ許可）で遮断。  
  - CGI スクリプトの **入力サニタイズ**（`escapeshellarg()` でエスケープ）をパッチで追加。  

### 3‑3. D‑Link DIR‑868L ルータ  
- **ファームウェア更新**: D‑Link 公式から **2.01b07 以降** の最新版へアップグレード。  
- **パッケージ名**: `dir-868l-firmware`  
- **緊急対策**:  
  - 管理画面への **HTTPS 強制** と **管理者パスワードの強化**（最低 12 文字、大小英数字＋記号）。  
  - `webfa_authentication.cgi` の `strcpy` を `strncpy` に置換し、長さ上限を 64 バイトに制限するパッチを適用（ベンダー提供の修正が出るまでの暫定策）。  

### 3‑4. Tuleap Enterprise Edition  
- **アップグレード**: 17.6 以上（または 17.5.1 のセキュリティパッチ）へ更新。  
- **パッケージ名**: `tuleap-ee`（RPM/Deb）  
- **緊急対策**:  
  - 該当機能（OS コマンド実行）を **Web UI から無効化**（管理コンソール → 「システム設定」→「コマンド実行」オプション OFF）。  
  - 受信パラメータを **正規表現でホワイトリスト**し、シェルメタ文字を除去する WAF ルールを追加。  

### 3‑5. libXrender (X11)  
- **

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-88857

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-20T18:16:54.443 |

Joomla Extension - OrdaSoft.com - Authenticated, Privileged Remote Code Execution in OrdaSoft Joomla Gallery extension for Joomla < 6.2.7 - The extensions saveWatermark() copied an uploaded file into a web-accessible directory using the client-supplied filename exactly as sent, with no extension check, no content check, and no filename sanitisation of any kind. An authenticated core.manage user could upload a .php file disguised with an image Content-Type header and execute it directly by requesting the resulting path.

### CVE-2026-88856

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-20T18:16:54.280 |

Joomla Extension - OrdaSoft.com - Authenticated, Privileged Remote Code Execution in OrdaSoft Joomla Gallery extension for Joomla < 6.2.7 - The extensions updateOSGallery(), reached via task=update_osgallery, read a JSON request body and called the value of a method field as a live PHP function, passing the value of a package field as its single argument, with no allow-list or is_callable() check of any kind. Any function name compatible with a single argument was directly reachable, including system, exec, shell_exec, and passthru.

### CVE-2026-94097

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-21T00:16:59.793 |

A vulnerability was determined in Netcore NBR200V2 1.3.241127.071246. This affects an unknown part of the file /www/cgi-bin/network_tools of the component CGI Diagnostic Endpoint. This manipulation of the argument param/key/val causes command injection. Remote exploitation of the attack is possible. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94089

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-20T21:16:55.780 |

A vulnerability was determined in D-Link DIR-868L 2.01b05. This issue affects the function strcpy of the file /webfa_authentication.cgi of the component Authentication Handler. Executing a manipulation of the argument id/password can lead to stack-based buffer overflow. The attack can be executed remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-88854

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-20T18:16:53.987 |

Joomla Extension - OrdaSoft.com - Unauthenticated SQL Injection in OrdaSoft Joomla Gallery extension for Joomla < 6.2.7 - The extensions showSearchResult() and showSearchResultAjax() read the textsearch/searchText request parameter with $input->getVar(), which is not a real Joomla filter method and falls through to a filter that strips HTML tags but does not touch quotes or SQL syntax. The value is concatenated directly into a LIKE clause with no escaping. The endpoint requires no login of any kind: mod_osgallery_search is a public, commonly-published search box. Any anonymous site visitor can inject a UNION SELECT and read arbitrary database content.

### CVE-2025-12999

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-21T09:17:04.533 |

UrlUtil.getBaseUrl builds the absolute URLs in a response — download links, icons, asset and API URLs — from the X-Forwarded-Host, X-Forwarded-Proto and X-Forwarded-Prefix request headers, with no check on whether the sender was a trusted proxy, falling back to the client-supplied Host header.                                                                                   

                                                                                                                                                                                              


Those responses are cached under keys that do not include the host (extension.json since 0.6.0, namespace.details.json since 0.9.0, sitemap since 0.14.5, latest.extension.version.vscode since 0.34.2). A single request carrying a forged header therefore places attacker-chosen URLs into an entry served to every other client for the lifetime of that entry — one hour by default, and cluster-wide where ovsx.redis.enabled is set.



The VSIX download URL, its signature URL and the public key URL are all derived from the same base URL, so extension signing does not limit the impact: an attacker who poisons an entry supplies the package, the signature over it, and the key used to verify it.                                                                                    



Exploitability depends on deployment topology. A server reachable directly by clients, or fronted by a proxy that relays the client's X-Forwarded-Host rather than overwriting it, is exploitable by an unauthenticated remote attacker. A proxy that overwrites the header is not.



An unauthenticated attacker can poison Open VSX's per-extension metadata cache with attacker-controlled download, signature, and public-key URLs by supplying a crafted X-Forwarded-Host header, causing downstream VS Code-compatible editors to fetch and install a malicious VSIX.



Workarounds (unpatched versions)

  


1. Configure the reverse proxy to set rather than relay X-Forwarded-Host, X-Forwarded-Proto and X-Forwarded-Prefix — note that nginx's $host is the client's Host header and is not a safe value.



2. Ensure the server is not reachable except through that proxy.



3. Flush the caches afterwards; poisoned entries survive the configuration change.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-88807

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-21T14:17:22.410 |

A heap overflow in libXrender before 0.9.13 in RenderQueryPictFormats could be used by malicious X servers to inject code into attached X clients.

### CVE-2026-84285

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-21T13:17:10.830 |

An OS Command Injection vulnerability affecting Tuleap Enterprise Edition from 17.3 through 17.5 could allow an attacker to execute arbitrary commands on the server.

### CVE-2026-92574

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-09-21T10:17:17.360 |

A vulnerability in CRI-O checkpoint restore allows a user who can create a pod from a malicious checkpointed container to bypass the destination Kubernetes security context. The restored process may retain credentials, Linux capabilities, no_new_privs, and seccomp state from the checkpoint instead of enforcing the destination configuration. This can allow execution with elevated privileges across the container security boundary.
Affected upstream supported versions are CRI-O 1.34 and later. Downstream Red Hat products are affected from OCP 4.17 onward. Fixes have been applied to supported branches but are not yet released.
Exploitation requires permission to create a pod from a malicious checkpoint image and checkpoint restore functionality to be available.

### CVE-2026-94381

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-21T13:17:13.360 |

MISP has a security issue that can let a user gain more access than their API key is supposed to allow.

A read-only API key should only let someone view information. However, after logging in with such a key, a specific MISP function could accidentally restore the user’s normal account permissions. This means someone with a read-only API key could potentially gain write, delete, or even administrator access if their underlying account has those permissions.

Exploiting the issue requires a valid read-only API key and a single request to the affected function.

The main impact is that MISP’s API key restrictions can be bypassed, allowing actions that the API key was specifically meant to prevent.




Version affected: <2.5.47

### CVE-2026-89139

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-749;CWE-1188` |
| Published | 2026-09-21T12:17:24.440 |

Temporal Server compiles a Worker Controller Instance module into its Worker Service, and that module registers a compute provider named subprocess whose function is to launch a worker by running a command on the machine hosting the Worker Service. The program name and the argument vector that provider executes are taken from the compute provider configuration supplied in the caller's request rather than from operator configuration. An authenticated caller holding only a write role in a single namespace can therefore configure a worker deployment version so that the Worker Service executes a command of the caller's choosing on its own host, under the account the server process runs as. Execution is immediate rather than deferred: the configuration handler invokes every provider using the invoke strategy directly after validating the submitted specification, so no scaling decision, task arrival, or unusual request sequence is required. Because the Worker Service process holds the persistence credentials for every namespace in the cluster and the cluster's TLS material, the consequence reaches beyond the caller's namespace to the cluster as a whole. The provider is present in the official temporal-server binaries and container images for the affected releases. The only control that can keep it unreachable is the compute provider allowlist, the per-namespace dynamic configuration setting workercontroller.compute_providers.enabled, and that control does not deny by default: its default value is an unset list, and the allowlist check is skipped entirely when the value is unset, so every registered compute provider is permitted, this one included. To determine whether a deployment is affected, check the following together. The deployed Temporal Server version is 1.31.0 or later and earlier than 1.31.3. The Worker Service is running, which it is in the default service set and therefore in a stock deployment. The effective per-namespace value of workercontroller.compute_providers.enabled is either unset or contains subprocess. And authorization is configured, meaning a real authorizer and claim mapper are in place; a deployment running with no authorizer already grants every caller unrestricted access to every namespace, so it has no namespace boundary for this to cross. Note that the separate per-namespace dynamic configuration setting workercontroller.enabled does not gate the affected path. It defaults to false, and a deployment that has never set it in any namespace is still affected, which was confirmed by running an affected release with no value for that setting present anywhere in dynamic configuration. To look for a compute configuration that is already attached, call DescribeWorkerDeploymentVersion for each worker deployment version in each namespace and check whether any scaling group's compute provider type is subprocess.

### CVE-2026-65654

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-21T12:17:16.133 |

github.com/temporalio/ringpop-go enforces configured LabelOptions limits when an application changes the local node's labels, but affected versions do not apply those limits to label maps received in SWIM membership changes. A network peer that can reach a live Ringpop TChannel listener can repeatedly submit changes for distinct member addresses containing label keys, values, or counts that exceed the receiver's configured limits. Accepted labels are retained in the member list and disseminated to peers, allowing memory and gossip-bandwidth consumption to exceed configured bounds and potentially making the hosting process unavailable. The fix validates peer-supplied label maps before they are retained or disseminated. Availability only; no confidentiality or integrity impact was identified.

### CVE-2026-65653

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-09-21T12:17:15.973 |

github.com/temporalio/tchannel-go did not reject TChannel call fragments containing checksum metadata but no length-prefixed argument chunks. The fragment reader left its chunk slice empty and then unconditionally selected the first element. A network peer can supply such a malformed call fragment, including as a direct initial call request after completing the standard initialization handshake. On that inbound path, the resulting unrecovered Go slice-bounds panic occurs on a library-created dispatch goroutine and terminates the hosting process. This allows remote denial of service against applications that expose the listener to untrusted peers. The impact is limited to availability; no confidentiality or integrity impact was identified.

### CVE-2026-65652

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-09-21T12:17:15.800 |

github.com/temporalio/tchannel-go did not validate the one-byte checksum-type field in inbound TChannel call frames. A network peer that can reach a listener can complete the standard initialization handshake and send a call request with an unsupported checksum type. The parser uses that value as an index into a four-entry checksum pool, causing an unrecovered Go panic on the connection read goroutine and terminating the hosting process. This allows remote denial of service against applications that expose the listener to untrusted peers. The impact is limited to availability; no confidentiality or integrity impact was identified.

### CVE-2026-65651

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-21T12:17:15.553 |

temporalio/sqlparser accepts SQL containing deeply nested unary expressions and can return a correspondingly deep abstract syntax tree without enforcing an applicable nesting limit. The library's String and Walk operations recursively traverse that tree. An application that parses attacker-controlled SQL and later formats or walks the returned tree can encounter a runtime-fatal Go stack overflow that terminates the process; Go panic recovery cannot contain this condition. Temporal Server passes caller-controlled query input through the affected parser in archival, visibility, and worker-query paths. In affected validation paths, the Server recursively formats an invalid expression while constructing an error. In a supported authenticated deployment, a caller with namespace read permission can terminate the receiving Frontend or Matching process. The dynamically confirmed ListWorkers route additionally requires at least one retained worker heartbeat. Repeated requests can sustain a denial of service. The issue affects availability only; no confidentiality or integrity impact was identified.

### CVE-2026-16651

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-09-21T12:17:10.167 |

temporalio/sqlparser can panic when Parse, ParseStrictDDL, or ParseNext processes a MySQL version comment whose contents are empty or consist only of one to five decimal digits. ExtractMysqlComment does not check the -1 result returned by strings.IndexFunc before using it as a slice boundary. The resulting Go runtime panic propagates unless the caller recovers it on the parsing goroutine, so applications that parse attacker-controlled SQL can terminate. Temporal Server exposes the affected parser through ListWorkers. When that API is enabled, an authenticated caller with namespace read permission can submit a malformed query that terminates the receiving Matching process. Repeated requests can sustain a denial of service. The issue affects availability only; no confidentiality or integrity impact was identified.

### CVE-2025-71421

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-21T14:17:14.897 |

UVdesk core-framework before 1.1.7 contains an improper privilege management vulnerability in the editAgent endpoint that allows agents with agent-management privilege to escalate their own role to administrator. Attackers can submit their own account identifier with a role parameter set to ROLE_ADMIN to gain full administrative control over agents, tickets, and mail configuration.

### CVE-2026-94383

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-434` |
| Published | 2026-09-21T13:17:13.560 |

The MISP blocklist workflow module accepted a user-supplied blocklist filename parameter without validating the file extension. The only sanitization applied was basename() to strip path components and a check for empty or dot values. A site administrator could specify a filename with an arbitrary extension that would be placed in the MISP export directory. If the underlying web server is configured to interpret and execute scripts from that directory, the resulting file could be invoked, leading to arbitrary code execution in the context of the web server process.

The vulnerability requires the attacker to hold site-administrator privileges within MISP, as the blocklist workflow module is restricted to that role. No additional user interaction is required beyond triggering the workflow action with a crafted filename parameter. The impact is full compromise of the MISP server's confidentiality, integrity, and availability, as arbitrary script execution grants the attacker the same privileges as the web server user.

Version affected: <2.5.47

### CVE-2026-94101

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-21T02:16:53.317 |

A security vulnerability has been detected in Netcore NBR200V2 1.3.241127.071246. The affected element is the function vlan_load_form_uci of the file /usr/bin/routerd. The manipulation of the argument wan_num leads to buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94100

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-21T01:16:30.170 |

A weakness has been identified in Netcore NBR200V2 1.3.241127.071246. Impacted is the function wan_config_set_vlan of the file /usr/bin/routerd of the component WAN VLAN Reconfiguration. Executing a manipulation of the argument vlan_wanX.ports can lead to buffer overflow. The attack may be performed from remote. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94099

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-21T01:16:29.983 |

A security flaw has been discovered in Netcore NBR200V2 1.3.241127.071246. This issue affects some unknown processing of the file restore.cgi of the component Backup Restore. Performing a manipulation of the argument QUERY_STRING results in command injection. The attack is possible to be carried out remotely. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94096

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-21T00:16:59.617 |

A vulnerability was found in Netcore NBR200V2 1.3.241127.071246. Affected by this issue is some unknown functionality of the file /usr/bin/network_tools of the component LAN IP Configuration Handler. The manipulation of the argument ipv4 results in command injection. The attack may be launched remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94095

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-21T00:16:59.440 |

A vulnerability has been found in Netcore NBR200V2 1.3.241127.071246. Affected by this vulnerability is an unknown functionality of the file /usr/bin/network_tools of the component Traceroute Diagnostic Feature. The manipulation of the argument url leads to command injection. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-88855

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-20T18:16:54.137 |

Joomla Extension - OrdaSoft.com - Authenticated, Privileged SQL Injection in OrdaSoft Joomla Gallery extension for Joomla < 6.2.7 - The extensions saveGallery() passes form data through a hand-rolled parser into Joomla’s Input object, then reads it back with the ARRAY/ STRING filter types, neither of which sanitises SQL content. Values from category_names[], catOrderIds, and image-ordering fields were concatenated directly into SQL with no quoting or integer cast, giving an authenticated core.manage user (a permission scoped to managing one gallery component, not administrator-wide trust) full read/write access to the database, including UNION-based extraction of #__users password hashes.

### CVE-2026-94146

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-123` |
| Published | 2026-09-21T07:16:53.993 |

A vulnerability was found in BioStar BIOS Update Utility 1.9.7.3. This issue affects the function sub_110BC of the file BSMEM64_W10.sys of the component IOCTL Handler. The manipulation of the argument PhysicalAddress/Size results in write-what-where condition. Attacking locally is a requirement. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94142

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-123` |
| Published | 2026-09-21T05:16:42.053 |

A security vulnerability has been detected in BioStar Temperature Monitor Utility 1.2.1806.2200. Affected by this vulnerability is the function sub_1105C of the file BS_HWMIO64_W10.sys of the component IOCTL Handler. Such manipulation of the argument PhysicalAddress leads to write-what-where condition. The attack needs to be performed locally. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94129

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-123` |
| Published | 2026-09-21T02:16:54.213 |

A vulnerability was detected in BioStar VALKYRIE AURORA 2.10.2411.0800. This vulnerability affects the function sub_1105C of the file BS_RVSIO64.sys of the component IOCTL Handler. The manipulation of the argument PhysicalAddress results in write-what-where condition. The attack needs to be approached locally. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94128

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-123` |
| Published | 2026-09-21T02:16:54.037 |

A security vulnerability has been detected in BioStar VIVID LED DJ 4.0.2411.1500. This affects the function sub_1105C of the file BS_LED64.sys of the component IOCTL Handler. The manipulation of the argument AssociatedIrp leads to write-what-where condition. Local access is required to approach this attack. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94098

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-21T01:16:29.800 |

A vulnerability was identified in Netcore NBR200V2 1.3.241127.071246. This vulnerability affects unknown code of the file /www/cgi-bin/upgrade of the component Firmware Upgrade CGI Endpoint. Such manipulation of the argument QUERY_STRING leads to command injection. The attack can be executed remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-94401

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73;CWE-918` |
| Published | 2026-09-21T14:17:30.957 |

MISP has a file-handling vulnerability that could let certain authenticated users make the server read files or access internal network services.

When importing an XML file, MISP did not properly verify that the uploaded content was actually XML. Because of this, a user with permission to modify data could upload a file containing a local file path or a web address instead.

If a local file path was supplied, MISP could read that file from the server. If a URL was supplied, MISP could make a request to that address, including systems that may only be reachable from inside the organization’s network.

The vulnerability could therefore expose sensitive local files and allow unauthorized requests to internal services.

Exploitation required a valid MISP account with modify permissions, but no additional user interaction was needed.

Version affected: <2.5.47

### CVE-2026-94374

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-472;CWE-639` |
| Published | 2026-09-21T13:17:12.953 |

MISP contains an insecure direct object reference vulnerability in the processModuleResultsData method of the Event model. When processing module results, the code iterates over EventReport entries supplied in the resolved data and saves each one. Unlike the adjacent attribute and object processing loops, the report loop did not unset the client-supplied 'id' field before calling save(). Because the MISP EventReport model's create() method does not strip the id field, an authenticated user with permission to submit module results could include an 'id' value referencing an existing report belonging to a different event. Upon save(), the ORM would update that existing row rather than insert a new one, allowing the attacker to 

 - read the content of another event's report by reparenting it into their own event
 - overwrite the report's fields with attacker-controlled data
 - change the report's event_id to redirect ownership. 




This constitutes an authorization bypass through a user-controlled key, enabling cross-event data disclosure and integrity compromise. The vulnerability requires an authenticated session with the ability to invoke module result processing on an event.

Version affected: <2.5.47

### CVE-2026-15801

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-21T09:17:05.743 |

A vulnerability was found in CRI-O related to the container checkpoint and restore feature. When CRI-O is configured to restore containers from checkpoint archives, insufficient validation of restore metadata may allow a user with sufficient privileges to perform unintended operations on the host filesystem. Successful exploitation requires that container checkpoint and restore functionality is enabled, which is not the default configuration. An attacker must also be able to trigger restoration of a container from untrusted checkpoint content.

### CVE-2026-88806

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-21T14:17:22.273 |

A malicious X server could exploit a buffer overflow in libX11 before 1.8.14 during handling of XkbGetMap overflowing the key_sym_map.

### CVE-2026-91866

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-21T12:17:25.000 |

A specially crafted pair of WS-Policy documents can force Neethi's policy-intersection to do exponential amounts of work, pinning the CPU for a long time (denial of service).
Users are recommended to upgrade to version 3.2.4, which fixes this issue.

### CVE-2026-91865

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-21T12:17:24.903 |

A small WS-Policy document using repeated policy references can force Neethi to re-expand the same references exponentially during normalization, consuming huge amounts of CPU and memory (denial of service).
Users are recommended to upgrade to version 3.2.4, which fixes this issue.

### CVE-2026-91864

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-21T12:17:24.807 |

A specially crafted WS-Policy document can pack unlimited content inside a policy assertion, which Neethi copies into memory without counting it against its size limits, exhausting the heap (denial of service).
Users are recommended to upgrade to version 3.2.4, which fixes this issue.

### CVE-2026-91863

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-21T12:17:24.697 |

A specially crafted WS-Policy document with deeply nested policy elements can bypass Neethi's nesting-depth limit and exhaust the thread stack, crashing the parser (denial of service).
Users are recommended to upgrade to version 3.2.4, which fixes this issue.

### CVE-2026-47321

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409;CWE-789` |
| Published | 2026-09-21T08:16:37.520 |

The CompressionFilter class uses ZLib to deflate and inflate data sent and received. When we inflate incoming data, the filter does not control the resulting size, and create a buffer no matter what.

Some compressed data may have a compression ration greater than 1 thousand, leading to an exhaustion of the application memory, as we don't control the deflated size.




The fix adds such a control by allowing the application developer to provide a fixed size limit, which when reached throws an exception. It also allows the user to provide a compression ratio that should not be exceeded, protected the application from small inflated files that inflate in gigantic files, but with a grace limit for the resulting size (1Mb) to avoid false positive (like a very small file inflating with a high ratio, but resulting with a acceptable size, like a few thousands bytes)




For application using this feature, it is highly recommended to create the CompressionFilter and to pass the maximum limit as a forth constructor parameter, maxDecompressedSize:




public CompressionFilter(final boolean compressInbound, final boolean compressOutbound, final int compressionLevel, final int maxDecompressedSize)Optionally one can also provide a maxDecompressRatio fifth parameter, and a decompressRatioMinSize sixth parameter to allow small inflated files with a high compression ratio to still be accepted.




Here are the additional constructor:






public CompressionFilter(final boolean compressInbound, final boolean compressOutbound,



            final int compressionLevel, final int maxDecompressedSize,



            final long maxDecompressRatio, final long decompressRatioMinSize)








Also note that a fluent API has been added to spare the users the pain to call a constructor with that many parameters:






 CompressionFilter compressionFilter = new CompressionFilter()

                                                .setCompressionLevel(Zlib.COMPRESSION_MAX)

                                                .setMaxDecompressedSize(1_000_000)

                                                .setMaxDecompressRatio(100).

                                                .setDecompressRatioMinSize(100_000); 









Applications using Apache MINA are advised to upgrade and configure their CompressionFilter instance.

### CVE-2026-94036

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-09-20T16:16:55.490 |

A security flaw has been discovered in D-Link DIR-X1860 and DIR-X1860Z up to 1.0.2.220120.165402. The impacted element is an unknown function of the file /ubus of the component routerd. The manipulation of the argument passwd_set results in improper access controls. The attack must originate from the local network. The exploit has been released to the public and may be used for attacks.

### CVE-2026-87858

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-09-21T12:17:22.230 |

Temporal Server decided whether a Workflow completion callback was internal by reading a caller-supplied HTTP header. An authenticated caller holding only write permission in a single namespace could attach a completion callback whose URL host matched the configured callback address allowlist, whose URL path was any Temporal HTTP API route, and whose header map contained a non-empty header named source. When the History service delivered that callback, the non-empty source header caused it to re-target the request at the local frontend client and rewrite only the scheme and host, preserving the caller's path, query, and request body. Where an internal frontend is deployed with its HTTP API enabled, that client resolves to the internal frontend, which authorizes every request as a system administrator without requiring authentication information. The result is that the server performs an attacker-chosen state-changing HTTP POST against its own administrative API on the caller's behalf, in namespaces where the caller has no permission. The caller never needs network access to the internal frontend, because the History service makes the request. Confirmed effects include terminating Workflows in other namespaces, registering namespaces, modifying another namespace's configuration, and deleting another namespace and its Workflows. The affected routing logic is present in both the HSM and CHASM callback delivery implementations. This description and the CVSS score in this record describe releases 1.30.0 and later, where any non-empty source header is sufficient. Releases 1.25.0 through 1.29.7 are affected by a narrower form of the same defect in which the header must exactly match a configured cluster ID, a UUID that a namespace-scoped caller cannot read through the API. The consequence once that match occurs is the same, but the attack is materially harder and scores lower. To determine whether a deployment is affected, check two settings together: the static Server configuration for a non-zero services.internal-frontend.rpc.httpPort, and the effective per-namespace dynamic configuration value of component.callbacks.allowedAddresses. A deployment is exposed only when an internal frontend is deployed with a non-zero HTTP port, at least one allowlist rule admits a host, and authorization is enabled. The allowlist is empty by default, which denies all external callback URLs, and the stock static topology does not include an internal frontend. Note that a failed attach returns the error 'invalid url: url does not match any configured callback address', which proves only that one tested URL did not match and does not prove the effective allowlist is empty. To look for callbacks already attached, use DescribeWorkflowExecution, which returns callback information for a Workflow's registered completion callbacks. Operators should be aware of a gap when searching for evidence of delivery: the frontend HTTP API server records the request method and URL at debug level only, so at default log levels a delivered request is not written to the internal frontend's logs, and the absence of such log entries is not evidence that the issue was not exploited.

### CVE-2026-94404

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-21T14:17:31.203 |

MISP has a security issue that could let an attacker change threat-intelligence data through a logged-in user’s browser without that user knowingly approving the change.

The affected function did not properly enforce MISP’s usual protection against forged requests. Because of this, an attacker could create a malicious webpage that silently sends a request to MISP when visited by an authenticated user.

If successful, the attacker could change details of an attribute, such as its value, type, category, comment, distribution settings, or related timestamps.

The attack requires the victim to already be logged in to MISP and to visit an attacker-controlled page.

The main impact is unauthorized modification of threat-intelligence data, which could lead to incorrect indicators, wrong classifications, or altered sharing settings and reduce confidence in the accuracy of the information stored in MISP.

Version affected: <2.5.47

### CVE-2026-94368

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-21T12:17:29.010 |

A flaw was found in the signature verification logic of noobaa-core, the core component of the NooBaa Multicloud Object Gateway. The issue occurs when the service processes S3 presigned URLs using Signature Version 4 (SigV4). Due to improper validation, the service fails to reject requests containing unsigned x-amz- headers, instead simply dropping them from the signature calculation. This allows an attacker who possesses a valid presigned PUT URL to add an unsigned x-amz-copy-source header, effectively converting a simple upload into a CopyObject operation. This can lead to unauthorized access and copying of any data the original signer is permitted to reach across the entire storage system.

### CVE-2026-16652

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-606` |
| Published | 2026-09-21T12:17:10.400 |

Temporal Server did not bound the work performed while searching for a Schedule's next action time. An authenticated caller with namespace write permission could create or update a Schedule that combines a fine-grained cadence with an exclusion calendar that rejects every candidate time, causing the server to evaluate excluded candidates without a per-search work budget. This can consume excessive CPU in Frontend and Schedule worker components. A persisted specification can also cause its backing Schedule Workflow to repeatedly fail and retry, allowing CPU consumption to continue without additional requests until the Schedule is deleted or its backing Workflow is terminated. Repeated or parallel exploitation can deny service. The issue affects availability only; it does not expose or modify Workflow data.

### CVE-2026-90860

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-212` |
| Published | 2026-09-21T07:16:53.463 |

The Canva Mobile App for HarmonyOS before v1.15.1 did not restrict the headers returned to an external origin running in a privileged WebView. A threat actor with control of the WebView could access a user’s session.
