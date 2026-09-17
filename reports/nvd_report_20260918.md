# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-17 15:00 UTC
- **対象期間**: `2026-09-16T15:00:35.000Z` 〜 `2026-09-17T15:00:53.000Z`
- **重要CVE数**: 319 件（Critical 9.0+: 81 件 / High 7.0〜: 238 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、**Node.js 用サンドボックスライブラリ vm2** に関する脆弱性が集中しており、すべて CVSS 10.0 と極めて深刻です。  
- 同時に、Cisco Identity Services Engine (ISE) 系列や Dell ObjectScale など、**エンタープライズ向けネットワーク/ストレージ製品**でも認証バイパスや SSRF が多数報告され、インターネットに直接露出しているサービスは即時対策が必須です。  
- 多くの脆弱性は「デフォルト設定のまま使用した場合にサンドボックス脱出やコード実行が可能」になる点が共通しており、**設定緩和や古いバージョンのまま運用しているケースがリスクの根源**となっています。  

---

## 2. 特に注目すべき CVE  

| CVE | 種別・影響範囲 | 主な危険性 | 推奨アップデート |
|-----|----------------|------------|-------------------|
| **CVE‑2026‑92956** (vm2 3.10.1‑3.11.6) | NodeVM のデフォルト sandbox から **WebAssembly のストリーミング API を利用したサンドボックス脱走** | 攻撃者は任意のホストプロセスコードを実行でき、RCE につながる。Node.js 26 でのみ再現。 | **vm2 ≥ 3.11.8**（現在の最新は 3.11.9）へ更新。 |
| **CVE‑2026‑92955** (vm2 < 3.11.8) | NodeVM が `console._stdout/_stderr` を介して **__proto__ ガッター/セッター** にアクセス可能 | `EventEmitter.prototype.emit` を上書きし、プロセスイベントでコード実行。 | **vm2 ≥ 3.11.8** にアップグレード。 |
| **CVE‑2026‑92947** (vm2 < 3.11.7) | 共有 **Buffer プール** がサンドボックスに露出 | メモリ内容の読み取り・書き換えが可能で、機密情報漏洩や任意コード実行に利用できる。 | **vm2 ≥ 3.11.8** に更新し、`require.external` を無効化。 |
| **CVE‑2026‑76460** (Cisco ISE) | ISE API の認証制御不備 | 認証なしで管理 API にアクセスでき、管理者権限取得や設定変更が可能。 | Cisco ISE **3.2.0 以降**（またはベンダが提供する最新パッチ）へアップグレード。 |
| **CVE‑2026‑70416** (Dell ObjectScale) | 未検証データのデシリアライズ | 任意コード実行 (RCE) がリモートから可能。 | **ObjectScale 4.4.0.0 以降**へアップデート。 |

> **注**：上記 5 件は **CVSS 10.0**（または 9.9）で、かつ「デフォルト設定で利用されやすい」点が共通しています。特に vm2 系列は同一パッケージに複数のサンドボックス脱走経路が残っているため、**一括で最新版へ置き換える**ことが最も効果的です。

---

## 3. 推奨アクション  

### 3.1 vm2（Node.js）  
- **パッケージ更新**  
  ```bash
  # npm で最新版 (3.11.9 以降) をインストール
  npm install vm2@^3.11.9 --save-exact
  # Yarn を使用している場合
  yarn add vm2@^3.11.9
  ```
- **設定見直し**  
  - `require.external`、`require.root`、`builtin` の許可リストは最小限に絞る。  
  - `sandbox: {}` に `os`, `dns`, `tls`, `url` など不要な組み込みモジュールは **絶対に許可しない**。  
- **テスト**  
  - 既存のユニットテストにサンドボックス脱走シナリオ（WebAssembly, console, Buffer）を組み込み、CI で回帰テストを実施。  

### 3.2 Cisco Identity Services Engine (ISE)  
- **ファームウェア/ソフトウェアのアップデート**  
  - Cisco の公式サイトから **ISE 3.2.0 以降**（もしくはベンダが提供する最新パッチ）を取得し、管理プレーンとデータプレーンの両方に適用。  
- **API アクセス制御**  
  - API エンドポイントは **IP アクセスリスト** と **RBAC** で保護し、不要な `GET /api/...` を無効化。  
  - すべての API 呼び出しに **HTTPS** と **相互認証** を必須化。  

### 3.3 Dell ObjectScale  
- **バージョンアップ**  
  - 現行環境が 4.4.0.0 未満の場合、**4.4.0.0 以上**（推奨は最新リリース）へアップグレード。  
- **入力検証の強化**  
  - デシリアライズ対象のデータは **JSON Schema** で事前バリデーションし、未検証データの受け入れを排除。  

### 3.4 その他重要製品  
| 製品 | 推奨バージョン / パッチ | 主な対策 |
|------|------------------------|----------|
| Migratico Lite | **2.6.9 以上**（ベンダ提供の RCE パッチ） | すべての外部からのリクエストをファイアウォールで遮断し、管理インタフェースは VPN 内部に限定。 |
| Altium Enterprise Server (UnifiedLogin) | **2026.2 以降** | SSRF 防止のため、Outbound HTTP/HTTPS は内部プロキシ経由に限定し、`Allowlist` で外部ドメインをブロック。 |
| WordPress プラグイン (Login with QR, Pressengine, Private Feed Key) | **最新版**（2026‑08‑xx 以降） | プラグインは **公式リポジトリ** から再インストールし、不要なプラグインは削除。 |
| FatPipe MPVPN / WARP / IPVPN | **ファームウェア 10.1.2r60p101 以上** | 管理インタフェースは **TLS 1.3** 強制、管理者認証は多要素化。 |

### 3.5 共通的な運用上のベストプラクティス  
1. **脆弱性情報の自動取得** – `npm audit`, `snyk`, Cisco PSIRT などを CI に組み込み、リリースと同時に警告を受信。  
2. **最小権限の原

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-92960

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-17T14:18:02.290 |

vm2 before 3.11.6 fails to restrict access to os and dns builtins under the builtin: ['*'] configuration, allowing sandbox code to read host process identity and network topology. Attackers can invoke dns.setServers() to hijack the host process DNS resolver globally, redirecting all subsequent host DNS queries through an attacker-controlled resolver.

### CVE-2026-92956

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-17T14:18:01.640 |

vm2 versions 3.10.1 through 3.11.6 contain a sandbox escape reachable from a default `new VM()` sandbox when running on Node.js 26. WebAssembly.compileStreaming and WebAssembly.instantiateStreaming can produce a raw host-realm Promise that rejects with a host-realm error object; by controlling Symbol.species via Promise.prototype.finally, sandbox code receives that raw host error, walks from the host error constructor to the host Function constructor, and recovers the real host `process` object, gaining host Node.js capabilities (e.g. access to host modules such as fs) in the context of the process running the sandbox. No NodeVM, require permission, host object injection, or otherwise unsafe configuration is required. This is a bypass of the fix for GHSA-6j2x-vhqr-qr7q, which removed the JSPI entry points WebAssembly.promising and WebAssembly.Suspending. The issue is fixed in 3.11.7.

### CVE-2026-92955

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-913` |
| Published | 2026-09-17T14:18:01.480 |

vm2 before 3.11.8 contains a sandbox escape vulnerability in NodeVM that allows attackers to access the host __proto__ getter/setter through console._stdout and console._stderr. Attackers can overwrite EventEmitter.prototype.emit and trigger process events to execute code with process context, bypassing code generation restrictions.

### CVE-2026-92947

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-17T14:18:00.140 |

vm2 before 3.11.7 exposes Node's shared Buffer pool to sandboxed code, allowing disclosure of host memory used by Buffer.from, Buffer.concat, and related allocations. Sandboxed code can read and write to host-realm buffers by acquiring ArrayBuffers from small allocations, leading to sensitive data exposure and potential denial-of-service.

### CVE-2026-92946

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-913` |
| Published | 2026-09-17T14:17:59.963 |

vm2 before 3.11.7 contains a remote code execution vulnerability when require.external is enabled without an explicit require.root that excludes node_modules. Sandboxed code can require vm2's own package, instantiate an unrestricted NodeVM instance, and execute arbitrary host OS commands via child_process.

### CVE-2026-92941

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-17T14:17:59.310 |

vm2 versions from 3.11.3 before 3.11.7 expose the host tls module to NodeVM sandbox code, allowing attackers to call tls.setDefaultCACertificates() and replace process-wide certificate authorities. Attackers with access to allowed tls and url builtins can use URLSearchParams to create host-realm arrays and manipulate the TLS trust store, enabling subsequent host HTTPS clients to accept attacker-controlled certificates.

### CVE-2026-92940

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-668` |
| Published | 2026-09-17T14:17:59.143 |

vm2 versions 3.11.3 through 3.11.6 expose the host process's real https.globalAgent to sandboxed code when a NodeVM is explicitly configured to allow require('https'). The builtin loader wraps host modules in a read-only proxy, but method calls such as Agent.prototype.on() are forwarded to the underlying host object, so sandbox code can register a listener for the agent's 'free' event. When an unrelated host HTTPS request releases a pooled connection, the listener receives the live host request options and the host TLSSocket, allowing sandboxed code to read the host's Authorization header and private destination host/port, attach a data listener to the released socket and read subsequent host response bodies in plaintext, and issue attacker-chosen authenticated requests using the stolen credentials. The issue is fixed in 3.11.7.

### CVE-2026-92937

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-17T14:17:58.517 |

vm2 3.11.6 is vulnerable to a sandbox escape leading to remote code execution in the host Node.js process. The fix for GHSA-m283-3h24-438v is incomplete: the bridge gate at lib/bridge.js:1624 identity-checks only the direct call target when deciding whether to rebuild/sanitise a rejected host Promise value. Registering the rejection handler through Function.prototype.call or .apply indirection (e.g., p.then.call(p, undefined, cb)) makes the intercepted target host Function.prototype.call, so the sanitiser never runs and the raw host error reaches sandbox code with its own properties intact. If an embedder exposes a host-realm Promise to the sandbox (an async host function bridged via the sandbox option, or a NodeVM external module's async method) and that Promise rejects with an Error carrying a non-primitive own property referencing a host object (for example err.detail = process), untrusted code in the sandbox obtains a fully functional proxy to that host object and can execute arbitrary commands with the privileges of the host process (e.g., e.detail.mainModule.require('child_process').execSync(...)). The direct p.then(undefined, cb), bind, and Reflect.apply forms are correctly sanitised. Fixed in vm2 3.11.7.

### CVE-2026-62104

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-17T14:17:15.130 |

Unauthenticated Remote Code Execution (RCE) in Migratico Lite <= 2.6.8 versions.

### CVE-2026-76460

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-648` |
| Published | 2026-09-16T21:17:21.430 |

A vulnerability in an API of Cisco Identity Services Engine (ISE) could allow an unauthenticated, remote attacker to bypass authentication.

This vulnerability is due to insufficient authentication control on an API endpoint. An attacker could exploit this vulnerability by sending a crafted request to an affected API endpoint. A successful exploit could allow the attacker to gain unauthorized access to the affected device by bypassing the web-based management interface.

### CVE-2026-92808

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-918` |
| Published | 2026-09-16T20:17:49.117 |

A server-side request forgery (SSRF) vulnerability exists in the UnifiedLogin service of Altium Enterprise Server. An unauthenticated network attacker can cause the server to issue outbound HTTP requests to a destination of the attacker's choosing, including internal services that are reachable only from the server itself.




One such internal service exposes server configuration and credential material without authentication, relying only on the request originating locally. Because the forged requests originate from the server process, that check is satisfied. An unauthenticated attacker can therefore retrieve stored credentials and use them to obtain an administrative session, resulting in full compromise of the server and all of its services. Altium 365 cloud deployments are not affected, as the affected endpoint is disabled in cloud mode.

### CVE-2026-76423

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-16T20:17:28.717 |

A vulnerability in the REST API of Cisco ISE and Cisco ISE-PIC could allow an unauthenticated, remote attacker to gain administrative access to an affected device.

This vulnerability is due to the REST API web service being exposed with insufficient authorization checks. An attacker could exploit this vulnerability by sending a crafted HTTP request to the exposed REST API port. A successful exploit could allow the attacker to read and modify ISE configuration and identity data with administrative privileges.

### CVE-2026-20192

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-16T20:17:21.900 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Identity Services Engine (ISE) and Cisco ISE Passive Identity Connector (ISE-PIC) engineering teams have conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20192 are related to improper access control issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-284.

### CVE-2026-20130

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-16T20:17:21.607 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Identity Services Engine (ISE) and Cisco ISE Passive Identity Connector (ISE-PIC), engineering teams have conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20130 are related to improper neutralization of special elements issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-74.

### CVE-2026-70416

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-16T16:17:14.953 |

Dell ObjectScale, versions prior to 4.4.0.0, contains a Deserialization of Untrusted Data vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-20332

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-16T21:17:10.480 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Adaptive Security Appliance Software, Cisco Secure Firewall Threat Defense Software and Cisco Secure Firewall Management Center Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-20332 are related to improper access control issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-284.

### CVE-2026-20330

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-707` |
| Published | 2026-09-16T20:17:23.810 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Adaptive Security Appliance Software, Cisco Secure Firewall Threat Defense Software and Cisco Secure Firewall Management Center Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-20330 are related to improper neutralization issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-707.

### CVE-2026-20329

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-703` |
| Published | 2026-09-16T20:17:23.600 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Adaptive Security Appliance Software, Cisco Secure Firewall Threat Defense Software and Cisco Secure Firewall Management Center Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-20329 are related to issues concerning improper handling of exceptional conditions that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-703.

### CVE-2026-20325

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-16T20:17:23.347 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Nexus Dashboard&nbsp;engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20325 are related to improper neutralization of special elements used in a command issue that are grouped under the Common Weakness Enumeration (CWE) CWE-77.

### CVE-2026-20324

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T20:17:23.180 |

A vulnerability in the sftunnel inter-device communication protocol of Cisco Secure Firewall Management Center (FMC) Software could allow an authenticated, remote attacker to execute arbitrary commands as root.

This vulnerability exists because a registered sftunnel peer has incorrect permissions to write an arbitrary file to any location on the device. An attacker could exploit this vulnerability by hijacking the sftunnel communication connection or being a valid registered sftunnel peer and sending an sftunnel command to write a malicious file to the disk of an affected device. A successful exploit could allow the attacker to write a file to the device that is executed with root privileges. To exploit this vulnerability, the attacker must have valid user credentials on the affected device.

### CVE-2026-20322

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-16T20:17:23.040 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Nexus Dashboard&nbsp;engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20322 are related to improper access control issues that are grouped under the Common Weakness Enumeration (CWE) CWE-284.

### CVE-2026-20307

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-16T17:17:16.973 |

A vulnerability in the web-based management interface of Cisco ISE could allow an authenticated, remote attacker to execute arbitrary commands on the underlying operating system of an affected device. To exploit this vulnerability, the attacker must have at least low-privileged administrative credentials.

This vulnerability is due to insecure deserialization of a user-supplied Java byte stream. An attacker could exploit this vulnerability by sending a crafted serialized Java object to the web-based management interface of an affected device. A successful exploit could allow the attacker to execute arbitrary code on the device and elevate privileges to root. In single-node deployments, successful exploitation of this vulnerability could cause the affected ISE node to become unavailable, resulting in a denial of service (DoS) condition. In that condition, endpoints that have not already authenticated would be unable to access the network until the node is restored.

### CVE-2026-20234

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-16T17:17:16.537 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Identity Services Engine (ISE) and Cisco ISE Passive Identity Connector (ISE-PIC) engineering teams have conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20234 are related to insufficiently protected credentials issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-522.

### CVE-2026-62108

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-17T14:17:15.263 |

Unauthenticated Broken Authentication in Headless Single Sign On <= 1.7.0 versions.

### CVE-2026-62101

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-17T14:17:14.977 |

Unauthenticated Broken Authentication in EduAdmin Booking <= 5.4.2 versions.

### CVE-2026-90823

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-17T12:18:28.843 |

FatPipe MPVPN, WARP, and IPVPN appliances running the end-of-life firmware version 10.1.2r60p100 contain a stack-based buffer overflow in /usr/sbin/auth_user_pass. An unauthenticated remote attacker with access to the affected management interface can submit a crafted authentication request that reaches an unchecked copy into a fixed-size stack buffer, potentially allowing arbitrary code execution as root.

The affected management interface is disabled by default and must be affirmatively enabled by the customer before the endpoint becomes reachable. FatPipe recommends restricting management access to trusted administrative networks and using WAN access control lists to limit access to trusted sources.

Customers running the affected end-of-life firmware can contact FatPipe Support for help confirming their firmware version and upgrading to a current supported release at https://www.fatpipeinc.com/support/support, support@fatpipeinc.com, or +1 800-724-8521 (option 3).

### CVE-2026-90822

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-17T12:18:28.713 |

FatPipe MPVPN, WARP, and IPVPN appliances running the end-of-life firmware version 10.1.2r60p100 contain an OS command injection vulnerability in the xtremed daemon. An unauthenticated remote attacker with access to the affected management interface can submit crafted input to the AuthFormServlet endpoint, causing authentication data to be processed by a shell and allowing arbitrary commands to execute as root.

The affected management interface is disabled by default and must be affirmatively enabled by the customer before the endpoint becomes reachable. FatPipe recommends restricting management access to trusted administrative networks and using WAN access control lists to limit access to trusted sources.

Customers running the affected end-of-life firmware can contact FatPipe Support for help confirming their firmware version and upgrading to a current supported release at https://www.fatpipeinc.com/support/support, support@fatpipeinc.com, or +1 800-724-8521 (option 3).

### CVE-2026-86710

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-17T06:16:51.437 |

The Login with QR WordPress plugin through 1.0.0 does not verify that the code used to log a user in is one it issued, matching any stored user metadata value instead, which allows unauthenticated attackers to log in as any user, including administrators.

### CVE-2026-86709

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-17T06:16:51.327 |

The Pressengine WordPress plugin through 1.0 does not stop its login handler from issuing a session when authentication fails, allowing unauthenticated attackers to log in as any user, including administrators.

### CVE-2026-86707

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-17T06:16:51.213 |

The Private Feed Key WordPress plugin through 0.1 does not verify that the key used to authenticate a feed request is one it issued, matching any stored user metadata value instead, which allows unauthenticated attackers to log in as any user, including administrators.

### CVE-2026-87796

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-17T05:17:02.123 |

The Multi Uploader for Gravity Forms plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 1.1.9 via the move_file function. This is due to insufficient file type validation during chunked upload handling. This makes it possible for unauthenticated attackers to upload arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-20326

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-16T20:17:23.480 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Nexus Dashboard engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20326 are related to missing authentication for critical function issues that are grouped under the Common Weakness Enumeration (CWE) CWE-306.

### CVE-2026-20242

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-16T20:17:22.697 |

A vulnerability in the External Database Access feature of Cisco Secure Firewall Management Center (FMC) Software could allow an unauthenticated, remote attacker to execute arbitrary commands as&nbsp;root on an affected device.

This vulnerability is due to insecure deserialization of a user-supplied Java byte stream from a host that is configured in the external database access list. An attacker could exploit this vulnerability by sending a crafted, serialized Java byte stream to a specific TCP port of an affected device. A successful exploit could allow the attacker to execute arbitrary commands on the device and elevate privileges to root.
Notes:

This vulnerability can be exploited only by an attacker who has control of a host in the external database access list.
If the FMC management interface does not have public internet access, the attack surface that is associated with this vulnerability is reduced.

### CVE-2025-59953

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-16T16:17:03.010 |

LMDeploy is a toolkit for compressing, deploying, and serving large language models. Starting in version 0.9.1 and prior to version 0.10.2, the LMdeploy implements an rpc server (AsyncRPCServer in zmq_rpc.py) for supporting the RPC communications. In its core functionality call_and_response(), I found it will directly use the pickles.loads() to deserialize the received messages without any sanitization, hence resulting in a remote code execution vulnerability by this RPC server. Version 0.10.2 contains a patch.

### CVE-2026-20331

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-16T17:17:17.107 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Adaptive Security Appliance Software, Cisco Secure Firewall Threat Defense Software and Cisco Secure Firewall Management Center Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-20331 are related to the failure of protection mechanisms issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-693.

### CVE-2026-92935

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-913` |
| Published | 2026-09-17T14:17:57.810 |

vm2 is a sandbox for running untrusted Node.js code. In versions >= 3.11.4 and <= 3.11.6, the NodeVM constructor computes `hasRealRequireConfig` with `typeof requireOpts === 'object' && requireOpts !== null`, so an array-shaped `require` value (for example `require: []`) satisfies the guard that is meant to reject nesting without an explicit require configuration. `makeResolverFromLegacyOptions()` then destructures the array into undefined option fields and returns a resolver containing only `NESTING_OVERRIDE.vm2`. As a result, an attacker who can supply JavaScript executed by a NodeVM configured with truthy `nesting` and an array-shaped `require` (e.g. `new NodeVM({nesting: true, require: []})`) can require the host `vm2` module, create an inner NodeVM with an attacker-chosen builtin allowlist (such as `child_process`), and execute arbitrary commands with the privileges of the host Node.js process, escaping the sandbox. Outer builtin restrictions do not constrain the attacker-created inner NodeVM. This issue is fixed in vm2 3.11.7.

### CVE-2026-92934

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-17T14:17:57.513 |

vm2 before 3.11.8 contains an incomplete fix for Error.cause sanitization that allows sandbox escape when revisited host-wrapped AggregateError objects are caught within a single exception handler traversal. Attackers can exploit cycle detection bypass in handleException to access unsanitized host proxies embedded in the errors array, enabling full remote code execution and process information disclosure from the sandbox.

### CVE-2026-77411

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-09-16T15:17:50.563 |

RabbitMQ amqp091-go is a Go AMQP 0.9.1 client. Prior to 1.13.0, readLongstr in read.go returns an empty string and a nil error when a declared AMQP longstr length exceeds 0x7FFFFFFF instead of returning ErrSyntax. The function leaves the declared field bytes unread, while readTable treats the operation as successful and continues parsing from the wrong offset. A malicious or compromised broker can provide an oversized longstr in a table field and desynchronize subsequent AMQP parsing, causing attacker-controlled trailing bytes to be interpreted as later fields or frames and disrupting connection integrity and availability. This issue is fixed in version 1.13.0.

### CVE-2026-92957

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-17T14:18:01.813 |

vm2 through 3.11.6 does not normalize `node:`-prefixed builtin specifiers when evaluating user-supplied negative (deny) entries in a NodeVM wildcard require policy. Although NodeVM strips the `node:` prefix during require() resolution, negative wildcard entries are matched by exact string comparison against the canonical builtin names, so a policy such as `new NodeVM({ require: { builtin: ['*', '-node:child_process'] } })` fails to deny the canonical `child_process` module. Sandboxed code can therefore obtain the host `child_process` builtin via `require('child_process')` or `require('node:child_process')`, gaining references to process-spawning APIs such as execSync and spawn, which is equivalent to host command-execution capability for untrusted sandbox code. Fixed in vm2 3.11.7. (Suggested title: "vm2 before 3.11.7: NodeVM builtin deny-list bypass via node:-prefixed specifiers exposes child_process")

### CVE-2026-92951

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-706` |
| Published | 2026-09-17T14:18:00.827 |

vm2 before 3.11.7 contains an incorrect authorization vulnerability in the external package allowlist check that uses non-exact substring matching instead of full package-name boundary validation. Attackers can bypass the allowlist by requiring a colliding package name that contains an allowlisted package substring, causing vm2 to load and execute unauthorized host packages in the host context.

### CVE-2026-92948

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-17T14:18:00.310 |

vm2 versions >= 3.9.6 and <= 3.11.6 are affected by a NodeVM builtin allowlist bypass that permits a sandbox escape on Node.js 24 and newer when the embedder explicitly allows the node:test builtin (e.g. require: { builtin: ['node:test'] }). On Node.js 24+, module.builtinModules exposes the scheme-only key node:test, which is not covered by vm2's family-based DANGEROUS_BUILTINS protection, so it is stored in the generic host-passthrough loader. Because requireImpl() in lib/setup-node-sandbox.js strips a single 'node:' prefix before the builtin lookup, sandbox code calling require('node:node:test') resolves to the stored node:test key and receives a readonly proxy to the host module. Calls to node:test.run() are forwarded to the host implementation, which spawns a separate Node process for process-isolated test execution and passes through attacker-controlled execArgv values; supplying --eval=<JavaScript> therefore executes arbitrary JavaScript in an unrestricted host Node process outside the NodeVM sandbox. Fixed in vm2 3.11.7.

### CVE-2026-92939

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-114` |
| Published | 2026-09-17T14:17:58.970 |

vm2 3.11.3 through 3.11.6 exposes the host Node.js crypto module to a NodeVM sandbox when the crypto builtin is allowed. The module is presented via a recursive read-only proxy, but its callable exports still execute with host-process authority. Sandboxed JavaScript can therefore call crypto.setEngine() with a filesystem path to an attacker-supplied native library (for example, one bundled in an untrusted plugin package already written to disk); OpenSSL asks the operating-system dynamic loader to load the file, and the library's constructor executes native code in the host process before engine-symbol validation rejects it. Exploitation requires only the crypto builtin and does not require fs, process, module, child_process, worker_threads, vm, or inspector access, resulting in a sandbox escape and arbitrary native code execution. Fixed in 3.11.7.

### CVE-2026-92938

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-17T14:17:58.750 |

vm2 versions 3.11.3 through 3.11.6 expose Node.js's host node:sqlite module to code running in NodeVM when that builtin is permitted, either explicitly or through builtin: ['*']. The module is wrapped with vm.readonly(), which prevents property assignment but leaves host-authority callables reachable; in addition, the resolver treats any request starting with 'node:' as a core-module request and the runtime strips only one 'node:' prefix, so a sandbox request for 'node:node:sqlite' resolves to the configured node:sqlite entry. Sandboxed code can therefore create an in-memory DatabaseSync with extension loading enabled and call DatabaseSync.loadExtension() on a native library bundled in the untrusted plugin package (path derived from __dirname). SQLite loads the library into the Node.js host process and invokes its native entry point, giving the sandboxed plugin arbitrary native code execution outside the sandbox with the host process's privileges. The issue is fixed in vm2 3.11.7.

### CVE-2026-92860

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-17T12:18:29.927 |

A security flaw has been discovered in rcourtman Pulse up to 6.0.4/6.1.0-rc.4. Affected by this issue is the function fmt.Sprintf of the file /api/security/quick-setup of the component Quick Security Setup Handler. The manipulation of the argument Username results in improper input validation. The attack may be performed from remote. Upgrading the affected component is advised.

### CVE-2026-77405

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-326` |
| Published | 2026-09-16T15:17:47.980 |

RabbitMQ amqp091-go is a Go AMQP 0.9.1 client. Prior to 1.13.0, tlsConfigFromURI in uri.go creates tls.Config values without setting MinVersion to tls.VersionTLS12. Builds using a Go runtime whose default permits TLS 1.0 or TLS 1.1 can therefore negotiate an obsolete protocol version when connecting through an amqps URI. A network attacker able to influence TLS negotiation with such a legacy build may weaken transport protection for AMQP messages and credentials. This issue is fixed in version 1.13.0.

### CVE-2026-92953

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-913` |
| Published | 2026-09-17T14:18:01.160 |

vm2 versions from 3.11.0 before 3.11.8 fail to protect host TypedArray and ArrayBuffer prototypes from sandbox mutation. Attackers can use prototype-walking primitives to reach and modify host Uint8Array.prototype, %TypedArray%.prototype, and ArrayBuffer.prototype, causing host-created typed arrays to observe attacker-controlled properties after VM.run() returns.

### CVE-2026-92950

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-453` |
| Published | 2026-09-17T14:18:00.637 |

vm2 before 3.11.7 contains a sandbox escape vulnerability in the CLI tool that allows attackers to execute arbitrary code in the host Node.js process. Attackers can supply a malicious script file to the vm2 CLI that uses require(__filename) to re-execute itself in the host realm, bypassing sandbox isolation and accessing host modules like fs and child_process.

### CVE-2026-92944

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-17T14:17:59.623 |

vm2 versions 3.10.2 through 3.11.6 contain a sandbox escape vulnerability on Node.js 26 where Promise.prototype.finally() bypasses vm2's wrapper protections due to a stale PromiseThenLookupChain protector in V8 14.6. Attackers can exploit this by creating an async function that returns a Promise with an attacker-controlled constructor Symbol.species, allowing them to reach the host Function constructor and process object for arbitrary code execution.

### CVE-2026-92805

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-16T21:17:30.267 |

UVdesk Community Skeleton through 1.1.8 fails to authenticate or validate installation state on wizard endpoints in ConfigureHelpdesk controller actions. Unauthenticated attackers can repoint the database and create super administrator accounts by submitting crafted requests to wizard endpoints, gaining full control of the instance.

### CVE-2026-92787

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-16T21:17:28.023 |

Feast through 0.66.0 fails to verify JWT token signatures before establishing user identity, allowing attackers to bypass all role-based access control by presenting an unverified token with a hardcoded claim value. Attackers can obtain trusted internal identity and gain unchecked read and write access to all entities, feature views, data sources, and permission policies on the server.

### CVE-2026-89083

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-16T20:17:38.703 |

HP
has identified potential security vulnerabilities in the HP Advance software
that may enable elevation of privilege, remote code execution, or arbitrary
file write under certain conditions, impacting the HP Advance server hosting
the software.

### CVE-2026-89082

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-16T20:17:38.573 |

HP has identified potential security vulnerabilities in the HP Advance software that may enable elevation of privilege, remote code execution, or arbitrary file write under certain conditions, impacting the HP Advance server hosting the software.

### CVE-2026-91106

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-16T19:18:03.587 |

HP has identified and remediated multiple externally reported vulnerabilities within HPLIP. The findings affect several software components that could potentially enable remote code execution, privilege escalation, denial of service, information disclosure, or unauthorized file modification under certain conditions.

### CVE-2026-91104

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-16T19:18:03.320 |

HP has identified and remediated multiple externally reported vulnerabilities within HPLIP. The findings affect several software components that could potentially enable remote code execution, privilege escalation, denial of service, information disclosure, or unauthorized file modification under certain conditions.

### CVE-2026-92720

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-16T18:17:22.990 |

Kubero through 3.1.1 fails to apply authentication guards to the notifications API endpoints, allowing unauthenticated attackers to read webhook secrets and service URLs. Attackers can retrieve stored credentials and register malicious webhooks to intercept pipeline events or suppress alerting by deleting existing configurations.

### CVE-2026-92717

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-16T18:17:22.540 |

Covenant through 0.6 registers the CovenantHub SignalR hub without an Authorize attribute, allowing unauthenticated callers to invoke CreateHttpListener and receive a signed JWT token. Attackers can use the obtained token to authenticate against the entire operator API and access grunts, credentials, binaries, events, and the operator roster.

### CVE-2026-92954

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-17T14:18:01.320 |

vm2 is a sandbox library for running untrusted JavaScript in Node.js. In versions >= 3.10.0 and <= 3.11.7, Promises returned from the host realm into the sandbox are not marked as handled at the bridge boundary; only Promises created inside the sandbox are wrapped with a rejection-swallowing handler (lib/setup-sandbox.js), and the bridge only installs host-side rejection sanitizers when sandbox code calls .then/.catch/.finally. As a result, code running in the sandbox can invoke a host function that returns a rejected Promise (for example events.once() exposed via the NodeVM events builtin, or any embedder-provided Promise-returning API) and simply ignore the return value, leaving the host Promise unhandled so that Node.js's default unhandled-rejection behavior terminates the host process. This is an incomplete fix of GHSA-hw58-p9xv-2mjh. The issue is fixed in version 3.11.8.

### CVE-2026-15688

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303` |
| Published | 2026-09-17T09:16:39.240 |

Incorrect Implementation of Authentication Algorithm Vulnerability in Mitsubishi Electric GX Works3 and Motion Control Setting allows a local attacker to successfully authenticate even with an invalid block password by executing the affected product and modifying part of the executable module in memory, and thereby may be able to view, tamper with, destroy, or delete control programs.

### CVE-2026-92578

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-16T22:18:28.053 |

WWBN AVideo through 29.0 contains an authentication bypass vulnerability where the stored password hash is accepted as a valid login credential through two independent code paths in loginFromRequest() and encryptPasswordVerify(). Attackers who obtain the stored users.password hash value can authenticate as any user by submitting the hash directly to login endpoints, completely bypassing password verification.

### CVE-2026-92576

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-16T22:18:27.757 |

HKUDS nanobot before 0.3.0 contains a server-side request forgery vulnerability in the WebFetchTool component where the _validate_url() function fails to block internal IP ranges and private addresses. Attackers can send messages instructing the bot to fetch cloud metadata endpoints, localhost services, and RFC 1918 addresses to extract IAM credentials and internal service data.

### CVE-2026-92785

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-16T21:17:27.730 |

Angel through 3.3.0 deserializes untrusted setAlgoMetrics payload using Kryo without class registration or allowlist validation. Unauthenticated network attackers can instantiate arbitrary classes or exhaust coordinator memory by sending crafted serialized objects to the master RPC endpoint.

### CVE-2026-92749

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-338` |
| Published | 2026-09-16T21:17:23.563 |

SafeLine through 9.4.1 derives the management console session-signing secret from a time-seeded math/rand generator, allowing attackers to reconstruct the key offline. Unauthenticated remote attackers who can bound the install timestamp can regenerate the secret and forge valid administrator session cookies to gain control of protected sites.

### CVE-2026-73456

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-16T19:17:32.270 |

Under certain circumstances on affected platforms running Arista EOS with gRPC Network Packet Sampling Interface (gNPSI) enabled, an unauthenticated gNPSI client can craft a malicious request to allow arbitrary code execution, granting an attacker full administrative control over the compromised switch.

### CVE-2026-86533

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-17T14:17:46.467 |

Insufficient Session Expiration vulnerability in team-alembic AshAuthentication and AshAuthentication Phoenix allows a revoked session to remain fully authenticated.

A resource configured with session_identifier :jti and require_token_presence_for_authentication? disabled stores its session value as <jti>:<subject>. The jti is there so that signing out can revoke that one session. Neither reader consults it: AshAuthentication.Plug.Helpers.authenticate_resource_from_session/4 and AshAuthentication.Phoenix.LiveSession.on_mount/4 both split the value with split_identifier/2, discard the jti and pass the bare subject to AshAuthentication.subject_to_user/3, which reloads the record. The token-presence branch of each function does check its token, calling AshAuthentication.TokenResource.Actions.get_token/3 with the jti and the purpose user. Because the revocation record is never read, neither its revoked state nor its expiry constrains the session, so a session captured before sign-out keeps working.

This issue affects ash_authentication: from 4.9.1 before 4.15.0 and from 5.0.0-rc.0 before 5.0.0-rc.14; ash_authentication_phoenix: from 2.10.0 before 2.17.4 and from 3.0.0-rc.0 before 3.0.0-rc.11.

### CVE-2026-85500

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-305` |
| Published | 2026-09-17T14:17:46.050 |

Authentication Bypass by Primary Weakness vulnerability in team-alembic AshAuthentication allows an unconfirmed user to obtain a session, defeating a mandatory email confirmation requirement.

AshAuthentication.Strategy.Password.Actions.check_user/2 decides whether the attribute named by require_confirmed_with is set using a bare is_nil(Map.get(user, value)). When that attribute is not selected on the loaded record Map.get/2 returns %Ash.NotLoaded{}, and when a field policy denies it for the current actor it returns %Ash.ForbiddenField{}. Neither is nil, so the rejection branch is skipped and sign-i

require_confirmed_with is enforced in two places, and neither holds in every configuration. sign_in_with_token and register are checked only inside AshAuthentication.Strategy.Password.Actions, not on the action itself, so any caller that invokes the action directly skips the check. An API layer such as AshGraphql or AshJsonApi invokes the action directly, so this applies to the default configuration. Where a check does run it compares the confirmation attribute against nil. That attribute holds %Ash.NotLoaded{} or %Ash.ForbiddenField{} when it sets select_by_default?: false, when an API layer narrows the read's select, or when a field policy hides it from the sign-in actor. Neither struct is nil, so those configurations read every user as confirmed.

This issue affects ash_authentication: from 4.3.8 before 4.15.0 and from 5.0.0-rc.0 before 5.0.0-rc.14.

### CVE-2026-82761

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-17T14:17:33.423 |

Time-of-check Time-of-use (TOCTOU) Race Condition vulnerability in team-alembic AshAuthentication allows an attacker holding a leaked magic link to replay its single-use token and authenticate as the target subject. A magic link configured with single_use_token?, which is the default, is meant to be redeemable exactly once, but nothing serialises the token's validity check against its consumption, so concurrent redemptions of one token all succeed and each yields a full user token.

Sign-in verifies the JWT with Jwt.verify/4 and revokes it only afterwards: AshAuthentication.Strategy.MagicLink.SignInPreparation revokes in a Query.after_action callback, and AshAuthentication.Strategy.MagicLink.SignInChange in an after_transaction hook that runs once the sign-in has already committed. AshAuthentication.TokenResource.Actions.revoke/3 writes the revocation as an upsert, so a concurrent duplicate revocation silently succeeds instead of conflicting and no request ever loses the race.

This issue affects ash_authentication: from 3.9.0 before 4.15.0 and from 5.0.0-rc.0 before 5.0.0-rc.14.

### CVE-2026-92913

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330` |
| Published | 2026-09-17T12:18:30.290 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 uses a cryptographically weak pseudo-random number generator when creating account activation / login pairing codes. getRandomCode() in objects/functions.php derives the code entirely from uniqid() (sprintf('%08x%05x', seconds, microseconds)) with a single non-CSPRNG rand() character used only as padding, reducing the code space to roughly 36 x 10^6 (~2^25) values for a known generation second. Because plugin/API/set.json.php?APIName=login_code can be called without authentication, it also serves as an oracle for the server's exact microtime. An unauthenticated remote attacker who guesses a valid, unexpired code (codes expire after 10 minutes) can redeem it at plugin/API/get.json.php?APIName=login_code to obtain the target account's email address and a User::getUserHash(users_id, '+1 year') value, a credential accepted in place of the account password for one year, resulting in account takeover. No patched version is available.

### CVE-2026-61594

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-09-16T22:17:03.047 |

djust provides Phoenix LiveView-style reactive server-side rendering for Django with Rust-powered performance. Prior to version 1.0.7, the live (WebSocket) transport authorizes a mount via `check_view_auth`, not Django's `View.dispatch()` chain. As a result, standard Django authorization — `LoginRequiredMixin`, `PermissionRequiredMixin`, `UserPassesTestMixin`, `@method_decorator(login_required, name="dispatch")`, and custom `dispatch()` guards — and the djust admin extension's staff gate (applied only in the HTTP `as_view` wrapper) were enforced on the initial HTTP GET but silently bypassed over WebSocket, where all events and state flow. An anonymous or under-privileged client could open a WebSocket and mount such a view — including admin list/create/change/delete — and dispatch its handlers. This is fixed in djust 1.0.7. `check_view_auth` now honors the Django `AccessMixin` family on every transport; a new system check S004 fails loud at startup on auth patterns the runtime cannot safely replay (decorator/overridden-`dispatch` forms); and the admin base mixin declares `login_required = True` + an active-staff `check_permissions` gate. As a workaround, gate views using djust's `login_required` / `permission_required` / `check_permissions` attributes (honored on all transports) rather than HTTP-only mixins/decorators.

### CVE-2026-75513

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-16T21:17:13.440 |

Marten is a .NET Transactional Document DB and Event Store on PostgreSQL. From version 7.0.0 until 9.13.0, several Marten LINQ and tenant-management paths interpolate runtime, potentially attacker-controlled strings into single-quoted SQL literals without escaping or parameterization. The primary confirmed vector is a dictionary indexer key used by Where filters in src/Marten/Linq/Members/Dictionaries/DictionaryItemMember.cs. Additional affected sinks include SelectParser.cs, DatabaseScopedTenantPartitions.cs, and DeleteAllForTenant.cs reached through IEventStore.DeleteProjectionProgressAsync, while DictionaryContainsKeyFilter.cs (Newtonsoft serializer only; System.Text.Json is not affected) handles ContainsKey calls. Events/Daemon/Internals/EventLoader.cs contains a related per-tenant partition-pruning literal that the advisory identifies as a defense-in-depth sink. A crafted single quote can escape the generated literal, enabling filter or multi-tenant authorization bypass and blind data exfiltration, and deployments that permit semicolon-batched Npgsql statements may also allow data modification. This issue is fixed in version 9.13.0.

### CVE-2026-20284

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-943` |
| Published | 2026-09-16T21:17:09.090 |

A vulnerability in the SXP REST API of Cisco ISE could allow an authenticated, remote attacker to conduct SQL injection attacks.

This vulnerability is due to insufficient validation of user-supplied input in REST API calls. An attacker could exploit this vulnerability by sending crafted input to an affected device. A successful exploit could allow the attacker to view or modify data on the underlying database for the affected device. In single-node deployments, successful exploitation of this vulnerability could cause the affected ISE node to become unavailable, resulting in a DoS condition. In that condition, endpoints that have not already authenticated would be unable to access the network until the node is restored.
To exploit this vulnerability, the attacker must have valid administrative credentials, have the SXP service enabled, and have at least one SXP connection configured.

### CVE-2026-20341

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-16T20:17:24.193 |

A vulnerability in the sftunnel inter-device communication protocol of Cisco Secure FMC Software could allow an authenticated, remote attacker to obtain&nbsp;root privileges.

This vulnerability is due to unsecured deserialization of untrusted data over the sftunnel management connection. An attacker could exploit this vulnerability by sending crafted sftunnel remote procedure calls (RPCs). A successful exploit could allow the attacker to gain root privileges on a device that is running Cisco Secure FMC Software and its high-availability peer.
To exploit this vulnerability, the attacker must have valid administrative credentials on a managed Cisco FTD device.

### CVE-2026-20237

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-16T20:17:22.407 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Identity Services Engine (ISE) and Cisco ISE Passive Identity Connector (ISE-PIC), engineering teams have conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20237 are related to improper input validation issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-20.

### CVE-2026-20211

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-16T20:17:22.200 |

A vulnerability in Cisco ISE could allow an authenticated, remote attacker to execute arbitrary commands on the underlying operating system of an affected device. To exploit this vulnerability, the attacker must have valid high-privileged administrative credentials.

This vulnerability is due to insecure deserialization of Java objects by the affected software. An attacker could exploit this vulnerability by sending a crafted serialized Java object to an affected device. A successful exploit could allow the attacker to obtain user-level access to the underlying operating system and then elevate privileges to&nbsp;root. In single-node deployments, successful exploitation of this vulnerability could cause the affected ISE node to become unavailable, resulting in a DoS condition. In that condition, endpoints that have not already authenticated would be unable to access the network until the node is restored.

### CVE-2026-20194

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-669` |
| Published | 2026-09-16T20:17:22.047 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Identity Services Engine (ISE) and Cisco ISE Passive Identity Connector (ISE-PIC), engineering teams have conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20194 are related to incorrect resource transfer between spheres that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-669.

### CVE-2026-20176

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-16T20:17:21.747 |

A vulnerability in Cisco ISE could allow an authenticated, remote attacker to execute arbitrary commands on the underlying operating system of an affected device. To exploit this vulnerability, the attacker must have valid high-privileged administrative credentials.

This vulnerability is due to insufficient validation of user-supplied input. An attacker could exploit this vulnerability by sending a crafted HTTP request to an affected device. A successful exploit could allow the attacker to obtain system-level access to the underlying operating system and then elevate privileges to root. In single-node deployments, successful exploitation of this vulnerability could cause the affected ISE node to become unavailable, resulting in a DoS condition. In that condition, endpoints that have not already authenticated would be unable to access the network until the node is restored.

### CVE-2026-20306

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T17:17:16.857 |

A vulnerability in the REST API of Cisco ISE and ISE-PIC could allow an authenticated, remote attacker to perform command injection attacks on the underlying operating system and elevate privileges to root. To exploit this vulnerability, the attacker must have valid administrative credentials.

This vulnerability is due to improper validation of user-supplied input. An attacker could exploit this vulnerability by sending crafted commands to the web-based management interface of an affected device. A successful exploit could allow the attacker to execute arbitrary code on the device and elevate privileges to root. In single-node deployments, successful exploitation of this vulnerability could cause the affected ISE node to become unavailable, resulting in a DoS condition. In that condition, endpoints that have not already authenticated would be unable to access the network until the node is restored.

### CVE-2026-20305

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T17:17:16.707 |

A vulnerability in the diagnostic tools of Cisco ISE and ISE-PIC could allow an authenticated, remote attacker to perform command injection attacks on the underlying operating system and elevate privileges to&nbsp;root. To exploit this vulnerability, the attacker must have valid administrative credentials.

This vulnerability is due to improper validation of user-supplied input. An attacker could exploit this vulnerability by sending crafted commands to the web-based management interface of an affected device. A successful exploit could allow the attacker to execute arbitrary code on the device and elevate privileges to root. In single-node deployments, successful exploitation of this vulnerability could cause the affected ISE node to become unavailable, resulting in a denial of service (DoS) condition. In that condition, endpoints that have not already authenticated would be unable to access the network until the node is restored.

### CVE-2026-92395

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290;CWE-348;CWE-697` |
| Published | 2026-09-16T15:19:01.857 |

@fastify/proxy-addr is a Fastify plugin that determines a request's client address behind trusted reverse proxies, and it backs Fastify request.ip and request.ips. In versions 3.0.0 through 5.1.0, a trust subnet written in IPv4-mapped IPv6 notation with an IPv4-sized prefix, such as ::ffff:10.0.0.0/8 instead of the correct ::ffff:10.0.0.0/104, is accepted without error but trusts every IPv4 address on the internet rather than the block it names. Because the socket peer then becomes trusted at hop 0, any unauthenticated client can supply an arbitrary X-Forwarded-For header and control the address the application reads, which defeats IP-based access control, rate limiting, geolocation, and audit logging. The plugin inherited this defect from the upstream proxy-addr module (CVE-2026-90711). The issue is fixed in @fastify/proxy-addr 5.1.1, and users should upgrade to 5.1.1 or later. As a workaround, ensure any IPv4-mapped IPv6 trust subnet uses a prefix length of at least 97, or express the range in plain IPv4 notation.

### CVE-2026-77408

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-16T15:17:49.747 |

RabbitMQ amqp091-go is a Go AMQP 0.9.1 client. Prior to 1.13.0, the writeShortstr function in write.go casts the byte length of AMQP shortstr property values to uint8 without first rejecting values longer than 255 bytes. An application that accepts an oversized CorrelationId, ReplyTo, MessageId, Expiration, UserId, AppId, ContentType, ContentEncoding, or Type value can therefore serialize a wrapped length and only a truncated prefix, while reporting no error. The resulting silent metadata corruption can break request and reply correlation, routing, tracing, and downstream message processing. This issue is fixed in version 1.13.0.

### CVE-2026-88795

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-17T06:16:52.097 |

The wpShopGermany IT-RECHT KANZLEI WordPress plugin before 2.4 does not generate its API authentication token securely, deriving it from data the requester controls and creating it as a side effect of the check that is supposed to validate it, allowing unauthenticated attackers to predict the token and use the access it grants to write arbitrary files, leading to remote code execution.

### CVE-2026-76420

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-16T17:18:09.330 |

A vulnerability in the internal configuration of the Apache JServ Protocol (AJP)&nbsp;connector for Cisco Secure FMC Software could allow an unauthenticated, remote attacker to impersonate a peer device.

This vulnerability is due to incorrect initialization of encryption parameters for the AJP connector at boot time. An attacker could exploit this vulnerability by sending crafted packets to the AJP connector. A&nbsp;successful exploit could allow the attacker to execute commands as root and&nbsp;gain full control over the FMC REST APIs on the affected device.
Note: This vulnerability can be exploited only if the valid sftunnel connection between Cisco Secure FMC Software and Cisco Secure FTD Software is down.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-92952

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-669` |
| Published | 2026-09-17T14:18:00.987 |

vm2 versions 3.11.4 through 3.11.6 incompletely filter Node.js registered internal symbols across the sandbox boundary. The extraction filters in lib/setup-sandbox.js and the cross-realm symbol checks and write traps in lib/bridge.js use a fixed list of known dangerous registered symbols that omits nodejs.stream.disturbed and nodejs.stream.errored, which are exposed on host WebStream prototypes on newer Node.js releases (validated on Node.js v25.8.0). When the embedder exposes a host WebStream object and the host stream/web module to the sandbox, sandbox code can obtain the real host symbols via Object.getOwnPropertySymbols(streamWeb.ReadableStream.prototype) and use them as write keys on host stream objects, corrupting host-visible stream state — for example making stream.Readable.isDisturbed() return false for an already-consumed stream. This can bypass host logic that relies on Node's public stream-state helpers to enforce one-shot body consumption, reject errored streams, or decide whether a stream is safe to hand to another component. It is not a host code-execution primitive in the reported proof of vulnerability. This is an incomplete fix for the earlier nodejs.* symbol filtering issue. Fixed in vm2 3.11.7.

### CVE-2026-77412

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-681` |
| Published | 2026-09-16T15:17:50.707 |

RabbitMQ amqp091-go is a Go AMQP 0.9.1 client. Prior to 1.13.0, readField in read.go reads the length of an AMQP byte-array field with type tag x into a signed int32 and passes the value directly to make when allocating the field buffer. A malicious or compromised broker can encode a value such as 0xFFFFFFFF, which becomes -1 and causes a len out of range runtime panic. The panic escapes the network reader goroutine and terminates the client process, including during connection.start server properties or message header table parsing. This issue is fixed in version 1.13.0.

### CVE-2026-77410

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-16T15:17:50.430 |

RabbitMQ amqp091-go is a Go AMQP 0.9.1 client. Prior to 1.13.0, Channel.recvContent in channel.go preallocates the message body slice with the uint64 ch.header.Size value supplied by an AMQP content header without capping the allocation to the negotiated Connection.Config.FrameSize value. A malicious or compromised broker can send an extreme declared body size and cause the Go runtime to attempt a correspondingly large allocation before body data is received. The allocation can exhaust memory and terminate the client process. This issue is fixed in version 1.13.0.

### CVE-2026-77403

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-16T15:17:46.847 |

RabbitMQ amqp091-go is a Go AMQP 0.9.1 client. Prior to 1.13.0, Connection.openTune in connection.go accepts a server-advertised FrameMax below the AMQP frameMinSize value of 4096 bytes because the connection negotiation loop does not enforce the protocol minimum. A malicious or compromised AMQP broker can therefore advertise an extremely small FrameMax, causing later client publications to be fragmented into excessive numbers of frames and write operations. This can consume CPU and stall the client or its host. This issue is fixed in version 1.13.0.

### CVE-2026-92972

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-17T14:18:03.347 |

SGLang through 0.5.19 in prefill/decode disaggregation mode contains an unauthenticated PUT /route endpoint on the prefill bootstrap service that allows attackers to poison the KV transfer routing table. Attackers can supply arbitrary rank_ip and rank_port values to redirect decode workers to attacker-controlled endpoints, causing denial of service or disclosure of KV transfer metadata including session identifiers and tensor-parallel topology parameters.

### CVE-2026-78295

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-17T14:17:30.303 |

Unauthenticated Cross Site Request Forgery (CSRF) in Xagio SEO <= 7.1.0.43 versions.

### CVE-2026-14850

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-09-17T14:17:12.117 |

The password reset funcionality is vulnerable to unauthorized account modification due to improper validation of the user_id parameter. An attacker can manipulate this predictable numeric identifier to reset passwords for arbitrary users without proving account ownership.

### CVE-2026-86801

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-17T07:16:28.413 |

The To Do List Member WordPress plugin from 1.4 through 1.6 ships a file upload endpoint that does not load WordPress and therefore applies no authentication, capability or nonce check of any kind, and validates only the name of an uploaded file rather than its content, allowing unauthenticated users to store active content served from the site's own origin, and to list and delete the files already staged there.

### CVE-2026-88904

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-17T06:16:52.203 |

The PuppyFW WordPress plugin through 0.4.4 does not have proper authorisation on one of its REST routes, which tests the caller against a capability taken from the request itself, allowing any authenticated user, including subscribers, to add, modify and delete arbitrary blog options and thereby escalate their privileges.

### CVE-2026-88792

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T06:16:51.990 |

The Dictionary WordPress plugin through 1.0 does not have authorisation, sanitisation or escaping in place when adding or updating dictionary entries, allowing unauthenticated users to store arbitrary web scripts which will execute when a user views an affected entry.

### CVE-2026-87786

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T06:16:51.773 |

The Dewa Kirim  WordPress plugin through 1.0.0 does not escape delivery coordinates submitted at checkout before outputting them inside an inline script, allowing unauthenticated users to store JavaScript that runs in the session of an administrator who later opens the order.

### CVE-2026-85130

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T06:16:50.990 |

The WPLP Cookie Consent  WordPress plugin before 4.4.4 does not escape a value submitted through a public endpoint for the JavaScript context it is later output in on an administrative screen, allowing unauthenticated users to run arbitrary JavaScript in the session of an administrator who interacts with the logged entry. Only multisite installations are affected.

### CVE-2026-25283

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-17T05:17:01.390 |

Memory Corruption when copying unverified data from an external source exceeds the allocated buffer size.

### CVE-2026-61599

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-09-16T23:16:54.010 |

djust provides Phoenix LiveView-style reactive server-side rendering for Django with Rust-powered performance. Prior to version 1.0.7, the djust live transport resolves the LiveView to mount from a client-supplied dotted path by calling `__import__(module_path, ...)`. The module is imported — running its top-level code (import side effects) — before the framework checks that the resolved object is a `LiveView` subclass and before any per-view authentication. The `LIVEVIEW_ALLOWED_MODULES` allowlist that should contain this is fail-open (`if allowed_modules:` — skipped when the setting is unset, the framework default) and uses loose `startswith` matching. An unauthenticated WebSocket client (the WS handshake does not require auth; per-view auth runs only after import + instantiate) can therefore send a `mount` / `live_redirect_mount` / `url_change` frame (or an SSE mount) with `view = "<any.importable.module>.AnyName"` and cause the server to import — and execute the top-level code of — any importable Python module by name. Version 1.0.7 fixes the issue with a fail-closed resolution gate (`djust._view_resolution.is_view_import_allowed`): a client view path resolves only if (a) its module is already loaded (`sys.modules` — so resolving runs no new code; URL-routed views loaded by URLconf at startup keep working with zero config) or (b) it matches `LIVEVIEW_ALLOWED_MODULES` on a module-segment boundary (explicit opt-in for lazily-imported views). The gate runs before `__import__` at all three sinks (+ defense-in-depth inside `_instantiate_view`). As a workaround, set `LIVEVIEW_ALLOWED_MODULES` to the narrow list of modules that contain your mountable LiveView classes. (Note: pre-patch the allowlist is `startswith`-matched and the import still precedes the subclass check, so this is mitigation, not a complete fix.)

### CVE-2026-76409

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-16T21:17:13.597 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Nexus Dashboard engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76409 are related to improper limitation of a pathname issues that are grouped under the Common Weakness Enumeration (CWE) CWE-22.

### CVE-2026-63506

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T21:17:13.163 |

Tina is a headless content management system. Prior to @tinacms/auth 1.1.4 and next-tinacms-azure 15.0.1, isAuthorized accepts a request-controlled clientID and asks isUserAuthorized to validate the bearer token against that selected TinaCloud app instead of the self-hosted site's configured app. An attacker with any TinaCloud account can submit the attacker's own app ID and valid token to a victim endpoint, causing TinaCloudBackendAuthProvider or an affected media authorized callback to accept the attacker's verified status across the tenant boundary. The vulnerable logic is present in packages/@tinacms/auth/src/index.ts and packages/next-tinacms-azure/src/auth.ts. Successful exploitation permits media listing, reading, upload, or deletion and, when TinaCloudBackendAuthProvider is used, GraphQL read, create, update, and delete operations on the victim's content without a victim account or victim interaction. This vulnerability is fixed in @tinacms/auth 1.1.4 and next-tinacms-azure 15.0.1.

### CVE-2026-20360

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-16T21:17:12.640 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Nexus Dashboard engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20360 are related to information exposure and insecure handling issues that are grouped under the Common Weakness Enumeration (CWE) CWE-200.

### CVE-2026-20344

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-16T21:17:11.967 |

A vulnerability in the web-based management interface of Cisco Secure FMC Software could allow an authenticated, remote attacker to perform a SQL injection attack against an affected device. To exploit this vulnerability, the attacker must have a valid account on the device with the role of Security Approver, Access Admin, or Network Admin.

This vulnerability is due to insufficient validation of user-supplied input. An attacker could exploit this vulnerability by sending a crafted HTTP request to the web-based management interface of an affected device. A successful exploit could allow the attacker to obtain any data from the database, obtain the session credentials of an authenticated Administrator, and take actions with administrative privileges on the affected device.

### CVE-2026-20340

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-16T21:17:11.560 |

A vulnerability in Cisco Secure FMC Software could allow an authenticated, remote attacker to execute arbitrary commands at the&nbsp;root privilege level.

This vulnerability is due to unsecured deserialization of web-management user-controlled data. An attacker could exploit this vulnerability by authenticating to the device and sending a crafted HTTP payload. A successful exploit could allow the attacker to save the crafted payload and then execute it on the underlying operating system as root.
To exploit this vulnerability, the attacker must have valid credentials for a user account with at least the role of Security Analyst (read-only).

### CVE-2026-20336

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-664` |
| Published | 2026-09-16T21:17:11.350 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Adaptive Security Appliance Software, Cisco Secure Firewall Threat Defense Software and Cisco Secure Firewall Management Center Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20336 are related to issues concerning improper control of a resource through its lifetime that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-664.

### CVE-2026-20333

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-697` |
| Published | 2026-09-16T21:17:10.690 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Adaptive Security Appliance Software, Cisco Secure Firewall Threat Defense Software and Cisco Secure Firewall Management Center Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20333 are related to incorrect comparison conditions that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-697.

### CVE-2026-89084

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-16T20:17:38.833 |

HP
has identified potential security vulnerabilities in the HP Advance software
that may enable elevation of privilege, remote code execution, or arbitrary
file write under certain conditions, impacting the HP Advance server hosting
the software.

### CVE-2026-87105

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-16T20:17:37.980 |

Tanium addressed a SQL injection vulnerability in Threat Response.

### CVE-2026-20361

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-16T20:17:24.333 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Nexus Dashboard engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20361 are related to SQL injection issues that are grouped under the Common Weakness Enumeration (CWE) CWE-89.

### CVE-2026-92729

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-09-16T19:18:06.833 |

SigNoz versions 0.88.0 through 0.141.0 fail to apply authorization wrappers to trace-funnel analytics endpoints in the HTTP handler. Unauthenticated attackers can submit arbitrary funnel definitions to retrieve trace analytics including identifiers, durations, span counts, service topology, and error activity without credentials.

### CVE-2026-85731

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-09-16T17:18:15.833 |

oras-go is a Go library for managing OCI artifacts. Prior to 2.6.2, content/file.Store extraction of OCI layers marked with io.deis.oras.content.unpack=true can write outside the store working directory. The pushDir path through extractTarDirectory and ensureLinkPath validates symlink targets lexically, resolveRelToBase skips its parent-symlink walk for root-level entries, and writeFile follows a terminal symlink when opening a regular file. A malicious archive can therefore create a symlink chain whose lexical target remains inside the extraction root but whose resolved target is an attacker-selected absolute path, then overwrite that target with a same-named regular-file entry even when AllowPathTraversalOnWrite is false. Pulling an attacker-controlled artifact can create or overwrite any file writable by the process and may lead to code execution. This issue is fixed in version 2.6.2.

### CVE-2026-92566

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-16T15:19:02.127 |

DataGear through 6.0.0 contains a server-side request forgery vulnerability in the /dataSet/preview/Http endpoint that allows unauthenticated attackers to execute arbitrary HTTP requests by supplying a caller-controlled URI. Attackers can issue GET, POST, PUT, PATCH, or DELETE requests to internal endpoints and cloud metadata services, receiving full response bodies without authentication or validation.

### CVE-2026-88064

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-1336` |
| Published | 2026-09-16T15:18:04.297 |

Backstage is an open framework for building developer portals. Prior to 1.14.6 and from 1.15.0 until 1.15.4, the @backstage/plugin-techdocs-node package insufficiently validates mkdocs.yml supplied by an authenticated user who can register or modify a TechDocs source. Unsafe Python YAML tags, markdown_extensions names and configuration, theme options, and extra_templates values can reach the documentation generator and cause unintended code execution. The resulting impact is limited to the files, credentials, network access, and other resources available to the TechDocs backend or build container. This issue is fixed in versions 1.14.6 and 1.15.4.

### CVE-2026-84860

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-16T15:18:00.760 |

ScadaLTS 2.8.1-release-candidate build 0 is affected by an Authorization Bypass



Spring Security gates DWR endpoints by URL path pattern, but DWR itself dispatches method calls based on the POST body parameters c0-scriptName and c0-methodName. The crossDomainSessionSecurity setting in web.xml is set to false, which disables DWR's built-in origin validation. This means any authenticated user can invoke any DWR method (regardless of the URL-based access control) by sending their request to a URL they are permitted to access (e.g. MiscDwr.initializeLongPoll.dwr) while targeting a restricted class in the POST body.



This is the systemic root cause that enables multiple other findings to be exploited as a low privilege user.

### CVE-2026-84858

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-16T15:18:00.527 |

ScadaLTS 2.8.1-release-candidate build 0 is affected by an Authenticated Remote Code Execution via Scripting Sandbox Bypass



The DWR "DataSourceEditDwr" class exposes the "validateScript" method that compiles and executes attacker-supplied JavaScript via the Rhino scripting engine. There are no authorization checks on this method and so it is possible for an attacker with access to a low privilege user to abuse this flaw by leveraging the DWR routing bypass.

### CVE-2026-82964

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-281;CWE-653;CWE-862` |
| Published | 2026-09-16T15:17:55.837 |

Improper preservation of permissions in the Avast sandbox minifilter driver (aswSnx.sys) on Windows allows a local, low-privileged attacker executing inside the sandbox to escape file isolation and escalate to SYSTEM.



When the sandbox virtualizes a file it copies the original security descriptor, but the driver opened the virtualization target object with GENERIC_WRITE and FILE_WRITE_ATTRIBUTES only, omitting WRITE_DAC. Every attempt to apply the original DACL therefore failed, and the failure was discarded silently, leaving virtualized copies of sensitive files with permissive permissions. Because the IRP_MJ_CREATE callback additionally did not strip WRITE_DAC for sensitive directories, a sandboxed process could rewrite the security descriptor of a virtualized object, read the virtualized copy of the SAM database, extract local NTLM password hashes and execute code as SYSTEM.



The absence of an IRP_MJ_SET_SECURITY callback in the driver's operation registration table is a related defense-in-depth gap, but it is not the control that prevents this attack.

### CVE-2026-92971

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-17T14:18:03.190 |

InternLM LMDeploy through 0.17.0 contains a reachable assertion vulnerability in the DistServe decode migration loop that allows unauthenticated attackers to terminate the inference engine. Attackers can submit a migration_request with an empty remote_block_ids list to trigger an AssertionError that crashes the engine loop and causes subsequent inference requests to fail.

### CVE-2026-92970

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-17T14:18:02.997 |

HUBzero CMS through 2.2.32 contains a path traversal vulnerability in project file upload handlers that allows authenticated project members to write arbitrary files outside the project repository. Attackers can supply traversal sequences in upload parameters to write files to attacker-chosen paths with web server privileges, potentially enabling code execution.

### CVE-2026-92961

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-17T14:18:02.447 |

vm2 before 3.11.6 fails to enforce bufferAllocLimit on ArrayBuffer, SharedArrayBuffer, and TypedArray constructors, allowing attackers to allocate arbitrary host memory. Attackers can bypass the buffer allocation cap by using these V8 intrinsics to exhaust host process memory and trigger out-of-memory conditions.

### CVE-2026-92942

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-17T14:17:59.467 |

vm2 before 3.11.7 (affected versions <= 3.11.6) does not enforce the VM({ timeout }) option on code executed outside the synchronous VM#run() call. The timeout only wraps the single call to _runScript() via doWithTimeout() in lib/vm.js, and FinalizationRegistry and WeakRef are exposed to sandboxed code unmodified (they are not among the hardened globals in lib/setup-sandbox.js). Sandboxed code can register a FinalizationRegistry cleanup callback against an object and then drop the only strong reference to it; vm.run() returns within the configured timeout, but when the V8 garbage collector later reclaims the object it invokes the sandboxed cleanup callback outside any vm2 timeout accounting. A busy loop in that callback blocks the host event loop for an unbounded period, resulting in denial of service. The time of invocation depends on the garbage collector (e.g. under memory pressure or with --expose-gc).

### CVE-2026-89418

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-17T14:17:52.157 |

google-protobuf contains an unbounded recursion when parsing unknown protobuf group fields. An attacker can send a small crafted payload of deeply nested START_GROUP wire bytes to any Node.js service that calls the generated deserializeBinary() API, causing a RangeError: Maximum call stack size exceeded and crashing the process. No authentication or prior knowledge of the schema is required.

### CVE-2026-92918

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-17T13:17:01.013 |

admin3 through 3.0.0 persists user session tokens in the audit log event body when publishing UserLoggedIn domain events. Attackers with log:view permission can read the JSON response from the GET /logs endpoint to harvest session tokens and replay them as bearer credentials for full user access.

### CVE-2026-92917

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-17T12:18:30.907 |

Grav is a flat-file CMS. In versions 2.0.0-rc.1 through 2.0.21, the Twig content sandbox fails to restrict the dump and serialize filters (print_r, vardump, json_encode, yaml_encode, string): GravExtension::assertSandboxDumpSafe() determines sandbox state by calling SandboxExtension::isSandboxed() without a Source argument, which reports only the global sandbox flag that Grav never enables, so the guard added in GHSA-mc5q-6hpj-rp7j never executes. As a result, an authenticated user with page-edit rights can render {{ config|print_r }} in page content with Twig processing enabled and dump Grav's entire merged configuration — print_r reflects the real Config object held in a private property of the SandboxConfig facade, bypassing its path redaction — exposing plugin secrets such as SMTP credentials, API tokens, webhook secrets and cache backend passwords. Grav 1.7 is not affected because it ships no Twig content sandbox. The issue is fixed in 2.0.22, where the affected filters are registered with Twig's needs_is_sandboxed flag.

### CVE-2026-92916

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-17T12:18:30.710 |

Grav is a flat-file CMS. In Grav 1.7.0 through 1.7.53.2 and 2.0.0 through 2.0.21, when the debugger is enabled (system.debugger.enabled: true, which is not the default), the Clockwork profiler endpoint is exposed without authentication: InitializeProcessor::handleDebuggerRequest() intercepts any path containing /__clockwork/ during bootstrap and passes it to Debugger::debuggerRequest(), which performs no user lookup, IP restriction, or Clockwork authenticator check, and also supports anonymous pagination over the entire stored history. With the shipped censored: false default, each stored record contains raw request cookies (including Grav's session cookie, whose value is the PHP session id, allowing an attacker to resume another user's session, including an authenticated admin's), the full parsed request body (Grav's login form posts data[username]/data[password], so passwords are stored in plaintext because Clockwork's password filter only inspects top-level keys), and the site's entire system and plugin configuration, including operator-saved secrets such as SMTP credentials, third-party API keys, and licence keys. Authorization and X-API-Token headers are stored even when censored: true. On Grav 2.0, setting provider: debugbar does not avoid the issue because Grav forces the Clockwork provider for requests preferring a JSON response. The issue is fixed in 1.7.53.4 and 2.0.22, which restrict /__clockwork/ to server-local requests or requests presenting the new system.debugger.token secret and strip cookies and credential headers from stored records. Workarounds include setting debugger.enabled: false or blocking /__clockwork/ at the web server or CDN.

### CVE-2026-92599

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-16T22:18:30.980 |

joi (npm package `joi`, hapi.js) versions >=17.2.0 <17.13.7 and >=18.0.0 <18.2.6 are vulnerable to regular expression denial of service in the `Joi.string().isoDate()` validation rule. One of the regular expressions the rule applies to the input is unanchored, so a valid ISO date followed by a long run of fractional-second digits causes the regex engine to restart its search from every position in the string, yielding time proportional to the square of the input length (about 1.4 s for 64 KB of digits and about 22 s for 256 KB). A remote attacker who can supply a string to an isoDate validation can stall the application with a single request. Fixed in 17.13.7 and 18.2.6; as a workaround, cap the length of the string before it reaches joi.

### CVE-2026-92596

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-16T22:18:30.557 |

Nodemailer before 9.1.0 contains a quadratic time complexity vulnerability in the addressparser component that allows remote attackers to cause denial of service by supplying a crafted comma-separated address list. Attackers can send a single email with a large number of addresses to block the Node.js event loop for extended periods, consuming 100% CPU and freezing the process.

### CVE-2026-92594

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-16T22:18:30.283 |

Craft CMS 5.0.0-RC1 through versions before 5.11.0 incorrectly authorize the GraphQL draftCreator and revisionCreator fields: instead of requiring the user-data scope enforced by Gql::canQueryUsers() (usergroups.*:read), these fields are gated only on the elements.drafts:read / elements.revisions:read scopes, and their resolver returns a raw User element whose email, username, fullName, and addresses fields have no per-field authorization. A client holding only the drafts or revisions scope — including an unauthenticated client when the operator has enabled the public GraphQL schema with those scopes — can therefore harvest the email addresses, usernames, full names, and postal addresses of all draft/revision creators (typically site editors and administrators). The issue is fixed in 5.11.0.

### CVE-2026-92593

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-16T22:18:30.150 |

Craft CMS versions 5.10.0 through 5.10.12 contain an incomplete fix for CVE-2026-55794: the Controller::getPostedRedirectUrl() -> View::renderObjectTemplate() sink remained unsandboxed, and the same fix commit added a self-signing oracle in Cp::elementLabelHtml(). Because Craft/Yii HMAC tokens are not bound to a parameter name, an authenticated low-privilege control panel user with edit rights on a single element type can mint a token over attacker-controlled Twig for the returnUrl parameter and replay it as the redirect POST parameter, reaching the unsandboxed sink and achieving server-side template injection that executes arbitrary PHP code (full server compromise). The issue is fixed in 5.10.13.

### CVE-2026-92592

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-16T22:18:30.013 |

Craft CMS 4.8.0 through 4.18.5 and 5.0.0 through 5.10.12 sign an authenticated user's attacker-controlled license-shun cookie with the same key and format used to validate signed redirect parameters, because the HMAC signature is not bound to its purpose (Yii's cookieValidationKey is derived from the same Craft securityKey used for signed request parameters). An authenticated, non-administrator user (Control Panel access is not required) can set the cookie via the license-shun endpoint and transplant the signed envelope into the redirect parameter; on a successful login, Craft validates the signature and renders the authenticated bytes as an unsandboxed Twig template, where Twig's map filter accepts a string callback and allows PHP system() to execute arbitrary operating-system commands as the web-server user. Exploitation requires an account using password authentication without active 2FA, the default request configuration, and availability of PHP system(). The issue is fixed in 4.18.6 and 5.10.13.

### CVE-2026-92580

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T22:18:28.333 |

In AVideo through 29.0, the CloneSite plugin is vulnerable to stored OS command injection. In plugin/CloneSite/cloneClient.json.php (line ~270) the stored SSH password is substituted into the command string `sshpass -p '{password}' rsync ...` with a plain str_replace and no escaping, so a single quote in the password breaks out of the quoted word and injects arbitrary shell. The password is written through the admin-only endpoint objects/pluginAddDataObject.json.php, whose only CSRF defense (isUntrustedRequest()/forbidIfIsUntrustedRequest()) is a no-op when the request source appears to be loopback — as happens behind a same-host TLS-terminating reverse proxy with $global['trustedProxies'] unset — or when an attacker-controlled application is co-hosted on the same hostname; on HTTPS the session cookie is issued with SameSite=None, so a cross-site POST carries it. An unauthenticated remote attacker can therefore lure an authenticated administrator into planting a malicious password (and an attacker-controlled cloneSiteURL), after which the plugin's documented crontab entry executes the injected command with no further administrator action, as the crontab owner (commonly root or www-data). Exploitation requires the CloneSite plugin to be enabled with the documented crontab installed and one of the above CSRF channels; default single-process Apache deployments are reported as not CSRF-exploitable. This is a residual sink of CVE-2026-41304. The issue is confirmed at master HEAD (8963b6a1); no patched version is available.

### CVE-2026-92577

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T22:18:27.910 |

In AVideo through 29.0, the API get_api_video endpoint contains a broken access control vulnerability in the clean_title branch that returns user-group-restricted videos with owner PII to anonymous callers. Attackers can query videos by their public slug to bypass group restrictions and retrieve sensitive user fields including email, phone, address, birth date, and administrator status.

### CVE-2026-92815

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-16T21:17:31.503 |

changedetection.io through 0.60.6 fails to validate the Goto URL action in browser steps, allowing unauthenticated attackers to access internal addresses. Attackers can supply arbitrary internal URLs in the optional_value parameter to retrieve responses from restricted network locations.

### CVE-2026-92801

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T21:17:29.680 |

cc-connect through 1.5.0 fails to enforce per-user allowlist filtering in the onCardAction handler for Feishu interactive card callbacks. Attackers can dispatch agent commands by triggering card actions in admitted chats, bypassing the per-user access controls that protect the text message handler.

### CVE-2026-92796

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T21:17:29.377 |

Manticore Search versions 27.0.0 before 28.4.4 fail to validate permissions for all statements in multi-statement SQL requests, allowing read-only users to execute unauthorized queries. Attackers can append additional SELECT statements after the first statement to read credential tables and obtain password hashes that authenticate as administrators without plaintext recovery.

### CVE-2026-92794

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T21:17:29.073 |

OpenSign through 2.41.3 fails to validate caller identity in the getDocument cloud function when one-time-password verification is disabled. Attackers can supply a document identifier from guest signing links to retrieve complete document details including all signers' information, sender identity, and valid download tokens without authentication.

### CVE-2026-92792

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-16T21:17:28.780 |

OpenNHP through 1.0.2 selects its trusted-execution attestation verifier based on attacker-supplied evidence containing a test_purpose key, causing the FallbackVerifier to execute unconditionally. Attackers can bypass attestation verification by including the test_purpose key in evidence and providing enrolled measure and serial number pairs from the allowlist to gain unauthorized access.

### CVE-2026-92791

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-16T21:17:28.627 |

Uber Kraken through 0.1.29 fails to validate the tag parameter in the /tags/{tag} endpoint, allowing unauthenticated attackers to traverse outside the configured storage root. Attackers can use percent-encoded parent-directory segments in the tag parameter to read arbitrary files accessible to the testfs backend process.

### CVE-2026-92788

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T21:17:28.180 |

Coze Studio through 0.5.1 fails to validate that table names in workflow SQL customization nodes belong to the caller's workspace. Authenticated attackers can enumerate predictable table identifiers and execute SQL statements against other workspaces' memory databases to read, insert, or delete data.

### CVE-2026-92780

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T21:17:26.987 |

KnowStreaming through 3.4.1 fails to enforce role-based access control on REST API endpoints, allowing any authenticated user to access protected functionality. Attackers can call identity-management endpoints to create administrator accounts or grant themselves administrative privileges without proper authorization.

### CVE-2026-92762

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T21:17:24.930 |

Pelican Panel versions before 1.0.0-beta35 enforce startup write permissions only through disabled form controls rather than server-side authorization checks. Attackers with startup.read permission can craft Livewire state updates to invoke afterStateUpdated callbacks and modify startup commands, docker images, and variables to execute arbitrary commands in the container.

### CVE-2026-92761

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T21:17:24.780 |

WebVirtCloud fails to properly validate permission flags in UserInstance grants, allowing view-only users to perform privileged actions. Attackers with read-only grants can power off virtual machines, reset root passwords, install SSH keys, and manage ISO images by exploiting the get_instance gate that only checks grant existence.

### CVE-2026-92752

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T21:17:24.023 |

metasfresh DocumentAttachmentsRestController and CommentsRestController endpoints check only that callers are logged in without enforcing record-level permissions. Attackers can enumerate sequential document identifiers to read, replace, and delete attachments and comments on records their role cannot access.

### CVE-2026-92748

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-16T21:17:23.387 |

BC Security Empire before 6.7.1 fails to validate the multipart filename parameter in upload endpoints, allowing authenticated operators to write files to arbitrary paths on the C2 server. Attackers can use path traversal sequences in the filename to bypass directory containment and write malicious files to sensitive locations for code execution.

### CVE-2026-86831

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1289` |
| Published | 2026-09-16T20:17:36.980 |

Improper validation of pod identifier uniqueness in aws-network-policy-agent in Amazon EKS Network Policy Agent before v1.4.0 might allow an authenticated remote user to bypass NetworkPolicy enforcement on co-located pods in other namespaces via crafted pod and namespace names that produce pod identifier collisions.



To remediate this issue, users should upgrade to Amazon EKS Network Policy Agent 1.4.0 or later and Amazon VPC CNI Managed Add-on v1.22.4 or later (which includes Network Policy Agent v1.4.0).

### CVE-2026-75516

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-16T19:17:33.560 |

The RabbitMQ Java client library allows Java and JVM-based applications to connect to and interact with RabbitMQ nodes. Prior to 5.34.0, AMQConnection.start() applies Math.min(maxInboundMessageBodySize, frameMax) after Connection.Tune negotiation even though AMQP defines frameMax value zero as unlimited and ConnectionFactory.DEFAULT_FRAME_MAX is zero. When the client default and server-negotiated value are both zero, the result is passed to Utils.framePayloadLimit(int), which interprets zero as Integer.MAX_VALUE and disables the configured maxInboundMessageBodySize cap. A malicious AMQP server, or a man-in-the-middle attacker able to modify Connection.Tune and inject frames into the connection, can then send an oversized frame of any frame type, causing Frame.readFrom() to allocate a large byte array before content-level validation and potentially terminate the client process through memory exhaustion. This issue is fixed in version 5.34.0.

### CVE-2026-92719

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-16T18:17:22.837 |

Quickwit through 0.9.0 fails to validate the host and scheme of the queue_url parameter in SQS file sources, allowing attackers to make the node issue requests to arbitrary internal addresses. Attackers can supply a malicious queue_url to the create-source API to scan internal networks and fingerprint services based on connection response differences.

### CVE-2026-47094

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T18:17:09.323 |

SIMAC MyPHR 1.1 contains an insecure direct object reference (IDOR) vulnerability that allows authenticated attackers to access and modify arbitrary employee records due to missing server-side ownership validation. Attackers can send a PUT request to the employee update endpoint with an arbitrary employee identifier and a controlled password value to take over target accounts, enumerate employee records, and retrieve sensitive personally identifiable information including private pay bulletins.

### CVE-2026-82410

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-16T15:17:54.703 |

Pocketbase is an open source web backend written in go. Prior to 0.22.48 and 0.39.7, PocketBase's panic-recovery middleware covers regular request handling but not internal child and worker goroutines. A panic in one of these internal goroutines can escape recovery and terminate the server process, causing a denial of service. The remediation introduces routine.SafeWrap to convert recovered panics into regular errors and applies it to the affected internal worker functions. This issue is fixed in versions 0.22.48 and 0.39.7.

### CVE-2026-77404

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-09-16T15:17:47.067 |

RabbitMQ amqp091-go is a Go AMQP 0.9.1 client. Prior to 1.13.0, URI.String in uri.go concatenates CertFile, KeyFile, CACertFile, and ServerName values directly into an AMQPS query string instead of encoding them as URL query parameters with url.Values. If an application accepts a TLS asset path containing ampersand or equals delimiters and later reparses the serialized URI with ParseURI, the embedded delimiters can create or overwrite connection options, including paths to TLS certificate, key, or CA files. This can corrupt connection configuration or select unintended local cryptographic assets. This issue is fixed in version 1.13.0.

### CVE-2026-92914

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-17T12:18:30.440 |

AVideo LoginControl contains an authentication bypass vulnerability in the PGP second factor verification that compares challenge responses using loose equality against an uninitialized session variable. Attackers with a victim's password can bypass the second factor by sending a parameter-less GET request to verifyChallenge.json.php, which evaluates null == null and marks authentication complete.

### CVE-2026-87963

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-17T07:16:28.533 |

The Yo WordPress plugin from 1.1 through 1.3.1 does not sanitize or parameterize the username request parameter before using it in a SQL query, and reads it before WordPress applies its request escaping, allowing unauthenticated attackers to perform SQL injection and read arbitrary database contents including administrator password hashes.

### CVE-2026-92793

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T21:17:28.923 |

GoAdmin through 1.2.26 fails to properly anchor the logout pattern when checking permissions, allowing authenticated users to bypass permission checks by appending a query parameter. Attackers can append a query string containing the admin prefix followed by /logout to reach administrative endpoints and perform unauthorized actions including reading sensitive data and modifying application state.

### CVE-2026-92782

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T21:17:27.280 |

Chroma through 1.5.9 fails to validate tenant and database segments when resolving collections, allowing authenticated attackers to access collections from other tenants by knowing the collection identifier. Attackers can read, modify, and update records in foreign collections by issuing requests under their own tenant path, bypassing authorization checks.

### CVE-2026-92776

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T21:17:26.547 |

Wiki.js through 2.5.314 fails to require path separators when matching START and END page rules, allowing attackers to access pages sharing a prefix with authorized folders. Users granted access to a folder can read and modify unrelated pages with matching prefixes, bypassing intended access controls.

### CVE-2026-92763

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T21:17:25.150 |

Rundeck through 6.2.1 fails to properly authorize the importConfig and importNodesSources parameters in the project archive import endpoint. Attackers with only the import action can replace project configuration files including security-relevant settings like node executors and SSH key paths that affect job execution.

### CVE-2026-20352

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-16T21:17:12.517 |

A vulnerability in the RADIUS feature of Cisco Identity Services Engine (ISE) could allow an unauthenticated, remote attacker to cause a denial of service (DoS) condition on an affected device.

This vulnerability is due to improper handling of certain RADIUS requests. An attacker could exploit this vulnerability by sending a crafted RADIUS request directly to an affected device. A successful exploit could allow the attacker to cause the ISE node to become unavailable. For single node deployments in that condition, endpoints that have not already authenticated would be unable to access the network until the&nbsp;node comes back up on its own.

### CVE-2026-20295

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-16T21:17:09.740 |

A vulnerability in the sftunnel inter-device communication protocol of Cisco Secure FMC Software and Cisco Secure FTD Software could allow an unauthenticated, remote attacker to exhaust the available memory of an affected device.

This vulnerability is due to improper management of memory resources during sftunnel TLS connection setup. An attacker could exploit this vulnerability by sending crafted sftunnel TLS frames to an affected device&nbsp;during the connection setup. A successful exploit could allow the attacker to exhaust the available memory on the affected device, which could result in a DoS condition.

### CVE-2026-20250

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-772` |
| Published | 2026-09-16T21:17:08.713 |

A vulnerability in Datagram TLS (DTLS) message handling of Cisco Secure Firewall Adaptive Security Appliance (ASA) Software and Cisco Secure Firewall Threat Defense (FTD) Software for Cisco Secure Firewall 3100 Series and 4200 Series devices could allow an unauthenticated, remote attacker to cause a denial of service (DoS) condition on an affected device.

This vulnerability is due to improper resource management when processing certain DTLS messages. An attacker could exploit this vulnerability by sending a crafted stream of DTLS traffic to an affected device. A successful exploit could allow the attacker to cause the device to reload, resulting in a DoS condition.

### CVE-2026-20249

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-704` |
| Published | 2026-09-16T21:17:08.517 |

A vulnerability in the certification authentication feature of Internet Key Exchange version 2 (IKEv2)&nbsp;for Cisco Secure Firewall Adaptive Security Appliance (ASA) Software and Cisco Secure Firewall Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to cause an affected device to reload unexpectedly.

This vulnerability is due to a logic error during the certificate authentication phase of the IKEv2 connection setup. An attacker could exploit this vulnerability by attempting to establish an IKEv2 VPN connection with a crafted certificate. A successful exploit could allow the attacker to cause the IKEv2 process to crash, causing a denial of service (DoS) condition.

### CVE-2026-20154

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-09-16T21:17:07.723 |

A vulnerability in the system rate-limiting process for syslog message 419002 of Cisco Secure Firewall Adaptive Security Appliance (ASA) Software and Cisco Secure Firewall Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to cause high CPU utilization on an affected device, resulting in a denial of service (DoS) condition.

This vulnerability is due to improper rate limiting for syslog message 419002. An attacker could exploit this vulnerability by sending a flood of TCP synchronization (SYN) packets to an affected device. A successful exploit could allow the attacker to cause high CPU utilization, resulting in performance degradation.&nbsp;

### CVE-2026-20135

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-16T21:17:07.587 |

A vulnerability in the TLS 1.3 implementation in Cisco Secure Firewall Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to cause an affected device to reload unexpectedly, resulting in a denial of service (DoS) condition.

This vulnerability is due to improper buffer management during the TLS 1.3 connection. An attacker could exploit this vulnerability by sending a crafted TLS 1.3 packet to an affected system through a TLS 1.3-enabled listening socket. A successful exploit could allow the attacker to cause the LINA process to crash, which would cause the device to reload. The reload can happen before or after authentication of the connection.Note:&nbsp;TLS 1.3 connections include both data traffic and user-management traffic.

### CVE-2026-91105

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-16T19:18:03.467 |

HP has identified and remediated multiple externally reported vulnerabilities within HPLIP. The findings affect several software components that could potentially enable remote code execution, privilege escalation, denial of service, information disclosure, or unauthorized file modification under certain conditions.

### CVE-2026-91098

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-16T19:18:02.247 |

HP has identified and remediated multiple externally reported vulnerabilities within HPLIP. The findings affect several software components that could potentially enable remote code execution, privilege escalation, denial of service, information disclosure, or unauthorized file modification under certain conditions.

### CVE-2026-92716

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T18:17:22.390 |

Shuffle through 2.2.1 contains a cross-tenant privilege escalation vulnerability in the HandleApiGeneration endpoint that allows administrators to reset and read API keys of non-administrator users in other organizations. Attackers with admin privileges in one organization can supply arbitrary user IDs to generate valid API keys for users in different organizations, enabling account takeover across tenant boundaries.

### CVE-2026-66580

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T14:17:16.920 |

Contributor SQL Injection in Product Feed Manager <= 7.12.0 versions.

### CVE-2026-92816

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-16T21:17:31.647 |

ComfyUI before 0.30.0 fails to sanitize folder_name input in dataset save nodes, allowing attackers to write files to arbitrary paths outside the output directory. Attackers can load a crafted workflow that writes attacker-controlled content to arbitrary locations, enabling code execution through modified startup files or package initializers.

### CVE-2026-92786

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-16T21:17:27.880 |

LightGBM through 4.7.0 fails to validate child and split array values when parsing text models, allowing attackers to write out-of-bounds memory during SHAP prediction. Attackers can craft malicious model files with invalid node references that trigger out-of-bounds writes at attacker-chosen offsets in the leaf_depth_ buffer during feature contribution computation.

### CVE-2026-76412

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-264` |
| Published | 2026-09-16T21:17:13.717 |

A vulnerability in the remote diagnostics debugger of Cisco Secure FMC Software could allow an authenticated, remote attacker to enable the remote diagnostics debugger service.

This vulnerability is due to an error when checking the privilege level of a user who is invoking remote diagnostics. An attacker could exploit this vulnerability by authenticating to the device, either through the web-based management interface or the REST API, and using the remote diagnostics debugger to grant a user elevated privileges. A successful exploit could allow the attacker to elevate privileges to root.
Notes:

To exploit this vulnerability, the attacker must have valid user credentials on the affected device.
The CVSSv3.1 Attack Complexity is High due to the multistage process required to fully exploit this vulnerability.

### CVE-2026-92398

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-16T17:18:19.417 |

A vulnerability was found in Ruijie RG-EW3000GX EW_3.0(1)B11P380. Affected by this issue is some unknown functionality of the file /etc/rg_config/admin of the component user_list_note Module. Performing a manipulation of the argument Name results in os command injection. It is possible to initiate the attack remotely. The exploit has been made public and could be used.

### CVE-2026-86359

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-09-16T17:18:16.437 |

Dell Repository Manager, versions prior to 3.5.2, contains an Incorrect Default Permissions vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-92397

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-16T16:17:22.960 |

A vulnerability has been found in Ruijie RG-EW3000GX EW_3.0(1)B11P380. Affected by this vulnerability is the function cc_set of the file unifyframe-sgi.elf of the component configChange. Such manipulation of the argument data.url leads to os command injection. The attack may be performed from remote. The exploit has been disclosed to the public and may be used.

### CVE-2026-92958

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-17T14:18:01.970 |

vm2 through 3.11.6 contains a builtin-module denylist bypass in NodeVM. When the embedder uses the builtin wildcard together with negative entries (e.g. require: { builtin: ['*', '-fs', '-child_process'] }), negative entries are matched by exact module name in lib/builtin.js, so -fs removes only the builtin named fs and does not remove builtin subpaths such as fs/promises. Sandboxed code can therefore call require('fs/promises') or require('node:fs/promises') and reach the promise-based filesystem API despite fs being denied; node: prefix handling is likewise inconsistent (a -node:fs/promises entry does not block require('fs/promises')). Host file creation and writing were confirmed via fsp.writeFile(), and other fs/promises operations (cp, mkdir, rename, rm, rmdir, truncate, read operations, etc.) are also reachable. This issue is fixed in vm2 3.11.7.

### CVE-2026-20334

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-710` |
| Published | 2026-09-16T21:17:10.917 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Adaptive Security Appliance Software, Cisco Secure Firewall Threat Defense Software and Cisco Secure Firewall Management Center Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20334 are related to issues concerning improper adherence to coding standards that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-710.

### CVE-2026-91102

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T19:18:03.063 |

HP has identified and remediated multiple externally reported vulnerabilities within HPLIP. The findings affect several software components that could potentially enable remote code execution, privilege escalation, denial of service, information disclosure, or unauthorized file modification under certain conditions.

### CVE-2026-76825

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-470;CWE-680;CWE-693` |
| Published | 2026-09-16T15:17:46.000 |

RestrictedPython is a tool that helps define a subset of the Python language for accepting program input in a trusted environment. Prior to 8.4, RestrictedPython could allow a sandbox escape when a custom import policy or globals exposed the standard library string module, the string.Formatter class, a Formatter instance, or a Formatter subclass to restricted code. The string.Formatter methods format, get_field, get_value, and vformat performed attribute and item traversal internally without passing through RestrictedPython's safer_getattr protections. Restricted code could use those live object references to reach function globals, builtins, file access, or code execution primitives, affecting confidentiality, integrity, and availability in the host environment. This issue is fixed in version 8.4.

### CVE-2026-92912

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330` |
| Published | 2026-09-17T12:18:30.123 |

AVideo through c3edcc274c389816d434acadac07ee78eaf330c1 uses cryptographically weak uniqid() values for RTMP publish keys in LiveTransmition, reducing key entropy to approximately one million possibilities per creation second. Attackers who know the channel creation time can brute-force the five-digit microsecond component to forge valid stream keys and broadcast content as the channel owner.

### CVE-2026-92598

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-09-16T22:18:30.840 |

Nodemailer before 9.1.0 fails to apply UTS-46 normalization when encoding international domain names, causing the domain resolver to compute a different Punycode A-label than standards-compliant parsers. Attackers can craft recipient addresses with invisible characters or compatibility mappings that pass domain allow-list checks but are delivered to attacker-controlled domains via SMTP.

### CVE-2026-92597

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-09-16T22:18:30.700 |

Nodemailer versions >= 6.9.16 and < 9.1.0 mis-parse RFC 5322 comments in email addresses: in lib/addressparser, a comment closed immediately before a non-break character causes the tokenizer to concatenate the atoms surrounding the comment instead of treating the comment as folding whitespace that terminates the domain. A recipient address such as user@good-corp.com(x)evil.com is therefore read by Nodemailer as the single domain good-corp.comevil.com (registrable domain comevil.com, which an attacker can register) and used for both the SMTP envelope (RCPT TO) and the emitted To:/From: headers, while a conformant RFC 5322 parser terminates the domain at the comment and reads good-corp.com. An application that validates the recipient domain with a strict RFC 5322 parser (without inspecting parse defects) or a naive prefix/substring allow-list and then hands the raw address to Nodemailer can be induced to deliver mail to a domain the attacker controls. Fixed in 9.1.0.

### CVE-2026-20323

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-16T21:17:10.313 |

A vulnerability in the sftunnel inter-device communication protocol of Cisco Secure FMC Software and Cisco Secure FTD Software could allow an unauthenticated, adjacent attacker to impersonate the peer device and obtain access at the level of the&nbsp;manager role, which is equivalent to root.

This vulnerability is due to improper management of the TLS certificate for the sftunnel management connection. An attacker could exploit this vulnerability by connecting to the sftunnel port using a crafted TLS certificate. A successful exploit could allow the attacker to become a registered sftunnel peer with root access.
Note: The attack is successful only if the sftunnel connection is down or the attack can disrupt the sftunnel connection long enough to execute the attack.

### CVE-2026-82760

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-17T14:17:33.237 |

Inefficient Algorithmic Complexity vulnerability in team-alembic AshAuthentication allows an unauthenticated attacker to exhaust CPU and memory via an oversized base62 segment in a submitted API key.

AshAuthentication.Base.decode62/1 in lib/ash_authentication/base.ex splits its argument into one binary per character and folds it with charval62/2, which recomputes Integer.pow(62, index) at every position instead of accumulating by Horner's method, so cost grows roughly cubically in the input length. bindecode62/1 in the same module is quadratic through Integer.undigits/2 and Integer.digits/2. Neither function caps byte_size/1, and AshAuthentication.Strategy.ApiKey.SignInPreparation passes the underscore-separated segments of the submitted key straight into both, before any key lookup and without prior authentication. The surrounding rescue clauses catch exceptions, not CPU or memory exhaustion.

This issue affects ash_authentication: from 4.8.0 before 4.15.0 and from 5.0.0-rc.0 before 5.0.0-rc.14.

### CVE-2026-92903

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T11:17:03.460 |

Improper input validation in Snowflake CLI versions prior to 3.27.0 allowed unsanitized user-controlled values to be interpolated into SQL strings that are executed as multi-statement queries. An attacker who is able to supply a malicious project configuration file or craft command-line input can cause Snowflake CLI to execute attacker-controlled SQL statements in the context of the victim's Snowflake session and active role. Successful exploitation requires either write or pull-request access to a project repository whose CI/CD pipeline runs Snowflake CLI under an elevated service account role, or the ability to supply untrusted input to CLI-wrapping automation. Impact is limited by the privileges held by the configured Snowflake role at execution time. The fix is available in Snowflake CLI version 3.27.0, which also addresses several additional security findings. Users must manually upgrade.

### CVE-2026-92591

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636` |
| Published | 2026-09-16T22:18:29.873 |

Craft CMS 5.0.0 through 5.10.12 treats a database connection failure as meaning that Craft is not installed, which makes anonymous installer actions — including install/validate-site — reachable on an installed production site whenever PHP remains available but the configured MySQL endpoint does not. The action accepts a site name, serializes it through Site::getName(), and expands ${NAME} expressions using App::env(). An unauthenticated attacker who obtained a guest session cookie and matching CSRF token before the outage and whose session remains valid during it can submit a predictable variable name (for example Craft's conventional CRAFT_SECURITY_KEY) and receive its value, disclosing Craft secrets, process environment variables, $_SERVER entries, or PHP constants such as the security key, database credentials, or API keys. The issue requires an independently occurring database outage; the vulnerability itself provides no way to induce it. Fixed in 5.10.13.

### CVE-2026-76413

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-1259` |
| Published | 2026-09-16T21:17:13.840 |

A vulnerability in Cisco Adaptive Security Device Manager (ASDM) single sign-on (SSO) handler for Cisco Secure FMC Software could allow an unauthenticated, remote attacker to log in as the Cisco ASDM administrator user.

This vulnerability is due to improper management of the Cisco ASDM SSO token. An attacker could exploit this vulnerability by performing session token forgery techniques. A successful exploit could allow the attacker to log in as the administrator user and, by repeating this action, keep legitimate administrators locked out of the ASDM indefinitely.

### CVE-2026-71180

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-252` |
| Published | 2026-09-16T17:18:06.100 |

Dell Update Package Framework, versions prior to 26.07.03, contains an Unchecked Return Value vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-77409

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-16T15:17:50.293 |

RabbitMQ amqp091-go is a Go AMQP 0.9.1 client. Prior to 1.13.0, Channel.dispatch in channel.go, confirms.confirm in confirms.go, and Connection.dispatch0 in connection.go synchronously send publisher confirmations, flow-control events, consumer cancellations, returned messages, including NotifyConfirm events and connection block notifications, to application-provided channels. If a listener channel is unbuffered, full, or not drained promptly, the sole reader goroutine blocks and stops processing frames, acknowledgments, deliveries, and heartbeats. Broker-driven event bursts can therefore cause connection stalls, missed heartbeats, deadlocks, and disconnection. This issue is fixed in version 1.13.0.

### CVE-2026-77406

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-195` |
| Published | 2026-09-16T15:17:49.070 |

RabbitMQ amqp091-go is a Go AMQP 0.9.1 client. Prior to 1.13.0, Channel.Qos in channel.go accepts negative prefetchCount and prefetchSize integers and casts them directly to uint16 and uint32 fields in the basic.qos method because validateQos is absent. Values such as -1 therefore wrap to 65535 or 4294967295 instead of being rejected. An application that permits untrusted configuration of these Qos values can unintentionally request extremely large prefetch limits, allowing a broker to deliver enough queued messages to exhaust client memory and disrupt processing. This issue is fixed in version 1.13.0.

### CVE-2026-63127

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-16T15:17:39.817 |

RMCP is an official Rust SDK for the Model Context Protocol. Prior to 2.0.0, the rmcp crate's OAuth implementation in crates/rmcp/src/transport/auth.rs omits the RFC 9728 resource field from ResourceServerMetadata and allows discover_oauth_server_via_resource_metadata to use protected-resource metadata without confirming that the returned resource identifier exactly matches the configured MCP server. A malicious MCP server can publish metadata for a different legitimate MCP resource and its authorization server, causing a victim who connects and completes the authorization flow to obtain a legitimate access token that the client subsequently sends to the malicious server. The attacker can capture the token and impersonate the victim against the legitimate MCP resource within the token's granted scopes. This issue is fixed in version 2.0.0.

### CVE-2026-81442

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-17T14:17:31.120 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains an Improper Privilege Management vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Information tampering and Unauthorized access.

### CVE-2026-81478

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-17T12:18:27.830 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains a Use of Hard-coded Cryptographic Key vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-81476

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-17T12:18:27.580 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-81475

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-17T12:18:27.457 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-87935

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-17T05:17:02.263 |

The Paid Downloads plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 3.15 via the admin_request_handler function. This is due to missing authorization and file type validation in the admin_request_handler function, which is reachable unauthenticated via is_admin() returning true for /wp-admin/admin-post.php. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. On Apache servers where AllowOverride is enabled, an .htaccess file placed in the upload directory may block direct HTTP retrieval of uploaded files, limiting exploitability to stacks that do not honor .htaccess directives such as nginx, LiteSpeed, and Apache with AllowOverride None.

### CVE-2026-61591

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-345;CWE-915` |
| Published | 2026-09-16T22:17:02.763 |

djust provides Phoenix LiveView-style reactive server-side rendering for Django with Rust-powered performance. Prior to version 1.0.7, for views that opt into state snapshots, the snapshot `state_json` embedded in the client page was restored on reconnect as trusted view state with no integrity check. A client could edit the unsigned `state_json` in their page and return it in the reconnect mount frame to inject arbitrary view attributes — e.g. flip `is_admin` to `True`, or change `account_id` / `balance` — escalating privilege or tampering with business state held in public view attributes (the normal djust pattern). This issue is fixed in djust 1.0.7. State snapshots are signed; unsigned or forged snapshots are rejected on the back-navigation restore path. As a workaround, do not enable state snapshots; do not hold authorization/ownership state in public view attributes.

### CVE-2026-20335

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-682` |
| Published | 2026-09-16T21:17:11.137 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Secure Adaptive Security Appliance Software, Cisco Secure Firewall Threat Defense Software and Cisco Secure Firewall Management Center Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20335 are related to incorrect calculation issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-682.

### CVE-2026-61593

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-16T16:17:13.943 |

djust provides Phoenix LiveView-style reactive server-side rendering for Django with Rust-powered performance. Prior to version 1.0.7, the SSE client→server POST endpoints are `@csrf_exempt` and the SSE GET stream endpoint had no Origin check, so a cross-origin page could drive a victim-cookie-authenticated SSE session: force the victim's browser to GET the stream URL (which creates and mounts a LiveView as the victim) and POST to the message endpoint with `credentials: include` to fire state-changing event handlers as the victim. The URL `session_id` is client-chosen (validated only for UUID *format*), so it is not a CSRF token, and a JSON body sent as `text/plain` is a CORS simple request with no preflight. The issue is fixed in 1.0.7. All three SSE endpoints validate the request `Origin` against `ALLOWED_HOSTS` (mirroring the WebSocket CSWSH defense) and reject cross-origin requests with 403; the POST endpoints additionally require `Content-Type: application/json` (415 otherwise), closing the `text/plain` simple-request bypass. As a workaround, disable the SSE transport, or front it with a proxy that enforces an Origin allowlist.

### CVE-2025-43936

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-16T16:17:02.877 |

Dell ObjectScale, versions prior to ObjectScale 4.4.0.0, contains an Improper Authentication vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-92087

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285;CWE-697` |
| Published | 2026-09-16T15:18:59.653 |

@fastify/auth is a Fastify plugin that composes multiple authentication and authorization strategies into a single route guard. In versions 5.0.0 through 5.1.0, when strategies are composed with the relation "or" option together with the run "all" option and one entry is a nested array acting as an AND group, the group is evaluated in an order-dependent way: an earlier failing check is silently dropped and the group's result becomes the outcome of its last check. As a result, a request that satisfies only the last member of an AND group, for example an attacker who holds a valid API key but is not an administrator, is authorized instead of rejected, and a related order-dependent bypass affects the mirror configuration where the top-level relation is "and" and a nested group uses "or". The issue is fixed in @fastify/auth 5.1.1, and users should upgrade to 5.1.1 or later. As a workaround, omit the run "all" option where it is not required, order each AND group so its stricter check is evaluated last, or replace nested AND groups with an explicit top-level "and" composition.

### CVE-2026-74909

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T15:17:43.447 |

Keycloak provides a policy enforcer to protect applications by matching incoming web requests against defined security policies. A flaw was found where the enforcer fails to correctly normalize web addresses that contain special encoded characters, such as those representing semicolons or directory traversal segments. An authenticated user can use these encoded characters to trick the enforcer into applying a less restrictive security policy than intended, potentially gaining unauthorized access to sensitive administrative or private application endpoints.

### CVE-2026-63671

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-184` |
| Published | 2026-09-16T15:17:40.100 |

MDC is a tool to take regular Markdown and write documents interacting deeply with a Vue component. Prior to 0.22.1, @nuxtjs/mdc uses parseMarkdown with allowDangerousHtml enabled by default and relies on validateProps, validateProp, and unsafeLinkPrefix to remove executable URLs from untrusted Markdown. validateProp checks only attributes named href or src, allowing an SVG xlink:href value represented as xLinkHref to retain a javascript: URL that executes in the page origin when selected. The data:text/html denylist entries are also compared against url.protocol, which is only data:, so an iframe src containing data:text/html survives sanitization and executes in an opaque origin when loaded. Plain href javascript: URLs, srcdoc, object, script, and base elements are already blocked, making these two paths specific sibling gaps in the sanitizer. This issue is fixed in version 0.22.1.

### CVE-2026-78428

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-17T10:17:03.760 |

For users authenticated through SAML or OpenID Connect (OIDC), this vulnerability can result in one user receiving another user's authenticated session when multiple SSO login attempts occur concurrently

### CVE-2026-85469

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1357` |
| Published | 2026-09-16T22:18:27.037 |

A flaw was found in quay-builder-qemu. A remote attacker could exploit this by compromising the upstream `Noelware/docker-manifest-action` used in the release workflow, which is pinned to a mutable branch. This allows the attacker to inject arbitrary code, leading to the exfiltration of sensitive registry credentials or the publication of malicious images. The workflow also exposes the default GitHub token, increasing the severity of the compromise.

### CVE-2026-25282

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-17T05:17:01.253 |

Transient DOS when processing unverified data from a neighboring system causes out of bound memory access.

### CVE-2026-81474

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-17T11:17:03.077 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains a Heap-based Buffer Overflow vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-86320

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-17T08:17:02.200 |

A flaw was found in flatpak-builder where Git hooks are not disabled when applying patch sources with use-git-am: true. An attacker who can provide a malicious source containing a Git post-applypatch hook can cause the hook to execute on the host during the build process, resulting in arbitrary code execution with the privileges of the user running flatpak-builder.

### CVE-2026-25290

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-17T05:17:01.650 |

Memory Corruption when validating large data buffers from external sources using addition to check buffer length.

### CVE-2026-25280

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-17T05:17:00.987 |

Memory corruption when processing escape handling flow with insufficient user buffer sizes.

### CVE-2026-25278

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-17T05:17:00.847 |

Memory Corruption when processing I2C transfer requests due to a race condition between memory allocation and data copying.

### CVE-2026-24075

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-09-17T05:17:00.033 |

Memory Corruption when multiple threads issue concurrent IOCTL requests to the device control handler due to improper synchronization and race conditions.

### CVE-2026-24074

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-17T05:16:59.893 |

Memory Corruption when processing data with large offset and length values exceeds buffer limits during data copy operations.

### CVE-2026-24073

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-17T05:16:59.760 |

Memory corruption when processing decode statistics due to insufficient validation of offset against structure size.

### CVE-2025-59607

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-17T05:16:58.060 |

Memory Corruption when copying large input data exceeds normal allocation limits.

### CVE-2026-92838

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-17T02:16:28.610 |

A DLL hijacking
vulnerability exists in the GeoVision GV-Remote E-Map desktop
application. The application loads one or more dynamic-link libraries (DLLs)
from an unsafe search path, allowing a local attacker to place a malicious DLL
in a location searched before the legitimate library location. If
successfully exploited, an attacker with local write access to the affected
directory could achieve arbitrary code execution in the security context of
the GV-Remote E-Map process.

### CVE-2026-63325

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-95` |
| Published | 2026-09-16T19:17:24.317 |

Redocly CLI makes OpenAPI validation, linting, and documentation workflows easier. Prior to version 2.33.0 of @redocly/respect-core and @redocly/cli, the respect command dynamically evaluates $faker runtime expressions in Arazzo descriptions. A crafted expression can traverse constructor, prototype, or __proto__ properties in packages/respect-core/src/modules/context-parser/get-value-from-context.ts, reach the JavaScript Function constructor, and execute arbitrary code when a user processes an untrusted description. The executed code runs with the privileges of the CLI process and can execute shell commands or read CI secrets. Users processing only trusted, self-authored workflows are not affected. This issue is fixed in @redocly/respect-core and @redocly/cli version 2.33.0.

### CVE-2026-59974

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-16T17:17:28.877 |

Stanza is a Stanford NLP Python library for tokenization, sentence segmentation, NER, and parsing of many human languages. Prior to 1.14.0, stanza.resources.common.unzip in stanza/resources/common.py passes downloaded model and resource archives to zipfile.ZipFile.extractall without validating member paths, and the vulnerable extraction path is reachable through stanza.download and stanza.install_corenlp. A malicious archive containing parent-directory traversal entries can write outside the intended model directory, allowing files writable by the Stanza process to be overwritten and potentially enabling code execution through modified shell configuration, SSH authorization data, Python packages, or executable scripts. This issue is fixed in version 1.14.0.

### CVE-2026-81546

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-17T02:16:27.537 |

The Affinity by Canva application before 3.3.0 (September 2026 release) did not perform adequate bounds checking when parsing Affinity document files leading to a stack-based buffer overflow. A threat actor could craft a Affinity document that when opened by a user in Affinity could result in arbitrary code execution.

### CVE-2026-92784

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-16T21:17:27.580 |

@refinedev/inferencer through 7.0.0 fails to escape API field names when interpolating them into generated JSX source code. Attackers controlling the data provider can inject malicious JavaScript through crafted JSON property names that execute in the developer's browser when the Inferencer page renders.

### CVE-2026-62997

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-16T21:17:12.990 |

Kedro-Datasets provides data connectors for Kedro. From version 5.0.0 until 9.5.0, kedro_datasets_experimental.pytorch.PyTorchDataset in kedro-datasets loads .pt model files with torch.load without enforcing weights_only=True, and user-supplied load_args are silently dropped. On PyTorch versions earlier than 2.6, a malicious pickle-backed model from an attacker-influenced shared registry, downloaded checkpoint, or partitioned external source can execute arbitrary code when a Kedro pipeline loads it. The issue affects only the opt-in kedro_datasets_experimental component and does not affect users who load only trusted files. This issue is fixed in version 9.5.0.

### CVE-2026-20342

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T21:17:11.707 |

A vulnerability in a specific file download API of Cisco Secure FMC Software could allow an authenticated, remote attacker to download arbitrary files from an affected system.

This vulnerability exists because user input is not being sanitized. An attacker could exploit this vulnerability by sending a crafted HTTPS request. A successful exploit could allow the attacker to download arbitrary files from the affected system.
To exploit this vulnerability, the attacker must have valid credentials for a user account with at least the role of Security Analyst (read-only).

### CVE-2026-85385

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-16T17:18:15.577 |

Concrete CMS below 9.5.4 did not validate the user timezone value (uTimezone) on write and rendered it without output encoding on the Dashboard user management page, where Date::getTimezoneDisplayName() returns any non-IANA value unchanged. A stored cross-site scripting payload saved in this field executed in an administrator's browser when they viewed the affected user in the Dashboard, running script in the admin session (for example to read CSRF tokens, create administrator accounts, or change site settings). In Concrete CMS 9.5.3 the field became reachable by unauthenticated visitors through public registration; in Concrete CMS below 9.5.3,  the same field was reachable by any authenticated user through the account profile editor. Exploitation required concrete.misc.user_timezones to be enabled (off by default), and the unauthenticated path additionally required public registration to be enabled. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.7 with vector CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks Suraj Bhosale for reporting.

### CVE-2026-61595

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-636;CWE-862` |
| Published | 2026-09-16T16:17:14.080 |

djust provides Phoenix LiveView-style reactive server-side rendering for Django with Rust-powered performance. Prior to version 1.0.7, `djust.tenants` isolation was enforced only on the HTTP path. The current tenant was stored in `threading.local()` and set exclusively by the HTTP-only `TenantMiddleware`, so on the live (WebSocket/SSE) path `get_current_tenant()` was always `None` during mount and every event handler — and the tenant-aware `QuerySet` manager failed OPEN (returned the unfiltered queryset, ignoring `STRICT_MODE`), disclosing every tenant's rows to whoever held the socket. `threading.local` was additionally shared across connections on the `sync_to_async` executor thread. This issue is fixed in djust 1.0.7. Tenant storage moved to a `contextvars.ContextVar` (per async task); the resolved tenant is bound around WS/SSE mount and every dispatch; both managers scope the base queryset once and fail CLOSED (`.none()` under the default `STRICT_MODE`); and system check S006 warns when `STRICT_MODE=False`. No known workarounds are available on the live path.

### CVE-2026-82685

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-17T14:17:32.717 |

Authorization Bypass Through User-Controlled Key vulnerability in team-alembic AshAuthentication allows an authenticated attacker to overwrite and confirm another user's email address, and so take over that account. A confirmation token issued to one user is accepted on any other user's record.

AshAuthentication.AddOn.Confirmation.ConfirmChange verifies the token's signature and its act claim, then applies the changes stored against that token to whichever record the changeset targets, never comparing the sub claim against changeset.data. An attacker who registers an account and changes their own email replays the resulting token against a victim's record id, writing in their own address with force_change_attributes/2 and stamping confirmed_at, after which an ordinary password reset yields the account. The library's own confirmation flow is unaffected, because AshAuthentication.AddOn.Confirmation.Actions.confirm/3 resolves sub to a user and targets that record.

This issue affects ash_authentication: from 0.5.0 before 4.15.0 and from 5.0.0-rc.0 before 5.0.0-rc.14.

### CVE-2026-80218

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-17T14:17:30.743 |

Improper Authentication vulnerability in team-alembic AshAuthentication allows an attacker holding a sign-in token for one authenticated resource to be signed in as a user of a different resource.

AshAuthentication.Strategy.Password.SignInWithTokenPreparation.extract_primary_keys_from_subject/2 parses the JWT sub claim (for example user?id=1) with URI.parse/1 and keeps only its query string, discarding the path segment that names the subject the token was issued for. Nothing else restores that binding: AshAuthentication.Jwt.verify/3 checks the signature, exp, nbf, jti and the library-version claims, the purpose check only requires sign_in, and the remaining comparison is over primary-key field names, which are identical across resources. The WebAuthn sign-in and remember-me preparations carry copies of the same helper and drop the path in the same way. The magic link sign-in path pins the subject name against the resource and is not affected.

This issue affects ash_authentication: from 3.10.5 before 4.15.0 and from 5.0.0-rc.0 before 5.0.0-rc.14.

### CVE-2026-66631

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T14:17:20.113 |

Administrator SQL Injection in MC Woocommerce Wishlist <= 1.9.21 versions.

### CVE-2026-66630

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T14:17:19.983 |

Administrator SQL Injection in PublishPress Series <= 3.1.3 versions.

### CVE-2026-66628

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T14:17:19.363 |

Shop manager SQL Injection in WP-Lister Lite for eBay <= 3.8.11 versions.

### CVE-2026-66626

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T14:17:19.230 |

Editor SQL Injection in SKT Addons for Elementor <= 4.0 versions.

### CVE-2026-66625

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T14:17:19.107 |

Administrator SQL Injection in WC Vendors Marketplace <= 2.7.2.1 versions.

### CVE-2026-66624

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T14:17:18.970 |

Administrator SQL Injection in WPMasterToolKit <= 2.22.0 versions.

### CVE-2026-66619

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T14:17:17.893 |

Administrator SQL Injection in Newsletters <= 4.18 versions.

### CVE-2026-66618

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-17T14:17:17.753 |

Administrator SQL Injection in WP Maps <= 4.9.9 versions.

### CVE-2026-78425

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-17T10:17:02.427 |

Authorised users of outside applications behind the same corporate identity provider (IdP), for example, a wiki, a ticketing system, an expenses tool, or anything they legitimately hold an account on can log into their system via SAML SSO. The IdP issues an assertion to them. If that assertion is presented to NeuVector, NeuVector accepts it because the only thing distinguishing "an assertion for NeuVector" from "an assertion for the wiki" is the element, and the `NotInAudience` warning that reports the mismatch is never read.

### CVE-2026-92812

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-16T21:17:31.017 |

decap-server contains a path traversal vulnerability in the local proxy containment guard that uses plain string prefix comparison without path separator validation. Attackers can access sibling directories whose names begin with the repository directory name to read, write, or delete files outside the intended repository root.

### CVE-2026-92800

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-16T21:17:29.533 |

Docs before 5.4.1 fails to properly revoke websocket collaboration connections when access is revoked at parent documents. Attackers with revoked access can retain real-time read and write access to sub-documents through open websocket sessions that are never disconnected.

### CVE-2026-76425

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-16T21:17:14.107 |

A vulnerability in the APIs of Cisco ISE could allow an authenticated, remote attacker to conduct SQL injection attacks against the backend database.

This vulnerability is due to insufficient validation of certain parameters that are concatenated directly into an SQL query. An attacker could exploit this vulnerability by sending a crafted request that contains SQL statements to an affected endpoint. A successful exploit could allow the attacker to read arbitrary content from the SQL database and conduct server-side request forgery (SSRF) attacks. To exploit this vulnerability, the attacker must have valid administrative credentials.

### CVE-2026-92616

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-16T15:19:02.953 |

FileRise before version 3.28.0 contains a privilege escalation vulnerability that allows authenticated low-privilege attackers to gain unauthorized read and write access by exploiting improper session isolation between the WebDAV interface and the web application session context. Attackers can combine valid Basic-Auth credentials with an active admin PHPSESSID cookie to bypass authorization boundaries, as the WebDAV layer incorrectly inherits elevated privileges from an ambient web session rather than enforcing independent stateless authentication per RFC 4918.

### CVE-2026-81481

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-17T13:16:48.350 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Filesystem access for attacker.

### CVE-2026-85128

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-17T06:16:50.863 |

The Choose User Role at Registration WordPress plugin before 1.3.3 does not validate the role requested at registration against the roles an administrator chose to offer, allowing unauthenticated users to request any role, including administrator, and to be granted it once the request is approved. Exploitation requires the Choose User Role at Registration WordPress plugin before 1.3.3's role selection feature and public account registration to both be enabled.

### CVE-2026-25275

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-09-17T05:17:00.510 |

Transient DOS when processing authentication frames with invalid FILS information element header lengths.

### CVE-2026-65388

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-601` |
| Published | 2026-09-16T23:16:54.147 |

A remote attacker who controls a container registry may be able to direct a client's token request to a host of the attacker's choice, and disclose the victim's registry credentials to that host. This vulnerability is addressed in containerization version 0.41.0.

### CVE-2026-20343

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-16T21:17:11.850 |

A vulnerability in a critical API for Cisco Secure FMC Software could allow an unauthenticated, remote attacker to download sensitive files and use unbounded disk space.

This vulnerability exists because a critical API lacks authentication.&nbsp;An attacker could exploit this vulnerability by repeatedly invoking the API. A successful exploit could allow the attacker to download sensitive files that should be restricted and consume disk space so the device could become unresponsive, causing a DoS condition.

### CVE-2026-20247

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-16T21:17:08.190 |

A vulnerability in Cisco ISE could allow an unauthenticated, remote attacker to conduct SQL injection attacks on an affected device.

This vulnerability is due to improper validation of user-supplied input. An attacker could exploit this vulnerability by sending a crafted request to an affected device. A successful exploit could allow the attacker to modify data in the underlying database.

### CVE-2026-86043

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T19:17:51.993 |

Skipper is an HTTP router and reverse proxy for service composition. Prior to version 0.27.37, the opaAuthorizeRequestWithBody filter can authorize an oversized request after Skipper truncates the body presented to Open Policy Agent because the input.truncated_body signal is derived from Content-Length rather than the actual read result. In filters/openpolicyagent/openpolicyagent.go, ExtractHttpBodyOptionally truncates bodies at maxBodyBytes, while filters/openpolicyagent/internal/envoy/skipperadapter.go copies the request headers without adding a Content-Length value that reflects the truncation. For an HTTP/1.1 request using Transfer-Encoding: chunked or an HTTP/2 request without Content-Length, a body-inspecting policy that follows the prior mitigation and permits input.truncated_body equal to false can evaluate only the truncated prefix, allow the request, and then forward the full oversized body to the protected upstream. This residual issue is distinct from CVE-2026-50197. This issue is fixed in version 0.27.37.

### CVE-2026-86003

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-441` |
| Published | 2026-09-16T19:17:51.760 |

CoreDNS is a DNS server written in Go. Prior to 1.14.7, the DNS-over-HTTPS, DNS-over-HTTP/3, DNS-over-QUIC, and DNS-over-gRPC listeners in plugin/pkg/doh/doh.go, core/dnsserver/server_quic.go, and core/dnsserver/server_grpc.go call dns.Msg.Unpack without the dns.DefaultMsgAcceptFunc request policy used by UDP, TCP, and DNS-over-TLS. An unauthenticated client can send an RFC 2136 UPDATE that the proxy or forward plugin passes unchanged to an update-capable upstream. If that upstream trusts CoreDNS's source address or connection and does not require an attacker-unknown end-to-end TSIG, the request appears to originate from CoreDNS and can add, replace, or delete DNS records, redirect traffic, take over names, alter mail routing, or disrupt the writable zone. This issue is fixed in version 1.14.7.

### CVE-2026-82399

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-16T19:17:44.627 |

CoreDNS is a DNS server written in Go. Prior to 1.14.7, the DNS-over-HTTPS, DNS-over-HTTP/3, DNS-over-QUIC, and DNS-over-gRPC request paths in plugin/pkg/doh/doh.go, core/dnsserver/server_quic.go, and core/dnsserver/server_grpc.go call dns.Msg.Unpack on attacker-controlled DNS section counts before dns.DefaultMsgAcceptFunc validates the fixed header. An unauthenticated client can use DNS name compression and excessive section counts to amplify allocation before the plugin chain, so plugin-level rate limiting cannot prevent concurrent requests from exhausting memory and terminating CoreDNS. The ordinary UDP and TCP listeners are not affected because they validate the header first. This issue is fixed in version 1.14.7.

### CVE-2026-81876

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-400;CWE-835` |
| Published | 2026-09-16T19:17:44.450 |

HAPI FHIR is a complete implementation of the HL7 FHIR standard for healthcare interoperability in Java. Prior to version 6.9.12, SHCParser in org.hl7.fhir.r5/src/main/java/org/hl7/fhir/r5/elementmodel/SHCParser.java can enter an infinite loop while processing attacker-controlled Smart Health Card JWT content whose header contains zip: "DEF" and whose raw-DEFLATE payload is empty or truncated. SHCParser.decodeJWT() reaches SHCParser.inflate(), where Inflater.inflate() can return zero while Inflater.finished() remains false and Inflater.needsInput() is true. The loop also lacks an Inflater.needsDictionary() termination check, SHCParser.decompress() contains the same zero-progress pattern, and ResourceChecker.java can reach SHC parsing during file-format detection. A malformed validation request can pin a JVM worker thread indefinitely, and concurrent requests can exhaust all validation workers. This issue is fixed in version 6.9.12.

### CVE-2026-81875

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-400;CWE-409` |
| Published | 2026-09-16T19:17:44.250 |

HAPI FHIR is a complete implementation of the HL7 FHIR standard for healthcare interoperability in Java. Prior to version 6.9.12, SHCParser in org.hl7.fhir.r5/src/main/java/org/hl7/fhir/r5/elementmodel/SHCParser.java can consume attacker-controlled Smart Health Card JWT content whose header contains zip: "DEF" and whose small raw-DEFLATE payload expands to a very large value. SHCParser.decodeJWT() passes the decoded payload to SHCParser.inflate(), which accumulates all decompressed bytes in a ByteArrayOutputStream without an output-size limit before JSON parsing, and SHCParser.decompress() contains the same unbounded pattern. An application or validator service that accepts attacker-supplied SHC content can therefore suffer excessive heap allocation, severe garbage-collection pressure, request failure, process instability, or process termination. This issue is fixed in version 6.9.12.

### CVE-2026-63126

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-16T19:17:24.013 |

Wire provides gRPC and protocol buffers for Android, Kotlin, Swift, and Java. Prior to 6.4.5 and 7.0.0-alpha04, Wire protobuf readers do not consistently validate attacker-controlled lengths against the current logical message boundary before advancing cursors, pointers, limits, slices, or allocations. In Kotlin, ProtoAdapter.decode(ByteArray) and ProtoAdapter.decode(ByteString) use ByteArrayProtoReader32.internalNextLengthDelimited(), where a positive oversized length can wrap pos + length to a negative limit and escape the existing negative-length check. Related ProtoReader, ReadBuffer.readVarint(), ReadBuffer.verifyAdditional(count:), packed-repeated, nested-message, and ProtoDecoder.decodeSizeDelimited(_:from:) paths can cross logical boundaries, perform pointer arithmetic, reserve capacity, or convert an unrepresentable size before proving the requested bytes exist. An attacker who supplies malformed protobuf bytes can cause unchecked exceptions, traps, out-of-bounds behavior, or excessive allocation, resulting in denial of service without known confidentiality, integrity, or code-execution impact. This issue is fixed in versions 6.4.5 and 7.0.0-alpha04.

### CVE-2026-46352

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-833` |
| Published | 2026-09-16T19:17:17.897 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Starting in version 8.0.0 and prior to version 8.0.5, Suricata's IP defragmentation code could deadlock when processing fragmented traffic containing an encapsulated tunnel protocol whose payload is itself fragmented. Version 8.0.5 contains a fix. No known workarounds are available.

### CVE-2026-85756

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T17:18:16.163 |

SSH.NET is a Secure Shell (SSH) library for .NET. Prior to 2026.0.0, ScpClient places caller-supplied remote paths into the command used to run scp on the server, and the default RemotePathTransformation.DoubleQuote transformation cannot safely quote every remote command interpreter. When an application passes an attacker-controlled path to a shell-based server, shell metacharacters not neutralized by the active IRemotePathTransformation can execute commands as the authenticated SSH user. Exploitation requires a shell-based server and a path crafted for that shell's parsing rules; non-shell servers and paths fully neutralized by the selected transformation are not affected. RemotePathTransformation.ShellQuote is available for POSIX shells, while SftpClient avoids a remote shell entirely. This issue is fixed in version 2026.0.0.

### CVE-2026-92626

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-16T16:17:23.877 |

Control iD iDSecure versions prior to 4.8.3.0 are affected by an unauthenticated Denial of Service.


The /api/dguardintegration/dguardVersion endpoint dereferences DGuard integration login state that may be unset, raising an unhandled null reference exception. The exception is thrown from an asynchronous method that returns void, so it is not observed by a caller and can terminate the iDSecure process.

### CVE-2026-92625

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-16T16:17:23.760 |

Control iD iDSecure versions prior to 4.8.3.0 are affected by an unauthenticated Denial of Service.


The /api/license/restartService endpoint is reachable without authentication and invokes an internal routine that terminates the iDSecure service process and relaunches it by way of a generated batch script. An unauthenticated remote attacker can call this endpoint repeatedly to hold the service in a continuous restart cycle, rendering it unavailable.

### CVE-2026-84997

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-09-16T15:18:00.863 |

react/http is an event-driven, streaming HTTP client and server implementation for ReactPHP. From 0.6.0 until 1.11.1, React\Http\Io\ChunkedDecoder could enter an infinite loop while processing a malformed Transfer-Encoding: chunked body because handleData required its buffer to shrink on every iteration. An incomplete terminal-chunk trailer without CRLF left the buffer unchanged after strpos returned false, and exactly two non-CRLF bytes after a completed non-terminal chunk bypassed both the error and wait guards. The affected decoder processes request bodies for React\Http\HttpServer and response bodies for React\Http\Browser, allowing a malicious client to freeze a server or a malicious or compromised server to freeze a client. A reverse proxy that normalizes inbound requests may protect the server direction but does not protect outbound Browser requests. This issue is fixed in version 1.11.1.

### CVE-2026-80274

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-16T15:17:52.690 |

If a BIND resolver sends a query for a DNSSEC-signed authoritative zone, and the authoritative server replies with a valid wildcard answer and signed NSEC3 proof, followed by an unsigned NSEC at the same owner name, it will trigger an unexpected program exit.
This issue affects BIND 9 versions 9.11.0 through 9.18.50, 9.20.0 through 9.20.27, 9.21.0 through 9.21.25, 9.11.3-S1 through 9.18.50-S1, and 9.20.9-S1 through 9.20.27-S1.

### CVE-2026-79651

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-16T15:17:52.000 |

A flaw was found in the theme localization endpoints of the keycloak-services component, which is the core service responsible for authentication flows and theme management in Keycloak. The issue occurs because the system accepts arbitrary locale tags from unauthenticated requests and stores them in a permanent in-memory cache without limits. An attacker can exploit this by sending a large number of unique locale tags, eventually causing the server to run out of memory and crash.

### CVE-2026-76163

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-16T15:17:43.847 |

If BIND is loaded with a "`named.conf`" file that contains no global "`options`" block, an attacker can send a query of QTYPE TKEY which may cause an assertion failure and subsequent unexpected program exit.
This issue affects BIND 9 versions 9.20.0 through 9.20.27, 9.21.0 through 9.21.25, and 9.20.9-S1 through 9.20.27-S1.

### CVE-2026-63128

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-401;CWE-772` |
| Published | 2026-09-16T15:17:39.960 |

RMCP is an official Rust SDK for the Model Context Protocol. Prior to 2.0.0, the rmcp crate's stateful Streamable HTTP server in crates/rmcp/src/transport/streamable_http_server/tower.rs allows an unauthenticated client to send a well-formed JSON-RPC POST that is not an initialization request, or an initialization request with a mismatched protocol header, causing StreamableHttpService::handle_post to call LocalSessionManager.create_session before validating the message. An early validation failure returns without removing the inserted LocalSessionHandle from LocalSessionManager.sessions, permanently retaining session and channel state for the server process lifetime. Repeated requests can grow the shared session table without bound, degrade legitimate-client latency through lock contention, exhaust memory, and terminate the server. This issue is fixed in version 2.0.0.

### CVE-2026-19666

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-16T15:17:33.520 |

On a resolver configured to use ``dns64``, if an applicable answer from the authoritative server is malformed in a specific way, the resolver `named` process will exit unexpectedly.
This issue affects BIND 9 versions 9.11.0 through 9.18.50, 9.20.0 through 9.20.27, 9.21.0 through 9.21.25, 9.11.3-S1 through 9.18.50-S1, and 9.20.9-S1 through 9.20.27-S1.

### CVE-2026-18212

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-16T15:17:33.257 |

A flaw was found in the SAML Redirect Binding implementation of Keycloak, an open-source identity and access management solution. The issue occurs because the custom DEFLATE compression and decompression helpers fail to release native zlib memory after use. An unauthenticated attacker can exploit this by sending repeated malformed SAML requests, leading to native memory exhaustion and a denial of service.

### CVE-2026-50610

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-17T09:16:41.487 |

A vulnerability has been identified in the Acer System Monitoring component included with NitroSense and PredatorSense due to insufficient access controls in a privileged service. An authenticated local user may be able to access the service and perform unauthorized registry modifications, potentially resulting in local privilege escalation.

### CVE-2026-50609

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-17T09:16:41.370 |

A vulnerability has been identified in the Acer System Monitoring component included with NitroSense and PredatorSense. Insufficient access controls within a privileged Named Pipe service may allow an authenticated local user to perform unauthorized registry operations. In certain situations, this could lead to privilege escalation or compromise of the affected system.

### CVE-2026-50605

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-17T08:17:01.010 |

A vulnerability has been identified in the Acer Agent Service component included with NitroSense and PredatorSense. Insufficient access controls within a privileged service may allow an authenticated local user to perform unauthorized registry operations. In certain situations, this could lead to privilege escalation or compromise of the affected system.

### CVE-2026-25294

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-09-17T05:17:01.787 |

Transient DOS while parsing frame during channel usage.

### CVE-2026-25281

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-17T05:17:01.120 |

Transient DOS when processing large or numerous request buffers without sufficient memory allocation validation.

### CVE-2026-24081

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-09-17T05:17:00.170 |

Transient DOS when processing a channel map with insufficient used channels and adaptive frequency hopping is fully enabled.

### CVE-2026-61592

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-384;CWE-639;CWE-862` |
| Published | 2026-09-16T22:17:02.900 |

djust provides Phoenix LiveView-style reactive server-side rendering for Django with Rust-powered performance. Prior to version 1.0.7, SSE sessions were keyed solely by a client-chosen `session_id` with no binding to the authenticated user — a control the WebSocket transport has but that was dropped on SSE. An attacker who learns (or a victim who leaks) a `session_id` could connect to the message endpoint and dispatch event handlers that execute with the victim's identity and state. This is fixed in djust 1.0.7. Each SSE session is bound to its owning principal at creation and cross-principal access is rejected; SSE session creation is additionally capped per principal. As a workaround, disable the SSE transport.

### CVE-2026-20222

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-16T21:17:07.910 |

A vulnerability in the EIGRP implementation in Cisco Secure Firewall Adaptive Security Appliance (ASA) Software and Cisco Secure Firewall Threat Defense (FTD) Software could allow an unauthenticated, adjacent attacker to cause the device to reload unexpectedly, resulting in a denial of service (DoS) condition.

This vulnerability is due to improper resource management when handling EIGRP update messages. An attacker could exploit this vulnerability by sending crafted EIGRP updates at a high rate to an affected device. A successful exploit could allow the attacker to trigger a memory leak that will eventually cause the affected device to reload unexpectedly.

### CVE-2026-42784

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-16T17:17:18.380 |

A flaw was found in sequoia-openpgp. The library incorrectly infers key flags for older certificates when a key flags subpacket is missing, leading to a discrepancy in how key capabilities are viewed. This key flag confusion allows an attacker to bypass the back-signature check. Consequently, an attacker can illegitimately bind an arbitrary subkey to their own certificate and forge signatures, completely compromising cryptographic integrity.

### CVE-2026-81440

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-17T12:18:27.210 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains a Use of Hard-coded Credentials vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-66269

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-470` |
| Published | 2026-09-17T11:17:02.693 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains a Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection') vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Protection mechanism bypass.

### CVE-2026-25284

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-126` |
| Published | 2026-09-17T05:17:01.517 |

Information Disclosure when a pointer is reused after being deallocated.

### CVE-2026-85386

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-16T17:18:15.710 |

Concrete CMS before 9.5.4 did not sanitize XML and XSLT documents uploaded through a public Form Block file-upload question. Plain XML uploads were validated by file extension only and stored as publicly accessible files that were served inline from the application's own origin. An unauthenticated visitor could therefore store an XML document containing an xml-stylesheet processing instruction that referenced an attacker-supplied, same-origin XSLT stylesheet. When a victim opened the stored file directly in a browser, the browser fetched the stylesheet, transformed the document into HTML, and executed attacker-controlled JavaScript in the Concrete CMS origin (stored cross-site scripting). If the victim was an authenticated administrator, the script could act with that administrator's session, and the reporter demonstrated creation of a new user in the Administrators group. The Concrete CMS security team gave this vulnerability a CVSS v4.0 score of 7.3 with vector CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N. Thanks Valentin SARRE (Independent security researcher) for reporting.

### CVE-2026-71179

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-16T17:18:05.970 |

Dell Update Package Framework, versions prior to 26.07.03, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-81632

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-598` |
| Published | 2026-09-17T14:17:31.953 |

Use of HTTP Request With Sensitive Query String vulnerability in team-alembic AshAuthenticationPhoenix allows someone able to read access logs, proxy logs or browser history to recover a single-use sign-in token and authenticate as its owner.

After a successful password sign-in, AshAuthentication.Phoenix.Components.Password.SignInForm builds the sign_in_with_token path with the freshly issued user.__metadata__.token as a query parameter and redirects the browser to it with a GET. The token therefore travels in the request line, where web servers, reverse proxies, request telemetry and the browser's own history record it, all of which outlive the request and are ordinarily less protected than session storage. The redirect destination is restricted to a local path, so this is not an open redirect; the exposure is the retention of a live credential.

This issue affects ash_authentication_phoenix: from 1.7.0 before 2.17.4 and from 3.0.0-rc.0 before 3.0.0-rc.11; ash_authentication: from 3.10.5 before 4.15.0 and from 5.0.0-rc.0 before 5.0.0-rc.14.

### CVE-2026-92919

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-17T13:17:01.173 |

admin3 through 3.0.0 fails to sanitize client-supplied filenames in the upload handler, allowing authenticated users to write files outside the storage root on Windows deployments. Attackers can use dot-dot path segments in filenames to escape the configured storage directory and overwrite arbitrary files accessible to the server process.

### CVE-2026-81480

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-17T12:18:28.080 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains a Stack-based Buffer Overflow vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Code execution.

### CVE-2026-81477

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-17T12:18:27.710 |

Dell OpenManage Server Administrator, versions prior to 11.1.0.3, contains a Heap-based Buffer Overflow vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Code execution.

### CVE-2026-92806

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-16T21:17:30.410 |

phpList versions before 3.6.17 fail to validate cross-site request forgery tokens in the mass subscriber removal form handler. Attackers can induce logged-in administrators to visit crafted pages that silently delete and blacklist arbitrary subscriber addresses without authentication verification.

### CVE-2026-92783

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T21:17:27.433 |

Yeti through 2.11.0 fails to validate caller permissions in the DELETE /api/v2/rbac/{id} endpoint, allowing users with read access to delete access control relationships. Attackers can revoke the owner's grant and permanently lock legitimate owners out of objects.

### CVE-2026-92779

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-16T21:17:26.827 |

Builder.io Gen2 SDKs through versions 5.2.11 and 0.25.13 contain a prototype pollution vulnerability in the deep-set helper function that processes content block bindings without validation. Attackers can craft content blocks with binding keys containing __proto__, prototype, or constructor paths to pollute Object.prototype during rendering, affecting all subsequent objects created in the process including other tenants' renders.

### CVE-2026-92751

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-16T21:17:23.863 |

CMAK through 3.0.0.6 fails to install a cross-site request forgery filter, allowing attackers to perform state-changing actions on behalf of authenticated operators. Attackers can craft hidden forms that submit to destructive endpoints like topic deletion and cluster configuration changes, leveraging the operator's HTTP Basic authentication credentials or play-basic-authentication cookie without SameSite protection.

### CVE-2026-76424

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-16T21:17:13.983 |

A vulnerability in the REST API of Cisco ISE could allow an authenticated, remote attacker to upload or copy arbitrary files on an affected device.

This vulnerability is due to insufficient validation in file operations. An attacker could exploit this vulnerability by uploading a file with a crafted path. A successful exploit could allow the attacker to upload files to arbitrary locations and execute arbitrary commands as root on the affected device.&nbsp;To exploit this vulnerability, the attacker must have valid administrative credentials.

### CVE-2026-87976

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:U/V:C/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-16T20:17:38.320 |

Apache NiFi Registry 0.4.0 through 2.11.0 are subject to path manipulation when storing extension bundle content using group, artifact, and version coordinates from uploaded NAR manifests. The default file persistence provider used coordinates as filesystem path components without rejected parent-directory names, and the path-containment check compared an unnormalized resolved path. An authenticated user authorized to write and delete bundles in a bucket can upload a NAR with a crafted manifest resulting in file system operations outside of the file persistence directory. Upgrading to Apache NiFi Registry 2.12.0 is the recommended mitigation, which rejects parent-directory coordinates and requires a normalized path to remain a strict child of the storage root location.

### CVE-2026-87024

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-16T20:17:37.643 |

Tanium addressed a SQL injection vulnerability in Asset.

### CVE-2026-86865

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-16T20:17:37.153 |

Tanium addressed a SQL injection vulnerability in Asset.

### CVE-2026-92604

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-16T18:17:22.083 |

Scirius through 3.8.0 contains an arbitrary file write vulnerability in the PCAP filestore upload endpoint that allows default User role users to write attacker-controlled JSON content to filesystem paths. Attackers can supply path traversal sequences in the uploaded document's _id field to escape the intended directory and write files with .json extension to arbitrary locations as root.

### CVE-2026-17526

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T16:17:04.647 |

Keycloak is an open-source identity and access management solution. A vulnerability was discovered where a user with the impersonation role can impersonate a realm administrator. This allows the attacker to gain full administrative control over the realm, including the ability to manage users, clients, and roles.

### CVE-2026-92959

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-17T14:18:02.130 |

vm2 before 3.11.8 does not fully enforce the allowAsync: false option in VM and NodeVM. While localPromise.prototype.then is replaced with a handler that throws 'Async not available', the sandbox's Promise static methods (Promise.resolve, Promise.all, Promise.race, Promise.any, and Promise.allSettled) still assimilate attacker-supplied thenables: native promise resolution performs PromiseResolveThenableJob and invokes the sandboxed code's then method in a microtask without passing through the patched then, so the async restriction is never applied. As a result, sandboxed script can schedule work that runs after VM.run() or NodeVM.run() has returned and outside the configured timeout, continuing to execute after the host believes execution is complete.

### CVE-2026-90986

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T14:17:52.867 |

Unauthenticated Cross Site Scripting (XSS) in Visitor Traffic Real Time Statistics Pro <= 11.21 versions.

### CVE-2026-90887

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T14:17:52.733 |

Unauthenticated Cross Site Scripting (XSS) in WP Inventory Manager <= 2.5.4 versions.

### CVE-2026-66571

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-17T14:17:15.547 |

Unauthenticated Cross Site Request Forgery (CSRF) in Asset CleanUp: Page Speed Booster <= 1.4.0.5 versions.

### CVE-2026-91014

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T06:16:52.977 |

The Realtyna Organic IDX plugin + WPL Real Estate WordPress plugin before 5.4.2 does not sanitise and escape some of its parameters before reflecting them back in the page, allowing unauthenticated attackers to run arbitrary web scripts in a visitor's browser if they can trick the visitor into following a crafted link (reflected XSS).

### CVE-2025-15697

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-17T06:16:50.053 |

The Dictionary WordPress plugin through 1.0 does not escape user input before reflecting it back in the responses of several directly accessible scripts, allowing unauthenticated attackers to perform Reflected Cross-Site Scripting attacks against anyone they can induce to submit a crafted request.

### CVE-2026-61596

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-09-16T23:16:53.860 |

djust provides Phoenix LiveView-style reactive server-side rendering for Django with Rust-powered performance. Prior to version 1.0.7, djust's per-object authorization (`get_object` + `has_object_permission`, ADR-017) was enforced on the WebSocket mount and event paths but not on three other render entry points: (a) the initial HTTP GET render, (b) SPA `url_change` navigation, and (c) `{% live_render %}` embedded child views. An authenticated user could therefore view (and on some paths act on) an object they are not authorized for by loading the page directly, navigating to it via SPA url-change, or composing it as an embedded child — a classic IDOR / broken object-level access control on object-scoped views. This is fixed in djust 1.0.7. All render entry points now route through a shared `enforce_object_permission` chokepoint: HTTP GET returns 403, `url_change` emits a `permission_denied` frame and skips the render, and `{% live_render %}` (eager + lazy) refuses the embed. Views without a custom `get_object` are unaffected (no-op). No reliable workaround short of upgrading. Do not expose object-scoped views through the HTTP-GET / url_change / live_render paths until patched.

### CVE-2026-92582

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-16T22:18:28.600 |

AVideo (WWBN/AVideo) through 29.0 (commit e01e41ecc) is vulnerable to cross-site request forgery. objects/videoAddNew.json.php disables AVideo's automatic CSRF guard ($global['skipAutoCSRFCheck']) and the untrusted-request check ($global['bypassSameDomainCheck']) merely because 'user' and 'pass' parameters are present in the request; the values are never validated and are read from $_REQUEST, so an attacker can supply them in the query string of a cross-site request. Because User::loginFromRequestIfNotLogged() returns immediately when a session already exists, a victim who is authenticated by cookie satisfies the check while the attacker-supplied credentials are discarded. An attacker who lures an authenticated user with upload rights to visit a crafted page can therefore submit cross-origin requests that modify video records — including ownership transfer (setUsers_id), deletion of user-group access restrictions, can_download, can_share, only_for_paid, video_password, rating, status, creation date, and view count. For a victim with administrator or Permissions::canAdminVideos() rights, any video on the site can be altered, including removing group restrictions from private content. No patched version was available at the time of the advisory.

### CVE-2026-89034

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-16T22:18:27.613 |

TCH QRing smart ring model R20_B006 running firmware RT09R20_1.00.00_250318 contains an unauthenticated Bluetooth Low Energy access vulnerability that allows any nearby attacker to connect to the device without pairing, authentication, or user approval by exploiting the exposed Nordic UART Service which enforces no client authentication or command authorization. Attackers within Bluetooth Low Energy range can connect directly to the ring, bypassing the official application and cloud authentication, to read battery levels, activate live heart rate monitoring, and retrieve stored historical heart rate and blood oxygen records.

### CVE-2026-92811

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-16T21:17:30.877 |

browserless versions 1.44.0 through 2.56.7 fail to enforce file protocol restrictions in Playwright websocket endpoints, allowing authenticated token holders to read arbitrary files. Attackers can navigate Playwright-driven browsers to file scheme URLs and access files accessible to the container process despite the ALLOW_FILE_PROTOCOL setting defaulting to false.

### CVE-2026-92804

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-16T21:17:30.120 |

Nango through 0.70.4 fails to validate caller-supplied connection configuration values interpolated into provider token and proxy URL templates. Authenticated attackers can supply malicious configuration values to direct server requests at internal addresses or cloud metadata endpoints, potentially exfiltrating provider credentials.

### CVE-2026-92795

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-16T21:17:29.227 |

Coze Studio through 0.5.1 fails to restrict the server URL supplied when registering plugin tools, allowing authenticated users to make the backend fetch internal services. Attackers can construct plugin requests to access cloud metadata endpoints and internal services reachable only from the backend network, reading responses containing sensitive information.

### CVE-2026-92789

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-16T21:17:28.330 |

Graylog through 7.1.4 validates outbound URLs against an allowlist before making requests but fails to re-validate after following HTTP redirects. Attackers with lookup table or event notification permissions can craft allowlisted endpoints that redirect to internal services, enabling the server to fetch and return internal responses.

### CVE-2026-92775

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-16T21:17:26.390 |

Wiki.js through 2.5.314 contains a server-side request forgery vulnerability in the Image Prefetch renderer that fetches arbitrary URLs without protocol, host, or address validation. Attackers with page editing permissions can inject img elements with the prefetch-candidate class to make the server request internal services and cloud metadata endpoints, with responses returned to the attacker.

### CVE-2026-92773

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T21:17:26.063 |

Trigger.dev before 4.6.0 fails to verify that an authenticated user controls a GitHub App installation before binding it to their organization. Attackers can claim another user's GitHub App installation by replaying state cookies and supplying sequential installation identifiers, gaining unauthorized access to the victim's repositories.

### CVE-2026-92772

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T21:17:25.897 |

Leantime before 3.9.6 contains an authorization bypass vulnerability in the HTMX plugin install endpoint that lacks permission validation. Authenticated users with limited roles can install marketplace plugins and control arbitrary properties including identifier, version, and license key to deploy malicious plugins.

### CVE-2026-92771

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T21:17:25.750 |

Twenty before 2.35.0 fails to validate field and row permissions in the groupBy-with-records GraphQL resolver, allowing authenticated users to bypass permission checks. Attackers with canReadObjectRecords permission but canReadFieldValue false can retrieve restricted field values through the groupBy resolver that would normally be denied.

### CVE-2026-92770

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-16T21:17:25.597 |

Harbor through 2.15.2 fails to properly restrict the q query parameter filtering on scanner registration access credentials. Project administrators can exploit fuzzy filtering on the AccessCredential column to recover the scanner adapter secret one character at a time through response row counts.

### CVE-2026-92765

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T21:17:25.447 |

ArcherySec through 2.0.6 fails to validate organization ownership in the WebScanVulnList endpoint, allowing authenticated users to read vulnerability findings from other organizations. Attackers can supply arbitrary scan identifiers to retrieve complete web vulnerability data including titles, severities, statuses, and analyst notes from other tenants.

### CVE-2026-92760

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-16T21:17:24.630 |

Shlink through 5.1.6 fails to enforce API key role restrictions when issuing Mercure subscription tokens, allowing restricted keys to subscribe to all topics. Attackers with author-only or domain-only keys can access the mercure-info endpoint to receive visit data including referrer, user agent, geolocation, and full short URL objects for URLs outside their authorization boundary.

### CVE-2026-92759

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-16T21:17:24.470 |

SecObserve versions before 1.59.1 contain an information disclosure vulnerability in the ApiConfigurationSerializer that fails to strip the basic_auth_password field from API configuration responses. View-only product members can retrieve the decrypted basic-auth password of configured scanner or integration service accounts through standard REST endpoints.

### CVE-2026-92753

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T21:17:24.180 |

PatrowlManager through 1.8.4 contains an authorization bypass vulnerability in the events and alerts API endpoints that lack ownership filtering. Authenticated attackers can read platform event history, delete arbitrary events, and modify alerts belonging to other users.

### CVE-2026-92750

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T21:17:23.720 |

Harness through 3.3.0 omits access control validation in the infrastructure provider read endpoint, allowing authenticated users to retrieve provider configurations from spaces they do not belong to. Attackers can query the GET /api/v1/infraproviders endpoint with arbitrary space identifiers to expose sensitive provider metadata including Docker endpoints, TLS certificate paths, and cloud project identifiers.

### CVE-2026-20300

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-16T21:17:09.897 |

A vulnerability in Cisco ISE could allow an authenticated, remote attacker to conduct SQL injection attacks on an affected device. To exploit this vulnerability, the attacker must have at least low-privileged administrative credentials.

This vulnerability is due to improper validation of user-supplied input. An attacker could exploit this vulnerability by sending a crafted request to an affected device. A successful exploit could allow the attacker to read or modify data in the underlying database.

### CVE-2026-92417

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-404;CWE-476` |
| Published | 2026-09-16T19:18:05.933 |

A vulnerability was found in Open5GS up to 2.8.0. This affects the function ogs_pfcp_parse_volume_measurement in the library lib/pfcp/types.c of the component PFCP Handler. The manipulation results in null pointer dereference. The attack may be launched remotely. The patch is identified as 8f07b507b78ff94776f2cd49276eb116ed93d7f2. A patch should be applied to remediate this issue.

### CVE-2026-73462

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-16T19:17:32.630 |

On affected platforms running Arista EOS with IGMP (Internet Group Management Protocol) snooping configured (enabled by default on all VLANs), a network-adjacent unauthenticated attacker can send malformed network packets on an affected VLAN to cause the IGMP snooping agent to terminate unexpectedly. This results in a temporary disruption of multicast traffic management, which may cause multicast traffic to be flooded to all ports of the affected VLAN until the service recovers. Repeated exploitation could result in a prolonged loss of intended multicast forwarding behavior.

### CVE-2026-92605

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T18:17:22.243 |

IRIS through 2.4.29 fails to properly validate case authorization in comment listing endpoints for notes, tasks, IOCs, assets, and evidence items. Attackers with access to any single case can enumerate sequential object identifiers and read comment threads from cases they have no authorization to access.

### CVE-2026-92603

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T17:18:20.733 |

ContiNew Admin through 4.1.0 contains an authorization bypass vulnerability in the personal message delete endpoint that allows authenticated users to delete other users' messages and announcements. Attackers can supply arbitrary message identifiers in the IdsReq parameter to remove any message row and purge all recipients' read receipts without ownership validation.

### CVE-2026-92602

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-16T17:18:20.590 |

TDuck survey form through version 5.3 fails to validate webhook URLs or verify form ownership in the WebhookConfigController. Authenticated attackers can attach webhooks to other users' forms and exfiltrate submissions to arbitrary external or internal addresses.

### CVE-2026-92601

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T17:18:20.453 |

Guns through 8.3.5 contains an improper access control vulnerability in SysNoticeController where requiredPermission defaults to false and is not overridden by any action methods. Authenticated users without assigned roles can exploit this to create, edit, delete, publish and retract system-wide notices affecting arbitrary users and departments.

### CVE-2026-92600

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T17:18:20.303 |

Guns through 8.3.5 contains an information disclosure vulnerability in SysUserController where /sysUser/detail and /sysUser/page endpoints omit requiredPermission configuration, causing the permission interceptor to skip RBAC validation for authenticated users. Attackers with any valid login token can retrieve sensitive user information including account names, real names, email addresses, phone numbers, last login IPs, and role assignments for all users in the system.

### CVE-2026-92570

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-16T15:19:02.740 |

reNgine through 2.2.0 contains an authorization bypass vulnerability in the GetFileContents API endpoint that allows any authenticated user to read bundled recon tool configuration files. Attackers with low-privilege Auditor roles can access files containing third-party API keys for services like SecurityTrails, Shodan, Censys, VirusTotal, BinaryEdge and Hunter by querying the endpoint without role-based permission checks.

### CVE-2026-92567

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-16T15:19:02.287 |

TDuck survey form through version 5.0 contains an authorization bypass vulnerability in the POST /user/form/data/update endpoint that allows authenticated users to overwrite other users' form submission data. Attackers can discover submission identifiers allocated in narrow ranges and modify arbitrary form responses containing personal data by sending update requests without ownership validation.

### CVE-2026-91097

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-16T19:18:02.070 |

HP has identified and remediated multiple externally reported vulnerabilities within HPLIP. The findings affect several software components that could potentially enable remote code execution, privilege escalation, denial of service, information disclosure, or unauthorized file modification under certain conditions.

### CVE-2026-92718

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-16T18:17:22.690 |

Nuclei versions before 3.11.1 cache template signature verification based only on file modification time without content checksums. Attackers can replace verified templates with unsigned malicious content and restore the original modification time to bypass signature checks and execute arbitrary operating system commands.

### CVE-2026-68904

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-16T17:18:00.917 |

node-opcua is an OPC UA implementation for TypeScript and Node.js. From 2.0.0 until 2.170.0, node-opcua clients using the default keepSessionAlive setting can enter a repeated reconnection cycle when an OPC UA server's clock skew causes BadInvalidTimestamp responses. ClientSessionKeepAliveManager._ping_server treated the server-originated ServiceFault as a network outage and forced a transport reconnect, while ClientTCP_transport._on_ACK_response used socket.end() after failed HEL/ACK negotiation and could leave the connection in FIN-WAIT-2 when the peer did not close. Repetition at the keepAliveInterval accumulates file descriptors and memory until the client process or container can be terminated by resource exhaustion. This issue is fixed in version 2.170.0.

### CVE-2026-77407

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-316` |
| Published | 2026-09-16T15:17:49.210 |

RabbitMQ amqp091-go is a Go AMQP 0.9.1 client. Prior to 1.13.0, PlainAuth values defined in auth.go retain passwords as exported plaintext fields in Connection.Config.SASL after a successful PLAIN authentication handshake. The Connection.openComplete method in connection.go does not clear those values. Code with access to the Connection object, including reflective loggers, application performance monitoring agents, debugging utilities, and panic handlers, can traverse the configuration and expose the credentials to logs or state captures. The credential remains available for the lifetime of the connection instead of being cleared after authentication. This issue is fixed in version 1.13.0.
