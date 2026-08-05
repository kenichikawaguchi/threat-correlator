# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-05 15:00 UTC
- **対象期間**: `2026-08-04T15:00:18.000Z` 〜 `2026-08-05T15:00:32.000Z`
- **重要CVE数**: 220 件（Critical 9.0+: 58 件 / High 7.0〜: 162 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上り、特に **リモートから認証不要でコード実行が可能** な脆弱性が目立ちます。  
- **IoT/組み込み系**（OpenPLC、rust‑iot‑platform、nanoMODBUS など）と **クラウド/コンテナ管理系**（Red Hat ACM、Flowise、HPE SD‑WAN）で高リスクが集中。  
- 多くは **入力検証不備**、**認証・認可の抜け**、**バッファオーバーフロー** といった古典的な欠陥で、攻撃者は単一のリクエストで完全な権限取得やサービス停止が可能です。  
- 2026 年は **LLM（Large Language Model）プラットフォーム**（Flowise）に対するコードインジェクション系脆弱性が多数報告され、AI アプリケーションのサプライチェーンリスクが顕在化しています。

---

## 2. 特に注目すべき CVE  

| CVE ID | スコア | 主な影響 | 注目理由 |
|--------|--------|----------|----------|
| **CVE‑2026‑64633** | 10.0 | エージェントホスト上で **リモート無認証コード実行** が可能 | **最高スコア** かつ「ネットワーク経由で直接シェル取得」できる点が危険。攻撃者は任意のバイナリを実行し、内部ネットワーク全体に横展開できる。 |
| **CVE‑2026‑71268** | 9.9 | OpenPLC Runtime v3 の `compile_program()` が **任意ファイル書き込み** を許す | 産業制御系（PLC）に直接影響し、PLC のファームウェア改ざんや制御ロジックの書き換えが可能。IoT/OT の境界が曖昧な環境で特に危険。 |
| **CVE‑2026‑10090** | 9.9 | Red Hat Advanced Cluster Management for Kubernetes の **Channel リソース作成権限のエスカレーション** | 名前空間レベルの「edit」権限だけで、任意の Helm リポジトリを指す Channel を作成でき、**クラスタ全体のコード実行** が可能。K8s 環境の権限分離が崩壊する典型例。 |
| **CVE‑2026‑71289** | 9.8 | NASA‑AMMOS ANMS のデフォルト `docker‑compose.yml` が **ホストネットワーク公開 + 高権限 CAP** を付与 | コンテナが直接ホストネットワークに露出し、`NET_ADMIN` 等の特権で **ネットワーク設定改ざん・横移動** が可能。デフォルト設定のまま本番環境にデプロイすると即リスク。 |
| **CVE‑2026‑71278** | 9.8 | rust‑iot‑platform の `calc‑rule` 作成 API が **認証無し** で利用可能 | 任意のスクリプトが保存され、後続リクエストで **サーバ側コード実行** が実現。IoT デバイス管理サーバの根幹に関わるため、認証欠如は致命的。 |

> **共通点**：すべて「認証・入力検証の欠如」か「特権設定のデフォルト公開」に起因し、**外部から直接コード実行** が可能になる点です。特に産業制御・クラウド管理・AI 開発環境は攻撃対象が広範囲になるため、早急な対策が必須です。

---

## 3. 推奨アクション  

### 3.1 パッケージ・コンポーネントのアップデート
| 製品 / ライブラリ | 現行バージョン (脆弱) | 推奨バージョン | 備考 |
|-------------------|----------------------|----------------|------|
| **OpenPLC Runtime** | ≤ 3.0.0 | ≥ 3.1.2 (CVE‑2026‑71268 修正) | `compile_program()` のパス正規化とサンドボックス化が追加 |
| **Red Hat Advanced Cluster Management (ACM)** | 2.7.x 以前 | ≥ 2.8.4 (CVE‑2026‑10090 修正) | Channel 作成時の RBAC 強化、Helm リポジトリ検証ロジック追加 |
| **NASA‑AMMOS ANMS** (docker‑compose) | デフォルト `docker‑compose.yml` | カスタム `docker‑compose.yml` で **host ネットワーク削除**、`cap_add` を **削除または最小化** | 可能なら `network_mode: bridge` に変更し、必要最小限の CAP だけ付与 |
| **rust‑iot‑platform** | 0.9.3 以前 | ≥ 0.9.5 (CVE‑2026‑71278 修正) | `calc‑rule` エンドポイントに認証ミドルウェアを必須化 |
| **microtar** | 1.0.0 以前 | ≥ 1.0.3 (CVE‑2026‑71267 修正) | `mtar_write_*_header()` で長さチェックを実装 |
| **nanoMODBUS** | ≤ 1.23.0 | ≥ 1.24.1 (CVE‑2026‑71256 / 71254 修正) | バッファ境界チェックとスタック保護を追加 |
| **Flowise** | < 3.1.3 | ≥ 3.1.3 (全 CVE‑2026‑704xx 系修正) | Python/JS バリデータ強化、Unicode 正規化、NodeVM 設定のデフォルトロックダウン |
| **OpenSIPS** | ≤ 4.0.0 | ≥ 4.1.0 (CVE‑2026‑45538 修正) | ヘッダー長チェックとスタック保護を実装 |
| **Veeam Service Provider Console** | 12.0.x 以前 | ≥ 12.1.2 (CVE‑2026‑58073 修正) | エージェント認証トークンの署名検証を必須化 |

> **※ バージョンは執筆時点の最新情報です。各ベンダーのリリースノートを必ず確認してください。**

### 3.2 設定・運用上の緊急対策
1. **ネットワーク分離**  
   - ANMS、OpenPLC、rust‑iot‑platform などの IoT/OT コンポーネントは **管理ネットワークと分離** し、外部からの直接アクセスを防止。  
   - 必要に応じて **ファイアウォールで IP 制限**（例：管理サーバからのみ 8089/tcp へ）を適用。

2. **認証・認可の強化**  
   - `calc‑rule` API、Flowise の REST エンドポイント、OpenSIPS の管理画面は **必ず Basic/Auth Token + MFA** を導入。  
   - Red Hat ACM の Namespace RBAC を見直し、`edit` 権限だけ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-64633

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-04T17:16:58.227 |

A vulnerability allowing remote unauthenticated code execution on the agent host.

### CVE-2026-71268

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-05T13:24:51.083 |

OpenPLC Runtime v3's compile_program() function (webserver/openplc.py) parses `(*FILE:path content*)` directives from uploaded Structured Text (.st) program files and writes the referenced content to `os.path.join('./core', file_path)` with no validation that file_path stays within the ./core directory. A crafted .st file containing a directive such as `(*FILE:../../../etc/cron.d/x * * * * root <command>*)` writes attacker-controlled content to an arbitrary filesystem path, enabling remote code execution (e.g. via cron or SSH authorized_keys). A path-validation function, validate_file_path(), exists elsewhere in the codebase (webserver/credentials.py) but is never invoked from compile_program(), leaving the sink unprotected. OpenPLC additionally ships with hardcoded default credentials (openplc:openplc), lowering the practical bar for exploitation.

### CVE-2026-10090

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-267` |
| Published | 2026-08-05T09:18:14.667 |

A flaw was found in the Application Subscription controller (multicluster-operators-subscription) of Red Hat Advanced Cluster Management for Kubernetes (ACM). A user with namespace-scoped "edit" privileges in an ACM hub namespace can create a Channel resource pointing to a Helm repository they control and a Subscription resource referencing it. The app-subscription controller fetches and applies the Helm chart contents with its own elevated authority, without verifying whether the subscription creator holds the "open-cluster-management:subscription-admin" role and without restricting applied resources to the subscription namespace. This allows the attacker to include cluster-scoped resources in the Helm chart, such as a ClusterRoleBinding granting the attacker's ServiceAccount the "cluster-admin" ClusterRole. Successful exploitation results in full cluster-admin privilege escalation. This contradicts the ACM documentation which states that non-subscription-admin users should have resources deployed into the subscription namespace only.

### CVE-2026-71289

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-05T13:24:53.703 |

The NASA-AMMOS Asynchronous Network Management System (ANMS) reference implementation's default docker-compose.yml publishes the amp-manager service's REST API directly to the host network interface (port 8089, e.g. "${ION_MGR_PORT:-8089}:8089/tcp") with cap_add: NET_ADMIN, NET_RAW, SYS_NICE, bypassing the CAM (Configuration and Access Manager) gateway that is otherwise the system's sole authentication boundary. The underlying REST server, implemented with CivetWeb in JHUAPL/dtnma-tools (src/refdm/nm_rest.c), is configured with enable_auth_domain_check set to "no" and registers every route, including the DTNMA agent command-dispatch endpoints (.../agents/{eid|idx}/send, which accept and forward EXECSET-encoded command sets to a registered DTNMA agent), with a null authentication callback. Any network-reachable client can therefore enumerate registered agents, submit arbitrary command sets to them, and clear stored reports, entirely without credentials. This affects NASA-AMMOS/anms and JHUAPL-DTNMA/dtnma-tools as published; both repositories present this as a reference/ground DTN network-management implementation and testbed, and the affected components communicate with DTNMA agents (which may represent simulated or real spacecraft/ground nodes depending on deployment) rather than being flight software running onboard a spacecraft.

### CVE-2026-71278

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-05T13:24:52.320 |

rust-iot-platform allows creating a "calc rule" via POST /calc-rule/create (api/src/controller/calc_rule_router.rs) containing an arbitrary `script` field. This route does not take the AuthToken request guard used elsewhere in the application, making it reachable without authentication. The stored script is subsequently executed via quick_js::Context::eval() in api/src/biz/calc_run_biz.rs with no sandboxing, allowing an unauthenticated attacker to achieve arbitrary JavaScript execution in the server process by creating and triggering a malicious calc rule.

### CVE-2026-71267

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-05T13:24:50.963 |

microtar's mtar_write_file_header() and mtar_write_dir_header() functions (src/microtar.c) copy a caller-supplied entry name into the 100-byte `name` field of a stack-allocated mtar_header_t via strcpy(h.name, name), with no check that strlen(name) is less than 100 before the copy. Any application that calls these functions with an externally-influenced filename longer than 99 characters (e.g. when archiving user-supplied or attacker-controlled filenames) triggers a stack buffer overflow.

### CVE-2026-71262

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-05T13:24:50.357 |

IoTSharp BlobStorageController.cs lacks the [Authorize] attribute applied to every other controller in the application (DevicesController, CustomersController, TenantsController, etc.), and no global authorization FallbackPolicy is configured in Startup.cs, leaving its Upload/Download/List/Modify/Delete endpoints reachable by unauthenticated remote attackers. The path/filename parameters passed to these endpoints (e.g. `_blob.WriteFileAsync($"{path}/{formFile.FileName}", ...)`) are used without sanitization, enabling path traversal that allows writing, reading, modifying, and deleting arbitrary files outside the intended blob storage directory, including web-accessible paths that can be leveraged for remote code execution via webshell upload.

### CVE-2026-71256

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-05T12:18:57.847 |

nanoMODBUS through v1.23.0 contains an out-of-bounds stack read leading to a wild-pointer write in nmbs_read_device_identification_basic() / recv_read_device_identification_res() in nanomodbus.c. A fixed 3-element stack array order[3] = {0,1,2} maps object IDs to buffer indices. The server-supplied object_id field (0-255, read directly from the wire) is used without any bounds check as buf_index = order[object_id]. When a malicious Modbus server sends a Read Device Identification response with object_id >= 3, this reads an out-of-bounds/garbage byte from the stack adjacent to order[], which is then used as an index into a 3-element buffers[] array of char* pointers. The resulting wild pointer is passed to strncpy() as the destination, causing an arbitrary-address write with server-controlled data.

### CVE-2026-71254

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-05T12:18:57.600 |

nanoMODBUS through v1.23.0 contains an out-of-bounds write in the Modbus server-side handle_read_file_record() function (FC 0x14, Read File Record) in nanomodbus.c. The function validates that the total request size does not exceed 245 bytes and that each sub-request's record_length is at most 124, but it never validates the CUMULATIVE response size across all sub-requests before processing them. The accumulator response_data_size is declared as uint8_t and is incremented by 2 + record_length*2 for each of up to 35 sub-requests; with 35 sub-requests of record_length=124, the cumulative demand is 8750 bytes, which overflows the uint8_t accumulator. A subsequent loop then calls get_n(), an internal function with no bounds checking, once per sub-request to obtain a pointer into the 260-byte msg.buf receive buffer and advances the internal buf_idx by up to 248 bytes per call; swap_regs() then writes to that pointer unconditionally. A single crafted FC 0x14 request from an unauthenticated network client can cause up to ~8490 bytes to be written out of bounds past the 260-byte buffer, corrupting adjacent memory in the server process and leading to denial of service or potential remote code execution, particularly on embedded/bare-metal targets without memory protection.

### CVE-2026-71248

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T11:16:27.863 |

Inventory-Management-System-PHP's login.php constructs its authentication query via direct string concatenation of raw POST parameters: $sql = "select * from user where email = '$email' and password = '$password'", with no escaping or parameterization, allowing authentication bypass via a payload such as email=' OR 1=1 LIMIT 1-- -. Separately, delete.php executes mysqli_query($db, "DELETE FROM product WHERE product_id=" . $_GET['id']) with no authentication check and no validation of the id parameter, allowing an unauthenticated attacker to delete arbitrary product rows or perform blind SQL injection via payloads such as id=0 OR SLEEP(5).

### CVE-2026-71237

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T11:16:26.503 |

Miantang/IoT-PHP's index.php implements a POST /userlogin route that reads the password directly from $_POST['pwd'] with no sanitization and concatenates it into a raw SQL string: mysql_query("select * from userlists where username='$username' and password='$password' limit 1"). The username value is passed through htmlspecialchars(), which does not encode single quotes by default and therefore does not prevent SQL injection through the password field. An unauthenticated attacker can submit a payload such as pwd=' OR '1'='1 to bypass authentication and, via UNION-based injection, extract arbitrary data from the database.

### CVE-2026-71231

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T11:16:25.740 |

IOTSmartHome's gui/login.php checkCookie() function builds an authentication query as SELECT * FROM users WHERE ID='<decoded lastLogin cookie>' after base64-decoding the client-supplied lastLogin cookie via safe_decode(), which performs URL-safe base64 decoding with no sanitization of the decoded value before it is concatenated into the SQL string. An unauthenticated attacker can set a lastLogin cookie containing a base64-encoded SQL injection payload (e.g. base64("' OR '1'='1")) to bypass authentication and, via UNION-based injection, extract arbitrary data including user credentials.

### CVE-2026-71214

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-05T08:16:43.807 |

The Aerie/PlanDev sequencing-server's authorization middleware (sequencing-server/src/app.ts) derives the caller's Hasura session role via getHasuraSession(), which prefers a session_variables object taken directly from the client-supplied JSON request body over the Authorization header's JWT claims, with no verification that the request actually originated from Hasura. By setting {"session_variables":{"x-hasura-role":"aerie_admin"}} in the body of a request to POST /command-expansion/put-expansion with no Authorization header, an unauthenticated attacker satisfies the role check and can insert arbitrary expansion rules into sequencing.expansion_rule, which govern how spacecraft activities are translated into commands. Separately, POST /put-dictionary is explicitly listed in the ENDPOINTS_WHITELIST and is exempt from any authentication, allowing unauthenticated writes of command dictionaries.

### CVE-2026-71207

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T08:16:42.717 |

The Stock-Inventory-Management-System application's login.php assigns raw $_POST username/password values to $_SESSION and builds its authentication query by directly concatenating those session values into a SQL statement with no parameterization or escaping. An unauthenticated remote attacker can submit a payload such as ' OR '1'='1 in the login form to bypass authentication entirely. The same script additionally contains hardcoded administrative credentials (admin/neola) in a post-login conditional check, providing a second, independent full-authentication-bypass path.

### CVE-2026-45538

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-04T21:16:36.270 |

OpenSIPS is a Session Initiation Protocol (SIP) server implementation. In versions 4.0.0 and prior, processing a SIP message with a header name longer than 255 bytes causes a stack buffer overflow when sip_to_json() is called in the routing script. Function sip_to_json() (modules/sipmsgops/sipmsgops.c) copies SIP header names into a fixed 255-byte stack buffer without bounds checking, performing a memcpy of the full header-name length even though the SIP parser imposes no such limit (a header name can be roughly 65000 bytes). As a result, when a routing script calls sip_to_json(), a SIP message with a header name longer than 255 bytes triggers a stack buffer overflow in which both the length and content of the overwrite are attacker-controlled, corrupting the saved frame pointer and return address. A single unauthenticated UDP packet to the SIP port (5060) can crash the process or, on builds without stack protections, hijack the return address to achieve remote code execution. This affects deployments whose routing script invokes sip_to_json(). This issue was not fixed at the time of publication.

### CVE-2026-0163

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-04T19:16:39.213 |

In multiple functions of vpu_ioctl.c, there is a possible use after free due to a use after free. This could lead to remote escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-24254

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-04T18:16:49.937 |

NVIDIA Dynamo for Linux contains a vulnerability in the multimodal serving topology, where an attacker could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, data tampering, denial of service, and information disclosure.

### CVE-2026-63456

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-04T17:16:57.853 |

Multiple vulnerabilities in the REST API interface of HPE Networking SD-WAN Orchestrator could allow an unauthenticated remote attacker to bypass web authentication mechanisms and access system functions. Successful exploitation could allow an attacker to view and modify potentially sensitive information on the target system.

### CVE-2026-63455

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-04T17:16:57.717 |

Multiple vulnerabilities in the REST API interface of HPE Networking SD-WAN Orchestrator could allow an unauthenticated remote attacker to bypass web authentication mechanisms and access system functions. Successful exploitation could allow an attacker to view and modify potentially sensitive information on the target system.

### CVE-2025-29296

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-04T17:16:42.920 |

H3C Magic BE18000 V200R007, H3C NX400 V100R015, H3C Magic NX30 Pro V100R0011, H3C Magic R3010 V100R009, H3C Magic NX15 V100R017, H3C Magic R1510 V100R016, H3C NE36 Pro V100R002 and H3C MC102G HM1A0V200R010 contain multiple command injection vulnerabilities in the /api/esps request handler. The affected object interfaces and methods are esps.dhcpd.vlan (getlist, delete), esps.filter.url (add, modify), esps.apcm.version (delete, H3C Magic NX15 only), esps.swcm.version (delete, upgrade, all affected models except H3C Magic NX15), and esps.system.ntp (set, all affected models except H3C Magic NX15). Attacker-controlled request parameters are incorporated into shell expressions executed by eval without adequate validation, allowing a remote attacker to execute arbitrary commands as root and gain complete control of the affected device.

### CVE-2026-70376

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-05T08:16:41.703 |

Pluck CMS's admin panel relies solely on a Referer-header comparison (requestedByTheSameDomain() in data/inc/functions.admin.php, gating every admin.php action) for CSRF protection, with no per-request anti-CSRF token anywhere in the admin area. When a request carries no Referer/Host information, the function's elseif branch returns true, treating the request as same-origin. Because a cross-site attacker page can suppress the Referer header (e.g. via <meta name=referrer content=no-referrer>), it can force an authenticated administrator's browser to submit forged admin actions with no valid Referer, including creating pages with raw HTML (stored XSS via the rendered page) and installing PHP modules/themes (remote code execution).

### CVE-2026-25289

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-04T16:16:24.890 |

Memory Corruption when processing Device Capability Extended attributes in certain NAN Service Discovery Frames with invalid length values.

### CVE-2026-70477

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-04T20:16:54.473 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, a prompt injection sent to a chatflow using a CSV Agent node can cause the LLM to respond with a malicious Python script that bypasses the blocklist validator and executes in an unsandboxed Pyodide environment. The specific flaw exists within the run method of the CSV_Agents class, where untrusted data is used to construct an LLM prompt and the resulting pythonCode is validated by validatePythonCodeForDataFrame before execution. An attacker can leverage this to execute arbitrary code in the context of the service account. This issue is fixed in 3.1.3.

### CVE-2026-70470

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-08-04T18:16:57.930 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, Flowise validatePythonCodeForDataFrame in packages/components/src/pythonCodeValidator.ts can be bypassed with Unicode homoglyph identifiers, allowing arbitrary Python execution inside Pyodide and full OS command execution on the Flowise host via Pyodide js module interop. The validator gates pyodide.runPythonAsync in packages/components/nodes/agents/CSVAgent/CSVAgent.ts and packages/components/nodes/agents/AirtableAgent/AirtableAgent.ts with an ASCII word-boundary blacklist. JavaScript regex word boundaries are ASCII-only, while Python 3 NFKC-normalizes identifiers at parse time, so homoglyph forms such as __cl𝐚ss__, __subcl𝐚sses__, __b𝐚se__, and __b𝐮iltins__ bypass the blacklist and are parsed as their ASCII equivalents. This issue is fixed in version 3.1.3.

### CVE-2026-58073

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-04T17:16:56.930 |

A vulnerability in Veeam Service Provider Console allowing an unauthenticated attacker to impersonate a managed agent andobtain that agent's credentials.

### CVE-2026-69264

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-95` |
| Published | 2026-08-04T18:16:57.027 |

Prior to 3.1.3, Flowise CSVAgent interpolates an attacker-controlled segment of the csvFile data URI directly into a Python source-code template that is then executed by Pyodide. Because Pyodide is loaded with the default js bridge to globalThis, which on Node.js exposes eval and dynamic import, the attacker can break out of the Python string literal, hand a JavaScript string to js.eval, dynamically import Node built-in modules such as fs and child_process, and execute arbitrary file I/O or OS commands as the Flowise process. The two validator paths around this code, validatePythonCodeForDataFrame and validateCustomReadCSVFunction, are never applied to the bootstrap template. A workspace user with chatflows:create or agentflows/chatflows update permission can plant a CSV Agent node with a crafted csvFile; once the chatflow is exposed via POST /api/v1/prediction/:id, any unauthenticated request triggers host remote code execution. This issue is fixed in version 3.1.3.

### CVE-2026-69259

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-04T17:17:01.413 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, the SQLite Record Manager node in packages/components/nodes/recordmanager/SQLiteRecordManager/SQLiteRecordManager.ts accepted user-controlled additionalConfig and spread it after the intended database setting, allowing additionalConfig.database to overwrite the SQLite database path. An authenticated attacker using the published Docker image, which ran as root, could write a SQLite database to paths such as /etc/chromium/exploit.conf; by controlling the table name and namespace value, the attacker could place shell syntax into the database file and trigger execution when Puppeteer launched Chromium and sourced /etc/chromium/*.conf. This issue is fixed in version 3.1.3.

### CVE-2026-69256

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-04T17:17:00.707 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, the CSVAgent node allowed users to provide Python code that is executed through pyodide; although a denylist blocked dangerous Python constructs, pandas.read_pickle() could deserialize a pickled payload and achieve code execution without matching the denied words. The affected file is flowise-components/nodes/agents/CSVAgent/CSVAgent.ts, where user-supplied customReadCSVFunc is evaluated as pd.${customReadCSVFunc}. An authenticated user who can create or modify a chatflow can add a CSV Agent, place a malicious read_pickle payload in the Additional Parameters, save the chatflow, and trigger /api/v1/prediction/<UUID> to execute commands. This issue is fixed in version 3.1.3.

### CVE-2026-69254

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-04T16:16:29.243 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, executeJavaScriptCode() accepted caller-provided nodeVMOptions and merged them over the default NodeVM security settings in packages/components/src/utils.ts. An authenticated attacker reaching packages/server/src/routes/node-custom-functions/index.ts could run a custom function that imported flowise-components/dist/src/utils.js, called executeJavaScriptCode() again with nodeVMOptions.require.builtin set to allow all built-in modules, and then required child_process to execute arbitrary system commands as root on the Flowise server. This issue is fixed in version 3.1.3.

### CVE-2026-66747

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-506` |
| Published | 2026-08-05T11:16:25.510 |

Zbtlink router firmware ships an embedded remote-control implant, ENDLESSDOORS, present in every published build across the product line. It is the open-source ycsunjane/rctl tool built in as an OpenWrt package (librctl.so), started at boot and run as root under the process name kworker to blend in with the kernel's [kworker/*] threads. It opens no listening port; it phones home over cleartext TCP to a hardcoded command-and-control server (command channel 7000, interactive-shell callback 7001) with no authentication and no transport encryption, re-attempting contact roughly every 35 seconds. Its command handler passes any received string to popen() as uid=0, and a reserved rctlbash command returns an interactive root shell. Because the channel is unauthenticated and cleartext, control is not limited to whoever planted it: any party that answers at the C2 address, occupies the network path (DNS or route hijack), or acquires the hardcoded fallback domain obtains unauthenticated remote code execution as root.

### CVE-2026-9273

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-640` |
| Published | 2026-08-05T06:16:40.967 |

The Membership Plugin – Kadence Memberships plugin for WordPress (formerly Restrict Content) is vulnerable to password reset link poisoning leading to account takeover in all versions up to, and including, 4.0.0. This is due to the legacy lost-password handler rc_process_lost_password_form() consuming the attacker-controlled rc_redirect POST parameter into two unvalidated sinks in legacy/includes/forms.php: wp_redirect( esc_url( $_POST['rc_redirect'] ) . ... ) at line 243, and add_query_arg( array( 'key' => $key, 'login' => ... ), $_POST['rc_redirect'] ) inside rc_send_password_reset_email() at line 306. The nonce required to reach the handler is broadcast by the public [login_form] shortcode at line 207 to any anonymous visitor. This makes it possible for unauthenticated attackers to issue a password-reset request for any account (including administrators) whose reset email body points the victim at an attacker-controlled host carrying a valid reset key/login. When the victim clicks the link, the reset key leaks to the attacker, who can replay it against the legitimate site to complete account takeover.

### CVE-2026-70554

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-04T21:16:38.613 |

MaxSite CMS contains a PHP object injection vulnerability that allows unauthenticated attackers to execute arbitrary code by passing attacker-controlled serialized data in the maxsite_comuser cookie directly to unserialize() without validation or class allowlisting. Attackers can craft a malicious serialized PHP object payload delivered in a single HTTP request to trigger magic methods during object graph reconstruction, enabling property-oriented programming attacks or remote code execution via available gadget chains such as those targeting SoapClient or Imagick extensions.

### CVE-2026-70553

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-04T20:16:56.023 |

MaxSite CMS contains a remote code execution vulnerability that allows unauthenticated attackers to inject arbitrary PHP code into the application configuration file by submitting crafted POST requests to the install endpoint after installation is complete. Attackers can supply a malicious db_dbprefix value containing a single quote to break out of a PHP string literal in application/config/database.php, appending attacker-controlled PHP statements that are executed by the web server on every subsequent request, resulting in persistent unauthenticated remote code execution as the web-server process user.

### CVE-2026-70552

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-04T20:16:55.883 |

MaxSite CMS 109.5 and earlier contains an authentication bypass vulnerability in the AJAX dispatcher that allows unauthenticated attackers to access admin-gated endpoints by supplying any X-Requested-With header and requesting a base64-encoded path resolving to any *-ajax.php file in the codebase. Attackers can exploit this dispatcher bypass to reach privileged plugin endpoints without credentials, enabling actions such as manipulating poll states and vote counts, and amplifying the impact of any dangerous operation performed by admin-only ajax files across the plugin tree.

### CVE-2026-69703

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-04T19:16:54.130 |

Atlas-Livre contains an improper access control vulnerability in the admin controllers under Espace_admin/controleur/ that allows unauthenticated attackers to bypass session-based authentication guards by sending raw HTTP requests that ignore redirects. Attackers can invoke destructive admin actions such as record deletion by requesting controller endpoints with GET parameters like supp, because the PHP header() redirect is never followed by an exit or die call, allowing all subsequent code including database operations to execute regardless of session state.

### CVE-2026-49435

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-04T19:16:51.810 |

Keysight IxChariot Endpoint and associated products contain a stack-based buffer overflow. An unauthenticated remote attacker can send a specially crafted packet and execute arbitrary code with administrative privileges.

### CVE-2017-20242

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-04T19:16:38.963 |

Keysight IxChariot Endpoint before 9.5.102 contains a stack-based buffer overflow. An unauthenticated remote attacker can send a specially crafted packet to crash the endpoint or potentially execute arbitrary code.

### CVE-2017-20241

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-04T19:16:38.810 |

Keysight IxChariot Endpoint before 9.5.102 contains a heap-based buffer overflow. An unauthenticated remote attacker can send a specially crafted packet to crash the endpoint or potentially execute arbitrary code.

### CVE-2026-69110

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-04T16:16:28.483 |

OpenCode Studio before 2.4.4 contains a missing authentication vulnerability that allows unauthenticated remote attackers to read arbitrary files within the temp and static/music directories by directly accessing the GET /api/tmp/:tmpFile and GET /api/music/:fileName endpoints. Attackers can retrieve intermediate audio, video artifacts, and subtitles belonging to other users' jobs, and additionally delete any video by ID through the unauthenticated DELETE /api/short-video/:videoId endpoint.

### CVE-2026-69098

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-04T16:16:28.190 |

kotaemon through 0.12.0 contains an insecure deserialization vulnerability in the check_connection endpoint that allows unauthenticated attackers to instantiate arbitrary Python classes by supplying crafted YAML/JSON input with a __type__ field. Attackers can exploit this to override the __type__ field with subprocess.check_output and arbitrary arguments, achieving remote code execution with application process privileges.

### CVE-2026-18801

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:H/SC:H/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-04T16:16:22.647 |

OpenMeter contains a stored, or second-order, SQL injection vulnerability in the handling of customer usage-attribution values.



An attacker who can create or update a customer can store a malicious value in the usageAttribution.key or usageAttribution.subjectKeys fields. When that customer is subsequently used in a meter or event query, OpenMeter inserts the stored value into a ClickHouse WITH map(...) expression using string concatenation.

OpenMeter versions from v1.0.0-beta.218 through v1.0.0-beta.231 are affected.

### CVE-2026-61515

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-912` |
| Published | 2026-08-04T15:16:36.967 |

Puwell IP Camera firmware versions 2.x through 4.x contains an unauthenticated command injection vulnerability that allows remote attackers to execute arbitrary operating system commands by sending a crafted JSON payload to the DebugShell interface exposed on TCP port 34567. Attackers can exploit the lack of authentication and input sanitization in the binary protocol service to pass arbitrary commands directly to the underlying operating system, achieving root-level code execution and complete device compromise.

### CVE-2026-61514

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-04T15:16:36.810 |

Puwell IP Camera firmware versions 2.x through 4.x contains an authentication bypass vulnerability that allows unauthenticated attackers to access device functions by sending protocol-conforming packets over TCP port 23456 without credentials. Attackers can exploit the unvalidated Session field in the proprietary control protocol header to access live video streams, control pan and tilt motors, activate audio functions, and remotely restart the device.

### CVE-2026-70478

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-04T20:16:54.610 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, the POST /api/v1/oauth2-credential/refresh/:credentialId endpoint is included in WHITELIST_URLS and requires no authentication. The endpoint decrypts the stored credential, sends a refresh request to the configured OAuth provider with the client secret and refresh token, and returns the refreshed access_token in the response body. An attacker with a credential ID can use the token to access the victim's connected service and can also exhaust refresh-token quota. This issue is fixed in 3.1.3.

### CVE-2026-69255

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-04T17:17:00.570 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, the CSVAgent in packages/components/nodes/agents/CSVAgent/CSVAgent.ts extracted attacker-controlled CSV data with file.split(',').pop() and interpolated it directly into executable Python as base64_string = "${base64String}" before calling Pyodide. The validatePythonCodeForDataFrame() denylist only checked later LLM-generated code and did not validate this initial code block. An authenticated attacker could inject a closing quote followed by Python code, use Pyodide's js bridge to load Node.js child_process, and execute arbitrary operating system commands as root in the Flowise container. This issue is fixed in version 3.1.3.

### CVE-2026-71277

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-05T13:24:52.200 |

rust-iot-platform's AuthToken request-guard implementation (api/src/main.rs) only checks whether the Authorization HTTP header is present, and never validates its value against any session, token store, or signature. Any request carrying an arbitrary non-empty Authorization header (e.g. `Authorization: fake`) satisfies the guard, granting access to every endpoint protected only by this request guard.

### CVE-2026-71263

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-05T13:24:50.473 |

The LINUXTCP port of FreeModbus contains an off-by-one bounds check in xMBPortTCPPool() (demo/LINUXTCP/port/porttcp.c). The check `if (usTCPFrameBytesLeft > MB_TCP_BUF_SIZE)` uses a strict greater-than comparison instead of greater-than-or-equal against the 263-byte MB_TCP_BUF_SIZE limit. An MBAP frame with a Length field of 264 makes usTCPFrameBytesLeft equal to 263, which passes the flawed check, and the subsequent recv() call writes up to 263 bytes starting at buffer offset 7 into the 263-byte static buffer aucTCPBuf, overflowing it by 7 bytes into the adjacent static variable usTCPBufPos. A single crafted, unauthenticated Modbus TCP packet triggers the overflow, since Modbus has no built-in authentication.

### CVE-2026-71238

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-05T11:16:26.630 |

DjangoCRM ships with its Django SECRET_KEY hardcoded directly in the committed webcrm/settings.py rather than read from an environment variable. Since this key is used for session signing, CSRF token generation, and password reset tokens, anyone who reads the public repository can forge valid session cookies (including for the superadmin account), forge CSRF tokens, and forge password reset tokens, achieving full account takeover. The repository also ships with DEBUG=True as the default, causing error pages to leak database credentials, email credentials, OAuth data, and internal file paths.

### CVE-2026-44945

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-441;CWE-497` |
| Published | 2026-08-05T10:17:27.460 |

A privilege escalation vulnerability exists in Rancher's impersonation middleware (pkg/auth/requests/impersonate.go). An authenticated Rancher user with the default user
 global role can gain full administrative access to the Rancher control 
plane and transitively to all downstream clusters it manages.

This issue affects Rancher: from 2.11.0 before 2.11.16, from 2.12.0 before 2.12.12, from 2.13.0 before 2.13.8, and from 2.14.0 before 2.14.2.

### CVE-2026-10059

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-05T09:18:13.720 |

A flaw was found in the Multicluster Engine for Kubernetes ClusterCurator controller. A tenant administrator with namespace-scoped privileges can exploit this vulnerability by creating a namespaced ClusterCurator. This action inadvertently grants the tenant administrator the ability to mint a token for a ServiceAccount with cluster-wide administrative authority. This leads to a privilege escalation, allowing the tenant administrator to gain full control over the cluster.

### CVE-2026-71213

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-307` |
| Published | 2026-08-05T08:16:43.647 |

Typemill's login endpoint (POST /tm/login, ControllerWebAuth::login()) performs no rate-limiting, failed-attempt counting, or account lockout when captcha is disabled, which is the default configuration. An unauthenticated attacker can send unlimited password-guessing requests against any account, including administrators, with no throttling. The only attempt-counting/lockout logic present in the same file protects an optional secondary email-authcode step and does not apply to the primary password check.

### CVE-2026-5581

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T08:16:35.007 |

The Multi Uploader for Gravity Forms plugin for WordPress is vulnerable to unauthorized arbitrary media deletion in all versions up to, and including, 1.1.8. This is due to missing capability checks in the `plupload_ajax_delete_file()` function, which is registered via `wp_ajax_nopriv_gfmu_delete_file`. The nonce intended for CSRF protection is exposed on any public-facing page containing a multi-uploader form field via the `GFMU_options` JavaScript object. This makes it possible for unauthenticated attackers to permanently delete any WordPress media attachment by supplying its attachment ID, potentially leading to complete media library destruction.

### CVE-2026-4431

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T08:16:33.457 |

The Easy Post Submission plugin for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the `create_post()` function in all versions up to, and including, 2.3.0. This is due to the `rbsm_submit_post` AJAX action being registered for unauthenticated users via `wp_ajax_nopriv_rbsm_submit_post` without any authorization checks when a `postId` parameter is supplied. This makes it possible for unauthenticated attackers to modify the title, content, excerpt, categories, and tags of arbitrary posts, as well as change the post status to draft (effectively unpublishing them) via the 'postId' parameter.

### CVE-2026-45537

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-04T23:16:51.687 |

OpenSIPS is a Session Initiation Protocol (SIP) server implementation. In versions prior to 3.6.6 and 4.0.0-rc1, the construct_uri() function concatenates multiple URI components (protocol, username, domain, port, params) into a fixed 1024-byte global BSS buffer without any bounds checking. When a routing script calls construct_uri() with an attacker-controlled username, a combined component length exceeding 1024 bytes overflows the buffer, corrupting adjacent global data with attacker-controlled content. The overflow reaches disable_503_translation, a global flag controlling SIP 503 response handling, allowing an attacker to deterministically set the flag via the URI username and alter the server's routing behavior for subsequent messages. Because the same buffer is shared with contact_builder(), the overflow also corrupts that function's data, and without a memory sanitizer the adjacent globals are silently overwritten on every request containing a long username. This issue has been fixed in versions 3.6.6 and 4.0.0-rc1.

### CVE-2026-45100

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-04T22:17:14.670 |

OpenSIPS is a Session Initiation Protocol (SIP) server implementation. Versions 3.4.0-beta through 3.6.5 and 4.0.0-beta contain a buffer overflow in the {s.b64encode} string transformation. The size check for {s.b64encode} only verifies that the input fits within the 64 KB transformation buffer, but base64 encoding expands the data by roughly a third, so an input between about 49,153 and 65,535 bytes produces more output than the buffer can hold and overflows it by up to 21,844 bytes. Because these transformation buffers sit next to each other in memory and are reused for chained transformations, the overflow writes attacker-controlled data into the adjacent buffer and corrupts values used by later transformations processing the same SIP message. A remote attacker can trigger this by sending a SIP message with a large header value (roughly 50,000 bytes or more) when the routing script applies  {s.b64encode}  to attacker-controlled input, making exploitability dependent on the deployment's routing configuration. This issue has been fixed in versions 3.6.6 and 4.0.0-rc1.

### CVE-2026-58072

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-04T17:16:56.633 |

A vulnerability in Veeam Service Provider Console allowing arbitrary file write on the management server, which can lead to remotecode execution.

### CVE-2026-69253

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-04T16:16:29.100 |

Flowise is a drag-and-drop user interface for building customized large language model (LLM) flows. Prior to version 3.1.3, several custom-tool components — AgentAsTool, ChatflowTool, and ExecuteFlow — ran code in the in-process  vm2  sandbox. To build that code, they inserted a user-controlled  baseURL  value straight into the JavaScript source, for example  const url = "${baseURL}/..."; . The only check on  baseURL  was  isValidURL , but a valid-looking URL can still contain characters that break out of a code string. An authenticated user could craft a  baseURL  that passed this check, closed the surrounding string, and injected their own JavaScript into the sandboxed script (code injection, CWE-94). The  vm2  sandbox runs in the same Node.js process as Flowise and exposes risky dependencies. As a result, the injected code could escape the sandbox and run arbitrary code on the Flowise server as the Flowise process user. Exploitation only requires an authenticated session. The issue is fixed in version 3.1.3, which passes the URL to the sandbox as data instead of inserting it into code and adds stricter URL validation.

### CVE-2026-69251

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-04T15:16:44.430 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, Flowise record manager and agent memory nodes allowed users to set arbitrary TypeORM DataSource options through the additionalConfig input in packages/components/nodes/recordmanager/MySQLRecordManager/MySQLrecordManager.ts, packages/components/nodes/recordmanager/PostgresRecordManager/PostgresRecordManager.ts, packages/components/nodes/recordmanager/SQLiteRecordManager/SQLiteRecordManager.ts, packages/components/nodes/memory/AgentMemory/MySQLAgentMemory/MySQLAgentMemory.ts, and packages/components/nodes/memory/AgentMemory/AgentMemory.ts. TypeORM DataSource options such as entities, subscribers, and migrations can load local JavaScript files, allowing an authenticated user to execute arbitrary code on the server by uploading a JavaScript payload and referencing it from additionalConfig.entities. This issue is fixed in version 3.1.3.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-71291

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-05T13:24:53.820 |

Bolt CMS renders content field values through Twig's full application-level Environment with no SandboxExtension registered anywhere in the codebase. In src/Entity/Field.php, getTwigValue() calls shouldBeRenderedAsTwig(), which gates rendering only on the field definition's allow_twig flag and a regex checking for `{{`, `{%`, or `{#`; when true, the raw field value is compiled and rendered via `self::getTwig()->createTemplate($value)->render(['record' => $this->getContent()])` with no sandboxing. Bolt's own bundled config/bolt/contenttypes.yaml sets `allow_twig: true` on the default "pages" contenttype's content field out of the box. Any user with edit access to that content type (a standard editor role, not just an administrator) can inject a Twig payload such as `{{ ['id']|map('passthru')|join }}` that executes arbitrary OS commands when the content is saved and rendered, achieving remote code execution as the web server user.

### CVE-2026-71288

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T13:24:53.583 |

Koha's guided report builder (reports/guided_reports.pl) reads the `order_by` CGI parameter and, for each value, a dynamically-named `{order}_ovalue` parameter, and concatenates both directly into an SQL ORDER BY clause with no allowlist or validation: `my @order_by = $input->multi_param('order_by'); foreach my $order (@order_by) { my $value = $input->param($order . "_ovalue"); $query_orderby = " ORDER BY $order $value"; }`. The resulting string is appended verbatim to the final query in C4::Reports::Guided (`$query .= $orderby;`) with no escaping. Since ORDER BY columns cannot be bound via prepared-statement placeholders, this requires an explicit allowlist, which does not exist. Any staff account with the low-privilege create_reports or execute_reports permission (commonly granted to non-admin library staff) can perform time-based blind SQL injection against the Koha database, which stores patron PII and staff/LDAP credentials.

### CVE-2026-71287

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T13:24:53.453 |

Cacti's sanitize_sql_column() (lib/functions.php) sanitizes user-supplied ORDER BY column names using the regex `preg_replace('/[^a-zA-Z0-9_().]/', '', $column)`. Because this allowlist retains letters, digits, underscore, parentheses, and dot (intended to support expressions like COUNT(id) and table.column), a payload such as `SLEEP(5)` passes through completely unmodified. The sanitized value is concatenated directly into raw SQL ORDER BY clauses (which cannot be parameterized) driven by a `sort_column` GET parameter in at least user_log.php, utilities.php, user_domains.php, and user_group_admin.php, allowing any authenticated Cacti user, regardless of privilege level, to perform time-based blind SQL injection against the Cacti database.

### CVE-2026-71281

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-05T13:24:52.723 |

Hugging Face peft's LoRA-GA and CorDA initialization modules (src/peft/tuners/lora/corda.py lines ~102 and ~163, and src/peft/tuners/lora/loraga.py line ~101) call torch.load() on config-specified cache/covariance files without weights_only=True, bypassing peft's own safe-loading wrapper used elsewhere in the codebase. Because torch.load() without weights_only=True performs full pickle deserialization, loading a malicious cache or covariance file (e.g. a shared/downloaded LoRA-GA or CorDA cache) results in arbitrary code execution.

### CVE-2026-71243

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-05T11:16:27.247 |

The backmeup npm package assembles shell command strings by directly concatenating its option values (name, source, destination, filter) - e.g. cmd = "mkdir -p " + path.join(info.destination, info.name) + "; " - and executes the resulting string through a shell via ssh2-exec (locally via child_process, or remotely via SSH when an ssh handle is supplied), rather than using execFile/spawn with an argument array. The only processing applied is path.normalize()/path.join(), which do not neutralize shell metacharacters (;, |, &, $(), backticks, newline). Any application that passes attacker-influenced values into these options (e.g. a user-chosen backup name) is vulnerable to arbitrary OS command execution on the backup host, or on the remote SSH target when one is configured.

### CVE-2026-71235

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-05T11:16:26.247 |

Magistrala's Rules Engine allows authenticated users to create rules with embedded Go or Lua scripts executed server-side when IoT messages arrive. The Go script engine (re/golang.go) runs scripts through the Yaegi interpreter with stdlib.Symbols, exposing the full Go standard library (including os and net/http) with validation limited to a regex blocking goroutines and panic() calls; dangerous functions such as os.ReadFile, os.WriteFile, os.Remove, and os.Environ remain fully accessible. The Lua script engine (re/lua.go) performs no input validation at all and preloads dangerous libraries: db (arbitrary database access), ioutil (file I/O), an HTTP client (SSRF), and filepath (traversal). An authenticated low-privileged user can achieve arbitrary file read/write, environment variable leakage, database access, and SSRF against internal microservices.

### CVE-2026-60009

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73;CWE-306;CWE-352` |
| Published | 2026-08-05T11:16:25.363 |

In Eclipse Theia versions up to and including 1.73.1, the `@theia/filesystem` backend binds `POST /file-upload` in every filesystem-enabled deployment. The handler takes an attacker-supplied absolute path from the multipart `uri` field and calls `fs.move(tmp, target, { overwrite: true })` with no workspace confinement and no authentication. In browser (non-Electron) deployments the connection token is enforced only on WebSocket upgrades; the HTTP middleware in `@theia/core` re-issues the cookie and calls `next()` without rejecting tokenless HTTP requests. Because `multipart/form-data` is a CORS-safelisted request type, a cross-origin web page can trigger the write with no preflight and no credentials, resulting in an unauthenticated arbitrary file write outside the workspace to any absolute path the backend process can write. This can escalate to remote code execution, for example by overwriting a startup-executed file such as `~/.bashrc`. Electron mode uses a separate `ElectronSecurityToken` and is not affected via this path.

### CVE-2026-6147

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-05T08:16:41.140 |

The LightSync Pro plugin for WordPress is vulnerable to arbitrary file uploads due to missing file type validation in the rest_replace_media() function in all versions up to, and including, 2.1.6. This makes it possible for authenticated attackers, with Author-level access and above, to upload arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-55997

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-312` |
| Published | 2026-08-05T08:16:34.330 |

Rancher issues long-lived registration tokens to authenticate nodes and agents joining a downstream cluster. These tokens were stored and exposed in plaintext with no expiration, so a malicious user could obtain one either through the Rancher API, etcd, stored automation, or direct file access on a node, and could use it at any time to register a rogue node into the cluster.

### CVE-2026-70375

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-05T07:16:39.697 |

HashBrown CMS through 1.4.6 contains an OS Command Injection vulnerability (CWE-78) in the Git deployer component. GitDeployer.pullRepo() in src/Server/Entity/Deployer/GitDeployer.js executes AppService.exec(`git checkout ${this.branch || 'master'}`), interpolating the configured branch value directly into a shell command with no escaping. GitDeployer.validate() only rejects a single-quote character in the repo, branch, username, and password fields; shell metacharacters such as ';', '&&', '|', backticks, and '$()' are not filtered. A user able to configure a project's Git deployer settings can set a malicious branch value (e.g. 'master;<command>#') that executes automatically on every subsequent deployer operation (media upload, content save, etc.), since pullRepo() is invoked unconditionally at the start of each such operation. This is related to CVE-2020-6948, which addressed single-quote escaping of the repo, username, and password fields in the same file's git clone invocation; the branch field used in the unquoted git checkout command was not covered by that fix and remains injectable.

### CVE-2026-70374

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-05T07:16:39.567 |

HashBrown CMS through 1.4.6 contains an OS Command Injection vulnerability (CWE-78) in the media upload thumbnail generation routine. Media.generateThumbnail() in src/Server/Entity/Resource/Media.js builds a temporary file path as 'thumbnail' + Path.extname(filename) and passes it, unescaped, into a shell command executed via AppService.exec() ('convert ' + tempFile + ...). The MIME-type filter in getMIMEType() (src/Common/utilities.js) truncates the extracted extension at the first '?' character, while Path.extname() does not, allowing a filename such as 'x.jpg?$(command)' to pass the image-type check while still injecting a shell command substitution into the exec() call. An authenticated user holding the media resource scope can achieve arbitrary OS command execution in the context of the Node.js process via POST /api/{project}/{environment}/media/new.

### CVE-2026-8761

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T06:16:40.660 |

The Dokan plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 5.0.1. This is due to a missing authorization check in the `CustomersController` REST controller (`includes/REST/CustomersController.php`), which re-registers WooCommerce's customer CRUD routes under the `/dokan/v1/customers/` namespace and replaces WooCommerce's native `manage_woocommerce` capability check with a vendor-only check that inspects the **requesting** user's role and never validates the **target** user. This makes it possible for authenticated attackers with Vendor/Seller-level access and above to read, modify, or delete any WordPress user — including administrators — via `GET`/`PUT`/`DELETE` requests against `/wp-json/dokan/v1/customers/{id}`. Setting the `password` parameter on an administrator's record yields a full site takeover.

### CVE-2026-18322

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-05T06:16:37.330 |

The Smart Popup by Supsystic plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.12.0. This is due to a permission map collision in the `havePermissions()` function in `classes/frame.php`, where `array_merge()` overwrites the popup module's administrator-restricted method list with the base controller's value, silently removing `save` from protected actions; this is compounded by the subscription confirmation email embedding the same generic `pps_nonce` that the unauthenticated `wp_ajax_nopriv_save` endpoint accepts, and by the complete absence of any server-side role allowlist in `createWpSubscriber()`. This makes it possible for unauthenticated attackers to submit a crafted POST request to `admin-ajax.php` using a nonce obtained from a public subscription confirmation email, setting `params[tpl][sub_wp_create_user_role]` to `administrator` via the exposed `popupControllerPps::save()` action, and then triggering the stored confirmation flow to create a persistent WordPress Administrator account with attacker-chosen credentials.

### CVE-2026-69258

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-915` |
| Published | 2026-08-04T17:17:01.280 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, the unauthenticated POST /api/v1/prediction/:id endpoint accepted an overrideConfig object and unconditionally spread it into internal flowConfig and flowData objects in packages/server/src/utils/buildChatflow.ts and packages/server/src/utils/index.ts without checking apiOverrideStatus. This allowed unauthenticated attackers to inject arbitrary properties into the flow execution context of any public chatflow, overwrite values such as chatId, sessionId, and chatHistory, and control values resolved through $flow.* template variables consumed by flow nodes. This issue is fixed in version 3.1.3.

### CVE-2026-18650

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-04T15:16:31.410 |

Missing Authorization vulnerability in HAVELSAN Inc. Liman MYS allows Privilege Escalation.

This issue affects Liman MYS: from 2.2.3 before 2.3.1.

### CVE-2026-71236

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-05T11:16:26.377 |

Grocy's API request-body parser (controllers/Api/BaseApiController.php, GetParsedAndFilteredRequestBody) purifies incoming field values with HTMLPurifier, then manually reverses HTML-entity encoding of the resulting output by replacing &amp;lt;, &amp;gt;, and &amp;amp; back to <, >, and & immediately after purification. This double-decode reconstructs live HTML/script tags from the entity-encoded form that HTMLPurifier produced to neutralize them, re-introducing stored XSS across API-writable fields (products, recipes, stock, users, chores, and others) that are rendered elsewhere without re-sanitization.

### CVE-2026-71233

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-05T11:16:25.997 |

InvoiceNinja v5-stable renders an invoice or quote's "terms" field in the client portal using Laravel Blade's raw output directive {!! $entity->terms !!} (resources/views/portal/ninja2020/invoices/includes/terms.blade.php) with no HTML sanitization. StoreInvoiceRequest.php only strips newlines from the field and does not purify HTML. An authenticated user with invoice creation access can set the terms field via the REST API (PUT /api/v1/invoices/{id}) to an HTML/JavaScript payload that executes in the client's browser when they view the invoice, enabling session cookie theft and client account takeover. This is a distinct code path from the previously published invoice line-item description field XSS (GHSA-98wm-cxpw-847p / CVE-2026-33628).

### CVE-2026-71190

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-08-05T06:16:40.023 |

In OpenStack Swift through 2.38.0, the proxy server Accept header parser contains a regular expression vulnerable to catastrophic backtracking (ReDoS). The "qdtext" pattern (?:[^"]|\\.)* allows an unauthenticated remote attacker to send a crafted Accept header that causes exponential CPU consumption in the proxy worker. A payload of 32 backslash-character pairs exceeds 30 seconds of CPU time. No authentication is required. Repeated requests can exhaust all proxy worker threads, resulting in a complete denial of service.

### CVE-2026-46334

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-476` |
| Published | 2026-08-05T00:17:00.177 |

OpenSIPS is a Session Initiation Protocol (SIP) server implementation. Versions prior to 3.6.6 and 4.0.0-rc1 contain a denial of service vulnerability in the SDP bandwidth-line parsing logic. A SIP request with Content-Type: application/sdp and a malformed session-level SDP bandwidth line missing the required colon delimiter can corrupt parsed SDP bandwidth metadata. When a route or module subsequently clones the corrupted SDP state, as occurs with dialog and QoS processing, the OpenSIPS worker process crashes. An unauthenticated remote attacker can therefore trigger a crash in any configuration whose routing script parses attacker-controlled SDP and applies dialog/QoS processing. This issue has been fixed in versions 3.6.6 and 4.0.0-rc1.

### CVE-2026-45809

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-05T00:17:00.030 |

OpenSIPS is a Session Initiation Protocol (SIP) server implementation. Versions prior to 3.6.6 and 4.0.0-rc1 contain a denial of service vulnerability in the watcherinfo generation functionality. An attacker can create an oversized watcher entry by sending a SUBSCRIBE Event: presence request with a long From URI, and then trigger presence.winfo watcherinfo XML generation for the same presentity. OpenSIPS copies the stored watcher URI into a fixed-size stack buffer, overflowing it and crashing the process. A remote attacker can crash an OpenSIPS worker in deployments that expose handle_subscribe() and allow watcherinfo (presence.winfo) generation. The issue is configuration-dependent because the presence and presence_xml modules must be loaded and SUBSCRIBE routing must be reachable. This issue has been fixed in versions 3.6.6 and 4.0.0-rc1.

### CVE-2026-70619

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-04T22:17:17.573 |

Odysseus before commit bf325f6 contains a missing authorization vulnerability that allows authenticated non-admin users to manage server-wide embedding backend configuration by invoking endpoint management routes that verify session authentication but omit the admin authorization guard. Attackers can supply an attacker-controlled URL to overwrite the embedding backend persisted in the endpoint configuration file and process environment, causing all subsequent embedding operations including chat messages, RAG queries, memory entries, and vault text to be transmitted in plaintext to the attacker-controlled destination, or delete the endpoint configuration to deny embedding service to all users.

### CVE-2026-45084

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-04T22:17:14.493 |

OpenSIPS is a Session Initiation Protocol (SIP) server implementation. Versions 3.4.0 through 3.6.5 contain a denial of service vulnerability in the presence module. When the presence module's handle_publish() function processes a SIP PUBLISH request with an Event: presence header and a message body while the configuration option enable_sphere_check=1 is set, it invokes the get_content_type() macro without first calling parse_content_type_hdr(), causing it to dereference uninitialized or NULL Content-Type parsing state and crash. If a Content-Type header is present but unparsed, msg->content_type->parsed is NULL and is dereferenced as a content_t pointer; if the request lacks a Content-Type header entirely, msg->content_type itself is NULL, and both cases lead to a crash. A remote attacker can therefore cause a denial of service against an affected instance with a single PUBLISH request over UDP or TCP, using either a valid Content-Type: application/pidf+xml request or one with the header removed, and the vulnerable code path itself does not enforce authentication (though a deployment's routing configuration may require it before this route is reached). The issue has been fixed in version 3.6.6 and 4.0.0-rc1.

### CVE-2026-70492

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-04T21:16:38.190 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.10.0 until 0.11.0, src/lib/components/chat/Messages/Markdown/KatexRenderer.svelte could store and render a chat message whose math block makes KaTeX fail with a stack overflow instead of a parse error. The catch branch fell back to inserting the original math source into the page as HTML through {@html} rather than as text, so script in the message runs in the browser of whoever views it, including shared chats and channels. The viewer's session token in localStorage can be stolen, and an administrator viewer can have their account taken over. This issue is fixed in 0.11.0.

### CVE-2026-16793

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-78` |
| Published | 2026-08-04T20:16:49.463 |

An improper neutralization of special elements used in an operating system command vulnerability was reported in Lenovo XClarity Orchestrator (LXCO) 2.2.0 that could allow an authenticated attacker to execute arbitrary operating system commands as a privileged user under a specific circumstance.

### CVE-2026-69263

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-08-04T17:17:01.683 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, the mitigation for CVE-2025-8943 blocked -y and --yes flags on npx, but packages/components/nodes/tools/MCP/core.ts denied only PATH, LD_LIBRARY_PATH, DYLD_LIBRARY_PATH, and NODE_OPTIONS by exact environment-variable name. Because npm reads configuration from npm_config_* variables, setting npm_config_yes=true reproduced --yes behavior without using a blocked flag, causing npx to auto-install and execute the named package when a Custom MCP server launched. This issue is fixed in version 3.1.3.

### CVE-2026-58075

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-04T17:16:57.190 |

A vulnerability allowing an unauthenticated attacker to read arbitrary files from the host, which can be further leveraged toescalate privileges locally.

### CVE-2026-58067

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-04T17:16:56.333 |

A vulnerability in Veeam Service Provider Console allowing an unauthenticated attacker to exhaust host memory and cause adenial of service.

### CVE-2026-15307

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73;CWE-918` |
| Published | 2026-08-04T17:16:46.127 |

An issue was discovered in Django 5.2 before 5.2.17 and 6.0 before 6.0.8.
GeoDjango spatial lookups optimistically parse the right-hand-side value as a raster by passing it to the `django.contrib.gis.gdal.GDALRaster` constructor. Any value used in a spatial lookup against a `GeometryField` or `RasterField` reaches this constructor, including untrusted input, for example a spatial-field filter submitted through the Django admin changelist query string by a staff user with view permission. A `dict`, or a `str` holding its JSON representation, is opened in write mode regardless of the constructor's `write=False` default, allowing a file with an attacker-chosen name and contents to be written through a file-backed GDAL driver. Any other `str` is treated as a datasource, allowing an outbound network request through a GDAL virtual filesystem handler. Writing a file to a location later imported by the application can result in remote code execution.
Earlier, unsupported Django series (such as 5.1.x, 5.0.x, and 4.2.x) were not evaluated and may also be affected.
Django would like to thank Bence Nagy, localhost-detect, and kimchunbok_ for reporting this issue.

### CVE-2026-69100

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-04T16:16:28.340 |

LAMP Rapid Development Platform through 5.6.2, fixed in commit 84b0c27, contains a remote code execution vulnerability in GlueFactory that executes unsandboxed Groovy scripts from database template fields without compilation restrictions or whitelisting. Attackers can write or influence the script field via message template endpoints to execute arbitrary Groovy code and OS commands on the backend server.

### CVE-2026-68494

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-04T15:16:41.443 |

The fix released in jackson-core 2.18.6 and 2.21.1 for CVE-2026-18401 (GHSA-72hv-8253-57qq, number length constraint bypass in the non-blocking parser) is incomplete. This record covers the remaining bypass.

The earlier fix wired validateIntegerLength() into a new _setIntLength() helper and invoked it wherever the integer portion of a number is decided: a terminator byte arrives, a '.' or 'e'/'E' is seen, or input ends inside a fully buffered value. It was not invoked on the attacker-relevant path where the parser runs out of input while still inside the MINOR_NUMBER_INTEGER_DIGITS minor state and returns NOT_AVAILABLE to the caller.

As a result, an attacker who streams JSON to a non-blocking parser in many small chunks, without ever sending a terminator byte, keeps the parser inside MINOR_NUMBER_INTEGER_DIGITS indefinitely. _textBuffer.expandCurrentSegment() grows the accumulator on every chunk while validateIntegerLength() is never called. The accumulator is bounded only by maxStringLength (20 MiB by default) rather than by maxNumberLength (1000 by default), an amplification of roughly 20,000x over the documented limit. Because Java char values occupy two bytes, a single connection can be driven to approximately 40 MiB of heap before the validator finally fires when the value completes.

The equivalent fraction-path code is correct: _finishFloatFraction() calls _setFractLength() before its NOT_AVAILABLE return. The missing call affects the integer-digit paths in _startPositiveNumber(), _startNegativeNumber() and _finishNumberIntegralPart() in NonBlockingUtf8JsonParserBase.

Impact: reactive frameworks such as Spring WebFlux/Reactor, Quarkus, Helidon and Vert.x feed inbound HTTP or gRPC bytes to the async parser as they arrive, which is precisely the chunked-feed shape required. Operators who set StreamReadConstraints.maxNumberLength expecting it to cap memory per number value do not get that guarantee; memory accumulates per concurrent connection and attacker-controlled concurrency can exhaust the JVM heap. The synchronous parsers (UTF8StreamJsonParser, ReaderBasedJsonParser) and the async parser operating on complete input are not affected.

Exploitation requires only the ability to stream data to a parsing endpoint; no privileges or user interaction are needed.

This issue affects com.fasterxml.jackson.core:jackson-core from version 2.15.0 through 2.18.7, and from 2.19.0 through 2.21.3, and tools.jackson.core:jackson-core from 3.0.0 through 3.1.3. Versions prior to 2.15.0 are not affected, because StreamReadConstraints -- which defines the maxNumberLength setting -- was first introduced in jackson-core 2.15.0, so no such constraint exists to be bypassed in earlier releases. Note that GHSA-r7wm-3cxj-wff9 states the affected 2.x range without a lower bound. The 2.22.x and 3.2.x release lines are not affected: those branches were created after the fix commit landed on 2026-05-21 and therefore contain it from their initial releases (2.22.0, tagged 2026-06-03, and 3.2.0, tagged 2026-06-08).

### CVE-2026-67200

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-04T15:16:40.717 |

Perspective 5.0.0 contains a path traversal vulnerability that allows unauthenticated remote attackers to read arbitrary files from the server filesystem by including literal ../ segments in HTTP request URL paths. Attackers can bypass the insufficient query-string-stripping sanitization to traverse outside the configured asset root directory and retrieve sensitive files such as system credentials and application secrets, with results exposed cross-origin due to a wildcard Access-Control-Allow-Origin header set on all responses.

### CVE-2026-67198

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-616` |
| Published | 2026-08-04T15:16:40.423 |

Perspective 5.0.0 contains a denial-of-service vulnerability in the VirtualServer protocol dispatcher that allows unauthenticated remote attackers to crash the server process by sending malformed or incomplete protobuf messages. Attackers can send well-formed requests such as ViewToArrowReq with no viewport set or MakeTableReq with no data field to trigger unwrap() calls on None values at nine distinct sites, causing the process to abort with SIGABRT.

### CVE-2026-67195

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-04T15:16:40.130 |

Perspective 5.0.0 contains a remote code execution vulnerability that allows unauthenticated attackers to execute arbitrary operating system commands by submitting crafted expression strings to the PolarsVirtualServer backend, which passes client-supplied input directly to Python's eval() with only __builtins__={} cleared. Attackers can exploit Python object attribute traversal through the interpreter's loaded class list to reach subprocess.Popen via a TableValidateExprReq or TableMakeViewReq protobuf message, achieving arbitrary command execution in the Perspective host process.

### CVE-2026-67623

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-08-05T14:17:10.047 |

Mistral Vibe before 2.23.3 contains a remote code execution vulnerability that allows attackers to execute arbitrary commands by embedding a malicious core.fsmonitor hook in a repository's .git/config file, which is triggered when vibe invokes git status --porcelain without suppressing hook execution. Attackers can distribute or create a crafted repository containing a malicious fsmonitor entry to achieve arbitrary command execution with the victim's full privileges when any vibe command is run inside that repository.

### CVE-2026-71270

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-05T13:24:51.327 |

Stirling-PDF's POST /api/v1/convert/url/pdf endpoint (ConvertWebsiteToPDF.java) was not updated with the CustomHtmlSanitizer/SsrfProtectionService SSRF protections that were added to three sibling conversion endpoints (html/pdf, file/pdf, markdown/pdf). The endpoint validates only that the initial requested URL resolves to a public IP, then fetches the page's HTML server-side and hands it, unsanitized, to a WeasyPrint subprocess. Embedded resource references in the fetched HTML (e.g. `<img src="http://169.254.169.254/...">`) are fetched by WeasyPrint with no per-resource SSRF filtering, allowing an attacker-controlled page to cause the server to retrieve cloud metadata endpoints or internal network resources and leak their contents back into the generated PDF.

### CVE-2026-71259

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-08-05T13:24:49.993 |

ESPHome through 2026.7.0-dev contains an operator-precedence bug in the cv.url() validator in esphome/config_validation.py: `if parsed.scheme and parsed.netloc or parsed.scheme == "file": return parsed.geturl()`. Because `and` binds tighter than `or`, any file: URI passes validation regardless of netloc. This validator gates the `url:` field of the external_components YAML directive's git source schema, which is passed to `git clone` (git supports file:// natively). A crafted `external_components` block with `url: "file:///attacker/repo"` clones an attacker-controlled local path, which is then added to Python's import machinery via ESPHome's component loader, executing arbitrary Python code when the YAML configuration is processed (e.g. via `esphome config`/`esphome run`).

### CVE-2026-71255

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-05T12:18:57.727 |

nanoMODBUS through v1.23.0 contains an out-of-bounds write in the Modbus client-side recv_read_device_identification_res() function (FC 0x2B/MEI 0x0E, Read Device Identification) in nanomodbus.c. The server-supplied object_length field (0-246) is validated only against the remaining PDU size (res_size_left) and is never validated against the caller-supplied buffers_length parameter. After copying data with strncpy(buffers_out[buf_index], str, buffers_length), the code unconditionally writes a NUL terminator at buffers_out[buf_index][object_length]. When a malicious or compromised Modbus server sends a response with object_length greater than or equal to the client's buffers_length, this NUL write lands past the end of the caller-provided buffer, corrupting adjacent stack or heap memory on the client.

### CVE-2026-18830

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1287` |
| Published | 2026-08-04T18:16:49.420 |

Insufficient input validation in Amazon Bedrock AgentCore harness might allow an authenticated remote user to execute configured tools bypassing model invocation and security controls via crafted content blocks in conversation messages. AWS has addressed this issue. No customer action is required.

### CVE-2026-58074

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-04T17:16:57.067 |

A vulnerability allowing a high-privileged user to execute arbitrary code on the server.

### CVE-2026-71280

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-05T13:24:52.573 |

go-shiori's DownloadBookmark() (internal/core/download.go) fetches a caller-supplied bookmark URL using a plain http.Client with no custom DialContext or destination-IP validation (no IsLoopback(), IsPrivate(), IsUnspecified(), or IsLinkLocalUnicast() checks). An authenticated user creating or updating a bookmark via POST /api/bookmark, PUT /api/v1/bookmarks/cache, or POST /api/bookmarks/ext can supply a loopback (127.0.0.1) or 0.0.0.0 (which Linux redirects to loopback) URL, causing the server to make outbound requests to internal-only services, cloud metadata endpoints, or other network-restricted resources.

### CVE-2026-71274

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-05T13:24:51.850 |

OpenBK7231T's CHANNEL_SetLabel() (src/cmnds/cmd_channels.c) stores channel labels received via the MQTT SetChannelLabel command using strdup() with no HTML sanitization. CHANNEL_GetLabel() returns these labels unsanitized, and they are rendered via hprintf255() at 15+ locations in src/httpserver/http_fns.c with no HTML encoding. An attacker with MQTT broker access (commonly unauthenticated in real deployments) can set a channel label containing a <script> payload that executes when any user views the device's web panel.

### CVE-2026-71272

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-05T13:24:51.573 |

Memos' webhook dispatch function safeDialContext() (internal/webhook/webhook.go) resolves the target hostname via net.DefaultResolver.LookupHost() and validates the resulting IPs against reserved ranges, but then dials net.JoinHostPort(host, port) using the original hostname rather than the already-validated IP address. Because net.Dialer.DialContext() performs its own independent DNS resolution, an attacker controlling DNS for the webhook's hostname (e.g. via a short TTL) can return a public, allowed IP during validation and a different, internal IP at dial time — a classic time-of-check/time-of-use DNS-rebinding bypass of the SSRF protection.

### CVE-2026-71271

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-05T13:24:51.447 |

Memos' webhook URL validation, isReservedIP() (internal/webhook/validate.go), checks a candidate IP against a reservedCIDRs list that omits 0.0.0.0/8 and never calls ip.IsUnspecified() — unlike the correctly implemented sibling function isInternalIP() in internal/httpgetter/html_meta.go, which does. Because Linux redirects connections to 0.0.0.0 to loopback (127.0.0.1), an attacker registering a webhook URL of http://0.0.0.0:PORT/ bypasses the reserved-IP check and causes the Memos server to make outbound HTTP requests to its own loopback interface, exposing internal-only services.

### CVE-2026-65986

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-434` |
| Published | 2026-08-04T21:16:36.990 |

CVAT is an open source interactive video and image annotation tool for computer vision. Versions 2.5.0 through 2.66.0 contain a XSS vulnerability that can be accessed through annotation guide assets. When CVAT serves the files attached to an annotation guide, it labels them with a media type ( Content-Type ) that the attacker can influence, so instead of treating an uploaded file as plain data, the victim's browser can be told to treat it as an HTML page and run any JavaScript inside it. This issue has been fixed in version 2.67.0.

### CVE-2026-18657

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-04T20:16:50.570 |

An uncontrolled search path element in Kiro CLI before version 2.10.0 on Windows might allow a remote unauthenticated actor to execute arbitrary code via a maliciously crafted project directory containing an executable that bypasses workspace trust protections when a local user starts Kiro CLI in the directory.



To remediate this issue, users should upgrade to version 2.10.0 or higher.

### CVE-2026-18656

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-04T20:16:50.410 |

An uncontrolled search path element in Kiro IDE before version 1.0.228 on Windows might allow a remote unauthenticated actor to execute arbitrary code via a maliciously crafted project directory containing an executable that bypasses workspace trust protections when a local user opens the directory.



To remediate this issue, users should upgrade to version 1.0.228 or higher.

### CVE-2026-64631

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-04T17:16:58.093 |

A vulnerability allowing a low-privileged user to inject SQL and extract database contents.

### CVE-2026-69250

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-04T15:16:44.277 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, the OAuth2 token refresh endpoint POST /api/v1/oauth2-credential/refresh/:credentialId is unauthenticated by design and performs a server-side HTTP request to the credential-controlled accessTokenUrl without SSRF protections. Runtime validation confirmed that the endpoint was reachable without authentication, triggered outbound POST requests to an attacker-controlled server, reflected the full remote response body to the caller through tokenInfo, and sent client_id, client_secret, grant_type=refresh_token, and refresh_token in the request body. This issue is fixed in version 3.1.3.

### CVE-2026-66839

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-08-05T06:16:38.980 |

NetKids iMark, provided by Integrated Systems Technologies, Inc., contains an Unquoted Search Path or Element vulnerability (CWE-428). An authenticated attacker may exploit this vulnerability to execute arbitrary code with SYSTEM privileges.

### CVE-2026-47781

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-829` |
| Published | 2026-08-04T19:16:51.240 |

PDM is a Python package and dependency manager. In versions up to and including 2.26.9, PDM automatically loads project-local plugins from a .pdm-plugins directory during initialization, allowing an attacker-controlled file in an untrusted repository checkout to execute arbitrary Python code before any command is parsed. This happens because load_plugins() runs during Core.init() and adds .pdm-plugins via site.addsitedir(), which processes .pth files and immediately executes any line beginning with import, so the code runs with the privileges of the user invoking pdm and even a benign command such as pdm --version triggers it (making the impact strongest in CI, automation, and privileged contexts). The issue is fixed in version 2.27.0.

### CVE-2026-47764

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-04T19:16:51.093 |

pdm is a Python package and dependency manager supporting the latest PEP standards. Versions prior to 2.27.0 are vulnerable to path traversal through write_to_fs. InstallDestination.write_to_fs() in src/pdm/installers/installers.py overrides the base class to add symlink/hardlink support but replaces the safe _path_with_destdir() (which validates via Path.resolve() + is_relative_to()) with a bare os.path.join() that performs no path validation. A malicious wheel with traversal entries can write arbitrary files. This issue has been fixed in version 2.27.0.

### CVE-2026-64634

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-04T17:16:58.347 |

A vulnerability allowing local privilege escalation to the Reporter service context.

### CVE-2026-71242

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-05T11:16:27.123 |

Crater's NotePolicy checks only a blanket Bouncer ability (manage-all-notes / view-all-notes) with no company-ownership comparison, unlike InvoicePolicy and other sibling policies which additionally verify $user->hasCompany($model->company_id). NotesController's show(), update(), and destroy() actions authorize via $this->authorize('view notes'/'manage notes') without passing the target Note model, and Note's company-scoping (scopeWhereCompany) is applied only in the list endpoint, not in show/update/destroy. Any authenticated user of one company can read, edit, or delete another company's notes by ID. This is a distinct finding from the previously reported CustomerPolicy company-ownership omission (a different policy class and controller).

### CVE-2026-71206

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-613` |
| Published | 2026-08-05T08:16:42.587 |

Shiori's CheckToken function (internal/domains/auth.go) validates only the JWT's HMAC signature and returns the embedded claims.Account object unmodified, never re-fetching the account from the database. No session store or token-revocation mechanism exists in the codebase. Deleting an account or demoting it from owner to a regular role has no effect on tokens already issued to that account — a deleted or demoted owner's token continues authenticating with its original owner-level privileges until natural expiry, which can be up to 30 days with 'remember me' enabled.

### CVE-2026-55739

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-05T08:16:33.903 |

Crater isolates data per company_id, and its Invoice/Estimate/Payment/Expense policies enforce both a Bouncer ability check and $user->hasCompany($model->company_id). CustomerPolicy's view/update/delete methods omit the company-ownership check entirely, checking only the blanket ability. Route-model-bound customer lookups and the bulk Customer::deleteCustomers() method are similarly unscoped (self::find($id) with no company filter). Any authenticated user of one company can read, reassign (steal), or delete another company's customer records, with deletion cascading to that customer's invoices and payments.

### CVE-2026-70476

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-639` |
| Published | 2026-08-04T20:16:54.330 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, several organization billing endpoints in packages/server/src/enterprise/routes/organization.route.ts and packages/server/src/enterprise/controllers/organization.controller.ts accept attacker-controlled Stripe subscriptionId values without verifying that the identifier belongs to the authenticated user's organization. An authenticated attacker can perform unauthorized Stripe subscription operations on other tenants, including changing subscription plans or modifying seat quantities, resulting in financial impact and service disruption. This issue is fixed in 3.1.3.

### CVE-2026-70473

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-202;CWE-862` |
| Published | 2026-08-04T19:16:54.830 |

Flowise is a drag-and-drop user interface for building customized large language model (LLM) flows. Prior to 3.1.3, Flowise GET /api/v1/upsert-history returns the entire server-wide upsert history instead of being scoped to the requesting user, tenant, or workspace. The response can exceed 100MB and includes sensitive configuration data, including Vector Store settings such as Qdrant Server URL and collection name. The observed behavior indicates missing or insufficient authorization checks, workspace/project/tenant isolation, and pagination or limits, exposing integration parameters and infrastructure details that may enable further targeted attacks. This issue is fixed in version 3.1.3.

### CVE-2026-71264

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T13:24:50.600 |

WLED's GET /json/cfg endpoint (registered in wled00/wled_server.cpp) calls serveJson() with no settings-PIN check, unlike the /edit endpoint which explicitly checks correctPIN, disclosing the device's general configuration (network, hardware, LED setup) to any unauthenticated client on the network. Separately, the settings-PIN unlock state is tracked via a single global boolean `correctPIN` (wled00/wled.h), not per-session state: once any single client submits the correct 4-digit PIN via POST /json, correctPIN becomes true for every client, granting all subsequent unauthenticated clients full configuration-write access (OTA firmware updates, WiFi reconfiguration, factory reset) until the device reboots.

### CVE-2026-71252

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T11:16:28.383 |

toner-management's admin state-changing handlers (add.php, edit.php, delete.php under admin/toners, admin/toner-brands, admin/printers, and related admin subdirectories) executed INSERT/UPDATE/DELETE database operations with no authentication or authorization check, while access control was enforced only in listing views. An unauthenticated remote attacker could invoke these handlers directly to create, modify, or destroy application data. The vendor has since merged a fix requiring an authenticated admin session before any such handler proceeds.

### CVE-2026-6627

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T08:16:41.280 |

The WPFormify – Stripe Payments with Form and Checkout plugin for WordPress is vulnerable to unauthorized modification and deletion of Stripe payment credentials in all versions up to, and including, 1.1.1. This is due to missing capability checks and nonce verification on the `wpf_stripe_callback_success()` and `wpf_stripe_disconnect()` functions, both hooked to `admin_init`. The `admin_init` hook fires on `admin-post.php` which is accessible without authentication. This makes it possible for unauthenticated attackers to overwrite the site's Stripe API credentials with attacker-controlled values (redirecting payments to the attacker's Stripe account) or disconnect the Stripe integration entirely by deleting the stored credentials.

### CVE-2026-70486

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-1021` |
| Published | 2026-08-04T20:16:55.747 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.9.0 until 0.11.0, the terminal file-preview serveUrl iframe branch always granted allow-same-origin together with allow-scripts for HTML files served from the application origin. Any authenticated user with access to a configured terminal server could cause script in a previewed file to run in the Open WebUI origin, read the victim's session token from localStorage, and take over the account, with possible server-side code execution if the victim was an admin or held workspace.functions. This issue is fixed in 0.11.0.

### CVE-2026-47623

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-04T18:16:51.983 |

NVIDIA Dynamo for Linux contains a vulnerability where an attacker could cause deserialization of untrusted data. A successful exploit of this vulnerability might lead to denial of service and data tampering.

### CVE-2026-24253

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-04T18:16:49.767 |

NVIDIA Dynamo for Linux contains a vulnerability where an attacker could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to denial of service and data tampering.

### CVE-2026-58071

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-04T17:16:56.463 |

A vulnerability in Veeam Service Provider Console allowing an unauthenticated attacker to access the proxied appliance API asPortal Administrator during a short window after an administrator session begins.

### CVE-2026-15979

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-05T14:17:03.547 |

The Content Egg – Affiliate Product Importer & Price Comparison plugin for WordPress is vulnerable to Arbitrary File Deletion via Path Traversal in versions up to and including 11.3.0. This is due to insufficient validation of the 'img_file' field within the cegg_data post metadata: the value passes only through wp_strip_all_tags() (which does not strip path traversal sequences), is stored directly in post meta, and is later concatenated without normalization into a filesystem path in getFullImgPath() before being passed to PHP's unlink(). This makes it possible for authenticated attackers, with author-level access and above, to delete arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-71285

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-05T13:24:53.210 |

Uptime Kuma's Matomo analytics integration (server/analytics/matomo-analytics.js) injects the admin-configurable Matomo `siteId` value as a bare, unquoted JavaScript expression inside a <script> block rendered on every public status page: `_paq.push(['setSiteId', ${escapedSiteIdHTMLAttribute}]);`. The escaping pipeline used (jsesc with isScriptContext:true, then html-escaper.escape()) does not escape the characters `]`, `)`, `;`, `(`, which are sufficient to break out of the array/push expression context. A siteId value such as `1]);alert(document.cookie)//`, once saved by an editor/admin, executes arbitrary JavaScript for every unauthenticated visitor of the public /status/<slug> page, enabling session-cookie theft and full page takeover.

### CVE-2026-71239

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-05T11:16:26.750 |

DjangoCRM's massmail module renders user-controlled EmlMessage fields (subject, content) through Django's Template() constructor with no sanitization, in at least three locations: message_previews.py builds an f-string embedding message.subject/message.content directly into a Template() call; email_creators.py passes eml_message.subject directly as a template string to Template(); and helpers.py contains the same f-string interpolation pattern. An authenticated user with mass-mail message edit rights can inject Django template syntax ({{ }} / {% %}) that executes at render time, enabling disclosure of other users' data and password hashes via request context variables, CSRF token forgery, and inclusion of arbitrary registered templates.

### CVE-2026-7520

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T08:16:44.560 |

The MailChimp Forms by MailMunch plugin for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the `sign_in()` and `sign_up()` AJAX handlers in all versions up to, and including, 3.2.7. This makes it possible for authenticated attackers, with Subscriber-level access and above, to relink the site's MailMunch integration to an attacker-controlled MailMunch account by submitting attacker-supplied credentials. Once relinked, all subscriber data captured by the plugin's forms is delivered to the attacker, and the forms/landing pages rendered on the site are pulled from the attacker's MailMunch account.

### CVE-2026-7444

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-05T08:16:44.400 |

The Search Analytics for WP plugin for WordPress is vulnerable to Cross-Site Request Forgery in all versions up to, and including, 1.4.16. This is due to missing or incorrect nonce validation on the `process_bulk_action()` function of `MWTSA_Stats_Table`. This makes it possible for unauthenticated attackers to delete arbitrary search-term records, including all associated search-history rows, via a forged request granted they can trick a user with access to the plugin's "Search Analytics" dashboard page (Administrator by default) into performing an action such as clicking on a link.

### CVE-2026-54418

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T08:16:33.777 |

Leantime through 3.6.2 exposes the JSON-RPC methods leantime.rpc.TwoFA.TwoFA.getSetupData, saveSecret, verifyAndEnable, and disable2FA, which act on a caller-supplied userId parameter with no ownership check, session pinning, or permission-attribute gate (unlike other RPC-exposed methods in the same dispatcher). Any authenticated user can invoke getSetupData with an arbitrary userId to read that user's live TOTP secret, or disable2FA to strip another account's two-factor authentication entirely, fully defeating account-level 2FA protection. This is related to CVE-2026-15509, which covers a similar missing-authorization pattern in the JSON-RPC editUser/addUser role-assignment path in the same application; the TwoFA service methods addressed here are a distinct, independently fixable set of RPC endpoints.

### CVE-2026-70494

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862;CWE-863` |
| Published | 2026-08-04T21:16:38.470 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.10.0 until 0.11.0, the DELETE /api/v1/folders/{id} handler in backend/open_webui/routers/folders.py allowed a user granted write access to a shared chat folder to permanently delete chats and messages belonging to the folder owner. The cascade following the authorization check is bound to the folder owner's id, but the subfolder check accepted any inherited write grant instead of requiring ownership or administrator status. A collaborator can destroy the owner's subtree or force-move chats out of it when delete_contents=false. This issue is fixed in 0.11.0.

### CVE-2026-70482

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-04T20:16:55.190 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.8.0 until 0.11.0, when ENABLE_OAUTH_TOKEN_EXCHANGE=True, /oauth/{provider}/token/exchange accepts a raw provider access token and validates it by calling the provider userinfo endpoint without confirming which OAuth client the token was issued to. Anyone holding an access token minted for any client registered with the same provider could exchange it for an Open WebUI session as that token user, including applications the operator does not control and has never authorized. This issue is fixed in 0.11.0.

### CVE-2026-24079

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-04T16:16:23.453 |

Cryptographic Issue while processing registration requests with malformed or missing authentication parameters.

### CVE-2026-71279

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-05T13:24:52.437 |

Zigbee2MQTT's ExternalJSExtension.getFilePath() (lib/extension/externalJS.ts) joins a `name` parameter received via an MQTT message (topic zigbee2mqtt/bridge/request/extension/save) into the extensions base path using path.join(basePath, name) with no sanitization. Because path.join() resolves `../` sequences, a name such as `../../tmp/evil.js` escapes the intended extensions directory. The extension handler only validates that the name ends in .js/.mjs/.cjs, writes the file, and then dynamically imports it via Node.js import(), achieving remote code execution. Requires the `enable_external_js` config option (off by default, but commonly enabled in legacy installs) and MQTT broker access, which is frequently unauthenticated in real deployments. The identical unsanitized getFilePath() is also used by the extension-removal handler, enabling arbitrary file deletion.

### CVE-2026-71266

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-05T13:24:50.843 |

tinyobjloader-c's tinyobj_parse_and_index_mtl_file() (tinyobj_loader_c.h) reads each line of a .mtl material file into a fixed 4096-byte stack buffer `linebuf` via memcpy(linebuf, p, p_len), guarded only by `assert(p_len < 4095)`. Because assert() compiles to a no-op under -DNDEBUG (standard for release builds), a crafted .mtl file containing a line (e.g. a "newmtl" material name) longer than 4096 bytes overflows linebuf into the adjacent stack variable namebuf and beyond, corrupting the stack of any application that loads attacker-supplied 3D model/material files. The identical vulnerable pattern is duplicated in a second function in the same file.

### CVE-2026-71261

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-05T13:24:50.233 |

dr_libs dr_wav.h (all versions through current master) contains an integer overflow in W64 CUE chunk metadata parsing. In drwav__metadata_process_chunk(), a stage-1 capacity estimate truncates the 64-bit W64 chunk sizeInBytes to size_t before dividing by DRWAV_CUE_POINT_BYTES; on 32-bit builds this truncation causes the pre-allocated extra metadata capacity to be computed incorrectly. The subsequent read in drwav__read_cue_to_metadata_obj() computes the actual cue point count and allocation size using the full-precision, attacker-controlled cuePointCount field without cross-checking it against the stage-1 capacity estimate, and the only bounds enforcement on the resulting memory region (drwav__metadata_get_memory()) is a DRWAV_ASSERT, which compiles to a no-op under -DNDEBUG (the default for release builds). A crafted W64 WAV file can therefore cause a heap buffer overflow in any 32-bit application parsing untrusted WAV metadata.

### CVE-2026-16022

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-05T13:20:39.450 |

@oblique/cli 15.4.0 contains an OS command injection vulnerability in the project creation functionality. The CLI constructs shell commands through string concatenation and executes them with execSync(). A user-controlled project-name argument is inserted into the shell command without proper neutralization, allowing shell metacharacters to execute additional operating-system commands when the CLI is invoked with a crafted project name.

### CVE-2026-24083

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-08-04T16:16:24.123 |

Memory Corruption while processing IOCTL device driver requests with invalid arguments.

### CVE-2026-24080

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-04T16:16:23.770 |

Memory Corruption when handling malformed request parameters in the fingerprint TA.

### CVE-2026-21366

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-04T16:16:22.780 |

Memory corruption while processing a packet with a size close to the maximum allowed value.

### CVE-2026-70479

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-04T20:16:54.760 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.9.6 until 0.11.0, with WEB_LOADER_ENGINE=playwright, the Playwright web loader validates only the top-level page request and lets sub-resource requests pass unvalidated. A page supplied by an authenticated user can use JavaScript to reach blocked internal addresses, and returned DOM can include data read from those addresses in web-search or RAG output. This issue is fixed in 0.11.0.

### CVE-2026-71294

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-05T13:24:54.180 |

Cotonti CMS's Comments plugin deserializes user-supplied data without restricting the classes that may be instantiated. In plugins/comments/controllers/actions/CreateAction.php, a `ci` POST parameter obtained via `cot_import('ci', 'P', 'TXT')` (trim-only sanitization) is passed to `unserialize(base64_decode($ci))` with no `allowed_classes` restriction, reachable by any member with write access to comments (the default `Auth_members => 'RW'` setting in plugins/comments/comments.setup.php). In plugins/comments/controllers/actions/EditAction.php, a `cb` parameter is similarly deserialized via `unserialize(base64_decode($this->comeback))` in prepareComeBack(), reachable by any member editing their own comment. Because unserialize() is called without allowed_classes, an attacker can construct a serialized PHP object of any class loaded by Cotonti (a PHP Object Injection primitive). This was demonstrated in practice using Cotonti's own MySQL_cache class: a crafted serialized MySQL_cache object, once deserialized and later garbage-collected, triggers its __destruct()->flush() chain, causing an attacker-controlled INSERT INTO cot_cache with attacker-chosen row values — confirming genuine POP-chain exploitation, with further impact (including potential RCE) contingent on other gadget chains available in a given Cotonti installation's loaded classes. A third sink in DeleteAction.php contains the identical unserialize() pattern but is gated behind an admin-only authorization check and is not reachable by ordinary members.

### CVE-2026-70474

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-04T19:16:54.977 |

Flowise is a drag-and-drop user interface for building customized large language model (LLM) flows. Prior to 3.1.3, Flowise has three OAuth2 credential endpoints that look up credentials by id alone with no workspaceId filter. The authorize, callback, and refresh handlers query the Credential table by id only; callback and refresh are whitelisted from authentication. This allows any authenticated user to initiate OAuth2 flows against credentials belonging to other workspaces, allows an unauthenticated attacker to forge OAuth2 callbacks to overwrite tokens in any credential, and allows an unauthenticated attacker to refresh tokens for any credential. The affected routes include /api/v1/oauth2-credential/authorize/<VICTIM_CREDENTIAL_UUID>, /api/v1/oauth2-credential/callback?code=ATTACKER_AUTH_CODE&state=<VICTIM_CREDENTIAL_UUID>, and /api/v1/oauth2-credential/refresh/<VICTIM_CREDENTIAL_UUID>. This issue is fixed in version 3.1.3.

### CVE-2026-69257

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918;CWE-1389` |
| Published | 2026-08-04T17:17:00.840 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, Flowise's HTTP security module httpSecurity.ts did not normalize IPv4-mapped IPv6 addresses such as ::ffff:127.0.0.1 and ::ffff:169.254.169.254 before checking them against the deny list. Because ipaddr.js reports these addresses as ipv6 while IPv4 CIDR deny-list entries are ipv4, isDeniedIP() skipped the IPv4 CIDR checks. An attacker who controls DNS resolution for a hostname used by the HTTP Node, API Chain, Document Loader, MCP tool, or other paths using secureAxiosRequest(), secureFetch(), or checkDenyList() could return a AAAA record for an IPv4-mapped target and cause requests to reach localhost, internal services, or cloud metadata endpoints. This issue is fixed in version 3.1.3.

### CVE-2026-25292

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:P/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1286` |
| Published | 2026-08-04T16:16:25.183 |

Memory Corruption when processing untrusted user input in the fastboot command handler for audio framework configuration.

### CVE-2026-7529

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T14:17:15.237 |

The wiseCampaign – WooCommerce Conversions Made Easy plugin for WordPress is vulnerable to unauthorized modification and disclosure of data due to every one of its REST API endpoints being registered with `permission_callback => '__return_true'` in all versions up to, and including, 1.1.16. This makes it possible for unauthenticated attackers to read and modify the plugin's banner, stockbar, and core settings — including saving/updating banner records, toggling stockbar/feature flags, changing the active banner, and uploading background-image files via wp_handle_upload() — without any nonce or capability check.

### CVE-2026-71265

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-05T13:24:50.720 |

Domoticz's MochadTCP::MatchLine() handler for MOCHAD_RFSEC messages (hardware/MochadTCP.cpp) copies network-received data from the up-to-1028-byte m_mochadbuffer into a fixed 50-byte stack buffer tempRFSECbuf using strcpy() with no length check, across three separate code branches (DS10A/KR10A/MS10A device types). An attacker on the local network segment able to reach the Mochad TCP bridge (default port 1099, no authentication) can send a crafted packet that overflows tempRFSECbuf by up to several hundred bytes, corrupting the Domoticz worker thread's stack.

### CVE-2026-61891

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-36;CWE-200;CWE-306` |
| Published | 2026-08-05T12:18:57.310 |

In Eclipse Theia versions up to and including 1.73.1, the `@theia/filesystem` backend exposes HTTP file-download endpoints (`GET /file`, `GET /files/`, `PUT /files/`) that convert a client-supplied URI directly to a filesystem path and stream the file, without confining it to the workspace or any allow-listed root. In browser (non-Electron) deployments the connection token is enforced only on WebSocket upgrades; the HTTP middleware in `@theia/core` re-issues the cookie and calls `next()` without rejecting tokenless HTTP requests, so these endpoints are reachable without a valid token. As a result an unauthenticated client can read any file readable by the backend process, including files outside the opened workspace (for example `/etc/hosts`, SSH keys, or tokens). Electron mode uses a separate `ElectronSecurityToken` and is not affected via this path.

### CVE-2026-71241

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-05T11:16:26.997 |

Book-Management-System's Flask API endpoints /student, /record, /books, /find_stu_book, and /find_not_return_book are missing the @login_required decorator that protects sibling routes (/search_student, /storage) in the same file. This allows any unauthenticated remote user to retrieve student PII (name, gender, card validity, debt status) and full book-borrowing history by supplying a card_id. Because card_id values are sequential integers, the entire student database can be enumerated without authentication.

### CVE-2026-71234

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-05T11:16:26.120 |

Documize Community's attachment download route (domain/attachment/endpoint.go, Download function, registered via AddPublic with no auth middleware) accepts a `secure` query parameter and grants access whenever the parameter is simply non-empty (len(secureToken) > 0), without comparing it to any server-stored value. Any non-empty string, such as ?secure=x, bypasses authentication entirely and allows downloading any organization's attachments. Sibling handlers in the same file (togglePublish, delete) correctly enforce session-based authorization, confirming this is an inconsistency rather than intended design.

### CVE-2026-12609

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-05T11:16:24.080 |

In Eclipse Theia versions 1.66.0 and up until including 1.73.1, the `@theia/plugin-ext` backend exposes the `/hostedPlugin/:pluginId/:path(*)` HTTP endpoint, which resolves the requested file path with `path.resolve(localPath, filePath)` without verifying that the resolved path stays within the plugin's directory. An unauthenticated network attacker can send percent-encoded `../` sequences (`%2e%2e%2f`) that decode into the path parameter and escape the plugin directory, allowing arbitrary files readable by the Theia backend process to be retrieved. Plugin IDs are derived deterministically from a plugin's publisher and name, so built-in plugins serve as reliable anchors that require no prior knowledge of the target system.

### CVE-2026-71215

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-05T08:16:43.940 |

art-template's sub-template resolution logic (src/compile/adapter/resolve-filename.js), used by both the include() and extend() template directives, resolves the target file path via path.resolve(root, filename) with no check afterward that the result remains inside root. Because path.resolve() discards root entirely when filename is an absolute path, and does not block '../' traversal sequences, and the resolved path is passed directly to fs.readFileSync() in loader.js with its contents compiled and rendered, an application that lets a sub-template name be influenced by external input (e.g. a query parameter passed into {{include page}}) allows an attacker to read arbitrary files on disk that the Node process can access.

### CVE-2026-71209

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-05T08:16:43.110 |

audiobookshelf's authentication-exemption check (server/routers/Auth.js) matches unauthenticated-allowed GET routes against req.path via a regex requiring a literal /items/:id/cover or /authors/:id/image shape, where req.path retains %2F sequences URL-encoded. Express's router decodes the :id route parameter before handler code runs, so a %2F-encoded '../' sequence in :id (e.g. ..%2f..%2f..%2ftmp%2fpwned) passes the literal-path auth-exemption check while resolving to a real path-traversal payload once decoded. CacheManager.handleCoverCache then joins this decoded value into a cache file path and streams the result before any database-backed ownership check. This bypasses the fix applied for CVE-2025-25205 (which anchored the exemption regex and switched it to req.path) and results in unauthenticated arbitrary file read of any file matching the pattern *_<width>[x<height>].<ext> that the service account can read.

### CVE-2026-71202

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-08-05T08:16:42.080 |

The raster Rust crate's crop() function (src/editor.rs) clamps the crop width/height against source dimensions but only clamps the offset_x/offset_y parameters against 0, never against the source width/height. When an offset exceeds the corresponding source dimension, `width2 - offset_x` (or the height equivalent) underflows to a negative i32, which release builds do not trap; the negative value is then cast to usize inside Image::blank()'s Vec::with_capacity() call, triggering a capacity-overflow panic and crashing the process on a single crafted crop request.

### CVE-2026-70378

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1284` |
| Published | 2026-08-05T08:16:41.957 |

imagecli's `carve <ratio>` pipeline operation (Carve::apply() in src/image_ops.rs) only asserts `ratio <= 1.0`, never validating that the ratio is positive. A negative ratio (e.g. -5) causes the computed target width to saturate to 0 via Rust's defined float-to-uint cast, which is then passed to imageproc::seam_carving::shrink_width — a function that panics when given a width below 2, crashing the process. This shares the same missing-input-validation root cause as the sibling `scale` finding in the same file but is an independently fixable, distinct code path.

### CVE-2026-70377

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-05T08:16:41.830 |

imagecli's `scale <ratio>` pipeline operation (Scale::apply() in src/image_ops.rs) computes output width/height as (dimension as f32 * ratio) as u32 with no upper-bound validation on the CLI-supplied ratio, which is parsed via nom::number::complete::float with no range check. A large ratio (e.g. 100000) causes an attempted allocation of hundreds of terabytes, aborting the process. Any application embedding imagecli as a library and accepting user-controlled pipeline strings is remotely crashable with a single request.

### CVE-2026-6639

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T08:16:41.427 |

The AI Chatbot & Workflow Automation by AIWU plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 1.4.6. This is due to the `getCurrentTaskResults()` method in `modules/workspace/controller.php` being accessible without authentication or authorization checks. The method is not included in the workspace controller's `getNoncedMethods()` array, the base `getPermissions()` returns an empty array, and all AJAX actions are registered with `wp_ajax_nopriv_` hooks (`classes/frame.php:282`). When tasks are created via features like the Bulk Post Generator, the task parameters — including the OpenAI API key in plaintext, AI prompts, keywords, and full AI model configuration — are stored in the database and returned in the JSON response. This makes it possible for unauthenticated attackers to enumerate sequential task IDs and retrieve sensitive configuration data including API keys.

### CVE-2026-59675

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-05T08:16:34.593 |

When API audit logging is enabled, the middleware reads the entire HTTP request body into memory without enforcing a size limit on login endpoints. Because the audit middleware is positioned earlier in the handler chain than Rancher's APIBodyLimitingHandler, the body-size cap (default 1 MiB) is bypassed for requests that pass through the audit copyReqBody path. An unauthenticated attacker can send arbitrarily large request bodies to the public login endpoints, causing the Rancher Manager server process to allocate memory proportional to the supplied body size. With just a few concurrent connections, this can exhaust available memory and terminate the Rancher Manager plane process, making the Rancher API and UI unavailable and interrupting management of all downstream clusters.

### CVE-2026-18881

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T08:16:32.750 |

The TableOn – WordPress Posts Table Filterable plugin for WordPress is vulnerable to blind SQL Injection via the `filter_data[comment_count]` parameter of the public `tableon_get_table_data` AJAX action in all versions up to, and including, 1.0.5.1. This is due to insufficient escaping on the user-supplied parameter and lack of sufficient preparation on the existing SQL query — the value is split on `:` and both halves are interpolated directly into a `posts_where` SQL clause without `intval()` casting or `$wpdb->prepare()`. This makes it possible for unauthenticated attackers to append additional SQL queries into the already-existing query that can be used to extract sensitive information from the database (researcher demonstrated extraction of database(), wp_users.user_login, and wp_users.user_pass).

### CVE-2026-12000

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T08:16:30.367 |

The Page and Post Restriction plugin for WordPress is vulnerable to Sensitive Information Exposure in versions up to and including 1.4.0 via the WordPress core REST endpoints /wp-json/wp/v2/pages, /wp-json/wp/v2/pages/<id>, /wp-json/wp/v2/posts, and /wp-json/wp/v2/posts/<id>. This is due to the plugin's REST guards — papr_restrict_page_post_rest_api() and the the_posts filter registered by papr_filter_posts() — sourcing their restricted-ID list exclusively from papr_get_restricted_posts_id(), which only reads the per-page metabox options papr_allowed_redirect_for_pages and papr_allowed_redirect_for_posts and never consults the two global toggles papr_access_for_only_loggedin and papr_access_for_only_loggedin_posts that the plugin's own UI describes as 'Make all Pages Private' / 'Make all Posts Private'. This makes it possible for unauthenticated attackers to read the full rendered content of every published page and post on sites configured with the documented global toggles, bypassing the security boundary enforced on the frontend by papr_restrict_logged_in_users().

### CVE-2026-15918

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T06:16:36.587 |

VikAppointments Service Booking Calendar wordpress plugin is vulnerable to unauthenticated SQL injection due to one of the parameters that controls how the public reviews list is sorted is taken from the incoming request and used to build a database query without proper validation or sanitization. Because this value is placed directly into the query, an attacker who is not logged in can inject arbitrary SQL through a normal booking page and read data from the site's database — including sensitive information such as WordPress user credentials. No authentication or special privileges are required

### CVE-2026-67861

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-04T22:17:16.460 |

An issue in open62541 v.1.5.5 and before allows a remote attacker to cause a denial of service via the UA_Client_getRemoteDataTypes component

### CVE-2026-67859

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-04T22:17:16.223 |

Buffer Overflow vulnerability in open62541 v1.5.5 allows a remote attacker to cause a denial of service via the Discovery/LDS handling.

### CVE-2026-67858

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-04T22:17:16.087 |

Buffer Overflow vulnerability exists in open62541 1.5.5 when the Local Discovery Server (LDS) is built with multicast discovery enabled through the MDNSD backend. An unauthenticated remote attacker can send a RegisterServer or RegisterServer2 request containing many unique discoveryUrls. This allows remote attackers to cause a denial of service.

### CVE-2026-67857

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-04T22:17:15.957 |

open62541 1.5.5 contains an out-of-bounds read in the client-side function responseReadNamespacesArray() in src/client/ua_client_connect.c.

### CVE-2026-45103

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-04T22:17:14.847 |

OpenSIPS is a Session Initiation Protocol (SIP) server implementation. In versions prior to 3.6.6 and 4.0.0-rc1, the TCP message framing layer parses the Content-Length header using unsigned int arithmetic with no overflow check. When an attacker sends a Content-Length value that overflows unsigned int (e.g., 4294967296), the framing layer computes a wrapped-around value (e.g., 0) and splits the TCP stream at the wrong boundary, causing the body of the first SIP message to be processed as a separate message and enabling SIP message smuggling. Because Content-Length is parsed in the transport layer before authentication, an unauthenticated, network-based attacker can smuggle arbitrary SIP messages over any TCP-based transport (proto_tcp, proto_tls, proto_ws, proto_wss) on any instance with TCP enabled, with no routing-script preconditions. This allows smuggled messages to bypass front-end SBC/proxy security policies, inherit the connection's authentication context, and evade rate limiting. This issue has been fixed in versions 3.6.6 and 4.0.0-rc1.

### CVE-2026-47618

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-04T18:16:51.367 |

NVIDIA Dynamo for Linux contains a vulnerability in the Rust multimodal media fetcher where an attacker could cause server-side request forgery. A successful exploit of this vulnerability might lead to information disclosure.

### CVE-2026-47617

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-04T18:16:51.250 |

NVIDIA Dynamo for Linux contains a vulnerability in the multimodal media fetcher where an attacker may cause server-side request forgery via DNS rebinding. A successful exploit of this vulnerability might lead to information disclosure.

### CVE-2026-47616

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-04T18:16:51.120 |

NVIDIA Dynamo for Linux contains a vulnerability in the multimodal media fetcher where an attacker may cause server-side request forgery. A successful exploit of this vulnerability might lead to information disclosure.

### CVE-2026-47615

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-04T18:16:50.997 |

NVIDIA Dynamo for Linux contains a vulnerability where an attacker may cause server-side request forgery by supplying a crafted URL in a multimodal request. A successful exploit of this vulnerability might lead to information disclosure.

### CVE-2026-47614

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-04T18:16:50.877 |

NVIDIA Dynamo for Linux contains a vulnerability where an attacker may cause server-side request forgery. A successful exploit of this vulnerability might lead to information disclosure.

### CVE-2026-47613

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-04T18:16:50.750 |

NVIDIA Dynamo for Linux contains a vulnerability where an attacker may cause improper limitation of a pathname to a restricted directory by supplying a crafted local path in a multimodal request. A successful exploit of this vulnerability might lead to information disclosure.

### CVE-2026-47612

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-04T18:16:50.630 |

NVIDIA Dynamo for Linux contains a vulnerability in the image loading component where an attacker may cause improper limitation of a pathname to a restricted directory. A successful exploit of this vulnerability might lead to information disclosure.

### CVE-2026-24255

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-1023` |
| Published | 2026-08-04T18:16:50.070 |

NVIDIA Dynamo for Linux contains a vulnerability in the multimodal embedding cache, where an attacker could cause a hash collision by submitting images that share an identical pixel byte sequence but have different dimensions. A successful exploit of this vulnerability might lead to data tampering.

### CVE-2026-56848

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-04T17:16:56.207 |

A flaw in Node.js HTTP/2 handling allows `nghttp2_session_mem_send()` to be called re-entrantly while `nghttp2_session_mem_recv()` is executing, resulting in a heap-use-after-free.

This vulnerability affects Node.js **26.x**, **24.x**, and **22.x**.

### CVE-2026-24084

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-1294` |
| Published | 2026-08-04T16:16:24.370 |

Weak configuration when UE does not verify the consistency of its additional security capabilities with the replayed capabilities.

### CVE-2026-16443

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-05T14:17:03.697 |

A flaw was found in the SAML metadata import functionality of the keycloak-services component, which is the core engine for identity brokering in Red Hat Build of Keycloak. When importing identity provider metadata that lacks specific usage attributes for keys, the system incorrectly disables signature validation for SAML responses even if a signing certificate is provided. This issue allows an unauthenticated attacker to forge a SAML response and gain unauthorized access to a user account by knowing their external identifier.

### CVE-2026-18898

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-05T04:17:16.790 |

A security flaw has been discovered in UTT HiPER 1200GW up to v2.5.3-170306. This affects the function strcpy of the file /goform/ConfigAdvideo. The manipulation of the argument timestart results in stack-based buffer overflow. The attack can be launched remotely. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-18897

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-05T02:16:37.773 |

A vulnerability was identified in UTT HiPER 1250GW up to v3.2.7-210907-180535. The impacted element is the function strcpy of the file /goform/getOneApConfTempEntry. The manipulation of the argument tempName leads to stack-based buffer overflow. The attack can be initiated remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-18895

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-05T02:16:37.403 |

A vulnerability was found in UTT HiPER 1250GW up to 3.2.7-210907-180535. Impacted is the function strcpy of the file /goform/APSecurity_5g. Performing a manipulation of the argument cipher results in stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-18787

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-04T17:16:48.817 |

A vulnerability was identified in GL.iNet AX1800 up to 4.8.3. The affected element is the function remove_rule of the file /usr/share/gl-ngx/oui-rpc.lua of the component RPC Endpoint. The manipulation of the argument args.id leads to command injection. The attack is possible to be carried out remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure.

### CVE-2026-25288

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-08-04T16:16:24.693 |

Transient DOS when processing a short target wake time channel usage response frame with insufficient packet size.

### CVE-2026-71226

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-05T13:24:47.223 |

Memory Corruption via Uncanceled AIO Requests on Error: libkcapi's one-shot AIO path can return an error before all submitted IOCBs are drained, allowing later kernel writes into caller-owned output buffers.

### CVE-2026-25703

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-202;CWE-306;CWE-524` |
| Published | 2026-08-05T10:17:27.300 |

NeuVector through 5.4.9 is can potentially leak information from manager /network/graph API due to missing authentication and cached data containing sensitive information.

### CVE-2026-6079

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T08:16:40.997 |

The Material Dashboard plugin for WordPress is vulnerable to unauthorized access and modification of data due to missing capability checks on the amd_ajax_target_task_manager() function in all versions up to, and including, 1.4.10. This makes it possible for unauthenticated attackers to enumerate all scheduled tasks (potentially exposing PII), execute arbitrary tasks, and delete any task via the public_amd_ajax_handler AJAX action.

### CVE-2026-18902

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-05T06:16:37.490 |

A vulnerability was detected in H3C NX15 V100R017. Affected by this vulnerability is the function esps.wan.repeater.set/repeaterproc of the file /api/esps. Performing a manipulation of the argument my2P4key results in command injection. Remote exploitation of the attack is possible. The exploit is now public and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-18901

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-08-05T05:16:49.433 |

A security vulnerability has been detected in H3C NX15 V100R017. Affected is the function service.add of the file /api/esps of the component Web API. Such manipulation leads to exposed dangerous routine. The attack may be launched remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-18900

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-05T05:16:49.243 |

A weakness has been identified in H3C NX15 V100R017. This impacts the function file.exec of the file /api/esps of the component Backend RPC. This manipulation of the argument File causes os command injection. The attack may be initiated remotely. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure.

### CVE-2026-18814

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-04T22:17:13.750 |

A vulnerability was found in H3C NX15 V100R017. This impacts the function reload.reload_config of the file /api/esps. The manipulation results in command injection. The attack can be launched remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure.

### CVE-2026-18813

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-04T21:16:36.053 |

A vulnerability has been found in H3C NX15 V100R017. This affects the function delete of the file /api/esps. The manipulation of the argument esps.apcm.version leads to command injection. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-18812

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-04T21:16:35.890 |

A flaw has been found in H3C NX15 V100R017. The impacted element is the function esps.ipv6.wan of the file /api/esps. Executing a manipulation of the argument workMode can lead to command injection. It is possible to launch the attack remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-18811

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-04T21:16:35.730 |

A vulnerability was detected in H3C NX15 V100R017. The affected element is the function Add of the file /api/esps. Performing a manipulation of the argument esps.filter.url results in command injection. It is possible to initiate the attack remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure.

### CVE-2026-17506

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-05T14:17:04.040 |

The Independent Analytics plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 404 not_found_url tracking parameter in versions up to, and including, 2.15.0. This is due to the get_cell_content() function applying urldecode() after esc_url() when rendering the URL column for 404 entries — a sequence that allows percent-encoded HTML to pass URL validation and then be reconstructed as raw markup, which wp_kses_post() does not strip because it retains img elements and data-* attributes, and because the public REST endpoint /iawp/search accepts unauthenticated requests as long as they carry a signature that is itself embedded in public page HTML. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-71292

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T13:24:53.943 |

Subrion CMS's admin grid sorting helper, _gridGetSorting() in includes/classes/ia.base.controller.admin.php, whitelists the `dir` (ASC/DESC) request parameter via in_array(), but falls back to the raw, attacker-supplied `sort` GET parameter whenever the requested key is not present in the per-controller $_gridSorting whitelist array: `$column = isset($this->_gridSorting[$params['sort']]) ? ... : $params['sort'];`, which is then placed into `sprintf(' ORDER BY %s`%s` %s', $tableAlias, $column, $direction)` with only backtick-quoting and no escaping. Because a backtick in the payload breaks out of the identifier context, an authenticated admin session can inject arbitrary SQL (error-based via EXTRACTVALUE, or time-based via SLEEP()) to extract database contents including administrator password hashes. Most of Subrion's ~29 admin grid controllers either define no $_gridSorting whitelist at all (e.g. pages.php, transactions.php, languages.php) or an incomplete one covering only some of their sortable columns (e.g. members.php whitelists only 1 of 7 sortable fields), making the vast majority of admin grid endpoints exploitable.

### CVE-2026-71284

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-05T13:24:53.093 |

Fledge's backup-restore upload handler, upload_backup() (python/fledge/services/core/api/backup_restore.py), takes the first extracted tar member's filename (tar_file_names[0]) and builds a shell command via string formatting: `cmd = "cp {} {}".format(source, backup_path); ret_code = os.system(cmd)`. The only pre-check on the filename is a prefix/suffix match (startswith(backup_prefix), endswith(valid_extensions)), which a name such as `fledge_backup_$(id>/tmp/pwn).db` satisfies while still injecting a shell command substitution. Because os.system() invokes a shell and no quoting (shlex.quote, list-form subprocess) is applied, an admin uploading a crafted backup archive achieves arbitrary OS command execution.

### CVE-2026-71269

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-05T13:24:51.207 |

Node-RED's local-filesystem library storage module (getLibraryEntry() and saveLibraryEntry() in packages/node_modules/@node-red/runtime/lib/storage/localfilesystem/library.js), reachable via GET/POST /library/:lib/:type/*path, joins the user-supplied path parameter directly into the filesystem path via fspath.join(libDir, type, path) with no traversal sanitization, containment check, or path normalization/prefix verification. An authenticated user (including read-only-scoped tokens for the read path) can supply a path containing `../` sequences to read arbitrary files outside the library directory; a user with write access can write arbitrary files, enabling remote code execution via SSH authorized_keys or cron injection. This is a distinct, separately unpatched traversal from the previously fixed CVE-2021-21298 (Projects API).

### CVE-2026-18933

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-05T12:18:56.553 |

The wp-downloadmanager WordPress plugin, in version 1.68.11 (also affecting the 6.9.4 release line), allows an admin-privileged user (current_user_can('manage_downloads')) to upload arbitrary files via download-add.php with no extension or MIME-type validation of any kind - no wp_check_filetype_and_ext(), no validate_file(), and no extension blocklist exist anywhere in the upload handler. The destination path is additionally built by concatenating the raw, unsanitized $_POST['file_upload_to'] value with no traversal check (no ../ filtering, no basename()/realpath() applied). Since the base download path is required to live under WP_CONTENT_DIR (a web-accessible location), an uploaded PHP file lands in a web-servable path and can be directly executed, resulting in remote code execution. The plugin's own later changelog confirms these protections were absent in this version: v1.69 added file-type validation via wp_check_filetype_and_ext(), and v1.69.1 added directory-traversal protection - neither existed in 1.68.11.

### CVE-2026-71232

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-05T11:16:25.873 |

MacCMS10's admin template editor (application/admin/controller/Template.php) blocks dangerous PHP functions in template content via a blacklist regex, but the blacklist omitted exec, passthru, popen, show_source, create_function, register_shutdown_function, register_tick_function, and error_log. Combined with ThinkPHP's {if} template tag, which embeds the condition attribute directly into raw PHP (<?php if(condition): ?>), an authenticated administrator could inject a payload such as {if condition="exec('id > /tmp/pwned.txt')"}{/if} to achieve remote code execution. Fixed in commit 71ad3bb29570e110d8e973acff68040a3050ddf0 (2026-06-22), which added the missing functions to the filter.

### CVE-2026-7693

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-05T08:16:44.703 |

The Backup Migration plugin for WordPress is vulnerable to OS Command Injection in all versions up to, and including, 2.1.5.1 due to insufficient sanitization of the `file` POST parameter on the `restoreBackup()` AJAX handler. The handler applies `esc_attr()` — an HTML-context sanitizer that does not strip shell metacharacters — and concatenates the result, unquoted, into a `php-cli -f … bmi_restore <file> <remote>` command passed to `exec()`. This makes it possible for authenticated attackers, with Administrator-level access (or any user granted the plugin's `do_backups` capability) and above, to execute arbitrary OS commands as the web-server user, bypassing WordPress hardening constants such as `DISALLOW_FILE_EDIT` and `DISALLOW_FILE_MODS` that would otherwise prevent code execution from the admin UI. This is an incomplete fix of CVE-2023-7002, which patched the same pattern only in the `$_POST['url']` path of `handleQuickMigration()`; the equivalent mitigations (`rawurlencode()` + explicit shell-metachar replacement + double-quoting in `exec()`) were never applied to `$backupName`.

### CVE-2026-6020

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-08-05T08:16:40.850 |

The ShopLentor plugin for WordPress is vulnerable to arbitrary function execution via the woolentoropt/v1/custom-action REST API endpoint in all versions up to, and including, 3.3.7. This is due to the handle_action() method passing user-supplied input directly to call_user_func() without an allowlist of permitted callbacks. This makes it possible for authenticated attackers, with Administrator-level access and above, to execute arbitrary PHP callable functions via the 'callback' parameter.

### CVE-2026-54416

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-05T08:16:33.637 |

Pluck CMS through 4.7.21 restricts dangerous file uploads in its admin file-management feature using a fixed blacklist in data/inc/files.php ('.php','php3','php4','php5','php6','php7','phtml','.phtm','.pht','.ph3','.ph4','.ph5','.asp','.cgi','.phar'), checked against the last 4-5 characters of the filename. The blacklist omits the '.php8' extension. An authenticated administrator can upload a file named e.g. shell.php8, which is stored unmodified and, on servers running PHP 8.x, is executed as PHP by the web server, resulting in remote code execution.

### CVE-2026-16143

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-05T06:16:36.880 |

The VikRentItems – Flexible Rental Management System plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the customer email field of the booking checkout form in versions up to, and including, 1.2.1. This is due to insufficient input sanitization and output escaping in the saveorder() function, which stores the raw email value via VikRequest::getString() (applying only sanitize_text_field(), which does not neutralize HTML attribute-breaking characters such as double quotes), and in the editorder template which echoes the stored custmail value into an HTML input element's value attribute without esc_attr(). This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-69252

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-04T16:16:28.960 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, the /api/v1/files route was protected only by the feat:files feature gate and did not enforce checkPermission on GET or DELETE. A low-privileged authenticated API key with unrelated permissions could call GET /api/v1/files to list files under the organization storage root and DELETE /api/v1/files?path=... to delete files belonging to other workspaces in the same organization because getAllFiles and deleteFile used activeOrganizationId and a user-controlled path without restricting access by permissions or activeWorkspaceId. This issue is fixed in version 3.1.3.

### CVE-2026-71276

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T13:24:52.080 |

Magistrala (formerly Mainflux)'s message-readers API reads a `format` value from the HTTP query string (readers/api/http/transport.go) with no validation and interpolates it directly into raw SQL queries via fmt.Sprintf() in both the PostgreSQL reader (readers/postgres/messages.go: `fmt.Sprintf("SELECT * FROM %s WHERE %s ...", format, cond)`) and the TimescaleDB reader (readers/timescale/messages.go, same pattern), enabling SQL injection by any authenticated user able to query channel messages.

### CVE-2026-71245

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T11:16:27.487 |

Mautic's getLeadIdsByFieldValueAction (LeadBundle/Controller/AjaxController.php) reads a field parameter from the request, sanitizes it only with InputHelper::clean() (which HTML-entity-encodes quotes and angle brackets but does not restrict other characters), and passes it into LeadRepository::buildQueryForGetLeadsByFieldValue() where it is concatenated directly as a raw SQL column identifier ($col = 'l.'.$field) rather than being validated against a whitelist of real column names or passed as a bound parameter. Since Doctrine cannot parameterize identifiers, and the sanitizer does not block spaces, parentheses, or other SQL-relevant characters, an attacker can inject SQL via the field name itself. The action requires only a valid session (any authenticated user), unlike sibling actions in the same controller that carry additional permission checks.

### CVE-2026-71211

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-05T08:16:43.367 |

MLflow's AI Gateway accepts an auth_config.api_base value when creating a gateway secret (mlflow/server/handlers.py, _create_gateway_secret) with no validation of scheme, host, or IP range; the value is stored verbatim. The gateway proxy endpoint (mlflow/server/gateway_api.py, raw_proxy) subsequently issues an HTTP request to that stored api_base plus a caller-supplied path and returns the full response body. MLflow's existing SSRF guard, _validate_webhook_url (which blocks non-global and metadata IPs), is never invoked anywhere in this gateway secret/proxy code path. The CreateGatewaySecret action additionally has no entry in the permission-validator map, so it requires only basic authentication rather than any specific scope, meaning any authenticated user — including read-only accounts — can create a secret pointing at an internal address and reach it via the proxy endpoint, potentially exposing cloud-instance IAM credentials via metadata services. This is related to CVE-2026-4035, which addresses a distinct mechanism in the same gateway-secret feature (server-side $ENV_VAR resolution inside the api_key field leaking credentials to the configured upstream); the finding here is an independent missing-validation gap in the api_base destination itself, unaffected by that fix.

### CVE-2026-55707

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-05T06:16:37.903 |

In OpenStack Neutron before 28.0.2, the subnetpool onboarding API does not verify ownership of the target subnets. An authenticated user can onboard subnets from another project's shared network into their own subnetpool, mutating the victim's subnet state and altering L3 routing and address scope behavior for victim routers.

### CVE-2026-13227

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-04T21:16:35.140 |

An Improper Authorization vulnerability exists in ERPNext version <v16.25.0 and <15.115.0  due to insufficient access control in the whitelisted API method erpnext.crm.doctype.prospect.prospect.get_opportunities.

This issue affects ERPNext: before 15.115.0, before 16.26.0.

### CVE-2026-70485

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-04T20:16:55.610 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.9.0 until 0.11.0, Open WebUI checked whether a user-supplied URL destination was globally routable by applying ipaddress.is_global to the literal IPv6 address without examining IPv4 addresses embedded in transition encodings. On a deployment with a NAT64 gateway, any verified user could wrap an internal or cloud-metadata IPv4 address in the NAT64 well-known prefix, pass the filter, and receive the internal response body through RAG URL ingestion, URL-to-markdown conversion, or web-search content retrieval. This issue is fixed in 0.11.0.

### CVE-2026-70475

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-04T20:16:54.170 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, the PUT /api/v1/executions/:id endpoint in packages/server/src/routes/executions/index.ts lacks the checkAnyPermission() middleware that protects other execution endpoints. Any authenticated user, regardless of assigned permissions, can modify execution state, data, and metadata of any execution in their workspace, enabling privilege escalation and manipulation of workflow execution results. This issue is fixed in 3.1.3.

### CVE-2026-47682

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-04T20:16:51.747 |

CVAT is an open source interactive video and image annotation tool for computer vision. In versions 1.6.0 through 2.64.0, an attacker with write access to a cloud storage that's been added to a CVAT instance, or ability to add new cloud storages, is able to overwrite arbitrary files on the server's filesystem. This issue has been fixed in version 2.65.0.

### CVE-2026-70472

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-863` |
| Published | 2026-08-04T19:16:54.680 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, Flowise openai-assistants-vector-store endpoints accept a client-controlled credential parameter and load credentials by id without checking whether that credential belongs to the caller workspace. Route permissions assistants:* only check feature access. The controller passes req.query.credential straight to the service, and the service uses findOneBy({ id: credentialId }), decrypts the credential, and calls OpenAI APIs without a workspaceId check. If an attacker knows another workspace credentialId, the attacker can use that workspace OpenAI key, read, modify, or delete victim vector stores and files, cause billing impact on the victim OpenAI account, and violate multi-tenant boundaries. This issue is fixed in version 3.1.3.

### CVE-2026-70471

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-04T19:16:54.540 |

Flowise is a drag-and-drop user interface for building customized large language model (LLM) flows. Prior to 3.1.3, Flowise injects $vars into the code execution sandbox without requiring variables:view, bypassing the permission-protected Variables API. Variables for the active workspace are fetched at packages/components/src/utils.ts and runtime variables are resolved from server environment variables, while the official variables route enforces variables:view. A user or API key that is denied variables:view can call /api/v1/node-custom-function and receive $vars pre-populated with all variables for the workspace, including Variable.name to Variable.value static variables and Variable.name to process.env[Variable.name] runtime variables. This can expose secrets such as database passwords, JWT secrets, SMTP passwords, and cloud keys, depending on the workspace Variables configuration. This issue is fixed in version 3.1.3.

### CVE-2026-69702

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-04T19:16:53.980 |

SnailJob 1.7.0 contains a denial of service vulnerability in the FuryUtil.deserialize helper that allows authenticated attackers to crash the server by supplying a crafted Zstandard-compressed payload with an inflated frame_content_size field in the frame header. Attackers can store a base64-encoded Zstandard payload declaring an arbitrarily large decompressed size in a retry task argument, causing the JVM to attempt an unbounded array allocation and triggering an unrecoverable java.lang.OutOfMemoryError when the task is dispatched through the retry-task pipeline.

### CVE-2026-13229

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-04T19:16:41.890 |

Zammad 7.1.0 contains an authenticated improper authorization vulnerability in the ticket article attachment cloning endpoint.

### CVE-2026-69262

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-04T17:17:01.547 |

Flowise is a drag & drop user interface to build a customized large language model flow. Prior to 3.1.3, `DELETE /api/v1/chatflows/:id` authorized requests with checkAnyPermission('chatflows:delete,agentflows:delete'), so possession of either permission was sufficient to reach the delete path. The delete logic then resolved the target record only by id and workspaceId and did not validate the target resource type, allowing a caller with only agentflows:delete to delete a CHATFLOW and a caller with only chatflows:delete to delete an AGENTFLOW in the same workspace. This issue is fixed in version 3.1.3.

### CVE-2026-15314

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-04T17:16:46.313 |

Tapo P110 v1
smart Wi-Fi Plug contains an improper boundary validation vulnerability in the
handling of authenticated HTTP request bodies due to insufficient input
validation before memory copy operations. This may lead to buffer overflow condition,
causing the web service process to crash.





Successful exploitation
may cause the web service process to stop responding or restart, resulting in a
denial-of-service condition.

### CVE-2026-67618

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-04T15:16:41.293 |

marimo before 0.23.15 contains a configuration injection vulnerability that allows notebook authors to exfiltrate operator API keys by embedding a malicious base_url in PEP-723 inline script metadata, which is merged into session configuration with higher precedence than the operator's own settings due to insufficient sanitization in sanitize_pyproject_dict. When an operator opens the crafted notebook and makes an AI request, marimo resolves the attacker-controlled base_url from the notebook config while falling back to the operator's OPENAI_API_KEY environment variable for authentication, transmitting the API key to the attacker-controlled endpoint without requiring any cell execution.

### CVE-2026-67199

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-04T15:16:40.570 |

Perspective 5.0.0 contains a denial of service vulnerability that allows remote attackers to block the server event loop indefinitely by submitting a crafted expression containing unbounded for or while loop constructs in a TableMakeViewReq message. Attackers can embed an arbitrarily large iteration count in an expression column evaluated once per table row, causing the Tornado IOLoop to block without any iteration cap, deadline, or cancellation check, rendering the server unresponsive to all connected clients.

### CVE-2026-11368

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-04T15:16:24.843 |

The Bluetooth host ATT layer (subsys/bluetooth/host/att.c) associates each in-flight ATT TX buffer with its owning channel via the static tx_meta_data_storage[] array (data->att_chan = chan). When a buffer's last reference is dropped, its net-buf destroy callback defers the completion handling to the system workqueue (att_tx_destroy -> att_tx_destroy_work_handler -> att_on_sent_cb -> bt_att_sent), where bt_att_sent dereferences the channel and its ATT context (sys_slist_get(&att->reqs)).

When a peer disconnects while an ATT PDU (a server notification/indication or any response) is still in flight in the controller TX path, L2CAP tears the channel down in l2cap_chan_del(): it runs the disconnected callback and then the released callback (bt_att_released), which frees the channel slab slot. Because the in-flight buffer is held by the connection TX path rather than the channel's own queue, its deferred destroy work can run after the channel has been freed. The att_on_sent_cb guard intended to drop the stale callback itself dereferences meta->att_chan, which is now a dangling pointer into a freed (and possibly reused) slab slot.

A remote peer with an ATT connection can drive this by disconnecting during routine ATT traffic; no pairing or user interaction is required to reach the ATT bearer. The result is a use-after-free read/write of freed channel memory, reliably crashing the Bluetooth host (denial of service) and, because the channel slab slot may be reused, potentially corrupting live memory.

The fix makes bt_att_released() NULL the att_chan field of every tx_meta_data_storage[] entry still referencing the channel before freeing it, so the deferred guard observes a NULL pointer and drops the callback. Teardown and the destroy work both run on the cooperative system workqueue, so the array update is serialized and needs no lock.

### CVE-2026-16792

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-04T20:16:49.317 |

An improper certificate validation vulnerability was reported in multiple Lenovo XClarity Orchestrator (LXCO) 2.2.0 microservices that could allow an adjacent network attacker to intercept sensitive communications by performing a machine-in-the-middle attack against HTTPS connections during TLS certificate validation under certain circumstances.

### CVE-2026-69704

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-04T19:16:54.280 |

Atals-Livre contains a SQL injection vulnerability that allows attackers to manipulate database queries by passing unsanitized input through a GET parameter to the supp() deletion helper function. Attackers can inject malicious SQL syntax via the vulnerable GET parameter to perform unauthorized database operations including data deletion and extraction.
