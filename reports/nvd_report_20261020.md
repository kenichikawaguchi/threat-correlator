# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-19 15:01 UTC
- **対象期間**: `2026-10-18T15:00:30.000Z` 〜 `2026-10-19T15:01:07.000Z`
- **重要CVE数**: 52 件（Critical 9.0+: 8 件 / High 7.0〜: 44 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件** 超に上り、特に **Apache Camel 系列** と **Web アプリケーション向けのデシリアライズ／コードインジェクション** が目立ちます。  
- 最高スコア **10.0**（CVE‑2026‑78162）を含む、リモートコード実行 (RCE) が可能な脆弱性が多数報告されています。  
- WordPress 系プラグインや WordPress 以外の CMS（MapSVG、HivePress、FlyCms）でも、**デフォルト認証情報やファイルアップロードの制御不備** が深刻なリスクを生んでいます。  
- 多くの脆弱性は **バージョンアップだけで解消可能** である一方、設定ミス（デシリアライズフィルタ未設定、ポート開放、認証ルール未設定）による影響も大きいため、**パッケージ更新と設定見直しの同時実施** が必須です。

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 製品・コンポーネント | 主な影響 | 注目理由 |
|-----|--------|----------------------|----------|----------|
| **CVE‑2026‑78162** | 10.0 | Apache Camel (core, `camel-hazelcast` など) | デシリアライズ不正データにより任意コード実行 (RCE) が可能。`camel-hazelcast` がデフォルトで `JavaSerializationFilterConfig` を設定しないため、攻撃者がシリアライズオブジェクトを注入できる。 | **最高スコア** かつ **Apache Camel 4 系全体** に波及。多くのエンタープライズ統合システムで使用されているため、被害拡大リスクが極めて高い。 |
| **CVE‑2026‑111406** | 9.9 | MapSVG (mapsvg‑lite‑interactive‑vector‑maps) ≤ 8.16.1 | 任意ファイルアップロードにより Web シェルを配置可能。アップロード時の MIME/拡張子チェックが不十分。 | **Web アプリケーションの最前線** で利用されるプラグイン。攻撃者がサーバー上で直接コードを実行でき、情報漏洩・改ざんにつながる。 |
| **CVE‑2026‑110887** | 9.9 | HivePress ≤ 1.7.32 | 不適切なコード生成制御によりリモートコードインクルージョン (RCE)。`hivepress` のテンプレートエンジンが外部入力を直接評価。 | **WordPress エコシステム** の人気プラグインで、インストールベースが大きく、攻撃対象になりやすい。 |
| **CVE‑2026‑108983** | 9.8 | GeoWebServer.exe (デフォルトポート) | デフォルトで公開されている管理ポートが外部から到達可能。認証なしで情報取得・設定変更が可能。 | **インフラ系サービス** のデフォルト設定ミス。外部からのスキャンで容易に検出でき、攻撃の足掛かりになる。 |
| **CVE‑2026‑112296** | 9.3 | FlyCms (コミット `edfdf724` 以前) | デフォルト認証情報 `flycms / admin123` が残存。認証なしでスーパ管理者権限取得が可能。 | **デフォルト認証情報** は最も簡単に悪用できる脆弱性。内部・外部問わず即座に権限取得が可能。 |

> **※** これら以外にも Apache Camel 系列で **8.8 以上** の脆弱性が多数（JGroups、Spring‑Redis、Netty‑HTTP など）報告されています。上記 5 件は **スコアが高く、かつ実運用でのインパクトが大きい** ものとして優先的に対策すべきです。

---

## 3. 推奨アクション  

### 3‑1. Apache Camel 系列（CVE‑2026‑78162 を含む）  
- **パッケージ更新**  
  - `org.apache.camel:camel-core` → **4.22.1** 以上  
  - `org.apache.camel:camel-hazelcast` → **4.22.1** 以上  
  - `org.apache.camel:camel-jgroups` → **4.22.1** 以上  
  - `org.apache.camel:camel-spring-redis` → **4.22.1** 以上  
  - `org.apache.camel:camel-smooks` → **4.22.1** 以上（XML External Entity 対策）  
- **設定見直し**  
  - `camel-hazelcast` の `javaSerializationFilterConfig` を必ず有効化（`allowList` に安全クラスのみ列挙）。  
  - すべての Camel コンポーネントで **`useMDCLogging`** や **`allowSerializedObjects`** 等のデシリアライズ制御フラグを `false` に設定。  
  - 不要なコンポーネントは **削除** し、攻撃対象を減らす。  

### 3‑2. MapSVG (mapsvg‑lite‑interactive‑vector‑maps)  
- **アップデート**：バージョン **8.16.2** 以上へ。  
- **ファイルアップロード制御**  
  - `php.ini` の `file_uploads` を `On` のままにする場合は、`upload_max_filesize` と `post_max_size` を適切に制限し、**MIME タイプと拡張子のホワイトリスト** を実装。  
  - Web サーバー側で **`mod_security`** などの WAF ルールを追加し、`.php` 系スクリプトのアップロードをブロック。  

### 3‑3. HivePress (WordPress プラグイン)  
- **アップデ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-78162

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-19T11:17:19.037 |

Deserialization of Untrusted Data vulnerability in Apache Camel.



This issue affects Apache Camel: from 4.0.0 before 4.18.5, from 4.19.0 before 4.22.1.



The camel-hazelcast component applies a default Hazelcast JavaSerializationFilterConfig to the instances it creates from its own configuration, a protection introduced by CVE-2026-43865. That change did not reach two of the configuration paths Camel builds itself, so those paths continued to create Hazelcast instances whose Java deserialization is unrestricted. ReplicatedHazelcastAggregationRepository extends HazelcastAggregationRepository but overrides doStart() without calling super.doStart(), keeping its own copy of the bootstrap block, and therefore never received the filter: a route using it without supplying a hazelcastInstance starts a Hazelcast member that deserializes values read from the backing ReplicatedMap with no class restriction. HazelcastDefaultComponent#getOrCreateHzClientInstance() builds its own ClientConfig when hazelcastMode=client is selected and neither a referenced ClientConfig nor hazelcastConfigUri is supplied, and likewise applied no filter, so client-mode endpoints behaved differently from node-mode endpoints for an otherwise identical configuration. In both cases an attacker able to publish into the Hazelcast cluster that the affected instance is attached to can cause a serialized Java object of their choosing to be deserialized inside Hazelcast's own serialization layer, before Camel processes the exchange, resulting in remote code execution. Hazelcast clusters have neither authentication nor TLS enabled by default. Selecting client mode is a topology choice rather than a security option, so neither path required the deployment to opt in to unsafe behaviour.



Users are recommended to upgrade to version 4.23.0, which fixes the issue. If users are on the 4.22.x releases stream, then they are suggested to upgrade to 4.22.1. If users are on the 4.18.x releases stream, then they are suggested to upgrade to 4.18.5. The 4.14.x releases stream and earlier reached end of life before this issue was resolved and will not receive a fix, so deployments on those lines must move to a supported release. For deployments that cannot upgrade immediately, supply an explicit Hazelcast configuration carrying a JavaSerializationFilterConfig, or inject a pre-built HazelcastInstance, since a user-supplied configuration is never overwritten by Camel. Alternatively set the JVM-wide filter -Djdk.serialFilter=!java.net.;java.;javax.;org.apache.camel.;!* and enable Hazelcast cluster authentication and TLS to restrict who can reach the cluster.

### CVE-2026-111406

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-19T10:16:46.007 |

Unrestricted Upload of File with Dangerous Type vulnerability in PT Norther Lights Production MapSVG mapsvg-lite-interactive-vector-maps allows Upload a Web Shell to a Web Server.This issue affects MapSVG: from n/a through 8.16.1.

### CVE-2026-110887

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-19T10:16:45.627 |

Improper Control of Generation of Code ('Code Injection') vulnerability in HivePress HivePress hivepress allows Remote Code Inclusion.This issue affects HivePress: from n/a through 1.7.32.

### CVE-2026-108983

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-19T02:17:05.853 |

A vulnerability is in Web Server default connection ports under the process name GeoWebServer.exe .

### CVE-2026-112296

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-10-19T14:17:08.510 |

FlyCms through commit edfdf724 contains a default credentials vulnerability that allows unauthenticated remote attackers to gain super administrator access via the flycms account with password admin123. Attackers can log in through POST /api/auth/login, solving only the image captcha, to obtain full control of site content, users and configuration.

### CVE-2026-112292

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-19T14:17:07.903 |

CheckCle through 1.6.0 contains a missing authorization vulnerability that allows unauthenticated attackers to read, modify and delete records because shipped PocketBase collections use empty API rules. Attackers can query /api/collections/<name>/records endpoints to steal server_token values and alert_configurations secrets, disable alerting, alter status pages, or delete monitoring data.

### CVE-2026-103091

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-306;CWE-862;CWE-863;CWE-1188` |
| Published | 2026-10-19T03:16:58.377 |

Missing Authorization (CWE-862) and Initialization of a Resource with an Insecure Default (CWE-1188) in the MCP proxy (HandleStreamPassThrough in mcp_service.go) and OIDC registration flow (GET /info and POST /register in internal/controlplane/server.go) in Google OSS Agent Mesh (SAM) versions 0.1.0-alpha.1 through 0.1.0-alpha.8 allow a remote attacker to self-enroll into the mesh and invoke arbitrary tools across all connected MCP backend nodes. Because GET /info publicly discloses OIDC configuration, POST /register auto-enrolls any valid OIDC token holder without claim filtering or ban checks, and the default policy binds sam:system:authenticated to wildcard services and targets, an attacker can obtain a mesh credential with full read, write, and execution access on backend services. Users should upgrade to version 0.1.0-alpha.9 or later, which enforces a fail-closed default policy, explicit policy-binding requirements on enrollment, and ban checks.

### CVE-2026-102503

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-10-19T03:16:58.193 |

Missing Authentication for Critical Function (CWE-306) and Missing Authorization (CWE-862) in the /libp2p-http ingress server (StartIngressServer in cmd/sam-node/node.go) in Google OSS Agent Mesh (SAM) versions 0.1.0-alpha.1 through 0.1.0-alpha.2 allow an unauthenticated remote libp2p peer to bypass Biscuit capability policy enforcement and invoke arbitrary registered backend services (including command/stdio-backed MCP servers, A2A, and inference endpoints). While the MCP protocol stream handler enforces WithBiscuitAuth and Authorize checks, the parallel /libp2p-http ingress routes requests directly to backend service handlers without verifying a Biscuit token or mesh enrollment. Users should upgrade to version 0.1.0-alpha.3 or later.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-88900

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-19T12:17:11.980 |

Deserialization of Untrusted Data vulnerability in Apache Camel Camel-Jgroups component.



This issue affects Apache Camel: from 4.0.0 before 4.18.5, from 4.19.0 before 4.22.1.



JGroupsEndpoint.createExchange(Message), which CamelJGroupsReceiver calls for every message the jgroups consumer receives before the exchange is routed, set the exchange body from org.jgroups.Message.getObject(). For an ObjectMessage, which is the message type the Camel jgroups producer sends, JGroups Java-deserializes the payload through an ObjectInputStream on its own receive thread as the message arrives, and getObject() returns the resulting object. No java.io.ObjectInputFilter was applied on that path unless the deployment had set a JVM-wide serialization filter: camel-jgroups installed none, and the JGroups versions shipped with the affected releases apply none of their own, so any serializable class on the application classpath could be instantiated and its deserialization callbacks run. Unless a channel or the channelProperties option is configured, the consumer creates its channel with new JChannel(), the stock JGroups protocol stack, which multicasts over UDP without the AUTH protocol and without encryption, so any host able to reach the cluster's multicast group or bind port can join the cluster and send messages to the consumer without credentials. Such a host could send a crafted serialized object that leads to remote code execution in the Camel process when a usable deserialization gadget chain is present on the classpath, and no non-default option was required on the consumer. Because JGroups materializes the object before Camel's receiver runs, a check performed by Camel can only inspect the deserialized result and cannot stop code that runs during deserialization, so closing the issue also requires a control that applies before the payload is read, as described in the mitigation. Exploitation requires network access to the cluster's multicast group or bind port, which with the default UDP multicast transport means a host on an adjacent network, and a usable gadget chain on the classpath, which is why the severity is assessed as high rather than critical.



Users are recommended to upgrade to version 4.23.0, which fixes the issue. If users are on the 4.22.x releases stream, then they are suggested to upgrade to 4.22.1. If users are on the 4.18.x releases stream, then they are suggested to upgrade to 4.18.5. The 4.14.x releases stream and earlier, and the 4.15.x to 4.17.x and 4.19.x to 4.21.x release lines, reached end of life before this issue was resolved and will not receive a fix, so deployments on those lines must move to a supported release.

### CVE-2026-83531

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-917` |
| Published | 2026-10-19T11:17:21.507 |

Improper Control of Generation of Code ('Code Injection'), Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') vulnerability in Apache Camel.



This issue affects Apache Camel: from 4.4.0 before 4.18.5, from 4.19.0 before 4.22.1.



The dynamic-router-control endpoint, introduced in 4.4.0, lets routing participants manage Dynamic Router subscriptions by sending control messages. When it handled a subscribe or update request, DynamicRouterControlProducer took the subscription predicate and the name of the language used to compile it from the incoming message, either from the predicate and expressionLanguage fields of a DynamicRouterControlMessage body or from the CamelDynamicRouterPredicate and CamelDynamicRouterExpressionLanguage headers. DynamicRouterControlService then resolved that language from the CamelContext and compiled the expression into a Predicate, with no allow-list and no opt-in. The compiled predicate was added to the channel's rule base and evaluated against every exchange routed through the corresponding dynamic-router endpoint for as long as the subscription existed. A route that forwards messages from an external transport to the control endpoint, as shown in the component documentation for routing participants in other JVMs or applications, therefore let any actor able to send a message on that transport supply an expression of their choosing, which was evaluated with the privileges of the Camel process. Any expression language available on the classpath could be selected, including the simple language, which is always present and was the default on the header path, so removing optional expression languages from the classpath did not prevent the issue. Exploitation requires the ability to send a message on a transport whose route forwards it to a dynamic-router-control endpoint; no other authentication or user interaction is needed. Releases before 4.4.0 are not affected, because their control channel took predicate expressions only from the endpoint URI configured by the route author.



Users are recommended to upgrade to version 4.23.0, which fixes the issue. If users are on the 4.22.x releases stream, then they are suggested to upgrade to 4.22.1. If users are on the 4.18.x releases stream, then they are suggested to upgrade to 4.18.5. The 4.14.x releases stream and earlier reached end of life before this issue was resolved and will not receive a fix, so deployments on those lines must move to a supported release. After upgrading, a control message that carries a predicate expression or an expression language is rejected unless the new allowPredicateFromMessage option is enabled on the dynamic-router-control endpoint; enable it only when every sender of control messages is trusted. For deployments that cannot upgrade immediately, do not forward messages from untrusted or shared transports to a dynamic-router-control endpoint. Where control messages must cross such a transport, authenticate the sender and make sure the predicate and expression language of each subscription are set by the route rather than taken from the incoming message, for example by removing the CamelDynamicRouterPredicate and CamelDynamicRouterExpressionLanguage headers and clearing the predicate and expressionLanguage fields of a DynamicRouterControlMessage before it reaches the endpoint. Removing optional expression languages from the classpath is not a sufficient workaround. As defence in depth, restrict who can send to the transports that feed the control endpoint, and on 4.23.0 and 4.22.1 set the allowedSchemes option of the dynamic-router endpoint to limit which endpoints a subscription's destinationUri may name.

### CVE-2026-78165

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-19T11:17:19.643 |

Deserialization of Untrusted Data vulnerability in Apache Camel Spring Redis component.



This issue affects Apache Camel: from 2.11.0 before 4.18.5, from 4.19.0 before 4.22.1.



RedisConfiguration.getSerializer lazily built a bare JdkSerializationRedisSerializer whenever no serializer option was configured, and that instance was used for every read the component performs. Spring's implementation delegates through DeserializingConverter to DefaultDeserializer, which reads the bytes with a ConfigurableObjectInputStream and installs no java.io.ObjectInputFilter on the stream, so an arbitrary serialized class graph was materialised and its readObject method executed. RedisConsumer.setBody applied that serializer to the raw bytes of every message published to the subscribed channels, before the Exchange was constructed and therefore before any route logic could inspect the message, so an actor able to issue PUBLISH on a subscribed channel reached the deserialization sink directly. The same default serializer backed the RedisTemplate built by RedisConfiguration.createDefaultTemplate, so the producer read commands GET, HGET, HGETALL and HVALS deserialized whatever was stored in the Redis keyspace, and SpringRedisIdempotentRepository shared that template. Configuring a custom redisTemplate did not close the consumer path, because RedisConsumer.setBody reads getSerializer directly rather than the serializer attached to the template, so a deployment that had wired a String serializer into its own template remained exposed on the consumer side unless it also set the serializer option. The component never constructed a java.io.ObjectInputStream itself, which is why earlier passes over the Camel codebase for unfiltered Java deserialization did not reach it. The behaviour dates back to the introduction of the component, first released in 2.11.0, and was unchanged until this fix.



Users are recommended to upgrade to version 4.23.0, which fixes the issue. If users are on the 4.22.x releases stream, then they are suggested to upgrade to 4.22.1. If users are on the 4.18.x releases stream, then they are suggested to upgrade to 4.18.5. The 4.14.x releases stream and earlier reached end of life before this issue was resolved and will not receive a fix, so deployments on those lines must move to a supported release. For deployments that cannot upgrade immediately, set the JVM-wide jdk.serialFilter system property, which the affected code path honours because it reads through a java.io.ObjectInputStream, for example -Djdk.serialFilter=!java.net.**;java.**;javax.**;org.apache.camel.**;!* ; or set the serializer endpoint option to a serializer that does not use Java serialization, such as StringRedisSerializer, noting that this must be set as the serializer option and not only on a custom redisTemplate. As defence in depth, require authentication on the Redis instance and restrict which clients may publish to the subscribed channels, and do not expose a Redis instance consumed by Camel to untrusted networks.

### CVE-2026-111408

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-19T10:16:46.257 |

Deserialization of Untrusted Data vulnerability in ExpressTech Quiz And Survey Master quiz-master-next allows Object Injection.This issue affects Quiz And Survey Master: from n/a through 11.2.7.

### CVE-2026-13695

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-19T09:17:08.880 |

SQL injection (SQLi) vulnerability—specifically a UNION-based vulnerability—in the Integratec application that affects the sInfo parameter sent via POST to the endpoint /login/ap_Login.aspx/start. Successful exploitation of this vulnerability could allow an attacker to steal data from the database, such as credentials and user information, and cause errors and partial denial-of-service conditions. Furthermore, this vulnerability could facilitate other types of follow-up attacks, such as data exfiltration or privilege escalation.

### CVE-2026-112264

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-19T14:17:03.003 |

BentoML through 1.4.39 contains a Dockerfile instruction injection vulnerability that allows attackers to add arbitrary build instructions by embedding newlines in docker.env mapping keys rendered by the legacy base.j2 template. Attackers can supply a crafted bentofile.yaml or imported bento archive so that bentoml containerize executes injected RUN instructions during docker build, accessing build secrets and poisoning images.

### CVE-2026-112263

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-19T14:17:02.787 |

Television (tv) 0.15.0 through 0.15.9 contains an OS command injection vulnerability that allows attackers to run shell commands through improperly escaped single quotes in format_command. Attackers can plant a file with a crafted name containing an apostrophe so that triggering an action like the default edit action executes commands with victim privileges.

### CVE-2026-112161

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-19T09:17:08.097 |

MobaXterm Personal Edition (Portable) 26.4 GA extracts the CygUtils64.plugin file without first verifying its integrity. A local attacker with write permissions on this file can replace the ‘bin/cygwin1.dll’ library contained within it with a malicious library. When the victim opens a Local Shell session or uses a Cygwin-based function, the application extracts the component and loads the tampered library, executing code with the victim’s permissions. Exploitation requires write access to the plugin and does not, in itself, involve privilege escalation.

### CVE-2026-112265

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-19T14:17:03.277 |

LangBot through 4.11.0 contains a missing authenticity verification vulnerability that allows unauthenticated attackers to inject forged Lark/Feishu events by skipping signature checks. Attackers knowing a bot UUID can POST fabricated im.message.receive_v1 or card.action.trigger events to drive the LLM pipeline, tools, and approvals as other users.

### CVE-2026-112266

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-187` |
| Published | 2026-10-19T14:17:03.987 |

SGLang through 0.5.22 contains a denial of service vulnerability that allows API clients to abort other users' in-flight generation requests by supplying a short client-controlled rid. Attackers can submit streaming /generate requests with single hex character rids and disconnect, triggering prefix-matching abort logic that terminates all other clients' requests.

### CVE-2026-111915

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-19T14:17:00.740 |

Yank Note before 3.93.1 contains a path traversal vulnerability that allows unauthenticated remote attackers to read arbitrary files via the path or doc parameter of /api/help. Attackers can supply repeated '../' segments, which bypass the single-replacement sanitization in the publicly allowlisted endpoint, to read SSH keys, configuration, or notes.

### CVE-2026-88901

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-19T11:17:25.340 |

Improper Restriction of XML External Entity Reference vulnerability in Apache Camel.



This issue affects Apache Camel: from 4.7.0 before 4.18.5, from 4.19.0 before 4.22.1.



Improper Restriction of XML External Entity Reference in the Smooks component (camel-smooks) in Apache Camel allows an attacker who supplies the XML message body to read local files or issue requests to internal network locations via an external entity declaration in that body. This issue affects Apache Camel: from 4.7.0 before 4.18.5, from 4.19.0 before 4.22.1. The Smooks data format (.unmarshal().smooks(...)) and the Smooks component (smooks:) parse the incoming XML body with the reader Smooks resolves by default, which is the Woodstox SAX parser. That reader resolves external general and parameter entities and loads external DTDs, and camel-smooks applied none of the parser hardening that the other Camel XML components apply. A DOCTYPE with an external subset, or an external general entity, declared in the XML document is therefore resolved and expanded while the body is unmarshalled, and the resolved content is bound into the unmarshalled result and returned on InOut routes. An external sender whose XML reaches a camel-smooks data format or endpoint could therefore read files readable by the Camel process and cause the process to issue requests to hosts the document names. No non-default option is required, since resolving external entities was the default behaviour. Configurations that declare their own reader - EDI, CSV, JSON, or a custom reader - do not use the XML reader and are not affected. Users are recommended to upgrade to version 4.18.5, 4.22.1 or 4.23.0, which fixes the issue.



Upgrade to Apache Camel 4.23.0, which fixes the issue. Users on the 4.18.x LTS releases stream should upgrade to 4.18.5. Users on the 4.22.x LTS releases stream should upgrade to 4.22.1. camel-smooks now parses the XML body with a javax.xml.parsers.DocumentBuilder that does not resolve external general or parameter entities and does not load external DTDs, and hands Smooks the resulting document, matching the secure XML processing configuration used by org.apache.camel.converter.jaxp.XmlConverter and the other Camel XML components. This hardening is applied only when the Smooks configuration parses XML with its default reader, so EDI, CSV, JSON and custom-reader configurations, and the marshalling direction, are unchanged. A new allowExternalEntities option, disabled by default, restores the previous behaviour for trusted legacy configurations that rely on external entity resolution. The camel-4.14.x releases stream and earlier reached end of life before this issue was resolved and will not receive a fix, so deployments on those lines must move to a supported release. For deployments that cannot upgrade immediately, do not apply camel-smooks to XML received from untrusted senders.

### CVE-2026-80344

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-19T11:17:21.363 |

Server-Side Request Forgery (SSRF) vulnerability in Apache Camel AS2 component.

This issue affects Apache Camel: from 4.0.0 before 4.18.5, from 4.19.0 before 4.22.1.

In the AS2 protocol the sender of a message may request that the Message Disposition Notification be returned asynchronously to an address the sender supplies. camel-as2 took that address from the inbound message and used it as the destination for the outgoing receipt without constraining it to anything the deployment had configured. A remote partner therefore chose the host the Camel instance would connect to when delivering the MDN. That gives server-side request forgery from the position of the AS2 receiver, including reaching hosts that are only routable from inside the deployment's network, and where the outbound connection carries credentials configured for MDN delivery those credentials are presented to the attacker-chosen destination.

Upgrade to Apache Camel 4.23.0, which fixes the issue. Users on the 4.18.x LTS releases stream should upgrade to 4.18.5. Users on the 4.22.x LTS releases stream should upgrade to 4.22.1. The asynchronous MDN destination is now constrained rather than taken verbatim from the inbound message. For deployments that cannot upgrade immediately, restrict outbound connectivity from the AS2 receiver to the partner endpoints it legitimately delivers receipts to, and do not attach credentials to MDN delivery that are valid for any host other than those partners.

### CVE-2026-80343

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-178` |
| Published | 2026-10-19T11:17:21.223 |

Improper Handling of Case Sensitivity vulnerability in Apache Camel Netty HTTP component.



This issue affects Apache Camel: from 4.0.0 before 4.18.5, from 4.19.0 before 4.22.1.



The camel-netty-http security constraint compared the request path against the configured context path using a case-sensitive match, while the routing that dispatches the request to the endpoint did not apply the same rule. The two comparisons therefore disagreed for any path whose case differed from the configured value. An external caller could alter the case of a character in a path segment so that the security constraint no longer recognised the path as protected, while the request still dispatched to the same endpoint. The result is that the constraint is skipped and the protected route is reached without satisfying it. No credential, prior access or special configuration is required beyond being able to send a request to the consumer.



Upgrade to Apache Camel 4.23.0, which fixes the issue. Users on the 4.18.x LTS releases stream should upgrade to 4.18.5. Users on the 4.22.x LTS releases stream should upgrade to 4.22.1. The constraint now matches the request path with the same case rules the dispatch uses, so the two can no longer disagree. For deployments that cannot upgrade immediately, place the authorization decision in front of the Camel consumer, for example in a reverse proxy that normalises the request path before forwarding.

### CVE-2026-80312

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-19T11:17:21.073 |

Improper Authentication vulnerability in Apache Camel OAuth component.



This issue affects Apache Camel: from 4.11.0 before 4.18.5, from 4.19.0 before 4.22.1.



The camel-oauth processors that guard a route did not stop the exchange when authentication could not be completed. Where a failure to establish an authenticated session should have terminated routing and returned an error to the caller, the processors fell through and returned control to the route, so the request continued to the protected endpoint as though authentication had succeeded. The effect is a fail-open authentication guard: an unauthenticated caller reached whatever the route did next. The condition is reached on the ordinary request path of a route configured to require OAuth, and needs no special configuration or prior access on the caller's part.



Upgrade to Apache Camel 4.23.0, which fixes the issue. Users on the 4.18.x LTS releases stream should upgrade to 4.18.5. Users on the 4.22.x LTS releases stream should upgrade to 4.22.1. The processors now stop the exchange and set the appropriate error status whenever an authenticated session cannot be established, so a failed authentication no longer reaches the protected part of the route. For deployments that cannot upgrade immediately, place an explicit authorization check after the OAuth processor rather than relying on it to halt the exchange, and verify that the route stops on failure.

### CVE-2026-78164

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-200;CWE-1336` |
| Published | 2026-10-19T11:17:19.403 |

Improper Neutralization of Special Elements Used in a Template Engine and Exposure of Sensitive Information to an Unauthorized Actor vulnerability in Apache Camel HTTP, Netty HTTP, Undertow and Vert.x HTTP components.



This issue affects Apache Camel: from 4.0.0 before 4.18.5, from 4.19.0 before 4.22.1.



The Camel HTTP producer families let an inbound message override the endpoint URI through the CamelHttpUri and CamelRestHttpUri headers, and then passed that message-supplied string through CamelContext.resolvePropertyPlaceholders() before using it. Property-placeholder resolution is a configuration-resolution facility, not a URI-parsing step: it reaches operating-system environment variables, JVM system properties, every PropertiesFunction registered on the classpath - including the secret functions - and, through camel-bean, the invocation of a no-argument method on any bean in the registry. Applying it to Exchange content therefore turned a URI string into a configuration- and bean-evaluation context. A route author opted into none of this: a plain static to("http://backend/api") was sufficient. Seven call sites were affected: HttpHelper.createURL and HttpHelper.createMethod in camel-http-common, HttpMethodHelper.createMethod in camel-http, VertxHttpHelper.resolveHttpURI in camel-vertx-http, UndertowHelper.createURL and UndertowHelper.createMethod in camel-undertow, and NettyHttpHelper.createURL in camel-netty-http. The bridgeEndpoint option did not bound the exposure: it suppresses the CamelHttpUri override in the createURL family but not in the createMethod family, so a route using the documented bridging configuration still resolved placeholders taken from the header, and CamelRestHttpUri was consumed before any bridgeEndpoint check in all four components. Only camel-http offered an opt-out, skipControlHeaders, which defaults to false. Reaching the headers did not always require header injection, because several Camel HTTP consumers populate CamelHttpUri from the request line themselves as a documented reverse-proxy feature. An unresolvable placeholder additionally produced a RuntimeExchangeException whose message echoed the URI, which distinguishes a set from an unset configuration key even where no outbound request is made. The behaviour predates the 4.x line. This advisory continues the alignment CAMEL-24282 applied to the toD and enrich dynamic-URI EIPs in 4.22.0, extending the same build-time-resolution contract to the HTTP producer components.



Users should upgrade to version 4.23.0, which fixes the issue. Users on the 4.22.x releases stream should upgrade to 4.22.1. Users on the 4.18.x releases stream should upgrade to 4.18.5. The 4.14.x releases stream and earlier reached end of life before this issue was resolved and will not receive a fix, so deployments on those lines must move to a supported release. For deployments that cannot upgrade immediately, strip the override headers at the trust boundary before the producer with removeHeader("CamelHttpUri") and removeHeader("CamelRestHttpUri"), or set skipControlHeaders=true on camel-http endpoints, which is the only component offering that option. Note that bridgeEndpoint=true is not a workaround: it suppresses the header override when the outbound URL is built but not when the header is re-parsed for the query string. Percent-encoding the placeholder delimiters is likewise not a mitigation for camel-netty-http, whose binding decodes the request path before the value reaches the header, so proxy or WAF rules written against the raw delimiters do not help there. As defence in depth, ensure consumers exposed to untrusted senders apply a strict inbound HeaderFilterStrategy over the Camel namespace, and resolve secrets through a vault rather than through environment variables or system properties that a placeholder can name.

### CVE-2026-16487

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-19T06:17:24.203 |

A flaw was found in bootc when operating with the default containers signature policy. Automatic or manual upgrades of a mutable image tag may apply unsigned content for registries that fall through to insecureAcceptAnything, allowing an attacker who can update that tag to execute arbitrary OS content as the host root filesystem on reboot.

### CVE-2026-111441

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-19T03:16:58.543 |

在 openGauss-server 的 src/gausskernel/cbb/utils/hll/hll.cpp 中，内置函数 HllObjectUnpack() 存在长度校验缺陷。该函数从用户提供的 packed HLL 解析 lenUsed 与 lenTotal 后，仅检查输入长度足以覆盖 HLL_HEAD_SIZE + lenUsed，随后按 lenTotal 分配缓冲区、按 lenUsed 调用 memcpy_s() 拷贝输入，既未校验 lenTotal >= lenUsed，也将 memcpy_s() 目标大小写成 lenUsed 而非实际分配的 lenTotal，导致安全拷贝无法拦截越界写。hll_in()、hll_print()、hll_cardinality() 等 SQL 入口会走同一解包路径。因此，普通数据库连接用户只需构造 lenTotal 小于 lenUsed 的畸形 packed HLL（例如经 ::hll 进入 hll_in()），即可触发服务端堆越界写，存在内存破坏风险。此问题随 packed HLL 解包函数 HllObjectUnpack() 进入代码，v2.1.0 起即存在。受影响版本包括 2.1.0、3.0.x、3.1.x、5.0.x、5.1.0、6.0.x，以及 7.0.0-RC1、7.0.0-RC2、7.0.0-RC3。该问题已在 7.0.0-LTS 版本修复，通过在 HllObjectUnpack() 中补齐 lenUsed <= lenTotal 校验，并将 memcpy_s() 的目标大小改为实际分配的 lenTotal。修复 PR 见 https://gitcode.com/opengauss/openGauss-server/pull/9380 。

### CVE-2026-111398

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-19T10:16:45.880 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in PT Norther Lights Production MapSVG mapsvg-lite-interactive-vector-maps allows Path Traversal.This issue affects MapSVG: from n/a through 8.16.1.

### CVE-2026-112082

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-404` |
| Published | 2026-10-19T06:17:23.013 |

A vulnerability was identified in sgl-project SGLang up to 0.5.19. This impacts the function Scheduler.expert_distribution_handle of the file python/sglang/srt/eplb/expert_distribution.py of the component Expert-Distribution Recording Endpoint. Such manipulation leads to denial of service. It is possible to launch the attack remotely. The exploit is publicly available and might be used. The pull request to fix this issue awaits acceptance.

### CVE-2026-108120

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:A/V:X/RE:M/U:Amber` |
| Weaknesses | `CWE-31` |
| Published | 2026-10-19T06:17:21.097 |

Brian Mariani from DigitalCanion SA has discovered a path traversal vulnerability in the View Logs functionality of 
koozali's SME Server version 11.0rc1-215 allowing an unauthenticated 
attacker to access files outside of the intended directory, leading to 
exfiltration of files located outside the intended system logs 
directory, including potentially sensitive system and application files.

### CVE-2026-85251

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-19T11:17:23.417 |

Exposure of Sensitive Information to an Unauthorized Actor vulnerability in Apache Camel HTTP component.

This issue affects Apache Camel: from 4.0.0 before 4.18.5, from 4.19.0 before 4.22.1.

Two paths handed credentials to a redirect target, which is a host chosen by the remote server rather than by the route, once followRedirects=true. OAuth2ClientConfigurer registers its interceptor with addRequestInterceptorFirst, and HttpClient runs protocol-level request interceptors inside ProtocolExec, which sits below RedirectExec in the exec chain; the interceptor therefore ran again for every redirect hop and re-attached Authorization: Bearer  to whatever host the Location header named. Separately, credentials were registered against an AuthScope matching any host, so basic and digest credentials were presented to a redirect target as well. A remote endpoint - or anyone who can influence its responses - could therefore collect the bearer token or the configured credentials simply by answering with a redirect to a host it controls.

Upgrade to Apache Camel 4.23.0, which fixes the issue. Users on the 4.18.x LTS releases stream should upgrade to 4.18.5. Users on the 4.22.x LTS releases stream should upgrade to 4.22.1. Credentials are now sent only to the authority the endpoint was configured with, and are not re-attached when a redirect crosses to another host. For deployments that cannot upgrade immediately, set followRedirects=false on endpoints that carry credentials, and handle any redirect explicitly in the route so that the destination is chosen by the route rather than by the remote server.

### CVE-2026-85250

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-19T11:17:23.257 |

Improper Restriction of XML External Entity Reference vulnerability in Apache Camel XPath component.

This issue affects Apache Camel: from 4.0.0 before 4.18.5, from 4.19.0 before 4.22.1.

With documentType set to InputSource, XPathBuilder handed the payload straight to javax.xml.xpath, which builds a DocumentBuilder of its own using the JDK defaults. The hardening applied to Camel's default document type was therefore bypassed: a DOCTYPE declaration that is refused on the default type was accepted here, and the external entity it declared was resolved and expanded into the evaluated document. An external sender whose XML reaches such an expression could read files readable by the Camel process and cause the process to issue requests to hosts it names. The two document types disagreeing on parser configuration is what made this reachable, since a deployment choosing InputSource for streaming reasons had no indication it was also choosing a weaker parser.

Upgrade to Apache Camel 4.23.0, which fixes the issue. Users on the 4.18.x LTS releases stream should upgrade to 4.18.5. Users on the 4.22.x LTS releases stream should upgrade to 4.22.1. The InputSource document type now goes through the same hardened parser as the default type, so a DOCTYPE is refused. Note that it also shares that type's documented escape hatch: the same DocumentBuilderFactory system properties that relax the default type relax this one, so a deployment that has set them remains unprotected by design. For deployments that cannot upgrade immediately, do not use documentType=InputSource on expressions evaluated over untrusted XML; the default document type already refuses a DOCTYPE.

### CVE-2026-108984

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-19T02:17:05.997 |

A vulnerability is in Web Server default connection ports under the process name GeoWebServer.exe .

### CVE-2026-103314

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294` |
| Published | 2026-10-19T13:16:53.617 |

A flaw was found in Red Hat Advanced Cluster Security for Kubernetes (RHACS). The Central SAML authentication ACS endpoint does not retain used SAML assertion or response identifiers to prevent replay. An attacker who obtains a valid, unexpired signed SAML response can submit it multiple times and receive distinct Central authentication tokens for the mapped identity.

### CVE-2026-79986

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-19T11:17:20.860 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Apache Camel Azure Files component.



This issue affects Apache Camel: from 4.0.0 before 4.18.5, from 4.19.0 before 4.22.1.



The Camel remote-file consumers poll a directory on a remote server and build the absolute remote path of each file by concatenating the configured directory with the file name reported in the server's directory listing. That concatenation (FtpUtils.absoluteFilePath and GenericFileConsumer) applied no lexical normalization and no check that the result stayed inside the directory being polled, and the resulting path became the operand for every subsequent remote operation on the file: retrieval (FtpOperations.retrieveFile / SftpOperations, reached from GenericFileConsumer where the retrieve name is taken verbatim from GenericFile.getAbsoluteFilePath), deletion when delete=true (GenericFileDeleteProcessStrategy), and renaming when move, preMove, moveFailed or readLock=rename is configured (GenericFileProcessStrategySupport and GenericFileRenameExclusiveReadLockStrategy). Neither isValidFile nor isMatched performed any containment check. A listing entry that is not a single path segment therefore resolved to a path outside the configured polling directory, causing Camel to read, delete or rename files outside it using the endpoint's own credentials. A listing name is not route-controlled data. It is supplied by the remote server, and the FTP control channel carries no integrity protection at all, so an on-path attacker can rewrite a LIST response without holding any credentials; a compromised, malicious or multi-tenant server, or a server backed by a virtual filesystem, can emit such a name directly. Retrieval is reachable in a default consumer configuration, since the remote consumers download every listed file; deletion and renaming additionally require one of the disposition options above, all of which are common. Escape from the directory Camel was configured to poll is unconditional, while escape from the server's own account boundary additionally depends on whether that server confines the account. The jailStartingDirectory option, which is documented as restricting Camel to the starting directory and is enabled by default, governed producer writes and, since the localWorkDirectory containment work, consumer downloads to the local work directory - but it did not constrain this remote operand, so its name and description claimed a boundary that was not enforced here. The same entry point had already been recognised on the local side: the localWorkDirectory download path was constrained so that a remote file name containing parent-directory segments could not resolve outside the local work directory. The remote operand was the remaining half of that surface. This artifact provides the azure-files scheme. Its consumer derives from the same RemoteFileConsumer base class and composed the remote path through a plain concatenation helper, so it inherited the same unconstrained resolution. Reaching it requires a listing name that is not a single path segment, which the Azure Files REST service does not normally return; the exposure was corrected on the same basis as the other remote-file consumers rather than from a demonstrated proof of concept against this scheme.



Upgrade to Apache Camel 4.23.0, which fixes the issue. Users on the 4.22.x releases stream should upgrade to 4.22.1. Users on the 4.18.x LTS releases stream should upgrade to 4.18.5. The 4.14.x stream reached end of life and does not receive this fix; users on it should move to a supported releases stream.

### CVE-2026-79985

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-19T11:17:20.647 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Apache Camel SMB component.



This issue affects Apache Camel: from 4.2.0 before 4.18.5, from 4.19.0 before 4.22.1.



The Camel remote-file consumers poll a directory on a remote server and build the absolute remote path of each file by concatenating the configured directory with the file name reported in the server's directory listing. That concatenation (FtpUtils.absoluteFilePath and GenericFileConsumer) applied no lexical normalization and no check that the result stayed inside the directory being polled, and the resulting path became the operand for every subsequent remote operation on the file: retrieval (FtpOperations.retrieveFile / SftpOperations, reached from GenericFileConsumer where the retrieve name is taken verbatim from GenericFile.getAbsoluteFilePath), deletion when delete=true (GenericFileDeleteProcessStrategy), and renaming when move, preMove, moveFailed or readLock=rename is configured (GenericFileProcessStrategySupport and GenericFileRenameExclusiveReadLockStrategy). Neither isValidFile nor isMatched performed any containment check. A listing entry that is not a single path segment therefore resolved to a path outside the configured polling directory, causing Camel to read, delete or rename files outside it using the endpoint's own credentials. A listing name is not route-controlled data. It is supplied by the remote server, and the FTP control channel carries no integrity protection at all, so an on-path attacker can rewrite a LIST response without holding any credentials; a compromised, malicious or multi-tenant server, or a server backed by a virtual filesystem, can emit such a name directly. Retrieval is reachable in a default consumer configuration, since the remote consumers download every listed file; deletion and renaming additionally require one of the disposition options above, all of which are common. Escape from the directory Camel was configured to poll is unconditional, while escape from the server's own account boundary additionally depends on whether that server confines the account. The jailStartingDirectory option, which is documented as restricting Camel to the starting directory and is enabled by default, governed producer writes and, since the localWorkDirectory containment work, consumer downloads to the local work directory - but it did not constrain this remote operand, so its name and description claimed a boundary that was not enforced here. The same entry point had already been recognised on the local side: the localWorkDirectory download path was constrained so that a remote file name containing parent-directory segments could not resolve outside the local work directory. The remote operand was the remaining half of that surface. This artifact provides the smb scheme. Its consumer walks the share listing on its own rather than through RemoteFileConsumer, skipping only the exact "." and ".." entries, so a name carrying traversal segments in any other form was concatenated unchecked. Reaching it requires a server that emits a listing name which is not a single path segment, which a conforming SMB2 implementation does not do; the exposure was corrected on the same basis as the other remote-file consumers rather than from a demonstrated proof of concept against this scheme.



Upgrade to Apache Camel 4.23.0, which fixes the issue. Users on the 4.22.x releases stream should upgrade to 4.22.1. Users on the 4.18.x LTS releases stream should upgrade to 4.18.5. The 4.14.x stream reached end of life and does not receive this fix; users on it should move to a supported releases stream.

### CVE-2026-79984

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-19T11:17:20.437 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Apache Camel Mina SFTP component.



This issue affects Apache Camel: from 4.18.0 before 4.18.5, from 4.19.0 before 4.22.1.



The Camel remote-file consumers poll a directory on a remote server and build the absolute remote path of each file by concatenating the configured directory with the file name reported in the server's directory listing. That concatenation (FtpUtils.absoluteFilePath and GenericFileConsumer) applied no lexical normalization and no check that the result stayed inside the directory being polled, and the resulting path became the operand for every subsequent remote operation on the file: retrieval (FtpOperations.retrieveFile / SftpOperations, reached from GenericFileConsumer where the retrieve name is taken verbatim from GenericFile.getAbsoluteFilePath), deletion when delete=true (GenericFileDeleteProcessStrategy), and renaming when move, preMove, moveFailed or readLock=rename is configured (GenericFileProcessStrategySupport and GenericFileRenameExclusiveReadLockStrategy). Neither isValidFile nor isMatched performed any containment check. A listing entry that is not a single path segment therefore resolved to a path outside the configured polling directory, causing Camel to read, delete or rename files outside it using the endpoint's own credentials. A listing name is not route-controlled data. It is supplied by the remote server, and the FTP control channel carries no integrity protection at all, so an on-path attacker can rewrite a LIST response without holding any credentials; a compromised, malicious or multi-tenant server, or a server backed by a virtual filesystem, can emit such a name directly. Retrieval is reachable in a default consumer configuration, since the remote consumers download every listed file; deletion and renaming additionally require one of the disposition options above, all of which are common. Escape from the directory Camel was configured to poll is unconditional, while escape from the server's own account boundary additionally depends on whether that server confines the account. The jailStartingDirectory option, which is documented as restricting Camel to the starting directory and is enabled by default, governed producer writes and, since the localWorkDirectory containment work, consumer downloads to the local work directory - but it did not constrain this remote operand, so its name and description claimed a boundary that was not enforced here. The same entry point had already been recognised on the local side: the localWorkDirectory download path was constrained so that a remote file name containing parent-directory segments could not resolve outside the local work directory. The remote operand was the remaining half of that surface. This artifact provides the mina-sftp scheme, an alternative SFTP implementation whose consumer derives from the same RemoteFileConsumer base class and therefore inherited the same unconstrained resolution.



Upgrade to Apache Camel 4.23.0, which fixes the issue. Users on the 4.22.x releases stream should upgrade to 4.22.1. Users on the 4.18.x LTS releases stream should upgrade to 4.18.5. The 4.14.x stream reached end of life and does not receive this fix; users on it should move to a supported releases stream.

### CVE-2026-79983

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-19T11:17:20.207 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Apache Camel FTP component.



This issue affects Apache Camel: from 4.0.0 before 4.18.5, from 4.19.0 before 4.22.1.



The Camel remote-file consumers poll a directory on a remote server and build the absolute remote path of each file by concatenating the configured directory with the file name reported in the server's directory listing. That concatenation (FtpUtils.absoluteFilePath and GenericFileConsumer) applied no lexical normalization and no check that the result stayed inside the directory being polled, and the resulting path became the operand for every subsequent remote operation on the file: retrieval (FtpOperations.retrieveFile / SftpOperations, reached from GenericFileConsumer where the retrieve name is taken verbatim from GenericFile.getAbsoluteFilePath), deletion when delete=true (GenericFileDeleteProcessStrategy), and renaming when move, preMove, moveFailed or readLock=rename is configured (GenericFileProcessStrategySupport and GenericFileRenameExclusiveReadLockStrategy). Neither isValidFile nor isMatched performed any containment check. A listing entry that is not a single path segment therefore resolved to a path outside the configured polling directory, causing Camel to read, delete or rename files outside it using the endpoint's own credentials. A listing name is not route-controlled data. It is supplied by the remote server, and the FTP control channel carries no integrity protection at all, so an on-path attacker can rewrite a LIST response without holding any credentials; a compromised, malicious or multi-tenant server, or a server backed by a virtual filesystem, can emit such a name directly. Retrieval is reachable in a default consumer configuration, since the remote consumers download every listed file; deletion and renaming additionally require one of the disposition options above, all of which are common. Escape from the directory Camel was configured to poll is unconditional, while escape from the server's own account boundary additionally depends on whether that server confines the account. The jailStartingDirectory option, which is documented as restricting Camel to the starting directory and is enabled by default, governed producer writes and, since the localWorkDirectory containment work, consumer downloads to the local work directory - but it did not constrain this remote operand, so its name and description claimed a boundary that was not enforced here. The same entry point had already been recognised on the local side: the localWorkDirectory download path was constrained so that a remote file name containing parent-directory segments could not resolve outside the local work directory. The remote operand was the remaining half of that surface. This artifact provides the ftp, ftps and sftp schemes, all of which are affected. The reporter demonstrated the issue end to end against an ftp endpoint, driving a Camel route with a malicious server whose LIST response named a file outside the polled directory.



Upgrade to Apache Camel 4.23.0, which fixes the issue. Users on the 4.22.x releases stream should upgrade to 4.22.1. Users on the 4.18.x LTS releases stream should upgrade to 4.18.5. The 4.14.x stream reached end of life and does not receive this fix; users on it should move to a supported releases stream.

### CVE-2026-16460

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-19T07:16:31.253 |

A flaw was found in bootc and ostree. Already-staged deployments are finalized without revalidating the deployment's container image against the current containers signature policy. Unsigned OS content staged under a prior permissive policy can remain bootable after policy is hardened to reject unsigned images, leading to full host compromise on reboot.

### CVE-2026-76740

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-19T07:16:31.900 |

A security vulnerability in HPE Compute Scale-up Server 3200 and 3250 platforms, Superdome Flex and Superdome Flex 280 servers could be exploited remotely to execute arbitrary commands on the RMC.

### CVE-2026-8168

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-19T14:17:08.840 |

Uncontrolled recursion in the SVG parser and renderer of the Qt SVG module (QtSvg) in Qt Group Qt allows attackers to cause a denial of service (application crash via stack exhaustion) via a crafted SVG file with deeply nested elements.

### CVE-2026-112287

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-19T14:17:07.143 |

Krayin CRM before 2.2.7 contains a broken object level authorization vulnerability in EmailController write actions that allows scope-restricted authenticated users to manipulate other users' emails by supplying their numeric IDs. Attackers can call update, destroy, mass-update or mass-destroy endpoints to edit, re-send via is_draft=0, trash or permanently delete emails and disclose their subject, body and linked lead and person data.

### CVE-2026-112286

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-19T14:17:06.990 |

Krayin CRM before 2.2.7 contains an insecure direct object reference vulnerability that allows scope-restricted authenticated users to read other users' quotes by bypassing per-user data scope checks in QuoteController. Attackers can query the quotes search and lead-products endpoints to retrieve quote addresses, totals, contact details, and product pricing belonging to any user or lead.

### CVE-2026-112279

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-19T14:17:05.977 |

rdesktop through 1.9.0 contains a heap out-of-bounds read vulnerability in process_bmpcache2() in orders.c that allows malicious RDP servers to crash clients via crafted revision-2 bitmap cache orders. Attackers can send an uncompressed order with large width/height or an underflowing mode nibble and short payload, causing memcpy() reads past the receive buffer and denial of service.

### CVE-2026-112278

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-19T14:17:05.830 |

rdesktop through 1.9.0 contains a heap out-of-bounds read vulnerability in process_raw_bmpcache() in orders.c that allows malicious RDP servers to crash clients. Attackers can send a raw bitmap cache order declaring large width, height, and bpp values with a tiny payload, causing memcpy() to read past the receive buffer and crash the client.

### CVE-2026-112277

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-19T14:17:05.663 |

rdesktop through 1.9.0 contains a heap out-of-bounds read vulnerability in process_plane() in bitmap.c that allows malicious RDP servers to crash clients by sending malformed 32 bpp compressed bitmaps. Attackers can declare a large bitmap geometry with a short compressed body in bitmap update PDUs or bitmap cache orders, causing unbounded reads past the receive buffer and denial of service.

### CVE-2026-112270

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-19T14:17:04.627 |

SGLang through 0.5.22 with the Mooncake disaggregation backend contains an uncontrolled memory allocation vulnerability in handle_staging_rsp() that lets unauthenticated network-adjacent attackers exhaust Prefill memory. Attackers can obtain the rank address from the /route endpoint and send STAGING_RSP messages with huge chunk_idx values under fresh room IDs, causing the scheduler to be OOM-killed.

### CVE-2026-112269

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-19T14:17:04.467 |

SGLang through 0.5.22 with the Mooncake disaggregation backend accepts unauthenticated decode registration messages on the Prefill rank ZMQ PULL socket, allowing denial of service. Network-adjacent attackers can send many registrations with unique mooncake_session_id values and large nested-buffer frames to exhaust Prefill memory until the scheduler is OOM-killed.

### CVE-2026-112262

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-19T14:17:02.633 |

RisingWave before 3.1.0 contains a missing authorization vulnerability that allows low-privileged SQL users to read and write arbitrary server files by creating posix_fs sources and fs sinks. Attackers holding schema CREATE privilege can set posix_fs.root or fs.path to any directory to read credentials and keys or write files as root.

### CVE-2026-112188

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-285` |
| Published | 2026-10-19T10:16:47.413 |

MISP contains a vulnerability in its server settings lookup mechanism that allows an authenticated user to retrieve sensitive configuration data that should have been redacted.

The settings lookup function resolves a dotted setting name to a node in the configuration tree. When a branch name (such as Security, MISP, or Plugin) is supplied instead of a specific leaf setting, the function returns the entire sub-tree. Because a branch node does not carry a redaction flag, the redaction check in the settings retrieval endpoint is bypassed, and the full branch contents are returned to the caller. This exposes sensitive values including the security salt, Redis connection passwords, and plugin API keys.

A second endpoint that edits server settings similarly reads the entire configuration store when a branch name is resolved, returning all settings to the caller.

The impact is disclosure of sensitive server configuration secrets to any user who can access the server settings endpoints.

Affected versions: <2.5.48.

### CVE-2026-110379

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-19T10:16:45.490 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Ays Pro Quiz Maker quiz-maker allows Reflected XSS.This issue affects Quiz Maker: from n/a through 6.7.1.91.

### CVE-2026-112178

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-19T09:17:08.240 |

MISP contains an access control flaw in the proposal (shadow attribute) visibility logic. The authorization check accepted any attribute or object carrying one of the user's sharing groups without verifying the distribution level, and denied the owning organisation access to proposals on its own organisation-only attributes.

- A user belonging to a sharing group could view proposals on attributes or objects with that sharing group, regardless of the attribute's distribution level (levels 1-3 should restrict visibility)

- The owning organisation could not view proposals on its own org-only attributes

Security impact: Unauthorized disclosure of proposed attribute changes to users who should not have access based on distribution level restrictions.

Affected: <2.5.48

### CVE-2026-111440

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-10-19T04:17:03.657 |

在 openGauss-connector-jdbc 的 pgjdbc/src/main/java/org/postgresql/log/LogFactory.java 中，LogFactory 根据 JDBC 连接参数中的 logger 类名调用 Class.forName 加载类后，直接反射调用以 String 为参数的构造函数，再转换为 Log。缺少 asSubclass(Log.class) 校验，非 Log 实现类也会在类型检查前被实例化。因此，当攻击者可控制 JDBC URL 或连接属性中的 logger 类名，且客户端 classpath 中存在可被加载的类时，可能在客户端触发非预期的类加载与构造副作用。

此漏洞自 JDBC 1.1.0引入，影响 1.1.0 及之后的 2.x、3.x、5.x、6.x 各版本及补丁（含 6.0.0 分支最新 6.0.6），以及 7.0.0-RC1、7.0.0-RC2、7.0.0-RC3，并在 7.0.0-LTS 版本修复。修复在 Class.forName 之后先执行 asSubclass(Log.class)，仅允许 Log 子类进入构造。修复pr见https://gitcode.com/opengauss/openGauss-connector-jdbc/pull/423。
